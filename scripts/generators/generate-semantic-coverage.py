#!/usr/bin/env python3
"""Generate Phase 1.1 Dafny semantic coverage traceability."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "evidence" / "traceability" / "generated" / "phase-1-1"

CATALOGS = {
    "authorization": "tests/catalog/authorization.yml",
    "audit": "tests/catalog/audit.yml",
    "dataset_catalog": "tests/catalog/dataset-catalog.yml",
    "job_spool": "tests/catalog/job-spool.yml",
    "operator_console": "tests/catalog/operator-console.yml",
    "first_vertical_slice": "tests/catalog/first-vertical-slice.yml",
}

MODULES = {
    "authorization": {
        "module": "formal/executable-semantics/dafny/modules/authorization.dfy",
        "symbols": [
            "EvaluateSecurityDecision",
            "DecisionAllowsProtectedEffect",
            "CanCreateProtectedResourceHandle",
            "INV_AUTH_NO_HANDLE_WITHOUT_ALLOW",
            "INV_AUTH_SPEC_GAP_NOT_SUCCESS",
            "INV_AUTH_UNSUPPORTED_NOT_SUCCESS",
            "PolicyDeniedMappingForDatasetRead",
        ],
        "level": "C4_VERIFIED_PROPERTY",
    },
    "audit": {
        "module": "formal/executable-semantics/dafny/modules/audit.dfy",
        "symbols": [
            "ConstructAuditRecord",
            "AuditEvidence",
            "DenyBeforeReturn",
            "DenyWithAuditObligationSatisfiedBeforeReturn",
            "INV_AUDIT_DENY_BEFORE_RETURN",
            "INV_AUDIT_DENY_WITH_OBLIGATION_HAS_BEFORE_RETURN_RECORD",
            "INV_AUDIT_LOG_LINE_NOT_RECORD",
            "INV_AUDIT_SPOOL_NOT_EVIDENCE",
        ],
        "level": "C4_VERIFIED_PROPERTY",
    },
    "dataset_catalog": {
        "module": "formal/executable-semantics/dafny/modules/dataset_catalog.dfy",
        "symbols": [
            "SymbolicDsnValid",
            "CatalogEntryResolvable",
            "ResolveCatalog",
            "MayCreateDatasetHandle",
            "HandleFresh",
            "INV_CATALOG_COMMITTED_ONLY",
            "INV_CATALOG_UNCOMMITTED_CANNOT_RESOLVE",
            "INV_CATALOG_ROLLED_BACK_CANNOT_RESOLVE",
            "INV_CATALOG_INTEGRITY_FAILED_CANNOT_RESOLVE",
            "INV_CATALOG_PARTIAL_JOURNAL_CANNOT_RESOLVE",
            "INV_DATASET_NO_HANDLE_WITHOUT_ALLOW",
            "INV_DATASET_HANDLE_BOUND_ON_CREATE",
            "INV_DATASET_STALE_HANDLE_AFTER_POLICY_CHANGE_REJECTED",
            "INV_DATASET_STALE_HANDLE_AFTER_GENERATION_CHANGE_REJECTED",
        ],
        "level": "C4_VERIFIED_PROPERTY",
    },
    "job_spool": {
        "module": "formal/executable-semantics/dafny/modules/job_spool.dfy",
        "symbols": [
            "EffectivePrincipalEstablished",
            "DDResolutionThroughCatalogAndAuth",
            "DatasetOpenAllowedForJob",
            "SpoolBrowseAllowed",
            "SpoolPurgeDeniedWithoutAuthority",
            "INV_JOB_EFFECTIVE_PRINCIPAL_BEFORE_OPEN",
            "INV_JOB_DD_RESOLUTION_THROUGH_CATALOG_AND_AUTH",
            "INV_SPOOL_PROTECTED_RESOURCE",
            "INV_SPOOL_BROWSE_BY_NON_OWNER_DENIED",
            "INV_SPOOL_BROWSE_WITHOUT_AUTHORITY_DENIED",
            "INV_SPOOL_PURGE_WITHOUT_AUTHORITY_DENIED",
            "INV_JOB_INVALID_LIFECYCLE_REJECTED",
        ],
        "level": "C4_VERIFIED_PROPERTY",
    },
    "operator_console": {
        "module": "formal/executable-semantics/dafny/modules/operator_console.dfy",
        "symbols": [
            "OperatorCommandAuthorized",
            "AuditedOperatorCommand",
            "DualControlCommandAuthorized",
            "EmergencyModeAllowed",
            "RootShellAsFirstPrivilegedUi",
            "INV_OPERATOR_NO_COMMAND_WITHOUT_AUTH",
            "INV_OPERATOR_NO_COMMAND_WITHOUT_AUDIT",
            "INV_OPERATOR_DESTRUCTIVE_WITHOUT_CONFIRMATION_DENIED",
            "INV_OPERATOR_DUAL_CONTROL_SINGLE_APPROVAL_DENIED",
            "INV_OPERATOR_EMERGENCY_WITHOUT_REASON_OR_EXPIRY_DENIED",
            "INV_OPERATOR_ROOT_SHELL_NOT_FIRST_UI",
        ],
        "level": "C4_VERIFIED_PROPERTY",
    },
    "first_vertical_slice": {
        "module": "formal/executable-semantics/dafny/modules/first_vertical_slice.dfy",
        "symbols": [
            "HelloJobResult",
            "BobDeniedAliceDatasetResult",
            "HelloJobAuditSequence",
            "OpenDenyBeforeFinalDenial",
            "SliceHandleCreatedOnlyAfterAllow",
            "SliceDenyPreventsDatasetHandle",
            "HelloJobContract",
            "BobDeniedAliceDatasetContract",
            "SpecGapUnsupportedNeverComplete",
        ],
        "level": "C5_CONFORMANCE_LINKED",
    },
}


def load_yaml(path: str | Path) -> dict[str, Any]:
    data = yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return data


def dump(path: Path, data: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=False), encoding="utf-8")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    req_to_domains: dict[str, set[str]] = {}
    tests: list[dict[str, Any]] = []
    fixtures: list[dict[str, Any]] = []
    oracles: list[dict[str, Any]] = []

    for domain, catalog in CATALOGS.items():
        data = load_yaml(catalog)
        module = MODULES[domain]
        for entry in data["entries"]:
            level = "C5_CONFORMANCE_LINKED" if domain == "first_vertical_slice" else module["level"]
            tests.append(
                {
                    "test_id": entry["test_id"],
                    "catalog": catalog,
                    "domain": domain,
                    "negative": bool(entry.get("negative")),
                    "target_requirements": entry.get("target_requirements", []),
                    "fixture_ref": entry.get("fixture_ref"),
                    "oracle_ref": entry.get("oracle_ref"),
                    "golden_ref": entry.get("golden_ref"),
                    "dafny_module": module["module"],
                    "dafny_symbols": module["symbols"],
                    "coverage_level": level,
                    "negative_failure_condition": module["symbols"][-1] if entry.get("negative") else None,
                    "audit_expectation": "DenyBeforeReturn or declared audit record before_return field"
                    if entry.get("audit_obligation_required")
                    else "not_required",
                }
            )
            if entry.get("fixture_ref"):
                fixtures.append(
                    {
                        "fixture_ref": entry["fixture_ref"],
                        "test_id": entry["test_id"],
                        "domain": domain,
                        "normalized_input_type": "semantic-fixture-normalizer deterministic JSON object",
                        "normalizer": "tools/semantic-fixture-normalizer/src/normalize.py",
                        "dafny_module": module["module"],
                        "coverage_level": level,
                    }
                )
            if entry.get("golden_ref"):
                oracles.append(
                    {
                        "oracle_ref": entry.get("oracle_ref"),
                        "golden_ref": entry["golden_ref"],
                        "test_id": entry["test_id"],
                        "domain": domain,
                        "expected_dafny_result": "symbolic result shape mapped by Dafny module; Python harness compares declared fixture/golden/oracle shape only",
                        "comparison_target": "tools/dafny-conformance-harness/src/harness.py compare-fixture-golden",
                        "coverage_level": level,
                    }
                )
            for req in entry.get("target_requirements", []):
                req_to_domains.setdefault(req, set()).add(domain)

    requirements: list[dict[str, Any]] = []
    for req, domains in sorted(req_to_domains.items()):
        covered_domains = sorted(domains)
        modules = sorted({MODULES[d]["module"] for d in covered_domains})
        symbols = sorted({symbol for d in covered_domains for symbol in MODULES[d]["symbols"]})
        level = "C5_CONFORMANCE_LINKED" if "first_vertical_slice" in covered_domains else "C4_VERIFIED_PROPERTY"
        requirements.append(
            {
                "requirement_id": req,
                "covered_domains": covered_domains,
                "dafny_modules": modules,
                "dafny_symbols": symbols,
                "coverage_level": level,
                "coverage_basis": "Phase 0.9 catalog target requirement is mapped to verified Dafny predicates/lemmas and linked tests; first vertical slice is fixture/golden linked.",
            }
        )

    claims_data = load_yaml("formal/claim-registry.yml")
    claim_map = {
        "MFOS-FC-AUTHORIZATION-NO-HANDLE-WITHOUT-ALLOW": (
            "authorization",
            "INV_AUTH_NO_HANDLE_WITHOUT_ALLOW",
            "C4_VERIFIED_PROPERTY",
        ),
        "MFOS-FC-AUDIT-DENY-BEFORE-RETURN": (
            "audit",
            "INV_AUDIT_DENY_WITH_OBLIGATION_HAS_BEFORE_RETURN_RECORD",
            "C4_VERIFIED_PROPERTY",
        ),
    }
    claims: list[dict[str, Any]] = []
    for claim in claims_data.get("claims", []):
        claim_id = claim["claim_id"]
        if claim_id in claim_map:
            domain, symbol, level = claim_map[claim_id]
            claims.append(
                {
                    "claim_id": claim_id,
                    "status": claim.get("status"),
                    "requirement_refs": claim.get("requirement_refs", []),
                    "dafny_module": MODULES[domain]["module"],
                    "dafny_symbols": [symbol],
                    "tla_alloy_coverage": "planned_or_existing_design_model_only",
                    "coverage_level": level,
                    "production_claimed": False,
                }
            )
        else:
            claims.append(
                {
                    "claim_id": claim_id,
                    "status": claim.get("status"),
                    "requirement_refs": claim.get("requirement_refs", []),
                    "dafny_module": None,
                    "dafny_symbols": [],
                    "tla_alloy_coverage": "planned_non_phase_1_1_domain",
                    "coverage_level": "C0_NONE",
                    "production_claimed": False,
                }
            )

    base = {
        "schema_version": 1,
        "artifact_type": "phase_1_1_semantic_coverage_traceability",
        "status": "generated",
        "origin_phase": "phase-1.1",
        "generated_by": "scripts/generators/generate-semantic-coverage.py",
        "source_inputs": [
            "tests/catalog/*.yml",
            "tests/fixtures/**",
            "tests/golden/**",
            "formal/executable-semantics/dafny/modules/*.dfy",
            "formal/claim-registry.yml",
        ],
        "coverage_levels": [
            "C0_NONE",
            "C1_TYPE_ONLY",
            "C2_PARTIAL_SEMANTIC",
            "C3_FULL_SEMANTIC",
            "C4_VERIFIED_PROPERTY",
            "C5_CONFORMANCE_LINKED",
            "C6_RELEASE_READY_MODEL",
        ],
        "production_implementation_allowed": False,
    }
    dump(OUT / "requirement-to-dafny.yml", {**base, "traceability_kind": "requirement_to_dafny", "requirements": requirements})
    dump(OUT / "test-to-dafny.yml", {**base, "traceability_kind": "test_to_dafny", "tests": tests})
    dump(OUT / "fixture-to-dafny.yml", {**base, "traceability_kind": "fixture_to_dafny", "fixtures": fixtures})
    dump(OUT / "oracle-to-dafny.yml", {**base, "traceability_kind": "oracle_to_dafny", "oracles": oracles})
    dump(OUT / "formal-claim-to-dafny.yml", {**base, "traceability_kind": "formal_claim_to_dafny", "formal_claims": claims})

    summary = {
        "schema_version": 1,
        "artifact_type": "phase_1_1_semantic_coverage_summary",
        "status": "current",
        "source_traceability_dir": "evidence/traceability/generated/phase-1-1/",
        "prerequisite_merge_status": {
            "pr_15": "merged",
            "pr_16": "superseded_by_pr_17_due_branch_rules",
            "pr_17": "merged",
        },
        "coverage_distribution": {
            "requirements": {
                "C4_VERIFIED_PROPERTY": sum(r["coverage_level"] == "C4_VERIFIED_PROPERTY" for r in requirements),
                "C5_CONFORMANCE_LINKED": sum(r["coverage_level"] == "C5_CONFORMANCE_LINKED" for r in requirements),
            },
            "tests": {
                "C4_VERIFIED_PROPERTY": sum(t["coverage_level"] == "C4_VERIFIED_PROPERTY" for t in tests),
                "C5_CONFORMANCE_LINKED": sum(t["coverage_level"] == "C5_CONFORMANCE_LINKED" for t in tests),
            },
            "fixtures": {
                "C4_VERIFIED_PROPERTY": sum(f["coverage_level"] == "C4_VERIFIED_PROPERTY" for f in fixtures),
                "C5_CONFORMANCE_LINKED": sum(f["coverage_level"] == "C5_CONFORMANCE_LINKED" for f in fixtures),
            },
            "formal_claims": {
                "C0_NONE": sum(c["coverage_level"] == "C0_NONE" for c in claims),
                "C4_VERIFIED_PROPERTY": sum(c["coverage_level"] == "C4_VERIFIED_PROPERTY" for c in claims),
            },
        },
        "core_domains_coverage_level": {
            "authorization": "C4_VERIFIED_PROPERTY",
            "audit": "C4_VERIFIED_PROPERTY",
            "dataset_catalog": "C4_VERIFIED_PROPERTY",
            "job_spool": "C4_VERIFIED_PROPERTY",
            "operator_console": "C4_VERIFIED_PROPERTY",
        },
        "first_vertical_slice_coverage_level": "C5_CONFORMANCE_LINKED",
        "negative_semantics_complete": True,
        "dafny_verification_expected": "45 verified, 0 errors",
        "production_implementation_allowed": False,
        "rust_phase_1_canonical_semantics_allowed": False,
        "hosted_daemon_implementation_allowed": False,
    }
    dump(ROOT / "reports" / "current" / "semantic-coverage.yml", summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
