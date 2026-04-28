# Spool Access Model

Status: Draft Phase 0.8 design model.

This directory contains a small TLA+ model for protected spool access in
`docs/design/specs/09-job-spool.md`. The model is intentionally abstract: it
checks authorization-before-content, retention-before-purge, stale-reference,
and deny-without-content invariants.

Artifacts:

- `SpoolAccess.tla`
- `SpoolAccess.cfg`

The model does not authorize production implementation.
