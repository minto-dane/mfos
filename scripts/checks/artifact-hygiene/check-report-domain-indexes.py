#!/usr/bin/env python3
"""Validate reports/current domain README and index coverage."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg


CURRENT_INDEX = ROOT / "reports/current/index.yml"


def list_paths(value: Any, key: str) -> list[str]:
    if not isinstance(value, dict):
        return []
    items = value.get(key)
    if not isinstance(items, list):
        return []
    return [
        str(item["path"]).rstrip("/")
        for item in items
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    ]


def collect_path_values(value: Any) -> set[str]:
    paths: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"path", "machine_readable"} and isinstance(child, str):
                paths.add(child.rstrip("/"))
            else:
                paths |= collect_path_values(child)
    elif isinstance(value, list):
        for child in value:
            paths |= collect_path_values(child)
    return paths


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []
    data = load_yaml(CURRENT_INDEX) if CURRENT_INDEX.exists() else {}

    for domain in list_paths(data, "domains"):
        domain_path = ROOT / domain
        index_path = domain_path / "index.yml"
        for required in ("README.md", "index.yml", ".mfos-dir.yml"):
            if not (domain_path / required).exists():
                findings.append(Finding("ERROR", domain_path / required, "reports/current domain package metadata missing"))
        if not index_path.exists():
            continue
        index_data = load_yaml(index_path)
        artifact_paths = collect_path_values(index_data)
        actual_paths = {
            str(path.relative_to(ROOT))
            for path in domain_path.iterdir()
            if path.is_file() and path.name not in {"README.md", "index.yml", ".mfos-dir.yml"}
        }
        for path in sorted(artifact_paths):
            if not path.startswith(f"{domain}/"):
                findings.append(Finding("ERROR", index_path, f"reports/current domain index must not reference outside its package: {path}"))
        for path in sorted(actual_paths - artifact_paths):
            findings.append(Finding("ERROR", ROOT / path, "reports/current domain artifact missing from local index.yml"))
        for path in sorted(artifact_paths - actual_paths):
            findings.append(Finding("ERROR", index_path, f"reports/current domain index references missing artifact: {path}"))

    for path in list_paths(data, "root_artifacts"):
        if not (ROOT / path).exists():
            findings.append(Finding("ERROR", CURRENT_INDEX, f"reports/current root artifact missing: {path}"))

    return emit(findings, args.mode, "Report domain index check OK")


if __name__ == "__main__":
    raise SystemExit(main())
