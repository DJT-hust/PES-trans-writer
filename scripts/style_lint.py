#!/usr/bin/env python3
"""Lightweight style lint for IEEE PES manuscript drafts.

This script flags generic AI-sounding phrases and unsupported novelty language.
It does not prove quality; it provides a checklist for human revision.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

BANNED_PATTERNS = {
    r"\bit is worth noting that\b": "Use the sentence only if it adds a concrete mechanism; otherwise delete it.",
    r"\bin today'?s rapidly evolving\b": "Replace generic context with a concrete power-system consequence.",
    r"\bcomprehensive analysis\b": "Specify the cases, metrics, and mechanisms analyzed.",
    r"\bextensive simulations?\b": "Specify the test system, scenarios, and metrics.",
    r"\bsuperior performance\b": "Quantify the comparison or state the mechanism.",
    r"\bsignificant(?:ly)? improve[sd]?\b": "Quantify the improvement or mark as TODO.",
    r"\bnovel framework\b": "Name the technical novelty instead of saying 'novel framework'.",
    r"\bcutting-edge\b": "Use a technical descriptor.",
    r"\brevolutioni[sz]e[sd]?\b": "Avoid marketing language.",
    r"\bpaves? the way\b": "State the practical implication directly.",
    r"\bto the best of (?:the )?authors'? knowledge\b": "Use only with a documented literature search.",
    r"\bfor the first time\b": "Use only with a documented literature search.",
}

WEAK_RESULT_PATTERNS = [
    r"Fig\.\s*~?\\ref\{[^}]+\}\s+shows\s+the\s+effectiveness",
    r"Table\s*~?\\ref\{[^}]+\}\s+shows\s+the\s+effectiveness",
    r"results\s+validate\s+the\s+effectiveness",
]


def iter_tex_files(path: Path):
    if path.is_file():
        yield path
    else:
        yield from path.rglob("*.tex")
        yield from path.rglob("*.md")


def main() -> int:
    parser = argparse.ArgumentParser(description="Flag generic phrases in IEEE PES manuscript drafts.")
    parser.add_argument("path", type=Path, help="A .tex/.md file or a manuscript folder")
    args = parser.parse_args()

    files = list(iter_tex_files(args.path))
    if not files:
        print("No .tex or .md files found.")
        return 1

    issues = 0
    for file in files:
        text = file.read_text(encoding="utf-8", errors="ignore")
        lines = text.splitlines()
        for i, line in enumerate(lines, start=1):
            lowered = line.lower()
            for pat, advice in BANNED_PATTERNS.items():
                if re.search(pat, lowered, flags=re.IGNORECASE):
                    print(f"{file}:{i}: generic phrase -> {line.strip()}")
                    print(f"  advice: {advice}")
                    issues += 1
            for pat in WEAK_RESULT_PATTERNS:
                if re.search(pat, line, flags=re.IGNORECASE):
                    print(f"{file}:{i}: weak result sentence -> {line.strip()}")
                    print("  advice: add numerical evidence and a mechanism-level explanation.")
                    issues += 1
    if issues == 0:
        print("No obvious generic IEEE PES style issues found.")
    else:
        print(f"Found {issues} potential style issue(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
