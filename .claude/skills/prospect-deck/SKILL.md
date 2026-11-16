---
name: prospect-deck
description: Build a short, co-branded Addressable deck for ONE named prospect, ready to send, present or publish. Styled and worded for the prospect's business (casino, sportsbook, prediction market, trading platform, perps, FX broker). Six slides - a verified why-now, one number the prospect cannot see about its own users (or about companies like it when it has no on-chain trail), two or three highlights, one ask (advertise, or enrich user data for personalisation, segmentation and VIP identification) - written for a specific buyer (company, role, language, culture) and reviewed from that buyer's seat. Outputs PDF, HTML, PNG and PPTX. Use for any prospect deck, pitch, intro deck, teaser, one-pager or leave-behind for a company, a deck to post on LinkedIn or publish, a shorter version of a hidden-VIP pack or sales report, or a deck translated or adapted for a market. Not for batch vertical packs (hidden-vip-packs), tenant insight PDFs (sales-reports) or wallet-list reports (onchain-entity-prospect-reports).
---

# Prospect deck

One prospect, one buyer, six slides. The deck's job is to earn a reply, not to explain Addressable. A buyer gives a
cold deck a few seconds per slide and forwards it only if one fact in it is about them and new to them. So every
choice here serves one sentence the buyer should be able to repeat: **"Addressable can see something about my users
that I can't, it matters this month, and the next step is small."**

The existing skills produce the evidence; this one produces the argument:

| Skill | Gives this deck |
|---|---|
| `hidden-vip-packs` | Hidden-VIP counts, spend elsewhere, countries, prospects in a market, for a whole vertical |
| `sales-reports` | A client's own users from its pixel (own tenant only) |
| `onchain-entity-prospect-reports` | Where a prospect's wallets or omnibus depositors also play |
| `prospect-deck-check` | The why-now procedure and the last fact check before sending |
| `addressable-brand` | The palette, type and logos the builder already applies |

If numbers already exist from one of them, start at step 3 and reuse them. Do not rerun queries to restate a number.

## What "done" means

The deck passes `lint_deck.py --final` and these tests, which are the brief:

0. **Their business.** It looks and reads like the prospect's own industry: a casino, a sportsbook, a prediction
   market, a trading platform and an FX broker each get their own visual, vocabulary, data route and urgency hooks.
1. **Our data, their blind spot.** The hero number is something the prospect cannot compute from its own systems.
2. **Simple.** One hero, two or three highlights, about 170 words in the whole deck. Detail lives in speaker notes.
3. **Co-branded.** Addressable's logo and the prospect's real logo on the cover and the close.
4. **Urgent, honestly.** A dated, verified reason to act now, with its effect measured in our data where possible.
5. **Never empty.** No on-chain trail means the deck is built on companies like the prospect, and says so.
6. **One ask.** Both paths shown (advertise, enrich), one marked as where this buyer starts, one next step.
7. **Read as the buyer.** Reviewed by a fresh reader playing that person: company, role, language, culture.

## Guardrails (inherited, non-negotiable)

- **No wallet addresses** anywhere: slides, notes, file names, chat.
- **Every figure covers at least 3 people** (`n_min` on each claim).
- **Never reveal our coverage:** not how many casinos, exchanges, tenants, sites or wallets we track, and no
  match-rate or accuracy figures.
- **One client's data never appears in another company's deck.** A client's pixel data goes only in its own deck.
  Before naming a competitor on a slide, check HubSpot: if it is an Addressable client, ask the user first.
- **Never lie, never miss.** Every number on a slide is a claim with a source in `deck.json`; every news item is
  verified (two independent sources or one primary). What cannot be traced comes out.
- **Say what was measured, not why.** "1 in 5 funded another casino", not "players fled".
- **No risk, fraud or sanctions angle.** The deck is about value and growth.
- **Never invent commercial terms.** Prices, discounts, free pilots and guarantees come from the user or
  `references/cta.md`, never from you.
- **Nothing outward without an explicit OK for that action:** no email, Slack, HubSpot write, upload or post.

## Workflow

Work in a folder per deck (`<work>/<prospect-slug>/`), with `deck.json` as the single source. Keep query results
and the claims they feed next to it. Ask the user only for what you cannot find: who the buyer is, and whether the
deck is private (sent to the prospect) or public (published). Use `AskUserQuestion` for those, one call.

### 1. Know the buyer before the data

Read `references/buyer-review.md` part A and write the buyer block of `deck.json` first: company, the person's
role and what they are measured on, the language they work in, their market and its norms. Look in HubSpot, Apollo,
meeting notes (Granola, Fireflies, Meetings) and Slack before searching the web: a past call often holds the buyer's
own words, and their words make the best headline. The buyer decides the hero number, the primary path and the tone,
so this comes before any query.

Set `prospect.vertical` now (`casino`, `sportsbook`, `prediction`, `exchange`, `perps`, `fx`) and read
`references/verticals.md` and that type's profile in `assets/verticals.json`: its words, the words it never uses,
the hero ideas that land, its urgency hooks and where its data comes from. The builder draws the deck for that
business and the lint fails on the wrong vocabulary.

### 2. Find what we know and they don't

Read `references/data-playbook.md`. In short:

```bash
python3 <skill>/scripts/insight_sql.py --name "<Prospect>" --sector <casino|sportsbook|exchange|brokerage> --out <work>/sql
```

Run the probe. **Labelled on-chain → direct mode**: the set is the prospect itself. **No rows → proxy mode**: pick
two to five companies like it (same product, size band and markets), confirm the set with the user, and build on
them. A client with a pixel can also use its own tenant data through `sales-reports`. Then generate and run the
benchmark, overlap and momentum queries (about 1 to 2 GB each; say the estimate first). Check the results for the
artifacts the playbook lists before trusting any of them.

Proxy mode is a full deck, not an apology: "this is what players at casinos like yours do, and you cannot see it
either" is the pitch. But it never implies the numbers are the prospect's own users: `mode: "proxy"`, a `basis` line
on every data slide, and the peer set described on the method slide.

### 3. Why now

Read `references/urgency.md`. Three sources, best first: a verified event near the prospect (follow
`prospect-deck-check/references/why-now.md` for the sweep, the verification and the measurement), a trend in our own
data (momentum, recency, new hidden VIPs this month), and macro (regulation dates, market shifts). Aim for one event
plus one measured effect. If nothing verified turns up, a trend from our data alone is a valid why-now. If there is
truly nothing, set `urgency_skipped` with the reason and tell the user: no urgency beats invented urgency.

### 4. Choose the story, then write it

Read `references/story.md` and `references/deck-spec.md`. List every candidate fact, score each for *new to them*,
*about their KPI* and *actionable this quarter*, and keep one hero and two or three highlights. Everything else goes
to notes or is cut. Write headlines as the conclusion, in the buyer's language from the start (do not write English
and translate at the end). Fill `claims` as each number goes in, not afterwards.

### 5. Choose the ask

Read `references/cta.md`. Both paths always appear; `primary` is the one this buyer owns: acquisition and marketing
roles start with **Advertise**, CRM, VIP, retention, product and data roles start with **Enrich** (personalise,
segment, identify VIPs). The `next` slide carries one ask small enough to say yes to in a reply: by default one that needs nothing from the
buyer. Asking for a user sample first is a data transfer, not a small step.

### 6. Logo, build, render

```bash
python3 <skill>/scripts/fetch_logo.py <prospect domain> --out <work>/<slug>
```

Look at the candidates and choose the real, current, full logo; set `prospect.logo` and `logo_plate`. Then:

```bash
python3 <skill>/scripts/lint_deck.py <work>/<slug>/deck.json
```
```bash
python3 <skill>/scripts/build_deck.py <work>/<slug>/deck.json
```
```bash
node <skill>/scripts/render.js <work>/<slug>/deck.html
```
```bash
python3 <skill>/scripts/make_pptx.py <work>/<slug>/deck.json
```

`render.js` fails if any text spills outside a slide. The fix is always fewer words, never smaller type.

### 7. Look at it

Read the PNGs in `png/`. Check the prospect's logo is crisp and on the right plate, the hero number dominates its
slide, nothing wraps awkwardly, and the deck reads in order with the headlines alone. Then read only the headlines
aloud, top to bottom: they should make the whole argument.

### 8. Review it from the buyer's seat

Read `references/buyer-review.md` part D. Start a **fresh** agent with `agents/buyer.md`, the buyer block and the PNGs
only: no data notes, no rationale, no claims. It answers as the buyer and scores the deck. Fix what it flags, rebuild,
and review again with another fresh agent until every score is 4 or more. Record the result in `review` in
`deck.json`. Objections that need a product fact (how matching works, who else can see their users, a customer
result) are not yours to answer: use the approved answers in `buyer-review.md`, or ask the user. Then:

```bash
python3 <skill>/scripts/lint_deck.py <work>/<slug>/deck.json --final
```

### 9. Fact check

Run `prospect-deck-check` on the PDF with the `claims.json` the lint wrote (its `check_deck.py`, plus
`verify_onchain.py` for any on-chain fact in the why-now). It must print OK. If that skill is not installed, say so
and list the checks that did not run as open items: an unrun check is never a pass.

### 10. Deliver

Read `references/publishing.md`. Send the user `deck.pdf`, `deck.html`, `deck.pptx` and the cover PNG with
`SendUserFile`, plus in chat: the one-sentence takeaway the buyer reviewer gave, the events used and left out, the
open objections the reviewer raised (these are the first questions on the call), a talk track of one line per slide,
a share message in the buyer's language, and the Athena scan total. For a public version, build a second
`deck.json` with `audience: "public"`: it drops the prospect's name, logo and own data.

## Files

| Path | Does |
|---|---|
| `scripts/insight_sql.py` | Probe (direct or proxy?), benchmark, overlap and momentum queries for the prospect or its peer set |
| `scripts/fetch_logo.py` | Logo candidates from the prospect's own site |
| `scripts/lint_deck.py` | The gate: story shape, word budgets, traced numbers, verified events, guardrails, proxy and public rules, the buyer review (`--final`); writes `claims.json` |
| `scripts/build_deck.py` | `deck.json` to one self-contained `deck.html` |
| `scripts/render.js` | `deck.html` to `deck.pdf`, `png/slide-NN.png`, `og.png`; fails on overflow |
| `scripts/make_pptx.py` | PNGs and notes to `deck.pptx` |
| `scripts/deckspec.py` | The word budgets and fixed labels (shared by the scripts) |
| `scripts/vertical_preview.py` | Builds the same fixture for every business type, to compare looks side by side |
| `assets/verticals.json` | The business-type profiles: look, words, words to avoid, data route, hero ideas, urgency hooks |
| `agents/buyer.md` | Brief for the buyer-seat reviewer |
| `references/deck-spec.md` | `deck.json` fields and slide types |
| `references/verticals.md` | What changes per business type and how to add one |
| `references/story.md` | The arc, how to pick the hero and highlights, headline rules |
| `references/data-playbook.md` | Direct, proxy and tenant routes, the insight menu, artifacts to rule out |
| `references/urgency.md` | Finding, verifying and wording the why-now |
| `references/cta.md` | The two paths, the ask by buyer role, offers |
| `references/buyer-review.md` | Buyer dossier, role lenses, language and culture, the review loop |
| `references/publishing.md` | Private and public versions, formats, share messages |
| `examples/examplex.deck.json` | A complete fictional proxy-mode deck. It passes the draft lint; its `review` block is a real second-round "revise", kept to show what the buyer review catches and what only the user can answer |

Requirements: Python 3.10+, Node 18+ with Playwright and Chromium (`CHROMIUM_PATH` to use an installed Chrome),
`python-pptx` for the PPTX, and the Athena MCP connector for new numbers. Fonts and Addressable logos are bundled.
