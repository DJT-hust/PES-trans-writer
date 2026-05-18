#!/usr/bin/env python3
"""Mechanical reference gate for PES-trans-writer.

This script does not certify that a reference is real or high quality. It only
checks parseable metadata, citation-key consistency, excluded-venue patterns,
placeholder text, optional DOI/Crossref metadata, and audit-block presence.
Google Scholar and primary-source verification remain mandatory.
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

REQUIRED_BY_TYPE = {
    "article": ["author", "title", "year", "journal"],
    "inproceedings": ["author", "title", "year", "booktitle"],
    "conference": ["author", "title", "year", "booktitle"],
    "book": ["author", "title", "year", "publisher"],
    "techreport": ["author", "title", "year", "institution"],
}

FORBIDDEN_PATTERNS = [
    r"\bMDPI\b", r"\bMultidisciplinary Digital Publishing Institute\b",
    r"^\s*Energies\s*$", r"^\s*Sustainability\s*$", r"^\s*Applied Sciences\s*$",
    r"^\s*Processes\s*$", r"^\s*Mathematics\s*$", r"^\s*Sensors\s*$", r"^\s*Electronics\s*$",
]

PREFERRED_VENUE_PATTERNS = [
    r"IEEE Transactions on Power Systems", r"IEEE Transactions on Smart Grid",
    r"IEEE Transactions on Sustainable Energy", r"IEEE Transactions on Power Delivery",
    r"IEEE Transactions on Energy Conversion", r"IEEE Transactions on Industry Applications",
    r"IEEE Transactions on Industrial Informatics",
    r"IEEE Transactions on Neural Networks and Learning Systems",
    r"IEEE Transactions on Pattern Analysis and Machine Intelligence",
    r"Advances in Neural Information Processing Systems|NeurIPS",
    r"International Conference on Machine Learning|\bICML\b",
    r"International Conference on Learning Representations|\bICLR\b",
    r"AAAI", r"IJCAI", r"Knowledge Discovery and Data Mining|\bKDD\b",
    r"Journal of Machine Learning Research|\bJMLR\b",
    r"Operations Research", r"Management Science",
    r"Manufacturing & Service Operations Management", r"Production and Operations Management",
    r"Transportation Science", r"The Energy Journal", r"Energy Economics",
    r"Econometrica", r"American Economic Review", r"Journal of Economic Theory",
]

PLACEHOLDER_PATTERNS = [r"\bTODO\b", r"\bTBD\b", r"\bPLACEHOLDER\b", r"\bunknown\b", r"\?\?\?"]


def strip_outer(value: str) -> str:
    value = value.strip().rstrip(',').strip()
    while len(value) >= 2 and ((value[0] == '{' and value[-1] == '}') or (value[0] == '"' and value[-1] == '"')):
        value = value[1:-1].strip()
    return re.sub(r"\s+", " ", value)


def find_entry_end(text: str, open_idx: int, open_char: str) -> int:
    close_char = '}' if open_char == '{' else ')'
    depth = 1
    i = open_idx + 1
    in_quote = False
    escaped = False
    while i < len(text):
        ch = text[i]
        if ch == '"' and not escaped:
            in_quote = not in_quote
        if not in_quote:
            if ch == open_char:
                depth += 1
            elif ch == close_char:
                depth -= 1
                if depth == 0:
                    return i
        escaped = (ch == '\\' and not escaped)
        if ch != '\\':
            escaped = False
        i += 1
    return len(text) - 1


def parse_bibtex(text: str) -> Dict[str, Dict[str, str]]:
    entries: Dict[str, Dict[str, str]] = {}
    pos = 0
    while True:
        m = re.search(r"@([A-Za-z]+)\s*([\{\(])\s*([^,\s]+)\s*,", text[pos:])
        if not m:
            break
        entry_type = m.group(1).lower()
        open_char = m.group(2)
        key = m.group(3).strip()
        body_start = pos + m.end()
        body_end = find_entry_end(text, pos + m.start(2), open_char)
        body = text[body_start:body_end]
        fields: Dict[str, str] = {"ENTRYTYPE": entry_type, "ID": key}
        k = 0
        while k < len(body):
            fm = re.search(r"([A-Za-z][A-Za-z0-9_\-]*)\s*=\s*", body[k:])
            if not fm:
                break
            name = fm.group(1).lower()
            vstart = k + fm.end()
            if vstart >= len(body):
                break
            if body[vstart] in ['{', '"']:
                if body[vstart] == '{':
                    q = find_entry_end(body, vstart, '{') + 1
                else:
                    q = vstart + 1
                    escaped = False
                    while q < len(body):
                        if body[q] == '"' and not escaped:
                            q += 1
                            break
                        escaped = (body[q] == '\\' and not escaped)
                        if body[q] != '\\':
                            escaped = False
                        q += 1
                value = body[vstart:q]
                k = q
            else:
                q = vstart
                while q < len(body) and body[q] not in [',', '\n']:
                    q += 1
                value = body[vstart:q]
                k = q
            fields[name] = strip_outer(value)
        entries[key] = fields
        pos = body_end + 1
    return entries


def collect_tex(root: Path) -> str:
    if root.is_file():
        return root.read_text(encoding="utf-8", errors="replace")
    return "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in sorted(root.rglob("*.tex")))


def citation_keys(tex: str) -> List[str]:
    keys: List[str] = []
    cite_cmd = r"\\cite(?:t|p|alp|author|year|yearpar)?\s*(?:\[[^\]]*\]\s*)*\{([^}]+)\}"
    for m in re.finditer(cite_cmd, tex):
        for key in m.group(1).split(','):
            key = key.strip()
            if key:
                keys.append(key)
    return keys


def audit_keys(text: str) -> set[str]:
    return set(re.findall(r"^###\s+`([^`]+)`\s*$", text, flags=re.M))


def venue(entry: Dict[str, str]) -> str:
    return entry.get("journal") or entry.get("booktitle") or entry.get("publisher") or entry.get("institution") or ""


def normalize_title(s: str) -> str:
    s = re.sub(r"[{}\\]", "", s).lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def contains_any(patterns: Iterable[str], text: str) -> List[str]:
    return [pat for pat in patterns if re.search(pat, text or "", flags=re.I)]


def crossref_lookup(doi: str) -> Tuple[str, int] | None:
    encoded = urllib.parse.quote(doi.strip())
    url = f"https://api.crossref.org/works/{encoded}"
    req = urllib.request.Request(url, headers={"User-Agent": "PES-trans-writer/1.1 (reference-check)"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    msg = data.get("message", {})
    title_list = msg.get("title") or []
    title = title_list[0] if title_list else ""
    year = 0
    for key in ["published-print", "published-online", "issued"]:
        parts = msg.get(key, {}).get("date-parts")
        if parts and parts[0]:
            year = int(parts[0][0])
            break
    return title, year


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("bib", type=Path, help="Path to refs.bib")
    ap.add_argument("--tex-root", type=Path, help="Paper folder or main.tex for citation-key checks")
    ap.add_argument("--audit", type=Path, help="Path to reference_audit.md")
    ap.add_argument("--online", action="store_true", help="Try DOI/Crossref metadata checks")
    ap.add_argument("--strict-unused", action="store_true", help="Treat unused BibTeX entries as errors")
    args = ap.parse_args()

    errors: List[str] = []
    warnings: List[str] = []

    if not args.bib.exists():
        print(f"ERROR: BibTeX file not found: {args.bib}")
        return 2

    bib_text = args.bib.read_text(encoding="utf-8", errors="replace")
    entries = parse_bibtex(bib_text)
    if "\\begin{thebibliography}" in bib_text:
        errors.append("refs.bib appears to contain a LaTeX thebibliography block; use BibTeX entries only.")
    if not entries:
        warnings.append("No BibTeX entries found. This is acceptable only for an early compile-safe skeleton without citations.")

    for key, e in entries.items():
        et = e.get("ENTRYTYPE", "").lower()
        req = REQUIRED_BY_TYPE.get(et, ["author", "title", "year"])
        for f in req:
            if not e.get(f):
                errors.append(f"{key}: missing required field `{f}` for @{et}.")
        values = " ".join(v for k, v in e.items() if k not in {"ENTRYTYPE", "ID"})
        if contains_any(PLACEHOLDER_PATTERNS, values):
            errors.append(f"{key}: contains placeholder text.")
        v = venue(e)
        forbidden = contains_any(FORBIDDEN_PATTERNS, v) + contains_any(FORBIDDEN_PATTERNS, e.get("publisher", ""))
        if forbidden:
            errors.append(f"{key}: venue/publisher matches excluded pattern(s): {', '.join(sorted(set(forbidden)))}.")
        if not contains_any(PREFERRED_VENUE_PATTERNS, v):
            warnings.append(f"{key}: venue `{v or 'MISSING'}` is not in the preferred high-recognition venue patterns; manual quality check required.")
        if not e.get("doi"):
            warnings.append(f"{key}: DOI missing. Verify through Google Scholar and a primary source; add DOI when available.")
        if args.online and e.get("doi"):
            try:
                cr = crossref_lookup(e["doi"])
                if cr:
                    cr_title, cr_year = cr
                    if cr_title and normalize_title(cr_title) != normalize_title(e.get("title", "")):
                        warnings.append(f"{key}: Crossref title differs. BibTeX=`{e.get('title','')}` Crossref=`{cr_title}`")
                    if cr_year and e.get("year") and str(cr_year) != str(e.get("year")):
                        warnings.append(f"{key}: Crossref year {cr_year} differs from BibTeX year {e.get('year')}.")
            except Exception as ex:
                warnings.append(f"{key}: online DOI check failed: {ex}")

    cited: List[str] = []
    if args.tex_root:
        if not args.tex_root.exists():
            errors.append(f"TeX root not found: {args.tex_root}")
        else:
            tex = collect_tex(args.tex_root)
            if "\\begin{thebibliography}" in tex:
                errors.append("Manual thebibliography block found in TeX source; use refs.bib instead.")
            cited = citation_keys(tex)
            for key in cited:
                if contains_any(PLACEHOLDER_PATTERNS, key):
                    errors.append(f"Citation key `{key}` is a placeholder. Use a comment until the reference is verified.")
            for key in sorted(set(cited) - set(entries)):
                errors.append(f"Citation key `{key}` appears in TeX but is missing from refs.bib.")
            unused = sorted(set(entries) - set(cited))
            for key in unused[:30]:
                msg = f"BibTeX key `{key}` is not cited in TeX source."
                if args.strict_unused:
                    errors.append(msg)
                else:
                    warnings.append(msg)

    if args.audit:
        if not args.audit.exists():
            errors.append(f"Reference audit file not found: {args.audit}")
        else:
            audit_text = args.audit.read_text(encoding="utf-8", errors="replace")
            aks = audit_keys(audit_text)
            must_audit = set(cited) if cited else set(entries)
            for key in sorted(must_audit - aks):
                errors.append(f"Reference audit is missing a block headed exactly as ### `{key}`.")
            for key in sorted(aks - set(entries)):
                warnings.append(f"Reference audit contains `{key}`, but refs.bib has no matching entry.")
            for key in sorted(must_audit & aks):
                block = re.search(rf"^###\s+`{re.escape(key)}`\s*$([\s\S]*?)(?=^###\s+`|\Z)", audit_text, flags=re.M)
                if block:
                    text = block.group(1)
                    required_labels = ["Google Scholar check", "Primary source checked", "Venue quality reason", "Warning-list / MDPI check", "Metadata consistency"]
                    for label in required_labels:
                        m = re.search(rf"-\s*{re.escape(label)}\s*:\s*(.+)", text)
                        if not m or contains_any(PLACEHOLDER_PATTERNS, m.group(1)):
                            warnings.append(f"{key}: audit field `{label}` is missing or still a placeholder.")

    print("Reference validation summary")
    print(f"- BibTeX entries: {len(entries)}")
    print(f"- Cited keys: {len(set(cited)) if cited else 'not checked'}")
    print(f"- Errors: {len(errors)}")
    print(f"- Warnings: {len(warnings)}")
    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"- {e}")
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"- {w}")
    print("\nNote: Passing this script does not replace Google Scholar and primary-source verification.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
