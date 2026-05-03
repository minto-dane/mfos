# Phase 1.4.2 Spool Coverage Report

Status: current.

Generated traceability lives under
`evidence/traceability/generated/phase-1-4-2/`.

## Coverage Summary

- Spool protected-resource aggregate: `C4_VERIFIED_PROPERTY`
- Required scenario rows: `C5_CONFORMANCE_LINKED`
- Fixture/golden rows: `C5_CONFORMANCE_LINKED`
- Requirement aggregate: `C2_PARTIAL_SEMANTIC`
- Formal claim aggregate: `C3_FULL_SEMANTIC`
- C5 overclaim remaining: false

## C5 Scenario Rows

- `spool-browse-owner-0912`: owner browse allowed.
- `spool-browse-nonowner-0913`: non-owner browse denied with no content.
- `spool-purge-denied-0914`: purge without authority denied.
- `spool-export-no-audit-0915`: export with required audit unavailable fails closed.
- `spool-evidence-not-audit-0916`: SpoolEvidence is not AuditEvidence.
- `spool-cross-request-replay-0917`: cross-request authorization replay blocked.
- `spool-spec-gap-not-success-0918`: SPEC_GAP is not success.
- `spool-unsupported-fails-0919`: UNSUPPORTED fails closed.
- `spool-deny-audit-0920`: DENY with audit obligation links to before-return audit.

## Coverage Boundaries

`MFOS-REQ-SPOOL-0101` remains parent-level `C2_PARTIAL_SEMANTIC`; Phase 1.4.2
subclaims carry `C4_VERIFIED_PROPERTY` only where explicit Dafny lemmas exist.
No requirement-wide C5 or release-ready model claim is made.
