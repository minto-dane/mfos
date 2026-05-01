# Dafny Toolchain Red-team Review

Status: current
Date: 2026-04-29

## Findings

Critical: none.

Major: none.

Minor:

- Conformance comparison remains structural unless reviewed Dafny model-output
  evidence is supplied.

## Checks

- Dafny toolchain is pinned to 4.11.0 by `scripts/install-dafny.sh`.
- The pinned release asset SHA-256 is checked before extraction.
- `scripts/validate-dafny-semantics.sh --require-dafny` fails when Dafny is
  unavailable and succeeds only after the verifier runs.
- The verification command covers `formal/executable-semantics/dafny/modules/*.dfy`.
- The current module set verifies with `97 verified, 0 errors`.
- No case-only duplicate Dafny files remain in the canonical module path.
- Python loader/harness tooling remains nonsemantic.
- No Rust semantic-core, production code, hosted daemon, semantic-runner
  implementation, or PXM/MFVM/CVM/cluster implementation was introduced.
- Dafny-generated code remains forbidden from production paths.
