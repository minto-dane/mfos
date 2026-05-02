#!/usr/bin/env python3
"""Validate Phase 1.4.1 Job lifecycle, effective principal, and DD coverage."""

from __future__ import annotations

import filecmp
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml


ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "scripts").is_dir() and (parent / "docs").is_dir())
TRACEABILITY_DIR = ROOT / "evidence" / "traceability" / "generated" / "phase-1-4-1"
TRACE_FILES = [
    "coverage-summary.yml",
    "job-lifecycle-to-dafny.yml",
    "effective-principal-to-dafny.yml",
    "dd-resolution-to-dafny.yml",
    "test-to-dafny.yml",
    "fixture-to-dafny.yml",
    "requirement-to-dafny.yml",
    "formal-claim-to-dafny.yml",
]
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
PROOF_LEVELS = {"C4_VERIFIED_PROPERTY", "C5_CONFORMANCE_LINKED", "C6_RELEASE_READY_MODEL"}
SEMANTIC_LEVELS = {"C3_FULL_SEMANTIC", "C4_VERIFIED_PROPERTY", "C5_CONFORMANCE_LINKED", "C6_RELEASE_READY_MODEL"}
REQUIRED_BOUND_DD_SYMBOLS = {
    "INV_JOB_DD_DECISION_REQUIRES_EFFECTIVE_CONTEXT",
    "INV_JOB_DD_BOUND_DECISION_BINDS_REQUEST",
    "INV_JOB_DD_CROSS_REQUEST_AUTHORIZATION_REPLAY_BLOCKED",
    "INV_JOB_DD_DENY_MFOS_OK_INVALID",
    "INV_JOB_DD_VALID_ALLOW_AND_DENY_DISTINGUISHABLE",
    "INV_JOB_DD_DENY_PRODUCES_NO_HANDLE",
    "INV_JOB_DD_UNRESOLVED_CATALOG_FAILS",
    "INV_JOB_DD_DENY_AUDIT_UNAVAILABLE_FAILS_CLOSED",
}
BROAD_PARENT_REQUIREMENTS_REQUIRING_SUBCLAIMS = {
    "MFOS-REQ-JOB-0101",
    "MFOS-REQ-JOB-0102",
    "MFOS-REQ-JOB-0103",
}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return data


def row_name(row: dict[str, Any]) -> str:
    return str(row.get("test_id") or row.get("property_id") or row.get("subclaim_id") or row.get("requirement_id") or row.get("claim_id") or "<unknown>")


def level_rank(level: Any) -> int:
    return LEVEL_RANK.get(str(level), -1)


def exact_dafny_symbol_declared(module_text: str, symbol: str, symbol_kind: str) -> bool:
    kind = re.escape(symbol_kind or "lemma")
    pattern = rf"^\s*(?:ghost\s+)?{kind}\s+{re.escape(symbol)}\s*(?:\(|<)"
    return re.search(pattern, module_text, flags=re.MULTILINE) is not None


def compare_generated() -> list[str]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp_trace = Path(tmp) / "traceability"
        subprocess.run(
            [
                sys.executable,
                "scripts/generators/generate-job-dd-coverage.py",
                "--traceability-dir",
                str(tmp_trace),
            ],
            cwd=ROOT,
            check=True,
        )
        for name in TRACE_FILES:
            actual = TRACEABILITY_DIR / name
            expected = tmp_trace / name
            if not actual.exists():
                errors.append(f"missing generated traceability file: {actual}")
            elif not expected.exists():
                errors.append(f"coverage generator did not produce expected traceability file: {expected}")
            elif not filecmp.cmp(actual, expected, shallow=False):
                errors.append(f"stale generated traceability file: {actual}")
    return errors


def validate_c5_links(source_name: str, row: dict[str, Any], errors: list[str]) -> None:
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
        errors.append(f"{source_name}:{row_id}: C5 row must use embedded-oracle golden convention")
    fixture = load_yaml(ROOT / str(refs["fixture_ref"]))
    golden = load_yaml(ROOT / str(refs["golden_ref"]))
    oracle = golden.get("oracle")
    if not isinstance(oracle, dict):
        errors.append(f"{source_name}:{row_id}: golden_ref must embed an oracle mapping")
        return
    if fixture.get("expected_oracle") != refs["golden_ref"]:
        errors.append(f"{source_name}:{row_id}: fixture expected_oracle does not match golden_ref")
    if golden.get("fixture_ref") != refs["fixture_ref"] or oracle.get("fixture_ref") != refs["fixture_ref"]:
        errors.append(f"{source_name}:{row_id}: golden/oracle fixture_ref mismatch")
    if golden.get("deterministic") is not True:
        errors.append(f"{source_name}:{row_id}: C5 golden vector must be deterministic")
    if fixture.get("expected_evidence") != oracle.get("evidence_required"):
        errors.append(f"{source_name}:{row_id}: fixture expected_evidence must match oracle evidence_required")
    semantic_facts = fixture.get("semantic_facts")
    if not isinstance(semantic_facts, dict):
        errors.append(f"{source_name}:{row_id}: C5 fixture must declare semantic_facts")
    else:
        symbols = {str(mapping.get("dafny_symbol")) for mapping in row.get("coverage_mappings") or [] if mapping.get("dafny_symbol")}
        fact_symbol = semantic_facts.get("dafny_property")
        if fact_symbol and str(fact_symbol) not in symbols:
            errors.append(f"{source_name}:{row_id}: fixture semantic_facts.dafny_property is not linked by the C5 row")
        for required_key in row.get("required_fixture_fact_keys") or []:
            if required_key not in semantic_facts:
                errors.append(f"{source_name}:{row_id}: C5 fixture semantic_facts lacks {required_key}")
    for golden_field, oracle_field in (
        ("expected_decisions", "expected_decisions"),
        ("expected_state_transitions", "expected_state_transitions"),
        ("expected_audit_sequence", "expected_audit_records"),
        ("expected_final_state", "expected_final_state"),
    ):
        if golden.get(golden_field) != oracle.get(oracle_field):
            errors.append(f"{source_name}:{row_id}: golden {golden_field} must mirror embedded oracle")
    failure = oracle.get("expected_failure") if isinstance(oracle.get("expected_failure"), dict) else {}
    if golden.get("expected_failure_mode") != failure.get("error_code"):
        errors.append(f"{source_name}:{row_id}: golden expected_failure_mode must mirror embedded oracle failure")
    if str(row.get("test_type")) == "negative":
        output = golden.get("expected_normalized_output") if isinstance(golden.get("expected_normalized_output"), dict) else {}
        if output.get("outcome") == "EXPECTED_SUCCESS":
            errors.append(f"{source_name}:{row_id}: negative row must not be marked success")
        if failure.get("fail_closed") is not True:
            errors.append(f"{source_name}:{row_id}: expected fail_closed true")
    for mapping in row.get("coverage_mappings") or []:
        evidence_ref = mapping.get("evidence_ref")
        if evidence_ref and str(evidence_ref).startswith("EV-") and evidence_ref not in (oracle.get("evidence_required") or []):
            errors.append(f"{source_name}:{row_id}: mapping evidence_ref is not required by embedded oracle")


def validate_rows(source_name: str, rows: list[dict[str, Any]], errors: list[str]) -> None:
    for row in rows:
        row_id = row_name(row)
        row_level = str(row.get("coverage_level"))
        mappings = row.get("coverage_mappings") or []
        if row_level not in LEVEL_RANK:
            errors.append(f"{source_name}:{row_id}: unknown coverage level {row_level}")
            continue
        if source_name == "requirement-to-dafny.yml":
            req_id = str(row.get("requirement_id"))
            is_phase_subclaim = bool(row.get("subclaim_id"))
            if row.get("phase_scope") != "phase-1-4-1":
                errors.append(f"{source_name}:{row_id}: Phase 1.4.1 requirement row must declare phase_scope")
            if row.get("partial_coverage") is True and level_rank(row_level) >= level_rank("C4_VERIFIED_PROPERTY"):
                errors.append(f"{source_name}:{row_id}: partial parent requirement must not claim C4/C5/C6")
            if (
                req_id in BROAD_PARENT_REQUIREMENTS_REQUIRING_SUBCLAIMS
                and not is_phase_subclaim
                and level_rank(row_level) >= level_rank("C4_VERIFIED_PROPERTY")
                and row.get("full_requirement_modeled") is not True
            ):
                errors.append(f"{source_name}:{row_id}: broad parent requirement must not claim C4/C5/C6 without full_requirement_modeled")
            if is_phase_subclaim and not row.get("covered_subclaim"):
                errors.append(f"{source_name}:{row_id}: phase-scoped requirement subclaim must describe covered_subclaim")
        if row_level in SEMANTIC_LEVELS and not mappings:
            errors.append(f"{source_name}:{row_id}: semantic row lacks coverage_mappings")
            continue
        for mapping in mappings:
            if row_level in PROOF_LEVELS and mapping.get("verification_status") != "verified":
                errors.append(f"{source_name}:{row_id}: C4/C5 mapping not verified")
            if not mapping.get("evidence_ref"):
                errors.append(f"{source_name}:{row_id}: semantic mapping lacks evidence_ref")
            if str(mapping.get("coverage_level")) not in LEVEL_RANK:
                errors.append(f"{source_name}:{row_id}: mapping has unknown coverage level {mapping.get('coverage_level')}")
            if level_rank(mapping.get("coverage_level")) < level_rank(row_level):
                errors.append(f"{source_name}:{row_id}: mapping coverage level below row coverage level")
            module_path = ROOT / str(mapping.get("dafny_module", ""))
            if not module_path.exists():
                errors.append(f"{source_name}:{row_id}: missing Dafny module {module_path}")
            elif mapping.get("dafny_symbol"):
                text = module_path.read_text(encoding="utf-8")
                if not exact_dafny_symbol_declared(text, str(mapping["dafny_symbol"]), str(mapping.get("symbol_kind") or "lemma")):
                    errors.append(f"{source_name}:{row_id}: Dafny symbol {mapping['dafny_symbol']} not declared")
        expected_symbols = {str(symbol) for symbol in row.get("expected_dafny_symbols") or []}
        if expected_symbols:
            symbols = {str(mapping.get("dafny_symbol")) for mapping in mappings}
            missing = expected_symbols - symbols
            if missing:
                errors.append(f"{source_name}:{row_id}: missing expected Dafny symbol links: {', '.join(sorted(missing))}")
        if row_level == "C4_VERIFIED_PROPERTY" and (row.get("fixture_ref") or row.get("oracle_ref") or row.get("golden_ref")):
            errors.append(f"{source_name}:{row_id}: C4 row must not carry fixture/oracle/golden refs")
        if row_level == "C5_CONFORMANCE_LINKED":
            validate_c5_links(source_name, row, errors)


def validate_aggregate(source_name: str, data: dict[str, Any], errors: list[str]) -> None:
    rows = data.get("entries") or data.get("tests") or data.get("fixtures") or data.get("requirements") or data.get("formal_claims") or []
    if not isinstance(rows, list):
        errors.append(f"{source_name}: rows must be a list")
        return
    if rows and "coverage_level" not in data:
        errors.append(f"{source_name}: aggregate coverage_level is required when rows are present")
    elif "coverage_level" in data and str(data.get("coverage_level")) not in LEVEL_RANK:
        errors.append(f"{source_name}: unknown aggregate coverage level {data.get('coverage_level')}")
    worst = min((str(row.get("coverage_level")) for row in rows), key=lambda level: LEVEL_RANK.get(level, -1)) if rows else "C0_NONE"
    if level_rank(data.get("coverage_level")) > level_rank(worst):
        errors.append(f"{source_name}: aggregate {data.get('coverage_level')} exceeds child aggregate {worst}")
    validate_rows(source_name, rows, errors)


def collect_mapped_symbols() -> dict[str, list[tuple[str, str, dict[str, Any]]]]:
    symbols: dict[str, list[tuple[str, str, dict[str, Any]]]] = {}
    for name in TRACE_FILES:
        data = load_yaml(TRACEABILITY_DIR / name)
        rows = data.get("entries") or data.get("tests") or data.get("fixtures") or data.get("requirements") or data.get("formal_claims") or []
        if not isinstance(rows, list):
            continue
        for row in rows:
            for mapping in row.get("coverage_mappings") or []:
                symbol = mapping.get("dafny_symbol")
                if symbol:
                    symbols.setdefault(str(symbol), []).append((name, str(row.get("coverage_level")), row))
    return symbols


def validate_bound_decision_traceability(errors: list[str]) -> None:
    mapped = collect_mapped_symbols()
    for symbol in sorted(REQUIRED_BOUND_DD_SYMBOLS):
        rows = mapped.get(symbol) or []
        if not rows:
            errors.append(f"Phase 1.4.1 binding-strengthened symbol lacks traceability row: {symbol}")
            continue
        if not any(level_rank(level) >= level_rank("C4_VERIFIED_PROPERTY") for _, level, _ in rows):
            errors.append(f"Phase 1.4.1 binding-strengthened symbol must be C4 or higher: {symbol}")
        for source_name, level, row in rows:
            if level == "C4_VERIFIED_PROPERTY" and (row.get("fixture_ref") or row.get("oracle_ref") or row.get("golden_ref")):
                errors.append(f"{source_name}:{row_name(row)}: C4 binding row for {symbol} must not carry fixture/oracle/golden refs")


def validate_policy_boundaries(errors: list[str]) -> None:
    job_text = (ROOT / "formal/executable-semantics/dafny/modules/job_spool.dfy").read_text(encoding="utf-8")
    type_text = (ROOT / "formal/executable-semantics/dafny/modules/types.dfy").read_text(encoding="utf-8")
    required_refs = [
        "DatasetCatalog.MayCreateDatasetHandle",
        "DatasetCatalog.CreateDatasetHandle",
        "Authorization.CanCreateProtectedResourceHandle",
        "DatasetCatalog.DeniedDatasetOpenWithAudit",
    ]
    for ref in required_refs:
        if ref not in job_text:
            errors.append(f"job_spool.dfy must reference {ref}")
    required_bound_surface = {
        "types.dfy": [
            "datatype EffectiveJobContext",
            "datatype BoundDDDecision",
        ],
        "job_spool.dfy": [
            "predicate EffectiveJobContextValid",
            "predicate IsBoundDDDecision",
            "predicate BoundDDDecisionValid",
            "predicate BoundDDDecisionDeniesWithAudit",
            "function DDResolutionFailureError(bound: BoundDDDecision",
            "function ResolveDDForJob(bound: BoundDDDecision",
            "function DeniedDDResolutionWithAudit(bound: BoundDDDecision",
            "Authorization.DecisionWellFormed(decision)",
            "decision.context.correlation_id == ctx.correlation_id",
            "decision.context.correlation_id == ctx.effective.value.correlation_id",
            "bound.decision.context.object_generation == entry.catalog_generation",
        ],
    }
    for marker in required_bound_surface["types.dfy"]:
        if marker not in type_text:
            errors.append(f"types.dfy missing binding-strengthened DD surface marker: {marker}")
    for marker in required_bound_surface["job_spool.dfy"]:
        if marker not in job_text:
            errors.append(f"job_spool.dfy missing binding-strengthened DD surface marker: {marker}")
    forbidden_raw_surfaces = [
        "function ResolveDDForJob(ctx: JobContext",
        "function DDResolutionFailureError(ctx: JobContext",
        "function DeniedDDResolutionWithAudit(dd: DD, decision: SecurityDecision",
    ]
    for marker in forbidden_raw_surfaces:
        if marker in job_text:
            errors.append(f"job_spool.dfy still exposes raw DD decision surface: {marker}")
    for forbidden in (
        ROOT / "formal" / "executable-semantics" / "rust",
        ROOT / "implementation" / "services" / "jobd",
        ROOT / "implementation" / "services" / "spoold",
        ROOT / "implementation" / "services" / "operatord",
    ):
        if forbidden.exists():
            errors.append(f"Phase 1.4.1 must not introduce Rust semantic-core or daemon implementation artifact: {forbidden}")
    for path in sorted((ROOT / "reports/current").glob("*phase-1-4-1*")):
        errors.append(f"Phase 1.4.1 report must not be under reports/current: {path}")


def validate_python_boundary(errors: list[str]) -> None:
    for rel in (
        "scripts/generators/generate-job-dd-coverage.py",
        "scripts/phases/phase-1/check-phase1-4-1-job-dd-coverage.py",
    ):
        text = (ROOT / rel).read_text(encoding="utf-8")
        forbidden = [
            r"if\s+.*\.get\(['\"]operation['\"]\)\s*==",
            r"if\s+.*ValidJobTransition",
            r"if\s+.*DDResolutionPreconditions",
            r"if\s+.*CanCreateProtectedResourceHandle",
            r"if\s+.*MayCreateDatasetHandle",
        ]
        for pattern in forbidden:
            if re.search(pattern, text):
                errors.append(f"{rel}: Python tooling appears to evaluate Job/DD business semantics: {pattern}")


def main() -> int:
    errors = compare_generated()
    for name in TRACE_FILES:
        data = load_yaml(TRACEABILITY_DIR / name)
        validate_aggregate(name, data, errors)
    formal = load_yaml(TRACEABILITY_DIR / "formal-claim-to-dafny.yml")
    for claim in formal.get("formal_claims", []) or []:
        if claim.get("coverage_level") in PROOF_LEVELS:
            errors.append(f"{claim.get('claim_id')}: formal claim must not be C4/C5/C6 without proof artifacts")
        if claim.get("proof_claimed") or claim.get("proof_artifact_refs"):
            errors.append(f"{claim.get('claim_id')}: Phase 1.4.1 must not invent formal proof artifacts")
    validate_bound_decision_traceability(errors)
    validate_policy_boundaries(errors)
    validate_python_boundary(errors)
    if errors:
        for error in errors:
            print(f"phase1.4.1 job/dd coverage error: {error}", file=sys.stderr)
        return 1
    print("Phase 1.4.1 Job/DD coverage check OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
