---
spec_id: "MFOS-SPEC-14-NUCLEUS"
title: "MFOS Nucleus Specification v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001", "EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001", "EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001", "EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001", "NIST-160-001", "TCG-001", "X64-AMD-001", "X64-INTEL-001", "X64-LINUX-CET-001", "X64-LINUX-PKU-001"]
requirement_refs: ["MFOS-REQ-NUCLEUS-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Nucleus Specification v0.1

Status: Draft  
Owner: MFOS architecture  
Profile applicability: Baseline, Enterprise-Standalone, Enterprise-PXM, High-Assurance  
Source basis: user-provided MFOS Source-Grounded High-Assurance Architecture v0.3

## 1. Purpose

This document specifies the MFOS nucleus.

The nucleus provides the smallest privileged execution core needed to run MFOS services, enforce address-space isolation, expose typed system interfaces, enforce baseline memory protection, launch trusted services, propagate identity and audit obligations, and contain faults.

MFOS is z/OS-inspired in enterprise semantics, but the nucleus is not a z/Architecture emulator and does not claim z/OS kernel, MVS, SVC, PC, or assembler-services compatibility.

## 2. Scope

The nucleus covers:

- Boot handoff and minimal initialization.
- Address spaces and page-table management.
- Baseline scheduler.
- SVC entry and dispatch.
- Typed object handles.
- Copy-in/copy-out.
- IPC and PCALL transport primitives.
- Service lifecycle supervision.
- NX/W^X enforcement.
- SMEP/SMAP/CET use where profile and hardware support allow.
- Fault containment and crash dump trigger.
- Kernel audit hooks.
- Partition-aware API surface.
- Failure modes, tests, negative tests, fuzz targets, and open spec gaps.

## 3. Non-Objectives

The nucleus must not own:

- RACF-like policy decision.
- Dataset semantics.
- Catalog semantics.
- Spool formatting.
- Job scheduling policy.
- workload policy.
- AMF policy semantics.
- Update policy semantics.
- Operator business command semantics.
- Desktop stack.
- Broad third-party driver ecosystem.
- POSIX-first filesystem model.
- Linux syscall compatibility.

The nucleus may enforce object isolation and typed handles, but securityd remains the central policy decision point for protected resource access.

## 4. Source Matrix References

Required source IDs for this spec:

- EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001: system integrity concept.
- EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001: storage-domain inspiration and divergence.
- EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001: storage protection reference for conceptual mapping only.
- EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001: cross-memory communication concept inspiration.
- EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001: cross-memory security concern inspiration.
- X64-INTEL-001: x64 system programming, paging, protection, VMX, MSR, CET, PKU/PKS reality.
- X64-AMD-001: AMD64 system programming, paging, SVM/NPT reality.
- X64-LINUX-PKU-001: PKU limitations; data access only and not instruction fetch.
- X64-LINUX-CET-001: CET shadow stack and IBT reference.
- TCG-001: measured boot interaction.
- NIST-160-001: secure system engineering.
- FBVBS-001: state-machine, traceability, no-fake-success, and partition discipline.

## 5. Design Position

The nucleus is a privileged object and execution manager. It is not the enterprise policy brain.

```text
nucleus owns:
  CPU entry and trap handling
  address spaces
  page tables
  typed handles
  copy-in/copy-out
  SVC dispatch
  IPC transport
  service lifecycle
  fault containment
  minimum scheduler
  memory protection primitives

nucleus does not own:
  final authorization for protected resources
  dataset or catalog policy
  job semantics
  spool semantics
  operator command policy
  AMF governance policy
  update governance policy
```

## 6. Execution States

```text
USER_JOB
USER_SUBSYSTEM
TRUSTED_SERVICE
AUTHORIZED_SERVICE
SUPERVISOR
GUARD
PM_ROOT
```

Rules:

- `USER_JOB` and `USER_SUBSYSTEM` cannot directly access supervisor memory.
- `TRUSTED_SERVICE` can receive PCALL requests through typed endpoints only.
- `AUTHORIZED_SERVICE` can use selected privileged interfaces when approved by securityd and registered policy.
- `SUPERVISOR` is nucleus execution.
- `GUARD` is outside baseline nucleus authority and exists only in High-Assurance profile.
- `PM_ROOT` belongs to PXM and must not be conflated with MFOS supervisor.

## 7. Storage Domains

```text
USER_PRIVATE
JOB_SHARED
SERVICE_PRIVATE
SECURITY_ROOT
AUDIT_ROOT
CATALOG_ROOT
SPOOL_ROOT
NUCLEUS_TEXT
NUCLEUS_DATA
DEVICE_DMA
PARTITION_METADATA
```

Rules:

- Storage domains are MFOS software-defined policy categories, not x64 storage keys.
- PKU/PKS may assist compartments but must not be the primary system-integrity boundary.
- Instruction fetch protection must rely on page permissions, NX, W^X, and profile-specific controls, not PKU.
- High-Assurance root protection belongs to PXM Guard, not Baseline nucleus.

## 8. Nucleus Object Model and Manifest

### 8.1 KernelObject

```yaml
KernelObject:
  object_id: uint64
  object_type: address_space | thread | process | service | endpoint | buffer | mapping | device_ref | partition_ref | audit_hook
  owner_subject: SubjectRef
  owning_partition: PartitionRef
  generation: uint64
  rights_mask: uint64
  policy_version: uint64?
  audit_obligation: AuditObligationRef?
  state: active | quiesced | revoked | faulted | destroyed
```

### 8.2 TypedHandle

```yaml
TypedHandle:
  handle_id: uint64
  object_id: uint64
  object_type: string
  generation: uint64
  rights:
    - read
    - write
    - execute
    - map
    - send
    - receive
    - manage
  subject: SubjectRef
  expiry: timestamp?
  policy_version: uint64?
  catalog_generation: uint64?
  sealed: bool
```

### 8.3 AddressSpace

```yaml
AddressSpace:
  address_space_id: uint64
  owner_subject: SubjectRef
  execution_state: ExecutionState
  mappings:
    - MappingRef
  allowed_storage_domains:
    - StorageDomain
  partition_id: uint64
  measurement_context: sha384?
```

### 8.4 Service

```yaml
Service:
  service_id: string
  component_id: string
  execution_state: TRUSTED_SERVICE | AUTHORIZED_SERVICE
  address_space: AddressSpaceRef
  endpoints:
    - EndpointRef
  manifest_digest: sha384
  policy_version: uint64
  status: defined | loaded | starting | running | degraded | quiesced | faulted | stopped
  restart_policy: never | on_failure | operator_only
```

### 8.5 NucleusManifest

```yaml
NucleusManifest:
  manifest_version: 1
  component_id: nucleus
  component_version: semver
  target_arch: x86_64
  target_vendor: intel | amd | any
  required_cpu_features:
    - nx
  optional_cpu_features:
    - smep
    - smap
    - cet
    - pku
    - pks
    - iommu
  profile_applicability:
    - Baseline
    - Enterprise-Standalone
    - Enterprise-PXM
    - High-Assurance
  boot_protocol_version: string
  svc_abi_version: string
  pcall_abi_version: string
  hash:
    algorithm: sha384
    value: hex
  size: uint64
  generation: uint64
  security_epoch: uint64
  source_matrix_refs:
    - EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
    - X64-INTEL-001
    - X64-AMD-001
```

## 9. Boot / IPL State Machine

```text
POWER_ON
  -> FIRMWARE_INIT
  -> SECURE_BOOT_VERIFY
  -> MEASURE_BOOT_CHAIN
  -> PXM_LOAD              [Enterprise-PXM/High-Assurance]
  -> PXM_MEASURE           [Enterprise-PXM/High-Assurance]
  -> GUARD_INIT            [High-Assurance]
  -> MFOS_LOAD
  -> MFOS_NUCLEUS_INIT
  -> SERVICE_START_AUDITD
  -> SERVICE_START_SECURITYD
  -> SERVICE_START_CATALOGD
  -> SERVICE_START_DATASETD
  -> SERVICE_START_SPOOLD
  -> SERVICE_START_JOBD
  -> SERVICE_START_OPERATORD
  -> OPERATOR_READY
```

Failure rules:

- auditd start failure:
  - Baseline: operator recovery mode only; no job submit, normal dataset open, policy update, AMF load, or update activation.
  - Enterprise-Standalone: operator recovery mode only unless recovery policy proves required audit sink availability.
  - Enterprise-PXM: operator recovery mode only unless PXM boot audit sink can be reconciled.
  - High-Assurance: boot stops or enters recovery mode.
- securityd start failure:
  - All profiles: operator recovery mode only.
- Guard required but unavailable:
  - High-Assurance: boot denied.

## 10. Service Lifecycle State Machine

```text
DEFINED
  -> MEASURED
  -> LOADED
  -> STARTING
  -> RUNNING
  -> QUIESCED
  -> STOPPED
```

Failure states:

```text
MEASUREMENT_FAILED
LOAD_DENIED
START_FAILED
SERVICE_FAULTED
AUDIT_REQUIRED_BUT_UNAVAILABLE
SECURITYD_UNAVAILABLE
UNSUPPORTED
SPEC_GAP
```

Service restart must not hide security-sensitive failures. A restarted service must receive a new generation and audit record.

## 11. Nucleus ABIs

### 11.1 Boot Handoff ABI

```yaml
BootHandoff:
  boot_protocol_version: string
  firmware_measurement_log: bytes?
  memory_map: MemoryMap
  initrd_ref: ArtifactRef?
  activation_profile_ref: ArtifactRef
  command_line: string?
  profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  pxm_present: bool
  guard_required: bool
```

Rules:

- Unknown boot protocol version returns boot failure.
- Missing activation profile returns `MFOS_ERR_INVALID_PARAMETER`.
- High-Assurance with `guard_required = true` and no Guard returns `MFOS_ERR_GUARD_REQUIRED`.

### 11.2 SVC Entry ABI

SVC is specified in [15-svc-pcall.md](15-svc-pcall.md). The nucleus owns the CPU trap/entry path and dispatch validation. It must not implement resource policy outside required mediation hooks.

### 11.3 PCALL Transport ABI

PCALL is specified in [15-svc-pcall.md](15-svc-pcall.md). The nucleus owns endpoint transport, bounded transfer, identity propagation, and failure isolation.

### 11.4 IPC Primitive

```yaml
IPCMessage:
  abi_version: ipc-v1
  sender_subject: SubjectRef
  sender_execution_state: ExecutionState
  endpoint_id: uint64
  correlation_id: uuid
  payload_buffer: SealedBufferRef
  payload_len: uint64
  audit_obligation: AuditObligationRef?
```

IPC must use bounded buffers. The nucleus must reject payload length overflow and stale endpoint handles.

### 11.5 Copy-In/Copy-Out ABI

```yaml
CopyRequest:
  source_address_space: AddressSpaceRef
  target_address_space: AddressSpaceRef
  source_buffer: UserBufferRef | SealedBufferRef
  target_buffer: KernelBufferRef | UserBufferRef | SealedBufferRef
  length: uint64
  direction: copy_in | copy_out | copy_between
  correlation_id: uuid
```

Rules:

- User pointers are never directly dereferenced by supervisor code.
- All copy operations are bounded.
- Failed validation returns typed error.
- Partial copy semantics must be explicit; default is fail without partial commit.

## 12. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-NUCLEUS-0001 | Nucleus must implement boot handoff validation. | boot test |
| MFOS-REQ-NUCLEUS-0002 | Nucleus must maintain address spaces with user/supervisor separation. | isolation test |
| MFOS-REQ-NUCLEUS-0003 | Nucleus must implement SVC entry and dispatch validation. | ABI test |
| MFOS-REQ-NUCLEUS-0004 | Nucleus must implement typed object handles. | handle test |
| MFOS-REQ-NUCLEUS-0005 | Nucleus must implement IPC primitive with bounded payloads. | IPC test |
| MFOS-REQ-NUCLEUS-0006 | Nucleus must implement baseline scheduler sufficient for services and jobs. | scheduler test |
| MFOS-REQ-NUCLEUS-0007 | Nucleus must manage page tables and mapping rights. | mapping test |
| MFOS-REQ-NUCLEUS-0008 | Nucleus must enforce NX and W^X. | W^X test |
| MFOS-REQ-NUCLEUS-0009 | Nucleus must use copy-in/copy-out for untrusted buffers. | negative test |
| MFOS-REQ-NUCLEUS-0010 | Nucleus must implement service lifecycle supervision. | integration test |
| MFOS-REQ-NUCLEUS-0011 | Nucleus must contain service faults and produce fault records. | fault injection |
| MFOS-REQ-NUCLEUS-0012 | Nucleus must expose kernel audit hooks without replacing auditd. | audit test |
| MFOS-REQ-NUCLEUS-0013 | Nucleus must trigger crash dump on unrecoverable internal corruption. | crash test |
| MFOS-REQ-NUCLEUS-0014 | Nucleus must expose partition-aware APIs even in implicit single partition mode. | API test |
| MFOS-REQ-NUCLEUS-0015 | Nucleus must not decide final protected-resource authorization. | architecture review |
| MFOS-REQ-NUCLEUS-0016 | Nucleus must return `MFOS_ERR_UNSUPPORTED` for specified but unimplemented SVCs. | no-fake-success CI |
| MFOS-REQ-NUCLEUS-0017 | Nucleus must return `MFOS_ERR_SPEC_GAP` for undefined SVCs or ABIs. | no-fake-success CI |
| MFOS-REQ-NUCLEUS-0018 | Nucleus must reject stale, wrong-type, wrong-generation, or rights-insufficient handles. | negative test |
| MFOS-REQ-NUCLEUS-0019 | Nucleus must not treat PKU/PKS as primary system-integrity boundary. | design review |
| MFOS-REQ-NUCLEUS-0020 | Nucleus must not map writable executable pages. | mapping negative test |

## 13. Invariants

```text
INV-NUC-001:
  Supervisor code must not directly dereference user-controlled pointers.

INV-NUC-002:
  A typed handle is valid only when object_id, object_type, generation,
  rights, subject, and policy_version constraints match the current object.

INV-NUC-003:
  A user job cannot obtain a protected resource handle unless the owning
  service received a securityd ALLOW or ALLOW_WITH_AUDIT decision.

INV-NUC-004:
  No mapping may be writable and executable at the same time.

INV-NUC-005:
  Unsupported nucleus calls must not return success.

INV-NUC-006:
  Undefined nucleus behavior must be surfaced as SPEC_GAP, not invented.

INV-NUC-007:
  Implicit single partition mode must use the same partition-aware API
  shape as PXM-backed mode.

INV-NUC-008:
  A service crash must not silently preserve stale handles from the crashed
  service generation.
```

## 14. Security and Audit Obligations

Nucleus must emit or request audit records for:

- Boot handoff acceptance or failure.
- Service start, stop, restart, crash, and generation change.
- SVC dispatch failure for security-sensitive interfaces.
- PCALL endpoint registration and failure.
- Stale handle rejection.
- W^X violation attempt.
- Copy-in/copy-out validation failure for protected operations.
- Crash dump trigger.
- Partition-aware API operation.

Nucleus audit hook payload:

```yaml
NucleusAuditEvent:
  schema_version: uint16
  component_id: nucleus
  event_type: string
  subject: SubjectRef?
  object: ObjectRef?
  operation: string
  decision: string
  reason_code: string
  policy_version: uint64?
  partition_id: uint64
  execution_state: ExecutionState
  correlation_id: uuid
  previous_hash: sha384?
```

The nucleus may buffer early boot audit events until auditd is available, but buffer overflow and flush failure must follow profile-specific failure policy.

## 15. Failure Modes

| Failure | Required behavior |
| --- | --- |
| Invalid boot handoff | Boot stop or recovery mode. |
| Missing activation profile | Return boot error; do not invent defaults. |
| Unsupported CPU feature required by profile | Return `MFOS_ERR_UNSUPPORTED`; boot denied for that profile. |
| User pointer validation failure | Return `MFOS_ERR_INVALID_PARAMETER`; audit when security-sensitive. |
| Stale handle | Return `MFOS_ERR_STALE_HANDLE`; audit when protected object. |
| Wrong handle type | Return `MFOS_ERR_INVALID_PARAMETER`; no operation. |
| Insufficient handle rights | Return `MFOS_ERR_UNAUTHORIZED`; audit. |
| W^X violation | Return `MFOS_ERR_POLICY_DENIED`; audit. |
| SVC unknown but specified future ID | Return `MFOS_ERR_UNSUPPORTED`. |
| SVC undefined | Return `MFOS_ERR_SPEC_GAP`. |
| auditd unavailable | Apply profile failure policy. |
| securityd unavailable | Protected operations fail closed; operator recovery only. |
| service crash | Revoke service-generation handles; audit; apply restart policy. |
| internal corruption | Trigger crash dump or panic-equivalent; audit if possible. |

## 16. Positive Tests

- `nucleus_boot_valid_handoff_succeeds`.
- `nucleus_creates_user_address_space`.
- `nucleus_enforces_user_supervisor_separation`.
- `nucleus_creates_typed_handle`.
- `nucleus_validates_handle_generation`.
- `nucleus_svc_dispatch_known_call`.
- `nucleus_copy_in_bounded_buffer_succeeds`.
- `nucleus_ipc_bounded_message_succeeds`.
- `nucleus_service_start_records_generation`.
- `nucleus_wx_enforcement_allows_rx_after_verify`.
- `nucleus_implicit_partition_api_reports_partition`.

## 17. Negative Tests

- `nucleus_rejects_invalid_boot_protocol`.
- `nucleus_rejects_missing_activation_profile`.
- `nucleus_rejects_user_pointer_deref_path`.
- `nucleus_rejects_copy_len_overflow`.
- `nucleus_rejects_stale_handle`.
- `nucleus_rejects_wrong_type_handle`.
- `nucleus_rejects_rights_insufficient_handle`.
- `nucleus_rejects_writable_executable_mapping`.
- `nucleus_rejects_unknown_undefined_svc_as_spec_gap`.
- `nucleus_rejects_unimplemented_specified_svc_as_unsupported`.
- `nucleus_revokes_handles_after_service_crash`.
- `nucleus_protected_operation_fails_when_securityd_unavailable`.
- `nucleus_security_operation_fails_when_audit_required_but_unavailable`.
- `nucleus_does_not_authorize_dataset_access_locally`.

## 18. Fuzz Targets

- `fuzz_boot_handoff`.
- `fuzz_memory_map_parser`.
- `fuzz_activation_profile_ref`.
- `fuzz_svc_frame_decoder`.
- `fuzz_pcall_frame_decoder`.
- `fuzz_typed_handle_decoder`.
- `fuzz_ipc_message_decoder`.
- `fuzz_copy_request_validator`.
- `fuzz_service_manifest_decoder`.
- `fuzz_crash_dump_metadata`.

Fuzz targets must preserve the distinction between invalid parameter, unsupported feature, and spec gap.

## 19. Conformance Profiles

### Baseline

- NX/W^X required.
- securityd/auditd integration required.
- typed handles required.
- SVC and PCALL ABI validation required.
- Implicit single partition backend allowed.
- SMEP/SMAP/CET used when available but not required for conformance.

### Enterprise-Standalone

- Secure Boot and measured boot integration required.
- TPM measurement integration required where available.
- IOMMU required for platform DMA protection when claimed.
- SMEP/SMAP required where hardware supports profile claim.
- Remote audit export expected through auditd.
- PXM is not required and cross-partition device-assignment claims are prohibited.

### Enterprise-PXM

- All Enterprise-Standalone nucleus requirements apply.
- PXM load and measurement hooks are required for partition lifecycle claims.
- IOMMU and interrupt remapping are required for device assignment claims.
- Side-partition and passthrough claims require PXM evidence.

### High-Assurance

- PXM required.
- PXM Guard required.
- Guard failure denies boot.
- Guard protects selected roots, not ordinary nucleus policy.
- Nucleus/PXM/Guard evidence required for High-Assurance claim.
- CET may be profile-required on supported hardware.

## 20. Evidence Artifacts

Nucleus implementation must produce:

- Boot validation log.
- Memory-map validation report.
- Page-table mapping test report.
- W^X test report.
- typed-handle test report.
- copy-in/copy-out negative test report.
- SVC/PCALL ABI conformance report.
- Service lifecycle fault-injection report.
- Audit hook report.
- Partition-aware API report.
- CPU feature matrix report.

## 21. Spec Gaps

- Concrete boot protocol wire format is not fixed.
- Concrete scheduler policy is minimal and not fully specified.
- Exact page-table layout is implementation-specific and not fixed.
- Driver model is intentionally unspecified.
- Crash dump format is not fixed.
- Early boot audit buffer size and overflow policy need a profile-specific value.
- Service manifest format is referenced but not fully specified here.
- CPU feature policy per hardware generation is not fixed.
- Formal model for handle rights is not yet written.
- SMP and interrupt details are not fully specified here.

## 22. Inactive Future Implementation Prompt Template

Phase status: inactive future template. This section does not authorize production implementation, hosted daemon implementation, or portable semantic-core implementation.

```text
Future authorized implementation agents would implement the MFOS nucleus.

Implement only the requirement IDs listed in the task. Do not claim z/OS,
MVS, SVC, PC, APF, or z/Architecture compatibility.

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
- Keep nucleus small.
- Do not put dataset, catalog, spool, workload policy, AMF policy, or update policy
  semantics in the nucleus.
- Use typed handles and bounded copy-in/copy-out.
- Never dereference user pointers directly in supervisor code.
- Use securityd for final authorization of protected resources.
- Use auditd for security-sensitive events and failures.
- Enforce NX/W^X.
- Do not treat PKU/PKS as the primary system-integrity boundary.
- Return MFOS_ERR_UNSUPPORTED for specified but unimplemented features.
- Return MFOS_ERR_SPEC_GAP for undefined behavior.
- Add negative tests with implementation.
```
