#!/usr/bin/env python3
"""Normalize MFOS fixture YAML into deterministic JSON.

The normalizer copies declared fixture fields into a stable shape. It does not
authorize, schedule, execute, resolve, or evaluate MFOS behavior.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


def canonical(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): canonical(value[key]) for key in sorted(value, key=str)}
    if isinstance(value, list):
        return [canonical(item) for item in value]
    return value


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: fixture must be a mapping")
    return data


def normalize_fixture(path: Path) -> dict[str, Any]:
    fixture = load_yaml(path)
    inputs = fixture.get("inputs")
    first_input = inputs[0] if isinstance(inputs, list) and inputs and isinstance(inputs[0], dict) else {}
    return canonical(
        {
            "fixture_path": path.as_posix(),
            "fixture_id": fixture.get("fixture_id"),
            "fixture_version": fixture.get("fixture_version"),
            "target_specs": fixture.get("target_specs", []),
            "target_requirements": fixture.get("target_requirements", []),
            "initial_state": fixture.get("initial_state", {}),
            "input_id": first_input.get("input_id"),
            "operation": first_input.get("operation"),
            "deterministic_seed": first_input.get("deterministic_seed"),
            "expected_oracle": fixture.get("expected_oracle"),
            "expected_evidence": fixture.get("expected_evidence", []),
            "not_allowed": fixture.get("not_allowed", []),
            "status": fixture.get("status"),
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    args = parser.parse_args()
    print(json.dumps(normalize_fixture(args.fixture), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
