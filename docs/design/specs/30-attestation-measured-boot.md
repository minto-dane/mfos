---
spec_id: "MFOS-SPEC-30-ATTESTATION-MEASURED-BOOT"
title: "MFOS Measured Boot and Attestation Specification v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "MS-VBS-001", "MS-VSM-001", "NIST-160-001", "NIST-193-001", "SLSA-001", "TCG-001", "TUF-001", "X64-AMD-001", "X64-INTEL-001"]
requirement_refs: ["MFOS-REQ-ATTEST-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Measured Boot and Attestation Specification v0.1

Status: Draft design split

Owner area: `docs/design/specs/30-attestation-measured-boot.md`

This document defines MFOS measured boot and attestation design.

MFOS is z/OS-inspired and source-grounded. It does not claim compatibility with IBM products, z/Architecture, z/OS APIs, RACF, JES, DFSMS, SMF, JCL, or any external attestation ecosystem. TPM, Secure Boot, measured boot, and remote attestation are evidence mechanisms. They do not replace MFOS authorization, audit, update verification, PXM isolation, or PXM Guard root protection.

## 1. Purpose

Measured boot and attestation provide evidence about what was loaded, measured, activated, and sealed during the MFOS boot and High-Assurance root setup process.

This specification exists to:

- Define TPM event log expectations for MFOS.
- Define the component measurement list.
- Bind activation profile hashes into boot and partition evidence.
- Bind Guard root claims into High-Assurance evidence.
- Correlate boot, PXM, Guard, update, and audit evidence.
- Define remote attestation claim sets.
- Require freshness through nonces and time/epoch constraints.
- Define failure modes and negative tests.
- Keep measurement claims scoped and prevent overclaiming measured boot as runtime integrity proof.

## 2. Scope

This specification covers:

- Boot measurement roles and trust boundaries.
- TPM event log expectations.
- Component measurements.
- Activation profile hash requirements.
- PXM and Guard measurement claims.
- Audit correlation for boot and attestation evidence.
- Remote attestation request and response model.
- Nonce and freshness rules.
- Profile-specific requirements for Baseline, Enterprise-Standalone, Enterprise-PXM, and High-Assurance.
- Failure modes, tests, evidence artifacts, and SPEC_GAPs.

This specification does not define:

- Final TPM quote binary protocol.
- Final cryptographic algorithms.
- Final certificate authority or verifier trust store.
- Full firmware vendor verification.
- Remote verifier service implementation.
- Recovery policy internals.
- Runtime memory integrity proof.
- Device-specific DMA correctness.
- PXM Guard isolation internals.
- External platform compatibility.

## 3. Source Matrix References

| Source ID | Use |
| --- | --- |
| TCG-001 | TPM, measured boot, PCR/event-log concepts, and quote-style attestation reference. |
| NIST-160-001 | Secure system engineering and assurance lifecycle framing. |
| NIST-193-001 | Firmware resiliency, detection, and recovery framing. |
| X64-INTEL-001 | Intel x64 boot/platform feature reality where platform detection interacts with evidence. |
| X64-AMD-001 | AMD64 boot/platform feature reality where platform detection interacts with evidence. |
| TUF-001 | Update metadata freshness, rollback, and mix-and-match reference for update-related measurements. |
| SLSA-001 | Provenance evidence reference for measured release artifacts. |
| MS-VBS-001 | Informative executable mapping/code-integrity root reference for High-Assurance Guard claims only. |
| MS-VSM-001 | Informative root-isolation reference for Guard attestation claims only. |
| FBVBS-001 | Internal transfer source for evidence discipline, freshness, attestation, command-page, and no-fake-success rules. |

## 4. Normative Language

- `MUST`: required for the applicable profile.
- `SHOULD`: strongly recommended; deviation requires an ADR and evidence.
- `MAY`: optional.
- `MUST NOT`: prohibited.
- `UNSUPPORTED`: specified behavior not implemented or not available.
- `SPEC_GAP`: behavior undefined by specification; implementation must not invent success.

## 5. Core Principles

```text
ATTEST-PRIN-001:
  Measured boot records what was measured under the assumed boot chain. It does
  not prove that runtime state remains uncompromised.

ATTEST-PRIN-002:
  Secure Boot, TPM, event logs, PCRs, and quotes do not replace securityd,
  auditd, uvsd, PXM, or Guard.

ATTEST-PRIN-003:
  Attestation evidence must be nonce-bound, profile-scoped, policy-version
  bound, and auditable.

ATTEST-PRIN-004:
  High-Assurance root claims must bind to Guard root state and Guard evidence.

ATTEST-PRIN-005:
  Unknown, missing, malformed, stale, replayed, or SPEC_GAP evidence cannot
  satisfy Enterprise-Standalone, Enterprise-PXM, or High-Assurance claims.
```

## 6. Profile Applicability

| Capability | Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance |
| --- | --- | --- | --- | --- |
| Secure Boot evidence | SHOULD | MUST | MUST | MUST |
| Measured boot evidence | MAY | MUST | MUST | MUST |
| TPM 2.0 | MAY | MUST for measured boot or attestation claim | MUST | MUST |
| TPM event log parsing | MAY | MUST | MUST | MUST |
| Activation profile hash in evidence | SHOULD | MUST | MUST | MUST |
| PXM measurement | OPTIONAL | OPTIONAL unless PXM is enabled | SHOULD when PXM enabled | MUST |
| Guard measurement | NOT REQUIRED | NOT REQUIRED | OPTIONAL when Guard helper enabled | MUST |
| Guard root claims | NOT REQUIRED | NOT REQUIRED | OPTIONAL helper claim only | MUST for HA root claims |
| Remote attestation | MAY | SHOULD | SHOULD | MUST |
| Nonce-bound attestation | MUST if attestation enabled | MUST | MUST | MUST |
| Audit correlation | MUST if evidence is generated | MUST | MUST | MUST |
| Fail closed on missing required evidence | SHOULD | MUST | MUST | MUST |

Baseline may boot without TPM-backed measured boot if it makes no measured-boot or attestation claim. Enterprise-Standalone, Enterprise-PXM, and High-Assurance must not silently downgrade required measurement evidence.

## 7. Trust Boundaries

```text
Firmware/UEFI -> bootloader measurement
Bootloader -> PXM Core measurement
PXM Core -> PXM Guard measurement [HA]
PXM Core -> MFOS nucleus measurement
PXM Core -> activation profile hash
MFOS nucleus -> service image measurements
uvsd -> update metadata and artifact measurement verification
Guard -> Guard root seal/verify claims [HA]
auditd -> boot and attestation evidence records
remote verifier -> nonce-bound attestation request/response
```

All inputs from firmware, event logs, boot parameters, remote verifiers, side partitions, and recovery tools are untrusted until parsed, validated, and bound into MFOS evidence through approved interfaces.

## 8. TPM Event Log Expectations

### 8.1 Event Log Requirements

MFOS event log processing MUST support these abstract expectations:

- Event log records are ordered.
- Event log records identify measured component or event type.
- Each measured component has an algorithm identifier and digest.
- Event log replay must be able to reconstruct expected PCR-like aggregate values for supported banks.
- Event log parsing must distinguish malformed records from unsupported records.
- Event log evidence must bind to boot session identity or boot nonce where available.
- Event log evidence must be correlated with MFOS audit records once auditd is available.

### 8.2 Event Classes

```text
BOOT_FIRMWARE_EVENT
BOOT_BOOTLOADER_EVENT
BOOT_PXM_CORE_EVENT
BOOT_PXM_GUARD_EVENT
BOOT_MFOS_NUCLEUS_EVENT
BOOT_SERVICE_IMAGE_EVENT
BOOT_ACTIVATION_PROFILE_EVENT
BOOT_UPDATE_POLICY_EVENT
BOOT_SECURITY_POLICY_EVENT
BOOT_AUDIT_POLICY_EVENT
BOOT_AMF_REGISTRY_EVENT
BOOT_GUARD_ROOT_EVENT
BOOT_RECOVERY_POLICY_EVENT
BOOT_PLATFORM_FEATURE_EVENT
BOOT_EVENTLOG_REPLAY_RESULT
```

### 8.3 Required Event Fields

```yaml
MeasuredBootEvent:
  schema_version: uint16
  event_seq: uint64
  event_type: string
  component_id: string
  component_kind: firmware | bootloader | pxm_core | pxm_guard | nucleus | service | policy | activation_profile | guard_root | platform
  digest_algorithm: sha256 | sha384 | sha512 | vendor_specific
  digest: hex
  measurement_context: sha384?
  pcr_index: uint32?
  pcr_bank: string?
  source: firmware | bootloader | pxm | guard | mfos | recovery
  timestamp_utc: timestamp?
  boot_session_id: uuid?
  correlation_id: uuid?
```

Final binary event log format and canonical parser behavior remain SPEC_GAPs.

### 8.4 Event Log Limits

TPM event log evidence does not by itself prove:

- The component is policy-approved.
- The component remains unchanged at runtime.
- The measured code is vulnerability-free.
- Device DMA is contained.
- Audit records are complete.
- Guard roots are valid.

Policy approval comes from uvsd, securityd, amfd, PXM, and Guard according to their specifications.

## 9. Component Measurement List

### 9.1 Required Measurement Categories

Enterprise-Standalone, Enterprise-PXM, and High-Assurance SHOULD measure these components where present. High-Assurance MUST measure the required HA subset.

| Component | Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance | Notes |
| --- | --- | --- | --- | --- | --- |
| Firmware measurement summary | MAY | MUST | MUST | MUST | Exact firmware event mapping is platform-specific. |
| Bootloader | SHOULD | MUST | MUST | MUST | Required for boot-chain evidence. |
| PXM Core | MAY | OPTIONAL unless PXM is enabled | SHOULD when PXM enabled | MUST | Required for HA partition claim. |
| PXM Guard | NOT REQUIRED | NOT REQUIRED | OPTIONAL when Guard helper enabled | MUST | Required for HA root claim. |
| MFOS nucleus | SHOULD | MUST | MUST | MUST | Required for MFOS boot evidence. |
| securityd | SHOULD | MUST | MUST | MUST | Required for authorization evidence. |
| auditd | SHOULD | MUST | MUST | MUST | Required for audit evidence. |
| catalogd | MAY | SHOULD | SHOULD | SHOULD | Required for dataset/catalog production claim. |
| datasetd | MAY | SHOULD | SHOULD | SHOULD | Required for dataset production claim. |
| jobd | MAY | SHOULD | SHOULD | SHOULD | Required for job production claim. |
| spoold | MAY | SHOULD | SHOULD | SHOULD | Required for spool production claim. |
| operatord | MAY | SHOULD | SHOULD | SHOULD | Required for operator console production claim. |
| workpolicyd | MAY | SHOULD | SHOULD | SHOULD | Required for workload policy claim. |
| amfd | SHOULD | MUST if AMF enabled | MUST if AMF enabled | MUST if AMF enabled | Required for AMF claim. |
| uvsd | SHOULD | MUST | MUST | MUST | Required for update claim. |
| AMF registry | MAY | MUST if AMF enabled | MUST if AMF enabled | MUST | HA requires Guard-linked root claim. |
| Update root metadata | SHOULD | MUST | MUST | MUST | Must bind security_epoch. |
| Security policy root | SHOULD | MUST | MUST | MUST | HA requires Guard root claim. |
| Audit policy/root | SHOULD | MUST | MUST | MUST | HA requires Guard audit root claim. |
| Activation profile | SHOULD | MUST | MUST | MUST | Hash binds PXM activation context. |
| Recovery image/profile | MAY | SHOULD | SHOULD | MUST when recovery claim exists | Required for recovery readiness. |
| Linux/Desktop gateway config | MAY | SHOULD if enabled | SHOULD if enabled | SHOULD if enabled | Must not imply Linux/Desktop trust. |

### 9.2 Measurement Identifiers

Each measured component SHOULD have:

```yaml
MeasuredComponent:
  component_id: string
  component_kind: string
  component_version: string?
  source_artifact_id: string?
  expected_digest: hex?
  observed_digest: hex
  digest_algorithm: string
  signer_id: string?
  security_epoch: uint64?
  policy_version: uint64?
  source_matrix_refs:
    - TCG-001
```

Expected digests come from approved update metadata, activation profiles, AMF manifests, or Guard root policy. An observed digest without an approved expected digest may be diagnostic evidence, but it MUST NOT satisfy an Enterprise-Standalone, Enterprise-PXM, or High-Assurance approval claim.

## 10. Activation Profile Hash

### 10.1 Activation Profile Binding

The activation profile hash binds:

- Partition kind.
- Image references and expected image hashes.
- CPU and memory assignment constraints.
- Device assignment constraints.
- IOMMU and interrupt remapping requirements.
- Secure Boot and measured boot requirements.
- TPM requirements.
- Guard requirements for High-Assurance.
- Recovery profile references.
- Policy epoch.
- Source Matrix references.

### 10.2 Activation Profile Event

```yaml
ActivationProfileMeasurement:
  profile_id: string
  profile_version: uint64
  partition_id: uint64
  partition_kind: MFOS | LINUX_DESKTOP | SERVICE | RECOVERY | TEST
  activation_profile_hash: sha384
  policy_epoch: uint64
  required_profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  measured_at_stage: DEFINE | MEASURE | LOAD | ACTIVATE
  pcr_ref: string?
  boot_session_id: uuid
  audit_correlation_id: uuid
```

### 10.3 Activation Profile Rules

- Enterprise-Standalone, Enterprise-PXM, and High-Assurance MUST record activation profile hash before activation.
- High-Assurance MUST bind activation profile hash to Guard activation-profile root where Guard policy requires it.
- A partition activation using an unmeasured or mismatched activation profile MUST be denied for Enterprise-Standalone, Enterprise-PXM, and High-Assurance claims.
- Activation profile hash mismatch MUST be audited.

## 11. Guard Root Claims

Guard root claims apply only to High-Assurance, or to Enterprise builds explicitly using Guard as an optional measurement helper. Guard claims must remain scoped to selected root objects.

### 11.1 Claimable Guard Roots

```text
GUARD_ROOT_SECURITY_POLICY
GUARD_ROOT_AUDIT_CHAIN
GUARD_ROOT_AMF_REGISTRY
GUARD_ROOT_SVC_TABLE
GUARD_ROOT_NUCLEUS_TEXT
GUARD_ROOT_EXECUTABLE_MAPPING_POLICY
GUARD_ROOT_PAGE_TABLE_POLICY
GUARD_ROOT_ACTIVATION_PROFILE
GUARD_ROOT_EMERGENCY_STATE
GUARD_ROOT_UPDATE_POLICY
```

### 11.2 Guard Root Claim Schema

```yaml
GuardRootClaim:
  root_type: string
  root_id: string
  root_version: uint64
  security_epoch: uint64
  policy_version: uint64
  root_digest: sha384
  guard_lifecycle_state: UNINITIALIZED | MEASURED | INITIALIZED | ROOTS_SEALED | READY | LOCKDOWN | RECOVERY | SHUTDOWN
  root_state: UNSEALED | SEALED | VERIFIED | TRANSITION_PENDING | REVOKED | FAULTED
  measurement_context: sha384
  transition_id: uuid?
  audit_event_id: uuid?
```

### 11.3 Guard Claim Rules

- Guard root claims MUST be produced by Guard or by an approved Guard evidence path.
- MFOS services MUST NOT self-assert Guard root claims.
- A Guard root claim in `FAULTED`, `REVOKED`, `TRANSITION_PENDING`, `LOCKDOWN`, or `RECOVERY` MUST NOT satisfy a normal High-Assurance ready claim unless the verifier explicitly requested recovery-state evidence.
- Guard root claims MUST include measurement context and audit correlation.
- Guard root mismatch MUST produce a failure claim and audit event.

## 12. Audit Correlation

Measured boot and attestation evidence MUST correlate with audit records once auditd is available.

### 12.1 Correlation IDs

```text
boot_session_id:
  UUID generated for one boot session.

measurement_context:
  Digest over boot session, component measurements, activation profile hash,
  policy epoch, and profile name.

attestation_id:
  UUID for one attestation response.

audit_correlation_id:
  UUID linking boot measurements, PXM events, Guard events, and attestation
  records.
```

### 12.2 Audit Events

MFOS MUST audit:

- Boot measurement collection started.
- Boot measurement collection completed.
- TPM event log parsed.
- TPM event log parse failed.
- Activation profile measured.
- Activation profile mismatch.
- Component expected/observed digest match.
- Component digest mismatch.
- PXM measurement accepted or denied.
- Guard measurement accepted or denied.
- Guard root claim emitted.
- Remote attestation requested.
- Remote attestation produced.
- Remote attestation denied.
- Nonce replay detected.
- Stale attestation request rejected.
- Required evidence missing.
- Attestation evidence exported.

### 12.3 Audit Timing

- A denial based on missing, malformed, stale, replayed, or mismatched evidence SHOULD be audited before the caller receives the final denial when audit path is available.
- Before auditd starts, boot evidence MUST be written to an approved boot audit sink if the profile requires evidence.
- Boot audit sink reconciliation with auditd is REQUIRED before Enterprise-Standalone, Enterprise-PXM, or High-Assurance ready state is claimed.

## 13. Remote Attestation Model

### 13.1 Attestation Request

```yaml
AttestationRequest:
  request_id: uuid
  verifier_id: string
  requested_profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  nonce: bytes
  nonce_created_at: timestamp?
  requested_claims:
    - BOOT_CHAIN
    - TPM_EVENT_LOG
    - ACTIVATION_PROFILE
    - PXM_STATE
    - GUARD_ROOTS
    - UPDATE_EPOCH
    - SERVICE_MEASUREMENTS
    - AUDIT_HEAD
    - HARDWARE_PROFILE
    - RECOVERY_STATE
  max_age_seconds: uint64
  policy_version: uint64?
  verifier_context: bytes?
```

### 13.2 Attestation Response

```yaml
AttestationResponse:
  schema_version: uint16
  attestation_id: uuid
  request_id: uuid
  verifier_id: string
  subject_system_id: string
  boot_session_id: uuid
  requested_profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  actual_profile_state: NOT_CLAIMED | BASELINE_READY | ENTERPRISE_READY | HIGH_ASSURANCE_READY | RECOVERY | DEGRADED | FAILED
  nonce: bytes
  produced_at: timestamp
  freshness:
    nonce_status: MATCHED | MISSING | REPLAYED | STALE | SPEC_GAP
    max_age_seconds: uint64
    evidence_age_seconds: uint64?
  measurements:
    measurement_context: sha384
    activation_profile_hash: sha384?
    component_measurement_set_hash: sha384
    tpm_event_log_hash: sha384?
  pcr_claims:
    - bank: string
      index: uint32
      value: hex
  guard_root_claims:
    - GuardRootClaim
  update_claims:
    security_epoch: uint64?
    update_root_digest: sha384?
    rollback_state: NOT_CHECKED | PASSED | FAILED | RECOVERY_ALLOWED
    freshness_state: NOT_CHECKED | PASSED | FAILED
  audit_claims:
    audit_head_sequence: uint64?
    audit_head_hash: sha384?
    audit_event_ids:
      - uuid
    audit_correlation_id: uuid
  hardware_claims:
    hardware_profile_report_hash: sha384?
    secure_boot_state: ENABLED | DISABLED | UNKNOWN | SPEC_GAP
    measured_boot_state: ENABLED | DISABLED | UNKNOWN | SPEC_GAP
    tpm_state: PRESENT | ENABLED | DISABLED | UNSUPPORTED | UNKNOWN | SPEC_GAP
  result: PASS | FAIL | DEGRADED | RECOVERY | UNSUPPORTED | SPEC_GAP
  reason_code: string
  signature: bytes?
  quote: bytes?
```

Final quote format, signature format, verifier trust anchors, and certificate chain handling remain SPEC_GAPs.

### 13.3 Required Claims by Profile

| Claim | Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance |
| --- | --- | --- | --- | --- |
| Nonce echo | MUST if attestation enabled | MUST | MUST | MUST |
| Boot session ID | MUST if attestation enabled | MUST | MUST | MUST |
| Activation profile hash | SHOULD | MUST | MUST | MUST |
| TPM event log hash | MAY | MUST | MUST | MUST |
| PCR claims | MAY | MUST | MUST | MUST |
| Component measurement set hash | SHOULD | MUST | MUST | MUST |
| Update security epoch | SHOULD | MUST | MUST | MUST |
| Audit correlation ID | MUST if attestation enabled | MUST | MUST | MUST |
| Audit head claim | MAY | SHOULD | SHOULD | MUST |
| Guard root claims | NOT REQUIRED | NOT REQUIRED | OPTIONAL | MUST |
| Hardware profile report hash | MAY | SHOULD | SHOULD | MUST |
| Recovery state | SHOULD if recovery active | MUST if recovery active | MUST if recovery active | MUST if recovery active |

## 14. Freshness and Nonces

### 14.1 Nonce Rules

- Remote attestation MUST include a verifier-provided nonce.
- The response MUST echo the exact nonce.
- Nonces MUST be single-use within the verifier freshness window.
- Replayed nonces MUST be rejected or produce a failed attestation response.
- Missing nonce MUST fail Enterprise-Standalone, Enterprise-PXM, and High-Assurance remote attestation.
- Nonce validation state MUST be auditable.

### 14.2 Freshness Inputs

Freshness may use:

- Verifier nonce.
- Attestation response production time.
- TPM quote freshness where available.
- Timestamp metadata freshness from update verification.
- Security epoch.
- Policy version.
- Audit head sequence.
- Guard root version.

Freshness MUST NOT rely on wall-clock time alone unless the verifier policy explicitly permits it.

### 14.3 Staleness Rules

Evidence is stale when:

- It is older than request `max_age_seconds`.
- It uses a replayed nonce.
- Its policy version is older than verifier policy requires.
- Its security epoch is older than verifier policy requires.
- Its Guard root version is older than verifier policy requires.
- Its audit head sequence is older than verifier policy requires.

Stale evidence MUST NOT satisfy Enterprise-Standalone, Enterprise-PXM, or High-Assurance attestation.

## 15. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-ATTEST-0001 | MFOS MUST NOT claim external platform compatibility through measured boot or attestation. | claim review |
| MFOS-REQ-ATTEST-0002 | Measured boot MUST be described as boot evidence, not runtime integrity proof. | architecture review |
| MFOS-REQ-ATTEST-0003 | Enterprise-Standalone, Enterprise-PXM, and High-Assurance measured boot claims MUST require TPM event log evidence or an explicitly approved equivalent evidence path. | attestation test |
| MFOS-REQ-ATTEST-0004 | TPM event log parsing MUST distinguish malformed, unsupported, missing, and SPEC_GAP records. | parser test |
| MFOS-REQ-ATTEST-0005 | Activation profile hash MUST be included in Enterprise-Standalone, Enterprise-PXM, and High-Assurance boot evidence. | measurement test |
| MFOS-REQ-ATTEST-0006 | High-Assurance attestation MUST include Guard root claims for every claimed Guard-protected root. | Guard attestation test |
| MFOS-REQ-ATTEST-0007 | Guard root claims MUST include root type, version, digest, security_epoch, policy_version, measurement_context, and audit correlation. | schema test |
| MFOS-REQ-ATTEST-0008 | Remote attestation MUST be nonce-bound. | replay negative test |
| MFOS-REQ-ATTEST-0009 | Replayed or stale nonce MUST NOT satisfy attestation. | replay negative test |
| MFOS-REQ-ATTEST-0010 | Attestation responses MUST include audit correlation when auditd or boot audit sink is available. | audit test |
| MFOS-REQ-ATTEST-0011 | Missing required component measurement MUST fail the affected profile claim. | negative test |
| MFOS-REQ-ATTEST-0012 | Mismatched observed digest versus expected digest MUST fail the affected profile claim. | negative test |
| MFOS-REQ-ATTEST-0013 | Unknown or SPEC_GAP evidence state MUST NOT satisfy Enterprise-Standalone, Enterprise-PXM, or High-Assurance claims. | negative test |
| MFOS-REQ-ATTEST-0014 | Boot audit sink evidence MUST be reconciled into auditd before Enterprise-Standalone, Enterprise-PXM, or High-Assurance ready state is claimed. | integration test |
| MFOS-REQ-ATTEST-0015 | Attestation evidence MUST bind requested profile, actual profile state, policy_version, and security_epoch where applicable. | schema test |
| MFOS-REQ-ATTEST-0016 | Guard root mismatch MUST produce failed or recovery-state attestation, not normal High-Assurance ready. | Guard negative test |
| MFOS-REQ-ATTEST-0017 | Measured boot MUST NOT replace uvsd update verification or amfd module verification. | architecture review |
| MFOS-REQ-ATTEST-0018 | Attestation export MUST produce an audit record. | audit test |
| MFOS-REQ-ATTEST-0019 | Recovery attestation MUST identify recovery state and must not claim normal ready state. | recovery test |
| MFOS-REQ-ATTEST-0020 | Unsupported attestation claims MUST return UNSUPPORTED, and undefined claims MUST return SPEC_GAP. | no-fake-success test |

## 16. Failure Modes

| Failure | Required behavior |
| --- | --- |
| TPM absent in Baseline with no attestation claim | Continue without TPM claim. |
| TPM absent in Enterprise measured-boot claim | Deny measured-boot/attestation claim or enter approved recovery/degraded state. |
| TPM absent in High-Assurance | Deny High-Assurance ready state unless approved recovery policy explicitly permits recovery-state evidence. |
| TPM event log missing | Deny Enterprise-Standalone/Enterprise-PXM/HA measured-boot claim. |
| TPM event log malformed | Reject evidence, audit parse failure, deny affected claim. |
| TPM event log replay mismatch | Reject evidence, audit replay mismatch, deny affected claim. |
| Unsupported event type | Return UNSUPPORTED for that event class; deny claim if event is required. |
| SPEC_GAP event type | Return SPEC_GAP; deny claim if event is required. |
| Missing activation profile hash | Deny Enterprise-Standalone/Enterprise-PXM/HA activation evidence claim. |
| Activation profile hash mismatch | Deny activation claim, audit mismatch. |
| Component observed digest mismatch | Deny affected component/profile claim, audit mismatch. |
| Expected digest unavailable | Diagnostic only; cannot satisfy Enterprise-Standalone/Enterprise-PXM/HA claim. |
| Guard unavailable in HA | Deny High-Assurance Guard root claims. |
| Guard root mismatch | Return failed/recovery attestation; audit root mismatch. |
| Guard root state is LOCKDOWN | Attestation may report LOCKDOWN but MUST NOT report normal HA ready. |
| Auditd unavailable after boot | Fail Enterprise-Standalone/Enterprise-PXM/HA ready claim unless boot audit sink reconciliation policy permits recovery/degraded state. |
| Boot audit sink missing when required | Deny profile claim. |
| Nonce missing | Deny Enterprise-Standalone/Enterprise-PXM/HA remote attestation. |
| Nonce replayed | Deny attestation and audit replay. |
| Evidence stale | Deny attestation. |
| Verifier requests unknown claim | Return SPEC_GAP for claim; do not return success for that claim. |
| Signature or quote generation unavailable | Return UNSUPPORTED; deny profiles that require signed/quoted evidence. |

## 17. Negative Tests

```text
ATTEST-NEG-0001  Enterprise measured-boot claim succeeds without TPM event log; test must fail.
ATTEST-NEG-0002  High-Assurance ready claim succeeds without Guard root claims; test must fail.
ATTEST-NEG-0003  Attestation response accepts missing nonce; test must fail for Enterprise-Standalone/Enterprise-PXM/HA.
ATTEST-NEG-0004  Replayed nonce satisfies attestation; test must fail.
ATTEST-NEG-0005  Stale evidence satisfies attestation; test must fail.
ATTEST-NEG-0006  Activation profile hash mismatch still reports ready; test must fail.
ATTEST-NEG-0007  Component digest mismatch still reports ready; test must fail.
ATTEST-NEG-0008  Guard root mismatch reports HIGH_ASSURANCE_READY; test must fail.
ATTEST-NEG-0009  Guard LOCKDOWN reports normal ready state; test must fail.
ATTEST-NEG-0010  Unknown requested claim returns PASS; test must fail.
ATTEST-NEG-0011  SPEC_GAP evidence satisfies Enterprise-Standalone/Enterprise-PXM/HA claim; test must fail.
ATTEST-NEG-0012  Malformed TPM event log is accepted; test must fail.
ATTEST-NEG-0013  Event log replay mismatch is ignored; test must fail.
ATTEST-NEG-0014  Measured boot is described as runtime integrity proof; claim review must fail.
ATTEST-NEG-0015  Secure Boot replaces uvsd update verification; architecture review must fail.
ATTEST-NEG-0016  Attestation export produces no audit record; test must fail.
ATTEST-NEG-0017  Expected digest unavailable but production claim passes; test must fail.
ATTEST-NEG-0018  Recovery-state system claims normal ready state; test must fail.
ATTEST-NEG-0019  Boot audit sink evidence is not reconciled before Enterprise ready; test must fail.
ATTEST-NEG-0020  Unsupported quote generation returns successful attestation; test must fail.
```

## 18. Positive Tests

```text
ATTEST-POS-0001  Baseline reports no measured-boot claim when TPM is absent.
ATTEST-POS-0002  Enterprise attestation includes nonce, boot session, TPM event log hash, activation profile hash, component measurement set hash, and audit correlation.
ATTEST-POS-0003  High-Assurance attestation includes Guard root claims for security policy, audit chain, AMF registry, activation profile, and update policy when claimed.
ATTEST-POS-0004  Activation profile hash is recorded before PXM activation.
ATTEST-POS-0005  Component digest match is recorded with expected and observed digest.
ATTEST-POS-0006  Attestation response echoes verifier nonce exactly.
ATTEST-POS-0007  Audit record links attestation_id, boot_session_id, measurement_context, and audit_correlation_id.
ATTEST-POS-0008  Recovery attestation reports RECOVERY state and does not claim normal ready.
ATTEST-POS-0009  Unsupported optional claim returns UNSUPPORTED without invalidating unrelated required claims.
ATTEST-POS-0010  Event log parser rejects malformed record and emits audit failure evidence.
```

## 19. Evidence Artifacts

Measured boot and attestation evidence MUST produce or link:

```text
EVID-ATTEST-BOOT-SESSION
EVID-ATTEST-TPM-EVENTLOG-RAW
EVID-ATTEST-TPM-EVENTLOG-PARSED
EVID-ATTEST-PCR-CLAIMS
EVID-ATTEST-COMPONENT-MEASUREMENTS
EVID-ATTEST-ACTIVATION-PROFILE
EVID-ATTEST-PXM-MEASUREMENT
EVID-ATTEST-GUARD-MEASUREMENT
EVID-ATTEST-GUARD-ROOTS
EVID-ATTEST-UPDATE-EPOCH
EVID-ATTEST-AUDIT-CORRELATION
EVID-ATTEST-REMOTE-REQUEST
EVID-ATTEST-REMOTE-RESPONSE
EVID-ATTEST-NONCE-FRESHNESS
EVID-ATTEST-QUOTE
EVID-ATTEST-SIGNATURE
EVID-ATTEST-NEGATIVE-TESTS
EVID-ATTEST-SPEC-GAPS
```

Each evidence artifact SHOULD include:

- evidence_id
- boot_session_id
- attestation_id where applicable
- profile requested
- profile claimed
- profile actually reached
- component IDs
- expected digests
- observed digests
- activation profile hash
- policy_version
- security_epoch
- Guard root digests where applicable
- TPM event log reference
- PCR claim references
- nonce and freshness status
- audit_event_ids
- audit_correlation_id
- source_matrix_refs
- requirement_ids
- SPEC_GAPs

## 20. Attestation Evidence Bundle Draft

```yaml
AttestationEvidenceBundle:
  schema_version: 1
  bundle_id: uuid
  boot_session_id: uuid
  attestation_id: uuid?
  generated_at: timestamp
  requested_profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  actual_profile_state: NOT_CLAIMED | BASELINE_READY | ENTERPRISE_READY | HIGH_ASSURANCE_READY | RECOVERY | DEGRADED | FAILED
  measurement_context: sha384
  activation_profile_hash: sha384?
  component_measurement_set_hash: sha384
  tpm_event_log:
    raw_ref: string?
    parsed_ref: string?
    replay_result: PASS | FAIL | UNSUPPORTED | SPEC_GAP
  guard_roots:
    - root_type: string
      root_version: uint64
      root_digest: sha384
      root_state: string
      audit_event_id: uuid?
  audit:
    audit_correlation_id: uuid
    boot_audit_sink_ref: string?
    auditd_reconciliation_event_id: uuid?
    audit_head_sequence: uint64?
    audit_head_hash: sha384?
  freshness:
    nonce: bytes?
    nonce_status: MATCHED | MISSING | REPLAYED | STALE | NOT_APPLICABLE | SPEC_GAP
    max_age_seconds: uint64?
    evidence_age_seconds: uint64?
  result: PASS | FAIL | DEGRADED | RECOVERY | UNSUPPORTED | SPEC_GAP
  reason_code: string
  signature_ref: string?
  quote_ref: string?
  spec_gaps:
    - string
```

Final serialization and signing are SPEC_GAPs.

## 21. Inactive Future Implementation Prompt Template

Phase status: inactive future template. This section does not authorize production implementation, hosted daemon implementation, or portable semantic-core implementation.

```text
You are an MFOS measured boot and attestation implementation agent.

Use docs/design/specs/30-attestation-measured-boot.md and linked specs.

Hard constraints:
- Do not claim z/OS compatibility.
- Do not claim external attestation ecosystem compatibility.
- Do not describe measured boot as runtime integrity proof.
- Do not let TPM, Secure Boot, PCRs, quotes, or event logs replace securityd,
  auditd, uvsd, PXM, or Guard.
- Return UNSUPPORTED for specified but unavailable attestation behavior.
- Return SPEC_GAP for undefined event, claim, quote, or evidence behavior.
- Missing, malformed, stale, replayed, UNKNOWN, or SPEC_GAP evidence must not
  satisfy Enterprise-Standalone, Enterprise-PXM, or High-Assurance claims.
- Remote attestation must be nonce-bound.
- High-Assurance attestation must include Guard root claims for claimed roots.
- Attestation export must be audited.

Required output:
1. Implemented Requirement IDs
2. Source Matrix IDs
3. Assumptions
4. Component Measurements Implemented
5. Event Log Handling
6. Activation Profile Hash Handling
7. Guard Root Claims
8. Remote Attestation Claims
9. Freshness and Nonce Handling
10. Audit Correlation
11. Failure Modes
12. Negative Tests Added
13. Evidence Artifacts
14. SPEC_GAPs
```

## 22. SPEC_GAPs

Global attestation and measured boot gaps:

- Final TPM event log parser and supported event formats.
- Final PCR bank policy.
- Final digest algorithms and migration policy.
- Final boot session ID creation and persistence rules.
- Final measured component list for each release profile.
- Final activation profile canonicalization.
- Final measurement_context canonicalization.
- Final Guard root claim canonicalization.
- Final remote attestation protocol.
- Final quote format.
- Final signature format.
- Final verifier trust anchor and certificate chain policy.
- Final nonce storage and replay cache.
- Final freshness time source policy.
- Final audit boot-sink format and reconciliation protocol.
- Final attestation evidence bundle serialization.
- Final evidence signing or immutability mechanism.
- Final recovery-state attestation policy.
- Final side-partition or remote verifier authorization policy.
- Final handling for systems without TPM but with alternative measured-boot evidence.
- Final relationship between attestation evidence and release provenance/SBOM.

Agents MUST NOT fill these gaps with success-path behavior. They must return SPEC_GAP or UNSUPPORTED as appropriate.
