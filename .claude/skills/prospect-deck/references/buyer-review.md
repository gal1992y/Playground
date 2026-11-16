# The buyer: who reads this, and reviewing it from their seat

A deck is read by one person, at one company, in one language, with their own targets and their own way of being
sold to. Part A builds that person before any slide is written. Parts B and C say how the deck changes for them.
Part D is the review that proves it worked.

## A. The buyer dossier (step 1 of the workflow)

Fill the `buyer` block of `deck.json`. Ten minutes of looking beats any amount of guessing:

| Field | What to find | Where |
|---|---|---|
| `company` | What it sells, to whom, where it is licensed, its size and stage, its tone in public (playful, institutional, crypto-native), news in the last quarter | Its site, HubSpot company record, Similarweb (traffic by country, competing sites), the news sweep |
| `role` | The person's title and what they are measured on; who they report to; who they would forward this to | HubSpot contact, Apollo, LinkedIn, past meeting notes (Granola, Fireflies, Meetings), Slack |
| `language` | The language they work in, and the language of the company's own site and posts | Their LinkedIn, the site's default language, earlier emails |
| `market` | Where they sit and the market they sell into; its regulator; how business is done there | Company record, licence pages |
| `kpis`, `tone`, `notes` | Their own words from earlier calls; objections already raised; anything they said they do not want | Meeting notes, email threads |

If the user names a company but no person, write the deck for the most likely first reader (ask which, with the
role table in `cta.md`) and say so. If a fact is a guess, mark it as one in `notes`; do not present it to the
reviewer as known.

## B. Role lenses

The same data yields a different hero for each reader. Pick the hero and the path with this:

| Reader | Measured on | Wants to see | Is put off by |
|---|---|---|---|
| CMO, acquisition, growth | New depositing users, CAC, share of market | Reachable audience, where rivals' users are in play, momentum | Retention detail, method up front |
| CRM, VIP, retention | Second deposit, VIP revenue, churn | Hidden VIPs among existing users, shared loyalty, who to call first | Acquisition talk, vague "insights" |
| Product, data, BI | Segments, models, experiments | What fields they would get, how fresh, how it joins to their IDs | Adjectives, unexplained numbers |
| CEO, founder, commercial | Revenue, position against rivals | One number about concentration or wallet share, and the ask | More than six slides |
| Compliance, legal | Exposure | The method slide: aggregates, no personal data, sources | Anything that reads as surveillance of individuals |

Every reader asks the same three silent questions: *Is this about us? Is it true? What do I have to do?* The cover,
the method slide and the close answer them.

## C. Language and culture

**Language.** Write the deck in the language the buyer works in, from the first draft. Translating a finished
English deck produces English idioms in other words.

- Translate everything: slides, `labels` (kickers, "Prepared for", "Start here", "Confidential"), `date`, the share
  message. Keep product and venue names as they are written locally.
- Use the market's formats: decimal and thousands marks (1,296 / 1.296 / 1 296), currency placement, dates.
  Currency: keep USD figures in USD (it is what was measured) and say so once; do not convert silently.
- Use the industry's local words, not the dictionary's (how operators there say "player", "deposit", "VIP").
  When unsure, read the prospect's own site and reuse its terms.
- Right-to-left languages (Hebrew, Arabic, Persian, Urdu) flip automatically from `lang`. Check the PNGs: numbers
  and Latin names inside right-to-left lines are the usual place for mistakes.
- Check length after translating: German, Portuguese and Russian run longer than English. The budgets still apply.
  Cut words; do not shrink type.
- Scripts beyond Latin, Cyrillic and Greek use system fonts: confirm the PNGs show real glyphs, not boxes.
- If the buyer works in English at a non-English company, English is right. Record the reason in
  `language_decision` whenever the deck's language is not the buyer's first language.

**Culture.** These are questions to answer from what you know of this buyer and market, not rules about
nationalities. People differ more within a country than countries do from each other, so prefer evidence about
the person (how they wrote to us, how their company speaks in public) over generalities, and when you have none,
choose the more respectful option.

- **Directness of the claim.** Would this reader welcome "you can't see your own VIPs", or hear it as an insult to
  their team? The softer form states the fact without the accusation: "What one casino can't see about its players."
- **Directness of the ask.** "Share a sample" or "We would welcome 20 minutes with your team"? The specificity
  stays; the verb changes.
- **Pressure.** Does urgency read as helpful or as pushing? Where pushing costs trust, frame the why-now as an
  opening and leave the conclusion to them.
- **Naming rivals.** Is naming a competitor's incident normal here, or bad form, or legally touchy? When in doubt,
  describe it without the name and keep the name for the conversation.
- **Hierarchy.** Will the reader decide, or carry this to someone senior? If it travels upward, the deck must stand
  without a presenter and the method slide matters more.
- **Formality.** Titles, formal address (vous, Sie, usted, 您), first names, humour. Match how they addressed us.
- **Regulation and vocabulary.** A licensed operator, a listed company or a broker reads "whales", "degens" and
  "bets" very differently from a crypto-native team. The vertical profile lists words to avoid; the buyer's own
  site is the best guide.
- **Sensitive ground.** Gambling, leverage and crypto are restricted or stigmatised in some markets and for some
  readers. Stay on value and service to existing adult customers; nothing that reads as targeting the vulnerable.
- **Privacy and data law.** A buyer under GDPR, LGPD or similar reads any "user data" pitch through their privacy
  officer's eyes. The method slide says what the data is (public blockchain records, aggregates, no names or
  account data), and nothing on the slides asks them to send customer data casually.
- **Safer gambling.** For licensed gambling operators, "find the big spenders and send them offers" is a compliance
  problem. Put service and limits next to offers ("Tailor service, offers and limits"), speak of adults who already
  play, and never frame high spend alone as the target.
- **Money and law by their name.** Use the buyer's currency where the figure is theirs; keep measured USD figures
  in USD and say so. Name the actual regulator, law or ordinance, the way locals name it. "The Ministry" and
  "new licence rules" are an outsider's phrasing.
- **Proof.** Some readers want references and a method before any claim; others want the number first. Order the
  talk track accordingly, and never drop the method slide for a formal buyer.

Write the decisions into `buyer.tone` so the reviewer and the next editor can see them.

## D. The review loop (step 8)

The author cannot unsee the data. A fresh reader can. So the review is done by a new agent that gets only what the
buyer would get.

1. Start a fresh agent (general-purpose) with the text of `agents/buyer.md`, the `buyer` block, and the paths of
   the PNGs in `png/`. Give it nothing else: not the claims, not the query results, not why a slide exists, not this
   conversation. If the deck is not in English, tell it to read and answer in the deck's language, then summarise
   in English.
2. It returns: what it remembered after one pass, six scores from 1 to 5, the objections it would raise, what it
   would do next, and up to three fixes.
3. Fix what it flagged. Prefer cutting to adding. A fix that needs a new number goes back through `claims`.
4. Rebuild and review again with **another** fresh agent (a reviewer that has seen the old deck remembers it).
   Stop when every score is 4 or more and the takeaway matches the sentence you wrote in `story.md`. Three rounds is
   usual; if it takes more, the hero is wrong for this buyer: go back to step 4 of the workflow.
5. Record the last round in `deck.json`:

```json
"review": {
  "buyer": {"company": "Examplex", "role": "Head of CRM and VIP", "language": "en", "market": "Brazil"},
  "rounds": 2,
  "scores": {"relevance": 5, "clarity": 5, "credibility": 4, "urgency": 4, "fit": 4, "action": 5},
  "verdict": "pass",
  "takeaway": "Some of my small depositors are big players elsewhere and I cannot see them.",
  "changes": ["Round 1: 'whales' replaced with 'VIPs'", "Round 1: cover no longer leads with Addressable"],
  "open_objections": ["How do you match my players without personal data?"]
}
```

The scores, in the buyer's words:

| Score | The buyer's question |
|---|---|
| `relevance` | Is this about my business and my targets? |
| `clarity` | Did I get it in one pass, and can I repeat it? |
| `credibility` | Do I believe the numbers and the source? |
| `urgency` | Is there a reason to deal with this now and not next quarter? |
| `fit` | Does it sound like it was written for someone like me, in my language, the way business is done here? |
| `action` | Do I know exactly what the next step is, and is it small enough? |

What the first review of this skill's own sample caught, so check these before spending a review round: peers that
are not really like the prospect; "your players" on data about other companies; a number with no base; a change with
no baseline; an ask that needs the buyer's customer data; a generic contact; a method line that raises more doubt
than it settles.

Never write the review block yourself to get past the lint. If no review ran, say so and deliver the deck as a
draft. The `open_objections` are not failures: they go to the user as the first questions to expect on the call.

When the deck will be forwarded (most are), run one more fresh reader as the person it goes to (the buyer's boss,
or the analyst who checks the numbers) and fix what blocks them. The method slide usually decides that one.

## Standing objections: answers come from the user, not from you

Two review rounds on this skill's sample ended on the same questions, and they will come up with real buyers. They
cannot be fixed with wording, and guessing the answer is inventing product facts. Ask the user for the approved
answer once, record it here, and put it on the method slide or in the notes:

| The buyer asks | Approved answer |
|---|---|
| "If you can see what my users do at rivals, can rivals target my users? Is my company in your data?" | *not recorded: ask the user* |
| "How do you match one of my users, what do I have to provide, and what share will match?" (No match-rate figures on slides: guardrail) | *not recorded: ask the user* |
| "The method says aggregates only, the product enriches individual profiles. Which is it?" | *not recorded: ask the user* |
| "Who else uses this, and what did it do for them?" (Never name a client without the user's OK) | *not recorded: ask the user* |
| "What does it cost and how long to integrate?" | *not recorded: ask the user* |

Until an answer is recorded, list the question under `open_objections` and tell the user it will be asked. A deck
whose only remaining gaps are these may go out as the user decides; say plainly that the review did not pass and why.
