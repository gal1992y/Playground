#!/usr/bin/env python3
"""deck.json -> one self-contained deck.html (fonts, logos and styles inside the file).

usage: build_deck.py <deck.json> [--out <dir>]        (default: the deck.json's folder)

The HTML is the single source for every format: open it in a browser to present or publish it, and run render.js
on it for the PDF and the per-slide PNGs. Python standard library only.
"""
import argparse, base64, html, mimetypes, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deckspec  # noqa: E402

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(SKILL, 'assets')
esc = lambda s: html.escape(str(s if s is not None else ''), quote=True)


def rich(s):
    """Escape, then turn *phrase* into the gradient-emphasised phrase."""
    return re.sub(r'\*([^*]+)\*', r'<em>\1</em>', esc(s))


def data_uri(path):
    mime = mimetypes.guess_type(path)[0] or ('image/svg+xml' if path.endswith('.svg') else 'application/octet-stream')
    with open(path, 'rb') as f:
        return f'data:{mime};base64,' + base64.b64encode(f.read()).decode()


def font_css():
    import json
    out = []
    for f in json.load(open(os.path.join(ASSETS, 'fonts', 'fonts.json'))):
        out.append("@font-face{font-family:'%s';font-style:normal;font-weight:%s;font-display:swap;"
                   "src:url(%s) format('woff2');unicode-range:%s}" % (
                       f['family'], f['weight'], data_uri(os.path.join(ASSETS, 'fonts', f['file'])), f['range']))
    return '\n'.join(out)


CSS = r"""
:root{--navy:#002333;--purple:#C552FF;--purple-dark:#AA00FF;--pink:#EC006A;--gold:#FEC600;--muted:#595959;--soft:#808080;
--line:#E0E0E0;--bg:#F7F7F7;--tint:#FDF9FF;--grad:linear-gradient(100deg,#AA00FF 0%,#EC006A 55%,#FEC600 100%);
--head:'Outfit','Noto Sans','Noto Sans Hebrew','Noto Sans Arabic','Noto Sans CJK SC',system-ui,sans-serif;
--body:'Inter','Noto Sans','Noto Sans Hebrew','Noto Sans Arabic','Noto Sans CJK SC',system-ui,sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
html{background:#0b1a22}
body{font-family:var(--body);color:var(--navy);-webkit-font-smoothing:antialiased}
.deck{display:flex;flex-direction:column;align-items:center;gap:28px;padding:28px 0}
.frame{width:min(100vw,1280px);aspect-ratio:16/9;position:relative;overflow:hidden;border-radius:10px;box-shadow:0 10px 40px rgba(0,0,0,.35)}
.slide{width:1280px;height:720px;position:absolute;top:0;left:0;transform-origin:top left;background:#fff;overflow:hidden;
display:flex;flex-direction:column;padding:64px 80px 0}
.slide::before{content:'';position:absolute;top:0;left:0;right:0;height:6px;background:var(--grad)}
h1,h2,.num,.kicker,.big{font-family:var(--head)}
em{font-style:normal;background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:var(--pink)}
.kicker{font-size:15px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--accent,#AA00FF);margin-bottom:18px}
.motif{position:absolute;inset-inline-end:64px;top:46%;transform:translateY(-50%);width:400px;height:400px;color:var(--accent,#AA00FF);opacity:.2;pointer-events:none}
.slide.dark>.motif{position:absolute;z-index:0;color:#fff;opacity:.13;inset-inline-end:36px;width:400px;height:400px}
.slide>.grow,.slide>.foot{position:relative;z-index:1}
h2{font-size:50px;line-height:1.08;font-weight:700;letter-spacing:-.01em;max-width:1000px;text-wrap:balance}
.grow{flex:1;display:flex;flex-direction:column;justify-content:center;min-height:0}
.foot{height:64px;flex:none;display:flex;align-items:center;justify-content:space-between;gap:24px;border-top:1px solid var(--line);
font-size:12.5px;color:var(--soft);margin-top:auto}
.foot img.ab{height:19px}
.foot .mid{flex:1;text-align:center}
.foot .who{display:flex;align-items:center;gap:10px}
.foot .who img{height:22px;max-width:110px;object-fit:contain}
.foot .who .plate{padding:4px 8px;border-radius:6px}
.plate.dark{background:var(--navy)}.plate.light{background:#fff}
.basis{font-size:14px;color:var(--soft);margin-top:22px}

/* cover and next: navy */
.slide.dark{background:var(--navy);color:#fff;padding:64px 80px}
.slide.dark::after{content:'';position:absolute;inset:0;pointer-events:none;
background:radial-gradient(620px 420px at 92% 8%,color-mix(in srgb,var(--accent,#AA00FF) 46%,transparent),transparent 70%),radial-gradient(560px 400px at 100% 100%,rgba(236,0,106,.30),transparent 70%),radial-gradient(420px 300px at 62% 112%,rgba(254,198,0,.16),transparent 70%)}
.slide.dark>*{position:relative;z-index:1}
.lockup{display:flex;align-items:center;gap:26px}
.lockup img.ab{height:34px}
.lockup .x{font-family:var(--head);font-weight:300;font-size:30px;color:rgba(255,255,255,.55)}
.lockup .plate{height:64px;min-width:64px;padding:12px 20px;border-radius:14px;display:flex;align-items:center;justify-content:center}
.lockup .plate.dark{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18)}
.lockup .plate img{height:40px;max-width:230px;object-fit:contain;display:block}
.lockup .plate span{font-family:var(--head);font-weight:700;font-size:26px;color:var(--navy)}
.lockup .plate.dark span{color:#fff}
.cover h1{font-size:74px;line-height:1.04;font-weight:800;letter-spacing:-.02em;max-width:780px;text-wrap:balance}
.cover .sub{font-size:25px;line-height:1.4;color:rgba(255,255,255,.78);margin-top:26px;max-width:700px}
.cover .meta{font-size:15px;color:rgba(255,255,255,.6);letter-spacing:.04em}
.dark em{background:linear-gradient(100deg,#D47FFF 0%,#FF5C9D 55%,#FEC600 100%);-webkit-background-clip:text;background-clip:text}

/* why now */
.events{display:flex;gap:22px;margin-top:40px}
.event{flex:1;background:var(--bg);border-radius:16px;padding:24px 26px;border-top:4px solid var(--accent,#EC006A)}
.event .d{font-family:var(--head);font-weight:700;font-size:15px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent,#EC006A)}
.event .t{font-family:var(--head);font-weight:600;font-size:25px;line-height:1.22;margin-top:10px}
.event .s{font-size:13px;color:var(--soft);margin-top:12px}
.effect{margin-top:30px;font-size:24px;line-height:1.4;color:var(--navy);padding-inline-start:20px;border-inline-start:4px solid transparent;border-image:linear-gradient(180deg,#AA00FF,#EC006A) 1;max-width:1000px}

/* hero */
.hero .big{font-size:210px;line-height:.92;font-weight:800;letter-spacing:-.04em;background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:var(--pink);display:inline-block;padding-inline-end:.06em}
.hero .unit{font-family:var(--head);font-size:34px;font-weight:600;color:var(--navy);margin-inline-start:14px}
.hero .line{font-family:var(--head);font-size:40px;line-height:1.18;font-weight:600;margin-top:22px;max-width:700px;text-wrap:balance}

/* highlights */
.cards{display:flex;gap:24px;margin-top:40px}
.card{flex:1;border-radius:18px;padding:32px 30px;background:#fff;border:1px solid var(--line);box-shadow:0 1px 3px rgba(0,0,0,.05),0 6px 22px rgba(0,35,51,.07);position:relative;overflow:hidden}
.card::before{content:'';position:absolute;inset:0 0 auto 0;height:5px;background:var(--grad)}
.card .num{font-size:66px;line-height:1;font-weight:800;letter-spacing:-.02em;color:var(--navy)}
.card .lab{font-family:var(--head);font-size:23px;font-weight:600;line-height:1.25;margin-top:16px}
.card .det{font-size:16.5px;line-height:1.45;color:var(--muted);margin-top:10px}

/* compare */
.bars{margin-top:40px;display:flex;flex-direction:column;gap:20px}
.bar{display:grid;grid-template-columns:260px 1fr 150px;align-items:center;gap:22px}
.bar .l{font-family:var(--head);font-size:22px;font-weight:600}
.bar .track{height:38px;background:var(--bg);border-radius:10px;overflow:hidden}
.bar .fill{height:100%;border-radius:10px;background:#D9DDE0;min-width:8px}
.bar.accent .fill{background:var(--grad)}
.bar .v{font-family:var(--head);font-size:30px;font-weight:700;text-align:end}
.bar.accent .v{color:var(--pink)}

/* statement */
.statement h2{font-size:62px;max-width:1040px}
.statement .sub{font-size:25px;line-height:1.4;color:var(--muted);margin-top:24px;max-width:860px}

/* paths */
.paths{display:flex;gap:26px;margin-top:36px}
.path{flex:1;border-radius:20px;padding:32px 34px;border:1.5px solid var(--line);background:#fff;position:relative}
.path.primary{border:0;background:var(--navy);color:#fff;box-shadow:0 14px 40px rgba(0,35,51,.28)}
.path .tag{position:absolute;top:-14px;inset-inline-start:30px;background:var(--grad);color:#fff;font-family:var(--head);font-weight:700;font-size:13px;letter-spacing:.1em;text-transform:uppercase;padding:6px 14px;border-radius:999px}
.path .name{font-family:var(--head);font-size:15px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--accent,#AA00FF)}
.path.primary .name{color:#E7B9FF}
.path .ttl{font-family:var(--head);font-size:31px;font-weight:700;line-height:1.15;margin-top:10px}
.path .ln{font-size:17px;line-height:1.45;color:var(--muted);margin-top:10px}
.path.primary .ln{color:rgba(255,255,255,.75)}
.path ul{list-style:none;margin-top:18px;display:flex;flex-direction:column;gap:10px}
.path li{font-family:var(--head);font-size:20px;font-weight:500;display:flex;gap:12px;align-items:center}
.path li::before{content:'';width:9px;height:9px;border-radius:50%;background:var(--grad);flex:none}

/* next */
.next h1{font-size:64px;line-height:1.06;font-weight:800;letter-spacing:-.02em;max-width:780px;text-wrap:balance}
.next .ask{display:inline-block;margin-top:34px;background:var(--grad);color:#fff;font-family:var(--head);font-weight:700;font-size:27px;padding:20px 34px;border-radius:14px;text-decoration:none;max-width:1000px}
.next .contact{font-size:19px;line-height:1.6;color:rgba(255,255,255,.82)}
.next .contact b{font-family:var(--head);font-weight:600;color:#fff;font-size:22px}
.next .contact a{color:#E7B9FF;text-decoration:none}

/* method */
.method h2{font-size:34px}
.method ul{margin-top:22px;padding-inline-start:22px;display:flex;flex-direction:column;gap:9px;font-size:16.5px;line-height:1.45;color:var(--muted);max-width:1040px}
.method .src{margin-top:20px;font-size:13.5px;line-height:1.6;color:var(--soft)}
.method .src b{color:var(--muted);font-family:var(--head);letter-spacing:.08em;text-transform:uppercase;font-size:12px}
.method .src a{color:var(--purple-dark);text-decoration:none}

@page{size:1280px 720px;margin:0}
@media print{
 html{background:#fff}.deck{display:block;padding:0;gap:0}
 .frame{width:1280px;height:720px;aspect-ratio:auto;border-radius:0;box-shadow:none;break-after:page;page-break-after:always}
 .slide{transform:none!important;position:relative}
 *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
"""

JS = r"""
(function(){var fr=[].slice.call(document.querySelectorAll('.frame'));
function fit(){if(window.matchMedia('print').matches)return;fr.forEach(function(f){f.firstElementChild.style.transform='scale('+(f.clientWidth/1280)+')'})}
fit();addEventListener('resize',fit);addEventListener('beforeprint',function(){fr.forEach(function(f){f.firstElementChild.style.transform='none'})});addEventListener('afterprint',fit);
addEventListener('keydown',function(e){var d=({ArrowRight:1,ArrowDown:1,PageDown:1,' ':1,ArrowLeft:-1,ArrowUp:-1,PageUp:-1})[e.key];if(!d)return;
var y=scrollY+innerHeight/2,i=0;fr.forEach(function(f,k){if(f.offsetTop<=y)i=k});var t=fr[Math.max(0,Math.min(fr.length-1,i+d))];
if(t){e.preventDefault();t.scrollIntoView({behavior:'smooth',block:'center'})}})})();
"""


def _motif(kind):
    """Line drawing for the business type, 520x520, drawn in currentColor. Decoration only: it carries no data."""
    P = []
    a = P.append
    if kind == 'chips':
        for cx, cy, r in ((330, 170, 120), (170, 330, 92), (390, 390, 64)):
            a(f'<circle cx="{cx}" cy="{cy}" r="{r}"/><circle cx="{cx}" cy="{cy}" r="{r * .72:.0f}" stroke-dasharray="{r * .22:.0f} {r * .16:.0f}"/>'
              f'<circle cx="{cx}" cy="{cy}" r="{r * .34:.0f}"/>')
    elif kind == 'pitch':
        a('<rect x="40" y="110" width="440" height="300" rx="6"/><line x1="260" y1="110" x2="260" y2="410"/><circle cx="260" cy="260" r="58"/>'
          '<circle cx="260" cy="260" r="4" fill="currentColor"/><rect x="40" y="185" width="78" height="150"/><rect x="40" y="225" width="30" height="70"/>'
          '<rect x="402" y="185" width="78" height="150"/><rect x="450" y="225" width="30" height="70"/>'
          '<path d="M118 232a44 44 0 0 1 0 56M402 232a44 44 0 0 0 0 56"/>')
    elif kind == 'odds':
        a('<line x1="40" y1="260" x2="480" y2="260" stroke-dasharray="6 10"/>'
          '<path d="M40 330H110V300H170V345H230V250H290V205H350V225H410V140H480" stroke-width="5"/>'
          '<rect x="40" y="430" width="286" height="34" rx="8" fill="currentColor" stroke="none"/><rect x="336" y="430" width="144" height="34" rx="8"/>'
          '<circle cx="480" cy="140" r="9" fill="currentColor"/>')
    elif kind == 'candles':
        for i, (lo, hi, o, c) in enumerate(((330, 210, 310, 240), (300, 180, 240, 280), (340, 230, 280, 320), (360, 250, 320, 270),
                                            (300, 160, 270, 190), (240, 130, 190, 220), (260, 110, 220, 140), (190, 60, 140, 90), (150, 50, 90, 120))):
            x = 52 + i * 50
            top, h = min(o, c), abs(o - c)
            fill = ' fill="currentColor"' if c < o else ''
            a(f'<line x1="{x}" y1="{hi + 110}" x2="{x}" y2="{lo + 110}"/><rect x="{x - 13}" y="{top + 110}" width="26" height="{h}" rx="3"{fill}/>')
    elif kind == 'depth':
        a('<path d="M40 150H100V200H150V260H200V330H250V420" stroke-width="5"/><path d="M480 130H420V190H370V250H320V320H270V420" stroke-width="5"/>'
          '<line x1="40" y1="420" x2="480" y2="420"/><line x1="260" y1="90" x2="260" y2="440" stroke-dasharray="6 10"/>')
    elif kind == 'waves':
        import math
        for ph, amp, w in ((0, 70, 5), (2.2, 46, 3)):
            pts = ' '.join(f'{40 + i * 8},{260 - amp * math.sin(i / 9 + ph) - i * .35:.1f}' for i in range(56))
            a(f'<polyline points="{pts}" stroke-width="{w}"/>')
        for i in range(12):
            a(f'<line x1="{40 + i * 40}" y1="424" x2="{40 + i * 40}" y2="{410 if i % 3 else 396}"/>')
        a('<line x1="40" y1="424" x2="480" y2="424"/>')
    else:
        n = ((90, 150), (250, 90), (410, 170), (160, 310), (330, 300), (240, 440), (440, 400))
        for i, j in ((0, 1), (1, 2), (0, 3), (1, 4), (2, 4), (3, 4), (3, 5), (4, 5), (4, 6), (2, 6)):
            a(f'<line x1="{n[i][0]}" y1="{n[i][1]}" x2="{n[j][0]}" y2="{n[j][1]}"/>')
        for k, (x, y) in enumerate(n):
            a(f'<circle cx="{x}" cy="{y}" r="{18 if k == 4 else 11}" fill="currentColor"/>')
    return ('<svg class="motif" viewBox="0 0 520 520" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true">' + ''.join(P) + '</svg>')


class Builder:
    def __init__(self, d):
        self.d, self.L = d, d['labels']
        p = d['prospect']
        self.name = p.get('name') or 'Prospect'
        self.ab_color = data_uri(os.path.join(ASSETS, 'logo-color.svg'))
        self.ab_neg = data_uri(os.path.join(ASSETS, 'logo-negative.svg'))
        self.plate = 'dark' if p.get('logo_plate') == 'dark' else 'light'
        logo = p.get('logo')
        self.show_logo = bool(logo) and not (d['audience'] == 'public' and not p.get('logo_permission'))
        self.logo = None
        if self.show_logo:
            path = logo if os.path.isabs(logo) else os.path.join(d['_dir'], logo)
            if not os.path.exists(path):
                sys.exit(f'prospect logo not found: {path}')
            self.logo = data_uri(path)
        self.named = d['audience'] != 'public' or p.get('logo_permission')
        self.v = d['_v']
        self.motif = _motif(self.v.get('motif'))

    def plate_html(self):
        inner = f'<img src="{self.logo}" alt="{esc(self.name)}">' if self.logo else f'<span>{esc(self.name)}</span>'
        return f'<div class="plate {self.plate}">{inner}</div>'

    def lockup(self):
        if not self.named:
            return f'<div class="lockup"><img class="ab" src="{self.ab_neg}" alt="Addressable"></div>'
        return (f'<div class="lockup"><img class="ab" src="{self.ab_neg}" alt="Addressable"><span class="x">&times;</span>'
                f'{self.plate_html()}</div>')

    def foot(self, n):
        mid = ''
        if self.d['audience'] != 'public':
            mid = f"{esc(self.L['confidential'])} &middot; {esc(self.L['prepared_for'])} {esc(self.name)}"
        who = ''
        if self.named and self.logo:
            who = f'<span class="plate {self.plate}"><img src="{self.logo}" alt="{esc(self.name)}"></span>'
        return (f'<div class="foot"><img class="ab" src="{self.ab_color}" alt="Addressable"><span class="mid">{mid}</span>'
                f'<span class="who">{who}<span>{n}</span></span></div>')

    def basis(self, s):
        return f'<div class="basis">{esc(s["basis"])}</div>' if s.get('basis') else ''

    def kicker(self, s, key):
        return f'<div class="kicker">{esc(s.get("kicker") or self.L[key])}</div>'

    # ---- slide types
    def cover(self, s, n):
        meta = ' &middot; '.join(x for x in [
            (f"{esc(self.L['prepared_for'])} {esc(self.name)}" if self.named else ''), esc(self.d.get('date', ''))] if x)
        sub = f'<div class="sub">{rich(s.get("subtitle"))}</div>' if s.get('subtitle') else ''
        return (f'<section class="slide dark cover">{self.motif}{self.lockup()}<div class="grow"><h1>{rich(s.get("title"))}</h1>{sub}</div>'
                f'<div class="meta">{meta}</div></section>')

    def why_now(self, s, n):
        ev = ''.join(f'<div class="event"><div class="d">{esc(e.get("date"))}</div><div class="t">{rich(e.get("text"))}</div>'
                     f'<div class="s">{esc(e.get("source"))}</div></div>' for e in s.get('events', []))
        eff = f'<div class="effect">{rich(s["effect"])}</div>' if s.get('effect') else ''
        return (f'<section class="slide why"><div class="grow">{self.kicker(s, "why_now")}<h2>{rich(s.get("headline"))}</h2>'
                f'<div class="events">{ev}</div>{eff}{self.basis(s)}</div>{self.foot(n)}</section>')

    def hero(self, s, n):
        unit = f'<span class="unit">{esc(s["unit"])}</span>' if s.get('unit') else ''
        return (f'<section class="slide hero">{self.motif}<div class="grow">{self.kicker(s, "what_we_see")}'
                f'<div><span class="big">{esc(s.get("number"))}</span>{unit}</div>'
                f'<div class="line">{rich(s.get("line") or s.get("headline"))}</div>{self.basis(s)}</div>{self.foot(n)}</section>')

    def highlights(self, s, n):
        cards = ''.join(f'<div class="card"><div class="num">{esc(i.get("number"))}</div><div class="lab">{rich(i.get("label"))}</div>'
                        + (f'<div class="det">{rich(i["detail"])}</div>' if i.get('detail') else '') + '</div>'
                        for i in s.get('items', []))
        return (f'<section class="slide hl"><div class="grow">{self.kicker(s, "highlights")}<h2>{rich(s.get("headline"))}</h2>'
                f'<div class="cards">{cards}</div>{self.basis(s)}</div>{self.foot(n)}</section>')

    def compare(self, s, n):
        rows = ''.join(f'<div class="bar{" accent" if r.get("accent") else ""}"><div class="l">{esc(r.get("label"))}</div>'
                       f'<div class="track"><div class="fill" style="width:{max(0, min(100, float(r.get("pct", 0)))):.1f}%"></div></div>'
                       f'<div class="v">{esc(r.get("value"))}</div></div>' for r in s.get('rows', []))
        return (f'<section class="slide cmp"><div class="grow">{self.kicker(s, "compare")}<h2>{rich(s.get("headline"))}</h2>'
                f'<div class="bars">{rows}</div>{self.basis(s)}</div>{self.foot(n)}</section>')

    def statement(self, s, n):
        k = f'<div class="kicker">{esc(s["kicker"])}</div>' if s.get('kicker') else ''
        sub = f'<div class="sub">{rich(s["sub"])}</div>' if s.get('sub') else ''
        return (f'<section class="slide statement"><div class="grow">{k}<h2>{rich(s.get("headline"))}</h2>{sub}{self.basis(s)}</div>'
                f'{self.foot(n)}</section>')

    def paths(self, s, n):
        out = ''
        order = ['advertise', 'enrich'] if s.get('primary') != 'enrich' else ['enrich', 'advertise']
        for k in order:
            p = s.get(k) or {}
            prim = s.get('primary') == k
            pts = ''.join(f'<li>{rich(x)}</li>' for x in p.get('points') or [])
            out += (f'<div class="path{" primary" if prim else ""}">'
                    + (f'<div class="tag">{esc(self.L["start_here"])}</div>' if prim else '')
                    + f'<div class="name">{esc(self.L[k])}</div><div class="ttl">{rich(p.get("title"))}</div>'
                    + (f'<div class="ln">{rich(p["line"])}</div>' if p.get('line') else '') + f'<ul>{pts}</ul></div>')
        return (f'<section class="slide"><div class="grow">{self.kicker(s, "paths")}<h2>{rich(s.get("headline"))}</h2>'
                f'<div class="paths">{out}</div></div>{self.foot(n)}</section>')

    def next(self, s, n):
        c = s.get('contact') or {}
        link = c.get('link') or ''
        href = link if re.match(r'https?://', link) else ('https://' + link if link else '')
        ask = (f'<a class="ask" href="{esc(href)}">{rich(s.get("ask"))}</a>' if href else f'<div class="ask">{rich(s.get("ask"))}</div>')
        bits = []
        if c.get('name'):
            bits.append(f'<b>{esc(c["name"])}</b>' + (f' &middot; {esc(c["role"])}' if c.get('role') else ''))
        if c.get('email'):
            bits.append(f'<a href="mailto:{esc(c["email"])}">{esc(c["email"])}</a>')
        if link:
            bits.append(f'<a href="{esc(href)}">{esc(re.sub(r"^https?://", "", link))}</a>')
        return (f'<section class="slide dark next">{self.motif}{self.lockup()}<div class="grow">'
                f'<div class="kicker" style="color:#E7B9FF">{esc(s.get("kicker") or self.L["next"])}</div>'
                f'<h1>{rich(s.get("headline"))}</h1><div>{ask}</div></div><div class="contact">{"<br>".join(bits)}</div></section>')

    def method(self, s, n):
        pts = ''.join(f'<li>{rich(x)}</li>' for x in s.get('points') or [])
        srcs = ' &middot; '.join((f'<a href="{esc(x["url"])}">{esc(x.get("name") or x["url"])}</a>' if x.get('url') else esc(x.get('name')))
                                 for x in s.get('sources', []))
        src = f'<div class="src"><b>{esc(self.L["sources"])}</b><br>{srcs}</div>' if srcs else ''
        return (f'<section class="slide method"><div class="grow">{self.kicker(s, "method")}'
                + (f'<h2>{rich(s["headline"])}</h2>' if s.get('headline') else '')
                + f'<ul>{pts}</ul>{src}</div>{self.foot(n)}</section>')

    def html(self):
        d = self.d
        frames = []
        for n, s in enumerate(d['slides'], 1):
            t = s.get('type')
            if t not in deckspec.SLIDE_TYPES:
                sys.exit(f'slide {n}: unknown type {t!r} (allowed: {", ".join(deckspec.SLIDE_TYPES)})')
            frames.append(f'<div class="frame v-{d["_vkey"]}" id="s{n}" data-type="{t}" style="--accent:{esc(self.v.get("accent", "#AA00FF"))}">'
                          f'{getattr(self, t)(s, n)}</div>')
        cover = next((s for s in d['slides'] if s.get('type') == 'cover'), {})
        title = deckspec.plain(cover.get('title') or f'Addressable for {self.name}')
        desc = deckspec.plain(cover.get('subtitle') or '')
        robots = '' if d['audience'] == 'public' else '<meta name="robots" content="noindex,nofollow">'
        return (f'<!doctype html><html lang="{esc(d["lang"])}" dir="{esc(d["dir"])}"><head><meta charset="utf-8">'
                f'<meta name="viewport" content="width=device-width,initial-scale=1">{robots}'
                f'<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">'
                f'<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">'
                f'<meta property="og:type" content="article"><meta property="og:image" content="og.png">'
                f'<style>{font_css()}{CSS}</style></head><body><main class="deck">{"".join(frames)}</main>'
                f'<script>{JS}</script></body></html>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('deck')
    ap.add_argument('--out')
    a = ap.parse_args()
    d = deckspec.load(a.deck)
    out = a.out or d['_dir']
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, 'deck.html')
    with open(p, 'w', encoding='utf8') as f:
        f.write(Builder(d).html())
    print(f'wrote {p} ({len(d["slides"])} slides, {os.path.getsize(p) // 1024} KB)')


if __name__ == '__main__':
    main()
