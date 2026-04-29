# Pre-Phase-1 Second-Pass Remediation

Status: current  
Date: 2026-04-28  
Branch: `fix/pre-phase-1-total-readiness-second-pass`

## Summary

The second pass found no production implementation, hosted daemon, semantic
runner, Rust semantic-core, or PXM/MFVM/CVM/cluster implementation. It did find
several readiness-blocking metadata and executable-spec artifact issues. Those
Critical/Major issues have been repaired without starting Phase 1
implementation.

## Repairs

- Converted the Rust service implementation prompt into an inactive future
  template that is explicitly forbidden for Phase 1.
- Removed hosted semantic prototype paths from pack outputs and spec routing.
- Corrected the audit deny-before-return catalog and golden vector.
- Aligned formal claim/proof-obligation schemas with formal registries and
  strengthened proof-obligation validation.
- Added canonical `MFOS-REQ-DAFNY-*` requirements, registry tests, and evidence
  linkage.
- Aligned the fixture and embedded-oracle schemas with the current Phase 0.9
  artifact shapes and made validators check schema required fields.
- Expanded no-implementation validation to cover future implementation scaffold
  roots.
- Updated source workbench parity and public-safe source guidance.
- Deduplicated generated Phase 0.9 requirement-to-test traceability and made
  missing fixture evidence visible as a generated gap.

## Remaining Minor

Legacy `schemas/mfos/*.schema.yml` files still need normalization to the newer
schema style. The new schema validator surfaces this as draft-mode warnings
only; the warnings are not Phase 1 blockers because Phase 1 is limited to
Dafny scaffold and loader-only artifact validation.

## Scope

Allowed:

- Dafny scaffold metadata and policy work.
- Loader-only artifact validation.
- Traceability repair.

Forbidden:

- Rust semantic-core or Portable Semantic Core.
- Semantic runner.
- Hosted daemon or hosted semantic prototype.
- Production service or generated production code.
- PXM/MFVM/CVM/cluster implementation.
