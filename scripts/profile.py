#!/usr/bin/env python3
"""Repo-local decision profile for the decision-review skill.

Stores what we learn about *how this person decides* — across sessions, across agents,
inside the repo. This is the memory layer that makes the second review faster than
the first.

Usage:
    profile.py read
    profile.py summary
    profile.py append --kind technical --signal unvalidated_premise --note "..."
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# 复用，不要自创。缺信号时记进 note 并说明词表缺什么。
SIGNALS = {
    # 已经观察到的强项 —— 可以依赖
    "evidence_seeking",     # 主动去找可查的证据
    "provenance_checked",   # 会追问"这是谁说的"
    "reversed_on_evidence", # 被证据说服后改立场
    "domain_expertise",     # 领域知识扎实，结论具体
    "decisive",             # 能在信息不全时拍板
    "pushback",             # 顶回挑战，且理由自洽
    # 需要优先推的惯性 —— 下次先推这里
    "unvalidated_premise",  # 带着未验证前提往下走
    "sourced_from_handoff", # 关键事实只存在于交接笔记/聊天记录
    "authority_confusion",  # 内部判断被当成外部要求
    "action_over_analysis", # 用动手回避建模
    "sunk_cost_reasoning",  # 用"已经投入了"当理由
    "preference_as_principle",  # 偏好被包装成架构原则/最佳实践
    "scope_creep",
}

KINDS = ["technical", "commercial", "process", "org", "mixed"]

HEADER = """# Decision Profile

Repo-local decision calibration for the decision-review skill.
Read at Phase 1. Append at Phase 6. Do not invent signals outside the vocabulary.

## Sessions
"""


def repo_root() -> Path:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return Path(out)
    except (subprocess.CalledProcessError, FileNotFoundError):
        sys.exit("error: not inside a git repository (this profile is repo-local by design)")


def profile_path() -> Path:
    return repo_root() / ".agents" / "profile.md"


def _collect(text: str, field: str) -> Counter[str]:
    c: Counter[str] = Counter()
    for line in text.splitlines():
        m = re.match(rf"^-\s*{field}:\s*(.+)$", line)
        if m:
            for item in (x.strip() for x in m.group(1).split(",")):
                if item:
                    c[item] += 1
    return c


def cmd_read(_args: argparse.Namespace) -> None:
    path = profile_path()
    if not path.exists():
        print("(no profile yet — this is a cold first session)")
        return
    print(path.read_text(encoding="utf-8").rstrip())


def cmd_summary(_args: argparse.Namespace) -> None:
    path = profile_path()
    if not path.exists():
        print("(no profile yet)")
        return
    text = path.read_text(encoding="utf-8")

    print(f"sessions recorded: {text.count(chr(10) + '### ')}")

    signals = _collect(text, "signals")
    if signals:
        print("\nrecurring signals (push here first):")
        for name, n in signals.most_common():
            print(f"  {name:26} {n}{'   <-- repeating' if n > 1 else ''}")

    kinds = _collect(text, "kind")
    if kinds:
        print("\ndecision kinds:")
        for name, n in kinds.most_common():
            print(f"  {name:26} {n}")

    topics = _collect(text, "topics")
    if topics:
        print("\ntopics:")
        for name, n in topics.most_common(10):
            print(f"  {name:26} {n}")

    if not signals and not topics:
        print("(profile exists but carries no signals yet)")


def cmd_append(args: argparse.Namespace) -> None:
    bad = [s for s in args.signal if s not in SIGNALS]
    if bad:
        sys.exit(
            f"error: unknown signal(s): {', '.join(bad)}\n"
            f"valid: {', '.join(sorted(SIGNALS))}\n"
            "if the pattern you saw is missing, record it in --note instead of inventing a signal"
        )
    if not args.signal and not args.note:
        sys.exit("error: nothing to record; pass --signal and/or --note")

    path = profile_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(HEADER, encoding="utf-8")

    stamp = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")
    block = [f"\n### {stamp}\n"]
    if args.kind:
        block.append(f"- kind: {args.kind}")
    if args.signal:
        block.append(f"- signals: {', '.join(args.signal)}")
    if args.topic:
        block.append(f"- topics: {', '.join(args.topic)}")
    if args.note:
        for line in args.note.splitlines():
            block.append(f"- note: {line.strip()}")
    if args.assignment:
        block.append(f"- assignment: {args.assignment}")

    with path.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(block) + "\n")

    print(f"appended to {path}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("read", help="print the full profile").set_defaults(func=cmd_read)
    sub.add_parser("summary", help="aggregate signals, kinds and topics").set_defaults(func=cmd_summary)

    ap = sub.add_parser("append", help="record one session's observations")
    ap.add_argument("--kind", choices=KINDS, help="what kind of decision this was")
    ap.add_argument("--signal", action="append", default=[], help="repeatable; see SIGNALS in this file")
    ap.add_argument("--topic", action="append", default=[], help="repeatable")
    ap.add_argument("--note", help="one specific observation, ideally quoting the user")
    ap.add_argument("--assignment", help="the action you handed them")
    ap.set_defaults(func=cmd_append)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
