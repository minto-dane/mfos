#!/usr/bin/env python3
"""Check naming-safe requirement, test, evidence, and claim namespaces."""

from __future__ import annotations

import re
from pathlib import Path

from mfos_lint import EVIDENCE, REQUIREMENTS, TESTS, Finding, ROOT, emit, load_yaml, mode_arg, source_ids


REQ_RE = re.compile(r"^MFOS-REQ-[A-Z0-9]+-\d{4}$")
TEST_RE = re.compile(r"^(TEST|NEG)-MFOS-[A-Z0-9]+-[A-Z0-9-]*\d{4}$")
EVID_RE = re.compile(r"^EV-MFOS-[A-Z0-9]+-[A-Z0-9-]*\d{4}$")
CLAIM_RE = re.compile(r"^MFOS-CLAIM-[A-Z0-9-]+-\d{4}$")
CLAIM_TREE = ROOT / "docs/design/assurance/claim-tree.yml"


def entries(path: Path) -> list[dict[str, object]]:
    data = load_yaml(path)
    if not isinstance(data, dict):
        return []
    return [entry for entry in data.get("entries", []) if isinstance(entry, dict)]


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []
    known_sources = source_ids()

    for entry in entries(REQUIREMENTS):
        rid = str(entry.get("requirement_id", ""))
        if not REQ_RE.match(rid):
            findings.append(Finding("ERROR", REQUIREMENTS, f"invalid requirement_id namespace: {rid}"))
        if rid.startswith(("IBM-", "RACF-", "SMF-", "JES2-", "DFSMS-")):
            findings.append(Finding("ERROR", REQUIREMENTS, f"external/product ID used as requirement_id: {rid}"))
        for ref in entry.get("source_refs", []) if isinstance(entry.get("source_refs"), list) else []:
            if not isinstance(ref, dict):
                continue
            sid = str(ref.get("source_id", ""))
            if sid not in known_sources:
                findings.append(Finding("ERROR", REQUIREMENTS, f"{rid}: unknown source_ref: {sid}"))
            if sid.startswith("EXTREF-") and ref.get("source_type") != "external_reference":
                findings.append(Finding("ERROR", REQUIREMENTS, f"{rid}: EXTREF source_ref must use source_type=external_reference: {sid}"))
            if sid.startswith("IBM-"):
                findings.append(Finding("ERROR", REQUIREMENTS, f"{rid}: legacy IBM source_ref used: {sid}"))

    for entry in entries(TESTS):
        tid = str(entry.get("test_id", ""))
        if not TEST_RE.match(tid):
            findings.append(Finding("ERROR", TESTS, f"invalid test_id namespace: {tid}"))
        for rid in entry.get("requirement_ids", []) if isinstance(entry.get("requirement_ids"), list) else []:
            if not REQ_RE.match(str(rid)):
                findings.append(Finding("ERROR", TESTS, f"{tid}: invalid requirement_id reference: {rid}"))

    for entry in entries(EVIDENCE):
        eid = str(entry.get("evidence_id", ""))
        if not EVID_RE.match(eid):
            findings.append(Finding("ERROR", EVIDENCE, f"invalid evidence_id namespace: {eid}"))
        for rid in entry.get("requirement_ids", []) if isinstance(entry.get("requirement_ids"), list) else []:
            if not REQ_RE.match(str(rid)):
                findings.append(Finding("ERROR", EVIDENCE, f"{eid}: invalid requirement_id reference: {rid}"))

    claim_data = load_yaml(CLAIM_TREE)
    if isinstance(claim_data, dict):
        for claim in claim_data.get("claims", []):
            if not isinstance(claim, dict):
                continue
            cid = str(claim.get("claim_id", ""))
            if not CLAIM_RE.match(cid):
                findings.append(Finding("ERROR", CLAIM_TREE, f"invalid claim_id namespace: {cid}"))
            for tid in claim.get("tests", []) if isinstance(claim.get("tests"), list) else []:
                if not TEST_RE.match(str(tid)):
                    findings.append(Finding("ERROR", CLAIM_TREE, f"{cid}: invalid test reference: {tid}"))
            for eid in claim.get("evidence", []) if isinstance(claim.get("evidence"), list) else []:
                if not EVID_RE.match(str(eid)):
                    findings.append(Finding("ERROR", CLAIM_TREE, f"{cid}: invalid evidence reference: {eid}"))

    return emit(findings, args.mode, "Requirement namespace check OK")


if __name__ == "__main__":
    raise SystemExit(main())
