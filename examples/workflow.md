# Example Workflow

## 1. Inspect project

```bash
python scripts/inspect_project.py ../my_project --out work/project_inventory.json
```

## 2. Prepare contributions

Create `work/contributions.md`:

```markdown
C1: We formulate a network-constrained provincial carbon-electricity co-scheduling model that jointly represents thermal units, hydro, wind, PV, storage, bilateral electricity exchange, and carbon allowance trading.

C2: We develop a tractable implementation that preserves DC power-flow constraints and intertemporal storage/hydro constraints while maximizing provincial operating profit under coupled electricity and carbon prices.

C3: We validate the model through scenario studies that quantify how renewable penetration, carbon price, and interprovincial transfer limits reshape profit, emissions, and power exchanges.
```

## 3. Build narrative logic map

```bash
python scripts/build_narrative_map.py --contributions work/contributions.md \
  --out paper/narrative_logic_map.md \
  --section-checklist-out paper/section_logic_checklist.md \
  --title "Network-Constrained Provincial Carbon-Electricity Co-Scheduling" \
  --target-journal "IEEE Transactions on Smart Grid"
```

Before drafting prose, fill `paper/narrative_logic_map.md` with project-specific content. The manuscript should follow:

```text
system need -> technical bottleneck -> grouped literature gap -> proposed mechanism -> contribution-specific validation -> practical implication
```

## 4. Build plan and skeleton

```bash
python scripts/build_figure_plan.py --contributions work/contributions.md \
  --out paper/figure_plan.md \
  --structures-out paper/figures/figure_structures.md

python scripts/build_ieee_skeleton.py --contributions work/contributions.md \
  --out paper \
  --title "Network-Constrained Provincial Carbon-Electricity Co-Scheduling" \
  --target-journal "IEEE Transactions on Smart Grid"
```

## 5. Add references only after verification

Write BibTeX entries in `paper/refs.bib`, then fill `paper/reference_audit.md`.

```bash
python scripts/validate_bibtex.py paper/refs.bib --tex-root paper --audit paper/reference_audit.md
```

## 6. Check logic and LaTeX

```bash
python scripts/validate_narrative_logic.py paper
python scripts/latex_sanity_check.py paper/main.tex
```

Before final delivery, use strict mode:

```bash
python scripts/validate_narrative_logic.py paper --strict
```
