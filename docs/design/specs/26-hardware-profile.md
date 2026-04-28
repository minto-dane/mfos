---
spec_id: "MFOS-SPEC-26-HARDWARE-PROFILE"
title: "MFOS x64 Hardware and Profile Matrix Specification v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "MS-VBS-001", "MS-VSM-001", "NIST-160-001", "NIST-193-001", "TCG-001", "X64-AMD-001", "X64-INTEL-001", "X64-LINUX-CET-001", "X64-LINUX-PKU-001"]
requirement_refs: ["MFOS-REQ-HW-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS x64 Hardware and Profile Matrix Specification v0.1

Status: Draft design split

Owner area: `docs/design/specs/26-hardware-profile.md`

This document defines the x64 hardware and platform profile matrix for MFOS.

MFOS is z/OS-inspired and source-grounded. It does not claim compatibility with IBM products, z/Architecture, z/OS APIs, RACF, JES, DFSMS, SMF, JCL, or z/Architecture storage keys. x64 PKU, PKS, CET, SMEP, SMAP, NX, IOMMU, VT-x, AMD-V, EPT, NPT, TPM, Secure Boot, and measured boot are enforcement aids and evidence sources. They do not replace MFOS authorization, audit, object model, or Guard root semantics.

## 1. Purpose

This specification exists to:

- Define required and optional x64 CPU/platform features by Baseline, Enterprise-Standalone, Enterprise-PXM, and High-Assurance profiles.
- Separate Intel and AMD implementation notes without creating two different MFOS semantics.
- Prevent overclaims about PKU, PKS, CET, IOMMU, TPM, measured boot, or virtualization.
- Define profile gating for device assignment, PXM, PXM Guard, update, recovery, and audit evidence.
- Define feature detection APIs that must be specified before implementation can rely on hardware behavior.
- Define failure modes, negative tests, evidence artifacts, and gaps for platform conformance.

## 2. Scope

This specification covers:

- x86_64 CPU and platform feature profile matrix.
- Intel and AMD notes for feature discovery and backend differences.
- Required versus optional feature behavior.
- PKU, PKS, and CET limitations.
- NX, W^X, SMEP, SMAP, page table, and executable mapping expectations.
- IOMMU and interrupt remapping requirements.
- VT-x/EPT and AMD-V/SVM/NPT profile roles.
- TPM, Secure Boot, measured boot, and event log expectations.
- Detection API requirements.
- Failure modes.
- Tests and negative tests.
- Evidence artifacts.
- SPEC_GAPs.

This specification does not cover:

- Device-specific driver implementation.
- Final page table layout.
- Final VMX/SVM backend implementation.
- Final TPM quote protocol.
- Final attestation claims.
- Firmware vendor certification.
- Cryptographic primitive proofs.
- Non-x64 ports.

## 3. Source Matrix References

| Source ID | Use |
| --- | --- |
| X64-INTEL-001 | Intel x64 protection, paging, interrupt, VMX, EPT, MSR, CET, PKU, PKS where applicable. |
| X64-AMD-001 | AMD64 protection, paging, interrupt, SVM, NPT, AMD-specific system programming differences. |
| X64-LINUX-PKU-001 | PKU limitation reference: data access oriented, thread-local PKRU behavior, not instruction-fetch protection. |
| X64-LINUX-CET-001 | CET deployment and limitation reference for shadow stack and IBT style control-flow hardening. |
| TCG-001 | TPM, measured boot, firmware measurement, and event log reference. |
| NIST-160-001 | Secure system engineering lifecycle reference. |
| NIST-193-001 | Firmware resiliency and recovery framing. |
| MS-VBS-001 | Informative executable mapping and code integrity isolation reference for High-Assurance Guard only. |
| MS-VSM-001 | Informative higher-privilege root-object isolation reference for Guard only. |
| FBVBS-001 | Internal transfer source for profile gates, command discipline, evidence, and no-fake-success requirements. |

## 4. Normative Language

- `MUST`: required for the applicable profile.
- `SHOULD`: strongly recommended; deviation requires an ADR and evidence.
- `MAY`: optional.
- `MUST NOT`: prohibited.
- `UNSUPPORTED`: specified behavior not implemented or not available on the detected platform.
- `SPEC_GAP`: behavior undefined by specification; implementation must not invent success.

## 5. Profile Definitions

```text
Baseline:
  Development and small-scale semantic prototype profile.
  Must preserve MFOS authorization, audit, no-fake-success, and basic memory
  safety claims, but may run without full PXM or Guard.

Enterprise:
  Production-oriented profile.
  Requires measured boot evidence, TPM where applicable, stronger device
  isolation, remote audit/export expectations, update provenance, and stricter
  platform conformance.

High-Assurance:
  Highest assurance profile.
  Requires PXM and Guard for selected root objects, stronger boot evidence,
  strict device assignment gating, Guard-sealed roots, and attestation evidence.
```

## 6. Hardware Claim Rules

```text
HW-CLAIM-001:
  Hardware features are mechanisms, not MFOS semantic roots.

HW-CLAIM-002:
  Authorization is decided by securityd, not by PKU, PKS, CET, IOMMU, TPM,
  Secure Boot, measured boot, VMX, SVM, EPT, or NPT.

HW-CLAIM-003:
  Audit evidence is produced by auditd and profile-specific audit sinks, not by
  CPU feature presence alone.

HW-CLAIM-004:
  Guard root protection in High-Assurance requires Guard. PKU, PKS, CET, page
  table bits, or IOMMU alone are not Guard.

HW-CLAIM-005:
  x64 features MUST NOT be described as implementing z/Architecture storage
  keys or as storage-key-compatible.

HW-CLAIM-006:
  Platform feature detection MUST be authoritative before a profile claim can
  rely on a feature.
```

## 7. Profile Matrix

### 7.1 CPU and Memory Protection

| Feature | Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance | Notes |
| --- | --- | --- | --- | --- | --- |
| x86_64 long mode | MUST | MUST | MUST | MUST | MFOS x64 profile requires 64-bit mode. |
| Page tables with supervisor/user separation | MUST | MUST | MUST | MUST | Required for nucleus/user separation. |
| NX/XD execute-disable | MUST | MUST | MUST | MUST | Required for non-executable data mappings. |
| W^X policy | MUST | MUST | MUST | MUST | Writable and executable at once is prohibited unless a future spec defines a safe transition. |
| Ring 0 / Ring 3 separation | MUST | MUST | MUST | MUST | Required baseline privilege separation. |
| SMEP | SHOULD when available | MUST when available | MUST when available | MUST when available | Absence blocks claims that require SMEP, but not all Baseline boot. |
| SMAP | SHOULD when available | MUST when available | MUST when available | MUST when available | Copy-in/copy-out remains required even with SMAP. |
| CET shadow stack | MAY | SHOULD for trusted services when supported | SHOULD for trusted services when supported | SHOULD; MAY become MUST for a pinned HA platform | Control-flow hardening only. |
| CET IBT | MAY | SHOULD for trusted services when supported | SHOULD for trusted services when supported | SHOULD; MAY become MUST for a pinned HA platform | Control-flow hardening only. |
| PKU | MAY for user compartments | MAY for user compartments | MAY for user compartments | MAY for user compartments | Data-access helper only. |
| PKS | MAY when available | MAY for kernel metadata helper | MAY for kernel metadata helper | MAY for kernel metadata helper | Cannot replace Guard. |
| PCID/INVPCID | MAY | SHOULD | SHOULD | SHOULD | Performance and TLB hygiene helper; not a security root alone. |
| 1GiB pages | MAY | MAY | MAY | MAY | Must not weaken W^X or isolation. |

### 7.2 Virtualization and Partitioning

| Feature | Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance | Notes |
| --- | --- | --- | --- | --- | --- |
| PXM implicit single partition backend | MAY | MUST for non-PXM claim | MAY for development only | MUST NOT support HA claim | API must still be partition-aware. |
| Intel VT-x | OPTIONAL | NOT REQUIRED | SHOULD for Intel PXM backend | MUST for Intel HA PXM backend if Intel platform | Required only for full Intel PXM backend claims. |
| Intel EPT | OPTIONAL | NOT REQUIRED | SHOULD for Intel PXM backend | MUST for Intel HA PXM backend if Intel platform | Second-stage paging helper. |
| AMD-V / SVM | OPTIONAL | NOT REQUIRED | SHOULD for AMD PXM backend | MUST for AMD HA PXM backend if AMD platform | Required only for full AMD PXM backend claims. |
| AMD NPT | OPTIONAL | NOT REQUIRED | SHOULD for AMD PXM backend | MUST for AMD HA PXM backend if AMD platform | Second-stage paging helper. |
| VMFUNC or similar fast switching | OPTIONAL | OPTIONAL | OPTIONAL | SPEC_GAP | Must not enter success path until specified. |
| Nested virtualization | SPEC_GAP | SPEC_GAP | SPEC_GAP | SPEC_GAP | Not part of current profile. |

### 7.3 DMA, IOMMU, and Interrupts

| Feature | Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance | Notes |
| --- | --- | --- | --- | --- | --- |
| IOMMU present | SHOULD | MUST for platform DMA protection | MUST | MUST | Required for passthrough and side partition device claims. |
| IOMMU enabled by firmware/platform | SHOULD | MUST for platform DMA protection | MUST | MUST | Present but disabled is not sufficient. |
| IOMMU domain isolation | SHOULD | MUST for platform DMA protection | MUST | MUST | Device DMA must be confined. |
| Interrupt remapping | SHOULD | SHOULD unless device assignment is claimed | MUST | MUST | Required with passthrough/assigned devices. |
| Device teardown checklist support | SHOULD | NOT APPLICABLE without device assignment claim | MUST | MUST | Reassignment blocked until teardown complete. |
| DMA remapping fault reporting | SHOULD | SHOULD | MUST | MUST | Faults must be auditable. |
| ATS/PRI/PASID policy | SPEC_GAP | SPEC_GAP | SPEC_GAP | SPEC_GAP | No success path until device-specific policy exists. |
| Shared raw MFOS storage to side partition | MUST NOT | MUST NOT | MUST NOT | MUST NOT | Use audited gateway, not raw sharing. |

### 7.4 Boot, TPM, and Measurement

| Feature | Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance | Notes |
| --- | --- | --- | --- | --- | --- |
| UEFI boot | SHOULD | MUST | MUST | MUST | Legacy boot is development-only if allowed by local build. |
| Secure Boot | SHOULD | MUST | MUST | MUST | Required for production-oriented claims. |
| Measured boot | MAY | MUST | MUST | MUST | Must produce event evidence. |
| TPM 2.0 | MAY | MUST | MUST | MUST | Absence blocks Enterprise-Standalone/Enterprise-PXM/HA measurement claims. |
| TPM event log parsing | MAY | MUST | MUST | MUST | Required evidence artifact. |
| Remote attestation | MAY | SHOULD | SHOULD | MUST | Final protocol remains SPEC_GAP. |
| TPM sealing for selected secrets | MAY | SHOULD | SHOULD | MUST for selected HA roots/secrets | Exact secret policy remains separate. |
| Firmware resiliency evidence | MAY | SHOULD | SHOULD | SHOULD | Recovery assumptions must be explicit. |

### 7.5 Guard and Root Protection

| Feature | Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance | Notes |
| --- | --- | --- | --- | --- | --- |
| PXM Guard | NOT REQUIRED | NOT REQUIRED | OPTIONAL measurement helper | MUST | Guard protects selected roots only. |
| Guard-sealed security root | NOT REQUIRED | NOT REQUIRED | OPTIONAL | MUST | securityd remains PDP. |
| Guard-sealed audit root | NOT REQUIRED | NOT REQUIRED | OPTIONAL | MUST | auditd remains audit schema owner. |
| Guard executable mapping approval | NOT REQUIRED | NOT REQUIRED | OPTIONAL | MUST | Hardware features help enforce, Guard authorizes root policy. |
| Guard AMF registry approval | NOT REQUIRED | NOT REQUIRED | OPTIONAL | MUST | amfd remains manifest/signature checker. |
| Guard attestation | NOT REQUIRED | NOT REQUIRED | OPTIONAL | MUST | Final claim schema is SPEC_GAP. |

## 8. Intel Notes

Intel-specific implementation notes:

- Feature discovery MUST use CPUID leaves and MSR checks defined by the pinned Intel SDM revision for the platform profile.
- Intel VT-x support MUST verify VMX availability, firmware enablement, required VMX controls, and failure modes before claiming PXM backend support.
- Intel EPT support MUST verify EPT availability, EPT memory type support needed by the backend, invalidation behavior, and executable mapping controls before claiming second-stage paging enforcement.
- Intel IOMMU support MUST verify platform DMA remapping availability, enabled state, domain creation, translation invalidation, and fault reporting before device assignment claims.
- Interrupt remapping MUST be detected separately from DMA remapping. DMA remapping alone is insufficient for device assignment claims that require interrupt remapping.
- Intel PKU availability MUST NOT imply instruction-fetch protection, root protection, or storage-key-compatible behavior.
- Intel PKS, if available, is a profile-gated helper only. It MUST NOT replace Guard.
- Intel CET enablement MUST account for CPU support, control registers, OS context switching, executable format/toolchain readiness, and per-component enablement.

Intel-specific SPEC_GAPs:

- Pinned Intel SDM revision for each supported release.
- Required VMX control set for PXM.
- Required EPT control set for Guard/PXM claims.
- Intel IOMMU detection and fault event schema.
- Intel interrupt remapping detection API.
- Intel CET enablement and context-switch ABI.

## 9. AMD Notes

AMD-specific implementation notes:

- Feature discovery MUST use CPUID leaves and MSR checks defined by the pinned AMD APM revision for the platform profile.
- AMD-V/SVM support MUST verify SVM availability, firmware enablement, required intercept/control behavior, and failure modes before claiming PXM backend support.
- AMD NPT support MUST verify nested paging availability, invalidation behavior, and executable mapping controls before claiming second-stage paging enforcement.
- AMD IOMMU support MUST verify DMA remapping availability, enabled state, domain creation, invalidation, and fault reporting before device assignment claims.
- Interrupt remapping MUST be detected separately where platform support exposes it. DMA remapping alone is insufficient for claims that require interrupt remapping.
- AMD platform security features MAY provide additional evidence only after a separate source-matrix entry and profile rule exist.
- CET-like support, if present on a given AMD platform, MUST be detected and enabled by the same MFOS component policy discipline as Intel CET. It is not an authorization mechanism.
- AMD PKU-like or protection-key behavior MUST be treated through the common MFOS PKU/PKS limitation rules when exposed by the platform.

AMD-specific SPEC_GAPs:

- Pinned AMD APM revision for each supported release.
- Required SVM control set for PXM.
- Required NPT control set for Guard/PXM claims.
- AMD IOMMU detection and fault event schema.
- AMD interrupt remapping detection API.
- AMD CET/toolchain enablement matrix where applicable.

## 10. PKU, PKS, and CET Limitations

### 10.1 PKU

PKU MAY be used for:

- User-space compartments.
- Parser sandboxes.
- Service-internal data compartments.
- Optional performance-oriented access gating.

PKU MUST NOT be used for:

- Instruction-fetch protection.
- Security policy root protection.
- Audit root protection.
- AMF registry root protection.
- Guard replacement.
- SVC table integrity.
- Kernel page table root protection.
- Authorization decisions.
- Compatibility claims with external storage-key systems.

Required PKU failure behavior:

- If PKU is absent, MFOS MUST either disable PKU-backed compartments or use a specified non-PKU compartment backend.
- If no fallback backend is specified, the feature MUST return UNSUPPORTED.
- PKU bypass or WRPKRU misuse tests MUST fail architecture review if treated as impossible without evidence.

### 10.2 PKS

PKS MAY be used for:

- Kernel metadata write gating where available.
- Audit append buffer helper protections.
- Catalog metadata cache helper protections.
- SVC table write gating as an implementation helper.

PKS MUST NOT be used for:

- Guard replacement.
- Instruction-fetch protection.
- Primary system-integrity root.
- Authorization decisions.
- Audit evidence generation.
- Mandatory platform requirement across all x64 builds.
- Compatibility claims with external storage-key systems.

Required PKS failure behavior:

- If PKS is absent, Enterprise-Standalone, Enterprise-PXM, and High-Assurance MAY still boot if all profile-required roots are protected by approved non-PKS mechanisms.
- If a component explicitly requires PKS and no fallback is specified, that component MUST return UNSUPPORTED.

### 10.3 CET

CET MAY harden:

- Trusted service control flow.
- securityd, auditd, amfd, uvsd, and selected operator/service processes.
- Nucleus and PXM/Guard paths only after context switching and exception handling are specified.

CET MUST NOT be used for:

- Authorization.
- Audit obligation satisfaction.
- Dataset, catalog, spool, job, AMF, PXM, or Guard policy decisions.
- Data confidentiality.
- DMA isolation.
- Root-object sealing.

Required CET failure behavior:

- If CET is unavailable, MFOS MUST not claim CET-hardened execution.
- If a profile pins CET as required for a component, failure to enable CET for that component MUST fail that component's profile claim.
- CET must not be silently disabled after a component claims CET enablement.

## 11. IOMMU and Interrupt Remapping Requirements

### 11.1 Mandatory Device Assignment Rule

For Enterprise-Standalone, Enterprise-PXM, and High-Assurance device assignment:

```text
DeviceAssignmentAllowed :=
  IOMMU_PRESENT
  and IOMMU_ENABLED
  and IOMMU_DOMAIN_CREATED
  and DEVICE_BOUND_TO_DOMAIN
  and INTERRUPT_REMAP_PRESENT
  and INTERRUPT_REMAP_ENABLED
  and DEVICE_TEARDOWN_POLICY_DEFINED
  and AUDIT_OBLIGATION_AVAILABLE
```

If any term is false, device assignment MUST be denied or return UNSUPPORTED. It MUST NOT return success.

### 11.2 Teardown Rule

Before device reassignment:

```text
TeardownComplete :=
  command_queues_stopped
  and partition_access_quiesced
  and interrupts_masked_or_rerouted
  and dma_stopped
  and iommu_mappings_revoked
  and translation_caches_flushed
  and required_device_reset_completed
  and interrupt_routes_revoked
  and ownership_record_cleared
  and teardown_audit_recorded
```

If `TeardownComplete` is false, reassignment MUST be denied.

### 11.3 Side Partition Rule

Linux/Desktop side partitions MUST NOT receive direct access to MFOS-protected raw storage. Data exchange must use an audited gateway or a separately specified export/import path.

## 12. TPM, Secure Boot, and Measured Boot Requirements

### 12.1 Measurement Targets

Enterprise-Standalone, Enterprise-PXM, and High-Assurance measured boot evidence SHOULD include:

- Firmware and bootloader measurements.
- PXM Core image measurement where PXM is active.
- PXM Guard image measurement where Guard is active.
- MFOS nucleus measurement.
- securityd, auditd, amfd, uvsd measurements where profile-required.
- Activation profile hash.
- Update policy root hash.
- Guard root digests where High-Assurance applies.

The exact component list remains a SPEC_GAP until the boot measurement schema is approved.

### 12.2 Measured Boot Limits

Measured boot proves that measurements were recorded under the assumed boot chain. It does not prove:

- Runtime code remains uncompromised.
- Device DMA is safe.
- securityd authorization is correct.
- auditd records are complete after boot.
- Guard roots are valid unless Guard verified them.

### 12.3 Secure Boot Limits

Secure Boot verifies configured boot artifacts according to platform policy. It does not replace:

- Update verification.
- AMF signature verification.
- securityd authorization.
- auditd evidence.
- Guard root sealing.

### 12.4 TPM Failure Behavior

- Baseline MAY continue without TPM if no TPM-backed claim is made.
- Enterprise MUST suspend measured-boot/attestation claims if TPM or event log evidence is unavailable.
- High-Assurance MUST fail boot, enter recovery, or deny HA claim if required TPM evidence is unavailable.

## 13. Detection APIs To Be Specified

The following APIs are required before production implementation can rely on hardware features. Names are provisional and normative only as detection concepts.

### 13.1 Hardware Profile Discovery

```text
hw_profile_detect() -> HardwareProfileReport
hw_profile_validate(profile_name, report) -> ProfileValidationResult
hw_profile_get_feature(feature_id) -> FeatureStatus
hw_profile_get_vendor() -> CPU_VENDOR_INTEL | CPU_VENDOR_AMD | CPU_VENDOR_OTHER
hw_profile_get_evidence() -> HardwareEvidenceBundle
```

### 13.2 CPU Feature Detection

```text
cpu_detect_long_mode()
cpu_detect_nx()
cpu_detect_smep()
cpu_detect_smap()
cpu_detect_cet_shadow_stack()
cpu_detect_cet_ibt()
cpu_detect_pku()
cpu_detect_pks()
cpu_detect_vmx()
cpu_detect_svm()
cpu_detect_ept()
cpu_detect_npt()
```

### 13.3 Platform and Device Isolation Detection

```text
platform_detect_iommu_present()
platform_detect_iommu_enabled()
platform_detect_iommu_fault_reporting()
platform_detect_interrupt_remapping_present()
platform_detect_interrupt_remapping_enabled()
platform_validate_device_assignment(device_id)
platform_validate_device_teardown(device_id)
```

### 13.4 Boot and TPM Detection

```text
boot_detect_uefi()
boot_detect_secure_boot_state()
boot_detect_measured_boot_state()
tpm_detect_present()
tpm_read_event_log()
tpm_validate_event_log(schema_version)
tpm_quote(nonce, requested_claims)
```

### 13.5 Detection API Rules

- Detection APIs MUST report `PRESENT`, `ENABLED`, `DISABLED`, `UNSUPPORTED`, `UNKNOWN`, or `SPEC_GAP`.
- `UNKNOWN` MUST NOT satisfy a profile requirement.
- `SPEC_GAP` MUST NOT satisfy a profile requirement.
- Feature detection MUST be audited when it affects a profile claim.
- Detection reports MUST include source, timestamp, CPU vendor, CPU family/model/stepping where available, firmware state where available, and error codes.

Final ABI, data schema, and error codes remain SPEC_GAPs.

## 14. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-HW-0001 | Hardware features MUST be treated as mechanisms, not authorization semantics. | architecture review |
| MFOS-REQ-HW-0002 | x64 protection features MUST NOT be described as external storage-key compatibility. | claim review |
| MFOS-REQ-HW-0003 | NX and W^X MUST be required for all profiles. | boot/config test |
| MFOS-REQ-HW-0004 | SMEP and SMAP MUST be enabled in Enterprise-Standalone, Enterprise-PXM, and High-Assurance when supported. | platform test |
| MFOS-REQ-HW-0005 | PKU MUST NOT be used as instruction-fetch protection or system-integrity root. | negative test |
| MFOS-REQ-HW-0006 | PKS MUST NOT replace Guard. | architecture review |
| MFOS-REQ-HW-0007 | CET MUST be treated as control-flow hardening only. | claim review |
| MFOS-REQ-HW-0008 | Device assignment in Enterprise-Standalone, Enterprise-PXM, and High-Assurance MUST require IOMMU domain setup and interrupt remapping. | device test |
| MFOS-REQ-HW-0009 | Device reassignment MUST be denied until teardown checklist completion. | negative test |
| MFOS-REQ-HW-0010 | Enterprise-Standalone, Enterprise-PXM, and High-Assurance measured boot claims MUST require TPM/event-log evidence. | attestation test |
| MFOS-REQ-HW-0011 | High-Assurance MUST require PXM and Guard for HA root-object claims. | profile review |
| MFOS-REQ-HW-0012 | Intel and AMD backend feature sets MUST be detected separately. | detection test |
| MFOS-REQ-HW-0013 | Detection API result UNKNOWN MUST NOT satisfy a profile requirement. | negative test |
| MFOS-REQ-HW-0014 | SPEC_GAP detection results MUST NOT satisfy profile requirements. | negative test |
| MFOS-REQ-HW-0015 | Hardware profile validation MUST produce evidence artifacts for release claims. | evidence review |
| MFOS-REQ-HW-0016 | Secure Boot MUST NOT replace update verification or AMF verification. | architecture review |
| MFOS-REQ-HW-0017 | Measured boot MUST NOT be claimed as runtime integrity proof. | claim review |
| MFOS-REQ-HW-0018 | Side partition device and storage access MUST respect IOMMU and gateway rules. | integration test |
| MFOS-REQ-HW-0019 | Profile claims MUST fail closed when required hardware evidence is missing. | negative test |
| MFOS-REQ-HW-0020 | Unsupported hardware-dependent features MUST return UNSUPPORTED, not success. | no-fake-success test |

## 15. Failure Modes

| Failure | Required behavior |
| --- | --- |
| NX unavailable | Deny all profile claims; boot only in explicit non-production diagnostic mode if specified. |
| W^X cannot be enforced | Deny normal boot or enter recovery; no production claim. |
| SMEP unsupported | Baseline may continue without SMEP claim; Enterprise-Standalone/Enterprise-PXM/HA may continue only if requirement says "when supported" and absence is recorded. |
| SMEP supported but enable fails | Enterprise-Standalone/Enterprise-PXM/HA profile claim fails unless an approved profile exception exists. |
| SMAP supported but enable fails | Enterprise-Standalone/Enterprise-PXM/HA profile claim fails unless an approved profile exception exists. |
| PKU absent | Disable PKU compartments or return UNSUPPORTED for PKU-backed compartment features. |
| PKU used as instruction-fetch protection | Architecture review failure; implementation must be rejected. |
| PKS absent | Use approved non-PKS mechanism or return UNSUPPORTED for PKS-specific helper. |
| PKS used as Guard replacement | Architecture review failure; HA claim denied. |
| CET absent | Do not claim CET hardening; continue only if profile does not require it. |
| CET enablement fails for required component | Component profile claim fails. |
| VT-x/EPT absent on Intel full-PXM claim | Full Intel PXM backend claim denied or UNSUPPORTED. |
| SVM/NPT absent on AMD full-PXM claim | Full AMD PXM backend claim denied or UNSUPPORTED. |
| IOMMU absent or disabled | Enterprise-Standalone/Enterprise-PXM/HA device assignment denied. |
| Interrupt remapping absent or disabled | Enterprise-Standalone/Enterprise-PXM/HA device assignment denied. |
| IOMMU fault reporting unavailable | Device assignment claim denied unless profile explicitly permits with evidence. |
| TPM absent in Enterprise-Standalone/Enterprise-PXM/HA measured-boot claim | Measured-boot/attestation claim denied; HA boot policy applies. |
| TPM event log malformed | Evidence rejected; profile claim denied or recovery mode. |
| Secure Boot disabled in Enterprise-Standalone/Enterprise-PXM/HA | Production profile claim denied unless explicit recovery profile applies. |
| Detection API returns UNKNOWN | Requirement not satisfied. |
| Detection API returns SPEC_GAP | Requirement not satisfied; no success path. |
| Hardware evidence missing at release | Release claim blocked for affected profile. |

## 16. Negative Tests

```text
HW-NEG-0001  PKU claimed as instruction-fetch protection is rejected.
HW-NEG-0002  PKU or PKS claimed as external storage-key compatibility is rejected.
HW-NEG-0003  PKS claimed as Guard replacement is rejected.
HW-NEG-0004  CET claimed as authorization enforcement is rejected.
HW-NEG-0005  IOMMU absent but device assignment succeeds; test must fail.
HW-NEG-0006  Interrupt remapping absent but device assignment succeeds; test must fail.
HW-NEG-0007  Device reassigned before teardown completion; test must fail.
HW-NEG-0008  TPM event log unavailable but Enterprise measured-boot claim succeeds; test must fail.
HW-NEG-0009  Secure Boot disabled but Enterprise production claim succeeds; test must fail.
HW-NEG-0010  Detection API UNKNOWN satisfies requirement; test must fail.
HW-NEG-0011  Detection API SPEC_GAP satisfies requirement; test must fail.
HW-NEG-0012  Intel VMX absent but Intel full-PXM backend claim succeeds; test must fail.
HW-NEG-0013  AMD SVM absent but AMD full-PXM backend claim succeeds; test must fail.
HW-NEG-0014  CET required component silently runs without CET; test must fail.
HW-NEG-0015  Measured boot treated as runtime Guard proof; claim review must fail.
HW-NEG-0016  Side partition receives raw MFOS protected storage; test must fail.
HW-NEG-0017  Unsupported hardware-dependent feature returns success; test must fail.
HW-NEG-0018  W^X violation accepted for executable mapping; test must fail.
HW-NEG-0019  IOMMU fault is not audited; test must fail for Enterprise-Standalone/Enterprise-PXM/HA.
HW-NEG-0020  Hardware profile report omits CPU vendor and still validates; test must fail.
```

## 17. Positive Tests

```text
HW-POS-0001  Baseline validates on x86_64 with NX, W^X, page-table separation, and no HA claim.
HW-POS-0002  Enterprise validates with Secure Boot, measured boot, TPM event log, IOMMU, and interrupt remapping evidence.
HW-POS-0003  High-Assurance validates only when PXM and Guard requirements are satisfied.
HW-POS-0004  Intel profile detects VMX/EPT and records Intel evidence.
HW-POS-0005  AMD profile detects SVM/NPT and records AMD evidence.
HW-POS-0006  PKU absent results in PKU compartment UNSUPPORTED without failing unrelated profile claims.
HW-POS-0007  CET supported and enabled for a trusted service records CET evidence.
HW-POS-0008  Device assignment succeeds only after IOMMU domain and interrupt remapping evidence are present.
HW-POS-0009  TPM event log validates against the approved measured boot schema.
HW-POS-0010  Hardware profile validation emits release evidence bundle.
```

## 18. Evidence Artifacts

Hardware profile validation MUST produce or link:

```text
EVID-HW-PROFILE-REPORT
EVID-HW-CPU-VENDOR
EVID-HW-CPUID
EVID-HW-MSR
EVID-HW-NX-WX
EVID-HW-SMEP-SMAP
EVID-HW-CET
EVID-HW-PKU
EVID-HW-PKS
EVID-HW-VMX-EPT
EVID-HW-SVM-NPT
EVID-HW-IOMMU
EVID-HW-INTERRUPT-REMAP
EVID-HW-DEVICE-TEARDOWN
EVID-HW-IOMMU-FAULT
EVID-BOOT-SECUREBOOT
EVID-BOOT-MEASURED
EVID-BOOT-TPM-EVENTLOG
EVID-ATTEST-QUOTE
EVID-HW-NEGATIVE-TESTS
EVID-HW-SPEC-GAPS
```

Each evidence artifact SHOULD include:

- profile name
- platform vendor
- CPU vendor
- CPU family/model/stepping where available
- firmware version where available
- detection tool version
- timestamp
- feature status
- raw detection data reference
- normalized validation result
- linked requirement IDs
- linked Source Matrix IDs
- negative tests run
- SPEC_GAPs

## 19. Hardware Profile Report Schema Draft

This schema is provisional. Final serialization is a SPEC_GAP.

```yaml
HardwareProfileReport:
  schema_version: 1
  report_id: uuid
  generated_at: timestamp
  requested_profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  validation_result: PASS | FAIL | DEGRADED | SPEC_GAP
  cpu:
    vendor: INTEL | AMD | OTHER | UNKNOWN
    family: string?
    model: string?
    stepping: string?
    features:
      long_mode: FeatureStatus
      nx: FeatureStatus
      smep: FeatureStatus
      smap: FeatureStatus
      cet_shadow_stack: FeatureStatus
      cet_ibt: FeatureStatus
      pku: FeatureStatus
      pks: FeatureStatus
      vmx: FeatureStatus
      svm: FeatureStatus
      ept: FeatureStatus
      npt: FeatureStatus
  platform:
    uefi: FeatureStatus
    secure_boot: FeatureStatus
    measured_boot: FeatureStatus
    tpm2: FeatureStatus
    iommu_present: FeatureStatus
    iommu_enabled: FeatureStatus
    interrupt_remapping_present: FeatureStatus
    interrupt_remapping_enabled: FeatureStatus
  evidence:
    cpuid_report_ref: string?
    msr_report_ref: string?
    tpm_event_log_ref: string?
    iommu_report_ref: string?
    interrupt_remap_report_ref: string?
    negative_test_report_ref: string?
  unsatisfied_requirements:
    - requirement_id: string
      reason_code: string
  spec_gaps:
    - string
```

```text
FeatureStatus:
  PRESENT
  ENABLED
  DISABLED
  UNSUPPORTED
  UNKNOWN
  SPEC_GAP
```

## 20. Inactive Future Implementation Prompt Template

Phase status: inactive future template. This section does not authorize production implementation, hosted daemon implementation, or portable semantic-core implementation.

```text
You are an MFOS x64 hardware profile implementation agent.

Use docs/design/specs/26-hardware-profile.md and linked source matrix entries.

Hard constraints:
- Do not claim z/OS compatibility.
- Do not claim storage-key compatibility.
- Do not treat PKU, PKS, CET, IOMMU, TPM, Secure Boot, measured boot, VMX,
  SVM, EPT, or NPT as MFOS authorization semantics.
- Do not use PKU as instruction-fetch protection.
- Do not use PKS as Guard replacement.
- Do not use CET as authorization or audit enforcement.
- Return UNSUPPORTED for specified but unavailable hardware features.
- Return SPEC_GAP for unspecified detection or enforcement behavior.
- UNKNOWN and SPEC_GAP detection results must not satisfy profile requirements.
- Device assignment must fail closed without required IOMMU and interrupt
  remapping evidence.
- Enterprise-Standalone, Enterprise-PXM, and High-Assurance measured-boot claims must fail without required
  TPM/event-log evidence.

Required output:
1. Implemented Requirement IDs
2. Source Matrix IDs
3. CPU Vendor and Platform Assumptions
4. Detection APIs Implemented
5. Unsupported Features
6. SPEC_GAPs
7. Profile Validation Matrix
8. Failure Modes
9. Negative Tests Added
10. Evidence Artifacts
11. Claim Review Notes
```

## 21. SPEC_GAPs

Global hardware/profile gaps:

- Pinned Intel SDM revision per MFOS release.
- Pinned AMD APM revision per MFOS release.
- Final CPUID/MSR detection tables.
- Final hardware detection ABI.
- Final hardware profile report serialization.
- Final measured boot component list.
- Final TPM event log schema and parser.
- Final attestation quote protocol and claim schema.
- Final Secure Boot policy integration.
- Final VMX/EPT PXM backend requirements.
- Final SVM/NPT PXM backend requirements.
- Final IOMMU programming and validation model.
- Final interrupt remapping programming and validation model.
- Final DMA fault audit schema.
- Final device-specific teardown and reset profiles.
- Final CET context-switch and executable format policy.
- Final PKS support policy by CPU/platform generation.
- Final fallback backend for PKU-backed compartments.
- Final handling of ATS, PRI, PASID, SR-IOV, and peer-to-peer DMA.
- Final side-partition device allowlist.
- Final hardware evidence signing or immutability mechanism.

Agents MUST NOT fill these gaps with success-path behavior. They must return SPEC_GAP or UNSUPPORTED as appropriate.
