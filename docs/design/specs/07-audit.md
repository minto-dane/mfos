---
spec_id: "MFOS-SPEC-07-AUDIT"
title: "MFOS Audit and auditd Specification v0.8 Design Freeze"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "phase-0.8-design-freeze"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001", "EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001", "EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001", "EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001", "EXTREF-IBM-Z-DPM-0001", "EXTREF-IBM-ZOS-JES-INTRODUCTION-0001", "EXTREF-IBM-ZOS-JES-JOB-FLOW-0001", "EXTREF-IBM-ZOS-JES2-LIBRARY-0001", "EXTREF-IBM-Z-LPAR-INTRODUCTION-0001", "EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001", "EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001"]
requirement_refs: ["MFOS-REQ-AUDIT-*"]
claim_refs: []
test_refs: ["TEST-MFOS-AUDIT-*", "NEG-MFOS-AUDIT-*"]
evidence_refs: ["EV-MFOS-AUDIT-*"]
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Audit and auditd Specification v0.8 Design Freeze

Status: Phase 0.8 design freeze

Owner area: `docs/design/specs/07-audit.md`

This document defines the MFOS audit evidence model and the `auditd` service. Audit is not ordinary logging. Audit records are security evidence used for authorization accountability, system integrity, job accounting, dataset activity, operator actions, update safety, partition operations, and High-Assurance Guard audit-root transitions.

Phase 0.8 freezes audit semantics at design level only. This document, the machine-readable `AuditRecord` schema, the audit append state-machine artifact, the Phase 0.8 audit test catalog, and the audit-lead report do not authorize production implementation work.

MFOS is z/OS-inspired and source-grounded. It does not claim compatibility with IBM products, z/Architecture, z/OS APIs, RACF, JES, DFSMS, SMF, or JCL.

## 1. Purpose

`auditd` provides:

- Append-only audit record ingestion.
- Schema validation.
- Monotonic sequencing.
- Hash-chain evidence.
- Local durable storage.
- Query and export with authorization.
- Retention enforcement.
- Failure policy enforcement.
- Remote export in Enterprise-Standalone, Enterprise-PXM, and High-Assurance profiles.
- Guard-sealed audit root in High-Assurance profile.

The audit model exists to prevent:

- Treating console output or spool output as audit evidence.
- Returning security denies before required deny audit is durable.
- Allowing services to emit unstructured logs as security evidence.
- Silent audit loss.
- Hash-chain gaps without detection.
- Audit query bypass.
- Guard root claims without audit linkage.

## 2. Scope

This specification defines:

- Audit trust levels.
- Audit event classes.
- Audit record schema.
- Canonicalization and hash-chain rules.
- Append protocol.
- Required audit obligations.
- Failure policies by profile.
- Query, export, redaction, and retention rules.
- Recovery and tamper response.
- Invariants, failure modes, tests, negative tests, fuzz targets, and spec gaps.

This specification does not define:

- Physical storage layout.
- Final cryptographic signature algorithms.
- Remote collector protocol.
- Full SIEM integration.
- Compression format.
- Long-term archival system.
- Guard implementation internals.
- Kernel crash dump format.

## 3. Source Matrix References

Phase 0.8 audit source references in this document are `EXTREF-*` IDs only.

| Source ID | Audit use |
| --- | --- |
| EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | System/job-related record collection for billing, reliability, configuration, scheduling, dataset activity, profiling, and security maintenance. |
| EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001 | Security audit fields inspired by RACF type 80: unauthorized attempts, event codes, user identification, authorities used, and audit reasons. |
| EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001 | System integrity requires unauthorized subjects not to bypass audit-relevant protection. |
| EXTREF-IBM-ZOS-SECURITY-SERVER-0001 | Security manager audit administration and protected resource event concepts. |
| EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001 | Protected-resource decisions, profiles, access attempts, and authorization-linked audit records. |
| EXTREF-IBM-ZOS-JES-INTRODUCTION-0001 | Job, SYSIN, SYSOUT, and spool lifecycle events. |
| EXTREF-IBM-ZOS-JES-JOB-FLOW-0001 | Job-flow correlation across submit, execution, completion, and output lifecycle records. |
| EXTREF-IBM-ZOS-JES2-LIBRARY-0001 | Operator-visible job and spool administration events. |
| EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001 | Dataset and catalog activity events. |
| EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001 | Dataset and catalog metadata required in audit payloads. |
| EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001 | Authorized module events and authority use. |
| EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001 | Boundary, parameter, and authority-use negative-test framing. |
| EXTREF-IBM-Z-LPAR-INTRODUCTION-0001 | Partition operation events. |
| EXTREF-IBM-Z-DPM-0001 | Partition management events and operator-controlled lifecycle actions. |
| EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001 | Security-advisory update events that require audit evidence. |

## 3.1 Phase 0.8 Evidence Boundary

An MFOS audit evidence item is exactly one of:

- A schema-valid `AuditRecord` accepted by `auditd`, durably appended to an audit stream, and linked into the stream hash chain.
- A verified exported representation of one or more such records that preserves stream ID, sequence range, hashes, schema version, and export audit records.
- A High-Assurance Guard-sealed audit root that binds to a verified audit stream head and is supported by the underlying `AuditRecord` chain.

The following are not audit evidence and MUST NOT satisfy an audit obligation:

- A diagnostic log line.
- A console line.
- A spool entry.
- Spool output, SYSOUT-like output, or job output.
- A remote collector receipt without the local durable `AuditRecord` and chain metadata.
- A checksum-only file or record without `auditd` schema validation and hash-chain linkage.

## 4. Normative Language

- `MUST`: required for the applicable profile.
- `SHOULD`: strongly recommended; deviation requires ADR and evidence.
- `MAY`: optional.
- `MUST NOT`: prohibited.
- `UNSUPPORTED`: specified behavior not implemented; fail closed where security-sensitive.
- `SPEC_GAP`: undefined behavior; do not invent success or evidence.

## 5. auditd Responsibilities

```text
AUD-R-001  append-only record stream
AUD-R-002  schema validation
AUD-R-003  hash chain
AUD-R-004  local durable store
AUD-R-005  remote export
AUD-R-006  audit query authorization
AUD-R-007  audit retention
AUD-R-008  audit failure policy
AUD-R-009  correlation ID management
AUD-R-010  Guard-sealed root in High-Assurance profile
AUD-R-011  canonical record encoding
AUD-R-012  redaction policy for query/export
AUD-R-013  tamper detection and alerting
AUD-R-014  recovery and continuity after crash
AUD-R-015  audit stream metadata management
```

## 6. auditd Non-Responsibilities

`auditd` MUST NOT:

- Decide resource authorization. `securityd` is the policy decision point.
- Store spool content as audit evidence.
- Parse JCL-like input for job semantics.
- Interpret business policy beyond audit schema and retention.
- Rewrite committed audit records.
- Hide denied security events for operator convenience.
- Treat CRC or checksum as tamper resistance.
- Claim Guard-sealed roots outside High-Assurance evidence.
- Accept caller-supplied record hashes without recomputation.

## 7. Audit Trust Levels

```text
AUD-L0  diagnostic console output
AUD-L1  local auditd append stream
AUD-L2  hash-chained local audit
AUD-L3  remote exported audit
AUD-L4  Guard-sealed audit root
AUD-L5  external/OOB authoritative audit path
```

Rules:

- AUD-L0 is never sufficient for security evidence.
- Baseline MUST provide at least AUD-L1 for protected events and SHOULD provide AUD-L2.
- Enterprise MUST provide AUD-L2 and remote export capability for AUD-L3.
- High-Assurance MUST provide Guard-sealed audit root for AUD-L4.
- AUD-L5 is optional and requires separate hardware or operational design.

## 8. Audit Streams

```yaml
AuditStream:
  stream_id: string
  stream_name: string
  stream_class: SECURITY | SYSTEM | JOB | DATASET | OPERATOR | UPDATE | PARTITION | GUARD | DIAGNOSTIC
  trust_level: AUD-L1 | AUD-L2 | AUD-L3 | AUD-L4 | AUD-L5
  partition_id: PartitionId
  schema_version: uint16
  current_sequence: uint64
  current_hash: Digest
  created_at: Timestamp
  sealed_root_ref: GuardRootRef?
  retention_policy: RetentionPolicyRef
  export_policy: ExportPolicyRef?
  status: ACTIVE | DEGRADED | SEALED | RECOVERING | RETIRED
```

Rules:

- Security-sensitive records MUST be written to a security-capable stream.
- Stream sequence numbers MUST be monotonic per stream.
- Stream rollover MUST preserve chain continuity through a rollover record.

## 9. Audit Event Classes

```yaml
AuditClass:
  - SECURITY_DECISION
  - SECURITY_DENY
  - POLICY_CHANGE
  - DATASET_ACCESS
  - DATASET_DENY
  - CATALOG_UPDATE
  - JOB_SUBMIT
  - JOB_EXECUTE
  - JOB_COMPLETE
  - SPOOL_ACCESS
  - SPOOL_PURGE
  - OPERATOR_COMMAND
  - AMF_LOAD
  - UPDATE_SECURITY_CRITICAL
  - PARTITION_OPERATION
  - DEVICE_ASSIGNMENT
  - GUARD_ROOT_TRANSITION
  - BREAK_GLASS
  - AUTHENTICATION
  - AUDIT_ADMIN
  - AUDIT_TAMPER
  - RECOVERY
```

Rules:

- `SECURITY_DENY`, `POLICY_CHANGE`, `BREAK_GLASS`, `AMF_LOAD`, `UPDATE_SECURITY_CRITICAL`, `PARTITION_OPERATION`, `DEVICE_ASSIGNMENT`, `GUARD_ROOT_TRANSITION`, and `AUDIT_TAMPER` are security-critical.
- Security-critical records MUST NOT be downgraded to diagnostic records.

### 9.1 Audit Record Types

`record_type` is the closed Phase 0.8 payload discriminator. `event_class` groups records for policy and retention; `record_type` selects required payload fields and reason-code expectations.

```yaml
AuditRecordType:
  - STREAM_CREATE
  - STREAM_ROLLOVER
  - SECURITY_DECISION
  - SECURITY_DENY
  - DATASET_ACCESS
  - DATASET_DENY
  - CATALOG_UPDATE
  - JOB_EVENT
  - SPOOL_EVENT
  - OPERATOR_COMMAND
  - POLICY_CHANGE
  - BREAK_GLASS
  - AMF_LOAD
  - UPDATE_EVENT
  - PARTITION_OPERATION
  - DEVICE_ASSIGNMENT
  - GUARD_ROOT_TRANSITION
  - AUDIT_QUERY
  - AUDIT_EXPORT
  - AUDIT_ADMIN
  - AUDIT_TAMPER
  - RECOVERY
```

Rules:

- Unknown `record_type` values are schema-invalid in Phase 0.8.
- Security-sensitive record types MUST use a security-capable audit stream.
- `SECURITY_DENY` and denial variants of resource-specific records MUST satisfy deny-before-return rules.
- `AUDIT_QUERY`, `AUDIT_EXPORT`, `AUDIT_ADMIN`, `AUDIT_TAMPER`, and `RECOVERY` are audit-service records and MUST be emitted by `auditd`, not by arbitrary callers.

### 9.2 Reason Code Registry

`reason_code` is a closed Phase 0.8 enum. It is not free-form text and MUST be preserved through query and export, subject only to authorized redaction of surrounding payload fields.

```yaml
AuditReasonCode:
  - AUD_RC_POLICY_ALLOW
  - AUD_RC_POLICY_DENY
  - AUD_RC_POLICY_MISSING
  - AUD_RC_POLICY_STALE
  - AUD_RC_POLICY_MALFORMED
  - AUD_RC_SUBJECT_UNKNOWN
  - AUD_RC_OBJECT_UNKNOWN
  - AUD_RC_OPERATION_INVALID
  - AUD_RC_OPERATION_UNSUPPORTED
  - AUD_RC_SPEC_GAP
  - AUD_RC_AUTHORITY_USED
  - AUD_RC_OBLIGATION_UNSATISFIED
  - AUD_RC_AUDIT_APPEND_REQUIRED
  - AUD_RC_AUDIT_APPEND_FAILED
  - AUD_RC_AUDIT_SCHEMA_INVALID
  - AUD_RC_AUDIT_CHAIN_MISMATCH
  - AUD_RC_AUDIT_STORE_FULL
  - AUD_RC_AUDIT_EXPORT_QUEUED
  - AUD_RC_AUDIT_EXPORT_FAILED
  - AUD_RC_AUDIT_QUERY_UNAUTHORIZED
  - AUD_RC_REDACTION_POLICY_MISSING
  - AUD_RC_RETENTION_DENIED
  - AUD_RC_GUARD_ROOT_REQUIRED
  - AUD_RC_GUARD_ROOT_FAILED
  - AUD_RC_RECOVERY_MODE
  - AUD_RC_BREAK_GLASS_OPEN
  - AUD_RC_BREAK_GLASS_EXPIRED
  - AUD_RC_UPDATE_SECURITY_EVENT
  - AUD_RC_PARTITION_POLICY_DENIED
  - AUD_RC_DEVICE_TEARDOWN_INCOMPLETE
```

Rules:

- Denials MUST use a reason code that distinguishes policy denial, missing policy, stale policy, malformed policy, unknown subject, unknown object, invalid operation, unsupported operation, or spec gap.
- Audit service failures MUST use audit-specific reason codes, not generic denial text.
- A human-readable explanation MAY appear in payload, but the canonical reason is the `reason_code` enum.

## 10. Audit Record Schema

```yaml
AuditObligationRef:
  obligation_id: string
  kind: AUDIT | MFA | DUAL_CONTROL | BREAK_GLASS | GUARD_APPROVAL | OPERATOR_CONFIRMATION | RATE_LIMIT | NOTIFY | REMOTE_EXPORT | LOCKDOWN
  required_before_return: bool
  required_before_effect: bool
  satisfied: bool
  failure_policy: FAIL_CLOSED | DEGRADED_READ_ONLY | RECOVERY_MODE
```

```yaml
AuditRecord:
  magic: "MFAR"
  evidence_kind: AUDIT_RECORD
  schema_version: uint16
  record_id: string
  stream_id: string
  record_seq: uint64
  timestamp_utc: Timestamp
  partition_id: PartitionId
  component_id: string
  profile: BASELINE | ENTERPRISE_STANDALONE | ENTERPRISE_PXM | HIGH_ASSURANCE | DEV
  record_type: AuditRecordType
  event_class: AuditClass
  correlation_id: CorrelationId
  parent_correlation_id: CorrelationId?
  request_id: string?
  decision_id: string?
  subject: AuditSubject
  object: AuditObject
  operation: string
  decision: ALLOW | DENY | ALLOW_WITH_AUDIT | REQUIRE_MFA | REQUIRE_DUAL_CONTROL | REQUIRE_BREAK_GLASS | REQUIRE_GUARD_APPROVAL | REQUIRE_OPERATOR_CONFIRMATION | UNSUPPORTED | SPEC_GAP | NONE
  reason_code: string
  policy_version: uint64?
  authority_used: [AuthorityClassId]
  obligations: [AuditObligationRef]
  activation_profile_hash: Digest?
  measurement_context: Digest?
  guard_root:
    root_type: string?
    root_version: uint64?
    root_digest: Digest?
    guard_measurement: Digest?
  payload_schema: string
  payload: map
  redaction_policy: string
  previous_hash: Digest
  payload_hash: Digest
  canonical_record_hash: Digest
  record_hash: Digest
  signature: Signature?
```

Rules:

- `magic`, `evidence_kind`, `schema_version`, `record_id`, `stream_id`, `record_seq`, `timestamp_utc`, `partition_id`, `component_id`, `profile`, `record_type`, `event_class`, `correlation_id`, `subject`, `object`, `operation`, `decision`, `reason_code`, `previous_hash`, `payload_hash`, `canonical_record_hash`, and `record_hash` are required.
- `policy_version` is required for authorization-related records.
- `decision_id` is required when recording a `securityd` decision result.
- `guard_root` fields are required for Guard root transition records.
- `payload` MUST be schema-bound and size-bounded.
- Unknown fields MUST be rejected unless a future schema version defines extension handling.

### 10.1 Correlation ID Semantics

`correlation_id` binds all audit records for one protected workflow: ingress request, `securityd` decision, deny or allow evidence, side-effect result, query/export record, and recovery record when applicable.

Rules:

- `correlation_id` MUST be created by a trusted ingress component, `securityd`, or `auditd`; it MUST NOT be trusted from unverified caller text.
- A caller-supplied request token MAY be preserved as `request_id`, but it is not the authoritative correlation ID.
- A workflow that forks into sub-operations MUST either preserve the original `correlation_id` or set `parent_correlation_id` to the original value.
- Records that prove deny-before-return ordering MUST share the same `correlation_id` as the denied protected operation.
- Query and export result evidence MUST include the query/export operation correlation ID and the referenced audit record range.

## 11. Audit Subject Schema

```yaml
AuditSubject:
  subject_id: string
  subject_type: HUMAN | SERVICE | JOB | PROGRAM | OPERATOR | PARTITION | SYSTEM | UNKNOWN
  principal_id: PrincipalId?
  effective_principal_id: PrincipalId?
  groups: [GroupId]
  roles: [RoleId]
  job_id: JobId?
  program_id: ProgramId?
  module_id: ModuleId?
  service_id: string?
  operator_session_id: string?
  partition_id: PartitionId?
  auth_strength: NONE | PASSWORD | MFA | CERTIFICATE | HARDWARE_BACKED | RECOVERY | UNKNOWN
  emergency_active: bool
```

Rules:

- Audit subject is copied from trusted authorization context, not caller-supplied text.
- `UNKNOWN` is allowed only for diagnostic or recovery records and MUST be reason-coded.

## 12. Audit Object Schema

```yaml
AuditObject:
  resource_type: DATASET | CATALOG | SPOOL | JOB | PROGRAM | AMF_MODULE | OPERATOR_COMMAND | PARTITION | DEVICE | AUDIT_STREAM | UPDATE_ARTIFACT | GUARD_ROOT | SECURITY_POLICY | WORKLOAD_POLICY | SYSTEM | UNKNOWN
  object_id: string
  object_name: string?
  owner_principal_id: PrincipalId?
  security_profile_id: PolicyId?
  generation: uint64?
  catalog_generation: uint64?
  partition_id: PartitionId?
```

Rules:

- Protected objects MUST be canonicalized before audit.
- `UNKNOWN` MUST NOT be used for normal protected-resource operations.

## 13. Hash Chain

Logical hash calculation:

```text
payload_hash = SHA384(canonical(payload))
canonical_record_hash = SHA384(canonical(record_without_signature_and_record_hash))
record_hash = SHA384(previous_hash || canonical_record_hash)
```

Rules:

- `previous_hash` MUST equal the prior committed record hash for the same stream.
- The first record in a stream MUST use a profile-defined genesis hash and a stream creation record.
- `record_hash` MUST be computed by `auditd`, not accepted from callers.
- Hash chain gaps MUST be detected during append and recovery.
- CRC or checksum MAY detect accidental corruption but MUST NOT be described as tamper resistance.

## 14. Canonicalization Rules

Until concrete encoding is specified:

- Field ordering MUST be deterministic.
- Numeric values MUST have a single canonical form.
- Timestamps MUST be UTC and normalized.
- Duplicate fields MUST be rejected.
- Unknown fields MUST be rejected.
- Optional absent fields and explicit null MUST NOT be treated as equivalent unless the schema declares it.
- Payload schemas MUST define their own canonicalization rules.

## 15. Append Protocol

```text
RECEIVE_AUDIT_REQUEST
  -> VALIDATE_CALLER_COMPONENT
  -> VALIDATE_SCHEMA
  -> VALIDATE_EVENT_CLASS
  -> ASSIGN_STREAM_AND_SEQUENCE
  -> CANONICALIZE_PAYLOAD
  -> COMPUTE_PAYLOAD_HASH
  -> COMPUTE_RECORD_HASH
  -> DURABLE_APPEND
  -> UPDATE_STREAM_HEAD
  -> EXPORT_IF_REQUIRED
  -> GUARD_APPEND_ROOT?      [High-Assurance]
  -> RETURN_AUDIT_REF
```

Failure states:

```text
CALLER_UNTRUSTED
SCHEMA_INVALID
EVENT_CLASS_INVALID
STREAM_UNAVAILABLE
SEQUENCE_CONFLICT
DURABLE_APPEND_FAILED
EXPORT_FAILED
GUARD_APPEND_FAILED
SPEC_GAP
UNSUPPORTED
```

Rules:

- Required pre-return audit MUST not return success until durable append completes.
- High-Assurance Guard append root MUST complete before claiming AUD-L4 evidence.
- Export failure behavior depends on profile and event class.

### 15.1 Deny-Before-Return Semantics

For protected resources, a DENY is not caller-visible until the required deny audit evidence is durable according to the active profile.

Required ordering:

```text
SECURITYD_DECISION_DENY
  -> BUILD_DENY_AUDIT_RECORD
  -> AUDITD_DURABLE_APPEND
  -> RECEIVE_AUDIT_RECORD_REF
  -> RETURN_DENY_TO_CALLER
```

Rules:

- If `AUDITD_DURABLE_APPEND` fails for a required deny record, the enforcement point MUST fail closed and return a typed audit-unavailable result, recovery-mode result, or lockdown result defined by profile.
- A failed required deny audit MUST NOT be reported as a successful ordinary denial.
- No protected handle, side effect, state mutation, spool entry, console line, or diagnostic log may substitute for the required deny `AuditRecord`.
- Deny records MUST include `record_type`, `event_class`, `subject`, `object`, `operation`, `decision`, `reason_code`, `policy_version` when applicable, `correlation_id`, and hash-chain fields.

## 16. Required Audit Obligations

| Operation family | Required audit |
| --- | --- |
| Security allow/deny for protected resources | Decision record, including subject, object, operation, reason, policy version. |
| Denied access | `SECURITY_DENY` before caller receives final denied result for protected resources. |
| Dataset open/create/delete/purge | Dataset access or deny record. |
| Catalog create/update/delete | Catalog update record with transaction ID. |
| Job submit/execute/complete/cancel | Job event with job ID, effective principal, class, return code if applicable. |
| Spool browse/export/purge/hold/release | Spool access or purge record. |
| Operator command | Parsed command ID, authority class, decision, confirmation/dual-control status. |
| Policy change | Precommit and commit records with old/new policy version. |
| Break-glass | Enable, every privileged use if required, and close/expiry records. |
| AMF load | Manifest digest, artifact digest, signer, authority class, decision, revocation status. |
| Update activation | Artifact ID, generation, security epoch, rollback/freeze/mix-and-match status. |
| Partition operation | Partition ID, activation profile hash, operation, result. |
| Device assignment | Device ID, IOMMU domain, interrupt remapping status, teardown completion. |
| Guard root transition | Root type, version, digest, Guard measurement, result. |
| Audit administration | Query/export/retention/purge attempts and results. |

## 17. Failure Policy by Profile

| Failure | Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance |
| --- | --- | --- | --- | --- |
| auditd unavailable at boot | Enter operator recovery mode only | Enter operator recovery mode; security operations fail closed | Enter operator recovery mode; security and partition operations fail closed | Boot stop or recovery mode |
| required deny audit append fails | Fail closed | Fail closed | Fail closed and alert | Fail closed and alert |
| local durable audit store full | Fail security-sensitive operations; allow configured non-security diagnostics | Fail security-sensitive operations and alert | Fail security-sensitive and partition operations; alert | Enter recovery or lockdown policy |
| remote export fails | Queue locally if capacity exists | Queue locally and alert | Queue locally and alert unless policy requires remote-first | Fail selected security-critical operations if policy requires remote-first |
| hash chain mismatch | Mark stream degraded and alert | Stop stream, recover from last good checkpoint, alert | Stop stream, recover from last good checkpoint, quarantine partition audit claims, alert | Lockdown or recovery mode; Guard mismatch if applicable |
| Guard append root fails | Not applicable | Optional helper failure; alert if configured | Optional helper failure; alert if configured | Fail Guard-root operation |
| audit query authorization unavailable | Deny query | Deny query | Deny query | Deny query |

Boot-time audit failure restrictions:

- Baseline recovery mode MUST NOT allow job submit, ordinary dataset open, policy update, AMF load, update activation, partition device assignment, or operator destructive commands.
- Baseline recovery mode MAY access explicitly marked recovery datasets only through recovery commands that are authorized by immutable boot policy and later reconciled with auditd.
- Enterprise recovery mode MUST preserve measured-boot evidence and remote-export backlog state before returning to normal operations.
- High-Assurance MUST NOT enter normal operations when Guard-sealed audit root is required and unavailable.

## 18. Query and Export Authorization

Rules:

- Audit query and export are protected operations on `AUDIT_STREAM`.
- `auditd` MUST request `securityd` authorization for query, export, retention update, stream seal, and stream retire.
- Query results MUST apply redaction policy.
- Redaction MUST NOT alter stored committed records.
- Export MUST preserve record hash and sequence.
- Exported records MUST include enough stream metadata to verify chain continuity.
- Unauthorized query/export attempts MUST be denied before any protected record content is returned.
- Query/export attempts and results MUST themselves be audit records when auditd can append.

Query lifecycle:

```text
REQUEST_QUERY
  -> SECURITYD_AUTHORIZE_QUERY
  -> APPLY_SCOPE
  -> APPLY_REDACTION
  -> AUDIT_QUERY_EVENT
  -> RETURN_RESULTS
```

Export lifecycle:

```text
REQUEST_EXPORT
  -> SECURITYD_AUTHORIZE_EXPORT
  -> SELECT_RECORD_RANGE
  -> VERIFY_CHAIN_RANGE
  -> APPLY_EXPORT_POLICY
  -> AUDIT_EXPORT_EVENT
  -> TRANSMIT_OR_STAGE
  -> RECORD_EXPORT_RESULT
```

### 18.1 Redaction Policy

Redaction is a view transform for query and export only. It is never a mutation of committed records.

```yaml
RedactionMode:
  - REDACT_NONE
  - REDACT_SUBJECT_IDENTIFIERS
  - REDACT_OBJECT_NAMES
  - REDACT_PAYLOAD_FIELDS
  - REDACT_EXPORT_MINIMAL
  - REDACT_DENY
```

Rules:

- `REDACT_NONE` is allowed only after `securityd` authorizes the subject for unredacted audit access.
- Redaction MUST preserve `record_id`, `stream_id`, `record_seq`, `record_type`, `event_class`, `decision`, `reason_code`, `correlation_id`, `previous_hash`, `payload_hash`, `canonical_record_hash`, and `record_hash` unless the query itself is denied.
- A redacted view MUST include metadata that identifies the redaction policy used.
- A missing redaction policy for sensitive records MUST deny query/export rather than return unredacted data by default.
- Redaction MUST NOT be used to hide audit tamper, missing records, hash-chain gaps, or denied security events from authorized security review.

### 18.2 Remote Export Placeholder

Enterprise-Standalone, Enterprise-PXM, and High-Assurance profiles require remote export capability, but Phase 0.8 does not specify the transport protocol, collector trust model, collector identity, retry encoding, or long-term archive format.

Rules:

- Local durable append remains the primary audit evidence path unless a future approved profile defines an external authoritative path.
- A remote export receipt is not audit evidence unless it references a verified local stream range and preserves sequence and hash metadata.
- An unimplemented export transport MUST return `MFOS_ERR_UNSUPPORTED`.
- An undefined export transport or collector trust model MUST return `MFOS_ERR_SPEC_GAP`.
- Export failure behavior follows the profile failure-policy table and MUST create an `AUDIT_EXPORT` or `AUDIT_TAMPER` record when append remains possible.

## 19. Retention and Sealing

```yaml
RetentionPolicy:
  retention_policy_id: string
  min_retention_days: uint32
  max_retention_days: uint32?
  legal_hold_supported: bool
  purge_requires_dual_control: bool
  guard_seal_required: bool
```

Rules:

- Retention expiry permits purge consideration; it does not force purge.
- Security-critical audit purge MUST require authorization and audit.
- High-Assurance audit stream sealing MUST bind stream head hash to a Guard root when required.
- Retention policy changes MUST be audited.

### 19.1 Guard Audit Root Placeholder

High-Assurance audit-root sealing is required, but Phase 0.8 does not define Guard call ABI, attestation claim format, key hierarchy, or root storage internals.

Rules:

- Baseline, Enterprise-Standalone, and Enterprise-PXM MAY carry `guard_root` as absent/null and MUST NOT claim AUD-L4 evidence from it.
- High-Assurance Guard audit-root records MUST use `record_type: GUARD_ROOT_TRANSITION` and event class `GUARD_ROOT_TRANSITION`.
- A High-Assurance claim that an audit root is sealed or verified is invalid unless the relevant `AuditRecord` has `guard_root.root_type`, `guard_root.root_version`, `guard_root.root_digest`, and `guard_root.guard_measurement`.
- Guard append failure for a required audit root MUST fail the Guard-root operation closed.
- The concrete Guard ABI is a spec gap; implementations MUST NOT invent a success path from this placeholder.

## 20. Recovery

Recovery lifecycle:

```text
START_RECOVERY
  -> OPEN_STREAM_METADATA
  -> SCAN_RECORDS
  -> VERIFY_SEQUENCE
  -> VERIFY_HASH_CHAIN
  -> IDENTIFY_LAST_GOOD_RECORD
  -> MARK_CORRUPT_RANGE
  -> WRITE_RECOVERY_RECORD
  -> EXPORT_ALERT
  -> RESUME_OR_SEAL_DEGRADED
```

Rules:

- Recovery MUST NOT rewrite committed records to hide corruption.
- Recovery records MUST identify last good sequence and detected corrupt range.
- If the stream head was Guard-sealed, recovery MUST compare local head with Guard root.

## 21. Record Payload Profiles

### 21.1 Security Decision Payload

```yaml
SecurityDecisionPayload:
  decision_id: string
  request_id: string
  matched_rules: [string]
  obligations: [string]
  handle_constraints: map
  cache_allowed: bool
```

### 21.2 Dataset Access Payload

```yaml
DatasetAccessPayload:
  dsn: string
  dataset_generation: uint64
  catalog_generation: uint64
  disposition: SHR | OLD | NEW | MOD | SYSOUT
  handle_id: string?
```

### 21.3 Job Event Payload

```yaml
JobEventPayload:
  job_id: JobId
  job_name: string
  job_class: string
  service_class: string
  step_name: string?
  return_code: int?
  abend_reason: string?
```

### 21.4 Operator Command Payload

```yaml
OperatorCommandPayload:
  command_id: string
  command_name: string
  parsed_arguments_digest: Digest
  destructive: bool
  confirmation_satisfied: bool
  dual_control_satisfied: bool
  automation: bool
```

### 21.5 AMF Load Payload

```yaml
AmfLoadPayload:
  module_id: ModuleId
  manifest_digest: Digest
  artifact_digest: Digest
  signer: string
  authority_class: AuthorityClassId
  revocation_status: CLEAR | REVOKED | UNKNOWN
  guard_approval: bool?
```

### 21.6 Update Payload

```yaml
UpdatePayload:
  artifact_id: UpdateArtifactId
  component_id: string
  component_version: string
  generation: uint64
  security_epoch: uint64
  rollback_detected: bool
  freeze_detected: bool
  mix_and_match_detected: bool
```

### 21.7 Guard Root Payload

```yaml
GuardRootPayload:
  root_type: string
  old_version: uint64?
  new_version: uint64
  root_digest: Digest
  guard_measurement: Digest
  transition: SEAL | VERIFY | MISMATCH | RETIRE
```

## 22. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-AUDIT-0001 | Security decisions MUST carry audit obligations. | traceability audit |
| MFOS-REQ-AUDIT-0002 | Required deny audit MUST be emitted before caller receives final denied result. | negative test |
| MFOS-REQ-AUDIT-0003 | Audit record MUST include schema version, record ID, sequence, timestamp, subject, object, operation, decision, reason code, and hashes. | schema test |
| MFOS-REQ-AUDIT-0004 | Audit stream MUST provide a hash chain at AUD-L2 and above. | tamper test |
| MFOS-REQ-AUDIT-0005 | Audit failure policy MUST be defined per profile. | fault injection |
| MFOS-REQ-AUDIT-0006 | Enterprise-Standalone, Enterprise-PXM, and High-Assurance profiles MUST implement remote export capability. | integration test |
| MFOS-REQ-AUDIT-0007 | High-Assurance profile MUST bind audit root to Guard evidence. | Guard test |
| MFOS-REQ-AUDIT-0008 | Spool output MUST NOT be treated as audit evidence. | documentation review |
| MFOS-REQ-AUDIT-0009 | Audit query/export MUST be authorized through `securityd`. | security test |
| MFOS-REQ-AUDIT-0010 | Redaction MUST affect query/export views only, not committed records. | query test |
| MFOS-REQ-AUDIT-0011 | Hash chain mismatch MUST be detected during append or recovery. | tamper test |
| MFOS-REQ-AUDIT-0012 | Required audit records MUST be schema-bound and size-bounded. | fuzz/schema test |
| MFOS-REQ-AUDIT-0013 | Audit stream rollover MUST preserve chain continuity. | rollover test |
| MFOS-REQ-AUDIT-0014 | Recovery MUST not rewrite committed records to hide corruption. | crash recovery test |
| MFOS-REQ-AUDIT-0015 | Guard root transition records MUST include root type, version, digest, and measurement context. | Guard integration test |

## 23. Invariants

```text
INV-AUD-001:
  For a required pre-return audit obligation, the caller cannot receive final
  operation result until auditd returns a durable AuditRecordRef or the
  operation fails closed.

INV-AUD-002:
  record_hash for stream sequence N MUST include previous_hash from sequence
  N-1 and the canonical hash of record N.

INV-AUD-003:
  auditd computes record hashes; callers cannot supply authoritative hashes.

INV-AUD-004:
  Redaction cannot modify committed records.

INV-AUD-005:
  Audit query, export, retention change, stream seal, and stream retire are
  protected operations requiring securityd authorization.

INV-AUD-006:
  Security-critical audit events cannot be downgraded to diagnostic console
  output or spool output.

INV-AUD-007:
  High-Assurance audit root claims cannot exist unless Guard sealed or
  verified the stream root for the relevant version.

INV-AUD-008:
  Recovery cannot hide gaps, mismatches, or corrupt ranges; it MUST emit
  recovery or tamper records.

INV-AUD-009:
  Remote export does not replace local durable append unless a future profile
  explicitly specifies an OOB authoritative path.

INV-AUD-010:
  SPEC_GAP and UNSUPPORTED audit paths MUST NOT return evidence success.
```

## 24. Failure Modes

| Failure | Required behavior |
| --- | --- |
| Caller untrusted | Reject append; audit meta-event if possible. |
| Schema invalid | Reject append; no partial record. |
| Payload too large | Reject append with bounded error. |
| Unknown event class | `MFOS_ERR_SPEC_GAP` unless class is specified but unimplemented. |
| Specified class unimplemented | `MFOS_ERR_UNSUPPORTED`. |
| Sequence conflict | Retry with lock or fail closed for required audit. |
| Durable append failure | Follow profile failure policy; security-critical operations fail closed. |
| Hash chain mismatch | Mark stream degraded, alert, enter recovery or lockdown per profile. |
| Remote export failure | Queue or fail according to profile and event class. |
| Guard append failure | High-Assurance Guard-root operation fails closed. |
| Query unauthorized | Deny and audit if possible. |
| Redaction policy missing | Deny query/export for sensitive records. |
| Retention purge unauthorized | Deny purge and audit. |
| Time source unavailable | Continue with monotonic sequence; mark timestamp uncertainty or fail profile-specific expiry-sensitive events. |

### 24.1 Audit Append State Machine

The Phase 0.8 design state machine is captured in `formal/tla/audit-append/AuditAppend.tla`.

```text
IDLE
  -> RECEIVED
  -> VALIDATED
  -> SEQUENCED
  -> HASHED
  -> DURABLE
  -> EXPORT_PENDING?        [profile/export policy]
  -> EXPORTED?              [successful export]
  -> GUARD_PENDING?         [High-Assurance audit root]
  -> GUARDED?               [High-Assurance audit root]
  -> RETURNED
```

Failure and recovery states:

```text
REJECTED
FAILED_CLOSED
DEGRADED
RECOVERING
SEALED
```

Rules:

- `RECEIVED` to `RETURNED` is valid only for non-required diagnostic records rejected before evidence claim; it is invalid for required audit.
- Required audit must pass through `DURABLE` before `RETURNED`.
- AUD-L3 claim requires `EXPORTED` or an explicit queued/export-failed record allowed by profile.
- AUD-L4 claim requires `GUARDED`.
- `DEGRADED` streams cannot produce new security-critical evidence until recovery policy allows resume or creates a new stream with rollover evidence.
- `SEALED` streams reject ordinary append except recovery metadata explicitly allowed by retention/recovery policy.

### 24.2 Invalid Transitions

The following transitions are prohibited and require negative tests:

| Invalid transition | Required result |
| --- | --- |
| `RECEIVED -> RETURNED` for required deny audit | Fail closed; no caller-visible DENY result. |
| `VALIDATED -> DURABLE` without sequence assignment | Reject append or fail closed for required audit. |
| `SEQUENCED -> DURABLE` without canonical hash calculation | Reject append or fail closed for required audit. |
| `DURABLE -> HASHED` after commit | Invalid; hash must be computed before durable append. |
| `REJECTED -> RETURNED_SUCCESS` | Invalid; rejected evidence cannot satisfy an obligation. |
| `DEGRADED -> AUD_L4_CLAIMED` | Invalid; Guard-backed evidence claim must fail. |
| `GUARD_PENDING -> RETURNED_AUD_L4` | Invalid; High-Assurance root operation fails closed. |
| `QUERY_REQUESTED -> RESULTS_RETURNED` without `securityd` authorization | Deny query; audit if possible. |
| `REDACTED_VIEW -> COMMITTED_RECORD_MUTATED` | Invalid; committed records are immutable. |
| `EXPORT_PENDING -> EXPORTED` without chain verification | Invalid; export fails and records failure when possible. |
| `SEALED -> ORDINARY_APPEND` | Reject append; use new stream or approved recovery record. |

## 25. Positive Tests

| Test ID | Description |
| --- | --- |
| TEST-MFOS-AUDIT-POS-0001 | Append valid security decision record and receive `AuditRecordRef`. |
| TEST-MFOS-AUDIT-POS-0002 | Append DENY record before returning denial to caller. |
| TEST-MFOS-AUDIT-POS-0003 | Verify hash chain across multiple records. |
| TEST-MFOS-AUDIT-POS-0004 | Append dataset open allow record with dataset and catalog generation. |
| TEST-MFOS-AUDIT-POS-0005 | Append job submit and job complete records with same correlation ID. |
| TEST-MFOS-AUDIT-POS-0006 | Append operator command record with confirmation status. |
| TEST-MFOS-AUDIT-POS-0007 | Authorize audit query and return redacted view. |
| TEST-MFOS-AUDIT-POS-0008 | Export a verified record range with stream metadata. |
| TEST-MFOS-AUDIT-POS-0009 | Rollover stream while preserving chain continuity. |
| TEST-MFOS-AUDIT-POS-0010 | Seal audit root through Guard in High-Assurance design test mode. |

## 26. Negative Tests

| Test ID | Description |
| --- | --- |
| NEG-MFOS-AUDIT-DENY-BEFORE-RETURN-0001 | Required deny audit append fails; caller MUST receive audit-unavailable error, not original denial success. |
| NEG-MFOS-AUDIT-FORGED-HASH-0002 | Caller supplies forged `record_hash`; auditd recomputes and rejects mismatch. |
| NEG-MFOS-AUDIT-SCHEMA-MISSING-FIELD-0003 | Missing required field in audit record; expect schema rejection. |
| NEG-MFOS-AUDIT-DUPLICATE-FIELD-0004 | Duplicate field in canonical input; expect schema rejection. |
| NEG-MFOS-AUDIT-SPOOL-AS-EVIDENCE-0005 | Spool output or spool entry presented as audit evidence; expect rejection. |
| NEG-MFOS-AUDIT-LOG-AS-EVIDENCE-0006 | Diagnostic log line or console line presented as audit evidence; expect rejection. |
| NEG-MFOS-AUDIT-QUERY-UNAUTHORIZED-0007 | Query audit stream without `securityd` authorization; expect denial. |
| NEG-MFOS-AUDIT-EXPORT-REDACTION-MISSING-0008 | Export sensitive record without redaction policy; expect denial. |
| NEG-MFOS-AUDIT-TAMPER-MIDDLE-0009 | Tamper with middle record; chain verification detects mismatch. |
| NEG-MFOS-AUDIT-SEQUENCE-GAP-0010 | Remove a record; sequence verification detects gap. |
| NEG-MFOS-AUDIT-REMOTE-EXPORT-FAIL-0011 | Remote export fails for Enterprise stream; local queue and alert behavior verified. |
| NEG-MFOS-AUDIT-GUARD-ROOT-MISSING-0012 | Guard required but unavailable for High-Assurance audit root; expect fail closed. |
| NEG-MFOS-AUDIT-RETENTION-PURGE-0013 | Attempt retention purge before expiry or without required dual control; expect denial and audit. |
| NEG-MFOS-AUDIT-UNKNOWN-RECORD-TYPE-0014 | Unknown event class or record type; expect `MFOS_ERR_SPEC_GAP` or schema rejection according to field. |
| NEG-MFOS-AUDIT-UNSUPPORTED-EXPORT-0015 | Unimplemented export transport; expect `MFOS_ERR_UNSUPPORTED`. |
| NEG-MFOS-AUDIT-INVALID-TRANSITION-0016 | Attempt invalid append/query/export state transition; expect rejection or fail closed. |

## 27. Fuzz Targets

| Fuzz ID | Target |
| --- | --- |
| TEST-MFOS-AUDIT-FUZZ-0001 | AuditRecord parser and canonicalizer. |
| TEST-MFOS-AUDIT-FUZZ-0002 | Audit payload parser for security decision events. |
| TEST-MFOS-AUDIT-FUZZ-0003 | Dataset access payload parser. |
| TEST-MFOS-AUDIT-FUZZ-0004 | Job event payload parser. |
| TEST-MFOS-AUDIT-FUZZ-0005 | Operator command payload parser. |
| TEST-MFOS-AUDIT-FUZZ-0006 | AMF load payload parser. |
| TEST-MFOS-AUDIT-FUZZ-0007 | Update payload parser. |
| TEST-MFOS-AUDIT-FUZZ-0008 | Guard root payload parser. |
| TEST-MFOS-AUDIT-FUZZ-0009 | Stream metadata parser and rollover record parser. |
| TEST-MFOS-AUDIT-FUZZ-0010 | Query filter and redaction policy parser. |
| TEST-MFOS-AUDIT-FUZZ-0011 | Duplicate field, unknown field, oversized payload, invalid enum, and timestamp normalization handling. |

## 28. Evidence Requirements

Phase 0.8 evidence is planned design evidence, not release evidence.

Required evidence classes:

- Schema evidence: validation of positive and negative `AuditRecord` fixtures against `schemas/mfos/audit-record.schema.yml`.
- Ordering evidence: trace showing required deny audit durable append before caller-visible result.
- Hash-chain evidence: stream sequence, `previous_hash`, `canonical_record_hash`, and `record_hash` verification across valid, tampered, removed, and rollover cases.
- Failure-policy evidence: fault-injection traces for auditd unavailable, local store full, remote export failure, Guard append failure, and query authorization unavailable.
- Query/redaction evidence: authorized and unauthorized query/export attempts with redacted views and immutable committed records.
- State-machine evidence: review or model-check output for `formal/tla/audit-append/AuditAppend.tla`.
- Guard placeholder evidence: High-Assurance claims remain blocked unless Guard audit-root fields and Guard state-machine evidence exist.
- Remote export placeholder evidence: export protocol gaps return `MFOS_ERR_SPEC_GAP` and unimplemented transports return `MFOS_ERR_UNSUPPORTED`.

Evidence records MUST include requirement IDs, test IDs, stream ID, sequence range, record hashes, correlation IDs, profile, result, and artifact path. A log line, console line, spool entry, spool output, or unverified remote receipt MUST NOT be accepted as audit evidence.

## 29. Spec Gaps

| Gap ID | Gap |
| --- | --- |
| AUD-GAP-001 | Concrete canonical serialization format is not fixed. |
| AUD-GAP-002 | Final signature algorithms and key hierarchy are not fixed. |
| AUD-GAP-003 | Remote export protocol and collector trust model are not specified. |
| AUD-GAP-004 | Audit storage physical format and crash-consistency mechanism are not specified. |
| AUD-GAP-005 | Exact stream rollover and archival format need a dedicated spec. |
| AUD-GAP-006 | Redaction policy language is not yet fixed. |
| AUD-GAP-007 | Time-source trust policy by profile needs a dedicated spec. |
| AUD-GAP-008 | Guard call payload and attestation claim format belong in Guard spec. |
| AUD-GAP-009 | AUD-L5 external/OOB authoritative audit path is intentionally deferred. |
| AUD-GAP-010 | Privacy policy for personally identifiable audit fields is not yet specified. |
| AUD-GAP-011 | Requirement registry entries for all audit IDs still need synchronization outside this owned Phase 0.8 artifact set. |
| AUD-GAP-012 | Production encoders, decoders, storage writers, and export clients are not specified here and remain blocked. |
| AUD-GAP-013 | Final audit-query role taxonomy and operator delegation policy belong with securityd policy profiles. |
| AUD-GAP-014 | Exact MFOS error-code mapping for audit failure, unsupported export, and spec-gap transport is not final. |

## 30. Phase 0.8 Implementation Gate

This design freeze does not permit production code. Before implementation work begins, an implementation task must identify:

1. The exact requirement IDs implemented.
2. The `AuditRecord` schema version and canonical serialization.
3. The source matrix IDs used for any externally inspired semantics.
4. The remaining spec gaps and unsupported features.
5. The state-machine evidence and negative tests proving deny-before-return, hash-chain integrity, query authorization, redaction immutability, remote export failure policy, and Guard audit-root behavior.
6. The evidence artifact locations and reviewer sign-off required for the claimed profile.

## Phase 0.8 Core Semantics Freeze

This section freezes the Audit semantics for Phase 0.8. It is a design-level freeze only and does not authorize production implementation, hosted daemon implementation, Portable Semantic Core implementation, or executable specs.

### Frozen Requirement Set

The authoritative Phase 0.8 audit evidence semantics in this file are the
`MFOS-REQ-AUDIT-0001` through `MFOS-REQ-AUDIT-0015` requirements in Section 22.
The bridge IDs below are a core-freeze scaffold and do not authorize
implementation or profile claims until the requirement registry is synchronized.

- `MFOS-REQ-AUDIT-0101`
- `MFOS-REQ-AUDIT-0102`
- `MFOS-REQ-AUDIT-0103`
- `MFOS-REQ-AUDIT-0104`
- `MFOS-REQ-AUDIT-0105`

### Machine-Readable Artifacts

- Pack contract: `docs/design/packs/PACK-06-*/pack.yml`
- State machine: `formal/tla/audit-append/state-machine.yml`
- Test catalog: `tests/catalog/archive/phase-0-8/*`
- Requirement mirror: `requirements/by-domain/`
- Evidence traceability: `evidence/traceability/archive/phase-0-8/*`

### Freeze Rules

- Undefined behavior returns `MFOS_ERR_SPEC_GAP`.
- Specified but unimplemented behavior returns `MFOS_ERR_UNSUPPORTED`.
- Deny paths with audit obligations must define deny-before-return behavior.
- Security-sensitive behavior requires a negative test catalog entry.
- No fake success, empty stub, or silent fallback is allowed.
