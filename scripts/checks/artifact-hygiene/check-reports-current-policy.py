#!/usr/bin/env python3
"""Enforce the reports/current policy for stable cross-phase reports."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg


CURRENT_ROOT = ROOT / "reports/current"
REPORT_INDEX = ROOT / "reports/index.yml"
PHASE_NAME_RE = re.compile(r"(?:pre[-_]?phase[-_]?\d+|phase[-_]\d+(?:[-_]\d+)*)", re.IGNORECASE)


def collect_paths(value: Any) -> set[str]:
    paths: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "path" and isinstance(child, str):
                paths.add(child.rstrip("/"))
            else:
                paths |= collect_paths(child)
    elif isinstance(value, list):
        for child in value:
            paths |= collect_paths(child)
    return paths


def covered(path: Path, indexed: set[str]) -> bool:
    rel = str(path.relative_to(ROOT))
    return rel in indexed or any(rel.startswith(prefix + "/") for prefix in indexed)


def yaml_top(path: Path) -> dict[str, Any]:
    if path.suffix not in {".yml", ".yaml"}:
        return {}
    data = load_yaml(path)
    return data if isinstance(data, dict) else {}


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []
    indexed = collect_paths(load_yaml(REPORT_INDEX)) if REPORT_INDEX.exists() else set()

    for path in sorted(CURRENT_ROOT.rglob("*") if CURRENT_ROOT.exists() else []):
        if not path.is_file() or path.name in {"README.md", "index.yml", ".mfos-dir.yml"}:
            continue
        if PHASE_NAME_RE.search(path.name):
            findings.append(Finding("ERROR", path, "reports/current filename must not be phase-specific"))
        data = yaml_top(path)
        generated_by = data.get("generated_by") or data.get("generator")
        if data.get("status") == "generated" or (isinstance(generated_by, str) and generated_by.startswith("scripts/")):
            findings.append(Finding("ERROR", path, "generated report belongs under reports/generated, not reports/current"))
        if not covered(path, indexed):
            findings.append(Finding("ERROR", path, "reports/current artifact is not indexed in reports/index.yml"))

    return emit(findings, args.mode, "Reports/current policy check OK")


if __name__ == "__main__":
    raise SystemExit(main())
