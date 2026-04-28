---
spec_id: "MFOS-SPEC-06-AUTHORIZATION"
title: "MFOS Authorization and securityd Specification v0.8 Design Freeze"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS Phase 0.8 authorization lead"
last_reviewed: "2026-04-27"
source_refs: ["EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001", "EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001", "EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001", "EXTREF-IBM-ZOS-JES-INTRODUCTION-0001", "EXTREF-IBM-Z-LPAR-INTRODUCTION-0001", "EXTREF-IBM-Z-DPM-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001"]
requirement_refs: ["MFOS-REQ-AUTH-*"]
claim_refs: []
test_refs: ["TEST-MFOS-AUTH-*", "NEG-MFOS-AUTH-*"]
evidence_refs: ["EV-MFOS-AUTH-*"]
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Authorization and securityd Specification v0.8 Design Freeze

Status: Phase 0.8 design freeze.

Owner area: `docs/design/specs/06-authorization.md`

This document freezes MFOS authorization semantics at design level. It defines
the `securityd` policy decision point, protected resources, subject/object/
operation/context inputs, `SecurityDecision`, `PolicyBinding`, obligations,
policy versioning, delegation, emergency access, dual control, rollback, policy
lint, failure modes, state-machine behavior, tests, evidence expectations, and
known spec gaps.

This document does not authorize production implementation. Any runtime,
service, kernel, policy engine, or compatibility claim based only on this
document is prohibited. Undefined behavior is `SPEC_GAP`; specified but
unimplemented behavior is `UNSUPPORTED`; both fail closed.

MFOS is z/OS-inspired and source-grounded. It does not claim compatibility with
IBM products, z/Architecture, z/OS APIs, RACF, JES, DFSMS, SMF, or JCL.

## 1. Purpose

`securityd` is the central MFOS authorization decision point:

```text
SecurityDecision =
  f(subject, object, operation, decision_context, active_policy_version)
```

The decision is not a Boolean. It carries a decision result, reason code,
policy version, matched policy bindings, handle constraints, cache rules,
obligations, evidence hooks, and failure policy.

This specification exists to prevent:

- Distributed authorization allow decisions outside `securityd`.
- Protected resource access without a policy-bound decision.
- Dataset, catalog, spool, job, operator, AMF, update, audit, partition, Guard,
  or policy side effects after deny, unsupported behavior, or spec gaps.
- Operator command execution as untyped shell command execution.
- AMF module authority being treated as administrator or operator authority.
- Emergency access that bypasses audit, expiry, reason capture, or review.
- Dual-control approval by the same effective principal.
- Policy rollback that silently downgrades security epoch or audit obligations.
- Policy lint results being treated as runtime authorization allows.
- Fake success for unsupported or undefined authorization behavior.

## 2. Scope

In scope:

- Protected resource classes and valid operation families.
- Subject, object, operation, and decision context semantics.
- `SecurityDecision` and `PolicyBinding` design contracts.
- Decision results, obligations, handle constraints, cacheability, and evidence
  requirements.
- Policy bundle versioning, activation, rollback, lint, and cache invalidation.
- Delegation, emergency access, operator confirmation, and dual control.
- Enforcement point responsibilities and non-responsibilities.
- Authorization state machines, invalid transitions, invariants, failure modes,
  positive tests, negative tests, fuzz tests, and spec gaps.

Out of scope:

- Authentication protocol internals.
- External identity provider integration.
- Concrete policy language grammar.
- Physical policy storage format.
- Cryptographic algorithm selection.
- Guard internals.
- Dataset physical formatting or access-method implementation.
- POSIX permission emulation.
- Production implementation.

## 3. Source Matrix References

| Source ID | Authorization use |
| --- | --- |
| `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001` | System integrity framing: unauthorized subjects must not bypass protected resource controls, audit, or authorized state. |
| `EXTREF-IBM-ZOS-SECURITY-SERVER-0001` | Security manager, protected resource, command, administration, callable service, and audit concepts. |
| `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001` | User, group, protected resource profile, access list, and default access concepts. |
| `EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001` | Authorized program boundary mapped to MFOS AMF authority classes and module checks. |
| `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001` | Negative testing for authorized-boundary confusion and unsafe parameter handling. |
| `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001` | Dataset and catalog resources require security-mediated access. |
| `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001` | Job submission, queues, SYSIN, SYSOUT, and spool resources require security decisions. |
| `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001` | Security-sensitive decisions create audit and accounting evidence. |
| `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001` | Security audit inspiration for denied access, authority used, and audit reason fields. |
| `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001` | Partition-aware authorization boundaries. |
| `EXTREF-IBM-Z-DPM-0001` | Partition management operations require explicit management-plane authorization. |

## 4. Normative Language

- `MUST`: required for the applicable profile.
- `SHOULD`: strongly recommended; deviation requires reviewed rationale and
  evidence.
- `MAY`: optional and not sufficient for an assurance claim.
- `MUST NOT`: prohibited.
- `UNSUPPORTED`: specified behavior not implemented; fail closed.
- `SPEC_GAP`: undefined by this specification; fail closed and open design work.

## 5. Design-Freeze Rules

| Rule ID | Rule |
| --- | --- |
| `MFOS-AUTH-FREEZE-0001` | This document freezes authorization semantics only. It is not production code authorization. |
| `MFOS-AUTH-FREEZE-0002` | Source references in this spec are `EXTREF-*` only. |
| `MFOS-AUTH-FREEZE-0003` | Requirement, test, evidence, invariant, gap, schema, and formal artifact IDs in this authorization area use MFOS-owned namespaces. |
| `MFOS-AUTH-FREEZE-0004` | `SPEC_GAP`, `UNSUPPORTED`, parser failure, policy absence, stale policy, and stale decision cache never produce allow. |
| `MFOS-AUTH-FREEZE-0005` | A downstream implementation task must cite requirements, schemas, tests, evidence, and open gaps before any code work can begin. |

## 6. securityd Responsibilities

| ID | Responsibility |
| --- | --- |
| `MFOS-AUTH-R-0001` | Principal, group, role, label, and authority-class resolution from trusted identity sources. |
| `MFOS-AUTH-R-0002` | Protected resource profile lookup and canonical object resolution. |
| `MFOS-AUTH-R-0003` | Central authorization decisions for dataset, catalog, spool, job, program, AMF module, operator command, partition, device, audit, update, Guard root, security policy, and workload policy resources. |
| `MFOS-AUTH-R-0004` | `SecurityDecision` production with decision result, reason, policy version, matched bindings, obligations, and constraints. |
| `MFOS-AUTH-R-0005` | Delegation evaluation, revocation handling, and delegation audit obligations. |
| `MFOS-AUTH-R-0006` | Emergency access workflow decisions, expiry enforcement, and incident-review obligations. |
| `MFOS-AUTH-R-0007` | Dual-control and operator-confirmation requirements. |
| `MFOS-AUTH-R-0008` | Policy bundle versioning, transaction, activation, rollback, epoch checks, and decision-cache invalidation. |
| `MFOS-AUTH-R-0009` | Policy lint gate for policy activation and rollback. |
| `MFOS-AUTH-R-0010` | Audit obligation generation and audit-before-return or audit-before-effect flags. |
| `MFOS-AUTH-R-0011` | Query authorization for security policy, audit stream, and decision evidence inspection. |

## 7. securityd Non-Responsibilities

`securityd` MUST NOT:

- Authenticate credentials directly except through a separately specified
  authentication service contract.
- Parse raw JCL-like job text.
- Interpret dataset records, blocks, or spool payloads.
- Schedule jobs or assign workload dispatch priority.
- Load AMF modules.
- Verify executable page mappings directly.
- Store audit records or rewrite committed audit evidence.
- Replace Guard approval where Guard approval is required.
- Treat POSIX `root`, administrator role, operator role, AMF authority, or
  emergency access as equivalent authority.
- Return allow when policy is missing, malformed, stale, unsupported, or
  undefined.

## 8. Protected Resource Classes

Protected resources are grouped into classes. Every protected operation on
these classes requires a `SecurityDecision` unless a separately specified
bootstrap exception exists.

```yaml
ProtectedResourceClass:
  - MFOS_RESOURCE_DATASET
  - MFOS_RESOURCE_CATALOG
  - MFOS_RESOURCE_SPOOL
  - MFOS_RESOURCE_JOB
  - MFOS_RESOURCE_PROGRAM
  - MFOS_RESOURCE_AMF_MODULE
  - MFOS_RESOURCE_OPERATOR_COMMAND
  - MFOS_RESOURCE_PARTITION
  - MFOS_RESOURCE_DEVICE
  - MFOS_RESOURCE_AUDIT_STREAM
  - MFOS_RESOURCE_UPDATE_ARTIFACT
  - MFOS_RESOURCE_GUARD_ROOT
  - MFOS_RESOURCE_SECURITY_POLICY
  - MFOS_RESOURCE_WORKLOAD_POLICY
  - MFOS_RESOURCE_AUTHORIZATION_EVIDENCE
  - MFOS_RESOURCE_SYSTEM
  - MFOS_RESOURCE_SERVICE
```

| Resource class | Examples | Required enforcement points |
| --- | --- | --- |
| `MFOS_RESOURCE_DATASET` | User dataset, system dataset, module dataset | `datasetd`, `jobd`, nucleus handle issuer |
| `MFOS_RESOURCE_CATALOG` | Dataset name entry, system catalog entry | `catalogd`, `datasetd` |
| `MFOS_RESOURCE_SPOOL` | SYSIN, SYSOUT, held output, exported spool | `spoold`, `jobd`, `operatord` |
| `MFOS_RESOURCE_JOB` | Submit, cancel, hold, restart, inspect | `jobd`, `operatord` |
| `MFOS_RESOURCE_PROGRAM` | Execute program, establish program identity | `jobd`, `amfd` |
| `MFOS_RESOURCE_AMF_MODULE` | Load authorized extension module | `amfd`, nucleus, Guard when required |
| `MFOS_RESOURCE_OPERATOR_COMMAND` | Typed command such as display, cancel, purge, activate | `operatord` |
| `MFOS_RESOURCE_PARTITION` | Create, load, start, quiesce, destroy | PXM or partition backend |
| `MFOS_RESOURCE_DEVICE` | Assign, release, reset, teardown | PXM or device backend |
| `MFOS_RESOURCE_AUDIT_STREAM` | Query, export, retention update, seal | `auditd`, `securityd` |
| `MFOS_RESOURCE_UPDATE_ARTIFACT` | Stage, approve, activate, roll back update | `uvsd`, `operatord` |
| `MFOS_RESOURCE_GUARD_ROOT` | Seal, verify, attest, transition | Guard and policy-root workflow |
| `MFOS_RESOURCE_SECURITY_POLICY` | Create, stage, commit, roll back policy | `securityd`, `operatord` |
| `MFOS_RESOURCE_WORKLOAD_POLICY` | Activate workload policy, inspect service class policy | `workpolicyd`, `operatord` |
| `MFOS_RESOURCE_AUTHORIZATION_EVIDENCE` | Decision evidence, policy lint result, approval record | `securityd`, `auditd` |
| `MFOS_RESOURCE_SYSTEM` | Local system state, emergency-state target, service registry display | `operatord`, nucleus-facing service registry |
| `MFOS_RESOURCE_SERVICE` | Managed service instance, service lifecycle display or control target | service registry, `operatord` |

## 9. Operation Vocabulary

```yaml
Operation:
  - MFOS_OP_READ
  - MFOS_OP_WRITE
  - MFOS_OP_APPEND
  - MFOS_OP_CREATE
  - MFOS_OP_UPDATE
  - MFOS_OP_DELETE
  - MFOS_OP_PURGE
  - MFOS_OP_EXECUTE
  - MFOS_OP_SUBMIT
  - MFOS_OP_CANCEL
  - MFOS_OP_BROWSE
  - MFOS_OP_EXPORT
  - MFOS_OP_HOLD
  - MFOS_OP_RELEASE
  - MFOS_OP_LOAD
  - MFOS_OP_ACTIVATE
  - MFOS_OP_DEACTIVATE
  - MFOS_OP_ASSIGN
  - MFOS_OP_QUERY
  - MFOS_OP_ADMINISTER
  - MFOS_OP_ATTEST
  - MFOS_OP_DELEGATE
  - MFOS_OP_ROLLBACK
```

Rules:

- Operation names are shared vocabulary, not universal grants.
- Each resource class MUST define its valid operation set.
- Unknown resource/operation pairs return `SPEC_GAP` and `MFOS_ERR_SPEC_GAP`.
- Known but unimplemented pairs return `UNSUPPORTED` and
  `MFOS_ERR_UNSUPPORTED`.
- Alias operations MUST canonicalize before policy evaluation.

### 9.1 Valid Operation Matrix

| Resource class | Valid operation families |
| --- | --- |
| `MFOS_RESOURCE_DATASET` | `MFOS_OP_READ`, `MFOS_OP_WRITE`, `MFOS_OP_APPEND`, `MFOS_OP_CREATE`, `MFOS_OP_UPDATE`, `MFOS_OP_DELETE`, `MFOS_OP_ADMINISTER` |
| `MFOS_RESOURCE_CATALOG` | `MFOS_OP_READ`, `MFOS_OP_CREATE`, `MFOS_OP_UPDATE`, `MFOS_OP_DELETE`, `MFOS_OP_QUERY`, `MFOS_OP_ADMINISTER` |
| `MFOS_RESOURCE_SPOOL` | `MFOS_OP_BROWSE`, `MFOS_OP_EXPORT`, `MFOS_OP_HOLD`, `MFOS_OP_RELEASE`, `MFOS_OP_PURGE`, `MFOS_OP_QUERY` |
| `MFOS_RESOURCE_JOB` | `MFOS_OP_SUBMIT`, `MFOS_OP_CANCEL`, `MFOS_OP_HOLD`, `MFOS_OP_RELEASE`, `MFOS_OP_QUERY`, `MFOS_OP_ADMINISTER` |
| `MFOS_RESOURCE_PROGRAM` | `MFOS_OP_EXECUTE`, `MFOS_OP_QUERY` |
| `MFOS_RESOURCE_AMF_MODULE` | `MFOS_OP_LOAD`, `MFOS_OP_QUERY`, `MFOS_OP_ADMINISTER` |
| `MFOS_RESOURCE_OPERATOR_COMMAND` | `MFOS_OP_EXECUTE`, `MFOS_OP_QUERY`, `MFOS_OP_ADMINISTER` |
| `MFOS_RESOURCE_PARTITION` | `MFOS_OP_CREATE`, `MFOS_OP_LOAD`, `MFOS_OP_ACTIVATE`, `MFOS_OP_DEACTIVATE`, `MFOS_OP_QUERY`, `MFOS_OP_ADMINISTER` |
| `MFOS_RESOURCE_DEVICE` | `MFOS_OP_ASSIGN`, `MFOS_OP_RELEASE`, `MFOS_OP_QUERY`, `MFOS_OP_ADMINISTER` |
| `MFOS_RESOURCE_AUDIT_STREAM` | `MFOS_OP_QUERY`, `MFOS_OP_EXPORT`, `MFOS_OP_UPDATE`, `MFOS_OP_ADMINISTER` |
| `MFOS_RESOURCE_UPDATE_ARTIFACT` | `MFOS_OP_CREATE`, `MFOS_OP_UPDATE`, `MFOS_OP_ACTIVATE`, `MFOS_OP_ROLLBACK`, `MFOS_OP_QUERY`, `MFOS_OP_ADMINISTER` |
| `MFOS_RESOURCE_GUARD_ROOT` | `MFOS_OP_ATTEST`, `MFOS_OP_ACTIVATE`, `MFOS_OP_QUERY`, `MFOS_OP_ADMINISTER` |
| `MFOS_RESOURCE_SECURITY_POLICY` | `MFOS_OP_CREATE`, `MFOS_OP_UPDATE`, `MFOS_OP_ACTIVATE`, `MFOS_OP_ROLLBACK`, `MFOS_OP_QUERY`, `MFOS_OP_ADMINISTER`, `MFOS_OP_DELEGATE` |
| `MFOS_RESOURCE_WORKLOAD_POLICY` | `MFOS_OP_CREATE`, `MFOS_OP_UPDATE`, `MFOS_OP_ACTIVATE`, `MFOS_OP_QUERY`, `MFOS_OP_ADMINISTER` |
| `MFOS_RESOURCE_AUTHORIZATION_EVIDENCE` | `MFOS_OP_QUERY`, `MFOS_OP_EXPORT`, `MFOS_OP_ADMINISTER` |
| `MFOS_RESOURCE_SYSTEM` | `MFOS_OP_QUERY`, `MFOS_OP_ADMINISTER` |
| `MFOS_RESOURCE_SERVICE` | `MFOS_OP_QUERY`, `MFOS_OP_ACTIVATE`, `MFOS_OP_DEACTIVATE`, `MFOS_OP_ADMINISTER` |

## 10. Subject Model

```yaml
Subject:
  subject_id: MFOS-owned string
  subject_type: MFOS_SUBJECT_HUMAN | MFOS_SUBJECT_SERVICE | MFOS_SUBJECT_JOB | MFOS_SUBJECT_PROGRAM | MFOS_SUBJECT_OPERATOR | MFOS_SUBJECT_PARTITION | MFOS_SUBJECT_SYSTEM
  principal_ref: MFOS-owned string?
  effective_principal_ref: MFOS-owned string?
  groups: [MFOS-owned string]
  roles: [MFOS-owned string]
  authority_classes: [MFOS-owned string]
  labels: [string]
  job_ref: MFOS-owned string?
  program_identity_ref: MFOS-owned string?
  service_ref: MFOS-owned string?
  operator_session_ref: MFOS-owned string?
  partition_ref: MFOS-owned string?
  authentication_context:
    auth_strength: MFOS_AUTH_NONE | MFOS_AUTH_PASSWORD | MFOS_AUTH_MFA | MFOS_AUTH_CERTIFICATE | MFOS_AUTH_HARDWARE_BACKED | MFOS_AUTH_RECOVERY
    authenticated_at_utc: Timestamp?
    expires_at_utc: Timestamp?
  emergency_context:
    active: bool
    reason_ref: MFOS-owned string?
    expires_at_utc: Timestamp?
    incident_ref: MFOS-owned string?
```

Rules:

- Caller-supplied subject identity MUST NOT override trusted nucleus,
  scheduler, service, or operator-session identity.
- Job effective principal MUST be established before protected resource open.
- Program identity MUST be established before execute or AMF checks.
- Emergency context MUST be explicit, time-bound, reason-bound, and audited.
- A disabled, locked, expired, unauthenticated, or unresolved subject is
  unauthorized.

## 11. Object Model

```yaml
ObjectRef:
  resource_class: ProtectedResourceClass
  object_id: MFOS-owned string
  object_name: string?
  owner_principal_ref: MFOS-owned string?
  security_profile_ref: MFOS-owned string?
  object_generation: uint64?
  catalog_generation: uint64?
  partition_ref: MFOS-owned string?
  guard_root_ref: MFOS-owned string?
  source_matrix_refs: [EXTREF-*]
```

Rules:

- Object refs MUST be canonicalized before policy evaluation.
- Generation-aware objects MUST include generation in the decision context.
- A missing security profile fails closed unless a bootstrap exception is
  explicitly specified.
- A display name is never the authority-bearing object identity.

## 12. Decision Context

```yaml
DecisionContext:
  request_id: MFOS-owned string
  correlation_id: MFOS-owned string
  timestamp_utc: Timestamp
  partition_ref: MFOS-owned string
  requested_policy_version: uint64?
  active_policy_version_seen_by_caller: uint64?
  activation_profile_hash: Digest?
  job_context:
    job_ref: MFOS-owned string?
    job_class: string?
    service_class: string?
    step_name: string?
  operator_context:
    command_ref: MFOS-owned string?
    console_ref: MFOS-owned string?
    automation: bool
    confirmation_token_ref: MFOS-owned string?
    dual_control_token_ref: MFOS-owned string?
  program_context:
    program_ref: MFOS-owned string?
    module_ref: MFOS-owned string?
    signer_ref: MFOS-owned string?
    digest: Digest?
    authority_class_ref: MFOS-owned string?
  dataset_context:
    dataset_name: string?
    disposition: MFOS_DISP_SHR | MFOS_DISP_OLD | MFOS_DISP_NEW | MFOS_DISP_MOD | MFOS_DISP_SYSOUT?
    catalog_generation: uint64?
    dataset_generation: uint64?
  update_context:
    artifact_ref: MFOS-owned string?
    generation: uint64?
    security_epoch: uint64?
  guard_context:
    root_ref: MFOS-owned string?
    root_version: uint64?
    guard_required: bool
  emergency_context:
    requested: bool
    reason_ref: MFOS-owned string?
    expires_at_utc: Timestamp?
  delegation_context:
    delegation_chain_refs: [MFOS-owned string]
    delegation_depth: uint8
```

Rules:

- Context fields MUST be typed, bounded, and canonicalized.
- Missing context for a policy condition fails closed.
- Context values used for authorization MUST be copied into decision evidence.
- Context cannot weaken object generation, partition, policy version, or subject
  binding.

## 13. SecurityDecision Contract

The machine-readable design schema is
`schemas/mfos/security-decision.schema.yml`.

```yaml
SecurityDecision:
  schema_version: 1
  decision_id: MFOS-owned string
  request_id: MFOS-owned string
  subject: Subject
  object: ObjectRef
  operation: Operation
  context: DecisionContext
  result: MFOS_AUTH_ALLOW | MFOS_AUTH_ALLOW_WITH_OBLIGATIONS | MFOS_AUTH_DENY | MFOS_AUTH_REQUIRE_MFA | MFOS_AUTH_REQUIRE_DUAL_CONTROL | MFOS_AUTH_REQUIRE_BREAK_GLASS | MFOS_AUTH_REQUIRE_OPERATOR_CONFIRMATION | MFOS_AUTH_REQUIRE_GUARD_APPROVAL | MFOS_AUTH_UNSUPPORTED | MFOS_AUTH_SPEC_GAP | MFOS_AUTH_ERROR
  reason_code: MFOS-owned string
  policy_id: MFOS-owned string
  policy_version: uint64
  policy_epoch: uint64
  matched_binding_refs: [MFOS-owned string]
  obligations: [AuthorizationObligation]
  handle_constraints: AuthorizationHandleConstraints
  cacheability: DecisionCacheability
  issued_at_utc: Timestamp
  expires_at_utc: Timestamp?
  evidence_refs: [MFOS-owned string]
```

Rules:

- A `SecurityDecision` is scoped to the exact subject, object, operation,
  context, policy version, policy epoch, and matched bindings.
- `MFOS_AUTH_REQUIRE_*` results are not allow results.
- `MFOS_AUTH_UNSUPPORTED`, `MFOS_AUTH_SPEC_GAP`, and `MFOS_AUTH_ERROR` are not
  allow results.
- `MFOS_AUTH_ALLOW_WITH_OBLIGATIONS` is not effective until required obligations
  are satisfied at their declared barrier.
- A decision result MUST identify the policy version and policy epoch used.
- A decision with missing or unparseable obligations fails closed.

## 14. Decision Results

| Result | Meaning | Caller behavior |
| --- | --- | --- |
| `MFOS_AUTH_ALLOW` | Operation is permitted subject to constraints. | Enforce handle constraints and non-blocking obligations. |
| `MFOS_AUTH_ALLOW_WITH_OBLIGATIONS` | Operation is permitted only after required obligations are satisfied. | Satisfy pre-return or pre-effect obligations before proceeding. |
| `MFOS_AUTH_DENY` | Policy prohibits the operation. | No handle, no side effect, audit as required. |
| `MFOS_AUTH_REQUIRE_MFA` | Stronger authentication is required. | Do not proceed; obtain a fresh auth context. |
| `MFOS_AUTH_REQUIRE_DUAL_CONTROL` | Independent approval is required. | Do not proceed until a valid dual-control token is presented. |
| `MFOS_AUTH_REQUIRE_BREAK_GLASS` | Emergency workflow is required. | Do not proceed without explicit emergency context. |
| `MFOS_AUTH_REQUIRE_OPERATOR_CONFIRMATION` | Human confirmation is required. | Do not proceed until confirmation token is verified. |
| `MFOS_AUTH_REQUIRE_GUARD_APPROVAL` | Guard approval is required by profile, object, or policy. | Do not proceed until Guard result is bound to the request. |
| `MFOS_AUTH_UNSUPPORTED` | Behavior is specified but unavailable. | Fail closed with `MFOS_ERR_UNSUPPORTED`. |
| `MFOS_AUTH_SPEC_GAP` | Behavior is undefined. | Fail closed with `MFOS_ERR_SPEC_GAP` and open design work. |
| `MFOS_AUTH_ERROR` | Validation or internal decision construction failed. | Fail closed with typed error and audit when security-sensitive. |

## 15. Obligation Model

```yaml
AuthorizationObligation:
  obligation_id: MFOS-owned string
  kind: MFOS_OBL_AUDIT | MFOS_OBL_MFA | MFOS_OBL_DUAL_CONTROL | MFOS_OBL_EMERGENCY_REASON | MFOS_OBL_EMERGENCY_EXPIRY | MFOS_OBL_OPERATOR_CONFIRMATION | MFOS_OBL_GUARD_APPROVAL | MFOS_OBL_RATE_LIMIT | MFOS_OBL_NOTIFY | MFOS_OBL_REMOTE_EXPORT | MFOS_OBL_LOCKDOWN | MFOS_OBL_POLICY_LINT | MFOS_OBL_INCIDENT_REVIEW
  required_before_return: bool
  required_before_effect: bool
  failure_policy: MFOS_OBL_FAIL_CLOSED | MFOS_OBL_DEGRADED_READ_ONLY | MFOS_OBL_RECOVERY_MODE
  payload_ref: MFOS-owned string?
  audit_class: MFOS_AUDIT_SECURITY_DECISION | MFOS_AUDIT_SECURITY_DENY | MFOS_AUDIT_POLICY_CHANGE | MFOS_AUDIT_DATASET_ACCESS | MFOS_AUDIT_SPOOL_ACCESS | MFOS_AUDIT_OPERATOR_COMMAND | MFOS_AUDIT_AMF_LOAD | MFOS_AUDIT_PARTITION_OPERATION | MFOS_AUDIT_BREAK_GLASS | MFOS_AUDIT_POLICY_LINT?
```

Rules:

- Obligations are part of the decision, not advisory metadata.
- Required obligations MUST be satisfied before their declared barrier.
- A failed `MFOS_OBL_AUDIT` with `required_before_return` or
  `required_before_effect` fails closed.
- `MFOS_OBL_LOCKDOWN` can only make the caller stricter; it cannot authorize
  progress.
- Emergency and dual-control obligations MUST be auditable.

## 16. PolicyBinding Contract

The machine-readable design schema is
`schemas/mfos/policy-binding.schema.yml`.

```yaml
PolicyBinding:
  schema_version: 1
  binding_id: MFOS-owned string
  policy_id: MFOS-owned string
  policy_version_min: uint64
  policy_version_max: uint64?
  status: MFOS_BINDING_DRAFT | MFOS_BINDING_STAGED | MFOS_BINDING_ACTIVE | MFOS_BINDING_RETIRED | MFOS_BINDING_ROLLED_BACK
  precedence: uint32
  effect: MFOS_BINDING_ALLOW | MFOS_BINDING_DENY | MFOS_BINDING_REQUIRE_MFA | MFOS_BINDING_REQUIRE_DUAL_CONTROL | MFOS_BINDING_REQUIRE_BREAK_GLASS | MFOS_BINDING_REQUIRE_OPERATOR_CONFIRMATION | MFOS_BINDING_REQUIRE_GUARD_APPROVAL
  subject_selector: SubjectSelector
  object_selector: ObjectSelector
  operation_set: [Operation]
  context_conditions: [ContextCondition]
  obligations: [AuthorizationObligation]
  delegation:
    delegable: bool
    max_chain_depth: uint8
    allow_transitive_delegation: bool
  emergency_access:
    permitted: bool
    maximum_lifetime_minutes: uint16
    incident_review_required: bool
  dual_control:
    required: bool
    independent_principals_required: bool
    self_approval_allowed: false
  source_matrix_refs: [EXTREF-*]
```

Rules:

- Explicit deny dominates allow.
- Higher-precedence bindings cannot override `SPEC_GAP`, parser failure, stale
  policy, or malformed policy into allow.
- A binding that requires an obligation MUST include the obligation in every
  matching `SecurityDecision`.
- A binding with emergency access or delegation MUST include expiry and audit
  obligations.
- A binding with Guard approval cannot replace `securityd` authorization, and
  `securityd` authorization cannot replace Guard approval.

## 17. Policy Versioning and Activation

```yaml
PolicyBundle:
  policy_id: MFOS-owned string
  policy_version: uint64
  policy_epoch: uint64
  security_epoch: uint64
  status: MFOS_POLICY_STAGED | MFOS_POLICY_ACTIVE | MFOS_POLICY_RETIRED | MFOS_POLICY_ROLLED_BACK
  bindings: [PolicyBinding]
  principal_index_digest: Digest
  group_index_digest: Digest
  role_index_digest: Digest
  resource_index_digest: Digest
  created_by: MFOS-owned string
  approved_by: [MFOS-owned string]
  created_at_utc: Timestamp
  activated_at_utc: Timestamp?
  source_matrix_refs: [EXTREF-*]
```

Rules:

- Active policy bundles are immutable.
- Policy activation creates a new active `policy_version`.
- Rollback activates a new `policy_version` whose content may match a previous
  bundle; it MUST NOT reuse an old active version number.
- `security_epoch` downgrade is rejected.
- Decision caches and handles bound to previous policy versions MUST be
  invalidated or revalidated according to explicit migration rules.
- Policy activation and rollback require policy lint, authorization,
  dual-control when required, and audit.

## 18. Delegation

Delegation is a policy-bound authority transfer. It is not identity mutation and
does not make the delegate the delegator.

Rules:

- Delegation requires `MFOS_OP_DELEGATE` on `MFOS_RESOURCE_SECURITY_POLICY` or
  on the delegated resource class as specified by policy.
- Delegation MUST be scope-bound to subject selector, object selector,
  operations, context conditions, policy version range, and expiry.
- Delegation MUST NOT grant more authority than the delegator has at the time
  of delegation.
- Delegation depth greater than the binding maximum fails closed.
- Transitive delegation is denied unless the binding explicitly permits it.
- Delegation of AMF load, Guard root transition, policy activation, policy
  rollback, audit retention weakening, or emergency access requires explicit
  policy binding and dual-control.
- Delegation revocation invalidates cached decisions and handles using the
  revoked delegation.
- Self-delegation is rejected as malformed authority evidence.

## 19. Emergency Access

Emergency access is an exceptional authorization context, not a superuser mode.

Rules:

- Emergency access MUST be reason-bound, operator-bound, incident-bound,
  time-bound, and audited before activation.
- Emergency access maximum lifetime is 60 minutes unless a stricter profile
  rule applies. Longer lifetime is `SPEC_GAP`.
- Emergency access MUST NOT disable audit, policy lint, dual control, Guard
  approval, or evidence capture.
- Emergency access MUST NOT grant AMF load, Guard root, policy activation,
  policy rollback, audit retention weakening, partition destructive operation,
  or update activation unless the binding explicitly permits that operation and
  adds dual-control plus incident review.
- Emergency access expiry or revocation invalidates decisions and handles that
  depend on emergency context.
- Emergency access closeout MUST create incident-review evidence.

## 20. Dual Control and Operator Confirmation

Rules:

- Dual control requires two independent effective principals.
- The requester cannot satisfy the approver role for the same decision.
- A service account cannot satisfy human dual control unless the policy binding
  explicitly defines an automation approval role and its evidence requirements.
- Dual-control tokens are bound to request ID, subject, object, operation,
  context digest, policy version, policy epoch, and expiry.
- Operator confirmation is not dual control. It proves explicit human
  confirmation for the same operator session.
- Dual-control and confirmation failures produce no protected side effect.

## 21. Policy Rollback

Rules:

- Rollback requires authorization on `MFOS_RESOURCE_SECURITY_POLICY` with
  `MFOS_OP_ROLLBACK`.
- Rollback target MUST be a previously active, immutable, measurable policy
  bundle that passes current lint requirements.
- Rollback creates a new active policy version; it never reuses the old version
  number.
- Rollback MUST NOT decrease `security_epoch`.
- Rollback MUST preserve or strengthen audit obligations for security-sensitive
  resources unless a reviewed spec update defines otherwise.
- Rollback requires audit before commit and audit after commit.
- Rollback failure leaves the prior active policy unchanged.

## 22. Policy Lint Gate

Policy lint is a pre-activation and pre-rollback control. It is not a runtime
authorization allow.

| ID | Required lint property |
| --- | --- |
| `MFOS-AUTH-LINT-0001` | Default access for protected resources is deny unless an explicit public read-only exception is documented and audited. |
| `MFOS-AUTH-LINT-0002` | Wildcard destructive dataset, catalog, spool, device, partition, update, Guard root, or policy authority is blocked without explicit dual-control and owner evidence. |
| `MFOS-AUTH-LINT-0003` | AMF authority cannot be granted to broad administrator, operator, automation, default, or emergency roles without explicit module-governance binding. |
| `MFOS-AUTH-LINT-0004` | Emergency access requires reason, expiry, audit, incident review, and bounded scope. |
| `MFOS-AUTH-LINT-0005` | Spool export, audit export, and authorization evidence export require audit and redaction policy. |
| `MFOS-AUTH-LINT-0006` | Policy activation or rollback that changes security-sensitive authority requires dual-control. |
| `MFOS-AUTH-LINT-0007` | Rollback target cannot lower security epoch or weaken mandatory audit obligations. |

Rules:

- Blocking lint findings prevent activation and rollback.
- `SPEC_GAP` or `UNSUPPORTED` lint behavior prevents activation when the lint
  rule is required for the target profile.
- Lint evidence MUST be linked to the activation or rollback audit record.

## 23. Decision Algorithm

Logical algorithm:

```text
1. Validate request schema.
2. Canonicalize subject from trusted context.
3. Canonicalize object reference.
4. Canonicalize operation and validate resource/operation pair.
5. Load active policy bundle.
6. Verify requested policy version and policy epoch.
7. Resolve principal, group, role, label, authority class, delegation, and emergency context.
8. Resolve resource profile and object generation.
9. Evaluate explicit deny bindings.
10. Evaluate required obligations such as MFA, dual control, emergency access, confirmation, Guard approval, and lint.
11. Evaluate allow bindings.
12. Attach mandatory audit and evidence obligations.
13. Attach handle constraints and cacheability.
14. Return typed SecurityDecision.
```

Required fail-closed points:

- Invalid schema.
- Untrusted subject identity.
- Object canonicalization failure.
- Unknown resource/operation pair.
- Policy unavailable, malformed, stale, or mismatched.
- Resource profile missing.
- Required context missing.
- Delegation chain invalid.
- Emergency context expired or malformed.
- Dual-control token invalid.
- Audit obligation cannot be constructed.

## 24. Enforcement Points

| Enforcement point | Required behavior |
| --- | --- |
| Nucleus handle issuer | Refuse protected handles without matching allow decision and satisfied pre-effect obligations. |
| `catalogd` | Authorize catalog read/update/delete and system dataset catalog changes. |
| `datasetd` | Authorize open/create/update/delete and bind handles to subject, object generation, operation, policy version, and expiry. |
| `jobd` | Authorize submit, execute, program load, and dataset/spool resolution. |
| `spoold` | Authorize browse, export, hold, release, and purge. |
| `operatord` | Parse typed command, authorize command, satisfy confirmation or dual control, and audit before effect. |
| `amfd` | Require `securityd` decision plus AMF manifest, signature, revocation, ABI, and profile checks. |
| `auditd` | Authorize audit query, export, retention, and redaction policy changes through `securityd`. |
| `uvsd` | Authorize update approval, activation, and rollback. |
| PXM | Authorize partition and device operations when exposed to MFOS operators or services. |
| Guard | Provide required Guard approval evidence; never replace `securityd`. |

## 25. State Machines

The formal/design artifact is `formal/tla/authorization/MFOSAuthorization.tla`.

### 25.1 Decision Lifecycle

```text
MFOS_AUTH_STATE_REQUEST_RECEIVED
  -> MFOS_AUTH_STATE_VALIDATE_REQUEST
  -> MFOS_AUTH_STATE_CANONICALIZE_SUBJECT
  -> MFOS_AUTH_STATE_CANONICALIZE_OBJECT
  -> MFOS_AUTH_STATE_LOAD_POLICY
  -> MFOS_AUTH_STATE_EVALUATE_BINDINGS
  -> MFOS_AUTH_STATE_BUILD_OBLIGATIONS
  -> MFOS_AUTH_STATE_RETURN_DECISION
```

Terminal non-allow states:

```text
MFOS_AUTH_STATE_INVALID_REQUEST
MFOS_AUTH_STATE_UNTRUSTED_SUBJECT
MFOS_AUTH_STATE_UNKNOWN_OBJECT
MFOS_AUTH_STATE_INVALID_OPERATION
MFOS_AUTH_STATE_POLICY_UNAVAILABLE
MFOS_AUTH_STATE_POLICY_VERSION_MISMATCH
MFOS_AUTH_STATE_PROFILE_MISSING
MFOS_AUTH_STATE_OBLIGATION_FAILED
MFOS_AUTH_STATE_UNSUPPORTED
MFOS_AUTH_STATE_SPEC_GAP
```

### 25.2 Protected Effect Lifecycle

```text
MFOS_AUTH_STATE_DECISION_RETURNED
  -> MFOS_AUTH_STATE_SATISFY_PRE_EFFECT_OBLIGATIONS
  -> MFOS_AUTH_STATE_BIND_HANDLE
  -> MFOS_AUTH_STATE_EFFECT_ALLOWED
```

`MFOS_AUTH_STATE_BIND_HANDLE` and `MFOS_AUTH_STATE_EFFECT_ALLOWED` are reachable
only from `MFOS_AUTH_ALLOW` or `MFOS_AUTH_ALLOW_WITH_OBLIGATIONS` with required
pre-effect obligations satisfied.

### 25.3 Policy Transaction Lifecycle

```text
MFOS_AUTH_STATE_BEGIN_POLICY_TX
  -> MFOS_AUTH_STATE_VALIDATE_POLICY_SCHEMA
  -> MFOS_AUTH_STATE_AUTHORIZE_POLICY_CHANGE
  -> MFOS_AUTH_STATE_STAGE_POLICY
  -> MFOS_AUTH_STATE_RUN_POLICY_LINT
  -> MFOS_AUTH_STATE_REQUIRE_APPROVALS
  -> MFOS_AUTH_STATE_AUDIT_PRECOMMIT
  -> MFOS_AUTH_STATE_COMMIT_POLICY_VERSION
  -> MFOS_AUTH_STATE_INVALIDATE_DECISION_CACHE
  -> MFOS_AUTH_STATE_AUDIT_COMMIT
  -> MFOS_AUTH_STATE_POLICY_ACTIVE
```

Failure states:

```text
MFOS_AUTH_STATE_POLICY_SCHEMA_INVALID
MFOS_AUTH_STATE_POLICY_LINT_FAILED
MFOS_AUTH_STATE_APPROVAL_MISSING
MFOS_AUTH_STATE_AUDIT_REQUIRED_BUT_UNAVAILABLE
MFOS_AUTH_STATE_EPOCH_DOWNGRADE_DETECTED
MFOS_AUTH_STATE_ROLLBACK_NOT_AUTHORIZED
```

### 25.4 Emergency Access Lifecycle

```text
MFOS_AUTH_STATE_REQUEST_EMERGENCY_ACCESS
  -> MFOS_AUTH_STATE_AUTHENTICATE_OPERATOR
  -> MFOS_AUTH_STATE_AUTHORIZE_EMERGENCY_ACCESS
  -> MFOS_AUTH_STATE_REQUIRE_REASON
  -> MFOS_AUTH_STATE_SET_EXPIRY
  -> MFOS_AUTH_STATE_AUDIT_BEFORE_ENABLE
  -> MFOS_AUTH_STATE_ENABLE_EMERGENCY_CONTEXT
  -> MFOS_AUTH_STATE_MONITOR_EMERGENCY_USE
  -> MFOS_AUTH_STATE_EXPIRE_OR_REVOKE
  -> MFOS_AUTH_STATE_AUDIT_CLOSE
  -> MFOS_AUTH_STATE_INCIDENT_REVIEW_REQUIRED
```

## 26. Invalid Transitions

| ID | Invalid transition | Required result |
| --- | --- | --- |
| `MFOS-AUTH-INVALID-0001` | `MFOS_AUTH_DENY` to protected handle or side effect. | Reject and audit as security violation. |
| `MFOS-AUTH-INVALID-0002` | `MFOS_AUTH_REQUIRE_*` to protected handle or side effect without satisfying the requirement. | Reject and return requirement result. |
| `MFOS-AUTH-INVALID-0003` | `MFOS_AUTH_UNSUPPORTED` or `MFOS_AUTH_SPEC_GAP` to allow. | Reject with typed fail-closed error. |
| `MFOS-AUTH-INVALID-0004` | Policy rollback directly activates an old version number. | Reject rollback transaction. |
| `MFOS-AUTH-INVALID-0005` | Emergency access enables while audit is unavailable. | Reject emergency activation. |
| `MFOS-AUTH-INVALID-0006` | Dual-control approval uses the same effective principal twice. | Reject approval evidence. |
| `MFOS-AUTH-INVALID-0007` | Delegation grants authority broader than delegator's current effective authority. | Reject delegation and invalidate dependent cache entries. |
| `MFOS-AUTH-INVALID-0008` | Policy lint blocker transitions to active policy. | Reject activation. |
| `MFOS-AUTH-INVALID-0009` | Guard-required operation proceeds without Guard approval evidence. | Reject operation. |
| `MFOS-AUTH-INVALID-0010` | Stale cached decision survives policy version or delegation revocation. | Re-evaluate or deny; never allow from stale cache. |

## 27. Invariants

```text
MFOS-INV-AUTH-0001:
  A protected resource handle exists only after securityd produced
  MFOS_AUTH_ALLOW or MFOS_AUTH_ALLOW_WITH_OBLIGATIONS for the same subject,
  object, operation, context, policy_version, and policy_epoch.

MFOS-INV-AUTH-0002:
  MFOS_AUTH_DENY, MFOS_AUTH_UNSUPPORTED, MFOS_AUTH_SPEC_GAP, and
  MFOS_AUTH_ERROR produce no protected side effects.

MFOS-INV-AUTH-0003:
  MFOS_AUTH_REQUIRE_* results are not allow results.

MFOS-INV-AUTH-0004:
  Policy version, policy epoch, delegation revocation, emergency expiry, or
  binding retirement invalidates dependent cached decisions.

MFOS-INV-AUTH-0005:
  Emergency access cannot disable audit, lint, dual control, Guard approval,
  or incident review obligations.

MFOS-INV-AUTH-0006:
  Workload policy and dispatch priority cannot grant resource authorization.

MFOS-INV-AUTH-0007:
  AMF authority requires explicit AMF authority class and cannot be inferred
  from administrator, operator, emergency, or service role alone.

MFOS-INV-AUTH-0008:
  Guard approval cannot replace securityd authorization, and securityd
  authorization cannot replace Guard approval when Guard is required.

MFOS-INV-AUTH-0009:
  Local enforcement points can make a decision stricter but cannot create a
  broader allow than securityd.

MFOS-INV-AUTH-0010:
  Parser ambiguity, duplicate fields, unknown enum values, unknown policy
  expressions, and malformed bindings cannot be converted into allow.
```

## 28. Failure Modes

| Failure | Required result |
| --- | --- |
| Invalid request schema | `MFOS_ERR_INVALID_PARAMETER`; no side effect. |
| Caller identity untrusted | `MFOS_ERR_UNAUTHENTICATED`; audit if security-sensitive. |
| Subject denied by policy | `MFOS_ERR_POLICY_DENIED`; no side effect. |
| Policy unavailable | Fail closed; only explicitly specified recovery query mode can operate. |
| Policy malformed | `MFOS_ERR_POLICY_INVALID`; no active policy change or protected effect. |
| Policy version mismatch | `MFOS_ERR_POLICY_VERSION_MISMATCH`; no handle. |
| Policy epoch mismatch | `MFOS_ERR_POLICY_EPOCH_MISMATCH`; re-evaluate or deny. |
| Security epoch downgrade | `MFOS_ERR_ROLLBACK_DETECTED`; alert and audit. |
| Missing resource profile | `MFOS_ERR_POLICY_DENIED` unless bootstrap exception exists. |
| Unknown resource/operation pair | `MFOS_ERR_SPEC_GAP`; no side effect. |
| Known operation unimplemented | `MFOS_ERR_UNSUPPORTED`; no side effect. |
| Required audit unavailable | `MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE`; no protected effect. |
| MFA required but absent | Return `MFOS_AUTH_REQUIRE_MFA`; no side effect. |
| Dual control required but absent | Return `MFOS_AUTH_REQUIRE_DUAL_CONTROL`; no side effect. |
| Dual control self-approval | `MFOS_ERR_DUAL_CONTROL_INVALID`; audit. |
| Delegation expired or revoked | `MFOS_ERR_DELEGATION_INVALID`; invalidate dependent decisions. |
| Emergency access expired | Deny, audit, and require closeout evidence. |
| Guard required but unavailable | `MFOS_ERR_GUARD_REQUIRED`; no side effect. |
| Policy lint blocker | `MFOS_ERR_POLICY_LINT_BLOCKED`; policy remains unchanged. |
| Decision cache stale | Re-evaluate or deny; never allow based on stale cache. |

## 29. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| `MFOS-REQ-AUTH-0001` | `securityd` MUST be the central decision point for protected resource access. | architecture inspection |
| `MFOS-REQ-AUTH-0002` | Decision input MUST include subject, object, operation, context, and policy version. | schema and interface test |
| `MFOS-REQ-AUTH-0003` | `SecurityDecision` MUST support obligations beyond allow and deny. | schema test |
| `MFOS-REQ-AUTH-0004` | `datasetd` MUST NOT issue protected dataset handles without an allow decision and satisfied required obligations. | negative test |
| `MFOS-REQ-AUTH-0005` | `jobd` MUST obtain authorization before job submit, step execute, program load, and dataset or spool resolution. | integration test |
| `MFOS-REQ-AUTH-0006` | `operatord` MUST obtain authorization before executing typed operator commands. | command negative test |
| `MFOS-REQ-AUTH-0007` | AMF load MUST pass through `securityd` and `amfd`; Guard approval is additionally required when policy or profile requires it. | AMF negative test |
| `MFOS-REQ-AUTH-0008` | Policy updates MUST be transactional and increment policy version. | transaction test |
| `MFOS-REQ-AUTH-0009` | Emergency access MUST require reason, expiry, operator identity, authorization, audit, and incident review. | emergency drill |
| `MFOS-REQ-AUTH-0010` | Policy rollback MUST require authorization, lint, approval, new policy version, and audit. | rollback test |
| `MFOS-REQ-AUTH-0011` | Missing, malformed, unsupported, stale, or undefined policy MUST fail closed. | negative test |
| `MFOS-REQ-AUTH-0012` | Denied protected-resource decisions MUST not create handles or side effects. | negative test |
| `MFOS-REQ-AUTH-0013` | Required audit obligations MUST be emitted before caller result or protected effect as specified. | audit integration test |
| `MFOS-REQ-AUTH-0014` | Decision caches MUST be invalidated on policy version change, policy epoch change, delegation revocation, binding retirement, or emergency expiry. | cache invalidation test |
| `MFOS-REQ-AUTH-0015` | Caller-supplied identity MUST NOT override trusted scheduler, service, nucleus, or operator-session identity. | negative test |
| `MFOS-REQ-AUTH-0016` | Delegation MUST be scope-bound, time-bound, revocable, and audited. | delegation negative test |
| `MFOS-REQ-AUTH-0017` | Dual-control approval MUST use independent effective principals and request-bound approval evidence. | dual-control negative test |
| `MFOS-REQ-AUTH-0018` | Policy lint blockers, unsupported required lint behavior, and lint spec gaps MUST block policy activation and rollback. | policy lint test |
| `MFOS-REQ-AUTH-0019` | Guard-required authorization MUST require both `securityd` allow and Guard approval evidence. | Guard integration test |
| `MFOS-REQ-AUTH-0020` | Authorization evidence query and export MUST be protected resources. | evidence access test |

## 30. Positive Tests

| Test ID | Description |
| --- | --- |
| `TEST-MFOS-AUTH-POS-0001` | Explicit dataset read binding allows a matching subject to read a matching dataset after audit obligation construction. |
| `TEST-MFOS-AUTH-POS-0002` | Job submit returns `MFOS_AUTH_ALLOW_WITH_OBLIGATIONS` with audit obligation and no side effect before required audit barrier. |
| `TEST-MFOS-AUTH-POS-0003` | Operator display command with matching authority class, confirmation not required, and valid session returns allow. |
| `TEST-MFOS-AUTH-POS-0004` | Destructive operator command returns `MFOS_AUTH_REQUIRE_OPERATOR_CONFIRMATION` before effect, then allow after valid confirmation. |
| `TEST-MFOS-AUTH-POS-0005` | Policy activation increments policy version and invalidates prior decision cache. |
| `TEST-MFOS-AUTH-POS-0006` | Emergency access activates only after reason, expiry, audit, authorization, and incident reference are present. |
| `TEST-MFOS-AUTH-POS-0007` | Delegated read authority works within object scope, operation scope, policy version range, and expiry. |
| `TEST-MFOS-AUTH-POS-0008` | Rollback creates a new policy version from a previously active lint-passing bundle without lowering security epoch. |

## 31. Negative Tests

| Test ID | Description |
| --- | --- |
| `NEG-MFOS-AUTH-NEG-0001` | Different subject attempts to read another subject's dataset; expect deny, no handle, and deny audit. |
| `NEG-MFOS-AUTH-NEG-0002` | Dataset open bypasses `securityd`; expect no handle and test failure. |
| `NEG-MFOS-AUTH-NEG-0003` | Caller supplies forged `effective_principal_ref`; expect untrusted subject rejection. |
| `NEG-MFOS-AUTH-NEG-0004` | Missing security profile on protected dataset; expect fail closed. |
| `NEG-MFOS-AUTH-NEG-0005` | Policy version mismatch; expect `MFOS_ERR_POLICY_VERSION_MISMATCH`. |
| `NEG-MFOS-AUTH-NEG-0006` | Required deny audit fails before caller result; expect `MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE`. |
| `NEG-MFOS-AUTH-NEG-0007` | Unknown resource/operation pair; expect `MFOS_ERR_SPEC_GAP`. |
| `NEG-MFOS-AUTH-NEG-0008` | Known but unimplemented operation; expect `MFOS_ERR_UNSUPPORTED`. |
| `NEG-MFOS-AUTH-NEG-0009` | Destructive operator command without confirmation attempts side effect; expect no side effect. |
| `NEG-MFOS-AUTH-NEG-0010` | Dual-control command is approved by same effective principal twice; expect rejection. |
| `NEG-MFOS-AUTH-NEG-0011` | Emergency access without reason, expiry, or incident reference; expect rejection. |
| `NEG-MFOS-AUTH-NEG-0012` | Emergency access attempts to disable audit; expect rejection. |
| `NEG-MFOS-AUTH-NEG-0013` | AMF load with administrator role but no AMF authority class; expect denial. |
| `NEG-MFOS-AUTH-NEG-0014` | Workload service class attempts to grant dataset access; expect policy rejection. |
| `NEG-MFOS-AUTH-NEG-0015` | Guard-required operation lacks Guard approval evidence; expect no protected transition. |
| `NEG-MFOS-AUTH-NEG-0016` | Policy rollback lowers security epoch; expect rollback detection. |
| `NEG-MFOS-AUTH-NEG-0017` | Stale cached decision is used after policy update, delegation revocation, or emergency expiry; expect re-evaluation or deny. |
| `NEG-MFOS-AUTH-NEG-0018` | Delegation grants broader scope than delegator has; expect rejection and audit. |
| `NEG-MFOS-AUTH-NEG-0019` | Policy lint blocker attempts to activate; expect policy remains unchanged. |
| `NEG-MFOS-AUTH-NEG-0020` | Authorization evidence export by unauthorized subject; expect deny and no evidence disclosure. |

## 32. Fuzz Tests

| Test ID | Target | Required property |
| --- | --- | --- |
| `TEST-MFOS-AUTH-FUZZ-0001` | `SecurityDecision` parser and canonicalizer. | Unknown enum, duplicate field, oversized payload, and malformed obligation fail closed. |
| `TEST-MFOS-AUTH-FUZZ-0002` | `PolicyBinding` parser and selector canonicalizer. | Ambiguous selector, wildcard destructive grant, and malformed condition cannot activate. |
| `TEST-MFOS-AUTH-FUZZ-0003` | Subject, group, role, and delegation expansion. | Cycles, depth overflow, and revoked delegation fail closed. |
| `TEST-MFOS-AUTH-FUZZ-0004` | Resource class and operation matrix evaluator. | Unknown pairs return `SPEC_GAP`; known unsupported pairs return `UNSUPPORTED`; neither allows. |
| `TEST-MFOS-AUTH-FUZZ-0005` | Operator confirmation and dual-control token parser. | Self-approval, mismatched request binding, expired token, and malformed token fail closed. |
| `TEST-MFOS-AUTH-FUZZ-0006` | Emergency access request parser. | Missing reason, invalid expiry, and audit-disabling fields fail closed. |
| `TEST-MFOS-AUTH-FUZZ-0007` | Policy transaction and rollback parser. | Epoch downgrade, old version reuse, lint bypass, and precommit audit omission fail closed. |
| `TEST-MFOS-AUTH-FUZZ-0008` | Decision cache key canonicalizer. | Policy version, policy epoch, object generation, context digest, and subject mismatch cannot hit allow cache. |

## 33. Evidence Requirements

| Evidence ID | Required evidence |
| --- | --- |
| `EV-MFOS-AUTH-SPEC-0001` | Reviewed design freeze report for this specification. |
| `EV-MFOS-AUTH-SCHEMA-0001` | Schema review for `schemas/mfos/security-decision.schema.yml`. |
| `EV-MFOS-AUTH-SCHEMA-0002` | Schema review for `schemas/mfos/policy-binding.schema.yml`. |
| `EV-MFOS-AUTH-FORMAL-0001` | State-machine review for `formal/tla/authorization/MFOSAuthorization.tla`. |
| `EV-MFOS-AUTH-TESTCAT-0001` | Review of `tests/catalog/phase-0-8-authorization-tests.yml`. |
| `EV-MFOS-AUTH-LINT-0001` | Policy lint gate evidence for activation and rollback semantics. |
| `EV-MFOS-AUTH-AUDIT-0001` | Audit obligation mapping showing before-return and before-effect barriers. |
| `EV-MFOS-AUTH-GAP-0001` | Open-gap review confirming no implementation may infer gap behavior. |

Evidence rules:

- Evidence artifacts are requirements for future implementation authorization;
  they are not implementation artifacts themselves.
- Evidence for denied protected-resource decisions MUST show absence of handles,
  absence of side effects, and required audit behavior.
- Fuzz evidence MUST include seed corpus description, target schema, and
  fail-closed assertions.
- Policy rollback evidence MUST include precommit audit, postcommit audit,
  policy version transition, lint result, and cache invalidation.

## 34. Spec Gaps

| Gap ID | Gap | Required handling |
| --- | --- | --- |
| `MFOS-GAP-AUTH-0001` | Concrete policy expression grammar is not fixed. | Return `MFOS_AUTH_SPEC_GAP`; no production parser inference. |
| `MFOS-GAP-AUTH-0002` | Bootstrap policy for first boot and recovery query mode is not fully specified. | Deny protected effects outside explicit bootstrap design. |
| `MFOS-GAP-AUTH-0003` | External authentication provider integration is not specified. | Authentication plugins cannot be assumed. |
| `MFOS-GAP-AUTH-0004` | MFA, dual-control, confirmation, and Guard token wire formats are not specified. | Token parsing behavior is `SPEC_GAP`. |
| `MFOS-GAP-AUTH-0005` | Concrete decision cache protocol and distributed invalidation transport are not specified. | Cache cannot be used for production allow without later design. |
| `MFOS-GAP-AUTH-0006` | Redaction policy language for audit and authorization evidence export is shared with audit design and not complete here. | Export must fail closed without explicit redaction policy. |
| `MFOS-GAP-AUTH-0007` | Full delegation administration workflow is not specified. | Delegation changes cannot be implemented from this spec alone. |
| `MFOS-GAP-AUTH-0008` | Policy lint executable rule language is not fixed. | Lint `SPEC_GAP` blocks activation. |
| `MFOS-GAP-AUTH-0009` | Partition backend authority mapping is profile-dependent and incomplete. | Partition destructive operations remain denied without profile-specific design. |
| `MFOS-GAP-AUTH-0010` | POSIX subsystem authorization mapping is intentionally deferred. | POSIX behavior cannot imply MFOS authorization success. |

## 35. No Implementation Authorization

This Phase 0.8 artifact is a design freeze. It may be used for review,
requirements alignment, schema review, formal-model planning, test cataloging,
and evidence planning only.

Before production code is authorized, a future task MUST provide:

1. Updated requirements registry entries for all `MFOS-REQ-AUTH-*` requirements
   used by code.
2. Reviewed machine-readable schemas and compatibility checks.
3. Passing design-validation and namespace checks.
4. State-machine review and invalid-transition evidence.
5. Positive, negative, and fuzz test plans tied to the test catalog.
6. Evidence registry entries and audit-obligation review.
7. Explicit closure or fail-closed handling for every `MFOS-GAP-AUTH-*` gap.
