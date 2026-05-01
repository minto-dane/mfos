# Phase 1.4 Red-Team Plan

Status date: 2026-05-01
Status: current planning-only red-team plan.

This plan defines checks for a future Phase 1.4 implementation PR. It does not
implement Job/Spool/Operator Dafny semantics.

## Red-Team Objectives

- Prevent coverage overclaim for Job/Spool/Operator rows.
- Prevent architecture, production, daemon, semantic-runner, and Rust
  semantic-core boundary violations.
- Prevent Python tooling from becoming a Job/Spool/Operator semantic evaluator.
- Prevent bypasses across Phase 1.2 Authorization/Audit and Phase 1.3
  Dataset/Catalog dependencies.
- Prevent first vertical slice upgrades by inference.

## Required Attack Checks

| Area | Red-team check |
| --- | --- |
| Job principal | Try to open a dataset before effective principal establishment; expected result is fail closed. |
| DD catalog path | Try to bind a DD directly to a dataset handle without catalog resolution; expected result is no handle. |
| DD authorization path | Try to bind a DD after catalog success but before authorization allow; expected result is no handle. |
| Unauthorized dataset | Try to complete a job step with a denied dataset decision; expected result is failed step/job and no handle. |
| Lifecycle | Try invalid job, step, spool, and operator-command transitions; expected result is non-success and no protected side effect. |
| Audit correlation | Try protected step completion without required audit correlation; expected result is fail closed. |
| Spool ownership | Try non-owner browse; expected result is denied unless an explicit authorization property covers the exception. |
| Spool purge | Try purge without authority or retention eligibility; expected result is no purge. |
| Spool export | Try export when required audit is unavailable or missing; expected result is fail closed. |
| Operator authorization | Try command execution without authorization allow; expected result is no execution. |
| Confirmation | Try destructive command execution without confirmation; expected result is denied or pending, not executing. |
| Dual control | Try dual-control execution with a single approval; expected result is denied or pending. |
| Emergency | Try emergency mode without reason or expiry; expected result is denied. |
| Automation | Try automation direct service calls, self-confirmation, or audit bypass; expected result is denied. |
| Privileged UI | Try to represent a root shell as the first privileged UI; expected result is not a successful operator path. |

## Coverage Overclaim Checks

The future red-team pass must verify:

- C4 rows have exact verified Dafny symbols.
- C5 rows have exact C4 symbols plus fixture/oracle/golden links.
- Aggregate C5 claims have no required child row below C5.
- Dataset/Catalog and Authorization/Audit dependencies are cited at their
  actual scoped levels.
- Formal claims remain below C4/C5 unless proof artifacts exist.
- Verification counts are not used as primary coverage evidence.
- Existing Phase 0.9 fixture/golden seeds are not treated as Phase 1.4 C5 by
  presence alone.

## Boundary Checks

The future red-team pass must search for:

- Production implementation under implementation, services, nucleus, guard,
  pxm, or runtime paths.
- Rust semantic-core, Portable Semantic Core, or generated production code.
- Hosted daemon, server, listener, RPC, HTTP, background worker, or hosted
  semantic prototype behavior.
- Semantic-runner command implementation.
- Python branching that decides job lifecycle, spool ownership, DD resolution,
  operator authorization, confirmation, dual-control, emergency, automation, or
  return-code behavior.
- Wording that claims z/OS, JES, JES2, JCL, RACF, SMF, or external command
  compatibility.

## Planned Validator Expectations

The future `scripts/check-phase1-4-job-spool-operator-coverage.py` validator
should be structural and evidence-oriented. It should not compute MFOS
Job/Spool/Operator outcomes in Python.

Allowed validator behavior:

- Parse generated coverage YAML.
- Check exact Dafny symbol declarations.
- Check verification status for C4/C5 rows.
- Check fixture/oracle/golden path consistency.
- Check aggregate coverage ranks against required child rows.
- Check formal-claim proof boundaries.
- Check that Phase 1.4 reports are deterministic and indexed.

Forbidden validator behavior:

- Decide whether a job transition is valid.
- Decide whether a spool browse is authorized.
- Decide whether an operator command is authorized.
- Interpret command text, job-control text, SYSIN, SYSOUT, or DD data.
- Simulate confirmation, dual-control, emergency expiry, automation ingress,
  audit availability, or return-code aggregation.

## Red-Team Judgment

```yaml
phase_1_4_red_team_plan_defined: true
phase_1_4_red_team_executed_by_this_pr: false
phase_1_4_implementation_started: false
production_implementation_allowed: false
rust_phase_1_canonical_semantics_allowed: false
hosted_daemon_implementation_allowed: false
recommended_next_action: execute this red-team plan against the later Phase 1.4 implementation PR
```
