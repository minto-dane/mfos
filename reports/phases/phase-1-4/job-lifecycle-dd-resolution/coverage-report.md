# Phase 1.4.1 Coverage Report

Status: current.

Generated traceability lives under
`evidence/traceability/generated/phase-1-4-1/`.

`Status: current` applies to this review report package. Linked fixtures,
goldens, and embedded oracles remain `status: draft` conformance evidence until
a later promotion gate. The generated traceability path is intentionally in the
Phase 1.4.1 package and remains non-production Dafny semantics evidence only.

Coverage summary:

```yaml
job_lifecycle_coverage_level: C4_VERIFIED_PROPERTY
effective_principal_coverage_level: C4_VERIFIED_PROPERTY
dd_resolution_coverage_level: C4_VERIFIED_PROPERTY
phase_1_4_1_required_test_coverage_level: C5_CONFORMANCE_LINKED
phase_1_4_1_fixture_coverage_level: C5_CONFORMANCE_LINKED
phase_1_4_1_parent_requirement_coverage_level: C2_PARTIAL_SEMANTIC
phase_1_4_1_requirement_subclaim_coverage_level: C4_VERIFIED_PROPERTY
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

Broad parent requirement rows remain `C2_PARTIAL_SEMANTIC` when the requirement
includes service provenance, program opens, spool opens, other protected
resources, or production `jobd` behavior outside Phase 1.4.1. Phase-scoped
subclaim rows are `C4_VERIFIED_PROPERTY` only where an explicit verified Dafny
property exists. The complete child scenario links are recorded in
`test-to-dafny.yml` and `fixture-to-dafny.yml`.

Requirement rows now distinguish:

- parent requirements: partial coverage only, with `not_claimed` listing the
  broad behavior outside Phase 1.4.1;
- Phase 1.4.1 subclaims: verified Dafny properties for dataset/DD effective
  principal, DD catalog/authorization binding, and authorization-bypass denial;
- C5 scenario rows: fixture/oracle/golden linked conformance rows only.

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

Remediated PR #29 evidence blockers:

- `cancelled-cannot-execute-0926` now uses modeled `MFOS_ERR_INVALID_STATE`
  instead of undefined `MFOS_ERR_INVALID_STATE_TRANSITION`.
- `cancelled-cannot-execute-0926` keeps attempted transitions in JobState
  space: `JOB_CANCELLED` to `JOB_EXECUTING`, with final state
  `JOB_CANCELLED`.
- `valid-submit-ready-0928` records the atomic Dafny lifecycle sequence:
  `JOB_SUBMITTED -> JOB_VALIDATED -> JOB_READY`.
