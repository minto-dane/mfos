#!/usr/bin/env python3
"""Check high-level artifact directory layout hygiene."""

from __future__ import annotations

from pathlib import Path

from mfos_lint import Finding, ROOT, emit, mode_arg


REQUIRED_INDEXED_DIRS = [
    Path("reports"),
    Path("tests/catalog"),
    Path("tests/fixtures"),
    Path("tests/golden"),
    Path("evidence/traceability"),
]

CANONICAL_ROOT_FILES_ALLOWED = {
    Path("reports"): {"README.md", "index.yml"},
}


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    for directory in REQUIRED_INDEXED_DIRS:
        full = ROOT / directory
        if not full.exists():
            findings.append(Finding("ERROR", full, "required artifact directory missing"))
            continue
        for required in ("README.md", "index.yml"):
            path = full / required
            if not path.exists():
                findings.append(Finding("ERROR", path, "required artifact directory metadata missing"))

    for directory, allowed_names in CANONICAL_ROOT_FILES_ALLOWED.items():
        full = ROOT / directory
        if not full.exists():
            continue
        for child in full.iterdir():
            if child.is_file() and child.name not in allowed_names:
                findings.append(Finding("ERROR", child, "unexpected root-level report artifact"))

    for path in sorted((ROOT / "tests/catalog").glob("phase-0-*.yml")):
        findings.append(Finding("ERROR", path, "phase-specific catalog must be under tests/catalog/archive/<phase>/"))

    for path in sorted((ROOT / "evidence/traceability").glob("phase-0-*.yml")):
        findings.append(Finding("ERROR", path, "phase-specific traceability must be under archive/ or generated/<phase>/"))

    return emit(findings, args.mode, "Artifact layout check OK")


if __name__ == "__main__":
    raise SystemExit(main())
