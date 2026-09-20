#!/usr/bin/env python3
"""Validate this skill's SKILL.md frontmatter and its internal references.

Checks the failure modes a harness will trip over — all of which are silent:

- the frontmatter fence opens and closes
- the block is valid YAML. An unquoted scalar containing ": " breaks every
  consumer, and the symptom is "the skill never triggers", not an error.
- `name` is present and kebab-case
- `description` is present and within the limits consumers enforce
- every references/ path named in SKILL.md actually exists

Run:  python3 scripts/validate.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("error: PyYAML is required.  Install with: pip install pyyaml")

SKILL_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD = SKILL_ROOT / "SKILL.md"

# Limits consumers actually enforce. Keep these in sync if a harness changes.
#   dsh   — catalogDescriptionMaxLength defaults to 500, past which it truncates
#   Codex — descriptionLimit is 1024 with descriptionLimitBehavior "error"
TRUNCATE_AT = 500
REJECT_AT = 1024

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REF_RE = re.compile(r"references/[A-Za-z0-9._-]+\.md")

errors: list[str] = []
warnings: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def warn(message: str) -> None:
    warnings.append(message)


def load_frontmatter() -> tuple[dict | None, str]:
    """Return (parsed frontmatter, full SKILL.md text)."""
    if not SKILL_MD.exists():
        fail(f"{SKILL_MD} not found")
        return None, ""

    text = SKILL_MD.read_text(encoding="utf-8")
    if not text.startswith("---"):
        fail("SKILL.md does not start with a '---' frontmatter fence")
        return None, text

    end = text.find("\n---", 3)
    if end == -1:
        fail("SKILL.md frontmatter fence is never closed")
        return None, text

    block = text[3:end].strip("\n")

    if "\t" in block:
        fail("frontmatter contains a tab; YAML forbids tabs as indentation")

    try:
        data = yaml.safe_load(block)
    except yaml.YAMLError as exc:
        fail(f"frontmatter is not valid YAML:\n{exc}")
        return None, text

    if not isinstance(data, dict):
        fail("frontmatter did not parse into a mapping")
        return None, text

    return data, text


def check_name(data: dict) -> None:
    name = data.get("name")
    if not name or not str(name).strip():
        fail("frontmatter is missing `name`")
        return
    name = str(name).strip()
    if not NAME_RE.match(name):
        fail(f"`name` is not kebab-case: {name!r}")
    if name != SKILL_ROOT.name:
        warn(f"`name` ({name}) differs from the directory name ({SKILL_ROOT.name}) — legal, but check it's intended")


def check_description(data: dict) -> None:
    description = data.get("description")
    if description is None or not str(description).strip():
        fail("frontmatter is missing `description` (a skill with no description never triggers)")
        return

    length = len(str(description).strip())
    if length > REJECT_AT:
        fail(f"description is {length} chars; Codex rejects past {REJECT_AT}")
    elif length > TRUNCATE_AT:
        warn(f"description is {length} chars; dsh truncates past {TRUNCATE_AT} (the tail is lost silently)")
    else:
        print(f"  description: {length} chars (under dsh's {TRUNCATE_AT})")


def check_references(text: str) -> None:
    """Check both directions: referenced files exist, and nothing is orphaned.

    Orphans matter because a file in references/ that SKILL.md never points at is
    content no agent will ever read — the skill silently loses whatever it describes.
    Reachability follows links transitively, so a file referenced only from another
    reference still counts.
    """
    body = text.split("\n---\n", 1)[-1]
    ref_dir = SKILL_ROOT / "references"

    reached: set[str] = set()
    frontier = set(REF_RE.findall(body))
    while frontier:
        ref = frontier.pop()
        if ref in reached:
            continue
        reached.add(ref)
        path = SKILL_ROOT / ref
        if path.exists():
            frontier |= set(REF_RE.findall(path.read_text(encoding="utf-8")))

    missing = sorted(r for r in reached if not (SKILL_ROOT / r).exists())
    for ref in missing:
        fail(f"SKILL.md references {ref}, which does not exist")

    orphans: list[str] = []
    if ref_dir.is_dir():
        for path in sorted(ref_dir.glob("*.md")):
            rel = f"references/{path.name}"
            if rel not in reached:
                orphans.append(rel)
    for orphan in orphans:
        fail(f"{orphan} exists but nothing points at it — no agent will ever read it")

    if not missing and not orphans:
        print(f"  references: {len(reached)} reachable, none orphaned")


def main() -> int:
    print(f"validating {SKILL_MD.relative_to(SKILL_ROOT.parent)}")

    data, text = load_frontmatter()
    if data is not None:
        check_name(data)
        check_description(data)
        check_references(text)

    for message in warnings:
        print(f"  warning: {message}")
    for message in errors:
        print(f"  ERROR:   {message}")

    if errors:
        print(f"\n{len(errors)} error(s)")
        return 1
    print("\nok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
