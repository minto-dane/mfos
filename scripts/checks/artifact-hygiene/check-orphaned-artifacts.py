#!/usr/bin/env python3
"""Detect current artifacts that are not represented in artifact indexes."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from pathlib import Path
from typing import Any

from lib.mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg


INDEX_PATHS = [
    ROOT / "reports/index.yml",
    ROOT / "scripts/index.yml",
    ROOT / "fuzz/targets/index.yml",
    ROOT / "tasks/index.yml",
    ROOT / "docs/design/tasks/index.yml",
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


def has_material(path: Path) -> bool:
    if path.is_file():
        return True
    return any(child.is_file() for child in path.rglob("*"))


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

    for path in sorted((ROOT / "reports/current").glob("*")):
        if path.name in {"README.md", "index.yml", ".mfos-dir.yml"}:
            continue
        if path.is_file() and not covered(path, indexed):
            findings.append(Finding("ERROR", path, "current report is not listed in reports/index.yml"))
        if path.is_dir() and not covered(path, indexed):
            findings.append(Finding("ERROR", path, "current report package is not listed in reports/index.yml"))

    for path in sorted((ROOT / "scripts").glob("*")):
        if path.name in {"README.md", "index.yml"}:
            continue
        if not covered(path, indexed):
            findings.append(Finding("ERROR", path, "current script artifact is not listed in scripts/index.yml"))

    for path in sorted((ROOT / "fuzz/targets").glob("*")):
        if path.name in {"README.md", "index.yml", "archive"}:
            continue
        if path.is_dir() and not has_material(path):
            continue
        if not covered(path, indexed):
            findings.append(Finding("ERROR", path, "current fuzz target artifact is not listed in fuzz/targets/index.yml"))

    for path in sorted((ROOT / "tasks").glob("*")):
        if path.name in {"README.md", "index.yml", "archive"}:
            continue
        if path.is_dir() and not has_material(path):
            continue
        if not covered(path, indexed):
            findings.append(Finding("ERROR", path, "current task artifact is not listed in tasks/index.yml"))

    for path in sorted((ROOT / "docs/design/tasks").glob("*")):
        if path.name in {"README.md", "index.yml", "archive"}:
            continue
        if not covered(path, indexed):
            findings.append(Finding("ERROR", path, "current design task artifact is not listed in docs/design/tasks/index.yml"))

    return emit(findings, args.mode, "Orphaned artifact check OK")


if __name__ == "__main__":
    raise SystemExit(main())
