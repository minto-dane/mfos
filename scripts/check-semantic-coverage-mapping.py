#!/usr/bin/env python3
"""Validate Phase 1.1 semantic coverage mappings are explicit and truthful."""

from __future__ import annotations

import filecmp
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent.parent
TRACEABILITY_DIR = ROOT / "evidence" / "traceability" / "generated" / "phase-1-1"
REPORTS_DIR = ROOT / "reports" / "generated" / "phase-1-1"
LEVEL_RANK = {
    "C0_NONE": 0,
    "C1_TYPE_ONLY": 1,
    "C2_PARTIAL_SEMANTIC": 2,
    "C3_FULL_SEMANTIC": 3,
    "C4_VERIFIED_PROPERTY": 4,
    "C5_CONFORMANCE_LINKED": 5,
    "C6_RELEASE_READY_MODEL": 6,
}
EXPECTED_FILES = [
    "requirement-to-dafny.yml",
    "test-to-dafny.yml",
    "fixture-to-dafny.yml",
    "oracle-to-dafny.yml",
    "formal-claim-to-dafny.yml",
]
EXPECTED_REPORTS = [
    "semantic-coverage.yml",
    "semantic-coverage-report.md",
    "negative-semantics-report.md",
    "semantic-coverage-open-issues.md",
    "semantic-coverage-red-team-review.md",
]


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return data


def compare_generated() -> list[str]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        tmp_trace = tmp_path / "traceability"
        tmp_reports = tmp_path / "reports"
        subprocess.run(
            [
                sys.executable,
                "scripts/generators/generate-semantic-coverage.py",
                "--traceability-dir",
                str(tmp_trace),
                "--reports-dir",
                str(tmp_reports),
            ],
            cwd=ROOT,
            check=True,
        )
        for name in EXPECTED_FILES:
            actual = TRACEABILITY_DIR / name
            expected = tmp_trace / name
            if not actual.exists():
                errors.append(f"missing generated traceability file: {actual}")
            elif not filecmp.cmp(actual, expected, shallow=False):
                errors.append(f"stale generated traceability file: {actual}")
        for name in EXPECTED_REPORTS:
            actual = REPORTS_DIR / name
            expected = tmp_reports / name
            if not actual.exists():
                errors.append(f"missing generated report file: {actual}")
            elif not filecmp.cmp(actual, expected, shallow=False):
                errors.append(f"stale generated report file: {actual}")
    return errors


def validate_test_mapping() -> list[str]:
    errors: list[str] = []
    data = load_yaml(TRACEABILITY_DIR / "test-to-dafny.yml")
    for test in data.get("tests", []):
        test_id = test.get("test_id", "<unknown>")
        level = test.get("coverage_level")
        mappings = test.get("coverage_mappings")
        if "dafny_symbols" in test:
            errors.append(f"{test_id}: legacy domain-wide dafny_symbols field is forbidden")
        if "negative_failure_condition" in test:
            errors.append(f"{test_id}: legacy negative_failure_condition fallback field is forbidden")
        if not isinstance(mappings, list) or not mappings:
            errors.append(f"{test_id}: coverage_mappings must be a non-empty list")
            continue
        if LEVEL_RANK.get(level, -1) >= LEVEL_RANK["C4_VERIFIED_PROPERTY"]:
            for mapping in mappings:
                if not mapping.get("dafny_symbol"):
                    errors.append(f"{test_id}: C4/C5 mapping lacks dafny_symbol")
                if not mapping.get("evidence_ref"):
                    errors.append(f"{test_id}: C4/C5 mapping lacks evidence_ref")
                if mapping.get("verification_status") != "verified":
                    errors.append(f"{test_id}: C4/C5 mapping is not verified")
                if LEVEL_RANK.get(mapping.get("coverage_level"), -1) < LEVEL_RANK["C4_VERIFIED_PROPERTY"]:
                    errors.append(f"{test_id}: C4/C5 entry includes lower-level mapping")
        if test.get("negative"):
            negative_symbols = test.get("negative_failure_conditions", [])
            if LEVEL_RANK.get(level, -1) >= LEVEL_RANK["C4_VERIFIED_PROPERTY"] and not negative_symbols:
                errors.append(f"{test_id}: verified negative test lacks negative_failure_conditions")
            if "UNSUPPORTED" in test_id and "INV_AUTH_UNSUPPORTED_NOT_SUCCESS" not in negative_symbols:
                errors.append(f"{test_id}: unsupported negative test must map to INV_AUTH_UNSUPPORTED_NOT_SUCCESS")
            if "SPEC-GAP" in test_id and "INV_AUTH_SPEC_GAP_NOT_SUCCESS" not in negative_symbols:
                errors.append(f"{test_id}: spec-gap negative test must map to INV_AUTH_SPEC_GAP_NOT_SUCCESS")
            if "MALFORMED-DSN" in test_id:
                joined = " ".join(str(symbol) for symbol in negative_symbols)
                if "STALE_HANDLE" in joined:
                    errors.append(f"{test_id}: malformed DSN must not map to stale-handle property")
    return errors


def main() -> int:
    errors = compare_generated() + validate_test_mapping()
    if errors:
        for error in errors:
            print(f"semantic coverage mapping error: {error}", file=sys.stderr)
        return 1
    print("Semantic coverage mapping check OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
