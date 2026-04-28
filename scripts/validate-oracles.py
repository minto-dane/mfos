#!/usr/bin/env python3
"""Validate Phase 0.9 oracle definitions embedded in golden vectors."""

from __future__ import annotations

import sys

from mfos_phase09 import GOLDEN_DIR, ORACLE_RE, as_list, load_yaml, rel, yaml_files


REQUIRED = {
    "oracle_id",
    "oracle_version",
    "fixture_ref",
    "expected_decisions",
    "expected_state_transitions",
    "expected_audit_records",
    "expected_failure",
    "expected_final_state",
    "evidence_required",
    "status",
}


def main() -> int:
    errors: list[str] = []
    count = 0
    for path in yaml_files(GOLDEN_DIR):
        data = load_yaml(path)
        oracle = data.get("oracle") if isinstance(data, dict) else None
        if not isinstance(oracle, dict):
            errors.append(f"{rel(path)}: golden vector must contain oracle mapping")
            continue
        count += 1
        oracle_id = str(oracle.get("oracle_id", "<missing>"))
        missing = sorted(REQUIRED - set(oracle))
        if missing:
            errors.append(f"{rel(path)}:{oracle_id}: oracle missing fields: {', '.join(missing)}")
        if not ORACLE_RE.match(oracle_id):
            errors.append(f"{rel(path)}:{oracle_id}: invalid oracle_id namespace")
        if not as_list(oracle.get("expected_decisions")):
            errors.append(f"{rel(path)}:{oracle_id}: expected_decisions must be non-empty")
        if oracle.get("requires_state_transitions", True) is not False and not as_list(oracle.get("expected_state_transitions")):
            errors.append(f"{rel(path)}:{oracle_id}: expected_state_transitions must be non-empty")
        for record in as_list(oracle.get("expected_audit_records")):
            if isinstance(record, dict) and record.get("decision") == "DENY" and record.get("before_return") is not True:
                errors.append(f"{rel(path)}:{oracle_id}: DENY audit record must set before_return: true")
        if not as_list(oracle.get("evidence_required")):
            errors.append(f"{rel(path)}:{oracle_id}: evidence_required must be non-empty")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Phase 0.9 oracle validation OK: {count} oracles checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
