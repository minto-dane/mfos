#!/usr/bin/env python3
"""Enforce domain-sharded reports/current structure."""

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
CURRENT_INDEX = CURRENT_ROOT / "index.yml"
PHASE_NAME_RE = re.compile(r"(?:pre[-_]?phase[-_]?\d+|phase[-_]\d+(?:[-_]\d+)*)", re.IGNORECASE)

ALLOWED_ROOT_FILES = {
    ".mfos-dir.yml",
    "README.md",
    "index.yml",
    "repository-information-architecture-report.md",
    "repository-information-architecture-migration.yml",
    "repository-information-architecture-open-issues.md",
    "repository-information-architecture-red-team-review.md",
}


def paths_from_index(data: Any, key: str) -> set[str]:
    if not isinstance(data, dict):
        return set()
    values = data.get(key)
    if not isinstance(values, list):
        return set()
    return {
        str(item["path"]).rstrip("/")
        for item in values
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    }


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    data = load_yaml(CURRENT_INDEX) if CURRENT_INDEX.exists() else {}
    domain_paths = paths_from_index(data, "domains")
    root_artifacts = paths_from_index(data, "root_artifacts")
    expected_root_artifacts = {
        f"reports/current/{name}" for name in ALLOWED_ROOT_FILES if name not in {".mfos-dir.yml", "README.md", "index.yml"}
    }
    if root_artifacts != expected_root_artifacts:
        findings.append(Finding("ERROR", CURRENT_INDEX, "root_artifacts must list only repository information architecture root reports"))

    for child in sorted(CURRENT_ROOT.iterdir() if CURRENT_ROOT.exists() else []):
        rel = str(child.relative_to(ROOT)).rstrip("/")
        if child.is_file():
            if child.name not in ALLOWED_ROOT_FILES:
                findings.append(Finding("ERROR", child, "reports/current root must not contain domain report files"))
            continue
        if not child.is_dir():
            continue
        if PHASE_NAME_RE.fullmatch(child.name):
            findings.append(Finding("ERROR", child, "reports/current domain directory must not be phase-specific"))
        if child.name in {"generated", "archive", "archives", "phases", "phase"}:
            findings.append(Finding("ERROR", child, "reports/current domain directory must not encode another lifecycle root"))
        if rel not in domain_paths:
            findings.append(Finding("ERROR", child, "reports/current domain directory is not listed in reports/current/index.yml"))

    for domain in sorted(domain_paths):
        path = ROOT / domain
        if not path.is_dir():
            findings.append(Finding("ERROR", CURRENT_INDEX, f"listed reports/current domain is missing: {domain}"))

    return emit(findings, args.mode, "Reports/current domain structure check OK")


if __name__ == "__main__":
    raise SystemExit(main())
