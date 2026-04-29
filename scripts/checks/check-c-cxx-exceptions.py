#!/usr/bin/env python3
"""Check C/C++ exception policy and schema structure."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, REQUIREMENTS, ROOT, emit, load_yaml, mode_arg


SCHEMA = ROOT / "schemas/mfos/c-cxx-exception.schema.yml"
SPEC = ROOT / "docs/design/specs/39-language-and-verification-policy.md"
REQUIRED_SCHEMA_FIELDS = {
    "exception_id",
    "schema_version",
    "status",
    "component",
    "reason",
    "no_rust_alternative_justification",
    "no_policy_logic",
    "no_business_semantics",
    "cfi_required",
    "cet_required",
    "sanitizer_required",
    "codeql_required",
    "linked_adr",
    "linked_tests",
    "reviewer",
    "source_refs",
    "requirement_refs",
    "evidence_refs",
    "spec_gap_policy",
    "implementation_allowed",
}
REQUIRED_SPEC_PHRASES = {
    "C/C++ Exception Policy",
    "C and C++ are not default MFOS implementation languages",
    "explicit LAP-4 exceptions",
    "does not authorize general C/C++ production code",
    "clang CFI for C/C++ Boundaries",
    "clang CFI evidence must include",
    "C/C++ safety equivalence to safe Rust",
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
        findings.append(Finding("ERROR", SCHEMA, "C/C++ exception schema must be a mapping"))
    else:
        if schema.get("implementation_allowed") is not False:
            findings.append(Finding("ERROR", SCHEMA, "implementation_allowed must be false"))
        required = set(_strings(schema.get("required")))
        missing = sorted(REQUIRED_SCHEMA_FIELDS - required)
        if missing:
            findings.append(Finding("ERROR", SCHEMA, f"schema missing required fields: {', '.join(missing)}"))
        props = schema.get("properties")
        if isinstance(props, dict):
            if props.get("no_policy_logic", {}).get("const") is not True:
                findings.append(Finding("ERROR", SCHEMA, "no_policy_logic must be const true"))
            if props.get("no_business_semantics", {}).get("const") is not True:
                findings.append(Finding("ERROR", SCHEMA, "no_business_semantics must be const true"))

    if not SPEC.exists():
        findings.append(Finding("ERROR", SPEC, "language policy spec missing"))
    else:
        text = SPEC.read_text(encoding="utf-8")
        for phrase in sorted(REQUIRED_SPEC_PHRASES):
            if phrase not in text:
                findings.append(Finding("ERROR", SPEC, f"missing C/C++ exception policy phrase: {phrase}"))

    req_id, req = _requirement_by_title("unsafe and assembly boundary policy")
    if req is None:
        findings.append(Finding("ERROR", REQUIREMENTS, "missing unsafe and assembly boundary policy requirement"))
    else:
        text = str(req.get("normative_text", ""))
        for phrase in ("C/C++ boundaries", "explicit contracts", "evidence before implementation"):
            if phrase not in text:
                findings.append(Finding("ERROR", REQUIREMENTS, f"{req_id}: missing phrase: {phrase}"))

    return emit(findings, args.mode, "C/C++ exception check OK")


if __name__ == "__main__":
    raise SystemExit(main())
