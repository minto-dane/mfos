#!/usr/bin/env python3
"""Ensure generated report artifacts live under generated lifecycle roots."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg


REPORT_INDEX = ROOT / "reports/index.yml"
REPORT_CURRENT = ROOT / "reports/current"
REPORT_GENERATED = ROOT / "reports/generated"


def yaml_top(path: Path) -> dict[str, Any]:
    if path.suffix not in {".yml", ".yaml"}:
        return {}
    data = load_yaml(path)
    return data if isinstance(data, dict) else {}


def generated_report_entries(index: dict[str, Any]) -> dict[str, str]:
    entries: dict[str, str] = {}
    for item in index.get("generated_reports", []) if isinstance(index.get("generated_reports"), list) else []:
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            generator = item.get("generator") or item.get("generated_by")
            entries[item["path"].rstrip("/")] = str(generator or "")
    return entries


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []
    index = load_yaml(REPORT_INDEX) if REPORT_INDEX.exists() else {}
    index = index if isinstance(index, dict) else {}
    generated_entries = generated_report_entries(index)

    for path in sorted(REPORT_CURRENT.rglob("*") if REPORT_CURRENT.exists() else []):
        if not path.is_file():
            continue
        data = yaml_top(path)
        generated_by = data.get("generated_by") or data.get("generator")
        if data.get("status") == "generated" or (isinstance(generated_by, str) and generated_by.startswith("scripts/")):
            findings.append(Finding("ERROR", path, "generated report artifact must not be under reports/current"))

    for path in sorted(REPORT_GENERATED.rglob("*") if REPORT_GENERATED.exists() else []):
        if not path.is_file() or path.name in {"README.md", "index.yml", ".mfos-dir.yml"}:
            continue
        rel = str(path.relative_to(ROOT))
        generator = generated_entries.get(rel)
        data = yaml_top(path)
        artifact_generator = data.get("generated_by") or data.get("generator")
        if not generator and not (isinstance(artifact_generator, str) and artifact_generator.startswith("scripts/")):
            findings.append(Finding("ERROR", path, "generated report lacks generator metadata in artifact or reports/index.yml"))
        if generator and not generator.startswith("scripts/"):
            findings.append(Finding("ERROR", REPORT_INDEX, f"generated report generator must reference scripts/: {rel}"))

    return emit(findings, args.mode, "Generated artifact placement check OK")


if __name__ == "__main__":
    raise SystemExit(main())
