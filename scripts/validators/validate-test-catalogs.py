#!/usr/bin/env python3
"""Validate Phase 0.9 test catalog YAML artifacts."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

import sys

from lib.mfos_phase09 import (
    REQ_RE,
    SOURCE_RE,
    TEST_RE,
    as_list,
    has_before_return,
    is_phase_one_or_later,
    load_yaml,
    phase09_catalog_paths,
    rel,
)


REQUIRED_ENTRY_FIELDS = {
    "test_id",
    "test_name",
    "test_type",
    "phase_to_implement",
    "target_pack",
    "target_specs",
    "target_requirements",
    "source_refs",
    "preconditions",
    "inputs",
    "expected",
    "oracle_ref",
    "fixture_ref",
    "golden_ref",
    "negative",
    "security_sensitive",
    "audit_obligation_required",
    "evidence_required",
    "status",
}
EXPECTED_FIELDS = {"decisions", "state_transitions", "audit_records", "failure_mode", "final_state"}
TEST_TYPES = {
    "conformance",
    "positive",
    "negative",
    "failure_mode",
    "invalid_transition",
    "parser",
    "fuzz_seed",
    "audit_evidence",
    "crash_recovery_model",
    "traceability",
    "red_team",
}


def main() -> int:
    errors: list[str] = []
    total = 0

    for path in phase09_catalog_paths():
        if not path.exists():
            errors.append(f"missing required Phase 0.9 catalog: {rel(path)}")
            continue
        data = load_yaml(path)
        if not isinstance(data, dict):
            errors.append(f"{rel(path)}: catalog must be a mapping")
            continue
        if data.get("phase") != "0.9":
            errors.append(f"{rel(path)}: phase must be '0.9'")
        if data.get("implementation_allowed") is not False:
            errors.append(f"{rel(path)}: implementation_allowed must be false")
        entries = data.get("entries")
        if not isinstance(entries, list) or not entries:
            errors.append(f"{rel(path)}: entries must be a non-empty list")
            continue
        for entry in entries:
            total += 1
            if not isinstance(entry, dict):
                errors.append(f"{rel(path)}: catalog entry must be a mapping")
                continue
            test_id = str(entry.get("test_id", "<missing>"))
            missing = sorted(REQUIRED_ENTRY_FIELDS - set(entry))
            if missing:
                errors.append(f"{rel(path)}:{test_id}: missing fields: {', '.join(missing)}")
            if not TEST_RE.match(test_id):
                errors.append(f"{rel(path)}:{test_id}: invalid test_id namespace")
            if entry.get("test_type") not in TEST_TYPES:
                errors.append(f"{rel(path)}:{test_id}: invalid test_type {entry.get('test_type')}")
            if not is_phase_one_or_later(entry.get("phase_to_implement")):
                errors.append(f"{rel(path)}:{test_id}: phase_to_implement must be Phase 1 or later")
            for req in as_list(entry.get("target_requirements")):
                if not isinstance(req, str) or not REQ_RE.match(req):
                    errors.append(f"{rel(path)}:{test_id}: invalid target requirement {req}")
            for source in as_list(entry.get("source_refs")):
                if not isinstance(source, str) or not SOURCE_RE.match(source):
                    errors.append(f"{rel(path)}:{test_id}: source_refs must use EXTREF-* IDs: {source}")
            expected = entry.get("expected")
            if not isinstance(expected, dict):
                errors.append(f"{rel(path)}:{test_id}: expected must be a mapping")
                continue
            missing_expected = sorted(EXPECTED_FIELDS - set(expected))
            if missing_expected:
                errors.append(f"{rel(path)}:{test_id}: expected missing fields: {', '.join(missing_expected)}")
            negative = entry.get("negative") is True or entry.get("test_type") in {"negative", "failure_mode", "invalid_transition"}
            if negative and not expected.get("failure_mode"):
                errors.append(f"{rel(path)}:{test_id}: negative/failure test requires expected.failure_mode")
            if entry.get("audit_obligation_required") is True:
                records = expected.get("audit_records")
                if not as_list(records):
                    errors.append(f"{rel(path)}:{test_id}: audit obligation requires expected.audit_records")
                joined = f"{test_id} {entry.get('test_name', '')}".upper()
                if ("DENY" in joined or "BEFORE-RETURN" in joined or "DENIED" in joined) and not has_before_return(records):
                    errors.append(f"{rel(path)}:{test_id}: deny-before-return test requires before_return: true")
            if entry.get("security_sensitive") is True and not negative and not as_list(expected.get("audit_records")):
                errors.append(f"{rel(path)}:{test_id}: security_sensitive positive test requires audit expectation")
            if not as_list(entry.get("evidence_required")):
                errors.append(f"{rel(path)}:{test_id}: evidence_required must be non-empty")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Phase 0.9 test catalog validation OK: {total} entries checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
