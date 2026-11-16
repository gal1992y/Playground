# deck.json

One file holds the whole deck: who it is for, the slides, and the source of every number. `examples/examplex.deck.json`
is a complete one. Paths are relative to the file.

## Top level

| Field | Meaning |
|---|---|
| `prospect` | `name`, `domain`, `logo` (file), `logo_plate` (`light` = white plate for a dark or coloured logo, `dark` for a white logo), `vertical` (required: `casino`, `sportsbook`, `prediction`, `exchange`, `perps`, `fx`; sets the look, the words and the data route, see `verticals.md`), `markets` (ISO2). `logo_waived`: reason, when no usable logo exists. `logo_permission`: true only when the prospect agreed to be named in a public deck |
| `buyer` | `company`, `role`, `language`, `market`, plus free notes (`kpis`, `tone`, `name`). Written in step 1 |
| `mode` | `direct` (numbers about the prospect's own users) or `proxy` (numbers about companies like it) |
| `audience` | `private` (sent to the prospect; footer says Confidential) or `public` (published; no prospect name, logo or own data) |
| `lang`, `dir` | Language code of the slides; `dir` is set to `rtl` automatically for he, ar, fa, ur |
| `date` | Month and year for the cover, written in the deck's language |
| `labels` | Overrides for the fixed strings (kickers, "Prepared for", "Start here", "Confidential"...). Translate all of them for a non-English deck; the keys are in `scripts/deckspec.py` |
| `slides` | The slides, in order |
| `claims` | One entry per number shown: `text` exactly as on the slide, `value`, `source` (query name and column, execution id, URL), `kind` (`query`, `url`, `definition`), `n_min` (people behind it; required for `query`), `scope` (`prospect`, `peers`, `market`, `public`) |
| `template` | Fixed phrases with a number in them that are not data ("20 minutes", "top 1%", "day one") |
| `events` | Why-now events: `id`, `date` (ISO), `title`, `status` (`verified`, `single-source`, `unconfirmed`, `dropped`), `sources` [`name`, `url`, `kind`: `primary`, `regulator`, `company`, `analytics`, `onchain`, `press`, `social`], `figures`, `conflicts`, `conflict_handling` |
| `vocabulary_ok` | Words from the vertical's avoid list that are right in this deck (rare) |
| `urgency_skipped` | Reason, when the deck has no why-now slide |
| `language_decision` | Reason, when the deck's language is not the buyer's |
| `review` | The buyer review result (see `buyer-review.md`): `buyer`, `rounds`, `scores`, `verdict`, `takeaway`, `changes`, `open_objections` |

## Slides

Every slide takes `notes` (the talk track; goes to the PPTX speaker notes, never on the slide) and, on data slides,
`basis` (one small line saying whose data and which period; required in proxy mode). In any headline or line,
`*phrase*` marks the one phrase set in the brand gradient. Use it once per slide, on the words that carry the point.

| `type` | Fields | Budget |
|---|---|---|
| `cover` | `title`, `subtitle` | Title up to 10 words |
| `why_now` | `headline`, `events` [`id`, `date` (as shown), `text`, `source` (name)], `effect` | 1 to 3 events |
| `hero` | `number`, `unit` (optional), `line` | One per deck |
| `highlights` | `headline`, `items` [`number`, `label`, `detail`] | 2 or 3 items |
| `compare` | `headline`, `rows` [`label`, `value` (as shown), `pct` (bar length 0 to 100), `accent`] | 2 to 5 rows, one accent |
| `statement` | `headline`, `sub`, `kicker` | One sentence and one support line |
| `paths` | `headline`, `primary` (`advertise` or `enrich`), `advertise` and `enrich` {`title`, `line`, `points`} | 3 points per path, 6 words each |
| `next` | `headline`, `ask`, `contact` {`name`, `role`, `email`, `link`} | Ask up to 14 words |
| `method` | `points`, `sources` [`name`, `url`] | Optional, last, up to 90 words |

Budgets for the whole deck: 8 story slides at most (6 is the target), headlines up to 10 words, 35 words of body
text per slide (48 on `paths`), 230 words in total. The method slide is extra. The numbers live in
`scripts/deckspec.py`; `lint_deck.py` enforces them.

The usual six: `cover`, `why_now`, `hero`, `highlights`, `paths`, `next`, then `method`. Add a `compare` when one
contrast (here against elsewhere, you against peers) makes the point better than a third highlight. Add a
`statement` only when a single sentence deserves a slide of its own.
