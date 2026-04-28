# MFOS Source Traceability Policy v0.1

Status: design draft

This policy defines how MFOS Source Matrix IDs map to requirement IDs, tests,
and evidence. It applies to the machine-readable ledger in
`docs/design/source-matrix/source-matrix.yml` and the human-readable ledger in
`docs/design/source-matrix/source-matrix.md`.

MFOS is z/OS-inspired. This policy does not permit z/OS compatibility claims.

## Purpose

Traceability exists to stop architecture drift and fake success. Every
source-grounded concept must be connected to requirements, verification, tests,
and evidence before it can support a conformance or production claim.

The policy ensures that:

- Source IDs explain where a concept came from.
- Requirement IDs explain what MFOS must do.
- Test IDs explain how MFOS rejects invalid behavior and accepts valid behavior.
- Evidence IDs explain what artifact proves the work was verified.
- AI agents can work independently without inventing ungrounded semantics.

## Scope

This policy applies to:

- Source IDs in `source-matrix.yml`.
- Requirements in design specs.
- Positive, negative, fuzz, crash-recovery, fault-injection, conformance, and
  supply-chain tests.
- Review checklists, CI checks, formal models, audit evidence, provenance, and
  production readiness records.
- Implementation prompts and AI-generated work summaries.

## Non-objectives

This policy does not:

- Define component behavior by itself.
- Replace component specifications.
- Authorize compatibility claims with IBM, Microsoft, Linux, Intel, AMD, TCG,
  NIST, SLSA, TUF, or seL4 sources.
- Permit requirements without source IDs for z/OS-inspired concepts.
- Permit code or tests to complete `UNSUPPORTED` or `SPEC_GAP` paths; they must fail closed.

## Traceability Chain

The required chain is:

```text
Source ID
  -> Mapping record
  -> Requirement ID
  -> Verification obligation
  -> Test ID or review ID
  -> Evidence artifact
  -> Conformance or production claim
```

No conformance claim may skip a link in this chain.

## Identifier Classes

Source ID:
  A stable ID from `source-matrix.yml`, such as `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001` or `TUF-001`.

Mapping ID:
  A concept mapping ID from a split spec, such as `MFOS-MAP-SI-0001`.

Requirement ID:
  A normative MFOS requirement, such as `MFOS-REQ-SYSINT-0001`.

Verification reference:
  A named verification method or obligation, such as `negative-test`,
  `source-matrix-lint`, `state-machine-test`, `tamper-test`, or
  `supply-chain-audit`.

Test ID:
  A concrete executable or reviewable test. The preferred format is:

```text
TEST-<AREA>-<TYPE>-<NNNN>
```

Examples:

```text
TEST-SI-NEG-0001
TEST-AUD-TAMPER-0001
TEST-UVS-ROLLBACK-0001
TEST-PXM-FAULT-0001
TEST-CAT-CRASH-0001
```

Evidence ID:
  A concrete artifact proving a verification result. The preferred format is:

```text
EVID-<AREA>-<KIND>-<YYYYMMDD>-<NNNN>
```

Examples:

```text
EVID-SI-CI-20260427-0001
EVID-AUD-FUZZ-20260427-0001
EVID-UVS-PROVENANCE-20260427-0001
```

## Requirement Mapping Rules

TRC-REQ-0001:
  Every requirement for a z/OS-inspired concept must reference at least one
  Source Matrix ID.

TRC-REQ-0002:
  Every requirement using an IBM-derived term must reference a mapping record
  that states semantic overlap and MFOS divergence.

TRC-REQ-0003:
  Requirements may cite informative sources only as supporting context. A
  conformance requirement must be grounded by a normative or internal transfer
  source unless an architecture review approves an exception.

TRC-REQ-0004:
  If no source supports a proposed z/OS-like concept, the requirement must be
  marked `SPEC_GAP` and must not be implemented.

TRC-REQ-0005:
  A requirement for a specified but unfinished behavior must define
  `UNSUPPORTED` fail-closed behavior.

TRC-REQ-0006:
  Requirement IDs must be stable. A changed requirement keeps its ID only if the
  obligation is semantically the same; otherwise create a new ID and mark the
  old one superseded.

## Test Mapping Rules

TRC-TEST-0001:
  Every security-sensitive requirement must map to at least one negative test.

TRC-TEST-0002:
  Positive tests are not sufficient for protected-resource behavior. Dataset,
  catalog, spool, job, operator, AMF, update, PXM, and Guard paths require deny
  or failure tests.

TRC-TEST-0003:
  Parser requirements require fuzz targets or a documented reason why fuzzing
  is not applicable.

TRC-TEST-0004:
  State-machine requirements require legal-transition and illegal-transition
  tests.

TRC-TEST-0005:
  Audit requirements require ordering tests where security denial must be
  recorded before the caller receives the result.

TRC-TEST-0006:
  Update requirements require rollback, freeze, mix-and-match, bad signature,
  bad hash, bad size, revoked key, and security epoch downgrade tests.

TRC-TEST-0007:
  PXM requirements require teardown, invalid-state, memory-zeroing, IOMMU, and
  interrupt-remapping tests before production passthrough claims.

TRC-TEST-0008:
  Guard requirements require root mismatch, executable mapping, AMF registry,
  SVC table, unavailable-Guard, and attestation tests.

## Evidence Mapping Rules

TRC-EVID-0001:
  Evidence must be reproducible or reviewable by another agent or maintainer.

TRC-EVID-0002:
  CI output, test logs, fuzz corpus summaries, formal model reports, review
  approvals, SBOMs, signed provenance, attestation reports, and production
  readiness records may be evidence artifacts.

TRC-EVID-0003:
  Evidence must record the source IDs, requirement IDs, test IDs, code or spec
  revision, toolchain version where applicable, date, and result.

TRC-EVID-0004:
  Evidence for a denied operation must show that the protected result was not
  produced and that required audit evidence was produced in the required order.

TRC-EVID-0005:
  Evidence for `UNSUPPORTED` must show fail-closed behavior.

TRC-EVID-0006:
  Evidence for `SPEC_GAP` must show that no implementation path treats the gap
  as success.

## Traceability Record Shape

Use this shape for machine-readable traceability records:

```yaml
trace_id: TRC-<AREA>-<NNNN>
source_ids:
  - EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
mapping_ids:
  - MFOS-MAP-SI-0001
requirement_ids:
  - MFOS-REQ-SYSINT-0001
verification_refs:
  - negative-test
test_ids:
  - TEST-SI-NEG-0001
evidence_ids:
  - EVID-SI-CI-20260427-0001
status: draft | ready | verified | blocked | superseded
gaps:
  - string
```

## AI Work Output Contract

Every AI-generated implementation, test, review, or spec patch must report:

1. Source IDs used.
2. Mapping IDs used or created.
3. Requirement IDs implemented or affected.
4. Tests added or updated.
5. Negative tests added or updated.
6. Evidence artifacts produced.
7. Unsupported features.
8. Spec gaps.
9. Audit obligations.
10. Security invariants.

If any item is not applicable, the output must say why. Empty success summaries
are not acceptable.

## Minimum Gates

Design gate:
  A split spec may be considered reviewable only when every z/OS-inspired
  concept has source IDs, mapping records, allowed wording, prohibited wording,
  and gaps.

Implementation gate:
  A security-sensitive implementation task may start only when requirement IDs,
  source IDs, failure modes, audit obligations, and negative tests are known.

CI gate:
  CI must reject source-grounded production paths with missing requirement IDs,
  missing source IDs, fake success, untracked `UNSUPPORTED`, untracked
  `SPEC_GAP`, or missing negative tests.

Production gate:
  Production claims require verified evidence for all linked requirements,
  source IDs, test IDs, and profile-specific obligations.

High-Assurance gate:
  High-Assurance claims require Guard-root evidence, audit-root evidence,
  update freshness evidence, provenance evidence, and explicit assumptions.

## Review Checklist

- Source IDs exist in `source-matrix.yml`.
- IBM-derived terms have overlap and divergence.
- Allowed wording avoids compatibility claims.
- Prohibited wording is absent from specs, release text, prompts, and comments.
- Requirements link to source IDs and mapping IDs.
- Protected-resource requirements include audit obligations.
- Negative tests exist for authorization boundaries.
- Parser specs include fuzz targets.
- State machines include invalid transition tests.
- Evidence artifacts link back to requirements and source IDs.
- `UNSUPPORTED` and `SPEC_GAP` are distinct.
- PXM does not contain MFOS enterprise semantics.
- Guard is limited to selected High-Assurance root objects.

## Current Gaps

- A dedicated traceability index file does not yet exist.
- No lint tool currently validates `source-matrix.yml` against specs and tests.
- Existing requirement IDs are design-draft references and still need canonical
  registration in per-component specs.
- Test ID and evidence ID registries still need to be created.
- Source freshness and version-pin policy still needs automation.
