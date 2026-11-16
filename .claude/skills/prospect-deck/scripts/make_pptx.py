#!/usr/bin/env python3
"""png/slide-NN.png + deck.json -> deck.pptx, for presenting live: one full-bleed picture per slide, the talk track
(`notes` in deck.json) as speaker notes, and the slide's text as the picture's alt text.

usage: make_pptx.py <deck.json> [--out <dir>]     (run build_deck.py and render.js first)

The slides are pictures on purpose: the deck looks the same in PowerPoint, Keynote and Google Slides, and nobody
edits a number away from its source. To change a word, change deck.json and rebuild. Needs python-pptx.
"""
import argparse, glob, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deckspec  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('deck')
    ap.add_argument('--out')
    a = ap.parse_args()
    try:
        from pptx import Presentation
        from pptx.util import Emu
    except ImportError:
        sys.exit('python-pptx is missing: pip install python-pptx')
    d = deckspec.load(a.deck)
    out = a.out or d['_dir']
    pngs = sorted(glob.glob(os.path.join(out, 'png', 'slide-*.png')))
    if len(pngs) != len(d['slides']):
        sys.exit(f'{len(pngs)} PNGs for {len(d["slides"])} slides: run build_deck.py and render.js again')
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)       # 16:9
    blank = prs.slide_layouts[6]
    for s, png in zip(d['slides'], pngs):
        sl = prs.slides.add_slide(blank)
        pic = sl.shapes.add_picture(png, 0, 0, prs.slide_width, prs.slide_height)
        head, body = deckspec.slide_text(s)
        pic._element.xpath('.//p:cNvPr')[0].set('descr', ' | '.join(x for x in [head] + body if x)[:1800])
        if s.get('notes'):
            sl.notes_slide.notes_text_frame.text = s['notes']
    prs.core_properties.title = deckspec.plain(next((s.get('title') for s in d['slides'] if s.get('type') == 'cover'), '') or 'Addressable')
    prs.core_properties.author = 'Addressable'
    p = os.path.join(out, 'deck.pptx')
    prs.save(p)
    print('wrote', p)


if __name__ == '__main__':
    main()
