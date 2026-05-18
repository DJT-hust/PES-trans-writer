# Changelog

## 2026-05-17 -- Narrative logic gate repair

- Added a mandatory manuscript-level narrative gate.
- Added `templates/narrative_logic_map_template.md` and `templates/section_logic_guide.md`.
- Added `scripts/build_narrative_map.py` to create `paper/narrative_logic_map.md` and `paper/section_logic_checklist.md` from confirmed contributions.
- Added `scripts/validate_narrative_logic.py` to check narrative-planning files and optional strict TODO removal.
- Updated `SKILL.md` so final prose must follow: system need -> technical bottleneck -> grouped literature gap -> proposed mechanism -> contribution-specific validation -> practical implication.
- Updated `build_ieee_skeleton.py` to generate narrative-planning files and preserve existing planning files unless `--overwrite-planning` is used.
- Updated README, example workflow, and smoke tests.

## 2026-05-17 -- Repair release

- Made contribution-first behavior a script-level gate.
- Fixed compile-safety issues in generated LaTeX.
- Added claim-evidence and reproducibility ledgers.
- Clarified that reference checks are mechanical and must be paired with Google Scholar / primary-source verification.
- Improved BibTeX and project-inspection checks.
