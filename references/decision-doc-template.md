# Decision Document Template

Write it in the user's language. Every section either carries evidence you actually gathered,
or gets deleted. **Filling a section with filler is worse than leaving it out** — it makes the
document look more reliable than it is.

Save to `docs/<date>-<slug>.md`, follow the repo's existing naming convention, and report the
path.

For section 8, which concerns a person rather than the work, tell the user before you write
it that it will be committed to git.

---

```markdown
# <Decision name>: <one line saying what decision this is>

Status: DRAFT
Generated: <date>
Repo: <repo>
Branch: <branch>
Decision maker: <who>
Deadline: <by when it must be settled>

## 1. Context

<What this decision is and why it has to be made now. Specific enough to read as
"choose A, B, or C". Not a project introduction.>

## 2. Evidence gathered

| Evidence | Source | Bearing |
| --- | --- | --- |
| <one line> | <something pointable: file:line, command, measurement> | <what it supports or refutes> |

<Only what you actually checked. Anything unchecked belongs in section 7, not here.>

## 3. Premises

| # | Premise | Status | Basis |
| --- | --- | --- | --- |
| 1 | <statement> | verified / unverified / preference | <source, or "to settle: needs X"> |

<Mark the ones the user confirmed as "confirmed".
Premises the user explicitly rejected **stay in the table marked "rejected"** — don't delete
them. They are dead ends that need to stay dead.>

## 4. Rejected paths (don't rediscover these)

- <overturned conclusion> — <what evidence overturned it>
- <excluded option> — <why it was excluded>

<This section is for your future self and for other agents. Without it, the next round walks
the same dead ends all over again.>

## 5. Options

### A) <name>
Summary / Cost (S/M/L/XL) / Risk / Pros / Cons / Reuses

### B) <name>
...

### C) <name> (optional)
...

<At least 2 genuinely different options — not one option at three levels of intensity.
Five or more means splitting into separate briefs, and **any excluded option must be stated
here with its reason for exclusion**.>

## 6. Criteria

| Outcome | Means | Next step |
| --- | --- | --- |
| <observing X> | <what it tells you> | <what to do> |

<Must include falsifiable entries: a result that means some option is wrong. An option with
no falsification condition is a position, not an option.>

## 7. Open questions

1. <question> — <what evidence would settle it> — <cost of getting it>
2. ...

<While this section is non-empty, the completion status is DONE_WITH_CONCERNS.>

## 8. What I noticed about how you think

<2-4 specific observations, quoting the user's own words. Generic praise is worse than
deleting the section.>

## 9. The assignment

<One action, completable this week, with a clear definition of done. Not a strategy, not
"keep researching". Include the reverse signal — if nothing turns up, what does that mean.>
```

---

## Quality check before finishing

- Can I point at a source for every line in section 2? (If not, it moves to section 7)
- Are there any `unverified` entries in section 3? If everything is `verified`, I probably
  didn't work backwards properly
- Is section 4 non-empty? If it is empty, I wasn't overturning anything, only recording
- Are there falsifiable entries in section 6?
- Does the action in section 9 have a definition of done?
- Is any section there only to look complete?
