# Phase 1.4 Planning Report

Status date: 2026-05-01
Status: current planning package.

Phase 1.4 is planned only. This report defines the future Job / Spool /
Operator Dafny deepening scope and gates, but it does not implement Phase 1.4
semantics, production code, Rust semantic-core behavior, hosted daemons,
semantic-runner commands, or service implementations.

## Stop-Gate Baseline

The Phase 1.4 planning gate starts from the integrated state recorded by the
post-merge integration sweep:

- Post-merge integration sweep: passed.
- Dafny verification baseline: `136 verified, 0 errors`.
- Coverage overclaim remaining: `false`.
- Architecture overclaim remaining: `false`.
- Production boundary violated: `false`.
- Phase 1.2 Authorization/Audit coverage check: required dependency.
- Phase 1.3 Dataset/Catalog coverage check: required dependency.

Phase 1.4 implementation remains gated. The current Job/Spool and Operator
Console Dafny modules are earlier coarse executable-semantics surfaces; this
planning package does not claim that they satisfy Phase 1.4.

## Scope

Future Phase 1.4 Dafny work is scoped to non-production executable semantics
for:

- Job lifecycle.
- Job effective principal.
- DD resolution.
- DD resolution through Catalog and Authorization.
- Job step execution placeholder.
- Return code model.
- Failure state model.
- `SpoolEntry` as protected resource.
- SYSIN/SYSOUT symbolic model.
- Spool browse, purge, and export authorization.
- Operator command lifecycle.
- Operator command authorization.
- Destructive command confirmation.
- Dual-control command behavior.
- Emergency mode metadata.
- Automation hook non-bypass.
- Submit, cancel, and display flows.
- First vertical slice completion dependencies.

Out of scope for Phase 1.4 planning and still forbidden:

- Production implementation.
- Rust semantic-core or Portable Semantic Core implementation.
- Hosted daemon or hosted semantic prototype implementation.
- `jobd`, `spoold`, `operatord`, `securityd`, `auditd`, `catalogd`,
  `datasetd`, nucleus, PXM, Guard, MFVM, CVM, SGX, or cluster runtime
  implementation.
- A job-control parser, operator parser, target resolver, scheduler, spool
  content store, audit persistence path, or production service call.
- z/OS, JES, JES2, JCL, RACF, SMF, or external command compatibility claims.
- Source-grounding closure for MFOS-native job-control grammar and DD-shaped
  identifiers; planning may record the gap, but semantic implementation must
  not infer external compatibility behavior from it.

## Phase Dependencies

Phase 1.4 must explicitly depend on Phase 1.2 Authorization/Audit:

- Authorization has `C4_VERIFIED_PROPERTY` coverage.
- Audit has `C5_CONFORMANCE_LINKED` coverage.
- Authorization/Audit integration has `C5_CONFORMANCE_LINKED` coverage.
- Audit-unavailable fail-closed behavior is linked to
  `INV_AUDIT_DENY_TRANSITION_FAILS_CLOSED_WHEN_UNAVAILABLE`.
- Formal claims remain not proof-backed.

Phase 1.4 must explicitly depend on Phase 1.3 Dataset/Catalog:

- Dataset/Catalog phase-scope coverage is `C5_CONFORMANCE_LINKED` only over
  required Dataset/Catalog aggregate rows.
- Dataset/Catalog full-domain completion remains false.
- Requirement coverage remains `C2_PARTIAL_SEMANTIC`.
- Authorization/Audit integration coverage is `C4_VERIFIED_PROPERTY`.
- Crash-mid-commit C5 coverage is limited to partial candidate
  non-resolution; full crash recovery selection is not modeled or claimed.

## Required Dafny Properties

The future Phase 1.4 implementation PR must provide explicit verified Dafny
properties for these required rows. Existing coarse symbols may be reused only
if strengthened to meet the stated obligation and linked by the Phase 1.4
coverage generator.

| Required property | Phase 1.4 acceptance rule |
| --- | --- |
| Job effective principal exists before dataset open. | Dataset open cannot succeed unless the job has an established effective principal. |
| DD resolution cannot bypass catalog resolution. | A dataset DD cannot produce a dataset handle unless catalog resolution succeeded through the Phase 1.3 model. |
| DD resolution cannot bypass authorization. | A dataset DD cannot produce a handle unless the Phase 1.2 authorization decision permits the operation. |
| Unauthorized dataset in job step fails. | A job step with an unauthorized dataset DD reaches a fail-closed step/job failure state and creates no dataset handle. |
| Invalid job lifecycle transition is not success. | Any transition outside the modeled valid lifecycle returns a non-success result and no protected side effect. |
| Step completion requires audit correlation where required. | A required audit correlation must exist before a protected step completion is treated as complete. |
| SpoolEntry is protected resource. | Spool entries have protected-resource identity, owner, and class before browse, purge, or export. |
| Spool browse by non-owner is denied. | Non-owner browse cannot return spool content unless future policy explicitly grants authority through authorization. |
| Spool purge without authority is denied. | Purge cannot remove content unless purge authority and retention preconditions are satisfied. |
| Spool export without audit is denied. | Export cannot complete when required export audit evidence is unavailable or missing. |
| Operator command cannot execute without authorization. | Operator commands cannot reach an executing/effect state without an allow decision. |
| Destructive command without confirmation is denied. | Destructive commands that require confirmation cannot execute with unsatisfied confirmation. |
| Dual-control command with single approval is denied. | A dual-control command cannot execute with only one approval. |
| Emergency mode without reason or expiry is denied. | Emergency mode requires both reason and expiry metadata and cannot synthesize authority. |
| Automation hook cannot bypass authorization/audit. | Automation ingress cannot skip parser, target resolution, authorization, obligations, or audit. |
| Root shell is not first privileged UI. | A root shell path cannot be the first privileged interactive UI or successful operator command path. |

## Required Conformance Artifacts

Phase 1.4 C5 rows require fixture, embedded oracle, and golden-vector linkage.
The existing Phase 0.9 fixture/golden corpus may be used as seed material, but
Phase 1.4 must not upgrade coverage unless the future coverage generator links
the exact row to a verified Dafny property and validates the artifact shape.

| Required artifact | Current seed or planned location |
| --- | --- |
| Valid job submit fixture | `tests/fixtures/job/hello-job-0901.yml`; operator submit flow seed `tests/fixtures/oper/submit-job-0904.yml` |
| Job without principal denied fixture | `tests/fixtures/job/submit-no-principal-0903.yml` |
| DD bypass catalog denied fixture | Existing seed `tests/fixtures/job/dd-bypass-denied-0907.yml`; Phase 1.4 must split or annotate catalog-bypass intent before C5 if needed. |
| DD bypass authorization denied fixture | Existing seeds `tests/fixtures/job/dd-bypass-denied-0907.yml` and `tests/fixtures/job/unauthorized-dataset-0908.yml`; Phase 1.4 must keep authorization-bypass and unauthorized-dataset rows distinguishable. |
| Unauthorized dataset in job step fixture | `tests/fixtures/job/unauthorized-dataset-0908.yml` |
| Invalid job lifecycle transition fixture | `tests/fixtures/job/invalid-lifecycle-0910.yml` |
| Spool owner browse allowed fixture | `tests/fixtures/job/spool-browse-owner-0912.yml` |
| Spool non-owner browse denied fixture | `tests/fixtures/job/spool-browse-nonowner-0913.yml` |
| Spool purge unauthorized fixture | `tests/fixtures/job/spool-purge-denied-0914.yml` |
| Spool export without audit fixture | `tests/fixtures/job/spool-export-no-audit-0915.yml` |
| Operator display allowed fixture | `tests/fixtures/oper/display-system-0901.yml` |
| Operator cancel unauthorized fixture | `tests/fixtures/oper/cancel-job-denied-0905.yml` |
| Destructive command without confirmation fixture | `tests/fixtures/oper/destructive-no-confirm-0906.yml` |
| Dual-control single approval denied fixture | `tests/fixtures/oper/dual-control-single-0907.yml` |
| Emergency mode missing reason/expiry fixture | `tests/fixtures/oper/emergency-no-reason-0908.yml` and `tests/fixtures/oper/emergency-no-expiry-0909.yml` |
| Automation hook bypass denied fixture | `tests/fixtures/oper/automation-bypass-0910.yml` |

Each fixture must continue to point at a deterministic golden vector with an
embedded oracle under the corresponding `tests/golden/job/` or
`tests/golden/oper/` path.

## Coverage Rules

Phase 1.4 coverage must use the existing coverage-rank vocabulary without
overclaim:

- `C4_VERIFIED_PROPERTY` requires an explicit Dafny property, verified by the
  pinned Dafny gate, with the exact symbol declared in the target module.
- `C5_CONFORMANCE_LINKED` requires C4 plus fixture, embedded oracle, and golden
  vector links for the row.
- Aggregate C5 requires every required child row in that aggregate to be C5.
- Formal claims without proof artifacts must remain below C4/C5.
- Dafny verification count is supporting evidence, not primary coverage
  evidence.
- A current fixture/golden pair is not enough for C5 unless the Phase 1.4
  generated traceability row links it to the verified Dafny property.

## Planned Validators

The required future Phase 1.4 validator is:

```text
scripts/check-phase1-4-job-spool-operator-coverage.py
```

It is intentionally not added in this planning-only package. It should land
with the real Phase 1.4 generator and generated traceability artifacts so it is
neither a vacuous pass nor an implementation blocker with no artifacts.

The future validator must be structural only. It may check YAML shape, path
existence, exact Dafny symbol declaration, C4/C5 coverage ranks,
fixture/oracle/golden consistency, aggregate rank safety, formal-claim
non-overclaim, and Python non-semantic boundaries. It must not evaluate job
lifecycle, spool ownership, operator authorization, confirmation,
dual-control, emergency, automation, or DD-resolution business semantics in
Python.

The planned generator, if needed, is:

```text
scripts/generators/generate-job-spool-operator-coverage.py
```

The planned generated traceability package is:

```text
evidence/traceability/generated/phase-1-4/
```

No generated Phase 1.4 traceability package is created by this planning PR.

## Deferred Gaps

Deferred to the future Phase 1.4 implementation PR:

- Strengthen or replace the current coarse Job/Spool and Operator Dafny
  predicates with verified properties for all required rows.
- Add deterministic generated traceability and coverage reports.
- Add the Phase 1.4 coverage checker and generator.
- Decide whether DD catalog-bypass and authorization-bypass require split
  fixture names beyond the current Phase 0.9 seeds.
- Resolve or explicitly re-bound the source-grounding risk around MFOS-native
  job-control grammar and DD-shaped identifiers before using those shapes for
  semantic evaluator claims.

Deferred beyond Phase 1.4 unless separately authorized:

- Full job-control parsing.
- Full operator command grammar execution.
- Real spool content browse, purge, or export.
- Program loader and step execution semantics beyond symbolic placeholders.
- Restart, conditional execution, procedures, symbolic parameters,
  concatenation, parallel steps, raw export gateways, and degraded recovery.
- Production services, daemons, semantic runner, or Rust semantic-core.

## Planning Judgment

```yaml
phase_1_4_planning_complete: true
phase_1_4_implementation_started: false
phase_1_4_entry_gate_defined: true
phase_1_4_exit_gate_defined: true
phase_1_4_required_properties_listed: true
phase_1_4_required_conformance_artifacts_listed: true
phase_1_4_validator_planned: true
phase_1_4_validator_scaffolded: false
production_implementation_allowed: false
rust_phase_1_canonical_semantics_allowed: false
hosted_daemon_implementation_allowed: false
recommended_next_action: review and accept the Phase 1.4 planning gate before any non-production Dafny implementation PR
```
