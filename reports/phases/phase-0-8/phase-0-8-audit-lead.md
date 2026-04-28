# Phase 0.8 Audit Lead Report

Date: 2026-04-27

Scope:

- `docs/design/specs/07-audit.md`
- `schemas/mfos/audit-record.schema.yml`
- `formal/tla/audit-append/`
- `tests/catalog/phase-0-8-audit-tests.yml`
- `reports/phases/phase-0-8/phase-0-8-audit-lead.md`

No production code was added or modified.

## Freeze Result

Audit semantics are frozen at design level for Phase 0.8.

The freeze defines `auditd` as the evidence service, adds a closed `AuditRecord` schema, fixes record types and reason codes, requires correlation IDs, defines hash-chain semantics, and states deny-before-return ordering. It also freezes profile failure policy, redaction rules, remote export placeholder behavior, High-Assurance Guard audit-root placeholder behavior, audit query authorization, failure modes, state-machine transitions, positive/negative tests, and evidence requirements.

Source references in the Phase 0.8 audit-owned artifacts are `EXTREF-*` IDs only.

## Evidence Boundary

Accepted audit evidence is limited to schema-valid `AuditRecord` entries durably appended by `auditd`, verified exports that preserve stream sequence and hashes, and Guard-sealed audit roots bound to verified stream heads.

Diagnostic log lines, console lines, spool entries, spool output, and unverified remote collector receipts are not audit evidence and cannot satisfy audit obligations.

## Artifacts

- `docs/design/specs/07-audit.md`: upgraded to Phase 0.8 design freeze, with record taxonomy, reason-code registry, correlation semantics, deny-before-return, redaction, export, Guard root, state-machine, invalid transitions, tests, evidence requirements, and spec gaps.
- `schemas/mfos/audit-record.schema.yml`: design schema for `AuditRecord`, including required fields, closed enums, correlation IDs, subject/object models, obligations, hash fields, and Guard-root conditional requirements.
- `formal/tla/audit-append/AuditAppend.tla`: abstract state machine for append, export, Guard seal, query authorization, recovery, and invariants.
- `formal/tla/audit-append/README.md`: state-machine scope and invariant summary.
- `formal/tla/audit-append/state-machine.yml`: pre-existing Phase 0.8 state-machine scaffold preserved; the TLA artifact is the fuller audit append model.
- `tests/catalog/phase-0-8-audit-tests.yml`: Phase 0.8 positive, negative, fuzz, invalid-transition, and evidence test catalog.

## Spec Gaps

Blocking gaps remain for canonical serialization, signature/key hierarchy, remote export protocol, physical storage and crash consistency, redaction policy language, Guard ABI/attestation format, audit-query role taxonomy, error-code mapping, and registry synchronization outside the owned Phase 0.8 files. The generic `MFOS-REQ-AUDIT-0101` through `0105` bridge IDs in the core-freeze scaffold remain inactive until registry synchronization.

These gaps block production implementation and profile claims until resolved by follow-on owned work.
