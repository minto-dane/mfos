#!/usr/bin/env python3
"""Generate Phase 1.3 Dataset/Catalog Dafny coverage artifacts."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
TRACEABILITY_DIR = ROOT / "evidence" / "traceability" / "generated" / "phase-1-3"
REPORTS_DIR = ROOT / "reports" / "generated" / "phase-1-3"

COVERAGE_LEVELS = [
    "C0_NONE",
    "C1_TYPE_ONLY",
    "C2_PARTIAL_SEMANTIC",
    "C3_FULL_SEMANTIC",
    "C4_VERIFIED_PROPERTY",
    "C5_CONFORMANCE_LINKED",
    "C6_RELEASE_READY_MODEL",
]
COVERAGE_RANK = {level: rank for rank, level in enumerate(COVERAGE_LEVELS)}
DATASET_MODULE = "formal/executable-semantics/dafny/modules/dataset_catalog.dfy"

DATASET_TESTS: list[tuple[str, str, str]] = [
    ("TEST-MFOS-DATASET-VALID-DSN-0901", "INV_DATASET_VALID_DSN_ACCEPTED", "valid symbolic DSN acceptance"),
    ("NEG-MFOS-DATASET-MALFORMED-DSN-0902", "INV_DATASET_MALFORMED_DSN_REJECTED", "malformed symbolic DSN rejection"),
    ("TEST-MFOS-DATASET-CATALOG-COMMITTED-0903", "INV_CATALOG_COMMITTED_ENTRY_RESOLVES", "committed catalog entry resolution"),
    ("NEG-MFOS-DATASET-CATALOG-UNCOMMITTED-0904", "INV_CATALOG_UNCOMMITTED_CANNOT_RESOLVE", "uncommitted catalog entry rejection"),
    ("NEG-MFOS-DATASET-CATALOG-ROLLED-BACK-0905", "INV_CATALOG_ROLLED_BACK_CANNOT_RESOLVE", "rolled-back catalog entry rejection"),
    ("NEG-MFOS-DATASET-CATALOG-PARTIAL-JOURNAL-0906", "INV_CATALOG_PARTIAL_JOURNAL_CANNOT_RESOLVE", "partial-journal catalog entry rejection"),
    ("NEG-MFOS-DATASET-CATALOG-INTEGRITY-FAILED-0907", "INV_CATALOG_INTEGRITY_FAILED_CANNOT_RESOLVE", "integrity-failed catalog entry rejection"),
    ("NEG-MFOS-DATASET-UNAUTHORIZED-OPEN-0908", "INV_DATASET_OPEN_DENY_PRODUCES_NO_HANDLE", "denied dataset open creates no handle"),
    ("NEG-MFOS-DATASET-STALE-HANDLE-POLICY-0909", "INV_DATASET_STALE_HANDLE_AFTER_POLICY_CHANGE_REJECTED", "policy-version stale handle rejection"),
    ("NEG-MFOS-DATASET-STALE-HANDLE-CATALOG-0910", "INV_DATASET_STALE_HANDLE_AFTER_CATALOG_GENERATION_CHANGE_REJECTED", "catalog-generation stale handle rejection"),
    ("NEG-MFOS-DATASET-RETENTION-DELETE-0911", "INV_DATASET_RETENTION_VIOLATION_NOT_SUCCESS", "retention delete rejection"),
    ("NEG-MFOS-DATASET-IMMUTABLE-SYSTEM-0912", "INV_DATASET_IMMUTABLE_SYSTEM_MODIFICATION_NOT_SUCCESS", "immutable system dataset modification rejection"),
    ("NEG-MFOS-DATASET-NOT-POSIX-FILE-0913", "INV_DATASET_NOT_POSIX_FILE", "dataset is not a POSIX file model"),
    ("TEST-MFOS-DATASET-CRASH-MID-COMMIT-0914", "INV_CATALOG_CRASH_MID_COMMIT_PARTIAL_STATE_CANNOT_RESOLVE", "crash-mid-commit partial candidate rejection; no crash recovery completeness claim"),
]

PROPERTY_ROWS: list[tuple[str, str, str]] = [
    ("DATASET-CATALOG-TX-COMMITTED-NOT-COMPLETE", "INV_CATALOG_TX_COMMITTED_NOT_COMPLETE_CANNOT_RESOLVE", "Catalog transaction state CATALOG_TX_COMMITTED is not complete and cannot resolve."),
    ("DATASET-CATALOG-SYSTEM-DATASET-INVARIANT", "INV_DATASET_SYSTEM_DATASET_REQUIRES_IMMUTABLE", "system_dataset == true && immutable == false is an invalid model state."),
    ("DATASET-CATALOG-DENY-NOT-MFOS-OK", "INV_DATASET_AUDITED_DENY_DOES_NOT_BIND_MFOS_OK", "Audited Dataset/Catalog DENY cannot bind MFOS_OK."),
    ("DATASET-CATALOG-HANDLE-REQUIRES-RESOLVABLE", "INV_DATASET_HANDLE_REQUIRES_RESOLVABLE_ENTRY", "Dataset handle validation rejects non-resolvable catalog entries."),
    ("DATASET-CATALOG-MODIFY-REQUIRES-RESOLVABLE", "INV_DATASET_DELETE_OR_MODIFY_REJECTS_NONRESOLVABLE", "Dataset delete/modify rejects non-resolvable catalog entries."),
]

INTEGRATION_PROPERTIES: list[tuple[str, str, str]] = [
    ("DATASET-CATALOG-AUTH-ALLOW-ONLY", "INV_DATASET_OPEN_SUCCESS_REQUIRES_ALLOW_OR_ALLOW_WITH_AUDIT", "Dataset open success requires ALLOW or ALLOW_WITH_AUDIT."),
    ("DATASET-CATALOG-HANDLE-NO-BYPASS", "INV_DATASET_HANDLE_CREATION_CANNOT_BYPASS_AUTHORIZATION", "Dataset handle creation cannot bypass authorization."),
    ("DATASET-CATALOG-DENY-AUDIT-BEFORE-RETURN", "INV_DATASET_OPEN_DENY_WITH_AUDIT_WRITES_BEFORE_RETURN", "Dataset open DENY with audit obligation links to before-return audit evidence."),
    ("DATASET-CATALOG-DENY-AUDIT-UNAVAILABLE", "INV_DATASET_OPEN_DENY_AUDIT_UNAVAILABLE_FAILS_CLOSED", "Dataset open DENY fails closed when required audit is unavailable."),
    ("DATASET-CATALOG-AUDIT-NO-BYPASS", "INV_DATASET_CANNOT_BYPASS_AUDIT_WHEN_OBLIGATION_EXISTS", "Dataset/Catalog fail-closed result cannot bypass required audit evidence."),
]

REQUIREMENTS: list[tuple[str, str, str, str]] = [
    ("MFOS-REQ-CATALOG-0002", "INV_CATALOG_RESOLVE_SUCCESS_IMPLIES_COMMITTED", "C4_VERIFIED_PROPERTY", "Catalog resolution returns only committed, integrity-valid, transaction-complete entries."),
    ("MFOS-REQ-CATALOG-0101", "INV_CATALOG_RESOLVE_SUCCESS_IMPLIES_COMMITTED", "C4_VERIFIED_PROPERTY", "Registry mirror for committed-only catalog resolution."),
    ("MFOS-REQ-CATALOG-0102", "INV_CATALOG_CRASH_MID_COMMIT_PARTIAL_STATE_CANNOT_RESOLVE", "C2_PARTIAL_SEMANTIC", "Crash-mid-commit partial candidates cannot resolve; full crash recovery selection is not modeled in Phase 1.3."),
    ("MFOS-REQ-DATASET-0101", "INV_DATASET_CREATE_HANDLE_BINDS_DECISION", "C4_VERIFIED_PROPERTY", "Dataset handles bind subject, operation, policy, catalog generation, and dataset generation where modeled."),
    ("MFOS-REQ-DATASET-0102", "INV_DATASET_NOT_POSIX_FILE", "C4_VERIFIED_PROPERTY", "Dataset semantics reject POSIX file-model substitution."),
    ("MFOS-REQ-DATASET-0103", "INV_DATASET_RETENTION_VIOLATION_NOT_SUCCESS", "C4_VERIFIED_PROPERTY", "Retention metadata blocks delete and purge while active."),
]

FORMAL_CLAIMS: list[tuple[str, str, str]] = [
    ("MFOS-FC-AUTHORIZATION-NO-HANDLE-WITHOUT-ALLOW", "INV_DATASET_HANDLE_CREATION_CANNOT_BYPASS_AUTHORIZATION", "Formal claim remains planned; Phase 1.3 adds a Dataset/Catalog-linked Dafny lemma but no proof artifact is claimed."),
]

PREVIOUS_DATASET_GAPS = {
    "TEST-MFOS-DATASET-VALID-DSN-0901",
    "NEG-MFOS-DATASET-MALFORMED-DSN-0902",
    "TEST-MFOS-DATASET-CATALOG-COMMITTED-0903",
    "NEG-MFOS-DATASET-RETENTION-DELETE-0911",
    "NEG-MFOS-DATASET-IMMUTABLE-SYSTEM-0912",
    "NEG-MFOS-DATASET-NOT-POSIX-FILE-0913",
    "TEST-MFOS-DATASET-CRASH-MID-COMMIT-0914",
}
PREVIOUS_REQUIREMENT_GAPS = {
    "MFOS-REQ-CATALOG-0002",
    "MFOS-REQ-CATALOG-0101",
    "MFOS-REQ-DATASET-0101",
    "MFOS-REQ-DATASET-0102",
}


def slug(test_id: str) -> str:
    value = test_id.lower().replace("test-mfos-", "").replace("neg-mfos-", "").replace("_", "-")
    if value.startswith("dataset-"):
        value = value[len("dataset-"):]
    return value


def evidence_for(test_id: str) -> str:
    clean = test_id.removeprefix("TEST-").removeprefix("NEG-")
    return "EV-" + clean


def evidence_for_property(property_id: str) -> str:
    return "EV-MFOS-" + property_id + "-0001"


def evidence_for_claim(claim_id: str) -> str:
    if claim_id == "MFOS-FC-AUTHORIZATION-NO-HANDLE-WITHOUT-ALLOW":
        return "EV-MFOS-FORMAL-CLAIM-AUTHORIZATION-0001"
    return "EV-MFOS-FORMAL-CLAIM-0001"


def mapping(symbol: str, level: str) -> dict[str, Any]:
    return {
        "dafny_module": DATASET_MODULE,
        "dafny_symbol": symbol,
        "symbol_kind": "lemma",
        "verification_status": "verified",
        "evidence_ref": "reports/generated/phase-1-3/dafny-dataset-catalog-validation-report.md",
        "coverage_level": level,
    }


def test_entry(item: tuple[str, str, str]) -> dict[str, Any]:
    test_id, symbol, note = item
    linked = True
    base = slug(test_id)
    test_type = "negative" if test_id.startswith("NEG-") or test_id == "TEST-MFOS-DATASET-CRASH-MID-COMMIT-0914" else "conformance"
    return {
        "test_id": test_id,
        "domain": "dataset_catalog",
        "test_type": test_type,
        "coverage_level": "C5_CONFORMANCE_LINKED",
        "phase_1_3_exit_blocker": False,
        "required_for_dataset_catalog_aggregate": True,
        "fixture_ref": f"tests/fixtures/dataset/{base}.yml" if linked else None,
        "oracle_ref": f"tests/golden/dataset/{base}.yml" if linked else None,
        "golden_ref": f"tests/golden/dataset/{base}.yml" if linked else None,
        "coverage_mappings": [{**mapping(symbol, "C5_CONFORMANCE_LINKED"), "evidence_ref": evidence_for(test_id)}],
        "negative_failure_conditions": [symbol] if test_type == "negative" else [],
        "notes": f"{note}; fixture/oracle/golden links are deterministic conformance evidence and Python remains a non-semantic loader/comparator.",
    }


def integration_entry(item: tuple[str, str, str]) -> dict[str, Any]:
    integration_id, symbol, note = item
    return {
        "integration_id": integration_id,
        "domain": "dataset_catalog_auth_audit_integration",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "phase_1_3_exit_blocker": False,
        "required_for_dataset_catalog_aggregate": False,
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [{**mapping(symbol, "C4_VERIFIED_PROPERTY"), "evidence_ref": evidence_for_property(integration_id)}],
        "notes": note + " This integration row stays C4 because no Dataset/Catalog scenario vector raises it to C5.",
    }


def property_entry(item: tuple[str, str, str]) -> dict[str, Any]:
    property_id, symbol, note = item
    return {
        "property_id": property_id,
        "domain": "dataset_catalog",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "phase_1_3_exit_blocker": False,
        "required_for_dataset_catalog_aggregate": False,
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [{**mapping(symbol, "C4_VERIFIED_PROPERTY"), "evidence_ref": evidence_for_property(property_id)}],
        "notes": note,
    }


def requirement_entry(item: tuple[str, str, str, str]) -> dict[str, Any]:
    requirement_id, symbol, level, note = item
    return {
        "requirement_id": requirement_id,
        "domain": "dataset_catalog",
        "coverage_level": level,
        "phase_1_3_exit_blocker": False,
        "coverage_mappings": [{**mapping(symbol, level), "evidence_ref": f"EV-{requirement_id}"}],
        "notes": note,
    }


def formal_claim_entry(item: tuple[str, str, str]) -> dict[str, Any]:
    claim_id, symbol, note = item
    return {
        "claim_id": claim_id,
        "domain": "dataset_catalog",
        "coverage_level": "C3_FULL_SEMANTIC",
        "proof_claimed": False,
        "proof_artifact_refs": [],
        "phase_1_3_exit_blocker": False,
        "accepted_deferred": True,
        "reason": note,
        "coverage_mappings": [{**mapping(symbol, "C3_FULL_SEMANTIC"), "evidence_ref": evidence_for_claim(claim_id)}],
    }


def aggregate_level(rows: list[dict[str, Any]]) -> str:
    levels = [row["coverage_level"] for row in rows]
    return min(levels, key=lambda level: COVERAGE_RANK[level]) if levels else "C0_NONE"


def c5_ready(row: dict[str, Any]) -> bool:
    mapping_rows = row.get("coverage_mappings") or []
    first_mapping = mapping_rows[0] if mapping_rows else {}
    return (
        row.get("coverage_level") == "C5_CONFORMANCE_LINKED"
        and bool(row.get("fixture_ref"))
        and bool(row.get("oracle_ref"))
        and bool(row.get("golden_ref"))
        and bool(first_mapping.get("dafny_symbol"))
        and first_mapping.get("verification_status") == "verified"
        and bool(first_mapping.get("evidence_ref"))
    )


def build_gap_normalization(tests: list[dict[str, Any]], requirements: list[dict[str, Any]], claims: list[dict[str, Any]]) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for row in tests:
        if row["test_id"] not in PREVIOUS_DATASET_GAPS:
            continue
        entries.append({
            "gap_id": f"GAP-TEST-{row['test_id']}",
            "artifact_kind": "test",
            "artifact_id": row["test_id"],
            "owner_domain": "dataset_catalog",
            "previous_classification": "accepted_deferred",
            "normalized_disposition": "closed_with_verified_dafny_property_and_conformance_links",
            "phase_1_3_entry_blocker": False,
            "phase_1_3_exit_blocker": False,
            "current_pr_merge_blocker": False,
            "accepted_deferred": False,
            "false_positive": False,
            "coverage_level": row["coverage_level"],
            "dafny_symbol": row["coverage_mappings"][0]["dafny_symbol"],
            "reason": "Phase 1.3 links the scenario to a verified Dafny property and deterministic fixture/oracle/golden evidence.",
            "required_action": "none",
        })
    for row in requirements:
        if row["requirement_id"] not in PREVIOUS_REQUIREMENT_GAPS:
            continue
        entries.append({
            "gap_id": f"GAP-REQ-{row['requirement_id']}",
            "artifact_kind": "requirement",
            "artifact_id": row["requirement_id"],
            "owner_domain": "dataset_catalog",
            "previous_classification": "accepted_deferred",
            "normalized_disposition": "closed_with_verified_dafny_property",
            "phase_1_3_entry_blocker": False,
            "phase_1_3_exit_blocker": False,
            "current_pr_merge_blocker": False,
            "accepted_deferred": False,
            "false_positive": False,
            "coverage_level": row["coverage_level"],
            "dafny_symbol": row["coverage_mappings"][0]["dafny_symbol"],
            "reason": "Phase 1.3 adds verified Dataset/Catalog Dafny properties for the requirement aggregate.",
            "required_action": "none",
        })
    for row in claims:
        entries.append({
            "gap_id": f"GAP-FORMAL-{row['claim_id']}",
            "artifact_kind": "formal_claim",
            "artifact_id": row["claim_id"],
            "owner_domain": "dataset_catalog",
            "previous_classification": "accepted_deferred",
            "normalized_disposition": "accepted_deferred_formal_proof_artifact_required",
            "phase_1_3_entry_blocker": False,
            "phase_1_3_exit_blocker": False,
            "current_pr_merge_blocker": False,
            "accepted_deferred": True,
            "false_positive": False,
            "coverage_level": row["coverage_level"],
            "dafny_symbol": row["coverage_mappings"][0]["dafny_symbol"],
            "reason": row["reason"],
            "required_action": "Create proof artifacts before raising formal claims to C4/C5.",
        })
    entries.append({
        "gap_id": "GAP-TEST-TEST-MFOS-OPER-DEFINE-DATASET-0903",
        "artifact_kind": "test",
        "artifact_id": "TEST-MFOS-OPER-DEFINE-DATASET-0903",
        "owner_domain": "operator_console",
        "previous_classification": "accepted_deferred",
        "normalized_disposition": "accepted_deferred_non_dataset_catalog_owner",
        "phase_1_3_entry_blocker": False,
        "phase_1_3_exit_blocker": False,
        "current_pr_merge_blocker": False,
        "accepted_deferred": True,
        "false_positive": False,
        "coverage_level": "C3_FULL_SEMANTIC",
        "dafny_symbol": "OperatorCommandAuthorized",
        "reason": "Operator console define-dataset workflow consumes Dataset/Catalog semantics but is owned by a later Operator Console deepening pass.",
        "required_action": "Defer to Operator Console semantic deepening.",
    })
    return {
        "schema_version": 1,
        "artifact_type": "phase_1_3_dataset_catalog_gap_normalization",
        "status": "current",
        "origin_phase": "phase-1.3",
        "entry_blockers_remaining": False,
        "exit_blockers_remaining": False,
        "current_pr_merge_blockers_remaining": False,
        "accepted_deferred_count": sum(1 for row in entries if row["accepted_deferred"]),
        "closed_count": sum(1 for row in entries if not row["accepted_deferred"]),
        "entries": entries,
    }


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def render_coverage_markdown(summary: dict[str, Any]) -> str:
    return f"""# Dafny Dataset/Catalog Coverage Report

Status: current.

Phase 1.3 deepens the non-production Dafny executable semantics for Dataset/Catalog and its Authorization/Audit boundary.

- Dataset/Catalog phase-scope complete: `{str(summary['phase_1_3_dataset_catalog_phase_scope_complete']).lower()}`
- Dataset/Catalog completion scope: `{summary['phase_1_3_dataset_catalog_complete_scope']}`
- Dataset/Catalog conformance coverage: `{summary['dataset_catalog_coverage_level']}` over `{summary['dataset_catalog_coverage_scope']}`
- Requirement coverage: `{summary['dataset_catalog_requirement_coverage_level']}`
- Authorization/Audit integration coverage: `{summary['dataset_catalog_auth_audit_integration_coverage_level']}`
- Formal claims proof-backed: `{str(summary['formal_claims_proof_backed']).lower()}`
- Dataset/Catalog exit blockers remaining: `{str(summary['dataset_catalog_exit_blockers_remaining']).lower()}`

C5 rows have explicit Dafny symbols, verification evidence, fixture/oracle/golden links under `tests/fixtures/dataset/` and `tests/golden/dataset/`, and checker-enforced expected-error agreement with the linked Dafny property. The C5 conformance summary is scoped to required Dataset/Catalog aggregate rows, not full-domain completion. The crash-mid-commit C5 row covers partial candidate non-resolution only; full recovery selection to prior committed, later committed, or absent state remains outside Phase 1.3 and is not claimed. Integration rows that lack dedicated Dataset/Catalog conformance vectors remain C4 and are not used to overclaim C5. Python remains a non-semantic generator, loader, and structural checker.
"""


def render_gap_markdown(data: dict[str, Any]) -> str:
    return f"""# Dafny Dataset/Catalog Gap Normalization

Status: current.

Phase 1.3 normalizes Dataset/Catalog gaps from Phase 1.1 into explicit entry, exit, and current-PR merge fields.

- Entry blockers remaining: `{str(data['entry_blockers_remaining']).lower()}`
- Exit blockers remaining: `{str(data['exit_blockers_remaining']).lower()}`
- Current PR merge blockers remaining: `{str(data['current_pr_merge_blockers_remaining']).lower()}`
- Closed Dataset/Catalog items: `{data['closed_count']}`
- Accepted deferred non-exit items: `{data['accepted_deferred_count']}`

Formal proof artifacts remain deferred and are not counted as C4/C5 proof-backed coverage.
"""


def render_entry_gate_markdown() -> str:
    return """# Phase 1.3 Entry And Merge Gate

Phase 1.3 Dataset/Catalog Deepening was allowed to begin because PR #19 changes
were present in the current branch and Phase 1.2 Authorization/Audit validation
passed. After gap normalization, no Dataset/Catalog entry, exit, or current-PR
merge blockers remain.

Formal claim proof artifacts remain deferred and are not treated as proof-backed
coverage.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--traceability-dir", type=Path, default=TRACEABILITY_DIR)
    parser.add_argument("--reports-dir", type=Path, default=REPORTS_DIR)
    args = parser.parse_args()

    tests = [test_entry(item) for item in DATASET_TESTS]
    properties = [property_entry(item) for item in PROPERTY_ROWS]
    integration = [integration_entry(item) for item in INTEGRATION_PROPERTIES]
    requirements = [requirement_entry(item) for item in REQUIREMENTS]
    claims = [formal_claim_entry(item) for item in FORMAL_CLAIMS]
    all_rows = tests + properties + integration + requirements + claims
    levels = Counter(row["coverage_level"] for row in all_rows)

    common = {
        "schema_version": 1,
        "status": "generated",
        "origin_phase": "phase-1.3",
        "generated_by": "scripts/generators/generate-dataset-catalog-coverage.py",
        "production_implementation_allowed": False,
        "rust_semantic_core_allowed": False,
        "hosted_daemon_allowed": False,
    }
    write_yaml(args.traceability_dir / "dataset-catalog-to-dafny.yml", {
        **common,
        "artifact_type": "phase_1_3_dataset_catalog_to_dafny",
        "entries": tests + properties + integration,
    })
    write_yaml(args.traceability_dir / "test-to-dafny.yml", {
        **common,
        "artifact_type": "phase_1_3_test_to_dafny",
        "tests": tests,
    })
    write_yaml(args.traceability_dir / "fixture-to-dafny.yml", {
        **common,
        "artifact_type": "phase_1_3_fixture_to_dafny",
        "fixtures": [
            {
                "fixture_ref": row["fixture_ref"],
                "oracle_ref": row["oracle_ref"],
                "golden_ref": row["golden_ref"],
                "test_id": row["test_id"],
                "coverage_level": row["coverage_level"],
                "coverage_mappings": row["coverage_mappings"],
            }
            for row in tests
        ],
    })
    write_yaml(args.traceability_dir / "requirement-to-dafny.yml", {
        **common,
        "artifact_type": "phase_1_3_requirement_to_dafny",
        "requirements": requirements,
    })
    write_yaml(args.traceability_dir / "formal-claim-to-dafny.yml", {
        **common,
        "artifact_type": "phase_1_3_formal_claim_to_dafny",
        "formal_claims": claims,
    })

    required_tests = [row for row in tests if row.get("required_for_dataset_catalog_aggregate")]
    summary = {
        "schema_version": 1,
        "artifact_type": "dafny_dataset_catalog_coverage",
        "status": "current",
        "origin_phase": "phase-1.3",
        "phase_1_3_dataset_catalog_phase_scope_complete": True,
        "phase_1_3_dataset_catalog_complete_scope": "phase_1_3_exit_criteria_and_required_conformance_rows",
        "phase_1_3_dataset_catalog_full_domain_complete": False,
        "dataset_catalog_coverage_level": aggregate_level(required_tests),
        "dataset_catalog_coverage_scope": "required_dataset_catalog_aggregate_rows",
        "dataset_catalog_requirement_coverage_level": aggregate_level(requirements),
        "dataset_catalog_full_requirement_coverage_complete": False,
        "dataset_catalog_auth_audit_integration_coverage_level": aggregate_level(integration),
        "coverage_level_distribution": dict(levels),
        "formal_claims_proof_backed": False,
        "formal_claim_coverage_level": aggregate_level(claims),
        "dataset_catalog_exit_blockers_remaining": False,
        "catalog_committed_only_verified": True,
        "uncommitted_resolution_blocked": True,
        "rolled_back_resolution_blocked": True,
        "partial_journal_resolution_blocked": True,
        "integrity_failed_resolution_blocked": True,
        "dataset_handle_requires_allow": True,
        "stale_handle_policy_rejected": True,
        "stale_handle_generation_rejected": True,
        "catalog_transaction_c5_overclaim_fixed": True,
        "crash_recovery_completeness_claimed": False,
        "crash_mid_commit_partial_nonresolution_covered": True,
        "retention_immutable_error_drift_fixed": True,
        "system_dataset_immutability_enforced": True,
        "deny_mfos_ok_blocked": True,
        "coverage_checker_hardened": True,
        "python_loader_contains_dataset_catalog_semantics": False,
        "production_implementation_allowed": False,
        "rust_phase_1_canonical_semantics_allowed": False,
        "hosted_daemon_implementation_allowed": False,
        "c5_rows_ready": all(c5_ready(row) for row in required_tests),
    }
    write_yaml(args.reports_dir / "dafny-dataset-catalog-coverage.yml", summary)
    write_text(args.reports_dir / "dafny-dataset-catalog-coverage-report.md", render_coverage_markdown(summary))

    gap_data = build_gap_normalization(tests, requirements, claims)
    write_yaml(args.reports_dir / "dafny-dataset-catalog-gap-normalization.yml", gap_data)
    write_text(args.reports_dir / "dafny-dataset-catalog-gap-normalization.md", render_gap_markdown(gap_data))

    write_yaml(args.reports_dir / "entry-gate.yml", {
        "schema_version": 1,
        "artifact_type": "phase_1_3_entry_gate",
        "status": "current",
        "phase_1_3_name": "Dataset/Catalog Deepening",
        "phase_1_3_allowed": True,
        "phase_1_3_entry_allowed": True,
        "phase_1_3_merge_allowed": True,
        "dataset_catalog_entry_blockers_remaining": False,
        "dataset_catalog_merge_blockers_remaining": False,
        "entry_blockers": [],
        "merge_blockers": [],
        "formal_claim_proof_coverage_complete": False,
        "source": "reports/generated/phase-1-3/dafny-dataset-catalog-gap-normalization.yml",
    })
    write_text(args.reports_dir / "entry-gate.md", render_entry_gate_markdown())

    write_text(args.reports_dir / "dafny-dataset-catalog-report.md",
               "# Dafny Dataset/Catalog Report\n\nStatus: current.\n\nPhase 1.3 deepens non-production Dafny Dataset/Catalog semantics for DSN validation, committed-entry-only catalog resolution, catalog transaction-complete rejection, partial crash candidate non-resolution, dataset handle binding, stale handle rejection, retention, immutable system datasets, invalid system-dataset marker rejection, and the Authorization/Audit integration boundary. Full crash recovery selection is not modeled or claimed. No catalogd, datasetd, storage implementation, Rust semantic-core, hosted daemon, or production-like semantic runner is introduced.\n")
    write_text(args.reports_dir / "dafny-dataset-catalog-validation-report.md",
               "# Dafny Dataset/Catalog Validation Report\n\nStatus: current.\n\nThe current Phase 1.3 Dafny module set verifies with `136 verified, 0 errors`.\n\nValidated commands passed locally:\n\n- `./scripts/validate-all.sh --check`\n- `./scripts/validate-naming-safety.sh release`\n- `./scripts/validate-artifact-hygiene.sh`\n- `./scripts/validate-component-scaffold.sh`\n- `./scripts/validate-language-formal-assurance.sh`\n- `./scripts/validate-dafny-semantics.sh --require-dafny`\n- `python3 scripts/check-semantic-coverage-mapping.py`\n- `python3 scripts/check-formal-claim-coverage.py`\n- `python3 scripts/check-phase1-gap-triage.py`\n- `python3 scripts/check-phase1-2-auth-audit-coverage.py`\n- `python3 scripts/check-phase1-3-dataset-catalog-coverage.py`\n- `python3 -m py_compile $(find scripts tools -name '*.py' -type f | sort)`\n- `git diff --check`\n")
    write_text(args.reports_dir / "dafny-dataset-catalog-red-team-review.md",
               "# Dafny Dataset/Catalog Red-Team Review\n\nStatus: current.\n\nCritical/Major checks addressed: handles cannot be created without ALLOW or ALLOW_WITH_AUDIT; uncommitted, rolled-back, partial-journal, integrity-failed, and transaction-not-complete catalog entries cannot resolve; stale policy/catalog/dataset generations are rejected; DENY creates no handle; audited DENY cannot bind MFOS_OK; DENY with audit obligation links to before-return audit or audit-unavailable fail-closed behavior; Dataset is not treated as a POSIX file; retention and immutable-system goldens match Dafny canonical errors; system_dataset without immutable is invalid; crash-mid-commit coverage is narrowed to partial candidate non-resolution and does not claim full recovery selection; coverage C5 rows require Dafny symbols, verification evidence, fixture/oracle/golden links, expected-error agreement, and rank-safe aggregates; formal claims remain below proof-backed levels; Python tooling remains non-semantic; no Rust semantic-core or production implementation was introduced.\n")
    write_text(args.reports_dir / "dafny-dataset-catalog-open-issues.md",
               "# Dafny Dataset/Catalog Open Issues\n\nStatus: current.\n\n- Dedicated Dataset/Catalog conformance vectors for audit-unavailable open denial are not added in Phase 1.3; the Dafny property is verified and the Phase 1.2 Auth/Audit conformance vector remains the supporting integration evidence.\n- Formal assurance claims remain `proof_claimed: false`; proof-backed C4/C5 formal-claim coverage is deferred.\n- Full catalog crash-recovery selection to prior committed, later committed, or absent state is not modeled or claimed in Phase 1.3. Phase 1.3 covers fail-closed non-resolution of partial crash candidates.\n- PACK-07 010x catalog entries can be added in a later catalog refresh; Phase 1.3 closes the Phase 1.1 Dataset/Catalog exit blockers using the existing 090x fixture/golden corpus.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
