---
spec_id: "MFOS-SPEC-24-FORMAL-METHODS"
title: "MFOS Formal Methods Specification v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001", "EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001", "EXTREF-IBM-ZOS-JES-INTRODUCTION-0001", "EXTREF-IBM-Z-LPAR-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001", "MS-VSM-001", "NIST-160-001", "SEL4-001", "TUF-001"]
requirement_refs: []
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Formal Methods Specification v0.1

Status: Draft design split

Owner area: `docs/design/specs/24-formal-methods.md`

This document defines the initial MFOS formal methods scope and the candidate models extracted from `docs/design/mfos-design.md`.

MFOS is z/OS-inspired and source-grounded. This document does not claim compatibility with IBM products, z/Architecture, z/OS APIs, RACF, JES, DFSMS, SMF, JCL, or any other external platform.

## 1. Purpose

Formal methods in MFOS exist to make core safety and security claims precise before they become production code.

The first formal work is not a proof of the whole operating system. It is a staged set of executable or machine-checkable models for the highest-risk MFOS semantics:

- Authorization decisions.
- Dataset open and stale-handle prevention.
- Audit append and hash-chain obligations.
- Catalog transactions and crash recovery.
- Job lifecycle.
- Spool access.
- Operator command execution.
- AMF load.
- Update rollback and freeze resistance.
- PXM partition lifecycle.
- Device teardown.
- Guard root transition.

The models are intended to catch impossible states, unauthorized success, missing audit, rollback acceptance, unsafe teardown, and root mismatch acceptance before implementation hardens around bad assumptions.

## 2. Scope

This specification defines:

- Formal model objectives.
- Candidate model inventory.
- Common model vocabulary.
- Requirements for state variables, actions, invariants, liveness, negative properties, evidence, and SPEC_GAP tracking.
- The initial candidate models `FORMAL-001` through `FORMAL-012`.

This specification does not define:

- A final proof assistant choice.
- Final TLA+, Alloy, Coq, Isabelle, Lean, or model-checker syntax.
- Complete implementation proofs.
- CPU instruction semantics.
- Cryptographic primitive proofs.
- Device-specific hardware proofs.
- Proof that all third-party code is correct.
- A claim of external platform compatibility.

## 3. Source Matrix References

| Source ID | Formal methods use |
| --- | --- |
| EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001 | System integrity statement for unauthorized bypass properties. |
| EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001 | Negative testing discipline for authorized boundary confusion. |
| EXTREF-IBM-ZOS-SECURITY-SERVER-0001 | Security manager and protected resource concepts for authorization model. |
| EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001 | Catalog and dataset concepts for dataset and catalog models. |
| EXTREF-IBM-ZOS-JES-INTRODUCTION-0001 | Job, spool, queue, and initiator concepts for job and spool models. |
| EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | Audit/accounting evidence concepts for audit model. |
| EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001 | Authorized program boundary concepts for AMF model. |
| EXTREF-IBM-Z-LPAR-INTRODUCTION-0001 | Logical partition concepts for PXM lifecycle model. |
| TUF-001 | Update root/timestamp/snapshot/targets roles and rollback/freeze/mix-and-match properties. |
| MS-VSM-001 | Informative root-isolation reference for Guard model only. |
| SEL4-001 | Reference for explicit proof boundary and assumptions discipline. |
| NIST-160-001 | Secure systems engineering lifecycle. |
| FBVBS-001 | Internal transfer source for traceability, state machines, command discipline, audit roots, and proof obligations. |

## 4. Normative Language

- `MUST`: required for the applicable model or profile.
- `SHOULD`: strongly recommended; deviation requires an ADR and evidence.
- `MAY`: optional.
- `MUST NOT`: prohibited.
- `UNSUPPORTED`: specified behavior not implemented.
- `SPEC_GAP`: behavior undefined by specification; implementation and model must not invent success.

## 5. Formal Methods Strategy

MFOS uses staged formal methods:

1. State-machine models for lifecycle and transaction correctness.
2. Relational models for authorization, handles, references, and ownership.
3. Temporal models for audit-before-result, eventual completion, and no-stuck-success properties.
4. Refinement mapping from model states to implementation events after prototypes exist.
5. Proof-assistant work only after the model boundaries and implementation interfaces stabilize.

Recommended early tools:

- TLA+ style models for temporal state machines.
- Alloy style models for bounded relational consistency checks.
- Property-based tests generated from model transitions.
- Trace checkers that validate implementation logs against model actions.

The tool choice remains a SPEC_GAP until the repository contains approved model harnesses.

## 6. Global Modeling Rules

Each candidate model MUST include:

- Model ID.
- Linked specification files.
- State variables.
- Actions.
- Invariants.
- Liveness properties.
- Negative properties.
- Evidence artifacts.
- SPEC_GAPs.

Each model MUST make unauthorized success impossible in the model state space.

Each model MUST represent audit obligations where the related operation is security-sensitive.

Each model MUST distinguish:

- Denied behavior.
- Unsupported behavior.
- Spec-gap behavior.
- Internal corruption.

Each model MUST include a small finite configuration suitable for bounded checking before large-state exploration is attempted.

## 7. Common State Vocabulary

The candidate models share these abstract values.

```text
Decision:
  ALLOW
  DENY
  ALLOW_WITH_AUDIT
  REQUIRE_MFA
  REQUIRE_DUAL_CONTROL
  REQUIRE_GUARD_APPROVAL
  UNSUPPORTED
  SPEC_GAP

AuditState:
  NOT_REQUIRED
  REQUIRED
  PENDING
  APPENDED
  FAILED

ObjectState:
  ABSENT
  DEFINED
  ACTIVE
  LOCKED
  REVOKED
  DELETED
  FAULTED

Result:
  OK
  DENIED
  UNSUPPORTED
  SPEC_GAP
  INVALID_STATE
  FAILED_CLOSED
  INTERNAL_CORRUPTION
```

## 8. Global Invariants

```text
FM-INV-0001 NoUnauthorizedSuccess:
  No protected operation reaches Result = OK unless an authorization decision
  for the same subject, object, operation, context, and policy_version permits it.

FM-INV-0002 AuditBeforeDenyReturn:
  If a protected operation is denied and the active profile requires audit,
  the caller cannot observe the final denial result before the denial audit
  obligation is APPENDED or the operation fails closed due to audit failure.

FM-INV-0003 NoSpecGapSuccess:
  SPEC_GAP actions never produce Result = OK.

FM-INV-0004 NoUnsupportedSuccess:
  UNSUPPORTED actions never produce Result = OK.

FM-INV-0005 PolicyVersionBinding:
  Handles, tokens, root transitions, update decisions, and operation grants are
  bound to the policy_version used to authorize them.

FM-INV-0006 NoSilentFallback:
  A failed required service, missing policy, missing audit path, failed Guard
  approval, or invalid state cannot be converted to success by fallback.
```

## 9. Candidate Models

### 9.1 FORMAL-001: Authorization Decision Model

Linked specs:

- `docs/design/specs/03-system-integrity.md`
- `docs/design/specs/06-authorization.md`
- `docs/design/specs/07-audit.md`

Purpose:

Model `securityd` as the central policy decision point for protected resource access.

State variables:

```text
Subjects
Objects
Operations
Contexts
PolicyVersion
PolicyRules
ResourceProfiles
Decisions
Obligations
AuditStateByDecision
BreakGlassState
DualControlApprovals
ResultByRequest
```

Actions:

```text
SubmitAuthRequest(subject, object, operation, context, policy_version)
EvaluatePolicy(request)
AttachObligations(request)
ApproveDualControl(request)
EnterBreakGlass(subject, reason, expiry)
ExpireBreakGlass(subject)
AppendDecisionAudit(request)
ReturnDecision(request)
RejectMissingPolicy(request)
RejectStalePolicyVersion(request)
ReturnUnsupported(request)
ReturnSpecGap(request)
```

Invariants:

```text
AUTH-INV-001:
  ALLOW or ALLOW_WITH_AUDIT exists only if a policy rule matches the exact
  subject, object, operation, context, and policy_version.

AUTH-INV-002:
  DENY decisions with audit obligations cannot be returned before audit append
  succeeds or the operation fails closed.

AUTH-INV-003:
  Break-glass decisions require reason, expiry, subject, and audit obligation.

AUTH-INV-004:
  Dual-control operations require two distinct approved subjects.

AUTH-INV-005:
  Missing, malformed, stale, or undefined policy cannot produce ALLOW.
```

Liveness:

```text
AUTH-LIVE-001:
  Every well-formed authorization request eventually reaches exactly one final
  result: ALLOW, DENY, UNSUPPORTED, SPEC_GAP, or FAILED_CLOSED.

AUTH-LIVE-002:
  Break-glass state eventually expires unless renewed through an audited action.
```

Negative properties:

```text
AUTH-NEG-001 unauthorized_allow_never_happens
AUTH-NEG-002 missing_policy_allow_never_happens
AUTH-NEG-003 stale_policy_allow_never_happens
AUTH-NEG-004 break_glass_without_expiry_never_happens
AUTH-NEG-005 dual_control_same_actor_never_succeeds
AUTH-NEG-006 unsupported_operation_success_never_happens
```

Evidence artifacts:

```text
formal/authorization/README.md
formal/authorization/model.*
formal/authorization/counterexamples/
formal/authorization/properties.md
tests/model-traces/authorization/*.json
docs/design/assurance/evidence/authorization.md
```

SPEC_GAPs:

- Final policy language semantics.
- Authentication protocol and principal proof format.
- Exact MFA and dual-control approval object schema.
- Final model-checker syntax and runner.

### 9.2 FORMAL-002: Dataset Open Invariant Model

Linked specs:

- `docs/design/specs/06-authorization.md`
- `docs/design/specs/08-dataset-catalog.md`
- `docs/design/specs/07-audit.md`

Purpose:

Model dataset open so that a dataset handle cannot exist unless catalog resolution, authorization, policy-version binding, audit obligations, and handle lifecycle constraints are satisfied.

State variables:

```text
Datasets
CatalogEntries
CatalogGeneration
Subjects
OpenRequests
PolicyVersion
SecurityDecision
AuditStateByOpen
Handles
HandleState
HandleExpiry
DatasetLockState
RetentionState
```

Actions:

```text
RequestOpen(subject, dsn, operation)
ResolveCatalog(dsn)
AuthorizeDatasetOpen(request)
AppendOpenAudit(request)
CreateHandle(request)
UseHandle(handle)
CloseHandle(handle)
RevokeHandle(handle)
UpdatePolicyVersion()
UpdateCatalogGeneration(dsn)
LockDataset(dsn)
ReturnCatalogNotFound(request)
ReturnPolicyDenied(request)
ReturnAuditFailure(request)
```

Invariants:

```text
DATAOPEN-INV-001:
  Active handles exist only for committed catalog entries.

DATAOPEN-INV-002:
  Active handles are bound to subject, operation, policy_version,
  catalog_generation, and expiry.

DATAOPEN-INV-003:
  No handle is created after DENY, CATALOG_NOT_FOUND, audit failure, or SPEC_GAP.

DATAOPEN-INV-004:
  A handle becomes stale if policy_version or catalog_generation changes beyond
  the version bound to the handle.

DATAOPEN-INV-005:
  Locked datasets cannot produce new handles unless the lock policy explicitly
  permits the operation.
```

Liveness:

```text
DATAOPEN-LIVE-001:
  Every well-formed open request eventually reaches OPEN_ACTIVE or a final
  failure state.

DATAOPEN-LIVE-002:
  Every active handle is eventually closed, revoked, or expired in finite model
  executions.
```

Negative properties:

```text
DATAOPEN-NEG-001 unauthorized_dataset_open_never_creates_handle
DATAOPEN-NEG-002 catalog_not_found_never_creates_handle
DATAOPEN-NEG-003 stale_handle_use_never_succeeds
DATAOPEN-NEG-004 policy_version_mismatch_never_succeeds
DATAOPEN-NEG-005 audit_required_but_unavailable_never_creates_handle
```

Evidence artifacts:

```text
formal/dataset-open/README.md
formal/dataset-open/model.*
formal/dataset-open/counterexamples/
formal/dataset-open/properties.md
tests/model-traces/dataset-open/*.json
docs/design/assurance/evidence/dataset-open.md
```

SPEC_GAPs:

- Final DSN grammar.
- Dataset record/block access method semantics.
- Lock hierarchy and concurrent-open compatibility matrix.
- Retention policy interaction with open handles.

### 9.3 FORMAL-003: Audit Append Invariant Model

Linked specs:

- `docs/design/specs/07-audit.md`
- `docs/design/specs/17-guard.md`

Purpose:

Model append-only audit records, monotonic sequencing, hash-chain linkage, failure policy, and Guard-sealed audit root obligations.

State variables:

```text
AuditRecords
NextSequence
PreviousHash
RecordHash
AppendRequests
SchemaValidity
DurabilityState
RemoteExportState
GuardAuditRoot
Profile
AuditFailurePolicy
QueryAuthorizations
```

Actions:

```text
SubmitAuditRecord(record)
ValidateSchema(record)
CanonicalizeRecord(record)
ComputeRecordHash(record)
AppendLocal(record)
AdvanceHashChain(record)
ExportRemote(record)
AppendGuardRoot(record)
RejectMalformedRecord(record)
DetectHashGap()
DetectTamper()
ApplyAuditFailurePolicy(request)
AuthorizeAuditQuery(subject, query)
```

Invariants:

```text
AUDIT-INV-001:
  Appended records have strictly monotonic sequence numbers.

AUDIT-INV-002:
  Every appended record links to the prior accepted hash except the genesis
  record.

AUDIT-INV-003:
  Malformed records cannot advance the audit chain.

AUDIT-INV-004:
  Security-sensitive operations requiring audit cannot return success if append
  fails under the active profile.

AUDIT-INV-005:
  High-Assurance accepted audit records eventually correspond to a Guard audit
  root append or a fail-closed state.
```

Liveness:

```text
AUDIT-LIVE-001:
  Every valid append request eventually reaches APPENDED, FAILED_CLOSED, or
  REJECTED.

AUDIT-LIVE-002:
  Enterprise-Standalone, Enterprise-PXM, and High-Assurance remote-export queues eventually drain or enter
  an explicit export-failure state.
```

Negative properties:

```text
AUDIT-NEG-001 hash_chain_gap_never_undetected
AUDIT-NEG-002 malformed_record_never_appended
AUDIT-NEG-003 audit_failure_never_silently_downgrades
AUDIT-NEG-004 deny_return_before_required_audit_never_happens
AUDIT-NEG-005 non_monotonic_guard_audit_root_never_accepted
```

Evidence artifacts:

```text
formal/audit-append/README.md
formal/audit-append/model.*
formal/audit-append/counterexamples/
formal/audit-append/properties.md
tests/model-traces/audit-append/*.json
docs/design/assurance/evidence/audit-append.md
```

SPEC_GAPs:

- Final canonical encoding.
- Final hash and signature algorithms.
- Remote export protocol.
- Genesis record format.
- Guard audit root binary format.

### 9.4 FORMAL-004: Catalog Transaction Model

Linked specs:

- `docs/design/specs/08-dataset-catalog.md`
- `docs/design/specs/06-authorization.md`
- `docs/design/specs/07-audit.md`

Purpose:

Model catalog entry creation/update/delete as crash-recoverable transactions that do not expose phantom committed entries.

State variables:

```text
CatalogEntries
JournalEntries
TransactionState
PreparedEntry
CommittedEntry
CatalogGeneration
VolumeExtents
AuthorizationDecision
AuditStateByTx
CrashState
RecoveryState
```

Actions:

```text
BeginTx(subject, operation, dsn)
ValidateDsn(dsn)
AuthorizeCatalogUpdate(tx)
PrepareEntry(tx)
WriteJournal(tx)
CommitEntry(tx)
WriteCommitMarker(tx)
AppendCatalogAudit(tx)
CrashAt(point)
RecoverScanJournal()
RollbackIncomplete(tx)
VerifyCommitted(tx)
RepairOrphanExtents()
CompleteRecovery()
```

Invariants:

```text
CATTX-INV-001:
  Catalog resolution returns only committed entries.

CATTX-INV-002:
  Prepared but uncommitted entries are never visible as committed entries.

CATTX-INV-003:
  Catalog generation increases only on committed transactions.

CATTX-INV-004:
  Immutable or system dataset entries cannot be modified without an explicit
  authorized operation and audit obligation.

CATTX-INV-005:
  Recovery leaves no phantom committed entry after crash before commit marker.
```

Liveness:

```text
CATTX-LIVE-001:
  Every non-crashing transaction eventually reaches COMMITTED or ROLLED_BACK.

CATTX-LIVE-002:
  Recovery eventually completes with committed entries verified and incomplete
  transactions rolled back.
```

Negative properties:

```text
CATTX-NEG-001 crash_before_commit_never_creates_committed_entry
CATTX-NEG-002 unauthorized_catalog_update_never_commits
CATTX-NEG-003 immutable_entry_update_without_authority_never_commits
CATTX-NEG-004 orphan_extent_never_visible_as_dataset
CATTX-NEG-005 malformed_dsn_never_commits
```

Evidence artifacts:

```text
formal/catalog-transaction/README.md
formal/catalog-transaction/model.*
formal/catalog-transaction/counterexamples/
formal/catalog-transaction/properties.md
tests/model-traces/catalog-transaction/*.json
docs/design/assurance/evidence/catalog-transaction.md
```

SPEC_GAPs:

- Final catalog storage layout.
- Final journal record encoding.
- Extent allocation and repair semantics.
- Multi-catalog transaction semantics.
- Concurrent transaction isolation level.

### 9.5 FORMAL-005: Job Lifecycle Model

Linked specs:

- `docs/design/specs/09-job-spool.md`
- `docs/design/specs/06-authorization.md`
- `docs/design/specs/08-dataset-catalog.md`
- `docs/design/specs/07-audit.md`

Purpose:

Model a job from submit through conversion, validation, queueing, execution, output, completion, and purge while preserving effective principal and dataset/spool authorization boundaries.

State variables:

```text
Jobs
JobState
Submitter
EffectivePrincipal
JclParseState
ConversionState
SecurityDecision
Queue
Initiators
StepState
DatasetOpenState
SpoolEntries
ReturnCode
AuditStateByJob
CancelState
```

Actions:

```text
SubmitJob(submitter, payload)
ParseJcl(job)
EstablishEffectivePrincipal(job)
AuthorizeJobSubmit(job)
ConvertJob(job)
ValidateJob(job)
EnqueueJob(job)
SelectJob(job)
StartStep(job, step)
ResolveDd(job, dd)
OpenDatasetForStep(job, dd)
CaptureSysout(job, step)
CompleteStep(job, step)
CompleteJob(job)
CancelJob(job)
HoldJob(job)
PurgeJob(job)
AppendJobAudit(job, event)
```

Invariants:

```text
JOB-INV-001:
  Effective principal is established before any dataset, program, or spool
  resource is opened.

JOB-INV-002:
  A job cannot enter EXECUTING_STEP unless submit, conversion, validation, and
  required authorization have succeeded.

JOB-INV-003:
  DD resolution cannot bypass catalogd, datasetd, or securityd.

JOB-INV-004:
  SYSOUT spool entries are bound to job_id, owner, output_class, and security
  profile.

JOB-INV-005:
  Canceled or failed jobs cannot later reach COMPLETE RC=0.
```

Liveness:

```text
JOB-LIVE-001:
  Every validated queued job eventually reaches SELECTED, HELD, CANCELED, or
  FAILED under fair initiator scheduling assumptions.

JOB-LIVE-002:
  Every executing step eventually reaches STEP_COMPLETE, STEP_FAILED, ABENDED,
  or CANCELED under bounded execution assumptions.
```

Negative properties:

```text
JOB-NEG-001 job_submit_identity_spoofing_never_succeeds
JOB-NEG-002 dataset_open_before_effective_principal_never_happens
JOB-NEG-003 unauthorized_dd_resolution_never_executes_step
JOB-NEG-004 failed_step_never_becomes_complete_rc0_without_policy
JOB-NEG-005 canceled_job_never_executes_new_step
```

Evidence artifacts:

```text
formal/job-lifecycle/README.md
formal/job-lifecycle/model.*
formal/job-lifecycle/counterexamples/
formal/job-lifecycle/properties.md
tests/model-traces/job-lifecycle/*.json
docs/design/assurance/evidence/job-lifecycle.md
```

SPEC_GAPs:

- Final JCL-like language subset.
- ABEND reason taxonomy.
- Initiator fairness and resource scheduling policy.
- Restart and checkpoint semantics.
- Program identity establishment details.

### 9.6 FORMAL-006: Spool Access Model

Linked specs:

- `docs/design/specs/09-job-spool.md`
- `docs/design/specs/06-authorization.md`
- `docs/design/specs/07-audit.md`

Purpose:

Model spool entry creation, browse, export, purge, retention, and ownership so spool output is a protected resource and not treated as audit evidence.

State variables:

```text
SpoolEntries
SpoolState
Owners
JobIds
OutputClass
SecurityProfile
RetentionPolicy
BrowseRequests
ExportRequests
PurgeRequests
SecurityDecision
AuditStateBySpoolOp
QuotaState
```

Actions:

```text
CreateSpoolEntry(job, owner, output_class)
AppendSysout(entry, bytes)
CloseSpoolEntry(entry)
AuthorizeBrowse(subject, entry)
BrowseSpool(entry)
AuthorizeExport(subject, entry)
ExportSpool(entry)
AuthorizePurge(subject, entry)
RequestPurge(entry)
ApplyRetention(entry)
CompletePurge(entry)
AppendSpoolAudit(entry, operation)
RejectQuotaExceeded(entry)
```

Invariants:

```text
SPOOL-INV-001:
  Spool browse, export, and purge require securityd decisions.

SPOOL-INV-002:
  Non-owner access requires an explicit policy rule.

SPOOL-INV-003:
  Retention-protected spool entries cannot be purged until retention allows it.

SPOOL-INV-004:
  Spool output is not audit evidence.

SPOOL-INV-005:
  Purged spool entries cannot later be browsed or exported.
```

Liveness:

```text
SPOOL-LIVE-001:
  Closed spool entries eventually become browseable, held, or purge-pending
  according to policy.

SPOOL-LIVE-002:
  Purge-pending entries eventually become PURGED when retention permits and no
  fault remains.
```

Negative properties:

```text
SPOOL-NEG-001 non_owner_browse_without_policy_never_succeeds
SPOOL-NEG-002 purge_under_retention_never_succeeds
SPOOL-NEG-003 purged_entry_browse_never_succeeds
SPOOL-NEG-004 export_without_audit_never_succeeds
SPOOL-NEG-005 spool_as_audit_record_never_succeeds
```

Evidence artifacts:

```text
formal/spool-access/README.md
formal/spool-access/model.*
formal/spool-access/counterexamples/
formal/spool-access/properties.md
tests/model-traces/spool-access/*.json
docs/design/assurance/evidence/spool-access.md
```

SPEC_GAPs:

- Output class policy grammar.
- Spool quota enforcement details.
- Redaction rules for export.
- Physical spool storage layout.

### 9.7 FORMAL-007: Operator Command Model

Linked specs:

- `docs/design/specs/10-operator-console.md`
- `docs/design/specs/06-authorization.md`
- `docs/design/specs/07-audit.md`

Purpose:

Model operator commands as typed system interfaces with grammar, authority class, confirmation, dual control, execution, and audit.

State variables:

```text
Commands
ParsedCommand
CommandId
OperatorSubject
AuthorityClass
TargetObject
ConfirmationState
DualControlState
SecurityDecision
ExecutionState
AuditStateByCommand
EmergencyMode
AutomationHookState
```

Actions:

```text
EnterCommand(subject, text)
ParseCommand(text)
IdentifyCommand(parsed)
ResolveTarget(command)
AuthorizeCommand(command)
RequestConfirmation(command)
ConfirmCommand(command)
RequestDualControl(command)
ApproveDualControl(command, approver)
ExecuteCommand(command)
AppendCommandAudit(command)
DisplayResult(command)
EnterEmergencyMode(reason, expiry)
RejectMalformedCommand(command)
RejectUnauthorizedCommand(command)
```

Invariants:

```text
OPER-INV-001:
  No operator command executes without command_id, subject, resolved authority
  class, authorization decision, and audit obligation.

OPER-INV-002:
  Destructive commands requiring confirmation cannot execute before
  confirmation.

OPER-INV-003:
  Dual-control commands require two distinct approved subjects.

OPER-INV-004:
  Automation hooks cannot bypass operator authority or audit.

OPER-INV-005:
  Root shell text is not an operator command success path.
```

Liveness:

```text
OPER-LIVE-001:
  Every well-formed command eventually reaches EXECUTED, DENIED, CANCELED,
  UNSUPPORTED, SPEC_GAP, or FAILED_CLOSED.

OPER-LIVE-002:
  Pending confirmation eventually expires, is confirmed, or is canceled.
```

Negative properties:

```text
OPER-NEG-001 unauthorized_operator_command_never_executes
OPER-NEG-002 destructive_command_without_confirmation_never_executes
OPER-NEG-003 dual_control_same_actor_never_executes
OPER-NEG-004 automation_bypass_never_executes
OPER-NEG-005 malformed_command_never_executes
```

Evidence artifacts:

```text
formal/operator-command/README.md
formal/operator-command/model.*
formal/operator-command/counterexamples/
formal/operator-command/properties.md
tests/model-traces/operator-command/*.json
docs/design/assurance/evidence/operator-command.md
```

SPEC_GAPs:

- Final operator command grammar.
- Final destructive command classification.
- Confirmation timeout values.
- Automation hook API.
- Emergency command subset.

### 9.8 FORMAL-008: AMF Load Model

Linked specs:

- `docs/design/specs/12-amf.md`
- `docs/design/specs/06-authorization.md`
- `docs/design/specs/07-audit.md`
- `docs/design/specs/17-guard.md`

Purpose:

Model Authorized Module Facility loading so signed, measured, revocable modules with explicit authority class are loaded only from approved immutable sources, with audit and optional Guard approval.

State variables:

```text
AmfModules
ArtifactSource
ArtifactDigest
SignerState
ManifestState
SignatureState
RevocationState
CatalogImmutability
AuthorityClass
SecurityDecision
GuardApprovalState
MappingState
RegistryState
AuditStateByLoad
Profile
```

Actions:

```text
RequestAmfLoad(module)
ResolveArtifact(module)
VerifySignature(module)
VerifyManifest(module)
CheckRevocation(module)
CheckCatalogImmutability(module)
AuthorizeAmfLoad(module)
RequestGuardApproval(module)
MapReadExecute(module)
RegisterAmf(module)
AppendAmfAudit(module)
RejectInvalidSignature(module)
RejectRevokedModule(module)
RejectMutableSource(module)
RejectGuardDenied(module)
```

Invariants:

```text
AMF-INV-001:
  Registered AMF modules have valid signature, manifest, digest, authority
  class, source immutability, authorization, and audit.

AMF-INV-002:
  Revoked signer, digest, or security_epoch cannot be loaded.

AMF-INV-003:
  Mutable dataset or unapproved artifact source cannot become registered AMF.

AMF-INV-004:
  High-Assurance AMF load cannot register without Guard approval.

AMF-INV-005:
  AMF modules cannot gain audit-disable authority.
```

Liveness:

```text
AMF-LIVE-001:
  Every AMF load request eventually reaches READY or a final fail-closed state.

AMF-LIVE-002:
  Revocation updates eventually prevent new loads of revoked modules under fair
  policy propagation assumptions.
```

Negative properties:

```text
AMF-NEG-001 invalid_signature_never_loads
AMF-NEG-002 revoked_signer_never_loads
AMF-NEG-003 mutable_dataset_amf_load_never_succeeds
AMF-NEG-004 missing_authority_class_never_loads
AMF-NEG-005 ha_guard_denied_amf_never_registers
```

Evidence artifacts:

```text
formal/amf-load/README.md
formal/amf-load/model.*
formal/amf-load/counterexamples/
formal/amf-load/properties.md
tests/model-traces/amf-load/*.json
docs/design/assurance/evidence/amf-load.md
```

SPEC_GAPs:

- Final AMF manifest schema.
- Signature algorithm and trust root.
- Revocation distribution and freshness.
- Exact ABI safety contract.
- Exact executable mapping transition.

### 9.9 FORMAL-009: Update Rollback and Freeze Model

Linked specs:

- `docs/design/specs/13-update.md`
- `docs/design/specs/07-audit.md`
- `docs/design/specs/17-guard.md`

Purpose:

Model update metadata verification, rollback prevention, freeze detection, mix-and-match detection, security_epoch monotonicity, staged activation, and recovery rollback controls.

State variables:

```text
RootMetadataVersion
TimestampMetadataVersion
TimestampExpiry
SnapshotMetadataVersion
TargetsMetadataVersion
TargetArtifacts
ArtifactHashes
ArtifactSizes
SecurityEpoch
InstalledGeneration
StagedGeneration
MetadataSetConsistency
VerificationState
ApprovalState
GuardUpdateRoot
AuditStateByUpdate
CurrentTime
RecoveryPolicy
```

Actions:

```text
ReceiveMetadata(bundle)
VerifyRoot(bundle)
VerifyTimestamp(bundle, current_time)
VerifySnapshot(bundle)
VerifyTargets(bundle)
VerifyArtifact(artifact)
CheckEpoch(bundle)
CheckDependencies(bundle)
DetectRollback(bundle)
DetectFreeze(bundle, current_time)
DetectMixAndMatch(bundle)
StageUpdate(bundle)
ApproveUpdate(bundle)
ActivateProfileUpdate(bundle)
MeasureActivatedUpdate(bundle)
CommitUpdate(bundle)
RecoveryRollback(bundle)
AppendUpdateAudit(bundle)
RejectUpdate(bundle, reason)
```

Invariants:

```text
UPDATE-INV-001:
  Committed generation cannot decrease except through approved recovery rollback.

UPDATE-INV-002:
  security_epoch cannot decrease except through approved recovery rollback.

UPDATE-INV-003:
  Expired timestamp metadata cannot authorize staging or activation.

UPDATE-INV-004:
  Snapshot and targets versions must form a consistent metadata view.

UPDATE-INV-005:
  Artifact hash and size mismatch cannot stage or activate.

UPDATE-INV-006:
  High-Assurance update root transitions require Guard linkage.
```

Liveness:

```text
UPDATE-LIVE-001:
  Every received update bundle eventually reaches STAGED, REJECTED,
  FAILED_CLOSED, or NEEDS_APPROVAL.

UPDATE-LIVE-002:
  Staged approved updates eventually reach COMMITTED or ROLLED_BACK under fair
  activation assumptions.
```

Negative properties:

```text
UPDATE-NEG-001 rollback_metadata_never_accepted
UPDATE-NEG-002 freeze_metadata_never_accepted
UPDATE-NEG-003 mix_and_match_metadata_never_accepted
UPDATE-NEG-004 artifact_hash_mismatch_never_stages
UPDATE-NEG-005 unsigned_artifact_never_activates
UPDATE-NEG-006 security_epoch_downgrade_never_commits
```

Evidence artifacts:

```text
formal/update-rollback-freeze/README.md
formal/update-rollback-freeze/model.*
formal/update-rollback-freeze/counterexamples/
formal/update-rollback-freeze/properties.md
tests/model-traces/update-rollback-freeze/*.json
docs/design/assurance/evidence/update-rollback-freeze.md
```

SPEC_GAPs:

- Final TUF-like metadata schema.
- Final time source and clock-failure model.
- Recovery rollback approval policy.
- Dependency/conflict solver semantics.
- Final Guard update root payload format.

### 9.10 FORMAL-010: PXM Partition Lifecycle Model

Linked specs:

- `docs/design/specs/16-pxm.md`
- `docs/design/specs/07-audit.md`

Purpose:

Model PXM partition lifecycle transitions, activation profile requirements, measurement, audit, implicit single-partition behavior, and invalid transition denial.

State variables:

```text
Partitions
PartitionState
ActivationProfile
ActivationProfileHash
ImageMeasurement
LogicalCpuAssignments
MemoryDomains
DeviceAssignments
IommuDomains
InterruptRoutes
AuditStateByPXMOp
BackendMode
GuardRequired
GuardApprovalState
```

Actions:

```text
DefinePartition(profile)
MeasurePartition(partition)
LoadPartition(partition)
ActivatePartition(partition)
StartPartition(partition)
DispatchPartition(partition)
DeschedulePartition(partition)
QuiescePartition(partition)
ResumePartition(partition)
FaultPartition(partition)
RecoverPartition(partition)
DeactivatePartition(partition)
DestroyPartition(partition)
RejectInvalidTransition(partition)
AppendPxmAudit(operation)
```

Invariants:

```text
PXMLIFE-INV-001:
  RUNNABLE partitions must have passed DEFINE, MEASURE, LOAD, and ACTIVATE
  through legal transitions.

PXMLIFE-INV-002:
  Illegal transitions never change partition state to a success state.

PXMLIFE-INV-003:
  Implicit single-partition backend cannot claim High-Assurance PXM conformance.

PXMLIFE-INV-004:
  PXM does not interpret MFOS dataset, job, catalog, spool, security profile,
  or workload policy semantics.

PXMLIFE-INV-005:
  High-Assurance transitions requiring Guard cannot succeed without Guard.
```

Liveness:

```text
PXMLIFE-LIVE-001:
  Every valid lifecycle command eventually reaches the requested next legal
  state or an explicit fail-closed state.

PXMLIFE-LIVE-002:
  FAULTED partitions eventually remain FAULTED, recover to RUNNABLE, or move to
  DESTROYED through approved recovery or destruction actions.
```

Negative properties:

```text
PXMLIFE-NEG-001 start_from_defined_never_succeeds
PXMLIFE-NEG-002 activate_without_measure_never_succeeds
PXMLIFE-NEG-003 invalid_state_transition_never_succeeds
PXMLIFE-NEG-004 pxm_dataset_policy_decision_never_happens
PXMLIFE-NEG-005 ha_without_guard_never_claims_ready
```

Evidence artifacts:

```text
formal/pxm-lifecycle/README.md
formal/pxm-lifecycle/model.*
formal/pxm-lifecycle/counterexamples/
formal/pxm-lifecycle/properties.md
tests/model-traces/pxm-lifecycle/*.json
docs/design/assurance/evidence/pxm-lifecycle.md
```

SPEC_GAPs:

- Final VMX/SVM backend semantics.
- Exact activation profile schema.
- Exact scheduler fairness for partition dispatch.
- Boot audit sink before auditd availability.
- Recovery partition policy details.

### 9.11 FORMAL-011: Device Teardown Model

Linked specs:

- `docs/design/specs/16-pxm.md`
- `docs/design/specs/07-audit.md`

Purpose:

Model device assignment and teardown so a device cannot be reassigned before DMA, interrupts, ownership, mappings, and memory reuse hazards are cleared.

State variables:

```text
Devices
DeviceAssignmentState
OwnerPartition
IommuMappings
InterruptRoutes
DmaState
DeviceCommandQueues
DeviceResetState
MemoryDomains
TeardownChecklist
AuditStateByDeviceOp
FaultState
```

Actions:

```text
RequestAssignDevice(device, partition)
PrepareDevice(device)
CreateIommuDomain(device, partition)
CreateInterruptRoutes(device, partition)
ActivateDeviceAssignment(device, partition)
RequestReleaseDevice(device)
StopCommandQueues(device)
QuiesceDeviceAccess(device)
MaskInterrupts(device)
StopDma(device)
RevokeIommuMappings(device)
FlushTranslations(device)
ResetDevice(device)
RevokeInterruptRoutes(device)
ClearOwnership(device)
MarkReleased(device)
FaultTeardown(device, reason)
AppendDeviceAudit(device, operation)
```

Invariants:

```text
DEVTD-INV-001:
  A device cannot be assigned to a new exclusive owner while prior ownership
  remains active.

DEVTD-INV-002:
  Device reassignment cannot occur before DMA is stopped, IOMMU mappings are
  revoked, interrupt routes are revoked, and ownership is cleared.

DEVTD-INV-003:
  Teardown failure leaves the device unavailable for new assignment.

DEVTD-INV-004:
  Memory associated with a destroyed or released partition cannot be reused
  before CPU, IOMMU, interrupt, device ownership, and zeroing requirements are
  satisfied.

DEVTD-INV-005:
  Device assignment requiring IOMMU and interrupt remapping cannot become ACTIVE
  without them.
```

Liveness:

```text
DEVTD-LIVE-001:
  Every release request eventually reaches RELEASED or FAULTED under fair device
  response assumptions.

DEVTD-LIVE-002:
  FAULTED teardown eventually remains isolated, is retried, or is handed to
  recovery workflow.
```

Negative properties:

```text
DEVTD-NEG-001 device_reassigned_before_teardown_never_happens
DEVTD-NEG-002 active_dma_after_release_never_happens
DEVTD-NEG-003 interrupt_route_after_release_never_happens
DEVTD-NEG-004 iommu_mapping_after_release_never_happens
DEVTD-NEG-005 teardown_fault_then_reassign_never_succeeds
```

Evidence artifacts:

```text
formal/device-teardown/README.md
formal/device-teardown/model.*
formal/device-teardown/counterexamples/
formal/device-teardown/properties.md
tests/model-traces/device-teardown/*.json
docs/design/assurance/evidence/device-teardown.md
```

SPEC_GAPs:

- Device-specific reset semantics.
- Exact PCIe/IOMMU invalidation ordering.
- Exact interrupt remapping hardware model.
- Device fault containment after failed reset.
- DMA in-flight completion model.

### 9.12 FORMAL-012: Guard Root Transition Model

Linked specs:

- `docs/design/specs/17-guard.md`
- `docs/design/specs/07-audit.md`
- `docs/design/specs/12-amf.md`
- `docs/design/specs/13-update.md`

Purpose:

Model Guard root sealing, verification, transition, rollback rejection, audit-root append, AMF registry protection, executable mapping authorization, and root mismatch failure policy.

State variables:

```text
GuardLifecycleState
GuardRoots
RootType
RootVersion
RootDigest
SecurityEpoch
PolicyVersion
MeasurementContext
TransitionRequests
ApprovalState
AuditRootSequence
ExecutableMappingRequests
AmfRegistryRoot
SvcTableRoot
EmergencyState
AttestationClaims
AuditStateByGuardOp
```

Actions:

```text
MeasureGuard()
InitializeGuard()
SealRoot(root_type, digest, version)
VerifyRoot(root_type, digest, version)
RequestRootTransition(root_type, old_digest, new_digest)
ApproveRootTransition(transition)
DenyRootTransition(transition)
RevokeRoot(root_type)
DetectRootMismatch(root_type)
EnterLockdown(reason)
RecoveryReseal(root_type)
AuthorizeExecutableMapping(request)
AuthorizeAmfLoad(request)
VerifySvcTable(digest)
AppendAuditRoot(sequence, chain_hash)
EnterEmergencyMode(reason, operator, expiry)
ExitEmergencyMode(operator)
Attest(nonce, claims)
```

Invariants:

```text
GUARDROOT-INV-001:
  Guard scope is limited to approved root types.

GUARDROOT-INV-002:
  Root transition cannot reduce version or security_epoch unless approved
  recovery policy explicitly allows it.

GUARDROOT-INV-003:
  SVC table mismatch cannot be ignored.

GUARDROOT-INV-004:
  Audit root sequence accepted by Guard is strictly monotonic.

GUARDROOT-INV-005:
  High-Assurance executable mapping cannot become active without Guard
  authorization.

GUARDROOT-INV-006:
  Guard cannot interpret ordinary dataset, job, spool, catalog, POSIX, Linux,
  or workload policy business semantics.

GUARDROOT-INV-007:
  Emergency mode cannot disable audit root append obligations.
```

Liveness:

```text
GUARDROOT-LIVE-001:
  Every well-formed root transition request eventually reaches APPROVED, DENIED,
  REVOKED, or LOCKDOWN.

GUARDROOT-LIVE-002:
  LOCKDOWN eventually remains locked down or enters approved recovery workflow.
```

Negative properties:

```text
GUARDROOT-NEG-001 guard_root_mismatch_ignored_never_happens
GUARDROOT-NEG-002 root_rollback_without_recovery_never_succeeds
GUARDROOT-NEG-003 non_monotonic_audit_root_never_succeeds
GUARDROOT-NEG-004 executable_mapping_without_guard_never_succeeds_in_ha
GUARDROOT-NEG-005 guard_dataset_policy_decision_never_happens
GUARDROOT-NEG-006 emergency_mode_without_expiry_never_succeeds
```

Evidence artifacts:

```text
formal/guard-root-transition/README.md
formal/guard-root-transition/model.*
formal/guard-root-transition/counterexamples/
formal/guard-root-transition/properties.md
tests/model-traces/guard-root-transition/*.json
docs/design/assurance/evidence/guard-root-transition.md
```

SPEC_GAPs:

- Exact Guard isolation mechanism.
- Exact attestation evidence format.
- Exact root digest canonicalization.
- Exact emergency recovery policy.
- Exact executable mapping implementation boundary.
- Exact Guard audit root binary payload.

## 10. Model Acceptance Criteria

A candidate model is accepted for design use when:

- It has a model README.
- It lists linked requirement IDs and source IDs.
- It has executable or reviewable model text.
- It has at least one bounded configuration.
- It checks all listed invariants for the bounded configuration.
- It includes negative properties.
- Counterexamples are either fixed or documented as expected failures.
- Evidence artifacts are linked from the assurance plan.
- SPEC_GAPs are listed and not hidden behind success behavior.

## 11. Implementation Trace Requirements

Once implementation exists, security-sensitive tests SHOULD emit trace events that can be checked against these formal actions.

Trace events SHOULD include:

- model_id
- action_id
- subject
- object
- operation
- policy_version
- previous_state
- next_state
- decision
- audit_state
- reason_code
- correlation_id

Trace checking remains a SPEC_GAP until a model runner and trace schema are approved.

## 12. AI Formal Specification Prompt

```text
You are an MFOS formal specification engineer.

Use docs/design/specs/24-formal-methods.md and the linked component specs.

Create or revise one candidate formal model.

Hard constraints:
- Do not claim z/OS compatibility.
- Do not invent behavior for SPEC_GAPs.
- UNSUPPORTED and SPEC_GAP must never produce success.
- Include state variables, actions, invariants, liveness, negative properties,
  evidence artifacts, and SPEC_GAPs.
- Include unauthorized success as an impossible property.
- Include audit obligations for security-sensitive actions.
- Include rollback, stale policy, stale handle, replay, invalid transition, or
  root mismatch negative properties where applicable.
- Keep the model small enough for bounded checking before expanding it.

Required output:
1. Model ID
2. Linked Specification Files
3. Source Matrix IDs
4. State Variables
5. Actions
6. Invariants
7. Liveness Properties
8. Negative Properties
9. Counterexample Expectations
10. Evidence Artifacts
11. SPEC_GAPs
12. Trace Mapping Proposal
```
