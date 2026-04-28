#!/usr/bin/env python3
"""Validate MFOS Phase 0.6 assurance claim tree."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from pathlib import Path

from lib.mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg, requirement_ids


CLAIM_TREE = ROOT / "docs/design/assurance/claim-tree.yml"
REQUIRED = {
    "claim_id",
    "profile",
    "claim",
    "protected_assets",
    "threat_scope",
    "trusted_components",
    "requirements",
    "tests",
    "evidence",
    "assumptions",
    "not_claimed",
    "residual_risks",
}
PROFILES = {"Baseline", "Enterprise-Standalone", "Enterprise-PXM", "High-Assurance"}


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []
    known_reqs = requirement_ids()

    if not CLAIM_TREE.exists():
        findings.append(Finding("ERROR", CLAIM_TREE, "claim tree registry missing"))
        return emit(findings, args.mode, "Claim validation OK")

    data = load_yaml(CLAIM_TREE)
    if not isinstance(data, dict):
        findings.append(Finding("ERROR", CLAIM_TREE, "claim tree must be a mapping"))
        return emit(findings, args.mode, "Claim validation OK")

    claims = data.get("claims")
    if not isinstance(claims, list) or not claims:
        findings.append(Finding("ERROR", CLAIM_TREE, "claims must be a non-empty list"))
        return emit(findings, args.mode, "Claim validation OK")

    seen: set[str] = set()
    for idx, claim in enumerate(claims, 1):
        if not isinstance(claim, dict):
            findings.append(Finding("ERROR", CLAIM_TREE, f"claim #{idx} is not a mapping"))
            continue
        cid = str(claim.get("claim_id", f"<claim-{idx}>"))
        if cid in seen:
            findings.append(Finding("ERROR", CLAIM_TREE, f"duplicate claim_id: {cid}"))
        seen.add(cid)

        missing = sorted(REQUIRED - set(claim))
        if missing:
            findings.append(Finding("ERROR", CLAIM_TREE, f"{cid}: missing fields: {', '.join(missing)}"))
        if claim.get("profile") not in PROFILES:
            findings.append(Finding("ERROR", CLAIM_TREE, f"{cid}: invalid profile: {claim.get('profile')}"))
        for field in ("protected_assets", "threat_scope", "trusted_components", "requirements", "tests", "evidence", "assumptions", "not_claimed", "residual_risks"):
            if field in claim and not isinstance(claim[field], list):
                findings.append(Finding("ERROR", CLAIM_TREE, f"{cid}: {field} must be a list"))
        if not claim.get("assumptions"):
            findings.append(Finding("ERROR", CLAIM_TREE, f"{cid}: assumptions must not be empty"))
        if not claim.get("not_claimed"):
            findings.append(Finding("ERROR", CLAIM_TREE, f"{cid}: not_claimed must not be empty"))

        for rid in claim.get("requirements", []) if isinstance(claim.get("requirements"), list) else []:
            if "*" not in rid and rid not in known_reqs:
                findings.append(Finding("WARN", CLAIM_TREE, f"{cid}: requirement not in priority catalog: {rid}"))

        if claim.get("profile") == "Baseline":
            lower = str(claim.get("claim", "")).lower()
            if "after nucleus compromise" in lower and "not_claimed" not in lower:
                findings.append(Finding("ERROR", CLAIM_TREE, f"{cid}: baseline may imply post-nucleus-compromise protection"))
        if claim.get("profile") == "High-Assurance":
            evidence_text = " ".join(claim.get("evidence", []) if isinstance(claim.get("evidence"), list) else [])
            if "GRD" not in evidence_text and "ATTESTATION" not in evidence_text:
                findings.append(Finding("ERROR", CLAIM_TREE, f"{cid}: High-Assurance claim lacks Guard/attestation evidence reference"))

    return emit(findings, args.mode, f"Claim validation OK: {len(claims)} claims checked")


if __name__ == "__main__":
    raise SystemExit(main())
