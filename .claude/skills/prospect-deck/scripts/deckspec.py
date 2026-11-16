"""Shared by build_deck.py and lint_deck.py: the deck.json shape, the text budgets, and the visible text of each slide.

The budgets are the point of this skill. A prospect gives a cold deck a few seconds per slide, so every slide carries
one idea, and the lint fails a deck that says more. Change a budget here, not by working around the lint.
"""
import json, os, re

SLIDE_TYPES = ('cover', 'why_now', 'hero', 'highlights', 'compare', 'statement', 'paths', 'next', 'method')
DATA_TYPES = ('hero', 'highlights', 'compare')          # slides that state numbers from our data

BUDGET = {
    'slides': 8,            # story slides; the optional method slide is not counted
    'headline_words': 10,
    'body_words': 35,       # everything on a slide except its headline and the footer
    'paths_words': 48,      # the two-path slide carries two cards
    'method_words': 90,
    'deck_words': 230,      # all story slides together
    'highlights': 3,
    'events': 3,
    'compare_rows': 5,
    'path_points': 3,
    'path_point_words': 6,
    'ask_words': 14,
}

LABELS = {                   # every fixed string the builder prints; override per language in deck.json "labels"
    'prepared_for': 'Prepared for',
    'why_now': 'Why now',
    'what_we_see': 'What we see',
    'highlights': 'Highlights',
    'compare': 'The gap',
    'paths': 'What to do with it',
    'next': 'Next step',
    'method': 'Method and sources',
    'advertise': 'Advertise',
    'enrich': 'Enrich',
    'start_here': 'Start here',
    'confidential': 'Confidential',
    'sources': 'Sources',
}

RTL_LANGS = {'he', 'ar', 'fa', 'ur'}
_VJ = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'verticals.json')


def vertical(name):
    """(key, profile) for a business type. Unknown or missing types fall back to 'default'."""
    with open(_VJ, encoding='utf8') as f:
        j = json.load(f)
    k = re.sub(r'[^a-z_]', '', str(name or '').strip().lower().replace(' ', '_').replace('-', '_'))
    k = j['aliases'].get(k, k)
    if k not in j['verticals']:
        k = 'default'
    return k, j['verticals'][k]


def load(path):
    with open(path, encoding='utf8') as f:
        d = json.load(f)
    d.setdefault('slides', [])
    d.setdefault('claims', [])
    d.setdefault('events', [])
    d.setdefault('template', [])
    d.setdefault('prospect', {})
    d.setdefault('buyer', {})
    d.setdefault('mode', 'direct')
    d.setdefault('audience', 'private')
    d.setdefault('lang', 'en')
    d.setdefault('mode', 'direct')
    d['_vkey'], d['_v'] = vertical(d['prospect'].get('vertical'))
    # the vertical's own kickers apply to English decks; a translated deck supplies its own labels
    vl = d['_v'].get('labels', {}) if d['lang'].split('-')[0].lower() == 'en' else {}
    if vl and d['mode'] == 'proxy':
        vl = dict(vl)
        if 'like yours' not in vl.get('what_we_see', ''):          # the data is about peers: never "your players"
            vl['what_we_see'] = f"What {d['_v']['people']} like yours do elsewhere"
    d['labels'] = {**LABELS, **vl, **d.get('labels', {})}
    d['dir'] = d.get('dir') or ('rtl' if d['lang'].split('-')[0].lower() in RTL_LANGS else 'ltr')
    d['_dir'] = os.path.dirname(os.path.abspath(path))
    return d


def plain(s):
    """Headline markup: *phrase* is the one emphasised phrase. Strip it for counting and scanning."""
    return re.sub(r'\*([^*]+)\*', r'\1', str(s or ''))


def words(s):
    return len(re.findall(r"[^\s]+", plain(s).strip()))


def slide_text(s):
    """(headline, [body strings]) exactly as the prospect will read them. Notes are not included."""
    t = s.get('type')
    head = s.get('headline') or s.get('title') or ''
    body = []
    add = lambda *xs: body.extend(str(x) for x in xs if x not in (None, ''))
    if t == 'cover':
        add(s.get('subtitle'))
    elif t == 'why_now':
        for e in s.get('events', []):
            add(e.get('date'), e.get('text'), e.get('source'))
        add(s.get('effect'))
    elif t == 'hero':
        add(s.get('number'), s.get('unit'), s.get('line'))
    elif t == 'highlights':
        for i in s.get('items', []):
            add(i.get('number'), i.get('label'), i.get('detail'))
    elif t == 'compare':
        for r in s.get('rows', []):
            add(r.get('label'), r.get('value'))
    elif t == 'statement':
        add(s.get('sub'))
    elif t == 'paths':
        for k in ('advertise', 'enrich'):
            p = s.get(k) or {}
            add(p.get('title'), p.get('line'), *(p.get('points') or []))
    elif t == 'next':
        add(s.get('ask'))
        c = s.get('contact') or {}
        add(c.get('name'), c.get('role'), c.get('email'), c.get('link'))
    elif t == 'method':
        add(*(s.get('points') or []))
        for src in s.get('sources', []):
            add(src.get('name'))
    add(s.get('kicker'), s.get('basis'), s.get('note'))
    return plain(head), [plain(b) for b in body]


def counted_body(s):
    """Body strings that count against the word budget: contact details, source names and basis notes do not."""
    t = s.get('type')
    out = []
    add = lambda *xs: out.extend(plain(x) for x in xs if x not in (None, ''))
    if t == 'cover':
        add(s.get('subtitle'))
    elif t == 'why_now':
        for e in s.get('events', []):
            add(e.get('text'))
        add(s.get('effect'))
    elif t == 'hero':
        add(s.get('line'))
    elif t == 'highlights':
        for i in s.get('items', []):
            add(i.get('label'), i.get('detail'))
    elif t == 'compare':
        for r in s.get('rows', []):
            add(r.get('label'))
    elif t == 'statement':
        add(s.get('sub'))
    elif t == 'paths':
        for k in ('advertise', 'enrich'):
            p = s.get(k) or {}
            add(p.get('line'), *(p.get('points') or []))
    elif t == 'next':
        add(s.get('ask'))
    elif t == 'method':
        add(*(s.get('points') or []))
    return out
