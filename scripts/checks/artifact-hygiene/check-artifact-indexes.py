#!/usr/bin/env python3
"""Validate artifact index structure and referenced paths."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from pathlib import Path
from typing import Any

from lib.mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg


INDEXES = [
    ROOT / "reports/index.yml",
    ROOT / "reports/current/fixedpoint/index.yml",
    ROOT / "scripts/index.yml",
    ROOT / "fuzz/targets/index.yml",
    ROOT / "tasks/index.yml",
    ROOT / "docs/design/tasks/index.yml",
    ROOT / "tests/catalog/index.yml",
    ROOT / "tests/fixtures/index.yml",
    ROOT / "tests/golden/index.yml",
    ROOT / "evidence/traceability/index.yml",
]


def walk_refs(value: Any) -> list[tuple[str, str]]:
    refs: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"path", "wrapper", "target", "wrapper_target", "generated_by", "generator", "superseded_by", "machine_readable", "machine_readable_path", "contains"}:
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
            if key in {"generated_by", "generator"} and not ref.startswith("scripts/"):
                findings.append(Finding("WARN", index, f"{key} should reference scripts/: {ref}"))
            if not path.exists():
                findings.append(Finding("ERROR", index, f"{key} references missing path: {ref}"))

    return emit(findings, args.mode, "Artifact index check OK")


if __name__ == "__main__":
    raise SystemExit(main())
