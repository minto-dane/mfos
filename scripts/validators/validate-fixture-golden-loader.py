#!/usr/bin/env python3
"""Loader-only validation for Phase 0.9 fixture/golden/oracle artifacts.

This script intentionally does not execute fixtures, evaluate oracles, emit
PASS/FAIL for MFOS behavior, or implement the semantic-runner contract.
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_phase09 import FIXTURE_DIR, GOLDEN_DIR, load_yaml, rel, yaml_files


def canonical(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: canonical(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [canonical(item) for item in value]
    return value


def add_mismatch(errors: list[str], path: Path, field: str) -> None:
    errors.append(f"{rel(path)}: top-level {field} does not match embedded oracle shape")


def expected_golden_path(fixture: dict[str, Any]) -> str:
    value = fixture.get("expected_oracle")
    return value if isinstance(value, str) else ""


def first_input(fixture: dict[str, Any]) -> dict[str, Any]:
    inputs = fixture.get("inputs")
    if isinstance(inputs, list) and inputs and isinstance(inputs[0], dict):
        return inputs[0]
    return {}


def validate_pair(fixture_path: Path, fixture: dict[str, Any], golden: dict[str, Any], errors: list[str]) -> None:
    golden_path = GOLDEN_DIR.parent / expected_golden_path(fixture)
    oracle = golden.get("oracle")
    if not isinstance(oracle, dict):
        errors.append(f"{rel(golden_path)}: golden vector must embed an oracle mapping")
        return

    fixture_rel = rel(fixture_path)
    if golden.get("fixture_ref") != fixture_rel:
        errors.append(f"{rel(golden_path)}: fixture_ref must equal {fixture_rel}")
    if oracle.get("fixture_ref") != fixture_rel:
        errors.append(f"{rel(golden_path)}: oracle.fixture_ref must equal {fixture_rel}")

    normalized_input = golden.get("normalized_input")
    if not isinstance(normalized_input, dict):
        errors.append(f"{rel(golden_path)}: normalized_input must be a mapping")
    else:
        input0 = first_input(fixture)
        copied_fields = {
            "fixture_id": fixture.get("fixture_id"),
            "operation": input0.get("operation"),
            "deterministic_seed": input0.get("deterministic_seed"),
        }
        for key, expected in copied_fields.items():
            if normalized_input.get(key) != expected:
                errors.append(f"{rel(golden_path)}: normalized_input.{key} must copy fixture {key}")

    field_pairs = [
        ("expected_decisions", "expected_decisions"),
        ("expected_state_transitions", "expected_state_transitions"),
        ("expected_audit_sequence", "expected_audit_records"),
        ("expected_final_state", "expected_final_state"),
    ]
    for golden_field, oracle_field in field_pairs:
        if canonical(golden.get(golden_field)) != canonical(oracle.get(oracle_field)):
            add_mismatch(errors, golden_path, golden_field)

    expected_failure = oracle.get("expected_failure")
    oracle_error = expected_failure.get("error_code") if isinstance(expected_failure, dict) else None
    if golden.get("expected_failure_mode") != oracle_error:
        add_mismatch(errors, golden_path, "expected_failure_mode")

    expected_output = golden.get("expected_normalized_output")
    if isinstance(expected_output, dict) and expected_output.get("final_state") != golden.get("expected_final_state"):
        errors.append(f"{rel(golden_path)}: expected_normalized_output.final_state must match expected_final_state")

    if canonical(fixture.get("expected_evidence")) != canonical(oracle.get("evidence_required")):
        errors.append(f"{rel(golden_path)}: oracle.evidence_required must match fixture expected_evidence")


def main() -> int:
    errors: list[str] = []
    fixture_files = yaml_files(FIXTURE_DIR)
    golden_files = {rel(path): path for path in yaml_files(GOLDEN_DIR)}
    seen_golden: set[str] = set()

    if not fixture_files:
        errors.append(f"missing fixtures under {rel(FIXTURE_DIR)}")
    if not golden_files:
        errors.append(f"missing golden vectors under {rel(GOLDEN_DIR)}")

    for fixture_path in fixture_files:
        fixture = load_yaml(fixture_path)
        if not isinstance(fixture, dict):
            errors.append(f"{rel(fixture_path)}: fixture must be a mapping")
            continue
        golden_ref = expected_golden_path(fixture)
        if not golden_ref:
            errors.append(f"{rel(fixture_path)}: expected_oracle must name a golden vector path")
            continue
        golden_path = golden_files.get(golden_ref)
        if golden_path is None:
            errors.append(f"{rel(fixture_path)}: expected_oracle target is missing: {golden_ref}")
            continue
        seen_golden.add(golden_ref)
        golden = load_yaml(golden_path)
        if not isinstance(golden, dict):
            errors.append(f"{golden_ref}: golden vector must be a mapping")
            continue
        validate_pair(fixture_path, fixture, golden, errors)

    unreferenced = sorted(set(golden_files) - seen_golden)
    for golden_ref in unreferenced:
        errors.append(f"{golden_ref}: golden vector is not referenced by any fixture expected_oracle")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        "Phase 0.9 loader-only fixture/golden/oracle validation OK: "
        f"{len(fixture_files)} fixture-golden pairs checked; no semantic execution performed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
