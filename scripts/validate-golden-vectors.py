#!/usr/bin/env python3
"""Validate Phase 0.9 golden vector YAML artifacts."""

from __future__ import annotations

import sys

from mfos_phase09 import GOLDEN_DIR, GOLDEN_RE, as_list, load_yaml, rel, yaml_files


REQUIRED = {
    "golden_id",
    "golden_version",
    "fixture_ref",
    "normalized_input",
    "expected_normalized_output",
    "expected_decisions",
    "expected_audit_sequence",
    "expected_state_transitions",
    "expected_final_state",
    "expected_failure_mode",
    "deterministic",
    "oracle",
    "status",
}


def main() -> int:
    errors: list[str] = []
    files = yaml_files(GOLDEN_DIR)
    if not files:
        errors.append(f"missing golden vectors under {rel(GOLDEN_DIR)}")
    for path in files:
        data = load_yaml(path)
        if not isinstance(data, dict):
            errors.append(f"{rel(path)}: golden vector must be a mapping")
            continue
        golden_id = str(data.get("golden_id", "<missing>"))
        missing = sorted(REQUIRED - set(data))
        if missing:
            errors.append(f"{rel(path)}:{golden_id}: missing fields: {', '.join(missing)}")
        if not GOLDEN_RE.match(golden_id):
            errors.append(f"{rel(path)}:{golden_id}: invalid golden_id namespace")
        if data.get("deterministic") is not True:
            errors.append(f"{rel(path)}:{golden_id}: deterministic must be true")
        if not isinstance(data.get("normalized_input"), dict):
            errors.append(f"{rel(path)}:{golden_id}: normalized_input must be a mapping")
        if not isinstance(data.get("expected_normalized_output"), dict):
            errors.append(f"{rel(path)}:{golden_id}: expected_normalized_output must be a mapping")
        if not as_list(data.get("expected_decisions")):
            errors.append(f"{rel(path)}:{golden_id}: expected_decisions must be non-empty")
        if not as_list(data.get("expected_state_transitions")):
            errors.append(f"{rel(path)}:{golden_id}: expected_state_transitions must be non-empty")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Phase 0.9 golden vector validation OK: {len(files)} vectors checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
