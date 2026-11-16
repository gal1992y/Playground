# Business types

A casino, a sportsbook, a prediction market, a trading platform and an FX broker do not call their customers the
same thing, fear the same events or read the same data. `prospect.vertical` selects a profile from
`assets/verticals.json`, and the profile changes four things:

| | What changes | Where |
|---|---|---|
| **Look** | The line drawing on the cover, the hero and the close, and the accent colour of kickers, event cards and the cover glow. The brand gradient, type and layout stay Addressable's | `build_deck.py` (`motif`, `accent`) |
| **Words** | Who the customers are, what a venue is, what a VIP is called; the kicker above the hero; words this business does not use (the lint fails on them) | `people`, `person`, `venue`, `vip`, `labels`, `avoid` |
| **Data** | Which sector `insight_sql.py` reads, or which other skill holds the numbers | `sector`, `data_route` |
| **Story** | The hero ideas that land and the events that create urgency for this business | `hero_ideas`, `urgency_hooks`, `sample` |

| `vertical` | Also accepts | Customers | Look | Data route in one line | Typical why-now |
|---|---|---|---|---|---|
| `casino` | gambling, igaming | players | chips, pink | `insight_sql.py --sector casino` | A rival's outage or licence change |
| `sportsbook` | sports, betting | bettors | pitch, green | `--sector sportsbook`, sports-led peers; sports trading from user profiles | The fixture calendar |
| `prediction` | prediction_market | traders | odds line, blue | Contracts: `hidden-vip-packs` or `sales-reports` | A dated event: election, final, macro print |
| `exchange` | trading, cefi, cex | traders | candles, purple | `--sector exchange`; `whynow_sql.py` for switchers | A rival's hack or a licensing deadline |
| `perps` | derivatives, dex | traders | order-book depth, violet | Contracts: `hidden-vip-packs` or `sales-reports` | An incentive season ending, a liquidation event |
| `fx` | forex, cfd, broker | clients | currency waves, orange | Almost always proxy: `--sector brokerage` | A regulator's leverage or marketing rule |

Anything else gets the neutral profile (network motif, "users") and a lint warning: pick the closest type, or add
one.

How to use a profile: read its `hero_ideas`, `urgency_hooks` and `sample` before choosing the story, write in its
words, and keep its `avoid` list in mind (a broker has clients and positions, never players and bets; a prediction
market is trading, not gambling). The `sample` copy is a starting point with invented numbers, not text to ship.
A business that is two types at once (a casino with a sportsbook) takes the type of the product the buyer runs.

**FX and CFD brokers** need the most care. They are regulated, fiat-first and usually have no on-chain trail, so
the deck is proxy mode on brokerages and exchanges and must say so: the numbers describe active crypto traders in
the broker's markets, not the broker's book. The honest pitch is "these are the high-value traders you want as
clients, here is how they behave, and here is how to recognise them when they sign up".

To check the look after any change, or when adding a type:

```bash
python3 <skill>/scripts/vertical_preview.py <out dir>
```

It builds a four-slide fixture per type; render each with `render.js` and compare the covers side by side. To add
a type: add a profile to `assets/verticals.json` (and an alias if it has other names), add its drawing to `_motif`
in `build_deck.py`, add its sector to `insight_sql.py` if the deposit labels cover it, and run the preview.
