---
spec_id: "MFOS-SPEC-15-SVC-PCALL"
title: "MFOS SVC and PCALL ABI Specification v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001", "EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001", "EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001", "NIST-160-001", "X64-AMD-001", "X64-INTEL-001"]
requirement_refs: ["MFOS-REQ-PCALL-*", "MFOS-REQ-SVC-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS SVC and PCALL ABI Specification v0.1

Status: Draft  
Owner: MFOS architecture  
Profile applicability: Baseline, Enterprise-Standalone, Enterprise-PXM, High-Assurance  
Source basis: user-provided MFOS Source-Grounded High-Assurance Architecture v0.3

## 1. Purpose

This document specifies the MFOS SVC and PCALL ABIs.

SVC is the nucleus-mediated system call boundary. PCALL is the typed synchronous service-call boundary between MFOS services or between nucleus-mediated callers and trusted services.

The ABI design is inspired by enterprise operating-system system-interface discipline and cross-memory communication concerns, but MFOS does not claim z/OS SVC, PC instruction, cross-memory, assembler-services, or binary compatibility.

## 2. Scope

This spec covers:

- SVC frame layout.
- SVC dispatch rules.
- PCALL endpoint model.
- PCALL frame layout.
- Typed buffer and handle passing.
- Identity propagation.
- securityd authorization propagation.
- auditd obligation propagation.
- Error model.
- Endpoint manifests.
- Failure modes.
- Tests, negative tests, fuzz targets, and spec gaps.

## 3. Non-Objectives

SVC/PCALL must not:

- Provide arbitrary cross-address-space pointer access.
- Trust caller-supplied identity.
- Let services bypass securityd.
- Let services bypass auditd obligations.
- Act as a POSIX syscall compatibility ABI.
- Act as a z/OS SVC or PC compatibility ABI.
- Create a hidden root shell path.
- Return fake success for unsupported or undefined operations.

## 4. Source Matrix References

Required source IDs for this spec:

- EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001: system integrity and system-interface discipline.
- EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001: authorized-boundary negative test discipline.
- EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001: cross-memory communication inspiration.
- EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001: cross-memory security controls inspiration.
- EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001: authorized boundary concept inspiration.
- X64-INTEL-001: x64 trap, privilege, paging, and protection reality.
- X64-AMD-001: AMD64 system programming reality.
- FBVBS-001: fixed command page, caller sequence, unused-field zeroing, fixed error codes, and no-fake-success discipline.
- NIST-160-001: secure system engineering.

## 5. Design Principles

1. Caller identity comes from scheduler and nucleus context, not caller memory.
2. User pointers are opaque until validated through bounded copy-in/copy-out.
3. SVC calls are typed and versioned.
4. PCALL endpoints are typed and versioned.
5. Protected resource decisions are mediated by securityd.
6. Audit obligations are explicit and propagated.
7. Unsupported specified operations return `MFOS_ERR_UNSUPPORTED`.
8. Undefined operations return `MFOS_ERR_SPEC_GAP`.
9. All reserved fields must be zero on input and preserved or zeroed on output as specified.
10. No normal SVC/PCALL path may require Guard transition; Guard calls are separate and profile-scoped.

## 6. ABI Versioning

```text
SVC ABI version:   svc-v1
PCALL ABI version: pcall-v1
Buffer ABI:        sealed-buffer-v1
Handle ABI:        typed-handle-v1
```

Rules:

- ABI major version mismatch returns `MFOS_ERR_UNSUPPORTED`.
- ABI minor version with unknown required flag returns `MFOS_ERR_UNSUPPORTED`.
- Unknown reserved bits set by caller return `MFOS_ERR_INVALID_PARAMETER`.
- ABI behavior not specified here returns `MFOS_ERR_SPEC_GAP`.

## 7. SVC ABI

### 7.1 SVC Call Categories

```text
SVC_HANDLE
SVC_MEMORY
SVC_IPC
SVC_SERVICE
SVC_DATASET_GATEWAY
SVC_CATALOG_GATEWAY
SVC_SPOOL_GATEWAY
SVC_JOB_GATEWAY
SVC_OPERATOR_GATEWAY
SVC_AUDIT_GATEWAY
SVC_SECURITY_GATEWAY
SVC_AMF_GATEWAY
SVC_UPDATE_GATEWAY
SVC_PARTITION_GATEWAY
SVC_DIAGNOSTIC
```

Gateway calls pass typed requests to owning services. The nucleus validates framing, identity, handles, and bounded buffers; it does not own the business policy.

### 7.2 SVC Frame

```yaml
SVCFrameV1:
  abi_version: svc-v1
  call_id: uint32
  call_category: string
  flags: uint64
  caller_sequence: uint64
  correlation_id: uuid
  caller_context:
    subject: SubjectRef
    job: JobRef?
    program_identity: ProgramIdentityRef?
    execution_state: ExecutionState
    partition_id: uint64
  input:
    request_type: string
    request_buffer: UserBufferRef | SealedBufferRef | null
    request_len: uint64
    handles:
      - TypedHandle
  output:
    response_buffer: UserBufferRef | SealedBufferRef | null
    response_len: uint64
  audit:
    audit_obligation: AuditObligationRef?
    audit_required: bool
  reserved_zero:
    - uint64
    - uint64
```

Implementation note: `caller_context` in the in-memory frame is populated by the nucleus. Callers must not provide authoritative values for subject, job, program identity, execution state, or partition.

### 7.3 SVC Result

```yaml
SVCResultV1:
  abi_version: svc-v1
  status: MFOS_OK | MFOS_ERR_*
  reason_code: string
  caller_sequence: uint64
  correlation_id: uuid
  output_len: uint64
  returned_handles:
    - TypedHandle
  audit_record_id: uuid?
  obligations_completed:
    - string
  reserved_zero:
    - uint64
    - uint64
```

### 7.4 SVC Dispatch Rules

- The nucleus validates ABI version, call ID, category, flags, lengths, handles, and reserved fields.
- The nucleus derives caller identity from execution context.
- The nucleus validates user buffers before copying.
- The nucleus performs copy-in into kernel-owned bounded buffers.
- The nucleus routes service-owned requests through PCALL or service gateway.
- The nucleus propagates audit obligations.
- The nucleus returns typed errors.
- The nucleus must not fabricate success when a downstream service is unavailable.

### 7.5 SVC Error Mapping

| Condition | Error |
| --- | --- |
| Unknown ABI major version | `MFOS_ERR_UNSUPPORTED` |
| Unknown required flag | `MFOS_ERR_UNSUPPORTED` |
| Reserved field nonzero | `MFOS_ERR_INVALID_PARAMETER` |
| Undefined call ID | `MFOS_ERR_SPEC_GAP` |
| Specified but unimplemented call ID | `MFOS_ERR_UNSUPPORTED` |
| Bad user buffer | `MFOS_ERR_INVALID_PARAMETER` |
| Copy length overflow | `MFOS_ERR_INVALID_PARAMETER` |
| Stale handle | `MFOS_ERR_STALE_HANDLE` |
| Wrong handle type | `MFOS_ERR_INVALID_PARAMETER` |
| Insufficient rights | `MFOS_ERR_UNAUTHORIZED` |
| Policy deny | `MFOS_ERR_POLICY_DENIED` |
| Audit required but unavailable | `MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE` |

## 8. PCALL ABI and Endpoint Manifest

### 8.1 PCALL Purpose

PCALL is a typed synchronous service call. It replaces arbitrary cross-address-space pointer access with explicit endpoint, request, buffer, identity, policy, and audit fields.

PCALL supports:

- trusted service to trusted service calls.
- nucleus-mediated user request to trusted service endpoint.
- authorized service endpoint calls under AMF authority.
- securityd and auditd obligation propagation.

PCALL does not support arbitrary direct access to caller address space.

### 8.2 PCALL Endpoint Manifest

```yaml
PCALLEndpointManifest:
  manifest_version: 1
  endpoint_id: string
  service_id: string
  abi_version: pcall-v1
  request_type: string
  response_type: string
  allowed_callers:
    - execution_state: USER_JOB | USER_SUBSYSTEM | TRUSTED_SERVICE | AUTHORIZED_SERVICE | SUPERVISOR
      service_id: string?
      authority_class: string?
  required_authorization:
    securityd: bool
    authority_class: string?
    resource_type: string?
    operation: string?
  audit:
    audit_required: bool
    audit_class: string
  buffer_policy:
    max_request_len: uint64
    max_response_len: uint64
    sealed_buffer_required: bool
    allow_user_buffer: false
  failure_policy:
    fail_closed: true
  source_matrix_refs:
    - EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
    - EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001
```

### 8.3 PCALL Request

```yaml
PCALLRequestV1:
  abi_version: pcall-v1
  endpoint_id: string
  caller_sequence: uint64
  correlation_id: uuid
  caller_context:
    subject: SubjectRef
    job: JobRef?
    program_identity: ProgramIdentityRef?
    execution_state: ExecutionState
    partition_id: uint64
    service_id: string?
    authority_class: string?
  policy_version: uint64
  request_type: string
  request_buffer: SealedBufferRef
  request_len: uint64
  handles:
    - TypedHandle
  audit_obligation: AuditObligationRef?
  reserved_zero:
    - uint64
    - uint64
```

### 8.4 PCALL Response

```yaml
PCALLResponseV1:
  abi_version: pcall-v1
  status: MFOS_OK | MFOS_ERR_*
  reason_code: string
  endpoint_id: string
  caller_sequence: uint64
  correlation_id: uuid
  response_type: string
  response_buffer: SealedBufferRef?
  response_len: uint64
  returned_handles:
    - TypedHandle
  audit_record_id: uuid?
  obligations_completed:
    - string
  reserved_zero:
    - uint64
    - uint64
```

### 8.5 PCALL Rules

- Endpoint must exist and be active.
- Endpoint manifest must match request ABI, request type, caller class, and buffer policy.
- The nucleus or service runtime must derive caller context; caller-supplied identity is not authoritative.
- PCALL payloads are sealed bounded buffers.
- securityd is final PDP when endpoint manifest requires authorization.
- audit obligations must be completed or explicitly carried forward.
- Downstream failure must not be converted to success.
- Endpoint implementations must return typed errors.

## 9. Typed Handles and Buffers

### 9.1 TypedHandleRef

```yaml
TypedHandleRef:
  handle_id: uint64
  object_type: string
  generation: uint64
  required_rights:
    - string
```

Validation checks:

- handle exists.
- generation matches current object.
- object type matches expected type.
- subject is allowed to use the handle.
- rights cover operation.
- expiry has not passed.
- policy version constraints hold.

### 9.2 SealedBuffer

```yaml
SealedBuffer:
  buffer_id: uint64
  owner_subject: SubjectRef
  max_len: uint64
  actual_len: uint64
  direction: request | response | bidirectional
  generation: uint64
  integrity_tag: sha384?
```

Rules:

- `actual_len <= max_len`.
- Overflow rejects the call.
- Direction mismatch rejects the call.
- Stale buffer generation rejects the call.
- Sealed buffers cannot be reinterpreted as executable mappings.

## 10. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-SVC-0001 | SVC ABI must be versioned. | ABI test |
| MFOS-REQ-SVC-0002 | SVC caller identity must be derived from nucleus context. | negative test |
| MFOS-REQ-SVC-0003 | SVC must validate call ID, category, flags, lengths, handles, and reserved fields before dispatch. | ABI test |
| MFOS-REQ-SVC-0004 | SVC must use bounded copy-in/copy-out for user buffers. | negative test |
| MFOS-REQ-SVC-0005 | SVC must distinguish unsupported specified calls from spec gaps. | error test |
| MFOS-REQ-SVC-0006 | SVC must not return success when a required downstream service fails. | no-fake-success CI |
| MFOS-REQ-SVC-0007 | SVC gateway calls must not implement final protected-resource authorization in the nucleus. | architecture review |
| MFOS-REQ-SVC-0008 | SVC must propagate audit obligations. | audit test |
| MFOS-REQ-SVC-0009 | SVC must reject stale, wrong-type, or rights-insufficient handles. | negative test |
| MFOS-REQ-SVC-0010 | SVC must zero or reject reserved fields according to ABI rules. | fuzz test |
| MFOS-REQ-PCALL-0001 | PCALL ABI must be versioned. | ABI test |
| MFOS-REQ-PCALL-0002 | PCALL endpoints must be declared in endpoint manifests. | manifest test |
| MFOS-REQ-PCALL-0003 | PCALL must use typed endpoints and typed request/response schemas. | interface test |
| MFOS-REQ-PCALL-0004 | PCALL must not allow arbitrary cross-address-space pointer access. | negative test |
| MFOS-REQ-PCALL-0005 | PCALL caller identity must be derived from trusted context. | negative test |
| MFOS-REQ-PCALL-0006 | PCALL must call securityd when endpoint manifest requires authorization. | integration test |
| MFOS-REQ-PCALL-0007 | PCALL must propagate audit obligations and record endpoint failures. | audit test |
| MFOS-REQ-PCALL-0008 | PCALL must reject sealed buffer overflow, direction mismatch, and stale generation. | negative test |
| MFOS-REQ-PCALL-0009 | PCALL endpoint failure must return typed error and not fake success. | no-fake-success CI |
| MFOS-REQ-PCALL-0010 | PCALL endpoint registration by AMF module must be constrained by AMF authority class. | AMF integration test |

## 11. Invariants

```text
INV-SVC-001:
  SVC caller subject, job, program identity, execution state, and partition
  are derived from nucleus context and cannot be supplied authoritatively by
  caller-controlled memory.

INV-SVC-002:
  No SVC dispatch occurs until ABI version, call ID, flags, reserved fields,
  lengths, buffers, and handles validate.

INV-SVC-003:
  SVC must never dereference user pointers without bounded copy-in/copy-out.

INV-SVC-004:
  A protected resource gateway SVC cannot return a usable handle unless the
  owning service has a valid securityd ALLOW or ALLOW_WITH_AUDIT decision.

INV-PCALL-001:
  PCALL endpoint invocation is valid only when endpoint manifest, caller
  execution state, request type, buffer policy, handle rights, policy version,
  and audit obligations match.

INV-PCALL-002:
  PCALL does not grant arbitrary cross-address-space pointer access.

INV-PCALL-003:
  Endpoint failure, authorization denial, or audit failure cannot be converted
  to MFOS_OK.

INV-PCALL-004:
  AMF-registered endpoints are callable only within the module's declared
  authority class.
```

## 12. Audit Obligations

SVC audit obligations:

- Unknown security-sensitive call.
- Protected-resource gateway call.
- Stale handle rejection for protected object.
- Rights denial.
- Downstream securityd deny.
- Audit-required downstream failure.
- Operator command gateway call.
- AMF load gateway call.
- Update activation gateway call.

PCALL audit obligations:

- Endpoint registration.
- Endpoint invocation when manifest requires audit.
- Endpoint authorization deny.
- Endpoint buffer validation failure for security-sensitive endpoint.
- Endpoint implementation failure for security-sensitive endpoint.
- Endpoint returning handle to caller.
- AMF endpoint authority mismatch.

Audit payload:

```yaml
SvcPcallAuditEvent:
  schema_version: uint16
  component_id: nucleus | service_runtime
  interface: SVC | PCALL
  call_id: uint32?
  endpoint_id: string?
  subject: SubjectRef
  job: JobRef?
  program_identity: ProgramIdentityRef?
  operation: string
  decision: string
  reason_code: string
  policy_version: uint64?
  correlation_id: uuid
  caller_sequence: uint64
  partition_id: uint64
  returned_handle_types:
    - string
  previous_hash: sha384?
```

## 13. Failure Modes

| Failure | Required behavior |
| --- | --- |
| ABI major mismatch | `MFOS_ERR_UNSUPPORTED` |
| Unknown required flag | `MFOS_ERR_UNSUPPORTED` |
| Reserved field nonzero | `MFOS_ERR_INVALID_PARAMETER` |
| Undefined call/endpoint | `MFOS_ERR_SPEC_GAP` |
| Specified but unimplemented call/endpoint | `MFOS_ERR_UNSUPPORTED` |
| Caller identity mismatch attempt | ignore caller field; audit and deny if tampering detected |
| Buffer length overflow | `MFOS_ERR_INVALID_PARAMETER` |
| User buffer invalid | `MFOS_ERR_INVALID_PARAMETER` |
| Stale handle | `MFOS_ERR_STALE_HANDLE` |
| Wrong handle type | `MFOS_ERR_INVALID_PARAMETER` |
| Insufficient handle rights | `MFOS_ERR_UNAUTHORIZED` |
| Endpoint inactive | `MFOS_ERR_UNSUPPORTED` or service-specific unavailable error |
| securityd unavailable for protected call | fail closed |
| auditd unavailable for audit-required call | `MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE` |
| Endpoint panic/fault | contain fault, revoke generation-scoped outputs, audit |
| Downstream service timeout | typed timeout error; no fake success |

## 14. Positive Tests

- `svc_valid_version_dispatches_known_call`.
- `svc_derives_caller_identity_from_context`.
- `svc_copy_in_bounded_request_succeeds`.
- `svc_gateway_routes_to_datasetd`.
- `svc_gateway_propagates_audit_obligation`.
- `svc_returns_unsupported_for_specified_unimplemented_call`.
- `pcall_valid_endpoint_invocation_succeeds`.
- `pcall_securityd_authorized_endpoint_succeeds`.
- `pcall_returns_typed_handle_after_authorized_decision`.
- `pcall_audit_required_invocation_records_event`.
- `pcall_amf_endpoint_with_matching_authority_succeeds`.

## 15. Negative Tests

- `svc_rejects_unknown_abi_major`.
- `svc_rejects_unknown_required_flag`.
- `svc_rejects_nonzero_reserved_field`.
- `svc_rejects_undefined_call_as_spec_gap`.
- `svc_rejects_bad_user_buffer`.
- `svc_rejects_copy_length_overflow`.
- `svc_rejects_caller_supplied_identity`.
- `svc_rejects_stale_handle`.
- `svc_rejects_wrong_type_handle`.
- `svc_rejects_rights_insufficient_handle`.
- `svc_fails_closed_when_securityd_unavailable`.
- `svc_fails_when_audit_required_but_unavailable`.
- `svc_does_not_authorize_dataset_access_in_nucleus`.
- `pcall_rejects_unknown_endpoint`.
- `pcall_rejects_manifest_request_type_mismatch`.
- `pcall_rejects_caller_execution_state_mismatch`.
- `pcall_rejects_arbitrary_pointer_payload`.
- `pcall_rejects_buffer_overflow`.
- `pcall_rejects_buffer_direction_mismatch`.
- `pcall_rejects_stale_buffer_generation`.
- `pcall_rejects_securityd_denial`.
- `pcall_rejects_audit_required_but_unavailable`.
- `pcall_rejects_amf_authority_mismatch`.
- `pcall_endpoint_fault_does_not_return_success`.

## 16. Fuzz Targets

- `fuzz_svc_frame_v1`.
- `fuzz_svc_flags`.
- `fuzz_svc_reserved_fields`.
- `fuzz_svc_call_id_dispatch`.
- `fuzz_svc_handle_vector`.
- `fuzz_svc_buffer_lengths`.
- `fuzz_pcall_endpoint_manifest`.
- `fuzz_pcall_request_v1`.
- `fuzz_pcall_response_v1`.
- `fuzz_pcall_buffer_policy`.
- `fuzz_typed_handle_ref`.
- `fuzz_sealed_buffer`.
- `fuzz_error_mapping`.

Fuzz harnesses must assert that malformed frames never return `MFOS_OK`.

## 17. Conformance Profiles

### Baseline

- SVC and PCALL versioning required.
- typed handles required.
- bounded copy-in/copy-out required.
- audit obligation propagation required.
- securityd mediation for protected resource gateways required.
- implicit single partition accepted.

### Enterprise-Standalone

- measured service endpoint manifests required.
- endpoint registration audit required.
- remote audit export through auditd required.
- SVC/PCALL ABI conformance report required for release.
- PXM calls unavailable except the implicit single-partition status surface.

### Enterprise-PXM

- measured service endpoint manifests required.
- endpoint registration audit required.
- remote audit export through auditd required.
- SVC/PCALL ABI conformance report required for release.
- PXM CALL ABI available for partition lifecycle operations.
- device assignment calls allowed only after PXM teardown evidence exists.

### High-Assurance

- Guard calls are separate from normal SVC/PCALL fast path.
- Guard approval required for selected root-object transitions.
- AMF endpoint registry may require Guard seal.
- SVC table integrity may require Guard verification.
- Endpoint manifest roots may require Guard seal.

## 18. SVC Table Integrity

SVC table entry:

```yaml
SVCTableEntry:
  call_id: uint32
  call_category: string
  abi_version: svc-v1
  handler_id: string
  implemented: bool
  status: active | unsupported | reserved | deprecated
  required_execution_state:
    - USER_JOB
    - USER_SUBSYSTEM
    - TRUSTED_SERVICE
    - AUTHORIZED_SERVICE
  audit_required: bool
  source_matrix_refs:
    - EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
```

Rules:

- Reserved entries must not return success.
- Deprecated entries must have explicit behavior.
- Unimplemented specified entries return `MFOS_ERR_UNSUPPORTED`.
- Undefined entries return `MFOS_ERR_SPEC_GAP`.
- High-Assurance profile may require Guard verification of SVC table digest.

## 19. Evidence Artifacts

Implementations must produce:

- SVC ABI conformance report.
- PCALL ABI conformance report.
- SVC table digest report.
- Endpoint manifest registry report.
- typed-handle validation test report.
- buffer validation fuzz report.
- securityd propagation integration report.
- audit obligation propagation report.
- no-fake-success report.
- AMF endpoint authority integration report.
- Guard SVC table verification report for High-Assurance.

## 20. Spec Gaps

- Numeric call ID allocation table is not yet fixed.
- Concrete binary frame layout and alignment rules are not fixed.
- Endianness is expected to be little-endian on x86_64 but the canonical encoding is not fixed.
- Timeout and cancellation semantics need a separate section.
- Async service calls are out of scope.
- Shared-memory bulk transfer is out of scope until a sealed shared-buffer model is specified.
- Detailed PCALL endpoint schema language is not fixed.
- Service runtime implementation is not specified here.
- Guard CALL ABI is referenced but remains in the Guard spec.
- Formal model for caller sequence replay protection is not yet written.

## 21. Inactive Future Implementation Prompt Template

Phase status: inactive future template. This section does not authorize production implementation, hosted daemon implementation, or portable semantic-core implementation.

```text
Future authorized implementation agents would implement MFOS SVC and PCALL ABI.

Implement only the requirement IDs listed in the task. Do not claim z/OS
SVC, PC, cross-memory, assembler-services, or binary compatibility.

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

Rules:
- Derive caller identity from trusted nucleus/service context.
- Never trust caller-supplied identity.
- Use typed handles and sealed bounded buffers.
- Do not allow arbitrary cross-address-space pointer access.
- Use securityd for protected-resource authorization.
- Propagate audit obligations and record denials.
- Return MFOS_ERR_UNSUPPORTED for specified but unimplemented features.
- Return MFOS_ERR_SPEC_GAP for undefined behavior.
- Do not return success for malformed, denied, unsupported, or undefined calls.
- Add negative tests and fuzz targets with ABI parser or dispatcher code.
```
