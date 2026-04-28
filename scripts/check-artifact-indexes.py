#!/usr/bin/env python3
"""Validate artifact index structure and referenced paths."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg


INDEXES = [
    ROOT / "reports/index.yml",
    ROOT / "tests/catalog/index.yml",
    ROOT / "tests/fixtures/index.yml",
    ROOT / "tests/golden/index.yml",
    ROOT / "evidence/traceability/index.yml",
]


def walk_refs(value: Any) -> list[tuple[str, str]]:
    refs: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"path", "generated_by", "superseded_by"}:
                if isinstance(child, str):
                    refs.append((key, child))
                elif isinstance(child, list):
                    refs.extend((key, item) for item in child if isinstance(item, str))
            refs.extend(walk_refs(child))
    elif isinstance(value, list):
        for child in value:
            refs.extend(walk_refs(child))
    return refs


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    for index in INDEXES:
        if not index.exists():
            findings.append(Finding("ERROR", index, "artifact index missing"))
            continue
        data = load_yaml(index)
        if not isinstance(data, dict):
            findings.append(Finding("ERROR", index, "artifact index must be a mapping"))
            continue
        if "schema_version" not in data:
            findings.append(Finding("ERROR", index, "artifact index missing schema_version"))
        if not any(key in data for key in ("current", "sections", "generated", "archive")):
            findings.append(Finding("ERROR", index, "artifact index must declare current/sections/generated/archive"))
        for key, ref in walk_refs(data):
            path = ROOT / ref
            if key == "generated_by" and not ref.startswith("scripts/"):
                findings.append(Finding("WARN", index, f"generated_by should reference scripts/: {ref}"))
            if not path.exists():
                findings.append(Finding("ERROR", index, f"{key} references missing path: {ref}"))

    return emit(findings, args.mode, "Artifact index check OK")


if __name__ == "__main__":
    raise SystemExit(main())
