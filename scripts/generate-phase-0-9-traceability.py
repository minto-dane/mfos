#!/usr/bin/env python3
"""Generate Phase 0.9 executable-spec traceability matrices."""

from __future__ import annotations

from collections import defaultdict

from mfos_phase09 import (
    FUZZ_PLAN,
    GOLDEN_DIR,
    ROOT,
    all_catalog_entries,
    as_list,
    load_yaml,
    rel,
    write_yaml,
    yaml_files,
)


OUT = ROOT / "evidence/traceability"


def main() -> int:
    req_to_test: dict[str, list[str]] = defaultdict(list)
    test_to_fixture: dict[str, dict[str, str]] = {}
    fixture_to_oracle: dict[str, dict[str, str]] = {}
    gaps: list[dict[str, str]] = []

    for catalog_path, entry in all_catalog_entries():
        test_id = str(entry.get("test_id"))
        for req in as_list(entry.get("target_requirements")):
            req_to_test[str(req)].append(test_id)
        fixture_ref = str(entry.get("fixture_ref", ""))
        oracle_ref = str(entry.get("oracle_ref", ""))
        golden_ref = str(entry.get("golden_ref", ""))
        test_to_fixture[test_id] = {
            "catalog": rel(catalog_path),
            "fixture_ref": fixture_ref,
            "oracle_ref": oracle_ref,
            "golden_ref": golden_ref,
        }
        for kind, ref in (("fixture_ref", fixture_ref), ("golden_ref", golden_ref)):
            if ref and not (ROOT / ref).exists():
                gaps.append({"gap_type": "missing_fixture" if kind == "fixture_ref" else "missing_oracle", "artifact": ref, "test_id": test_id})

    for path in yaml_files(GOLDEN_DIR):
        data = load_yaml(path)
        oracle = data.get("oracle", {}) if isinstance(data, dict) else {}
        fixture_ref = str(data.get("fixture_ref", ""))
        if fixture_ref:
            fixture_to_oracle[fixture_ref] = {
                "golden_ref": rel(path),
                "oracle_id": str(oracle.get("oracle_id", "")),
            }

    req_to_fuzz: dict[str, list[str]] = defaultdict(list)
    if FUZZ_PLAN.exists():
        data = load_yaml(FUZZ_PLAN)
        for target in as_list(data.get("targets")):
            if isinstance(target, dict):
                target_id = str(target.get("target_id"))
                for req in as_list(target.get("target_requirements")):
                    req_to_fuzz[str(req)].append(target_id)
    else:
        gaps.append({"gap_type": "missing_fuzz_target", "artifact": rel(FUZZ_PLAN), "test_id": ""})

    write_yaml(
        OUT / "phase-0-9-requirement-to-test.yml",
        {"traceability_kind": "phase_0_9_requirement_to_test", "entries": [{"requirement_id": k, "tests": sorted(v)} for k, v in sorted(req_to_test.items())]},
    )
    write_yaml(
        OUT / "phase-0-9-test-to-fixture.yml",
        {"traceability_kind": "phase_0_9_test_to_fixture", "entries": [{"test_id": k, **v} for k, v in sorted(test_to_fixture.items())]},
    )
    write_yaml(
        OUT / "phase-0-9-fixture-to-oracle.yml",
        {"traceability_kind": "phase_0_9_fixture_to_oracle", "entries": [{"fixture_ref": k, **v} for k, v in sorted(fixture_to_oracle.items())]},
    )
    write_yaml(
        OUT / "phase-0-9-requirement-to-fuzz-target.yml",
        {"traceability_kind": "phase_0_9_requirement_to_fuzz_target", "entries": [{"requirement_id": k, "fuzz_targets": sorted(v)} for k, v in sorted(req_to_fuzz.items())]},
    )
    write_yaml(
        OUT / "phase-0-9-gap-report.yml",
        {
            "traceability_kind": "phase_0_9_gap_report",
            "status": "generated",
            "gap_classes": [
                "missing_test",
                "missing_fixture",
                "missing_oracle",
                "missing_negative_test",
                "missing_audit_expectation",
                "missing_failure_mode",
                "missing_fuzz_target",
                "source_gap",
                "spec_gap",
                "naming_safety_gap",
            ],
            "entries": gaps,
        },
    )
    print("Phase 0.9 traceability generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
