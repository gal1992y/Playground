#!/usr/bin/env python3
"""Gate for a prospect deck. Run it on every draft; run it with --final before anything is shared.

usage: lint_deck.py <deck.json> [--final]

Fails (exit 1) on:
  story      no cover first, no hero or highlights, not exactly one `paths` slide, no `next` slide last,
             more story slides than the budget, a why-now slide missing with no `urgency_skipped` reason
  budget     a headline, slide or the whole deck over its word budget; more than 3 highlights; more than 3 events
  numbers    a number on a slide that no claim in deck.json accounts for; a claim with no source;
             a figure covering fewer than 3 people (`n_min`)
  events     a why-now event that is not `verified` in `events`, or verified without a date, a URL, and
             two independent sources or one primary source
  proxy      (mode "proxy") a data slide with no `basis` line, "your players" on peer data, or a claim scoped to the
             prospect's own users
  public     (audience "public") prospect-scoped claims, or the prospect's name or logo without `logo_permission`
  guardrails wallet addresses, our coverage ("we track N casinos"), match-accuracy figures, site counts,
             raw dollar figures about named third parties' users below the people floor, em dashes, broken values
  vocabulary a word this kind of business does not use for its own customers (assets/verticals.json)
  cta        `paths.primary` not advertise or enrich; an ask that is empty or too long; no contact; a first ask
             that needs the buyer's user data (unless `data_ask_ok`)
  --final    no buyer review recorded for this buyer, a score under 4, or a verdict other than "pass"

Warns on causal wording, hype words, and a deck language that differs from the buyer's.
Writes claims.json next to the deck in the format prospect-deck-check's check_deck.py reads.
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deckspec  # noqa: E402
from deckspec import BUDGET, words

MONTHS = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*'
NUM = re.compile(r'(?<![\w.#/])\$?(?:\d{1,3}(?:[,.\u00a0 ]\d{3})+|\d+)(?:[.,]\d+)?\s?(?:[KMB](?![a-z])|%|×|x(?=\s|$|\W))?\+?')
PRIMARY = {'primary', 'regulator', 'company', 'onchain', 'analytics'}
GUARDS = [
    ('wallet address (0x)', re.compile(r'0x[0-9a-fA-F]{8,}')),
    ('wallet address (base58)', re.compile(r'(?<![A-Za-z0-9])[1-9A-HJ-NP-Za-km-z]{32,44}(?![A-Za-z0-9])')),
    ('ENS name', re.compile(r'\b[a-z0-9-]+\.eth\b')),
    ('local path', re.compile(r'(?:/Users/|/home/|~/|C:\\)')),
    ('broken value', re.compile(r'\b(?:undefined|NaN|Infinity|null|None)\b|\[object|\{\{|\}\}|<[A-Z_]{3,}>')),
    ('em dash (house rule)', re.compile('\u2014')),
    ('match accuracy figure', re.compile(r'(?i)(?:match(?:ing)?\s+(?:rate|accuracy)|accuracy)[^.]{0,40}\d+\s?%|\d+\s?%[^.]{0,30}match(?:ing)?\s+(?:rate|accuracy)')),
    ('website count', re.compile(r'(?i)\b[\d,]+\+?\s+(?:web)?sites\b|\bdeployed on\s+[\d,]+')),
    ('our coverage', re.compile(r'(?i)\bwe\s+(?:track|cover|monitor|label|see)\s+(?:over\s+|more than\s+)?[\d,.]+\+?[KMB]?\s+(?:casinos|exchanges|tenants|brands|entities|clients|customers|wallets|devices|users)\b'
                                r'|\b[\d,.]+\+?[KMB]?\s+(?:tenants|clients|customers)\s+(?:on|in|across)\s+(?:our|the addressable)')),
    ('risk or sanctions wording', re.compile(r'(?i)\b(?:sanction(?:ed|s)?|money launder\w*|fraudsters?|scammers?)\b')),
]
CAUSAL = re.compile(r"(?i)(?<!not )(?<!n't )(?<!never )\b(moved to|switched to|fled|flock\w* to|migrat\w+ to|left for|abandon\w*)\b")
HYPE = re.compile(r'(?i)\b(revolutionary|game.?chang\w+|cutting.edge|best.in.class|world.class|unparalleled|seamless(?:ly)?|unlock\w*|supercharge\w*|leverage|synerg\w+|next.gen\w*|disrupt\w*|guarantee\w*)\b')


def norm(s):
    return re.sub(r'[\s\u00a0]+', ' ', str(s)).strip().lower()


def number_tokens(text):
    text = re.sub(r'https?://\S+|\b[\w.+-]+@[\w.-]+\b|\b\d{4}-\d{2}-\d{2}\b', lambda m: ' ' * len(m.group(0)), text)
    out = []
    for m in NUM.finditer(text):
        tok, (s, e) = m.group(0).strip(), m.span()
        before, after = text[max(0, s - 12):s], text[e:e + 12]
        if re.search(MONTHS + r'\s*$', before) or re.match(r'\s*' + MONTHS, after):
            continue                                              # a day of the month
        bare = re.sub(r'\D', '', tok)
        if re.fullmatch(r'\d{4}', tok) and 1990 <= int(tok) <= 2100:
            continue                                              # a year
        if not bare:
            continue
        out.append(tok)
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    final = '--final' in sys.argv
    if len(args) != 1:
        sys.exit(__doc__)
    d = deckspec.load(args[0])
    E, W = [], []
    slides = d['slides']
    types = [s.get('type') for s in slides]
    story = [s for s in slides if s.get('type') != 'method']
    proxy, public = d['mode'] == 'proxy', d['audience'] == 'public'
    P = d['prospect']
    name = P.get('name', '')

    # ---- story
    if not types or types[0] != 'cover':
        E.append('story: the first slide must be the cover')
    for i, t in enumerate(types, 1):
        if t not in deckspec.SLIDE_TYPES:
            E.append(f'story: slide {i} has unknown type {t!r}')
    if not any(t in ('hero', 'highlights') for t in types):
        E.append('story: no hero or highlights slide: the deck has to show what we know and they do not')
    if types.count('paths') != 1:
        E.append(f'cta: exactly one `paths` slide (advertise / enrich) is needed, found {types.count("paths")}')
    if not story or story[-1].get('type') != 'next':
        E.append('cta: the last story slide must be `next` (one ask, one contact)')
    if types.count('hero') > 1:
        E.append('story: one hero number per deck; move the others into highlights')
    if len(story) > BUDGET['slides']:
        E.append(f'budget: {len(story)} story slides, the limit is {BUDGET["slides"]} (the method slide is extra)')
    if 'why_now' not in types and not d.get('urgency_skipped'):
        E.append('story: no why-now slide. Add one, or set "urgency_skipped" to the reason (e.g. "sweep found nothing verified")')
    if 'method' in types and types[-1] != 'method':
        E.append('story: the method slide goes last')

    # ---- budgets
    total = 0
    for i, s in enumerate(slides, 1):
        t = s.get('type')
        head, _ = deckspec.slide_text(s)
        hw = words(head)
        if t == 'hero':
            head, hw = '', 0
        if hw > BUDGET['headline_words']:
            E.append(f'budget: slide {i} headline is {hw} words (max {BUDGET["headline_words"]}): "{head}"')
        if t not in ('hero', 'method') and not head:
            E.append(f'story: slide {i} ({t}) has no headline')
        bw = sum(words(x) for x in deckspec.counted_body(s))
        lim = BUDGET['method_words'] if t == 'method' else BUDGET['paths_words'] if t == 'paths' else BUDGET['body_words']
        if bw > lim:
            E.append(f'budget: slide {i} ({t}) has {bw} words of body text (max {lim}). Cut, or move detail to notes')
        if t != 'method':
            total += hw + bw
        if t == 'highlights' and not 2 <= len(s.get('items', [])) <= BUDGET['highlights']:
            E.append(f'budget: slide {i} needs 2 or 3 highlights, has {len(s.get("items", []))}')
        if t == 'why_now' and not 1 <= len(s.get('events', [])) <= BUDGET['events']:
            E.append(f'budget: slide {i} needs 1 to 3 events, has {len(s.get("events", []))}')
        if t == 'compare' and not 2 <= len(s.get('rows', [])) <= BUDGET['compare_rows']:
            E.append(f'budget: slide {i} needs 2 to 5 rows, has {len(s.get("rows", []))}')
        if t == 'hero' and not (s.get('number') and (s.get('line') or s.get('headline'))):
            E.append(f'story: slide {i} (hero) needs a `number` and one `line`')
        if t == 'paths':
            if s.get('primary') not in ('advertise', 'enrich'):
                E.append(f'cta: slide {i} `primary` must be "advertise" or "enrich" (the path this buyer starts with)')
            for k in ('advertise', 'enrich'):
                p = s.get(k) or {}
                if not p.get('title'):
                    E.append(f'cta: slide {i} path "{k}" has no title. Both paths are always shown')
                pts = p.get('points') or []
                if len(pts) > BUDGET['path_points']:
                    E.append(f'budget: slide {i} path "{k}" has {len(pts)} points (max {BUDGET["path_points"]})')
                for x in pts:
                    if words(x) > BUDGET['path_point_words']:
                        E.append(f'budget: slide {i} path point over {BUDGET["path_point_words"]} words: "{x}"')
        if t == 'next':
            aw = words(s.get('ask'))
            if not aw:
                E.append(f'cta: slide {i} has no `ask`')
            elif aw > BUDGET['ask_words']:
                E.append(f'cta: slide {i} ask is {aw} words (max {BUDGET["ask_words"]}). One ask, one sentence')
            c = s.get('contact') or {}
            if not (c.get('name') and (c.get('email') or c.get('link'))):
                E.append(f'cta: slide {i} needs a contact name and an email or link')
        if proxy and t in deckspec.DATA_TYPES + ('why_now',):
            shown = [deckspec.slide_text(s)[0]] + deckspec.slide_text(s)[1] + [d['labels'].get({'hero': 'what_we_see', 'highlights': 'highlights', 'compare': 'compare', 'why_now': 'why_now'}[t], '')]
            for seg in shown:
                m = re.search(r'(?i)\byour (?:own )?(?:players|bettors|traders|clients|users|customers|depositors|vips)\b', seg)
                if m:
                    E.append(f'proxy: slide {i} says "{m.group(0)}" but the data is about other companies. Say "{d["_v"]["people"]} like yours" or drop the possessive')
                    break
        if t == 'hero' and not re.search(r'[%×x]|\bin\b', str(s.get('number', ''))) and not re.search(r'(?i)\b(?:of|out of|among)\s+[\d$]', str(s.get('line', '')) + ' ' + str(s.get('basis', ''))):
            W.append(f'numbers: slide {i} hero is a raw count with no base. Say what it is out of ("1,296 of 133,000 players"): a buyer cannot judge a number without its denominator')
        if t == 'next' and re.search(r'(?i)\b(?:share|send|upload|give)\b.{0,30}\b(?:sample|users?|players?|clients?|data|list|wallets?)\b', str(s.get('ask', ''))) and not d.get('data_ask_ok'):
            E.append(f'cta: slide {i} asks the buyer to hand over user data as the first step. For most buyers, and every regulated one, that needs legal sign-off, '
                     f'so it is not a small ask. Lead with a step that needs nothing from them, or set "data_ask_ok" to why it is fine here (e.g. "they offered a sample on the call")')
        if proxy and t in deckspec.DATA_TYPES and not s.get('basis'):
            E.append(f'proxy: slide {i} ({t}) needs a `basis` line saying whose data this is (e.g. "Casinos like {name}, last 90 days")')
    if total > BUDGET['deck_words']:
        E.append(f'budget: the deck has {total} words on its story slides (max {BUDGET["deck_words"]})')

    # ---- numbers traced to claims
    claim_texts = [norm(c.get('text', '')) for c in d['claims']]
    tmpl = [norm(x) for x in d['template']]
    for c in d['claims']:
        if not c.get('source'):
            E.append(f'numbers: claim "{c.get("text")}" has no source')
        if c.get('kind') == 'query' and 'n_min' not in c:
            E.append(f'numbers: claim "{c.get("text")}" comes from a query but has no `n_min` (the smallest count of people behind it)')
        if isinstance(c.get('n_min'), (int, float)) and c['n_min'] < 3:
            E.append(f'guardrail: claim "{c.get("text")}" covers {c["n_min"]} people; every published figure covers at least 3')
        if c.get('scope') == 'prospect' and proxy:
            E.append(f'proxy: claim "{c.get("text")}" is scoped to the prospect, but this deck is in proxy mode (no data on their own users)')
        if c.get('scope') == 'prospect' and public:
            E.append(f'public: claim "{c.get("text")}" is about the prospect\'s own users and cannot be published')
        if c.get('scope') == 'client':
            E.append(f'guardrail: claim "{c.get("text")}" is scoped to another client: one client\'s data never goes in another company\'s deck')
    for i, s in enumerate(slides, 1):
        head, body = deckspec.slide_text(s)
        for seg in [head] + body:
            nseg = norm(seg)
            for tok in number_tokens(seg):
                nt = norm(tok)
                if any(nt in ct for ct in claim_texts) or any(nt in x for x in tmpl):
                    continue
                if any(ct and ct in nseg and nt in ct for ct in claim_texts):
                    continue
                E.append(f'numbers: slide {i} shows "{tok}" ("{seg[:60]}") and no claim accounts for it. '
                         f'Add the claim with its real source, or take the number out')
    used = ' '.join(norm(x) for s in slides for x in [deckspec.slide_text(s)[0]] + deckspec.slide_text(s)[1])
    for c in d['claims']:
        if norm(c.get('text', '')) and norm(c['text']) not in used:
            W.append(f'numbers: claim "{c["text"]}" is not on any slide (fine if it only supports the talk track)')

    # ---- events
    ev = {e.get('id'): e for e in d['events']}
    for i, s in enumerate(slides, 1):
        if s.get('type') != 'why_now':
            continue
        for e in s.get('events', []):
            src = ev.get(e.get('id'))
            if not src:
                E.append(f'events: slide {i} event "{e.get("text")}" has no entry in `events` (id {e.get("id")!r})')
                continue
            if src.get('status') != 'verified':
                E.append(f'events: "{src.get("title")}" is {src.get("status")!r}: only verified events go on a slide')
            ss = src.get('sources') or []
            if not src.get('date'):
                E.append(f'events: "{src.get("title")}" has no date')
            if any(not x.get('url') for x in ss) or not ss:
                E.append(f'events: "{src.get("title")}" needs a URL for every source')
            names = {norm(x.get('name', '')) for x in ss}
            if not (any(x.get('kind') in PRIMARY for x in ss) or len(names) >= 2):
                E.append(f'events: "{src.get("title")}" needs two independent sources or one primary source')
            if src.get('conflicts') and not src.get('conflict_handling'):
                E.append(f'events: "{src.get("title")}" has conflicting sources and no `conflict_handling`')
    for e in d['events']:
        if e.get('status') != 'verified' and norm(e.get('title', '')) and norm(e['title']) in used:
            E.append(f'events: unverified event "{e.get("title")}" appears on a slide')

    # ---- guardrails over every string that can reach the prospect (slides and notes: notes travel in the PPTX)
    for i, s in enumerate(slides, 1):
        head, body = deckspec.slide_text(s)
        for seg in [head] + body + [str(s.get('notes') or '')]:
            for label, rx in GUARDS:
                m = rx.search(seg)
                if m:
                    shown = m.group(0) if 'wallet' not in label else m.group(0)[:6] + '…'
                    E.append(f'guardrail: slide {i}: {label}: "{shown}"')
        for seg in [head] + body:
            if CAUSAL.search(seg):
                W.append(f'wording: slide {i} uses causal wording ("{CAUSAL.search(seg).group(0)}"). Keep it only if switching was measured')
            if HYPE.search(seg):
                W.append(f'wording: slide {i} uses a hype word ("{HYPE.search(seg).group(0)}"). Say the plain thing')

    # ---- the words of this business (assets/verticals.json): a broker has clients, a sportsbook has bettors
    if not P.get('vertical'):
        E.append('vertical: set `prospect.vertical` (casino, sportsbook, prediction, exchange, perps, fx): it sets the look, the words and the data route')
    elif d['_vkey'] == 'default':
        W.append(f'vertical: "{P.get("vertical")}" has no profile, so the deck uses the neutral look and words. Pick the closest one if it fits')
    ok = {norm(x) for x in d.get('vocabulary_ok', [])}
    for i, s in enumerate(slides, 1):
        head, body = deckspec.slide_text(s)
        for seg in [head] + body:
            for word, why in d['_v'].get('avoid', {}).items():
                m = re.search(r'(?i)\b' + re.escape(word) + r'\w*', seg)
                if m and norm(m.group(0)) not in ok:
                    E.append(f'vocabulary: slide {i} says "{m.group(0)}" in a {d["_v"]["label"].lower()} deck: {why}. '
                             f'(If it is right here, add the word to "vocabulary_ok".)')

    # ---- logos, public tier
    if public:
        if name and not P.get('logo_permission'):
            for i, s in enumerate(slides, 1):
                head, body = deckspec.slide_text(s)
                if any(re.search(r'\b' + re.escape(name) + r'\b', x) for x in [head] + body):
                    E.append(f'public: slide {i} names {name}. A published deck names the prospect only with `logo_permission`')
    else:
        logo = P.get('logo')
        if not logo:
            E.append('brand: no prospect logo (`prospect.logo`). Fetch it with fetch_logo.py or ask for the file; '
                     'set "logo_waived" with the reason to ship with the name set in type') if not P.get('logo_waived') else None
        elif not os.path.exists(logo if os.path.isabs(logo) else os.path.join(d['_dir'], logo)):
            E.append(f'brand: prospect logo file not found: {logo}')
    if not d.get('date'):
        W.append('brand: no `date` (month and year on the cover)')

    # ---- language
    b = d['buyer']
    if b.get('language') and b['language'].split('-')[0].lower() != d['lang'].split('-')[0].lower() and not d.get('language_decision'):
        W.append(f'language: the buyer reads {b["language"]} and the deck is in {d["lang"]}. Translate it, or record why not in "language_decision"')

    # ---- final: the buyer review
    if final:
        r = d.get('review') or {}
        rb = r.get('buyer') or {}
        for k in ('company', 'role', 'language', 'market'):
            if not rb.get(k):
                E.append(f'review: no buyer {k} recorded. The deck is reviewed as a specific person, not "a prospect"')
        sc = r.get('scores') or {}
        for k in ('relevance', 'clarity', 'credibility', 'urgency', 'fit', 'action'):
            if k not in sc:
                E.append(f'review: no score for {k}')
            elif sc[k] < 4:
                E.append(f'review: {k} scored {sc[k]} of 5. Fix what the buyer flagged and review again')
        if r.get('verdict') != 'pass':
            E.append(f'review: verdict is {r.get("verdict")!r}, not "pass"')
        if not r.get('takeaway'):
            E.append('review: no `takeaway` (the one sentence the buyer remembered). If they could not give one, the deck is not simple enough')
        if not r.get('rounds'):
            E.append('review: `rounds` is missing')

    # ---- claims.json for prospect-deck-check
    # check_deck.py matches number by number, so phrases are also listed by their bare numbers:
    # "20 minutes" -> template "20"; a claim worded "1 in 5" -> "1" and "5" carried by the same source
    tmpl_out = list(d['template']) + sorted({t for x in d['template'] for t in number_tokens(x)} - set(d['template']))
    claims_out = [{k: c[k] for k in ('text', 'value', 'source', 'kind') if k in c} for c in d['claims']]
    have = {norm(c.get('text', '')) for c in d['claims']}
    for c in d['claims']:
        toks = number_tokens(str(c.get('text', '')))
        if len(toks) > 1:
            for t in toks:
                if norm(t) not in have:
                    have.add(norm(t))
                    v = float(re.sub(r'[^\d.]', '', t) or 0)
                    claims_out.append({'text': t, 'value': v, 'kind': c.get('kind', 'query'),
                                       'source': f'part of "{c["text"]}": {c.get("source", "")}'})
    ledger = {'deck': f'{name} prospect deck', 'as_of': d.get('as_of') or d.get('date', ''),
              'claims': claims_out,
              'evidence_files': d.get('evidence_files', []), 'template': tmpl_out,
              'events': [{k: v for k, v in e.items() if k != 'id'} for e in d['events']]}
    lp = os.path.join(d['_dir'], 'claims.json')
    with open(lp, 'w', encoding='utf8') as f:
        json.dump(ledger, f, indent=1, ensure_ascii=False)

    for w in W:
        print('warn  ' + w)
    for e in E:
        print('FAIL  ' + e)
    print(f'{len(story)} story slides, {total} words, {len(d["claims"])} claims, mode {d["mode"]}, audience {d["audience"]}'
          f'{", final" if final else ""}. Wrote {lp}')
    if E:
        print(f'NOT READY: {len(E)} problem(s)')
        sys.exit(1)
    print('OK' + ('' if final else ' (draft). Run the buyer review, then --final'))


if __name__ == '__main__':
    main()
