# PR 29 Phase 1.4.1 Review

Status: remediation complete; CodeRabbit re-review pending.

This review covers PR #29, `phase 1.4.1: bind job DD authorization
semantics`, after the Phase 1.4.1 evidence-package remediation. Scope reviewed:
Job lifecycle, effective principal, DD resolution, binding witnesses, coverage
traceability, validation quality, CodeRabbit advisory comments, and production
boundary preservation.

## Validation

Local validation passed after remediation:

```yaml
validate_all_check: passed
validate_naming_safety_release: passed
validate_artifact_hygiene_before_py_compile: passed
validate_component_scaffold: passed
validate_language_formal_assurance: passed
validate_dafny_semantics_require_dafny: passed
dafny_verification_result: "184 verified, 0 errors"
semantic_coverage_mapping: passed
formal_claim_coverage: passed
phase1_gap_triage: passed
phase1_2_auth_audit_coverage: passed
phase1_3_dataset_catalog_coverage: passed
phase1_4_1_job_dd_coverage_root_wrapper: passed
phase1_4_1_job_dd_coverage_canonical: passed
python_py_compile: passed
pycache_removed_after_compile: true
validate_artifact_hygiene_after_pycache_cleanup: passed
git_diff_check: passed
```

## Binding Review

- `BoundDDDecision` remains the DD resolution input surface.
  `ResolveDDForJob` takes `BoundDDDecision`, not a raw `SecurityDecision`.
- `IsBoundDDDecision` binds effective principal subject, DD object, operation,
  policy version, decision context policy version, request correlation id, and
  effective-principal correlation id.
- `BoundDDDecisionMatchesEntry` binds the decision object generation to the
  catalog entry generation.
- Cross-request replay remains blocked by
  `INV_JOB_DD_CROSS_REQUEST_AUTHORIZATION_REPLAY_BLOCKED`.
- `EffectiveJobContext` remains required by `BoundDDDecisionValid`; DD
  resolution cannot reach the handle creation path without an established
  effective principal.
- `ValidDenyDecision` still requires a non-success error code, and
  `INV_JOB_DD_DENY_MFOS_OK_INVALID` rejects `DENY` plus `MFOS_OK`.
- `INV_JOB_DD_DENY_PRODUCES_NO_HANDLE` verifies that a DENY decision makes
  `ResolveDDForJob` return an error.
- `job_spool.dfy` delegates handle creation, authorization effect checks,
  catalog placement, and audit-linked denial behavior to existing
  `DatasetCatalog`, `Authorization`, and Audit-linked helpers.

## Remediated Findings

### Cancelled-job error code

Resolved. `tests/golden/job/cancelled-cannot-execute-0926.yml` now uses the
modeled Dafny error code `MFOS_ERR_INVALID_STATE` for the audit reason,
transition reason, expected failure mode, and embedded oracle failure.

### Cancelled-job state space

Resolved. `tests/fixtures/job/cancelled-cannot-execute-0926.yml` now keeps the
attempted transition in JobState space: `JOB_CANCELLED -> JOB_EXECUTING`.
The golden final state and transition state use `JOB_CANCELLED`.

### Valid-submit transition sequence

Resolved. `tests/golden/job/valid-submit-ready-0928.yml` now records the two
atomic Dafny transitions:

- `JOB_SUBMITTED -> JOB_VALIDATED`;
- `JOB_VALIDATED -> JOB_READY`.

The fixture lifecycle path and golden/oracle final state use the same Dafny
constructor names.

### Broad requirement overclaim

Resolved locally. Generated parent requirement rows for `MFOS-REQ-JOB-0101`,
`MFOS-REQ-JOB-0102`, and `MFOS-REQ-JOB-0103` now remain
`C2_PARTIAL_SEMANTIC` with explicit `not_claimed` fields for service
provenance, program/spool/other protected-resource opens, and production
`jobd` behavior outside Phase 1.4.1. Phase-scoped subclaim rows carry
`C4_VERIFIED_PROPERTY` only where an explicit Dafny property is verified.

The Phase 1.4.1 coverage validator now rejects broad parent requirement rows
that claim C4/C5/C6 without `full_requirement_modeled: true`.

### CodeRabbit comments

The confirmed Critical/Major CodeRabbit findings are addressed locally:

- undefined cancelled-job error code: fixed;
- cancelled-job JobState/StepState mismatch: fixed;
- valid-submit composite transition: fixed.

Minor advisory comments were also handled where safe:

- coverage report now explains that `Status: current` applies to the report
  package while linked fixtures/goldens/oracles remain draft evidence;
- coverage report flags the generated Phase 1.4.1 traceability path as
  intentional non-production Dafny evidence;
- validation report distinguishes the post-`py_compile` artifact-hygiene rerun;
- Dafny policy now has an explicit Phase 1.4.1 section;
- Dataset/Catalog coverage generator no longer labels the cumulative
  `184 verified, 0 errors` result as Phase 1.3-only.

The follow-up CodeRabbit review on commit `d341251` raised two validator-quality
Majors. Both are addressed locally: the Phase 1.4.1 coverage checker now reports
missing regenerated files as validation errors before `filecmp.cmp()`, and it
rejects unknown row, mapping, and aggregate coverage levels explicitly.

CodeRabbit re-review must be requested after this remediation is pushed.

## Scope Review

No remediation change weakens `BoundDDDecision` or `EffectiveJobContext`. No
Spool browse/purge/export, Operator command semantics, full first vertical
slice, production code, Rust semantic-core, hosted daemon, `jobd`, `spoold`, or
`operatord` implementation was introduced.

Python tooling remains structural: it checks generated traceability freshness,
fixture/golden/oracle links, aggregate overclaim, broad-parent requirement
coverage, and placement policy. It does not decide Job/DD lifecycle
transitions, DD authorization, catalog resolution, dataset handle creation,
audit obligation, or return-code semantics.

## Judgment

```yaml
pr_29_merge_allowed: false
critical_findings_remaining: false
major_findings_remaining: false
cancelled_job_error_code_fixed: true
cancelled_job_state_space_fixed: true
valid_submit_transition_sequence_fixed: true
broad_requirement_overclaim_fixed: true
bound_dd_decision_sound: true
raw_security_decision_path_remaining: false
cross_request_replay_blocked: true
effective_principal_required: true
coverage_overclaim_remaining: false
coderabbit_blocking_findings_remaining: true
production_boundary_violated: false
```

Recommended next action: push the remediation commit, request CodeRabbit
re-review, wait for GitHub checks, and update this judgment if no new blocking
findings remain.
