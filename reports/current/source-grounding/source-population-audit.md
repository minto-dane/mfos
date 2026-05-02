# Sources Population Audit

`sources/` is now populated as a public-safe workbench, not as canonical source authority. The canonical ledger remains `docs/design/source-matrix/` until an ADR-backed migration updates validators, traceability, packs, and docs together.

## Counts

- Source files excluding ignored cache: 154
- Source-card artifacts: 49
- Concept-card artifacts: 21
- Notes: 18

## Policy Result

No IBM PDFs, HTML mirrors, screenshots, copied manuals, record layouts, command syntax, macro signatures, or message catalogs were committed. `sources/_cache/` remains ignored and contains only local, noncanonical cache metadata if present.

## Design Result

The population improves research depth and reviewability, but it does not make the semantic freeze fully valid. Phase 1 may use reviewed non-production Dafny executable semantics and conformance-harness validation, but Portable Semantic Core behavior, semantic evaluator/runner work, production implementation, and PACK-08 syntax/naming promotion remain blocked until source-card review status, fixture/source refs, golden/oracle source refs, and PACK-08 syntax/naming risk are closed.

## Remaining Blockers

- ADR-backed migration from `docs/design/source-matrix/` to `sources/` is not complete.
- `sources/source-matrix-parity.yml` now records a workbench candidate for every
  current canonical Source Matrix card, but this is not a canonical migration
  and still needs an automated parity validator.
- Job-control syntax and DD/JCL-shaped names in PACK-08 remain blocked for semantic-evaluator, semantic-runner, and production implementation work.
- Public release still requires legal/IP review.
