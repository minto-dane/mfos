---
spec_id: "MFOS-SPEC-33-SEMANTIC-RUNNER-CONTRACT"
title: "MFOS Semantic Runner Contract v0.1"
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
# MFOS Semantic Runner Contract v0.1

Status: Draft design split

Owner area: `docs/design/specs/33-semantic-runner-contract.md`

Audience: future runner authors, conformance authors, CI authors, release reviewers.

This document defines the contract a future semantic runner must satisfy when one is implemented. It does not implement a runner, evaluator, adapter, CLI, or CI job. The contract exists so artifacts created in Phase 0.9 have a fixed target.

## 1. Purpose

The semantic runner contract defines the boundary between artifacts and execution. A future runner may read test cases, fixtures, and oracles, but it MUST NOT invent missing MFOS behavior or silently treat missing semantics as success.

## 2. Source Matrix References

| Source ID | Use |
| --- | --- |
| `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001` | Runner no-bypass, no-fake-success, and fail-closed result discipline. |
| `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001` | Boundary-negative handling for malformed artifacts and untrusted input. |
| `EXTREF-IBM-ZOS-SECURITY-SERVER-0001` | Protected-resource authorization observation boundaries. |
| `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001` | Audit evidence rejection and audit ordering boundaries. |

## 3. Runner Inputs

A future runner input set MUST contain:

- one conformance suite or one test case,
- the referenced fixture artifacts,
- the referenced oracle artifacts,
- the schema versions used for validation,
- an observation output path,
- an explicit profile claim boundary.

The runner MUST reject any input that is not validated against its declared schema version.

## 4. Runner Non-Authority

A future runner MUST NOT:

- define MFOS semantics,
- repair invalid artifacts,
- fill SPEC_GAP behavior,
- downgrade unsupported behavior into success,
- accept logs as audit evidence,
- use host privileges as fixture authority,
- use wall-clock time unless the fixture declares it as an input,
- access network resources unless represented as fixture objects.

Only specifications and schemas define artifact meaning. The runner executes those definitions.

## 5. Observation Model

The future runner observation model is not implemented in Phase 0.9, but its minimum fields are fixed:

```yaml
observation_kind: semantic_runner_observation
schema_version: 1
runner_id: string
runner_version: string
suite_id: string?
test_id: string
fixture_id: string
oracle_id: string
started_at_utc: string
completed_at_utc: string
outcome: PASS | FAIL | BLOCKED | UNSUPPORTED | SPEC_GAP | INVALID_ARTIFACT
observed_events: []
observed_state_transitions: []
observed_audit_refs: []
observed_failure: {}
artifact_digests: []
```

This is a contract sketch, not a schema in this phase.

## 6. Evaluation Order

A future runner MUST process a test case in this order:

1. Validate all artifacts against declared schemas.
2. Verify naming safety and `EXTREF-*` source refs.
3. Verify that all referenced artifacts are present.
4. Load fixture state as immutable initial state.
5. Apply declared inputs in deterministic order.
6. Record observations without filtering.
7. Evaluate the oracle against observations.
8. Emit an observation result.

If any earlier step fails, later steps MUST NOT be treated as passed.

## 7. Failure Handling

Runner failures are distinct from MFOS expected failures.

| Condition | Runner outcome |
| --- | --- |
| Malformed artifact | `INVALID_ARTIFACT` |
| Missing referenced artifact | `BLOCKED` |
| Unsupported fixture feature | `UNSUPPORTED` |
| Undefined semantic behavior | `SPEC_GAP` |
| Expected MFOS typed failure observed | Determined by oracle |
| Unexpected success on negative case | `FAIL` |

## 8. Deterministic Replay

A future runner MUST make replay possible by recording:

- artifact IDs and digests,
- schema versions,
- declared clock,
- declared security epoch,
- declared policy version,
- input order,
- dependency states,
- runner version,
- observation digest.

The replay contract is a requirement on future evidence. It does not create a runner implementation.

## 9. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| `MFOS-REQ-EXECSPEC-0201` | A semantic runner MUST validate artifacts before execution. | runner review |
| `MFOS-REQ-EXECSPEC-0202` | A semantic runner MUST NOT define or infer missing MFOS semantics. | runner review |
| `MFOS-REQ-EXECSPEC-0203` | A semantic runner MUST reject missing referenced fixtures or oracles as `BLOCKED`. | negative runner test |
| `MFOS-REQ-EXECSPEC-0204` | A semantic runner MUST distinguish runner failure from expected MFOS typed failure. | negative runner test |
| `MFOS-REQ-EXECSPEC-0205` | A semantic runner MUST process inputs in deterministic declared order. | replay test |
| `MFOS-REQ-EXECSPEC-0206` | A semantic runner MUST record artifact digests and schema versions for replay. | evidence review |
| `MFOS-REQ-EXECSPEC-0207` | A semantic runner MUST reject non-audit substitutes for audit evidence. | audit negative test |
| `MFOS-REQ-EXECSPEC-0208` | A semantic runner MUST not use ambient host identity, wall clock, filesystem state, or network state. | isolation review |
| `MFOS-REQ-EXECSPEC-0209` | A semantic runner MUST report `UNSUPPORTED` and `SPEC_GAP` distinctly. | no-fake-success test |
| `MFOS-REQ-EXECSPEC-0210` | A semantic runner result MUST NOT by itself authorize production readiness. | release review |

## 10. Gaps

| Gap ID | Gap | Impact |
| --- | --- | --- |
| `EXECSPEC-GAP-0201` | Runner observation schema is not finalized. | Future runner output remains blocked. |
| `EXECSPEC-GAP-0202` | Runner implementation is intentionally absent. | No executable evaluation exists. |
| `EXECSPEC-GAP-0203` | Replay digest canonicalization tool is not implemented. | Reproducible evidence is design-only. |
