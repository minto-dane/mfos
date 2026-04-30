---
spec_id: MFOS-SPEC-45-X86-64-TARGET-PROFILES
title: MFOS x86-64 Target Profiles
canonical_language: en-US
japanese_mirror: missing
status: draft
owner: MFOS architecture
last_reviewed: '2026-04-30'
source_refs:
- FBVBS-001
- X64-INTEL-001
- X64-AMD-001
- X64-LINUX-CET-001
- TCG-001
- NIST-193-001
- EXTREF-X86-64-MICROARCH-LEVELS-0001
- EXTREF-GLIBC-HWCAPS-X86-64-V4-0001
- EXTREF-GCC-X86-64-V4-0001
- EXTREF-INTEL-TDX-OVERVIEW-0001
- EXTREF-INTEL-TDX-ATTESTATION-0001
- EXTREF-AMD-SEV-OVERVIEW-0001
- EXTREF-AMD-SEV-ES-0001
- EXTREF-AMD-SEV-SNP-0001
- EXTREF-AMD-SEV-TIO-0001
- EXTREF-INTEL-SGX-OVERVIEW-0001
- EXTREF-INTEL-SGX-ATTESTATION-0001
- EXTREF-INTEL-SGX-DCAP-0001
- EXTREF-INTEL-CET-0001
- EXTREF-CLANG-CFI-0001
- EXTREF-CLANG-KCFI-0001
- EXTREF-GCC-CF-PROTECTION-0001
- EXTREF-RUST-CF-PROTECTION-0001
- EXTREF-LINUX-KVM-API-0001
- EXTREF-MICROSOFT-HYPERV-TLFS-0001
requirement_refs:
- MFOS-REQ-X64-*
- MFOS-REQ-X64-V4-*
- MFOS-REQ-X64-CVM-*
- MFOS-REQ-X64-TEE-*
- MFOS-REQ-HARDENING-*
- MFOS-REQ-CPUFEAT-*
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs:
- PACK-14
- PACK-31
- PACK-32
- PACK-34
- PACK-36
spec_gap_policy: implementation_must_not_infer_or_fill_gaps
---

# MFOS x86-64 Target Profiles

Status: Draft target-profile policy. This document defines documentation,
requirements, registry, validation, and evidence policy only. It does not
authorize production code, Rust semantic-core work, Dafny semantic changes,
nucleus work, PXM/MFVM/CVM/TEE/SGX runtime work, cluster runtime work,
architecture backends, CPU feature detection, hardware paths, hosted daemons, or
service implementation.

## 1. Purpose

Define x86-64 target profiles for the x86-64-first MFOS implementation plan
without making MFOS x86-64-only. These profiles distinguish baseline,
server-modern, optional v4 performance, maximum-feature, Confidential VM,
enclave/TEE, and hardening-evidence concerns.

All profile feature references must use feature IDs from
`docs/design/registries/cpu-feature-registry.yml`. The profile registry is
`docs/design/registries/cpu-target-profiles.yml`.

## 2. Non-compatibility Statement

MFOS is independently specified. References to `EXTREF-LINUX-KVM-API-0001` and
`EXTREF-MICROSOFT-HYPERV-TLFS-0001` are external comparison/source references
only. MFOS does not claim Hyper-V compatibility, KVM compatibility, Intel TDX
service compatibility, AMD SEV service compatibility, Intel SGX service
compatibility, Linux compatibility, glibc compatibility, GCC compatibility, or
external API compatibility.

## 3. Global Profile Rules

- MFOS is x86-64-first for initial implementation planning.
- MFOS is not x86-64-only.
- Optional x86-64 features must be capability-gated.
- No optional x86-64 feature is globally available unless required by the
  selected conformance profile.
- CPU feature presence does not define MFOS enterprise semantics.
- Missing required profile evidence produces `profile_not_satisfied`,
  `unsupported`, or fail-closed behavior, not silent downgrade.
- Non-x86 support is not claimed as implemented.
- CPU features, target profiles, and platform features are recorded as design
  registry entries until a later implementation gate exists.

## 4. MFOS-X64-BASELINE

Purpose: minimum initial x86-64 profile for early implementation and
verification planning.

Rules:

- Must not require x86-64-v4.
- Must not require TDX, SEV-SNP, or SGX.
- Must not require optional maximum-performance features.
- Must use explicit CPU/platform capability discovery for optional features.
- Must preserve architecture-neutral semantics when optional features are absent.
- Must reference only CPU Feature Registry entries.

Registry requirements:

- Required features: `X64_PROFILE_X86_64_BASELINE`, `X64_FEATURE_NX`,
  `X64_FEATURE_WX_POLICY_SUPPORT`.
- Forbidden features include `X64_FEATURE_X86_64_V4`,
  `X64_FEATURE_INTEL_TDX`, `X64_FEATURE_AMD_SEV_SNP`, and
  `X64_FEATURE_INTEL_SGX`.

## 5. MFOS-X64-SERVER-MODERN

Purpose: modern datacenter x86-64 server profile.

This profile may require or strongly prefer source-grounded server features such
as NX/W^X-capable execution, virtualization extensions, IOMMU, interrupt
remapping, measured boot, TPM or equivalent attestation component, NUMA
awareness, and datacenter-grade observability hooks. The current registry keeps
only NX and W^X as required while the rest remain explicit optional entries
until source-grounded profile rules and evidence gates are complete.

All feature claims must reference CPU Feature Registry IDs and must identify
whether the evidence is build, binary, runtime, platform, or attestation
evidence.

## 6. MFOS-X64-V4-PERFORMANCE

Purpose: optional high-performance profile for systems satisfying x86-64-v4
feature-level requirements.

Rules:

- x86-64-v4 MUST NOT be MFOS baseline.
- x86-64-v4 MUST be optional.
- x86-64-v4 MUST be capability-gated.
- Baseline artifacts MUST NOT contain x86-64-v4-only instructions.
- v4-optimized artifacts MUST be separate from baseline artifacts.
- Runtime or boot-time feature detection MUST select v4 artifacts only on
  v4-capable systems.
- Absence of v4 MUST NOT break architecture-neutral semantics.
- v4 support claims MUST require build flags, feature detection, and binary
  evidence.
- v4 support MUST NOT imply TDX, SEV, SEV-SNP, SGX, CET, CFI, or any unrelated
  feature.
- PXM Core, PXM Guard, nucleus entry/exit, interrupt/trap, context switch,
  VMX/SVM boundary, and other TCB critical paths MUST NOT use v4 instructions by
  default.
- Any TCB v4 use requires ADR, XSAVE/vector-state analysis, test/proof
  obligation, binary evidence, and rollback/fallback behavior.
- v4 profile must reference CPU Feature Registry entries.

Source grounding for the profile name and artifact-routing concepts includes
`EXTREF-X86-64-MICROARCH-LEVELS-0001`,
`EXTREF-GLIBC-HWCAPS-X86-64-V4-0001`, and
`EXTREF-GCC-X86-64-V4-0001`. MFOS does not copy external feature tables.

## 7. MFOS-X64-MAX-FEATURE

Purpose: best-effort profile for newest available x86-64 features.

Rules:

- Features are individually capability-gated.
- No feature may be assumed globally.
- Unsupported features must produce profile-not-satisfied, unsupported, or
  fail-closed behavior, not silent downgrade.
- Build artifacts and feature evidence must identify what is actually enabled.
- All features must reference CPU Feature Registry entries.

This profile is not a product promise. It is a registry and evidence bucket for
future feature-specific claims.

## 8. MFOS-X64-CVM-INTEL-TDX

Purpose: Confidential VM profile for Intel TDX-capable platforms.

Rules:

- TDX is an allowed feature/profile name.
- TDX support must be source-grounded by `EXTREF-INTEL-TDX-OVERVIEW-0001` and
  `EXTREF-INTEL-TDX-ATTESTATION-0001`.
- TDX support must not imply Hyper-V/KVM compatibility.
- TDX support must not imply SGX support.
- TDX launch, measurement, attestation, and secret-release semantics must be
  specified before implementation.
- TDX-related features must reference CPU Feature Registry entries.

No TDX runtime, launch path, attestation service, secret-release service, or CVM
implementation is authorized by this profile.

## 9. MFOS-X64-CVM-AMD-SEV-SNP

Purpose: Confidential VM profile for AMD SEV-SNP-capable platforms.

Rules:

- SEV, SEV-ES, SEV-SNP, and SEV-TIO are allowed feature/profile names when used
  as external technology references or MFOS profile requirements.
- SEV-SNP support must be source-grounded by
  `EXTREF-AMD-SEV-OVERVIEW-0001`, `EXTREF-AMD-SEV-ES-0001`,
  `EXTREF-AMD-SEV-SNP-0001`, and `EXTREF-AMD-SEV-TIO-0001` where applicable.
- SEV-SNP support must not imply KVM compatibility.
- SEV-SNP launch, memory integrity, attestation, and secret-release semantics
  must be specified before implementation.
- SEV-related features must reference CPU Feature Registry entries.

No SEV-SNP runtime, launch path, attestation service, secret-release service, or
CVM implementation is authorized by this profile.

## 10. MFOS-X64-TEE-INTEL-SGX

Purpose: optional Intel SGX enclave / TEE profile.

Rules:

- Intel SGX MUST NOT be MFOS baseline.
- Intel SGX MUST NOT be modeled as a Confidential VM profile.
- SGX is an enclave/application TEE profile, not a VM-wide confidential
  computing profile.
- SGX support MUST be capability-gated and platform-enabled.
- Absence of SGX MUST NOT change architecture-neutral MFOS semantics.
- SGX attestation mode MUST be modeled separately from SGX feature presence.
- SGX use in the MFOS TCB requires ADR, threat model, attestation evidence, and
  side-channel risk analysis.
- SGX support does not imply TDX support.
- SGX support does not imply Hyper-V or KVM compatibility.
- SGX-related features must reference CPU Feature Registry entries.

SGX source grounding uses `EXTREF-INTEL-SGX-OVERVIEW-0001`,
`EXTREF-INTEL-SGX-ATTESTATION-0001`, and `EXTREF-INTEL-SGX-DCAP-0001`.

## 11. MFOS-HARDENING-CET-CFI

Purpose: hardening evidence profile.

Rules:

- CET/CFI are build/toolchain/binary evidence requirements, not language
  replacements.
- CET/CFI support must be verified by emitted binary evidence and toolchain
  flags.
- Rust safety does not replace CFI/CET evidence where a profile requires it.
- C/C++ exceptions must use relevant CFI/CET mitigations where applicable and
  supported.
- CET/CFI feature claims must reference CPU Feature Registry entries where CPU
  support is involved.

Relevant source refs include `EXTREF-INTEL-CET-0001`,
`X64-LINUX-CET-001`, `EXTREF-CLANG-CFI-0001`,
`EXTREF-CLANG-KCFI-0001`, `EXTREF-GCC-CF-PROTECTION-0001`, and
`EXTREF-RUST-CF-PROTECTION-0001`.

## 12. CPU Feature Registry Requirements

The CPU Feature Registry must record:

- `feature_id`
- `name`
- `architecture`
- `feature_kind`
- `status`
- `source_refs`
- `profile_affinity`
- `required_for_profiles`
- `optional_for_profiles`
- `forbidden_in_profiles`
- `forbidden_in_components`
- `capability_detection`
- `build_evidence_required`
- `binary_evidence_required`
- `runtime_evidence_required`
- `security_semantics_dependency`
- `fallback_behavior`
- `attestation`
- `side_channel_risk_review_required`
- `notes`
- `review_status`

The registry must not detect CPU features. It records identity, source
grounding, profile membership, evidence expectations, usage restrictions, and
review status.

## 13. CPU Target Profile Registry Requirements

The CPU Target Profile Registry must record:

- `profile_id`
- `architecture`
- `purpose`
- `required_features`
- `optional_features`
- `forbidden_features`
- `required_platform_features`
- `required_build_evidence`
- `required_binary_evidence`
- `required_runtime_evidence`
- `fallback_behavior`
- `not_claimed`
- `source_refs`
- `requirements`
- `tests`
- `evidence_required`
- `review_status`

Profiles must reference CPU features through registry IDs, not prose-only
claims.

## 14. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| `MFOS-REQ-X64-0001` | MFOS MUST define an x86-64 baseline profile. | registry validator |
| `MFOS-REQ-X64-0002` | MFOS MUST define a modern server x86-64 profile. | registry validator |
| `MFOS-REQ-X64-0003` | MFOS MUST define a maximum-feature x86-64 profile with feature detection gates. | registry validator |
| `MFOS-REQ-X64-0004` | Optional x86-64 features MUST be capability-gated. | x64 profile validator |
| `MFOS-REQ-X64-0005` | Absence of optional x86-64 features MUST NOT change architecture-neutral semantics. | architecture validator |
| `MFOS-REQ-X64-V4-0001` | MFOS MUST define x86-64-v4 as optional performance profile, not baseline. | x64 profile validator |
| `MFOS-REQ-X64-CVM-0001` | Intel TDX MUST be modeled as a Confidential VM profile, not a global baseline requirement. | CPU registry validator |
| `MFOS-REQ-X64-CVM-0002` | AMD SEV-SNP MUST be modeled as a Confidential VM profile, not a global baseline requirement. | CPU registry validator |
| `MFOS-REQ-X64-TEE-0001` | Intel SGX MUST be modeled as optional enclave/TEE profile, not baseline. | CPU registry validator |
| `MFOS-REQ-X64-TEE-0002` | Intel SGX MUST NOT be modeled as a Confidential VM profile. | CPU registry validator |
| `MFOS-REQ-HARDENING-0001` | CET/CFI claims MUST require build, toolchain, binary, and runtime/platform evidence. | hardening evidence review |
| `MFOS-REQ-CPUFEAT-0001` | MFOS MUST maintain a machine-readable CPU Feature Registry. | CPU registry validator |

The full requirement entries live in
`docs/design/registries/requirements.yaml`.

## 15. Failure Modes

| Failure | Required result |
| --- | --- |
| Baseline requires x86-64-v4 | validation fails |
| Baseline requires TDX, SEV-SNP, or SGX | validation fails |
| x86-64-v4 profile implies CVM, SGX, CET, or CFI | validation fails |
| CVM profile implies v4 performance | validation fails |
| SGX profile is classified as CVM | validation fails |
| SGX feature presence is treated as SGX attestation mode | validation fails |
| Optional feature missing after claim | profile-not-satisfied, unsupported, or fail-closed behavior |
| Feature status implies implementation without evidence | validation fails |

## 16. Negative Tests

- `NEG-MFOS-X64-BASELINE-V4-0001`: baseline requires v4; validation fails.
- `NEG-MFOS-X64-BASELINE-CVM-TEE-0001`: baseline requires TDX, SEV-SNP, or SGX;
  validation fails.
- `NEG-MFOS-X64-V4-TCB-0001`: TCB path uses v4 without ADR, XSAVE/vector-state
  analysis, tests/proofs, binary evidence, and fallback; validation fails.
- `NEG-MFOS-X64-CVM-TDX-SGX-0001`: TDX profile implies SGX; validation fails.
- `NEG-MFOS-X64-TEE-SGX-CVM-0001`: SGX profile is marked CVM; validation fails.
- `NEG-MFOS-X64-TEE-SGX-ATTESTATION-CONFLATE-0001`: SGX feature presence is
  treated as DCAP/EPID attestation mode; validation fails.

## 17. Evidence Requirements

Evidence required before any implementation or support claim:

- Source-card coverage.
- Requirement coverage.
- CPU Feature Registry entry.
- CPU Target Profile Registry entry.
- Positive and negative tests.
- CI validation.
- Build flag evidence where a profile depends on build choices.
- Binary inspection evidence where a profile depends on emitted instructions or
  hardening properties.
- Runtime/platform evidence where a profile depends on discovered capabilities.
- Attestation evidence where a profile depends on TDX, SEV-SNP, SGX attestation,
  or measured boot.
- ADR and side-channel review for any TCB use of optional v4 or SGX features.

## 18. Spec Gaps

- `X64-GAP-0001`: no CPU feature detection implementation exists.
- `X64-GAP-0002`: no architecture backend implementation exists.
- `X64-GAP-0003`: no CVM runtime exists.
- `X64-GAP-0004`: no SGX enclave runtime exists.
- `X64-GAP-0005`: no production hardening evidence exists.
