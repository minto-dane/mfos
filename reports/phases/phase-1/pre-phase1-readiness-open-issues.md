# Pre-Phase-1 Readiness Open Issues

Status: current  
Date: 2026-04-28

No Critical or Major issues remain.

## Minor

1. Some current reports still describe earlier branches such as
   `fix/total-repo-remediation`; those reports are historical context and are
   indexed as current remediation records, not the active branch state. The
   active branch state is recorded in `docs/design/STATUS.md` and
   `reports/phases/phase-1/pre-phase1-readiness-final-report.md`.
2. Source-grounding remains conditional for semantic evaluator work. This does
   not block Phase 1 Dafny scaffold and loader-only artifact validation, but it
   continues to block semantic evaluator and production claims.
3. Legacy `schemas/mfos/*.schema.yml` files still emit draft-mode
   normalization warnings from `validate-schema-files.py`. They are visible and
   nonblocking because Phase 1 is limited to Dafny scaffold and loader-only
   artifact validation.
4. The fixed-point closure PR must pass GitHub checks before merge. PR #10,
   PR #11, PR #12, and PR #13 have already landed in `dev`.

## Blockers

None for Phase 1 Dafny scaffold plus loader-only artifact validation.
