# Abstract Style Patterns for IEEE PES Transactions

The abstract must be a single paragraph. Prefer 150--200 words unless the target journal template specifies otherwise. No citations, equations, displayed math, tables, or figure references.

## Five-sentence abstract pattern

1. **System problem**: State the practical system issue.
2. **Limitation**: State why existing methods are insufficient.
3. **Proposed method**: Name the model, algorithm, or framework.
4. **Mechanism**: Explain the technical mechanism without implementation clutter.
5. **Validation and implication**: Give the test system/data and key quantitative findings if available.

## Seven-sentence abstract pattern

Use this when the paper has both modeling and algorithmic contributions.

1. Context and consequence.
2. Existing modeling limitation.
3. Proposed model.
4. Proposed solution/reformulation.
5. Feasibility, tractability, or theoretical property.
6. Case-study setup.
7. Key findings and practical implication.

## Good abstract verbs

Use precise verbs:

- formulates, characterizes, embeds, derives, reformulates, approximates, coordinates, benchmarks, validates, quantifies, decomposes, aggregates, disaggregates, schedules, clears, dispatches.

Use cautiously:

- proposes, develops, investigates, demonstrates.

Avoid:

- revolutionizes, unlocks, empowers, provides a comprehensive analysis, significantly improves, shows superiority, paves the way.

## Evidence rules

When result values exist, write them into the abstract:

```latex
Case studies on [system/data] show that the proposed method reduces [metric] by [x]\% while maintaining [constraint/quality metric].
```

When result values are missing, insert a TODO instead of inventing numbers:

```latex
Case studies on [TEST SYSTEM] show that the proposed method reduces [METRIC] by [VALUE]\% compared with [BASELINE].
```
