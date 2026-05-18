#!/usr/bin/env python3
"""Create a compact inventory of a research project for manuscript drafting.

The script avoids modifying the project. It scans filenames, extensions, likely
entry points, result files, dependency hints, and simple modeling keywords.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List

CODE_EXTS = {".m", ".mlx", ".py", ".ipynb", ".jl", ".gms", ".mod", ".r", ".R", ".cpp", ".c", ".h", ".hpp", ".java", ".sh", ".bat", ".ps1"}
DATA_EXTS = {".csv", ".xlsx", ".xls", ".mat", ".json", ".parquet", ".feather", ".h5", ".hdf5", ".dat"}
RESULT_EXTS = {".log", ".out", ".txt"}
IMAGE_EXTS = {".eps", ".png", ".jpg", ".jpeg", ".svg", ".tif", ".tiff"}
DOC_EXTS = {".tex", ".bib", ".md", ".docx", ".pdf"}

IGNORE_DIRS = {".git", ".svn", "__pycache__", ".ipynb_checkpoints", "node_modules", "venv", ".venv", "env", "dist", "build", "target", ".idea", ".vscode"}
ENTRY_PATTERNS = ["main", "run", "start", "experiment", "case", "simulate", "simulation", "train", "solve", "dispatch", "opf", "uc", "market", "carbon"]
DEPENDENCY_FILES = ["requirements.txt", "environment.yml", "pyproject.toml", "Pipfile", "Project.toml", "Manifest.toml", "package.json", "DESCRIPTION"]
MODELING_KEYWORDS = {
    "matpower": r"\b(loadcase|runopf|rundcopf|runpf|mpc\.)\b",
    "yalmip": r"\b(sdpvar|binvar|optimize\s*\(|sdpsettings)\b",
    "gurobi": r"\b(gurobi|Model\(|addVars|addConstr)\b",
    "pyomo": r"\b(pyomo|ConcreteModel|Var\(|Constraint\(|Objective\()\b",
    "cvx_cvxpy": r"\b(cvx_begin|cvxpy|cp\.Variable|cp\.Problem)\b",
    "pandas_results": r"\b(read_csv|to_csv|read_excel|to_excel)\b",
    "random_seed": r"\b(seed\s*\(|rng\s*\(|RandomState|default_rng)\b",
}


def sha1_head(path: Path, nbytes: int = 1024 * 1024) -> str:
    h = hashlib.sha1()
    try:
        with path.open("rb") as f:
            h.update(f.read(nbytes))
        return h.hexdigest()
    except OSError:
        return ""


def safe_rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace(os.sep, "/")
    except ValueError:
        return str(path)


def iter_files(root: Path, max_files: int) -> Iterable[Path]:
    count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and not d.startswith(".")]
        for name in filenames:
            if count >= max_files:
                return
            path = Path(dirpath) / name
            if path.is_file():
                count += 1
                yield path


def classify_file(path: Path) -> str:
    ext = path.suffix.lower()
    parent = "/".join(part.lower() for part in path.parts)
    stem = path.stem.lower()
    if ext in CODE_EXTS:
        return "code"
    if ext in IMAGE_EXTS or "figure" in parent or re.search(r"(^|[/_\-])fig(s|ure)?($|[/_\-])", parent):
        return "figure"
    if ext == ".pdf":
        return "figure" if ("figure" in parent or stem.startswith("fig")) else "document"
    if ext in DATA_EXTS or "data" in parent or "dataset" in parent:
        if "result" in parent or "output" in parent:
            return "result"
        return "data"
    if ext in RESULT_EXTS or "result" in parent or "output" in parent or "log" in parent:
        return "result"
    if ext in DOC_EXTS:
        return "document"
    return "other"


def is_likely_entry(path: Path) -> bool:
    stem = path.stem.lower()
    return path.suffix.lower() in CODE_EXTS and any(p in stem for p in ENTRY_PATTERNS)


def scan_keywords(path: Path) -> List[str]:
    try:
        size = path.stat().st_size
    except OSError:
        return []
    if path.suffix.lower() not in CODE_EXTS or size > 2_000_000:
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    hits = []
    for name, pat in MODELING_KEYWORDS.items():
        if re.search(pat, text, flags=re.I):
            hits.append(name)
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project", type=Path, help="Project folder to inspect")
    ap.add_argument("--out", type=Path, default=Path("project_inventory.json"))
    ap.add_argument("--max-files", type=int, default=5000)
    args = ap.parse_args()

    root = args.project.resolve()
    if not root.exists():
        raise SystemExit(f"Project path does not exist: {root}")

    files: List[Dict[str, object]] = []
    ext_counts: Counter[str] = Counter()
    class_counts: Counter[str] = Counter()
    by_class: defaultdict[str, List[str]] = defaultdict(list)
    entries: List[str] = []
    dependencies: List[str] = []
    keyword_hits: defaultdict[str, List[str]] = defaultdict(list)

    for path in iter_files(root, args.max_files):
        rel = safe_rel(path, root)
        ext = path.suffix.lower() or "[no_ext]"
        cls = classify_file(path)
        try:
            size = path.stat().st_size
            mtime = int(path.stat().st_mtime)
        except OSError:
            size = 0
            mtime = 0

        hits = scan_keywords(path)
        item: Dict[str, object] = {"path": rel, "extension": ext, "class": cls, "size_bytes": size, "mtime_unix": mtime}
        if size <= 25 * 1024 * 1024:
            item["sha1_head"] = sha1_head(path)
        if hits:
            item["modeling_keyword_hits"] = hits
            for h in hits:
                if len(keyword_hits[h]) < 50:
                    keyword_hits[h].append(rel)
        files.append(item)
        ext_counts[ext] += 1
        class_counts[cls] += 1
        if len(by_class[cls]) < 50:
            by_class[cls].append(rel)
        if is_likely_entry(path):
            entries.append(rel)
        if path.name in DEPENDENCY_FILES:
            dependencies.append(rel)

    inventory = {
        "project_root": str(root),
        "file_count_scanned": len(files),
        "extension_counts": dict(ext_counts.most_common()),
        "class_counts": dict(class_counts.most_common()),
        "samples_by_class": dict(by_class),
        "likely_entry_points": entries[:100],
        "dependency_files": dependencies,
        "modeling_keyword_hits": dict(keyword_hits),
        "files": files,
        "manuscript_hints": {
            "look_for_methods_in": [p for p in entries if Path(p).suffix.lower() in CODE_EXTS][:20],
            "look_for_results_in": by_class.get("result", [])[:20],
            "look_for_figures_in": by_class.get("figure", [])[:20],
            "look_for_data_in": by_class.get("data", [])[:20],
            "manual_pdf_review_needed": [p for p in by_class.get("document", []) if p.lower().endswith(".pdf")][:20],
        },
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(inventory, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote inventory to {args.out}")
    print(json.dumps(inventory["manuscript_hints"], indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
