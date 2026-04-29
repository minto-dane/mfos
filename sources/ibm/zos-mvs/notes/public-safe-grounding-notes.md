# Public-Safe Grounding Notes

## Review Position

The z/OS MVS cards are MFOS design-background mappings for job, spool, catalog,
and workload-management concepts. They intentionally exclude JES command syntax,
JCL grammar, DFSMS data structures, spool internals, macros, tables, diagrams,
and IBM record layouts.

## Requirements Hooks

- `MFOS-REQ-JOB-0001`, `MFOS-REQ-JOB-0003`, and `MFOS-REQ-JOB-0005` need state-machine and authorization tests.
- `MFOS-REQ-SPOOL-0001`, `MFOS-REQ-SPOOL-0003`, and `MFOS-REQ-SPOOL-0004` need browse, output, retention, and purge controls.
- `MFOS-REQ-CATALOG-0002` through `MFOS-REQ-CATALOG-0004` need schema and transaction tests.
- `MFOS-REQ-WPOL-0001`, `MFOS-REQ-WPOL-0002`, `MFOS-REQ-WPOL-0006`, `MFOS-REQ-WPOL-0009`, and `MFOS-REQ-WPOL-0010` need policy authorization and starvation tests.

## Negative Tests

- Unauthorized submit and spool browse must fail closed.
- Invalid lifecycle transitions and retention-bypassing purge must be rejected.
- Catalog resolution must not expose uncommitted, rolled-back, or integrity-mismatched entries.
- WLM policy updates must be authorized and audited.

## Key Gaps

- Basic Skills JES topics are useful but not release pinned.
- MFOS still needs an initial JCL-like grammar decision without importing IBM syntax.
- catalogd needs a native transaction journal and recovery model.
- wlmd needs a phase-1 policy schema and starvation-resistant dispatch rules.
