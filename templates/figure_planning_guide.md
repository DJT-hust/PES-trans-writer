# Figure Planning Guide

A PES Transactions manuscript should plan figures before drafting the main text. The figures should be evidence-bearing, not decorative.

## Required outputs

1. `paper/figure_plan.md`: one table that maps each figure to section, contribution, data source, and key message.
2. `paper/figures/figure_structures.md`: one structure block per figure with layout, panels, axes, units, annotations, data source, generation command, and caption draft.

## Rules

- Every figure must support one of the confirmed 2--3 contributions.
- Do not plan a C3 figure if the manuscript has only two contributions.
- Do not put drawing instructions inside LaTeX section files.
- A figure may be a conceptual diagram only when its structure clarifies the method or system boundary.
- A result figure must have a matching claim in `claim_evidence_table.md`.
- A figure should have a reproducible generation command whenever it is data-driven.

## Common PES figure types

- System architecture or market interaction schematic.
- Method workflow or algorithm pipeline.
- Objective value, cost, profit, emission, violation, curtailment, or reserve comparison.
- Power-flow, congestion, frequency, or security-metric plot.
- Sensitivity analysis or ablation study.
- Runtime, convergence, optimality gap, or scalability figure.
