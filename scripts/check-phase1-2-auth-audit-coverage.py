#!/usr/bin/env python3
"""Validate Phase 1.2 Authorization/Audit coverage artifacts."""

from __future__ import annotations

import filecmp
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent.parent
TRACEABILITY_DIR = ROOT / "evidence" / "traceability" / "generated" / "phase-1-2"
REPORTS_DIR = ROOT / "reports" / "current"
EVIDENCE_REGISTRY = ROOT / "docs/design/registries/evidence.yaml"
TRACE_FILES = [
    "authorization-to-dafny.yml",
    "audit-to-dafny.yml",
    "auth-audit-integration-to-dafny.yml",
    "test-to-dafny.yml",
    "requirement-to-dafny.yml",
    "formal-claim-to-dafny.yml",
]
REPORT_FILES = [
    "phase-1-2-entry-gate.yml",
    "phase-1-2-entry-gate.md",
    "dafny-authorization-audit-coverage.yml",
    "dafny-authorization-audit-coverage-report.md",
    "phase-1-2-gap-normalization.yml",
    "phase-1-2-gap-normalization.md",
    "dafny-authorization-audit-report.md",
    "dafny-authorization-audit-validation-report.md",
    "dafny-authorization-audit-red-team-review.md",
    "dafny-authorization-audit-open-issues.md",
]
SEMANTIC_LEVELS = {"C3_FULL_SEMANTIC", "C4_VERIFIED_PROPERTY", "C5_CONFORMANCE_LINKED", "C6_RELEASE_READY_MODEL"}
PROOF_LEVELS = {"C4_VERIFIED_PROPERTY", "C5_CONFORMANCE_LINKED", "C6_RELEASE_READY_MODEL"}
COVERAGE_LEVELS = [
    "C0_NONE",
    "C1_TYPE_ONLY",
    "C2_PARTIAL_SEMANTIC",
    "C3_FULL_SEMANTIC",
    "C4_VERIFIED_PROPERTY",
    "C5_CONFORMANCE_LINKED",
    "C6_RELEASE_READY_MODEL",
]
LEVEL_RANK = {level: rank for rank, level in enumerate(COVERAGE_LEVELS)}
DOMAIN_SUMMARY_KEYS = {
    "authorization": "authorization_coverage_level",
    "audit": "audit_coverage_level",
    "auth_audit_integration": "auth_audit_integration_coverage_level",
}
DOMAIN_TRACE_FILES = {
    "authorization": "authorization-to-dafny.yml",
    "audit": "audit-to-dafny.yml",
    "auth_audit_integration": "auth-audit-integration-to-dafny.yml",
}
AUDIT_UNAVAILABLE_TEST_ID = "NEG-MFOS-AUDIT-AUDIT-UNAVAILABLE-0906"
AUDIT_UNAVAILABLE_SYMBOL = "INV_AUDIT_DENY_TRANSITION_FAILS_CLOSED_WHEN_UNAVAILABLE"
AUDIT_ALLOW_WITH_AUDIT_UNAVAILABLE_SYMBOL = "INV_AUDIT_ALLOW_WITH_AUDIT_FAILS_CLOSED_WHEN_UNAVAILABLE"
AUDIT_UNAVAILABLE_ERROR = "MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE"
AUDIT_UNAVAILABLE_REQUIRED_REQS = {
    "MFOS-REQ-AUDIT-0001",
    "MFOS-REQ-AUDIT-0002",
    "MFOS-REQ-AUDIT-0005",
    "MFOS-REQ-AUDIT-0101",
}
PENDING_AUTH_TESTS = {
    "TEST-MFOS-AUTH-REQUIRE-MFA-0904": "REQUIRE_MFA",
    "TEST-MFOS-AUTH-REQUIRE-DUAL-CONTROL-0905": "REQUIRE_DUAL_CONTROL",
    "TEST-MFOS-AUTH-REQUIRE-BREAK-GLASS-0906": "REQUIRE_BREAK_GLASS",
    "TEST-MFOS-AUTH-REQUIRE-GUARD-APPROVAL-0907": "REQUIRE_GUARD_APPROVAL",
    "TEST-MFOS-AUTH-REQUIRE-OPERATOR-CONFIRMATION-0908": "REQUIRE_OPERATOR_CONFIRMATION",
}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return data


def row_name(row: dict[str, Any]) -> str:
    return str(row.get("test_id") or row.get("requirement_id") or row.get("claim_id") or "<unknown>")


def level_rank(level: Any) -> int:
    return LEVEL_RANK.get(str(level), -1)


def worst_level(rows: list[dict[str, Any]]) -> str:
    levels = [str(row.get("coverage_level")) for row in rows]
    return min(levels, key=level_rank) if levels else "C0_NONE"


def exact_dafny_symbol_declared(module_text: str, symbol: str, symbol_kind: str) -> bool:
    kind = re.escape(symbol_kind or "lemma")
    pattern = rf"^\s*(?:ghost\s+)?{kind}\s+{re.escape(symbol)}\s*(?:\(|<)"
    return re.search(pattern, module_text, flags=re.MULTILINE) is not None


def validate_c5_conformance_links(
    name: str,
    row: dict[str, Any],
    mapping: dict[str, Any],
    errors: list[str],
) -> None:
    row_id = row_name(row)
    refs = {key: row.get(key) for key in ("fixture_ref", "oracle_ref", "golden_ref")}
    if any(not ref for ref in refs.values()):
        return
    if refs["oracle_ref"] != refs["golden_ref"]:
        errors.append(f"{name}:{row_id}: C5 row must use the embedded oracle golden vector convention")
    fixture_path = ROOT / str(refs["fixture_ref"])
    golden_path = ROOT / str(refs["golden_ref"])
    if not fixture_path.exists() or not golden_path.exists():
        return
    fixture = load_yaml(fixture_path)
    golden = load_yaml(golden_path)
    oracle = golden.get("oracle")
    if not isinstance(oracle, dict):
        errors.append(f"{name}:{row_id}: golden_ref must embed an oracle mapping")
        return
    if fixture.get("expected_oracle") != refs["golden_ref"]:
        errors.append(f"{name}:{row_id}: fixture expected_oracle does not match golden_ref")
    if golden.get("fixture_ref") != refs["fixture_ref"]:
        errors.append(f"{name}:{row_id}: golden fixture_ref does not match fixture_ref")
    if oracle.get("fixture_ref") != refs["fixture_ref"]:
        errors.append(f"{name}:{row_id}: embedded oracle fixture_ref does not match fixture_ref")
    if golden.get("deterministic") is not True:
        errors.append(f"{name}:{row_id}: C5 golden vector must be deterministic")
    if fixture.get("expected_evidence") != oracle.get("evidence_required"):
        errors.append(f"{name}:{row_id}: fixture expected_evidence must match oracle evidence_required")
    evidence_ref = mapping.get("evidence_ref")
    if evidence_ref and evidence_ref not in (oracle.get("evidence_required") or []):
        errors.append(f"{name}:{row_id}: mapping evidence_ref is not required by the embedded oracle")
    mirror_pairs = [
        ("expected_decisions", "expected_decisions"),
        ("expected_state_transitions", "expected_state_transitions"),
        ("expected_audit_sequence", "expected_audit_records"),
        ("expected_final_state", "expected_final_state"),
    ]
    for golden_key, oracle_key in mirror_pairs:
        if golden.get(golden_key) != oracle.get(oracle_key):
            errors.append(f"{name}:{row_id}: golden {golden_key} does not mirror oracle {oracle_key}")
    expected_failure = oracle.get("expected_failure")
    if not isinstance(expected_failure, dict):
        errors.append(f"{name}:{row_id}: embedded oracle expected_failure must be a mapping")
    elif golden.get("expected_failure_mode") != expected_failure.get("error_code"):
        errors.append(f"{name}:{row_id}: golden expected_failure_mode does not mirror oracle expected_failure.error_code")


def validate_audit_unavailable_conformance(row: dict[str, Any], errors: list[str]) -> None:
    if row.get("coverage_level") != "C5_CONFORMANCE_LINKED":
        errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: audit-unavailable integration must be C5 after conformance closure")
        return
    requirement_refs = set(row.get("requirement_refs") or [])
    if not AUDIT_UNAVAILABLE_REQUIRED_REQS.issubset(requirement_refs):
        missing = sorted(AUDIT_UNAVAILABLE_REQUIRED_REQS - requirement_refs)
        errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: missing audit-unavailable requirement refs: {', '.join(missing)}")
    mappings = row.get("coverage_mappings")
    mapping = mappings[0] if isinstance(mappings, list) and mappings else {}
    if mapping.get("dafny_symbol") != AUDIT_UNAVAILABLE_SYMBOL:
        errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: must link exact Dafny symbol {AUDIT_UNAVAILABLE_SYMBOL}")
    refs = {key: row.get(key) for key in ("fixture_ref", "oracle_ref", "golden_ref")}
    if any(not ref for ref in refs.values()):
        errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: audit-unavailable C5 requires fixture/oracle/golden refs")
        return
    fixture_path = ROOT / str(refs["fixture_ref"])
    golden_path = ROOT / str(refs["golden_ref"])
    if not fixture_path.exists() or not golden_path.exists():
        return
    fixture = load_yaml(fixture_path)
    golden = load_yaml(golden_path)
    oracle = golden.get("oracle")
    if not isinstance(oracle, dict):
        errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: golden vector must embed oracle")
        return
    initial_state = fixture.get("initial_state")
    if not isinstance(initial_state, dict):
        errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: fixture requires initial_state")
        return
    decision = initial_state.get("authorization_decision")
    if not isinstance(decision, dict):
        errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: fixture requires initial authorization_decision")
    else:
        if decision.get("result") != "DENY":
            errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: fixture authorization_decision must be DENY")
        if "AUDIT_SECURITY_DECISION" not in (decision.get("obligations") or []):
            errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: fixture DENY decision must carry audit obligation")
    audit_service = initial_state.get("audit_service")
    if not isinstance(audit_service, dict) or audit_service.get("available") is not False:
        errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: fixture must model audit service unavailable")

    decision_results = {
        item.get("result")
        for item in (oracle.get("expected_decisions") or [])
        if isinstance(item, dict)
    }
    if "DENY" not in decision_results:
        errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: oracle must expect DENY")
    if decision_results & {"ALLOW", "ALLOW_WITH_AUDIT"}:
        errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: oracle must expect no success decision")
    expected_failure = oracle.get("expected_failure")
    if not isinstance(expected_failure, dict):
        errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: oracle expected_failure must be a mapping")
    else:
        if expected_failure.get("error_code") != AUDIT_UNAVAILABLE_ERROR:
            errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: oracle must expect {AUDIT_UNAVAILABLE_ERROR}")
        if expected_failure.get("fail_closed") is not True:
            errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: oracle must expect fail_closed: true")
    if oracle.get("expected_final_state") in {"COMPLETE", "SUCCESS"}:
        errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: oracle must not expect success final state")
    if oracle.get("expected_audit_records") not in ([], None):
        errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: oracle must not fabricate audit evidence when audit is unavailable")
    if golden.get("expected_audit_sequence") not in ([], None):
        errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: golden must not fabricate audit evidence when audit is unavailable")
    finalization = oracle.get("expected_finalization")
    if not isinstance(finalization, dict):
        errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: oracle requires expected_finalization")
    else:
        expected = {
            "audit_available": False,
            "final_result": "DENY",
            "final_error": AUDIT_UNAVAILABLE_ERROR,
            "result_released": False,
            "records_appended": 0,
        }
        for key, value in expected.items():
            if finalization.get(key) != value:
                errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: oracle expected_finalization.{key} must be {value!r}")
    release = oracle.get("expected_protected_resource_release")
    if not isinstance(release, dict):
        errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: oracle requires expected_protected_resource_release")
    else:
        if release.get("handle_created") is not False:
            errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: oracle must expect no dataset/protected-resource handle")
        if release.get("protected_resource_released") is not False:
            errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: oracle must expect no protected resource release")
    expected_output = golden.get("expected_normalized_output")
    if not isinstance(expected_output, dict):
        errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: golden requires expected_normalized_output")
    else:
        for key in ("result_released", "protected_resource_released", "audit_evidence_fabricated"):
            if expected_output.get(key) is not False:
                errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: golden expected_normalized_output.{key} must be false")
        if expected_output.get("final_error") != AUDIT_UNAVAILABLE_ERROR:
            errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: golden expected_normalized_output.final_error must be {AUDIT_UNAVAILABLE_ERROR}")
    if oracle.get("expected_no_silent_success") is not True:
        errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: oracle must assert expected_no_silent_success")
    if oracle.get("expected_no_audit_evidence_fabricated") is not True:
        errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: oracle must assert expected_no_audit_evidence_fabricated")

    audit_module = ROOT / "formal/executable-semantics/dafny/modules/audit.dfy"
    module_text = audit_module.read_text(encoding="utf-8") if audit_module.exists() else ""
    if not exact_dafny_symbol_declared(module_text, AUDIT_ALLOW_WITH_AUDIT_UNAVAILABLE_SYMBOL, "lemma"):
        errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: required-audit unavailable protected-effect lemma missing: {AUDIT_ALLOW_WITH_AUDIT_UNAVAILABLE_SYMBOL}")


def compare_generated() -> list[str]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        tmp_trace = tmp_path / "traceability"
        tmp_reports = tmp_path / "reports"
        subprocess.run(
            [
                sys.executable,
                "scripts/generators/generate-auth-audit-coverage.py",
                "--traceability-dir",
                str(tmp_trace),
                "--reports-dir",
                str(tmp_reports),
            ],
            cwd=ROOT,
            check=True,
        )
        for name in TRACE_FILES:
            actual = TRACEABILITY_DIR / name
            expected = tmp_trace / name
            if not actual.exists():
                errors.append(f"missing generated traceability file: {actual}")
            elif not filecmp.cmp(actual, expected, shallow=False):
                errors.append(f"stale generated traceability file: {actual}")
        for name in REPORT_FILES:
            actual = REPORTS_DIR / name
            expected = tmp_reports / name
            if not actual.exists():
                errors.append(f"missing generated report file: {actual}")
            elif not filecmp.cmp(actual, expected, shallow=False):
                errors.append(f"stale generated report file: {actual}")
    return errors


def validate_mapping_content() -> list[str]:
    errors: list[str] = []
    coverage = load_yaml(REPORTS_DIR / "dafny-authorization-audit-coverage.yml")
    gate = load_yaml(REPORTS_DIR / "phase-1-2-entry-gate.yml")
    evidence_registry = load_yaml(EVIDENCE_REGISTRY)
    known_evidence = {
        entry.get("evidence_id")
        for entry in evidence_registry.get("entries", [])
        if isinstance(entry, dict)
    }
    if coverage.get("authorization_audit_exit_blockers_remaining"):
        errors.append("Phase 1.2 coverage still reports Authorization/Audit exit blockers")
    if gate.get("merge_blockers") or gate.get("authorization_audit_merge_blockers_remaining"):
        errors.append("Phase 1.2 entry gate still reports merge blockers")
    if gate.get("phase_1_2_merge_allowed") is not True:
        errors.append("Phase 1.2 entry gate must report phase_1_2_merge_allowed true after closure")
    if coverage.get("formal_claims_proof_backed"):
        errors.append("Phase 1.2 coverage must not claim proof-backed formal claims")
    if coverage.get("python_loader_contains_semantics"):
        errors.append("Python loader/harness semantics flag must remain false")

    auth_catalog = load_yaml(ROOT / "tests/catalog/authorization.yml")
    catalog_entries = {
        entry.get("test_id"): entry
        for entry in auth_catalog.get("entries", [])
        if isinstance(entry, dict)
    }
    for test_id, expected_result in PENDING_AUTH_TESTS.items():
        entry = catalog_entries.get(test_id)
        if not isinstance(entry, dict):
            errors.append(f"{test_id}: missing authorization catalog entry")
            continue
        expected = entry.get("expected") if isinstance(entry.get("expected"), dict) else {}
        decisions = expected.get("decisions") if isinstance(expected.get("decisions"), list) else []
        results = {item.get("result") for item in decisions if isinstance(item, dict)}
        if expected_result not in results or results & {"ALLOW", "ALLOW_WITH_AUDIT"}:
            errors.append(f"{test_id}: pending authorization catalog must use {expected_result} and no success result")
        if expected.get("final_state") != "PENDING":
            errors.append(f"{test_id}: pending authorization catalog final_state must be PENDING")
        if expected.get("audit_records") not in ([], None):
            errors.append(f"{test_id}: pending authorization catalog must not fabricate audit records")
        golden_path = ROOT / str(entry.get("golden_ref", ""))
        if not golden_path.exists():
            errors.append(f"{test_id}: pending authorization golden missing: {golden_path}")
            continue
        golden = load_yaml(golden_path)
        golden_results = {
            item.get("result")
            for item in (golden.get("expected_decisions") or [])
            if isinstance(item, dict)
        }
        if expected_result not in golden_results or golden_results & {"ALLOW", "ALLOW_WITH_AUDIT"}:
            errors.append(f"{test_id}: pending authorization golden must use {expected_result} and no success result")
        if golden.get("expected_final_state") != "PENDING":
            errors.append(f"{test_id}: pending authorization golden final state must be PENDING")
        if golden.get("expected_audit_sequence") not in ([], None):
            errors.append(f"{test_id}: pending authorization golden must not fabricate audit records")

    minimum_fields_golden = load_yaml(ROOT / "tests/golden/audit/minimum-fields-0902.yml")
    minimum_records = minimum_fields_golden.get("expected_audit_sequence") or []
    if not any(isinstance(record, dict) and record.get("timestamp_present") is True for record in minimum_records):
        errors.append("TEST-MFOS-AUDIT-MINIMUM-FIELDS-0902: golden must include timestamp evidence")

    domain_rows: dict[str, list[dict[str, Any]]] = {}
    for domain, file_name in DOMAIN_TRACE_FILES.items():
        data = load_yaml(TRACEABILITY_DIR / file_name)
        rows = data.get("entries")
        if not isinstance(rows, list):
            errors.append(f"{file_name}: entries must be a list")
            rows = []
        domain_rows[domain] = rows
        aggregate = worst_level(rows)
        summary_level = coverage.get(DOMAIN_SUMMARY_KEYS[domain])
        if level_rank(summary_level) > level_rank(aggregate):
            below = [
                f"{row_name(row)}={row.get('coverage_level')}"
                for row in rows
                if level_rank(row.get("coverage_level")) < level_rank(summary_level)
            ]
            errors.append(
                f"{DOMAIN_SUMMARY_KEYS[domain]} overclaims child rows: "
                f"{summary_level} > {aggregate}; below rows: {', '.join(below)}"
            )
        if domain == "auth_audit_integration" and summary_level == "C5_CONFORMANCE_LINKED":
            below_c5 = [
                f"{row_name(row)}={row.get('coverage_level')}"
                for row in rows
                if row.get("coverage_level") != "C5_CONFORMANCE_LINKED"
            ]
            if below_c5:
                errors.append(
                    "auth_audit_integration_coverage_level is C5 while required child rows are below C5: "
                    + ", ".join(below_c5)
                )

    gap = load_yaml(REPORTS_DIR / "phase-1-2-gap-normalization.yml")
    if gap.get("exit_blockers_remaining"):
        errors.append("gap normalization still reports exit blockers")
    for entry in gap.get("entries", []):
        if entry.get("current_pr_merge_blocker") or entry.get("phase_1_2_exit_blocker"):
            errors.append(f"{entry.get('gap_id')}: Phase 1.2 merge/exit blocker remains")
        if entry.get("previous_classification") == "fix_before_next_merge" and not (
            entry.get("normalized_disposition") or entry.get("accepted_deferred")
        ):
            errors.append(f"{entry.get('gap_id')}: ambiguous fix_before_next_merge was not normalized")

    for name in ("authorization-to-dafny.yml", "audit-to-dafny.yml", "auth-audit-integration-to-dafny.yml", "test-to-dafny.yml", "requirement-to-dafny.yml"):
        data = load_yaml(TRACEABILITY_DIR / name)
        rows = data.get("entries") or data.get("tests") or data.get("requirements") or []
        for row in rows:
            row_id = row_name(row)
            row_level = row.get("coverage_level")
            if row.get("coverage_level") in SEMANTIC_LEVELS:
                mappings = row.get("coverage_mappings", [])
                if not mappings:
                    errors.append(f"{name}:{row_id}: semantic row lacks mappings")
                for mapping in mappings:
                    if not mapping.get("dafny_symbol"):
                        errors.append(f"{name}:{row_id}: semantic mapping lacks dafny_symbol")
                    if row.get("coverage_level") in PROOF_LEVELS and mapping.get("verification_status") != "verified":
                        errors.append(f"{name}:{row_id}: C4/C5 mapping not verified")
                    if not mapping.get("evidence_ref"):
                        errors.append(f"{name}:{row_id}: semantic mapping lacks evidence_ref")
                    elif mapping.get("evidence_ref") not in known_evidence:
                        errors.append(f"{name}:{row_id}: semantic mapping evidence_ref is not registered: {mapping.get('evidence_ref')}")
                    if level_rank(mapping.get("coverage_level")) < level_rank(row_level):
                        errors.append(f"{name}:{row_id}: mapping coverage level is below row coverage level")
                    module_path = ROOT / str(mapping.get("dafny_module", ""))
                    if not module_path.exists():
                        errors.append(f"{name}:{row_id}: Dafny module does not exist: {module_path}")
                    elif mapping.get("dafny_symbol"):
                        module_text = module_path.read_text(encoding="utf-8")
                        if not exact_dafny_symbol_declared(module_text, mapping["dafny_symbol"], str(mapping.get("symbol_kind") or "lemma")):
                            errors.append(f"{name}:{row_id}: Dafny symbol {mapping['dafny_symbol']} is not declared as {mapping.get('symbol_kind') or 'lemma'} in {module_path}")
                if row.get("coverage_level") == "C5_CONFORMANCE_LINKED":
                    for key in ("fixture_ref", "oracle_ref", "golden_ref"):
                        ref = row.get(key)
                        if not ref:
                            errors.append(f"{name}:{row_id}: C5 row lacks {key}")
                        elif not (ROOT / ref).exists():
                            errors.append(f"{name}:{row_id}: referenced {key} does not exist: {ref}")
                    if mappings:
                        validate_c5_conformance_links(name, row, mappings[0], errors)
                if row.get("coverage_level") == "C4_VERIFIED_PROPERTY":
                    for key in ("fixture_ref", "oracle_ref", "golden_ref"):
                        if row.get(key):
                            errors.append(f"{name}:{row_id}: C4 row must not carry conformance {key}")
                    notes = str(row.get("notes", "")).lower()
                    if "conformance-linked" in notes or "fixture/oracle/golden links" in notes:
                        errors.append(f"{name}:{row_id}: C4 row must not be described as conformance-linked")

    integration_rows = domain_rows.get("auth_audit_integration", [])
    audit_unavailable_rows = [row for row in integration_rows if row.get("test_id") == AUDIT_UNAVAILABLE_TEST_ID]
    if len(audit_unavailable_rows) != 1:
        errors.append(f"{AUDIT_UNAVAILABLE_TEST_ID}: expected exactly one auth/audit integration row")
    else:
        validate_audit_unavailable_conformance(audit_unavailable_rows[0], errors)

    formal = load_yaml(TRACEABILITY_DIR / "formal-claim-to-dafny.yml")
    for claim in formal.get("formal_claims", []):
        if claim.get("coverage_level") in PROOF_LEVELS:
            errors.append(f"{claim.get('claim_id')}: formal claim must not be C4/C5/C6 without proof artifacts")
        if claim.get("proof_claimed") or claim.get("proof_artifact_refs"):
            errors.append(f"{claim.get('claim_id')}: Phase 1.2 must not invent proof artifacts")
    return errors


def main() -> int:
    errors = compare_generated() + validate_mapping_content()
    if errors:
        for error in errors:
            print(f"phase1.2 auth/audit coverage error: {error}", file=sys.stderr)
        return 1
    print("Phase 1.2 Authorization/Audit coverage check OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
