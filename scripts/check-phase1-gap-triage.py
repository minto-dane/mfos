#!/usr/bin/env python3
"""Validate Phase 1.1 gap triage and Phase 1.2 entry gate consistency."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any
import sys

import yaml


ROOT = Path(__file__).resolve().parent.parent
TRACE = ROOT / "evidence" / "traceability" / "generated" / "phase-1-1"
TRIAGE = ROOT / "reports" / "current" / "phase-1-1-gap-triage.yml"
GATE = ROOT / "reports" / "current" / "phase-1-2-entry-gate.yml"
STATUS = ROOT / "docs" / "design" / "STATUS.md"
REPORT_INDEX = ROOT / "reports" / "index.yml"
GAP_LEVELS = {"C0_NONE", "C1_TYPE_ONLY", "C2_PARTIAL_SEMANTIC", "C3_FULL_SEMANTIC"}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return data


def expected_gaps() -> list[tuple[str, str, str]]:
    gaps: list[tuple[str, str, str]] = []
    tests = load_yaml(TRACE / "test-to-dafny.yml")
    for item in tests.get("tests", []):
        if item.get("coverage_level") in GAP_LEVELS:
            gaps.append(("test", item["test_id"], item["coverage_level"]))
    reqs = load_yaml(TRACE / "requirement-to-dafny.yml")
    for item in reqs.get("requirements", []):
        if item.get("coverage_level") in GAP_LEVELS:
            gaps.append(("requirement", item["requirement_id"], item["coverage_level"]))
    claims = load_yaml(TRACE / "formal-claim-to-dafny.yml")
    for item in claims.get("formal_claims", []):
        if item.get("coverage_level") in GAP_LEVELS:
            gaps.append(("formal_claim", item["claim_id"], item["coverage_level"]))
    return gaps


def main() -> int:
    errors: list[str] = []
    triage = load_yaml(TRIAGE)
    gate = load_yaml(GATE)
    status_text = STATUS.read_text(encoding="utf-8")
    report_index = REPORT_INDEX.read_text(encoding="utf-8")

    expected = set(expected_gaps())
    actual = {
        (item.get("artifact_kind"), item.get("artifact_id"), item.get("coverage_level"))
        for item in triage.get("gaps", [])
    }
    missing = expected - actual
    extra = actual - expected
    for kind, artifact_id, level in sorted(missing):
        errors.append(f"triage missing {kind} gap {artifact_id} at {level}")
    for kind, artifact_id, level in sorted(extra):
        errors.append(f"triage contains stale/unexpected {kind} gap {artifact_id} at {level}")

    classifications = Counter(item.get("classification") for item in triage.get("gaps", []))
    if dict(classifications) != triage.get("classification_counts"):
        errors.append("classification_counts does not match gaps")
    levels = Counter(item.get("coverage_level") for item in triage.get("gaps", []))
    if dict(levels) != triage.get("coverage_level_counts"):
        errors.append("coverage_level_counts does not match gaps")
    kinds = Counter(item.get("artifact_kind") for item in triage.get("gaps", []))
    if dict(kinds) != triage.get("artifact_kind_counts"):
        errors.append("artifact_kind_counts does not match gaps")

    auth_audit = [item for item in triage.get("gaps", []) if item.get("domain") in {"authorization", "audit"}]
    if any(item.get("classification") == "accepted_deferred" for item in auth_audit):
        errors.append("Authorization/Audit gap is incorrectly accepted_deferred")

    entry_blockers = [item for item in triage.get("gaps", []) if item.get("phase_1_2_entry_blocker")]
    merge_blockers = [item for item in triage.get("gaps", []) if item.get("phase_1_2_merge_blocker")]
    if len(entry_blockers) != triage.get("phase_1_2_entry_blocker_count"):
        errors.append("phase_1_2_entry_blocker_count does not match gaps")
    if len(merge_blockers) != triage.get("phase_1_2_merge_blocker_count"):
        errors.append("phase_1_2_merge_blocker_count does not match gaps")
    if triage.get("phase_1_2_entry_allowed") and entry_blockers:
        errors.append("phase_1_2_entry_allowed is true while entry blockers exist")
    if gate.get("merge_blockers") != merge_blockers:
        errors.append("entry gate merge blockers differ from triage merge blockers")
    if gate.get("entry_blockers") != entry_blockers:
        errors.append("entry gate entry blockers differ from triage entry blockers")
    if gate.get("phase_1_2_entry_allowed") != triage.get("phase_1_2_entry_allowed"):
        errors.append("entry gate allowed flag differs from triage")

    required_status_terms = [
        "phase_1_1_gap_triage_complete: true",
        "phase_1_2_authorization_audit_deepening_allowed: true",
        "phase_1_2_authorization_audit_merge_blockers_remaining: true",
    ]
    for term in required_status_terms:
        if term not in status_text:
            errors.append(f"STATUS.md missing {term}")
    for path in (
        "reports/current/phase-1-1-gap-triage.md",
        "reports/current/phase-1-1-gap-triage.yml",
        "reports/current/phase-1-2-entry-gate.md",
        "reports/current/phase-1-2-entry-gate.yml",
    ):
        if path not in report_index:
            errors.append(f"reports/index.yml missing {path}")

    if errors:
        for error in errors:
            print(f"phase1 gap triage error: {error}", file=sys.stderr)
        return 1
    print("Phase 1.1 gap triage check OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
