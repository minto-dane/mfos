#!/usr/bin/env python3
"""Check hardening-evidence policy and schema structure."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, REQUIREMENTS, ROOT, emit, load_yaml, mode_arg


SCHEMA = ROOT / "schemas/mfos/hardening-evidence.schema.yml"
SPEC = ROOT / "docs/design/specs/39-language-and-verification-policy.md"
REQUIRED_SCHEMA_FIELDS = {
    "artifact_id",
    "schema_version",
    "status",
    "component",
    "build_profile",
    "target_triple",
    "toolchain",
    "compiler_flags",
    "linker_flags",
    "lto_status",
    "cfi_status",
    "cet_status",
    "cfg_status",
    "kcfi_status",
    "binary_evidence",
    "runtime_checks",
    "unsupported_objects",
    "exceptions",
    "reviewer",
    "source_refs",
    "requirement_refs",
    "evidence_refs",
    "spec_gap_policy",
    "implementation_allowed",
}
REQUIRED_SPEC_PHRASES = {
    "CFI Evidence Policy",
    "CET Evidence Policy",
    "Toolchain Pinning",
    "Sanitizer Policy",
    "Static Analysis Policy",
    "CodeQL Policy",
    "Sanitizers are validation aids, not production proof",
    "CodeQL reports are not a complete security review",
    "must not claim complete control-flow integrity",
}


def _strings(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _requirement_by_title(title_fragment: str) -> tuple[str, dict[str, object]] | tuple[None, None]:
    data = load_yaml(REQUIREMENTS)
    if not isinstance(data, dict):
        return None, None
    for entry in data.get("entries", []):
        if not isinstance(entry, dict):
            continue
        if title_fragment.lower() in str(entry.get("title", "")).lower():
            return str(entry.get("requirement_id", "")), entry
    return None, None


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    schema = load_yaml(SCHEMA) if SCHEMA.exists() else None
    if not isinstance(schema, dict):
        findings.append(Finding("ERROR", SCHEMA, "hardening evidence schema must be a mapping"))
    else:
        if schema.get("implementation_allowed") is not False:
            findings.append(Finding("ERROR", SCHEMA, "implementation_allowed must be false"))
        required = set(_strings(schema.get("required")))
        missing = sorted(REQUIRED_SCHEMA_FIELDS - required)
        if missing:
            findings.append(Finding("ERROR", SCHEMA, f"schema missing required fields: {', '.join(missing)}"))
        props = schema.get("properties")
        if not isinstance(props, dict):
            findings.append(Finding("ERROR", SCHEMA, "properties must be a mapping"))
        else:
            for field in ("cfi_status", "cet_status", "cfg_status", "kcfi_status"):
                if field not in props:
                    findings.append(Finding("ERROR", SCHEMA, f"missing hardening status field: {field}"))

    if not SPEC.exists():
        findings.append(Finding("ERROR", SPEC, "language policy spec missing"))
    else:
        text = SPEC.read_text(encoding="utf-8")
        for phrase in sorted(REQUIRED_SPEC_PHRASES):
            if phrase not in text:
                findings.append(Finding("ERROR", SPEC, f"missing hardening evidence policy phrase: {phrase}"))

    for title_fragment, expected in (
        ("CFI and CET policy", "defense-in-depth aids"),
        ("toolchain pinning and static analysis policy", "before release claims"),
    ):
        req_id, req = _requirement_by_title(title_fragment)
        if req is None:
            findings.append(Finding("ERROR", REQUIREMENTS, f"missing {title_fragment} requirement"))
            continue
        text = str(req.get("normative_text", ""))
        if expected not in text:
            findings.append(Finding("ERROR", REQUIREMENTS, f"{req_id}: missing phrase: {expected}"))

    return emit(findings, args.mode, "Hardening evidence check OK")


if __name__ == "__main__":
    raise SystemExit(main())
