# Numerical Results Writing Style

Every results paragraph should do more than describe a figure. Use the following logic:

```text
Observation -> numerical evidence -> mechanism -> implication.
```

## Result paragraph template

```latex
Fig.~\ref{fig:...} compares [metric] under [cases]. The proposed method [main observation], with [number] compared with [baseline]. This reduction is mainly caused by [binding constraint/dispatch shift/price response/modeling mechanism]. Therefore, [operational implication].
```

## Robustness/sensitivity paragraph

```latex
Table~\ref{tab:...} reports the sensitivity of [metric] to [parameter]. As [parameter] increases, [metric] changes from [value] to [value]. The trend is consistent with [mechanism], because [technical explanation]. This also indicates that [method] is not tuned to a single operating point.
```

## Computation paragraph

```latex
The computational performance is summarized in Table~\ref{tab:runtime}. All cases are solved under the same hardware, solver, and optimality-gap settings. Compared with [baseline], [method] reduces the average solution time from [a] to [b], mainly because [decomposition/reformulation/sparsity/screening] reduces [variables/constraints/integer variables].
```

## Common issues to fix

- Do not write “Fig. X shows the effectiveness of the proposed method.” State what is effective and by how much.
- Do not mix economic, physical, and computational metrics without explaining trade-offs.
- Do not claim robustness from one scenario.
- Always define the baseline before comparing.
- Report units in tables and axes.
