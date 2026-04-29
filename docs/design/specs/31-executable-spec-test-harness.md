---
spec_id: "MFOS-SPEC-31-EXECUTABLE-SPEC-TEST-HARNESS"
title: "MFOS Executable-Spec Test Harness Artifact Contract v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-28"
source_refs: ["EXTREF-DAFNY-REFERENCE-0001", "EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001"]
requirement_refs: ["MFOS-REQ-DAFNY-*", "MFOS-REQ-EXECSPEC-*"]
claim_refs: []
test_refs: ["TEST-MFOS-EXECSPEC-CONF-*", "NEG-MFOS-EXECSPEC-CONF-*"]
evidence_refs: ["EV-MFOS-EXECSPEC-*"]
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Executable-Spec Test Harness Artifact Contract v0.1

Status: Draft design split

Owner area: `docs/design/specs/31-executable-spec-test-harness.md`

Audience: test architects, conformance authors, schema authors, release reviewers, implementation agents.

This document defines the deterministic artifact contract for executable-spec tests. It does not implement a production runner, service adapter, hosted daemon, or production test harness. Phase 1 executable-semantics authority is non-production Dafny source plus fixture/oracle/golden conformance checks under `docs/design/specs/43-dafny-executable-semantics-policy.md`; this contract does not authorize Rust semantic-core work, future semantic-runner command implementation, hosted daemons, or production generated code. MFOS is source-grounded and z/OS-inspired; these artifacts do not claim external product compatibility or external API compatibility.

## 1. Purpose

The executable-spec test harness artifacts make design-level tests precise enough that a future runner can consume them without inventing behavior. A test case must declare:

- the requirement IDs it verifies,
- the external source references that ground source-derived behavior,
- the fixture that provides the initial semantic world,
- the oracle that defines expected outcome, audit, state, and failure obligations,
- deterministic execution constraints,
- unsupported and SPEC_GAP behavior.

The contract freezes artifact shape only. A passing artifact validation is not a passing product test.

## 2. Scope

In scope:

- Test case document shape.
- Suite manifest document shape.
- Fixture and oracle reference rules.
- Determinism requirements.
- Naming-safety requirements.
- Result vocabulary for future evidence reports.
- Validation boundaries for draft executable-spec artifacts.

Out of scope:

- Runner implementation.
- Semantic evaluator implementation.
- Runtime service adapters.
- CI job definitions.
- Production evidence collection.
- Automatic migration from Phase 0.8 planned catalogs.

## 3. Source Matrix References

| Source ID | Use |
| --- | --- |
| `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001` | Fail-closed and no-bypass semantics for protected operations. |
| `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001` | Boundary-negative test discipline and untrusted-input handling. |
| `EXTREF-IBM-ZOS-SECURITY-SERVER-0001` | Protected-resource authorization traceability. |
| `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001` | Audit evidence and ordering traceability. |
| `EXTREF-DAFNY-REFERENCE-0001` | Phase 1 executable-semantics artifact language background. |

All `source_refs` in executable-spec artifacts MUST use `EXTREF-*` IDs. MFOS-owned identifiers MUST NOT include external product names or abbreviations.

## 4. Artifact Set

The Phase 0.9 executable-spec artifact set is:

| Artifact | Schema | Purpose |
| --- | --- | --- |
| Test case | `schemas/test-case.schema.yml` | Names one deterministic test and links fixture, oracle, requirements, sources, and evidence expectations. |
| Test fixture | `schemas/test-fixture.schema.yml` | Defines the initial world and deterministic inputs. |
| Oracle | `schemas/oracle.schema.yml` | Defines expected outcome, audit, state, and failure obligations. |
| Expected audit | `schemas/expected-audit.schema.yml` | Defines required audit records, ordering, and rejected evidence substitutes. |
| Expected state transition | `schemas/expected-state-transition.schema.yml` | Defines allowed state movement and forbidden side effects. |
| Expected failure | `schemas/expected-failure.schema.yml` | Defines typed failure results and fail-closed side-effect rules. |
| Conformance suite | `schemas/conformance-suite.schema.yml` | Groups test cases for a profile or release claim. |

Each schema is design-only. Schema validation confirms artifact shape, not semantic correctness.

## 5. Canonical ID Families

| ID kind | Pattern |
| --- | --- |
| Requirement ID | `^MFOS-REQ-[A-Z0-9]+-[0-9]{4}$` |
| Test ID | `^(TEST|NEG)-MFOS-[A-Z0-9]+-[A-Z0-9-]*[0-9]{4}$` |
| Fixture ID | `^FIXTURE-MFOS-[A-Z0-9]+-[A-Z0-9-]*[0-9]{4}$` |
| Oracle ID | `^ORACLE-MFOS-[A-Z0-9]+-[A-Z0-9-]*[0-9]{4}$` |
| Expected audit ID | `^EXP-MFOS-AUDIT-[A-Z0-9-]*[0-9]{4}$` |
| Expected state ID | `^EXP-MFOS-STATE-[A-Z0-9-]*[0-9]{4}$` |
| Expected failure ID | `^EXP-MFOS-FAIL-[A-Z0-9-]*[0-9]{4}$` |
| Suite ID | `^SUITE-MFOS-[A-Z0-9]+-[A-Z0-9-]*[0-9]{4}$` |
| Evidence ID | `^EV-MFOS-[A-Z0-9]+-[A-Z0-9-]*[0-9]{4}$` |
| Source ref | `^EXTREF-[A-Z0-9-]+-[0-9]{4}$` |

ID rules:

- MFOS-owned identifiers MUST NOT contain external product tokens.
- Legacy IDs MAY appear only in `legacy_ids` arrays.
- Requirement references MUST be concrete before a release claim; wildcard requirement refs are draft-only metadata.
- Source references MUST resolve to the Source Matrix.

## 6. Test Case Semantics

A test case MUST be deterministic and declarative. It MUST NOT contain executable code, host commands, dynamic expressions, inline scripts, or evaluator plugins.

Required test-case fields:

- `artifact_kind: test_case`
- `schema_version: 1`
- `test_id`
- `title`
- `status`
- `test_type`
- `owning_spec`
- `requirement_ids`
- `source_refs`
- `fixture_ref`
- `oracle_ref`
- `determinism`
- `expected_evidence`

Test types:

```text
unit
integration
negative
fuzz
conformance
crash_recovery
fault_injection
supply_chain
formal_model
release_gate
```

`fuzz` test cases in Phase 0.9 may declare seed and corpus obligations, but they MUST NOT require a campaign runner to exist.

## 7. Determinism Rules

Every executable-spec artifact MUST define or inherit:

- fixed `clock_utc`,
- fixed `security_epoch`,
- fixed policy version where policy affects behavior,
- deterministic actor identities,
- deterministic object generations,
- deterministic input sequence,
- canonical ordering for maps and emitted observations,
- explicit handling for unavailable dependencies,
- no host filesystem dependency outside declared artifact refs,
- no network dependency,
- no randomness unless a literal seed is declared.

Future runners MUST reject artifacts that depend on wall clock time, ambient environment variables, host user identity, network access, or unspecified ordering.

## 8. Outcome Vocabulary

Test case evaluation, when a future runner exists, MUST use this vocabulary:

| Outcome | Meaning |
| --- | --- |
| `PASS` | All oracle obligations are satisfied. |
| `FAIL` | At least one oracle obligation is violated. |
| `BLOCKED` | Required fixture, schema, or prerequisite is unavailable. |
| `UNSUPPORTED` | The behavior is specified as unsupported and failed closed as expected. |
| `SPEC_GAP` | The behavior is unspecified and failed closed as expected. |
| `INVALID_ARTIFACT` | The artifact is malformed or violates this contract. |

`UNSUPPORTED` and `SPEC_GAP` are not success for the underlying feature. They may satisfy a negative test only when the oracle explicitly expects that fail-closed result.

## 9. Evidence Boundary

Accepted future evidence:

- schema validation report for the test case, fixture, and oracle,
- runner observation document when a runner exists,
- audit record references accepted by the audit service,
- state snapshot digests produced from canonical fixture state,
- conformance suite result manifest.

Rejected evidence:

- diagnostic log lines,
- console output,
- spool output,
- screenshots,
- unverified remote acknowledgments,
- human notes without linked artifact IDs.

## 10. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| `MFOS-REQ-EXECSPEC-0001` | Executable-spec test cases MUST be declarative artifacts and MUST NOT embed runner code or evaluator code. | schema review |
| `MFOS-REQ-EXECSPEC-0002` | Every test case MUST list at least one concrete `MFOS-REQ-*` requirement ID. | schema validation |
| `MFOS-REQ-EXECSPEC-0003` | Every source-grounded test case MUST list `EXTREF-*` source refs only. | naming safety validation |
| `MFOS-REQ-EXECSPEC-0004` | Every test case MUST link exactly one fixture and exactly one oracle. | schema validation |
| `MFOS-REQ-EXECSPEC-0005` | Every fixture, oracle, and test case MUST declare deterministic clock, epoch, ordering, and environment constraints. | artifact review |
| `MFOS-REQ-EXECSPEC-0006` | `UNSUPPORTED` and `SPEC_GAP` expectations MUST be explicit and fail closed. | negative artifact review |
| `MFOS-REQ-EXECSPEC-0007` | Audit-sensitive test cases MUST link expected audit obligations and reject non-audit substitutes. | oracle review |
| `MFOS-REQ-EXECSPEC-0008` | State-changing test cases MUST define expected state transitions and forbidden side effects. | oracle review |
| `MFOS-REQ-EXECSPEC-0009` | Conformance suites MUST state the claimed profile and the requirement coverage boundary. | suite review |
| `MFOS-REQ-EXECSPEC-0010` | Artifact validation MUST NOT be represented as runtime conformance or production readiness. | release review |

## 11. Gaps

| Gap ID | Gap | Impact |
| --- | --- | --- |
| `EXECSPEC-GAP-0001` | Runner implementation is intentionally absent. | Blocks actual execution and result evidence. |
| `EXECSPEC-GAP-0002` | Semantic evaluator implementation is intentionally absent. | Blocks automated oracle evaluation. |
| `EXECSPEC-GAP-0003` | Phase 0.8 planned catalogs are not migrated into this artifact format. | Blocks full suite coverage. |
| `EXECSPEC-GAP-0004` | Canonical observation report schema is not defined in this phase. | Blocks final evidence archival. |
