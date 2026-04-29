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
- fixture/oracle/golden alignment contracts,
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

## Pinned Verification Toolchain

Phase 1 verification uses the pinned Dafny release installed by
`scripts/install-dafny.sh`:

- Dafny: `4.11.0+fcb2042d6d043a2634f0854338c08feeaaaf4ae2`
- Z3: `Z3 version 4.14.1 - 64 bit`
- Asset: `dafny-4.11.0-x64-ubuntu-22.04.zip`
- SHA-256: `a46a9ff7cdd720f7955854c78e95df13f4cfe6b80691b05f8654fe19e8267179`

Verification command:

```sh
./scripts/install-dafny.sh
./scripts/validate-dafny-semantics.sh --require-dafny
```

The current module set verifies with `26 verified, 0 errors`.
