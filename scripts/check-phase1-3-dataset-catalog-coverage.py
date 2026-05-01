#!/usr/bin/env python3
"""Validate Phase 1.3 Dataset/Catalog coverage artifacts."""

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
TRACEABILITY_DIR = ROOT / "evidence" / "traceability" / "generated" / "phase-1-3"
REPORTS_DIR = ROOT / "reports" / "current"
EVIDENCE_REGISTRY = ROOT / "docs/design/registries/evidence.yaml"
TRACE_FILES = [
    "dataset-catalog-to-dafny.yml",
    "test-to-dafny.yml",
    "fixture-to-dafny.yml",
    "requirement-to-dafny.yml",
    "formal-claim-to-dafny.yml",
]
REPORT_FILES = [
    "phase-1-3-entry-gate.yml",
    "phase-1-3-entry-gate.md",
    "dafny-dataset-catalog-gap-normalization.yml",
    "dafny-dataset-catalog-gap-normalization.md",
    "dafny-dataset-catalog-report.md",
    "dafny-dataset-catalog-validation-report.md",
    "dafny-dataset-catalog-coverage-report.md",
    "dafny-dataset-catalog-coverage.yml",
    "dafny-dataset-catalog-red-team-review.md",
    "dafny-dataset-catalog-open-issues.md",
]
PROOF_LEVELS = {"C4_VERIFIED_PROPERTY", "C5_CONFORMANCE_LINKED", "C6_RELEASE_READY_MODEL"}
SEMANTIC_LEVELS = {"C3_FULL_SEMANTIC", "C4_VERIFIED_PROPERTY", "C5_CONFORMANCE_LINKED", "C6_RELEASE_READY_MODEL"}
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
EXPECTED_NEGATIVE_SYMBOLS = {
    "NEG-MFOS-DATASET-MALFORMED-DSN-0902": "INV_DATASET_MALFORMED_DSN_REJECTED",
    "NEG-MFOS-DATASET-CATALOG-UNCOMMITTED-0904": "INV_CATALOG_UNCOMMITTED_CANNOT_RESOLVE",
    "NEG-MFOS-DATASET-CATALOG-ROLLED-BACK-0905": "INV_CATALOG_ROLLED_BACK_CANNOT_RESOLVE",
    "NEG-MFOS-DATASET-CATALOG-PARTIAL-JOURNAL-0906": "INV_CATALOG_PARTIAL_JOURNAL_CANNOT_RESOLVE",
    "NEG-MFOS-DATASET-CATALOG-INTEGRITY-FAILED-0907": "INV_CATALOG_INTEGRITY_FAILED_CANNOT_RESOLVE",
    "NEG-MFOS-DATASET-UNAUTHORIZED-OPEN-0908": "INV_DATASET_OPEN_DENY_PRODUCES_NO_HANDLE",
    "NEG-MFOS-DATASET-STALE-HANDLE-POLICY-0909": "INV_DATASET_STALE_HANDLE_AFTER_POLICY_CHANGE_REJECTED",
    "NEG-MFOS-DATASET-STALE-HANDLE-CATALOG-0910": "INV_DATASET_STALE_HANDLE_AFTER_CATALOG_GENERATION_CHANGE_REJECTED",
    "NEG-MFOS-DATASET-RETENTION-DELETE-0911": "INV_DATASET_RETENTION_VIOLATION_NOT_SUCCESS",
    "NEG-MFOS-DATASET-IMMUTABLE-SYSTEM-0912": "INV_DATASET_IMMUTABLE_SYSTEM_MODIFICATION_NOT_SUCCESS",
    "NEG-MFOS-DATASET-NOT-POSIX-FILE-0913": "INV_DATASET_NOT_POSIX_FILE",
}
EXPECTED_ROW_ERRORS = {
    "NEG-MFOS-DATASET-MALFORMED-DSN-0902": "MFOS_ERR_INVALID_DSN",
    "NEG-MFOS-DATASET-CATALOG-UNCOMMITTED-0904": "MFOS_ERR_CATALOG_NOT_FOUND",
    "NEG-MFOS-DATASET-CATALOG-ROLLED-BACK-0905": "MFOS_ERR_CATALOG_NOT_FOUND",
    "NEG-MFOS-DATASET-CATALOG-PARTIAL-JOURNAL-0906": "MFOS_ERR_INTERNAL_CORRUPTION",
    "NEG-MFOS-DATASET-CATALOG-INTEGRITY-FAILED-0907": "MFOS_ERR_INTERNAL_CORRUPTION",
    "NEG-MFOS-DATASET-UNAUTHORIZED-OPEN-0908": "MFOS_ERR_POLICY_DENIED",
    "NEG-MFOS-DATASET-STALE-HANDLE-POLICY-0909": "MFOS_ERR_POLICY_VERSION_MISMATCH",
    "NEG-MFOS-DATASET-STALE-HANDLE-CATALOG-0910": "MFOS_ERR_STALE_HANDLE",
    "NEG-MFOS-DATASET-RETENTION-DELETE-0911": "MFOS_ERR_RETENTION_DENIED",
    "NEG-MFOS-DATASET-IMMUTABLE-SYSTEM-0912": "MFOS_ERR_IMMUTABLE",
    "NEG-MFOS-DATASET-NOT-POSIX-FILE-0913": "MFOS_ERR_UNSUPPORTED",
    "TEST-MFOS-DATASET-CRASH-MID-COMMIT-0914": "MFOS_ERR_INTERNAL_CORRUPTION",
}
EXPECTED_SUCCESS_ROWS = {
    "TEST-MFOS-DATASET-VALID-DSN-0901",
    "TEST-MFOS-DATASET-CATALOG-COMMITTED-0903",
}
REQUIRED_PROPERTY_SYMBOLS = {
    "INV_CATALOG_TX_COMMITTED_NOT_COMPLETE_CANNOT_RESOLVE",
    "INV_DATASET_SYSTEM_DATASET_REQUIRES_IMMUTABLE",
    "INV_DATASET_AUDITED_DENY_DOES_NOT_BIND_MFOS_OK",
    "INV_DATASET_HANDLE_REQUIRES_RESOLVABLE_ENTRY",
    "INV_DATASET_DELETE_OR_MODIFY_REJECTS_NONRESOLVABLE",
}
CRASH_PARTIAL_SYMBOL = "INV_CATALOG_CRASH_MID_COMMIT_PARTIAL_STATE_CANNOT_RESOLVE"
CRASH_RECOVERY_COMPLETENESS_SYMBOL = "INV_CATALOG_CRASH_MID_COMMIT_RECOVERY_EXPOSES_ONLY_SAFE_STATE"
FORMAL_CLAIM_REGISTRY = ROOT / "formal" / "claim-registry.yml"


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return data


def row_name(row: dict[str, Any]) -> str:
    return str(row.get("test_id") or row.get("property_id") or row.get("requirement_id") or row.get("claim_id") or row.get("integration_id") or "<unknown>")


def level_rank(level: Any) -> int:
    return LEVEL_RANK.get(str(level), -1)


def worst_level(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "C0_NONE"
    return min((str(row.get("coverage_level")) for row in rows), key=lambda level: LEVEL_RANK.get(level, -1))


def collect_symbols(rows: list[dict[str, Any]]) -> set[str]:
    symbols: set[str] = set()
    for row in rows:
        for mapping in row.get("coverage_mappings") or []:
            symbol = mapping.get("dafny_symbol")
            if symbol:
                symbols.add(str(symbol))
    return symbols


def expect_summary_not_above(summary_name: str, summary_level: Any, child_rows: list[dict[str, Any]], errors: list[str]) -> None:
    worst = worst_level(child_rows)
    if level_rank(summary_level) > level_rank(worst):
        errors.append(f"{summary_name}={summary_level} exceeds child aggregate level {worst}")


def load_claim_registry_ids() -> set[str]:
    registry = load_yaml(FORMAL_CLAIM_REGISTRY)
    return {str(row.get("claim_id")) for row in registry.get("claims", []) if isinstance(row, dict)}


def first_decision_result(golden: dict[str, Any]) -> str | None:
    decisions = golden.get("expected_decisions") or []
    if isinstance(decisions, list) and decisions and isinstance(decisions[0], dict):
        result = decisions[0].get("result")
        return str(result) if result is not None else None
    return None


def validate_expected_error(source_name: str, row_id: str, golden: dict[str, Any], errors: list[str]) -> None:
    expected_error = EXPECTED_ROW_ERRORS.get(row_id)
    if expected_error is None and row_id in EXPECTED_SUCCESS_ROWS:
        if golden.get("expected_failure_mode") is not None:
            errors.append(f"{source_name}:{row_id}: success row must not carry expected_failure_mode")
        oracle = golden.get("oracle") or {}
        failure = oracle.get("expected_failure") if isinstance(oracle, dict) else {}
        if isinstance(failure, dict) and failure.get("error_code") is not None:
            errors.append(f"{source_name}:{row_id}: success row oracle must not carry expected failure error")
        return
    if expected_error is None:
        return
    observed = [
        ("expected_failure_mode", golden.get("expected_failure_mode")),
    ]
    audit_records = golden.get("expected_audit_sequence") or []
    if isinstance(audit_records, list) and audit_records and isinstance(audit_records[0], dict):
        observed.append(("expected_audit_sequence[0].reason_code", audit_records[0].get("reason_code")))
    transitions = golden.get("expected_state_transitions") or []
    if isinstance(transitions, list) and transitions and isinstance(transitions[0], dict):
        observed.append(("expected_state_transitions[0].reason", transitions[0].get("reason")))
    oracle = golden.get("oracle") or {}
    failure = oracle.get("expected_failure") if isinstance(oracle, dict) else {}
    if isinstance(failure, dict):
        observed.append(("oracle.expected_failure.error_code", failure.get("error_code")))
        if failure.get("fail_closed") is not True:
            errors.append(f"{source_name}:{row_id}: expected fail-closed oracle for {expected_error}")
    for field, value in observed:
        if value != expected_error:
            errors.append(f"{source_name}:{row_id}: {field}={value} does not match Dafny expected error {expected_error}")
    if first_decision_result(golden) == "DENY" and expected_error in {None, "MFOS_OK", "OK"}:
        errors.append(f"{source_name}:{row_id}: DENY row must not bind MFOS_OK/OK")
    output = golden.get("expected_normalized_output") or {}
    if isinstance(output, dict) and output.get("outcome") != "EXPECTED_FAIL_CLOSED":
        errors.append(f"{source_name}:{row_id}: fail-closed row must use EXPECTED_FAIL_CLOSED")


def validate_crash_row(
    source_name: str,
    row: dict[str, Any],
    fixture: dict[str, Any],
    golden: dict[str, Any],
    errors: list[str],
) -> None:
    row_id = row_name(row)
    if row_id != "TEST-MFOS-DATASET-CRASH-MID-COMMIT-0914":
        return
    symbols = collect_symbols([row])
    if CRASH_PARTIAL_SYMBOL not in symbols:
        errors.append(f"{source_name}:{row_id}: crash-mid-commit row must map to partial-state non-resolution symbol")
    if CRASH_RECOVERY_COMPLETENESS_SYMBOL in symbols:
        errors.append(f"{source_name}:{row_id}: crash recovery completeness symbol is not modeled in Phase 1.3")
    note = str(row.get("notes", "")).lower()
    forbidden_phrases = ("recovery exposes", "committed or absent", "safe catalog state")
    if any(phrase in note for phrase in forbidden_phrases):
        errors.append(f"{source_name}:{row_id}: C5 note claims crash recovery completeness instead of partial-state non-resolution")
    initial_state = fixture.get("initial_state") or {}
    catalog_transaction = initial_state.get("catalog_transaction") if isinstance(initial_state, dict) else {}
    recovery_expectation = (
        catalog_transaction.get("recovery_expectation")
        if isinstance(catalog_transaction, dict)
        else None
    )
    if recovery_expectation != "partial_candidate_nonresolution_only":
        errors.append(
            f"{source_name}:{row_id}: fixture recovery_expectation must be "
            "partial_candidate_nonresolution_only and must not claim recovery selection"
        )
    output = golden.get("expected_normalized_output") or {}
    if isinstance(output, dict) and output.get("recovery_exposes_only_committed_or_absent") is True:
        errors.append(f"{source_name}:{row_id}: golden must not claim full recovery exposure")
    recovery = (golden.get("oracle") or {}).get("expected_recovery") if isinstance(golden.get("oracle"), dict) else {}
    if isinstance(recovery, dict) and recovery.get("exposes_only_committed_or_absent") is True:
        errors.append(f"{source_name}:{row_id}: oracle must not claim full recovery exposure")


def exact_dafny_symbol_declared(module_text: str, symbol: str, symbol_kind: str) -> bool:
    kind = re.escape(symbol_kind or "lemma")
    pattern = rf"^\s*(?:ghost\s+)?{kind}\s+{re.escape(symbol)}\s*(?:\(|<)"
    return re.search(pattern, module_text, flags=re.MULTILINE) is not None


def compare_generated() -> list[str]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        tmp_trace = tmp_path / "traceability"
        tmp_reports = tmp_path / "reports"
        subprocess.run(
            [
                sys.executable,
                "scripts/generators/generate-dataset-catalog-coverage.py",
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


def validate_c5_links(source_name: str, row: dict[str, Any], mapping: dict[str, Any], errors: list[str]) -> None:
    row_id = row_name(row)
    refs = {key: row.get(key) for key in ("fixture_ref", "oracle_ref", "golden_ref")}
    for key, ref in refs.items():
        if not ref:
            errors.append(f"{source_name}:{row_id}: C5 row lacks {key}")
        elif not (ROOT / str(ref)).exists():
            errors.append(f"{source_name}:{row_id}: referenced {key} does not exist: {ref}")
    if any(not ref for ref in refs.values()):
        return
    if refs["oracle_ref"] != refs["golden_ref"]:
        errors.append(f"{source_name}:{row_id}: C5 row must use the embedded oracle golden vector convention")
    fixture = load_yaml(ROOT / str(refs["fixture_ref"]))
    golden = load_yaml(ROOT / str(refs["golden_ref"]))
    oracle = golden.get("oracle")
    if not isinstance(oracle, dict):
        errors.append(f"{source_name}:{row_id}: golden_ref must embed an oracle mapping")
        return
    if fixture.get("expected_oracle") != refs["golden_ref"]:
        errors.append(f"{source_name}:{row_id}: fixture expected_oracle does not match golden_ref")
    if golden.get("fixture_ref") != refs["fixture_ref"]:
        errors.append(f"{source_name}:{row_id}: golden fixture_ref does not match fixture_ref")
    if oracle.get("fixture_ref") != refs["fixture_ref"]:
        errors.append(f"{source_name}:{row_id}: embedded oracle fixture_ref does not match fixture_ref")
    if golden.get("deterministic") is not True:
        errors.append(f"{source_name}:{row_id}: C5 golden vector must be deterministic")
    if fixture.get("expected_evidence") != oracle.get("evidence_required"):
        errors.append(f"{source_name}:{row_id}: fixture expected_evidence must match oracle evidence_required")
    if golden.get("expected_decisions") != oracle.get("expected_decisions"):
        errors.append(f"{source_name}:{row_id}: golden expected_decisions must mirror embedded oracle")
    if golden.get("expected_state_transitions") != oracle.get("expected_state_transitions"):
        errors.append(f"{source_name}:{row_id}: golden expected_state_transitions must mirror embedded oracle")
    if golden.get("expected_audit_sequence") != oracle.get("expected_audit_records"):
        errors.append(f"{source_name}:{row_id}: golden expected_audit_sequence must mirror embedded oracle expected_audit_records")
    if golden.get("expected_final_state") != oracle.get("expected_final_state"):
        errors.append(f"{source_name}:{row_id}: golden expected_final_state must mirror embedded oracle")
    if row_id == "TEST-MFOS-DATASET-CATALOG-COMMITTED-0903":
        tx = ((fixture.get("initial_state") or {}).get("catalog_transaction") or {})
        if tx.get("candidate_state") != "CATALOG_COMMITTED":
            errors.append(f"{source_name}:{row_id}: committed fixture must declare CATALOG_COMMITTED candidate_state")
        if tx.get("transaction_state") != "CATALOG_TX_COMPLETE":
            errors.append(f"{source_name}:{row_id}: committed fixture must declare CATALOG_TX_COMPLETE")
        if tx.get("integrity_valid") is not True or tx.get("integrity_tag_verified") is not True:
            errors.append(f"{source_name}:{row_id}: committed fixture must declare valid integrity state")
        expected_tx = golden.get("expected_catalog_transaction")
        oracle_tx = oracle.get("expected_catalog_transaction")
        if expected_tx != oracle_tx or expected_tx != {
            "candidate_state": "CATALOG_COMMITTED",
            "transaction_state": "CATALOG_TX_COMPLETE",
            "integrity_valid": True,
            "integrity_tag_verified": True,
        }:
            errors.append(f"{source_name}:{row_id}: committed golden/oracle must mirror transaction-complete evidence")
    failure = oracle.get("expected_failure")
    if isinstance(failure, dict) and golden.get("expected_failure_mode") != failure.get("error_code"):
        errors.append(f"{source_name}:{row_id}: golden expected_failure_mode must mirror embedded oracle expected_failure.error_code")
    for mapping_row in row.get("coverage_mappings") or [mapping]:
        evidence_ref = mapping_row.get("evidence_ref")
        if evidence_ref and evidence_ref.startswith("EV-") and evidence_ref not in (oracle.get("evidence_required") or []):
            errors.append(f"{source_name}:{row_id}: mapping evidence_ref is not required by the embedded oracle")
    validate_expected_error(source_name, row_id, golden, errors)
    validate_crash_row(source_name, row, fixture, golden, errors)


def validate_rows(source_name: str, rows: list[dict[str, Any]], errors: list[str], known_evidence: set[str] | None = None) -> None:
    for row in rows:
        row_id = row_name(row)
        row_level = row.get("coverage_level")
        mappings = row.get("coverage_mappings") or []
        if row_level == "C4_VERIFIED_PROPERTY":
            if row.get("fixture_ref") or row.get("oracle_ref") or row.get("golden_ref"):
                errors.append(f"{source_name}:{row_id}: C4 row must not carry fixture/oracle/golden links")
            note = str(row.get("notes", "")).lower()
            if "conformance" in note or "fixture/oracle/golden" in note:
                errors.append(f"{source_name}:{row_id}: C4 row must not be described as conformance-linked")
        if row_level in SEMANTIC_LEVELS and not mappings:
            errors.append(f"{source_name}:{row_id}: semantic row lacks mappings")
            continue
        for mapping in mappings:
            if not mapping.get("dafny_symbol"):
                errors.append(f"{source_name}:{row_id}: semantic mapping lacks dafny_symbol")
            if row_level in PROOF_LEVELS and mapping.get("verification_status") != "verified":
                errors.append(f"{source_name}:{row_id}: C4/C5 mapping not verified")
            if not mapping.get("evidence_ref"):
                errors.append(f"{source_name}:{row_id}: semantic mapping lacks evidence_ref")
            elif str(mapping.get("evidence_ref")).startswith("EV-") and known_evidence is not None and mapping.get("evidence_ref") not in known_evidence:
                errors.append(f"{source_name}:{row_id}: semantic mapping evidence_ref is not registered: {mapping.get('evidence_ref')}")
            if level_rank(mapping.get("coverage_level")) < level_rank(row_level):
                errors.append(f"{source_name}:{row_id}: mapping coverage level is below row coverage level")
            module_path = ROOT / str(mapping.get("dafny_module", ""))
            if not module_path.exists():
                errors.append(f"{source_name}:{row_id}: Dafny module does not exist: {module_path}")
            elif mapping.get("dafny_symbol"):
                module_text = module_path.read_text(encoding="utf-8")
                if not exact_dafny_symbol_declared(module_text, mapping["dafny_symbol"], str(mapping.get("symbol_kind") or "lemma")):
                    errors.append(f"{source_name}:{row_id}: Dafny symbol {mapping['dafny_symbol']} is not declared as {mapping.get('symbol_kind') or 'lemma'} in {module_path}")
        if row_level == "C5_CONFORMANCE_LINKED" and mappings:
            for mapping in mappings:
                if not mapping.get("dafny_symbol"):
                    errors.append(f"{source_name}:{row_id}: C5 row lacks explicit Dafny symbol")
                if mapping.get("verification_status") != "verified":
                    errors.append(f"{source_name}:{row_id}: C5 row lacks verification evidence")
                if not mapping.get("evidence_ref"):
                    errors.append(f"{source_name}:{row_id}: C5 row lacks verification evidence ref")
            validate_c5_links(source_name, row, mappings[0], errors)
        if str(row_id).startswith("NEG-") or row_id == "TEST-MFOS-DATASET-CRASH-MID-COMMIT-0914":
            expected_symbol = EXPECTED_NEGATIVE_SYMBOLS.get(row_id)
            if row_id == "TEST-MFOS-DATASET-CRASH-MID-COMMIT-0914":
                expected_symbol = CRASH_PARTIAL_SYMBOL
            actual_symbols = {str(mapping.get("dafny_symbol")) for mapping in mappings}
            if expected_symbol and expected_symbol not in actual_symbols:
                errors.append(f"{source_name}:{row_id}: negative test maps to unrelated Dafny symbol; expected {expected_symbol}")
            if "MALFORMED-DSN" in row_id and any("STALE" in symbol for symbol in actual_symbols):
                errors.append(f"{source_name}:{row_id}: malformed DSN maps to stale handle logic without explicit justification")


def validate_python_boundary(errors: list[str]) -> None:
    for rel in (
        "scripts/generators/generate-dataset-catalog-coverage.py",
        "scripts/check-phase1-3-dataset-catalog-coverage.py",
    ):
        text = (ROOT / rel).read_text(encoding="utf-8")
        forbidden = [
            r"if\s+.*\.get\(['\"]operation['\"]\)\s*==",
            r"if\s+.*\.get\(['\"]candidate_state['\"]\)\s*==",
            r"if\s+.*\.get\(['\"]transaction_state['\"]\)\s*==",
            r"if\s+.*CatalogEntryResolvable",
        ]
        for pattern in forbidden:
            if re.search(pattern, text):
                errors.append(f"{rel}: Python tooling appears to evaluate Dataset/Catalog business semantics: {pattern}")


def validate_mapping_content() -> list[str]:
    errors: list[str] = []
    coverage = load_yaml(REPORTS_DIR / "dafny-dataset-catalog-coverage.yml")
    gate = load_yaml(REPORTS_DIR / "phase-1-3-entry-gate.yml")
    evidence_registry = load_yaml(EVIDENCE_REGISTRY)
    known_evidence = {
        entry.get("evidence_id")
        for entry in evidence_registry.get("entries", [])
        if isinstance(entry, dict)
    }
    if coverage.get("dataset_catalog_exit_blockers_remaining"):
        errors.append("Phase 1.3 coverage still reports Dataset/Catalog exit blockers")
    if gate.get("merge_blockers") or gate.get("dataset_catalog_merge_blockers_remaining"):
        errors.append("Phase 1.3 entry gate still reports Dataset/Catalog merge blockers")
    if gate.get("phase_1_3_merge_allowed") is not True:
        errors.append("Phase 1.3 entry gate must report phase_1_3_merge_allowed true after closure")
    if coverage.get("formal_claims_proof_backed"):
        errors.append("Phase 1.3 coverage must not claim proof-backed formal claims")
    if coverage.get("python_loader_contains_dataset_catalog_semantics"):
        errors.append("Python loader/harness semantics flag must remain false")

    dataset_data = load_yaml(TRACEABILITY_DIR / "dataset-catalog-to-dafny.yml")
    dataset_rows = dataset_data.get("entries")
    if not isinstance(dataset_rows, list):
        errors.append("dataset-catalog-to-dafny.yml: entries must be a list")
        dataset_rows = []
    required_rows = [row for row in dataset_rows if row.get("required_for_dataset_catalog_aggregate")]
    expect_summary_not_above("dataset_catalog_coverage_level", coverage.get("dataset_catalog_coverage_level"), required_rows, errors)
    if level_rank(coverage.get("dataset_catalog_coverage_level")) >= level_rank("C5_CONFORMANCE_LINKED"):
        below = [
            f"{row_name(row)}={row.get('coverage_level')}"
            for row in required_rows
            if level_rank(row.get("coverage_level")) < level_rank("C5_CONFORMANCE_LINKED")
        ]
        if below:
            errors.append("dataset_catalog_coverage_level is C5+ while required child rows are below C5: " + ", ".join(below))
    symbols = collect_symbols(dataset_rows)
    missing_properties = sorted(REQUIRED_PROPERTY_SYMBOLS - symbols)
    if missing_properties:
        errors.append("Phase 1.3 Dataset/Catalog required property symbols missing: " + ", ".join(missing_properties))
    if CRASH_RECOVERY_COMPLETENESS_SYMBOL in symbols:
        errors.append("Phase 1.3 must not claim crash recovery completeness without a recovery model")
    validate_rows("dataset-catalog-to-dafny.yml", dataset_rows, errors, known_evidence)

    test_data = load_yaml(TRACEABILITY_DIR / "test-to-dafny.yml")
    validate_rows("test-to-dafny.yml", test_data.get("tests") or [], errors, known_evidence)

    req_data = load_yaml(TRACEABILITY_DIR / "requirement-to-dafny.yml")
    req_rows = req_data.get("requirements") or []
    expect_summary_not_above("dataset_catalog_requirement_coverage_level", coverage.get("dataset_catalog_requirement_coverage_level"), req_rows, errors)
    for row in req_rows:
        if row_name(row) == "MFOS-REQ-CATALOG-0102" and level_rank(row.get("coverage_level")) >= level_rank("C4_VERIFIED_PROPERTY"):
            errors.append("MFOS-REQ-CATALOG-0102 must not be C4/C5 until crash recovery selection is modeled")
    validate_rows("requirement-to-dafny.yml", req_rows, errors, known_evidence)

    fixture_data = load_yaml(TRACEABILITY_DIR / "fixture-to-dafny.yml")
    validate_rows("fixture-to-dafny.yml", fixture_data.get("fixtures") or [], errors, known_evidence)

    formal = load_yaml(TRACEABILITY_DIR / "formal-claim-to-dafny.yml")
    formal_rows = formal.get("formal_claims", []) or []
    expect_summary_not_above("formal_claim_coverage_level", coverage.get("formal_claim_coverage_level"), formal_rows, errors)
    claim_ids = load_claim_registry_ids()
    for claim in formal.get("formal_claims", []):
        claim_id = str(claim.get("claim_id"))
        if not claim_id.startswith("MFOS-FC-"):
            errors.append(f"{claim_id}: formal claim id must use MFOS-FC-* namespace")
        if claim_id not in claim_ids:
            errors.append(f"{claim_id}: formal claim is not present in formal/claim-registry.yml")
        if claim.get("coverage_level") in PROOF_LEVELS:
            errors.append(f"{claim.get('claim_id')}: formal claim must not be C4/C5/C6 without proof artifacts")
        if claim.get("proof_claimed") or claim.get("proof_artifact_refs"):
            errors.append(f"{claim.get('claim_id')}: Phase 1.3 must not invent proof artifacts")
    validate_rows("formal-claim-to-dafny.yml", formal_rows, errors, known_evidence)

    integration_rows = [row for row in dataset_rows if row.get("domain") == "dataset_catalog_auth_audit_integration"]
    expect_summary_not_above("dataset_catalog_auth_audit_integration_coverage_level", coverage.get("dataset_catalog_auth_audit_integration_coverage_level"), integration_rows, errors)

    dataset_text = (ROOT / "formal/executable-semantics/dafny/modules/dataset_catalog.dfy").read_text(encoding="utf-8")
    audit_text = (ROOT / "formal/executable-semantics/dafny/modules/audit.dfy").read_text(encoding="utf-8")
    if "requires !IsSuccessError(decision.error_code)" not in dataset_text:
        errors.append("Dataset/Catalog audited DENY entry point does not block MFOS_OK")
    if "function FinalizeDeniedOperation" in audit_text and "requires !IsSuccessError(decision.error_code)" not in audit_text:
        errors.append("Audit FinalizeDeniedOperation does not block DENY+MFOS_OK")

    gap = load_yaml(REPORTS_DIR / "dafny-dataset-catalog-gap-normalization.yml")
    if gap.get("exit_blockers_remaining"):
        errors.append("gap normalization still reports exit blockers")
    for entry in gap.get("entries", []):
        if entry.get("phase_1_3_exit_blocker") or entry.get("current_pr_merge_blocker"):
            errors.append(f"{entry.get('gap_id')}: Phase 1.3 exit/current PR blocker remains")
    validate_python_boundary(errors)
    return errors


def main() -> int:
    errors = compare_generated() + validate_mapping_content()
    if errors:
        for error in errors:
            print(f"phase1.3 dataset/catalog coverage error: {error}", file=sys.stderr)
        return 1
    print("Phase 1.3 Dataset/Catalog coverage check OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
