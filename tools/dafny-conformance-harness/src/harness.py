#!/usr/bin/env python3
"""Non-production Dafny conformance-support harness.

The harness compares declared fixture/golden/oracle shapes and optional model
output JSON. It does not implement MFOS semantic decisions.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[3]


def canonical(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): canonical(value[key]) for key in sorted(value, key=str)}
    if isinstance(value, list):
        return [canonical(item) for item in value]
    return value


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected mapping")
    return data


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def compare_fixture_golden(fixture: Path, golden: Path) -> dict[str, Any]:
    fixture_data = load_yaml(fixture)
    golden_data = load_yaml(golden)
    oracle = golden_data.get("oracle")
    errors: list[str] = []

    fixture_rel = fixture.relative_to(ROOT).as_posix()
    if golden_data.get("fixture_ref") != fixture_rel:
        errors.append("golden.fixture_ref does not match fixture path")
    if not isinstance(oracle, dict):
        errors.append("golden lacks embedded oracle mapping")
    elif oracle.get("fixture_ref") != fixture_rel:
        errors.append("oracle.fixture_ref does not match fixture path")

    expected_oracle = fixture_data.get("expected_oracle")
    if isinstance(expected_oracle, str) and expected_oracle != golden.relative_to(ROOT).as_posix():
        errors.append("fixture.expected_oracle does not point to golden path")

    return {
        "fixture": fixture_rel,
        "golden": golden.relative_to(ROOT).as_posix(),
        "comparison_status": "loadable" if not errors else "mismatch",
        "errors": errors,
        "semantic_execution_performed": False,
    }


def compare_model_output(golden: Path, model_output: Path) -> dict[str, Any]:
    golden_data = load_yaml(golden)
    output_data = load_json(model_output)
    expected = canonical(golden_data.get("expected_normalized_output", {}))
    actual = canonical(output_data.get("expected_normalized_output", output_data))
    return {
        "golden": golden.relative_to(ROOT).as_posix(),
        "model_output": model_output.as_posix(),
        "comparison_status": "match" if expected == actual else "mismatch",
        "semantic_execution_performed": False,
    }


def toolchain_status() -> dict[str, Any]:
    return {
        "dafny_binary": shutil.which("dafny"),
        "verification_status": "available" if shutil.which("dafny") else "blocked_by_missing_toolchain",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    pair = sub.add_parser("compare-fixture-golden")
    pair.add_argument("fixture", type=Path)
    pair.add_argument("golden", type=Path)

    model = sub.add_parser("compare-model-output")
    model.add_argument("golden", type=Path)
    model.add_argument("model_output", type=Path)

    sub.add_parser("toolchain-status")

    args = parser.parse_args()
    if args.command == "compare-fixture-golden":
        result = compare_fixture_golden(args.fixture, args.golden)
    elif args.command == "compare-model-output":
        result = compare_model_output(args.golden, args.model_output)
    else:
        result = toolchain_status()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("comparison_status") != "mismatch" else 1


if __name__ == "__main__":
    raise SystemExit(main())
