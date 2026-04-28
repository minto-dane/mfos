---
spec_id: "MFOS-SPEC-17-GUARD"
title: "MFOS Design Specification 17: PXM Guard"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001", "MS-VBS-001", "MS-VSM-001", "NIST-160-001", "TCG-001", "X64-AMD-001", "X64-INTEL-001"]
requirement_refs: ["MFOS-REQ-GUARD-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Design Specification 17: PXM Guard

Status: Draft v0.1

Audience: high-assurance architecture agents, Guard implementation agents, security reviewers, formal methods engineers, test engineers

This document defines PXM Guard. Guard is a High-Assurance profile component that protects selected MFOS root objects after measured boot and during root transitions. Guard is not the MFOS kernel, not securityd, not auditd, not a job scheduler, and not a dataset policy engine.

MFOS is z/OS-inspired, not z/OS-compatible. PXM Guard uses VBS/VSM-like isolation concepts as an architectural reference, but it is not Windows VBS, not Windows VSM, and not a clone of any Microsoft implementation.

## 1. Purpose

PXM Guard exists to keep a very small set of high-value roots from being silently modified by a compromised or confused MFOS component.

Guard protects:

- Security policy root.
- Audit chain root.
- AMF registry root.
- SVC table root.
- Nucleus text measurement root.
- Executable mapping policy root.
- Page table policy root.
- Activation profile root.
- Emergency state root.
- Update policy root.

Guard provides:

- Root sealing.
- Root verification.
- Root transition authorization.
- Executable mapping authorization.
- AMF load authorization for High-Assurance.
- SVC table integrity checks.
- Audit root append.
- Emergency mode entry and exit checks.
- Measurement-bound secret release.
- Attestation.

Guard must be boring: small, explicit, deterministic, auditable, and hostile to feature growth.

## 2. Scope

### 2.1 In Scope

- High-Assurance root object model.
- Guard lifecycle.
- Guard call ABI.
- Guard root transition state machine.
- Executable mapping authorization.
- AMF registry sealing.
- SVC table verification.
- Audit chain root append.
- Emergency mode root transition.
- Guard attestation.
- Guard failure policies.
- Guard audit obligations.

### 2.2 Out of Scope

- Ordinary dataset contents.
- Dataset access policy interpretation.
- Catalog lookup.
- Job scheduling.
- Spool formatting.
- Operator UI rendering.
- POSIX subsystem behavior.
- Linux/Desktop application behavior.
- Normal business policy interpretation.
- Broad cryptographic policy selection beyond required root validation primitives.
- Replacing securityd.
- Replacing auditd.
- Replacing PXM Core.

## 3. Source Matrix References

| Source ID | Use |
| --- | --- |
| EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001 | System integrity reference for separating unauthorized behavior from authorized state claims. |
| EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001 | Authorized-program boundary reference used for AMF root protection framing. |
| EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001 | Authorized-boundary negative testing reference for SVC, PCALL, and AMF paths. |
| X64-INTEL-001 | x64 page table, VMX, EPT, MSR, CET, PKU/PKS, and protection reference. |
| X64-AMD-001 | AMD64 SVM, NPT, and system programming reference. |
| MS-VBS-001 | Reference for isolated code integrity and executable mapping concepts. |
| MS-VSM-001 | Reference for a higher-privilege isolation layer controlling memory access protections. |
| TCG-001 | Measured boot and TPM event log reference. |
| NIST-160-001 | Secure system engineering lifecycle reference. |
| FBVBS-001 | Internal transfer source for Guard-like root protection, command ABI discipline, audit roots, and proof obligations. |

Guard references Microsoft VBS/VSM as informative design input only. MFOS must not claim Windows compatibility or reuse Microsoft-specific semantics as MFOS guarantees.

## 4. Normative Language

The keywords MUST, MUST NOT, REQUIRED, SHOULD, SHOULD NOT, MAY, UNSUPPORTED, and SPEC_GAP are normative for this specification.

- MUST means required for the applicable conformance profile.
- SHOULD means strongly recommended; divergence requires an ADR and evidence.
- MAY means optional and not part of a guarantee unless a profile says otherwise.
- UNSUPPORTED means specified behavior that is not implemented in a given build and must fail closed.
- SPEC_GAP means behavior with no approved specification. It must not be implemented as a success path.

## 5. Profile Applicability

| Capability | Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance |
| --- | --- | --- | --- | --- |
| Guard component | NOT REQUIRED | NOT REQUIRED | OPTIONAL measurement helper | MUST |
| Guard-sealed security root | NOT REQUIRED | NOT REQUIRED | OPTIONAL | MUST |
| Guard-sealed audit root | NOT REQUIRED | NOT REQUIRED | OPTIONAL | MUST |
| Guard AMF approval | NOT REQUIRED | NOT REQUIRED | OPTIONAL | MUST |
| Guard executable mapping policy | NOT REQUIRED | NOT REQUIRED | OPTIONAL | MUST |
| Guard SVC table verification | NOT REQUIRED | NOT REQUIRED | OPTIONAL | MUST |
| Guard attestation | NOT REQUIRED | NOT REQUIRED | OPTIONAL | MUST |
| Guard failure boot policy | NOT REQUIRED | NOT REQUIRED | SHOULD if Guard enabled | MUST |

Baseline and Enterprise builds may compile without Guard. They must not claim High-Assurance root protection.

## 6. Terms

### 6.1 Guard Root

A Guard Root is a compact, versioned, measurement-bound digest representing the authoritative state of a protected root object.

### 6.2 Root Transition

A Root Transition is a change from one accepted root digest and version to another accepted root digest and version.

### 6.3 Guard-Sealed

Guard-Sealed means Guard recorded and accepted the root digest, version, policy epoch, and transition evidence. It does not mean that all business policy semantics were interpreted by Guard.

### 6.4 Executable Mapping

An Executable Mapping is a transition that makes a page range executable for a code identity. Guard authorizes the mapping policy, not the code's business behavior.

### 6.5 Emergency State

Emergency State is a restricted root state that permits break-glass or recovery actions under explicit reason, expiry, operator identity, and audit obligations.

## 7. Guard Root Object Model

### 7.1 GuardRoot

```yaml
GuardRoot:
  root_type: GuardRootType
  root_id: string
  version: uint64
  security_epoch: uint64
  digest: sha384
  policy_version: uint64
  activation_profile_hash: sha384
  measurement_context: sha384
  state: UNSEALED | SEALED | VERIFIED | TRANSITION_PENDING | REVOKED | FAULTED
  last_transition_id: uuid?
  sealed_at: timestamp?
```

### 7.2 GuardRootType

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

### 7.3 GuardRootTransition

```yaml
GuardRootTransition:
  transition_id: uuid
  root_type: GuardRootType
  old_version: uint64
  old_digest: sha384
  new_version: uint64
  new_digest: sha384
  security_epoch: uint64
  policy_version: uint64
  actor: SubjectRef
  reason_code: string
  approval_refs: [string]
  audit_correlation_id: uuid
  requested_at: timestamp
  decided_at: timestamp?
  decision: ALLOW | DENY | FAIL_CLOSED
```

### 7.4 CodeIdentity

```yaml
CodeIdentity:
  code_id: string
  component_type: nucleus | service | amf_module | pxm_core | pxm_guard | recovery_image
  digest: sha384
  signer: string?
  authority_class: string?
  security_epoch: uint64
  measurement_context: sha384
  source_matrix_refs: [string]
```

### 7.5 ExecutableMappingRequest

```yaml
ExecutableMappingRequest:
  page_range_id: string
  start_address: uint64
  size: uint64
  requested_permissions: READ_EXECUTE | EXECUTE_ONLY
  code_identity: CodeIdentity
  policy_version: uint64
  previous_mapping_digest: sha384?
  caller_component: string
  correlation_id: uuid
```

## 8. Responsibilities

Guard MUST implement:

- GRD-R-001 Guard root model.
- GRD-R-002 Guard call ABI.
- GRD-R-003 security root seal.
- GRD-R-004 audit root seal.
- GRD-R-005 AMF registry seal.
- GRD-R-006 SVC table verification.
- GRD-R-007 executable mapping policy.
- GRD-R-008 attestation.
- GRD-R-009 failure policy.
- GRD-R-010 lockdown tests.
- GRD-R-011 update policy root verification.
- GRD-R-012 emergency state entry and exit.
- GRD-R-013 measurement-bound secret release.

## 9. Non-Responsibilities

Guard MUST NOT:

- Decide whether ALICE can read USER.ALICE.INPUT.
- Parse JCL-like job control.
- Resolve DSNs.
- Browse, purge, or format spool entries.
- Interpret workload policy service class goals.
- Render operator panels.
- Act as the operator console.
- Replace securityd as the policy decision point.
- Replace auditd as the audit record schema owner.
- Implement general filesystem semantics.
- Implement POSIX semantics.
- Host Linux/Desktop applications.
- Become a broad microkernel.
- Expose arbitrary pointer APIs.
- Accept unbounded payloads.
- Treat PKU or PKS as a substitute for Guard isolation.

## 10. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-GUARD-0001 | Guard MUST be required only for High-Assurance conformance. | profile review |
| MFOS-REQ-GUARD-0002 | Guard scope MUST be limited to root objects listed in this spec. | architecture review |
| MFOS-REQ-GUARD-0003 | Guard MUST NOT interpret dataset, job, spool, catalog, or workload policy semantics. | architecture review |
| MFOS-REQ-GUARD-0004 | Security policy root transitions MUST be recorded by both Guard and auditd. | integration test |
| MFOS-REQ-GUARD-0005 | Executable mappings MUST NOT violate Guard executable mapping policy. | negative test |
| MFOS-REQ-GUARD-0006 | SVC table mismatch MUST trigger lockdown or panic-equivalent failure policy. | fault injection |
| MFOS-REQ-GUARD-0007 | AMF registry mismatch MUST deny AMF load and generate audit alert. | negative test |
| MFOS-REQ-GUARD-0008 | Guard unavailable boot behavior MUST be defined per profile. | boot test |
| MFOS-REQ-GUARD-0009 | Guard calls MUST use typed bounded payloads and reject reserved nonzero fields. | ABI test |
| MFOS-REQ-GUARD-0010 | Guard MUST bind root versions to security_epoch and policy_version. | rollback test |
| MFOS-REQ-GUARD-0011 | Guard MUST reject rollback to an older root version unless an approved recovery policy explicitly allows it. | rollback negative test |
| MFOS-REQ-GUARD-0012 | Guard MUST reject root transition requests with stale measurement_context. | replay negative test |
| MFOS-REQ-GUARD-0013 | Guard MUST authorize High-Assurance AMF loads before executable mapping. | AMF integration test |
| MFOS-REQ-GUARD-0014 | Guard MUST append audit root updates monotonically by record sequence. | audit chain test |
| MFOS-REQ-GUARD-0015 | Guard MUST distinguish UNSUPPORTED from SPEC_GAP. | error model test |
| MFOS-REQ-GUARD-0016 | Guard MUST not return success if required audit evidence cannot be recorded. | audit failure test |
| MFOS-REQ-GUARD-0017 | Guard MUST provide attestation over selected claims and caller-provided nonce. | attestation test |
| MFOS-REQ-GUARD-0018 | Guard secret release MUST be bound to measurement_context and root state. | secret release test |
| MFOS-REQ-GUARD-0019 | Guard emergency mode entry MUST require reason, operator identity, expiry, and audit. | emergency drill |
| MFOS-REQ-GUARD-0020 | Guard emergency mode exit MUST audit the exit and reverify affected roots. | emergency drill |

## 11. Guard Lifecycle

```text
UNINITIALIZED
  -> MEASURED
  -> INITIALIZED
  -> ROOTS_SEALED
  -> READY
  -> LOCKDOWN
  -> RECOVERY
  -> SHUTDOWN
```

### 11.1 Lifecycle Rules

- UNINITIALIZED cannot accept root transition calls.
- MEASURED records Guard image and policy measurements.
- INITIALIZED accepts only boot root setup calls.
- ROOTS_SEALED means required initial roots are sealed for the active High-Assurance policy.
- READY means Guard can authorize root transitions and mapping calls.
- LOCKDOWN means Guard detected a root mismatch, policy violation, replay, or required audit failure.
- RECOVERY means Guard is operating only through approved recovery policy.
- SHUTDOWN means Guard has stopped accepting calls except platform teardown events.

### 11.2 Lifecycle Failure Rules

- High-Assurance boot MUST fail if Guard cannot reach ROOTS_SEALED.
- If Guard detects SVC table mismatch in READY, it MUST enter LOCKDOWN or trigger panic-equivalent behavior.
- If audit root append fails under High-Assurance, Guard MUST enter LOCKDOWN unless recovery policy explicitly permits RECOVERY.

## 12. Guard Root State Machine

### 12.1 States

```text
UNSEALED
SEALED
VERIFIED
TRANSITION_PENDING
REVOKED
FAULTED
```

### 12.2 Legal Transitions

| Current | Trigger | Next | Required condition |
| --- | --- | --- | --- |
| UNSEALED | SEAL_ROOT | SEALED | Digest, version, epoch, and measurement context accepted. |
| SEALED | VERIFY_ROOT | VERIFIED | Presented digest and version match sealed root. |
| VERIFIED | REQUEST_TRANSITION | TRANSITION_PENDING | Caller authorized and transition request is well formed. |
| TRANSITION_PENDING | APPROVE_TRANSITION | SEALED | New digest, version, epoch, approval, and audit accepted. |
| TRANSITION_PENDING | DENY_TRANSITION | VERIFIED | Denial recorded and old root remains active. |
| SEALED | REVOKE_ROOT | REVOKED | Recovery or update policy allows revocation. |
| VERIFIED | REVOKE_ROOT | REVOKED | Recovery or update policy allows revocation. |
| SEALED | ROOT_MISMATCH | FAULTED | Mismatch recorded and failure policy invoked. |
| VERIFIED | ROOT_MISMATCH | FAULTED | Mismatch recorded and failure policy invoked. |
| TRANSITION_PENDING | ROOT_MISMATCH | FAULTED | Mismatch recorded and failure policy invoked. |
| FAULTED | RECOVERY_RESEAL | SEALED | Recovery policy, measurements, and audit accepted. |

All other transitions MUST return MFOS_ERR_GUARD_DENIED or MFOS_ERR_PARTITION_INVALID_STATE and MUST audit the denial when audit is available.

## 13. Guard Call ABI

### 13.1 Common Request Header

```yaml
GuardCallHeader:
  abi_magic: "GRDC"
  abi_version: uint16
  command: GuardCommand
  caller_sequence: uint64
  caller_subject: SubjectRef
  caller_component: string
  caller_partition_id: uint64
  policy_version: uint64
  security_epoch: uint64
  correlation_id: uuid
  nonce: bytes?
  request_length: uint32
  request_hash: sha384
  reserved_zero: bytes
```

Rules:

- reserved_zero MUST be zero.
- caller_sequence MUST be monotonic per caller endpoint.
- nonce MUST be present for ATTEST.
- request_length MUST be bounded by the active profile.
- caller identity MUST come from authenticated execution context, not payload self-claims.
- Unknown commands MUST return MFOS_ERR_SPEC_GAP unless specified but unimplemented, in which case they MUST return MFOS_ERR_UNSUPPORTED.

### 13.2 Commands

```text
GUARD_MEASURE_COMPONENT
GUARD_SEAL_ROOT
GUARD_VERIFY_ROOT
GUARD_REQUEST_ROOT_TRANSITION
GUARD_APPROVE_ROOT_TRANSITION
GUARD_AUTHORIZE_EXEC_MAPPING
GUARD_AUTHORIZE_AMF_LOAD
GUARD_VERIFY_SVC_TABLE
GUARD_APPEND_AUDIT_ROOT
GUARD_ENTER_EMERGENCY_MODE
GUARD_EXIT_EMERGENCY_MODE
GUARD_RELEASE_SECRET
GUARD_ATTEST
GUARD_GET_STATUS
```

### 13.3 Response

```yaml
GuardCallResponse:
  abi_magic: "GRDR"
  abi_version: uint16
  command: GuardCommand
  caller_sequence: uint64
  correlation_id: uuid
  result: MfosErrorCode
  reason_code: string
  guard_lifecycle_state: string
  root_type: GuardRootType?
  root_version: uint64?
  root_digest: sha384?
  audit_event_id: uuid?
  attestation_blob: bytes?
  payload_length: uint32
  payload_hash: sha384?
```

### 13.4 Error Codes

Guard calls MUST use the MFOS error model, including:

```text
MFOS_OK
MFOS_ERR_UNAUTHENTICATED
MFOS_ERR_UNAUTHORIZED
MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE
MFOS_ERR_UNSUPPORTED
MFOS_ERR_SPEC_GAP
MFOS_ERR_INVALID_PARAMETER
MFOS_ERR_AMF_SIGNATURE_INVALID
MFOS_ERR_AMF_REVOKED
MFOS_ERR_GUARD_REQUIRED
MFOS_ERR_GUARD_DENIED
MFOS_ERR_ROLLBACK_DETECTED
MFOS_ERR_FREEZE_DETECTED
MFOS_ERR_MIX_AND_MATCH_DETECTED
MFOS_ERR_INTERNAL_CORRUPTION
```

## 14. Protected Root Rules

### 14.1 Security Policy Root

- Guard stores the digest and version of the active security policy root.
- securityd remains the policy interpreter.
- Guard authorizes root transitions, not individual access checks.
- Rollback to older policy_version MUST be denied unless recovery policy explicitly allows it.

### 14.2 Audit Chain Root

- Guard stores the latest accepted audit chain root.
- auditd remains the audit schema owner and record producer.
- Guard accepts monotonic append operations with record sequence and chain hash.
- Out-of-order append MUST be denied.

### 14.3 AMF Registry Root

- Guard stores the digest of the approved AMF registry.
- amfd remains the AMF manifest parser and loader.
- Guard authorizes High-Assurance AMF loads against registry digest, signer, module digest, authority class, and security_epoch.
- Revoked signer, digest, or epoch MUST fail closed.

### 14.4 SVC Table Root

- Guard stores the SVC table digest.
- The nucleus remains the SVC implementation owner.
- SVC table mismatch MUST cause lockdown or panic-equivalent behavior.

### 14.5 Nucleus Text Root

- Guard stores measured nucleus text digest.
- Guard does not patch nucleus code.
- Mismatch MUST trigger High-Assurance failure policy.

### 14.6 Executable Mapping Policy Root

- Guard authorizes page ranges becoming executable.
- Writable and executable at the same time MUST be denied unless a future spec explicitly defines a safe transition.
- Guard MUST verify code identity, digest, security_epoch, and policy_version.

### 14.7 Page Table Policy Root

- Guard stores the page table policy root.
- Guard does not become a general page fault handler.
- Guard denies root policy violations and records audit evidence.

### 14.8 Activation Profile Root

- Guard stores activation profile digest for High-Assurance partitions.
- PXM remains the activation lifecycle owner.
- Activation profile root mismatch MUST deny High-Assurance activation.

### 14.9 Emergency State Root

- Guard stores emergency mode state, reason, actor, expiry, and affected roots.
- Emergency mode cannot disable audit.
- Emergency mode cannot create unlimited root transition authority.

### 14.10 Update Policy Root

- Guard stores update policy root for High-Assurance.
- uvsd remains the update metadata verifier.
- Guard denies rollback, freeze, and mix-and-match outcomes when uvsd evidence conflicts with Guard root state.

## 15. Invariants

```text
INV-GRD-001:
  Guard scope is limited to the approved GuardRootType set.

INV-GRD-002:
  Guard cannot interpret ordinary dataset, job, spool, catalog, POSIX,
  Linux/Desktop, or workload policy business semantics.

INV-GRD-003:
  A High-Assurance executable mapping cannot become active unless Guard
  authorized the code identity, digest, security_epoch, policy_version,
  and page range.

INV-GRD-004:
  Audit root sequence numbers accepted by Guard are strictly monotonic.

INV-GRD-005:
  A root transition cannot reduce security_epoch unless an approved
  recovery policy explicitly permits it.

INV-GRD-006:
  SVC table root mismatch cannot be ignored.

INV-GRD-007:
  Guard success requires audit evidence when the operation has an audit
  obligation under the active High-Assurance policy.

INV-GRD-008:
  Guard cannot accept caller-supplied identity, state, root digest, or
  measurement context as authoritative without independent verification.

INV-GRD-009:
  Emergency mode cannot disable Guard audit root append requirements.

INV-GRD-010:
  PKU and PKS cannot be used as replacements for Guard root protection.
```

## 16. Audit Obligations

Guard MUST produce or require audit records for:

- Guard initialization.
- Guard roots sealed.
- Guard root verified.
- Guard root transition requested.
- Guard root transition approved.
- Guard root transition denied.
- Guard root mismatch.
- Executable mapping allowed or denied.
- AMF load allowed or denied.
- SVC table verified.
- SVC table mismatch.
- Audit root appended.
- Audit root append denied.
- Emergency mode entered.
- Emergency mode exited.
- Secret release allowed or denied.
- Attestation requested.
- Guard lockdown entered.
- Guard recovery mode entered.
- Guard unavailable at boot when required.
- UNSUPPORTED operation attempt.
- SPEC_GAP operation attempt.

### 16.1 Audit Timing

- Denied Guard decisions MUST be recorded before final result returns when the audit path is available.
- High-Assurance Guard success MUST NOT be returned if the operation requires Guard-sealed audit and the audit append fails.
- During early boot, Guard MAY use a boot audit sink, but reconciliation into auditd is required before High-Assurance ready state.

### 16.2 Audit Fields

Guard audit records MUST include:

- event_id
- timestamp_utc
- component_id = "pxm_guard"
- operation
- subject
- caller_component
- root_type when applicable
- old_root_version when applicable
- new_root_version when applicable
- old_digest when applicable
- new_digest when applicable
- policy_version
- security_epoch
- measurement_context
- decision
- reason_code
- correlation_id

## 17. Failure Modes

| Failure | Required behavior |
| --- | --- |
| Guard required but unavailable at High-Assurance boot | Deny boot or enter approved recovery mode. |
| Initial root seal failure | Deny High-Assurance ready state. |
| Root digest mismatch | Enter LOCKDOWN or configured panic-equivalent failure. |
| SVC table mismatch | Enter LOCKDOWN or panic-equivalent failure. |
| AMF registry mismatch | Deny AMF load and audit alert. |
| Executable mapping policy violation | Deny mapping, keep pages non-executable, audit denial. |
| Writable-executable mapping request | Deny unless future approved spec defines a safe path. |
| Audit root append failure | Fail closed or enter recovery based on policy. |
| Stale measurement context | Deny and audit replay/stale evidence. |
| Root rollback attempt | Deny and return rollback error. |
| security_epoch downgrade | Deny unless approved recovery policy allows it. |
| Unknown Guard command | Return SPEC_GAP and audit. |
| Specified but unavailable Guard command | Return UNSUPPORTED and audit. |
| Emergency mode expired | Deny emergency-only operations and require exit or renewal workflow. |
| Internal Guard metadata corruption | Enter LOCKDOWN and require recovery workflow. |

## 18. Tests

### 18.1 Positive Tests

- GRD-T-POS-0001: Guard initializes and reaches ROOTS_SEALED with valid High-Assurance boot inputs.
- GRD-T-POS-0002: Security policy root seal records digest, version, policy_version, and security_epoch.
- GRD-T-POS-0003: VERIFY_ROOT succeeds for matching digest and version.
- GRD-T-POS-0004: Approved security policy root transition moves TRANSITION_PENDING to SEALED.
- GRD-T-POS-0005: Audit root append accepts monotonic record sequence.
- GRD-T-POS-0006: AMF load is authorized for approved digest, signer, authority class, and epoch.
- GRD-T-POS-0007: Executable mapping succeeds for approved code identity and page range.
- GRD-T-POS-0008: SVC table verification succeeds for matching digest.
- GRD-T-POS-0009: ATTEST includes caller nonce and selected claims.
- GRD-T-POS-0010: Emergency mode entry succeeds with reason, operator identity, expiry, and audit.

### 18.2 Negative Tests

- GRD-T-NEG-0001: Guard refuses dataset read authorization request.
- GRD-T-NEG-0002: Guard refuses job scheduling request.
- GRD-T-NEG-0003: Root rollback without recovery policy is denied.
- GRD-T-NEG-0004: security_epoch downgrade is denied.
- GRD-T-NEG-0005: Stale measurement_context is denied.
- GRD-T-NEG-0006: Non-monotonic audit root append is denied.
- GRD-T-NEG-0007: SVC table mismatch triggers lockdown or panic-equivalent behavior.
- GRD-T-NEG-0008: AMF registry mismatch denies AMF load.
- GRD-T-NEG-0009: Revoked AMF signer denies AMF load.
- GRD-T-NEG-0010: Writable-executable mapping request is denied.
- GRD-T-NEG-0011: Unknown command returns SPEC_GAP, not success.
- GRD-T-NEG-0012: Specified but unavailable command returns UNSUPPORTED, not success.
- GRD-T-NEG-0013: Nonzero reserved field in Guard call header is rejected.
- GRD-T-NEG-0014: Replayed caller_sequence is denied.
- GRD-T-NEG-0015: Emergency mode request without expiry is denied.
- GRD-T-NEG-0016: Emergency mode request without audit path is denied under High-Assurance.

### 18.3 Fuzz Targets

- GRD-FUZZ-0001: Guard call header parser.
- GRD-FUZZ-0002: Root transition payload parser.
- GRD-FUZZ-0003: Executable mapping request parser.
- GRD-FUZZ-0004: AMF authorization request parser.
- GRD-FUZZ-0005: Attestation claim selector parser.

### 18.4 Fault-Injection Tests

- GRD-FI-0001: Audit root append storage failure.
- GRD-FI-0002: Guard metadata corruption before VERIFY_ROOT.
- GRD-FI-0003: SVC table mutation after READY.
- GRD-FI-0004: AMF registry digest mutation after seal.
- GRD-FI-0005: Attestation nonce replay.

## 19. Evidence Artifacts

Implementation agents MUST produce:

- Requirement IDs implemented.
- Source Matrix IDs referenced.
- Guard root state machine transition tests.
- Guard call ABI tests.
- Root rollback and epoch downgrade negative tests.
- Audit root monotonicity evidence.
- SVC table mismatch evidence.
- AMF registry mismatch evidence.
- Executable mapping denial evidence.
- Attestation sample with nonce.
- UNSUPPORTED and SPEC_GAP inventory.
- High-Assurance profile claim statement.

## 20. Spec Gaps

The following are intentionally not specified yet:

- Exact isolation mechanism for Guard on each x64 platform.
- Exact VMX/SVM/VTL-like implementation strategy.
- Exact Guard memory layout.
- Exact cryptographic signature algorithms and key hierarchy.
- Exact attestation evidence format.
- Exact secret release key derivation design.
- Exact panic-equivalent behavior for each boot profile.
- Exact boot audit sink format before auditd is available.
- Formal TLA+/Alloy model file path and syntax.
- Guard performance budget and batching policy.

Agents MUST NOT fill these gaps with success-path code. They must return SPEC_GAP or UNSUPPORTED as appropriate.

## 21. Inactive Future Implementation Prompt Template

Phase status: inactive future template. This section does not authorize production implementation, hosted daemon implementation, or portable semantic-core implementation.

```text
You are an MFOS PXM Guard implementation agent.

Implement only the Guard behavior covered by docs/design/specs/17-guard.md.

Hard constraints:
- Do not claim z/OS compatibility.
- Do not claim Windows VBS or VSM compatibility.
- Keep Guard small and limited to approved GuardRootType objects.
- Do not implement dataset, catalog, job, spool, workload policy, POSIX, Linux/Desktop, or operator UI semantics in Guard.
- Do not replace securityd or auditd.
- Use requirement IDs in code comments and tests.
- Use Source Matrix IDs in design comments where VBS/VSM-like, x64, or IBM system-integrity concepts are used.
- No fake success, empty stub, or silent fallback.
- Return UNSUPPORTED for specified but unavailable behavior.
- Return SPEC_GAP for unspecified behavior.
- Enforce root state machine transitions.
- Deny rollback, stale measurement context, and security_epoch downgrade unless approved recovery policy allows them.
- Enforce executable mapping authorization.
- Enforce AMF registry root authorization in High-Assurance.
- Enforce audit root monotonic append.
- Add positive, negative, fuzz, and fault-injection tests with IDs from this spec.

Required output:
1. Implemented Requirement IDs
2. Source Matrix IDs
3. Assumptions
4. Spec Gaps
5. Unsupported Features
6. Security Invariants
7. Audit Obligations
8. Failure Modes
9. Tests Added
10. Negative Tests Added
11. Fuzz Targets Added
12. Unsafe Code Justification
13. Review Checklist
14. Evidence Artifacts
```
