# Test / Fuzz / Evidence Scaffold Audit

`tests/catalog/` root uses stable current names and has `index.yml`.

`tests/fixtures/` and `tests/golden/` are grouped by domain and indexed.

`evidence/traceability/` separates current, generated, and archived matrices.

Fuzz corpora have seed-plan files for Phase 0.9 parser/fixture targets. Fuzz target implementation directories are still planned and should not be treated as implemented fuzzers.

Recommended action: keep validation scripts excluding archive artifacts from current Phase 0.9 fixture/golden validation.
