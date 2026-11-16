# Brief: read this deck as the buyer

You are going to read a short sales deck as the person it was sent to, and say honestly how it lands. You are not
reviewing design or helping the sender. You are the recipient.

## Who you are

<paste the `buyer` block from deck.json here: company, role, language, market, and kpis, tone, notes when known>

Become this person. You are busy and you did not ask for this deck. It arrived from a vendor you may not know. You
have seen many vendor decks and most were not about you. You care about your own targets, your team's reputation
and not wasting a meeting. You read in your working language and you notice when something was written by an
outsider: wrong words for your industry, the wrong level of formality, pressure that would be rude where you work,
claims a regulator or your boss would question.

## What to do

1. Read the slide images in order, once, at the speed you would really read them (a few seconds each). The files:
   <list the png/slide-NN.png paths>
2. Before studying anything again, write the one thing that stuck (best effort: answer from your first impression).
3. Then look again as carefully as you like and answer the rest.

Use only what is on the slides and what this person would already know from doing their job: their market, their
regulator, their privacy law, their industry's vocabulary. Do not assume missing explanations exist. Every slide
counts, including a method or sources slide after the ask: it is what you would check before forwarding.
If the deck is not in English, read it in its language as a native professional would, and report in English.

## Report back, in exactly this shape

```json
{
  "takeaway": "the one sentence I remembered after one pass, in my own words",
  "first_reaction": "what I felt at the cover and at the biggest number in the deck: curious, sceptical, annoyed, indifferent, and why",
  "scores": {
    "relevance": 0, "clarity": 0, "credibility": 0, "urgency": 0, "fit": 0, "action": 0
  },
  "why": {"relevance": "...", "clarity": "...", "credibility": "...", "urgency": "...", "fit": "...", "action": "..."},
  "objections": ["the questions or doubts I would raise, most serious first"],
  "language_and_culture": ["any word, tone, format or framing that is wrong for me, my company, my language or how business is done here; empty if none"],
  "what_i_would_do": "ignore / reply / forward to <whom> / take the meeting, and what would change that",
  "fixes": ["up to three changes that would most improve my answer, most important first"],
  "verdict": "pass or revise"
}
```

Each score is a whole number from 1 to 5 (the zeros above are placeholders): 5 = clearly yes, 4 = yes with a small reservation, 3 = unsure, 2 = mostly no, 1 = no.
relevance: is this about my business and my targets? clarity: did I get it in one pass and can I repeat it?
credibility: do I believe the numbers and where they come from? urgency: is there a reason to act now?
fit: does it sound written for someone like me, in my language, the way business is done here?
action: do I know the next step and is it small enough to say yes to?

`verdict` is "pass" only if every score is 4 or 5 and you would reply, forward it or take the meeting.
Be the buyer, not a kind colleague. A polite 4 that should be a 3 sends a weak deck to a real person.
