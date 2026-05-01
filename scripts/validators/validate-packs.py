#!/usr/bin/env python3
"""Validate MFOS Phase 0.6 pack contracts."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg


PACK_INDEX = ROOT / "packs/pack-index.yml"
CANONICAL_PACK_ROOT = ROOT / "docs/design/packs"
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
CANONICAL_SYNC_FIELDS = REQUIRED - {"implementation_allowed"}


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

    if data.get("bridge_only") is not True:
        findings.append(Finding("ERROR", PACK_INDEX, "top-level pack-index.yml must declare bridge_only: true"))
    if data.get("canonical_source") != "docs/design/packs":
        findings.append(Finding("ERROR", PACK_INDEX, "top-level pack-index.yml must declare canonical_source: docs/design/packs"))

    seen: set[str] = set()
    by_id: dict[str, dict[str, object]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            findings.append(Finding("ERROR", PACK_INDEX, "pack entry is not a mapping"))
            continue
        pid = str(entry.get("pack_id", "<missing>"))
        if pid in seen:
            findings.append(Finding("ERROR", PACK_INDEX, f"duplicate pack_id: {pid}"))
        seen.add(pid)
        by_id[pid] = entry
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

    expected = {f"PACK-{idx:02d}" for idx in range(38)}
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

    for canonical_path in sorted(CANONICAL_PACK_ROOT.glob("PACK-*/pack.yml")):
        canonical = load_yaml(canonical_path)
        if not isinstance(canonical, dict):
            findings.append(Finding("ERROR", canonical_path, "canonical pack contract must be a mapping"))
            continue
        pid = str(canonical.get("pack_id", "<missing>"))
        bridge = by_id.get(pid)
        if bridge is None:
            findings.append(Finding("ERROR", PACK_INDEX, f"{pid}: canonical pack is missing from bridge projection"))
            continue
        for field in sorted(CANONICAL_SYNC_FIELDS):
            canonical_value = canonical.get(field)
            bridge_value = bridge.get(field)
            if isinstance(canonical_value, list) and isinstance(bridge_value, list):
                if sorted(str(item) for item in canonical_value) != sorted(str(item) for item in bridge_value):
                    findings.append(Finding("ERROR", PACK_INDEX, f"{pid}: bridge projection drifts from canonical {canonical_path.relative_to(ROOT)} field {field}"))
            elif canonical_value != bridge_value:
                findings.append(Finding("ERROR", PACK_INDEX, f"{pid}: bridge projection drifts from canonical {canonical_path.relative_to(ROOT)} field {field}"))
        canonical_impl = canonical.get("implementation_allowed")
        bridge_impl = bridge.get("implementation_allowed")
        if isinstance(canonical_impl, dict) and isinstance(bridge_impl, dict):
            for key, value in canonical_impl.items():
                if bridge_impl.get(key) != value:
                    findings.append(Finding("ERROR", PACK_INDEX, f"{pid}: bridge implementation_allowed.{key} drifts from canonical {canonical_path.relative_to(ROOT)}"))

    return emit(findings, args.mode, f"Pack validation OK: {len(entries)} packs checked")


if __name__ == "__main__":
    raise SystemExit(main())
