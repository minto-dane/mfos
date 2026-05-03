#!/usr/bin/env python3
"""Generate Phase 1.4.2 Spool protected-resource coverage artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
TRACEABILITY_DIR = ROOT / "evidence" / "traceability" / "generated" / "phase-1-4-2"
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
    symbol: str,
    note: str,
    negative: bool = True,
    required_fixture_fact_keys: list[str] | None = None,
) -> dict[str, Any]:
    evidence_ref = "EV-" + test_id.removeprefix("TEST-").removeprefix("NEG-")
    return {
        "test_id": test_id,
        "domain": "spool_protected_resource",
        "test_type": "negative" if negative else "conformance",
        "coverage_level": "C5_CONFORMANCE_LINKED",
        "phase_1_4_2_exit_blocker": False,
        "required_for_phase_1_4_2_spool": True,
        "fixture_ref": f"tests/fixtures/job/{slug}.yml",
        "oracle_ref": f"tests/golden/job/{slug}.yml",
        "golden_ref": f"tests/golden/job/{slug}.yml",
        "coverage_mappings": [mapping(symbol, "C5_CONFORMANCE_LINKED", evidence_ref)],
        "expected_dafny_symbols": [symbol],
        "required_fixture_fact_keys": required_fixture_fact_keys or [
            "dafny_property",
            "spool_operation",
            "authorization_result",
        ],
        "negative_failure_conditions": [symbol] if negative else [],
        "notes": note,
    }


SPOOL_TESTS = [
    c5_test(
        "TEST-MFOS-JOB-SPOOL-BROWSE-OWNER-0912",
        "spool-browse-owner-0912",
        "INV_SPOOL_OWNER_BROWSE_ALLOWED",
        "Spool owner browse can release content only through a bound allowing Spool decision.",
        negative=False,
        required_fixture_fact_keys=[
            "dafny_property",
            "spool_operation",
            "owner_principal",
            "subject_principal",
            "authorization_result",
            "content_released",
        ],
    ),
    c5_test(
        "NEG-MFOS-JOB-SPOOL-BROWSE-NONOWNER-0913",
        "spool-browse-nonowner-0913",
        "INV_SPOOL_BROWSE_BY_NON_OWNER_RETURNS_NO_CONTENT",
        "Non-owner browse without an allowing authorization releases no spool content.",
        required_fixture_fact_keys=[
            "dafny_property",
            "spool_operation",
            "owner_principal",
            "subject_principal",
            "authorization_result",
            "content_released",
            "audit_before_return",
        ],
    ),
    c5_test(
        "NEG-MFOS-JOB-SPOOL-PURGE-DENIED-0914",
        "spool-purge-denied-0914",
        "INV_SPOOL_PURGE_WITHOUT_AUTHORITY_DENIED",
        "Spool purge without an allowing authorization is fail-closed.",
        required_fixture_fact_keys=[
            "dafny_property",
            "spool_operation",
            "authorization_result",
            "purge_completed",
        ],
    ),
    c5_test(
        "NEG-MFOS-JOB-SPOOL-EXPORT-NO-AUDIT-0915",
        "spool-export-no-audit-0915",
        "INV_SPOOL_EXPORT_AUDIT_UNAVAILABLE_FAILS_CLOSED",
        "Spool export with required audit unavailable fails closed and releases no export.",
        required_fixture_fact_keys=[
            "dafny_property",
            "spool_operation",
            "authorization_result",
            "audit_required",
            "audit_available",
            "export_completed",
        ],
    ),
    c5_test(
        "NEG-MFOS-JOB-SPOOL-DENY-AUDIT-0920",
        "spool-deny-audit-0920",
        "INV_SPOOL_DENY_WITH_AUDIT_LINKS_BEFORE_RETURN",
        "Spool DENY with an audit obligation links to before-return audit evidence.",
        required_fixture_fact_keys=[
            "dafny_property",
            "spool_operation",
            "authorization_result",
            "audit_required",
            "audit_before_return",
            "content_released",
        ],
    ),
    c5_test(
        "NEG-MFOS-JOB-SPOOL-EVIDENCE-NOT-AUDIT-0916",
        "spool-evidence-not-audit-0916",
        "INV_SPOOL_EVIDENCE_NOT_AUDIT_EVIDENCE",
        "Spool evidence is distinct from AuditEvidence and cannot satisfy audit evidence.",
        required_fixture_fact_keys=[
            "dafny_property",
            "spool_operation",
            "spool_evidence_present",
            "audit_evidence_present",
            "audit_satisfied_by_spool_evidence",
        ],
    ),
    c5_test(
        "NEG-MFOS-JOB-SPOOL-CROSS-REQUEST-REPLAY-0917",
        "spool-cross-request-replay-0917",
        "INV_SPOOL_CROSS_REQUEST_AUTHORIZATION_REPLAY_BLOCKED",
        "A Spool authorization decision from another correlation id cannot satisfy the bound witness.",
        required_fixture_fact_keys=[
            "dafny_property",
            "spool_operation",
            "context_correlation_id",
            "decision_correlation_id",
            "authorization_result",
        ],
    ),
    c5_test(
        "NEG-MFOS-JOB-SPOOL-SPEC-GAP-NOT-SUCCESS-0918",
        "spool-spec-gap-not-success-0918",
        "INV_SPOOL_SPEC_GAP_NOT_SUCCESS",
        "SPEC_GAP is not a successful Spool access decision.",
        required_fixture_fact_keys=[
            "dafny_property",
            "spool_operation",
            "authorization_result",
            "access_success",
        ],
    ),
    c5_test(
        "NEG-MFOS-JOB-SPOOL-UNSUPPORTED-FAILS-0919",
        "spool-unsupported-fails-0919",
        "INV_SPOOL_UNSUPPORTED_NOT_SUCCESS",
        "UNSUPPORTED is not a successful Spool access decision.",
        required_fixture_fact_keys=[
            "dafny_property",
            "spool_operation",
            "authorization_result",
            "access_success",
        ],
    ),
]

PROPERTY_ROWS = [
    {
        "property_id": "SPOOL-ENTRY-PROTECTED-RESOURCE",
        "domain": "spool_protected_resource",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                "INV_SPOOL_PROTECTED_RESOURCE",
                "C4_VERIFIED_PROPERTY",
                "reports/phases/phase-1-4/spool-protected-resource/validation-report.md",
            )
        ],
        "notes": "Verified Dafny property for protected SpoolEntry identity and ownership.",
    },
    {
        "property_id": "SPOOL-DECISION-BINDS-REQUEST",
        "domain": "spool_protected_resource",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                "INV_SPOOL_DECISION_BINDS_ENTRY",
                "C4_VERIFIED_PROPERTY",
                "reports/phases/phase-1-4/spool-protected-resource/validation-report.md",
            )
        ],
        "notes": "BoundSpoolDecision binds subject, object, operation, policy version, and correlation id.",
    },
    {
        "property_id": "SPOOL-BROWSE-CANNOT-BYPASS-AUTHORIZATION",
        "domain": "spool_protected_resource",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                "INV_SPOOL_BROWSE_CANNOT_BYPASS_AUTHORIZATION",
                "C4_VERIFIED_PROPERTY",
                "reports/phases/phase-1-4/spool-protected-resource/validation-report.md",
            )
        ],
        "notes": "Browse content release depends on Authorization.DecisionAllowsProtectedEffect.",
    },
    {
        "property_id": "SPOOL-PURGE-REQUIRES-AUTHORITY",
        "domain": "spool_protected_resource",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                "INV_SPOOL_PURGE_REQUIRES_AUTHORITY_AND_RETENTION",
                "C4_VERIFIED_PROPERTY",
                "reports/phases/phase-1-4/spool-protected-resource/validation-report.md",
            )
        ],
        "notes": "Purge cannot complete without authority and non-retained entry state.",
    },
    {
        "property_id": "SPOOL-EXPORT-REQUIRES-AUDIT",
        "domain": "spool_protected_resource",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                "INV_SPOOL_EXPORT_REQUIRES_AUTHORITY_AND_AUDIT",
                "C4_VERIFIED_PROPERTY",
                "reports/phases/phase-1-4/spool-protected-resource/validation-report.md",
            )
        ],
        "notes": "Export success requires authority and satisfied audit obligation.",
    },
    {
        "property_id": "SPOOL-DENY-PRODUCES-NO-SUCCESS",
        "domain": "spool_protected_resource",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                "INV_SPOOL_DENY_PRODUCES_NO_SUCCESSFUL_ACCESS",
                "C4_VERIFIED_PROPERTY",
                "reports/phases/phase-1-4/spool-protected-resource/validation-report.md",
            )
        ],
        "notes": "A DENY decision cannot release browse, purge, or export success.",
    },
    {
        "property_id": "SPOOL-DENY-AUDIT-UNAVAILABLE-FAILS-CLOSED",
        "domain": "spool_protected_resource",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                "INV_SPOOL_DENY_AUDIT_UNAVAILABLE_FAILS_CLOSED",
                "C4_VERIFIED_PROPERTY",
                "reports/phases/phase-1-4/spool-protected-resource/validation-report.md",
            )
        ],
        "notes": "DENY with required audit fails closed when audit is unavailable.",
    },
    {
        "property_id": "SPOOL-DIAGNOSTIC-LOG-NOT-AUDIT",
        "domain": "spool_protected_resource",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                "INV_SPOOL_DIAGNOSTIC_LOG_LINE_NOT_AUDIT_EVIDENCE",
                "C4_VERIFIED_PROPERTY",
                "reports/phases/phase-1-4/spool-protected-resource/validation-report.md",
            )
        ],
        "notes": "Diagnostic log lines remain distinct from AuditEvidence.",
    },
]

REQUIREMENT_ROWS = [
    {
        "requirement_id": "MFOS-REQ-SPOOL-0101",
        "coverage_level": "C2_PARTIAL_SEMANTIC",
        "symbol": "INV_SPOOL_PROTECTED_RESOURCE",
        "mapping_level": "C4_VERIFIED_PROPERTY",
        "partial_coverage": True,
        "covered_subclaim": "Phase 1.4.2 verifies symbolic SpoolEntry protected-resource access semantics.",
        "not_claimed": [
            "production spoold behavior",
            "real spool storage",
            "operator command integration",
            "SYSOUT device semantics",
        ],
        "notes": "Parent requirement remains partial because production spool service behavior is outside Phase 1.4.2.",
    },
    {
        "requirement_id": "MFOS-REQ-SPOOL-0101",
        "subclaim_id": "MFOS-REQ-SPOOL-0101-PHASE-1-4-2-PROTECTED-RESOURCE",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "symbol": "INV_SPOOL_PROTECTED_RESOURCE",
        "mapping_level": "C4_VERIFIED_PROPERTY",
        "partial_coverage": False,
        "covered_subclaim": "SpoolEntry is a protected resource with valid symbolic id and owner.",
        "not_claimed": [],
        "notes": "Phase-scoped subclaim only; this does not promote production spoold behavior.",
    },
    {
        "requirement_id": "MFOS-REQ-SPOOL-0101",
        "subclaim_id": "MFOS-REQ-SPOOL-0101-PHASE-1-4-2-BOUND-DECISION",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "symbol": "INV_SPOOL_DECISION_BINDS_ENTRY",
        "mapping_level": "C4_VERIFIED_PROPERTY",
        "partial_coverage": False,
        "covered_subclaim": "Spool access decisions bind subject, object, operation, policy version, and correlation id.",
        "not_claimed": [],
        "notes": "Phase-scoped subclaim only.",
    },
    {
        "requirement_id": "MFOS-REQ-SPOOL-0101",
        "subclaim_id": "MFOS-REQ-SPOOL-0101-PHASE-1-4-2-AUDITED-EXPORT",
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "symbol": "INV_SPOOL_EXPORT_REQUIRES_AUTHORITY_AND_AUDIT",
        "mapping_level": "C4_VERIFIED_PROPERTY",
        "partial_coverage": False,
        "covered_subclaim": "Spool export requires authorization and satisfied audit obligation.",
        "not_claimed": [],
        "notes": "Phase-scoped subclaim only.",
    },
]

FORMAL_CLAIMS = [
    {
        "claim_id": "MFOS-FC-SPOOL-PROTECTED-RESOURCE",
        "domain": "spool_protected_resource",
        "coverage_level": "C3_FULL_SEMANTIC",
        "proof_claimed": False,
        "proof_artifact_refs": [],
        "accepted_deferred": True,
        "reason": "Phase 1.4.2 adds verified Dafny properties and conformance links, but does not add separate formal proof artifacts.",
        "coverage_mappings": [
            mapping(
                "INV_SPOOL_DECISION_BINDS_ENTRY",
                "C3_FULL_SEMANTIC",
                "reports/phases/phase-1-4/spool-protected-resource/coverage-report.md",
            )
        ],
    }
]


def aggregate_level(rows: list[dict[str, Any]]) -> str:
    return min((row["coverage_level"] for row in rows), key=lambda level: COVERAGE_RANK[level]) if rows else "C0_NONE"


def requirement_entry(item: dict[str, Any]) -> dict[str, Any]:
    level = item["coverage_level"]
    mapping_level = item.get("mapping_level", level)
    return {
        "requirement_id": item["requirement_id"],
        **({"subclaim_id": item["subclaim_id"]} if item.get("subclaim_id") else {}),
        "domain": "spool_protected_resource",
        "phase_scope": "phase-1-4-2",
        "partial_coverage": item.get("partial_coverage", False),
        "covered_subclaim": item.get("covered_subclaim"),
        "not_claimed": item.get("not_claimed", []),
        "coverage_level": level,
        "fixture_ref": None,
        "oracle_ref": None,
        "golden_ref": None,
        "coverage_mappings": [
            mapping(
                item["symbol"],
                mapping_level,
                "reports/phases/phase-1-4/spool-protected-resource/coverage-report.md",
            )
        ],
        "notes": item["notes"],
    }


def write_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=False), encoding="utf-8")


def build() -> dict[str, Any]:
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
        for row in SPOOL_TESTS
    ]
    return {
        "spool_rows": SPOOL_TESTS + PROPERTY_ROWS,
        "tests": SPOOL_TESTS,
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
    write_yaml(trace_dir / "spool-access-to-dafny.yml", {
        "schema_version": 1,
        "phase": "phase-1.4.2",
        "domain": "spool_protected_resource",
        "coverage_level": aggregate_level(data["spool_rows"]),
        "entries": data["spool_rows"],
    })
    write_yaml(trace_dir / "test-to-dafny.yml", {
        "schema_version": 1,
        "phase": "phase-1.4.2",
        "tests": data["tests"],
        "coverage_level": aggregate_level(data["tests"]),
    })
    write_yaml(trace_dir / "fixture-to-dafny.yml", {
        "schema_version": 1,
        "phase": "phase-1.4.2",
        "fixtures": data["fixtures"],
        "coverage_level": aggregate_level(data["fixtures"]),
    })
    write_yaml(trace_dir / "requirement-to-dafny.yml", {
        "schema_version": 1,
        "phase": "phase-1.4.2",
        "requirements": data["requirements"],
        "coverage_level": aggregate_level(data["requirements"]),
    })
    write_yaml(trace_dir / "formal-claim-to-dafny.yml", {
        "schema_version": 1,
        "phase": "phase-1.4.2",
        "formal_claims": data["formal_claims"],
        "coverage_level": aggregate_level(data["formal_claims"]),
    })
    write_yaml(trace_dir / "coverage-summary.yml", {
        "schema_version": 1,
        "phase": "phase-1.4.2",
        "coverage_levels": {
            "spool_protected_resource": aggregate_level(data["spool_rows"]),
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
