# PXM/MFVM Requirements Docs Red-Team Review

Status date: 2026-04-28

## Critical Findings

None remaining after remediation.

## Major Findings

None remaining after remediation.

## Minor Findings

- PXM Control API wire format is intentionally draft and must be frozen before semantic evaluator work.
- Confidential VM profile-specific launch and attestation formats remain draft.
- Cluster quorum and scheduler algorithms remain unspecified.
- Proof obligations are registered as planned, not proven.

## Checks Performed

- MFVM is not treated as a trusted root.
- PXM is prohibited from interpreting enterprise semantics.
- MFVM cannot directly own privileged virtualization roots.
- Nested virtualization is not required.
- TDX/SEV names are allowed only as technology/profile names.
- Hyper-V/KVM names remain external-reference/comparison context only.
- CVM secret release without attestation is a negative test and fail-closed rule.
- Cluster placement is not security enforcement.
- Formal verification is not overclaimed.
- Phase 1 gates remain conservative.

## Judgment

No Critical or Major red-team finding remains. Phase 0.10 does not authorize implementation.
