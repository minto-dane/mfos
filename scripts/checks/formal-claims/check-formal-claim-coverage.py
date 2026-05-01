#!/usr/bin/env python3
"""Validate formal-claim coverage does not outrun proof registry status."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "scripts").is_dir() and (parent / "docs").is_dir())
CLAIM_REGISTRY = ROOT / "formal" / "claim-registry.yml"
FORMAL_COVERAGE = ROOT / "evidence" / "traceability" / "generated" / "phase-1-1" / "formal-claim-to-dafny.yml"
SUMMARY = ROOT / "reports" / "generated" / "phase-1-1" / "semantic-coverage.yml"
PROOF_LEVELS = {"C4_VERIFIED_PROPERTY", "C5_CONFORMANCE_LINKED", "C6_RELEASE_READY_MODEL"}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return data


def main() -> int:
    errors: list[str] = []
    registry = load_yaml(CLAIM_REGISTRY)
    coverage = load_yaml(FORMAL_COVERAGE)
    summary = load_yaml(SUMMARY)

    registry_proof_claimed = bool(registry.get("proof_claimed"))
    claims_by_id = {claim["claim_id"]: claim for claim in registry.get("claims", [])}

    for item in coverage.get("formal_claims", []):
        claim_id = item.get("claim_id")
        level = item.get("coverage_level")
        source_claim = claims_by_id.get(claim_id, {})
        proof_artifacts = item.get("proof_artifact_refs") or source_claim.get("proof_artifact_refs") or []
        if level in PROOF_LEVELS:
            if not registry_proof_claimed:
                errors.append(f"{claim_id}: {level} is forbidden while claim registry proof_claimed is false")
            if source_claim.get("status") in {"planned", "draft"}:
                errors.append(f"{claim_id}: {level} is forbidden while registry status is {source_claim.get('status')}")
            if not proof_artifacts:
                errors.append(f"{claim_id}: {level} is forbidden without proof_artifact_refs")

    formal_complete = bool(summary.get("phase_1_1_formal_claim_coverage_complete"))
    if formal_complete and not registry_proof_claimed:
        errors.append("semantic-coverage.yml claims formal coverage complete while registry proof_claimed is false")

    if errors:
        for error in errors:
            print(f"formal claim coverage error: {error}", file=sys.stderr)
        return 1
    print("Formal claim coverage check OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
