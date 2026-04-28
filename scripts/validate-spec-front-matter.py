#!/usr/bin/env python3
"""Validate MFOS Phase 0.6 split-spec front matter."""

from __future__ import annotations

from mfos_lint import SOURCE_ID_RE, Finding, SPECS_DIR, emit, mode_arg, parse_front_matter, source_ids


REQUIRED = {
    "spec_id",
    "title",
    "canonical_language",
    "japanese_mirror",
    "status",
    "owner",
    "last_reviewed",
    "source_refs",
    "requirement_refs",
    "claim_refs",
    "test_refs",
    "evidence_refs",
    "implementation_allowed",
    "downstream_packs",
    "spec_gap_policy",
}


def markdown_table_cells(line: str) -> list[str]:
    """Split a Markdown table row while ignoring pipes inside inline code."""
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return []
    cells: list[str] = []
    current: list[str] = []
    in_code = False
    for char in stripped[1:-1]:
        if char == "`":
            in_code = not in_code
            current.append(char)
        elif char == "|" and not in_code:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    cells.append("".join(current).strip())
    return cells


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    known_sources = source_ids()
    findings: list[Finding] = []
    checked = 0

    for path in sorted(SPECS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        fm, error = parse_front_matter(path)
        if error:
            findings.append(Finding("ERROR", path, error))
            continue
        if fm is None:
            findings.append(Finding("ERROR", path, "missing Phase 0.6 front matter"))
            continue
        checked += 1
        missing = sorted(REQUIRED - set(fm))
        if missing:
            findings.append(Finding("ERROR", path, f"front matter missing fields: {', '.join(missing)}"))

        spec_id = fm.get("spec_id")
        if path.name == "INDEX.md":
            if spec_id != "MFOS-SPEC-INDEX":
                findings.append(Finding("ERROR", path, f"INDEX.md spec_id must be MFOS-SPEC-INDEX, got {spec_id}"))
        elif not (isinstance(spec_id, str) and spec_id.startswith("MFOS-SPEC-")):
            findings.append(Finding("ERROR", path, f"invalid spec_id: {spec_id}"))

        for field in ("source_refs", "requirement_refs", "claim_refs", "test_refs", "evidence_refs", "downstream_packs"):
            if field in fm and not isinstance(fm[field], list):
                findings.append(Finding("ERROR", path, f"{field} must be a list"))

        if fm.get("canonical_language") not in {"en", "en-US"}:
            findings.append(Finding("ERROR", path, f"canonical_language must be en or en-US, got {fm.get('canonical_language')}"))

        if fm.get("implementation_allowed") is not False:
            findings.append(Finding("ERROR", path, "draft specs must not allow implementation directly"))

        if fm.get("spec_gap_policy") != "implementation_must_not_infer_or_fill_gaps":
            findings.append(Finding("ERROR", path, "spec_gap_policy must block inferred implementation"))

        for source_id in fm.get("source_refs", []) if isinstance(fm.get("source_refs"), list) else []:
            if source_id not in known_sources:
                findings.append(Finding("ERROR", path, f"unknown source_ref in front matter: {source_id}"))

        body = text.split("---\n", 2)[2] if text.startswith("---\n") and len(text.split("---\n", 2)) == 3 else text
        body_sources = set(SOURCE_ID_RE.findall(body))
        fm_sources = set(fm.get("source_refs", [])) if isinstance(fm.get("source_refs"), list) else set()
        missing_body_sources = sorted(body_sources - fm_sources)
        if missing_body_sources:
            findings.append(
                Finding(
                    "ERROR",
                    path,
                    "body Source Matrix IDs missing from front matter: "
                    + ", ".join(missing_body_sources),
                )
            )

        in_table = False
        table_width = 0
        table_start = 0
        for lineno, line in enumerate(text.splitlines(), 1):
            cells = markdown_table_cells(line)
            if not cells:
                in_table = False
                table_width = 0
                table_start = 0
                continue
            if not in_table:
                in_table = True
                table_width = len(cells)
                table_start = lineno
            elif len(cells) != table_width:
                findings.append(
                    Finding(
                        "ERROR",
                        path,
                        f"Markdown table width mismatch: table starts at line {table_start} with {table_width} cells, line has {len(cells)} cells",
                        lineno,
                    )
                )

    return emit(findings, args.mode, f"Spec front matter validation OK: {checked} specs checked")


if __name__ == "__main__":
    raise SystemExit(main())
