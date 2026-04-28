---
spec_id: "MFOS-SPEC-11-WORKLOAD-POLICY"
title: "MFOS Workload Policy Specification v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["EXTREF-IBM-ZOS-JES-INTRODUCTION-0001", "EXTREF-IBM-ZOS-JES-JOB-FLOW-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001", "EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001"]
requirement_refs: ["MFOS-REQ-WPOL-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Workload Policy Specification v0.1

Status: Draft

Owned component: `workpolicyd`

Primary source matrix IDs: `EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001`, `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-JES-JOB-FLOW-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001`

Related requirements: `MFOS-REQ-WPOL-*`, `MFOS-REQ-JOB-*`, `MFOS-REQ-OPER-*`, `MFOS-REQ-AUTH-*`, `MFOS-REQ-AUDIT-*`, `MFOS-REQ-AI-*`

## 1. Purpose

This specification defines MFOS workload management. `workpolicyd` classifies submitted work, controls concurrency, provides dispatch hints, and records workload decisions for audit and accounting.

MFOS is z/OS-inspired, not z/OS-compatible. The source-grounded overlap is the enterprise idea of grouping work into service classes, goals, importance, and reporting classes. MFOS diverges by introducing a staged x64-native design. Phase 1 implements job classes, priority, max concurrency, resource caps, and dispatch hints. Later phases add richer service-class and goal semantics.

## 2. Scope

In scope:

- Job class definitions.
- Service class definitions.
- Report class labels.
- Priority and max-concurrency control.
- Resource cap model.
- Dispatch hint generation for jobd.
- Overload policy.
- workload policy activation through operatord and securityd.
- workload policy decision audit and accounting hooks.

Out of scope:

- z/OS external workload management compatibility.
- Exact z/OS velocity or response-time algorithms.
- Sysplex-like multi-node workload balancing.
- Live migration.
- Direct CPU scheduler ownership in Phase 1.
- Dataset access decisions.
- Security policy decisions.

## 3. Non-Compatibility Statement

MFOS MUST NOT claim z/OS external workload management compatibility. MFOS MAY say "external-workload-management-informed service class and goal model" when Source Matrix IDs and MFOS divergence are explicit.

Prohibited wording:

- "z/OS external-workload-management-compatible"
- "z/OS service-class compatible"
- "z/OS velocity compatible"

Allowed wording:

- "external-workload-management-informed service-class model"
- "MFOS workload policy"
- "service-class-like dispatch hint"

## 4. Component Responsibilities

`workpolicyd` owns workload classification and dispatch policy hints.

Responsibilities:

- `WPOL-R-001` Job class.
- `WPOL-R-002` Service class.
- `WPOL-R-003` Priority.
- `WPOL-R-004` Resource cap.
- `WPOL-R-005` Dispatch hint.
- `WPOL-R-006` Max concurrency.
- `WPOL-R-007` Overload policy.
- `WPOL-R-008` Report class.
- `WPOL-R-009` Future response-time goal.
- `WPOL-R-010` Future velocity-like goal.

Non-responsibilities:

- Final security authorization.
- Dataset access.
- Job parsing.
- Step execution.
- Audit schema ownership.
- Nucleus scheduler internals.
- PXM partition scheduling.

## 5. Staged Capability Model

Phase 1:

- Job class.
- Priority.
- Max concurrent jobs per class.
- Static resource cap.
- Dispatch hint.
- Basic overload action.

Phase 2:

- Service class.
- Report class.
- Business importance.
- Velocity-like goal placeholder with explicit non-compatibility statement.

Phase 3:

- Response-time goal.
- Policy activation workflow.
- Operator workload policy panel/command set.
- Richer accounting and feedback loop.

## 6. Object Model

### 6.1 WlmPolicy

```yaml
WlmPolicy:
  policy_id: string
  version: uint64
  state: DRAFT | VALIDATED | ACTIVE | RETIRED | REJECTED
  job_classes: [JobClass]
  service_classes: [ServiceClass]
  report_classes: [ReportClass]
  overload_policy: OverloadPolicy
  created_by: PrincipalRef
  activated_by: PrincipalRef?
  created_at_utc: timestamp
  activated_at_utc: timestamp?
  source_matrix_refs: [string]
```

### 6.2 JobClass

```yaml
JobClass:
  class_id: string
  description: string
  enabled: bool
  default_service_class: string
  priority: uint8
  max_concurrent: uint32
  queue_limit: uint32
  submit_allowed_profiles: [SecurityProfileRef]
  resource_cap:
    cpu_weight: uint32
    max_memory_bytes: uint64?
    max_runtime_seconds: uint64?
    max_io_ops: uint64?
```

### 6.3 ServiceClass

```yaml
ServiceClass:
  service_class_id: string
  description: string
  importance: uint8
  goal:
    type: DISCRETIONARY | VELOCITY_LIKE | RESPONSE_TIME
    velocity_target: uint8?
    response_time_ms: uint64?
  admission:
    max_concurrent: uint32?
    overload_action: HOLD | DEFER | REJECT | RUN_LOW_PRIORITY
```

### 6.4 ReportClass

```yaml
ReportClass:
  report_class_id: string
  description: string
  match:
    job_class: string?
    service_class: string?
    principal_group: string?
```

### 6.5 WlmDecision

```yaml
WlmDecision:
  decision_id: uuid
  job_id: string
  policy_id: string
  policy_version: uint64
  job_class: string
  service_class: string
  report_class: string?
  priority: uint8
  dispatch_hint: RUN_NOW | HOLD | DEFER | REJECT | RUN_LOW_PRIORITY
  reason_code: string
  resource_cap_snapshot: map
  decided_at_utc: timestamp
  correlation_id: uuid
```

## 7. State Machines

### 7.1 Policy Lifecycle

```text
CREATE_DRAFT
  -> VALIDATE_SCHEMA
  -> VALIDATE_REFERENCES
  -> SECURITYD_AUTHORIZE_ACTIVATION
  -> AUDIT_POLICY_VALIDATED
  -> ACTIVATE
  -> ACTIVE
  -> RETIRE
```

Failure states:

```text
SCHEMA_INVALID
REFERENCE_INVALID
POLICY_DENIED
AUDIT_REQUIRED_BUT_UNAVAILABLE
CONFLICT_WITH_ACTIVE_POLICY
SPEC_GAP
```

Activation rules:

- Only one workload policy version may be active per MFOS partition.
- Activation MUST be authorized by securityd.
- Activation MUST be audited before `workpolicyd` returns success.
- Active policy changes MUST increment policy version.
- Jobd MUST receive the active policy version with each dispatch decision.

### 7.2 Job Classification Lifecycle

```text
CLASSIFY_REQUEST
  -> LOAD_ACTIVE_POLICY
  -> VALIDATE_JOB_CLASS
  -> MAP_SERVICE_CLASS
  -> CHECK_QUEUE_LIMIT
  -> CHECK_MAX_CONCURRENCY
  -> CHECK_RESOURCE_CAP
  -> PRODUCE_DISPATCH_HINT
  -> AUDIT_DECISION
  -> RETURN_DECISION
```

Failure states:

```text
NO_ACTIVE_POLICY
JOB_CLASS_DISABLED
JOB_CLASS_UNKNOWN
SERVICE_CLASS_UNKNOWN
QUEUE_LIMIT_EXCEEDED
MAX_CONCURRENCY_REACHED
RESOURCE_CAP_EXCEEDED
POLICY_VERSION_MISMATCH
AUDIT_REQUIRED_BUT_UNAVAILABLE
SPEC_GAP
```

Dispatch hint semantics:

| Hint | Meaning |
| --- | --- |
| `RUN_NOW` | Job may be selected by jobd when an initiator is available. |
| `HOLD` | Job remains queued until operator or policy release. |
| `DEFER` | Job remains queued and should be reconsidered later. |
| `REJECT` | Job should not be accepted under current policy. |
| `RUN_LOW_PRIORITY` | Job may run only after higher-priority eligible work. |

## 8. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| `MFOS-REQ-WPOL-0001` | workpolicyd MUST support job classes. | Unit tests |
| `MFOS-REQ-WPOL-0002` | workpolicyd MUST support priority and max concurrency per job class. | Queue tests |
| `MFOS-REQ-WPOL-0003` | workpolicyd MUST return typed dispatch hints to jobd. | Interface tests |
| `MFOS-REQ-WPOL-0004` | workpolicyd MUST support service class identifiers in policy and decisions. | Schema tests |
| `MFOS-REQ-WPOL-0005` | workpolicyd MUST support report class labels for accounting. | Audit tests |
| `MFOS-REQ-WPOL-0006` | workload policy activation MUST require securityd authorization. | Negative tests |
| `MFOS-REQ-WPOL-0007` | workload policy activation MUST be audited before success is returned. | Ordering tests |
| `MFOS-REQ-WPOL-0008` | Unknown job class MUST fail closed or map only through explicit default policy. | Negative tests |
| `MFOS-REQ-WPOL-0009` | Overload behavior MUST be explicit: hold, defer, reject, or run low priority. | Policy tests |
| `MFOS-REQ-WPOL-0010` | z/OS-compatible velocity or response-time claims MUST NOT be made. | Documentation review |
| `MFOS-REQ-WPOL-0011` | Active policy version MUST be included in every workload policy decision. | Interface tests |
| `MFOS-REQ-WPOL-0012` | Jobd MUST not reinterpret workload policy beyond typed dispatch hints. | Architecture review |

## 9. Security Invariants

```text
INV-WPOL-001:
  workload policy activation cannot succeed without a securityd ALLOW or
  ALLOW_WITH_AUDIT decision for the operator subject and policy object.

INV-WPOL-002:
  workload policy dispatch decisions cannot override securityd authorization for job,
  dataset, program, operator, or spool resources.

INV-WPOL-003:
  every dispatch decision returned to jobd must include policy_id,
  policy_version, job_class, service_class, dispatch_hint, and reason_code.

INV-WPOL-004:
  overload cannot silently fall back to run-now behavior.

INV-WPOL-005:
  workload policy cannot claim z/OS-compatible goal semantics.
```

## 10. Audit Obligations

Required audit events:

| Event | Required fields |
| --- | --- |
| `WORKLOAD_POLICY_CREATE` | subject, policy_id, draft_version |
| `WORKLOAD_POLICY_VALIDATE` | subject, policy_id, validation_result |
| `WORKLOAD_POLICY_ACTIVATE_ALLOW` | subject, policy_id, policy_version |
| `WORKLOAD_POLICY_ACTIVATE_DENY` | subject, policy_id, reason_code, security_policy_version |
| `WORKLOAD_POLICY_RETIRE` | subject, policy_id, policy_version |
| `WLM_CLASSIFY_REQUEST` | job_id, job_class, requested_service_class, correlation_id |
| `WLM_DECISION` | decision_id, job_id, policy_id, policy_version, dispatch_hint, reason_code |
| `WLM_OVERLOAD` | job_class, service_class, overload_action, current_counts |
| `WORKLOAD_POLICY_MISMATCH` | job_id, expected_version, observed_version |

Ordering rules:

- Policy activation DENY MUST be audited before returning denial.
- Policy activation success MUST be audited before new policy is reported active.
- Dispatch decision audit MUST occur before jobd selects the job for execution when audit is required by profile.

## 11. Failure Modes

| Error | Meaning | Required behavior |
| --- | --- | --- |
| `MFOS_ERR_UNAUTHORIZED` | Policy operation denied. | No activation; audit denial. |
| `MFOS_ERR_POLICY_DENIED` | Policy rejects job classification. | Return typed rejection decision. |
| `MFOS_ERR_POLICY_VERSION_MISMATCH` | Caller decision context is stale. | Reclassify or fail closed. |
| `MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE` | Required workload policy audit cannot be written. | Fail closed for activation; hold classification if required. |
| `MFOS_ERR_INVALID_PARAMETER` | Invalid policy or class definition. | Reject policy draft. |
| `MFOS_ERR_UNSUPPORTED` | Future goal type exists but is not implemented. | Reject policy activation or mark unsupported. |
| `MFOS_ERR_SPEC_GAP` | Behavior not specified. | No success path. |
| `MFOS_ERR_INTERNAL_CORRUPTION` | Active policy state inconsistent. | Hold classification and require operator recovery. |

## 12. Positive Tests

- Activate policy with job class `A`, priority 10, max concurrent 2, default service class `BATCH`.
- Submit job class `A`; `workpolicyd` returns `RUN_NOW` with active policy version.
- Submit third job when two class `A` jobs are running; `workpolicyd` returns `DEFER` or `HOLD` according to overload policy.
- Submit job with report class mapping; accounting record includes report class.
- Operator displays active workload policy through operatord.
- Retire inactive policy version and audit retirement.
- Update policy version and verify new decisions carry incremented version.

## 13. Negative Tests

- Unauthorized operator attempts policy activation; no active policy changes and denial is audited first.
- Policy references unknown service class; validation fails.
- Job submits unknown class without explicit default mapping; classification rejects or holds according to policy.
- Overload action missing; policy validation fails.
- Future `VELOCITY_LIKE` goal used before implementation; returns unsupported.
- Jobd attempts to treat `RUN_LOW_PRIORITY` as security authorization; architecture test fails.
- Auditd unavailable during policy activation; activation fails closed.
- Stale policy version used for dispatch; decision is rejected or recomputed.
- Active policy storage corruption; workpolicyd holds classification and requests operator recovery.

## 14. Fuzz Targets

- `fuzz_wlm_policy_parser`: malformed policy documents, invalid references, unknown goal types.
- `fuzz_job_classification_request`: invalid job class, oversized labels, missing principal, stale version.
- `fuzz_overload_policy`: conflicting limits, zero concurrency, extreme priorities.
- `fuzz_policy_activation`: duplicate versions, replayed activation, concurrent activation requests.
- `fuzz_dispatch_hint_consumer`: invalid hints, missing reason codes, policy mismatch.

Fuzz target requirements:

- Policy parser must not panic.
- Invalid policies must not become active.
- No overload condition may silently return `RUN_NOW`.
- Dispatch decisions must always include policy version and reason code.

## 15. Spec Gaps

- Exact service-class goal algorithms.
- Velocity-like metric definition.
- Response-time goal measurement and feedback loop.
- CPU scheduler integration ABI.
- Memory pressure feedback.
- IO resource accounting.
- Operator workload policy panel details.
- Multi-partition workload policy coordination.
- Policy language syntax and signing model.
- Relationship between workload policy version and global security policy version.

## 16. Inactive Future Implementation Prompt Template

Phase status: inactive future template. This section does not authorize production implementation, hosted daemon implementation, or portable semantic-core implementation.

```text
Future authorized implementation agents would implement MFOS workpolicyd behavior.

Use these spec IDs:
- MFOS-REQ-WPOL-0001 through MFOS-REQ-WPOL-0012

Source Matrix IDs:
- EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001
- EXTREF-IBM-ZOS-JES-INTRODUCTION-0001
- EXTREF-IBM-ZOS-JES-JOB-FLOW-0001
- EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001
- EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001
- EXTREF-IBM-ZOS-SECURITY-SERVER-0001
- EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001

Rules:
- Do not claim z/OS external workload management compatibility.
- workload policy is policy and dispatch hint logic, not security authorization.
- Policy activation must use securityd and auditd.
- Every dispatch decision must include policy_id, policy_version, dispatch_hint, and reason_code.
- Unknown or overloaded conditions must not silently run.
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
