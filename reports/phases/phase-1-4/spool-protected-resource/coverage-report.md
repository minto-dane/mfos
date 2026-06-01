# Phase 1.4.2 Spool Coverage Planning Report

Status: planning-only / draft.

Draft generated traceability for the executable-semantics slice is staged under
`evidence/traceability/generated/phase-1-4-2/`; it is not production
implementation evidence.

## Coverage Summary

- Planned Spool protected-resource aggregate: `C4_VERIFIED_PROPERTY`
- Planned required scenario rows: `C5_CONFORMANCE_LINKED`
- Planned fixture/golden rows: `C5_CONFORMANCE_LINKED`
- Planned requirement aggregate: `C2_PARTIAL_SEMANTIC`
- Planned formal claim aggregate: `C3_FULL_SEMANTIC`
- C5 overclaim remaining: false

## C5 Scenario Rows

- `spool-browse-owner-0912`: planned owner browse conformance row.
- `spool-browse-nonowner-0913`: planned non-owner browse denial row.
- `spool-purge-denied-0914`: planned purge-without-authority denial row.
- `spool-export-no-audit-0915`: planned export audit-unavailable fail-closed row.
- `spool-evidence-not-audit-0916`: planned SpoolEvidence/AuditEvidence separation row.
- `spool-cross-request-replay-0917`: planned cross-request replay denial row.
- `spool-spec-gap-not-success-0918`: planned SPEC_GAP-not-success row.
- `spool-unsupported-fails-0919`: planned UNSUPPORTED fail-closed row.
- `spool-deny-audit-0920`: planned DENY-before-return audit row.

## Coverage Boundaries

`MFOS-REQ-SPOOL-0101` remains parent-level `C2_PARTIAL_SEMANTIC`; Phase 1.4.2
subclaims carry `C4_VERIFIED_PROPERTY` only where explicit Dafny lemmas exist.
No requirement-wide C5 or release-ready model claim is made.
