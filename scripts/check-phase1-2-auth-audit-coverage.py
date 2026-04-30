#!/usr/bin/env python3
"""Validate Phase 1.2 Authorization/Audit coverage artifacts."""

from __future__ import annotations

import filecmp
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent.parent
TRACEABILITY_DIR = ROOT / "evidence" / "traceability" / "generated" / "phase-1-2"
REPORTS_DIR = ROOT / "reports" / "current"
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


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return data


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
            if row.get("coverage_level") in SEMANTIC_LEVELS:
                mappings = row.get("coverage_mappings", [])
                if not mappings:
                    errors.append(f"{name}:{row.get('test_id') or row.get('requirement_id')}: semantic row lacks mappings")
                for mapping in mappings:
                    if not mapping.get("dafny_symbol"):
                        errors.append(f"{name}:{row.get('test_id') or row.get('requirement_id')}: semantic mapping lacks dafny_symbol")
                    if row.get("coverage_level") in PROOF_LEVELS and mapping.get("verification_status") != "verified":
                        errors.append(f"{name}:{row.get('test_id') or row.get('requirement_id')}: C4/C5 mapping not verified")
                    if not mapping.get("evidence_ref"):
                        errors.append(f"{name}:{row.get('test_id') or row.get('requirement_id')}: semantic mapping lacks evidence_ref")
                    module_path = ROOT / str(mapping.get("dafny_module", ""))
                    if not module_path.exists():
                        errors.append(f"{name}:{row.get('test_id') or row.get('requirement_id')}: Dafny module does not exist: {module_path}")
                    elif mapping.get("dafny_symbol") and mapping["dafny_symbol"] not in module_path.read_text(encoding="utf-8"):
                        errors.append(f"{name}:{row.get('test_id') or row.get('requirement_id')}: Dafny symbol {mapping['dafny_symbol']} not found in {module_path}")
                if row.get("coverage_level") == "C5_CONFORMANCE_LINKED":
                    for key in ("fixture_ref", "oracle_ref", "golden_ref"):
                        ref = row.get(key)
                        if not ref:
                            errors.append(f"{name}:{row.get('test_id') or row.get('requirement_id')}: C5 row lacks {key}")
                        elif not (ROOT / ref).exists():
                            errors.append(f"{name}:{row.get('test_id') or row.get('requirement_id')}: referenced {key} does not exist: {ref}")

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
