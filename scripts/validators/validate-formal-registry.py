#!/usr/bin/env python3
"""Validate the MFOS formal assurance registry."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg


REGISTRY = ROOT / "formal" / "registry.yml"
REQUIRED_TOP_LEVEL = {
    "schema_version",
    "registry_kind",
    "status",
    "implementation_allowed",
    "proof_claimed",
    "formal_claims",
    "proof_obligations",
    "model_registry",
    "tool_registry",
    "evidence_registry",
}
REQUIRED_CLAIMS = {
    "authorization_no_handle_without_allow",
    "audit_deny_before_return",
    "update_no_rollback",
    "partition_memory_ownership",
    "pxm_capability_required_for_resource_operation",
    "mfvm_cannot_bypass_pxm",
    "cvm_launch_requires_measurement",
    "cvm_secret_release_requires_attestation",
    "private_shared_memory_transition_validity",
    "cluster_policy_distribution_integrity",
    "cluster_attestation_collection_integrity",
}
REQUIRED_TOOLS = {"TLA+", "Alloy", "Kani", "Verus", "CodeQL", "fuzzing", "property tests"}
PLANNING_STATUSES = {"planned", "draft"}
EVIDENCE_STATUSES = {"planned", "draft"}


def _strings(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    if not REGISTRY.exists():
        findings.append(Finding("ERROR", REGISTRY, "formal registry missing"))
        return emit(findings, args.mode, "Formal registry validation OK")

    data = load_yaml(REGISTRY)
    if not isinstance(data, dict):
        findings.append(Finding("ERROR", REGISTRY, "formal registry must be a mapping"))
        return emit(findings, args.mode, "Formal registry validation OK")

    for field in sorted(REQUIRED_TOP_LEVEL - set(data)):
        findings.append(Finding("ERROR", REGISTRY, f"missing top-level field: {field}"))
    if data.get("implementation_allowed") is not False:
        findings.append(Finding("ERROR", REGISTRY, "implementation_allowed must be false"))
    if data.get("proof_claimed") is not False:
        findings.append(Finding("ERROR", REGISTRY, "proof_claimed must be false unless proof artifacts exist"))

    claims = data.get("formal_claims")
    if not isinstance(claims, list) or not claims:
        findings.append(Finding("ERROR", REGISTRY, "formal_claims must be a non-empty list"))
        claims = []
    normalized_claims: set[str] = set()
    claim_ids: set[str] = set()
    claim_evidence_refs: set[str] = set()
    claim_obligation_refs: set[str] = set()
    for claim in claims:
        if not isinstance(claim, dict):
            findings.append(Finding("ERROR", REGISTRY, "formal claim entry is not a mapping"))
            continue
        cid = str(claim.get("claim_id", ""))
        if cid in claim_ids:
            findings.append(Finding("ERROR", REGISTRY, f"duplicate formal claim: {cid}"))
        claim_ids.add(cid)
        normalized_claims.add(cid.removeprefix("MFOS-FORMAL-CLAIM-").lower().replace("-", "_"))
        for field in ("claim_id", "status", "requirements", "assumptions", "not_claimed", "proof_obligations", "evidence_refs"):
            if field not in claim:
                findings.append(Finding("ERROR", REGISTRY, f"{cid or '<missing>'}: missing {field}"))
        if claim.get("status") not in PLANNING_STATUSES:
            findings.append(Finding("ERROR", REGISTRY, f"{cid}: status must be planned or draft"))
        if not _strings(claim.get("requirements")):
            findings.append(Finding("ERROR", REGISTRY, f"{cid}: requirements must be non-empty"))
        if not _strings(claim.get("assumptions")):
            findings.append(Finding("ERROR", REGISTRY, f"{cid}: assumptions must be non-empty"))
        not_claimed = _strings(claim.get("not_claimed"))
        if not not_claimed:
            findings.append(Finding("ERROR", REGISTRY, f"{cid}: not_claimed must be non-empty"))
        elif not any("verification" in item.lower() or "proof" in item.lower() for item in not_claimed):
            findings.append(Finding("ERROR", REGISTRY, f"{cid}: not_claimed must explicitly limit proof/verification scope"))
        claim_obligation_refs.update(_strings(claim.get("proof_obligations")))
        claim_evidence_refs.update(_strings(claim.get("evidence_refs")))

    missing_claims = sorted(REQUIRED_CLAIMS - normalized_claims)
    if missing_claims:
        findings.append(Finding("ERROR", REGISTRY, f"missing required formal claims: {', '.join(missing_claims)}"))

    obligations = data.get("proof_obligations")
    obligation_ids: set[str] = set()
    if not isinstance(obligations, list) or not obligations:
        findings.append(Finding("ERROR", REGISTRY, "proof_obligations must be a non-empty list"))
    else:
        for obligation in obligations:
            if not isinstance(obligation, dict):
                findings.append(Finding("ERROR", REGISTRY, "proof obligation entry is not a mapping"))
                continue
            oid = str(obligation.get("obligation_id", ""))
            if oid in obligation_ids:
                findings.append(Finding("ERROR", REGISTRY, f"duplicate proof obligation: {oid}"))
            obligation_ids.add(oid)
            cid = str(obligation.get("claim_id", ""))
            if cid not in claim_ids:
                findings.append(Finding("ERROR", REGISTRY, f"{oid}: unknown claim_id {cid or '<missing>'}"))
            if obligation.get("status") not in PLANNING_STATUSES:
                findings.append(Finding("ERROR", REGISTRY, f"{oid}: status must be planned or draft"))
            if obligation.get("proof_claimed") is not False:
                findings.append(Finding("ERROR", REGISTRY, f"{oid}: proof_claimed must be false in Phase 0.10"))
            if obligation.get("proof_artifact") not in {None, ""}:
                findings.append(Finding("ERROR", REGISTRY, f"{oid}: proof_artifact must be empty until proof exists"))
            if not _strings(obligation.get("acceptance_criteria")):
                findings.append(Finding("ERROR", REGISTRY, f"{oid}: acceptance_criteria must be non-empty"))
            if not _strings(obligation.get("accepted_tools")):
                findings.append(Finding("ERROR", REGISTRY, f"{oid}: accepted_tools must be non-empty"))

    missing_obligations = sorted(claim_obligation_refs - obligation_ids)
    if missing_obligations:
        findings.append(Finding("ERROR", REGISTRY, f"claims link missing proof obligations: {', '.join(missing_obligations)}"))

    tools = data.get("tool_registry")
    got_tools = {str(item.get("tool_name")) for item in tools if isinstance(item, dict)} if isinstance(tools, list) else set()
    missing_tools = sorted(REQUIRED_TOOLS - got_tools)
    if missing_tools:
        findings.append(Finding("ERROR", REGISTRY, f"missing required tools: {', '.join(missing_tools)}"))
    if isinstance(tools, list):
        for tool in tools:
            if not isinstance(tool, dict):
                findings.append(Finding("ERROR", REGISTRY, "tool registry entry is not a mapping"))
                continue
            name = str(tool.get("tool_name", "<missing>"))
            if tool.get("status") not in PLANNING_STATUSES:
                findings.append(Finding("ERROR", REGISTRY, f"{name}: tool status must be planned or draft"))
            role = str(tool.get("evidence_role", "")).lower()
            if "not proof evidence" not in role:
                findings.append(Finding("ERROR", REGISTRY, f"{name}: evidence_role must state it is not proof evidence yet"))

    evidence = data.get("evidence_registry")
    evidence_ids: set[str] = set()
    if not isinstance(evidence, list) or not evidence:
        findings.append(Finding("ERROR", REGISTRY, "evidence_registry must be a non-empty list"))
    else:
        for item in evidence:
            if not isinstance(item, dict):
                findings.append(Finding("ERROR", REGISTRY, "evidence registry entry is not a mapping"))
                continue
            eid = str(item.get("evidence_id", ""))
            if eid in evidence_ids:
                findings.append(Finding("ERROR", REGISTRY, f"duplicate formal evidence entry: {eid}"))
            evidence_ids.add(eid)
            if item.get("status") not in EVIDENCE_STATUSES:
                findings.append(Finding("ERROR", REGISTRY, f"{eid}: evidence status must remain planned or draft"))
            if item.get("claim_ref") not in claim_ids:
                findings.append(Finding("ERROR", REGISTRY, f"{eid}: unknown claim_ref {item.get('claim_ref')}"))
            if item.get("artifact_path") not in {None, ""}:
                findings.append(Finding("ERROR", REGISTRY, f"{eid}: artifact_path must be empty until reviewed proof evidence exists"))

    missing_evidence = sorted(claim_evidence_refs - evidence_ids)
    if missing_evidence:
        findings.append(Finding("ERROR", REGISTRY, f"claims link missing evidence entries: {', '.join(missing_evidence)}"))

    return emit(findings, args.mode, "Formal registry validation OK")


if __name__ == "__main__":
    raise SystemExit(main())
