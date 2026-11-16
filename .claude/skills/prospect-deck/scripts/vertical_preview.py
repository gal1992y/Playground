#!/usr/bin/env python3
"""Render the same deck once per business type, to check that each one looks and reads like its own business.

usage: vertical_preview.py <out dir> [--logo <file>]

For every profile in assets/verticals.json it writes <out>/<vertical>/deck.json from the profile's sample copy
(invented numbers, marked as a fixture), builds it, and prints the commands to render. Use it after changing a
profile, a motif or the CSS, and when adding a new business type.
"""
import json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    out = sys.argv[1]
    logo = sys.argv[sys.argv.index('--logo') + 1] if '--logo' in sys.argv else os.path.join(SKILL, 'examples', 'examplex-logo.svg')
    V = json.load(open(os.path.join(SKILL, 'assets', 'verticals.json')))['verticals']
    for k, v in V.items():
        s = v['sample']
        d = os.path.join(out, k)
        os.makedirs(d, exist_ok=True)
        shutil.copy(logo, os.path.join(d, 'logo.svg'))
        deck = {
            '_comment': 'Fixture for the look of one business type. Every number is invented.',
            'prospect': {'name': 'Examplex', 'logo': 'logo.svg', 'vertical': k}, 'mode': 'proxy', 'date': 'November 2026',
            'buyer': {'company': 'Examplex', 'role': 'Head of CRM', 'language': 'en', 'market': 'Global'},
            'urgency_skipped': 'fixture',
            'slides': [
                {'type': 'cover', 'title': s['title'], 'subtitle': s['subtitle']},
                {'type': 'hero', 'number': s['number'], 'line': s['line'], 'basis': f'{v["venues"].capitalize()} like Examplex, last 90 days.'},
                {'type': 'paths', 'headline': 'Two ways to *act on it*', 'primary': 'enrich',
                 'enrich': {'title': f'Know every {v["person"]} on day one', 'points': s['enrich']},
                 'advertise': {'title': f'Reach proven {v["people"]}', 'points': s['advertise']}},
                {'type': 'next', 'headline': 'See this for *your own market* in 20 minutes', 'ask': 'Book 20 minutes. Nothing needed from you.',
                 'contact': {'name': 'Addressable', 'link': 'addressable.io'}},
            ],
            'claims': [{'text': s['number'], 'value': 0, 'kind': 'query', 'source': 'fixture', 'n_min': 100, 'scope': 'peers'}],
            'template': ['$500', '$5,000', '$50,000', '90 days', '20 minutes', 'Book 20', 'day one', 'two or more', 'Two ways', 'six-figure', 'six figures'],
        }
        p = os.path.join(d, 'deck.json')
        json.dump(deck, open(p, 'w'), indent=1)
        lint = subprocess.run([sys.executable, os.path.join(HERE, 'lint_deck.py'), p], capture_output=True, text=True)
        subprocess.run([sys.executable, os.path.join(HERE, 'build_deck.py'), p], check=True, capture_output=True)
        print(f'{k:<11} {"lint OK" if lint.returncode == 0 else "LINT FAILS:"}')
        if lint.returncode:
            print('   ' + '\n   '.join(l for l in lint.stdout.splitlines() if l.startswith('FAIL')))
    print(f'render each with: node {os.path.join(HERE, "render.js")} {out}/<vertical>/deck.html')


if __name__ == '__main__':
    main()
