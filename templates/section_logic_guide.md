# Section Logic Guide

Use this guide when drafting or revising IEEE PES Transactions manuscripts with `PES-trans-writer`. The manuscript must follow a single contribution-driven narrative:

`system need -> technical bottleneck -> grouped literature gap -> proposed mechanism -> contribution-specific validation -> practical implication`.

## Abstract

Required flow:

1. Define the system problem in one concrete sentence.
2. State the unresolved gap or limitation.
3. Name the proposed model, algorithm, or mechanism.
4. Explain the key technical move, not only the application domain.
5. State the test system, data source, or case-study setting.
6. Report only verified numerical findings.
7. Close with the operational, market, security, or sustainability implication.

Do not use citations, equations, tables, footnotes, or unverifiable numbers.

## Introduction

Required flow:

1. Start from the system-level need, not from the method.
2. Narrow to the technical bottleneck addressed in this paper.
3. Review literature by method family or problem family.
4. Explain what each family still fails to cover.
5. State the exact gap within the scope of this paper.
6. Introduce the proposed mechanism in one paragraph.
7. List exactly two or three contributions.
8. End with paper organization.

Do not write a one-reference-one-sentence literature list. Do not claim "for the first time" unless the reference audit supports it.

## Problem Formulation

Required flow:

1. Define the system boundary, time scale, participants, and data inputs.
2. State assumptions before equations.
3. Define sets, parameters, variables, and units.
4. Present the baseline decision problem.
5. Explain why the baseline is insufficient for the stated gap.
6. Transition to the proposed method.

Do not introduce a method contribution before the reader understands the baseline problem.

## Methodology

Required flow:

1. Restate the core idea and connect it to a confirmed contribution.
2. Present the model, reformulation, algorithm, or data-driven module.
3. Explain approximations and tractability arguments.
4. Provide implementation details needed for reproducibility.
5. State how the method will be tested.

Every subsection should map to C1, C2, or C3 in `contribution_map.md`.

## Case Studies

Required flow:

1. State the test system, data, time resolution, and scenario horizon.
2. Specify baselines and why they are fair.
3. Specify metrics and units.
4. Report solver, hardware, package versions, and random seeds.
5. Explain scenario design.

Do not present results before the experimental setup is reproducible.

## Numerical Results

Required flow for each result paragraph:

1. Observation: what changes across methods, scenarios, or parameters.
2. Evidence: exact value, percentage, or visual pattern from a verified table or figure.
3. Mechanism: why the change occurs in power-system, market, optimization, or learning terms.
4. Implication: what the result means for operation, planning, market participation, or computational practice.

Avoid "Fig. X shows the effectiveness" as a standalone claim.

## Conclusion

Required flow:

1. Revisit the problem and gap.
2. Summarize the method without re-deriving it.
3. Report only the most important verified findings.
4. State limitations or deployment conditions when relevant.
5. Close with a practical implication.

Do not introduce new references, new experiments, or new claims.
