---
spec_id: "MFOS-SPEC-05-OBJECT-MODEL"
title: "MFOS Core Object Model Specification v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001", "EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001", "EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001", "EXTREF-IBM-Z-DPM-0001", "EXTREF-IBM-ZOS-JES-INTRODUCTION-0001", "EXTREF-IBM-ZOS-JES-JOB-FLOW-0001", "EXTREF-IBM-Z-LPAR-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001", "EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001", "TUF-001"]
requirement_refs: ["MFOS-REQ-OBJ-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Core Object Model Specification v0.1

Status: Draft design split

Owner area: `docs/design/specs/05-object-model.md`

This document defines the first-class objects that all MFOS services must use. It is source-grounded and AI-friendly: every schema has explicit identity, ownership, lifecycle, authorization hooks, audit obligations, invariants, failure modes, and test expectations.

MFOS is a z/OS-inspired enterprise operating system design. It does not claim compatibility with IBM products, z/Architecture binaries, z/OS APIs, RACF, JES, DFSMS, SMF, or JCL.

## 1. Purpose

The object model is the shared contract for:

- `securityd` authorization input and protected resource profiles.
- `auditd` evidence records.
- `catalogd` and `datasetd` managed storage semantics.
- `jobd` job lifecycle and effective identity.
- `spoold` protected SYSIN/SYSOUT resources.
- `operatord` command grammar, authority, and audit.
- `workpolicyd` job class and service class metadata.
- `amfd` authorized module identity and authority class.
- `uvsd` update artifact and rollback control.
- `PXM` partition identity and activation profile linkage.
- `PXM Guard` root objects in the High-Assurance profile.

The model is deliberately not a POSIX file/process/user model. POSIX-like objects may be added later as an optional subsystem, but they must not bypass the objects defined here.

## 2. Scope

This specification defines:

- Canonical object identifiers.
- Common scalar types.
- Core schemas.
- Object lifecycle states.
- Handle binding rules.
- Cross-object references.
- Required authorization and audit hooks.
- Invariants and failure behavior.
- Positive tests, negative tests, and fuzz targets.

This specification does not define:

- Concrete on-disk encoding.
- RPC transport.
- Full operator command grammar.
- Full policy language.
- Full dataset access methods.
- Kernel ABI details.
- Cryptographic library implementation.
- External identity provider integration.

## 3. Source Matrix References

The following source IDs are inherited from the MFOS architecture source matrix.

| Source ID | Object-model use |
| --- | --- |
| EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001 | System integrity boundary and unauthorized-circumvention model. |
| EXTREF-IBM-ZOS-SECURITY-SERVER-0001 | Security manager, profile, principal, and audit-administration concepts. |
| EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001 | User, group, protected resource, access list, and default access mapping. |
| EXTREF-IBM-ZOS-JES-INTRODUCTION-0001 | Job, queue, initiator, SYSIN, SYSOUT, and spool concepts. |
| EXTREF-IBM-ZOS-JES-JOB-FLOW-0001 | Job flow state inspiration for job lifecycle objects. |
| EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001 | Catalog entry as dataset attributes plus location. |
| EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001 | Dataset allocation, catalog, storage administration, and data set use concepts. |
| EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | Audit/accounting record purpose and system/job-related information. |
| EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001 | Security audit record fields for denied and authorized security events. |
| EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001 | Service class, report class, workload goal, and importance metadata. |
| EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001 | Authorized program mapping to AMF identity and authority class. |
| EXTREF-IBM-Z-LPAR-INTRODUCTION-0001 | Partition, activation profile, logical CPU, memory, and I/O assignment concepts. |
| EXTREF-IBM-Z-DPM-0001 | Object-oriented partition management-plane inspiration. |
| TUF-001 | Update artifact role separation and rollback/freeze resistance. |
| FBVBS-001 | Requirement traceability, state machines, no fake success, and evidence discipline. |

## 4. Normative Language

Keywords in this document have the following meanings:

- `MUST`: required for the applicable profile.
- `SHOULD`: strongly recommended; deviation requires an ADR and evidence.
- `MAY`: optional and not automatically part of an assurance claim.
- `MUST NOT`: prohibited.
- `SPEC_GAP`: undefined behavior that must not be implemented as a successful operation.
- `UNSUPPORTED`: specified behavior not yet implemented; it must fail closed.

## 5. Design Principles

1. Every protected object MUST have a stable object identity.
2. Every protected object MUST have an owner or explicitly state why ownership is not applicable.
3. Every protected object MUST be authorized through `securityd` before access.
4. Every security-sensitive object transition MUST produce an audit obligation.
5. An object handle MUST bind subject, object, operation, policy version, and generation.
6. A stale handle MUST fail closed.
7. Dataset objects MUST NOT be reduced to POSIX path wrappers.
8. Operator commands MUST be first-class protected objects, not shell strings.
9. AMF authority MUST be module authority, not administrator privilege.
10. PXM and Guard objects MUST remain separate from MFOS enterprise objects.
11. Unknown fields in production input MUST be rejected unless the schema explicitly declares forward-compatible extension handling.
12. A missing object, malformed object, unsupported object class, or undefined object class MUST NOT produce success.

## 6. Common Types

### 6.1 Identifiers

```yaml
IdentifierRules:
  PrincipalId: "PRN-[A-Z0-9][A-Z0-9._-]{0,63}"
  GroupId: "GRP-[A-Z0-9][A-Z0-9._-]{0,63}"
  RoleId: "ROL-[A-Z0-9][A-Z0-9._-]{0,63}"
  JobId: "JOB-[A-Z0-9]{8,32}"
  DatasetName: "MFOS DSN grammar; see dataset/catalog spec"
  CatalogEntryId: "CAT-[A-F0-9]{32}"
  SpoolId: "SPL-[A-F0-9]{32}"
  ProgramId: "PGM-[A-F0-9]{32}"
  ModuleId: "AMF-[A-F0-9]{32}"
  PolicyId: "POL-[A-F0-9]{32}"
  PartitionId: "PXM-[A-F0-9]{16}"
  GuardRootId: "GRD-[A-F0-9]{32}"
  UpdateArtifactId: "UPD-[A-F0-9]{32}"
  CorrelationId: "UUIDv7 preferred"
```

Rules:

- IDs generated by MFOS services MUST be collision-resistant within the deployment.
- User-supplied names MUST NOT be accepted as internal object IDs unless explicitly typed as external names.
- All IDs stored in audit records MUST be canonical.
- Object IDs MUST NOT encode secrets.

### 6.2 Hashes and Signatures

```yaml
Digest:
  algorithm: SHA384
  value: hex

Signature:
  algorithm: string
  key_id: string
  value: base64
  signed_payload_digest: Digest
```

Rules:

- SHA-384 is the baseline digest for identity and audit-chain fields.
- Alternative digest algorithms require a profile-specific cryptographic policy.
- A digest is not an authorization decision.
- A signature is not an authorization decision.

### 6.3 Time

```yaml
Timestamp:
  value: RFC3339_UTC
  source: MONOTONIC_KERNEL | TPM_TIME | NETWORK_TIME | OPERATOR_ENTERED | UNKNOWN
  uncertainty_ms: uint64
```

Rules:

- Audit ordering MUST use monotonic sequence numbers in addition to timestamps.
- Expiry decisions MUST fail closed if time cannot be trusted for the active profile.
- User-provided timestamps MUST NOT override service-generated timestamps.

### 6.4 Profile Applicability

```yaml
ConformanceProfile:
  - Baseline
  - Enterprise
  - High-Assurance
```

Rules:

- Object fields marked High-Assurance-only MAY be absent in Baseline and Enterprise.
- High-Assurance root object claims MUST be tied to Guard evidence.

### 6.5 Policy Binding

`PolicyBinding` is the common object used to bind handles, command approvals,
load approvals, and protected transitions to the exact `securityd` decision
that authorized them.

```yaml
PolicyBinding:
  policy_version: uint64
  decision_id: string
  decision_time: Timestamp
  valid_until: Timestamp?
  obligations_hash: Digest
  decision_result: ALLOW | ALLOW_WITH_AUDIT
```

Rules:

- A `PolicyBinding` MUST reference an existing `SecurityDecision`.
- A `PolicyBinding` MUST NOT be fabricated by the enforcement point.
- If `valid_until` has expired, the bound handle or approval MUST fail closed.
- `obligations_hash` MUST bind the obligations that the enforcement point must satisfy.
- `DENY`, `UNSUPPORTED`, and `SPEC_GAP` decisions MUST NOT produce a successful `PolicyBinding`.

### 6.6 Object Generation Binding

`ObjectGenerationBinding` is the common generation snapshot used to reject stale
handles and stale authorizations.

```yaml
ObjectGenerationBinding:
  catalog_entry_generation: uint64?
  dataset_generation: uint64?
  spool_generation: uint64?
  security_policy_generation: uint64?
  workload_policy_generation: uint64?
  amf_registry_generation: uint64?
  guard_root_generation: uint64?
  activation_profile_generation: uint64?
  update_artifact_generation: uint64?
```

Rules:

- A generation field MUST be present when the target object type has a generation.
- A stale generation MUST fail with the object-specific stale or mismatch error.
- Generation comparison MUST use committed object state, not caller-supplied state.
- Missing generation on a generation-aware protected object MUST fail closed.

## 7. Core Schemas

All schemas are logical schemas. Concrete serialization is a separate specification.

### 7.1 Principal

```yaml
Principal:
  principal_id: PrincipalId
  display_name: string
  auth_methods:
    - PASSWORD
    - CERTIFICATE
    - KERBEROS
    - PASSKEY
    - MFA_TOKEN
    - OPERATOR_CONSOLE
  groups: [GroupId]
  roles: [RoleId]
  labels: [string]
  status: ACTIVE | DISABLED | LOCKED | EXPIRED | EMERGENCY_ONLY
  created_at: Timestamp
  updated_at: Timestamp
  expiry: Timestamp?
  emergency_flags:
    break_glass_allowed: bool
    emergency_expiry: Timestamp?
    emergency_reason_required: bool
  security_profile: SecurityProfileRef?
  audit_subject_class: HUMAN | SERVICE | JOB_EFFECTIVE | SYSTEM | PARTITION
```

Authorization hooks:

- Create, update, disable, unlock, and emergency-mode changes MUST be authorized by `securityd`.
- Authentication success is not authorization success.

Audit obligations:

- Principal lifecycle changes MUST emit audit records.
- Failed authentication MAY be rate-limited but MUST remain auditable in Enterprise-Standalone, Enterprise-PXM, and High-Assurance profiles.
- Break-glass use MUST be audited before privileged access is granted.

### 7.2 Group

```yaml
Group:
  group_id: GroupId
  display_name: string
  members: [PrincipalId]
  nested_groups: [GroupId]
  status: ACTIVE | DISABLED
  owner: PrincipalId
  created_at: Timestamp
  updated_at: Timestamp
```

Rules:

- Cyclic group membership MUST be rejected.
- Group changes MUST create a new policy version if they affect authorization decisions.

### 7.3 Role

```yaml
Role:
  role_id: RoleId
  display_name: string
  authority_classes: [AuthorityClassId]
  assignable_by: [RoleId]
  status: ACTIVE | DISABLED
  created_at: Timestamp
  updated_at: Timestamp
```

Rules:

- Role assignment MUST NOT imply AMF authorization unless an explicit authority class allows it.
- Role delegation MUST be auditable.

### 7.4 AuthorityClass

```yaml
AuthorityClass:
  authority_class_id: string
  purpose: string
  allowed_resource_types: [ResourceType]
  allowed_operations: [Operation]
  profile_applicability: [ConformanceProfile]
  requires_dual_control: bool
  requires_guard_approval: bool
  audit_class: AuditClass
```

Rules:

- Authority class is narrower than administrator privilege.
- AMF authority classes MUST be explicit and revocable.

### 7.5 SecurityDecision

`SecurityDecision` is the canonical authorization result produced by `securityd`.
It is not a log message and not a caller assertion. Enforcement points use it to
create `PolicyBinding` objects and to satisfy audit obligations.

```yaml
SecurityDecision:
  decision_id: string
  subject: SubjectRef
  object: ObjectRef
  operation: Operation
  context: DecisionContext
  result: ALLOW | DENY | ALLOW_WITH_AUDIT | REQUIRE_MFA | REQUIRE_DUAL_CONTROL | REQUIRE_BREAK_GLASS | REQUIRE_GUARD_APPROVAL | REQUIRE_OPERATOR_CONFIRMATION | UNSUPPORTED | SPEC_GAP
  obligations: [DecisionObligation]
  policy_version: uint64
  policy_generation: uint64
  valid_until: Timestamp?
  reason_code: string
  audit_required: bool
  audit_before_return: bool
  source_policy: SecurityProfileRef
  correlation_id: CorrelationId
```

```yaml
DecisionContext:
  job_id: JobId?
  program_id: ProgramId?
  partition_id: PartitionId?
  service_class: string?
  operator_session_id: string?
  authentication_strength: string?
  emergency_state: bool
  request_time: Timestamp
```

```yaml
DecisionObligation:
  obligation_id: string
  obligation_type: AUDIT | MFA | DUAL_CONTROL | BREAK_GLASS | GUARD_APPROVAL | OPERATOR_CONFIRMATION | REDACTION | RETENTION_CHECK
  required_before_return: bool
  record_type: string?
  parameters: map
```

Rules:

- Only `securityd` may create authoritative `SecurityDecision` objects.
- The enforcement point MUST treat `REQUIRE_*` results as incomplete, not as `ALLOW`.
- `audit_before_return: true` MUST be satisfied before returning a caller-visible result.
- `UNSUPPORTED` means the operation is specified but unavailable.
- `SPEC_GAP` means the operation is undefined and MUST NOT be implemented as success.
- A `SecurityDecision` MUST be included in the audit correlation chain for protected operations.

### 7.6 ProgramIdentity

```yaml
ProgramIdentity:
  program_id: ProgramId
  program_name: string
  dsn_or_artifact_id: string
  signer: string?
  digest: Digest
  catalog_entry_generation: uint64
  amf_authorized: bool
  authority_class: string?
  allowed_service_classes: [string]
  measurement_context: Digest?
  status: ACTIVE | REVOKED | QUARANTINED | UNSUPPORTED
  source_matrix_refs: [string]
```

Rules:

- A program identity MUST be established before execution.
- A digest match MUST NOT bypass `securityd`.
- AMF-authorized programs MUST also pass `amfd` validation.

### 7.7 AuthorizedModule

```yaml
AuthorizedModule:
  module_id: ModuleId
  program_identity: ProgramIdentityRef
  manifest_digest: Digest
  artifact_digest: Digest
  signer: string
  authority_class: AuthorityClassId
  abi_version: string
  allowed_entrypoints: [string]
  revocation_refs: [string]
  security_epoch: uint64
  guard_root_ref: GuardRootRef?
  status: CANDIDATE | VERIFIED | LOADED | READY | REVOKED | FAILED
```

Rules:

- `AuthorizedModule` represents AMF module authority.
- It MUST NOT represent a generic plugin or administrator role.
- It MUST NOT receive arbitrary caller pointers in its ABI.

### 7.8 Job

```yaml
Job:
  job_id: JobId
  job_name: string
  submitter: PrincipalRef
  effective_principal: PrincipalRef
  program_identities: [ProgramIdentityRef]
  job_class: string
  service_class: string
  report_class: string?
  status: SUBMITTED | INPUT | CONVERSION | VALIDATED | QUEUED | SELECTED | EXECUTING_STEP | STEP_COMPLETE | OUTPUT | COMPLETE | PURGE_PENDING | PURGED | JCL_ERROR | SECURITY_DENIED | DATASET_OPEN_DENIED | PROGRAM_LOAD_DENIED | STEP_FAILED | CANCELED | HELD | ABENDED
  steps: [JobStep]
  return_code: int?
  abend_reason: string?
  spool_refs: [SpoolEntryRef]
  audit_correlation_id: CorrelationId
  submitted_at: Timestamp
  updated_at: Timestamp
```

Rules:

- Effective principal MUST be established before any dataset, program, or spool resource is opened.
- Job status transitions MUST follow the job/spool specification state machine.
- Job identity MUST be included in dataset and spool authorization contexts.

### 7.9 JobStep

```yaml
JobStep:
  step_id: string
  step_name: string
  program: ProgramIdentityRef
  dd_statements: [DatasetDisposition]
  status: PENDING | RESOLVING | AUTHORIZING | RUNNING | COMPLETE | FAILED | CANCELED | ABENDED
  start_time: Timestamp?
  end_time: Timestamp?
  return_code: int?
  failure_reason: string?
```

Rules:

- DD resolution MUST use `catalogd`, `datasetd`, and `securityd`.
- Step failure MUST preserve audit correlation.

### 7.10 DatasetDisposition

```yaml
DatasetDisposition:
  dd_name: string
  dsn: string?
  sysout: bool
  disposition: SHR | OLD | NEW | MOD | SYSOUT
  requested_operation: READ | WRITE | APPEND | CREATE | DELETE | EXECUTE
  resolved_dataset: DatasetRef?
  spool_entry: SpoolEntryRef?
```

Rules:

- `SYSOUT` creates or references protected spool resources.
- `DSN` references MUST be resolved through committed catalog entries.

### 7.11 Dataset

```yaml
Dataset:
  dsn: string
  owner: PrincipalRef
  dataset_type: SEQ | PDS_LITE | SYSIN | SYSOUT | LOG | CAT | POLICY | MODULE
  catalog_entry: CatalogEntryRef
  security_profile: SecurityProfileRef
  retention_policy: RetentionPolicyRef
  encryption_policy: EncryptionPolicyRef?
  integrity_policy: IntegrityPolicyRef
  generation: uint64
  status: ACTIVE | MIGRATED | LOCKED | DELETING | DELETED
  created_at: Timestamp
  updated_at: Timestamp
```

Rules:

- A dataset MUST be a managed resource with catalog, security, retention, and audit semantics.
- A persistent dataset MUST NOT be opened unless `catalogd` resolves a committed catalog entry.
- Dataset generation MUST be checked when a handle is used.

### 7.12 CatalogEntry

```yaml
CatalogEntry:
  catalog_entry_id: CatalogEntryId
  dsn: string
  attributes: map
  location: [VolumeExtentRef]
  owner: PrincipalRef
  generation: uint64
  immutable: bool
  system_dataset: bool
  integrity_tag: Digest
  security_profile: SecurityProfileRef
  created_at: Timestamp
  updated_at: Timestamp
  transaction_id: string
  commit_state: PREPARED | COMMITTED | ROLLED_BACK
```

Rules:

- `catalogd` MUST resolve only `COMMITTED` entries.
- Immutable or system dataset updates MUST require explicit authority and audit.
- Generation changes MUST invalidate stale dataset handles.

### 7.13 Volume and Extent

```yaml
Volume:
  volume_id: string
  volume_class: BOOT | SYSTEM | USER | SPOOL | AUDIT | RECOVERY | REMOVABLE
  owner_partition: PartitionRef?
  encryption_domain: string?
  status: ONLINE | OFFLINE | READ_ONLY | DEGRADED | RETIRED

VolumeExtent:
  volume_id: string
  start_block: uint64
  block_count: uint64
  allocation_generation: uint64
```

Rules:

- Volume ownership and partition assignment MUST be consistent with PXM device ownership where PXM is active.
- Audit volumes MUST have stricter failure policy than ordinary user volumes.

### 7.14 DatasetHandle

```yaml
DatasetHandle:
  handle_id: string
  subject: SubjectRef
  dataset: DatasetRef
  operation: READ | WRITE | APPEND | CREATE | DELETE | EXECUTE
  policy_version: uint64
  catalog_entry_generation: uint64
  dataset_generation: uint64
  policy_binding: PolicyBinding
  generation_binding: ObjectGenerationBinding
  issued_at: Timestamp
  expiry: Timestamp
  audit_correlation_id: CorrelationId
  status: ACTIVE | REVOKED | EXPIRED
```

Rules:

- A handle MUST be issued only after an allow decision from `securityd`.
- Handle use MUST verify policy version, catalog generation, dataset generation, subject, operation, and expiry.
- Handles MUST be unforgeable typed object references.
- `policy_binding` and `generation_binding` are authoritative for stale-handle checks.

### 7.15 SpoolEntry

```yaml
SpoolEntry:
  spool_id: SpoolId
  job_id: JobId
  owner: PrincipalRef
  output_class: string
  sysout_dataset_ref: DatasetRef
  security_profile: SecurityProfileRef
  retention_policy: RetentionPolicyRef
  status: OPEN | CLOSED | HELD | PURGE_PENDING | PURGED
  created_at: Timestamp
  updated_at: Timestamp
```

Rules:

- Spool entries are protected resources.
- Browse, purge, hold, release, and export MUST pass through `securityd`.

### 7.16 SpoolHandle

```yaml
SpoolHandle:
  handle_id: string
  subject: SubjectRef
  spool_entry: SpoolEntryRef
  operation: BROWSE | EXPORT | PURGE | HOLD | RELEASE
  policy_binding: PolicyBinding
  generation_binding: ObjectGenerationBinding
  issued_at: Timestamp
  expiry: Timestamp
  audit_correlation_id: CorrelationId
  status: ACTIVE | REVOKED | EXPIRED
```

Rules:

- A spool handle MUST bind the `SecurityDecision` through `policy_binding`.
- A spool handle MUST fail closed if the spool generation, policy version, subject, or operation does not match.

### 7.17 OperatorCommand

```yaml
OperatorCommand:
  command_id: string
  command_name: string
  grammar_version: string
  authority_class: AuthorityClassId
  target_resource_type: ResourceType
  destructive: bool
  requires_confirmation: bool
  requires_dual_control: bool
  audit_class: AuditClass
  automation_allowed: bool
```

Rules:

- Operator commands MUST NOT be treated as root shell commands.
- Commands MUST be parsed into typed operations before authorization.
- Automation hooks MUST use the same authorization and audit path.

### 7.18 OperatorCommandAuthorization

```yaml
OperatorCommandAuthorization:
  authorization_id: string
  command: OperatorCommand
  subject: SubjectRef
  target_object: ObjectRef
  policy_binding: PolicyBinding
  generation_binding: ObjectGenerationBinding
  confirmation_state: NOT_REQUIRED | REQUIRED | CONFIRMED | EXPIRED
  dual_control_state: NOT_REQUIRED | REQUIRED | SATISFIED | EXPIRED
  audit_correlation_id: CorrelationId
  status: ACTIVE | USED | EXPIRED | REVOKED
```

Rules:

- Operator command authorization MUST NOT be reused for a different target object.
- Destructive command authorizations MUST bind the resolved target generation.
- Confirmation and dual-control obligations MUST be satisfied before execution.

### 7.19 SecurityProfile

```yaml
SecurityProfile:
  security_profile_id: PolicyId
  profile_name: string
  resource_type: ResourceType
  owner: PrincipalRef
  access_rules: [AccessRule]
  default_decision: DENY | ALLOW_READ_ONLY | SPEC_GAP
  audit_rules: [AuditRule]
  policy_version: uint64
  status: ACTIVE | STAGED | RETIRED
```

Rules:

- Default decision SHOULD be deny.
- `SPEC_GAP` MUST NOT be converted to allow.
- Policy version changes MUST be transactional.

### 7.20 AccessRule

```yaml
AccessRule:
  rule_id: string
  effect: ALLOW | DENY | REQUIRE_MFA | REQUIRE_DUAL_CONTROL | REQUIRE_BREAK_GLASS | REQUIRE_GUARD_APPROVAL
  subjects:
    principals: [PrincipalId]
    groups: [GroupId]
    roles: [RoleId]
    labels: [string]
  operations: [Operation]
  conditions:
    job_class: [string]?
    service_class: [string]?
    partition_id: [PartitionId]?
    time_window: string?
    emergency_only: bool?
    source_program: [ProgramId]?
  obligations: [Obligation]
  priority: int
```

Rules:

- Deny rules MUST dominate allow rules unless the policy language explicitly defines a safer ordering.
- Conditions MUST be typed and bounded.

### 7.21 AuditRule

```yaml
AuditRule:
  rule_id: string
  operations: [Operation]
  decisions: [ALLOW | DENY | ALLOW_WITH_AUDIT | REQUIRE_MFA | REQUIRE_DUAL_CONTROL | REQUIRE_BREAK_GLASS | REQUIRE_GUARD_APPROVAL | REQUIRE_OPERATOR_CONFIRMATION | UNSUPPORTED | SPEC_GAP]
  audit_class: AuditClass
  required: bool
  redaction_policy: string
```

Rules:

- Deny decisions for protected resources MUST be auditable.
- Required audit obligations MUST fail closed when auditd is unavailable under the applicable profile policy.

### 7.22 AuditRecord Reference

```yaml
AuditRecordRef:
  record_id: string
  record_seq: uint64
  record_hash: Digest
  stream_id: string
```

Full audit schema is defined in `07-audit.md`.

### 7.23 WorkloadPolicy

```yaml
WorkloadPolicy:
  policy_id: string
  policy_version: uint64
  job_classes: [JobClass]
  service_classes: [ServiceClass]
  report_classes: [ReportClass]
  status: STAGED | ACTIVE | RETIRED
```

```yaml
JobClass:
  class_id: string
  max_concurrent: uint32
  default_priority: uint32
  allowed_submitters: [PrincipalId | GroupId | RoleId]
```

```yaml
ServiceClass:
  service_class_id: string
  importance: uint32
  goal_type: BASIC_PRIORITY | VELOCITY_LIKE | RESPONSE_TIME | DISCRETIONARY
  goal_parameters: map
```

Rules:

- Workload policy MUST NOT grant dataset or operator authority.
- workload policy hints MUST NOT override security decisions.

### 7.24 Partition

```yaml
Partition:
  partition_id: PartitionId
  partition_name: string
  profile: ActivationProfileRef
  state: DEFINED | MEASURED | LOADED | ACTIVATED | RUNNABLE | RUNNING | QUIESCED | FAULTED | DEACTIVATED | DESTROYED
  owner: PrincipalRef
  logical_cpus: [uint32]
  memory_domains: [string]
  device_assignments: [DeviceAssignmentRef]
  measurement_context: Digest?
  audit_correlation_id: CorrelationId
```

Rules:

- MFOS MUST remain partition-aware even when running with an implicit single partition backend.
- PXM MUST NOT interpret job, dataset, or security profile semantics.

### 7.25 ActivationProfile

```yaml
ActivationProfile:
  activation_profile_id: string
  partition_id: PartitionId
  cpu_config: map
  memory_config: map
  device_config: map
  boot_image_digest: Digest
  policy_bundle_digest: Digest
  guard_required: bool
  created_at: Timestamp
  version: uint64
```

Rules:

- Activation profile changes are security-sensitive.
- High-Assurance activation profiles MUST be Guard-measurable.

### 7.26 GuardRoot

```yaml
GuardRoot:
  guard_root_id: GuardRootId
  root_type: SECURITY_POLICY | AUDIT_CHAIN | AMF_REGISTRY | SVC_TABLE | NUCLEUS_TEXT | EXECUTABLE_MAPPING_POLICY | PAGE_TABLE_POLICY | ACTIVATION_PROFILE | EMERGENCY_STATE | UPDATE_POLICY
  digest: Digest
  version: uint64
  sealed_at: Timestamp
  guard_measurement: Digest
  status: SEALED | VERIFIED | MISMATCH | RETIRED
```

Rules:

- Guard roots are High-Assurance root objects.
- Guard MUST NOT interpret dataset policy or job scheduling semantics.

### 7.27 AMFLoadAuthorization

```yaml
AMFLoadAuthorization:
  authorization_id: string
  module_id: ModuleId
  subject: SubjectRef
  requested_authority_class: AuthorityClassId
  policy_binding: PolicyBinding
  generation_binding: ObjectGenerationBinding
  guard_root_ref: GuardRootRef?
  audit_correlation_id: CorrelationId
  status: ACTIVE | USED | EXPIRED | REVOKED
```

Rules:

- AMF load authorization MUST bind module digest, signer, authority class, policy version, and AMF registry generation.
- Phase 1 production AMF load MAY remain specified but unsupported; in that case requests MUST return `MFOS_ERR_UNSUPPORTED`.
- A test-only AMF authorization MUST NOT support a production AMF claim.

### 7.28 UpdateArtifact

```yaml
UpdateArtifact:
  artifact_id: UpdateArtifactId
  component_type: nucleus | service | amf_module | policy_bundle | pxm_core | pxm_guard | recovery_image
  component_id: string
  component_version: string
  target_arch: x86_64
  target_vendor: intel | amd | any
  required_cpu_features: [string]
  profile_applicability: [ConformanceProfile]
  hash: Digest
  size: uint64
  generation: uint64
  security_epoch: uint64
  dependencies: [ArtifactDependency]
  conflicts: [ArtifactConflict]
  signing_key_id: string
  signature: Signature
  revocation_refs: [string]
  rollback_policy:
    min_generation: uint64
  guard_required: bool
  activation_profile_constraints: [string]
  audit_class: AuditClass
  source_matrix_refs: [string]
```

Rules:

- Update artifacts MUST be verified by `uvsd` before activation.
- Rollback, freeze, and mix-and-match conditions MUST fail closed.

## 8. Resource Types and Operations

```yaml
ResourceType:
  - DATASET
  - CATALOG
  - SPOOL
  - JOB
  - PROGRAM
  - AMF_MODULE
  - OPERATOR_COMMAND
  - PARTITION
  - DEVICE
  - AUDIT_STREAM
  - UPDATE_ARTIFACT
  - GUARD_ROOT
  - SECURITY_POLICY
  - WORKLOAD_POLICY
```

```yaml
Operation:
  - READ
  - WRITE
  - APPEND
  - CREATE
  - UPDATE
  - DELETE
  - PURGE
  - EXECUTE
  - SUBMIT
  - CANCEL
  - BROWSE
  - EXPORT
  - HOLD
  - RELEASE
  - LOAD
  - ACTIVATE
  - DEACTIVATE
  - MEASURE
  - ASSIGN
  - RELEASE_DEVICE
  - QUERY
  - ADMINISTER
  - ATTEST
```

Rules:

- Operation meaning is resource-type-specific.
- Unknown operation/resource pairs MUST return `MFOS_ERR_SPEC_GAP`.
- Known but unimplemented operation/resource pairs MUST return `MFOS_ERR_UNSUPPORTED`.

## 9. Object Lifecycle Patterns

### 9.1 Create / Commit Lifecycle

```text
REQUEST_CREATE
  -> VALIDATE_SCHEMA
  -> AUTHORIZE_CREATE
  -> PREPARE_OBJECT
  -> WRITE_JOURNAL
  -> COMMIT_OBJECT
  -> AUDIT_CREATE
  -> READY
```

Failure states:

```text
SCHEMA_INVALID
AUTHORIZATION_DENIED
AUDIT_REQUIRED_BUT_UNAVAILABLE
JOURNAL_WRITE_FAILED
COMMIT_FAILED
SPEC_GAP
UNSUPPORTED
```

### 9.2 Open / Handle Lifecycle

```text
REQUEST_HANDLE
  -> RESOLVE_OBJECT
  -> AUTHORIZE_OPERATION
  -> ISSUE_TYPED_HANDLE
  -> HANDLE_ACTIVE
  -> HANDLE_USE
  -> CLOSE_OR_REVOKE
  -> HANDLE_RETIRED
```

Failure states:

```text
OBJECT_NOT_FOUND
POLICY_DENIED
POLICY_VERSION_MISMATCH
GENERATION_MISMATCH
HANDLE_EXPIRED
HANDLE_FORGED
AUDIT_REQUIRED_BUT_UNAVAILABLE
```

### 9.3 Update Lifecycle

```text
REQUEST_UPDATE
  -> VALIDATE_CURRENT_GENERATION
  -> AUTHORIZE_UPDATE
  -> PREPARE_NEW_GENERATION
  -> WRITE_JOURNAL
  -> COMMIT_NEW_GENERATION
  -> INVALIDATE_STALE_HANDLES
  -> AUDIT_UPDATE
  -> READY
```

### 9.4 Delete / Purge Lifecycle

```text
REQUEST_DELETE
  -> RESOLVE_OBJECT
  -> AUTHORIZE_DELETE_OR_PURGE
  -> CHECK_RETENTION
  -> PREPARE_TOMBSTONE
  -> WRITE_JOURNAL
  -> COMMIT_TOMBSTONE
  -> AUDIT_DELETE
  -> RECLAIM_AFTER_POLICY
```

Rules:

- Retention denial MUST NOT be downgraded into ordinary delete success.
- Purge is not the same as unlink.

## 10. Cross-Object Binding Rules

| Binding | Rule |
| --- | --- |
| Job -> Principal | `effective_principal` MUST be established before resource open. |
| Job -> Dataset | DD resolution MUST use catalog generation and security decision. |
| Dataset -> CatalogEntry | Persistent dataset MUST reference a committed catalog entry. |
| DatasetHandle -> Dataset | Handle MUST bind dataset generation and catalog generation. |
| DatasetHandle -> PolicyBinding | Handle MUST bind the allow decision that created it. |
| DatasetHandle -> ObjectGenerationBinding | Handle MUST bind the committed object generations used for authorization. |
| SpoolEntry -> Job | Spool entry MUST bind job ID and owner. |
| SpoolHandle -> PolicyBinding | Browse/export/purge/hold/release handles MUST bind the authorizing decision. |
| OperatorCommand -> AuthorityClass | Every command MUST have a declared authority class. |
| OperatorCommandAuthorization -> PolicyBinding | Command execution MUST bind subject, target, operation, decision, and generation. |
| AuthorizedModule -> AuthorityClass | AMF load MUST require explicit module authority. |
| AMFLoadAuthorization -> PolicyBinding | AMF executable transition MUST bind authorizing decision and AMF registry generation. |
| UpdateArtifact -> SecurityEpoch | Activation MUST reject rollback below minimum generation. |
| Partition -> ActivationProfile | Partition state changes MUST bind activation profile version. |
| GuardRoot -> RootObject | Guard root digest MUST bind root type and version. |

## 11. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-OBJ-0001 | Every protected object MUST have a canonical object type and object ID. | schema test |
| MFOS-REQ-OBJ-0002 | Protected object access MUST be represented as subject/object/operation/context. | interface test |
| MFOS-REQ-OBJ-0003 | Dataset objects MUST include catalog, security profile, retention, integrity, and generation metadata. | schema test |
| MFOS-REQ-OBJ-0004 | Dataset handles MUST bind subject, operation, policy version, catalog generation, dataset generation, and expiry. | negative test |
| MFOS-REQ-OBJ-0005 | Job objects MUST include submitter, effective principal, status, steps, spool references, and audit correlation ID. | schema test |
| MFOS-REQ-OBJ-0006 | Spool entries MUST be protected resources with owner, job ID, output class, security profile, and retention policy. | security test |
| MFOS-REQ-OBJ-0007 | Operator commands MUST be typed objects with authority class and audit class. | parser test |
| MFOS-REQ-OBJ-0008 | AMF module objects MUST include manifest digest, artifact digest, signer, authority class, ABI version, and revocation references. | manifest test |
| MFOS-REQ-OBJ-0009 | Policy version changes MUST invalidate stale authorization-sensitive handles. | stale handle test |
| MFOS-REQ-OBJ-0010 | Unknown object classes and operation pairs MUST fail with `MFOS_ERR_SPEC_GAP`. | negative test |
| MFOS-REQ-OBJ-0011 | Specified but unimplemented object operations MUST fail with `MFOS_ERR_UNSUPPORTED`. | no-fake-success test |
| MFOS-REQ-OBJ-0012 | High-Assurance root object claims MUST reference `GuardRoot` evidence. | evidence review |
| MFOS-REQ-OBJ-0013 | `SecurityDecision` MUST be the canonical authorization decision object for protected resources. | interface test |
| MFOS-REQ-OBJ-0014 | `PolicyBinding` MUST bind successful handles and authorizations to the exact `securityd` decision. | stale decision negative test |
| MFOS-REQ-OBJ-0015 | `ObjectGenerationBinding` MUST be checked before using generation-aware handles or authorizations. | generation mismatch test |

## 12. Invariants

```text
INV-OBJ-001:
  A protected resource handle must not exist unless securityd returned
  ALLOW or ALLOW_WITH_AUDIT for the same subject, object, operation,
  context, and policy_version.

INV-OBJ-002:
  A dataset handle is invalid if catalog_entry_generation or
  dataset_generation differs from the current committed object generation.

INV-OBJ-003:
  A job cannot enter EXECUTING_STEP until effective_principal is established.

INV-OBJ-004:
  A spool entry cannot be browsed, purged, exported, held, or released
  without a securityd decision for that spool object and operation.

INV-OBJ-005:
  An operator command cannot execute from an unparsed string; it must be
  parsed into a typed OperatorCommand and authorized.

INV-OBJ-006:
  AMF module load cannot reach READY unless signature, manifest,
  revocation, authority class, securityd authorization, and applicable
  Guard approval all succeed.

INV-OBJ-007:
  workload policy cannot grant authorization to protected resources.

INV-OBJ-008:
  PXM objects cannot interpret MFOS job, dataset, spool, or security profile
  semantics.

INV-OBJ-009:
  GuardRoot objects cannot expand Guard scope into job scheduling,
  ordinary dataset content, spool formatting, or operator UI rendering.

INV-OBJ-010:
  SPEC_GAP and UNSUPPORTED must never be converted into success.

INV-OBJ-011:
  A PolicyBinding cannot exist for a DENY, REQUIRE_*, UNSUPPORTED, or
  SPEC_GAP SecurityDecision.

INV-OBJ-012:
  A generation-aware handle or authorization cannot be used when its
  ObjectGenerationBinding differs from committed object state.

INV-OBJ-013:
  A SecurityDecision cannot be accepted from a caller. It must be produced by
  securityd and tied to the same subject, object, operation, context,
  policy_version, and correlation_id used by the enforcement point.
```

## 13. Failure Modes

| Failure | Required behavior |
| --- | --- |
| Malformed object schema | Reject with `MFOS_ERR_INVALID_PARAMETER`; audit if security-sensitive. |
| Unknown object class | Return `MFOS_ERR_SPEC_GAP`; do not create fallback object. |
| Known object class not implemented | Return `MFOS_ERR_UNSUPPORTED`. |
| Missing security profile | Fail closed unless a profile-specific bootstrap rule exists. |
| Missing owner | Reject except for explicitly ownerless system roots. |
| Stale generation | Revoke handle and return `MFOS_ERR_STALE_HANDLE`. |
| Policy version mismatch | Return `MFOS_ERR_POLICY_VERSION_MISMATCH`. |
| Retention conflict | Return retention-specific denial; do not purge. |
| Audit required but unavailable | Return `MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE` according to profile. |
| Guard root mismatch | High-Assurance: deny protected transition and alert. |
| Digest mismatch | Quarantine object or reject transition; audit required. |

## 14. Positive Tests

| Test ID | Description |
| --- | --- |
| OBJ-POS-001 | Create a valid principal, group, role, and security profile. |
| OBJ-POS-002 | Create a committed catalog entry and dataset object with matching generation. |
| OBJ-POS-003 | Issue a dataset handle after `securityd` allow decision. |
| OBJ-POS-004 | Submit a job with established effective principal and resolved DD statements. |
| OBJ-POS-005 | Create a SYSOUT spool entry linked to job ID and owner. |
| OBJ-POS-006 | Parse an operator command into a typed `OperatorCommand`. |
| OBJ-POS-007 | Load an AMF candidate object through verified manifest metadata. |
| OBJ-POS-008 | Represent implicit single partition as a valid `Partition` object. |
| OBJ-POS-009 | Seal a High-Assurance root as `GuardRoot` with digest and version. |
| OBJ-POS-010 | Create a `SecurityDecision`, derive a `PolicyBinding`, and issue a dataset handle with matching generation binding. |
| OBJ-POS-011 | Authorize a typed operator command with confirmation state and target generation binding. |

## 15. Negative Tests

| Test ID | Description |
| --- | --- |
| OBJ-NEG-001 | Attempt to create a dataset without a security profile; expect fail closed. |
| OBJ-NEG-002 | Attempt to open a dataset with stale catalog generation; expect `MFOS_ERR_STALE_HANDLE`. |
| OBJ-NEG-003 | Attempt to use a forged dataset handle; expect rejection and audit. |
| OBJ-NEG-004 | Attempt job execution before effective principal is set; expect failure. |
| OBJ-NEG-005 | Attempt spool browse without `securityd` decision; expect denial. |
| OBJ-NEG-006 | Attempt operator command execution from raw shell string; expect rejection. |
| OBJ-NEG-007 | Attempt AMF load with revoked signer; expect fail closed. |
| OBJ-NEG-008 | Attempt workload policy to grant dataset read; expect schema or policy rejection. |
| OBJ-NEG-009 | Attempt PXM partition operation using dataset profile semantics; expect spec violation. |
| OBJ-NEG-010 | Attempt unknown resource type and operation; expect `MFOS_ERR_SPEC_GAP`. |
| OBJ-NEG-011 | Attempt specified but unimplemented operation; expect `MFOS_ERR_UNSUPPORTED`. |
| OBJ-NEG-012 | Attempt GuardRoot claim without Guard evidence in High-Assurance profile; expect denial. |
| OBJ-NEG-013 | Attempt to create a `PolicyBinding` from a DENY decision; expect rejection. |
| OBJ-NEG-014 | Attempt to use a handle after `ObjectGenerationBinding` mismatch; expect stale-handle denial and audit. |
| OBJ-NEG-015 | Attempt to pass caller-supplied `SecurityDecision` to an enforcement point; expect rejection and audit. |

## 16. Fuzz Targets

| Fuzz ID | Target |
| --- | --- |
| OBJ-FUZZ-001 | Principal, group, role, and security profile schema parser. |
| OBJ-FUZZ-002 | Dataset name and catalog entry schema parser. |
| OBJ-FUZZ-003 | Dataset handle decoder and generation validator. |
| OBJ-FUZZ-004 | Job and DD statement object parser. |
| OBJ-FUZZ-005 | Spool entry schema parser. |
| OBJ-FUZZ-006 | Operator command object parser. |
| OBJ-FUZZ-007 | AMF manifest-derived object parser. |
| OBJ-FUZZ-008 | Update artifact manifest parser. |
| OBJ-FUZZ-009 | Partition and activation profile parser. |
| OBJ-FUZZ-010 | Unknown-field and duplicate-field handling across all schemas. |
| OBJ-FUZZ-011 | `SecurityDecision`, `PolicyBinding`, and `ObjectGenerationBinding` parser and validator. |

## 17. Spec Gaps

| Gap ID | Gap |
| --- | --- |
| OBJ-GAP-001 | Concrete serialization format is not fixed. Candidate options: canonical JSON, CBOR, or strict binary schemas. |
| OBJ-GAP-002 | DSN grammar belongs in dataset/catalog spec and is only referenced here. |
| OBJ-GAP-003 | Policy language expression grammar belongs in authorization spec. |
| OBJ-GAP-004 | Exact cryptographic signature algorithms are not fixed. |
| OBJ-GAP-005 | Operator command grammar belongs in operator console spec. |
| OBJ-GAP-006 | Volume allocation and extent format belong in dataset/catalog implementation specs. |
| OBJ-GAP-007 | PXM device assignment schema belongs in PXM specs. |
| OBJ-GAP-008 | Guard attestation claim format belongs in Guard specs. |
| OBJ-GAP-009 | POSIX subsystem object mapping is intentionally deferred. |
| OBJ-GAP-010 | Concrete `SecurityDecision` signature or MAC format is not fixed. |
| OBJ-GAP-011 | Canonical hashing for `DecisionObligation` and `obligations_hash` is not fixed. |

## 18. Inactive Future Implementation Prompt Template

Phase status: inactive future template. This section does not authorize production implementation, hosted daemon implementation, or portable semantic-core implementation.

```text
Future authorized implementation agents would implement MFOS object-model code.

Use this specification and preserve these constraints:
- Do not claim compatibility with IBM products or z/OS.
- Include requirement IDs in code comments for security-sensitive paths.
- Include Source Matrix IDs when implementing z/OS-inspired concepts.
- Do not create fake success paths.
- Return UNSUPPORTED for specified but unimplemented operations.
- Return SPEC_GAP for undefined object classes or operation pairs.
- Treat dataset, spool, operator command, AMF module, audit stream,
  security policy, update artifact, partition, and Guard root as protected
  resources.
- All protected object handles must bind subject, object, operation,
  policy_version, generation, and expiry where applicable.
- Use SecurityDecision as the only authoritative authorization result.
- Use PolicyBinding and ObjectGenerationBinding for handles, operator command
  authorizations, spool handles, and AMF load authorizations.
- Add unit tests, negative tests, and fuzz targets with the IDs from this spec.

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
