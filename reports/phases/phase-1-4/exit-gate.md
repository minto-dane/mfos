# Phase 1.4 Exit Gate

Status date: 2026-05-01
Status: defined for future implementation exit.

This exit gate defines the evidence required before Phase 1.4 may be claimed
complete in a later PR. This planning package does not satisfy or claim the
exit gate.

## Required Exit Evidence

A future Phase 1.4 implementation PR may claim exit only when all items below
are true:

1. Every required Job/Spool/Operator property in
   `reports/phases/phase-1-4/planning-report.md` is represented by an exact
   Dafny property symbol.
2. The pinned Dafny verification gate passes and verifies the changed module
   set.
3. The future Phase 1.4 coverage generator emits deterministic traceability
   under `evidence/traceability/generated/phase-1-4/`.
4. The future coverage summary records only scoped, row-backed coverage
   claims.
5. Every C4 row has an exact verified Dafny symbol.
6. Every C5 row has C4 plus fixture, embedded oracle, and golden-vector links.
7. Every aggregate C5 claim has all required child rows at C5.
8. Formal claims without proof artifacts remain below C4/C5.
9. The future Phase 1.4 validator passes and is wired into the validation set
   only after real generated artifacts exist.
10. `STATUS.md` is updated without implying production readiness or full-domain
    completion beyond the proven Phase 1.4 scope.

## Required Property Coverage

The future exit package must cover these rows without overclaim:

- Job effective principal exists before dataset open.
- DD resolution cannot bypass catalog resolution.
- DD resolution cannot bypass authorization.
- Unauthorized dataset in job step fails.
- Invalid job lifecycle transition is not success.
- Step completion requires audit correlation where required.
- `SpoolEntry` is protected resource.
- Spool browse by non-owner is denied.
- Spool purge without authority is denied.
- Spool export without audit is denied.
- Operator command cannot execute without authorization.
- Destructive command without confirmation is denied.
- Dual-control command with single approval is denied.
- Emergency mode without reason or expiry is denied.
- Automation hook cannot bypass authorization/audit.
- Root shell is not first privileged UI.

## Required Conformance Links

The future exit package must link all required fixture/oracle/golden rows listed
in the planning report. Seed fixture existence alone is not enough. The
validator must prove:

- Fixture `expected_oracle` equals the linked golden vector.
- Golden vector `fixture_ref` equals the linked fixture.
- Embedded oracle `fixture_ref` equals the linked fixture.
- Golden vector is deterministic.
- Fixture expected evidence matches embedded oracle evidence requirements.
- Golden expected decisions, transitions, audit records, final state, and
  failure fields mirror the embedded oracle.
- Linked evidence refs are registered or otherwise explicitly reviewed.

## Validation Required At Exit

The future implementation PR must pass the standard validation set and the
future Phase 1.4 coverage checker:

```text
./scripts/validate-all.sh --check
./scripts/validate-naming-safety.sh release
./scripts/validate-artifact-hygiene.sh
./scripts/validate-component-scaffold.sh
./scripts/validate-language-formal-assurance.sh
./scripts/validate-dafny-semantics.sh --require-dafny
python3 scripts/checks/semantic-coverage/check-semantic-coverage-mapping.py
python3 scripts/checks/formal-claims/check-formal-claim-coverage.py
python3 scripts/phases/phase-1/check-phase1-gap-triage.py
python3 scripts/phases/phase-1/check-phase1-2-auth-audit-coverage.py
python3 scripts/phases/phase-1/check-phase1-3-dataset-catalog-coverage.py
python3 scripts/check-phase1-4-job-spool-operator-coverage.py
python3 scripts/checks/check-architecture-portability-policy.py
python3 scripts/checks/check-x64-profile-policy.py
python3 scripts/checks/check-cpu-feature-registry.py
python3 scripts/checks/check-roadmap-phase-alignment.py
python3 -m py_compile $(find scripts tools -name '*.py' -type f | sort)
git diff --check
```

## Exit Blockers

Phase 1.4 must not exit if any item below remains:

- Required property row below C4 when exit criteria require proof.
- Required conformance row below C5 when included in the Phase 1.4 aggregate.
- Fixture/golden/oracle drift.
- Python business-semantics evaluation of Job/Spool/Operator behavior.
- Production code, Rust semantic-core, hosted daemon, or semantic runner.
- Job/Spool/Operator full-domain completion claim without child-row evidence.
- Formal claim C4/C5 overclaim without proof artifacts.
- First vertical slice C5 upgrade by inference rather than generated evidence.

## Exit Judgment

```yaml
phase_1_4_exit_gate_defined: true
phase_1_4_exit_gate_satisfied_by_this_pr: false
phase_1_4_implementation_started: false
phase_1_4_completion_claimed: false
production_implementation_allowed: false
rust_phase_1_canonical_semantics_allowed: false
hosted_daemon_implementation_allowed: false
recommended_next_action: implement and validate non-production Dafny semantics in a later PR only after entry-gate review
```
