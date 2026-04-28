# Repository Scaffold Open Issues

Status: current

## Critical

None.

## Major

- `implementation/` contains many empty future implementation directories. Root README states that directory presence is not readiness, but leaf directories do not each carry that warning. Recommended action: add component-level scaffold metadata before assigning Phase 1 agents.
- `sources/` contains a broad future source/concept-card tree while canonical Source Cards live under `docs/design/source-matrix/cards/`. Recommended action: either keep `sources/` explicitly planned via an index or migrate only after ADR.

## Minor

- `ci/linters/` contains empty placeholder directories while actual validators live under `scripts/` and are invoked by `.github/workflows/design-validation.yml`.
- Many planned future test/evidence/build/supply-chain directories are empty by design. They are not blockers, but should receive indexes before being assigned to agents.

phase_1_blockers_found: false
phase_1_should_remain_allowed: true
