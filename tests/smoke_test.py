#!/usr/bin/env python3
"""Standard-library smoke tests for PES-trans-writer.

The tests avoid network access, do not require LaTeX, and avoid spawning
external processes so they remain stable in constrained Codex environments.
"""

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from _common import require_contributions  # noqa: E402
from build_figure_plan import build_plan, build_structures  # noqa: E402
from build_ieee_skeleton import (  # noqa: E402
    CLAIM_EVIDENCE,
    MACROS,
    MAIN_TEX,
    REFS,
    REFERENCE_AUDIT,
    REPRO_MANIFEST,
    build_sections,
    contribution_map,
    figure_plan_stub,
    figure_structures_stub,
)
from build_narrative_map import build_narrative_map, build_section_logic_checklist  # noqa: E402


def build_paper_direct(paper: Path, contributions: list[str], title: str = "Smoke Test") -> None:
    sections_dir = paper / "sections"
    figures_dir = paper / "figures"
    sections_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    (paper / "main.tex").write_text(MAIN_TEX.replace("__TITLE__", title), encoding="utf-8")
    (paper / "macros.tex").write_text(MACROS, encoding="utf-8")
    for name, content in build_sections(contributions, draft=False).items():
        (sections_dir / name).write_text(content, encoding="utf-8")
    (paper / "refs.bib").write_text(REFS, encoding="utf-8")
    (paper / "reference_audit.md").write_text(REFERENCE_AUDIT, encoding="utf-8")
    (paper / "narrative_logic_map.md").write_text(build_narrative_map(contributions, "IEEE PES Transactions", title), encoding="utf-8")
    (paper / "section_logic_checklist.md").write_text(build_section_logic_checklist(contributions), encoding="utf-8")
    (paper / "contribution_map.md").write_text(contribution_map(contributions), encoding="utf-8")
    (paper / "figure_plan.md").write_text(figure_plan_stub(contributions), encoding="utf-8")
    (figures_dir / "figure_structures.md").write_text(figure_structures_stub(contributions), encoding="utf-8")
    (paper / "claim_evidence_table.md").write_text(CLAIM_EVIDENCE, encoding="utf-8")
    (paper / "reproducibility_manifest.md").write_text(REPRO_MANIFEST, encoding="utf-8")


def main() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="pes_writer_test_"))
    try:
        contrib = tmp / "contrib.md"
        contrib.write_text(
            "C1: We formulate a network-constrained scheduling model that links electricity dispatch, storage operation, and carbon trading decisions.\n\n"
            "C2: We design a reproducible computational workflow that maps project data and optimization outputs to verified manuscript claims.\n",
            encoding="utf-8",
        )
        paper = tmp / "paper"

        try:
            require_contributions(None, draft=False)
        except SystemExit:
            pass
        else:
            raise AssertionError("Contribution gate did not fail without contributions.")

        contributions = require_contributions(contrib, draft=False)
        assert len(contributions) == 2

        narrative = build_narrative_map(contributions, "IEEE Transactions on Smart Grid", "Smoke Test")
        section_logic = build_section_logic_checklist(contributions)
        assert "Contribution-to-evidence chain" in narrative
        assert "system need" in narrative.lower()
        assert "technical bottleneck" in narrative.lower()
        assert "Numerical Results" in section_logic

        fig_plan = build_plan(contributions)
        fig_structures = build_structures(contributions)
        assert "C3" not in fig_plan
        assert "Figure Structures" in fig_structures

        build_paper_direct(paper, contributions)
        required = [
            "main.tex",
            "claim_evidence_table.md",
            "narrative_logic_map.md",
            "section_logic_checklist.md",
            "contribution_map.md",
            "figure_plan.md",
            "figures/figure_structures.md",
            "refs.bib",
            "reference_audit.md",
        ]
        for rel in required:
            assert (paper / rel).exists(), rel

        tex = "\n".join(p.read_text(encoding="utf-8") for p in paper.rglob("*.tex"))
        assert "`" not in tex
        assert "```" not in tex
        assert "figures/example.pdf" not in tex
        assert "\\cite{todo}" not in tex
        assert "C3" not in (paper / "figure_plan.md").read_text(encoding="utf-8")
        assert "One-sentence thesis" in (paper / "narrative_logic_map.md").read_text(encoding="utf-8")
        assert "system need -> technical bottleneck" in (ROOT / "README.md").read_text(encoding="utf-8")
        print("All smoke tests passed.")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
