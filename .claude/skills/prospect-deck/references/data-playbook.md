# Data: what we know that they don't

The deck needs four or five numbers, not a report. Get them the cheapest way that is still true, and reuse numbers
that an earlier pack or report already produced (cite that file as the claim's source).

## 1. Pick the route

| The prospect is | Mode | Where the numbers come from | Claim `scope` |
|---|---|---|---|
| A client or trial with our pixel | direct | `sales-reports` on its own tenant only (overlap, value bands, sports trading). Aggregates for the deck; the user-level PDF stays a separate deliverable | `prospect` |
| Labelled on-chain (the probe returns its name) | direct | `insight_sql.py` with the prospect's own label as the set. Deeper: `hidden-vip-packs` for linked wallets and countries; `onchain-entity-prospect-reports` if they gave wallets or an omnibus | `prospect` |
| Not on-chain, or on-chain but tiny or unlabelled | proxy | `insight_sql.py` with two to five companies like it as the set | `peers` |
| Any | either | Market context: momentum across the sector, a verified public figure | `market`, `public` |

Run the probe first (`insight_sql.py --name "<Prospect>" --out <dir>`, about 0.3 GB) and confirm a match with the
user: a shared word in a name is not a match. The business type decides which sector the queries read and which
skill covers what they cannot: see `assets/verticals.json` (`sector`, `data_route`). Prediction markets and perp
DEXs are contracts, not deposit addresses, so their numbers come from `hidden-vip-packs` or `sales-reports`, not
from `insight_sql.py`.

## 2. Proxy mode: companies like the prospect

Use it whenever the prospect has no usable trail. It is the common case for fiat-first casinos and sportsbooks,
FX and CFD brokers, and anyone new.

Choose the peer set on purpose and write the reason down for the method slide:

- **Same product** as the buyer sees it (sports-led books for a sportsbook, not any casino).
- **Same size band.** Three mid-size peers beat one giant: one giant is the whole number.
- **Same markets** where it can be known. Find the prospect's top countries and closest competitors with Similarweb
  (traffic by country, competing sites) or from the user, then pick labelled peers that match.
- Two to five peers. Confirm the set with the user before running anything.
- A peer that is an Addressable client can be in the set (its public on-chain deposits are public), but never its
  pixel data, and ask the user before naming it on a slide.

**Peers must be like the prospect in the way the buyer would judge it, and described as what they are.** The first
buyer review of this skill's own sample failed on exactly this: "casinos like Examplex" turned out, on the method
slide, to be crypto casinos, and the reader was a fiat operator. Name the peer set by its true description in the
`basis` line ("three crypto casinos of your size"), never by a flattering likeness.

**The fiat question.** Our deposit data is crypto. For a fiat-first prospect (most licensed casinos and sportsbooks,
every FX broker) the buyer's first thought is "my customers pay by card or bank transfer: does this apply to me?"
Answer it on the slides before they ask: say the numbers describe the crypto-active part of the market, say how
that part relates to their business (the customers they are losing to crypto venues, or the high-value segment they
want to win), and do not imply coverage of their fiat base. If the honest answer is "this covers a small part of
your customers", say so; the deck then sells the audience they do not have yet (Advertise) rather than insight into
the one they do.

How to say it:

- Every data slide carries a `basis` line: "Casinos like Examplex in Brazil, last 90 days."
- The method slide says how the peers were chosen and that the prospect's own users are not in the data.
- Never "your players". Write "players at casinos like yours", or state the fact with no possessive.
- The honest turn is the close: "These are other casinos' players. Yours look the same, or they don't, and today
  you can't tell." The first step is still one that needs nothing from them (see `cta.md`): the sample comes second.
- Give every number its base and every change its baseline: "1,296 of 133,000 players", "1 in 5, against 1 in 10 in
  a normal fortnight". A count without a denominator, or a move without a normal rate, is the first thing a careful
  buyer attacks.

## 3. The insight menu

Each row is one sentence a buyer cannot produce alone. `benchmark`, `overlap` and `momentum` are the files
`insight_sql.py` writes; columns are named as they come back.

| Insight | From | Sentence | Lands with |
|---|---|---|---|
| Hidden VIPs | benchmark `hidden_vips`, `median_else_hidden` | "N players deposit under $500 here and over $5,000 elsewhere" | CRM, VIP, retention |
| Shared loyalty | `multi_venue_users / users` | "X% fund two or more casinos" | CRM, product, CEO |
| Concentration | `usd_top1pct / usd_set` | "The top 1% bring Y% of deposits" | CEO, finance, VIP |
| Wallet share | `usd_elsewhere / (usd_set + usd_elsewhere)` | "For every $1 here, they put $Z elsewhere" | CEO, growth |
| Where else | overlap `other_venue`, `shared_users` | "Their second home is <venue>" (check the client rule) | Marketing, growth |
| Momentum | momentum `depositors_recent / depositors_before` | "Depositors at <venue> rose X% in 30 days" | Marketing, CEO |
| Win-back pool | `whynow_sql.py` switchers `n2` | "N of a rival's recent users already know you" | Growth, CRM |
| Reachable audience | `hidden-vip-packs` prospects | "N proven players in your markets are not yours yet" | Acquisition |

Derive shares and ratios yourself from the returned columns, show them rounded, and put both columns in the claim's
`source`. `n_min` is the smallest people count behind the sentence.

## 4. Rule out artifacts before quoting anything

Each of these was seen in real results (16 Nov 2026, casinos, 90 days):

- **A venue that jumps several-fold in a month is a label backfill, not growth.** Momentum showed two casinos going
  from about 2K to about 20K depositors in 30 days. Check the venue by day before quoting any trend, and never build
  urgency on a step change you have not explained.
- **A chain that starts mid-window fakes a surge.** Tron has no rows before 3 Nov 2026 in the deposit table:
  `--exclude-chains 728126428` for any window that crosses it, and say which chains are compared.
- **Country cuts are thin.** Of 133K depositors of three casinos, 120 had a known location in Brazil, and 3 were
  hidden VIPs. A country filter keeps only device-linked wallets: use it to describe a market, not to size one,
  and prefer `hidden-vip-packs` when the country is the point.
- **One wallet can be the whole total.** Deposits are capped at $10M per wallet and venue in every query; still check
  what share the top few carry before quoting a sum. Prefer counts and medians to sums.
- **A partial last day** understates the recent window: end windows on a completed day.
- **Clients appear in overlap lists.** Before any venue is named on a slide, check HubSpot for it.
- **Under 3 people:** drop the row. The queries already do for venues; do it for anything you derive.

## 5. Cost and record

State the scan estimate before running (probe 0.3 GB; benchmark, overlap and momentum 1 to 2 GB each for 90 days;
a country join adds little). Save each result next to the deck and name the file and column in the claim. Report
the total with the deck. More than $10 in a day is worth telling the user about.
