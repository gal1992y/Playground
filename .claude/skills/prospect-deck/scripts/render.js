#!/usr/bin/env node
/* deck.html -> deck.pdf (one 1280x720 page per slide) + png/slide-NN.png (2x) + og.png (cover, 1200x675 link preview).

   usage: node render.js <deck.html> [--no-png]

   Needs Playwright with Chromium. It is looked up as `playwright`, then `@playwright/test`, in the usual Node
   paths and next to this script. Set CHROMIUM_PATH to use an installed Chrome or Chromium instead of
   Playwright's own (on a Mac: /Applications/Google Chrome.app/Contents/MacOS/Google Chrome). */
const fs = require('fs');
const path = require('path');

function loadPlaywright() {
  const extra = [process.cwd(), __dirname, '/opt/node-tools', path.join(process.env.HOME || '', '.claude')];
  for (const name of ['playwright', '@playwright/test', 'playwright-core']) {
    try { return require(name); } catch (e) { /* next */ }
    for (const base of extra) {
      try { return require(require.resolve(name, { paths: [base] })); } catch (e) { /* next */ }
    }
  }
  console.error('Playwright not found. Install it once:  npm i -g playwright && npx playwright install chromium\n' +
    'or set NODE_PATH to a folder that has it. With an installed Chrome, also set CHROMIUM_PATH.');
  process.exit(2);
}

(async () => {
  const file = process.argv[2];
  if (!file || !fs.existsSync(file)) { console.error('usage: node render.js <deck.html> [--no-png]'); process.exit(2); }
  const noPng = process.argv.includes('--no-png');
  const abs = path.resolve(file);
  const dir = path.dirname(abs);
  const { chromium } = loadPlaywright();
  const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  await page.goto('file://' + abs);
  await page.evaluate(() => document.fonts.ready);

  // overflow check: anything that spills outside its slide is a build error, not a style choice
  const spills = await page.evaluate(() => [...document.querySelectorAll('.frame')].map((f, i) => {
    const s = f.firstElementChild, r = s.getBoundingClientRect(), bad = [];
    const scale = r.width / 1280;
    for (const el of s.querySelectorAll('h1,h2,.grow,.cards,.events,.paths,.bars,.foot,.contact,.meta,.lockup,.card,.event,.path')) {
      const b = el.getBoundingClientRect();
      if (b.bottom > r.bottom + 1 || b.right > r.right + 1 || b.left < r.left - 1 || b.top < r.top - 1) bad.push(el.className || el.tagName);
    }
    const g = s.querySelector('.grow');
    if (g && g.scrollHeight > g.clientHeight + 2) bad.push('content taller than the slide by ' + Math.round((g.scrollHeight - g.clientHeight) / scale) + 'px');
    return bad.length ? `slide ${i + 1}: ${[...new Set(bad)].join(', ')}` : null;
  }).filter(Boolean));

  if (!noPng) {
    const out = path.join(dir, 'png');
    fs.mkdirSync(out, { recursive: true });
    for (const f of fs.readdirSync(out)) if (/^slide-\d+\.png$/.test(f)) fs.unlinkSync(path.join(out, f));
    const frames = await page.$$('.frame');
    for (let i = 0; i < frames.length; i++) {
      await frames[i].scrollIntoViewIfNeeded();
      await frames[i].screenshot({ path: path.join(out, `slide-${String(i + 1).padStart(2, '0')}.png`) });
    }
    const og = await browser.newContext({ viewport: { width: 1200, height: 675 }, deviceScaleFactor: 1 });
    const p2 = await og.newPage();
    await p2.goto('file://' + abs);
    await p2.evaluate(() => document.fonts.ready);
    await p2.addStyleTag({ content: '.deck{padding:0!important}.frame{border-radius:0!important;width:1200px!important}' });
    await p2.evaluate(() => window.dispatchEvent(new Event('resize')));
    await (await p2.$('.frame')).screenshot({ path: path.join(dir, 'og.png') });
    await og.close();
    console.log(`wrote ${frames.length} PNGs to ${out} and og.png`);
  }

  await page.emulateMedia({ media: 'print' });
  await page.evaluate(() => document.querySelectorAll('.slide').forEach((s) => { s.style.transform = 'none'; }));
  const pdf = path.join(dir, 'deck.pdf');
  await page.pdf({ path: pdf, width: '1280px', height: '720px', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  console.log('wrote ' + pdf);
  await browser.close();
  if (spills.length) {
    console.error('OVERFLOW (cut the text; do not shrink the type):\n  ' + spills.join('\n  '));
    process.exit(1);
  }
})().catch((e) => { console.error(e); process.exit(1); });
