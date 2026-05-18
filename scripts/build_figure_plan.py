#!/usr/bin/env python3
"""Create a contribution-linked figure plan and figure-structure file."""

from __future__ import annotations

import argparse
from pathlib import Path
from _common import require_contributions

BASE_ROLES = [
    {"fig": "Fig. 1", "file": "fig_system_architecture.pdf", "section": "Introduction / Problem Description", "contrib": "C1", "purpose": "System/problem architecture", "structure": "A schematic showing system boundary, actors, resources, data flow, decisions, and market or operation layers.", "message": "The studied problem couples physical operation, data inputs, and decision-making in a defined system boundary."},
    {"fig": "Fig. 2", "file": "fig_method_workflow.pdf", "section": "Methodology", "contrib": "C1/C2", "purpose": "Method or algorithm workflow", "structure": "A flowchart from input data and model construction to solution, validation, and output decisions.", "message": "The proposed method follows a reproducible computational path rather than an ad hoc implementation."},
    {"fig": "Fig. 3", "file": "fig_main_comparison.pdf", "section": "Numerical Results", "contrib": "C2", "purpose": "Main comparison against baselines", "structure": "A bar chart, line chart, boxplot, or table-like figure comparing proposed and baseline methods on the central metric.", "message": "The proposed method changes the main metric under identical experimental settings."},
]

OPTIONAL_THIRD = {"fig": "Fig. 4", "file": "fig_mechanism_sensitivity.pdf", "section": "Numerical Results", "contrib": "C3", "purpose": "Mechanism or sensitivity analysis", "structure": "A sensitivity curve, heat map, ablation plot, or scenario comparison explaining the operating condition behind the result.", "message": "The result is explained by a mechanism rather than a purely numerical comparison."}

DOMAIN_SUGGESTIONS = """# Optional Domain-Specific Figure Candidates

Select these only when the project evidence supports them.

- Optimization scheduling: cost/profit decomposition, constraint violation profile, solver runtime and optimality gap.
- Electricity market or carbon market: price trajectories, bid/offer curves, cleared quantities, carbon-electricity coupling diagram.
- VPP/DER aggregation: feasible operation region, DER portfolio allocation, reserve-performance relationship.
- Frequency/security constraints: frequency nadir curves, inertia/damping sensitivity, contingency comparison.
- Network-constrained dispatch: line-loading heat map, nodal price map, congestion pattern, power-flow comparison.
- Data-driven optimization: prediction error distribution, surrogate-model accuracy, ablation study, embedded-model runtime.
- Data center or workload scheduling: workload migration flow, climate-zone comparison, cooling-energy decomposition.
"""


def build_plan(contributions: list[str]) -> str:
    roles = list(BASE_ROLES)
    if len(contributions) == 3:
        roles.append(OPTIONAL_THIRD)
    lines = ["# Figure Plan", "", "This plan is mandatory before drafting the manuscript body. Each figure must support at least one confirmed contribution and must be backed by a data source or drawing specification.", "", "## Confirmed contributions", ""]
    for i, c in enumerate(contributions, 1):
        lines.append(f"- C{i}: {c}")
    lines.extend(["", "## Planned figures", "", "| Fig. | Tentative filename | Section | Related contribution | Purpose | Source data/code | Key message |", "|---|---|---|---|---|---|---|"])
    for r in roles:
        lines.append(f"| {r['fig']} | `{r['file']}` | {r['section']} | {r['contrib']} | {r['purpose']} | TODO | {r['message']} |")
    lines.append("")
    lines.append(DOMAIN_SUGGESTIONS)
    return "\n".join(lines)


def build_structures(contributions: list[str]) -> str:
    roles = list(BASE_ROLES)
    if len(contributions) == 3:
        roles.append(OPTIONAL_THIRD)
    lines = ["# Figure Structures", "", "Keep figure-design details here. Do not put drawing instructions inside the LaTeX manuscript body.", ""]
    for r in roles:
        lines.extend([
            f"## {r['fig']}: {r['purpose']}", "",
            f"- Filename: `{r['file']}`",
            f"- Related contribution: {r['contrib']}",
            f"- Intended structure: {r['structure']}",
            f"- Intended message: {r['message']}",
            "- Panels: TODO",
            "- Axes and units: TODO",
            "- Data source or drawing source: TODO",
            "- Baselines or scenarios: TODO",
            "- Annotations: TODO",
            "- Style constraints: IEEE two-column readable fonts, vector output preferred, consistent notation.",
            "- Generation command: TODO",
            "- Caption draft: TODO",
            "- Evidence status: TODO", "",
        ])
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--contributions", type=Path, help="Markdown/text file with 2--3 confirmed contributions")
    ap.add_argument("--out", type=Path, default=Path("paper/figure_plan.md"))
    ap.add_argument("--structures-out", type=Path, default=Path("paper/figures/figure_structures.md"))
    ap.add_argument("--draft", action="store_true", help="Allow provisional placeholders for early planning only")
    args = ap.parse_args()

    contributions = require_contributions(args.contributions, draft=args.draft)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.structures_out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(build_plan(contributions), encoding="utf-8")
    args.structures_out.write_text(build_structures(contributions), encoding="utf-8")
    print(f"Wrote figure plan to {args.out}")
    print(f"Wrote figure structures to {args.structures_out}")
    print(f"Confirmed contributions: {len(contributions)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
