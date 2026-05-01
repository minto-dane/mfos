# PR #21 Blocker Report

Status date: 2026-05-01
Status: superseded by merged replacement PR #22.

## Blocker

PR #21 could not be updated in place after review because the remote branch
`docs/architecture-portability-x64-target-profiles` rejects force-pushes under
repository rules.

The branch needed history cleanup because the remote PR #21 branch was stacked
on PR #20/PR #19 history, while PR #19 had already merged into `dev` as a
squash merge. A clean PR #21-only commit was reconstructed locally on top of
`origin/dev`, but GitHub rejected the required `--force-with-lease` update.

## Resolution

Created a clean replacement branch from the reviewed local commit and opened
replacement PR #22 against `dev`: <https://github.com/minto-dane/mfos/pull/22>.
PR #22 passed validation and merged.

The replacement PR preserved:

- Architecture portability policy.
- x86-64 target profiles.
- CPU Feature Registry and CPU Target Profile Registry.
- SGX as enclave/TEE, not CVM.
- TDX and SEV-SNP as CVM profiles.
- Roadmap and Phase 1 Dafny alignment validators.
- PR #21 review remediation and validation report.

## Merge Gate

PR #21 itself must not be merged from the stale stacked branch and remains
superseded.

Replacement PR #22 merged after GitHub checks passed because the reviewed
content had no remaining Critical or Major findings and local validation passed.

Production implementation remains false.
Rust Phase 1 semantic-core remains forbidden.
Hosted daemon implementation remains forbidden.
Phase 1.4 is not started.
