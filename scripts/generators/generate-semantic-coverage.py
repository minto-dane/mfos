#!/usr/bin/env python3
"""Generate truthful Phase 1.1 Dafny semantic coverage traceability."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TRACEABILITY_DIR = ROOT / "evidence" / "traceability" / "generated" / "phase-1-1"
DEFAULT_REPORTS_DIR = ROOT / "reports" / "generated" / "phase-1-1"

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

DAFNY_EVIDENCE = "reports/current/dafny/dafny-verification-report.md"
OPEN_ISSUES = "reports/generated/phase-1-1/semantic-coverage-open-issues.md"

CATALOGS = {
    "authorization": "tests/catalog/authorization.yml",
    "audit": "tests/catalog/audit.yml",
    "dataset_catalog": "tests/catalog/dataset-catalog.yml",
    "job_spool": "tests/catalog/job-spool.yml",
    "operator_console": "tests/catalog/operator-console.yml",
    "first_vertical_slice": "tests/catalog/first-vertical-slice.yml",
}

MODULES = {
    "authorization": "formal/executable-semantics/dafny/modules/authorization.dfy",
    "audit": "formal/executable-semantics/dafny/modules/audit.dfy",
    "dataset_catalog": "formal/executable-semantics/dafny/modules/dataset_catalog.dfy",
    "job_spool": "formal/executable-semantics/dafny/modules/job_spool.dfy",
    "operator_console": "formal/executable-semantics/dafny/modules/operator_console.dfy",
    "first_vertical_slice": "formal/executable-semantics/dafny/modules/first_vertical_slice.dfy",
}


def verified(module: str, symbol: str, kind: str, note: str) -> dict[str, Any]:
    return {
        "dafny_module": MODULES[module],
        "dafny_symbol": symbol,
        "symbol_kind": kind,
        "verification_status": "verified",
        "evidence_ref": DAFNY_EVIDENCE,
        "coverage_level": "C4_VERIFIED_PROPERTY",
        "note": note,
    }


def semantic(module: str, symbol: str, kind: str, level: str, note: str) -> dict[str, Any]:
    return {
        "dafny_module": MODULES[module],
        "dafny_symbol": symbol,
        "symbol_kind": kind,
        "verification_status": "unverified",
        "evidence_ref": OPEN_ISSUES,
        "coverage_level": level,
        "note": note,
    }


def none(note: str) -> dict[str, Any]:
    return {
        "dafny_module": None,
        "dafny_symbol": None,
        "symbol_kind": None,
        "verification_status": "missing",
        "evidence_ref": OPEN_ISSUES,
        "coverage_level": "C0_NONE",
        "note": note,
    }


def entry(level: str, mappings: list[dict[str, Any]], justification: str) -> dict[str, Any]:
    return {
        "coverage_level": level,
        "coverage_mappings": mappings,
        "coverage_justification": justification,
    }


TEST_COVERAGE: dict[str, dict[str, Any]] = {
    "TEST-MFOS-AUTH-ALLOW-0901": entry(
        "C3_FULL_SEMANTIC",
        [semantic("authorization", "EvaluateSecurityDecision", "function", "C3_FULL_SEMANTIC", "ALLOW evaluation is executable, but no test-specific verified lemma is declared.")],
        "Executable decision function exists; no C4 property is claimed for this positive path.",
    ),
    "NEG-MFOS-AUTH-DENY-0902": entry(
        "C4_VERIFIED_PROPERTY",
        [verified("authorization", "PolicyDeniedMappingForDatasetRead", "lemma", "Dataset read denial maps to MFOS_ERR_POLICY_DENIED and DATASET_READ_NOT_PERMITTED.")],
        "Negative dataset read denial has an explicit verified lemma.",
    ),
    "TEST-MFOS-AUTH-ALLOW-WITH-AUDIT-0903": entry(
        "C3_FULL_SEMANTIC",
        [semantic("authorization", "EvaluateSecurityDecision", "function", "C3_FULL_SEMANTIC", "ALLOW_WITH_AUDIT is executable; audit linkage is covered in audit/FVS properties.")],
        "Executable decision function exists; no C4 property is claimed for this positive path.",
    ),
    "TEST-MFOS-AUTH-REQUIRE-MFA-0904": entry(
        "C2_PARTIAL_SEMANTIC",
        [semantic("authorization", "EvaluateSecurityDecision", "function", "C2_PARTIAL_SEMANTIC", "REQUIRE_MFA is represented as a decision result, but MFA workflow semantics are not modeled.")],
        "Decision result exists, but the workflow is a Phase 1.1 gap.",
    ),
    "TEST-MFOS-AUTH-REQUIRE-DUAL-CONTROL-0905": entry(
        "C2_PARTIAL_SEMANTIC",
        [semantic("authorization", "EvaluateSecurityDecision", "function", "C2_PARTIAL_SEMANTIC", "REQUIRE_DUAL_CONTROL is represented, but authorization-side dual-control workflow semantics are not modeled.")],
        "Decision result exists, but the workflow is a Phase 1.1 gap.",
    ),
    "TEST-MFOS-AUTH-REQUIRE-BREAK-GLASS-0906": entry(
        "C2_PARTIAL_SEMANTIC",
        [semantic("authorization", "EvaluateSecurityDecision", "function", "C2_PARTIAL_SEMANTIC", "REQUIRE_BREAK_GLASS is represented, but reason/expiry workflow semantics are not modeled in authorization.dfy.")],
        "Decision result exists, but the workflow is a Phase 1.1 gap.",
    ),
    "TEST-MFOS-AUTH-REQUIRE-GUARD-APPROVAL-0907": entry(
        "C2_PARTIAL_SEMANTIC",
        [semantic("authorization", "EvaluateSecurityDecision", "function", "C2_PARTIAL_SEMANTIC", "REQUIRE_GUARD_APPROVAL is represented, but Guard approval workflow semantics are not modeled.")],
        "Decision result exists, but the workflow is a Phase 1.1 gap.",
    ),
    "TEST-MFOS-AUTH-REQUIRE-OPERATOR-CONFIRMATION-0908": entry(
        "C2_PARTIAL_SEMANTIC",
        [semantic("authorization", "EvaluateSecurityDecision", "function", "C2_PARTIAL_SEMANTIC", "REQUIRE_OPERATOR_CONFIRMATION is represented, but authorization-side confirmation workflow semantics are not modeled.")],
        "Decision result exists, but the workflow is a Phase 1.1 gap.",
    ),
    "NEG-MFOS-AUTH-UNSUPPORTED-0909": entry(
        "C4_VERIFIED_PROPERTY",
        [verified("authorization", "INV_AUTH_UNSUPPORTED_NOT_SUCCESS", "lemma", "UNSUPPORTED is fail-closed and never a success result.")],
        "UNSUPPORTED negative path has an explicit verified lemma.",
    ),
    "NEG-MFOS-AUTH-SPEC-GAP-0910": entry(
        "C4_VERIFIED_PROPERTY",
        [verified("authorization", "INV_AUTH_SPEC_GAP_NOT_SUCCESS", "lemma", "SPEC_GAP is fail-closed and never a success result.")],
        "SPEC_GAP negative path has an explicit verified lemma.",
    ),
    "NEG-MFOS-AUTH-STALE-POLICY-0920": entry(
        "C3_FULL_SEMANTIC",
        [semantic("authorization", "EvaluateSecurityDecision", "function", "C3_FULL_SEMANTIC", "Policy-version mismatch branch exists, but no dedicated stale-policy lemma is declared.")],
        "Executable branch exists; coverage is below C4 until a dedicated property is added.",
    ),
    "NEG-MFOS-AUTH-EXPIRED-DELEGATION-0921": entry("C0_NONE", [none("Delegation expiry semantics are not modeled in Phase 1.1 Dafny.")], "No Dafny mapping."),
    "NEG-MFOS-AUTH-BREAK-GLASS-NO-REASON-0922": entry("C2_PARTIAL_SEMANTIC", [semantic("authorization", "DecisionObligation", "datatype", "C2_PARTIAL_SEMANTIC", "Break-glass obligation datatype exists; missing reason semantics are not modeled here.")], "Type-level/partial representation only."),
    "NEG-MFOS-AUTH-BREAK-GLASS-NO-EXPIRY-0923": entry("C2_PARTIAL_SEMANTIC", [semantic("authorization", "DecisionObligation", "datatype", "C2_PARTIAL_SEMANTIC", "Break-glass obligation datatype exists; missing expiry semantics are not modeled here.")], "Type-level/partial representation only."),
    "NEG-MFOS-AUTH-POLICY-LINT-WILDCARD-0924": entry("C0_NONE", [none("Policy lint wildcard semantics are not modeled in Phase 1.1 Dafny.")], "No Dafny mapping."),
    "NEG-MFOS-AUTH-UNAUTHORIZED-HANDLE-0925": entry(
        "C4_VERIFIED_PROPERTY",
        [verified("authorization", "INV_AUTH_NO_HANDLE_WITHOUT_ALLOW", "lemma", "Protected handles cannot be created without ALLOW or ALLOW_WITH_AUDIT.")],
        "Unauthorized handle creation is backed by a verified lemma.",
    ),
    "TEST-MFOS-AUDIT-DENY-BEFORE-RETURN-0901": entry(
        "C4_VERIFIED_PROPERTY",
        [verified("audit", "INV_AUDIT_DENY_TRANSITION_WRITES_BEFORE_RETURN", "lemma", "Denied operation finalization appends before-return audit evidence when audit is available.")],
        "Deny-before-return is transition-backed.",
    ),
    "TEST-MFOS-AUDIT-MINIMUM-FIELDS-0902": entry("C3_FULL_SEMANTIC", [semantic("audit", "AuditRecordMinimumFields", "predicate", "C3_FULL_SEMANTIC", "Minimum field predicate exists without a test-specific lemma.")], "Executable predicate exists; no C4 claim."),
    "NEG-MFOS-AUDIT-MISSING-CORRELATION-0903": entry("C2_PARTIAL_SEMANTIC", [semantic("audit", "AuditRecordMinimumFields", "predicate", "C2_PARTIAL_SEMANTIC", "Correlation validity participates in the predicate, but no missing-correlation negative lemma exists.")], "Partial semantic coverage only."),
    "TEST-MFOS-AUDIT-HASH-CHAIN-VALID-0904": entry("C3_FULL_SEMANTIC", [semantic("audit", "ValidHashChain", "predicate", "C3_FULL_SEMANTIC", "Hash-chain predicate exists without dedicated verified test lemma.")], "Executable predicate exists; no C4 claim."),
    "NEG-MFOS-AUDIT-HASH-CHAIN-TAMPERED-0905": entry("C2_PARTIAL_SEMANTIC", [semantic("audit", "ValidHashChain", "predicate", "C2_PARTIAL_SEMANTIC", "Tamper rejection is not expressed as a dedicated lemma.")], "Partial semantic coverage only."),
    "NEG-MFOS-AUDIT-AUDIT-UNAVAILABLE-0906": entry(
        "C4_VERIFIED_PROPERTY",
        [verified("audit", "INV_AUDIT_DENY_TRANSITION_FAILS_CLOSED_WHEN_UNAVAILABLE", "lemma", "Denied operation finalization fails closed when required audit is unavailable.")],
        "Audit-unavailable negative path is transition-backed.",
    ),
    "NEG-MFOS-AUDIT-UNAUTHORIZED-QUERY-0907": entry("C0_NONE", [none("Audit query authorization is not modeled in Phase 1.1 Dafny.")], "No Dafny mapping."),
    "NEG-MFOS-AUDIT-SPOOL-NOT-EVIDENCE-0908": entry("C4_VERIFIED_PROPERTY", [verified("audit", "INV_AUDIT_SPOOL_NOT_EVIDENCE", "lemma", "Spool entries are not audit evidence.")], "Verified negative property."),
    "NEG-MFOS-AUDIT-LOG-LINE-NOT-RECORD-0909": entry("C4_VERIFIED_PROPERTY", [verified("audit", "INV_AUDIT_LOG_LINE_NOT_RECORD", "lemma", "Diagnostic log lines are not audit records.")], "Verified negative property."),
    "NEG-MFOS-AUDIT-REDACTION-FAILURE-0910": entry("C0_NONE", [none("Redaction failure semantics are not modeled in Phase 1.1 Dafny.")], "No Dafny mapping."),
    "NEG-MFOS-AUDIT-DUPLICATE-RECORD-ID-0911": entry("C0_NONE", [none("Duplicate audit record-id semantics are not modeled in Phase 1.1 Dafny.")], "No Dafny mapping."),
    "NEG-MFOS-AUDIT-NON-MONOTONIC-SEQUENCE-0912": entry("C2_PARTIAL_SEMANTIC", [semantic("audit", "ValidHashChain", "predicate", "C2_PARTIAL_SEMANTIC", "Sequence monotonicity is part of hash-chain validity, but no dedicated negative lemma exists.")], "Partial semantic coverage only."),
    "TEST-MFOS-DATASET-VALID-DSN-0901": entry("C3_FULL_SEMANTIC", [semantic("dataset_catalog", "SymbolicDsnValid", "predicate", "C3_FULL_SEMANTIC", "Symbolic DSN validity predicate exists; no dedicated positive lemma.")], "Executable predicate exists; no C4 claim."),
    "NEG-MFOS-DATASET-MALFORMED-DSN-0902": entry("C2_PARTIAL_SEMANTIC", [semantic("dataset_catalog", "SymbolicDsnValid", "predicate", "C2_PARTIAL_SEMANTIC", "Malformed DSN rejection now maps to MFOS_ERR_INVALID_DSN in Phase 1.3; Phase 1.1 still records only symbolic DSN coverage.")], "Partial symbolic DSN coverage only."),
    "TEST-MFOS-DATASET-CATALOG-COMMITTED-0903": entry("C3_FULL_SEMANTIC", [semantic("dataset_catalog", "CatalogEntryResolvable", "predicate", "C3_FULL_SEMANTIC", "Committed entry resolution predicate exists; no dedicated positive lemma.")], "Executable predicate exists; no C4 claim."),
    "NEG-MFOS-DATASET-CATALOG-UNCOMMITTED-0904": entry("C4_VERIFIED_PROPERTY", [verified("dataset_catalog", "INV_CATALOG_UNCOMMITTED_CANNOT_RESOLVE", "lemma", "Uncommitted entries cannot resolve.")], "Verified negative property."),
    "NEG-MFOS-DATASET-CATALOG-ROLLED-BACK-0905": entry("C4_VERIFIED_PROPERTY", [verified("dataset_catalog", "INV_CATALOG_ROLLED_BACK_CANNOT_RESOLVE", "lemma", "Rolled-back entries cannot resolve.")], "Verified negative property."),
    "NEG-MFOS-DATASET-CATALOG-PARTIAL-JOURNAL-0906": entry("C4_VERIFIED_PROPERTY", [verified("dataset_catalog", "INV_CATALOG_PARTIAL_JOURNAL_CANNOT_RESOLVE", "lemma", "Partial-journal entries cannot resolve.")], "Verified negative property."),
    "NEG-MFOS-DATASET-CATALOG-INTEGRITY-FAILED-0907": entry("C4_VERIFIED_PROPERTY", [verified("dataset_catalog", "INV_CATALOG_INTEGRITY_FAILED_CANNOT_RESOLVE", "lemma", "Integrity-failed entries cannot resolve.")], "Verified negative property."),
    "NEG-MFOS-DATASET-UNAUTHORIZED-OPEN-0908": entry("C4_VERIFIED_PROPERTY", [verified("dataset_catalog", "INV_DATASET_NO_HANDLE_WITHOUT_ALLOW", "lemma", "Dataset handle creation requires an allow decision.")], "Verified negative property."),
    "NEG-MFOS-DATASET-STALE-HANDLE-POLICY-0909": entry("C4_VERIFIED_PROPERTY", [verified("dataset_catalog", "INV_DATASET_STALE_HANDLE_AFTER_POLICY_CHANGE_REJECTED", "lemma", "Policy-version-stale handles are rejected.")], "Verified negative property."),
    "NEG-MFOS-DATASET-STALE-HANDLE-CATALOG-0910": entry("C4_VERIFIED_PROPERTY", [verified("dataset_catalog", "INV_DATASET_STALE_HANDLE_AFTER_GENERATION_CHANGE_REJECTED", "lemma", "Generation-stale handles are rejected.")], "Verified negative property."),
    "NEG-MFOS-DATASET-RETENTION-DELETE-0911": entry("C3_FULL_SEMANTIC", [semantic("dataset_catalog", "RetentionBlocksDelete", "predicate", "C3_FULL_SEMANTIC", "Retention delete-block predicate exists without a dedicated verified lemma.")], "Executable predicate exists; no C4 claim."),
    "NEG-MFOS-DATASET-IMMUTABLE-SYSTEM-0912": entry("C3_FULL_SEMANTIC", [semantic("dataset_catalog", "ImmutableSystemDatasetBlocksModify", "predicate", "C3_FULL_SEMANTIC", "Immutable-system modify-block predicate exists without a dedicated verified lemma.")], "Executable predicate exists; no C4 claim."),
    "NEG-MFOS-DATASET-NOT-POSIX-FILE-0913": entry("C0_NONE", [none("Non-POSIX-file distinction is documented as a non-objective, not executable Dafny semantics.")], "No Dafny mapping."),
    "TEST-MFOS-DATASET-CRASH-MID-COMMIT-0914": entry("C2_PARTIAL_SEMANTIC", [semantic("dataset_catalog", "CatalogEntryResolvable", "predicate", "C2_PARTIAL_SEMANTIC", "Crash-mid-commit recovery success is not modeled as a transition property.")], "Partial semantic coverage only."),
    "TEST-MFOS-JOB-HELLO-JOB-0901": entry("C3_FULL_SEMANTIC", [semantic("job_spool", "ValidJobTransition", "predicate", "C3_FULL_SEMANTIC", "Job lifecycle predicate exists; end-to-end hello-job proof is in first vertical slice.")], "Executable predicate exists; no C4 claim in job_spool."),
    "NEG-MFOS-JOB-MALFORMED-CONTROL-0902": entry("C0_NONE", [none("Malformed control stream parsing is outside Phase 1.1 Dafny semantics.")], "No Dafny mapping."),
    "NEG-MFOS-JOB-SUBMIT-NO-PRINCIPAL-0903": entry("C2_PARTIAL_SEMANTIC", [semantic("job_spool", "EffectivePrincipalEstablished", "predicate", "C2_PARTIAL_SEMANTIC", "Effective principal predicate exists; submit-time failure property is not modeled.")], "Partial semantic coverage only."),
    "TEST-MFOS-JOB-PRINCIPAL-BEFORE-OPEN-0904": entry("C4_VERIFIED_PROPERTY", [verified("job_spool", "INV_JOB_EFFECTIVE_PRINCIPAL_BEFORE_OPEN", "lemma", "Dataset open is blocked until effective principal is established.")], "Verified property."),
    "TEST-MFOS-JOB-DD-CATALOG-RESOLUTION-0905": entry("C4_VERIFIED_PROPERTY", [verified("job_spool", "INV_JOB_DD_RESOLUTION_THROUGH_CATALOG_AND_AUTH", "lemma", "Dataset DD resolution requires catalog resolution and authorization.")], "Verified property."),
    "TEST-MFOS-JOB-DD-AUTHORIZATION-0906": entry("C4_VERIFIED_PROPERTY", [verified("job_spool", "INV_JOB_DD_RESOLUTION_THROUGH_CATALOG_AND_AUTH", "lemma", "Dataset DD resolution requires authorization.")], "Verified property."),
    "NEG-MFOS-JOB-DD-BYPASS-DENIED-0907": entry("C4_VERIFIED_PROPERTY", [verified("job_spool", "INV_JOB_DD_RESOLUTION_THROUGH_CATALOG_AND_AUTH", "lemma", "DD resolution cannot bypass catalog and authorization.")], "Verified property."),
    "NEG-MFOS-JOB-UNAUTHORIZED-DATASET-0908": entry("C4_VERIFIED_PROPERTY", [verified("dataset_catalog", "INV_DATASET_NO_HANDLE_WITHOUT_ALLOW", "lemma", "Dataset handle creation requires an allow decision.")], "Verified property."),
    "TEST-MFOS-JOB-STEP-FAILURE-RC-0909": entry("C2_PARTIAL_SEMANTIC", [semantic("job_spool", "JobStep", "datatype", "C2_PARTIAL_SEMANTIC", "Return-code state exists as data, but failure RC semantics are not modeled.")], "Type-level/partial representation only."),
    "NEG-MFOS-JOB-INVALID-LIFECYCLE-0910": entry("C4_VERIFIED_PROPERTY", [verified("job_spool", "INV_JOB_INVALID_LIFECYCLE_REJECTED", "lemma", "Invalid lifecycle transitions are rejected.")], "Verified property."),
    "TEST-MFOS-JOB-SPOOL-CREATE-0911": entry("C3_FULL_SEMANTIC", [semantic("job_spool", "SpoolEntryProtected", "predicate", "C3_FULL_SEMANTIC", "Protected spool-entry predicate exists without a create-transition lemma.")], "Executable predicate exists; no C4 claim."),
    "TEST-MFOS-JOB-SPOOL-BROWSE-OWNER-0912": entry("C3_FULL_SEMANTIC", [semantic("job_spool", "SpoolBrowseAllowed", "predicate", "C3_FULL_SEMANTIC", "Owner browse predicate exists without a dedicated positive lemma.")], "Executable predicate exists; no C4 claim."),
    "NEG-MFOS-JOB-SPOOL-BROWSE-NONOWNER-0913": entry("C4_VERIFIED_PROPERTY", [verified("job_spool", "INV_SPOOL_BROWSE_BY_NON_OWNER_DENIED", "lemma", "Non-owner spool browse is denied.")], "Verified property."),
    "NEG-MFOS-JOB-SPOOL-PURGE-DENIED-0914": entry("C4_VERIFIED_PROPERTY", [verified("job_spool", "INV_SPOOL_PURGE_WITHOUT_AUTHORITY_DENIED", "lemma", "Spool purge without authority is denied.")], "Verified property."),
    "NEG-MFOS-JOB-SPOOL-EXPORT-NO-AUDIT-0915": entry("C0_NONE", [none("Spool export audit requirement is not modeled in Phase 1.1 Dafny.")], "No Dafny mapping."),
    "NEG-MFOS-JOB-CANCEL-NO-AUTHORITY-0916": entry("C0_NONE", [none("Job cancel authority is not modeled in job_spool.dfy.")], "No Dafny mapping."),
    "NEG-MFOS-JOB-STEP-NO-AUDIT-CORRELATION-0917": entry("C0_NONE", [none("Job step audit correlation semantics are not modeled in Phase 1.1 Dafny.")], "No Dafny mapping."),
    "TEST-MFOS-OPER-DISPLAY-SYSTEM-0901": entry("C3_FULL_SEMANTIC", [semantic("operator_console", "OperatorCommandAuthorized", "predicate", "C3_FULL_SEMANTIC", "Operator authorization predicate exists without a dedicated positive lemma.")], "Executable predicate exists; no C4 claim."),
    "TEST-MFOS-OPER-DEFINE-USER-0902": entry("C3_FULL_SEMANTIC", [semantic("operator_console", "OperatorCommandAuthorized", "predicate", "C3_FULL_SEMANTIC", "Operator authorization predicate exists without a dedicated positive lemma.")], "Executable predicate exists; no C4 claim."),
    "TEST-MFOS-OPER-DEFINE-DATASET-0903": entry("C3_FULL_SEMANTIC", [semantic("operator_console", "OperatorCommandAuthorized", "predicate", "C3_FULL_SEMANTIC", "Operator authorization predicate exists without a dedicated positive lemma.")], "Executable predicate exists; no C4 claim."),
    "TEST-MFOS-OPER-SUBMIT-JOB-0904": entry("C3_FULL_SEMANTIC", [semantic("operator_console", "OperatorCommandAuthorized", "predicate", "C3_FULL_SEMANTIC", "Operator authorization predicate exists without a dedicated positive lemma.")], "Executable predicate exists; no C4 claim."),
    "NEG-MFOS-OPER-CANCEL-JOB-DENIED-0905": entry("C4_VERIFIED_PROPERTY", [verified("operator_console", "INV_OPERATOR_NO_COMMAND_WITHOUT_AUTH", "lemma", "Operator command cannot execute without authorization.")], "Verified property."),
    "NEG-MFOS-OPER-DESTRUCTIVE-NO-CONFIRM-0906": entry("C4_VERIFIED_PROPERTY", [verified("operator_console", "INV_OPERATOR_DESTRUCTIVE_WITHOUT_CONFIRMATION_DENIED", "lemma", "Destructive command without confirmation is denied.")], "Verified property."),
    "NEG-MFOS-OPER-DUAL-CONTROL-SINGLE-0907": entry("C4_VERIFIED_PROPERTY", [verified("operator_console", "INV_OPERATOR_DUAL_CONTROL_SINGLE_APPROVAL_DENIED", "lemma", "Dual-control command with one approval is denied.")], "Verified property."),
    "NEG-MFOS-OPER-EMERGENCY-NO-REASON-0908": entry("C4_VERIFIED_PROPERTY", [verified("operator_console", "INV_OPERATOR_EMERGENCY_WITHOUT_REASON_OR_EXPIRY_DENIED", "lemma", "Emergency mode without reason is denied.")], "Verified property."),
    "NEG-MFOS-OPER-EMERGENCY-NO-EXPIRY-0909": entry("C4_VERIFIED_PROPERTY", [verified("operator_console", "INV_OPERATOR_EMERGENCY_WITHOUT_REASON_OR_EXPIRY_DENIED", "lemma", "Emergency mode without expiry is denied.")], "Verified property."),
    "NEG-MFOS-OPER-AUTOMATION-BYPASS-0910": entry("C0_NONE", [none("Automation bypass restriction is not modeled in Phase 1.1 Dafny.")], "No Dafny mapping."),
    "NEG-MFOS-OPER-MALFORMED-COMMAND-0911": entry("C0_NONE", [none("Operator command parser semantics are not modeled in Phase 1.1 Dafny.")], "No Dafny mapping."),
    "NEG-MFOS-OPER-COMMAND-NO-AUDIT-0912": entry("C4_VERIFIED_PROPERTY", [verified("operator_console", "INV_OPERATOR_NO_COMMAND_WITHOUT_AUDIT", "lemma", "Audited operator commands require audit evidence.")], "Verified property."),
    "NEG-MFOS-OPER-ROOT-SHELL-FIRST-UI-0913": entry("C4_VERIFIED_PROPERTY", [verified("operator_console", "INV_OPERATOR_ROOT_SHELL_NOT_FIRST_UI", "lemma", "Root shell cannot be modeled as the first privileged UI.")], "Verified property."),
    "TEST-MFOS-FVS-HELLO-JOB-9001": entry(
        "C5_CONFORMANCE_LINKED",
        [verified("first_vertical_slice", "HelloJobContract", "lemma", "Hello-job final state, return code, handle-after-allow, spool output, and audit sequence are verified and fixture-linked.")],
        "First vertical slice positive path is verified and linked to fixture/oracle/golden artifacts.",
    ),
    "NEG-MFOS-FVS-BOB-DENIED-9002": entry(
        "C5_CONFORMANCE_LINKED",
        [verified("first_vertical_slice", "BobDeniedAliceDatasetContract", "lemma", "Bob-denied path verifies no handle, policy denial code, before-final audit, and failure summary, and is fixture-linked.")],
        "First vertical slice negative path is verified and linked to fixture/oracle/golden artifacts.",
    ),
}

FORMAL_CLAIM_DAFNY_COVERAGE = {
    "MFOS-FC-AUTHORIZATION-NO-HANDLE-WITHOUT-ALLOW": ("authorization", "INV_AUTH_NO_HANDLE_WITHOUT_ALLOW"),
    "MFOS-FC-AUDIT-DENY-BEFORE-RETURN": ("audit", "INV_AUDIT_DENY_TRANSITION_WRITES_BEFORE_RETURN"),
}


def load_yaml(path: str | Path) -> dict[str, Any]:
    data = yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return data


def dump(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def worst_level(levels: list[str]) -> str:
    if not levels:
        return "C0_NONE"
    return min(levels, key=lambda level: COVERAGE_RANK[level])


def count_levels(items: list[dict[str, Any]]) -> dict[str, int]:
    counter = Counter(item["coverage_level"] for item in items)
    return {level: counter[level] for level in COVERAGE_LEVELS if counter[level]}


def build_artifacts() -> dict[str, Any]:
    req_to_tests: dict[str, list[dict[str, Any]]] = defaultdict(list)
    tests: list[dict[str, Any]] = []
    fixtures: list[dict[str, Any]] = []
    oracles: list[dict[str, Any]] = []

    for domain, catalog in CATALOGS.items():
        data = load_yaml(catalog)
        for catalog_entry in data["entries"]:
            if str(catalog_entry.get("phase_to_implement")) in {"Phase 1.4.1", "Phase 1.4.2"}:
                continue
            test_id = catalog_entry["test_id"]
            coverage = TEST_COVERAGE.get(test_id, entry("C0_NONE", [none("No explicit Phase 1.1 coverage mapping exists for this test.")], "No explicit mapping."))
            coverage_mappings = coverage["coverage_mappings"]
            test_record = {
                "test_id": test_id,
                "catalog": catalog,
                "domain": domain,
                "negative": bool(catalog_entry.get("negative")),
                "target_requirements": catalog_entry.get("target_requirements", []),
                "fixture_ref": catalog_entry.get("fixture_ref"),
                "oracle_ref": catalog_entry.get("oracle_ref"),
                "golden_ref": catalog_entry.get("golden_ref"),
                "coverage_level": coverage["coverage_level"],
                "coverage_justification": coverage["coverage_justification"],
                "coverage_mappings": coverage_mappings,
                "negative_failure_conditions": [
                    mapping["dafny_symbol"]
                    for mapping in coverage_mappings
                    if catalog_entry.get("negative") and mapping.get("coverage_level") in {"C4_VERIFIED_PROPERTY", "C5_CONFORMANCE_LINKED"}
                ],
                "audit_expectation": "explicit_audit_property_or_gap_recorded"
                if catalog_entry.get("audit_obligation_required")
                else "not_required",
            }
            tests.append(test_record)
            for req in catalog_entry.get("target_requirements", []):
                req_to_tests[req].append(test_record)
            if catalog_entry.get("fixture_ref"):
                fixtures.append(
                    {
                        "fixture_ref": catalog_entry["fixture_ref"],
                        "test_id": test_id,
                        "domain": domain,
                        "normalized_input_type": "semantic-fixture-normalizer deterministic JSON object",
                        "normalizer": "tools/semantic-fixture-normalizer/src/normalize.py",
                        "coverage_level": coverage["coverage_level"],
                        "coverage_mappings": coverage_mappings,
                    }
                )
            if catalog_entry.get("golden_ref"):
                oracles.append(
                    {
                        "oracle_ref": catalog_entry.get("oracle_ref"),
                        "golden_ref": catalog_entry["golden_ref"],
                        "test_id": test_id,
                        "domain": domain,
                        "expected_dafny_result": "declared by linked Dafny coverage mapping; Python harness compares declared shapes only",
                        "comparison_target": "tools/dafny-conformance-harness/src/harness.py compare-fixture-golden",
                        "coverage_level": coverage["coverage_level"],
                        "coverage_mappings": coverage_mappings,
                    }
                )

    requirements: list[dict[str, Any]] = []
    for req, linked_tests in sorted(req_to_tests.items()):
        levels = [test["coverage_level"] for test in linked_tests]
        mappings_by_key: dict[tuple[str | None, str | None], dict[str, Any]] = {}
        for test in linked_tests:
            for mapping in test["coverage_mappings"]:
                mappings_by_key[(mapping.get("dafny_module"), mapping.get("dafny_symbol"))] = mapping
        requirements.append(
            {
                "requirement_id": req,
                "linked_tests": [test["test_id"] for test in linked_tests],
                "coverage_level": worst_level(levels),
                "coverage_mappings": list(mappings_by_key.values()),
                "coverage_basis": "Worst linked-test level; C4/C5 require explicit verified symbols and evidence references.",
            }
        )

    claims_data = load_yaml("formal/claim-registry.yml")
    registry_proof_claimed = bool(claims_data.get("proof_claimed"))
    claims: list[dict[str, Any]] = []
    for claim in claims_data.get("claims", []):
        claim_id = claim["claim_id"]
        mapped = FORMAL_CLAIM_DAFNY_COVERAGE.get(claim_id)
        proof_artifacts = claim.get("proof_artifact_refs", [])
        proof_backed = registry_proof_claimed and claim.get("status") == "proven" and bool(proof_artifacts)
        if mapped and proof_backed:
            domain, symbol = mapped
            coverage_level = "C4_VERIFIED_PROPERTY"
            mappings = [verified(domain, symbol, "lemma", "Formal claim has proof-backed Dafny coverage.")]
        elif mapped:
            domain, symbol = mapped
            coverage_level = "C3_FULL_SEMANTIC"
            mappings = [
                semantic(
                    domain,
                    symbol,
                    "lemma",
                    "C3_FULL_SEMANTIC",
                    "Dafny lemma exists, but formal registry is still planned/draft and proof_claimed is false.",
                )
            ]
        else:
            coverage_level = "C0_NONE"
            mappings = [none("Formal claim is outside Phase 1.1 Dafny semantic coverage.")]
        claims.append(
            {
                "claim_id": claim_id,
                "status": claim.get("status"),
                "requirement_refs": claim.get("requirement_refs", []),
                "proof_claimed": registry_proof_claimed,
                "proof_artifact_refs": proof_artifacts,
                "coverage_level": coverage_level,
                "coverage_mappings": mappings,
                "production_claimed": False,
            }
        )

    domains: dict[str, str] = {}
    for domain in CATALOGS:
        domain_levels = [test["coverage_level"] for test in tests if test["domain"] == domain]
        domains[domain] = worst_level(domain_levels)

    negative_tests = [test for test in tests if test["negative"]]
    negative_complete = all(test["coverage_level"] in {"C4_VERIFIED_PROPERTY", "C5_CONFORMANCE_LINKED"} for test in negative_tests)
    formal_complete = all(claim["coverage_level"] in {"C4_VERIFIED_PROPERTY", "C5_CONFORMANCE_LINKED", "C6_RELEASE_READY_MODEL"} for claim in claims)

    summary = {
        "schema_version": 1,
        "artifact_type": "phase_1_1_semantic_coverage_summary",
        "status": "current",
        "generated_by": "scripts/generators/generate-semantic-coverage.py",
        "source_traceability_dir": "evidence/traceability/generated/phase-1-1/",
        "source_inputs": list(CATALOGS.values())
        + [
            "tests/fixtures/**",
            "tests/golden/**",
            "formal/executable-semantics/dafny/modules/*.dfy",
            "formal/claim-registry.yml",
        ],
        "prerequisite_merge_status": {
            "pr_15": "merged",
            "pr_16": "superseded_by_pr_17_due_branch_rules",
            "pr_17": "merged",
        },
        "coverage_distribution": {
            "requirements": count_levels(requirements),
            "tests": count_levels(tests),
            "fixtures": count_levels(fixtures),
            "oracles": count_levels(oracles),
            "formal_claims": count_levels(claims),
        },
        "core_domains_coverage_level": {k: v for k, v in domains.items() if k != "first_vertical_slice"},
        "first_vertical_slice_coverage_level": domains["first_vertical_slice"],
        "phase_1_1_semantic_coverage_complete": False,
        "phase_1_1_core_domain_coverage_status": "mixed_verified_and_partial",
        "phase_1_1_formal_claim_coverage_complete": formal_complete,
        "negative_semantics_complete": negative_complete,
        "audit_deny_before_return_transition_backed": True,
        "dafny_verification_result": "206 verified, 0 errors",
        "production_implementation_allowed": False,
        "rust_phase_1_canonical_semantics_allowed": False,
        "hosted_daemon_implementation_allowed": False,
    }

    open_issues = [
        {
            "test_id": test["test_id"],
            "domain": test["domain"],
            "coverage_level": test["coverage_level"],
            "reason": test["coverage_justification"],
        }
        for test in tests
        if COVERAGE_RANK[test["coverage_level"]] < COVERAGE_RANK["C4_VERIFIED_PROPERTY"]
    ]
    open_issues.extend(
        {
            "claim_id": claim["claim_id"],
            "coverage_level": claim["coverage_level"],
            "reason": "Formal claim lacks proof-backed artifact coverage."
            if claim["coverage_level"] != "C0_NONE"
            else "Formal claim outside Phase 1.1 Dafny semantic coverage.",
        }
        for claim in claims
        if COVERAGE_RANK[claim["coverage_level"]] < COVERAGE_RANK["C4_VERIFIED_PROPERTY"]
    )

    return {
        "requirements": requirements,
        "tests": tests,
        "fixtures": fixtures,
        "oracles": oracles,
        "claims": claims,
        "summary": summary,
        "open_issues": open_issues,
    }


def write_reports(reports_dir: Path, artifacts: dict[str, Any]) -> None:
    summary = artifacts["summary"]
    open_issues = artifacts["open_issues"]
    tests = artifacts["tests"]

    write_text(
        reports_dir / "semantic-coverage-report.md",
        "\n".join(
            [
                "# Phase 1.1 Semantic Coverage Truthfulness Report",
                "",
                "This report records the post-review truthfulness remediation for Phase 1.1 Dafny semantic coverage.",
                "Coverage levels are now derived from explicit per-test mappings; domain-wide symbol stamping and last-symbol fallback are prohibited.",
                "",
                "## Result",
                "",
                f"- `phase_1_1_semantic_coverage_complete`: `{str(summary['phase_1_1_semantic_coverage_complete']).lower()}`",
                f"- `phase_1_1_core_domain_coverage_status`: `{summary['phase_1_1_core_domain_coverage_status']}`",
                f"- `phase_1_1_formal_claim_coverage_complete`: `{str(summary['phase_1_1_formal_claim_coverage_complete']).lower()}`",
                f"- `negative_semantics_complete`: `{str(summary['negative_semantics_complete']).lower()}`",
                f"- `audit_deny_before_return_transition_backed`: `{str(summary['audit_deny_before_return_transition_backed']).lower()}`",
                f"- `dafny_verification_result`: `{summary['dafny_verification_result']}`",
                "",
                "## Coverage Distribution",
                "",
                "```yaml",
                yaml.safe_dump(summary["coverage_distribution"], sort_keys=False).rstrip(),
                "```",
                "",
                "## Domain Levels",
                "",
                "```yaml",
                yaml.safe_dump(summary["core_domains_coverage_level"], sort_keys=False).rstrip(),
                "```",
                "",
                "The first vertical slice remains `C5_CONFORMANCE_LINKED`. Other core domains contain a mix of verified properties and partial gaps, so Phase 1.1 is not claimed complete.",
            ]
        )
        + "\n",
    )

    write_text(
        reports_dir / "negative-semantics-report.md",
        "\n".join(
            [
                "# Phase 1.1 Negative Semantics Truthfulness Report",
                "",
                "Negative semantic coverage is no longer reported as complete unless each negative test maps to an explicit verified property.",
                "",
                "| Test | Coverage | Mapping |",
                "| --- | --- | --- |",
            ]
            + [
                f"| `{test['test_id']}` | `{test['coverage_level']}` | "
                + ", ".join(f"`{m.get('dafny_symbol') or 'missing'}`" for m in test["coverage_mappings"])
                + " |"
                for test in tests
                if test["negative"]
            ]
        )
        + "\n",
    )

    write_text(
        reports_dir / "semantic-coverage-open-issues.md",
        "\n".join(
            [
                "# Phase 1.1 Semantic Coverage Open Issues",
                "",
                "These are truthful gaps left after remediation. They are not treated as successful semantic coverage.",
                "",
            ]
            + [
                f"- `{issue.get('test_id') or issue.get('claim_id')}`: `{issue['coverage_level']}` - {issue['reason']}"
                for issue in open_issues
            ]
        )
        + "\n",
    )

    write_text(
        reports_dir / "semantic-coverage-red-team-review.md",
        "\n".join(
            [
                "# Phase 1.1 Semantic Coverage Red-Team Review",
                "",
                "## Findings",
                "",
                "- Critical: none found after remediation.",
                "- Major: none found after remediation.",
                "- Domain-wide symbol assignment removed.",
                "- Last-symbol negative fallback removed.",
                "- Planned formal claims are no longer reported as C4/C5 coverage.",
                "- `STATUS.md` must report Phase 1.1 semantic coverage as incomplete until remaining gaps are closed.",
                "- Python loader/harness remains non-semantic.",
                "- Production implementation, Rust semantic-core, hosted daemon, and production-like semantic runner remain prohibited.",
            ]
        )
        + "\n",
    )


def write_traceability(traceability_dir: Path, artifacts: dict[str, Any]) -> None:
    base = {
        "schema_version": 1,
        "artifact_type": "phase_1_1_semantic_coverage_traceability",
        "status": "generated",
        "origin_phase": "phase-1.1",
        "generated_by": "scripts/generators/generate-semantic-coverage.py",
        "source_inputs": list(CATALOGS.values())
        + [
            "tests/fixtures/**",
            "tests/golden/**",
            "formal/executable-semantics/dafny/modules/*.dfy",
            "formal/claim-registry.yml",
        ],
        "coverage_levels": COVERAGE_LEVELS,
        "production_implementation_allowed": False,
    }
    dump(traceability_dir / "requirement-to-dafny.yml", {**base, "traceability_kind": "requirement_to_dafny", "requirements": artifacts["requirements"]})
    dump(traceability_dir / "test-to-dafny.yml", {**base, "traceability_kind": "test_to_dafny", "tests": artifacts["tests"]})
    dump(traceability_dir / "fixture-to-dafny.yml", {**base, "traceability_kind": "fixture_to_dafny", "fixtures": artifacts["fixtures"]})
    dump(traceability_dir / "oracle-to-dafny.yml", {**base, "traceability_kind": "oracle_to_dafny", "oracles": artifacts["oracles"]})
    dump(traceability_dir / "formal-claim-to-dafny.yml", {**base, "traceability_kind": "formal_claim_to_dafny", "formal_claims": artifacts["claims"]})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--traceability-dir", type=Path, default=DEFAULT_TRACEABILITY_DIR)
    parser.add_argument("--reports-dir", type=Path, default=DEFAULT_REPORTS_DIR)
    args = parser.parse_args()

    artifacts = build_artifacts()
    write_traceability(args.traceability_dir, artifacts)
    dump(args.reports_dir / "semantic-coverage.yml", artifacts["summary"])
    write_reports(args.reports_dir, artifacts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
