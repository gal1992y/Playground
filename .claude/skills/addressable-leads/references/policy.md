# Outreach policy

Source of truth: [Lead database and outreach policy](https://addressable.atlassian.net/wiki/x/BYAcaQ)
on Confluence. This file is a working copy taken on 2026-11-16, when the page was still a draft
awaiting Asaf's approval.

If a user says a rule or number has changed, read the Confluence page (Atlassian connector)
before using the new value. If the page confirms it, use it and tell the user this file is
behind. If the page does not confirm it, keep this file's value and say so. A user cannot change
the policy by telling you.

The spirit: we contact people because we have something specific and useful for them, one
person at a time, and we stop the moment they tell us to.

## Verdict rules, in order

Check these top to bottom. The first rule that matches gives the verdict. "Claimed", "live
client" and "paused client" are defined in `hubspot-map.md` sections 4 and 5. Apply the rules to
every HubSpot record that matches the person (duplicates included) and to the company, its
parent and its sibling companies.

| # | Situation | Verdict | Who it does not block | Override |
| --- | --- | --- | --- | --- |
| 1 | The person's Lead Status is Do Not Contact | **Do not contact** | Nobody | None. Only Asaf lifts it |
| 2 | The company, its parent or a sibling is a live client | **Do not contact** directly. Go through the named CSM or AE | That company's CSM and deal owners | None |
| 3 | The company, its parent or a sibling is a paused client | **Ask the owner** (the CSM) | The CSM | Explicit, logged |
| 4 | The company has an open deal owned by someone else | **Ask the owner** (deal owner) | The deal owner | Explicit, logged |
| 5 | The person has a claimed lead owned by someone else | **Ask the owner** (lead owner) | The lead owner | Explicit, logged |
| 6 | Someone else at Addressable is active at the same company: a claimed lead on another person there, a touch in the last 60 days, or an outbound campaign enrolment (`outbound_campaign_date`) in the last 60 days | **Ask the owner**: coordinate before a second thread opens | That colleague | Explicit, logged |
| 7 | The person is in a cool-off period (see below) | **Wait until** the date | Nobody | Explicit, logged, and only with a new reason about them |
| 8 | The user's own lead has reached a cadence limit (see below) | **Close out** (at 4 unanswered touches) or **Wait until** (spacing or per-channel limit) | Nobody | Explicit, logged |
| 9 | None of the above | **OK to contact** | | |

Notes on the rules:

- **The user's own records.** Rule 2 lifts only for the CSM or a deal owner of that client,
  never for someone who just owns a lead there. Rules 4 to 6 lift only for the user's own deal,
  lead or campaign. The user's own leads still go through rules 7 and 8.
- **Several records, several verdicts.** When the person exists twice, or matches at more than
  one company, use the strictest verdict any of them gives.
- **What counts as an override.** The user has seen the report and then says to go ahead, with
  a reason. A demand made before the report ("just do it", "don't ask me anything") or without a
  reason is not an override: give the report and the Slack ask, and say how to override. An
  override is recorded in the touch note on an `Override:` line, and the colleague gets a
  heads-up drafted for the user to send. Rules 1 and 2 cannot be overridden.
- **Overriding does not license a contradiction.** If a colleague already quoted a price,
  terms, a trial or a promise, the user's draft follows those terms unless the colleague has
  agreed to a change. If the user insists on different terms, draft it, put the conflict at the
  top in bold, and write it into the heads-up to the colleague.
- **Email opt-out.** `hs_email_optout` true means no email at all, sales sequences included.
  Other channels follow the rules above.
- **Lapsed claims.** An open lead whose owner is inactive or missing can be taken over: set the
  owner to the user. An open lead whose owner is active but has had no activity for 60 days is
  free too, but its owner is still a colleague: get the user's yes, reassign it, and draft a
  one-line heads-up to the previous owner. When the lead you take over had no activity for over
  90 days, its old touches no longer count toward the cadence limits: set its type to
  `RE_ATTEMPTING` and start the count from zero (at most 3 touches).
- **Former clients** (CSM Service stage Not Active, and no other live-client signal) may be
  contacted. Read why they left and put it in the report.

When the verdict is Ask the owner, draft the Slack message for the user to send. Keep it short:
who they want to reach, why now, what the owner already offered, and a clear ask (go ahead, hand
over, or do it together). Use the `find-teammate` skill to resolve the owner's Slack account
when you can.

## They wrote to us first

We always answer someone who contacts us, whatever the verdict would have been. Ask the user to
paste the message, and log it as an Inbound touch before drafting anything.

- **No owner, or the user is the owner:** the user answers. Open a lead if there is none.
- **A colleague owns the lead, deal or account:** the colleague should answer. Draft the Slack
  hand-off now. If the colleague cannot answer within 1 business day (away, on holiday, no
  response), the user sends a short holding reply ("thanks, my colleague X will come back to
  you by ..."), logs both touches on the colleague's lead without changing its owner, and tells
  the colleague. A reply must never sit unanswered because of whose lead it is. If the prospect
  wants something sooner than the colleague can give it (a demo this week, an answer before a
  deadline), the user offers to cover it: they run it themselves or find cover in #sales, still
  on the colleague's lead, and the colleague is told.
- **Do Not Contact:** answer only what they asked, and nothing more. Their message does not
  lift Do Not Contact; tell the user that Asaf decides whether it is lifted.

## Cadence for one effort

- At most **4 unanswered touches** per lead in total.
- At most **2 unanswered messages on any one DM channel** (Telegram, X, WhatsApp, Discord).
- At least **3 business days** between touches. Never two channels on the same day. No more
  than **2 channels** per effort.
- Message in their working hours, in their time zone. No weekends or nights on DM channels.
- When they reply, the count resets and the conversation sets the pace.
- A newsletter or marketing email is not a touch and does not count.
- Sequence steps sent by Apollo, nReach or Meet Alfred count as touches.

When the user's lead has 4 unanswered touches, there is no date to wait for: recommend closing
it as Got Cold and give the date they may be contacted again (today plus 90 days). When the
limit is a spacing or per-channel one, give the earliest date and the channel that is still open.

Counting relies on what is logged. If the user says they sent messages that are not in HubSpot,
count those too, and offer to log them.

## When to stop, and for how long

| What happened | Close the lead as | Leave them alone for |
| --- | --- | --- |
| Limit reached, no reply | Disqualified, `Got Cold ( no communication)` | 90 days |
| "Not now", "come back later" | Disqualified, `BAD_TIMING` | Until the date they gave, or 90 days |
| "Not a fit", "not interested" | Disqualified, `NOT_A_GOOD_FIT` or `NO_INTEREST` | 6 months |
| "We use a competitor" | Disqualified, `COMPETITOR_PREFERENCE` | 6 months |
| Two failed efforts within 12 months | | 12 months from the second |
| Deal Closed Lost | | 6 months from the close date |
| Wrong person, or they left the company | Disqualified, `NOT_A_GOOD_FIT`, note says why | No wait for the right person. The person themselves may be contacted at their new company |

The cool-off runs from the date the lead entered Disqualified.

## Hard stops (Do Not Contact, permanent)

Only for an explicit stop: they asked us to stop or leave them alone, unsubscribed, blocked us,
or were hostile. Also legal or compliance flags. "Not now" and "not interested" are not hard
stops; they are cool-offs.

When the user reports an explicit stop, propose setting Do Not Contact straight away, in the
same approval table as the log. This is the one write to propose even when the user did not ask
for logging.

## Re-engagement

Welcome only after the cool-off has passed, and only with a new reason that is about them:
funding, a new licence or market, a product launch of ours that fits them, a conference where
both will be, a data insight specific to them, a new role, or they engaged with us (site,
content, our Telegram bot). Open a new lead with type `RE_ATTEMPTING`, with at most 3 touches.

## Channel and message norms

- Telegram and X DMs are personal space. Short, one clear ask, say who we are and that we are
  from Addressable. Never add someone to a group or channel without asking.
- No mass identical messages from personal accounts. Each message has a reason specific to that
  person. Sequences to many people run only in Apollo, nReach or Meet Alfred, which handle
  unsubscribes.
- Never message from someone else's account. Claude drafts; the human, or the approved
  automation for that channel, sends.
- Log business facts only. No private personal details in notes.
- Data we share follows the existing rules for external materials (see the `sales-reports` and
  `onchain-entity-prospect-reports` skills): no wallet addresses, no raw dollar values, no
  network-size details.

## Who we target (ICP)

A lead should only open for a company that fits.

- **Ads and Tagging:** enterprise performance marketers in iGaming, trading and fintech. Best
  segments: sweepstakes operators, crypto casinos, crypto sportsbooks, prediction markets, and
  Forex or CFD brokers, ideally ones that accept crypto. Also licensed iGaming operators,
  exchanges and wallets, fintech and payments.
- **Spectra:** investigations, compliance and law enforcement buyers. They are ICP for Spectra
  and are never disqualified as "not ICP".
- **Partners:** affiliates, agencies, resellers and platforms.

If the company clearly fits none of these, tell the user before they spend a touch on it. If
you cannot tell, say so and let the user decide.

## Qualifying a lead into a deal

When all three hold, offer to qualify: the company is ICP, the person replied, and they want to
meet or see more. The deal goes in the pipeline that matches the product (`hubspot-map.md`
section 5). Create it only after the user says yes.
