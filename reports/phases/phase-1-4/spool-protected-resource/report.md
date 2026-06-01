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

Traceability and evidence handling for this topic are tracked separately from
this Phase 1.4 planning report. This document stays limited to planned scope,
constraints, and executable-semantics verification intent; hosted service
behavior and implementation traceability remain deferred to a later
implementation gate.
