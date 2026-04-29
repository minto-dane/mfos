# Semantic Coverage Report

Status date: 2026-04-29

## Scope

This report records Phase 1.1 semantic coverage for the Phase 0.9 core
enterprise semantics artifacts against the non-production Dafny executable
semantics under `formal/executable-semantics/dafny/modules/`.

PR prerequisite status:

- PR #15 landed in `dev`.
- PR #16 could not be merged directly because repository rules prohibit both
  force-pushes and merge commits on its stacked branch.
- PR #17 landed the same Dafny toolchain verification closure content on top of
  `dev`; PR #16 was closed as superseded.

## Coverage Model

| Level | Meaning |
| --- | --- |
| `C0_NONE` | No Dafny-side coverage. |
| `C1_TYPE_ONLY` | Type exists only. |
| `C2_PARTIAL_SEMANTIC` | Partial semantics exist. |
| `C3_FULL_SEMANTIC` | Semantic definition exists. |
| `C4_VERIFIED_PROPERTY` | Dafny predicate, function, method, lemma, or invariant verifies. |
| `C5_CONFORMANCE_LINKED` | Fixture/oracle/golden traceability is linked to a Dafny target. |
| `C6_RELEASE_READY_MODEL` | Release-ready model. Not claimed in Phase 1.1. |

## Domain Coverage

| Domain | Coverage | Basis |
| --- | --- | --- |
| Authorization | `C4_VERIFIED_PROPERTY` | `authorization.dfy` verifies decision, fail-closed, policy-denial, and no-handle-without-allow properties. |
| Audit | `C4_VERIFIED_PROPERTY` | `audit.dfy` verifies audit evidence, deny-before-return, log-line-not-record, and spool-not-evidence properties. |
| Dataset/Catalog | `C4_VERIFIED_PROPERTY` | `dataset_catalog.dfy` verifies committed-only resolution, uncommitted/rolled-back/integrity-failed denial, handle authorization, and stale-handle rejection. |
| Job/Spool | `C4_VERIFIED_PROPERTY` | `job_spool.dfy` verifies principal-before-open, DD catalog/auth dependency, protected spool, non-owner browse denial, and purge-without-authority denial. |
| Operator Console | `C4_VERIFIED_PROPERTY` | `operator_console.dfy` verifies auth-before-execute, audit requirement, destructive confirmation, dual-control, emergency metadata, and root-shell exclusion. |
| First Vertical Slice | `C5_CONFORMANCE_LINKED` | `first_vertical_slice.dfy` verifies HELLO and BOB-denied contracts and links to Phase 0.9 fixtures/golden vectors. |

## Traceability Outputs

Generated traceability files are under
`evidence/traceability/generated/phase-1-1/` to preserve repository artifact
hygiene:

- `requirement-to-dafny.yml`
- `test-to-dafny.yml`
- `fixture-to-dafny.yml`
- `oracle-to-dafny.yml`
- `formal-claim-to-dafny.yml`

The generated mapping covers:

- 18 Phase 0.9 core requirement IDs referenced by the core test catalogs.
- 74 Phase 0.9 core catalog entries.
- 74 fixtures.
- 74 golden/oracle entries.
- 11 formal claims, with Phase 1.1 Dafny coverage for the authorization and
  audit claims and planned/non-Phase-1.1 status for PXM/MFVM/CVM/cluster claims.

## Verification

`./scripts/validate-dafny-semantics.sh --require-dafny` verifies the current
Dafny module set with:

```text
Dafny program verifier finished with 45 verified, 0 errors
```

This remains non-production evidence. It does not authorize Rust semantic-core,
semantic-runner, hosted daemon, service, nucleus, PXM, Guard, MFVM, CVM, cluster,
or production implementation work.

## Judgment

```yaml
phase_1_1_semantic_coverage_complete: true
core_domains_coverage_level:
  authorization: C4_VERIFIED_PROPERTY
  audit: C4_VERIFIED_PROPERTY
  dataset_catalog: C4_VERIFIED_PROPERTY
  job_spool: C4_VERIFIED_PROPERTY
  operator_console: C4_VERIFIED_PROPERTY
first_vertical_slice_coverage_level: C5_CONFORMANCE_LINKED
negative_semantics_complete: true
production_implementation_allowed: false
rust_phase_1_canonical_semantics_allowed: false
hosted_daemon_implementation_allowed: false
```
