#!/usr/bin/env python3
"""Check unsafe-inventory policy and schema structure."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, REQUIREMENTS, ROOT, emit, load_yaml, mode_arg


SCHEMA = ROOT / "schemas/mfos/unsafe-inventory-entry.schema.yml"
SPEC = ROOT / "docs/design/specs/39-language-and-verification-policy.md"
REQUIRED_SCHEMA_FIELDS = {
    "unsafe_id",
    "schema_version",
    "status",
    "component",
    "file",
    "function",
    "reason",
    "safety_contract",
    "preconditions",
    "postconditions",
    "invariants",
    "linked_requirements",
    "linked_tests",
    "linked_proof_obligations",
    "reviewer",
    "source_refs",
    "evidence_refs",
    "spec_gap_policy",
    "implementation_allowed",
}
REQUIRED_SPEC_PHRASES = {
    "Unsafe Exception Policy",
    "Unsafe Rust is forbidden by default",
    "requirement IDs and source refs",
    "caller and callee safety contracts",
    "memory ownership and aliasing rules",
    "explicit not-claimed boundaries",
    "not accepted evidence of memory safety",
    "MFOS_ERR_SPEC_GAP",
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
        findings.append(Finding("ERROR", SCHEMA, "unsafe inventory schema must be a mapping"))
    else:
        if schema.get("implementation_allowed") is not False:
            findings.append(Finding("ERROR", SCHEMA, "implementation_allowed must be false"))
        if schema.get("additionalProperties") is not False:
            findings.append(Finding("ERROR", SCHEMA, "additionalProperties must be false"))
        required = set(_strings(schema.get("required")))
        missing = sorted(REQUIRED_SCHEMA_FIELDS - required)
        if missing:
            findings.append(Finding("ERROR", SCHEMA, f"schema missing required fields: {', '.join(missing)}"))
        props = schema.get("properties")
        if not isinstance(props, dict):
            findings.append(Finding("ERROR", SCHEMA, "properties must be a mapping"))
        else:
            if props.get("implementation_allowed", {}).get("const") is not False:
                findings.append(Finding("ERROR", SCHEMA, "implementation_allowed property must const false"))

    if not SPEC.exists():
        findings.append(Finding("ERROR", SPEC, "language policy spec missing"))
    else:
        text = SPEC.read_text(encoding="utf-8")
        for phrase in sorted(REQUIRED_SPEC_PHRASES):
            if phrase not in text:
                findings.append(Finding("ERROR", SPEC, f"missing unsafe inventory policy phrase: {phrase}"))

    req_id, req = _requirement_by_title("unsafe and assembly boundary policy")
    if req is None:
        findings.append(Finding("ERROR", REQUIREMENTS, "missing unsafe and assembly boundary policy requirement"))
    else:
        text = str(req.get("normative_text", ""))
        for phrase in ("Unsafe Rust", "assembly", "C/C++", "contracts", "evidence before implementation"):
            if phrase not in text:
                findings.append(Finding("ERROR", REQUIREMENTS, f"{req_id}: missing phrase: {phrase}"))

    return emit(findings, args.mode, "Unsafe inventory check OK")


if __name__ == "__main__":
    raise SystemExit(main())
