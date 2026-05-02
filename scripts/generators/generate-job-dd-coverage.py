#!/usr/bin/env python3
"""Generate Phase 1.4.1 Job lifecycle / effective principal / DD coverage artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
TRACEABILITY_DIR = ROOT / "evidence" / "traceability" / "generated" / "phase-1-4-1"
JOB_MODULE = "formal/executable-semantics/dafny/modules/job_spool.dfy"

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


def mapping(symbol: str, level: str, evidence_ref: str) -> dict[str, Any]:
    return {
        "dafny_module": JOB_MODULE,
        "dafny_symbol": symbol,
        "symbol_kind": "lemma",
        "verification_status": "verified",
        "evidence_ref": evidence_ref,
        "coverage_level": level,
    }


def c5_test(
    test_id: str,
    slug: str,
    domain: str,
    symbol: str,
    note: str,
    negative: bool = True,
    required_fixture_fact_keys: list[str] | None = None,
) -> dict[str, Any]:
    evidence_ref = "EV-" + test_id.removeprefix("TEST-").removeprefix("NEG-")
    return {
        "test_id": test_id,
        "domain": domain,
        "test_type": "negative" if negative else "conformance",
        "coverage_level": "C5_CONFORMANCE_LINKED",
        "phase_1_4_1_exit_blocker": False,
        "required_for_phase_1_4_1_job_dd": True,
        "fixture_ref": f"tests/fixtures/job/{slug}.yml",
        "oracle_ref": f"tests/golden/job/{slug}.yml",
        "golden_ref": f"tests/golden/job/{slug}.yml",
        "coverage_mappings": [mapping(symbol, "C5_CONFORMANCE_LINKED", evidence_ref)],
        "expected_dafny_symbols": [symbol],
        "required_fixture_fact_keys": required_fixture_fact_keys or ["dafny_property", "job_state"],
        "negative_failure_conditions": [symbol] if negative else [],
        "notes": note,
    }


JOB_LIFECYCLE_TESTS = [
    c5_test(
        "TEST-MFOS-JOB-VALID-SUBMIT-READY-0928",
        "valid-submit-ready-0928",
        "job_lifecycle",
        "INV_JOB_VALID_SUBMIT_REACHES_READY",
        "Valid submit establishes the lifecycle path through VALIDATED to READY.",
        negative=False,
        required_fixture_fact_keys=["dafny_property", "submit_decision", "effective_principal", "lifecycle_path"],
    ),
    c5_test(
        "NEG-MFOS-JOB-INVALID-LIFECYCLE-0910",
        "invalid-lifecycle-0910",
        "job_lifecycle",
        "INV_JOB_INVALID_LIFECYCLE_REJECTED",
        "Invalid lifecycle transition returns a fail-closed transition result.",
        required_fixture_fact_keys=["dafny_property", "job_state", "attempted_transition"],
    ),
    c5_test(
        "NEG-MFOS-JOB-CANCELLED-CANNOT-EXECUTE-0926",
        "cancelled-cannot-execute-0926",
        "job_lifecycle",
        "INV_JOB_CANCELLED_CANNOT_EXECUTE_FURTHER",
        "Cancelled jobs cannot transition back to execution or running state.",
        required_fixture_fact_keys=["dafny_property", "job_state", "attempted_transition"],
    ),
]

EFFECTIVE_PRINCIPAL_TESTS = [
    c5_test(
        "TEST-MFOS-JOB-PRINCIPAL-BEFORE-OPEN-0904",
        "principal-before-open-0904",
        "effective_principal",
        "INV_JOB_EFFECTIVE_PRINCIPAL_BEFORE_OPEN",
        "Dataset open requires an established effective principal before a DD decision can be bound.",
        negative=False,
        required_fixture_fact_keys=["dafny_property", "job_state", "effective_principal", "dd_operation"],
    ),
    c5_test(
        "NEG-MFOS-JOB-SUBMIT-NO-PRINCIPAL-0903",
        "submit-no-principal-0903",
        "effective_principal",
        "INV_JOB_SUBMIT_NO_PRINCIPAL_FAILS_CLOSED",
        "Principal establishment failure returns no EffectivePrincipal.",
        required_fixture_fact_keys=["dafny_property", "submit_decision", "effective_principal"],
    ),
    c5_test(
        "NEG-MFOS-JOB-DATASET-OPEN-BEFORE-PRINCIPAL-0927",
        "dataset-open-before-principal-0927",
        "effective_principal",
        "INV_JOB_CONTEXT_EFFECTIVE_PRINCIPAL_BEFORE_OPEN",
        "JobContext DD resolution fails before effective principal establishment.",
        required_fixture_fact_keys=["dafny_property", "job_state", "effective_principal", "dd_operation"],
    ),
]

DD_TESTS = [
    c5_test(
        "TEST-MFOS-JOB-DD-CATALOG-RESOLUTION-0905",
        "dd-catalog-resolution-0905",
        "dd_resolution",
        "INV_JOB_DD_SUCCESS_CREATES_BOUND_DATASET_HANDLE",
        "DD resolution succeeds only through DatasetCatalog handle creation.",
        negative=False,
        required_fixture_fact_keys=["dafny_property", "job_state", "effective_principal", "catalog_state", "authorization_result", "dd_operation"],
    ),
    c5_test(
        "TEST-MFOS-JOB-DD-AUTHORIZATION-0906",
        "dd-authorization-0906",
        "dd_resolution",
        "INV_JOB_DD_RESOLUTION_THROUGH_CATALOG_AND_AUTH",
        "DD resolution requires DatasetCatalog and Authorization predicates.",
        negative=False,
        required_fixture_fact_keys=["dafny_property", "job_state", "effective_principal", "catalog_state", "authorization_result", "dd_operation"],
    ),
    c5_test(
        "NEG-MFOS-JOB-DD-CATALOG-BYPASS-DENIED-0918",
        "dd-catalog-bypass-denied-0918",
        "dd_resolution",
        "INV_JOB_DD_RESOLUTION_CANNOT_BYPASS_CATALOG",
        "DD resolution cannot bypass catalog resolution.",
        required_fixture_fact_keys=["dafny_property", "job_state", "effective_principal", "catalog_state", "authorization_result", "dd_operation"],
    ),
    c5_test(
        "NEG-MFOS-JOB-DD-AUTHORIZATION-BYPASS-DENIED-0919",
        "dd-authorization-bypass-denied-0919",
        "dd_resolution",
        "INV_JOB_DD_RESOLUTION_CANNOT_BYPASS_AUTHORIZATION",
        "DD resolution cannot bypass authorization.",
        required_fixture_fact_keys=["dafny_property", "job_state", "effective_principal", "catalog_state", "authorization_result", "dd_operation"],
    ),
    c5_test(
        "NEG-MFOS-JOB-DD-MALFORMED-DSN-0920",
        "dd-malformed-dsn-0920",
        "dd_resolution",
        "INV_JOB_DD_MALFORMED_DSN_FAILS",
        "Malformed symbolic DSN in DD resolution fails closed.",
        required_fixture_fact_keys=["dafny_property", "job_state", "effective_principal", "catalog_state", "authorization_result", "dd_operation", "dataset_name_shape"],
    ),
    c5_test(
        "NEG-MFOS-JOB-DD-CATALOG-UNCOMMITTED-0921",
        "dd-catalog-uncommitted-0921",
        "dd_resolution",
        "INV_JOB_DD_UNCOMMITTED_CATALOG_FAILS",
        "Uncommitted catalog entry cannot resolve through a job DD.",
        required_fixture_fact_keys=["dafny_property", "job_state", "effective_principal", "catalog_state", "authorization_result", "dd_operation"],
    ),
    c5_test(
        "NEG-MFOS-JOB-DD-CATALOG-ROLLED-BACK-0922",
        "dd-catalog-rolled-back-0922",
        "dd_resolution",
        "INV_JOB_DD_ROLLED_BACK_CATALOG_FAILS",
        "Rolled-back catalog entry cannot resolve through a job DD.",
        required_fixture_fact_keys=["dafny_property", "job_state", "effective_principal", "catalog_state", "authorization_result", "dd_operation"],
    ),
    c5_test(
        "NEG-MFOS-JOB-DD-CATALOG-PARTIAL-JOURNAL-0923",
        "dd-catalog-partial-journal-0923",
        "dd_resolution",
        "INV_JOB_DD_PARTIAL_JOURNAL_CATALOG_FAILS",
        "Partial-journal catalog entry cannot resolve through a job DD.",
        required_fixture_fact_keys=["dafny_property", "job_state", "effective_principal", "catalog_state", "authorization_result", "dd_operation"],
    ),
    c5_test(
        "NEG-MFOS-JOB-DD-CATALOG-INTEGRITY-FAILED-0924",
        "dd-catalog-integrity-failed-0924",
        "dd_resolution",
        "INV_JOB_DD_INTEGRITY_FAILED_CATALOG_FAILS",
        "Integrity-failed catalog entry cannot resolve through a job DD.",
        required_fixture_fact_keys=["dafny_property", "job_state", "effective_principal", "catalog_state", "authorization_result", "dd_operation"],
    ),
    c5_test(
        "NEG-MFOS-JOB-STALE-HANDLE-POLICY-0925",
        "stale-handle-policy-0925",
        "dd_resolution",
        "INV_JOB_DD_STALE_HANDLE_AFTER_POLICY_CHANGE_FAILS",
        "Stale handle after a policy version change fails in job context.",
        required_fixture_fact_keys=["dafny_property", "job_state", "effective_principal", "handle_policy_version", "active_policy_version"],
    ),
    c5_test(
        "NEG-MFOS-JOB-UNAUTHORIZED-DATASET-0908",
        "unauthorized-dataset-0908",
        "dd_resolution",
        "INV_JOB_UNAUTHORIZED_DATASET_STEP_FAILS_CLOSED",
        "Unauthorized dataset in a job step creates no DatasetHandle.",
        required_fixture_fact_keys=["dafny_property", "job_state", "effective_principal", "catalog_state", "authorization_result", "dd_operation"],
    ),
]

PROPERTY_ROWS = [
    {
        "property_id": "JOB-LIFECYCLE-CANNOT-EXECUTE-BEFORE-VALIDATION",
        "domain": "job_lifecycle",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                "INV_JOB_CANNOT_EXECUTE_BEFORE_VALIDATION",
                "C4_VERIFIED_PROPERTY",
                "reports/phases/phase-1-4/job-lifecycle-dd-resolution/validation-report.md",
            )
        ],
        "notes": "Verified Dafny property; no separate fixture vector is needed for this non-C5 property row.",
    },
    {
        "property_id": "JOB-FAILURE-RC-DETERMINISTIC",
        "domain": "job_lifecycle",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                "INV_JOB_RETURN_CODE_DETERMINISTIC",
                "C4_VERIFIED_PROPERTY",
                "reports/phases/phase-1-4/job-lifecycle-dd-resolution/validation-report.md",
            )
        ],
        "notes": "Return code placeholder is deterministic but remains symbolic and non-execution.",
    },
    {
        "property_id": "JOB-EFFECTIVE-PRINCIPAL-BINDS-POLICY",
        "domain": "effective_principal",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                "INV_JOB_EFFECTIVE_PRINCIPAL_BINDS_POLICY_AND_CORRELATION",
                "C4_VERIFIED_PROPERTY",
                "reports/phases/phase-1-4/job-lifecycle-dd-resolution/validation-report.md",
            )
        ],
        "notes": "EffectivePrincipal binds policy version and correlation id.",
    },
    {
        "property_id": "JOB-SUBMIT-AS-REQUIRES-AUTHORIZATION",
        "domain": "effective_principal",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                "INV_JOB_SUBMIT_AS_REQUIRES_AUTHORIZATION",
                "C4_VERIFIED_PROPERTY",
                "reports/phases/phase-1-4/job-lifecycle-dd-resolution/validation-report.md",
            )
        ],
        "notes": "Requested principal different from submitter requires an allowing submit-as decision.",
    },
    {
        "property_id": "DD-DENY-AUDIT-BEFORE-RETURN",
        "domain": "dd_resolution",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                "INV_JOB_DD_DENY_WITH_AUDIT_LINKS_BEFORE_RETURN",
                "C4_VERIFIED_PROPERTY",
                "reports/phases/phase-1-4/job-lifecycle-dd-resolution/validation-report.md",
            )
        ],
        "notes": "DD denial with audit obligation links to Phase 1.2 before-return audit semantics.",
    },
    {
        "property_id": "DD-DENY-AUDIT-UNAVAILABLE-FAILS-CLOSED",
        "domain": "dd_resolution",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                "INV_JOB_DD_DENY_AUDIT_UNAVAILABLE_FAILS_CLOSED",
                "C4_VERIFIED_PROPERTY",
                "reports/phases/phase-1-4/job-lifecycle-dd-resolution/validation-report.md",
            )
        ],
        "notes": "DD denial with an unavailable required audit path fails closed and releases no result.",
    },
    {
        "property_id": "DD-DENY-PRODUCES-NO-HANDLE",
        "domain": "dd_resolution",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                "INV_JOB_DD_DENY_PRODUCES_NO_HANDLE",
                "C4_VERIFIED_PROPERTY",
                "reports/phases/phase-1-4/job-lifecycle-dd-resolution/validation-report.md",
            )
        ],
        "notes": "A DENY authorization decision cannot create a DatasetHandle through DD resolution.",
    },
    {
        "property_id": "DD-UNRESOLVED-CATALOG-FAILS",
        "domain": "dd_resolution",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                "INV_JOB_DD_UNRESOLVED_CATALOG_FAILS",
                "C4_VERIFIED_PROPERTY",
                "reports/phases/phase-1-4/job-lifecycle-dd-resolution/validation-report.md",
            )
        ],
        "notes": "A DD cannot resolve through an unresolved catalog entry.",
    },
    {
        "property_id": "DD-BOUND-DECISION-REQUIRES-EFFECTIVE-CONTEXT",
        "domain": "dd_resolution",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                "INV_JOB_DD_DECISION_REQUIRES_EFFECTIVE_CONTEXT",
                "C4_VERIFIED_PROPERTY",
                "reports/phases/phase-1-4/job-lifecycle-dd-resolution/validation-report.md",
            )
        ],
        "notes": "The DD authorization witness is tied to an EffectiveJobContext rather than a raw SecurityDecision.",
    },
    {
        "property_id": "DD-BOUND-DECISION-BINDS-REQUEST-CORRELATION",
        "domain": "dd_resolution",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                "INV_JOB_DD_BOUND_DECISION_BINDS_REQUEST",
                "C4_VERIFIED_PROPERTY",
                "reports/phases/phase-1-4/job-lifecycle-dd-resolution/validation-report.md",
            )
        ],
        "notes": "Bound DD decisions carry subject, object, operation, policy version, and correlation id bindings.",
    },
    {
        "property_id": "DD-CROSS-REQUEST-AUTHORIZATION-REPLAY-BLOCKED",
        "domain": "dd_resolution",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                "INV_JOB_DD_CROSS_REQUEST_AUTHORIZATION_REPLAY_BLOCKED",
                "C4_VERIFIED_PROPERTY",
                "reports/phases/phase-1-4/job-lifecycle-dd-resolution/validation-report.md",
            )
        ],
        "notes": "A SecurityDecision with a different request correlation id cannot satisfy DD binding.",
    },
    {
        "property_id": "DD-DENY-MFOS-OK-INVALID",
        "domain": "dd_resolution",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                "INV_JOB_DD_DENY_MFOS_OK_INVALID",
                "C4_VERIFIED_PROPERTY",
                "reports/phases/phase-1-4/job-lifecycle-dd-resolution/validation-report.md",
            )
        ],
        "notes": "A DENY decision carrying MFOS_OK is not a valid deny state.",
    },
    {
        "property_id": "DD-ALLOW-DENY-STATES-DISTINGUISHABLE",
        "domain": "dd_resolution",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                "INV_JOB_DD_VALID_ALLOW_AND_DENY_DISTINGUISHABLE",
                "C4_VERIFIED_PROPERTY",
                "reports/phases/phase-1-4/job-lifecycle-dd-resolution/validation-report.md",
            )
        ],
        "notes": "Valid allow and valid deny states are disjoint Dafny predicates.",
    },
]

REQUIREMENT_ROWS = [
    {
        "requirement_id": "MFOS-REQ-JOB-0101",
        "coverage_level": "C2_PARTIAL_SEMANTIC",
        "symbol": "INV_JOB_CONTEXT_EFFECTIVE_PRINCIPAL_BEFORE_OPEN",
        "mapping_level": "C4_VERIFIED_PROPERTY",
        "partial_coverage": True,
        "covered_subclaim": "Phase 1.4.1 verifies the dataset/DD-open effective-principal precondition.",
        "not_claimed": [
            "program open authorization lifecycle",
            "spool open authorization lifecycle",
            "other protected resource open authorization lifecycle",
            "production jobd behavior",
        ],
        "notes": "Parent requirement remains partial because program, spool, other protected resources, and production jobd behavior are outside Phase 1.4.1.",
    },
    {
        "requirement_id": "MFOS-REQ-JOB-0101",
        "subclaim_id": "MFOS-REQ-JOB-0101-PHASE-1-4-1-DATASET-DD-OPEN",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "symbol": "INV_JOB_CONTEXT_EFFECTIVE_PRINCIPAL_BEFORE_OPEN",
        "mapping_level": "C4_VERIFIED_PROPERTY",
        "partial_coverage": False,
        "covered_subclaim": "Dataset/DD open from a JobContext cannot satisfy DD resolution before an effective principal exists.",
        "not_claimed": [],
        "notes": "Phase-scoped subclaim only; this does not promote the broad parent requirement to C4.",
    },
    {
        "requirement_id": "MFOS-REQ-JOB-0102",
        "coverage_level": "C2_PARTIAL_SEMANTIC",
        "symbol": "INV_JOB_DD_BOUND_DECISION_BINDS_REQUEST",
        "mapping_level": "C4_VERIFIED_PROPERTY",
        "partial_coverage": True,
        "covered_subclaim": "Phase 1.4.1 verifies DD handle creation through DatasetCatalog and Authorization semantics.",
        "not_claimed": [
            "catalogd service provenance",
            "securityd service provenance",
            "production jobd handle receipt",
        ],
        "notes": "Parent requirement remains partial because service provenance is not modeled in this non-production Dafny semantics PR.",
    },
    {
        "requirement_id": "MFOS-REQ-JOB-0102",
        "subclaim_id": "MFOS-REQ-JOB-0102-PHASE-1-4-1-DD-CATALOG-AUTH",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "symbol": "INV_JOB_DD_BOUND_DECISION_BINDS_REQUEST",
        "mapping_level": "C4_VERIFIED_PROPERTY",
        "partial_coverage": False,
        "covered_subclaim": "DD resolution requires a bound authorization decision and catalog generation before a DatasetHandle can be created.",
        "not_claimed": [],
        "notes": "Phase-scoped subclaim only; this does not model catalogd/securityd service provenance.",
    },
    {
        "requirement_id": "MFOS-REQ-JOB-0103",
        "coverage_level": "C2_PARTIAL_SEMANTIC",
        "symbol": "INV_JOB_DD_RESOLUTION_CANNOT_BYPASS_AUTHORIZATION",
        "mapping_level": "C4_VERIFIED_PROPERTY",
        "partial_coverage": True,
        "covered_subclaim": "Phase 1.4.1 verifies DD resolution cannot bypass Authorization semantics.",
        "not_claimed": [
            "securityd decision provenance",
            "jobd service-origin constraints",
            "production service interaction",
        ],
        "notes": "Parent requirement remains partial because Phase 1.4.1 does not model service provenance from securityd/jobd.",
    },
    {
        "requirement_id": "MFOS-REQ-JOB-0103",
        "subclaim_id": "MFOS-REQ-JOB-0103-PHASE-1-4-1-DD-AUTHORIZATION-BYPASS",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "symbol": "INV_JOB_DD_RESOLUTION_CANNOT_BYPASS_AUTHORIZATION",
        "mapping_level": "C4_VERIFIED_PROPERTY",
        "partial_coverage": False,
        "covered_subclaim": "DD resolution cannot create a DatasetHandle by bypassing Authorization semantics.",
        "not_claimed": [],
        "notes": "Phase-scoped subclaim only; this does not claim production securityd/jobd provenance.",
    },
]

FORMAL_CLAIMS = [
    {
        "claim_id": "MFOS-FC-AUTHORIZATION-NO-HANDLE-WITHOUT-ALLOW",
        "domain": "dd_resolution",
        "coverage_level": "C3_FULL_SEMANTIC",
        "proof_claimed": False,
        "proof_artifact_refs": [],
        "accepted_deferred": True,
        "reason": "Phase 1.4.1 links Job/DD semantics to verified Dafny lemmas, but does not add formal proof artifacts for this claim.",
        "coverage_mappings": [
            mapping(
                "INV_JOB_DD_DENY_PRODUCES_NO_HANDLE",
                "C3_FULL_SEMANTIC",
                "reports/phases/phase-1-4/job-lifecycle-dd-resolution/coverage-report.md",
            )
        ],
    }
]


def aggregate_level(rows: list[dict[str, Any]]) -> str:
    return min((row["coverage_level"] for row in rows), key=lambda level: COVERAGE_RANK[level]) if rows else "C0_NONE"


def requirement_entry(item: dict[str, Any]) -> dict[str, Any]:
    req_id = item["requirement_id"]
    symbol = item["symbol"]
    level = item["coverage_level"]
    mapping_level = item.get("mapping_level", level)
    return {
        "requirement_id": req_id,
        **({"subclaim_id": item["subclaim_id"]} if item.get("subclaim_id") else {}),
        "domain": "job_lifecycle_dd_resolution",
        "phase_scope": "phase-1-4-1",
        "partial_coverage": item.get("partial_coverage", False),
        "covered_subclaim": item.get("covered_subclaim"),
        "not_claimed": item.get("not_claimed", []),
        "coverage_level": level,
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [mapping(symbol, mapping_level, "reports/phases/phase-1-4/job-lifecycle-dd-resolution/coverage-report.md")],
        "notes": item["notes"],
    }


def write_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=False), encoding="utf-8")


def build() -> dict[str, Any]:
    tests = JOB_LIFECYCLE_TESTS + EFFECTIVE_PRINCIPAL_TESTS + DD_TESTS
    fixture_rows = [
        {
            "fixture_ref": row["fixture_ref"],
            "oracle_ref": row["oracle_ref"],
            "golden_ref": row["golden_ref"],
            "test_id": row["test_id"],
            "domain": row["domain"],
            "coverage_level": row["coverage_level"],
            "coverage_mappings": row["coverage_mappings"],
        }
        for row in tests
        if row["coverage_level"] == "C5_CONFORMANCE_LINKED"
    ]
    return {
        "job_rows": [row for row in JOB_LIFECYCLE_TESTS + PROPERTY_ROWS if row["domain"] == "job_lifecycle"],
        "principal_rows": [row for row in EFFECTIVE_PRINCIPAL_TESTS + PROPERTY_ROWS if row["domain"] == "effective_principal"],
        "dd_rows": [row for row in DD_TESTS + PROPERTY_ROWS if row["domain"] == "dd_resolution"],
        "tests": tests,
        "fixtures": fixture_rows,
        "requirements": [requirement_entry(row) for row in REQUIREMENT_ROWS],
        "formal_claims": FORMAL_CLAIMS,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--traceability-dir", type=Path, default=TRACEABILITY_DIR)
    args = parser.parse_args()
    data = build()
    trace_dir = args.traceability_dir
    write_yaml(trace_dir / "job-lifecycle-to-dafny.yml", {
        "schema_version": 1,
        "phase": "phase-1.4.1",
        "domain": "job_lifecycle",
        "coverage_level": aggregate_level(data["job_rows"]),
        "entries": data["job_rows"],
    })
    write_yaml(trace_dir / "effective-principal-to-dafny.yml", {
        "schema_version": 1,
        "phase": "phase-1.4.1",
        "domain": "effective_principal",
        "coverage_level": aggregate_level(data["principal_rows"]),
        "entries": data["principal_rows"],
    })
    write_yaml(trace_dir / "dd-resolution-to-dafny.yml", {
        "schema_version": 1,
        "phase": "phase-1.4.1",
        "domain": "dd_resolution",
        "coverage_level": aggregate_level(data["dd_rows"]),
        "entries": data["dd_rows"],
    })
    write_yaml(trace_dir / "test-to-dafny.yml", {
        "schema_version": 1,
        "phase": "phase-1.4.1",
        "tests": data["tests"],
        "coverage_level": aggregate_level(data["tests"]),
    })
    write_yaml(trace_dir / "fixture-to-dafny.yml", {
        "schema_version": 1,
        "phase": "phase-1.4.1",
        "fixtures": data["fixtures"],
        "coverage_level": aggregate_level(data["fixtures"]),
    })
    write_yaml(trace_dir / "requirement-to-dafny.yml", {
        "schema_version": 1,
        "phase": "phase-1.4.1",
        "requirements": data["requirements"],
        "coverage_level": aggregate_level(data["requirements"]),
    })
    write_yaml(trace_dir / "formal-claim-to-dafny.yml", {
        "schema_version": 1,
        "phase": "phase-1.4.1",
        "formal_claims": data["formal_claims"],
        "coverage_level": aggregate_level(data["formal_claims"]),
    })
    write_yaml(trace_dir / "coverage-summary.yml", {
        "schema_version": 1,
        "phase": "phase-1.4.1",
        "coverage_levels": {
            "job_lifecycle": aggregate_level(data["job_rows"]),
            "effective_principal": aggregate_level(data["principal_rows"]),
            "dd_resolution": aggregate_level(data["dd_rows"]),
            "required_tests": aggregate_level(data["tests"]),
            "fixtures": aggregate_level(data["fixtures"]),
            "requirements": aggregate_level(data["requirements"]),
            "formal_claims": aggregate_level(data["formal_claims"]),
        },
        "c5_scope": "required scenario and fixture rows only",
        "aggregate_c5_overclaim_remaining": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
