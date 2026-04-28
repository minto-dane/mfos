#!/usr/bin/env python3
"""Validate MFOS Phase 0.6 pack contracts."""

from __future__ import annotations

from mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg


PACK_INDEX = ROOT / "packs/pack-index.yml"
REQUIRED = {
    "pack_id",
    "title",
    "purpose",
    "scope",
    "non_objectives",
    "depends_on",
    "inputs",
    "outputs",
    "source_refs",
    "requirements",
    "object_model_refs",
    "state_machine_refs",
    "failure_modes",
    "audit_obligations",
    "positive_tests",
    "negative_tests",
    "fuzz_targets",
    "spec_gaps",
    "implementation_allowed",
    "prompt",
}


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    if not PACK_INDEX.exists():
        findings.append(Finding("ERROR", PACK_INDEX, "pack-index.yml missing"))
        return emit(findings, args.mode, "Pack validation OK")

    data = load_yaml(PACK_INDEX)
    if not isinstance(data, dict):
        findings.append(Finding("ERROR", PACK_INDEX, "pack index must be a mapping"))
        return emit(findings, args.mode, "Pack validation OK")
    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        findings.append(Finding("ERROR", PACK_INDEX, "entries must be a non-empty list"))
        return emit(findings, args.mode, "Pack validation OK")

    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            findings.append(Finding("ERROR", PACK_INDEX, "pack entry is not a mapping"))
            continue
        pid = str(entry.get("pack_id", "<missing>"))
        if pid in seen:
            findings.append(Finding("ERROR", PACK_INDEX, f"duplicate pack_id: {pid}"))
        seen.add(pid)
        missing = sorted(REQUIRED - set(entry))
        if missing:
            findings.append(Finding("ERROR", PACK_INDEX, f"{pid}: missing fields: {', '.join(missing)}"))
        for field in REQUIRED - {"implementation_allowed", "prompt", "purpose", "title", "pack_id"}:
            if field in entry and not isinstance(entry[field], list):
                findings.append(Finding("ERROR", PACK_INDEX, f"{pid}: {field} must be a list"))
        impl = entry.get("implementation_allowed")
        if not isinstance(impl, dict):
            findings.append(Finding("ERROR", PACK_INDEX, f"{pid}: implementation_allowed must be a mapping"))
        else:
            if impl.get("production") is not False:
                findings.append(Finding("ERROR", PACK_INDEX, f"{pid}: production implementation must be false in Phase 0.6"))
            for key in ("hosted_semantic_prototype", "production", "hardware_enforcement_claim", "system_integrity_claim"):
                if key not in impl:
                    findings.append(Finding("ERROR", PACK_INDEX, f"{pid}: implementation_allowed.{key} missing"))

    expected = {f"PACK-{idx:02d}" for idx in range(31)}
    missing_ids = sorted(expected - seen)
    if missing_ids:
        findings.append(Finding("ERROR", PACK_INDEX, f"missing pack ids: {', '.join(missing_ids)}"))

    pack07 = next((entry for entry in entries if isinstance(entry, dict) and entry.get("pack_id") == "PACK-07"), None)
    if isinstance(pack07, dict):
        required_deps = {f"PACK-{idx:02d}" for idx in range(7)}
        got = set(pack07.get("depends_on", []))
        missing_deps = sorted(required_deps - got)
        if missing_deps:
            findings.append(Finding("ERROR", PACK_INDEX, f"PACK-07 missing dependencies: {', '.join(missing_deps)}"))
    else:
        findings.append(Finding("ERROR", PACK_INDEX, "PACK-07 missing"))

    return emit(findings, args.mode, f"Pack validation OK: {len(entries)} packs checked")


if __name__ == "__main__":
    raise SystemExit(main())
