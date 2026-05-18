# Narrative Logic Map

This file is a required manuscript-planning gate. Complete it before drafting prose for the abstract, introduction, methodology, case studies, numerical results, or conclusion.

## 1. One-sentence thesis

- Thesis: TODO

The thesis should connect the system need, the unresolved technical bottleneck, and the proposed mechanism in one sentence. Avoid a generic phrase such as "a novel framework is proposed."

## 2. System need

- Studied system or market: TODO
- Operational, economic, security, or sustainability need: TODO
- Why the need matters for IEEE PES readers: TODO

## 3. Technical bottleneck

- Bottleneck in current practice or modeling: TODO
- Why this bottleneck is nontrivial: TODO
- What happens if it is ignored: TODO

## 4. Prior-work logic and gap

Group the literature by technical route rather than listing papers one by one.

| Literature group | Representative verified citations | What they handle well | Remaining limitation relative to this paper |
|---|---|---|---|
| Group 1: TODO | TODO | TODO | TODO |
| Group 2: TODO | TODO | TODO | TODO |
| Group 3: TODO | TODO | TODO | TODO |

- Gap statement: TODO

## 5. Proposed mechanism

- Core technical idea: TODO
- Why the idea addresses the gap: TODO
- Main assumptions: TODO
- Boundary of the claim: TODO

## 6. Contribution-to-evidence chain

Every contribution must map to a method element, a figure or table, and at least one verification item.

| Contribution | Gap addressed | Method element | Key equation/algorithm | Figure/table | Verification experiment | Expected result paragraph |
|---|---|---|---|---|---|---|
| C1 | TODO | TODO | TODO | TODO | TODO | TODO |
| C2 | TODO | TODO | TODO | TODO | TODO | TODO |
| C3, if used | TODO | TODO | TODO | TODO | TODO | TODO |

## 7. Section-level storyline

| Section | Local purpose | Required opening move | Required closing move | Evidence dependency |
|---|---|---|---|---|
| Abstract | Compact argument | Problem and gap | Key verified implication | Contribution map; claim-evidence table |
| Introduction | Motivate and position the paper | System need | Contributions and organization | Verified references; narrative gap |
| Problem Formulation | Define the studied decision problem | System boundary and assumptions | Baseline limitation or transition to method | Code/model audit |
| Methodology | Explain how the gap is addressed | Core idea linked to C1 | Reproducible procedure linked to C2/C3 | Equations; algorithms; implementation notes |
| Case Studies | Make validation credible | Test system and data | Metrics and baselines | Data inventory; solver settings |
| Numerical Results | Prove contributions with evidence | Main observation | Mechanism and implication | Figures; tables; claim-evidence table |
| Conclusion | Close without new claims | What was solved | Verified implication and limitation | Final checked claims |

## 8. Result narrative plan

Each result subsection should follow: observation -> numerical evidence -> mechanism -> implication.

| Result subsection | Related contribution | Main observation | Numerical evidence source | Mechanism to explain | Practical implication |
|---|---|---|---|---|---|
| TODO | TODO | TODO | TODO | TODO | TODO |

## 9. Risk controls

- Claims that must not be made without further evidence: TODO
- References that still require verification: TODO
- Figures that still lack data or drawing specifications: TODO
- Assumptions that must be stated explicitly: TODO
