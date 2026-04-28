#!/usr/bin/env python3
"""Check that MFOS evidence status is not overclaimed.

Draft evidence is allowed during Phase 0.x planning, but it must not look like
verified proof. Release-mode claim checks require verified or archived evidence
with digest and verification metadata.
"""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

import re
from pathlib import Path

from lib.mfos_lint import EVIDENCE, Finding, ROOT, emit, load_yaml, mode_arg


CLAIM_TREE = ROOT / "docs/design/assurance/claim-tree.yml"

VALID_STATUSES = {"draft", "collected", "verified", "archived", "rejected", "expired", "superseded"}
VERIFIED_STATUSES = {"verified", "archived"}
INVALID_FOR_CLAIMS = {"rejected", "expired", "superseded"}
VALID_RESULTS = {"pass", "fail", "not_checked"}
SHA384_RE = re.compile(r"^[0-9a-fA-F]{96}$")
RELEASE_CLAIM_STATUSES = {"EVIDENCED", "RELEASED", "evidenced", "released"}
RELEASE_CLAIM_LEVELS = {"CLAIM-L4", "CLAIM-L5"}


def _list_value(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str)]


def _load_entries(findings: list[Finding]) -> dict[str, dict[str, object]]:
    data = load_yaml(EVIDENCE)
    if not isinstance(data, dict):
        findings.append(Finding("ERROR", EVIDENCE, "evidence registry must be a mapping"))
        return {}
    entries = data.get("entries")
    if not isinstance(entries, list):
        findings.append(Finding("ERROR", EVIDENCE, "evidence registry entries must be a list"))
        return {}

    by_id: dict[str, dict[str, object]] = {}
    for idx, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            findings.append(Finding("ERROR", EVIDENCE, f"entry #{idx} is not a mapping"))
            continue
        eid = entry.get("evidence_id")
        if not isinstance(eid, str) or not eid:
            findings.append(Finding("ERROR", EVIDENCE, f"entry #{idx} missing evidence_id"))
            continue
        if eid in by_id:
            findings.append(Finding("ERROR", EVIDENCE, f"duplicate evidence_id: {eid}"))
        by_id[eid] = entry
    return by_id


def _check_entry(eid: str, entry: dict[str, object], mode: str, findings: list[Finding]) -> None:
    status = str(entry.get("status", ""))
    if status not in VALID_STATUSES:
        findings.append(Finding("ERROR", EVIDENCE, f"{eid}: invalid evidence status: {status or '<missing>'}"))

    artifact = entry.get("artifact")
    if not isinstance(artifact, dict):
        findings.append(Finding("ERROR", EVIDENCE, f"{eid}: artifact must be a mapping"))
        artifact = {}
    verification = entry.get("verification")
    if not isinstance(verification, dict):
        findings.append(Finding("ERROR", EVIDENCE, f"{eid}: verification must be a mapping"))
        verification = {}
    retention = entry.get("retention")
    if not isinstance(retention, dict):
        findings.append(Finding("ERROR", EVIDENCE, f"{eid}: retention must be a mapping"))
        retention = {}

    result = str(verification.get("result", ""))
    if result not in VALID_RESULTS:
        findings.append(Finding("ERROR", EVIDENCE, f"{eid}: invalid verification.result: {result or '<missing>'}"))

    if status == "draft":
        if result == "pass":
            findings.append(Finding("ERROR", EVIDENCE, f"{eid}: draft evidence must not have verification.result=pass"))
        if retention.get("class") in {"release", "production", "high_assurance"}:
            findings.append(Finding("ERROR", EVIDENCE, f"{eid}: draft evidence must not use release/production/high_assurance retention class"))
        if _list_value(entry.get("release_ids")):
            findings.append(Finding("ERROR", EVIDENCE, f"{eid}: draft evidence must not be bound to release_ids"))
        if mode == "release" and _list_value(entry.get("conformance_claim_ids")):
            findings.append(Finding("WARN", EVIDENCE, f"{eid}: draft evidence is claim-linked but not verified proof"))

    if status in VERIFIED_STATUSES:
        sha384 = artifact.get("sha384")
        if not isinstance(sha384, str) or not SHA384_RE.match(sha384):
            findings.append(Finding("ERROR", EVIDENCE, f"{eid}: verified/archived evidence requires artifact.sha384"))
        if result != "pass":
            findings.append(Finding("ERROR", EVIDENCE, f"{eid}: verified/archived evidence requires verification.result=pass"))
        for field in ("verifier", "verified_at_utc", "verification_method"):
            if not verification.get(field):
                findings.append(Finding("ERROR", EVIDENCE, f"{eid}: verified/archived evidence missing verification.{field}"))


def _claim_requires_release_evidence(claim: dict[str, object], mode: str) -> bool:
    if mode == "release":
        return True
    status = str(claim.get("status", ""))
    level = str(claim.get("claim_level", ""))
    return status in RELEASE_CLAIM_STATUSES or level in RELEASE_CLAIM_LEVELS


def _check_claims(evidence_by_id: dict[str, dict[str, object]], mode: str, findings: list[Finding]) -> None:
    if not CLAIM_TREE.exists():
        findings.append(Finding("ERROR", CLAIM_TREE, "claim tree registry missing"))
        return
    data = load_yaml(CLAIM_TREE)
    if not isinstance(data, dict):
        findings.append(Finding("ERROR", CLAIM_TREE, "claim tree registry must be a mapping"))
        return
    claims = data.get("claims")
    if not isinstance(claims, list):
        findings.append(Finding("ERROR", CLAIM_TREE, "claims must be a list"))
        return

    for idx, claim in enumerate(claims, 1):
        if not isinstance(claim, dict):
            findings.append(Finding("ERROR", CLAIM_TREE, f"claim #{idx} is not a mapping"))
            continue
        cid = str(claim.get("claim_id", f"<claim-{idx}>"))
        evidence_ids = _list_value(claim.get("evidence"))
        if not evidence_ids:
            findings.append(Finding("ERROR", CLAIM_TREE, f"{cid}: claim must list evidence IDs"))
            continue

        release_required = _claim_requires_release_evidence(claim, mode)
        for eid in evidence_ids:
            entry = evidence_by_id.get(eid)
            if entry is None:
                severity = "ERROR" if release_required else "WARN"
                findings.append(Finding(severity, CLAIM_TREE, f"{cid}: evidence not registered: {eid}"))
                continue

            status = str(entry.get("status", ""))
            if status in INVALID_FOR_CLAIMS:
                findings.append(Finding("ERROR", CLAIM_TREE, f"{cid}: evidence {eid} has invalid status for claims: {status}"))
            elif release_required and status not in VERIFIED_STATUSES:
                findings.append(Finding("ERROR", CLAIM_TREE, f"{cid}: release-mode claim requires verified/archived evidence, got {eid} status={status}"))
            elif status not in VERIFIED_STATUSES and _claim_requires_release_evidence(claim, mode):
                findings.append(Finding("WARN", CLAIM_TREE, f"{cid}: evidence {eid} is not verified proof yet: status={status}"))


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    evidence_by_id = _load_entries(findings)
    for eid, entry in sorted(evidence_by_id.items()):
        _check_entry(eid, entry, args.mode, findings)
    _check_claims(evidence_by_id, args.mode, findings)

    return emit(findings, args.mode, f"Evidence status check OK: {len(evidence_by_id)} entries checked")


if __name__ == "__main__":
    raise SystemExit(main())
