# PES-trans-writer

`PES-trans-writer` is a Codex-oriented skill for drafting IEEE PES Transactions-style LaTeX manuscripts from research code, project folders, and experimental data.

It is designed for evidence-based writing: Codex should inspect the project, extract the method and results, confirm 2--3 contributions, build a manuscript-level narrative logic map, plan figures, verify references, and only then draft IEEEtran-compatible LaTeX sections.

## Hard gates

1. **Confirmed contributions first.** Full manuscript drafting requires exactly two or three non-placeholder contributions.
2. **Narrative logic before prose.** The manuscript must include `narrative_logic_map.md` and `section_logic_checklist.md`. These files define the argument chain: system need -> technical bottleneck -> grouped literature gap -> proposed mechanism -> contribution-specific validation -> practical implication.
3. **Figure planning before body drafting.** The manuscript must include `figure_plan.md` and `figures/figure_structures.md`.
4. **Reference verification before citation insertion.** All citations must come from `refs.bib`; fake citation keys are not allowed.
5. **Claim-evidence tracking.** Quantitative and novelty claims must be recorded in `claim_evidence_table.md`.
6. **Compile-safe LaTeX.** Skeleton files should compile even before real figures or references are inserted.

## Recommended workflow

```bash
# 1. Inspect the project without modifying it.
python scripts/inspect_project.py /path/to/project --out work/project_inventory.json

# 2. Summarize tabular result files when available.
python scripts/summarize_results.py /path/to/project/results --out work/result_summary.md

# 3. Write and confirm two or three contributions.
cp templates/contribution_intake_form.md work/contributions.md
# Edit work/contributions.md manually or ask Codex to propose contributions for confirmation.

# 4. Generate the manuscript-level logic map.
python scripts/build_narrative_map.py --contributions work/contributions.md \
  --out paper/narrative_logic_map.md \
  --section-checklist-out paper/section_logic_checklist.md \
  --title "Your Manuscript Title" \
  --target-journal "IEEE Transactions on Smart Grid"

# 5. Generate a contribution-linked figure plan.
python scripts/build_figure_plan.py --contributions work/contributions.md \
  --out paper/figure_plan.md \
  --structures-out paper/figures/figure_structures.md

# 6. Build a compile-safe IEEEtran skeleton.
python scripts/build_ieee_skeleton.py --contributions work/contributions.md \
  --out paper \
  --title "Your Manuscript Title" \
  --target-journal "IEEE Transactions on Smart Grid"

# 7. Check the narrative gate and LaTeX/reference consistency.
python scripts/validate_narrative_logic.py paper
python scripts/latex_sanity_check.py paper/main.tex
python scripts/validate_bibtex.py paper/refs.bib --tex-root paper --audit paper/reference_audit.md
```

Use `--draft` only for early scaffolding. A draft scaffold is not submission-ready and should not be used to generate final manuscript prose.

## Narrative logic map

The key addition in this version is the mandatory `paper/narrative_logic_map.md`. Before writing prose, fill in:

- the one-sentence thesis;
- the system need;
- the technical bottleneck;
- grouped literature logic and gap;
- the proposed mechanism;
- contribution-to-evidence mapping;
- section-level storyline;
- result narrative plan.

The `paper/section_logic_checklist.md` file then keeps each section aligned with this storyline.

For final checks, run:

```bash
python scripts/validate_narrative_logic.py paper --strict
```

Strict mode is intended before finalization; it will fail while TODO placeholders remain.

## Reference verification

`validate_bibtex.py` performs mechanical checks only. It does not replace Google Scholar, IEEE Xplore, primary publisher pages, or human judgement on venue quality. Passing the script means the metadata is internally consistent enough for review; it does not certify that the reference is appropriate.

## Tests

```bash
make test
```

The tests use only the Python standard library and check strict contribution gating, narrative-map generation, skeleton generation, sanity checks, and reference-validation failure modes.
