# Dafny Executable Semantics

Status: Phase 1 non-production executable-semantics artifacts.

This directory contains the MFOS Phase 1 canonical executable-semantics source
artifacts written in Dafny. These artifacts are specification and conformance
artifacts only.

Dafny source files are allowed only under this directory and related
non-production test/evidence paths. Dafny generated output, if produced, must
remain under `generated/` and must not be linked into production MFOS binaries
or services.

Phase 1 scope here includes:

- pure Dafny semantic contracts and invariants,
- deterministic symbolic state transition functions,
- fixture/oracle/golden compatibility contracts,
- validate declared metadata shape,
- check source references and requirement references,
- check declared dependencies and proof status.

This directory does not authorize:

- semantic-runner implementation,
- hosted daemon implementation,
- Rust semantic-core or Portable Semantic Core implementation,
- production code,
- production use of Dafny-generated code,
- production readiness or conformance claims.

## Module Map

- `modules/common.dfy`: shared deterministic primitives.
- `modules/errors.dfy`: MFOS error taxonomy and fail-closed rules.
- `modules/types.dfy`: MFOS-owned symbolic object types.
- `modules/authorization.dfy`: authorization decision contracts.
- `modules/audit.dfy`: audit-evidence and deny-before-return contracts.
- `modules/dataset_catalog.dfy`: catalog resolution and dataset handle contracts.
- `modules/job_spool.dfy`: job, DD resolution, and spool contracts.
- `modules/operator_console.dfy`: operator command contracts.
- `modules/first_vertical_slice.dfy`: HELLO job and BOB denied ALICE dataset contracts.

Normative policy: `docs/design/specs/43-dafny-executable-semantics-policy.md`.
