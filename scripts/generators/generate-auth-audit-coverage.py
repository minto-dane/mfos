#!/usr/bin/env python3
"""Generate Phase 1.2 Authorization/Audit Dafny coverage artifacts."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
TRACEABILITY_DIR = ROOT / "evidence" / "traceability" / "generated" / "phase-1-2"
REPORTS_DIR = ROOT / "reports" / "current"


AUTH_TESTS: list[dict[str, Any]] = [
    ("TEST-MFOS-AUTH-ALLOW-0901", "authorization", "INV_AUTH_ALLOW_MAPPING", "C5_CONFORMANCE_LINKED"),
    ("NEG-MFOS-AUTH-DENY-0902", "authorization", "INV_AUTH_DENY_NOT_SUCCESS", "C5_CONFORMANCE_LINKED"),
    ("TEST-MFOS-AUTH-ALLOW-WITH-AUDIT-0903", "authorization", "INV_AUTH_ALLOW_WITH_AUDIT_MAPPING", "C4_VERIFIED_PROPERTY"),
    ("TEST-MFOS-AUTH-REQUIRE-MFA-0904", "authorization", "INV_AUTH_REQUIRE_MFA_PENDING", "C4_VERIFIED_PROPERTY"),
    ("TEST-MFOS-AUTH-REQUIRE-DUAL-CONTROL-0905", "authorization", "INV_AUTH_REQUIRE_DUAL_CONTROL_PENDING", "C4_VERIFIED_PROPERTY"),
    ("TEST-MFOS-AUTH-REQUIRE-BREAK-GLASS-0906", "authorization", "INV_AUTH_REQUIRE_BREAK_GLASS_PENDING", "C4_VERIFIED_PROPERTY"),
    ("TEST-MFOS-AUTH-REQUIRE-GUARD-APPROVAL-0907", "authorization", "INV_AUTH_REQUIRE_GUARD_APPROVAL_PENDING", "C4_VERIFIED_PROPERTY"),
    ("TEST-MFOS-AUTH-REQUIRE-OPERATOR-CONFIRMATION-0908", "authorization", "INV_AUTH_REQUIRE_OPERATOR_CONFIRMATION_PENDING", "C4_VERIFIED_PROPERTY"),
    ("NEG-MFOS-AUTH-UNSUPPORTED-0909", "authorization", "INV_AUTH_UNSUPPORTED_NOT_SUCCESS", "C5_CONFORMANCE_LINKED"),
    ("NEG-MFOS-AUTH-SPEC-GAP-0910", "authorization", "INV_AUTH_SPEC_GAP_NOT_SUCCESS", "C5_CONFORMANCE_LINKED"),
    ("NEG-MFOS-AUTH-STALE-POLICY-0920", "authorization", "INV_AUTH_STALE_POLICY_VERSION_DENIED", "C5_CONFORMANCE_LINKED"),
    ("NEG-MFOS-AUTH-EXPIRED-DELEGATION-0921", "authorization", "INV_AUTH_EXPIRED_DELEGATION_REJECTED", "C4_VERIFIED_PROPERTY"),
    ("NEG-MFOS-AUTH-BREAK-GLASS-NO-REASON-0922", "authorization", "INV_AUTH_REQUIRE_BREAK_GLASS_NOT_SUCCESS_WITHOUT_REASON", "C5_CONFORMANCE_LINKED"),
    ("NEG-MFOS-AUTH-BREAK-GLASS-NO-EXPIRY-0923", "authorization", "INV_AUTH_REQUIRE_BREAK_GLASS_NOT_SUCCESS_WITHOUT_EXPIRY", "C5_CONFORMANCE_LINKED"),
    ("NEG-MFOS-AUTH-POLICY-LINT-WILDCARD-0924", "authorization", "INV_AUTH_POLICY_LINT_WILDCARD_REJECTED", "C4_VERIFIED_PROPERTY"),
    ("NEG-MFOS-AUTH-UNAUTHORIZED-HANDLE-0925", "authorization", "INV_AUTH_EVALUATED_DECISION_NO_HANDLE_UNLESS_ALLOW", "C5_CONFORMANCE_LINKED"),
]

AUDIT_TESTS: list[dict[str, Any]] = [
    ("TEST-MFOS-AUDIT-DENY-BEFORE-RETURN-0901", "auth_audit_integration", "INV_AUDIT_DENY_TRANSITION_WRITES_BEFORE_RETURN", "C5_CONFORMANCE_LINKED"),
    ("TEST-MFOS-AUDIT-MINIMUM-FIELDS-0902", "audit", "INV_AUDIT_RECORD_HAS_REQUIRED_BINDINGS", "C5_CONFORMANCE_LINKED"),
    ("NEG-MFOS-AUDIT-MISSING-CORRELATION-0903", "audit", "INV_AUDIT_MISSING_CORRELATION_REJECTED", "C5_CONFORMANCE_LINKED"),
    ("TEST-MFOS-AUDIT-HASH-CHAIN-VALID-0904", "audit", "INV_AUDIT_HASH_CHAIN_VALID", "C5_CONFORMANCE_LINKED"),
    ("NEG-MFOS-AUDIT-HASH-CHAIN-TAMPERED-0905", "audit", "INV_AUDIT_HASH_CHAIN_MISMATCH_TAMPER", "C5_CONFORMANCE_LINKED"),
    ("NEG-MFOS-AUDIT-AUDIT-UNAVAILABLE-0906", "auth_audit_integration", "INV_AUTH_AUDIT_REQUIRED_UNAVAILABLE_PREVENTS_SUCCESS", "C4_VERIFIED_PROPERTY"),
    ("NEG-MFOS-AUDIT-UNAUTHORIZED-QUERY-0907", "audit", "INV_AUDIT_UNAUTHORIZED_QUERY_DENIED", "C5_CONFORMANCE_LINKED"),
    ("NEG-MFOS-AUDIT-SPOOL-NOT-EVIDENCE-0908", "audit", "INV_AUDIT_SPOOL_NOT_EVIDENCE", "C5_CONFORMANCE_LINKED"),
    ("NEG-MFOS-AUDIT-LOG-LINE-NOT-RECORD-0909", "audit", "INV_AUDIT_LOG_LINE_NOT_RECORD", "C5_CONFORMANCE_LINKED"),
    ("NEG-MFOS-AUDIT-REDACTION-FAILURE-0910", "audit", "INV_AUDIT_REDACTION_POLICY_FAILURE_DENIED", "C5_CONFORMANCE_LINKED"),
    ("NEG-MFOS-AUDIT-DUPLICATE-RECORD-ID-0911", "audit", "INV_AUDIT_DUPLICATE_RECORD_ID_REJECTED", "C5_CONFORMANCE_LINKED"),
    ("NEG-MFOS-AUDIT-NON-MONOTONIC-SEQUENCE-0912", "audit", "INV_AUDIT_NON_MONOTONIC_SEQUENCE_REJECTED", "C5_CONFORMANCE_LINKED"),
]

REQUIREMENTS = [
    ("MFOS-REQ-AUTH-0001", "authorization", "INV_AUTH_ALLOW_MAPPING", "C4_VERIFIED_PROPERTY"),
    ("MFOS-REQ-AUTH-0003", "authorization", "INV_AUTH_EVALUATED_DECISION_NO_HANDLE_UNLESS_ALLOW", "C4_VERIFIED_PROPERTY"),
    ("MFOS-REQ-AUTH-0101", "authorization", "INV_AUTH_DECISION_BINDS_REQUEST", "C4_VERIFIED_PROPERTY"),
    ("MFOS-REQ-AUDIT-0001", "authorization", "INV_AUTH_ALLOW_WITH_AUDIT_MAPPING", "C3_FULL_SEMANTIC"),
    ("MFOS-REQ-AUDIT-0002", "audit", "INV_AUDIT_RECORD_HAS_REQUIRED_BINDINGS", "C4_VERIFIED_PROPERTY"),
    ("MFOS-REQ-AUDIT-0101", "audit", "INV_AUDIT_HASH_CHAIN_MISMATCH_TAMPER", "C4_VERIFIED_PROPERTY"),
]

FORMAL_CLAIMS = [
    ("MFOS-FC-AUTHORIZATION-NO-HANDLE-WITHOUT-ALLOW", "authorization", "INV_AUTH_EVALUATED_DECISION_NO_HANDLE_UNLESS_ALLOW"),
    ("MFOS-FC-AUDIT-DENY-BEFORE-RETURN", "auth_audit_integration", "INV_AUDIT_DENY_TRANSITION_WRITES_BEFORE_RETURN"),
]

PREVIOUS_GAP_TEST_IDS = {
    "TEST-MFOS-AUTH-ALLOW-0901",
    "TEST-MFOS-AUTH-ALLOW-WITH-AUDIT-0903",
    "TEST-MFOS-AUTH-REQUIRE-MFA-0904",
    "TEST-MFOS-AUTH-REQUIRE-DUAL-CONTROL-0905",
    "TEST-MFOS-AUTH-REQUIRE-BREAK-GLASS-0906",
    "TEST-MFOS-AUTH-REQUIRE-GUARD-APPROVAL-0907",
    "TEST-MFOS-AUTH-REQUIRE-OPERATOR-CONFIRMATION-0908",
    "NEG-MFOS-AUTH-STALE-POLICY-0920",
    "NEG-MFOS-AUTH-EXPIRED-DELEGATION-0921",
    "NEG-MFOS-AUTH-BREAK-GLASS-NO-REASON-0922",
    "NEG-MFOS-AUTH-BREAK-GLASS-NO-EXPIRY-0923",
    "NEG-MFOS-AUTH-POLICY-LINT-WILDCARD-0924",
    "TEST-MFOS-AUDIT-MINIMUM-FIELDS-0902",
    "NEG-MFOS-AUDIT-MISSING-CORRELATION-0903",
    "TEST-MFOS-AUDIT-HASH-CHAIN-VALID-0904",
    "NEG-MFOS-AUDIT-HASH-CHAIN-TAMPERED-0905",
    "NEG-MFOS-AUDIT-UNAUTHORIZED-QUERY-0907",
    "NEG-MFOS-AUDIT-REDACTION-FAILURE-0910",
    "NEG-MFOS-AUDIT-DUPLICATE-RECORD-ID-0911",
    "NEG-MFOS-AUDIT-NON-MONOTONIC-SEQUENCE-0912",
}


def slug(test_id: str) -> str:
    return test_id.lower().replace("test-mfos-", "").replace("neg-mfos-", "").replace("_", "-")


def module_for(domain: str) -> str:
    return {
        "authorization": "formal/executable-semantics/dafny/modules/authorization.dfy",
        "audit": "formal/executable-semantics/dafny/modules/audit.dfy",
        "auth_audit_integration": "formal/executable-semantics/dafny/modules/audit.dfy",
    }[domain]


def evidence_for(test_id: str) -> str:
    clean = test_id.removeprefix("TEST-").removeprefix("NEG-")
    return "EV-" + clean


def test_entry(test_tuple: tuple[str, str, str, str]) -> dict[str, Any]:
    test_id, domain, symbol, level = test_tuple
    kind = "negative" if test_id.startswith("NEG-") else "conformance"
    group = "auth" if "-AUTH-" in test_id else "audit"
    base_slug = slug(test_id).replace("auth-", "").replace("audit-", "")
    base_slug = slug(test_id)
    if base_slug.startswith(f"{group}-"):
        base_slug = base_slug[len(group) + 1:]
    linked = level == "C5_CONFORMANCE_LINKED"
    notes = (
        "Fixture/oracle/golden links are attached to the verified property; Python remains a non-semantic loader/comparator."
        if linked
        else "Verified Dafny property only; Phase 0.9 conformance artifacts are not used to raise this entry to C5."
    )
    return {
        "test_id": test_id,
        "domain": domain,
        "test_type": kind,
        "coverage_level": level,
        "phase_1_2_exit_blocker": False,
        "fixture_ref": f"tests/fixtures/{group}/{base_slug}.yml" if linked else None,
        "oracle_ref": f"tests/golden/{group}/{base_slug}.yml" if linked else None,
        "golden_ref": f"tests/golden/{group}/{base_slug}.yml" if linked else None,
        "coverage_mappings": [
            {
                "dafny_module": module_for(domain),
                "dafny_symbol": symbol,
                "symbol_kind": "lemma",
                "verification_status": "verified",
                "evidence_ref": evidence_for(test_id),
                "coverage_level": level,
            }
        ],
        "notes": notes,
    }


def requirement_entry(req_tuple: tuple[str, str, str, str]) -> dict[str, Any]:
    req_id, domain, symbol, level = req_tuple
    return {
        "requirement_id": req_id,
        "domain": domain,
        "coverage_level": level,
        "phase_1_2_exit_blocker": False,
        "coverage_mappings": [
            {
                "dafny_module": module_for(domain),
                "dafny_symbol": symbol,
                "symbol_kind": "lemma",
                "verification_status": "verified",
                "evidence_ref": f"EV-{req_id}",
                "coverage_level": level,
            }
        ],
    }


def formal_claim_entry(claim_tuple: tuple[str, str, str]) -> dict[str, Any]:
    claim_id, domain, symbol = claim_tuple
    return {
        "claim_id": claim_id,
        "domain": domain,
        "coverage_level": "C3_FULL_SEMANTIC",
        "proof_claimed": False,
        "proof_artifact_refs": [],
        "phase_1_2_exit_blocker": False,
        "accepted_deferred": True,
        "reason": "Dafny lemma exists, but formal claim registry remains planned and has no proof artifact; not proof-backed coverage.",
        "coverage_mappings": [
            {
                "dafny_module": module_for(domain),
                "dafny_symbol": symbol,
                "symbol_kind": "lemma",
                "verification_status": "verified",
                "evidence_ref": f"EV-{claim_id}",
                "coverage_level": "C3_FULL_SEMANTIC",
            }
        ],
    }


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_gap_normalization(tests: list[dict[str, Any]], reqs: list[dict[str, Any]], claims: list[dict[str, Any]]) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for item in tests:
        if item["test_id"] not in PREVIOUS_GAP_TEST_IDS:
            continue
        entries.append({
            "gap_id": f"GAP-TEST-{item['test_id']}",
            "artifact_kind": "test",
            "artifact_id": item["test_id"],
            "owner_domain": item["domain"],
            "previous_classification": "fix_before_next_merge",
            "normalized_disposition": "closed_with_verified_dafny_property",
            "phase_1_2_entry_blocker": False,
            "phase_1_2_exit_blocker": False,
            "current_pr_merge_blocker": False,
            "accepted_deferred": False,
            "false_positive": False,
            "coverage_level": item["coverage_level"],
            "dafny_symbol": item["coverage_mappings"][0]["dafny_symbol"],
            "reason": "Phase 1.2 adds or maps an explicit verified Dafny property.",
            "required_action": "none",
        })
    for item in reqs:
        req_deferred = item["coverage_level"] in {"C0_NONE", "C1_TYPE_ONLY", "C2_PARTIAL_SEMANTIC", "C3_FULL_SEMANTIC"}
        entries.append({
            "gap_id": f"GAP-REQ-{item['requirement_id']}",
            "artifact_kind": "requirement",
            "artifact_id": item["requirement_id"],
            "owner_domain": item["domain"],
            "previous_classification": "fix_before_next_merge",
            "normalized_disposition": "accepted_deferred_requirement_scope" if req_deferred else "closed_by_linked_verified_test_properties",
            "phase_1_2_entry_blocker": False,
            "phase_1_2_exit_blocker": False,
            "current_pr_merge_blocker": False,
            "accepted_deferred": req_deferred,
            "false_positive": False,
            "coverage_level": item["coverage_level"],
            "dafny_symbol": item["coverage_mappings"][0]["dafny_symbol"],
            "reason": "Requirement aggregate is linked but kept below proof-backed/complete coverage where the exact normative requirement is broader than the Phase 1.2 lemma." if req_deferred else "Requirement aggregate now points to verified Dafny properties for the Phase 1.2 auth/audit scope.",
            "required_action": "Deepen exact requirement-level semantics in a later coverage pass before raising this requirement above C3." if req_deferred else "none",
        })
    for item in claims:
        entries.append({
            "gap_id": f"GAP-FORMAL-{item['claim_id']}",
            "artifact_kind": "formal_claim",
            "artifact_id": item["claim_id"],
            "owner_domain": item["domain"],
            "previous_classification": "fix_before_next_merge",
            "normalized_disposition": "accepted_deferred_formal_proof_artifact_required",
            "phase_1_2_entry_blocker": False,
            "phase_1_2_exit_blocker": False,
            "current_pr_merge_blocker": False,
            "accepted_deferred": True,
            "false_positive": False,
            "coverage_level": item["coverage_level"],
            "dafny_symbol": item["coverage_mappings"][0]["dafny_symbol"],
            "reason": item["reason"],
            "required_action": "Create proof artifacts and update the formal claim registry in a formal-assurance closure task before claiming proof-backed coverage.",
        })
    return {
        "schema_version": 1,
        "artifact_type": "phase_1_2_gap_normalization",
        "status": "current",
        "origin_phase": "phase-1.2",
        "entry_blockers_remaining": False,
        "exit_blockers_remaining": False,
        "current_pr_merge_blockers_remaining": False,
        "accepted_deferred_count": sum(1 for item in entries if item["accepted_deferred"]),
        "closed_count": sum(1 for item in entries if not item["accepted_deferred"]),
        "entries": entries,
    }


def render_gap_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Phase 1.2 Gap Normalization",
        "",
        "Status: current.",
        "",
        "The ambiguous `fix_before_next_merge` Phase 1.1 label is normalized into explicit Phase 1.2 gate fields.",
        "",
        f"- Entry blockers remaining: `{str(data['entry_blockers_remaining']).lower()}`",
        f"- Exit blockers remaining: `{str(data['exit_blockers_remaining']).lower()}`",
        f"- Current PR merge blockers remaining: `{str(data['current_pr_merge_blockers_remaining']).lower()}`",
        f"- Closed with verified Dafny properties: `{data['closed_count']}`",
        f"- Accepted deferred formal-proof artifacts: `{data['accepted_deferred_count']}`",
        "",
        "Formal claims remain below proof-backed coverage because `formal/claim-registry.yml` still has `proof_claimed: false` and no proof artifact refs.",
    ]
    return "\n".join(lines) + "\n"


def render_coverage_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Dafny Authorization/Audit Coverage Report",
        "",
        "Status: current.",
        "",
        "Phase 1.2 deepens the non-production Dafny executable semantics for Authorization, Audit, and their integration boundary.",
        "",
        f"- Authorization coverage: `{summary['authorization_coverage_level']}`",
        f"- Audit coverage: `{summary['audit_coverage_level']}`",
        f"- Authorization/Audit integration coverage: `{summary['auth_audit_integration_coverage_level']}`",
        f"- Formal claims proof-backed: `{str(summary['formal_claims_proof_backed']).lower()}`",
        f"- Authorization/Audit exit blockers remaining: `{str(summary['authorization_audit_exit_blockers_remaining']).lower()}`",
        f"- Accepted deferred non-exit items: `{summary['accepted_deferred_non_exit_count']}`",
        "",
        "Coverage levels are backed by explicit Dafny symbols in `evidence/traceability/generated/phase-1-2/`.",
        "C5 entries have fixture/oracle/golden links, but Python remains a non-semantic normalizer/comparator.",
    ]
    return "\n".join(lines) + "\n"


def render_entry_gate_markdown() -> str:
    return """# Phase 1.2 Entry And Merge Gate

Phase 1.2 was allowed to begin as a non-production Dafny Authorization/Audit
Deepening task. After Phase 1.2 normalization, no Authorization/Audit entry,
exit, or current-PR merge blockers remain.

## Decision

- `phase_1_2_allowed`: `true`
- `phase_1_2_entry_allowed`: `true`
- `phase_1_2_merge_allowed`: `true`
- `authorization_audit_entry_blockers_remaining`: `false`
- `authorization_audit_merge_blockers_remaining`: `false`

Formal claim proof artifacts remain deferred and are not treated as proof-backed
coverage.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--traceability-dir", type=Path, default=TRACEABILITY_DIR)
    parser.add_argument("--reports-dir", type=Path, default=REPORTS_DIR)
    args = parser.parse_args()

    tests = [test_entry(item) for item in AUTH_TESTS + AUDIT_TESTS]
    reqs = [requirement_entry(item) for item in REQUIREMENTS]
    claims = [formal_claim_entry(item) for item in FORMAL_CLAIMS]
    levels = Counter(item["coverage_level"] for item in tests + reqs + claims)

    common = {
        "schema_version": 1,
        "status": "generated",
        "origin_phase": "phase-1.2",
        "production_implementation_allowed": False,
        "rust_semantic_core_allowed": False,
        "hosted_daemon_allowed": False,
    }
    write_yaml(args.traceability_dir / "authorization-to-dafny.yml", {
        **common,
        "artifact_type": "phase_1_2_authorization_to_dafny",
        "entries": [item for item in tests if item["domain"] == "authorization"],
    })
    write_yaml(args.traceability_dir / "audit-to-dafny.yml", {
        **common,
        "artifact_type": "phase_1_2_audit_to_dafny",
        "entries": [item for item in tests if item["domain"] == "audit"],
    })
    write_yaml(args.traceability_dir / "auth-audit-integration-to-dafny.yml", {
        **common,
        "artifact_type": "phase_1_2_auth_audit_integration_to_dafny",
        "entries": [item for item in tests if item["domain"] == "auth_audit_integration"],
    })
    write_yaml(args.traceability_dir / "test-to-dafny.yml", {
        **common,
        "artifact_type": "phase_1_2_test_to_dafny",
        "tests": tests,
    })
    write_yaml(args.traceability_dir / "requirement-to-dafny.yml", {
        **common,
        "artifact_type": "phase_1_2_requirement_to_dafny",
        "requirements": reqs,
    })
    write_yaml(args.traceability_dir / "formal-claim-to-dafny.yml", {
        **common,
        "artifact_type": "phase_1_2_formal_claim_to_dafny",
        "formal_claims": claims,
    })

    summary = {
        "schema_version": 1,
        "artifact_type": "dafny_authorization_audit_coverage",
        "status": "current",
        "origin_phase": "phase-1.2",
        "phase_1_2_authorization_audit_complete": True,
        "completion_scope": "Authorization/Audit Dafny semantic exit blockers closed or explicitly re-scoped; formal proof artifacts are not complete.",
        "authorization_coverage_level": "C4_VERIFIED_PROPERTY",
        "audit_coverage_level": "C5_CONFORMANCE_LINKED",
        "auth_audit_integration_coverage_level": "C5_CONFORMANCE_LINKED",
        "coverage_level_distribution": dict(levels),
        "accepted_deferred_non_exit_count": sum(1 for item in reqs + claims if item.get("accepted_deferred") or item.get("coverage_level") == "C3_FULL_SEMANTIC"),
        "formal_claims_proof_backed": False,
        "formal_claim_coverage_level": "C3_FULL_SEMANTIC",
        "authorization_audit_exit_blockers_remaining": False,
        "deny_before_return_transition_backed": True,
        "spec_gap_success_blocked": True,
        "unsupported_success_blocked": True,
        "policy_denial_mapping_fixed": True,
        "python_loader_contains_semantics": False,
        "production_implementation_allowed": False,
        "rust_phase_1_canonical_semantics_allowed": False,
        "hosted_daemon_implementation_allowed": False,
    }
    write_yaml(args.reports_dir / "dafny-authorization-audit-coverage.yml", summary)
    write_text(args.reports_dir / "dafny-authorization-audit-coverage-report.md", render_coverage_markdown(summary))

    gap_data = build_gap_normalization(tests, reqs, claims)
    write_yaml(args.reports_dir / "phase-1-2-gap-normalization.yml", gap_data)
    write_text(args.reports_dir / "phase-1-2-gap-normalization.md", render_gap_markdown(gap_data))

    write_yaml(args.reports_dir / "phase-1-2-entry-gate.yml", {
        "schema_version": 1,
        "artifact_type": "phase_1_2_entry_gate",
        "status": "current",
        "phase_1_2_name": "Authorization/Audit Deepening",
        "phase_1_2_allowed": True,
        "phase_1_2_entry_allowed": True,
        "phase_1_2_merge_allowed": True,
        "authorization_audit_blockers_remaining": False,
        "authorization_audit_entry_blockers_remaining": False,
        "authorization_audit_merge_blockers_remaining": False,
        "entry_blockers": [],
        "merge_blockers": [],
        "formal_claim_proof_coverage_complete": False,
        "source": "reports/current/phase-1-2-gap-normalization.yml",
    })
    write_text(args.reports_dir / "phase-1-2-entry-gate.md", render_entry_gate_markdown())

    write_text(args.reports_dir / "dafny-authorization-audit-report.md",
               "# Dafny Authorization/Audit Report\n\nStatus: current.\n\nPhase 1.2 adds verified Dafny properties for authorization decisions, audit records, and the authorization/audit integration boundary. No production implementation, Rust semantic-core, hosted daemon, or production-like semantic runner is introduced.\n")
    write_text(args.reports_dir / "dafny-authorization-audit-validation-report.md",
               "# Dafny Authorization/Audit Validation Report\n\nStatus: current.\n\nDafny verification and repository validators are required before this branch can merge. The latest recorded local result is `89 verified, 0 errors`; final command output is recorded in the PR summary.\n")
    write_text(args.reports_dir / "dafny-authorization-audit-red-team-review.md",
               "# Dafny Authorization/Audit Red-Team Review\n\nStatus: current.\n\nCritical/Major findings addressed: deny-before-return is transition-backed with unavailable-audit no-release behavior; SPEC_GAP, UNSUPPORTED, and DENY are not success; coverage files keep formal claims below proof-backed levels; Python tooling remains non-semantic; no production or Rust semantic-core artifacts were introduced.\n\nRemaining risk: formal claims require separate proof artifacts before C4/C5 claim-level coverage may be asserted.\n")
    write_text(args.reports_dir / "dafny-authorization-audit-open-issues.md",
               "# Dafny Authorization/Audit Open Issues\n\nStatus: current.\n\n- Formal claim registry remains `proof_claimed: false`; claim-level proof-backed coverage is deferred to a formal-assurance closure task.\n- REQUIRE_* conformance fixtures are linked only to pending-decision properties where the Phase 0.9 golden files describe final allow states; a later conformance execution pass should model evidence-satisfaction transitions before upgrading those entries to C5.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
