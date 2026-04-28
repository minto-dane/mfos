---
spec_id: "MFOS-SPEC-18-LINUX-GATEWAY"
title: "MFOS Design Specification 18: Linux/Desktop Gateway"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-Z-DPM-0001", "EXTREF-IBM-Z-LPAR-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001", "EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001", "NIST-160-001", "X64-AMD-001", "X64-INTEL-001"]
requirement_refs: ["MFOS-REQ-LGW-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Design Specification 18: Linux/Desktop Gateway

Status: Draft v0.1

Audience: architecture agents, gateway implementation agents, security reviewers, desktop integration agents, test engineers

This document defines the Linux/Desktop Gateway for MFOS. The gateway connects MFOS with a side Linux/Desktop partition through explicit, authorized, audited, typed exchanges. It is not a Linux compatibility layer inside MFOS, not a POSIX-first filesystem model, and not a desktop subsystem embedded in the MFOS nucleus.

MFOS is z/OS-inspired, not z/OS-compatible. Linux/Desktop support is side-by-side integration, not a change to MFOS core enterprise semantics.

## 1. Purpose

The Linux/Desktop Gateway exists to keep desktop, browser, GUI application, GPU, clipboard, and broad driver risks outside the MFOS core while still allowing controlled exchange with MFOS-managed resources.

The gateway provides:

- A side partition model for Linux/Desktop workloads.
- A typed exchange protocol between Linux/Desktop and MFOS services.
- securityd-mediated authorization for every protected MFOS resource operation.
- auditd evidence for every meaningful import, export, submit, browse, and administrative action.
- Fail-closed behavior when policy, audit, or partition isolation prerequisites are missing.
- A path for desktop convenience without weakening MFOS job, dataset, catalog, spool, operator, security, audit, AMF, update, PXM, or Guard boundaries.

## 2. Scope

### 2.1 In Scope

- Gateway trust boundaries.
- Gateway endpoint and channel object model.
- Gateway call ABI.
- Linux/Desktop partition handshake.
- MFOS export workflow.
- MFOS import workflow.
- Spool browse/export workflow.
- Job submission handoff workflow.
- Operator approval workflow hooks.
- Security and audit obligations.
- Failure modes.
- Tests, negative tests, fuzz targets, and spec gaps.

### 2.2 Out of Scope

- Linux syscall compatibility inside MFOS.
- Running Linux binaries directly in MFOS.
- GPU driver stack inside MFOS.
- Browser or desktop compositor inside MFOS.
- Direct mounting of MFOS datasets as Linux filesystems.
- Direct raw block device sharing for MFOS-protected volumes.
- Direct clipboard access to MFOS protected resources.
- General POSIX subsystem design. That is a separate optional MFOS subsystem.
- PXM lifecycle details. See [16-pxm.md](16-pxm.md).
- PXM Guard root-object protection. See [17-guard.md](17-guard.md).

## 3. Source Matrix References

| Source ID | Use |
| --- | --- |
| EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001 | System integrity reference for preventing unauthorized bypass through system interfaces. |
| EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | Audit/accounting reference for system and job-related evidence. |
| EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001 | Reference for treating UNIX-like facilities as an environment, not the MFOS core identity. |
| EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001 | Reference for optional UNIX services separation and documentation boundaries. |
| EXTREF-IBM-Z-LPAR-INTRODUCTION-0001 | Conceptual reference for side partition separation. |
| EXTREF-IBM-Z-DPM-0001 | Conceptual reference for managed partition objects and external management plane. |
| X64-INTEL-001 | x64 isolation, VMX/EPT, IOMMU, and memory protection reference. |
| X64-AMD-001 | AMD64 SVM/NPT and system programming reference. |
| NIST-160-001 | Secure system engineering lifecycle reference. |
| FBVBS-001 | Internal transfer source for partition boundary, command ABI, audit, and fail-closed discipline. |

Linux/Desktop gateway concepts must be described as MFOS integration concepts, not z/OS compatibility claims.

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
| Linux/Desktop side partition | OPTIONAL | MUST NOT claim side-partition isolation | SHOULD for desktop use | SHOULD NOT be in MFOS partition |
| Gateway protocol | OPTIONAL | MUST if Linux/Desktop integration is enabled | MUST if Linux/Desktop integration is enabled | MUST if Linux/Desktop integration is enabled |
| securityd authorization | MUST if gateway enabled | MUST if gateway enabled | MUST | MUST |
| auditd records | MUST if gateway enabled | MUST if gateway enabled | MUST | MUST plus Guard-root linkage where applicable |
| Direct dataset mount in Linux | MUST NOT | MUST NOT | MUST NOT | MUST NOT |
| Raw MFOS volume sharing | MUST NOT | MUST NOT | MUST NOT | MUST NOT |
| Clipboard bridge | OPTIONAL restricted | OPTIONAL restricted | OPTIONAL restricted | OPTIONAL restricted plus stronger policy |
| File import/export | OPTIONAL restricted | MUST if gateway enabled | MUST if gateway enabled | MUST if gateway enabled |
| Job submission handoff | OPTIONAL | SHOULD if gateway enabled | SHOULD | SHOULD |
| Remote desktop into MFOS operator console | SPEC_GAP | SPEC_GAP | SPEC_GAP | SPEC_GAP |

## 6. Trust Boundaries

```text
Linux/Desktop application
  -> Linux/Desktop gateway agent
  -> PXM channel boundary
  -> MFOS gateway endpoint
  -> securityd authorization
  -> target MFOS service
  -> auditd evidence
```

Linux/Desktop applications are untrusted relative to MFOS protected resources. The Linux kernel and desktop stack are also outside the MFOS system integrity boundary unless a future profile explicitly proves otherwise.

MFOS MUST treat all gateway input as untrusted, even when it originates from an assigned side partition.

## 7. Terms

### 7.1 Gateway Endpoint

A Gateway Endpoint is a typed MFOS service endpoint that accepts gateway requests from a side partition after PXM has established a permitted channel.

### 7.2 Gateway Channel

A Gateway Channel is a bounded, typed, authenticated communication path between a side partition and an MFOS gateway endpoint.

### 7.3 Export

Export means MFOS emits an approved representation of a protected MFOS resource to a side partition or external destination.

### 7.4 Import

Import means MFOS accepts data or metadata from a side partition and turns it into an MFOS object only after validation, authorization, and audit.

### 7.5 Gateway Token

A Gateway Token is a short-lived capability-like value binding subject, operation, object, policy_version, channel_id, expiry, and audit obligation.

Gateway Tokens are not general MFOS handles and MUST NOT be accepted outside gateway endpoints.

## 8. Object Model

### 8.1 GatewayEndpoint

```yaml
GatewayEndpoint:
  endpoint_id: string
  endpoint_kind: IMPORT | EXPORT | SPOOL | JOB_SUBMIT | CLIPBOARD | STATUS
  owning_component: string
  allowed_partition_kinds:
    - LINUX_DESKTOP
    - SERVICE
  max_request_bytes: uint64
  max_response_bytes: uint64
  requires_securityd: true
  requires_auditd: true
  allowed_operations: [string]
  status: ENABLED | DISABLED | DEGRADED
```

### 8.2 GatewayChannel

```yaml
GatewayChannel:
  channel_id: uuid
  source_partition_id: uint64
  target_partition_id: uint64
  endpoint_id: string
  channel_state: REQUESTED | AUTHORIZED | OPEN | DRAINING | CLOSED | FAULTED
  channel_profile: string
  max_inflight_requests: uint32
  max_payload_bytes: uint64
  created_at: timestamp
  expires_at: timestamp
  audit_correlation_id: uuid
```

### 8.3 GatewayRequest

```yaml
GatewayRequest:
  request_id: uuid
  channel_id: uuid
  operation: GatewayOperation
  subject: SubjectRef
  object: ObjectRef?
  policy_version: uint64
  payload_format: string
  payload_hash: sha384
  payload_length: uint64
  requested_at: timestamp
  correlation_id: uuid
```

### 8.4 GatewayToken

```yaml
GatewayToken:
  token_id: uuid
  channel_id: uuid
  subject: SubjectRef
  object: ObjectRef
  operation: GatewayOperation
  policy_version: uint64
  issued_at: timestamp
  expires_at: timestamp
  audit_obligation_id: uuid
  token_hash: sha384
```

### 8.5 ImportPackage

```yaml
ImportPackage:
  package_id: uuid
  source_partition_id: uint64
  claimed_name: string
  content_type: string
  payload_hash: sha384
  payload_length: uint64
  scan_status: NOT_SCANNED | PASSED | FAILED | UNSUPPORTED
  target_dataset_dsn: string?
  target_job_name: string?
  received_at: timestamp
```

### 8.6 ExportPackage

```yaml
ExportPackage:
  package_id: uuid
  source_object: ObjectRef
  export_format: string
  payload_hash: sha384
  payload_length: uint64
  redaction_policy: string?
  destination_partition_id: uint64
  exported_at: timestamp
```

## 9. Responsibilities

The Linux/Desktop Gateway MUST implement:

- LGW-R-001 side partition endpoint registration.
- LGW-R-002 gateway channel lifecycle.
- LGW-R-003 typed request parsing.
- LGW-R-004 securityd authorization for protected resource operations.
- LGW-R-005 auditd evidence for gateway actions.
- LGW-R-006 dataset export through datasetd and catalogd.
- LGW-R-007 dataset import through validation, catalogd, datasetd, and securityd.
- LGW-R-008 spool browse/export through spoold and securityd.
- LGW-R-009 job submission handoff through jobd and securityd.
- LGW-R-010 optional clipboard bridge with explicit policy.
- LGW-R-011 fail-closed behavior on audit, policy, validation, or channel failure.
- LGW-R-012 replay and stale-token rejection.
- LGW-R-013 payload size, type, and hash validation.

## 10. Non-Responsibilities

The Linux/Desktop Gateway MUST NOT:

- Put Linux or desktop drivers inside the MFOS nucleus.
- Mount MFOS datasets directly in Linux.
- Expose MFOS raw storage volumes to Linux/Desktop partitions.
- Let Linux/Desktop processes hold native dataset handles.
- Let Linux/Desktop bypass securityd.
- Let Linux/Desktop bypass auditd.
- Let clipboard operations bypass resource authorization.
- Treat Linux user IDs as MFOS principals without explicit identity mapping.
- Treat a Linux root user as an MFOS operator.
- Provide an unmediated root shell into MFOS.
- Convert datasets into ordinary POSIX files as the primary model.
- Interpret AMF policy.
- Modify Guard roots.
- Assume the Linux/Desktop partition is trusted because PXM isolated it.

## 11. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-LGW-0001 | Linux/Desktop integration MUST use a side partition or explicitly marked non-production development mode. | architecture review |
| MFOS-REQ-LGW-0002 | The gateway MUST NOT mount MFOS datasets directly in Linux/Desktop. | negative test |
| MFOS-REQ-LGW-0003 | Every protected resource gateway operation MUST call securityd before target service access. | integration test |
| MFOS-REQ-LGW-0004 | Every gateway operation with a security decision MUST create audit evidence. | audit test |
| MFOS-REQ-LGW-0005 | DENY decisions MUST be audited before final result returns when audit is available. | negative test |
| MFOS-REQ-LGW-0006 | Gateway requests MUST include subject, operation, object when applicable, policy_version, channel_id, payload hash, and correlation_id. | ABI test |
| MFOS-REQ-LGW-0007 | Gateway tokens MUST bind subject, object, operation, policy_version, channel_id, expiry, and audit obligation. | token test |
| MFOS-REQ-LGW-0008 | Gateway tokens MUST be rejected outside the gateway endpoint that issued them. | negative test |
| MFOS-REQ-LGW-0009 | Linux root MUST NOT map automatically to MFOS operator authority. | privilege confusion test |
| MFOS-REQ-LGW-0010 | Gateway payloads MUST be bounded by endpoint profile limits. | parser test |
| MFOS-REQ-LGW-0011 | Gateway imports MUST validate content type, payload length, payload hash, target object, and authorization before object creation. | import test |
| MFOS-REQ-LGW-0012 | Gateway exports MUST apply authorization, redaction policy when present, and audit before data release. | export test |
| MFOS-REQ-LGW-0013 | Spool browse/export through gateway MUST be mediated by spoold and securityd. | integration test |
| MFOS-REQ-LGW-0014 | Job submission through gateway MUST be mediated by jobd and securityd. | integration test |
| MFOS-REQ-LGW-0015 | Clipboard bridge operations MUST be explicitly enabled by policy and audited. | clipboard negative test |
| MFOS-REQ-LGW-0016 | Gateway MUST distinguish UNSUPPORTED from SPEC_GAP. | error model test |
| MFOS-REQ-LGW-0017 | Gateway MUST reject replayed request IDs or stale gateway tokens. | replay test |
| MFOS-REQ-LGW-0018 | Gateway MUST fail closed when auditd is unavailable and the active profile requires audit. | fault injection |
| MFOS-REQ-LGW-0019 | Gateway MUST not accept caller-supplied MFOS identity without authenticated identity mapping. | identity negative test |
| MFOS-REQ-LGW-0020 | Gateway MUST audit channel open, close, fault, import, export, job submit, spool browse, deny, unsupported, and spec gap events. | audit review |

## 12. Gateway Channel State Machine

### 12.1 States

```text
REQUESTED
AUTHORIZED
OPEN
DRAINING
CLOSED
FAULTED
```

### 12.2 Legal Transitions

| Current | Trigger | Next | Required condition |
| --- | --- | --- | --- |
| none | REQUEST_CHANNEL | REQUESTED | Source partition and endpoint exist. |
| REQUESTED | AUTHORIZE_CHANNEL | AUTHORIZED | PXM channel policy and securityd authorization allow it. |
| AUTHORIZED | OPEN_CHANNEL | OPEN | Endpoint ready and audit open event recorded. |
| OPEN | CLOSE_CHANNEL | DRAINING | No new requests accepted. |
| DRAINING | DRAIN_COMPLETE | CLOSED | In-flight requests completed or canceled. |
| REQUESTED | DENY_CHANNEL | CLOSED | Denial audited. |
| AUTHORIZED | DENY_OPEN | CLOSED | Denial audited. |
| OPEN | CHANNEL_FAULT | FAULTED | Fault recorded and in-flight tokens revoked. |
| DRAINING | CHANNEL_FAULT | FAULTED | Fault recorded and in-flight tokens revoked. |
| FAULTED | CLOSE_CHANNEL | CLOSED | Fault cleanup completed. |

All other transitions MUST return an invalid state error and MUST audit when possible.

## 13. Gateway Request State Machine

### 13.1 States

```text
RECEIVED
PARSED
IDENTITY_MAPPED
AUTHORIZED
VALIDATED
EXECUTING
AUDITED
RESPONDED
DENIED
FAILED
```

### 13.2 Success Flow

```text
RECEIVED
  -> PARSED
  -> IDENTITY_MAPPED
  -> AUTHORIZED
  -> VALIDATED
  -> EXECUTING
  -> AUDITED
  -> RESPONDED
```

### 13.3 Failure Flow

```text
RECEIVED
  -> PARSED
  -> IDENTITY_MAPPED
  -> DENIED
  -> AUDITED
  -> RESPONDED
```

or:

```text
RECEIVED
  -> FAILED
  -> AUDITED
  -> RESPONDED
```

Rules:

- AUTHORIZED MUST occur before EXECUTING for protected MFOS resources.
- AUDITED MUST occur before RESPONDED for DENY when audit path is available.
- VALIDATED MUST occur before object creation for imports.
- Gateway MUST NOT create native dataset handles for Linux/Desktop callers.

## 14. Gateway Call ABI

### 14.1 Common Request Header

```yaml
GatewayCallHeader:
  abi_magic: "LGWC"
  abi_version: uint16
  command: GatewayCommand
  request_id: uuid
  channel_id: uuid
  caller_sequence: uint64
  source_partition_id: uint64
  caller_subject_claim: SubjectClaim?
  operation: GatewayOperation
  object_ref: ObjectRef?
  policy_version: uint64
  payload_length: uint64
  payload_hash: sha384
  correlation_id: uuid
  reserved_zero: bytes
```

Rules:

- reserved_zero MUST be zero.
- source_partition_id MUST match PXM channel state.
- caller_subject_claim MUST be mapped to an MFOS subject through configured identity mapping.
- caller_sequence MUST be monotonic per channel.
- request_id MUST be unique per channel until retention expiry.
- payload_length MUST be within endpoint maximum.
- payload_hash MUST match payload bytes.

### 14.2 Commands

```text
REQUEST_CHANNEL
OPEN_CHANNEL
CLOSE_CHANNEL
GET_STATUS
EXPORT_DATASET
IMPORT_DATASET
BROWSE_SPOOL
EXPORT_SPOOL
SUBMIT_JOB
REQUEST_CLIPBOARD_EXPORT
REQUEST_CLIPBOARD_IMPORT
CANCEL_REQUEST
```

### 14.3 Response

```yaml
GatewayCallResponse:
  abi_magic: "LGWR"
  abi_version: uint16
  command: GatewayCommand
  request_id: uuid
  channel_id: uuid
  caller_sequence: uint64
  result: MfosErrorCode
  reason_code: string
  audit_event_id: uuid?
  gateway_token_id: uuid?
  response_payload_length: uint64
  response_payload_hash: sha384?
  correlation_id: uuid
```

### 14.4 Error Codes

Gateway calls MUST use the MFOS error model, including:

```text
MFOS_OK
MFOS_ERR_UNAUTHENTICATED
MFOS_ERR_UNAUTHORIZED
MFOS_ERR_POLICY_DENIED
MFOS_ERR_POLICY_VERSION_MISMATCH
MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE
MFOS_ERR_UNSUPPORTED
MFOS_ERR_SPEC_GAP
MFOS_ERR_INVALID_PARAMETER
MFOS_ERR_INVALID_DSN
MFOS_ERR_CATALOG_NOT_FOUND
MFOS_ERR_DATASET_LOCKED
MFOS_ERR_IMMUTABLE
MFOS_ERR_STALE_HANDLE
MFOS_ERR_INTERNAL_CORRUPTION
```

## 15. Identity Mapping

Linux/Desktop identity is not MFOS identity.

Gateway identity mapping MUST:

- Bind Linux/Desktop partition identity to a configured MFOS trust mapping.
- Bind user claims to authenticated mechanisms approved for the gateway.
- Reject unmapped Linux UIDs, GIDs, process names, or desktop session identifiers.
- Reject Linux root as automatic MFOS operator authority.
- Include identity mapping result in audit records.

Example:

```yaml
IdentityMapping:
  source_partition_id: uint64
  external_subject:
    kind: LINUX_UID
    value: "1000"
  mfos_subject:
    principal_id: "ALICE"
  allowed_operations:
    - EXPORT_SPOOL
    - SUBMIT_JOB
  expires_at: timestamp
  policy_version: uint64
```

## 16. Operation Rules

### 16.1 EXPORT_DATASET

Required flow:

```text
Parse request
Map identity
Authorize DATASET EXPORT through securityd
Resolve DSN through catalogd
Open dataset through datasetd with export operation
Apply redaction/export policy if present
Create ExportPackage
Audit export
Return package metadata and payload through bounded channel
```

Gateway MUST NOT expose the native dataset handle to Linux/Desktop.

### 16.2 IMPORT_DATASET

Required flow:

```text
Parse request
Map identity
Validate payload length, hash, type, and target DSN
Authorize DATASET IMPORT or CREATE through securityd
Create or update catalog entry through catalogd when allowed
Write through datasetd
Audit import
Return committed dataset reference
```

Import MUST fail closed if validation, authorization, catalog transaction, dataset write, or audit fails.

### 16.3 BROWSE_SPOOL and EXPORT_SPOOL

Required flow:

```text
Parse request
Map identity
Authorize SPOOL BROWSE or EXPORT through securityd
Read through spoold
Apply output class and redaction policy
Audit browse or export
Return bounded response
```

### 16.4 SUBMIT_JOB

Required flow:

```text
Parse request
Map identity
Validate JCL-like payload boundary and size
Authorize JOB SUBMIT through securityd
Submit through jobd
Audit submit handoff
Return job_id or denial
```

jobd remains responsible for conversion, DD resolution, step execution, return code, and job audit events.

### 16.5 Clipboard Bridge

Clipboard bridge is optional and restricted.

Rules:

- It MUST be disabled by default.
- It MUST have explicit policy.
- It MUST not access protected MFOS resources without securityd authorization.
- It MUST record audit events.
- It MUST support redaction policy.
- It MUST reject oversized payloads.
- It MUST not auto-import executable content into AMF or system datasets.

## 17. Invariants

```text
INV-LGW-001:
  Linux/Desktop callers cannot obtain native MFOS dataset, catalog,
  spool, job, operator, AMF, PXM, or Guard handles.

INV-LGW-002:
  Every protected MFOS resource operation through the gateway requires
  a securityd decision bound to subject, object, operation, context,
  and policy_version.

INV-LGW-003:
  DENY decisions are audited before final result returns when an audit
  path is available.

INV-LGW-004:
  Linux root is not MFOS operator authority.

INV-LGW-005:
  Gateway tokens are valid only for the issuing endpoint, channel,
  subject, object, operation, policy_version, and expiry.

INV-LGW-006:
  MFOS datasets are not mounted directly as Linux filesystems.

INV-LGW-007:
  Raw MFOS protected storage volumes are not exposed to Linux/Desktop
  partitions.

INV-LGW-008:
  Gateway import cannot create or mutate an MFOS object before payload
  validation and authorization.

INV-LGW-009:
  Gateway export cannot release payload bytes before authorization,
  redaction where required, and audit obligation handling.

INV-LGW-010:
  Gateway cannot silently downgrade from audited gateway exchange to
  unaudited shared memory, shared disk, clipboard, or network transfer.
```

## 18. Audit Obligations

Gateway MUST audit:

- Channel requested.
- Channel authorized.
- Channel denied.
- Channel opened.
- Channel closed.
- Channel faulted.
- Identity mapping success.
- Identity mapping failure.
- Dataset export allowed or denied.
- Dataset import allowed or denied.
- Spool browse allowed or denied.
- Spool export allowed or denied.
- Job submit handoff allowed or denied.
- Clipboard export allowed or denied.
- Clipboard import allowed or denied.
- Replay detected.
- Stale token rejected.
- Payload validation failure.
- Audit-required operation blocked because audit was unavailable.
- UNSUPPORTED command attempt.
- SPEC_GAP command attempt.

### 18.1 Audit Timing

- DENY MUST be audited before final result returns when audit path is available.
- Export payload bytes MUST NOT be released before the export audit obligation is accepted under the active profile.
- Import object commit MUST NOT be reported as success before audit obligation is accepted under the active profile.

### 18.2 Audit Fields

Gateway audit records MUST include:

- event_id
- timestamp_utc
- component_id = "linux_gateway"
- source_partition_id
- endpoint_id
- channel_id
- request_id
- subject claim
- mapped MFOS subject when available
- operation
- object_ref when applicable
- policy_version
- payload_hash when applicable
- payload_length when applicable
- decision
- reason_code
- audit obligation ID
- correlation_id

## 19. Failure Modes

| Failure | Required behavior |
| --- | --- |
| Source partition not authorized for endpoint | Deny channel, audit denial. |
| Endpoint disabled | Return UNSUPPORTED or policy denial, audit. |
| Unknown command | Return SPEC_GAP and audit. |
| Specified but unavailable command | Return UNSUPPORTED and audit. |
| Identity mapping missing | Deny and audit identity failure. |
| Linux root claims operator authority | Deny and audit privilege confusion. |
| Payload hash mismatch | Deny, discard payload, audit validation failure. |
| Payload too large | Deny and audit validation failure. |
| Payload type unsupported | Return UNSUPPORTED or deny by policy. |
| securityd unavailable | Fail closed for protected operations. |
| auditd unavailable | Fail closed when audit is required. |
| catalogd unavailable for dataset operation | Fail closed or return service unavailable, no fake success. |
| datasetd unavailable for dataset operation | Fail closed or return service unavailable, no fake success. |
| spoold unavailable for spool operation | Fail closed or return service unavailable, no fake success. |
| jobd unavailable for job submit | Fail closed or return service unavailable, no fake success. |
| Stale gateway token | Deny and audit stale token. |
| Replayed request ID or sequence | Deny and audit replay. |
| Channel fault mid-export | Stop release, revoke tokens, audit fault. |
| Channel fault mid-import | Abort or roll back transaction, audit fault. |

## 20. Tests

### 20.1 Positive Tests

- LGW-T-POS-0001: Authorized Linux/Desktop side partition opens a gateway channel.
- LGW-T-POS-0002: Mapped user exports an allowed dataset through securityd, catalogd, datasetd, and auditd.
- LGW-T-POS-0003: Mapped user imports a valid package into an allowed target dataset.
- LGW-T-POS-0004: Mapped user browses allowed spool output through spoold and securityd.
- LGW-T-POS-0005: Mapped user submits a job through jobd and receives job_id.
- LGW-T-POS-0006: Gateway token binds channel, subject, object, operation, policy_version, and expiry.
- LGW-T-POS-0007: Clipboard export succeeds only when explicitly enabled by policy.
- LGW-T-POS-0008: Channel close drains in-flight request before CLOSED.
- LGW-T-POS-0009: Export applies redaction policy before payload release.
- LGW-T-POS-0010: Gateway audit record includes source partition, channel, request, mapped subject, and payload hash.

### 20.2 Negative Tests

- LGW-T-NEG-0001: Linux root cannot execute MFOS operator command by gateway identity claim.
- LGW-T-NEG-0002: Unmapped Linux UID is denied.
- LGW-T-NEG-0003: Direct dataset mount request returns SPEC_GAP or policy denial, never success.
- LGW-T-NEG-0004: Raw MFOS volume share request is denied.
- LGW-T-NEG-0005: Dataset export without securityd allow is denied.
- LGW-T-NEG-0006: Dataset import without securityd allow is denied before object creation.
- LGW-T-NEG-0007: Spool browse without securityd allow is denied.
- LGW-T-NEG-0008: Job submit without securityd allow is denied.
- LGW-T-NEG-0009: Payload hash mismatch is denied.
- LGW-T-NEG-0010: Oversized payload is denied.
- LGW-T-NEG-0011: Stale gateway token is denied.
- LGW-T-NEG-0012: Gateway token used on another endpoint is denied.
- LGW-T-NEG-0013: Replayed request_id is denied.
- LGW-T-NEG-0014: Replayed caller_sequence is denied.
- LGW-T-NEG-0015: Clipboard bridge attempt while disabled is denied.
- LGW-T-NEG-0016: Audit-required export with unavailable auditd fails closed.
- LGW-T-NEG-0017: Unknown command returns SPEC_GAP, not success.
- LGW-T-NEG-0018: Specified but unavailable command returns UNSUPPORTED, not success.
- LGW-T-NEG-0019: Nonzero reserved field in request header is rejected.
- LGW-T-NEG-0020: Channel fault mid-import rolls back or leaves no committed target object.

### 20.3 Fuzz Targets

- LGW-FUZZ-0001: Gateway call header parser.
- LGW-FUZZ-0002: Identity mapping parser.
- LGW-FUZZ-0003: Import package parser.
- LGW-FUZZ-0004: Export request parser.
- LGW-FUZZ-0005: Clipboard payload parser.
- LGW-FUZZ-0006: Gateway request state transition sequences.

### 20.4 Fault-Injection Tests

- LGW-FI-0001: securityd unavailable during dataset export.
- LGW-FI-0002: auditd unavailable during DENY.
- LGW-FI-0003: catalogd crash mid-import.
- LGW-FI-0004: datasetd write failure mid-import.
- LGW-FI-0005: spoold unavailable during browse.
- LGW-FI-0006: jobd unavailable during submit.
- LGW-FI-0007: channel fault mid-export.
- LGW-FI-0008: endpoint disabled while request is in flight.

## 21. Evidence Artifacts

Implementation agents MUST produce:

- Requirement IDs implemented.
- Source Matrix IDs referenced.
- Gateway ABI tests.
- Identity mapping tests.
- Securityd integration evidence.
- Auditd integration evidence.
- Dataset export and import traces.
- Spool browse/export traces.
- Job submit handoff trace.
- Negative tests for direct mount and raw volume share.
- Replay and stale token test results.
- Fuzz target registration.
- Unsupported and SPEC_GAP inventory.
- Profile conformance statement.

## 22. Spec Gaps

The following are intentionally not specified yet:

- Exact transport mechanism for the PXM channel.
- Exact shared-memory layout if a shared-memory transport is later approved.
- Exact identity provider integration for Linux/Desktop user sessions.
- Exact malware scanning or content scanning engine for imports.
- Exact redaction policy language.
- Exact clipboard policy grammar.
- Exact file format mapping between MFOS datasets and external desktop formats.
- Exact GUI management application behavior.
- Exact remote desktop behavior for operator console access.
- Exact network gateway behavior.
- Exact performance and backpressure policy.
- Formal TLA+/Alloy model file path and syntax.

Agents MUST NOT fill these gaps with success-path code. They must return SPEC_GAP or UNSUPPORTED as appropriate.

## 23. Inactive Future Implementation Prompt Template

Phase status: inactive future template. This section does not authorize production implementation, hosted daemon implementation, or portable semantic-core implementation.

```text
You are an MFOS Linux/Desktop Gateway implementation agent.

Implement only the gateway behavior covered by docs/design/specs/18-linux-gateway.md.

Hard constraints:
- Do not claim z/OS compatibility.
- Do not put Linux, POSIX, GPU, browser, or desktop stack inside the MFOS nucleus.
- Do not mount MFOS datasets directly in Linux/Desktop.
- Do not expose raw MFOS protected storage volumes to Linux/Desktop.
- Do not allow Linux root to become MFOS operator authority.
- Treat all gateway input as untrusted.
- Use securityd for protected resource authorization.
- Use auditd for gateway evidence.
- Use requirement IDs in code comments and tests.
- Use Source Matrix IDs in design comments where partition, audit, UNIX-environment, or x64 isolation concepts are used.
- No fake success, empty stub, or silent fallback.
- Return UNSUPPORTED for specified but unavailable behavior.
- Return SPEC_GAP for unspecified behavior.
- Enforce channel and request state machines.
- Enforce gateway token binding and expiry.
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
