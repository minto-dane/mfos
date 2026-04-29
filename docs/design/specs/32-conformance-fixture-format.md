---
spec_id: "MFOS-SPEC-32-CONFORMANCE-FIXTURE-FORMAT"
title: "MFOS Conformance Fixture Format v0.1"
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
# MFOS Conformance Fixture Format v0.1

Status: Draft design split

Owner area: `docs/design/specs/32-conformance-fixture-format.md`

Audience: conformance authors, schema authors, test engineers, release reviewers.

This document defines the deterministic fixture format used by executable-spec test cases. It does not define a fixture loader, persistence engine, runtime service, or evaluator. The fixture format is an MFOS-authored design artifact and does not claim external product compatibility.

## 1. Purpose

A fixture is the initial semantic world for one or more test cases. It makes preconditions explicit so a future runner does not need to infer subjects, objects, policy versions, audit streams, object generations, or dependency states.

Fixtures exist to prevent:

- ambient host state from changing test meaning,
- missing preconditions from being interpreted as success,
- source-derived semantics from appearing without source refs,
- negative tests from omitting side-effect absence checks.

## 2. Source Matrix References

| Source ID | Use |
| --- | --- |
| `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001` | Fail-closed fixture state and no-bypass preconditions. |
| `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001` | Boundary-negative fixture discipline for untrusted inputs. |
| `EXTREF-IBM-ZOS-SECURITY-SERVER-0001` | Protected-resource subject, object, operation, and policy fixture traceability. |
| `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001` | Audit stream and audit-obligation fixture traceability. |

## 3. Fixture Envelope

Current Phase 0.9 fixtures use this compact deterministic envelope:

```yaml
fixture_id: FIXTURE-MFOS-AREA-NAME-0001
fixture_version: 1
description: Human-readable title
target_specs:
  - docs/design/specs/NN-area.md
target_requirements:
  - MFOS-REQ-AREA-0001
preconditions:
  - All subjects, policy versions, object generations, and dependency states are symbolic and deterministic.
initial_state:
  clock: T0
  security_epoch: 1
  policy_version: 1
  objects: []
inputs:
  - input_id: INPUT-MFOS-PHASE09-0001
    operation: MFOS-DEFINED-OPERATION
    deterministic_seed: SEED-MFOS-PHASE09-0001
expected_oracle: tests/golden/area/name-0001.yml
expected_evidence:
  - EV-MFOS-AREA-NAME-0001
not_allowed:
  - production_claim
  - external_compatibility_claim
  - host_os_semantics_dependency
status: draft
```

The schema for this envelope is `schemas/test-fixture.schema.yml`.

## 4. Deterministic State Model

Fixture state MUST be declarative. A fixture may contain:

- `subjects`
- `objects`
- `policies`
- `audit_streams`
- `state_snapshots`
- `dependency_states`
- `inputs`
- `forbidden_ambient_inputs`

Fixtures MUST NOT contain:

- executable scripts,
- host commands,
- absolute host paths,
- environment variable references,
- network endpoints that are not literal fixture objects,
- dynamic timestamps,
- random value requests.

## 5. Object and Subject References

Fixture references are local to the fixture unless they use a registered MFOS ID. Local refs MUST match:

```text
^REF-[A-Z0-9][A-Z0-9-]*$
```

Rules:

- A local ref MUST be unique within a fixture.
- Any test input that names an object MUST reference an existing fixture object or explicitly expect `MFOS_ERR_SPEC_GAP`.
- Subject authority MUST be represented as fixture data, not as ambient host privilege.
- Object generation and policy version MUST be fixed when used by an oracle.

## 6. Dependency States

Dependencies are design-level semantic dependencies, not live processes. Allowed dependency states:

```text
AVAILABLE
UNAVAILABLE
DEGRADED
UNSUPPORTED
SPEC_GAP
```

A fixture MUST specify the expected behavior for every dependency state that affects test outcome. Missing dependency behavior MUST NOT be inferred as success.

## 7. Inputs

Inputs are ordered declarations of semantic actions. Each input MUST contain:

- `input_id`
- `actor_ref`
- `operation`
- `target_ref` or explicit `target_absent: true`
- `payload`
- `expected_observation_ref`

Input order is declaration order unless the fixture declares an explicit `happens_before` graph. If a `happens_before` graph is present, it MUST be acyclic.

## 8. Canonicalization

Fixture canonicalization rules:

- YAML mappings are interpreted as unordered and serialized for hashing with lexicographic key order.
- Arrays preserve declaration order unless a field explicitly states set semantics.
- Timestamps MUST be UTC date-time strings with `Z`.
- Digest strings MUST identify their algorithm.
- Null values are allowed only where the schema explicitly permits them.

## 9. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| `MFOS-REQ-EXECSPEC-0101` | Fixtures MUST be declarative design artifacts and MUST NOT embed executable fixture setup code. | schema review |
| `MFOS-REQ-EXECSPEC-0102` | Fixtures MUST declare deterministic clock, security epoch, policy version, and ordering mode. | schema validation |
| `MFOS-REQ-EXECSPEC-0103` | Fixtures MUST use `EXTREF-*` source refs only. | naming validation |
| `MFOS-REQ-EXECSPEC-0104` | Fixture subject and object refs MUST be explicit and unique within the fixture. | fixture validation |
| `MFOS-REQ-EXECSPEC-0105` | Fixture dependency states MUST be declared when they affect expected outcome. | fixture review |
| `MFOS-REQ-EXECSPEC-0106` | Inputs MUST be ordered and MUST bind actor, operation, target, and payload. | schema validation |
| `MFOS-REQ-EXECSPEC-0107` | Ambient host state MUST NOT affect fixture meaning. | artifact review |
| `MFOS-REQ-EXECSPEC-0108` | Missing required fixture data MUST block execution rather than produce success. | negative artifact review |
| `MFOS-REQ-EXECSPEC-0109` | Fixture canonicalization MUST be stable across machines. | schema review |
| `MFOS-REQ-EXECSPEC-0110` | Fixture validation MUST NOT imply semantic conformance. | release review |

## 10. Gaps

| Gap ID | Gap | Impact |
| --- | --- | --- |
| `EXECSPEC-GAP-0101` | No fixture loader exists. | Fixtures cannot be executed. |
| `EXECSPEC-GAP-0102` | No canonical digest tool exists. | Fixture hashes remain design-only. |
| `EXECSPEC-GAP-0103` | Fixture migration from Phase 0.8 catalogs is incomplete. | Coverage remains partial. |
