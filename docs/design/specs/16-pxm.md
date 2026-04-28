---
spec_id: "MFOS-SPEC-16-PXM"
title: "MFOS Design Specification 16: PXM Partition Manager"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-Z-DPM-0001", "EXTREF-IBM-Z-LPAR-INTRODUCTION-0001", "NIST-160-001", "NIST-193-001", "TCG-001", "X64-AMD-001", "X64-INTEL-001"]
requirement_refs: ["MFOS-REQ-PARTITION-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Design Specification 16: PXM Partition Manager

Status: Draft v0.1

Audience: architecture agents, implementation agents, security reviewers, test engineers

This document defines the PXM Partition Manager for MFOS. PXM is a partition isolation and lifecycle layer. It is not the MFOS enterprise semantics layer, and it MUST NOT interpret jobs, datasets, catalogs, spool entries, security profiles, operator business commands, or workload policies.

MFOS is z/OS-inspired, not z/OS-compatible. PXM is IBM LPAR/DPM-inspired at the management concept level, but it is not an implementation of IBM PR/SM, IBM Z firmware, or z/Architecture.

## 1. Purpose

PXM provides a partition-aware execution model for MFOS and side partitions.

PXM exists to:

- Define partition lifecycle and activation semantics.
- Assign logical CPU, memory, device, IOMMU, and interrupt routing resources.
- Maintain isolation between MFOS, Linux/Desktop, service, and recovery partitions.
- Provide a common API for both early implicit single-partition execution and later full partition manager execution.
- Generate audit records for partition lifecycle and device assignment events.
- Support High-Assurance PXM Guard without forcing Guard semantics into Baseline or Enterprise builds.

PXM does not define MFOS job, dataset, catalog, spool, security, audit schema, AMF, update, or operator command semantics. Those remain inside the MFOS partition.

## 2. Scope

### 2.1 In Scope

- Partition object model.
- Activation profile schema.
- Partition lifecycle state machine.
- PXM call ABI.
- Logical CPU assignment.
- Memory domain assignment and zero-before-reuse requirements.
- IOMMU domain association.
- Interrupt remapping association.
- Device assignment and teardown sequencing.
- Partition audit obligations.
- Implicit single-partition backend for early phases.
- Full PXM backend for Enterprise-PXM and High-Assurance phases.
- Recovery partition coordination.

### 2.2 Out of Scope

- Dataset authorization.
- Catalog resolution.
- Spool browse, purge, or retention.
- Job scheduling and initiators.
- workload policy service class interpretation.
- RACF-like security profile interpretation.
- Operator business command interpretation.
- Linux syscall compatibility.
- Desktop compositor design.
- PXM Guard root-object policy. See [17-guard.md](17-guard.md).
- Linux/Desktop gateway policy. See [18-linux-gateway.md](18-linux-gateway.md).

## 3. Source Matrix References

| Source ID | Use |
| --- | --- |
| EXTREF-IBM-Z-LPAR-INTRODUCTION-0001 | Conceptual reference for logical partitions as logical machine images with assigned processor, storage, I/O, and activation profile concepts. |
| EXTREF-IBM-Z-DPM-0001 | Conceptual reference for object-oriented partition management plane patterns. |
| X64-INTEL-001 | x64 protection, VMX, EPT, MSR, interrupt, and IOMMU-relevant architecture reference. |
| X64-AMD-001 | AMD64 system programming, SVM, NPT, and platform control reference. |
| TCG-001 | Measured boot and TPM event log reference for partition image/profile measurement. |
| NIST-160-001 | Secure system engineering lifecycle reference. |
| NIST-193-001 | Firmware resiliency and recovery reference. |
| FBVBS-001 | Internal transfer source for partition state machine discipline, command page style, and evidence obligations. |

Any new PXM concept with an IBM-derived name MUST include an explicit semantic-overlap and divergence note in the source matrix before implementation.

## 4. Normative Language

The keywords MUST, MUST NOT, REQUIRED, SHOULD, SHOULD NOT, MAY, UNSUPPORTED, and SPEC_GAP are normative for this specification.

- MUST means required for the applicable conformance profile.
- SHOULD means strongly recommended; divergence requires an ADR and evidence.
- MAY means optional and not part of a guarantee unless a profile says otherwise.
- UNSUPPORTED means specified behavior that is not implemented in a given build and MUST fail closed.
- SPEC_GAP means behavior with no approved specification. It MUST NOT be implemented as a success path.

## 5. Profile Applicability

| Capability | Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance |
| --- | --- | --- | --- | --- |
| Partition-aware API | MUST | MUST | MUST | MUST |
| Implicit single-partition backend | MAY | MUST for non-PXM claim | MAY for development only | MUST NOT be used for HA claim |
| Full PXM backend | OPTIONAL | NOT REQUIRED | MUST | MUST |
| Secure Boot integration | SHOULD | MUST | MUST | MUST |
| Measured Boot integration | MAY | MUST | MUST | MUST |
| TPM measurement binding | MAY | MUST | MUST | MUST |
| Cross-partition device assignment claim | MUST NOT claim | MUST NOT claim | MAY claim only after teardown tests pass | MAY claim only after teardown tests pass |
| IOMMU for PXM device assignment | REQUIRED when claimed | NOT APPLICABLE | MUST | MUST |
| Interrupt remapping for PXM device assignment | REQUIRED when claimed | NOT APPLICABLE | MUST | MUST |
| Partition audit | MUST for exposed API | MUST for exposed API | MUST | MUST |
| Recovery partition coordination | SHOULD | MAY for recovery-only workflows | MUST | MUST |
| PXM Guard support | NOT REQUIRED | NOT REQUIRED | OPTIONAL helper | MUST |

Baseline MAY run MFOS through an implicit single-partition backend. Enterprise-Standalone is a production profile for a single MFOS partition without cross-partition isolation or device-assignment claims. Enterprise-PXM is the first profile that MAY claim side-partition isolation and cross-partition device assignment, and only when the full PXM backend, IOMMU, interrupt remapping, teardown evidence, and audit obligations are satisfied. The implicit backend is still represented through the same partition-aware API so that MFOS does not split into PM and non-PM operating systems.

## 6. Terms

### 6.1 Partition

A Partition is a managed execution container with assigned logical CPU, memory, devices, interrupt routes, identity, image measurement, lifecycle state, and audit history.

### 6.2 MFOS Partition

The MFOS Partition contains the MFOS nucleus and services such as securityd, auditd, catalogd, datasetd, jobd, spoold, operatord, workpolicyd, amfd, and uvsd.

### 6.3 Side Partition

A Side Partition runs a non-MFOS workload such as Linux/Desktop, service tooling, or recovery tooling. It has no authority to bypass MFOS securityd or auditd for MFOS-protected resources.

### 6.4 Activation Profile

An Activation Profile is a declarative input that describes a partition's image, CPU, memory, device, boot, measurement, and recovery parameters.

### 6.5 Implicit Single Partition

The Implicit Single Partition backend represents early MFOS boot without a full partition manager. It exposes a PXM-compatible API for the single running MFOS partition and returns UNSUPPORTED for multi-partition operations.

### 6.6 PXM Core

PXM Core is the partition lifecycle and isolation component. It is deliberately smaller than MFOS and smaller than PXM Guard.

### 6.7 PXM Guard

PXM Guard is the High-Assurance root-object protection component. PXM Core calls Guard only for root-object checks defined in [17-guard.md](17-guard.md).

## 7. Object Model

### 7.1 Partition

```yaml
Partition:
  partition_id: uint64
  name: string
  kind: MFOS | LINUX_DESKTOP | SERVICE | RECOVERY | TEST
  state: PartitionState
  activation_profile_hash: sha384
  image_measurement: sha384?
  policy_epoch: uint64
  owner_principal: string?
  logical_cpus: [LogicalCpuRef]
  memory_domains: [MemoryDomainRef]
  device_assignments: [DeviceAssignmentRef]
  interrupt_routes: [InterruptRouteRef]
  iommu_domain: IommuDomainRef?
  boot_nonce: bytes?
  recovery_profile_id: string?
  audit_correlation_id: uuid
```

### 7.2 ActivationProfile

```yaml
ActivationProfile:
  profile_id: string
  profile_version: uint64
  partition_name: string
  partition_kind: MFOS | LINUX_DESKTOP | SERVICE | RECOVERY | TEST
  image_ref: string
  image_hash: sha384
  required_measurements:
    - component_id: string
      digest: sha384
  cpu:
    min_vcpus: uint16
    max_vcpus: uint16
    allowed_cpu_features: [string]
    forbidden_cpu_features: [string]
  memory:
    min_bytes: uint64
    max_bytes: uint64
    zero_before_reuse: true
  devices:
    - device_id: string
      assignment_mode: EXCLUSIVE | VIRTUAL | DENIED
      require_iommu: bool
      require_interrupt_remap: bool
  boot:
    secure_boot_required: bool
    measured_boot_required: bool
    tpm_required: bool
  recovery:
    recovery_partition_id: string?
    rollback_allowed: bool
  source_matrix_refs:
    - EXTREF-IBM-Z-LPAR-INTRODUCTION-0001
    - EXTREF-IBM-Z-DPM-0001
    - FBVBS-001
```

### 7.3 MemoryDomain

```yaml
MemoryDomain:
  domain_id: uint64
  partition_id: uint64
  base: uint64
  size: uint64
  permissions: READ | WRITE | EXECUTE | READ_WRITE | READ_EXECUTE
  lifecycle: RESERVED | ASSIGNED | MAPPED | REVOKING | ZEROING | FREE
  last_owner_partition_id: uint64?
  zeroed_after_last_owner: bool
```

### 7.4 DeviceAssignment

```yaml
DeviceAssignment:
  assignment_id: uint64
  partition_id: uint64
  device_id: string
  assignment_state: REQUESTED | PREPARED | ACTIVE | QUIESCING | TEARING_DOWN | RELEASED | FAULTED
  iommu_domain_id: uint64?
  interrupt_route_ids: [uint64]
  exclusive: bool
  assigned_at: timestamp?
  released_at: timestamp?
```

### 7.5 PartitionAuditEvent

```yaml
PartitionAuditEvent:
  schema_version: uint16
  event_id: uuid
  timestamp_utc: timestamp
  component_id: "pxm"
  partition_id: uint64?
  operation: string
  actor: SubjectRef
  decision: ALLOW | DENY | FAIL_CLOSED | UNSUPPORTED | SPEC_GAP
  reason_code: string
  previous_state: PartitionState?
  next_state: PartitionState?
  activation_profile_hash: sha384?
  image_measurement: sha384?
  device_id: string?
  iommu_domain_id: uint64?
  interrupt_route_ids: [uint64]
  correlation_id: uuid
```

## 8. Responsibilities

PXM Core MUST implement:

- PXM-R-001 partition create.
- PXM-R-002 partition measure.
- PXM-R-003 partition load.
- PXM-R-004 partition activate.
- PXM-R-005 partition start.
- PXM-R-006 partition quiesce.
- PXM-R-007 partition resume.
- PXM-R-008 partition recover.
- PXM-R-009 partition destroy.
- PXM-R-010 memory zero before reuse.
- PXM-R-011 logical CPU assignment.
- PXM-R-012 memory domain assignment.
- PXM-R-013 IOMMU domain setup.
- PXM-R-014 interrupt remapping.
- PXM-R-015 device assignment.
- PXM-R-016 device teardown.
- PXM-R-017 partition audit.
- PXM-R-018 service and recovery partition coordination.

## 9. Non-Responsibilities

PXM Core MUST NOT:

- Parse JCL-like input.
- Decide dataset access.
- Interpret RACF-like profiles.
- Interpret catalog entries as business resources.
- Manage spool contents.
- Schedule MFOS jobs.
- Interpret workload policy service classes.
- Interpret operator business commands.
- Own securityd policy.
- Own auditd schema semantics beyond PXM audit event payloads.
- Load AMF modules for MFOS services.
- Replace PXM Guard.
- Implement Linux/Desktop user experience features.

## 10. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-PARTITION-0001 | MFOS MUST expose partition-aware APIs even when running under the implicit single-partition backend. | API test |
| MFOS-REQ-PARTITION-0002 | The implicit backend MUST represent the running MFOS instance as one partition and MUST return UNSUPPORTED for unavailable multi-partition operations. | boot test |
| MFOS-REQ-PARTITION-0003 | PXM Core MUST be limited to partition lifecycle and isolation. | architecture review |
| MFOS-REQ-PARTITION-0004 | PXM MUST NOT interpret dataset, job, spool, catalog, security profile, or workload policy semantics. | architecture review |
| MFOS-REQ-PARTITION-0005 | PXM device assignment MUST require IOMMU domain setup and interrupt remapping in Enterprise-PXM and High-Assurance profiles; Enterprise-Standalone MUST NOT claim cross-partition device assignment. | device test |
| MFOS-REQ-PARTITION-0006 | PXM MUST deny device reassignment until teardown checklist completion is recorded. | negative test |
| MFOS-REQ-PARTITION-0007 | PXM MUST zero destroyed or released partition memory before reassignment. | memory reuse test |
| MFOS-REQ-PARTITION-0008 | PXM partition operations MUST generate audit records. | audit test |
| MFOS-REQ-PARTITION-0009 | Activation profile parsing MUST fail closed on unknown required fields, invalid resource ranges, or forbidden device combinations. | parser negative test |
| MFOS-REQ-PARTITION-0010 | Partition state transitions MUST follow the legal transition table in this spec. | state-machine test |
| MFOS-REQ-PARTITION-0011 | PXM calls MUST reject caller-supplied partition state claims and use authoritative PXM state. | privilege confusion test |
| MFOS-REQ-PARTITION-0012 | PXM calls MUST include caller identity, sequence number, correlation ID, and command version. | ABI test |
| MFOS-REQ-PARTITION-0013 | PXM MUST distinguish UNSUPPORTED from SPEC_GAP. | error model test |
| MFOS-REQ-PARTITION-0014 | PXM MUST record image and activation profile measurements before activation in Enterprise-PXM and High-Assurance profiles. | measurement test |
| MFOS-REQ-PARTITION-0015 | PXM MUST coordinate with recovery partition policy before RECOVER transitions. | recovery drill |
| MFOS-REQ-PARTITION-0016 | PXM MUST fail closed when required IOMMU or interrupt remapping features are absent for passthrough device assignment. | platform negative test |
| MFOS-REQ-PARTITION-0017 | PXM MUST revoke CPU mappings, IOMMU mappings, interrupt routes, and device ownership before memory is zeroed and reused. | teardown test |
| MFOS-REQ-PARTITION-0018 | PXM MUST expose all partition state changes to auditd or an equivalent boot-time audit sink. | audit integration test |
| MFOS-REQ-PARTITION-0019 | High-Assurance PXM MUST call Guard for Guard-required root-object transitions. | Guard integration test |
| MFOS-REQ-PARTITION-0020 | PXM MUST NOT present a successful partition operation if the required audit obligation cannot be satisfied under the active profile. | audit failure test |

## 11. State Machine

### 11.1 States

```text
DEFINED
MEASURED
LOADED
ACTIVATED
RUNNABLE
RUNNING
QUIESCED
FAULTED
DEACTIVATED
DESTROYED
```

### 11.2 Legal Transitions

| Current | Trigger | Next | Required condition |
| --- | --- | --- | --- |
| none | DEFINE_PARTITION | DEFINED | Activation profile parsed and admitted. |
| DEFINED | MEASURE_PARTITION | MEASURED | Image, profile, and policy measurements recorded. |
| MEASURED | LOAD_PARTITION | LOADED | Partition image placed into assigned memory. |
| LOADED | ACTIVATE_PARTITION | ACTIVATED | CPU, memory, device, IOMMU, and interrupt assignments committed. |
| ACTIVATED | START_PARTITION | RUNNABLE | Initial vCPU state built. |
| RUNNABLE | scheduler dispatch | RUNNING | Logical CPU available. |
| RUNNING | scheduler deschedule | RUNNABLE | vCPU context saved. |
| RUNNING | QUIESCE_PARTITION | QUIESCED | vCPUs stopped and device quiesce requested. |
| RUNNABLE | QUIESCE_PARTITION | QUIESCED | Runnable vCPUs removed from dispatch. |
| QUIESCED | RESUME_PARTITION | RUNNABLE | Resume condition cleared and resources remain valid. |
| RUNNING | partition fault | FAULTED | Fault captured and audit event queued. |
| RUNNABLE | partition fault | FAULTED | Fault captured and audit event queued. |
| QUIESCED | partition fault | FAULTED | Fault captured and audit event queued. |
| FAULTED | RECOVER_PARTITION | RUNNABLE | Recovery policy allows remeasure, zero, restore, or restart. |
| ACTIVATED | DEACTIVATE_PARTITION | DEACTIVATED | No vCPU running and devices quiesced. |
| QUIESCED | DEACTIVATE_PARTITION | DEACTIVATED | Devices quiesced and routes revoked. |
| FAULTED | DEACTIVATE_PARTITION | DEACTIVATED | Fault recorded and resources quiesced. |
| DEFINED | DESTROY_PARTITION | DESTROYED | Metadata removed and audit recorded. |
| MEASURED | DESTROY_PARTITION | DESTROYED | Metadata removed and audit recorded. |
| LOADED | DESTROY_PARTITION | DESTROYED | Image memory zeroed. |
| ACTIVATED | DESTROY_PARTITION | DESTROYED | Resources revoked and memory zeroed. |
| QUIESCED | DESTROY_PARTITION | DESTROYED | Resources revoked and memory zeroed. |
| FAULTED | DESTROY_PARTITION | DESTROYED | Resources revoked and memory zeroed. |
| DEACTIVATED | DESTROY_PARTITION | DESTROYED | Residual resources revoked and memory zeroed. |

All other transitions MUST return MFOS_ERR_PARTITION_INVALID_STATE and MUST emit a deny or fail-closed audit event when audit is available for the profile.

### 11.3 State Transition Rules

- DEFINE_PARTITION MUST NOT assign devices.
- MEASURE_PARTITION MUST NOT execute partition code.
- LOAD_PARTITION MUST NOT start vCPU execution.
- ACTIVATE_PARTITION MUST NOT dispatch vCPUs.
- START_PARTITION MUST NOT bypass measurement requirements.
- QUIESCE_PARTITION MUST be idempotent only for a partition already in QUIESCED. Other invalid repeats MUST return MFOS_ERR_PARTITION_INVALID_STATE.
- RECOVER_PARTITION MUST require explicit recovery policy.
- DESTROY_PARTITION MUST be fail-closed if CPU, IOMMU, interrupt, or device teardown is incomplete.

## 12. Invariants

```text
INV-PXM-001:
  Partition memory cannot be reassigned until all CPU mappings,
  IOMMU mappings, interrupt routes, and device ownership records
  are revoked and the memory is zeroed.

INV-PXM-002:
  A partition cannot enter RUNNABLE unless its activation profile
  was parsed, measured, loaded, and activated through legal transitions.

INV-PXM-003:
  A device cannot be assigned to more than one exclusive partition
  at the same time.

INV-PXM-004:
  Device assignment in Enterprise-PXM or High-Assurance cannot become ACTIVE
  unless IOMMU domain and interrupt remapping requirements are satisfied.

INV-PXM-005:
  PXM cannot make a security decision about MFOS datasets, jobs,
  catalogs, spool entries, or operator business commands.

INV-PXM-006:
  PXM success for lifecycle or device operations requires an audit
  obligation result compatible with the active profile.

INV-PXM-007:
  The implicit single-partition backend cannot claim High-Assurance
  PXM conformance.

INV-PXM-008:
  Caller-supplied state, identity, or measurement values cannot replace
  authoritative PXM state.
```

## 13. PXM Call ABI

### 13.1 Common Request Header

Every PXM call MUST use a typed request header.

```yaml
PxmCallHeader:
  abi_magic: "PXMC"
  abi_version: uint16
  command: PxmCommand
  caller_sequence: uint64
  caller_subject: SubjectRef
  caller_partition_id: uint64?
  target_partition_id: uint64?
  correlation_id: uuid
  request_length: uint32
  request_hash: sha384
  flags: [string]
  reserved_zero: bytes
```

Rules:

- reserved_zero bytes MUST be zero.
- caller_subject MUST come from the authenticated calling context, not from untrusted payload claims.
- request_length MUST be bounded by a profile-defined maximum.
- request_hash MUST cover header fields except request_hash plus payload bytes.
- caller_sequence MUST be monotonic per caller endpoint.
- replayed caller_sequence values MUST fail closed.
- Unknown commands MUST return MFOS_ERR_SPEC_GAP unless the command is specified but not implemented, in which case they MUST return MFOS_ERR_UNSUPPORTED.

### 13.2 Commands

```text
CREATE_PARTITION
MEASURE_PARTITION
LOAD_PARTITION
ACTIVATE_PARTITION
START_PARTITION
QUIESCE_PARTITION
RESUME_PARTITION
RECOVER_PARTITION
DEACTIVATE_PARTITION
DESTROY_PARTITION
ASSIGN_DEVICE
RELEASE_DEVICE
GET_PARTITION_STATUS
GET_FAULT_INFO
GET_RESOURCE_ASSIGNMENTS
GET_AUDIT_CURSOR
```

### 13.3 Response

```yaml
PxmCallResponse:
  abi_magic: "PXMR"
  abi_version: uint16
  command: PxmCommand
  caller_sequence: uint64
  correlation_id: uuid
  result: MfosErrorCode
  reason_code: string
  previous_state: PartitionState?
  next_state: PartitionState?
  audit_event_id: uuid?
  payload_length: uint32
  payload_hash: sha384?
```

### 13.4 Error Codes

PXM calls MUST use the MFOS error model, including:

```text
MFOS_OK
MFOS_ERR_UNAUTHENTICATED
MFOS_ERR_UNAUTHORIZED
MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE
MFOS_ERR_UNSUPPORTED
MFOS_ERR_SPEC_GAP
MFOS_ERR_INVALID_PARAMETER
MFOS_ERR_PARTITION_INVALID_STATE
MFOS_ERR_DEVICE_TEARDOWN_INCOMPLETE
MFOS_ERR_GUARD_REQUIRED
MFOS_ERR_GUARD_DENIED
MFOS_ERR_INTERNAL_CORRUPTION
```

### 13.5 Call Authorization

PXM call authorization is mediated by the platform management policy and MFOS securityd where MFOS is running and available. During early boot, before securityd is available, only boot-authorized subjects and immutable boot policy MAY issue PXM calls.

PXM MUST NOT accept caller self-asserted administrative authority.

## 14. Device Assignment Model

### 14.1 Assignment Preconditions

Before ASSIGN_DEVICE can succeed:

- The target partition MUST be DEFINED, MEASURED, LOADED, ACTIVATED, QUIESCED, or DEACTIVATED according to the device's allowed lifecycle window.
- The activation profile MUST allow the device.
- The device MUST not be actively assigned to another exclusive partition.
- Required IOMMU domain MUST exist.
- Required interrupt remapping MUST exist.
- Device reset requirements MUST be completed or explicitly UNSUPPORTED with assignment denied.
- Audit obligation MUST be satisfied.

### 14.2 Teardown Checklist

RELEASE_DEVICE and DESTROY_PARTITION MUST complete this checklist before memory or device reuse:

```text
1. Stop partition access to device command queues.
2. Quiesce partition vCPUs that can touch the device.
3. Mask or reroute device interrupts.
4. Stop DMA at device or platform boundary.
5. Revoke IOMMU mappings.
6. Flush device and IOMMU translation caches where required.
7. Reset device if required by device profile.
8. Revoke interrupt routes.
9. Clear PXM ownership record.
10. Record teardown audit event.
```

If any required step fails, PXM MUST leave the device in FAULTED or TEARING_DOWN and MUST NOT assign it to another partition.

### 14.3 Device Teardown Invalid Transitions

| Attempted transition | Required result |
| --- | --- |
| `ACTIVE -> RELEASED` without `QUIESCING` and `TEARING_DOWN` | Return `MFOS_ERR_DEVICE_TEARDOWN_INCOMPLETE`; keep device unavailable for reassignment. |
| `QUIESCING -> RELEASED` before partition vCPUs that can touch the device are stopped | Return `MFOS_ERR_DEVICE_TEARDOWN_INCOMPLETE`; keep assignment in `QUIESCING` or `FAULTED`. |
| `TEARING_DOWN -> RELEASED` before DMA is stopped and IOMMU mappings are revoked | Return `MFOS_ERR_DEVICE_TEARDOWN_INCOMPLETE`; keep device unavailable. |
| `TEARING_DOWN -> RELEASED` before interrupt routes are revoked | Return `MFOS_ERR_DEVICE_TEARDOWN_INCOMPLETE`; keep device unavailable. |
| `TEARING_DOWN -> ACTIVE` for the same or another partition | Return `MFOS_ERR_DEVICE_TEARDOWN_INCOMPLETE`; no reassignment. |
| `FAULTED -> ACTIVE` without device reset or explicit device-profile recovery | Return `MFOS_ERR_DEVICE_TEARDOWN_INCOMPLETE` or `MFOS_ERR_UNSUPPORTED`; no reassignment. |
| `RELEASED -> ACTIVE` for another partition before teardown audit is recorded | Return `MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE`; no reassignment. |
| `DESTROY_PARTITION -> DESTROYED` while any assigned device is not `RELEASED` or safely `FAULTED` and unavailable | Return `MFOS_ERR_DEVICE_TEARDOWN_INCOMPLETE`; partition resources remain unavailable until recovery. |
| `ASSIGN_DEVICE` on Enterprise-Standalone for a side-partition or cross-partition passthrough claim | Return `MFOS_ERR_UNSUPPORTED`; no device-assignment claim. |

## 15. Measurement Model

PXM measurement binds:

- Partition image digest.
- Activation profile digest.
- PXM policy epoch.
- Required boot component digests.
- Device assignment policy digest when device passthrough is requested.
- Guard root references in High-Assurance profile.

Enterprise-PXM and High-Assurance profiles MUST record PXM image and activation profile measurements before activation. Enterprise-Standalone measured boot evidence belongs to the platform boot profile and MUST NOT be presented as a PXM partition measurement claim. Baseline MAY record measurements but MUST NOT pretend a measurement exists if it was not performed.

## 16. Audit Obligations

PXM MUST produce audit events for:

- Partition defined.
- Partition measured.
- Partition loaded.
- Partition activated.
- Partition started.
- Partition quiesced.
- Partition resumed.
- Partition faulted.
- Partition recovered.
- Partition deactivated.
- Partition destroyed.
- Device assignment requested.
- Device assignment allowed or denied.
- Device release requested.
- Device teardown completed or failed.
- IOMMU setup failure.
- Interrupt remapping failure.
- Invalid state transition.
- Unsupported operation.
- Spec gap operation attempt.
- Guard-required operation allowed or denied.

### 16.1 Audit Timing

- DENY, FAIL_CLOSED, UNSUPPORTED, and SPEC_GAP audit records MUST be emitted before the caller receives the final result when the operation is security-sensitive or protected by the active profile.
- If auditd is unavailable during early boot, PXM MUST write to an approved boot audit sink and later reconcile with auditd.
- High-Assurance MUST fail closed when the active policy requires Guard-sealed audit and Guard audit root append fails.

### 16.2 Audit Fields

Each PXM audit event MUST include:

- event_id
- timestamp_utc
- component_id = "pxm"
- operation
- subject
- target partition
- previous_state when applicable
- next_state when applicable
- decision
- reason_code
- activation_profile_hash when applicable
- image_measurement when applicable
- device_id when applicable
- iommu_domain_id when applicable
- interrupt_route_ids when applicable
- policy_epoch
- correlation_id

## 17. Failure Modes

| Failure | Required behavior |
| --- | --- |
| Invalid activation profile | Return MFOS_ERR_INVALID_PARAMETER, no partition state change, audit denial. |
| Unknown required activation field | Return MFOS_ERR_SPEC_GAP or invalid profile error, no success path. |
| Unsupported multi-partition operation on implicit backend | Return MFOS_ERR_UNSUPPORTED, audit if available. |
| Illegal state transition | Return MFOS_ERR_PARTITION_INVALID_STATE, no state change. |
| Audit required but unavailable | Return MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE unless profile allows degraded boot sink. |
| IOMMU unavailable for required device assignment | Deny assignment, return MFOS_ERR_UNSUPPORTED or platform-specific denial. |
| Interrupt remapping unavailable for required device assignment | Deny assignment. |
| Device teardown incomplete | Return MFOS_ERR_DEVICE_TEARDOWN_INCOMPLETE, keep device unavailable. |
| Memory zeroing failure | Keep memory unavailable, fault partition or resource pool. |
| Measurement mismatch | Deny activation, mark partition FAULTED or remain MEASURED based on timing. |
| Guard required but unavailable | Return MFOS_ERR_GUARD_REQUIRED and deny High-Assurance activation. |
| Guard denies root transition | Return MFOS_ERR_GUARD_DENIED and audit denial. |
| Replay of PXM command sequence | Deny and audit replay attempt. |
| Internal metadata corruption | Enter fail-secure mode and require recovery workflow. |

## 18. Tests

### 18.1 Positive Tests

- PXM-T-POS-0001: Implicit backend exposes current MFOS partition status.
- PXM-T-POS-0002: DEFINE -> MEASURE -> LOAD -> ACTIVATE -> START reaches RUNNABLE.
- PXM-T-POS-0003: RUNNABLE dispatch reaches RUNNING and deschedule returns RUNNABLE.
- PXM-T-POS-0004: QUIESCE from RUNNING reaches QUIESCED.
- PXM-T-POS-0005: RESUME from QUIESCED reaches RUNNABLE.
- PXM-T-POS-0006: DESTROY from QUIESCED revokes resources and zeroes memory.
- PXM-T-POS-0007: Device assignment succeeds when profile, IOMMU, interrupt remapping, and audit conditions are satisfied.
- PXM-T-POS-0008: Recovery partition policy allows RECOVER from FAULTED to RUNNABLE.
- PXM-T-POS-0009: Enterprise-PXM measurement records activation profile and image digests before activation.
- PXM-T-POS-0010: PXM audit event includes correlation ID and previous/next state.

### 18.2 Negative Tests

- PXM-T-NEG-0001: START from DEFINED returns MFOS_ERR_PARTITION_INVALID_STATE.
- PXM-T-NEG-0002: ACTIVATE without MEASURE returns invalid state.
- PXM-T-NEG-0003: ASSIGN_DEVICE without IOMMU when required is denied.
- PXM-T-NEG-0004: ASSIGN_DEVICE without interrupt remapping when required is denied.
- PXM-T-NEG-0005: Reassign device before teardown completion is denied.
- PXM-T-NEG-0006: Destroyed partition memory cannot be reused before zeroing.
- PXM-T-NEG-0007: Caller-supplied fake partition state is ignored and audited.
- PXM-T-NEG-0008: Replayed caller_sequence is denied.
- PXM-T-NEG-0009: Unknown command returns SPEC_GAP, not success.
- PXM-T-NEG-0010: Specified but unimplemented command returns UNSUPPORTED, not success.
- PXM-T-NEG-0011: PXM refuses to answer dataset authorization request.
- PXM-T-NEG-0012: High-Assurance activation without Guard returns MFOS_ERR_GUARD_REQUIRED.
- PXM-T-NEG-0013: Audit-required operation with unavailable audit path fails closed.
- PXM-T-NEG-0014: Invalid activation profile with overlapping memory ranges is rejected.
- PXM-T-NEG-0015: Device teardown fault keeps device unavailable for new partitions.

### 18.3 Fuzz Targets

- PXM-FUZZ-0001: Activation profile parser.
- PXM-FUZZ-0002: PXM call header parser.
- PXM-FUZZ-0003: Device assignment profile parser.
- PXM-FUZZ-0004: State transition command sequences.

### 18.4 Fault-Injection Tests

- PXM-FI-0001: Audit sink unavailable during lifecycle operation.
- PXM-FI-0002: IOMMU setup failure after partial resource reservation.
- PXM-FI-0003: Interrupt route failure after device preparation.
- PXM-FI-0004: Memory zeroing failure during destroy.
- PXM-FI-0005: Recovery partition unavailable during RECOVER.

## 19. Evidence Artifacts

Implementation agents MUST produce:

- Requirement IDs implemented.
- Source Matrix IDs referenced.
- State machine transition tests.
- Device teardown evidence.
- Memory zero-before-reuse evidence.
- Audit event samples.
- Negative test results.
- Fuzz target registration.
- Unsupported and SPEC_GAP inventory.
- Profile conformance statement.

## 20. Spec Gaps

The following are intentionally not specified yet:

- Exact VMX/SVM implementation strategy for full PXM backend.
- Exact EPT/NPT page table format and ownership model.
- Exact IOMMU programming model per vendor.
- Exact interrupt remapping hardware programming model per platform.
- Device reset profiles for specific PCIe devices.
- Live migration.
- Nested virtualization.
- Multi-node or sysplex-like partition coordination.
- Performance scheduling policy between partitions.
- Formal TLA+/Alloy model file path and syntax.
- Final boot audit sink format before auditd is available.

Agents MUST NOT fill these gaps with success-path code. They MUST return SPEC_GAP or UNSUPPORTED as appropriate.

## 21. Inactive Future Implementation Prompt Template

Phase status: inactive future template. This section does not authorize production implementation, hosted daemon implementation, or portable semantic-core implementation.

```text
You are an MFOS PXM implementation agent.

Implement only the PXM behavior covered by docs/design/specs/16-pxm.md.

Hard constraints:
- Do not claim z/OS compatibility.
- Treat PXM as partition lifecycle and isolation only.
- Do not implement dataset, catalog, job, spool, workload policy, or operator business semantics in PXM.
- Use requirement IDs in code comments and tests.
- Use Source Matrix IDs in design comments where IBM LPAR/DPM or x64 concepts are used.
- No fake success, empty stub, or silent fallback.
- Return UNSUPPORTED for specified but unavailable behavior.
- Return SPEC_GAP for unspecified behavior.
- Enforce the partition state machine.
- Enforce zero-before-reuse for partition memory.
- Enforce IOMMU and interrupt remapping requirements for device assignment.
- Emit audit obligations for every lifecycle and device operation.
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
