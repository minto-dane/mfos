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


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return data


def row_name(row: dict[str, Any]) -> str:
    return str(row.get("test_id") or row.get("requirement_id") or row.get("claim_id") or row.get("integration_id") or "<unknown>")


def level_rank(level: Any) -> int:
    return LEVEL_RANK.get(str(level), -1)


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
    evidence_ref = mapping.get("evidence_ref")
    if evidence_ref and evidence_ref.startswith("EV-") and evidence_ref not in (oracle.get("evidence_required") or []):
        errors.append(f"{source_name}:{row_id}: mapping evidence_ref is not required by the embedded oracle")


def validate_rows(source_name: str, rows: list[dict[str, Any]], errors: list[str]) -> None:
    for row in rows:
        row_id = row_name(row)
        row_level = row.get("coverage_level")
        mappings = row.get("coverage_mappings") or []
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
            validate_c5_links(source_name, row, mappings[0], errors)
        if str(row_id).startswith("NEG-"):
            expected_symbol = EXPECTED_NEGATIVE_SYMBOLS.get(row_id)
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
    if coverage.get("dataset_catalog_coverage_level") == "C5_CONFORMANCE_LINKED":
        below = [
            f"{row_name(row)}={row.get('coverage_level')}"
            for row in required_rows
            if row.get("coverage_level") != "C5_CONFORMANCE_LINKED"
        ]
        if below:
            errors.append("dataset_catalog_coverage_level is C5 while required child rows are below C5: " + ", ".join(below))
    validate_rows("dataset-catalog-to-dafny.yml", dataset_rows, errors)

    test_data = load_yaml(TRACEABILITY_DIR / "test-to-dafny.yml")
    validate_rows("test-to-dafny.yml", test_data.get("tests") or [], errors)

    req_data = load_yaml(TRACEABILITY_DIR / "requirement-to-dafny.yml")
    validate_rows("requirement-to-dafny.yml", req_data.get("requirements") or [], errors)

    fixture_data = load_yaml(TRACEABILITY_DIR / "fixture-to-dafny.yml")
    validate_rows("fixture-to-dafny.yml", fixture_data.get("fixtures") or [], errors)

    formal = load_yaml(TRACEABILITY_DIR / "formal-claim-to-dafny.yml")
    for claim in formal.get("formal_claims", []):
        if claim.get("coverage_level") in PROOF_LEVELS:
            errors.append(f"{claim.get('claim_id')}: formal claim must not be C4/C5/C6 without proof artifacts")
        if claim.get("proof_claimed") or claim.get("proof_artifact_refs"):
            errors.append(f"{claim.get('claim_id')}: Phase 1.3 must not invent proof artifacts")
    validate_rows("formal-claim-to-dafny.yml", formal.get("formal_claims") or [], errors)

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
