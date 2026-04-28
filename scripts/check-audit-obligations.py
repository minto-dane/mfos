#!/usr/bin/env python3
"""Validate audit-obligation coverage in requirements and registry links."""

from __future__ import annotations

from pathlib import Path

from mfos_lint import EVIDENCE, REQUIREMENTS, TESTS, Finding, emit, mode_arg, registry_entries


PROTECTED_WORDS = (
    "protected",
    "authorization",
    "securityd",
    "dataset",
    "catalog",
    "spool",
    "operator",
    "AMF",
    "PXM",
    "Guard",
    "update",
    "boot",
    "attestation",
)


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []
    req_entries = registry_entries(REQUIREMENTS)
    test_entries = registry_entries(TESTS)
    evid_entries = registry_entries(EVIDENCE)
    test_reqs = {rid for entry in test_entries for rid in entry.get("requirement_ids", []) if isinstance(rid, str)}
    evid_reqs = {rid for entry in evid_entries for rid in entry.get("requirement_ids", []) if isinstance(rid, str)}

    for entry in req_entries:
        rid = str(entry.get("requirement_id", "<missing>"))
        text = f"{entry.get('title', '')} {entry.get('normative_text', '')}"
        audit = entry.get("audit_obligation")
        if not isinstance(audit, dict):
            findings.append(Finding("ERROR", REQUIREMENTS, f"{rid}: audit_obligation must be a mapping"))
            continue
        if not audit.get("obligation"):
            findings.append(Finding("ERROR", REQUIREMENTS, f"{rid}: audit_obligation.obligation is required"))
        if audit.get("obligation") == "required" and not audit.get("record_type"):
            findings.append(Finding("ERROR", REQUIREMENTS, f"{rid}: required audit obligation needs record_type"))
        if audit.get("before_return") is True and not audit.get("record_type"):
            findings.append(Finding("ERROR", REQUIREMENTS, f"{rid}: before_return audit requires record_type"))
        if any(word.lower() in text.lower() for word in PROTECTED_WORDS):
            if audit.get("obligation") in {None, "none", "not_applicable"} and "SPEC_GAP" not in text:
                findings.append(Finding("ERROR", REQUIREMENTS, f"{rid}: protected-resource requirement lacks audit obligation or SPEC_GAP"))
        if rid not in test_reqs:
            findings.append(Finding("WARN", REQUIREMENTS, f"{rid}: no test registry entry references this requirement"))
        if rid not in evid_reqs:
            findings.append(Finding("WARN", REQUIREMENTS, f"{rid}: no evidence registry entry references this requirement"))

    return emit(findings, args.mode, f"Audit obligation check OK: {len(req_entries)} requirements checked")


if __name__ == "__main__":
    raise SystemExit(main())
