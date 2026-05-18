#!/usr/bin/env python3
"""Lightweight checks for IEEE-style LaTeX manuscript drafts."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import List, Set

AI_PATTERNS = [
    r"\bdelves into\b",
    r"\bin today's rapidly evolving\b",
    r"\bcutting-edge\b",
    r"\binnovative framework\b",
    r"\bcomprehensive analysis\b",
    r"\bsuperiority of the proposed\b",
    r"\bsignificantly improves\b(?![^.]*\d)",
    r"\bit is worth noting that\b",
]


def read_with_inputs(path: Path, seen: Set[Path] | None = None) -> str:
    seen = seen or set()
    path = path.resolve()
    if path in seen or not path.exists():
        return ""
    seen.add(path)
    text = path.read_text(encoding="utf-8", errors="replace")
    base = path.parent
    for m in re.finditer(r"\\(?:input|include)\{([^}]+)\}", text):
        child = base / m.group(1)
        if child.suffix != ".tex":
            child = child.with_suffix(".tex")
        text += "\n" + read_with_inputs(child, seen)
    return text


def figure_paths(text: str) -> List[str]:
    return re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", text)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tex", type=Path, help="main.tex or section tex file")
    ap.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = ap.parse_args()

    text = read_with_inputs(args.tex)
    warnings: List[str] = []
    errors: List[str] = []

    if not text:
        errors.append(f"Could not read TeX source: {args.tex}")
    if "`" in text:
        errors.append("Backtick characters found in TeX source. Use \\texttt{...} or LaTeX quotes instead.")
    if "```" in text:
        errors.append("Markdown code fences found in TeX source.")

    if "\\begin{abstract}" in text:
        abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, flags=re.S)
        if abstract:
            a = abstract.group(1)
            if "\\cite" in a:
                errors.append("Abstract contains citations.")
            if re.search(r"\\begin\{equation\}|\\\[", a):
                errors.append("Abstract contains displayed equations.")
            word_count = len(re.findall(r"[A-Za-z0-9]+", a))
            if word_count and not (120 <= word_count <= 230):
                warnings.append(f"Abstract word count is {word_count}; target about 150--200 words.")

    for pat in AI_PATTERNS:
        if re.search(pat, text, flags=re.I):
            warnings.append(f"Possible AI-style phrase: `{pat}`")

    labels = set(re.findall(r"\\label\{([^}]+)\}", text))
    refs = set(re.findall(r"\\(?:ref|eqref)\{([^}]+)\}", text))
    for label in sorted(refs - labels)[:20]:
        warnings.append(f"Reference without local label: {label}")

    active_lines = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("%"))
    base = args.tex.parent if args.tex.is_file() else args.tex
    for fig in figure_paths(active_lines):
        candidates = [base / fig, base / (fig + ".pdf"), base / (fig + ".png"), base / (fig + ".eps")]
        if not any(p.exists() for p in candidates):
            warnings.append(f"Included graphic file appears missing: {fig}")

    if "TODO" in text or "\\draftnote" in text:
        warnings.append("Draft still contains TODO or draft-note placeholders.")

    if errors:
        print("Sanity-check errors:")
        for e in errors:
            print(f"- {e}")
    if warnings:
        print("Sanity-check warnings:")
        for w in warnings:
            print(f"- {w}")
    if not errors and not warnings:
        print("No common issues found by lightweight sanity check.")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
