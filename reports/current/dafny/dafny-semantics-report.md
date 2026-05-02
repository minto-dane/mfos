# Phase 1 Dafny Semantics Report

Status: current  
Date: 2026-04-29  
Scope: Phase 1 non-production Dafny executable-semantics artifacts and conformance-harness validation

## Summary

Phase 1 now has non-production Dafny executable-semantics source artifacts under
`formal/executable-semantics/dafny/modules/`.

The added Dafny modules model MFOS-owned symbolic semantics for:

- common deterministic primitives,
- error taxonomy,
- shared object types,
- authorization,
- audit,
- dataset/catalog,
- job/spool,
- operator console,
- first vertical slice.

The artifacts are not production implementation. They are not Rust
semantic-core code, not a hosted daemon, not service implementation, and not the
future `mfos-semantic-runner`.

## Policy Boundary

Allowed:

- Dafny source artifacts under `formal/executable-semantics/dafny/`.
- Non-production fixture/oracle/golden loading.
- Deterministic structural comparison.
- Verification status reporting.

Forbidden:

- production implementation,
- hosted daemon implementation,
- Rust semantic-core or Portable Semantic Core,
- future semantic-runner command implementation,
- generated Dafny code in production,
- PXM/MFVM/CVM/cluster implementation.

## Implemented Invariants

- `SPEC_GAP` and `UNSUPPORTED` are fail-closed and not success.
- Protected resource handles require `ALLOW` or `ALLOW_WITH_AUDIT`.
- Deny with audit obligation has before-return audit evidence.
- Catalog resolution requires committed, integrity-valid catalog entries.
- Dataset handles bind policy version and object generations.
- Stale dataset handles are rejected.
- Job dataset open requires an effective principal before open.
- DD resolution requires catalog resolution and authorization.
- Spool entries are protected resources.
- Operator commands require authorization; audited commands require audit evidence.
- Root shell is not modeled as first privileged UI.
- BOB denied ALICE dataset maps to `MFOS_ERR_POLICY_DENIED` with `DATASET_READ_NOT_PERMITTED`.

## Verification Status

Pinned Dafny 4.11.0 is installed through `scripts/install-dafny.sh`.
`scripts/validate-dafny-semantics.sh --require-dafny` verified
`formal/executable-semantics/dafny/modules/*.dfy` and completed with
`184 verified, 0 errors`.
