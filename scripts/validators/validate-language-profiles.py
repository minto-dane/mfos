#!/usr/bin/env python3
"""Validate MFOS language-assurance profile documentation structure."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, REQUIREMENTS, ROOT, emit, load_yaml, mode_arg, parse_front_matter


SPEC = ROOT / "docs/design/specs/39-language-and-verification-policy.md"
BRIDGE = ROOT / "requirements/by-domain/language.yml"
CATALOG = ROOT / "tests/catalog/language-verification.yml"

REQUIRED_PROFILES = {"LAP-0", "LAP-1", "LAP-2", "LAP-3", "LAP-4"}
REQUIRED_SPEC_PHRASES = {
    "Language Assurance Profiles",
    "Component Language Matrix",
    "Dafny Executable-semantics Policy",
    "Unsafe Exception Policy",
    "Assembly Boundary Policy",
    "C/C++ Exception Policy",
    "CFI Evidence Policy",
    "CET Evidence Policy",
    "clang CFI for C/C++ Boundaries",
    "Toolchain Pinning",
    "Static Analysis Policy",
    "Overclaim Bans",
    "MFOS_ERR_SPEC_GAP",
}


def _registry_requirements() -> dict[str, dict[str, object]]:
    data = load_yaml(REQUIREMENTS)
    if not isinstance(data, dict):
        return {}
    return {
        entry["requirement_id"]: entry
        for entry in data.get("entries", [])
        if isinstance(entry, dict) and isinstance(entry.get("requirement_id"), str)
    }


def _language_requirements_from_registry() -> set[str]:
    return {req_id for req_id in _registry_requirements() if req_id.startswith("MFOS-REQ-LANG-")}


def _as_strings(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    if not SPEC.exists():
        findings.append(Finding("ERROR", SPEC, "language verification policy spec missing"))
        return emit(findings, args.mode, "Language profile validation OK")

    front_matter, front_matter_error = parse_front_matter(SPEC)
    if front_matter_error:
        findings.append(Finding("ERROR", SPEC, f"invalid front matter: {front_matter_error}"))
        front_matter = {}
    elif front_matter is None:
        findings.append(Finding("ERROR", SPEC, "missing front matter"))
        front_matter = {}

    if front_matter.get("implementation_allowed") is not False:
        findings.append(Finding("ERROR", SPEC, "implementation_allowed must be false"))
    if front_matter.get("spec_gap_policy") != "implementation_must_not_infer_or_fill_gaps":
        findings.append(Finding("ERROR", SPEC, "spec_gap_policy must require no inferred gap filling"))
    for req in ("MFOS-REQ-LANG-*", "MFOS-REQ-FORMAL-*"):
        if req not in _as_strings(front_matter.get("requirement_refs")):
            findings.append(Finding("ERROR", SPEC, f"front matter missing requirement ref {req}"))

    text = SPEC.read_text(encoding="utf-8")
    for phrase in sorted(REQUIRED_SPEC_PHRASES):
        if phrase not in text:
            findings.append(Finding("ERROR", SPEC, f"missing language-profile policy phrase: {phrase}"))
    for profile in sorted(REQUIRED_PROFILES):
        if profile not in text:
            findings.append(Finding("ERROR", SPEC, f"missing language assurance profile: {profile}"))

    bridge = load_yaml(BRIDGE) if BRIDGE.exists() else None
    required_requirements: set[str] = set()
    if not isinstance(bridge, dict):
        findings.append(Finding("ERROR", BRIDGE, "language requirement bridge must be a mapping"))
        required_requirements = _language_requirements_from_registry()
    else:
        if bridge.get("implementation_allowed") is not False:
            findings.append(Finding("ERROR", BRIDGE, "implementation_allowed must be false"))
        if bridge.get("domain") != "language":
            findings.append(Finding("ERROR", BRIDGE, "domain must be language"))
        required_requirements = set(_as_strings(bridge.get("requirements")))
        if len(required_requirements) < 6:
            findings.append(Finding("ERROR", BRIDGE, "language bridge must list the Phase 0.10 language requirements"))

    registry = _registry_requirements()
    for req_id in sorted(required_requirements):
        entry = registry.get(req_id)
        if entry is None:
            findings.append(Finding("ERROR", REQUIREMENTS, f"missing canonical requirement {req_id}"))
            continue
        if entry.get("status") != "draft":
            findings.append(Finding("ERROR", REQUIREMENTS, f"{req_id}: status must remain draft in Phase 0.10"))
        if not _as_strings(entry.get("target_components")):
            findings.append(Finding("ERROR", REQUIREMENTS, f"{req_id}: target_components must be non-empty"))
        verification = entry.get("verification")
        if not isinstance(verification, dict) or "traceability_review" not in _as_strings(verification.get("primary")):
            findings.append(Finding("ERROR", REQUIREMENTS, f"{req_id}: verification.primary must include traceability_review"))

    catalog = load_yaml(CATALOG) if CATALOG.exists() else None
    if not isinstance(catalog, dict):
        findings.append(Finding("ERROR", CATALOG, "language verification test catalog must be a mapping"))
    else:
        if catalog.get("implementation_allowed") is not False:
            findings.append(Finding("ERROR", CATALOG, "implementation_allowed must be false"))
        entries = catalog.get("entries")
        if not isinstance(entries, list) or not entries:
            findings.append(Finding("ERROR", CATALOG, "entries must be a non-empty list"))
        else:
            covered = {
                req
                for entry in entries
                if isinstance(entry, dict)
                for req in _as_strings(entry.get("target_requirements"))
            }
            if not any(req.startswith("MFOS-REQ-LANG-") for req in covered):
                findings.append(Finding("ERROR", CATALOG, "catalog must cover at least one MFOS-REQ-LANG-* requirement"))

    return emit(findings, args.mode, "Language profile validation OK")


if __name__ == "__main__":
    raise SystemExit(main())
