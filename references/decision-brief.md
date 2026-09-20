# Decision Brief Format

## First: factual questions vs decisions

**Factual clarifications use a plain question.** "Who said this?" "Have you tried it?" "What
version is in production?" Don't wrap these in the brief format — it makes a one-line
question look like a trade-off that needs weighing.

**Decision points use a decision brief.** When the user has to choose between options.

The test: **if you can already name a recommendation, it's a decision. If you're only
gathering information, it's a question.**

## Format

```
D<N> — one-line title of the question
<project/branch/one line of grounding>

ELI10: <plain language, 2-4 sentences, name the stakes>

Stakes if wrong: <one sentence — what breaks, what's lost>

Recommendation: <option> because <one-line reason>

Completeness: A=X/10, B=Y/10

A) <option name> (recommended)
   ✅ <concrete, observable pro>
   ❌ <honest con>
B) <option name>
   ✅ <pro>
   ❌ <con>

Net: <one line saying what's actually being traded off>
```

## Rules

- **`D<N>` numbering:** the first decision in a session is `D1`, then increment. It's your
  own counter, not a runtime value.
- **ELI10 is always present**, always in plain language. The user should be able to follow
  the trade-off without domain knowledge.
- **`Recommendation` is always present**, including when you have no strong view:
  `Recommendation: A — this is a taste call, no strong preference either way.`
  Keep `(recommended)` on the default option even then.
- **`Completeness` only when the options differ in coverage**, not in kind:
  `10/10` complete / `7/10` happy path only / `3/10` shortcut.
  If they differ in kind: `Note: options differ in kind, not coverage — no score.`
- **Pros and cons:** minimum 2 pros and 1 con per option when the choice is real. **The cons
  must be honest** — a brief where no option has a downside isn't a brief, it's a pitch.
- **`Net:` closes it.** This is the line the user will actually think about.
- **Cost labels** when effort is involved, e.g. `(human: ~2 days / agent: ~15 min)`, so the
  compression is visible at the moment of deciding.
- **At most 4 options per brief.**

## Five or more options: split, never drop

The cap is 4 options. With five or more real options, **never drop, merge, or silently defer
one to fit.** Either:

- split into sequential briefs (issue one, wait for the answer, issue the next), or
- restructure into levels (pick a category first, then the specific item)

**Deliberately excluded options must be stated explicitly, outside the `Net:` line, with the
reason for excluding them.**

> Example:
> One option I **deliberately excluded**, stated rather than swallowed:
> **reframe the process so the loop doesn't cross the material boundary.** It may be the
> cheapest fix, but it changes the frozen business process — that's a **requirements
> question, not a verification method** — and it should go to the stakeholder separately, not
> be folded into this decision. If you want to take that path, we need a separate round.

Silent omission is not allowed. The user is entitled to know what options exist and why any
of them aren't listed.

## What a brief must never be

1. **A menu with no recommendation.** You must have taken a position.
2. **A wall of text.** If the ELI10 runs past four sentences, the decision isn't framed yet.
3. **Followed by your own continuation.** Issue the brief, stop. The next thing in the
   conversation should be the user's answer.

## After issuing it

**Stop.** Don't push forward, don't "while I'm here" do something else, don't ask the
question and hand over a conclusion in the same turn.

Continuing before the user has answered is the most serious failure mode in this workflow —
it turns the entire premise-confirmation step into a formality.
