# Job Lifecycle Model

Status: Draft Phase 0.8 design model.

This directory contains a small TLA+ model for the MFOS job lifecycle freeze in
`docs/design/specs/09-job-spool.md`. The model is intentionally abstract: it
checks ordering and safety invariants such as effective-principal-before-open,
authorization-before-queue, and no execution after terminal failure.

Artifacts:

- `JobLifecycle.tla`
- `JobLifecycle.cfg`

The model does not authorize production implementation.
