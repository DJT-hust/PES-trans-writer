#!/usr/bin/env python3
"""Validate that the manuscript narrative-planning files exist and are usable."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REQUIRED_FILES = [
    "narrative_logic_map.md",
    "section_logic_checklist.md",
    "contribution_map.md",
    "figure_plan.md",
    "figures/figure_structures.md",
    "claim_evidence_table.md",
]

MANDATORY_HEADINGS = [
    "One-sentence thesis",
    "System need",
    "Technical bottleneck",
    "Prior-work logic and gap",
    "Proposed mechanism",
    "Contribution-to-evidence chain",
    "Section-level storyline",
    "Result narrative plan",
]

TODO_RE = re.compile(r"\b(TODO|TBD|PLACEHOLDER|UNKNOWN|XXX|\?\?\?)\b", re.I)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paper", type=Path, help="Paper directory")
    ap.add_argument("--strict", action="store_true", help="Fail if narrative-planning files still contain TODO placeholders")
    args = ap.parse_args()

    issues = 0
    for rel in REQUIRED_FILES:
        p = args.paper / rel
        if not p.exists():
            print(f"MISSING: {p}")
            issues += 1
    narrative = args.paper / "narrative_logic_map.md"
    if narrative.exists():
        text = narrative.read_text(encoding="utf-8", errors="ignore")
        for heading in MANDATORY_HEADINGS:
            if heading not in text:
                print(f"MISSING HEADING in narrative_logic_map.md: {heading}")
                issues += 1
        contrib_rows = re.findall(r"\|\s*C[1-3]\s*\|", text)
        if len(contrib_rows) < 2:
            print("NARRATIVE ISSUE: contribution-to-evidence chain should contain at least C1 and C2 rows.")
            issues += 1
        if args.strict and TODO_RE.search(text):
            print("STRICT ISSUE: narrative_logic_map.md still contains TODO-style placeholders.")
            issues += 1
    if args.strict:
        for rel in REQUIRED_FILES:
            p = args.paper / rel
            if p.exists() and TODO_RE.search(p.read_text(encoding="utf-8", errors="ignore")):
                print(f"STRICT ISSUE: {rel} still contains TODO-style placeholders.")
                issues += 1

    if issues:
        print(f"Narrative logic validation found {issues} issue(s).")
        return 1
    print("Narrative logic gate passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
