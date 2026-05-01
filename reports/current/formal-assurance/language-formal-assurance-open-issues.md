# Language Formal Assurance Open Issues

Status date: 2026-04-28

## Open Issues

1. Toolchain versions, invocation profiles, trusted computing base assumptions,
   and proof-runner reproducibility remain draft.
2. Unsafe-boundary acceptance criteria and exception workflow remain draft.
3. CFI, CET, PKU, sanitizer, and static-analysis requirements are not yet tied
   to release-grade evidence.
4. Proof obligations are planned, but no proof artifacts are accepted.
5. Model acceptance criteria, coverage thresholds, and proof review workflow
   remain undefined.
6. Performance benchmark methodology, workload profiles, and evidence formats
   remain undefined.
7. Secure-operations rollback-drill and release-operations evidence formats
   remain undefined.
8. Semantic evaluator entry criteria are conditional and need a later reviewed
   gate decision per domain.

## Phase Gate Impact

These issues do not block Phase 1 loader-only artifact validation. They block
language/formal-assurance semantic evaluator work, verified-implementation
claims, performance/release claims, and all production implementation.

