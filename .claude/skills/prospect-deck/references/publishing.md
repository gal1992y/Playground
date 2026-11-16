# Sharing and publishing

One `deck.json` gives four files. Each has a place:

| File | Use it for |
|---|---|
| `deck.pdf` | Email attachment, LinkedIn or WhatsApp or Telegram direct message, LinkedIn document post (carousel) |
| `deck.html` | A link: one self-contained file (fonts and logos inside) that scrolls on a phone and pages with arrow keys. Host it anywhere static. Private decks carry `noindex` |
| `png/slide-NN.png`, `og.png` | Single slides for a post, a story or a chat message; `og.png` is the link preview and belongs next to the HTML |
| `deck.pptx` | Presenting live, with the talk track in the speaker notes. The slides are pictures: to change a word, change `deck.json` |

Name files for the recipient: `Addressable-for-<Prospect>-<Mon-YYYY>.pdf`.

## Private and public are different decks

| | `audience: "private"` | `audience: "public"` |
|---|---|---|
| Goes to | The prospect, directly | LinkedIn, X, the blog, a newsletter, an event |
| Prospect's name and logo | Yes | No, unless they agreed (`logo_permission: true`) |
| Numbers about the prospect's own users | Yes (direct mode) | Never |
| Numbers about peers and the market | Yes | Yes |
| Footer | "Confidential · Prepared for X" | None |
| Ask | A reply or a meeting | "See this for your own users" with a link |

The public version is the same story told about a market: "What casinos can't see about their players", built from
`peers` and `market` claims only. It is the strongest top-of-funnel piece this skill makes, and each private deck
can leave one behind. Build it as a second `deck.json`; the lint enforces the differences. Naming a rival's
incident in public is a bigger step than in a private deck: keep to verified facts, link the sources, and get the
user's OK on the wording.

A third party's logo is theirs. In a private deck sent to that company it is expected. Anywhere else it needs
their permission: the builder leaves it out of public decks by default.

## The message that carries it

Draft it for the user with the deck, in the buyer's language, for the channel they will use:

- Sixty words or fewer. The hero number in the first line, in their terms. One ask, the same as the deck's.
- No "I hope this finds you well", no product description, no attachment list.
- Email subject: the claim, not the company ("1,296 hidden VIPs at casinos like yours").
- LinkedIn post for the public version: the hero fact as the first line, two lines of what it means, the document
  attached, the ask as the last line. No hashtag wall.

Example (email, private, proxy mode):

> Subject: Hidden VIPs at casinos like Examplex
>
> Hi <name>, at casinos like yours in Brazil, 1,296 players deposit under $500 at one casino and over $5,000 at
> others. From the inside they look like small accounts. Six slides attached. If you share a user sample, we will
> show you which of yours they are. 20 minutes next week?

## Before anything leaves

- `lint_deck.py --final` printed OK, and `prospect-deck-check` printed OK on the PDF.
- The user has seen the PNGs, the events used and left out, and the open objections.
- **You send nothing.** No email, post, upload, share link, Slack message or HubSpot note without the user's
  explicit OK for that specific action. Hand over the files and the draft message; the user sends.
- After it goes out, offer to log the deck and its date on the HubSpot deal (again, on their OK).
