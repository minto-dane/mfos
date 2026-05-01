# Repository Information Architecture Report

Status: current.

## Scope

This refactor shards current reports by stable responsibility domain, records
every moved artifact in
`reports/current/repository-information-architecture-migration.yml`, and adds
validator coverage for flat-directory pressure, reports/current domain
structure, report-domain indexes, script namespace ownership, cross-directory
duplicate ownership, per-file current report indexing, and pack bridge/canonical
drift.

## Audited Areas

Audited `reports/`, `tests/catalog/`, `tests/fixtures/`, `tests/golden/`,
`evidence/traceability/`, `fuzz/`, `scripts/`, `tools/`, `formal/`,
`implementation/`, `docs/design/`, `docs/design/registries/`, `packs/`,
`prompts/`, `ai/`, `schemas/`, and `claims/`.

## Reports Current Domains

- `reports/current/architecture/`
- `reports/current/artifact-hygiene/`
- `reports/current/artifact-lifecycle/`
- `reports/current/ci/`
- `reports/current/dafny/`
- `reports/current/directory-ownership/`
- `reports/current/formal-assurance/`
- `reports/current/naming-safety/`
- `reports/current/platform/`
- `reports/current/readiness/`
- `reports/current/remediation/`
- `reports/current/scaffold/`

Existing `reports/current/fixedpoint/` and
`reports/current/source-grounding/` remain current live packages with explicit
indexes. The one-file policy domain was consolidated into the Dafny domain.

## Other IA Changes

- Added `fuzz/corpora/index.yml` and `fuzz/corpora/.mfos-dir.yml`.
- Added `formal/tla/README.md`, `.mfos-dir.yml`, and `index.yml`.
- Added `build/.mfos-dir.yml` and tightened build/AI/implementation tool
  boundary wording.
- Enriched fixture, golden, fuzz, and traceability indexes.
- Clarified `docs/design/packs/` as canonical pack contracts and
  `packs/pack-index.yml` as a bridge projection.
- Refreshed scaffold and directory ownership current reports against the live
  tree.
- Refreshed Japanese mirror source hashes without claiming complete translation.

## Boundary Statement

Phase-specific reports remain under `reports/phases/`, generated reports remain
under `reports/generated/`, and historical reports remain under
`reports/archive/`. Phase 1.4 remains planning-only. No production
implementation, Rust semantic-core, hosted daemon, semantic-runner command,
service implementation, runtime implementation, CPU feature detection, or
architecture backend was introduced.

## Validation

Local validation passed on 2026-05-01:

- `./scripts/validate-all.sh --check`: pass
- `./scripts/validate-naming-safety.sh release`: pass
- `./scripts/validate-artifact-hygiene.sh`: pass
- `./scripts/validate-component-scaffold.sh`: pass
- `./scripts/validate-language-formal-assurance.sh`: pass
- `./scripts/validate-dafny-semantics.sh --require-dafny`: pass,
  `136 verified, 0 errors`
- `python3 -m py_compile $(find scripts tools -name '*.py' -type f | sort)`:
  pass
- `git diff --check`: pass
