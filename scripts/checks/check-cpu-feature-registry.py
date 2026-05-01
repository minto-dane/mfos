#!/usr/bin/env python3
"""Validate CPU feature and target profile registry policy."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg, source_ids


FEATURE_REGISTRY = ROOT / "docs/design/registries/cpu-feature-registry.yml"
PROFILE_REGISTRY = ROOT / "docs/design/registries/cpu-target-profiles.yml"
TEST_REGISTRY = ROOT / "docs/design/registries/tests.yaml"
EVIDENCE_REGISTRY = ROOT / "docs/design/registries/evidence.yaml"

REQUIRED_FEATURE_FIELDS = {
    "feature_id",
    "name",
    "architecture",
    "feature_kind",
    "status",
    "source_refs",
    "profile_affinity",
    "required_for_profiles",
    "optional_for_profiles",
    "forbidden_in_profiles",
    "forbidden_in_components",
    "capability_detection",
    "build_evidence_required",
    "binary_evidence_required",
    "runtime_evidence_required",
    "security_semantics_dependency",
    "fallback_behavior",
    "attestation",
    "side_channel_risk_review_required",
    "notes",
    "review_status",
}
REQUIRED_PROFILE_FIELDS = {
    "profile_id",
    "profile_kind",
    "architecture",
    "purpose",
    "required_features",
    "optional_features",
    "forbidden_features",
    "required_platform_features",
    "required_build_evidence",
    "required_binary_evidence",
    "required_runtime_evidence",
    "fallback_behavior",
    "not_claimed",
    "source_refs",
    "requirements",
    "tests",
    "evidence_required",
    "review_status",
}
REQUIRED_FEATURE_IDS = {
    "X64_PROFILE_X86_64_BASELINE",
    "X64_PROFILE_X86_64_V2",
    "X64_PROFILE_X86_64_V3",
    "X64_PROFILE_X86_64_V4",
    "X64_FEATURE_NX",
    "X64_FEATURE_WX_POLICY_SUPPORT",
    "X64_FEATURE_SMEP",
    "X64_FEATURE_SMAP",
    "X64_FEATURE_INTEL_VMX",
    "X64_FEATURE_AMD_SVM",
    "X64_FEATURE_IOMMU_INTEL_VT_D",
    "X64_FEATURE_IOMMU_AMD_VI",
    "X64_FEATURE_INTERRUPT_REMAPPING",
    "X64_FEATURE_INTEL_TDX",
    "X64_FEATURE_AMD_SEV",
    "X64_FEATURE_AMD_SEV_ES",
    "X64_FEATURE_AMD_SEV_SNP",
    "X64_FEATURE_AMD_SEV_TIO",
    "X64_FEATURE_INTEL_SGX",
    "X64_FEATURE_INTEL_SGX_DCAP_ATTESTATION",
    "X64_FEATURE_INTEL_SGX_EPID_ATTESTATION",
    "X64_FEATURE_INTEL_CET",
    "X64_FEATURE_CET_SHADOW_STACK",
    "X64_FEATURE_CET_IBT",
    "X64_FEATURE_CFI_TOOLCHAIN",
    "X64_FEATURE_X86_64_V4",
    "X64_FEATURE_AVX512_CLASS",
    "X64_FEATURE_XSAVE_STATE_MANAGEMENT",
    "X64_FEATURE_NUMA_TOPOLOGY",
    "X64_FEATURE_TPM_OR_MEASURED_BOOT",
}
REQUIRED_PROFILES = {
    "MFOS-X64-BASELINE",
    "MFOS-X64-SERVER-MODERN",
    "MFOS-X64-V4-PERFORMANCE",
    "MFOS-X64-MAX-FEATURE",
    "MFOS-X64-CVM-INTEL-TDX",
    "MFOS-X64-CVM-AMD-SEV-SNP",
    "MFOS-X64-TEE-INTEL-SGX",
    "MFOS-HARDENING-CET-CFI",
}
BASELINE_FORBIDDEN = {
    "X64_PROFILE_X86_64_V4",
    "X64_FEATURE_X86_64_V4",
    "X64_FEATURE_INTEL_TDX",
    "X64_FEATURE_AMD_SEV_SNP",
    "X64_FEATURE_INTEL_SGX",
}
V4_UNRELATED = {
    "X64_FEATURE_INTEL_TDX",
    "X64_FEATURE_AMD_SEV",
    "X64_FEATURE_AMD_SEV_ES",
    "X64_FEATURE_AMD_SEV_SNP",
    "X64_FEATURE_AMD_SEV_TIO",
    "X64_FEATURE_INTEL_SGX",
    "X64_FEATURE_INTEL_CET",
    "X64_FEATURE_CFI_TOOLCHAIN",
}
CVM_V4 = {"X64_PROFILE_X86_64_V4", "X64_FEATURE_X86_64_V4"}
SGX_FORBIDDEN = {
    "X64_FEATURE_INTEL_TDX",
    "X64_FEATURE_AMD_SEV",
    "X64_FEATURE_AMD_SEV_ES",
    "X64_FEATURE_AMD_SEV_SNP",
    "X64_FEATURE_AMD_SEV_TIO",
}


def _entries(path: Path, id_key: str, findings: list[Finding]) -> dict[str, dict[str, object]]:
    data = load_yaml(path)
    if not isinstance(data, dict):
        findings.append(Finding("ERROR", path, "registry must be a mapping"))
        return {}
    if data.get("implementation_allowed") is not False:
        findings.append(Finding("ERROR", path, "implementation_allowed must be false"))
    if data.get("design_only") is not True:
        findings.append(Finding("ERROR", path, "design_only must be true"))
    result: dict[str, dict[str, object]] = {}
    for idx, entry in enumerate(data.get("entries", []), 1):
        if not isinstance(entry, dict):
            findings.append(Finding("ERROR", path, f"entry #{idx} is not a mapping"))
            continue
        item_id = entry.get(id_key)
        if not isinstance(item_id, str) or not item_id:
            findings.append(Finding("ERROR", path, f"entry #{idx} missing {id_key}"))
            continue
        if item_id in result:
            findings.append(Finding("ERROR", path, f"duplicate {id_key}: {item_id}"))
        result[item_id] = entry
    return result


def _strings(entry: dict[str, object], field: str) -> list[str]:
    value = entry.get(field)
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def _registry_ids(path: Path, id_key: str) -> set[str]:
    data = load_yaml(path)
    if not isinstance(data, dict):
        return set()
    result: set[str] = set()
    for entry in data.get("entries", []):
        if isinstance(entry, dict) and isinstance(entry.get(id_key), str):
            result.add(entry[id_key])
    return result


def _check_sources(path: Path, owner_id: str, refs: list[str], known_sources: set[str], findings: list[Finding]) -> None:
    if not refs:
        findings.append(Finding("ERROR", path, f"{owner_id}: source_refs must not be empty"))
        return
    for ref in refs:
        if ref not in known_sources:
            findings.append(Finding("ERROR", path, f"{owner_id}: unknown source_ref {ref}"))


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []
    known_sources = source_ids()
    known_tests = _registry_ids(TEST_REGISTRY, "test_id")
    known_evidence = _registry_ids(EVIDENCE_REGISTRY, "evidence_id")

    features = _entries(FEATURE_REGISTRY, "feature_id", findings)
    profiles = _entries(PROFILE_REGISTRY, "profile_id", findings)
    feature_ids = set(features)
    profile_ids = set(profiles)

    missing_features = sorted(REQUIRED_FEATURE_IDS - feature_ids)
    if missing_features:
        findings.append(Finding("ERROR", FEATURE_REGISTRY, "missing required feature IDs: " + ", ".join(missing_features)))
    missing_profiles = sorted(REQUIRED_PROFILES - profile_ids)
    if missing_profiles:
        findings.append(Finding("ERROR", PROFILE_REGISTRY, "missing required target profiles: " + ", ".join(missing_profiles)))

    for feature_id, entry in features.items():
        missing = sorted(REQUIRED_FEATURE_FIELDS - set(entry))
        if missing:
            findings.append(Finding("ERROR", FEATURE_REGISTRY, f"{feature_id}: missing fields: {', '.join(missing)}"))
        _check_sources(FEATURE_REGISTRY, feature_id, _strings(entry, "source_refs"), known_sources, findings)
        for field in ("profile_affinity", "required_for_profiles", "optional_for_profiles", "forbidden_in_profiles"):
            for profile_id in _strings(entry, field):
                if profile_id not in profile_ids:
                    findings.append(Finding("ERROR", FEATURE_REGISTRY, f"{feature_id}: {field} references missing profile_id {profile_id}"))
        for profile_id in _strings(entry, "required_for_profiles"):
            profile = profiles.get(profile_id, {})
            required_refs = set(_strings(profile, "required_features") + _strings(profile, "required_platform_features"))
            if feature_id not in required_refs:
                findings.append(Finding("ERROR", FEATURE_REGISTRY, f"{feature_id}: required_for_profiles lists {profile_id}, but target profile does not require it"))
        for profile_id in _strings(entry, "optional_for_profiles"):
            profile = profiles.get(profile_id, {})
            if feature_id not in set(_strings(profile, "optional_features")):
                findings.append(Finding("ERROR", FEATURE_REGISTRY, f"{feature_id}: optional_for_profiles lists {profile_id}, but target profile does not list it as optional"))
        for profile_id in _strings(entry, "forbidden_in_profiles"):
            profile = profiles.get(profile_id, {})
            if feature_id not in set(_strings(profile, "forbidden_features")):
                findings.append(Finding("ERROR", FEATURE_REGISTRY, f"{feature_id}: forbidden_in_profiles lists {profile_id}, but target profile does not forbid it"))
        detection = entry.get("capability_detection")
        if not isinstance(detection, dict):
            findings.append(Finding("ERROR", FEATURE_REGISTRY, f"{feature_id}: capability_detection must be a mapping"))
        elif detection.get("design_status") in {"implemented", "validated", "released"}:
            findings.append(Finding("ERROR", FEATURE_REGISTRY, f"{feature_id}: design registry must not claim implemented or validated feature detection"))
        if entry.get("review_status") in {"implemented", "validated", "released"}:
            findings.append(Finding("ERROR", FEATURE_REGISTRY, f"{feature_id}: review_status overclaims implementation evidence"))
        if feature_id in {"X64_PROFILE_X86_64_V4", "X64_FEATURE_X86_64_V4"}:
            forbidden_components = set(_strings(entry, "forbidden_in_components"))
            required_components = {"PXM_CORE", "PXM_GUARD", "NUCLEUS_ENTRY_EXIT", "INTERRUPT_TRAP", "CONTEXT_SWITCH", "VMX_SVM_BOUNDARY"}
            if not required_components.issubset(forbidden_components):
                findings.append(Finding("ERROR", FEATURE_REGISTRY, f"{feature_id}: missing default TCB v4 forbidden components"))
            if entry.get("security_semantics_dependency") != "none":
                findings.append(Finding("ERROR", FEATURE_REGISTRY, f"{feature_id}: v4 cannot define security semantics"))
        if feature_id.startswith("X64_FEATURE_INTEL_SGX"):
            if entry.get("feature_kind") != "enclave_tee":
                findings.append(Finding("ERROR", FEATURE_REGISTRY, f"{feature_id}: SGX entries must be enclave_tee"))
            if "MFOS-X64-CVM-INTEL-TDX" in _strings(entry, "required_for_profiles"):
                findings.append(Finding("ERROR", FEATURE_REGISTRY, f"{feature_id}: SGX must not be required for TDX CVM profile"))

    for profile_id, entry in profiles.items():
        missing = sorted(REQUIRED_PROFILE_FIELDS - set(entry))
        if missing:
            findings.append(Finding("ERROR", PROFILE_REGISTRY, f"{profile_id}: missing fields: {', '.join(missing)}"))
        _check_sources(PROFILE_REGISTRY, profile_id, _strings(entry, "source_refs"), known_sources, findings)
        for test_id in _strings(entry, "tests"):
            if test_id not in known_tests:
                findings.append(Finding("ERROR", PROFILE_REGISTRY, f"{profile_id}: references missing test_id {test_id}"))
        for evidence_id in _strings(entry, "evidence_required"):
            if evidence_id not in known_evidence:
                findings.append(Finding("ERROR", PROFILE_REGISTRY, f"{profile_id}: references missing evidence_id {evidence_id}"))
        refs = (
            _strings(entry, "required_features")
            + _strings(entry, "optional_features")
            + _strings(entry, "forbidden_features")
            + _strings(entry, "required_platform_features")
        )
        for feature_id in refs:
            if feature_id not in feature_ids:
                findings.append(Finding("ERROR", PROFILE_REGISTRY, f"{profile_id}: references missing feature_id {feature_id}"))
        required = set(_strings(entry, "required_features"))
        optional = set(_strings(entry, "optional_features"))
        forbidden = set(_strings(entry, "forbidden_features"))
        not_claimed = " ".join(_strings(entry, "not_claimed")).lower()
        if profile_id == "MFOS-X64-BASELINE":
            if required & BASELINE_FORBIDDEN:
                findings.append(Finding("ERROR", PROFILE_REGISTRY, "MFOS-X64-BASELINE requires forbidden optional/CVM/TEE features"))
            if not BASELINE_FORBIDDEN.issubset(forbidden):
                findings.append(Finding("ERROR", PROFILE_REGISTRY, "MFOS-X64-BASELINE must forbid v4, TDX, SEV-SNP, and SGX"))
        if profile_id == "MFOS-X64-V4-PERFORMANCE":
            if (required | optional) & V4_UNRELATED:
                findings.append(Finding("ERROR", PROFILE_REGISTRY, "v4 profile must not require or list optional TDX/SEV/SGX/CET/CFI"))
            if not V4_UNRELATED.issubset(forbidden):
                findings.append(Finding("ERROR", PROFILE_REGISTRY, "v4 profile must explicitly not imply TDX/SEV/SGX/CET/CFI"))
            if "baseline" not in not_claimed:
                findings.append(Finding("ERROR", PROFILE_REGISTRY, "v4 profile must state it is not baseline"))
        if entry.get("profile_kind") == "confidential_vm":
            if required & CVM_V4 or optional & CVM_V4:
                findings.append(Finding("ERROR", PROFILE_REGISTRY, f"{profile_id}: CVM profile must not imply x86-64-v4"))
            if "X64_FEATURE_INTEL_SGX" not in forbidden:
                findings.append(Finding("ERROR", PROFILE_REGISTRY, f"{profile_id}: CVM profile must forbid SGX implication"))
        if profile_id == "MFOS-X64-TEE-INTEL-SGX":
            if entry.get("profile_kind") != "enclave_tee":
                findings.append(Finding("ERROR", PROFILE_REGISTRY, "SGX target profile must be enclave_tee, not CVM"))
            if "X64_FEATURE_INTEL_SGX" not in required:
                findings.append(Finding("ERROR", PROFILE_REGISTRY, "SGX target profile must require SGX feature presence"))
            if (required | optional) & SGX_FORBIDDEN:
                findings.append(Finding("ERROR", PROFILE_REGISTRY, "SGX profile must not require or list optional TDX or SEV-family CVM features"))
            if not SGX_FORBIDDEN.issubset(forbidden):
                findings.append(Finding("ERROR", PROFILE_REGISTRY, "SGX profile must forbid TDX and SEV-family CVM implication"))
            runtime = " ".join(_strings(entry, "required_runtime_evidence")).lower()
            if "attestation_mode" not in runtime or "feature_presence" not in runtime:
                findings.append(Finding("ERROR", PROFILE_REGISTRY, "SGX feature presence and attestation mode must be separate evidence"))
        if profile_id == "MFOS-HARDENING-CET-CFI":
            if "memory safety" not in not_claimed or "formal verification" not in not_claimed:
                findings.append(Finding("ERROR", PROFILE_REGISTRY, "CET/CFI profile must not imply memory safety or formal verification"))

    return emit(findings, args.mode, "CPU feature registry check OK")


if __name__ == "__main__":
    raise SystemExit(main())
