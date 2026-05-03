# Phase 1.4.2 Spool Protected Resource Report

Status: current.

Phase 1.4.2 deepens only the Dafny executable semantics for SpoolEntry as a
protected resource. The scope is limited to owner browse, non-owner browse
denial, purge denial without authority, export fail-closed when required audit
is unavailable, SpoolEvidence versus AuditEvidence separation, and bound
Spool authorization/audit linkage.

## Dafny Semantics Added

- `SpoolAccessContext`, `BoundSpoolDecision`, `SpoolAccessResult`, and
  `SpoolEvidence` type-level witnesses.
- `IsBoundSpoolDecision` and `BoundSpoolDecisionValid` bind subject, SpoolEntry
  object id, operation, policy version, and correlation id.
- Browse, purge, and export success predicates require bound Spool decisions and
  reuse Phase 1.2 Authorization/Audit predicates.
- Denied Spool access with audit uses Phase 1.2 Audit finalization functions.
- Export with required audit unavailable fails closed.
- Spool evidence and diagnostic log lines cannot satisfy AuditEvidence.

## Boundaries

This is not production implementation. No Rust semantic-core, hosted daemon,
`jobd`, `spoold`, `operatord`, real spool storage, SYSOUT handling, operator
command semantics, or full First Vertical Slice implementation is introduced.
Python tooling remains structural only and does not decide Spool business
semantics.

## Evidence

Generated traceability is under
`evidence/traceability/generated/phase-1-4-2/`. C5 is claimed only for rows with
fixture, embedded oracle, and golden-vector links. Broad parent requirement
coverage remains partial where production spool service behavior is outside
Phase 1.4.2.
