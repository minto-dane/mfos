#!/usr/bin/env python3
"""Validate Phase 0.9 oracle definitions embedded in golden vectors."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

import sys

from lib.mfos_phase09 import GOLDEN_DIR, ORACLE_RE, ROOT, as_list, load_yaml, rel, yaml_files


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
SCHEMA = ROOT / "schemas/oracle.schema.yml"


def main() -> int:
    errors: list[str] = []
    count = 0
    if SCHEMA.exists():
        schema = load_yaml(SCHEMA)
        schema_required = set(as_list(schema.get("required") if isinstance(schema, dict) else []))
        if schema_required and schema_required != REQUIRED:
            errors.append(f"{rel(SCHEMA)}: required fields do not match embedded oracle validator contract")
    else:
        errors.append(f"missing oracle schema: {rel(SCHEMA)}")
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
        normalized = data.get("normalized_input", {}) if isinstance(data, dict) else {}
        operation = str(normalized.get("operation", ""))
        expected_failure = oracle.get("expected_failure", {})
        failure_code = str(expected_failure.get("error_code", "")) if isinstance(expected_failure, dict) else ""
        decisions = as_list(oracle.get("expected_decisions"))
        decision_results = {
            str(decision.get("result"))
            for decision in decisions
            if isinstance(decision, dict) and decision.get("result") is not None
        }
        if "DENY-BEFORE-RETURN" in {operation, oracle_id} and "DENY" not in decision_results:
            errors.append(f"{rel(path)}:{oracle_id}: deny-before-return oracle must expect DENY")
        if failure_code in {"MFOS_ERR_SPEC_GAP", "MFOS_ERR_UNSUPPORTED"}:
            if expected_failure.get("fail_closed") is not True:
                errors.append(f"{rel(path)}:{oracle_id}: {failure_code} must be fail_closed")
            if str(oracle.get("expected_final_state")) in {"COMPLETE", "SUCCESS"}:
                errors.append(f"{rel(path)}:{oracle_id}: {failure_code} must not produce success final state")
            if "ALLOW" in decision_results:
                errors.append(f"{rel(path)}:{oracle_id}: {failure_code} must not pair with ALLOW")
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
