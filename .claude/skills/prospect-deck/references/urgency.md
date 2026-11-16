# Why now

Urgency is the difference between "interesting" and "let's talk this week". It has to be true, dated and theirs.
Invented urgency costs the deal and the next one, so the rule is: a deck with no why-now is acceptable; a deck with
a stretched one is not.

## Three sources, in order of strength

| Source | Example | What makes it usable |
|---|---|---|
| **An event near the prospect**, last 60 to 90 days | A rival's outage, hack, frozen withdrawals, licence loss, product withdrawn from a market; the prospect's own launch or licence | Verified: date, figure at the source's precision, two independent sources or one primary. Follow `prospect-deck-check/references/why-now.md` end to end (sweep, verify, measure, word) |
| **A trend in our own data** | "412 new hidden VIPs appeared in the last 30 days"; "1 in 5 of a rival's depositors funded another casino in two weeks"; depositors at a rival up 11% in a month | A real query result with its artifacts ruled out (`data-playbook.md` section 4). Needs no news, so it is always available |
| **Macro** | A regulator's deadline, a tax or marketing rule, a tournament or election date, a market regime change | A primary source and a date. Only counts when the deck connects it to the prospect's users in one line |

The strongest slide pairs one event with its measured effect: the event says *something changed*, the number says
*and it is already moving the people you want*. Use `prospect-deck-check/scripts/whynow_sql.py` for the before and
after (run its coverage query first) and `insight_sql.py` momentum for the sector trend. Each business type has its
own likely hooks: `assets/verticals.json` (`urgency_hooks`).

## Rank the candidates

Score each candidate and keep at most three for the slide, ideally one or two:

- **Close:** about the prospect itself (3), a direct rival (2), its market (1), the whole industry (0).
- **Recent:** inside 30 days (2), inside 90 (1), older (0). A future date with a deadline scores 2.
- **Measured:** we can show its effect in our data (2), we can show the population it affects (1), neither (0).
- **Verified:** required. Unverified candidates are listed for the user and never reach a slide.

## Say it as a window, not a threat

The form is: **what changed, who is in play, how long the window is.**

- "Rivalbet paused withdrawals on 22 Oct. In the two weeks after, 1 in 5 of its depositors funded a different
  casino. Most have not chosen a new home yet."
- Not: "Players are fleeing Rivalbet. Act now before your competitors do."

Rules that keep it credible:

- Report what was measured. "Funded a different casino", not "left" or "switched", unless switching was measured.
- Keep the inconvenient half: "the money slowed but hasn't moved" is what makes the window believable.
- Neutral about the rival. An incident is bad news for real people and those people are the prospect's future
  customers. No gloating, no claims about anyone's security or solvency beyond the sources.
- If the rival is an Addressable client (check HubSpot), ask the user before naming it.
- Small counts are flagged or left out. Nothing under 3 people.
- No fear framing for regulated or formal buyers, and none where the culture reads pressure as disrespect
  (`buyer-review.md`): there, the same fact is an opening ("a window") rather than a risk ("you are losing").
- **Check the window against the send date.** A two-week effect measured to 4 Nov is past tense on 16 Nov. Either show
  what is still open (how many have not settled anywhere), or present it as a pattern that repeats ("when a rival
  stumbles, 1 in 5 look elsewhere within two weeks") and drop "now".
- Dates as the buyer writes them (22 Oct / Oct 22 / 22.10), in the deck's language.

## When the sweep finds nothing

Use the data trend alone and title the slide for it ("412 new hidden VIPs this month"). If the data has no honest
trend either, drop the slide, set `urgency_skipped` to the reason, and tell the user what was searched. Record the
sweep (including searches that found nothing) with the deck so "nothing found" is a result and not a gap.
