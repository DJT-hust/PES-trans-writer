---
name: PES-trans-writer
description: Draft IEEE PES Transactions-style LaTeX manuscripts from experimental code, project folders, and result data with contribution-first narrative logic, figure plans, reference audits, and low-AI-tone technical prose.
---

# PES-trans-writer

## Purpose

Use this skill in Codex to draft IEEE PES Transactions-style LaTeX manuscripts from experimental code, project folders, and result data. The output should be low-AI-tone, logically structured, technically precise, and terminology-preserving.

## Inputs

The user may provide:

- a project folder containing MATLAB, Python, Julia, GAMS, Pyomo, CVX/CVXPY, YALMIP, Gurobi, MATPOWER, or other experiment code;
- experimental data and result files such as `.mat`, `.csv`, `.xlsx`, `.json`, `.log`, figures, or tables;
- partial notes, model descriptions, equations, previous drafts, or reference PDFs;
- confirmed contributions, normally two or three items.

## Non-negotiable gates

### 1. Contributions first

Before drafting a full manuscript, obtain exactly two or three confirmed contribution statements. If the user has not provided them, inspect the project and propose 2--3 candidate contributions for confirmation. Do not proceed to final manuscript prose until the contributions are confirmed.

Use `templates/contribution_intake_form.md`. The scripts enforce this gate unless `--draft` is explicitly used.

### 2. Narrative logic map

Before writing any section prose, generate or update:

- `paper/narrative_logic_map.md`
- `paper/section_logic_checklist.md`

The narrative logic map is the manuscript-level argument. It must define the one-sentence thesis, system need, technical bottleneck, grouped literature gap, proposed mechanism, contribution-to-evidence chain, section-level storyline, and result narrative plan. Do not draft final prose until this map is project-specific. Use `templates/narrative_logic_map_template.md` and `templates/section_logic_guide.md`, or run `scripts/build_narrative_map.py`.

The manuscript must follow this single contribution-driven sequence: system need -> technical bottleneck -> grouped literature gap -> proposed mechanism -> contribution-specific validation -> practical implication.

### 3. Figure plan and figure structures

Before writing the manuscript body, generate or update:

- `paper/figure_plan.md`
- `paper/figures/figure_structures.md`

The figure plan must map each figure to a contribution, section, source data/code, purpose, and key message. The figure-structure file must separately specify layout, panels, axes, units, data source, baselines, annotations, caption draft, and generation command. Do not embed drawing instructions in LaTeX section text.

### 4. Verified references only

All references must be placed in `paper/refs.bib`. Do not use manual `thebibliography`. Do not insert fake citation keys such as `\cite{todo}`. Until a source is verified, use a LaTeX comment rather than a citation command.

Each cited source must be real and traceable through Google Scholar and a primary source or DOI/Crossref metadata. Prefer IEEE Transactions series, high-recognition AI venues, and recognized operations research, economics, or energy-economics journals. Do not use MDPI, warning-list, predatory, unverifiable, or low-quality sources.

Create an audit block for every cited key in `paper/reference_audit.md`.

### 5. Evidence ledger

Maintain `paper/claim_evidence_table.md`. Every quantitative result, novelty claim, comparison claim, and mechanism claim must be traceable to code, data, a figure/table, and a LaTeX location.

### 6. Compile-safe LaTeX

The generated skeleton must be valid LaTeX and should compile even when figures and references are not yet inserted. Avoid Markdown backticks and fenced code blocks inside `.tex` files. Do not include missing graphics in active figure environments.

## Writing style

Follow IEEE PES Transactions conventions:

- Use a direct technical tone.
- Build the full manuscript from `narrative_logic_map.md`: system need, technical bottleneck, grouped literature review, gap, proposed mechanism, contribution-specific validation, and practical implication.
- Avoid inflated phrases such as "cutting-edge", "comprehensive", "significantly improves" without numbers, or "superiority of the proposed method".
- Preserve standard power-system, market, optimization, and machine-learning terminology.
- State assumptions before equations.
- Explain numerical results through observation, evidence, mechanism, and implication.

## Recommended Codex workflow

1. Run `scripts/inspect_project.py` to inventory the project.
2. Run `scripts/summarize_results.py` on result folders when applicable.
3. Ask for or propose 2--3 contributions and wait for confirmation.
4. Run `scripts/build_narrative_map.py --contributions ...` and complete the narrative map.
5. Run `scripts/build_figure_plan.py --contributions ...`.
6. Run `scripts/build_ieee_skeleton.py --contributions ...`.
7. Draft each section only from the completed narrative map, verified project evidence, and confirmed contributions.
8. Add references only after verification and BibTeX audit.
9. Run `scripts/validate_narrative_logic.py`, `scripts/validate_bibtex.py`, and `scripts/latex_sanity_check.py`.
10. Update `claim_evidence_table.md` and `reproducibility_manifest.md` before finalizing.

## Section guidance

### Abstract

Use one paragraph of about 150--200 words. Follow the narrative map: problem, gap, method, test system/data, key verified result, and implication. Do not include citations, equations, tables, or unsupported numbers.

### Introduction

Use a limited reference structure inspired by strong IEEE PES articles: system need; technical bottleneck; literature review grouped by method; precise gap; proposed mechanism; 2--3 contributions; paper organization. Avoid one-reference-one-sentence listing.

### Methodology

Derive the model from the project code. Define sets, variables, parameters, objective, constraints, and solution procedure. When the code and manuscript notation differ, create a notation map instead of guessing.

### Case studies and numerical results

State data, test system, baselines, solvers, hardware, time resolution, and scenario settings. Each result paragraph should start with the observation, then provide numbers, mechanism, and implication.

### References

Use `refs.bib` only. Mechanical script checks are not sufficient; Google Scholar and primary-source checks remain mandatory.

## Failure behavior

If contributions, narrative logic, result evidence, reference verification, or project data are missing, stop and ask for the missing information or generate a clearly marked draft-only scaffold. Do not invent results, references, equations, baselines, or claims.
