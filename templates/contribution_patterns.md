# Contribution Patterns

Use contribution bullets only after the gap is clear. Each bullet should be independently verifiable from the manuscript.

## Preferred LaTeX forms

### Three technical bullets

```latex
The main contributions are summarized as follows:
\begin{itemize}
  \item \textit{[Technical title].} A [model/algorithm/reformulation] is developed to [capture/coordinate/embed] [technical feature]. This allows [decision maker] to [operational benefit] while preserving [constraint/property].
  \item \textit{[Technical title].} The proposed method [derives/transforms/decomposes] [hard component] into [solver-compatible form]. This reduces [computational burden/conservatism/manual tuning] without relaxing [critical requirement].
  \item \textit{[Validation title].} Case studies on [dataset/test system] quantify [metric]. Compared with [baseline], the proposed method [result], indicating [mechanism-level implication].
\end{itemize}
```

### Numbered contributions

Use this when the manuscript already uses a numbered style:

```latex
The main contributions of this paper are:
\begin{enumerate}
  \item ...
  \item ...
  \item ...
\end{enumerate}
```

## Contribution checks

For each bullet, verify that it answers:

- What is new in the model or algorithm?
- What specific limitation does it address?
- What constraints or physical/market mechanisms are preserved?
- Which experiment, theorem, or table supports it?

## Avoid unsupported novelty language

Do not use:

- To the best of our knowledge
- For the first time
- Novel and comprehensive

unless the user has provided a literature search that directly supports the claim.

Prefer:

- This paper differs from existing studies by ...
- The proposed formulation jointly captures ...
- The method is designed to retain ... while reducing ...
