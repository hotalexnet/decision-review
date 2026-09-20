# decision-review

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Runtime: Python 3](https://img.shields.io/badge/runtime-python3-blue.svg)](https://www.python.org/)
[![Standard: Agent Skills](https://img.shields.io/badge/standard-agent--skills-2ea44f.svg)](https://agentskills.io/specification)
[![Scope: Investigation](https://img.shields.io/badge/scope-investigation-8957e5.svg)](#scope)

**English** | [**中文**](./README.zh-CN.md)

**Audit a decision instead of making it.**

A skill for coding agents that reviews decisions which can be settled by investigation.
It extracts the premises, checks who actually said what, grades the evidence, and hands
back falsifiable criteria — instead of a confident recommendation.

## Why this exists

Ask an agent "should we switch platforms?" and you get an answer. The answer is usually
confident, usually plausible, and usually resting on a premise nobody verified.

The failure mode is not bad reasoning. It is **skipped premise extraction**: the agent
argues from assumptions it never surfaced, and the user can't see which assumption the
conclusion hangs on.

Worse, some of those assumptions are recorded in the wrong place. A throwaway line in a
handoff note — "database should be its own Postgres" — gets filed next to verbatim
stakeholder quotes, and within a week it has the same authority as a signed requirement,
having silently overridden a formal decision document that nobody remembers writing.

This skill exists to catch that. It makes the agent stop, name the premises, find out who
said what, and say plainly when the evidence isn't there yet.

## Scope

The boundary is **how the question converges**, not which domain it belongs to:

| | `decision-review` | product/market validation |
| --- | --- | --- |
| Question | Is this decision correct? | Is this worth building? |
| Converges by | **Investigation** — read the docs, check the source, ask the stakeholder, query the data | **Market contact** — find users, take money, watch retention |
| Failure signal | A premise was never tested | Nobody will pay |

Because the boundary is convergence mode, this skill is **not limited to technical or
architectural work**. It applies equally to:

- platform, vendor, and framework selection
- architecture and migration decisions
- taking on a client, or turning one down
- build vs. buy vs. self-host
- process and workflow changes
- pricing and contract trade-offs
- hiring or outsourcing

It does **not** apply to product/market validation — that needs market contact, not
investigation.

## The four mechanisms

1. **Extract the premises** — what has to be true for this decision to hold? Mark each
   one `verified`, `unverified`, or `preference`.
2. **Check the provenance** — who said it, in what capacity, and where is it recorded?
3. **Grade the evidence** — cheap (must be read), expensive (name the cost, don't guess),
   or absent (call it a preference).
4. **Produce falsifiable criteria** — what result means what, instead of one recommendation.

### One question at a time

Ask one question, then stop and wait.

Batch three questions and you get three shallow answers. Ask one, stay quiet, and the
second or third answer is the real one. This single rule carries most of the value — it
is why a review takes longer than a recommendation and reaches a different place.

### Evidence tiers

| Tier | Examples | What to do |
| --- | --- | --- |
| **Cheap** | repo docs, config, source, logs, data, git history | **Must read before taking any position** |
| **Expensive** | asking stakeholders, gathering data, running experiments, trialling competitors | Do not guess. Mark `unverified`, name the cost to settle it |
| **Absent** | taste, preference | Say it's a preference. Don't dress it up as "architecture" |

### Provenance — the check that gets skipped

Provenance needs no technical skill, which is exactly why it's the one everybody skips.
The highest-risk combination is **an internal judgement recorded in a formal format** —
"the customer requires", "non-negotiable", "exact wording".

Once recorded that way it carries the authority of an external constraint, and nobody can
tell how it took effect. The standard action: find the **existing formal decision
document**, compare it against the current conclusion, and when they conflict, **report
the conflict rather than resolving it** — say which documents disagree and who needs to
settle it.

## Install

`~/.agents/skills` is the shared skill root used by several harnesses, so one copy works
in all of them:

```bash
git clone https://github.com/hotalexnet/decision-review.git ~/.agents/skills/decision-review
```

| Harness | Skill roots it reads | Extra step |
| --- | --- | --- |
| **pi** | `~/.agents/skills`, `~/.pi/agent/skills` | none |
| **Codex** | `~/.codex/skills` + `~/.agents/skills` | none |
| **dsh** (DeepSeek Harness) | `~/.dsh/skills` + `~/.agents/skills` | none |
| **opencode** | `~/.config/opencode/skills/`, `<repo>/.opencode/skills/` | symlink |
| **Claude Code** | `~/.claude/skills/` | symlink |

```bash
# opencode
mkdir -p ~/.config/opencode/skills
ln -s ~/.agents/skills/decision-review ~/.config/opencode/skills/decision-review

# Claude Code
ln -s ~/.agents/skills/decision-review ~/.claude/skills/decision-review
```

Requirements: Python 3 (standard library only), and `git` for the profile layer.

## Usage

Any phrasing that asks whether a decision holds:

```
"Should we switch off X?"
"Help me review this decision."
"我们是不是该换掉 X？"
"Is this judgement backed by anything?"
```

A review runs through:

```
Phase 0  What decision is actually being made?
Phase 1  Read the cheap evidence. Nothing is said before this.
Phase 2  Check provenance. Extract the premises.
Phase 3  Confirm the premises, one at a time.          <- the highest-value gate
Phase 4  2-3 genuinely different options + falsifiable criteria table
Phase 5  Write the decision document
Phase 6  Signal reflection, one concrete assignment, write the profile
```

Each decision point is emitted as a **decision brief** — a compact markdown block with an
ELI10 of the trade-off, an explicit recommendation, and honest cons on every option:

```
D2 — What is the cheapest way to settle whether the material boundary is real?

ELI10: ...

Stakes if wrong: ...

Recommendation: B because ...

Completeness: A=4/10, B=9/10

A) Evaluate competing platforms first  (recommended)
   ✅ ...
   ❌ ...
B) Write the platform-neutral domain model, then prototype
   ✅ ...
   ❌ ...

Net: ...
```

If the harness provides a structured question tool (`ask_user_question` in dsh,
`AskUserQuestion` in Claude Code), the brief is delivered through it. Otherwise it is a
plain markdown message and the user's typed reply is the decision.

Calling an option **rejected** is never silent — excluded options are always named with
the reason for excluding them.

## Structure

```
SKILL.md                            the spine: four mechanisms, evidence rules, Phase 0-6
references/
  premises-and-evidence.md          premise extraction, provenance checks, evidence grading, posture
  decision-brief.md                 D<N> brief format, 4-option cap, exclusion-labelling rule
  decision-doc-template.md          output template + quality self-check
scripts/
  profile.py                        repo-local decision profile (read / summary / append)
provenance/                         the borrowed decision-brief format, kept as source of record
```

`SKILL.md` is the only always-loaded file (~175 lines); references load on demand.

## The memory layer

Written to `.agents/profile.md` inside the target repo, so it travels with the code and
works across harnesses. It complements task checkpoints rather than replacing them:

- **task checkpoints** (e.g. [`repo-checkpoint`](https://github.com/hotalexnet/agent-checkpoint)) — *where is this task*
- **decision profile** — *how does this person decide, and what do they keep getting stuck on*

```bash
python3 scripts/profile.py read      # at Phase 1
python3 scripts/profile.py append --kind technical --signal unvalidated_premise --note "..."
python3 scripts/profile.py summary   # aggregate across sessions, flag repeats
```

```console
$ python3 scripts/profile.py summary
sessions recorded: 3

recurring signals (push here first):
  unvalidated_premise        2   <-- repeating
  action_over_analysis       2   <-- repeating
  domain_expertise           1
```

Repeats are the point: they let a later session open with "you got stuck here last time"
instead of starting from zero.

The signal vocabulary lives in `scripts/profile.py`. Reuse it rather than inventing new
signals — if you see a pattern the vocabulary lacks, record it in `--note` and say so.

## Verifying it works

| Check | Pass condition |
| --- | --- |
| One question at a time | It stops after each question and waits |
| Evidence before position | It read the locally checkable evidence before taking a stance |
| Provenance checked | At least one key claim was challenged with "who said this?" |
| Premises challenged | At least one premise was marked unverified or overturned |
| Criteria are falsifiable | There is a "observing X means option A is wrong" entry |
| Profile written | `.agents/profile.md` contains real signals |
| No drift into implementation | It never started writing code or changing config |

### Known limitation

How sharp a review gets depends partly on the executing agent's own context — how much of
the repo it read, whether it checked the framework source. That cannot be separated from
what `SKILL.md` contributes on its own. A clean comparison would need a fresh session
holding nothing but `SKILL.md`.

This skill was extracted from a real session and has been run end to end once, on a
platform-selection decision, where it falsified a stated technical blocker by reading the
framework source. Treat the verification checklist as the honest bar, not the claim.

## Attribution

The decision-brief format, along with parts of the posture and anti-sycophancy rules, is
derived from [gstack](https://github.com/garrytan/gstack) by Garry Tan (MIT). See
[THIRD-PARTY-NOTICES.md](./THIRD-PARTY-NOTICES.md) for the per-file derivation and the
full license text.

The product/market skill that gstack's version came from was evaluated and deliberately
**not** carried over — it converges by market contact, which is a different mechanism.
See [`provenance/`](./provenance/README.md).

## License

MIT — see [LICENSE](./LICENSE).
