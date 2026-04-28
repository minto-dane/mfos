#!/usr/bin/env python3
"""Detect current artifacts that are not represented in artifact indexes."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg


INDEX_PATHS = [
    ROOT / "tests/catalog/index.yml",
    ROOT / "tests/fixtures/index.yml",
    ROOT / "tests/golden/index.yml",
    ROOT / "evidence/traceability/index.yml",
]


def collect_paths(value: Any) -> set[str]:
    out: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "path" and isinstance(child, str):
                out.add(child.rstrip("/"))
            else:
                out |= collect_paths(child)
    elif isinstance(value, list):
        for child in value:
            out |= collect_paths(child)
    return out


def indexed_paths() -> set[str]:
    paths: set[str] = set()
    for index in INDEX_PATHS:
        if index.exists():
            paths |= collect_paths(load_yaml(index))
    return paths


def covered(path: Path, indexed: set[str]) -> bool:
    rel = str(path.relative_to(ROOT))
    return rel in indexed or any(rel.startswith(prefix + "/") for prefix in indexed)


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []
    indexed = indexed_paths()

    for path in sorted((ROOT / "tests/catalog").glob("*.yml")):
        if path.name == "index.yml":
            continue
        if not covered(path, indexed):
            findings.append(Finding("ERROR", path, "current test catalog is not listed in tests/catalog/index.yml"))

    for root in (ROOT / "tests/fixtures", ROOT / "tests/golden"):
        for child in sorted(root.iterdir() if root.exists() else []):
            if child.name in {"README.md", "index.yml", "archive"}:
                continue
            if child.is_dir() and not covered(child, indexed):
                findings.append(Finding("ERROR", child, "current artifact directory is not listed in its index"))

    for path in sorted((ROOT / "evidence/traceability/current").glob("*.yml")):
        if not covered(path, indexed):
            findings.append(Finding("ERROR", path, "current traceability artifact is not listed in evidence/traceability/index.yml"))

    return emit(findings, args.mode, "Orphaned artifact check OK")


if __name__ == "__main__":
    raise SystemExit(main())
