#!/usr/bin/env python3
"""Validate MFOS proof-obligation registry links without claiming proof semantics."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg


REGISTRY = ROOT / "formal/registry.yml"
CLAIM_REGISTRY = ROOT / "formal/claim-registry.yml"
PROOF_OBLIGATIONS = ROOT / "formal/proof-obligations.yml"
TOOL_REGISTRY = ROOT / "formal/tool-registry.yml"
MODEL_REGISTRY = ROOT / "formal/model-registry.yml"
EVIDENCE_REGISTRY = ROOT / "formal/evidence-registry.yml"
SPEC = ROOT / "docs/design/specs/40-automated-reasoning-program.md"
SCHEMA = ROOT / "schemas/mfos/proof-obligation.schema.yml"
ALLOWED_TOOLS = {"TLA+", "Alloy", "Kani", "Verus", "Dafny", "CodeQL", "fuzzing", "property tests"}
REQUIRED_CRITERIA = {
    "linked model or harness exists",
    "assumptions documented",
    "review recorded",
    "counterexamples triaged",
}


def _strings(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _validate_split_registries(findings: list[Finding]) -> None:
    claims_data = load_yaml(CLAIM_REGISTRY) if CLAIM_REGISTRY.exists() else None
    obligations_data = load_yaml(PROOF_OBLIGATIONS) if PROOF_OBLIGATIONS.exists() else None
    tools_data = load_yaml(TOOL_REGISTRY) if TOOL_REGISTRY.exists() else None
    models_data = load_yaml(MODEL_REGISTRY) if MODEL_REGISTRY.exists() else None
    evidence_data = load_yaml(EVIDENCE_REGISTRY) if EVIDENCE_REGISTRY.exists() else None

    for path, data, expected_kind in (
        (CLAIM_REGISTRY, claims_data, "mfos_formal_claim_registry"),
        (PROOF_OBLIGATIONS, obligations_data, "mfos_proof_obligation_registry"),
        (TOOL_REGISTRY, tools_data, "mfos_formal_tool_registry"),
        (MODEL_REGISTRY, models_data, "mfos_formal_model_registry"),
        (EVIDENCE_REGISTRY, evidence_data, "mfos_formal_evidence_registry"),
    ):
        if not isinstance(data, dict):
            findings.append(Finding("ERROR", path, "split formal registry must be a mapping"))
            continue
        if data.get("registry_kind") != expected_kind:
            findings.append(Finding("ERROR", path, f"registry_kind must be {expected_kind}"))
        if data.get("implementation_allowed") is not False:
            findings.append(Finding("ERROR", path, "implementation_allowed must be false"))
        if data.get("proof_claimed") is not False:
            findings.append(Finding("ERROR", path, "proof_claimed must be false"))

    claims = claims_data.get("claims") if isinstance(claims_data, dict) else []
    obligations = obligations_data.get("proof_obligations") if isinstance(obligations_data, dict) else []
    tools = tools_data.get("tools") if isinstance(tools_data, dict) else []
    models = models_data.get("models") if isinstance(models_data, dict) else []
    evidence = evidence_data.get("evidence") if isinstance(evidence_data, dict) else []

    if not isinstance(claims, list) or not claims:
        findings.append(Finding("ERROR", CLAIM_REGISTRY, "claims must be a non-empty list"))
        claims = []
    if not isinstance(obligations, list) or not obligations:
        findings.append(Finding("ERROR", PROOF_OBLIGATIONS, "proof_obligations must be a non-empty list"))
        obligations = []
    if not isinstance(tools, list) or not tools:
        findings.append(Finding("ERROR", TOOL_REGISTRY, "tools must be a non-empty list"))
        tools = []
    if not isinstance(models, list) or not models:
        findings.append(Finding("ERROR", MODEL_REGISTRY, "models must be a non-empty list"))
        models = []
    if not isinstance(evidence, list) or not evidence:
        findings.append(Finding("ERROR", EVIDENCE_REGISTRY, "evidence must be a non-empty list"))
        evidence = []

    claim_ids = {str(item.get("claim_id")) for item in claims if isinstance(item, dict)}
    obligation_ids = {str(item.get("obligation_id")) for item in obligations if isinstance(item, dict)}
    tool_ids = {str(item.get("tool_id")) for item in tools if isinstance(item, dict)}
    model_ids = {str(item.get("model_id")) for item in models if isinstance(item, dict)}
    evidence_ids = {str(item.get("evidence_id")) for item in evidence if isinstance(item, dict)}

    for claim in claims:
        if not isinstance(claim, dict):
            findings.append(Finding("ERROR", CLAIM_REGISTRY, "claim entry is not a mapping"))
            continue
        cid = str(claim.get("claim_id", ""))
        if not cid.startswith("MFOS-FC-"):
            findings.append(Finding("ERROR", CLAIM_REGISTRY, f"{cid or '<missing>'}: claim_id must use MFOS-FC-*"))
        for field in ("requirement_refs", "assumptions", "not_claimed", "proof_obligation_refs", "model_refs", "evidence_refs"):
            if not _strings(claim.get(field)):
                findings.append(Finding("ERROR", CLAIM_REGISTRY, f"{cid}: {field} must be non-empty"))
        for oid in _strings(claim.get("proof_obligation_refs")):
            if oid not in obligation_ids:
                findings.append(Finding("ERROR", CLAIM_REGISTRY, f"{cid}: unknown proof obligation {oid}"))
        for mid in _strings(claim.get("model_refs")):
            if mid not in model_ids:
                findings.append(Finding("ERROR", CLAIM_REGISTRY, f"{cid}: unknown model {mid}"))
        for eid in _strings(claim.get("evidence_refs")):
            if eid not in evidence_ids:
                findings.append(Finding("ERROR", CLAIM_REGISTRY, f"{cid}: unknown evidence {eid}"))

    for obligation in obligations:
        if not isinstance(obligation, dict):
            findings.append(Finding("ERROR", PROOF_OBLIGATIONS, "proof obligation entry is not a mapping"))
            continue
        oid = str(obligation.get("obligation_id", ""))
        claim_ref = str(obligation.get("claim_ref", ""))
        if not oid.startswith("MFOS-PO-"):
            findings.append(Finding("ERROR", PROOF_OBLIGATIONS, f"{oid or '<missing>'}: obligation_id must use MFOS-PO-*"))
        if claim_ref not in claim_ids:
            findings.append(Finding("ERROR", PROOF_OBLIGATIONS, f"{oid}: unknown claim_ref {claim_ref or '<missing>'}"))
        if obligation.get("proof_claimed") is not False:
            findings.append(Finding("ERROR", PROOF_OBLIGATIONS, f"{oid}: proof_claimed must be false"))
        if obligation.get("proof_artifact") not in {None, ""}:
            findings.append(Finding("ERROR", PROOF_OBLIGATIONS, f"{oid}: proof_artifact must be empty until reviewed proof exists"))
        if not _strings(obligation.get("requirement_refs")):
            findings.append(Finding("ERROR", PROOF_OBLIGATIONS, f"{oid}: requirement_refs must be non-empty"))
        for tool_ref in _strings(obligation.get("accepted_tool_refs")):
            if tool_ref not in tool_ids:
                findings.append(Finding("ERROR", PROOF_OBLIGATIONS, f"{oid}: unknown tool ref {tool_ref}"))

    for model in models:
        if not isinstance(model, dict):
            continue
        mid = str(model.get("model_id", ""))
        for cid in _strings(model.get("claim_refs")):
            if cid not in claim_ids:
                findings.append(Finding("ERROR", MODEL_REGISTRY, f"{mid}: unknown claim ref {cid}"))

    for item in evidence:
        if not isinstance(item, dict):
            continue
        eid = str(item.get("evidence_id", ""))
        if item.get("proof_claimed") is not False:
            findings.append(Finding("ERROR", EVIDENCE_REGISTRY, f"{eid}: proof_claimed must be false"))
        if item.get("artifact_path") not in {None, ""}:
            findings.append(Finding("ERROR", EVIDENCE_REGISTRY, f"{eid}: artifact_path must be empty until reviewed proof exists"))
        if str(item.get("claim_ref", "")) not in claim_ids:
            findings.append(Finding("ERROR", EVIDENCE_REGISTRY, f"{eid}: unknown claim_ref"))
        for oid in _strings(item.get("proof_obligation_refs")):
            if oid not in obligation_ids:
                findings.append(Finding("ERROR", EVIDENCE_REGISTRY, f"{eid}: unknown proof obligation {oid}"))


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    if not SCHEMA.exists():
        findings.append(Finding("ERROR", SCHEMA, "proof obligation schema missing"))
    else:
        schema = load_yaml(SCHEMA)
        if not isinstance(schema, dict):
            findings.append(Finding("ERROR", SCHEMA, "proof obligation schema must be a mapping"))
        elif schema.get("implementation_allowed") is not False:
            findings.append(Finding("ERROR", SCHEMA, "implementation_allowed must be false"))

    data = load_yaml(REGISTRY) if REGISTRY.exists() else None
    if not isinstance(data, dict):
        findings.append(Finding("ERROR", REGISTRY, "formal registry must be a mapping"))
        return emit(findings, args.mode, "Proof obligation validation OK")

    claims = data.get("formal_claims")
    obligations = data.get("proof_obligations")
    if not isinstance(claims, list):
        findings.append(Finding("ERROR", REGISTRY, "formal_claims must be a list"))
        claims = []
    if not isinstance(obligations, list):
        findings.append(Finding("ERROR", REGISTRY, "proof_obligations must be a list"))
        obligations = []

    claim_ids = {str(claim.get("claim_id")) for claim in claims if isinstance(claim, dict)}
    obligation_by_id: dict[str, dict[str, object]] = {}
    for obligation in obligations:
        if not isinstance(obligation, dict):
            findings.append(Finding("ERROR", REGISTRY, "proof obligation entry is not a mapping"))
            continue
        oid = str(obligation.get("obligation_id", ""))
        if not oid:
            findings.append(Finding("ERROR", REGISTRY, "proof obligation missing obligation_id"))
            continue
        if oid in obligation_by_id:
            findings.append(Finding("ERROR", REGISTRY, f"duplicate proof obligation: {oid}"))
        obligation_by_id[oid] = obligation

    for claim in claims:
        if not isinstance(claim, dict):
            continue
        cid = str(claim.get("claim_id", ""))
        linked = _strings(claim.get("proof_obligations"))
        if not linked:
            findings.append(Finding("ERROR", REGISTRY, f"{cid}: claim must link proof_obligations"))
        if not _strings(claim.get("assumptions")):
            findings.append(Finding("ERROR", REGISTRY, f"{cid}: claim must document assumptions"))
        if not _strings(claim.get("not_claimed")):
            findings.append(Finding("ERROR", REGISTRY, f"{cid}: claim must document not_claimed boundaries"))
        for oid in linked:
            obligation = obligation_by_id.get(oid)
            if obligation is None:
                findings.append(Finding("ERROR", REGISTRY, f"{cid}: missing linked obligation {oid}"))
            elif obligation.get("claim_id") != cid:
                findings.append(Finding("ERROR", REGISTRY, f"{oid}: claim_id does not match {cid}"))

    for oid, obligation in sorted(obligation_by_id.items()):
        cid = str(obligation.get("claim_id", ""))
        if cid not in claim_ids:
            findings.append(Finding("ERROR", REGISTRY, f"{oid}: unknown claim_id {cid or '<missing>'}"))
        if obligation.get("proof_claimed") is not False:
            findings.append(Finding("ERROR", REGISTRY, f"{oid}: proof_claimed must be false"))
        if obligation.get("proof_artifact") not in {None, ""}:
            findings.append(Finding("ERROR", REGISTRY, f"{oid}: proof_artifact must be empty until reviewed proof exists"))
        if not _strings(obligation.get("requirements")):
            findings.append(Finding("ERROR", REGISTRY, f"{oid}: requirements must be non-empty"))
        if not _strings(obligation.get("invariants")):
            findings.append(Finding("ERROR", REGISTRY, f"{oid}: invariants must be non-empty"))
        tools = set(_strings(obligation.get("accepted_tools")))
        if not tools:
            findings.append(Finding("ERROR", REGISTRY, f"{oid}: accepted_tools must be non-empty"))
        unknown_tools = sorted(tools - ALLOWED_TOOLS)
        if unknown_tools:
            findings.append(Finding("ERROR", REGISTRY, f"{oid}: unknown accepted tools: {', '.join(unknown_tools)}"))
        criteria = set(_strings(obligation.get("acceptance_criteria")))
        missing_criteria = sorted(REQUIRED_CRITERIA - criteria)
        if missing_criteria:
            findings.append(Finding("ERROR", REGISTRY, f"{oid}: missing acceptance criteria: {', '.join(missing_criteria)}"))

    _validate_split_registries(findings)

    if not SPEC.exists():
        findings.append(Finding("ERROR", SPEC, "automated reasoning spec missing"))
    else:
        text = SPEC.read_text(encoding="utf-8")
        for phrase in (
            "Proof Obligation Registry",
            "does not claim any proof is complete",
            "CI must not turn planned proofs into claimed evidence",
            "Human Review",
        ):
            if phrase not in text:
                findings.append(Finding("ERROR", SPEC, f"missing proof-obligation boundary phrase: {phrase}"))

    return emit(findings, args.mode, "Proof obligation validation OK")


if __name__ == "__main__":
    raise SystemExit(main())
