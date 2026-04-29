# Phase 1 Dafny Verification Report

Status: current  
Date: 2026-04-29

## Result

```yaml
dafny_verification_status: passed
dafny_verification_passed: true
toolchain_found: true
dafny_version: 4.11.0+fcb2042d6d043a2634f0854338c08feeaaaf4ae2
z3_version: Z3 version 4.14.1 - 64 bit
install_method: scripts/install-dafny.sh pinned GitHub release download
install_asset: dafny-4.11.0-x64-ubuntu-22.04.zip
install_sha256: a46a9ff7cdd720f7955854c78e95df13f4cfe6b80691b05f8654fe19e8267179
verify_command: scripts/validate-dafny-semantics.sh --require-dafny
dafny_command: .tools/dafny/4.11.0/dafny/dafny verify <sorted find formal/executable-semantics/dafny/modules -type f -name '*.dfy'>
verified_modules: 9
module_list:
  - formal/executable-semantics/dafny/modules/audit.dfy
  - formal/executable-semantics/dafny/modules/authorization.dfy
  - formal/executable-semantics/dafny/modules/common.dfy
  - formal/executable-semantics/dafny/modules/dataset_catalog.dfy
  - formal/executable-semantics/dafny/modules/errors.dfy
  - formal/executable-semantics/dafny/modules/first_vertical_slice.dfy
  - formal/executable-semantics/dafny/modules/job_spool.dfy
  - formal/executable-semantics/dafny/modules/operator_console.dfy
  - formal/executable-semantics/dafny/modules/types.dfy
exit_code: 0
verification_summary: Dafny program verifier finished with 26 verified, 0 errors
started_at_utc: '2026-04-29T00:00:00Z'
completed_at_utc: '2026-04-29T00:00:00Z'
verification_output_path: reports/current/dafny-verification-report.md
assumptions:
  - The pinned Ubuntu 22.04 x64 Dafny release is the Phase 1 verification toolchain.
  - Verification covers current Phase 1 Dafny modules only.
reviewed_limitations:
  - No production readiness is claimed.
  - No semantic-runner, hosted daemon, or Rust semantic-core implementation is authorized.
reviewer_status: toolchain_and_report_reviewed
validator_default_behavior: record_blocked_status_without_claiming_success
validator_required_behavior: MFOS_REQUIRE_DAFNY=1 or --require-dafny fails when the toolchain is missing
```

The pinned Dafny toolchain was installed locally by `scripts/install-dafny.sh`.
`scripts/validate-dafny-semantics.sh --require-dafny` ran all current modules
under `formal/executable-semantics/dafny/modules/*.dfy` and completed with
`26 verified, 0 errors`.

## Evidence Boundary

This report is verification evidence for the current Phase 1 Dafny module set.
It is not production-readiness evidence, not hosted-daemon evidence, not
semantic-runner evidence, and not authorization to use Dafny-generated code in
production.

The verified modules are:

- `common.dfy`
- `errors.dfy`
- `types.dfy`
- `authorization.dfy`
- `audit.dfy`
- `dataset_catalog.dfy`
- `job_spool.dfy`
- `operator_console.dfy`
- `first_vertical_slice.dfy`

The proof evidence remains scoped to the symbolic Phase 1 Dafny semantics only.
