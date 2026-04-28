---
spec_id: "MFOS-SPEC-10-OPERATOR-CONSOLE"
title: "MFOS Operator Console Specification v0.8 Semantics Freeze"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "phase-0-8-semantics-frozen"
owner: "MFOS Phase 0.8 Operator Console Lead"
last_reviewed: "2026-04-27"
source_refs:
  - "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001"
  - "EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001"
  - "EXTREF-IBM-ZOS-SECURITY-SERVER-0001"
  - "EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001"
  - "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001"
  - "EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001"
  - "EXTREF-IBM-ZOS-JES-INTRODUCTION-0001"
  - "EXTREF-IBM-ZOS-JES2-LIBRARY-0001"
  - "EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001"
  - "EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001"
requirement_refs: ["MFOS-REQ-OPER-*", "MFOS-REQ-AUTH-*", "MFOS-REQ-AUDIT-*", "MFOS-REQ-SYSINT-*"]
claim_refs: []
test_refs: ["tests/catalog/phase-0-8-operator-console-tests.yml"]
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Operator Console Specification v0.8 Semantics Freeze

Status: Phase 0.8 semantics frozen. This is a design and test contract, not
production code.

Owned component: `operatord`

Primary source matrix IDs: `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`,
`EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`,
`EXTREF-IBM-ZOS-SECURITY-SERVER-0001`,
`EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001`,
`EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`,
`EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001`,
`EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`,
`EXTREF-IBM-ZOS-JES2-LIBRARY-0001`,
`EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`,
`EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001`

Related artifacts:

- `schemas/mfos/operator-command.schema.yml`
- `formal/tla/operator-command/`
- `tests/catalog/phase-0-8-operator-console-tests.yml`
- `reports/phase-0-8-operator-console-lead.md`

## 1. Purpose

This specification defines the MFOS operator console as the first interactive
system interface after boot. The operator console is not a root shell. It is a
typed, command-governed, authority-checked, audit-generating system interface
for controlled operations.

MFOS is z/OS-inspired, not z/OS-compatible. The source-grounded overlap is the
enterprise operator model: commands have grammar, authority, target resolution,
confirmation, system-state visibility, and audit. MFOS diverges by defining a
new command set, new authorization model, new audit schema, and new x64-native
service routing.

## 2. Scope

In scope:

- Operator identity and session establishment.
- Operator command grammar and parse result.
- `OperatorCommand` schema contract.
- Command classification, authority classes, and risk classes.
- Command lifecycle with parse, target resolution, authorization, obligations,
  execution, audit, and display.
- Confirmation and dual-control semantics.
- Emergency mode and break-glass workflow hooks.
- Automation hooks that cannot bypass authorization or audit.
- Display model and redaction obligations.
- Failure modes, invalid transitions, positive tests, negative tests, fuzz
  target decisions, evidence requirements, and remaining spec gaps.

Out of scope:

- z/OS system command compatibility.
- JES2 command compatibility.
- ISPF panel compatibility.
- TSO command compatibility.
- General-purpose root shell.
- Arbitrary script execution with elevated privilege.
- Direct kernel debugging interface.
- Desktop UI or GUI console.
- Production implementation.

## 3. Non-Compatibility Statement

MFOS MUST NOT claim z/OS command, JES2 command, TSO, ISPF, MVS, or operator
console compatibility. MFOS MAY say "operator-console-inspired enterprise
command surface" when Source Matrix IDs and MFOS divergences are explicit.

Prohibited wording:

- "z/OS-compatible commands"
- "JES2-compatible commands"
- "MVS-compatible console"
- "TSO-compatible command processor"

Allowed wording:

- "Source-grounded operator command model"
- "z/OS-inspired operator governance"
- "RACF-inspired command authorization through securityd"
- "SMF-inspired command audit through auditd"

## 4. Source Reference Boundary

Only `EXTREF-*` Source Matrix IDs are used as external source references in
this specification. They are design background and traceability anchors, not
compatibility claims.

| Source ID | Operator console use |
| --- | --- |
| `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001` | System interfaces must not let unauthorized subjects bypass protection, security checks, or authorized state. |
| `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001` | Negative testing discipline for privileged boundary confusion, untrusted parameters, and unintended authority transfer. |
| `EXTREF-IBM-ZOS-SECURITY-SERVER-0001` | Central security manager, protected-resource, administrative command, and audit concepts. |
| `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001` | Principal, group, resource profile, access authority, and default-deny concepts. |
| `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001` | Operator activity, job, resource, accounting, and security activity evidence. |
| `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001` | Security audit fields for denied access, authority used, and reason-coded decisions. |
| `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001` | Job queue, SYSIN, SYSOUT, and spool concepts used by MFOS job/spool commands. |
| `EXTREF-IBM-ZOS-JES2-LIBRARY-0001` | Command-review background for job/spool operations without JES2 compatibility. |
| `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001` | Dataset catalog concepts used by MFOS dataset definition and display commands. |
| `EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001` | Service-class and workload-policy concepts used by MFOS workload policy display and policy activation commands. |

## 5. Component Responsibilities

`operatord` owns the interactive and automation-facing operator command surface.

Responsibilities:

- `OPER-R-001` First interactive interface after boot.
- `OPER-R-002` Command grammar and canonical parse.
- `OPER-R-003` Command target resolution.
- `OPER-R-004` Command authorization request construction.
- `OPER-R-005` Command audit event construction and audit ordering.
- `OPER-R-006` System state display.
- `OPER-R-007` Job control command routing.
- `OPER-R-008` Dataset definition command routing.
- `OPER-R-009` Emergency mode command workflow.
- `OPER-R-010` Confirmation and dual-control workflow.
- `OPER-R-011` Automation hook ingress.
- `OPER-R-012` Failure display and no-fake-success handling.

Non-responsibilities:

- Final authorization decision.
- Dataset IO implementation.
- Job scheduling.
- workload policy optimization.
- PXM lifecycle implementation.
- Guard root enforcement.
- Shell process management.
- Audit chain persistence.

## 6. Object Model

### 6.1 OperatorSession

```yaml
OperatorSession:
  session_id: uuid
  principal: PrincipalRef
  authenticated_at_utc: timestamp
  auth_strength: PASSWORD | CERTIFICATE | PASSKEY | MFA | HARDWARE_BACKED | BREAK_GLASS
  terminal_id: string
  console_id: string
  partition_id: uint64
  authority_snapshot:
    policy_version: uint64
    roles: [string]
    groups: [string]
  state: ACTIVE | LOCKED | REAUTH_REQUIRED | EMERGENCY | CLOSED
  correlation_id: uuid
```

Rules:

- Session identity MUST come from trusted authentication context.
- Caller-supplied principal text MUST NOT replace the trusted session subject.
- A locked, closed, expired, or reauthentication-required session MUST NOT
  execute commands.
- `BREAK_GLASS` auth strength records emergency authentication context; it is
  not a general superuser mode.

### 6.2 OperatorCommand

`OperatorCommand` is the canonical typed object emitted by the parser and used
for authorization, obligations, audit, execution routing, and display. The
machine-readable contract is `schemas/mfos/operator-command.schema.yml`.

```yaml
OperatorCommand:
  schema_version: 1
  command_id: uuid
  session_id: uuid?
  subject_ref: PrincipalRef
  caller_type: HUMAN | AUTOMATION | RECOVERY
  raw_text_hash: sha384
  raw_text_capture_policy: HASH_ONLY | ALLOW_FULL_CAPTURE
  parsed_name: string
  command_class: DISPLAY | DEFINE | ALTER | SUBMIT | CANCEL | PURGE | BROWSE | SET_POLICY | EMERGENCY | CONFIRMATION | DUAL_CONTROL | AUTOMATION | DIAGNOSTIC
  command_version: uint16
  command_args: map
  target_refs: [ObjectRef]
  target_resolution:
    resolution_status: RESOLVED | AMBIGUOUS | NOT_FOUND | STALE | SPEC_GAP
    target_digest: sha384?
    generation_bound: bool
  authority_class: AuthorityClassId
  risk_class: LOW | MODERATE | HIGH | CRITICAL
  destructive: bool
  requires_confirmation: bool
  requires_dual_control: bool
  requires_mfa: bool
  confirmation:
    status: NOT_REQUIRED | PENDING | SATISFIED | EXPIRED | CANCELED
    token_ref: string?
  dual_control:
    status: NOT_REQUIRED | PENDING | APPROVED | DENIED | EXPIRED | REVOKED
    approval_id: uuid?
  emergency_context:
    active: bool
    emergency_id: uuid?
    reason: string?
    expires_at_utc: timestamp?
  automation_context:
    hook_id: string?
    schedule_id: string?
    idempotency_key: string?
  policy_version: uint64
  decision_ref: string?
  audit:
    pre_effect_audit_ref: AuditRecordRef?
    result_audit_ref: AuditRecordRef?
  state: RECEIVED | PARSE_FAILED | PARSED | TARGET_RESOLVED | AUTHZ_REQUESTED | AUTHZ_DENIED | OBLIGATION_PENDING | CONFIRMATION_PENDING | DUAL_CONTROL_PENDING | AUDIT_PENDING | EXECUTING | COMPLETE | DENIED | FAILED_CLOSED | UNSUPPORTED | SPEC_GAP | CANCELED | EXPIRED
```

Rules:

- Raw command text MUST NOT be executed directly.
- `raw_text_hash` MUST be present for every received command.
- `command_args` MUST contain typed values, not an executable text fragment.
- `authority_class` MUST be resolved before `AUTHZ_REQUESTED`.
- `target_refs` MUST be canonical before any command can execute.
- Unknown fields MUST be rejected by canonical parsers.

### 6.3 CommandResult

```yaml
CommandResult:
  command_id: uuid
  status: OK | DENIED | FAILED_CLOSED | UNSUPPORTED | SPEC_GAP | CANCELED | EXPIRED
  reason_code: string
  output_ref: SpoolEntryRef?
  display_frame: ConsoleDisplayFrame
  audit_record_ref: AuditRecordRef
```

### 6.4 DualControlApproval

```yaml
DualControlApproval:
  approval_id: uuid
  command_id: uuid
  requester: PrincipalRef
  approver: PrincipalRef
  requested_at_utc: timestamp
  approved_at_utc: timestamp?
  expires_at_utc: timestamp
  approval_reason: string
  target_digest: sha384
  policy_version: uint64
  status: PENDING | APPROVED | DENIED | EXPIRED | REVOKED
```

Rules:

- `requester` and `approver` MUST be distinct principals.
- Approval MUST be bound to `command_id`, target digest, policy version, and
  authority class.
- Approval cannot grant authority. It only satisfies a securityd obligation.

## 7. Authority Classes

Authority classes are typed labels used in security decisions. They are not
roles, not POSIX users, and not a root-equivalent bit.

Initial authority classes:

| Authority class | Scope |
| --- | --- |
| `OPER_DISPLAY` | Display system, service, job, dataset, spool, and workload policy status subject to target authorization and redaction. |
| `OPER_DATASET_DEFINE` | Define cataloged datasets through the dataset/catalog workflow. |
| `OPER_SECURITY_ADMIN` | Define or alter principal registry objects through security policy workflow. |
| `OPER_JOB_SUBMIT` | Submit typed inline job text to `jobd`. |
| `OPER_JOB_CONTROL` | Cancel, hold, release, or restart jobs when those commands are specified. |
| `OPER_SPOOL_BROWSE` | Browse spool objects after target authorization and redaction. |
| `OPER_SPOOL_PURGE` | Purge spool objects after retention, confirmation, and authorization checks. |
| `OPER_WLM_ADMIN` | Activate workload policy. |
| `OPER_EMERGENCY` | Enter, exit, or operate under emergency context when policy allows. |
| `OPER_CONFIRM` | Confirm a pending command as the initiating operator. |
| `OPER_DUAL_CONTROL_APPROVE` | Approve or reject a pending command requested by a distinct principal. |
| `OPER_AUTOMATION_SUBMIT` | Submit commands through automation ingress; requested commands still require their own authority class. |
| `OPER_DIAGNOSTIC` | Run specified diagnostic display commands with no protected side effects. |

Rules:

- Every command MUST have exactly one primary authority class.
- A command MAY require additional target-resource authorization by the
  receiving service.
- `OPER_AUTOMATION_SUBMIT` is ingress authority only. It MUST NOT substitute
  for the requested command authority.
- Emergency mode MUST NOT synthesize authority classes. It supplies emergency
  context to `securityd`.

## 8. Command Grammar

Commands are MFOS commands, not z/OS-compatible commands. Keywords are ASCII
uppercase in canonical form. Parsers MAY accept lowercase input only by
canonicalizing keywords before object creation; identifiers remain case rules
defined by their token type.

### 8.1 Lexical Rules

```text
SP              = one or more ASCII spaces or tabs
NL              = LF or CRLF
UUID            = RFC-4122 textual UUID
UINT            = 1*20 decimal digit, range checked by target type
IDENT           = [A-Z][A-Z0-9_-]{0,63}
PRINCIPAL_ID    = [A-Z][A-Z0-9._@-]{0,127}
GROUP_ID        = [A-Z][A-Z0-9._@-]{0,127}
ROLE_ID         = [A-Z][A-Z0-9._@-]{0,127}
DSN             = DSN_SEG("." DSN_SEG)*
DSN_SEG         = [A-Z][A-Z0-9_-]{0,7}
JOB_ID          = "JOB-" UINT | UUID
JOB_NAME        = IDENT
SPOOL_ID        = "SPL-" UINT | UUID
POLICY_ID       = IDENT | UUID
SERVICE_ID      = IDENT
TEXT_ARG        = 1..1024 UTF-8 bytes, no control chars except tab, ")" escaped as "\)"
```

Global input limits:

- Single-line command input MUST be no more than 8192 bytes before parsing.
- `SUBMIT INLINE` payload MUST be no more than 262144 bytes.
- A single `SUBMIT INLINE` payload line MUST be no more than 4096 bytes.
- NUL bytes and non-normalized duplicate fields MUST be rejected.

### 8.2 Grammar

```text
Command =
    DisplayCommand
  | DefineUserCommand
  | DefineDatasetCommand
  | SubmitInlineCommand
  | CancelJobCommand
  | PurgeSpoolCommand
  | BrowseSpoolCommand
  | SetWorkloadPolicyCommand
  | EnterEmergencyCommand
  | ExitEmergencyCommand
  | ConfirmCommand
  | CancelPendingCommand
  | ApproveCommand
  | RejectCommand

DisplayCommand =
    "DISPLAY" SP "SYSTEM"
  | "DISPLAY" SP "SERVICES" [SP "SERVICE(" SERVICE_ID ")"]
  | "DISPLAY" SP "JOB" SP (JOB_ID | "NAME(" JOB_NAME ")")
  | "DISPLAY" SP "SPOOL" SP SPOOL_ID
  | "DISPLAY" SP "DATASET" SP DSN
  | "DISPLAY" SP "WORKLOAD" SP "POLICY"

DefineUserCommand =
  "DEFINE" SP "USER" SP PRINCIPAL_ID
  [SP "GROUP(" GROUP_ID ")"]
  [SP "ROLE(" ROLE_ID ")"]
  SP "REASON(" TEXT_ARG ")"

DefineDatasetCommand =
  "DEFINE" SP "DATASET" SP DSN
  SP "OWNER(" PRINCIPAL_ID ")"
  SP "TYPE(" ("SEQ" | "PDS_LITE" | "LOG" | "POLICY" | "MODULE") ")"
  [SP "RETENTION(" POLICY_ID ")"]
  SP "REASON(" TEXT_ARG ")"

SubmitInlineCommand =
  "SUBMIT" SP "INLINE"
  [SP "CLASS(" IDENT ")"]
  [SP "AS(" PRINCIPAL_ID ")"]
  SP "REASON(" TEXT_ARG ")" NL
  InlinePayload NL
  "ENDSUBMIT"

CancelJobCommand =
  "CANCEL" SP "JOB" SP JOB_ID SP "REASON(" TEXT_ARG ")"

PurgeSpoolCommand =
  "PURGE" SP "SPOOL" SP SPOOL_ID SP "REASON(" TEXT_ARG ")"

BrowseSpoolCommand =
  "BROWSE" SP "SPOOL" SP SPOOL_ID

SetWorkloadPolicyCommand =
  "SET" SP "WORKLOAD" SP "POLICY" SP POLICY_ID SP "REASON(" TEXT_ARG ")"

EnterEmergencyCommand =
  "ENTER" SP "EMERGENCY" SP "REASON(" TEXT_ARG ")" SP "EXPIRES(" Duration ")"

ExitEmergencyCommand =
  "EXIT" SP "EMERGENCY" SP "REASON(" TEXT_ARG ")"

ConfirmCommand =
  "CONFIRM" SP "COMMAND" SP UUID SP "REASON(" TEXT_ARG ")"

CancelPendingCommand =
  "CANCEL" SP "COMMAND" SP UUID SP "REASON(" TEXT_ARG ")"

ApproveCommand =
  "APPROVE" SP "COMMAND" SP UUID SP "REASON(" TEXT_ARG ")"

RejectCommand =
  "REJECT" SP "COMMAND" SP UUID SP "REASON(" TEXT_ARG ")"
```

`DSN` is the Phase 0.8 dataset/catalog DSN grammar from
`08-dataset-catalog.md`. `operatord` MUST reject broader dataset-name syntax
before authorization; it MUST NOT invent a console-only dataset namespace.

`Duration` is `5M`, `15M`, `30M`, or `1H`. Phase 0.8 emergency duration MUST
NOT exceed 60 minutes. Longer emergency requests are `MFOS_ERR_SPEC_GAP` and
fail closed without activating emergency state.

### 8.3 Parse Results

| Parse condition | Required result |
| --- | --- |
| Valid grammar and known command | Create `OperatorCommand` with `PARSED` state. |
| Valid command class but implementation unavailable | Create command and return `MFOS_ERR_UNSUPPORTED`; no side effect. |
| Behavior undefined by this spec | Create command when possible and return `MFOS_ERR_SPEC_GAP`; no side effect. |
| Malformed token, duplicate operand, overlong field, invalid escape, or invalid payload boundary | Return `MFOS_ERR_INVALID_PARAMETER`; no side effect. |
| Shell metacharacters outside typed text fields | Treat as invalid parameter, not as shell syntax. |

## 9. Command Matrix

`securityd` MAY impose stricter obligations than the minimums below. It MUST
NOT weaken these minimums.

| Parsed name | Class | Authority class | Protected operation | Risk | Minimum obligations |
| --- | --- | --- | --- | --- | --- |
| `DISPLAY_SYSTEM` | DISPLAY | `OPER_DISPLAY` | `OPERATOR_COMMAND/QUERY` | LOW | Audit before return. |
| `DISPLAY_SERVICES` | DISPLAY | `OPER_DISPLAY` | `OPERATOR_COMMAND/QUERY` | LOW | Audit before return. |
| `DISPLAY_JOB` | DISPLAY | `OPER_DISPLAY` | `JOB/QUERY` | LOW | Audit before return; target redaction. |
| `DISPLAY_SPOOL` | DISPLAY | `OPER_DISPLAY` | `SPOOL/QUERY` | LOW | Audit before return; target redaction. |
| `DISPLAY_DATASET` | DISPLAY | `OPER_DISPLAY` | `DATASET/QUERY` | LOW | Audit before return; target redaction. |
| `DISPLAY_WLM` | DISPLAY | `OPER_DISPLAY` | `WORKLOAD_POLICY/QUERY` | LOW | Audit before return. |
| `DEFINE_USER` | DEFINE | `OPER_SECURITY_ADMIN` | `SECURITY_POLICY/CREATE` | CRITICAL | MFA and dual control. |
| `DEFINE_DATASET` | DEFINE | `OPER_DATASET_DEFINE` | `CATALOG/CREATE` | MODERATE | Audit before effect; `POLICY` or `MODULE` dataset type also requires dual control. |
| `SUBMIT_INLINE` | SUBMIT | `OPER_JOB_SUBMIT` | `JOB/SUBMIT` | MODERATE | Audit before effect; `AS()` different from session principal requires MFA and dual control. |
| `CANCEL_JOB` | CANCEL | `OPER_JOB_CONTROL` | `JOB/CANCEL` | HIGH | Reason and audit before effect; running or system job requires confirmation. |
| `PURGE_SPOOL` | PURGE | `OPER_SPOOL_PURGE` | `SPOOL/PURGE` | HIGH | Confirmation, retention authorization, and audit before effect. |
| `BROWSE_SPOOL` | BROWSE | `OPER_SPOOL_BROWSE` | `SPOOL/BROWSE` | LOW | Audit before return; redaction. |
| `SET_WORKLOAD_POLICY` | SET_POLICY | `OPER_WLM_ADMIN` | `WORKLOAD_POLICY/ACTIVATE` | CRITICAL | MFA, dual control, and audit before effect. |
| `ENTER_EMERGENCY` | EMERGENCY | `OPER_EMERGENCY` | `SYSTEM/ADMINISTER` | CRITICAL | MFA, reason, expiry, break-glass authorization, and audit before enable. |
| `EXIT_EMERGENCY` | EMERGENCY | `OPER_EMERGENCY` | `SYSTEM/ADMINISTER` | HIGH | Reason and audit before exit is displayed complete. |
| `CONFIRM_COMMAND` | CONFIRMATION | `OPER_CONFIRM` | `OPERATOR_COMMAND/UPDATE` | MODERATE | Same requester, fresh token, audit. |
| `CANCEL_COMMAND` | CONFIRMATION | `OPER_CONFIRM` | `OPERATOR_COMMAND/UPDATE` | LOW | Same requester or authorized controller, audit. |
| `APPROVE_COMMAND` | DUAL_CONTROL | `OPER_DUAL_CONTROL_APPROVE` | `OPERATOR_COMMAND/UPDATE` | HIGH | Distinct approver, target digest match, audit. |
| `REJECT_COMMAND` | DUAL_CONTROL | `OPER_DUAL_CONTROL_APPROVE` | `OPERATOR_COMMAND/UPDATE` | HIGH | Distinct approver or policy-authorized reviewer, audit. |

## 10. Target Resolution

Target resolution converts parsed operands into canonical protected object refs.
It is a security boundary and MUST complete before authorization.

| Command family | Target refs |
| --- | --- |
| `DISPLAY SYSTEM` | `SYSTEM` object mapped to authorization class `MFOS_RESOURCE_SYSTEM` for local partition and activation profile. |
| `DISPLAY SERVICES` | Service registry object and optional `SERVICE` object mapped to `MFOS_RESOURCE_SERVICE`. |
| `DISPLAY JOB`, `CANCEL JOB` | Canonical `JOB` object with job ID, owner, state, partition, and generation. |
| `DISPLAY SPOOL`, `BROWSE SPOOL`, `PURGE SPOOL` | Canonical `SPOOL` object with owner, job ID, retention policy, partition, and generation. |
| `DISPLAY DATASET` | Canonical `DATASET` and `CATALOG` objects with catalog generation. |
| `DEFINE DATASET` | `CATALOG` namespace object plus intended `DATASET` object. Existing object is a conflict unless policy defines idempotent create. |
| `DEFINE USER` | `SECURITY_POLICY` principal registry object plus intended principal object. Existing object is a conflict unless policy defines idempotent create. |
| `SUBMIT INLINE` | `JOB` submit queue object plus optional effective principal target. |
| `SET WORKLOAD POLICY` | `WORKLOAD_POLICY` object with policy ID and generation. |
| `ENTER EMERGENCY`, `EXIT EMERGENCY` | `SYSTEM` emergency-state object mapped to `MFOS_RESOURCE_SYSTEM`; High-Assurance profiles also include the Guard emergency root ref when required. |
| `CONFIRM`, `CANCEL`, `APPROVE`, `REJECT COMMAND` | Pending `OPERATOR_COMMAND` object by `command_id`. |

Rules:

- Ambiguous targets MUST fail closed with `MFOS_ERR_INVALID_PARAMETER` or
  `MFOS_ERR_SPEC_GAP` according to whether syntax or semantics caused the
  ambiguity.
- Target refs MUST include generation for generation-aware objects.
- If a target changes after resolution and before effect, operatord MUST
  re-resolve and reauthorize or fail closed with `MFOS_ERR_STALE_HANDLE`.
- Display commands MUST still resolve targets and authorize redaction before
  output.
- Target resolution MUST NOT follow shell paths, environment variables, or
  process-current-directory state.

## 11. Authorization

`operatord` is an enforcement point. `securityd` is the policy decision point.

Command authorization request:

```yaml
DecisionRequest:
  subject: trusted OperatorSession or automation principal subject
  object:
    resource_type: OPERATOR_COMMAND
    object_id: parsed_name
    generation: command_version
  operation: command protected operation
  context:
    operator_context:
      command_id: uuid
      console_id: string
      automation: bool
      confirmation_token: string?
      dual_control_token: string?
    emergency_context:
      break_glass_active: bool
      reason: string?
      expiry: timestamp?
    target_digest: sha384
    policy_version_requested: uint64?
  requested_obligations:
    - AUDIT
    - OPERATOR_CONFIRMATION?
    - DUAL_CONTROL?
    - MFA?
    - BREAK_GLASS?
    - GUARD_APPROVAL?
```

Rules:

- A protected command MUST NOT execute before `securityd` returns
  `MFOS_AUTH_ALLOW` or `MFOS_AUTH_ALLOW_WITH_OBLIGATIONS` for the current
  command, subject, target digest, operation, and policy version.
- `MFOS_AUTH_REQUIRE_MFA`, `MFOS_AUTH_REQUIRE_DUAL_CONTROL`,
  `MFOS_AUTH_REQUIRE_BREAK_GLASS`, `MFOS_AUTH_REQUIRE_GUARD_APPROVAL`, and
  `MFOS_AUTH_REQUIRE_OPERATOR_CONFIRMATION` are pending states, not allow
  decisions.
- Audit records may project these decisions into unprefixed audit enum values
  such as `REQUIRE_BREAK_GLASS`; that projection is not the `securityd`
  decision enum.
- Denied, unsupported, and spec-gap decisions MUST NOT have target side effects.
- Receiving services such as `jobd`, `spoold`, `catalogd`, `datasetd`, `workpolicyd`,
  `auditd`, PXM, or Guard MUST still enforce their own target-resource
  authorization. Operator command authorization is not a substitute for service
  authorization.
- Policy version mismatch MUST invalidate pending confirmation and approval
  tokens.

## 12. Command Lifecycle

### 12.1 Normal Lifecycle

```text
RECEIVE_INPUT
  -> HASH_RAW_TEXT
  -> PARSE_TYPED_COMMAND
  -> IDENTIFY_COMMAND
  -> RESOLVE_TARGET
  -> CLASSIFY_RISK_AND_AUTHORITY
  -> REQUEST_AUTHORIZATION
  -> SATISFY_MFA_IF_REQUIRED
  -> SATISFY_CONFIRMATION_IF_REQUIRED
  -> SATISFY_DUAL_CONTROL_IF_REQUIRED
  -> WRITE_PRE_EFFECT_AUDIT_IF_REQUIRED
  -> EXECUTE_TYPED_SERVICE_CALL
  -> WRITE_RESULT_AUDIT
  -> DISPLAY_RESULT
```

Terminal states:

```text
COMPLETE
DENIED
FAILED_CLOSED
UNSUPPORTED
SPEC_GAP
CANCELED
EXPIRED
```

Ordering rules:

- DENY MUST be audited before the denial is displayed when an audit obligation
  is present.
- A command with required pre-effect audit MUST NOT call the target service
  until auditd durably accepts the audit request.
- A destructive command MUST NOT execute before required confirmation and
  dual-control approval are satisfied.
- Automation uses the same lifecycle as human commands.
- Emergency mode is state and context with extra audit obligations, not a
  bypass.

### 12.2 Invalid Transitions

| Invalid transition | Required result |
| --- | --- |
| `RECEIVED` to `EXECUTING` | `MFOS_ERR_SPEC_GAP`; no side effect. |
| `PARSE_FAILED` to any non-terminal state | `MFOS_ERR_INVALID_PARAMETER`; no side effect. |
| `PARSED` to `EXECUTING` before target resolution | `MFOS_ERR_SPEC_GAP`; no side effect. |
| `TARGET_RESOLVED` to `EXECUTING` before allow decision | `MFOS_ERR_INVALID_STATE`; audit when possible. |
| `AUTHZ_DENIED` to `EXECUTING` | `MFOS_ERR_POLICY_DENIED`; audit violation. |
| `CONFIRMATION_PENDING` to `EXECUTING` without valid confirmation token | `MFOS_ERR_CONFIRMATION_REQUIRED`; no side effect. |
| `DUAL_CONTROL_PENDING` to `EXECUTING` without valid distinct approver | `MFOS_ERR_DUAL_CONTROL_REQUIRED`; no side effect. |
| `AUDIT_PENDING` to `EXECUTING` when pre-effect audit failed | `MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE`; no side effect. |
| Any terminal state to `EXECUTING` | `MFOS_ERR_INVALID_STATE`; no side effect. |
| Pending command to `EXECUTING` after policy version change | `MFOS_ERR_POLICY_VERSION_MISMATCH`; reauthorize or cancel. |
| Pending command to `EXECUTING` after target digest change | `MFOS_ERR_STALE_HANDLE`; re-resolve and reauthorize or cancel. |

## 13. Confirmation

Confirmation is a human acknowledgement for a pending command. It is not
authorization and does not grant authority.

Rules:

- Confirmation token MUST be bound to command ID, requester principal, session,
  target digest, risk class, policy version, and expiry.
- Confirmation expiry MUST be profile-defined and MUST NOT exceed 10 minutes.
- Confirmation MUST be invalidated by target digest change, policy version
  change, requester session close, emergency expiry, or command cancellation.
- `CONFIRM COMMAND` MUST be audited.
- `CONFIRM COMMAND` MUST NOT satisfy dual control.
- Automation MUST NOT satisfy human confirmation for production profiles.

## 14. Dual Control

Dual control requires a distinct authorized principal to approve a pending
command.

Rules:

- The requester and approver MUST be distinct principals.
- The approver MUST be authorized for `OPER_DUAL_CONTROL_APPROVE` and any
  `approver_authority_class` returned by `securityd`.
- The approval token MUST be bound to command ID, requester, approver, authority
  class, target digest, risk class, policy version, and expiry.
- Approval expiry MUST be profile-defined and MUST NOT exceed 30 minutes.
- Same-actor approval MUST fail closed even when the actor has multiple roles.
- Approval of a modified command is invalid. Modified command text creates a new
  `command_id`.
- `APPROVE COMMAND` and `REJECT COMMAND` MUST be audited.

## 15. Emergency Mode

Emergency mode exists for recovery when normal policy prevents necessary repair.
It does not disable audit or authorization.

Rules:

- Entry MUST include authenticated operator identity, reason, expiry, active
  policy version, and target emergency scope.
- Entry MUST require `securityd` decision `MFOS_AUTH_REQUIRE_BREAK_GLASS` or
  `MFOS_AUTH_ALLOW_WITH_OBLIGATIONS` according to policy.
- Entry MUST require MFA unless the active recovery policy explicitly defines a
  stronger hardware-backed recovery factor.
- High-Assurance profiles MAY require Guard approval before emergency mode
  becomes active.
- Emergency mode MUST expire, and Phase 0.8 expiry MUST NOT exceed 60 minutes.
  Longer durations are `MFOS_ERR_SPEC_GAP` and fail closed.
- All emergency commands MUST include emergency context in authorization and
  audit records.
- Emergency mode MUST NOT permit audit disablement.
- Emergency mode MUST NOT bypass `securityd`.
- Emergency mode MUST NOT grant AMF load, Guard root transition, policy update,
  partition control, or update activation authority unless a command profile
  explicitly permits that operation and securityd returns the required
  obligations.
- On expiry, pending emergency commands MUST transition to `EXPIRED` or require
  full reauthorization under a new emergency context.

Emergency lifecycle:

```text
ENTER_REQUEST
  -> AUTHENTICATE_OPERATOR
  -> AUTHORIZE_BREAK_GLASS
  -> RECORD_REASON
  -> SET_EXPIRY
  -> GUARD_APPROVAL_IF_REQUIRED
  -> AUDIT_BEFORE_ENABLE
  -> EMERGENCY_ACTIVE
  -> EXIT_REQUEST_OR_EXPIRY
  -> AUDIT_EXIT
  -> NORMAL_ACTIVE
```

## 16. Automation Hooks

Automation is a caller type, not a privilege.

Automation ingress operations:

```text
SUBMIT_OPERATOR_COMMAND
GET_COMMAND_STATUS
CANCEL_PENDING_COMMAND
SUBSCRIBE_COMMAND_EVENTS
```

Rules:

- Automation identities MUST be principals.
- Automation ingress requires `OPER_AUTOMATION_SUBMIT`; requested commands
  still require the command-specific authority class.
- Automation commands MUST pass through the same parser, target resolver,
  securityd authorization, obligation, audit, and display-result path.
- Automation MUST NOT execute raw internal service calls that bypass operator
  command policy.
- Automation MUST NOT self-confirm or approve commands it requested.
- Automation rate limiting is mandatory. If no profile-specific rate limit is
  configured, automation ingress MUST fail closed.
- Automation replay protection MUST bind idempotency key, command hash, subject,
  and policy version.
- Automation command results MUST be available as typed `CommandResult`
  objects, not as shell exit status.

## 17. Command Audit

Required audit events:

| Event | Required fields |
| --- | --- |
| `OPER_SESSION_START` | principal, terminal_id, console_id, auth_strength, partition_id |
| `OPER_SESSION_END` | principal, session_id, reason |
| `OPER_COMMAND_PARSE` | session_id or automation principal, command_id, parsed_name, raw_text_hash |
| `OPER_COMMAND_TARGET_RESOLVE` | command_id, target_refs, target_digest, resolution_status |
| `OPER_COMMAND_DENY` | command_id, subject, target_refs, reason_code, policy_version |
| `OPER_COMMAND_ALLOW` | command_id, subject, authority_class, policy_version, obligations |
| `OPER_CONFIRMATION` | command_id, confirmer, confirmation_status, reason |
| `OPER_DUAL_CONTROL_REQUEST` | command_id, requester, approval_id, target_digest |
| `OPER_DUAL_CONTROL_DECISION` | approval_id, approver, decision, reason |
| `OPER_COMMAND_EXECUTE` | command_id, component, operation, authority_class |
| `OPER_COMMAND_RESULT` | command_id, result, reason_code, result_digest |
| `OPER_EMERGENCY_ENTER` | principal, reason, expiry, policy_version, emergency_id |
| `OPER_EMERGENCY_EXIT` | principal, reason, duration, emergency_id |
| `OPER_AUTOMATION_COMMAND` | automation_principal, hook_id, command_id, policy_version, idempotency_key |

Rules:

- Raw command text MAY contain secrets and MUST be stored only as a hash unless
  command-specific policy permits full capture.
- Display output is not audit evidence unless auditd records it as an audit
  event.
- Denial audit MUST precede denial display when an audit obligation is present.
- Result audit MUST include enough typed status to distinguish success, denied,
  unsupported, spec gap, canceled, expired, and failed closed.
- Audit failure for a required pre-effect audit MUST fail closed.

## 18. Display Model

The console displays typed results. It does not display a shell prompt and does
not interpret display text as a command stream.

```yaml
ConsoleDisplayFrame:
  frame_id: uuid
  command_id: uuid
  timestamp_utc: timestamp
  severity: INFO | WARN | ERROR | SECURITY
  status: OK | DENIED | FAILED_CLOSED | UNSUPPORTED | SPEC_GAP | CANCELED | EXPIRED
  reason_code: string
  summary: string
  rows: [map]
  redaction_policy: string
  next_action: NONE | CONFIRM | WAIT_FOR_APPROVAL | REAUTHENTICATE | RETRY_AFTER_REAUTHORIZE | OPEN_SPEC_GAP
  audit_record_ref: AuditRecordRef?
```

Rules:

- Display summaries MUST be generated from typed command result fields.
- Display frames MUST NOT contain hidden executable commands.
- Sensitive target fields MUST be redacted according to securityd/auditd
  obligations before display.
- Pending confirmation and dual-control display MUST include command ID, target
  summary, risk class, expiry, and reason, but MUST NOT expose secrets from raw
  command text.
- `SPEC_GAP` display MUST clearly say the behavior is unspecified and had no
  side effect.
- `UNSUPPORTED` display MUST clearly say the behavior is specified but not
  implemented and had no side effect.

## 19. Failure Modes

| Error | Meaning | Required behavior |
| --- | --- | --- |
| `MFOS_ERR_UNAUTHENTICATED` | No valid operator session or automation principal. | Reject command; audit session failure when possible. |
| `MFOS_ERR_INVALID_PARAMETER` | Parse or target resolution failed. | No execution; display parameter failure. |
| `MFOS_ERR_UNAUTHORIZED` | Legacy umbrella wording only; not the primary policy-denial result for Phase 1 artifacts. | Treat as deprecated alias or error-model cleanup target; do not execute. |
| `MFOS_ERR_POLICY_DENIED` | `securityd` denies command authority or target action for a valid subject. | Do not execute; audit denial. |
| `MFOS_ERR_POLICY_VERSION_MISMATCH` | Pending token or command used stale policy. | Reauthorize or cancel; no side effect. |
| `MFOS_ERR_CONFIRMATION_REQUIRED` | Human confirmation obligation unsatisfied. | Hold pending command or deny on expiry. |
| `MFOS_ERR_DUAL_CONTROL_REQUIRED` | Distinct approver obligation unsatisfied. | Hold pending command or deny on expiry. |
| `MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE` | Required audit cannot be written. | Fail closed except explicitly specified recovery display paths. |
| `MFOS_ERR_UNSUPPORTED` | Command exists in class but is not implemented. | Display unsupported; no side effect. |
| `MFOS_ERR_SPEC_GAP` | Command behavior is unspecified. | Display spec gap; no side effect. |
| `MFOS_ERR_STALE_HANDLE` | Target changed between resolve and execute. | Re-resolve and reauthorize or fail closed. |
| `MFOS_ERR_GUARD_REQUIRED` | HA Guard approval needed. | Hold command until approved or deny. |
| `MFOS_ERR_INVALID_STATE` | Invalid lifecycle transition. | Fail closed; audit violation when possible. |
| `MFOS_ERR_RATE_LIMITED` | Automation or session rate limit exceeded. | Reject or delay without side effect; audit automation abuse when required. |
| `MFOS_ERR_EXPIRED` | Pending command, confirmation, approval, or emergency context expired. | Mark expired; no side effect. |

## 20. Security Invariants

```text
INV-OPER-001:
  No operator command executes without command_id, subject, target_refs,
  resolved authority class, authorization decision, and required audit
  obligation.

INV-OPER-002:
  Raw command text cannot cross from operatord into a privileged service
  without typed parsing and target resolution.

INV-OPER-003:
  Destructive commands cannot reach EXECUTING unless confirmation and
  dual-control obligations required by securityd are satisfied.

INV-OPER-004:
  Automation cannot receive more authority than the automation principal has
  under the current policy version.

INV-OPER-005:
  Emergency mode cannot disable auditd or bypass securityd.

INV-OPER-006:
  Same-actor dual control cannot execute the requested command.

INV-OPER-007:
  Unsupported, spec-gap, denied, expired, canceled, and failed-closed commands
  produce no target side effects.

INV-OPER-008:
  No root shell command text is a successful operator command path.
```

## 21. Positive Tests

| Test ID | Description |
| --- | --- |
| `TEST-MFOS-OPER-BOOT-0001` | Boot reaches operator console instead of root shell. |
| `TEST-MFOS-OPER-PARSE-0001` | Valid command grammar creates typed `OperatorCommand`. |
| `TEST-MFOS-OPER-DISPLAY-0001` | Authenticated operator runs `DISPLAY SYSTEM`; command is parsed, authorized, audited, and displayed. |
| `TEST-MFOS-OPER-SCHEMA-0001` | Valid `OperatorCommand` instances conform to `schemas/mfos/operator-command.schema.yml`. |
| `TEST-MFOS-OPER-DATASET-0001` | Operator defines a dataset through typed catalog/dataset workflow and audit records result. |
| `TEST-MFOS-OPER-SUBMIT-0001` | Operator submits inline job; `jobd` receives typed submit request and audit correlation ID. |
| `TEST-MFOS-OPER-SPOOL-0001` | Operator browses authorized spool output after redaction. |
| `TEST-MFOS-OPER-CANCEL-0001` | Operator cancels a queued job with reason and audit record. |
| `TEST-MFOS-OPER-PURGE-0001` | Destructive purge succeeds only after confirmation and retention authorization. |
| `TEST-MFOS-OPER-DUAL-0001` | Critical command executes after distinct authorized approver approval. |
| `TEST-MFOS-OPER-EMERGENCY-0001` | Emergency mode enter and exit produce required audit records and expiry. |
| `TEST-MFOS-OPER-AUTOMATION-0001` | Automation principal runs permitted `DISPLAY JOB` through normal lifecycle. |
| `TEST-MFOS-OPER-DISPLAY-0002` | Display frame includes status, reason code, redaction policy, and audit ref. |

## 22. Negative Tests

| Test ID | Description |
| --- | --- |
| `NEG-MFOS-OPER-AUTH-0001` | Unauthenticated input attempts `DEFINE USER`; command is rejected. |
| `NEG-MFOS-OPER-PARSE-0001` | Unknown command text is not executed and returns unsupported or spec gap. |
| `NEG-MFOS-OPER-PARSE-0002` | Shell metacharacter input is parsed as invalid parameter, never executed. |
| `NEG-MFOS-OPER-AUTH-0002` | Unauthorized operator attempts `DEFINE USER`; no user is created and denial is audited first. |
| `NEG-MFOS-OPER-CONFIRM-0001` | `PURGE SPOOL` without required confirmation does not execute. |
| `NEG-MFOS-OPER-DUAL-0001` | Dual-control command approved by same principal as requester is denied. |
| `NEG-MFOS-OPER-DUAL-0002` | Dual-control approval with stale target digest is denied. |
| `NEG-MFOS-OPER-EMERGENCY-0001` | Emergency command without reason or expiry is denied. |
| `NEG-MFOS-OPER-EMERGENCY-0002` | Emergency mode attempts to disable auditd; denied. |
| `NEG-MFOS-OPER-AUTOMATION-0001` | Automation calls internal dataset define path directly; denied as bypass attempt. |
| `NEG-MFOS-OPER-STALE-0001` | Command target changes after resolution; command fails closed or reauthorizes. |
| `NEG-MFOS-OPER-AUDIT-0001` | Auditd unavailable for destructive command; command fails closed. |
| `NEG-MFOS-OPER-STATE-0001` | Forced lifecycle transition from `PARSED` to `EXECUTING` fails closed. |
| `NEG-MFOS-OPER-POLICY-0001` | Pending approval after policy version change cannot execute. |
| `NEG-MFOS-OPER-DISPLAY-0001` | Display output with unredacted protected field is rejected. |

## 23. Fuzz Target Decisions

| Fuzz target | Scope | Required oracle |
| --- | --- | --- |
| `FUZZ-MFOS-OPER-PARSER-0001` | Malformed commands, overlong tokens, invalid escapes, shell metacharacters, duplicate operands. | Parser does not panic; raw text never executes; invalid input has no side effect. |
| `FUZZ-MFOS-OPER-INLINE-0001` | Nested `SUBMIT INLINE`, missing `ENDSUBMIT`, payload size boundaries, invalid line endings. | Payload remains data; malformed payload never reaches `jobd`. |
| `FUZZ-MFOS-OPER-TARGET-0001` | Invalid DSN, invalid job IDs, stale spool IDs, ambiguous target names. | Target resolution fails closed or reauthorizes; no stale side effect. |
| `FUZZ-MFOS-OPER-CONFIRM-0001` | Repeated confirmations, expired tokens, wrong requester, target digest changes. | Confirmation cannot create authority or execute modified command. |
| `FUZZ-MFOS-OPER-DUAL-0001` | Same actor, expired approval, wrong authority class, replayed approval. | Dual-control invariant holds. |
| `FUZZ-MFOS-OPER-EMERGENCY-0001` | Missing reason, invalid expiry, concurrent enter/exit, expired emergency context. | Emergency never disables securityd or auditd and expires closed. |
| `FUZZ-MFOS-OPER-AUTOMATION-0001` | Burst commands, malformed identity context, replayed idempotency keys. | Automation is rate-limited, replay-protected, and audited. |
| `FUZZ-MFOS-OPER-DISPLAY-0001` | Oversized rows, secret-looking fields, invalid severity/status, hidden command text. | Display frame remains typed, bounded, and redacted. |

Fuzz target requirements:

- Parser must not panic.
- Raw text must never execute directly.
- Malformed command must not call privileged service APIs.
- No denied command may have side effects.
- Corpus seeds MUST include positive grammar examples and negative bypass
  examples from the test catalog.

## 24. Evidence Requirements

Phase 0.8 evidence must include:

- Source traceability to the `EXTREF-*` IDs listed in this specification.
- Operator command grammar review record.
- Schema validation report for `schemas/mfos/operator-command.schema.yml`.
- Formal model or state-machine review for `formal/tla/operator-command/`.
- Positive parser, lifecycle, display, emergency, and automation test results.
- Negative authorization, confirmation, dual-control, emergency, automation
  bypass, audit-unavailable, stale-target, and invalid-transition test results.
- Fuzz campaign plan and initial corpus manifest for all fuzz targets in this
  specification.
- Audit ordering evidence showing denial audit before denial display.
- No-root-shell boot evidence.
- Spec-gap ledger showing unresolved items have no implementation success path.

Evidence artifacts MUST identify requirement IDs, source refs, test IDs,
profile under test, command IDs, policy version, and audit record refs.

## 25. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| `MFOS-REQ-OPER-0001` | First interactive UI after boot MUST be operator console, not root shell. | Boot test |
| `MFOS-REQ-OPER-0002` | Operator command grammar MUST be specified and parser-tested. | Parser tests and fuzzing |
| `MFOS-REQ-OPER-0003` | Operator commands MUST have authority classes. | Schema review |
| `MFOS-REQ-OPER-0004` | Destructive commands MUST be able to require confirmation or dual-control. | Operator drill |
| `MFOS-REQ-OPER-0005` | Operator commands MUST generate audit records. | Audit tests |
| `MFOS-REQ-OPER-0006` | Automation hooks MUST NOT bypass operator authority or audit. | Negative tests |
| `MFOS-REQ-OPER-0007` | Command DENY MUST be audited before display. | Ordering tests |
| `MFOS-REQ-OPER-0008` | Emergency mode MUST require reason, identity, expiry, and audit. | Emergency drill |
| `MFOS-REQ-OPER-0009` | Raw command text MUST NOT be directly executed. | Code review and tests |
| `MFOS-REQ-OPER-0010` | Unsupported commands MUST fail closed, not silently succeed. | No-fake-success CI |

## 26. Spec Gaps

The following gaps remain. They are implementation-blocking for the affected
feature unless resolved by a later spec update:

- Concrete authentication backend and terminal secure-attention model.
- Final policy bundle encoding for command profiles and rate-limit values.
- Full display message catalog and localization rules.
- Guard emergency approval API details for High-Assurance profiles.
- Concrete audit payload schema version for every operator audit event.
- Recovery-mode subset when auditd or securityd is degraded.
- Formal model checking harness values and CI integration.
- Exact production evidence archive paths for Phase 0.8 test outputs.

The following items are no longer open gaps for Phase 0.8:

- Operator console is not a root shell.
- Initial command grammar.
- `OperatorCommand` schema ownership and field set.
- Initial authority class taxonomy.
- Command lifecycle and invalid transitions.
- Target resolution order.
- Authorization and obligation ordering.
- Confirmation and dual-control semantics.
- Emergency mode expiry and no-bypass rules.
- Automation hook bypass prohibition.
- Audit event set and display model.
- Positive, negative, and fuzz target decisions.

## 27. Inactive Future Implementation Prompt Template

Phase status: inactive future template. This section does not authorize production implementation, hosted daemon implementation, or portable semantic-core implementation.

```text
Future authorized implementation agents would implement MFOS operatord behavior.

Use these spec IDs:
- MFOS-REQ-OPER-0001 through MFOS-REQ-OPER-0010

Source Matrix IDs:
- EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
- EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001
- EXTREF-IBM-ZOS-SECURITY-SERVER-0001
- EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001
- EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001
- EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001
- EXTREF-IBM-ZOS-JES-INTRODUCTION-0001
- EXTREF-IBM-ZOS-JES2-LIBRARY-0001
- EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001
- EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001

Rules:
- Do not claim z/OS, JES2, TSO, ISPF, MVS, or command compatibility.
- Operator console is not a root shell.
- Raw command text must be parsed into typed command objects.
- Every command must pass securityd authorization when protected.
- DENY must be audited before displaying denial.
- Destructive commands must satisfy confirmation or dual-control obligations.
- Automation must not bypass parser, authorization, or audit.
- Unsupported behavior returns MFOS_ERR_UNSUPPORTED.
- Unspecified behavior returns MFOS_ERR_SPEC_GAP.
- No fake success, empty stubs, or silent fallback.

Deliver:
1. Implemented requirement IDs
2. Source Matrix IDs
3. Assumptions
4. Spec gaps
5. Unsupported features
6. Security invariants
7. Audit obligations
8. Failure modes
9. Tests added
10. Negative tests added
11. Fuzz targets added
12. Unsafe code justification
13. Review checklist
14. Evidence artifacts
```

## Phase 0.8 Core Semantics Freeze

This section freezes the Operator Console semantics for Phase 0.8. It is a design-level freeze only and does not authorize production implementation, hosted daemon implementation, Portable Semantic Core implementation, or executable specs.

### Frozen Requirement Set

- `MFOS-REQ-OPER-0101`
- `MFOS-REQ-OPER-0102`
- `MFOS-REQ-OPER-0103`
- `MFOS-REQ-OPER-0104`

### Machine-Readable Artifacts

- Pack contract: `docs/design/packs/PACK-09-*/pack.yml`
- State machine: `formal/tla/operator-command/state-machine.yml`
- Test catalog: `tests/catalog/phase-0-8-*`
- Requirement mirror: `requirements/by-domain/`
- Evidence traceability: `evidence/traceability/phase-0-8-*`

### Freeze Rules

- Undefined behavior returns `MFOS_ERR_SPEC_GAP`.
- Specified but unimplemented behavior returns `MFOS_ERR_UNSUPPORTED`.
- Deny paths with audit obligations must define deny-before-return behavior.
- Security-sensitive behavior requires a negative test catalog entry.
- No fake success, empty stub, or silent fallback is allowed.
