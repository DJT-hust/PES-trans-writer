# IEEE PES Transactions Introduction Style Guide

This guide distills high-level writing and organization patterns from strong IEEE PES Transactions-style papers supplied by the user. It must be used as a style compass, not as a source of reusable sentences. Do not copy wording from the reference papers.

## Default Introduction architecture

Use a contribution-driven structure. Choose one of the following variants based on the target paper.

### Variant A: Compact problem-driven structure

Best for optimization, uncertainty, scheduling, market, or dispatch papers with a clear methodological gap.

1. **System-level context**: Explain why the resource, market mechanism, or operating constraint matters.
2. **Operational challenge**: State the concrete difficulty that blocks direct application, such as uncertainty, non-convexity, high dimensionality, coupled constraints, incomplete information, or computational burden.
3. **Method families in prior work**: Group the literature into two or three methodological streams. For each stream, explain what it handles and what it misses.
4. **Closely related works**: Compare with the most relevant works along dimensions that are aligned with the proposed contribution. A compact comparison table is encouraged when the distinction is not obvious.
5. **Proposed idea**: State the central modeling or algorithmic idea in one short paragraph before listing contributions.
6. **Contributions**: Use two or three bullets, each with a short technical title followed by concrete mechanism and verifiable effect.
7. **Paper organization**: One paragraph only. Avoid overexplaining section contents.

### Variant B: Background-Motivation / Literature Review / Contributions

Best for IEEE Transactions on Smart Grid or applied VPP/DER/market-operation papers.

Use explicit subsections under Introduction:

```latex
\section{Introduction}
\subsection{Background and Motivation}
\subsection{Literature Review}
\subsection{Contributions}
```

The first subsection should build from grid-level need to market/operational mechanism to the specific technical attribute considered by the paper. The literature review should be grouped by methodology or application scenario, not by a chronological list of authors. The contributions subsection should start from open questions and then list the paper's efforts.

### Variant C: Model-based vs data-driven tension

Best for papers combining optimization, machine learning, neural-network-constrained optimization, surrogate models, or learned constraints.

1. Start from the conventional modeling paradigm.
2. Explain why its assumptions are not reliable in the studied setting.
3. Discuss data-driven alternatives and their limitations, especially limited interpretability, lack of hard constraints, data inefficiency, extrapolation risk, or poor feasibility guarantees.
4. Position the proposed hybrid method as a way to retain optimization structure while learning the missing or hard-to-model relationship.
5. Make the contribution bullets explicitly distinguish: learning component, optimization embedding, and validation/benchmarking.

## Literature review rules

- Organize prior work by **method class**, **constraint type**, **market layer**, or **resource type**.
- After each group, include one limitation sentence that directly prepares the gap.
- Avoid a flat sequence of “Author A did X; Author B did Y; Author C did Z.”
- Use comparison tables only when they clarify dimensions such as uncertainty source, distribution reliance, dynamic constraints, network constraints, market mechanism, computation time, or validation data.
- Do not claim novelty solely because a combination is uncommon. State what is technically unresolved.

## Contribution bullet style

Strong bullets have three parts:

```text
Technical title: concrete method + mechanism + evidence/benefit.
```

Examples of acceptable title forms:

- Data-driven performance characterization
- Constraint-preserving aggregation model
- Solver-compatible reformulation
- Carbon-electricity co-optimization model
- Reproducible case-study validation

Avoid weak titles:

- Novel framework
- Comprehensive model
- Extensive simulations
- Superior performance

## Paper-organization paragraph

Keep it factual and compact:

```latex
The remainder of this paper is organized as follows. Section II introduces ... . Section III formulates ... . Section IV presents ... . Section V reports ... . Section VI concludes this paper.
```

Do not repeat contribution claims in the organization paragraph.

## Tone and cadence

Preferred tone:

- Formal but not ornate.
- Mechanism-first rather than adjective-first.
- Claims are tied to constraints, variables, algorithms, datasets, or numerical evidence.
- The writing can use short signposting sentences, but every paragraph should advance the argument.

Avoid:

- “With the rapid development of ...” unless tied to a concrete operational consequence.
- “This paper fills the gap” without naming the gap.
- “Excellent/superior/remarkable performance” unless accompanied by numbers.
- Marketing verbs such as revolutionize, empower, unlock, unleash, transform.

## Paragraph templates

### Context paragraph

```latex
[Resource/system trend] changes [operational property] in [system/market]. This creates [risk or requirement], because [mechanism]. As a result, [operator/aggregator/market participant] needs [decision/model] that accounts for [technical factors].
```

### Gap paragraph

```latex
Although existing studies have considered [factor A] and [factor B], they usually treat [missing coupling/constraint/information] separately. This simplification can [specific failure mode], especially when [condition]. Therefore, a model that jointly captures [key elements] is needed for [application].
```

### Proposed-method bridge

```latex
Motivated by these observations, this paper develops [method name] for [decision problem]. The key idea is to [central mechanism], so that [constraint/property] can be preserved while [computational or economic goal] is achieved.
```
