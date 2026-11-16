# Writing back to HubSpot

Every touch, on any channel, becomes a note on the lead in a fixed format, plus a few field
updates. The format is fixed so the next person's Claude can read it reliably. People can write
the same note by hand. Payload shapes are in `hubspot-map.md` section 8.

## Contents

1. The touch note
2. What to write on each event
3. Claiming: contact, company and lead
4. Logging a conversation that already happened
5. Closing out
6. Lists and campaigns (Meet Alfred, Apollo, nReach, conferences)
7. Approval and failures

## 1. The touch note

```text
LEADTOUCH | 2026-11-16 | Telegram | Outbound | by Keith Hutchison
Context: Ads | Conference (SiGMA Rome) | campaign: none
Offered: On-chain prospect report (Brazil depositors)
Shared: report PDF link; no pricing quoted
Said: congratulated on the Brazil licence, offered the depositor overlap report
Reply: none yet
Next: follow up on or after 2026-11-19 if no reply
```

| Line | Required | Content |
| --- | --- | --- |
| Header | Always | `LEADTOUCH`, the date the touch happened (YYYY-MM-DD), channel, direction, `by` the full name of the Addressable person who sent our message, or for an Inbound note, who received and handled theirs. Keep `LEADTOUCH` exactly: searches depend on it |
| `Context:` | First touch of a lead | `product | origin | campaign: name` (write `campaign: none` when there is none). Later touches may omit it |
| `Offered:` | Outbound and Meeting | The specific value we put in front of them, in words, not a category |
| `Shared:` | When anything was sent or quoted | Materials, links, prices, discounts, promo codes, trial terms, promises and their dates. Exact numbers. This line stops a colleague contradicting us later |
| `Said:` | Always | One line on our message |
| `Reply:` | Always | `none yet`, or their answer in one line, with its date if different from the header |
| `Next:` | Always | The next step and its date: "on or after" for a follow-up we are waiting to send, "by" for something we owe them, `none` when closing |
| `Override:` | Only when a verdict was overridden | Which verdict, the user's reason, and that the colleague was told |

Allowed values:

- **Channel:** Telegram, X DM, LinkedIn, Email, WhatsApp, Discord, Phone, Video call, In person.
- **Direction:** Outbound (we wrote), Inbound (they wrote first), Meeting (a call or meeting
  held). A meeting's channel is Video call, Phone or In person.
- **Product:** what we are ultimately trying to sell them: Ads, Tagging, Spectra, Data
  enrichment, or Partnership (agencies, affiliates, resellers, platforms). A report or data
  story is what we offered, not the product: put it on `Offered:`. If the product is unclear,
  use the campaign's product, else the product that fits the company's ICP segment
  (`policy.md`), and tell the user which you chose so they can correct it.
- **Origin:** how we found them: Conference, Inbound, Intro or referral, On-chain research,
  Data story or PR, Community or Telegram group, Apollo list, nReach, Meet Alfred, Agent
  sourced, Other. A cold message that mentions an event uses Conference only if we found them
  through the event (its attendee list, a meeting there). If you cannot tell how we found them,
  use Other and say so.

Keep it to business facts. Summarise; do not paste the conversation. No private personal
details and no wallet addresses. Prices and terms we quoted belong in `Shared:`.

The note is a `NOTE` with `hs_note_body` (lines joined by `<br>`), `hs_timestamp` (when the
touch happened), and associations to the **lead**, the **contact** and the **company**.

**One note or two.** One note per touch. A reply that came the same day as our message goes on
that note's `Reply:` line. A reply on a later day gets its own Inbound note, and our same-day
answer to it goes on that Inbound note's `Said:` line. A long exchange on one day is one note
that summarises it.

## 2. What to write on each event

| Event | Note | Lead stage | Contact Lead Status |
| --- | --- | --- | --- |
| User decides to reach out | None yet | Claim: one open lead owned by the user, New (section 3) | Unchanged; create the contact if missing |
| Message sent, no reply | Outbound | Attempting | `ATTEMPTED_TO_CONTACT` |
| They replied | Inbound, or `Reply:` on a same-day note | Connected | `REPLIED` |
| A meeting time is agreed by both sides | Note the agreed time | Connected | `MEETING_BOOKED` |
| Meeting held | Meeting note: what we offered, shared, and agreed | Connected (or Qualified, section 5) | `MEETING_BOOKED` until qualified |
| They wrote to us first | Inbound | Open a lead if none, Connected | `REPLIED` |
| Qualified | Note with `Next:` naming the deal | Qualified, deal created | `OPEN_DEAL` |
| Stopped | Final note, `Next: none` | Disqualified with reason and note | `UNRESPONSIVE` (no reply), `BAD_TIMING` or `UNQUALIFIED` to match |
| Explicitly asked us to stop | Final note stating so | Disqualified | `DO_NOT_CONTACT` |

A prospect asking to meet is not booked until a time is agreed: until then the status is
`REPLIED` and `Next:` says what we owe them.

Rules:

- Never move a stage backwards. Never overwrite a Lead Status of `DO_NOT_CONTACT`, `OPEN_DEAL`
  or `MEETING_BOOKED` with a weaker one.
- **Label** (`hs_lead_label`): set `HOT` when they asked for pricing, a proposal or a meeting;
  `WARM` when they replied with interest; leave it unset otherwise.
- **Contact owner:** set it to the user only when it is empty. Never change a colleague's
  contact owner.
- If the proposed dedicated fields exist (`hubspot-map.md` section 10), fill them in the same
  write.

## 3. Claiming: contact, company and lead

Claim as soon as the user decides to go ahead, before the message is sent, so a colleague who
checks afterwards sees it. Stop creating as soon as you find an existing record.

1. **Company.** Find it by association, domain or name. Create only if truly missing, with
   `name` and `domain`.
2. **Contact.** Find it by every identifier. Create only if missing, associated with the
   company. Store handles clean: lowercase, no `@`, no `t.me/` or `x.com/` prefix. Do not
   overwrite a handle that already holds a different value: tell the user. If the touch is on
   Telegram and the handle is missing, ask for it once.
3. **Lead.** Search for leads on the contact (on every duplicate contact too).
   - An open lead owned by the user: use it.
   - An open lead that is unclaimed: reuse it. Set the owner to the user (see "Lapsed claims"
     in `policy.md` for when to ask first).
   - An open lead claimed by someone else: stop. That is an Ask the owner verdict.
   - Only closed leads, or none: create one. Name `First Last YYYY-MM`, type `NEW_BUSINESS`
     (or `RE_ATTEMPTING` when a closed lead exists), associated with the contact (required)
     and the company. Create it directly at the stage the facts support: New for a fresh claim,
     Connected when you are logging a conversation in which they already replied.
4. **Check for a race.** Right after creating the lead, search the contact's leads once more.
   If another open lead appeared (a colleague claimed in the same minute, or the lifecycle
   workflow made one), the lead with the earlier `hs_createdate` keeps the claim. If that is a
   colleague's, tell the user it is now an Ask the owner, and disqualify the newer lead with
   the note "Duplicate".

Never leave two open leads on one person.

**If the user declines to claim** ("just draft it, I'll deal with HubSpot later"): give the
draft, say plainly that colleagues cannot see this outreach until it is logged, give the touch
note ready to paste, and offer again when they say it was sent.

## 4. Logging a conversation that already happened

People often talk first and tell Claude afterwards. When the user pastes a chat, a screenshot or
an email thread, or describes what happened:

1. Work out each touch: date, channel, direction, and who on our side sent it. If a date is
   missing, ask once. Do not guess a date.
2. Run the normal read (steps 1 to 3 of the loop). The conversation already happened, so the
   verdict cannot block it. Label the report **Logged after the fact** instead of a verdict, and
   still report any collision: the owner needs to know.
3. Write in this order: the lead (section 3), then one note per touch, oldest first, each with
   its real date in the header and in `hs_timestamp`, then one update for the lead stage and
   the contact status where the conversation ended.
4. If they are waiting on us (a question, pricing, a meeting time), lead the report with that.

When the conversation belongs to a colleague's lead, log the notes on that lead and do not
change its owner.

If the user reports several conversations at once ("log my Telegram chats from this week"), do
one person at a time with one approval table each.

## 5. Closing out

**Qualify.** Check the three conditions in `policy.md`. With the user's yes: create the deal in
the pipeline for the product at its entry stage (`hubspot-map.md` section 5), owned by the user
or the AE they name, associated with the contact, the company and the lead. Then move the lead
to `qualified-stage-id` and the contact to `OPEN_DEAL`. Name the deal the way existing deals in
that pipeline are named: look at two recent ones first.

**Disqualify.** Set the stage to `unqualified-stage-id`, `hs_lead_disqualification_reason` to
the matching value, and `hs_lead_disqualification_note` to one line with the specifics and the
date they may be contacted again. Tell the user that date.

**Do Not Contact.** Only for an explicit stop (`policy.md`). Set the contact's Lead Status to
`DO_NOT_CONTACT`, disqualify the open lead, and write the reason in the note: asked to stop,
unsubscribed or blocked, hostile, or legal or compliance. If the person is in an Apollo,
nReach or Meet Alfred campaign, tell the user to remove them there too: a running sequence
does not read HubSpot on its own.

After a lead is Qualified or Disqualified it cannot be edited by a normal user. Check the
reason and note before you write them.

## 6. Lists and campaigns (Meet Alfred, Apollo, nReach, conferences)

### Before: screen the list

For any list the user is about to load into a tool or work through by hand:

1. Match every row to HubSpot in batches (`hubspot-map.md`, "Screening a list"): by email, by
   LinkedIn slug or handle, and every company by domain.
2. Run the verdict rules on each matched row and sort it:
   - **Nothing in HubSpot:** stays in. (HubSpot not knowing them does not prove nobody has
     spoken to them; say so once in the summary.)
   - **Yours:** the user already owns the lead. Stays in; show the touch count.
   - **Ask the owner:** out, grouped by owner so the user can send one Slack message per
     colleague.
   - **Wait:** out, with the date.
   - **Do not contact:** Do Not Contact, live client, or email opt-out for an email sequence.
     Out.
   - **Not ICP:** flagged for the user to decide.
3. Give the clean list as a file in the tool's upload format, the excluded rows with a reason
   each, and counts per group. Lead with the counts.

Do not create contacts for unmatched rows at screening time. They are created when they engage.

### At enrolment: record who is in the campaign

Enrolment is what lets a colleague's check see that someone is already in a sequence. On the
day the list goes live:

- **Apollo and nReach** write `outbound_campaign_source`, `outbound_campaign_name` and
  `outbound_campaign_date` to the contact themselves, through their sync, and create contacts.
- **Meet Alfred** does not sync. Matched contacts get those three fields from the upload list,
  with source `Meet Alfred` and the campaign name prefixed with the runner's name
  ("Keith - SiGMA follow-up"). Unmatched rows: build an import CSV keyed by LinkedIn URL with
  name, company, LinkedIn URL, the three campaign fields, and the user as owner.

If the session has the Apollo connector and the user asks you to add people to a sequence,
screen first, then enrol only the clear and yours groups after the user confirms. This is the
one case where Claude starts outreach itself, because the tool handles unsubscribes.

### After: bring the results back

A campaign to hundreds of people should not create hundreds of notes.

- **Everyone who replied, accepted and answered, or booked:** these become real leads. Claim
  them (section 3) and write a touch note with the campaign in `Context:`, then continue one
  to one.
- **Anyone who asked to stop:** Do Not Contact (section 5).
- **No response:** nothing more; the campaign fields already show they were touched.

Writes are limited to 10 records per call. Up to about 30 records, write in calls of 10. Beyond
that, build a CSV for a HubSpot import (record ID, email or LinkedIn URL as the key, one column
per property) and give the user the file with one line on how to import it. The import is
theirs to run.

There is no Meet Alfred connector. Work from what the user gives you: the list before upload,
and the campaign export or pasted replies afterwards. LinkedIn messages sent by Meet Alfred
count as touches on the LinkedIn channel.

### Conferences

Before an event, screen the attendee or target list like any other list. The report per company
tells each of us who already knows whom, so we do not approach the same person twice at the same
booth. After the event, log each real conversation as a Meeting touch, channel In person, origin
Conference with the event name.

## 7. Approval and failures

- The connector requires showing the changes and getting a yes before each write. Show one table
  per touch covering the lead, the note and the contact (columns: Object, ID, Property, Current,
  New). On the first write of the session, mention that confirmations can be waived for the
  session.
- Before the first write in a session, check write access with `discover_hubspot_schema`
  (`GET_OBJECT_TYPES` for `LEAD` and `NOTE`). If write access is not available, say so, give the
  user the note text to paste by hand, and suggest they raise the permission in #sales.
- If one write in a set fails, report which succeeded and which did not. Never say a touch is
  logged unless the note was created.
