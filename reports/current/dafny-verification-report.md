# Phase 1 Dafny Verification Report

Status: current  
Date: 2026-04-29

## Result

```yaml
dafny_verification_status: blocked_by_missing_toolchain
dafny_verification_passed: false
toolchain_found: false
command_planned: dafny verify formal/executable-semantics/dafny/modules/*.dfy
validator_default_behavior: record_blocked_status_without_claiming_success
validator_required_behavior: MFOS_REQUIRE_DAFNY=1 or --require-dafny fails when the toolchain is missing
```

`dafny` is not available on the local `PATH`. No Dafny verification pass is
claimed. The default validation gate is allowed to pass artifact-structure
checks while recording `blocked_by_missing_toolchain`; release profiles that
require proof evidence must run `scripts/validate-dafny-semantics.sh
--require-dafny` or set `MFOS_REQUIRE_DAFNY=1`.

## Evidence Boundary

This report is evidence of attempted verification status only. It is not proof
evidence for the Dafny modules. A future verification pass must record:

- Dafny version,
- command line,
- module list,
- verification output,
- assumptions,
- reviewed limitations,
- reviewer status.
