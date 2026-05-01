#!/usr/bin/env python3
"""Detect high-risk flat directory pressure without forcing broad refactors."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, mode_arg


CURRENT_ROOT_ALLOWED = {
    ".mfos-dir.yml",
    "README.md",
    "index.yml",
    "repository-information-architecture-report.md",
    "repository-information-architecture-migration.yml",
    "repository-information-architecture-open-issues.md",
    "repository-information-architecture-red-team-review.md",
}

PRESSURE_BASELINES = {
    Path("scripts/checks"): 22,
    Path("scripts/validators"): 18,
}


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    current_root = ROOT / "reports/current"
    for path in sorted(current_root.iterdir() if current_root.exists() else []):
        if path.is_file() and path.name not in CURRENT_ROOT_ALLOWED:
            findings.append(Finding("ERROR", path, "flat reports/current root file must move into a stable domain package"))

    for rel, baseline in PRESSURE_BASELINES.items():
        root = ROOT / rel
        direct_files = [path for path in root.iterdir()] if root.exists() else []
        direct_file_count = sum(1 for path in direct_files if path.is_file())
        if direct_file_count > baseline:
            findings.append(Finding("WARN", root, f"direct file count {direct_file_count} exceeds baseline {baseline}; consider namespace sharding"))

    return emit(findings, args.mode, "Flat directory pressure check OK")


if __name__ == "__main__":
    raise SystemExit(main())
