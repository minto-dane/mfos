# Phase 1.4.1 Coverage Report

Status: current.

Generated traceability lives under
`evidence/traceability/generated/phase-1-4-1/`.

Coverage summary:

```yaml
job_lifecycle_coverage_level: C4_VERIFIED_PROPERTY
effective_principal_coverage_level: C4_VERIFIED_PROPERTY
dd_resolution_coverage_level: C4_VERIFIED_PROPERTY
phase_1_4_1_required_test_coverage_level: C5_CONFORMANCE_LINKED
phase_1_4_1_fixture_coverage_level: C5_CONFORMANCE_LINKED
phase_1_4_1_requirement_coverage_level: C4_VERIFIED_PROPERTY
formal_claim_coverage_level: C3_FULL_SEMANTIC
aggregate_c5_overclaim_remaining: false
c5_scope: required scenario and fixture rows only
```

C5 is claimed only where the row has:

- an explicit verified Dafny lemma;
- verification evidence;
- fixture reference;
- golden vector reference;
- embedded oracle linkage.

Requirement-level rows remain `C4_VERIFIED_PROPERTY`. They link verified Dafny
properties, but they do not claim C5 unless every child scenario is represented
as a complete fixture/oracle/golden set at that row. The complete child scenario
links are recorded in `test-to-dafny.yml` and `fixture-to-dafny.yml`.

C4 rows remain C4 when they have verified Dafny properties but no dedicated
fixture/oracle/golden vector. Formal claims remain below C4/C5 because this PR
does not add proof artifacts.

New binding-strengthening rows are intentionally C4, not C5:

- `INV_JOB_DD_DECISION_REQUIRES_EFFECTIVE_CONTEXT`
- `INV_JOB_DD_BOUND_DECISION_BINDS_REQUEST`
- `INV_JOB_DD_CROSS_REQUEST_AUTHORIZATION_REPLAY_BLOCKED`
- `INV_JOB_DD_DENY_MFOS_OK_INVALID`
- `INV_JOB_DD_VALID_ALLOW_AND_DENY_DISTINGUISHABLE`

These rows prove the DD authorization witness shape and replay/deny coherence
properties, but no dedicated fixture/oracle/golden vectors are claimed for them
in this PR.

Required C5-linked scenario families:

- valid job submit reaches READY;
- missing effective principal fails closed;
- dataset open before effective principal fails closed;
- DD resolution through committed catalog and ALLOW creates a bound handle;
- DD resolution through catalog but DENY creates no handle;
- catalog bypass and authorization bypass fail closed;
- malformed, uncommitted, rolled-back, partial-journal, and integrity-failed
  catalog cases fail closed;
- stale handle after policy change fails;
- invalid lifecycle transition fails;
- cancelled job cannot execute further.
