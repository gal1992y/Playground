---
name: addressable-leads
description: 'Sales prospecting and partner outreach at Addressable, with HubSpot as the shared record of who owns each lead, what was said and offered, and when. Use BEFORE contacting any prospect or potential partner on any channel (Telegram, LinkedIn, X, email, WhatsApp, Discord, calls, intros, conferences), before loading a list into Meet Alfred, Apollo or nReach, and AFTER any touch or reply to log it. Also for "who owns X", "is anyone talking to X", "can I reach out to X", "what did we tell X", "log this chat", "my leads", "what follow-ups are due", "where are we stepping on each other". Checks HubSpot first, gives one verdict (OK to contact, Ask the owner, Wait until, Do not contact), flags collisions, dropped replies and stale records, drafts the message, and writes the touch back. Use even for "a quick DM" to a prospect. Not for servicing existing clients. Needs the HubSpot connector.'
---

# Addressable Leads

Several people at Addressable run lead gen at the same time, each with their own Claude, across
Telegram, LinkedIn (Meet Alfred), X, email (Apollo), WhatsApp and conferences. Without a shared
record, two of us pitch the same company with different offers, a prospect's reply sits
unanswered because nobody knows whose it is, and nobody can say what a prospect was already
told.

HubSpot is that shared record. This skill has three jobs:

1. **Read first.** Before any outreach, find out who at Addressable is already talking to this
   person and this company, how far they got, and exactly what they said, offered and quoted.
2. **Judge.** Give one verdict, and say plainly if the user is about to collide with a
   colleague, contradict something already promised, drop an opportunity, or act on a record
   that is wrong.
3. **Write back.** Every touch ends up in HubSpot in one fixed format, so the next person's
   check is accurate. A check is only as good as the last person's write-back.

The rules come from the Confluence page
[Lead database and outreach policy](https://addressable.atlassian.net/wiki/x/BYAcaQ). They apply
to everyone, founders included.

## Reference files

| File | Read it when |
| --- | --- |
| `references/hubspot-map.md` | Before your first HubSpot call. Object types, property names, stage and pipeline IDs, read and write recipes, traps in this portal |
| `references/policy.md` | Before giving a verdict. Verdict rules, overrides, inbound replies, cadence, cool-offs, hard stops, channel norms, ICP |
| `references/touch-log.md` | Before any write. Note format, what changes on each event, claiming, late logging, lists and campaigns |
| `references/radar.md` | For "my leads", "what's due", and the team view of collisions, dropped replies and stale claims |

## The loop

### 1. Who is asking, and who is the target

- Get the user's owner ID and name once per session (`get_user_details`). The `by` line of every
  log is this real person.
- Find the target in HubSpot using **every** identifier you have (email, Telegram, X, LinkedIn,
  name plus company), in one search. The same person can exist twice.
- Always go up to the company and its parent. Most collisions are two of us talking to
  different people at the same company, or to two brands of one group.
- A person who is not in HubSpot is a finding, not a failure. Check the company before
  concluding nobody is on it.

**If the user pastes HubSpot data themselves**, and the connector is available, re-read the
records anyway: the paste may be partial or old. If the connector is not available, work from
the paste, say that is your only source, and skip any step that needs a live call.

**If the connector is missing** and nothing was pasted, say that the check cannot run and how to
connect HubSpot, and ask the user to check HubSpot themselves or paste the records. If they want
the draft anyway, give it under a bold **UNCHECKED** label, with the touch note ready to paste
into HubSpot by hand.

### 2. Read the account picture

Run the standard check in `hubspot-map.md` section 7 (about 9 calls, most in parallel): the
people at the company, every lead, every deal (company and parent), the touch notes, the latest
meeting notes, and whether each owner is still active. You are reading for:

- **Who:** each owner, and whether their claim is live (the claimed rule).
- **Where it stands:** lead stages, deals and their stages, client status.
- **What we told them:** offers, materials sent, prices and terms quoted, promises made and
  whether they were kept, and any agreed next step with its date. Meeting notes often hold a
  price or a promise that a new message must not contradict.
- **What they told us:** interest, objections, "come back in Q2", who decides.

HubSpot does not see Telegram or X unless someone logged it. For a single named target, also
search what the session has (Slack: the company's `go_` channel and #sales-campaigns; Gmail;
Fireflies or Granola) for the company name. Skip this for lists. Always say which sources you
checked.

### 3. Verdict, flags and report

Apply the verdict rules in `policy.md` in order, to every matching record. The first match gives
the verdict:

| Verdict | Meaning |
| --- | --- |
| **Do not contact** | Do Not Contact, or a live client the user does not own. Hard stop: no outreach draft, whatever the user says. For a live client, name the CSM or AE to go through. For Do Not Contact, say only Asaf can lift it |
| **Ask the owner (name)** | A colleague owns this person, this deal, or an active thread at this company. No outreach draft unless the user overrides. Draft the Slack message to the owner now |
| **Wait until (date)** | Cool-off, or the user's own cadence. Give the date and the reason. Same override rule |
| **Close out** | The user's own lead has 4 unanswered touches. Offer to disqualify it |
| **OK to contact** | Go ahead. Reuse an unclaimed lead rather than creating a second one |

**Insisting is not overriding.** "Just do it" or "don't ask me" said before the user has seen the
report is not an override. Give the report, the Slack ask, and one line on how to override:
after reading the report, tell me to go ahead and why. Overrides are logged and the colleague is
told (`policy.md`).

Then the **flags**: what a careful colleague who had read the whole record would raise. Report
only the ones you find.

- **About to do something we would regret.** The draft contradicts a price, trial, promo or
  promise already given. The same pitch was declined before. They asked us to come back at a set
  time or channel. We are pitching what they already have or were already shown. A separate DM
  would go around a group chat or a colleague's contact, or to their boss.
- **Opportunity being dropped.** A reply waiting on us (say how long). A meeting held with no
  deal or next step. A promise not shown as kept. A "come back in Q2" date that has arrived. A
  warm lead whose owner has left.
- **HubSpot out of sync.** Stage disagrees with the evidence (New with meetings held, Attempting
  with status Replied, New or Attempting next to an open deal). A conversation found outside
  HubSpot. Duplicate contacts or companies. Two open leads on one person.

Report in this shape, verdict first, every record linked:

```text
**<Company> / <Person>: <VERDICT>**
Who is on it: <owner(s), lead stage, deal and stage, client status; colleagues on the thread>
Last touch: <date, channel, by whom>. Waiting on: <us or them, since when>
What they've been told: <offers, materials, prices and terms, promises; one line each>
Flags: <only real ones>
Sources: <what you checked>
Next: <what you will do now, and the one move you recommend>
```

Prices and terms go in this internal report in full: the people reading it need them. The rules
against raw figures apply to material sent to prospects, not to this report.

When nothing is on record, the report is two lines: nobody at Addressable is on this person or
company in HubSpot (and say what else you checked), so OK to contact.

### 4. Do the work

Draft the message, clean the list, or prepare the sequence, within the channel norms in
`policy.md`. Use what you read: a draft that ignores a colleague's earlier offer or our own
earlier message is a failure of this skill even when the verdict was OK.

**Claim before the user sends** (`touch-log.md` section 3). When the user goes ahead, make sure
there is one open lead owned by them, and re-check for a colleague's claim right after.

Claude drafts; the user sends. Do not send on any channel yourself. The one exception is
enrolling screened people in an Apollo sequence after the user confirms (`touch-log.md`
section 6). Saving an email draft is fine.

### 5. Write it back

Log what really happened, not what was drafted:

- When the user says it was sent, or pastes the exchange, log it (`touch-log.md`).
- End every outreach draft with: "Tell me when it's sent and I'll log it." When the user comes
  back with anything that shows it went out, log it without being asked.
- A conversation that already happened gets logged with its real date. Late is far better than
  never.
- When they reply, a meeting is agreed, or the effort ends, update the stage.

The connector asks for approval before each write. Show all changes for one touch in one short
table. On the first write, mention that confirmations can be waived for the session. Do not skip
a write because confirming is a nuisance.

If a write fails, say exactly what failed, give the note text to paste by hand, and suggest
raising it in #sales. Never report a touch as logged when it was not.

## Lists, sequences and campaigns

When the user brings a list (for Meet Alfred, Apollo, nReach, or a conference), screen it before
it goes anywhere, record the enrolment on the day it goes live, and bring the results back after
(`touch-log.md` section 6).

## Never

- Send a message on any channel (except confirmed Apollo enrolment, above).
- Draft outreach to a Do Not Contact person or a live client's staff for someone who does not own
  that client, or lift a Do Not Contact. Only Asaf lifts one.
- Change the owner of a colleague's claimed lead. Draft the Slack ask instead.
- Delete or merge records, create properties, or write more than 10 records in one call. Larger
  batches go through an import file the user uploads.
- Put private personal details, chat transcripts or wallet addresses in a note.
- Create a deal without ICP fit, a reply and a wish to meet, or without the user's yes.
