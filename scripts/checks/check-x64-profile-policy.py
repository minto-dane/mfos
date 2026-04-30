#!/usr/bin/env python3
"""Check x86-64 target profile policy text and registry anchors."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg


SPEC = ROOT / "docs/design/specs/45-x86-64-target-profiles.md"
PROFILES = ROOT / "docs/design/registries/cpu-target-profiles.yml"

REQUIRED_PHRASES = {
    "MFOS is x86-64-first",
    "MFOS is not x86-64-only",
    "Optional x86-64 features must be capability-gated",
    "x86-64-v4 MUST NOT be MFOS baseline",
    "x86-64-v4 MUST be optional",
    "v4 support MUST NOT imply TDX, SEV, SEV-SNP, SGX, CET, CFI",
    "Baseline artifacts MUST NOT contain x86-64-v4-only instructions",
    "PXM Core, PXM Guard, nucleus entry/exit, interrupt/trap, context switch",
    "TDX support must not imply SGX support",
    "SEV-SNP support must not imply KVM compatibility",
    "Intel SGX MUST NOT be modeled as a Confidential VM profile",
    "SGX attestation mode MUST be modeled separately from SGX feature presence",
    "CET/CFI are build/toolchain/binary evidence requirements",
}


def _entries(path: Path) -> dict[str, dict[str, object]]:
    data = load_yaml(path)
    if not isinstance(data, dict):
        return {}
    return {
        str(entry["profile_id"]): entry
        for entry in data.get("entries", [])
        if isinstance(entry, dict) and isinstance(entry.get("profile_id"), str)
    }


def _strings(entry: dict[str, object], field: str) -> list[str]:
    value = entry.get(field)
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    text = SPEC.read_text(encoding="utf-8") if SPEC.exists() else ""
    normalized_text = " ".join(text.split())
    if not text:
        findings.append(Finding("ERROR", SPEC, "x86-64 target profile spec missing"))
    for phrase in sorted(REQUIRED_PHRASES):
        if phrase not in normalized_text:
            findings.append(Finding("ERROR", SPEC, f"missing required profile policy phrase: {phrase}"))

    profiles = _entries(PROFILES)
    baseline = profiles.get("MFOS-X64-BASELINE", {})
    v4 = profiles.get("MFOS-X64-V4-PERFORMANCE", {})
    tdx = profiles.get("MFOS-X64-CVM-INTEL-TDX", {})
    sev = profiles.get("MFOS-X64-CVM-AMD-SEV-SNP", {})
    sgx = profiles.get("MFOS-X64-TEE-INTEL-SGX", {})
    hardening = profiles.get("MFOS-HARDENING-CET-CFI", {})

    baseline_required = set(_strings(baseline, "required_features"))
    if baseline_required & {"X64_PROFILE_X86_64_V4", "X64_FEATURE_X86_64_V4", "X64_FEATURE_INTEL_TDX", "X64_FEATURE_AMD_SEV_SNP", "X64_FEATURE_INTEL_SGX"}:
        findings.append(Finding("ERROR", PROFILES, "baseline profile requires v4, TDX, SEV-SNP, or SGX"))

    if "X64_FEATURE_X86_64_V4" not in set(_strings(v4, "required_features")):
        findings.append(Finding("ERROR", PROFILES, "v4 profile must require the v4 feature registry ID"))
    if set(_strings(v4, "required_features")) & {"X64_FEATURE_INTEL_TDX", "X64_FEATURE_AMD_SEV", "X64_FEATURE_AMD_SEV_SNP", "X64_FEATURE_INTEL_SGX", "X64_FEATURE_INTEL_CET", "X64_FEATURE_CFI_TOOLCHAIN"}:
        findings.append(Finding("ERROR", PROFILES, "v4 profile implies unrelated CVM/TEE/hardening feature"))

    for profile_id, entry in (("MFOS-X64-CVM-INTEL-TDX", tdx), ("MFOS-X64-CVM-AMD-SEV-SNP", sev)):
        if entry.get("profile_kind") != "confidential_vm":
            findings.append(Finding("ERROR", PROFILES, f"{profile_id} must be confidential_vm"))
        features = set(_strings(entry, "required_features") + _strings(entry, "optional_features"))
        if "X64_FEATURE_X86_64_V4" in features or "X64_PROFILE_X86_64_V4" in features:
            findings.append(Finding("ERROR", PROFILES, f"{profile_id} must not imply x86-64-v4"))
        if "X64_FEATURE_INTEL_SGX" in features:
            findings.append(Finding("ERROR", PROFILES, f"{profile_id} must not imply SGX"))

    if sgx.get("profile_kind") != "enclave_tee":
        findings.append(Finding("ERROR", PROFILES, "SGX profile must be enclave_tee"))
    if "X64_FEATURE_INTEL_SGX" not in set(_strings(sgx, "required_features")):
        findings.append(Finding("ERROR", PROFILES, "SGX profile must require X64_FEATURE_INTEL_SGX"))
    sgx_runtime = set(_strings(sgx, "required_runtime_evidence"))
    if "sgx_feature_presence_evidence" not in sgx_runtime or "sgx_attestation_mode_evidence" not in sgx_runtime:
        findings.append(Finding("ERROR", PROFILES, "SGX attestation mode must be separate from feature presence"))

    not_claimed = " ".join(_strings(hardening, "not_claimed")).lower()
    if "rust safety replacement" not in not_claimed:
        findings.append(Finding("ERROR", PROFILES, "CET/CFI profile must not let Rust safety replace evidence"))

    return emit(findings, args.mode, "x86-64 profile policy check OK")


if __name__ == "__main__":
    raise SystemExit(main())
