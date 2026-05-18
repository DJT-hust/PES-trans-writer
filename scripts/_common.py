#!/usr/bin/env python3
"""Shared utilities for PES-trans-writer scripts."""

from __future__ import annotations

import re
from pathlib import Path
from typing import List

PLACEHOLDER_RE = re.compile(r"\b(TODO|TBD|PLACEHOLDER|INSERT|UNKNOWN|XXX|\?\?\?)\b", re.I)


def has_placeholder(text: str) -> bool:
    return bool(PLACEHOLDER_RE.search(text or ""))


def latex_escape(text: str) -> str:
    """Escape text intended for normal LaTeX text mode."""
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(ch, ch) for ch in text)


def parse_contributions(path: Path) -> List[str]:
    """Extract 2--3 contribution statements from a markdown/text file.

    Accepted forms include:
    - C1: statement
    - 1. statement
    - - statement
    - * statement

    Lines containing obvious placeholders are ignored.
    """
    if not path.exists():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8", errors="replace")
    items: List[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        line = re.sub(r"^[-*]\s+", "", line)
        line = re.sub(r"^(?:Contribution\s*)?C?\s*[1-3]\s*[:.)-]\s*", "", line, flags=re.I)
        line = line.strip()
        if not line or has_placeholder(line):
            continue
        if len(re.findall(r"[A-Za-z0-9]", line)) < 25:
            continue
        items.append(line)
    seen = set()
    out: List[str] = []
    for item in items:
        key = re.sub(r"\s+", " ", item.lower())
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out[:3]


def require_contributions(path: Path | None, draft: bool = False) -> List[str]:
    """Return confirmed contributions, or fail unless draft mode is enabled."""
    if draft:
        if path and path.exists():
            parsed = parse_contributions(path)
            if 2 <= len(parsed) <= 3:
                return parsed
        return [
            "Draft contribution placeholder: replace this item with a verified methodological contribution before manuscript drafting.",
            "Draft contribution placeholder: replace this item with a verified experimental or analytical contribution before manuscript drafting.",
        ]
    if path is None:
        raise SystemExit(
            "ERROR: confirmed contributions are required. Provide --contributions path/to/contributions.md "
            "with exactly 2 or 3 non-placeholder items, or use --draft only for a non-submission skeleton."
        )
    parsed = parse_contributions(path)
    if not (2 <= len(parsed) <= 3):
        raise SystemExit(
            f"ERROR: expected 2 or 3 confirmed non-placeholder contributions in {path}; found {len(parsed)}.\n"
            "Use templates/contribution_intake_form.md and write each item as C1:, C2:, and optional C3:."
        )
    return parsed


def tex_comment(text: str) -> str:
    return "\n".join("% " + line if line else "%" for line in text.splitlines())
