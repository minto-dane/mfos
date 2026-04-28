#!/usr/bin/env python3
"""Validate Phase 0.8 cross-artifact traceability.

This is a design-time guard. It does not execute tests and does not authorize
production, hosted daemon, portable semantic core, or executable-spec work.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "evidence/traceability/archive/phase-0-8/requirement-to-test.yml"
CATALOG_DIR = ROOT / "tests/catalog"
FVS_SPEC = ROOT / "docs/design/specs/30-first-vertical-slice-contract.md"
GAP_REPORT = ROOT / "evidence/traceability/archive/phase-0-8/gap-report.yml"

PACK_SPEC_MAP = {
    "PACK-05": ROOT / "docs/design/specs/06-authorization.md",
    "PACK-06": ROOT / "docs/design/specs/07-audit.md",
    "PACK-07": ROOT / "docs/design/specs/08-dataset-catalog.md",
    "PACK-08": ROOT / "docs/design/specs/09-job-spool.md",
    "PACK-09": ROOT / "docs/design/specs/10-operator-console.md",
}

PACK_FILES = {
    "PACK-05": ROOT / "docs/design/packs/PACK-05-authorization-model/pack.yml",
    "PACK-06": ROOT / "docs/design/packs/PACK-06-audit-schema/pack.yml",
    "PACK-07": ROOT / "docs/design/packs/PACK-07-dataset-catalog/pack.yml",
    "PACK-08": ROOT / "docs/design/packs/PACK-08-job-spool/pack.yml",
    "PACK-09": ROOT / "docs/design/packs/PACK-09-operator-console/pack.yml",
}


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def front_matter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    try:
        raw = text.split("---", 2)[1]
    except IndexError:
        return {}
    return yaml.safe_load(raw) or {}


def collect_tests(node: Any, out: dict[str, dict[str, Any]]) -> None:
    if isinstance(node, dict):
        test_id = node.get("test_id")
        if isinstance(test_id, str):
            out[test_id] = node
        for value in node.values():
            collect_tests(value, out)
    elif isinstance(node, list):
        for value in node:
            collect_tests(value, out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="draft", choices=["draft", "release"])
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    trace = load_yaml(TRACE)
    required_tests: set[str] = set()
    for entry in trace.get("entries", []) or []:
        for key in ("positive_tests", "negative_tests"):
            for test_id in entry.get(key, []) or []:
                required_tests.add(test_id)

    catalog_tests: dict[str, dict[str, Any]] = {}
    for catalog in sorted((CATALOG_DIR / "archive/phase-0-8").glob("*.yml")):
        data = load_yaml(catalog)
        collect_tests(data, catalog_tests)
        if data.get("implementation_allowed") is not False:
            errors.append(f"{catalog.relative_to(ROOT)} must set implementation_allowed: false")

    missing = sorted(required_tests - set(catalog_tests))
    if missing:
        errors.append(
            "Phase 0.8 traceability references uncataloged tests: "
            + ", ".join(missing[:20])
            + (" ..." if len(missing) > 20 else "")
        )
    for test_id in sorted(required_tests & set(catalog_tests)):
        test = catalog_tests[test_id]
        joined = " ".join(
            str(test.get(field, "")) for field in ("title", "input", "expected_decision", "expected_result")
        )
        if "traceability alias" in joined or "Design-level fixture" in joined:
            errors.append(f"{test_id} is still a generic alias placeholder, not a concrete planned test")
        if not test.get("target_requirements") and not test.get("requirement_ids"):
            errors.append(f"{test_id} must link target_requirements or requirement_ids")
        if not test.get("evidence_required") and not test.get("evidence_ids") and not test.get("evidence"):
            errors.append(f"{test_id} must declare evidence_required/evidence_ids/evidence")

    fvs = front_matter(FVS_SPEC)
    if "MFOS-REQ-AUDIT-0104" not in (fvs.get("requirement_refs") or []):
        errors.append("First vertical slice front matter must reference MFOS-REQ-AUDIT-0104")

    gap = load_yaml(GAP_REPORT)
    if gap.get("implementation_blocking_gaps") in (None, []):
        errors.append("Phase 0.8 gap report must list implementation_blocking_gaps")

    for pack_id, spec_path in PACK_SPEC_MAP.items():
        spec_refs = set(front_matter(spec_path).get("source_refs") or [])
        pack = load_yaml(PACK_FILES[pack_id])
        pack_refs = set(pack.get("source_refs") or [])
        missing_refs = sorted(spec_refs - pack_refs)
        extra_refs = sorted(pack_refs - spec_refs)
        if missing_refs:
            errors.append(f"{pack_id} source_refs missing owning spec refs: {', '.join(missing_refs)}")
        if extra_refs:
            errors.append(f"{pack_id} source_refs include stale refs not present in owning spec: {', '.join(extra_refs)}")
        impl = pack.get("implementation_allowed") or {}
        for key in ("production", "hosted_daemon", "portable_semantic_core", "executable_spec"):
            if impl.get(key) is not False:
                errors.append(f"{pack_id} implementation_allowed.{key} must be false")
        if impl.get("specification_only") is not True:
            errors.append(f"{pack_id} must set implementation_allowed.specification_only: true")

    for warning in warnings:
        print(f"WARN: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Phase 0.8 traceability check passed in {args.mode} mode.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
