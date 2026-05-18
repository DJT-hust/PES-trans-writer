# Reference Policy

References are a hard gate in `PES-trans-writer`.

## Storage rule

- All references must be stored in `paper/refs.bib`.
- The manuscript must use BibTeX citation keys from `refs.bib` only.
- Do not write a manual `thebibliography` block.
- Do not insert `\cite{todo}` or any other fake citation key. Use a LaTeX comment such as `% TODO citation: verified reference needed on DER aggregation` until the reference is verified.

## Verification rule

Every cited reference must be a real, traceable publication. Before inserting a citation into the TeX source, verify it using:

1. Google Scholar search results, and
2. a primary source such as IEEE Xplore, ACM, Springer, Elsevier, INFORMS, arXiv for preprints only when acceptable, official conference proceedings, or DOI/Crossref metadata.

The title, authors, venue, year, volume/issue/pages, and DOI must match the BibTeX entry as closely as possible.

## Preferred venues

Prefer high-recognition sources that are appropriate for the claim:

- IEEE Transactions series, especially PES-related journals.
- AI top venues such as NeurIPS, ICML, ICLR, AAAI, IJCAI, KDD, JMLR, and related top journals/conferences.
- Operations research, economics, and energy economics journals such as `Operations Research`, `Management Science`, `Manufacturing & Service Operations Management`, `Transportation Science`, `Energy Economics`, and `The Energy Journal`.

## Excluded or discouraged sources

Do not use MDPI, warning-list journals, predatory journals, unverifiable venues, low-recognition proceedings, or references that merely decorate a sentence without supporting a specific claim.

## Audit rule

For every cited key, create a block in `paper/reference_audit.md` headed exactly as:

```markdown
### `bibkey`
```

Fill in Google Scholar check, primary-source check, venue-quality reason, warning-list/MDPI check, and metadata consistency. The validation script is only a mechanical check and does not certify quality or truth.
