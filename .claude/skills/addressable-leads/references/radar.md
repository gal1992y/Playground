# My book and the team radar

Two views over the same data. "My book" is for anyone: what is mine and what is due. The "team
radar" is for whoever runs the pipeline review: where we collide, what we dropped, and what
HubSpot has wrong.

Both follow the quiet-when-clean rule: report only what needs action. If a section is empty,
leave it out.

## My book

Triggered by "my leads", "what's due", "what should I follow up on", or at the start of a lead
gen session.

1. Search open leads owned by the user: `LEAD`, `hubspot_owner_id` equal to the user's owner
   ID, `hs_pipeline_stage` in `new-stage-id`, `attempting-stage-id`, `connected-stage-id`,
   **and** `hs_last_activity_date` within the last 120 days. The date filter matters: without
   it the list fills with old automatic leads that were never worked.
2. For the leads returned (work the 30 most recent if there are more, and say so), read the
   newest touch note for the `Next:` date and the unanswered count.
3. Report in this order:
   - **Reply waiting on you:** they answered and we have not. Oldest first. This is the most
     valuable line in the report.
   - **Due today or overdue:** `Next:` date reached.
   - **At the limit:** 4 unanswered touches, or 2 on a DM channel. Recommend closing out.
   - **Going stale:** no touch for 30 days. At 60 days the claim lapses and others may pick
     it up.
   - **Claimed, never touched:** stage New for more than 7 days.
4. Offer to draft the follow-ups, one at a time, through the normal loop.

## Team radar

Triggered by "where are we stepping on each other", "what did we drop", "pipeline hygiene",
"lead gen review", or the Friday RevOps check. The data is the whole team's, so keep to
business facts and name owners only to route the fix.

Use `query_crm_data` for counts and `search_crm_objects` for the rows. One object type per SQL
query; joins are not available, so combine results yourself. Bound every search by date.

| Check | How to find it | Who fixes |
| --- | --- | --- |
| **Collisions** | Open leads with activity in the last 14 days, grouped by `hs_primary_company_id`: any company with two or more different active owners | The owners agree who leads. Draft one Slack message to both |
| **Same person, two of us** | Contacts with touch notes by two different people within 14 days | Same |
| **Dropped replies** | Contacts with Lead Status `REPLIED`, or `hs_sales_email_last_replied` or `outbound_campaign_last_reply` in the last 30 days, where no activity followed the reply within 2 business days | Lead owner; if none, flag for assignment |
| **Meetings that went nowhere** | Contacts with Lead Status `MEETING_BOOKED` and a meeting more than 14 days ago, company has no open deal | Meeting owner |
| **Warm leads with no owner** | Open leads in Connected whose owner is inactive or empty | Propose a new owner; the pipeline lead approves |
| **Stale claims** | Open leads with an active owner, last activity 30 to 60 days ago | Owner gets a nudge (Slack draft) |
| **Policy breaks** | More than 4 unanswered touches; a touch during a cool-off; a touch on a Do Not Contact person; an `Override:` line in a note | Owners, pipeline lead copied |
| **Out of sync** | Lead stage New or Attempting while contact status is Replied or Meeting Booked; open lead on a company that is a live client; two open leads on one contact | Fix with the owner's yes, 10 records at a time |
| **Tool mapping** | Recent sequence activity recorded under an inactive owner | RevOps |

Report shape:

```text
Lead gen radar, week of <date>
Collisions: <n>. <Company>: <owner A> (<last touch>) and <owner B> (<last touch>)
Dropped replies: <n>. <Person, Company>: replied <date>, owner <name>, nothing since
...
Suggested fixes: <the three that matter most, each with who acts>
```

Lead with the collisions and dropped replies: those cost deals. Hygiene items come last. Offer
to draft the Slack nudges; do not send them.

Volume: the portal holds more than 62,000 leads and reads return at most 200 rows. Always
filter by date and stage, page when the total exceeds a page, and state the window you covered.
If a check would need more than a few thousand rows, say that it needs an export and stop
there.
