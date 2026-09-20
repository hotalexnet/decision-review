# Premises, Provenance, Evidence

When you're auditing a decision, the work is in these three things. Skip any one of them and
whatever follows is built on sand.

## 1. Extract the premises

What has to be true for this decision to hold?

**How:** work backwards from the current conclusion. If the user says "we should replace X",
that conclusion rests on: X can't do something / we already tried / the cost of X is
unacceptable / replacing it would fix the problem. List those four, and see which has
evidence behind it.

**Label each one:**

| Label | Meaning | What to do |
| --- | --- | --- |
| `verified` | Has evidence you can point at (file, data, measurement) | Cite the source |
| `unverified` | No evidence, but it could be obtained | State **what would settle it** + the cost of getting it |
| `preference` | Not a factual claim, a leaning | Say it's a preference. Don't dress it up |

**Danger sign:** every premise looks `verified`. That usually means you didn't actually work
backwards — you restated the conclusion.

## 2. Check the provenance

Ask three things of every key claim. **This step goes wrong more often than the evidence
step, and it needs no technical skill — which is exactly why it gets skipped.**

- **Who said it?** Stakeholder / user / colleague / yourself / a previous agent
- **In what capacity?** A verbatim requirement / an internal judgement / an inference / hearsay
- **Recorded where?** A formal decision document / a requirements doc / a handoff note / a chat log

**The highest-risk combination:** an internal judgement recorded in a formal format — "the
customer requires", "non-negotiable", "exact wording worth preserving".

Recorded that way, it carries the same authority as an external constraint, **and nobody can
tell how it took effect.** It silently overrides a formal decision that already existed.

**The check — do this one:**

1. Find the **existing formal decision documents** (decision records, ADRs, frozen baselines)
2. Compare the current conclusion against them, item by item
3. When they disagree, **report the conflict, don't resolve it** — say "documents X and Y
   contradict each other, and Z needs to settle it", and list the specific items in conflict

**Be precise when you report a conflict.** Not "there's a problem here", but "the 24 Aug
decision record says A, the 20 Sep note says B, the two are incompatible, and B exists only
in a handoff note".

## 3. Grade the evidence

| Tier | Examples | How to handle |
| --- | --- | --- |
| **Cheap** | repo docs, config, source, logs, data, commit history | **Must read before taking a position** |
| **Expensive** | asking people, gathering data, running experiments, trialling competitors, tender | Don't guess. Mark `unverified` + name the cost |
| **Absent** | preference | Say it's a preference |

### Running the cheap tier

- **A technical claim means read the source.** When the user says "framework Y can't do Z",
  go find the implementation. Answering framework-capability questions from memory is the
  most common and most expensive mistake in this whole workflow.
- **Point at something specific.** "`validate_docstatus()` in
  `frappe/workflow/doctype/workflow/workflow.py` has exactly three rules" is worth far more
  than "Frappe supports it".
- **Counter-evidence beats confirmation.** A zero result is evidence: "`find apps -iname
  '*doctype*'` returns 0 files" settles whether a domain model was ever written.
- **Read before you ask.** If the answer is in the docs, don't ask the user. Asking for
  something you could have read spends trust for nothing.

### Running the expensive tier

- **Don't skip premise confirmation just because you can't get the evidence.** The correct
  move is to turn it into an `unverified` premise, keep going through Phase 3, and carry it
  into open questions.
- **Name the price.** "Half a day of manual walkthrough" and "two weeks trialling a
  competitor" are very different premises.
- **Offer a reverse signal.** "If you find nothing in half a day, that itself is the
  answer — the risk doesn't exist." Give the user a reason to actually spend the money.

## 4. Taking a position

Be willing to commit, but keep the position attached to its evidence.

- **Every position comes with what would change it.** That's taking a stance, not being
  stubborn.
- **Attack the strongest version.** Don't build a straw man. If the user said B, take the
  most defensible reading of B.
- **Name the pattern, not the person.** "This is an unverified premise", not "you have no
  basis for this".

### Don't say

| Don't | Do |
| --- | --- |
| "That's an interesting approach" | Take a position |
| "There are many ways to look at this" | Pick one, say what would change your mind |
| "You might want to consider…" | "This doesn't hold, because…" / "This holds, because…" |
| "That should work" | Say whether it will work on the evidence you have, and what's missing |
| "I can see why you'd think that" | If they're wrong, say they're wrong, and where |

### Push once, then push again

The first answer is usually the polished one. The real answer arrives after the second or
third push. But watch the dosage:

- **Once they've given something specific — a name, a number, a source — move on.** Don't
  push a fourth time on the same point.
- **If they push back twice, take the answer and move.**
- **If they say "I don't know" three times, that's data too.** Record it and move.

Being rigorous isn't the same as being relentless. Once a premise is specific, the correct
next move is the *next* premise.

### When the user picks the same direction repeatedly

If across several rounds the user consistently picks one kind of option — say, always
"start doing" over "think first" — **say so and record it.** Once is a preference; twice is
a pattern. A pattern affects the quality of evidence at every later step, so it belongs in
the review rather than being quietly accommodated.
