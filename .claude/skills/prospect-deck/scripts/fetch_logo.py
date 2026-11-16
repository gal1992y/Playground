#!/usr/bin/env python3
"""Collect logo candidates from the prospect's own website, for the cover lockup and the footer.

usage: fetch_logo.py <domain or URL> --out <dir>

Reads only the prospect's public site (home page, the images it links, /favicon.ico). It writes every candidate to
<dir>/logo-candidates/ and prints a ranked table. It does not choose: look at the top candidates (Read the image
files) and pick the one that is the real, current, full logo. Then set in deck.json:

    "prospect": {"logo": "logo-candidates/<file>", "logo_plate": "light" | "dark"}

logo_plate is the plate the logo sits on: "light" (white) for a dark or coloured logo, "dark" for a white logo.
Rules: never redraw, recolour, stretch or crop a prospect's logo, and never build one from text in their typeface.
If nothing usable comes back, ask the user for the file (brand kits are usually at /press, /brand or /media-kit), or
set "logo_waived" with the reason and the cover sets the name in type. Python standard library only.
"""
import argparse, hashlib, html, os, re, ssl, struct, sys, urllib.parse, urllib.request

UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
CTX = ssl.create_default_context()
for ca in (os.environ.get('SSL_CERT_FILE'), os.environ.get('REQUESTS_CA_BUNDLE'), '/root/.ccr/ca-bundle.crt'):
    if ca and os.path.exists(ca):
        CTX.load_verify_locations(ca)
        break


def get(url, limit=3_000_000):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
    with urllib.request.urlopen(req, timeout=20, context=CTX) as r:
        return r.read(limit), r.headers.get('Content-Type', ''), r.geturl()


def size_of(data, ctype):
    """(kind, width, height) without any imaging library."""
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        w, h = struct.unpack('>II', data[16:24])
        return 'png', w, h
    if data[:3] == b'\xff\xd8\xff':
        i = 2
        while i < len(data) - 9:
            if data[i] != 0xFF:
                i += 1
                continue
            m = data[i + 1]
            if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):
                h, w = struct.unpack('>HH', data[i + 5:i + 9])
                return 'jpg', w, h
            i += 2 + struct.unpack('>H', data[i + 2:i + 4])[0]
        return 'jpg', 0, 0
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return 'webp', 0, 0
    if data[:4] == b'\x00\x00\x01\x00':
        return 'ico', data[6] or 256, data[7] or 256
    head = data[:4000].decode('utf8', 'ignore')
    if '<svg' in head or 'svg' in ctype:
        m = re.search(r'viewBox=["\']\s*[\d.-]+[ ,]+[\d.-]+[ ,]+([\d.]+)[ ,]+([\d.]+)', head)
        return 'svg', (float(m.group(1)) if m else 0), (float(m.group(2)) if m else 0)
    return None, 0, 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('site')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    base = a.site if re.match(r'https?://', a.site) else 'https://' + a.site
    try:
        raw, _, final = get(base)
    except Exception as e:
        sys.exit(f'could not read {base}: {e}\nAsk the user for the logo file, or try the www. host or the brand/press page.')
    page = raw.decode('utf8', 'ignore')
    cands = []                                      # (score, why, url)
    add = lambda score, why, url: url and cands.append((score, why, urllib.parse.urljoin(final, html.unescape(url.strip()))))

    for tag in re.findall(r'<img\b[^>]*>', page, flags=re.I):
        src = re.search(r'\bsrc=["\']([^"\']+)', tag, flags=re.I)
        if not src or src.group(1).startswith('data:'):
            continue
        blob = tag.lower()
        if 'logo' in blob or 'brand' in blob:
            add(90 if '.svg' in blob else 70, 'img tagged logo', src.group(1))
    for m in re.finditer(r'["\'(]([^"\'()\s]*logo[^"\'()\s]*\.(?:svg|png|webp))', page, flags=re.I):
        add(80 if m.group(1).lower().endswith('.svg') else 60, 'file named logo', m.group(1))
    for tag in re.findall(r'<link\b[^>]*>', page, flags=re.I):
        rel = (re.search(r'\brel=["\']([^"\']+)', tag, flags=re.I) or [None, ''])[1].lower()
        href = re.search(r'\bhref=["\']([^"\']+)', tag, flags=re.I)
        if not href:
            continue
        if 'mask-icon' in rel or ('icon' in rel and '.svg' in href.group(1).lower()):
            add(45, 'svg icon (mark only)', href.group(1))
        elif 'apple-touch-icon' in rel:
            add(40, 'app icon (mark only)', href.group(1))
        elif 'icon' in rel:
            add(20, 'favicon (mark only)', href.group(1))
    for prop in ('og:logo', 'og:image', 'twitter:image'):
        m = re.search(r'<meta[^>]+(?:property|name)=["\']%s["\'][^>]+content=["\']([^"\']+)' % prop, page, flags=re.I) \
            or re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\']%s["\']' % prop, page, flags=re.I)
        if m:
            add(75 if prop == 'og:logo' else 15, prop + (' (usually a banner, not a logo)' if 'image' in prop else ''), m.group(1))
    add(10, 'favicon.ico (mark only)', '/favicon.ico')

    out = os.path.join(a.out, 'logo-candidates')
    os.makedirs(out, exist_ok=True)
    seen, rows = set(), []
    for score, why, url in sorted(cands, key=lambda c: -c[0]):
        if url in seen or len(rows) >= 12:
            continue
        seen.add(url)
        try:
            data, ctype, _ = get(url)
        except Exception:
            continue
        kind, w, h = size_of(data, ctype)
        if not kind or len(data) < 200:
            continue
        digest = hashlib.sha1(data).hexdigest()[:8]
        if digest in seen:
            continue
        seen.add(digest)
        if kind in ('png', 'jpg') and w and max(w, h) < 120:
            score -= 25                                              # too small to print
        if w and h and w / h > 1.6 and 'banner' not in why:
            score += 10                                              # wide = wordmark, what a lockup wants
        fn = f'{len(rows) + 1:02d}-{digest}.{kind}'
        open(os.path.join(out, fn), 'wb').write(data)
        rows.append((score, fn, kind, f'{int(w)}x{int(h)}' if w else '?', why))
    if not rows:
        sys.exit('no logo candidates found. Ask the user for the file (brand kit pages: /press, /brand, /media-kit).')
    print(f'{len(rows)} candidates in {out} (best guess first). Look at them before choosing:')
    for score, fn, kind, dim, why in sorted(rows, key=lambda r: -r[0]):
        print(f'  {score:>3}  {fn:<22} {dim:<10} {why}')
    print('SVG beats PNG; a full wordmark beats a mark-only icon; webp and ico need converting to PNG before use.')


if __name__ == '__main__':
    main()
