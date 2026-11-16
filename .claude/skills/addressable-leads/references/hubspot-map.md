# HubSpot map

How the lead record is stored in Addressable's HubSpot (account 22590214), and how to read and
write it with the HubSpot connector. Checked against the live portal on 2026-11-16. Tool names
are the connector's short names; your session may show them with a prefix.

## Contents

1. Tools, limits and response size
2. Records and what each one means
3. Contact properties
4. Lead properties, stages and the "claimed" rule
5. Deals: who is a client, who is in a deal
6. Notes and what was said
7. Read recipes (the standard check in about 9 calls)
8. Write recipes
9. Traps in this portal
10. Properties that may arrive later

## 1. Tools, limits and response size

| Need | Tool | Notes |
| --- | --- | --- |
| Who the user is | `get_user_details` with `include: ["USER_INFORMATION"]` | Once per session. Without `include` the response is about 11 KB |
| Owner names and whether active | `search_owners` with `ownerIds` | One call for every owner ID you collected |
| Find records | `search_crm_objects` | 200 per page, 18 filters, 100 IDs per association filter. Pass `chatInsights` (a short anonymised intent and `NEUTRAL`) on every call |
| Fetch records by ID | `get_crm_objects` | 100 IDs |
| Counts and group-bys | `query_crm_data` (SQL; call `tool_guidance` first) | One object type per query |
| Check a property or its options | `search_properties`, `get_properties` | `search_properties` is fuzzy: it never says "not found", so compare names exactly |
| Create or update | `manage_crm_objects` | **10 records per call**, approval table first |

Responses omit empty properties: a property that is absent from a result is empty.

Each person's Claude is connected as that person, so every write carries their real name.

## 2. Records and what each one means

| Record | Type name | Meaning | Owner means |
| --- | --- | --- | --- |
| Contact | `CONTACT` | The person. One per human. | Relationship owner |
| Company | `COMPANY` | The organisation. Can have a parent company | Account owner |
| Lead | `LEAD` | One outreach effort to one person, from first touch to Qualified or Disqualified. One open lead per person at most | The person working this effort now |
| Note | `NOTE` | One logged touch, in the fixed format | Whoever made the touch |
| Deal | `DEAL` | Created from a Qualified lead | The AE who runs it |

## 3. Contact properties

| Purpose | Property | Notes |
| --- | --- | --- |
| Name, title | `firstname`, `lastname`, `jobtitle` | |
| Email | `email` | About 18,800 contacts have none, so handles matter |
| Telegram | `telegram` | Stored inconsistently: `west_v1`, `@davidoptimo`, `-` |
| X | `twitterhandle` | |
| LinkedIn | `hs_linkedin_url` | `linkedin` is an older free-text copy |
| WhatsApp | `hs_whatsapp_phone_number` | |
| Outreach status | `hs_lead_status` | Values below. Set by Apollo and nReach syncs too |
| Email opt-out | `hs_email_optout` | True means no email of any kind |
| Owner | `hubspot_owner_id` | |
| Last contacted | `notes_last_contacted` | Email, call, meeting, LinkedIn, SMS, WhatsApp only. **Not** Telegram or X |
| Last activity | `notes_last_updated` | Includes notes, so a logged Telegram touch moves it |
| Last sales email reply | `hs_sales_email_last_replied` | |
| Outbound tool | `outbound_campaign_source` | `Apollo`, `nReach`, `Meet Alfred` |
| Campaign | `outbound_campaign_name`, `outbound_campaign_date`, `outbound_campaign_last_reply` | |
| Preferred channel | `communication_channel` | Telegram, Slack, Email, Whatsapp, Discord. Rarely filled |

`associatedcompanyid` usually comes back empty. To get from a contact to its company, search
companies by association (section 7).

`hs_lead_status` values: `NEW`, `OPEN`, `IN_PROGRESS`, `REPLIED`, `OPEN_DEAL`, `UNQUALIFIED`,
`ATTEMPTED_TO_CONTACT`, `CONNECTED`, `BAD_TIMING`, `DEAD_LEAD`, `MEETING_BOOKED`,
`UNRESPONSIVE`, `NURTURE`, `DO_NOT_CONTACT`.

**`DO_NOT_CONTACT` is the master stop flag.** It stops every channel.

## 4. Lead properties, stages and the "claimed" rule

| Purpose | Property | Notes |
| --- | --- | --- |
| Name | `hs_lead_name` | Convention: `First Last YYYY-MM` (month the effort started) |
| Stage | `hs_pipeline_stage` | Values below |
| Owner | `hubspot_owner_id` | Defaults to the current user on create |
| Type | `hs_lead_type` | `NEW_BUSINESS`, `UPSELL`, `RE_ATTEMPTING` |
| Label | `hs_lead_label` | `HOT`, `WARM`, `COLD` (rule in `touch-log.md` section 2) |
| Primary contact, company | `hs_primary_contact_id`, `hs_primary_company_id`, `hs_associated_company_name` | Set by HubSpot from the associations |
| Last activity | `hs_last_activity_date` | Follows the primary contact. Includes notes, meetings and tool-synced emails |
| Logged outreach | `hs_lead_outreach_activity_count`, `hs_lead_first_outreach_date` | Counts logged calls, emails, meetings. Not notes |
| Why we stopped | `hs_lead_disqualification_reason`, `hs_lead_disqualification_note` | Reason values below |
| When we stopped | `hs_v2_date_entered_unqualified_stage_id_1675714327` | Date the lead entered Disqualified |
| Created | `hs_createdate` | |

Stages (`hs_pipeline_stage`):

| Value | Label | Means |
| --- | --- | --- |
| `new-stage-id` | New | Claimed, not touched yet |
| `attempting-stage-id` | Attempting | At least one touch, no reply |
| `connected-stage-id` | Connected | They replied or we met |
| `qualified-stage-id` | Qualified | Real interest and fit; a deal exists |
| `unqualified-stage-id` | Disqualified | Stopped, with a reason |

A lead is **open** when its stage is anything other than Qualified or Disqualified. About 190
old leads sit on retired stage IDs; treat those as open. `hs_lead_is_open` comes back as `1`
but cannot be used as a filter: filter on the stage instead.

Disqualification reasons (use the value exactly, including the odd spacing on the first):
`Got Cold ( no communication)`, `BAD_TIMING`, `BUDGET_CONSTRAINTS`, `NO_DECISION_MAKING_POWER`,
`COMPETITOR_PREFERENCE`, `NOT_A_GOOD_FIT`, `NO_INTEREST`, `PRIOR_NEGATIVE_EXPERIENCE`,
`TECHNICAL_LIMITATIONS`. Put anything these do not cover (existing client, duplicate, wrong
person) in `hs_lead_disqualification_note`.

After a lead is Qualified or Disqualified, only a Super Admin can change its stage or owner. To
re-engage, open a new lead with type `RE_ATTEMPTING`.

### The "claimed" rule

HubSpot holds over 62,000 leads, and most were created automatically and never worked. So an
open lead with an owner does **not** by itself mean someone is on it. A lead is **claimed**
when all three hold:

1. It is open.
2. Its owner is an active user (`search_owners` returns `isActive: true`).
3. It has activity in the last 60 days (`hs_last_activity_date`, or the newest touch note), **or**
   it has no activity yet and was created (`hs_createdate`) in the last 7 days. The second case
   is a fresh claim made just before the first message.

Anything else is unclaimed, and whoever checks next may pick it up.

`isActive` can lag when someone leaves and their HubSpot user is not switched off. If an owner
looks active but the user says that person has left, believe the user and mention the mismatch.

The rules apply to everyone, founders included. Anyone can be the colleague whose thread gets
crossed.

## 5. Deals: who is a client, who is in a deal

Open deal: `hs_is_closed` is `false`. Read `dealname`, `pipeline`, `dealstage`,
`hubspot_owner_id`, `closedate`, `closed_lost_reason`, and `amount` with `deal_currency_code`.
For a stage ID not listed here, read the stage label from `discover_hubspot_schema`
(`GET_PIPELINES`, `DEAL`) once per session.

| Pipeline | ID | Stages (in order) |
| --- | --- | --- |
| Ads Sales Pipeline | `default` | `77508367` Sales Qualified Lead, `77505440` Meeting Booked, `1272981582` Demo Completed, `presentationscheduled` Discovery Call Completed, `1105767444` Proof-of-Value (Trial), `159424058` Solution & Budget Design, `248558985` Proposal, `1165183417` Negotiation, `248558986` Verbal Commit, `1267000732` Contracting, `1108874145` Offer Signed, `closedwon` Paid (Closed Won), `closedlost` Closed Lost |
| Tagging Sales Pipeline | `922798867` | `1411112504` New / Qualified, `1411112505` Demo Completed, `1411112506` Compliance Kit Shared, `1411112507` Compliance Kit Signed, `1411112508` Pilot In Progress, `1411198471` Pilot Results Delivered, `1411198472` Business Case Aligned, `1411198473` Commercial Offer Sent, `1411198474` Negotiation, `1411198475` Signed, `1411112509` Paid (Closed Won), `1411112510` Closed Lost |
| Renewals and Expansions | `746430535` | Open deal here = existing client. Won `1086412201`, lost `1086412202` |
| CSM Service | `36893546` | The client's service record. See below |
| Spectra - End Customers | `935020590` | Entry `1438733437` Lead Qualification. Won `1438733442`, lost `1438733443` |
| Spectra - Partners | `934983441` | Entry `1438733136`. Won `1438733141`, lost `1438733142` |
| Spectra - Resellers | `935024931` | Entry `1438733735`. Won `1438733740`, lost `1438733741` |
| Investigations, Financial Institutions | `828189103`, `860953347` | Deprecated. Read for history only |

### Client status

Decide in this order:

1. **The company has a CSM Service deal.** Its stage decides:

   | Stages | IDs | Status |
   | --- | --- | --- |
   | Pre-Onboarding to Onboarding Complete | `79359608`, `1076482099`, `126902598`, `126902599`, `121568842`, `1337292385` | **Live client** (onboarding) |
   | Live - Testing, Live First Quarter, Live Ongoing | `1311833420`, `1311833421`, `1076306831` | **Live client** |
   | Offline First Quarter, Offline Ongoing, Offline Internal | `1178904086`, `1076311921`, `1315231039` | **Paused client** |
   | Not Active | `79359614` | **Former client** |

2. **No CSM Service deal:** the company is a **live client** if it has an open Renewals and
   Expansions deal, or any deal won in the last 18 months. Otherwise it is not a client.

Check the company's parent too (association label "Parent Company") and the parent's other
child companies. A brand of a live client is treated as a live client.

When a lead is Qualified, the deal goes in the pipeline for the product: Ads to Ads Sales,
Tagging to Tagging Sales, Spectra to the Spectra pipeline that fits the buyer (end customer,
partner or reseller). Partnerships and agencies go to the pipeline of the product they would
sell or buy; if unclear, ask.

An open deal means the lead should be Qualified. A lead still in New or Attempting next to an
open deal is out of sync: flag it.

## 6. Notes and what was said

Notes are `NOTE` records with `hs_note_body` (the text, HTML allowed), `hs_timestamp` (when the
touch happened, ISO 8601 UTC) and `hubspot_owner_id`.

- Touch notes written by this skill start with the token `LEADTOUCH`. Find them with
  `hs_note_body CONTAINS_TOKEN LEADTOUCH` plus an association filter. These are short.
- Fireflies writes a meeting summary as a note on the company and attendees. These are the best
  source for prices, terms and promises given on a call, but each is about 1,000 words, and the
  connector returns the full text twice (in `hs_body_preview` and in `displayName`). So:
  - Search `LEADTOUCH` notes first, with a limit of 10.
  - Then search all notes with an association filter, newest first, **limit 3**. Read more
    only if those leave a gap that matters.
  - Never run a note search without an association filter.
- Old notes may not follow the `LEADTOUCH` format. Read them for meaning. Do not rewrite them.
- Logged emails, calls and meetings are separate activity types. The lead's
  `hs_lead_outreach_activity_count` and the contact's `notes_last_contacted` reflect them.

## 7. Read recipes (the standard check in about 9 calls)

All are `search_crm_objects` calls unless stated. Ask only for the properties you need.

**Contact properties to request** (call this set `CP`): `firstname`, `lastname`, `jobtitle`,
`email`, `telegram`, `twitterhandle`, `hs_linkedin_url`, `hs_lead_status`, `hubspot_owner_id`,
`notes_last_contacted`, `notes_last_updated`, `hs_sales_email_last_replied`,
`outbound_campaign_source`, `outbound_campaign_name`, `outbound_campaign_date`,
`outbound_campaign_last_reply`, `hs_email_optout`.

**1. User.** `get_user_details` with `include: ["USER_INFORMATION"]`.

**2. Person, by every identifier you have, in one call.** Each filter group is an OR. Search
all identifiers, not just the first: the same person can exist once with an email and once with
only a handle.

```json
{"objectType": "CONTACT",
 "properties": ["...CP"],
 "filterGroups": [
   {"filters": [{"propertyName": "email", "operator": "EQ", "value": "david@optimobet.com"}]},
   {"filters": [{"propertyName": "telegram", "operator": "IN",
                 "values": ["davidoptimo", "@davidoptimo", "t.me/davidoptimo", "https://t.me/davidoptimo"]}]},
   {"filters": [{"propertyName": "twitterhandle", "operator": "IN", "values": ["davidoptimo", "@davidoptimo"]}]},
   {"filters": [{"propertyName": "hs_linkedin_url", "operator": "CONTAINS_TOKEN", "value": "linkedin-slug"}]}
 ]}
```

If nothing matches, use the `query` field with the person's name, then narrow by company.

**3. Company.** By association to the contact:

```json
{"objectType": "COMPANY",
 "properties": ["name", "domain", "hubspot_owner_id"],
 "filterGroups": [{"associatedWith": [{"objectType": "contacts", "operator": "EQUAL", "objectIdValues": [CONTACT_ID]}]}]}
```

With no contact, search by `domain` (`EQ`, use the email domain), then by `query` with the name.
About 5,000 companies have no domain, and the same company can appear under a brand and a legal
name: check both.

Then, in parallel:

**4. Everyone at the company.** `CONTACT`, associated with `companies` `EQUAL` the company ID,
sorted by `notes_last_updated` descending, limit 20, properties `CP`.

**5. Leads.** `LEAD`, two filter groups: associated with the company; associated with the
contacts (`IN`, the contact IDs). Properties: the lead table in section 4.

**6. Deals.** `DEAL`, associated with the company. Properties as in section 5. Add a second
search on the parent company when there is one.

**7. Touch notes.** `NOTE`, `hs_note_body CONTAINS_TOKEN LEADTOUCH`, associated with the
company, sorted by `hs_timestamp` descending, limit 10.

**8. Other notes.** `NOTE`, associated with the company, sorted by `hs_timestamp` descending,
limit 3.

**9. Owners.** `search_owners` with every owner ID from steps 2 to 8.

Links: each search returns a `urlTemplate`. Use it to link every record you cite. For leads it
opens the lead list filtered to that lead, which is fine.

**Screening a list.** Batch by 100: one contact search with `email IN`, one with
`hs_linkedin_url` for LinkedIn rows (normalise to the profile slug: lowercase, no
`https://www.linkedin.com/in/`, no trailing slash, then match with `CONTAINS_TOKEN` per slug in
groups of 5), one company search with `domain IN`, then one lead search and one deal search for
the matched IDs. Never look rows up one at a time.

## 8. Write recipes

Always show the approval table first (`touch-log.md` section 7). Association targets use the
type names in capitals: `CONTACT`, `COMPANY`, `LEAD`, `DEAL`. Leave `hubspot_owner_id` out to
make the user the owner; set it only to give a record to someone else.

Create a lead (it must be associated with a contact):

```json
{"confirmationStatus": "CONFIRMED",
 "createRequest": {"objects": [{
   "objectType": "LEAD",
   "properties": {"hs_lead_name": "Aiko Tan 2026-11", "hs_pipeline_stage": "connected-stage-id",
                  "hs_lead_type": "NEW_BUSINESS"},
   "associations": [{"targetObjectType": "CONTACT", "targetObjectId": 111},
                    {"targetObjectType": "COMPANY", "targetObjectId": 222}]}]}}
```

Create the touch note, using the lead ID returned above:

```json
{"confirmationStatus": "CONFIRMED",
 "createRequest": {"objects": [{
   "objectType": "NOTE",
   "properties": {"hs_note_body": "LEADTOUCH | 2026-11-13 | Telegram | Outbound | by Tomer Sharoni<br>Context: ...",
                  "hs_timestamp": "2026-11-13T12:00:00Z"},
   "associations": [{"targetObjectType": "LEAD", "targetObjectId": 333},
                    {"targetObjectType": "CONTACT", "targetObjectId": 111},
                    {"targetObjectType": "COMPANY", "targetObjectId": 222}]}]}}
```

Update the lead and contact together (up to 10 objects per call):

```json
{"confirmationStatus": "CONFIRMED",
 "updateRequest": {"objects": [
   {"objectType": "LEAD", "objectId": 333, "properties": {"hs_pipeline_stage": "connected-stage-id"}},
   {"objectType": "CONTACT", "objectId": 111, "properties": {"hs_lead_status": "REPLIED"}}]}}
```

`hs_timestamp`: ISO 8601 in UTC. When only the date is known, use 12:00 UTC on that date.

## 9. Traps in this portal

- **Almost every contact already has a lead.** A workflow ("create lead upon contact lcs
  update") adds one when a lifecycle stage changes. So before creating a lead, look for an open
  one on the contact and reuse it. After creating a contact, search for its leads again before
  creating one, because the workflow may have just made one.
- **Departed owners.** Thousands of leads belong to people who have left, and many have no
  owner. That is why ownership is judged by the claimed rule, never by the owner field alone.
- **Tool activity under the wrong name.** At least one Apollo user is mapped to a departed
  person's HubSpot owner. If a lead shows recent sequence emails under a departed owner,
  somebody active is probably running that sequence: say so.
- **Telegram and X are invisible unless logged.** "Never contacted" in HubSpot can be false for
  these channels. Notes sometimes mention a Telegram group with the prospect: a separate DM to
  someone already in a group with a colleague goes around that colleague.
- **People on the thread who own nothing.** Meeting notes list attendees. A colleague who joined
  the calls but owns no record is still on the account: name them in the report and copy them
  on the Slack ask, which goes to the owner.
- **Lead Status is written by tools.** `hs_lead_status` can say Replied or Meeting Booked while
  the lead stage still says New or Attempting. Report the mismatch and fix the stage when the
  user agrees.
- **Duplicates and name mismatches.** The same person can exist once with an email and once with
  only a handle, and the same company under two names. Read all of them, report them, and do not
  merge. Placeholder names (a handle as the surname) are worth flagging.

## 10. Properties that may arrive later

The policy page proposes dedicated fields. On 2026-11-16 none of them existed. Once per
session, check with `get_properties` (object `leads`: `last_touch_date`, `unanswered_touches`,
`next_touch_allowed`, `outreach_channel`, `outreach_product`; object `contacts`: `quiet_until`,
`do_not_contact_reason`). Names listed under `propertiesNotFound` do not exist. If a field
exists, read it in preference to the derived value and fill it on every write. If it does not
exist, or the check cannot run, never write it.

| Proposed field | Until it exists, derive it from |
| --- | --- |
| `last_touch_date`, `last_touch_channel`, `last_touch_by` (lead) | Newest `LEADTOUCH` note, else `hs_last_activity_date` |
| `last_reply_date` (lead) | `Reply:` lines, `hs_sales_email_last_replied`, `outbound_campaign_last_reply` |
| `unanswered_touches` (lead) | `LEADTOUCH` Outbound notes since the last reply, plus tool emails since then |
| `next_touch_allowed` (lead) | `Next:` line of the newest note |
| `quiet_until` (contact) | Disqualified date plus the cool-off for that reason (`policy.md`) |
| `outreach_product`, `outreach_origin`, `outreach_channel`, `outreach_campaign` (lead) | `Context:` line of the first touch note |
| `value_offered`, `value_offered_detail` (lead) | `Offered:` and `Shared:` lines |
| `icp_segment`, `accepts_crypto` (company) | Judge from the website and deal history; say it is your judgement |
