# Pre-Submission Checklist

## Contributions and evidence

- [ ] The manuscript has exactly two or three confirmed contributions.
- [ ] `contribution_map.md` maps each contribution to method, equations/algorithms, figures/tables, and result paragraphs.
- [ ] `claim_evidence_table.md` contains every quantitative, novelty, comparison, and mechanism claim.
- [ ] No result number appears in the abstract, introduction, or results without a source file or experiment record.

## Narrative logic

- [ ] `narrative_logic_map.md` exists and is filled with project-specific content.
- [ ] `section_logic_checklist.md` exists and maps each section to the manuscript storyline.
- [ ] The manuscript follows: system need -> technical bottleneck -> grouped literature gap -> proposed mechanism -> contribution-specific validation -> practical implication.
- [ ] `validate_narrative_logic.py paper --strict` has been run before finalization.

## Figures

- [ ] `figure_plan.md` exists and each figure maps to a contribution.
- [ ] `figures/figure_structures.md` gives layout, panels, axes, units, data source, baselines, annotations, caption draft, and generation command.
- [ ] No figure refers to C3 if the manuscript has only two contributions.
- [ ] All active `\includegraphics` files exist.

## References

- [ ] All references are in `refs.bib`.
- [ ] No manual `thebibliography` block exists.
- [ ] No placeholder citation keys exist.
- [ ] Every cited key has a `reference_audit.md` block.
- [ ] Each cited paper has been checked on Google Scholar and a primary source or DOI/Crossref.
- [ ] No MDPI, warning-list, predatory, unverifiable, or low-recognition source is used.

## LaTeX and style

- [ ] The LaTeX source contains no Markdown backticks or fenced code blocks.
- [ ] The abstract has no citations, displayed equations, tables, or footnotes.
- [ ] The manuscript compiles in the target IEEEtran template.
- [ ] `latex_sanity_check.py` has been run.
- [ ] `validate_narrative_logic.py` has been run.
- [ ] `validate_bibtex.py` has been run.

## Reproducibility

- [ ] `reproducibility_manifest.md` records code version, data version, environment, solver, hardware, seeds, and experiment commands.
- [ ] All baselines and scenarios are defined.
- [ ] Solver settings and stopping criteria are reported.
