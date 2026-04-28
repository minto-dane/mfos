---
spec_id: "MFOS-SPEC-09-JOB-SPOOL"
title: "MFOS Job and Spool Specification v0.8"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS Phase 0.8 Job/Spool Lead"
last_reviewed: "2026-04-27"
source_refs: ["EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001", "EXTREF-IBM-ZOS-JES-INTRODUCTION-0001", "EXTREF-IBM-ZOS-JES-JOB-FLOW-0001", "EXTREF-IBM-ZOS-JES2-LIBRARY-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001"]
requirement_refs: ["MFOS-REQ-JOB-*", "MFOS-REQ-SPOOL-*"]
claim_refs: []
test_refs: ["tests/catalog/phase-0-8-job-spool-tests.yml"]
evidence_refs: ["reports/phase-0-8-job-spool-lead.md"]
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Job and Spool Specification v0.8

Status: Phase 0.8 semantic freeze draft. Production implementation is not authorized by this file.

Owned components: `jobd`, `spoold`

Primary schemas:

- `schemas/mfos/job.schema.yml`
- `schemas/mfos/job-step.schema.yml`
- `schemas/mfos/dd.schema.yml`
- `schemas/mfos/spool-entry.schema.yml`

Primary formal and test artifacts:

- `formal/tla/job-lifecycle/JobLifecycle.tla`
- `formal/tla/spool-access/SpoolAccess.tla`
- `tests/catalog/phase-0-8-job-spool-tests.yml`

## 1. Purpose

This specification freezes the Phase 0.8 MFOS job and spool semantics for design review. It defines the MFOS job-control stream grammar, Job, JobStep, DD, ProgramIdentity, job identity, effective principal establishment, DD resolution, job lifecycle, step execution, return-code handling, SpoolEntry lifecycle, input/output stream behavior, browse/purge/export authorization, retention, audit obligations, failure modes, invalid transitions, tests, fuzz targets, evidence expectations, and remaining spec gaps.

MFOS is z/OS-inspired, not z/OS-compatible. The source-grounded overlap is the enterprise batch model of submitting work, converting it, queueing it, selecting it for execution, capturing output, controlling protected spool access, and purging retained output through governed policy. MFOS defines a native subset and MUST NOT claim JES, JES2, JCL, RACF, DFSMS, SMF, or z/OS compatibility.

## 2. Source Matrix References

Only EXTREF Source Matrix IDs are used for this Phase 0.8 freeze.

| Source ID | Phase 0.8 use |
| --- | --- |
| `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001` | Job submission, queues, initiators, INPUT_STREAM, OUTPUT_STREAM, and spool as design-background concepts. |
| `EXTREF-IBM-ZOS-JES-JOB-FLOW-0001` | Input, conversion, processing, output, and purge as lifecycle-background concepts. |
| `EXTREF-IBM-ZOS-JES2-LIBRARY-0001` | Future operator and job/spool detail review, without command compatibility claims. |
| `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001` | Dataset names are resolved through a catalog service before dataset access. |
| `EXTREF-IBM-ZOS-SECURITY-SERVER-0001` | Protected resources are mediated by a central security service. |
| `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001` | Principal, protected resource, profile, access-list, and deny concepts. |
| `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001` | Job accounting and system activity evidence concepts. |
| `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001` | Security-deny audit fields, authority-used fields, and audit-reason concepts. |

## 3. Non-Compatibility Boundary

MFOS MUST NOT describe this subsystem as:

- JES-compatible
- JES2-compatible
- external job-control-language compatible
- z/OS-compatible batch
- RACF-compatible security
- SMF-compatible accounting

MFOS MAY use these phrases when paired with this non-compatibility boundary and Source Matrix IDs:

- JES-inspired job lifecycle
- MFOS-native job-control subset
- RACF-inspired protected-resource authorization
- SMF-inspired job audit evidence

This specification must not reproduce external command grammars, macro interfaces, binary data formats, message catalogs, data areas, or compatibility behavior.

## 4. Scope

In scope:

- Job submission request semantics.
- MFOS job-control stream grammar and parse diagnostics.
- Job identity and immutable job identifiers.
- Effective principal establishment.
- Program identity and program execution authorization.
- DD resolution through `catalogd`, `datasetd`, `spoold`, `securityd`, and `auditd`.
- Sequential step execution for the initial subset.
- Return-code and failure-state aggregation.
- INPUT_STREAM and OUTPUT_STREAM storage as protected spool entries.
- Spool browse, purge, export, retention, quota hooks, and stale-reference handling.
- State machines, invalid transitions, tests, fuzz targets, evidence obligations, and spec gaps.

Out of scope:

- Production implementation.
- External job-control-language grammar compatibility.
- Procedure libraries, symbolic parameters, conditional execution, INCLUDE, continuation cards, or concatenation.
- JES2 commands or initialization compatibility.
- Print or punch device emulation.
- z/OS abend-code compatibility.
- POSIX shell-first execution semantics.
- Direct dataset, catalog, program, or spool access without `securityd` authorization.

## 5. Normative Terms

`UNSUPPORTED` means the behavior is defined as a possible feature, but this Phase 0.8 profile does not implement or authorize it. The required result is `MFOS_ERR_UNSUPPORTED`, no protected side effect, and audit where the request is security-sensitive.

`SPEC_GAP` means the behavior is undefined by specification. The required result is `MFOS_ERR_SPEC_GAP`, no protected side effect, and a spec-gap evidence record or report entry.

`DENY` means `securityd` refused the operation for a valid subject. The required result is `MFOS_ERR_POLICY_DENIED`, no protected handle or content return, and deny audit before final caller result. Missing or untrusted job identity is `MFOS_ERR_UNAUTHENTICATED`, not a policy denial.

`AUDIT_REQUIRED_BUT_UNAVAILABLE` means an audit obligation that must complete before return or before effect cannot be satisfied. Protected work MUST fail closed with `MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE`.

## 6. Component Responsibilities

### 6.1 jobd

`jobd` owns job identity, conversion, queue state, initiator handoff, step orchestration, and job accounting.

Responsibilities:

- Accept or reject submit requests.
- Assign `job_id` after submit request shape is valid and before conversion audit.
- Parse MFOS job-control stream input and produce a source-located internal job graph.
- Establish `effective_principal` through `securityd`.
- Request program execution authorization before step execution.
- Resolve DD statements through the required service chain.
- Sequence steps in the initial subset.
- Aggregate step results into job result fields.
- Cancel jobs and revoke or close owned handles.
- Request required audit records.

Non-responsibilities:

- Final authorization policy decisions.
- Catalog namespace ownership.
- Dataset storage internals.
- Spool storage internals.
- workload policy definition.
- Operator command parsing.

### 6.2 spoold

`spoold` owns input/output stream storage and protected output access.

Responsibilities:

- Store inline INPUT_STREAM payloads as protected spool entries.
- Capture OUTPUT_STREAM record streams.
- Own `SpoolEntry` lifecycle and stale-reference checks.
- Enforce spool retention and purge preconditions supplied by policy.
- Require `securityd` decisions for browse, purge, export, hold, and release.
- Request required spool audit records.

Non-responsibilities:

- Job selection policy.
- Dataset access policy.
- Audit schema ownership.
- Print-device compatibility.
- Job return-code aggregation.

## 7. MFOS Job-Control Stream Grammar

MFOS job-control stream is a line-oriented MFOS-native grammar. It is not JCL compatibility.

### 7.1 Lexical Rules

```text
ALPHA        := "A".."Z"
DIGIT        := "0".."9"
NAME_CHAR    := ALPHA | DIGIT | "_" | "-"
NAME         := ALPHA NAME_CHAR{0,7}
CLASS        := ALPHA | DIGIT
PROGRAM      := NAME ( "." NAME )*
PRINCIPAL    := ALPHA NAME_CHAR{0,31}
DSN          := delegated to dataset/catalog DSN grammar
WS           := one or more spaces or tabs
EOL          := line terminator
TEXT         := any non-EOL bytes
```

Input MAY be normalized to uppercase by operator tooling before submission. `jobd` MUST record whether normalization occurred. The parser MUST preserve original source locations for every card and attribute.

### 7.2 Stream Grammar

```text
job_stream   := leading_line* job_card step_group+ trailing_line*
leading_line := blank_line | comment
trailing_line:= blank_line | comment
blank_line   := ""
comment      := "//*" TEXT

job_card     := "//" job_name WS "JOB" WS job_attrs
step_group   := exec_card dd_card*
exec_card    := "//" step_name WS "EXEC" WS exec_attrs
dd_card      := dataset_dd | output_dd | inline_dd

dataset_dd   := "//" dd_name WS "DD" WS dataset_attrs
output_dd    := "//" dd_name WS "DD" WS output_attrs
inline_dd    := "//" dd_name WS "DD" WS "*" EOL inline_record* inline_end
inline_end   := "/*"
inline_record:= TEXT EOL

job_name     := NAME
step_name    := NAME
dd_name      := NAME
```

### 7.3 Attribute Grammar

Attributes are comma-separated `KEY=VALUE` pairs. Whitespace around commas is allowed. Attribute order is not significant unless explicitly stated.

```text
job_attrs    := job_attr ( "," job_attr )*
job_attr     := "USER=" PRINCIPAL
              | "CLASS=" CLASS
              | "MSGCLASS=" CLASS
              | "SERVICE=" NAME

exec_attrs   := "PGM=" PROGRAM

dataset_attrs:= "DSN=" DSN "," "DISP=" disposition
              | "DISP=" disposition "," "DSN=" DSN

output_attrs := "OUTPUT=" ( CLASS | "*" )

disposition  := "SHR" | "OLD" | "NEW" | "MOD" | "TEMP"
```

### 7.4 Grammar Rules

- A job stream MUST contain exactly one `JOB` card.
- The `JOB` card MUST be the first non-comment, non-blank card.
- A job stream MUST contain at least one `EXEC` card.
- Each `EXEC` card starts a new `JobStep`.
- DD cards bind to the nearest preceding `EXEC` card.
- Step names MUST be unique within a job.
- DD names MUST be unique within a step.
- `USER` is optional. If omitted, `effective_principal` is the submitter subject after submit authorization.
- `CLASS` defaults to policy-defined class `A` only if `securityd` and `workpolicyd` policy explicitly provide that default; otherwise missing `CLASS` is `MFOS_ERR_INVALID_PARAMETER`.
- `MSGCLASS` defaults to the policy-defined job output class only if the policy explicitly provides that default; otherwise missing `MSGCLASS` is `MFOS_ERR_INVALID_PARAMETER`.
- `SERVICE` defaults to the policy-defined service class only if the policy explicitly provides that default; otherwise missing `SERVICE` is `MFOS_ERR_INVALID_PARAMETER`.
- Inline payload size MUST be bounded by a policy value included in submit context.
- Inline payload parsing ends only at a line equal to `/*`.
- Inline payload bytes MUST NOT be parsed as cards.
- Continuation, procedure library, symbolic parameter, include, conditional, concatenation, and nested inline behavior are defined as unsupported for Phase 0.8 and return `MFOS_ERR_UNSUPPORTED`.
- Unknown card operations, unknown attribute keys, malformed separators, duplicate attributes, or ambiguous grammar return `MFOS_ERR_SPEC_GAP` unless a more specific error is defined in this section.

### 7.5 Parser Output

Parser output MUST include:

- `source_digest`
- `source_encoding`
- `line_count`
- ordered `card_locations`
- normalized `job_name`
- ordered `JobStep` graph
- ordered `DDStatement` graph
- diagnostics with line, column, severity, error code, and source excerpt digest

Parser output MUST NOT include a dataset handle, program handle, spool handle, or authorization decision. Those are produced only after conversion and policy checks.

## 8. Object Model

The YAML schemas in `schemas/mfos/` are the machine-readable Phase 0.8 object freezes. This section is the normative semantic description.

### 8.1 Job

```yaml
Job:
  schema_version: 1
  job_id: JobId
  job_name: string
  submitter_principal: PrincipalRef
  requested_principal: PrincipalRef?
  effective_principal: PrincipalRef?
  job_class: string
  service_class: string
  message_class: string
  status: JobStatus
  failure_state: JobFailureState?
  failure_reason_code: string?
  steps: [JobStep]
  spool_refs: [SpoolEntryRef]
  result:
    job_return_code: uint16?
    max_step_return_code: uint16?
    failed_step_id: StepId?
    abend_reason: string?
  accounting:
    submitted_at_utc: timestamp
    started_at_utc: timestamp?
    completed_at_utc: timestamp?
    cpu_time_ms: uint64?
    io_count: uint64?
  audit_correlation_id: uuid
```

Rules:

- `job_id` is assigned by `jobd`, immutable, and not derived from `job_name`.
- `job_name` is operator-visible only and is not a security identity.
- `submitter_principal` is the authenticated submitter known to the submit interface.
- `requested_principal` is populated only when `USER=` appears on the `JOB` card.
- `effective_principal` MUST be absent until submit authorization and any submit-as authorization have succeeded.
- No dataset handle, program handle, or spool handle may be opened before `effective_principal` is present.
- `audit_correlation_id` MUST be assigned before the first required audit record.

### 8.2 JobStep

```yaml
JobStep:
  schema_version: 1
  step_id: StepId
  step_name: string
  ordinal: uint32
  program: ProgramIdentity
  dd: [DDStatement]
  status: JobStepStatus
  return_code: uint16?
  failure_state: StepFailureState?
  failure_reason_code: string?
  started_at_utc: timestamp?
  completed_at_utc: timestamp?
```

Rules:

- Steps execute in ascending `ordinal` order for Phase 0.8.
- Parallel step execution is a spec gap.
- Conditional execution based on earlier return codes is unsupported.
- A step with `status=COMPLETE` MUST have `return_code`.
- A step with `status=FAILED` or `ABENDED` MUST have `failure_state`.

### 8.3 ProgramIdentity

```yaml
ProgramIdentity:
  program_name: string
  program_ref: string?
  program_source: CATALOG_MODULE | BUILTIN_TEST_PROGRAM | SPEC_GAP
  authority_class: NORMAL | AUTHORIZED | SPEC_GAP
  measurement_ref: string?
  policy_version: uint64?
  authorization_decision_id: string?
```

Rules:

- `PGM=` is a symbolic program name, not a POSIX path.
- `jobd` MUST request a `securityd` `PROGRAM EXECUTE` decision for the `effective_principal`.
- Program identity resolution through a cataloged module dataset is the default design target.
- `BUILTIN_TEST_PROGRAM` is allowed only for non-production hosted semantic tests and MUST be labeled in evidence.
- Authorized-program execution is unsupported in Phase 0.8 unless a later AMF specification authorizes it.
- Unknown program namespace behavior returns `MFOS_ERR_SPEC_GAP`.

### 8.4 DDStatement

```yaml
DDStatement:
  schema_version: 1
  dd_id: DDId
  name: string
  kind: DATASET | INPUT_STREAM_INLINE | INPUT_STREAM_SPOOL | OUTPUT_STREAM
  operation: READ | WRITE | UPDATE | CREATE | APPEND
  disposition: SHR | OLD | NEW | MOD | TEMP?
  dsn: string?
  output_class: string?
  inline_digest: string?
  resolved:
    catalog_entry_ref: string?
    dataset_handle_ref: string?
    spool_entry_ref: string?
    security_decision_id: string?
    audit_obligation_id: string?
```

Rules:

- `DSN=` DDs are `DATASET` DDs.
- `DD *` cards are `INPUT_STREAM_INLINE` DDs until converted into `INPUT_STREAM_SPOOL`.
- `OUTPUT=` DDs are `OUTPUT_STREAM` DDs.
- A DD MUST NOT combine `DSN=`, `OUTPUT=`, and inline `*` forms.
- Raw device names, raw volume names, POSIX paths, URLs, and caller-supplied handles are invalid DD resources.
- A resolved DD handle MUST bind to `effective_principal`, operation, policy version, catalog generation where applicable, and audit obligation.

### 8.5 SpoolEntry

```yaml
SpoolEntry:
  schema_version: 1
  spool_id: SpoolId
  entry_type: INPUT_STREAM | OUTPUT_STREAM
  job_id: JobId
  step_id: StepId?
  dd_name: string?
  owner_principal: PrincipalRef
  effective_principal: PrincipalRef
  output_class: string
  security_profile: SecurityProfileRef
  retention_policy: RetentionPolicyRef
  status: SpoolStatus
  size_bytes: uint64
  record_count: uint64
  sequence: uint64
  content_digest: string?
  created_at_utc: timestamp
  closed_at_utc: timestamp?
  purge_after_utc: timestamp?
  purged_at_utc: timestamp?
  audit_correlation_id: uuid
```

Rules:

- `spool_id` is assigned by `spoold`, immutable, and not derived from `job_id` or output class.
- Spool content is a protected resource.
- Spool content is not audit evidence.
- A purged spool reference is stale and MUST NOT return content.
- `owner_principal` is the job `effective_principal` unless policy explicitly assigns ownership differently.

## 9. Identity, Authorization, and DD Resolution

### 9.1 Submit Authorization

Submit flow:

```text
receive_submit_request
  -> validate_request_shape
  -> assign_correlation_id
  -> parse_job_control_stream
  -> request_securityd_job_submit_decision
  -> satisfy_required_audit_obligations
  -> assign_job_id
  -> establish_effective_principal
  -> convert_job_graph
```

Rules:

- `securityd` MUST authorize `JOB SUBMIT` for the submitter before queueing.
- If `USER=` is present and differs from the submitter, `securityd` MUST authorize submit-as delegation.
- If delegation is denied, no `effective_principal` is established and no job enters `QUEUED`.
- Submit denial MUST be audited before the final denial result is returned.
- Missing `securityd`, stale policy, malformed policy, or unsatisfied audit obligations fail closed.

### 9.2 Dataset DD Resolution

For every `DATASET` DD, `jobd` MUST perform this service sequence:

```text
canonicalize_dsn_via_catalogd
  -> resolve_catalog_entry_via_catalogd
  -> request_securityd_dataset_decision
  -> satisfy_required_audit_obligations
  -> request_datasetd_handle
  -> bind_handle_to_dd
```

Rules:

- `catalogd` validates and canonicalizes the DSN before dataset authorization.
- `securityd` authorizes the operation against the resolved protected resource and `effective_principal`.
- `datasetd` issues the handle only after the authorization decision and audit obligation are satisfied.
- A denied, missing, stale, or malformed catalog result MUST NOT produce a dataset handle.
- `DISP=SHR` maps to `READ` unless a later DD attribute specifies a write operation.
- `DISP=OLD` maps to exclusive `UPDATE`.
- `DISP=NEW` maps to `CREATE`.
- `DISP=MOD` maps to `APPEND`.
- `DISP=TEMP` maps to temporary dataset creation and is unsupported until temporary dataset lifetime is specified.

### 9.3 INPUT_STREAM Resolution

Inline INPUT_STREAM flow:

```text
parse_inline_payload
  -> request_securityd_spool_create_decision
  -> satisfy_required_audit_obligations
  -> create_INPUT_STREAM_spool_entry
  -> write_inline_records
  -> close_INPUT_STREAM_spool_entry
  -> bind_spool_ref_to_dd
```

Rules:

- Inline INPUT_STREAM is stored as a `SpoolEntry` with `entry_type=INPUT_STREAM`.
- The INPUT_STREAM spool entry MUST be closed before the step enters `EXECUTING`.
- INPUT_STREAM browse by users or operators uses the same protected spool browse path as OUTPUT_STREAM.
- Oversized inline INPUT_STREAM fails conversion with `MFOS_ERR_LIMIT_EXCEEDED` or the policy-specific limit error.

### 9.4 OUTPUT_STREAM Resolution

OUTPUT_STREAM flow:

```text
request_securityd_spool_create_decision
  -> satisfy_required_audit_obligations
  -> create_OUTPUT_STREAM_spool_entry
  -> bind_open_spool_ref_to_dd
  -> capture_step_output
  -> close_OUTPUT_STREAM_spool_entry
```

Rules:

- `OUTPUT=*` resolves to the job `message_class`.
- `OUTPUT=<class>` resolves to the named output class after policy validation.
- OUTPUT_STREAM creation denial fails the step before program execution.
- OUTPUT_STREAM write failure after execution starts marks the step `FAILED` unless a later explicit policy defines incomplete-output completion.
- Phase 0.8 does not define external print or punch routing.

## 10. Job Lifecycle

### 10.1 JobStatus

```text
RECEIVED
INPUT
CONVERTING
JOB_CONTROL_STREAM_ERROR
VALIDATED
SECURITY_DENIED
QUEUED
SELECTED
EXECUTING
OUTPUT
COMPLETE
FAILED
ABENDED
CANCELING
CANCELED
HELD
PURGE_PENDING
PURGED
SPEC_GAP
UNSUPPORTED
AUDIT_REQUIRED_BUT_UNAVAILABLE
```

### 10.2 Valid Job Transitions

| From | To | Guard |
| --- | --- | --- |
| `RECEIVED` | `INPUT` | request shape accepted |
| `INPUT` | `CONVERTING` | parser starts |
| `INPUT` | `JOB_CONTROL_STREAM_ERROR` | parser rejects input |
| `CONVERTING` | `JOB_CONTROL_STREAM_ERROR` | conversion rejects input |
| `CONVERTING` | `SECURITY_DENIED` | submit or submit-as denied |
| `CONVERTING` | `VALIDATED` | syntax, submit authorization, and required audit complete |
| `VALIDATED` | `QUEUED` | effective principal and job graph exist |
| `QUEUED` | `SELECTED` | initiator and workload policy selection accept |
| `QUEUED` | `CANCELING` | authorized cancel request |
| `SELECTED` | `EXECUTING` | initiator starts first runnable step |
| `EXECUTING` | `OUTPUT` | all required steps reached terminal step state |
| `EXECUTING` | `FAILED` | step failure is terminal for the job |
| `EXECUTING` | `ABENDED` | abend-like failure is terminal for the job |
| `EXECUTING` | `CANCELING` | authorized cancel request |
| `OUTPUT` | `COMPLETE` | output close and accounting audit complete |
| `OUTPUT` | `FAILED` | required output close or accounting audit fails |
| `COMPLETE` | `PURGE_PENDING` | retention and authorization allow purge request |
| `FAILED` | `PURGE_PENDING` | retention and authorization allow purge request |
| `ABENDED` | `PURGE_PENDING` | retention and authorization allow purge request |
| `CANCELED` | `PURGE_PENDING` | retention and authorization allow purge request |
| `HELD` | `QUEUED` | authorized release before execution |
| `HELD` | `PURGE_PENDING` | authorized purge of held terminal output |
| `CANCELING` | `CANCELED` | resources closed or revoked and audit complete |
| `PURGE_PENDING` | `PURGED` | spool entries purged and stale references recorded |
| any non-terminal | `HELD` | authorized hold request |
| any non-terminal | `SPEC_GAP` | undefined requested behavior |
| any non-terminal | `UNSUPPORTED` | defined unsupported requested behavior |
| any non-terminal | `AUDIT_REQUIRED_BUT_UNAVAILABLE` | required audit cannot be completed |

### 10.3 Invalid Job Transitions

All transitions not listed in section 10.2 are invalid. Invalid transitions MUST return `MFOS_ERR_INVALID_TRANSITION`, MUST NOT mutate job or spool state, and MUST audit if the attempted transition was security-sensitive.

Explicit invalid transitions:

- `RECEIVED -> QUEUED`
- `INPUT -> EXECUTING`
- `CONVERTING -> QUEUED` without `VALIDATED`
- `JOB_CONTROL_STREAM_ERROR -> QUEUED`
- `SECURITY_DENIED -> QUEUED`
- `QUEUED -> COMPLETE`
- `SELECTED -> COMPLETE`
- `EXECUTING -> PURGED`
- `COMPLETE -> EXECUTING`
- `FAILED -> EXECUTING`
- `CANCELED -> EXECUTING`
- `PURGED -> any state`

## 11. Step Execution

### 11.1 JobStepStatus

```text
PENDING
RESOLVING_DD
AUTHORIZING_PROGRAM
OPENING_RESOURCES
READY
EXECUTING
CAPTURING_OUTPUT_STREAM
CLOSING_RESOURCES
COMPLETE
FAILED
ABENDED
CANCELING
CANCELED
SPEC_GAP
UNSUPPORTED
AUDIT_REQUIRED_BUT_UNAVAILABLE
```

### 11.2 Valid Step Transitions

| From | To | Guard |
| --- | --- | --- |
| `PENDING` | `RESOLVING_DD` | job is `EXECUTING` and prior steps are terminal |
| `RESOLVING_DD` | `AUTHORIZING_PROGRAM` | all DDs resolved or prepared |
| `RESOLVING_DD` | `FAILED` | DD resolution failed |
| `AUTHORIZING_PROGRAM` | `OPENING_RESOURCES` | program execute authorized and audit complete |
| `AUTHORIZING_PROGRAM` | `FAILED` | program execute denied or program unresolved |
| `OPENING_RESOURCES` | `READY` | dataset and spool handles opened |
| `OPENING_RESOURCES` | `FAILED` | resource open failed |
| `READY` | `EXECUTING` | initiator dispatches program |
| `EXECUTING` | `CAPTURING_OUTPUT_STREAM` | program exits normally and OUTPUT_STREAM remains open |
| `EXECUTING` | `ABENDED` | program abend-like failure or execution fault |
| `EXECUTING` | `CANCELING` | authorized cancel signal |
| `CAPTURING_OUTPUT_STREAM` | `CLOSING_RESOURCES` | output capture finished |
| `CAPTURING_OUTPUT_STREAM` | `FAILED` | required OUTPUT_STREAM capture failed |
| `CLOSING_RESOURCES` | `COMPLETE` | all handles closed and audit complete |
| `CLOSING_RESOURCES` | `FAILED` | required close, revoke, or audit failed |
| `CANCELING` | `CANCELED` | handles closed or revoked and audit complete |
| any non-terminal | `SPEC_GAP` | undefined requested behavior |
| any non-terminal | `UNSUPPORTED` | defined unsupported requested behavior |
| any non-terminal | `AUDIT_REQUIRED_BUT_UNAVAILABLE` | required audit cannot be completed |

### 11.3 Return Codes and Failure State

Return-code rules:

- `return_code` is an unsigned integer in range `0..4095`.
- Normal program exit sets step `status=COMPLETE` and records `return_code`.
- A nonzero return code is a completed step result, not automatically a step failure in Phase 0.8.
- If all steps complete, `job_return_code` is the maximum step return code.
- If any step enters `FAILED`, `ABENDED`, or `CANCELED`, the job terminal state reflects that failure class.
- Job `max_step_return_code` records the maximum return code among completed steps even when a later step fails.
- A failed step without normal program exit MUST record `failure_state` and `failure_reason_code`.
- An abend-like step failure MUST record `failure_state=ABENDED` and `abend_reason`.
- Multi-step conditional execution and return-code thresholds are unsupported.

Step failure states:

```text
JOB_CONTROL_STREAM_ERROR
SECURITY_DENIED
DATASET_RESOLVE_FAILED
DATASET_OPEN_DENIED
PROGRAM_RESOLVE_FAILED
PROGRAM_EXECUTE_DENIED
PROGRAM_LOAD_DENIED
INPUT_STREAM_PREPARE_FAILED
OUTPUT_STREAM_CREATE_DENIED
OUTPUT_STREAM_CAPTURE_FAILED
RESOURCE_CLOSE_FAILED
ABENDED
CANCELED
AUDIT_REQUIRED_BUT_UNAVAILABLE
UNSUPPORTED
SPEC_GAP
INTERNAL_CORRUPTION
```

## 12. Spool Semantics

### 12.1 SpoolStatus

```text
CREATE_REQUESTED
AUTHORIZING_CREATE
OPEN
WRITING
CLOSED
HELD
BROWSE_ACTIVE
EXPORTING
PURGE_PENDING
PURGED
FAILED
SPEC_GAP
UNSUPPORTED
AUDIT_REQUIRED_BUT_UNAVAILABLE
```

### 12.2 Valid Spool Transitions

| From | To | Guard |
| --- | --- | --- |
| `CREATE_REQUESTED` | `AUTHORIZING_CREATE` | create request accepted |
| `AUTHORIZING_CREATE` | `OPEN` | create authorized and audit complete |
| `AUTHORIZING_CREATE` | `FAILED` | create denied or audit failed |
| `OPEN` | `WRITING` | first record accepted |
| `OPEN` | `CLOSED` | empty entry close allowed by policy |
| `WRITING` | `WRITING` | next sequence accepted |
| `WRITING` | `CLOSED` | close accepted |
| `CLOSED` | `HELD` | hold policy or authorized hold request |
| `HELD` | `CLOSED` | authorized release |
| `CLOSED` | `BROWSE_ACTIVE` | browse authorized |
| `HELD` | `BROWSE_ACTIVE` | browse authorized for held output |
| `BROWSE_ACTIVE` | `CLOSED` | browse session closed |
| `BROWSE_ACTIVE` | `HELD` | browse session closed for held output |
| `CLOSED` | `EXPORTING` | export authorized |
| `HELD` | `EXPORTING` | export authorized for held output |
| `EXPORTING` | `CLOSED` | export complete for unheld output |
| `EXPORTING` | `HELD` | export complete for held output |
| `CLOSED` | `PURGE_PENDING` | retention and authorization allow purge |
| `HELD` | `PURGE_PENDING` | retention and authorization allow purge |
| `PURGE_PENDING` | `PURGED` | content removed and stale ref recorded |
| any non-terminal | `SPEC_GAP` | undefined requested behavior |
| any non-terminal | `UNSUPPORTED` | defined unsupported requested behavior |
| any non-terminal | `AUDIT_REQUIRED_BUT_UNAVAILABLE` | required audit cannot be completed |

### 12.3 Invalid Spool Transitions

All transitions not listed in section 12.2 are invalid. Invalid spool transitions MUST return `MFOS_ERR_INVALID_TRANSITION`, MUST NOT return content, MUST NOT remove content, and MUST audit if security-sensitive.

Explicit invalid transitions:

- `CREATE_REQUESTED -> WRITING`
- `AUTHORIZING_CREATE -> CLOSED`
- `OPEN -> BROWSE_ACTIVE`
- `OPEN -> EXPORTING`
- `WRITING -> BROWSE_ACTIVE`
- `WRITING -> PURGE_PENDING`
- `CLOSED -> PURGED`
- `PURGE_PENDING -> BROWSE_ACTIVE`
- `PURGED -> BROWSE_ACTIVE`
- `PURGED -> EXPORTING`
- `PURGED -> OPEN`
- `PURGED -> WRITING`

### 12.4 Browse

Browse flow:

```text
receive_browse_request
  -> identify_spool_entry
  -> reject_stale_or_purged_ref
  -> request_securityd_spool_browse_decision
  -> satisfy_required_audit_obligations
  -> open_browse_session
  -> return_records
```

Rules:

- Browse requires `securityd` `SPOOL BROWSE`.
- Browse denial MUST be audited before the final denial result.
- Browse of `PURGED` returns `MFOS_ERR_STALE_SPOOL_REF`.
- Browse MUST NOT expose records before authorization and required audit completion.

### 12.5 Export

Export flow:

```text
receive_export_request
  -> identify_spool_entry
  -> reject_stale_or_purged_ref
  -> validate_destination_class
  -> request_securityd_spool_export_decision
  -> satisfy_required_audit_obligations
  -> export_records
```

Rules:

- Export requires `securityd` `SPOOL EXPORT`.
- Export destination classes are policy names, not raw paths or URLs.
- Raw filesystem export is a spec gap.
- Export denial MUST be audited before final denial result.
- Export MUST record destination class, subject, spool ID, content digest, and result.

### 12.6 Purge and Retention

Purge flow:

```text
receive_purge_request
  -> identify_spool_entry
  -> reject_stale_or_purged_ref
  -> evaluate_retention_policy
  -> request_securityd_spool_purge_decision
  -> satisfy_required_audit_obligations
  -> mark_PURGE_PENDING
  -> remove_content
  -> mark_PURGED
```

Rules:

- Purge requires both retention eligibility and `securityd` `SPOOL PURGE`.
- `purge_after_utc` MUST be honored unless a policy-defined emergency purge path exists.
- Legal hold prevents purge until released by authorized policy action.
- Purge before retention expiry returns `MFOS_ERR_RETENTION_DENIED`.
- Purge denial MUST be audited before final denial result.
- After purge, browse and export return `MFOS_ERR_STALE_SPOOL_REF` and no content.

## 13. Audit Obligations

Required job audit events:

| Event | Required fields |
| --- | --- |
| `JOB_SUBMIT_REQUEST` | submitter, requested_principal, job_name, job_class, service_class, message_class, correlation_id |
| `JOB_SUBMIT_ALLOW` | job_id, effective_principal, policy_version, decision_id |
| `JOB_SUBMIT_DENY` | submitter, requested_principal, reason_code, policy_version, decision_id |
| `JOB_CONVERSION_RESULT` | job_id, result, diagnostic_count, source_digest |
| `JOB_QUEUED` | job_id, job_class, service_class, effective_principal |
| `JOB_SELECTED` | job_id, initiator_id, wlm_decision_ref |
| `JOB_STEP_START` | job_id, step_id, program_name, program_ref |
| `JOB_PROGRAM_DECISION` | job_id, step_id, program_name, decision, policy_version |
| `JOB_DD_RESOLVE` | job_id, step_id, dd_name, resource_ref, operation, result |
| `JOB_STEP_COMPLETE` | job_id, step_id, return_code, failure_state, abend_reason |
| `JOB_COMPLETE` | job_id, status, job_return_code, max_step_return_code, accounting_summary |
| `JOB_CANCEL_REQUEST` | subject, job_id, reason_code |
| `JOB_CANCEL_RESULT` | subject, job_id, result, resources_closed |
| `JOB_INVALID_TRANSITION` | subject, job_id, from_state, requested_state, reason_code |

Required spool audit events:

| Event | Required fields |
| --- | --- |
| `SPOOL_CREATE_REQUEST` | job_id, step_id, dd_name, entry_type, output_class, owner_principal |
| `SPOOL_CREATE_ALLOW` | spool_id, security_profile, retention_policy, policy_version |
| `SPOOL_CREATE_DENY` | subject, job_id, step_id, reason_code, policy_version |
| `SPOOL_WRITE` | spool_id, sequence, bytes_written, record_count |
| `SPOOL_CLOSE` | spool_id, size_bytes, content_digest, result |
| `SPOOL_BROWSE_ALLOW` | subject, spool_id, policy_version, decision_id |
| `SPOOL_BROWSE_DENY` | subject, spool_id, reason_code, policy_version |
| `SPOOL_EXPORT_ALLOW` | subject, spool_id, destination_class, policy_version |
| `SPOOL_EXPORT_DENY` | subject, spool_id, reason_code, policy_version |
| `SPOOL_PURGE_ALLOW` | subject, spool_id, retention_policy, policy_version |
| `SPOOL_PURGE_DENY` | subject, spool_id, reason_code, retention_policy |
| `SPOOL_PURGED` | subject, spool_id, purged_at_utc, stale_ref_generation |
| `SPOOL_INVALID_TRANSITION` | subject, spool_id, from_state, requested_state, reason_code |

Ordering rules:

- Submit deny audit MUST complete before `jobd` returns final denial.
- Dataset open deny audit MUST complete before a step receives final failure.
- Program execute deny audit MUST complete before a step receives final failure.
- Spool browse, purge, export, and create deny audit MUST complete before returning final denial.
- Required completion and purge audit failures MUST fail closed.

## 14. Failure Modes

| Error | State impact | Required behavior |
| --- | --- | --- |
| `MFOS_ERR_INVALID_PARAMETER` | `JOB_CONTROL_STREAM_ERROR` or request reject | Reject before queueing and before protected side effects. |
| `MFOS_ERR_INVALID_JOB_CONTROL` | `JOB_CONTROL_STREAM_ERROR` | Record diagnostics; do not enqueue. |
| `MFOS_ERR_UNAUTHENTICATED` | submit or step `FAILED` before protected open | No effective principal exists; no handle, no content, audit when possible. |
| `MFOS_ERR_POLICY_DENIED` | `SECURITY_DENIED` or step `FAILED` | No handle, no content, deny audit before final result. |
| `MFOS_ERR_INVALID_DSN` | step `FAILED` or `JOB_CONTROL_STREAM_ERROR` | No catalog or dataset handle. |
| `MFOS_ERR_CATALOG_NOT_FOUND` | step `FAILED` | No dataset handle; DD resolution audit records failure. |
| `MFOS_ERR_STALE_HANDLE` | step `FAILED` | Revoke handle and fail the step. |
| `MFOS_ERR_STALE_SPOOL_REF` | request reject | Return no spool content and audit if security-sensitive. |
| `MFOS_ERR_RETENTION_DENIED` | spool remains `CLOSED` or `HELD` | Do not purge; audit purge denial. |
| `MFOS_ERR_LIMIT_EXCEEDED` | `JOB_CONTROL_STREAM_ERROR` or step `FAILED` | Do not create oversized input or output stream entry. |
| `MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE` | fail-closed state | No protected work proceeds. |
| `MFOS_ERR_UNSUPPORTED` | `UNSUPPORTED` | No protected side effect; record unsupported evidence. |
| `MFOS_ERR_SPEC_GAP` | `SPEC_GAP` | No protected side effect; record spec-gap evidence. |
| `MFOS_ERR_INVALID_TRANSITION` | unchanged | State unchanged; audit if security-sensitive. |
| `MFOS_ERR_INTERNAL_CORRUPTION` | `HELD` or fail-closed state | Hold affected jobs or spool entries and require recovery review. |

## 15. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| `MFOS-REQ-JOB-0001` | Job lifecycle MUST include input, conversion, queueing, execution, output, and purge phases. | State-machine tests |
| `MFOS-REQ-JOB-0002` | MFOS job-control stream parser MUST be fuzzed with malformed cards, oversized input, and unsupported features. | Fuzz campaign |
| `MFOS-REQ-JOB-0003` | Job effective principal MUST be established before dataset, program, or spool open. | Integration tests |
| `MFOS-REQ-JOB-0004` | DD resolution MUST pass through `catalogd`, `datasetd`, `spoold`, `securityd`, and `auditd` as applicable. | Integration tests |
| `MFOS-REQ-JOB-0005` | Step completion or failure MUST include return code, failure state, or abend-like reason. | Unit tests |
| `MFOS-REQ-JOB-0006` | Job submit MUST require `securityd` authorization. | Negative tests |
| `MFOS-REQ-JOB-0007` | Job conversion failure MUST NOT enqueue executable work. | Parser tests |
| `MFOS-REQ-JOB-0008` | Job cancellation MUST close or revoke protected resource handles. | Integration tests |
| `MFOS-REQ-JOB-0009` | Job accounting MUST include submit, start, complete, CPU, IO, status, and result fields when available. | Schema tests |
| `MFOS-REQ-SPOOL-0001` | Spool entry MUST be a protected resource. | Security tests |
| `MFOS-REQ-SPOOL-0002` | Spool browse, purge, and export MUST require `securityd` decisions. | Negative tests |
| `MFOS-REQ-SPOOL-0003` | OUTPUT_STREAM MUST include owner, job ID, step ID, output class, security profile, retention policy, and content digest. | Schema tests |
| `MFOS-REQ-SPOOL-0004` | Spool retention MUST control purge eligibility. | Retention tests |
| `MFOS-REQ-SPOOL-0005` | Spool deny decisions MUST be audited before final denial result. | Ordering tests |
| `MFOS-REQ-SPOOL-0006` | OUTPUT_STREAM capture failure MUST fail the step unless a later explicit policy defines incomplete-output completion. | Fault injection |

## 16. Security Invariants

```text
INV-JOB-001:
  A job cannot enter QUEUED unless syntax validation, submit
  authorization, effective principal establishment, and required audit
  obligations have succeeded.

INV-JOB-002:
  No dataset, program, input stream, or output stream handle can be opened before
  effective_principal is established.

INV-JOB-003:
  DD resolution cannot produce a dataset handle unless catalogd
  resolved the DSN and securityd authorized the operation for the
  effective principal.

INV-JOB-004:
  A terminal failed, canceled, abended, unsupported, or spec-gap job
  cannot re-enter EXECUTING.

INV-JOB-005:
  Unsupported and spec-gap behavior cannot produce a protected side
  effect or a successful operation result.

INV-SPL-001:
  Spool content cannot be browsed or exported unless securityd allowed
  the operation and required audit obligations completed.

INV-SPL-002:
  Purge cannot proceed unless retention eligibility and securityd purge
  authorization both hold.

INV-SPL-003:
  Purged spool references are stale and cannot return content.

INV-SPL-004:
  Spool output cannot substitute for auditd evidence.
```

## 17. Test and Fuzz Freeze

The draft test catalog is `tests/catalog/phase-0-8-job-spool-tests.yml`.

Required positive coverage:

- Authorized submit, DD resolution, INPUT_STREAM, OUTPUT_STREAM, and RC=0 completion.
- Conversion of a multi-step MFOS job-control stream stream into an internal job graph.
- Effective principal defaulting to submitter when `USER=` is absent.
- Authorized submit-as with `USER=`.
- OUTPUT_STREAM creation and authorized owner browse.
- Retention-satisfied purge.

Required negative coverage:

- Unauthorized submit.
- Unauthorized submit-as.
- Malformed MFOS job-control stream input.
- Unsupported continuation, procedure, include, symbolic, or conditional grammar.
- Dataset access denied through DD resolution.
- Program execute denied.
- OUTPUT_STREAM create denied.
- Browse denied with no content return.
- Export denied with no content return.
- Purge denied before retention expiry.
- Stale spool reference after purge.
- Invalid job, step, and spool transitions.
- Required audit unavailable during deny or protected effect.

Required fuzz targets:

- `fuzz_job_control_stream_parser`
- `fuzz_job_submit_request`
- `fuzz_dd_resolution`
- `fuzz_inline_input_stream_payload`
- `fuzz_spool_record_stream`
- `fuzz_spool_access_request`
- `fuzz_job_cancel_race`

Fuzz invariants:

- Parser must not panic.
- Malformed input must not reach `QUEUED`.
- Unsupported input must not create handles.
- Spec-gap input must not create handles.
- Unauthorized DD resolution must not produce a dataset handle.
- Unauthorized spool browse or export must not return content.
- Purged spool references must not return content.

## 18. Evidence Expectations

Phase 0.8 evidence is design evidence only. Production evidence is not claimed.

Expected evidence artifacts:

- Schema parse and review evidence for the four YAML schemas.
- State-machine review evidence for job lifecycle and spool access models.
- Test catalog review evidence for positive, negative, fault-injection, and fuzz coverage.
- Source-grounding review confirming only EXTREF source refs are used in this spec.
- Spec-gap report showing unsupported and undefined behavior fail closed.
- Audit-obligation review for deny-before-return ordering.

Current evidence placeholder:

- `reports/phase-0-8-job-spool-lead.md`

## 19. Spec Gaps

| Gap ID | Gap | Required handling |
| --- | --- | --- |
| `SPEC-GAP-JOB-0001` | Final production program loader contract and module dataset schema. | Return `MFOS_ERR_SPEC_GAP` for undefined program namespaces. |
| `SPEC-GAP-JOB-0002` | Temporary dataset lifetime for `DISP=TEMP`. | Return `MFOS_ERR_UNSUPPORTED` for `DISP=TEMP` until specified. |
| `SPEC-GAP-JOB-0003` | Restart metadata and restart safety rules. | Reject restart requests with `MFOS_ERR_SPEC_GAP`. |
| `SPEC-GAP-JOB-0004` | Multi-step conditional execution. | Return `MFOS_ERR_UNSUPPORTED` for conditional grammar. |
| `SPEC-GAP-JOB-0005` | Procedure library and symbolic parameter model. | Return `MFOS_ERR_UNSUPPORTED` for PROC, INCLUDE, and symbolic forms. |
| `SPEC-GAP-JOB-0006` | Parallel step execution. | Do not schedule parallel steps. |
| `SPEC-GAP-JOB-0007` | Complete abend-like reason taxonomy. | Use generic `ABENDED` with reason string; no compatibility claim. |
| `SPEC-GAP-SPOOL-0001` | Binary spool record format. | Treat as internal draft; no external compatibility claim. |
| `SPEC-GAP-SPOOL-0002` | Quota hierarchy and emergency override. | Fail closed on quota ambiguity. |
| `SPEC-GAP-SPOOL-0003` | External print/export gateway. | Raw destinations return `MFOS_ERR_SPEC_GAP`. |
| `SPEC-GAP-SPOOL-0004` | Retention policy administration workflow. | Purge only when an approved policy object exists. |
| `SPEC-GAP-SPOOL-0005` | Incomplete-output completion policy. | OUTPUT_STREAM capture failure fails the step. |

## 20. Implementation Prompt Contract

No production implementation is authorized by Phase 0.8. A future implementation prompt MUST include:

```text
Use spec MFOS-SPEC-09-JOB-SPOOL v0.8 and these artifacts:
- schemas/mfos/job.schema.yml
- schemas/mfos/job-step.schema.yml
- schemas/mfos/dd.schema.yml
- schemas/mfos/spool-entry.schema.yml
- formal/tla/job-lifecycle/JobLifecycle.tla
- formal/tla/spool-access/SpoolAccess.tla
- tests/catalog/phase-0-8-job-spool-tests.yml

Rules:
- Do not claim z/OS, JES, JES2, JCL, RACF, DFSMS, or SMF compatibility.
- Job effective principal must exist before any dataset, program, input stream, or output stream handle opens.
- DD resolution must use catalogd, datasetd, spoold, securityd, and auditd as applicable.
- Spool entries are protected resources.
- Deny audit must complete before final denial result.
- Unsupported behavior returns MFOS_ERR_UNSUPPORTED.
- Undefined behavior returns MFOS_ERR_SPEC_GAP.
- Invalid transitions return MFOS_ERR_INVALID_TRANSITION and leave state unchanged.
- No protected content, handle, purge, export, or execution result may be produced by deny, unsupported, spec-gap, stale-reference, or audit-unavailable paths.

Deliver:
1. Implemented requirement IDs
2. Source Matrix IDs
3. Assumptions
4. Spec gaps
5. Unsupported features
6. Security invariants
7. Audit obligations
8. Failure modes
9. Positive tests added
10. Negative tests added
11. Fuzz targets added
12. Fault-injection tests added
13. Formal model evidence
14. Unsafe code justification
15. Review checklist
16. Evidence artifacts
```
