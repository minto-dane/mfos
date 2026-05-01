#!/usr/bin/env python3
"""Validate index path existence and report lifecycle section consistency."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg


REPORT_INDEX = ROOT / "reports/index.yml"
INDEXES = [
    REPORT_INDEX,
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


def walk_paths(value: Any) -> list[str]:
    refs: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"path", "wrapper", "target", "wrapper_target", "generated_by", "generator", "superseded_by", "machine_readable", "machine_readable_path", "contains"}:
                if isinstance(child, str):
                    refs.append(child)
                elif isinstance(child, list):
                    refs.extend(item for item in child if isinstance(item, str))
            else:
                refs.extend(walk_paths(child))
    elif isinstance(value, list):
        for child in value:
            refs.extend(walk_paths(child))
    return refs


def check_report_section(items: object, prefix: str, section: str, findings: list[Finding]) -> None:
    if not isinstance(items, list):
        findings.append(Finding("ERROR", REPORT_INDEX, f"reports/index.yml {section} section must be a list"))
        return
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            findings.append(Finding("ERROR", REPORT_INDEX, f"reports/index.yml {section} entry must include path"))
            continue
        path = item["path"]
        if not path.startswith(prefix):
            findings.append(Finding("ERROR", REPORT_INDEX, f"{section} entry has wrong lifecycle root: {path}"))


def collect_index_paths(value: Any) -> set[str]:
    paths: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "path" and isinstance(child, str):
                paths.add(child.rstrip("/"))
            else:
                paths |= collect_index_paths(child)
    elif isinstance(value, list):
        for child in value:
            paths |= collect_index_paths(child)
    return paths


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    for index in INDEXES:
        if not index.exists():
            findings.append(Finding("ERROR", index, "index file missing"))
            continue
        data = load_yaml(index)
        if not isinstance(data, dict):
            findings.append(Finding("ERROR", index, "index must be a mapping"))
            continue
        for ref in walk_paths(data):
            if ref.startswith("http://") or ref.startswith("https://"):
                continue
            if not (ROOT / ref).exists():
                findings.append(Finding("ERROR", index, f"references missing path: {ref}"))

    if REPORT_INDEX.exists():
        report_index = load_yaml(REPORT_INDEX)
        if isinstance(report_index, dict):
            check_report_section(report_index.get("current"), "reports/current/", "current", findings)
            check_report_section(report_index.get("generated_reports"), "reports/generated/", "generated_reports", findings)
            check_report_section(report_index.get("phase_reports"), "reports/phases/", "phase_reports", findings)
            check_report_section(report_index.get("archive"), "reports/archive/", "archive", findings)
            indexed = collect_index_paths(report_index)
            superseded_root = ROOT / "reports/archive/superseded"
            for path in sorted(superseded_root.rglob("*") if superseded_root.exists() else []):
                if path.is_file() and path.name != ".mfos-dir.yml":
                    rel = str(path.relative_to(ROOT))
                    if rel not in indexed:
                        findings.append(Finding("ERROR", REPORT_INDEX, f"superseded archive artifact is not indexed: {rel}"))

    return emit(findings, args.mode, "Index integrity check OK")


if __name__ == "__main__":
    raise SystemExit(main())
