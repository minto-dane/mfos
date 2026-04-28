---
spec_id: "MFOS-SPEC-34-ORACLE-DEFINITION-FORMAT"
title: "MFOS Oracle Definition Format v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-28"
source_refs: ["EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001"]
requirement_refs: ["MFOS-REQ-EXECSPEC-*"]
claim_refs: []
test_refs: ["TEST-MFOS-EXECSPEC-CONF-*", "NEG-MFOS-EXECSPEC-CONF-*"]
evidence_refs: ["EV-MFOS-EXECSPEC-*"]
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Oracle Definition Format v0.1

Status: Draft design split

Owner area: `docs/design/specs/34-oracle-definition-format.md`

Audience: oracle authors, conformance authors, schema authors, release reviewers.

This document defines the declarative oracle format for executable-spec artifacts. It does not implement oracle evaluation or semantic interpretation.

## 1. Purpose

An oracle states what must be observed for a test case to pass, fail, block, or satisfy a fail-closed negative expectation. Oracles make absence checks first-class so a future runner cannot treat partial success as full success.

## 2. Source Matrix References

| Source ID | Use |
| --- | --- |
| `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001` | Oracle rules for no-bypass and fail-closed expected results. |
| `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001` | Negative oracle obligations for malformed or untrusted inputs. |
| `EXTREF-IBM-ZOS-SECURITY-SERVER-0001` | Protected-resource authorization expectation boundaries. |
| `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001` | Audit evidence and ordering expectation boundaries. |

## 3. Oracle Envelope

Every oracle MUST use this envelope:

```yaml
artifact_kind: oracle
schema_version: 1
oracle_id: ORACLE-MFOS-AREA-NAME-0001
status: draft
oracle_kind: composite
requirement_ids:
  - MFOS-REQ-AREA-0001
source_refs:
  - EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
expected_outcome: PASS
evaluation_order:
  - outcome
  - audit
  - state
  - failure
expected_audit_refs: []
expected_state_transition_refs: []
expected_failure_ref: null
side_effect_absence: []
```

The schema for the envelope is `schemas/oracle.schema.yml`.

## 4. Oracle Kinds

Allowed oracle kinds:

```text
outcome_only
audit_ordering
state_transition
failure_semantics
conformance_matrix
composite
```

`outcome_only` is allowed only for tests whose requirements do not affect protected resources, state transitions, audit, or failure semantics.

## 5. Audit Expectations

Audit expectations MUST declare:

- required record classes,
- required ordering relative to caller-visible result,
- required correlation binding,
- rejected evidence substitutes,
- required absence of audit gaps.

The schema is `schemas/expected-audit.schema.yml`.

## 6. State Expectations

State expectations MUST declare:

- target state scope,
- pre-state selector,
- action selector,
- post-state selector,
- invariants,
- forbidden transitions,
- side-effect absence.

The schema is `schemas/expected-state-transition.schema.yml`.

## 7. Failure Expectations

Failure expectations MUST declare:

- expected error code,
- fail-closed classification,
- caller-visible result,
- required audit before result when applicable,
- state and side-effect absence.

The schema is `schemas/expected-failure.schema.yml`.

## 8. Pass and Fail Rules

An oracle passes only when every required expectation is satisfied. It fails when:

- a required audit record is absent,
- audit ordering is violated,
- forbidden state appears,
- expected failure returns success,
- expected success returns a typed failure,
- an unsupported or SPEC_GAP path is reported as success,
- a rejected evidence substitute is used,
- a side-effect absence assertion is violated.

## 9. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| `MFOS-REQ-EXECSPEC-0301` | Oracles MUST be declarative artifacts and MUST NOT embed evaluator code. | schema review |
| `MFOS-REQ-EXECSPEC-0302` | Oracles MUST list concrete requirement IDs and `EXTREF-*` source refs. | schema validation |
| `MFOS-REQ-EXECSPEC-0303` | Oracles for audit-sensitive tests MUST link expected audit definitions. | oracle review |
| `MFOS-REQ-EXECSPEC-0304` | Oracles for state-changing tests MUST link expected state transition definitions. | oracle review |
| `MFOS-REQ-EXECSPEC-0305` | Negative or fail-closed tests MUST link expected failure definitions. | oracle review |
| `MFOS-REQ-EXECSPEC-0306` | Oracles MUST treat missing required evidence as failure or blocked, not pass. | no-fake-success review |
| `MFOS-REQ-EXECSPEC-0307` | Oracles MUST reject logs, console output, and spool output as audit evidence. | audit review |
| `MFOS-REQ-EXECSPEC-0308` | Oracles MUST include side-effect absence assertions for security-sensitive negative tests. | negative review |
| `MFOS-REQ-EXECSPEC-0309` | Oracle validation MUST NOT imply implementation conformance. | release review |

## 10. Gaps

| Gap ID | Gap | Impact |
| --- | --- | --- |
| `EXECSPEC-GAP-0301` | Oracle evaluator is intentionally absent. | Oracles cannot be automatically evaluated. |
| `EXECSPEC-GAP-0302` | Observation schema is not finalized. | Full oracle-to-observation binding is deferred. |
| `EXECSPEC-GAP-0303` | Legacy planned tests are not mapped to oracle artifacts. | Coverage remains incomplete. |
