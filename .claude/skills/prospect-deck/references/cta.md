# The ask: two paths, one next step

Every deck ends by offering the same two things Addressable does with this data. Both are always shown, so the
buyer sees the whole offer and can forward the deck to the other team; one is marked "Start here" for this buyer.

## The two paths

**Enrich** (data enrichment): add what users do elsewhere to the profiles the prospect already holds.

- **VIP identification:** flag high-value users at signup, before their first large deposit.
- **Segmentation:** group users by real value and activity across venues, not by what they did on one site.
- **Personalisation:** fit the first offer, bonus, fee tier or message to what the user actually does.

**Advertise:** reach people who are already active at comparable venues, in the prospect's markets, instead of cold
traffic.

Write each path as an outcome in the vertical's words (`assets/verticals.json` has starting points for each
business type): "Know every player on day one", "Reach proven bettors". Three points per path, six words each.
Describe only what Addressable does today: if unsure whether a capability, integration or market is available,
ask the user rather than writing it.

## Which path is primary

| Buyer | Starts with | Because they own |
|---|---|---|
| CMO, Head of Acquisition, Growth, Performance, Affiliates | Advertise | New depositing users, CAC |
| Head of CRM, VIP, Retention, Loyalty | Enrich | Second deposit, VIP revenue, churn |
| Product, Data, BI, Personalisation | Enrich | Segments, models, experience |
| CEO, Founder, COO, Commercial | Whichever the hero number points at | Revenue; they forward it to the owner |
| Compliance, Legal (rarely the first reader) | Enrich, with the method slide strong | Whether this is allowed |

If the hero is about the prospect's existing users (hidden VIPs, shared loyalty), Enrich is the natural start. If it
is about people who are not users yet (reachable audience, a rival's unsettled depositors), Advertise is. When buyer
and hero disagree, change the hero: a CRM lead should not get an acquisition deck.

## The next step

One ask, one sentence, small enough to accept by reply. In order of how little it costs the buyer:

1. **See your own market:** a 20-minute walkthrough of this analysis for their market and rivals. It needs nothing
   from them, so it is the default first ask.
2. **Share a sample:** they send a sample of users (or wallets, or their omnibus); we return who is a hidden VIP.
   It turns "companies like yours" into "you", but it is a transfer of customer data: for most buyers, and every
   regulated one, it needs legal and a data agreement, so it is the *second* step. Make it the ask only when the
   buyer already offered it (then set `data_ask_ok` in `deck.json`), and say in the notes what is shared, how it is
   protected and under which agreement. The lint blocks a data ask as the first step otherwise.
3. **Size an audience:** we show how many proven users are reachable in their markets.
4. **A named follow-up** agreed with the user (a pilot, a test campaign).

Rules:

- **Never invent commercial terms.** No prices, discounts, free pilots, trial lengths, guarantees or delivery times
  unless the user gave them for this prospect. If the user has standing offers, they belong in this file.
- One ask per deck. Two asks get neither.
- "Small" is judged from the buyer's side: time, approvals and risk, not from ours.
- A real person on the close: name, role, a direct email and a booking link when there is one. Never a generic
  inbox alone. Ask the user whose name goes on it.
- The ask is a verb the buyer does ("Share", "See", "Book"), not "Learn more" or "Contact us".
- In formal or hierarchical settings, soften the verb, not the specificity: "We would welcome 20 minutes to walk
  your team through your own numbers."

## Standing offers

None recorded. Add confirmed offers here (what, for whom, any limit, who approved, date) so decks can use them
without asking each time.
