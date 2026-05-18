#!/usr/bin/env python3
"""Summarize common experiment result files for IEEE-style manuscript drafting.

Supports CSV/Excel/JSON/TXT/LOG/OUT and basic MAT-file introspection when scipy is
installed. The output is Markdown so Codex can convert it into LaTeX tables and
result paragraphs.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

RESULT_EXTS = {".csv", ".xlsx", ".xls", ".json", ".mat", ".log", ".out", ".txt"}
IGNORE_DIRS = {".git", "__pycache__", ".ipynb_checkpoints", "node_modules", "venv", ".venv"}


def iter_result_files(root: Path, max_files: int = 300) -> List[Path]:
    files: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and not d.startswith(".")]
        for name in filenames:
            p = Path(dirpath) / name
            if p.suffix.lower() in RESULT_EXTS:
                files.append(p)
                if len(files) >= max_files:
                    return files
    return files


def summarize_dataframe(path: Path, df: pd.DataFrame) -> str:
    lines: List[str] = []
    lines.append(f"### `{path}`")
    lines.append("")
    lines.append(f"- Shape: `{df.shape[0]}` rows × `{df.shape[1]}` columns")
    lines.append(f"- Columns: {', '.join(map(str, df.columns[:30]))}")
    numeric = df.select_dtypes(include="number")
    if not numeric.empty:
        desc = numeric.describe().T[["count", "mean", "std", "min", "max"]]
        lines.append("")
        lines.append("Numeric summary:")
        lines.append("")
        lines.append(desc.to_markdown())
    lines.append("")
    lines.append("First rows:")
    lines.append("")
    lines.append(df.head(8).to_markdown(index=False))
    lines.append("")
    return "\n".join(lines)


def summarize_json(path: Path) -> str:
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return f"### `{path}`\n\n- JSON read error: {exc}\n"
    text = json.dumps(obj, ensure_ascii=False, indent=2)
    return f"### `{path}`\n\n```json\n{text[:5000]}\n```\n"


def summarize_text(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        return f"### `{path}`\n\n- Text read error: {exc}\n"
    lines = text.splitlines()
    tail = "\n".join(lines[-80:])
    return f"### `{path}`\n\n- Lines: {len(lines)}\n\nTail excerpt:\n\n```text\n{tail[:6000]}\n```\n"


def summarize_mat(path: Path) -> str:
    try:
        import scipy.io as sio  # type: ignore
        mat = sio.loadmat(path, squeeze_me=True, struct_as_record=False)
        keys = [k for k in mat.keys() if not k.startswith("__")]
        lines = [f"### `{path}`", "", f"- MAT variables: {', '.join(keys[:50])}"]
        for k in keys[:30]:
            v: Any = mat[k]
            shape = getattr(v, "shape", None)
            dtype = getattr(v, "dtype", None)
            lines.append(f"- `{k}`: shape={shape}, dtype={dtype}, type={type(v).__name__}")
        lines.append("")
        return "\n".join(lines)
    except Exception as exc:
        return f"### `{path}`\n\n- MAT introspection unavailable or failed: {exc}\n"


def summarize_file(path: Path, root: Path) -> str:
    rel = path.relative_to(root) if path.is_relative_to(root) else path
    ext = path.suffix.lower()
    try:
        if ext == ".csv":
            return summarize_dataframe(rel, pd.read_csv(path))
        if ext in {".xlsx", ".xls"}:
            return summarize_dataframe(rel, pd.read_excel(path))
        if ext == ".json":
            return summarize_json(rel)
        if ext == ".mat":
            return summarize_mat(path).replace(str(path), str(rel))
        return summarize_text(rel if isinstance(rel, Path) else Path(rel)) if False else summarize_text(path).replace(str(path), str(rel))
    except Exception as exc:
        return f"### `{rel}`\n\n- Summary failed: {exc}\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("results", type=Path, help="Results folder or file")
    ap.add_argument("--out", type=Path, default=Path("result_summary.md"))
    ap.add_argument("--max-files", type=int, default=100)
    args = ap.parse_args()

    root = args.results.resolve()
    if root.is_file():
        files = [root]
        base = root.parent
    else:
        files = iter_result_files(root, max_files=args.max_files)
        base = root

    chunks = ["# Experiment Result Summary", "", f"Scanned path: `{root}`", "", f"Files summarized: {len(files)}", ""]
    for file in files:
        chunks.append(summarize_file(file, base))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(chunks), encoding="utf-8")
    print(f"Wrote result summary to {args.out}")


if __name__ == "__main__":
    main()
