#!/usr/bin/env python3
"""Create the manuscript-level narrative logic map.

This is a planning gate before section prose drafting. It forces the paper to
follow a single argument from system need to contribution-specific evidence.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from _common import require_contributions


def build_narrative_map(contributions: list[str], target_journal: str, title: str | None = None) -> str:
    title_line = title or "TODO"
    lines = [
        "# Narrative Logic Map",
        "",
        "This file is a required manuscript-planning gate. Complete it before drafting prose for the abstract, introduction, methodology, case studies, numerical results, or conclusion.",
        "",
        "## Metadata",
        "",
        f"- Working title: {title_line}",
        f"- Target journal: {target_journal}",
        "- Manuscript type: IEEE PES Transactions-style research article",
        "",
        "## 1. One-sentence thesis",
        "",
        "- Thesis: TODO",
        "",
        "The thesis should connect the system need, the unresolved technical bottleneck, and the proposed mechanism in one sentence. Avoid a generic phrase such as \"a novel framework is proposed.\"",
        "",
        "## 2. System need",
        "",
        "- Studied system or market: TODO",
        "- Operational, economic, security, or sustainability need: TODO",
        "- Why the need matters for IEEE PES readers: TODO",
        "",
        "## 3. Technical bottleneck",
        "",
        "- Bottleneck in current practice or modeling: TODO",
        "- Why this bottleneck is nontrivial: TODO",
        "- What happens if it is ignored: TODO",
        "",
        "## 4. Prior-work logic and gap",
        "",
        "Group the literature by technical route rather than listing papers one by one.",
        "",
        "| Literature group | Representative verified citations | What they handle well | Remaining limitation relative to this paper |",
        "|---|---|---|---|",
        "| Group 1: TODO | TODO | TODO | TODO |",
        "| Group 2: TODO | TODO | TODO | TODO |",
        "| Group 3: TODO | TODO | TODO | TODO |",
        "",
        "- Gap statement: TODO",
        "",
        "## 5. Proposed mechanism",
        "",
        "- Core technical idea: TODO",
        "- Why the idea addresses the gap: TODO",
        "- Main assumptions: TODO",
        "- Boundary of the claim: TODO",
        "",
        "## 6. Confirmed contributions",
        "",
    ]
    for i, c in enumerate(contributions, 1):
        lines.append(f"- C{i}: {c}")
    lines.extend([
        "",
        "## 7. Contribution-to-evidence chain",
        "",
        "Every contribution must map to a method element, a figure or table, and at least one verification item.",
        "",
        "| Contribution | Gap addressed | Method element | Key equation/algorithm | Figure/table | Verification experiment | Expected result paragraph |",
        "|---|---|---|---|---|---|---|",
    ])
    for i, _ in enumerate(contributions, 1):
        lines.append(f"| C{i} | TODO | TODO | TODO | TODO | TODO | TODO |")
    lines.extend([
        "",
        "## 8. Section-level storyline",
        "",
        "| Section | Local purpose | Required opening move | Required closing move | Evidence dependency |",
        "|---|---|---|---|---|",
        "| Abstract | Compact argument | Problem and gap | Key verified implication | Contribution map; claim-evidence table |",
        "| Introduction | Motivate and position the paper | System need | Contributions and organization | Verified references; narrative gap |",
        "| Problem Formulation | Define the studied decision problem | System boundary and assumptions | Baseline limitation or transition to method | Code/model audit |",
        "| Methodology | Explain how the gap is addressed | Core idea linked to C1 | Reproducible procedure linked to C2/C3 | Equations; algorithms; implementation notes |",
        "| Case Studies | Make validation credible | Test system and data | Metrics and baselines | Data inventory; solver settings |",
        "| Numerical Results | Prove contributions with evidence | Main observation | Mechanism and implication | Figures; tables; claim-evidence table |",
        "| Conclusion | Close without new claims | What was solved | Verified implication and limitation | Final checked claims |",
        "",
        "## 9. Result narrative plan",
        "",
        "Each result subsection should follow: observation -> numerical evidence -> mechanism -> implication.",
        "",
        "| Result subsection | Related contribution | Main observation | Numerical evidence source | Mechanism to explain | Practical implication |",
        "|---|---|---|---|---|---|",
    ])
    for i, _ in enumerate(contributions, 1):
        lines.append(f"| TODO result for C{i} | C{i} | TODO | TODO | TODO | TODO |")
    lines.extend([
        "",
        "## 10. Risk controls",
        "",
        "- Claims that must not be made without further evidence: TODO",
        "- References that still require verification: TODO",
        "- Figures that still lack data or drawing specifications: TODO",
        "- Assumptions that must be stated explicitly: TODO",
        "",
        "## 11. Drafting rule",
        "",
        "Do not draft final prose until Sections 1--10 are filled with project-specific content and no longer contain generic TODO placeholders for the core thesis, gap, proposed mechanism, and contribution-to-evidence chain.",
        "",
    ])
    return "\n".join(lines)


def build_section_logic_checklist(contributions: list[str]) -> str:
    rows = []
    for i, _ in enumerate(contributions, 1):
        rows.append(f"| C{i} | Methodology subsection | Key equation/algorithm | Figure/table | Result paragraph | TODO |")
    return "\n".join([
        "# Section Logic Checklist",
        "",
        "Use this checklist during drafting and revision. Each section must serve the manuscript narrative rather than stand alone as a generic template.",
        "",
        "## Contribution coverage",
        "",
        "| Contribution | Method section location | Equation/algorithm | Figure/table | Result paragraph | Status |",
        "|---|---|---|---|---|---|",
        *rows,
        "",
        "## Per-section checks",
        "",
        "- Abstract: problem -> gap -> method -> validation -> verified implication.",
        "- Introduction: system need -> technical bottleneck -> grouped literature -> gap -> contributions -> organization.",
        "- Problem Formulation: boundary -> assumptions -> notation -> baseline model -> limitation.",
        "- Methodology: core idea -> formulation/reformulation -> solution procedure -> tractability/reproducibility.",
        "- Case Studies: data/test system -> baselines -> metrics -> solver/hardware -> scenarios.",
        "- Numerical Results: observation -> numerical evidence -> mechanism -> implication.",
        "- Conclusion: solved problem -> method summary -> verified findings -> limitations/implication.",
    ]) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--contributions", type=Path, help="Markdown/text file with 2--3 confirmed contributions")
    ap.add_argument("--out", type=Path, default=Path("paper/narrative_logic_map.md"))
    ap.add_argument("--section-checklist-out", type=Path, default=Path("paper/section_logic_checklist.md"))
    ap.add_argument("--title", default=None)
    ap.add_argument("--target-journal", default="IEEE PES Transactions")
    ap.add_argument("--draft", action="store_true", help="Allow provisional placeholders for early planning only")
    args = ap.parse_args()

    contributions = require_contributions(args.contributions, draft=args.draft)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.section_checklist_out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(build_narrative_map(contributions, args.target_journal, args.title), encoding="utf-8")
    args.section_checklist_out.write_text(build_section_logic_checklist(contributions), encoding="utf-8")
    print(f"Wrote narrative logic map to {args.out}")
    print(f"Wrote section logic checklist to {args.section_checklist_out}")
    print(f"Confirmed contributions: {len(contributions)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
