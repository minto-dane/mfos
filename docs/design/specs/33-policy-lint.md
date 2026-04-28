---
spec_id: "MFOS-SPEC-33-POLICY-LINT"
title: "MFOS Policy Lint Specification v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001", "EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001", "NIST-160-001", "NIST-218-001"]
requirement_refs: ["MFOS-REQ-POLICY-LINT-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Policy Lint Specification v0.1

Status: Draft design split

Owned area: `docs/design/specs/33-policy-lint.md`

Audience: architecture agents, security policy authors, implementation agents,
test engineers, reviewers, release reviewers

MFOS is a source-grounded, z/OS-inspired enterprise operating system design.
This specification defines policy lint controls for MFOS policy artifacts. It
does not claim compatibility with z/OS, RACF, IBM APIs, or IBM products.

## 1. Purpose

Policy lint detects policy configurations that are syntactically valid but
semantically dangerous. It complements `securityd`; it does not replace
authorization decisions at runtime.

Policy lint exists to prevent:

- Overbroad default access.
- Wildcard destructive grants.
- AMF authority granted too broadly.
- Emergency authority without expiry.
- Spool export without audit.
- Policy updates without dual-control.
- Silent acceptance of policy patterns that weaken MFOS assurance claims.

## 2. Scope

In scope:

- `SecurityProfile`, `AccessRule`, `AuditRule`, `AuthorityClass`, operator
  emergency policy, spool export policy, AMF authority policy, and policy update
  workflow metadata.
- Policy lint before policy activation.
- Policy lint for production readiness and assurance evidence.
- Negative tests for dangerous but syntactically valid policies.

Out of scope:

- Full policy language grammar.
- External identity provider rules.
- Cryptographic key ceremony.
- Runtime access decisions after an activated policy is accepted.
- Claiming RACF or z/OS policy compatibility.

## 3. Source Matrix References

| Source ID | Policy-lint use |
| --- | --- |
| `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001` | System integrity and unauthorized-circumvention framing. |
| `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001` | Protected-resource profiles, users, groups, access lists, and authorization inspiration. |
| `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001` | Audit/accounting evidence and security event review. |
| `EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001` | AMF/APF-inspired authorized module authority confusion risk. |
| `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001` | Authorized-boundary negative testing discipline. |
| `FBVBS-001` | Requirements, evidence, fail-closed, and production proof discipline. |
| `NIST-160-001`, `NIST-218-001` | Secure system engineering and secure development practice. |

## 4. Normative Language

- `MUST`: required for applicable policy activation.
- `SHOULD`: strongly recommended; deviation requires ADR and evidence.
- `MAY`: optional and not sufficient for an assurance claim.
- `MUST NOT`: prohibited.
- `UNSUPPORTED`: specified but not implemented; fail closed.
- `SPEC_GAP`: undefined; fail closed and do not activate.

## 5. Policy Lint Model

```yaml
PolicyLintInput:
  policy_bundle_id: string
  policy_version: uint64
  target_profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  activation_context:
    requested_by: PrincipalRef
    operator_session_id: string?
    emergency_state: bool
    production_claim: bool
  security_profiles: [SecurityProfile]
  authority_classes: [AuthorityClass]
  audit_rules: [AuditRule]
  workflow_metadata:
    dual_control_required: bool
    approvers: [PrincipalRef]
    approval_records: [string]
    change_ticket: string?
```

```yaml
PolicyLintFinding:
  finding_id: string
  rule_id: POLICY-LINT-001 | POLICY-LINT-002 | POLICY-LINT-003 | POLICY-LINT-004 | POLICY-LINT-005 | POLICY-LINT-006 | POLICY-LINT-007 | POLICY-LINT-008 | POLICY-LINT-009
  severity: BLOCKER | HIGH | MEDIUM | LOW | INFO
  affected_policy_object: ObjectRef
  requirement_ids: [string]
  source_matrix_ids: [string]
  message: string
  required_action: string
  audit_record_type: string
```

```yaml
PolicyLintResult:
  policy_bundle_id: string
  policy_version: uint64
  target_profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  decision: PASS | FAIL | WARN | SPEC_GAP | UNSUPPORTED
  findings: [PolicyLintFinding]
  audit_correlation_id: CorrelationId
  evidence_artifact: string
```

Rules:

- Policy lint MUST run before policy activation in production profiles.
- A `BLOCKER` finding MUST prevent policy activation.
- `SPEC_GAP` policy syntax or semantics MUST prevent policy activation.
- `UNSUPPORTED` policy lint behavior MUST prevent policy activation when the
  unsupported lint rule is required for the target profile.
- Policy lint findings MUST be auditable.
- Passing policy lint is not an authorization decision for runtime access.

## 6. Lint Rules

### POLICY-LINT-001: Overly Broad Default Access

Requirement:

```text
POLICY-LINT-001:
  A protected resource profile MUST NOT use broad default access for
  production activation unless the profile is explicitly marked public,
  read-only, non-sensitive, and audited.
```

Detection examples:

- `default_decision: ALLOW_READ_ONLY` on sensitive dataset classes.
- Default access for `CATALOG`, `AUDIT_STREAM`, `AMF_MODULE`, `SECURITY_POLICY`,
  `UPDATE_ARTIFACT`, `GUARD_ROOT`, `PARTITION`, or `DEVICE`.
- Default allow without audit obligation.

Required finding:

```yaml
severity: BLOCKER
required_action: "Set default decision to DENY or provide an approved public read-only exception with audit."
audit_record_type: POLICY_LINT_BROAD_DEFAULT_ACCESS
```

### POLICY-LINT-002: Wildcard Destructive Grants

Requirement:

```text
POLICY-LINT-002:
  Policy MUST NOT grant wildcard destructive or administrative operations over
  dataset, catalog, spool, device, partition, update, Guard root, security
  policy, workload policy, service, system, or audit-stream resources without
  dual-control, bounded scope, explicit owner or steward evidence, and audit.
```

Detection examples:

- `DSN=*` with `DELETE`, `PURGE`, `UPDATE`, `ADMINISTER`, or equivalent.
- `USER.*` destructive grant to broad group or role.
- System dataset wildcard with any write-like operation.
- `SPOOL * PURGE`, `AUDIT_STREAM * ADMINISTER`, `DEVICE * ASSIGN`,
  `PARTITION * ADMINISTER`, `SYSTEM * ADMINISTER`, or equivalent broad grants.

Required finding:

```yaml
severity: BLOCKER
required_action: "Narrow resource scope or add dual-control, owner/steward approval, and audit evidence."
audit_record_type: POLICY_LINT_WILDCARD_DATASET_ALTER
```

### POLICY-LINT-003: AMF Authority Granted to Broad Role

Requirement:

```text
POLICY-LINT-003:
  AMF authority MUST NOT be granted to broad roles, default groups, automation
  roles, or emergency roles unless the AMF profile explicitly permits it and
  production AMF loading is enabled for the active conformance profile.
```

Detection examples:

- `AMF_MODULE LOAD` granted to `ROL-ADMIN`, `GRP-USERS`, wildcard group, or
  automation principal.
- AMF authority in Baseline production profile when AMF load is specified as
  unsupported.
- AMF authority without revocation, immutable source, and audit obligation.

Required finding:

```yaml
severity: BLOCKER
required_action: "Restrict AMF authority to explicit module-governance role or keep AMF load unsupported."
audit_record_type: POLICY_LINT_BROAD_AMF_AUTHORITY
```

### POLICY-LINT-004: Operator Emergency Role Without Expiry

Requirement:

```text
POLICY-LINT-004:
  Emergency or break-glass operator authority MUST have expiry, reason,
  audit, and incident-review obligations.
```

Detection examples:

- `break_glass_allowed: true` without `emergency_expiry`.
- Emergency role with no reason requirement.
- Emergency role can update policy or purge audit without dual-control.

Required finding:

```yaml
severity: BLOCKER
required_action: "Add expiry, reason requirement, audit obligation, and incident review workflow."
audit_record_type: POLICY_LINT_EMERGENCY_NO_EXPIRY
```

### POLICY-LINT-005: Export Allowed Without Audit And Redaction

Requirement:

```text
POLICY-LINT-005:
  Spool export, sensitive spool browse, audit export, authorization evidence
  export, and gateway export MUST require audit, redaction policy, and bounded
  recipient scope.
```

Detection examples:

- `SPOOL EXPORT` allowed without an `AuditRule`.
- Export allowed to side partition without redaction policy.
- SYSOUT export allowed for broad group without owner or job submitter binding.
- `AUDIT_STREAM EXPORT` or `AUTHORIZATION_EVIDENCE EXPORT` allowed without
  redaction policy and audit obligation.

Required finding:

```yaml
severity: BLOCKER
required_action: "Add audit and redaction policy, or deny export."
audit_record_type: POLICY_LINT_SPOOL_EXPORT_NO_AUDIT
```

### POLICY-LINT-006: Policy Update Without Dual-Control

Requirement:

```text
POLICY-LINT-006:
  Production policy activation that changes authorization, audit, AMF,
  emergency, update, Guard, or partition authority MUST require dual-control.
```

Detection examples:

- Security profile update has one approver.
- Audit weakening or redaction weakening lacks independent approval.
- Policy update changes AMF or Guard authority without dual-control.
- Emergency role grant is self-approved.

Required finding:

```yaml
severity: BLOCKER
required_action: "Require independent dual-control approval before activation."
audit_record_type: POLICY_LINT_POLICY_UPDATE_NO_DUAL_CONTROL
```

### POLICY-LINT-007: Broad Audit Query Access

Requirement:

```text
POLICY-LINT-007:
  Audit query authority MUST NOT be granted broadly. Audit queries require
  explicit role scope, target stream scope, redaction policy, and audit of the
  query itself.
```

Detection examples:

- `AUDIT_STREAM QUERY` granted to default, broad operator, automation, or
  emergency roles without target stream restrictions.
- Query can return security decision records without redaction policy.
- Query access omits audit obligation for the query event.

Required finding:

```yaml
severity: BLOCKER
required_action: "Narrow audit query authority and add redaction plus query audit."
audit_record_type: POLICY_LINT_BROAD_AUDIT_QUERY
```

### POLICY-LINT-008: Stale Delegation Without Expiry

Requirement:

```text
POLICY-LINT-008:
  Delegated authority MUST include expiry, delegator/delegatee identity,
  bounded resource scope, audit, and revocation evidence.
```

Detection examples:

- Delegation has no expiry or survives policy epoch change.
- Delegation grants destructive authority without dual-control.
- Delegation chain depth exceeds the target profile limit.

Required finding:

```yaml
severity: BLOCKER
required_action: "Add expiry, bounded scope, revocation path, and audit to delegated authority."
audit_record_type: POLICY_LINT_STALE_DELEGATION
```

### POLICY-LINT-009: Rollback Or Audit Weakening

Requirement:

```text
POLICY-LINT-009:
  Policy rollback or activation MUST NOT lower security epoch, weaken mandatory
  audit, weaken deny-before-return ordering, or remove required redaction
  without explicit reviewed recovery policy and dual-control.
```

Detection examples:

- Rollback target lowers security epoch.
- Proposed policy removes required audit obligations for deny paths.
- Proposed policy weakens redaction or evidence export controls.

Required finding:

```yaml
severity: BLOCKER
required_action: "Reject rollback or activation unless reviewed recovery policy preserves or strengthens audit/security posture."
audit_record_type: POLICY_LINT_ROLLBACK_WEAKENS_SECURITY
```

## 7. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| `MFOS-REQ-POLICY-LINT-0001` | Policy lint MUST run before production policy activation. | integration test |
| `MFOS-REQ-POLICY-LINT-0002` | `BLOCKER` findings MUST prevent activation. | negative test |
| `MFOS-REQ-POLICY-LINT-0003` | Policy lint findings MUST be auditable. | audit test |
| `MFOS-REQ-POLICY-LINT-0004` | Policy lint MUST include `POLICY-LINT-001` through `POLICY-LINT-009`. | conformance review |
| `MFOS-REQ-POLICY-LINT-0005` | Passing policy lint MUST NOT be treated as a runtime authorization decision. | architecture review |
| `MFOS-REQ-POLICY-LINT-0006` | Policy lint output MUST include finding severity, affected object, requirement IDs, source matrix IDs, required action, and audit record type. | schema test |

## 8. Audit Obligations

| Event | Required audit record |
| --- | --- |
| Policy lint run starts | `POLICY_LINT_START` |
| Policy lint pass | `POLICY_LINT_PASS` |
| Policy lint warning | `POLICY_LINT_WARN` |
| Policy lint blocker | `POLICY_LINT_BLOCKER` |
| Policy activation denied by lint | `POLICY_ACTIVATION_DENY_LINT` |
| Policy lint unsupported or spec gap | `POLICY_LINT_FAIL_CLOSED` |

Rules:

- A policy activation denied by lint MUST be audited before the activation caller
  receives the final denial.
- Audit weakening findings MUST be audited using the currently active audit
  policy, not the proposed weakened policy.

## 9. Failure Modes

| Failure | Required behavior |
| --- | --- |
| Lint engine unavailable for production activation | Return `MFOS_ERR_UNSUPPORTED` or profile-specific policy activation denial. |
| Policy syntax undefined | Return `MFOS_ERR_SPEC_GAP`; do not activate. |
| Required policy object missing | Deny activation. |
| Audit required but unavailable | Return `MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE`; do not activate. |
| Finding severity BLOCKER | Deny activation. |
| Finding severity WARN | Activation MAY proceed only if target profile allows warning acceptance with audit. |

## 10. Positive Tests

| Test ID | Description |
| --- | --- |
| `POLICY-LINT-POS-001` | Narrow dataset read policy with deny default passes lint. |
| `POLICY-LINT-POS-002` | Spool export policy with explicit audit and redaction passes lint. |
| `POLICY-LINT-POS-003` | Emergency role with expiry, reason, audit, and incident review passes lint. |
| `POLICY-LINT-POS-004` | Production policy update with two independent approvers passes lint. |

## 11. Negative Tests

| Test ID | Description |
| --- | --- |
| `POLICY-LINT-NEG-001` | Broad default access on protected dataset profile fails with `POLICY-LINT-001`. |
| `POLICY-LINT-NEG-002` | Wildcard dataset destructive grant fails with `POLICY-LINT-002`. |
| `POLICY-LINT-NEG-003` | AMF load authority granted to broad role fails with `POLICY-LINT-003`. |
| `POLICY-LINT-NEG-004` | Emergency role without expiry fails with `POLICY-LINT-004`. |
| `POLICY-LINT-NEG-005` | Spool export without audit fails with `POLICY-LINT-005`. |
| `POLICY-LINT-NEG-006` | Production policy update without dual-control fails with `POLICY-LINT-006`. |
| `POLICY-LINT-NEG-007` | Broad audit query access without stream scope, redaction, and query audit fails with `POLICY-LINT-007`. |
| `POLICY-LINT-NEG-008` | Delegated authority without expiry or revocation evidence fails with `POLICY-LINT-008`. |
| `POLICY-LINT-NEG-009` | Proposed rollback weakens audit and tries to use weakened audit policy for lint evidence; activation fails with `POLICY-LINT-009`. |

## 12. Fuzz Targets

| Fuzz ID | Target | Required property |
| --- | --- | --- |
| `POLICY-LINT-FUZZ-001` | SecurityProfile parser and lint input canonicalizer. | Malformed or ambiguous policy cannot activate. |
| `POLICY-LINT-FUZZ-002` | AccessRule condition parser. | Wildcards and duplicate rules are canonicalized before lint. |
| `POLICY-LINT-FUZZ-003` | AuditRule parser. | Missing audit obligations cannot be hidden by malformed fields. |
| `POLICY-LINT-FUZZ-004` | Workflow metadata parser. | Self-approval and duplicate approvers cannot satisfy dual-control. |

## 13. Evidence Artifacts

Policy lint evidence MUST include:

- Policy bundle ID and policy version.
- Target profile.
- Lint rule version.
- PASS/FAIL/WARN decision.
- Findings with `POLICY-LINT-*` IDs.
- Audit correlation ID.
- Activation decision.
- Review or ADR for accepted warnings.

## 14. Spec Gaps

| Gap ID | Gap |
| --- | --- |
| `POLICY-LINT-GAP-001` | Concrete security policy grammar is not fixed. |
| `POLICY-LINT-GAP-002` | Machine-readable policy lint schema is not registered in the central registry yet. |
| `POLICY-LINT-GAP-003` | Exact sensitive dataset class taxonomy is not fixed. |
| `POLICY-LINT-GAP-004` | Warning acceptance workflow is not fixed for every profile. |
| `POLICY-LINT-GAP-005` | Full policy-diff algorithm is not specified. |

## 15. Inactive Future Implementation Prompt Template

Phase status: inactive future template. This section does not authorize production implementation, hosted daemon implementation, or portable semantic-core implementation.

```text
Future authorized agents would implement or review MFOS policy lint.

Rules:
- Do not claim compatibility with z/OS, RACF, IBM APIs, or IBM products.
- Implement POLICY-LINT-001 through POLICY-LINT-006.
- A BLOCKER finding prevents policy activation.
- Passing policy lint is not a runtime authorization decision.
- Findings must include requirement IDs, source matrix IDs, severity,
  affected object, required action, and audit record type.
- Audit policy weakening must be audited under the currently active policy.
- Undefined policy behavior returns SPEC_GAP.
- Specified but unimplemented lint behavior returns UNSUPPORTED.
- Add positive tests, negative tests, and fuzz targets.

Required output:
1. Implemented Requirement IDs
2. Source Matrix IDs
3. Policy Lint Rule IDs
4. Assumptions
5. Spec Gaps
6. Unsupported Features
7. Audit Obligations
8. Failure Modes
9. Tests Added
10. Negative Tests Added
11. Fuzz Targets Added
12. Evidence Artifacts
```
