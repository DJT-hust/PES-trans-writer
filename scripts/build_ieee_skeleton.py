#!/usr/bin/env python3
"""Build a compile-safe IEEEtran-compatible LaTeX manuscript skeleton.

Strict mode requires 2--3 confirmed contributions. Use --draft only when the
user explicitly wants an early scaffold that is not ready for manuscript text.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from _common import latex_escape, require_contributions
from build_narrative_map import build_narrative_map, build_section_logic_checklist

MAIN_TEX = r'''\documentclass[journal]{IEEEtran}

\input{macros}

\begin{document}

\title{__TITLE__}

\author{Author~One,~\IEEEmembership{Member,~IEEE,}
        Author~Two,~\IEEEmembership{Senior~Member,~IEEE}%
\thanks{This work was supported in part by ...}%
\thanks{Author One and Author Two are with ... (e-mail: ...).}%
}

\maketitle

\input{sections/abstract}

\begin{IEEEkeywords}
Power systems, optimization, electricity markets, renewable energy integration.
\end{IEEEkeywords}

\input{sections/introduction}
\input{sections/nomenclature}
\input{sections/problem_formulation}
\input{sections/methodology}
\input{sections/case_studies}
\input{sections/results}
\input{sections/conclusion}

\appendices
\input{sections/appendix}

\bibliographystyle{IEEEtran}
\bibliography{refs}

\end{document}
'''

MACROS = r'''% Common packages compatible with IEEEtran. Keep the list minimal.
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{array}
\usepackage{cite}
\usepackage{xcolor}
\graphicspath{{figures/}}

% Draft helpers. Remove or disable before submission if required.
\newcommand{\draftnote}[1]{\textcolor{red}{[Draft note: #1]}}
\newcommand{\vect}[1]{\boldsymbol{#1}}
\newcommand{\set}[1]{\mathcal{#1}}
\newcommand{\E}{\mathbb{E}}
'''


def intro_section(contributions: list[str], draft: bool) -> str:
    bullets = "\n".join(f"  \\item {latex_escape(c)}" for c in contributions)
    draft_note = (
        "\n\\draftnote{The contribution bullets are provisional because this skeleton was generated in draft mode.}\n"
        if draft else ""
    )
    return rf'''\section{{Introduction}}
\label{{sec:introduction}}

The increasing integration of renewable generation, distributed energy resources, and market-based operational mechanisms has reshaped the scheduling and decision-making problems faced by modern power systems. A manuscript should first identify the studied system boundary, the operational or market signal that motivates the problem, and the technical reason why existing approaches are insufficient.

Existing studies should be grouped by technical route rather than listed one by one. Typical groups include model-based optimization, robust or stochastic optimization, data-driven surrogate modeling, market-participation models, and power-system security constrained scheduling. After the grouped review, state the unresolved gap with a precise scope. The final prose should follow the completed narrative logic map rather than this placeholder text.

To address the above gap, this paper develops the proposed method and validates it using the supplied project code, data, and experiments. The main contributions are summarized as follows:{draft_note}
\begin{{itemize}}
{bullets}
\end{{itemize}}

The remainder of this paper is organized as follows. Section~\ref{{sec:problem_formulation}} describes the studied problem. Section~\ref{{sec:methodology}} presents the proposed method. Section~\ref{{sec:case_studies}} introduces the case-study settings. Section~\ref{{sec:results}} discusses the numerical results. Section~\ref{{sec:conclusion}} concludes the paper.
'''


def build_sections(contributions: list[str], draft: bool) -> dict[str, str]:
    return {
        "abstract.tex": r'''\begin{abstract}
This paragraph is a compile-safe placeholder. Replace it with a 150--200 word abstract after the contribution map, figure plan, reference audit, and claim-evidence table are complete. The final abstract should state the problem, the specific gap, the proposed method, the data or test system, the most important numerical finding, and the implication. It should not contain citations, displayed equations, tables, footnotes, or unverified numerical claims.
\end{abstract}
''',
        "introduction.tex": intro_section(contributions, draft),
        "nomenclature.tex": r'''\section{Nomenclature}
\label{sec:nomenclature}

\begin{IEEEdescription}[\IEEEusemathlabelsep\IEEEsetlabelwidth{$P_{g,t}^{\max}$}]
\item[$\mathcal{T}$] Set of time intervals.
\item[$\mathcal{G}$] Set of dispatchable generators.
\item[$P_{g,t}$] Active power output of generator $g$ at time $t$.
\end{IEEEdescription}
''',
        "problem_formulation.tex": r'''\section{Problem Formulation}
\label{sec:problem_formulation}

This section should define the system boundary, decision variables, exogenous inputs, and baseline model. Replace the placeholder formulation below with equations extracted from the verified code or project notes.

\begin{equation}
\min_{x \in \mathcal{X}} \; f(x)
\label{eq:generic_objective}
\end{equation}

\begin{equation}
g(x) \leq 0.
\label{eq:generic_constraint}
\end{equation}
''',
        "methodology.tex": r'''\section{Methodology}
\label{sec:methodology}

This section should describe the proposed model, algorithm, or data-driven component. Define assumptions before equations, explain each approximation, and connect every subsection to one of the confirmed contributions.

\subsection{Proposed Model}
\label{subsec:proposed_model}

The proposed model should be written here using symbols consistent with Section~\ref{sec:nomenclature}. Avoid introducing results or claims that are not supported by the claim-evidence table.

\subsection{Implementation Procedure}
\label{subsec:implementation_procedure}

The solution procedure should be described in a reproducible manner, including solver settings, stopping criteria, random seeds, and data preprocessing steps when applicable.
''',
        "case_studies.tex": r'''\section{Case Studies}
\label{sec:case_studies}

This section should state the test system, data source, time resolution, solver, hardware, baseline methods, and scenario settings.

\begin{table}[!t]
\centering
\caption{Main Simulation Settings}
\label{tab:simulation_settings}
\begin{tabular}{lll}
\toprule
Item & Setting & Source \\
\midrule
Test system & To be verified & Project files \\
Time resolution & To be verified & Project files \\
Solver & To be verified & Project files \\
Baseline & To be verified & Project files \\
\bottomrule
\end{tabular}
\end{table}
''',
        "results.tex": r'''\section{Numerical Results}
\label{sec:results}

Present each result paragraph using the sequence of observation, numerical evidence, mechanism, and implication. Use \texttt{figure\_plan.md} and \texttt{figures/figure\_structures.md} to determine which figures belong in this section. Do not insert a formal figure environment until the corresponding file exists and its data source has been recorded in \texttt{claim\_evidence\_table.md}.

% Example compile-safe figure block. Uncomment only after the file exists.
% \begin{figure}[!t]
%   \centering
%   \IfFileExists{figures/fig_main_comparison.pdf}{%
%     \includegraphics[width=0.95\linewidth]{figures/fig_main_comparison.pdf}%
%   }{\fbox{\parbox{0.9\linewidth}{Figure file not generated yet.}}}
%   \caption{Replace with a mechanism-oriented caption linked to the relevant contribution.}
%   \label{fig:main_comparison}
% \end{figure}
''',
        "conclusion.tex": r'''\section{Conclusion}
\label{sec:conclusion}

Summarize the problem addressed, the proposed method, the most important verified findings, and the practical implication. Do not introduce new results, new references, or unsupported future-work claims.
''',
        "appendix.tex": r'''\section{Additional Model Details}
\label{app:model_details}

Put lengthy derivations, extra constraints, parameter tables, proof details, or data-cleaning details here.
''',
    }


def contribution_map(contributions: list[str]) -> str:
    chunks = ["# Contribution Map", "", "Every contribution must be supported by method text, equations or algorithms, experiments, figures or tables, and result paragraphs.", ""]
    for i, c in enumerate(contributions, 1):
        chunks.extend([
            f"## C{i}", "",
            f"- Statement: {c}",
            "- Related files: TODO",
            "- Method section support: TODO",
            "- Equation/algorithm support: TODO",
            "- Experiment/table/figure support: TODO",
            "- Result paragraph support: TODO",
            "- Status: draft / verified", "",
        ])
    return "\n".join(chunks)


def figure_plan_stub(contributions: list[str]) -> str:
    rows = [
        "# Figure Plan", "",
        "Finalize this file before drafting the manuscript body. Each figure must support one of the confirmed contributions and must have a matching structure block in `figures/figure_structures.md`.", "",
        "| Fig. | Tentative filename | Section | Related contribution | Purpose | Source data/code | Key message |",
        "|---|---|---|---|---|---|---|",
        "| Fig. 1 | `fig_system_architecture.pdf` | Introduction / Problem Description | C1 | System/problem architecture | TODO | Shows the studied system boundary and information flow. |",
        "| Fig. 2 | `fig_method_workflow.pdf` | Methodology | C1/C2 | Method or algorithm workflow | TODO | Shows how the proposed model is implemented. |",
        "| Fig. 3 | `fig_main_comparison.pdf` | Numerical Results | C2 | Main comparison against baselines | TODO | Quantifies the central performance difference. |",
    ]
    if len(contributions) == 3:
        rows.append("| Fig. 4 | `fig_mechanism_sensitivity.pdf` | Numerical Results | C3 | Mechanism or sensitivity analysis | TODO | Explains when and why the method works. |")
    return "\n".join(rows) + "\n"


def figure_structures_stub(contributions: list[str]) -> str:
    entries = [("Fig. 1: System/problem architecture", "C1"), ("Fig. 2: Method or algorithm workflow", "C1/C2"), ("Fig. 3: Main numerical comparison", "C2")]
    if len(contributions) == 3:
        entries.append(("Fig. 4: Mechanism or sensitivity analysis", "C3"))
    out = ["# Figure Structures", "", "Keep drawing-level notes here, separate from the LaTeX manuscript.", ""]
    for title, contrib in entries:
        out.extend([
            f"## {title}", "",
            f"- Related contribution: {contrib}",
            "- Intended message: TODO",
            "- Layout: TODO",
            "- Panels: TODO",
            "- Axes/units: TODO",
            "- Data source: TODO",
            "- Baselines: TODO",
            "- Annotations: TODO",
            "- Caption draft: TODO",
            "- Generation command: TODO",
            "- Verification status: TODO", "",
        ])
    return "\n".join(out)


REFS = """@comment{Do not invent references. Add only verified BibTeX entries here.}
@comment{Each cited key must have a matching audit block in reference_audit.md.}
"""

REFERENCE_AUDIT = """# Reference Audit

Every cited BibTeX key in `refs.bib` must have one block below. Script checks are mechanical only. Google Scholar, IEEE Xplore or another primary publisher page, DOI/Crossref metadata, and venue-quality checks must be performed before a citation is inserted into the manuscript.

## Summary

- Total BibTeX entries: TODO
- Total cited entries: TODO
- Entries requiring manual verification: TODO

## Audit entries

### `bibkey_todo`

- Claim supported: TODO
- Verified title: TODO
- Verified authors: TODO
- Verified venue/year: TODO
- DOI or stable source: TODO
- Google Scholar check: TODO; query used: `TODO`
- Primary source checked: TODO; source: TODO
- Venue quality reason: TODO
- Warning-list / MDPI check: TODO
- Metadata consistency: TODO
- Notes: TODO
"""

CLAIM_EVIDENCE = """# Claim-Evidence Table

Use this ledger to prevent unsupported claims and invented numerical results.

| Claim ID | Claim text | Source file or experiment | Result value | Figure/table | LaTeX location | Reference support | Status |
|---|---|---|---|---|---|---|---|
| CL1 | TODO | TODO | TODO | TODO | TODO | TODO | TODO |
"""

REPRO_MANIFEST = """# Reproducibility Manifest

## Project snapshot

- Project path: TODO
- Inventory file: TODO
- Code commit or archive hash: TODO
- Data version: TODO

## Environment

- Operating system: TODO
- Python/MATLAB/Julia version: TODO
- Solver and version: TODO
- Key package versions: TODO
- Random seeds: TODO

## Experiment commands

| Experiment | Command | Output files | Used in paper |
|---|---|---|---|
| TODO | TODO | TODO | TODO |

## Notes

Record any manual preprocessing, excluded runs, failed cases, and hardware information here.
"""


def write_if_absent(path: Path, content: str, overwrite: bool = False) -> None:
    """Write content unless a planning file already exists.

    Existing planning files may contain project-specific edits; do not clobber
    them during skeleton regeneration unless --overwrite-planning is passed.
    """
    if path.exists() and not overwrite:
        return
    path.write_text(content, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("paper"), help="Output paper directory")
    ap.add_argument("--title", default="Title to Be Finalized")
    ap.add_argument("--target-journal", default="IEEE PES Transactions", help="Target IEEE PES Transactions journal")
    ap.add_argument("--contributions", type=Path, help="Markdown/text file with 2--3 confirmed contribution statements")
    ap.add_argument("--draft", action="store_true", help="Allow placeholder contributions for an early scaffold only")
    ap.add_argument("--overwrite-planning", action="store_true", help="Overwrite existing narrative, figure, and evidence planning files")
    args = ap.parse_args()

    contributions = require_contributions(args.contributions, draft=args.draft)
    out = args.out
    sections_dir = out / "sections"
    figures_dir = out / "figures"
    sections_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    (out / "main.tex").write_text(MAIN_TEX.replace("__TITLE__", latex_escape(args.title)), encoding="utf-8")
    (out / "macros.tex").write_text(MACROS, encoding="utf-8")
    for name, content in build_sections(contributions, args.draft).items():
        (sections_dir / name).write_text(content, encoding="utf-8")
    (out / "refs.bib").write_text(REFS, encoding="utf-8")
    (out / "reference_audit.md").write_text(REFERENCE_AUDIT, encoding="utf-8")
    write_if_absent(out / "narrative_logic_map.md", build_narrative_map(contributions, args.target_journal, args.title), args.overwrite_planning)
    write_if_absent(out / "section_logic_checklist.md", build_section_logic_checklist(contributions), args.overwrite_planning)
    write_if_absent(out / "contribution_map.md", contribution_map(contributions), args.overwrite_planning)
    write_if_absent(out / "figure_plan.md", figure_plan_stub(contributions), args.overwrite_planning)
    write_if_absent(figures_dir / "figure_structures.md", figure_structures_stub(contributions), args.overwrite_planning)
    write_if_absent(out / "claim_evidence_table.md", CLAIM_EVIDENCE, args.overwrite_planning)
    write_if_absent(out / "reproducibility_manifest.md", REPRO_MANIFEST, args.overwrite_planning)

    print(f"Wrote compile-safe IEEE skeleton to {out}")
    print(f"Target journal: {args.target_journal}")
    print(f"Confirmed contributions: {len(contributions)}")
    print("Next: complete narrative_logic_map.md, section_logic_checklist.md, claim_evidence_table.md, figure_plan.md, figures/figure_structures.md, refs.bib, and reference_audit.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
