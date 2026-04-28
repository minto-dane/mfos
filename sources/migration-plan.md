# Source Grounding Migration Plan

`docs/design/source-matrix` remains the canonical Source Matrix until an
accepted ADR migrates authority to `sources/`.

This plan defines how `sources/` can become the long-term home without creating
two competing sources of truth.

## Current State

- Canonical source-card index: `docs/design/source-matrix/source-matrix.yml`
- Canonical source cards: `docs/design/source-matrix/cards/`
- Canonical schema note: `docs/design/source-matrix/source-card-schema.md`
- Workbench root: `sources/`
- Cache root: `sources/_cache/`, ignored local scratch space

`sources/` is currently a populated public-safe workbench for retrieval logs,
source-card drafts, concept-card drafts, mapping notes, and migration policy.
It is not authoritative for normative design citations until an accepted ADR
migrates authority and regenerates validators, traceability, packs, docs, and
indexes together.

## Migration Principles

1. Preserve one canonical source of truth at every point.
2. Move metadata, not copied source material.
3. Keep IBM and other external source references public-safe.
4. Require explicit legal-control fields for external marks and
   non-compatibility boundaries.
5. Require concept cards to distinguish semantic overlap from MFOS divergence.
6. Treat cache manifests as local review aids, never as authority.

## Phases

### Phase 0: Bridge Policy

- Maintain `sources/registry.yml` as the bridge registry.
- Maintain `sources/source-grounding-index.yml` as the workbench index.
- Maintain `sources/retrieval-log.yml` for public-safe retrieval metadata.
- Keep all canonical source-card references pointed at
  `docs/design/source-matrix`.

Exit gate: policy files agree that `docs/design/source-matrix` is canonical
until ADR migration.

### Phase 1: Inventory and Parity

- Inventory every current Source Matrix ID.
- Define a field-by-field mapping from the current source-card schema to the
  `sources/source-card.schema.yml` shape.
- Identify records needing copyright, citation, or legal-control cleanup before
  migration.
- Define automated checks that fail if an external document, mirror, screenshot,
  or copied source substitute appears under `sources/`.

Exit gate: parity report covers all current Source Matrix IDs.

### Phase 2: Dry-Run Migration

- Create migrated public-safe source-card candidates under `sources/` without
  changing canonical authority.
- Link concept-card candidates to canonical Source Matrix IDs.
- Regenerate or dry-run traceability indexes from both locations and compare
  results.
- Review IBM/public-source retrieval records for cache and copyright policy
  compliance.

Exit gate: dry-run output has no source-ID loss, no traceability loss, and no
committed external source material.

### Phase 3: ADR Authority Transfer

- Adopt an ADR naming `sources/` as the canonical source-grounding home.
- Freeze or redirect `docs/design/source-matrix` according to the ADR.
- Update validators, traceability generators, and design citations to resolve
  through `sources/`.
- Retain a compatibility index from old Source Matrix paths to new paths.

Exit gate: validators enforce the new canonical path and reject divergent
updates to the old canonical records.

## Cache and Retrieval Requirements

For IBM and other public sources:

- Commit only metadata, short paraphrased mappings, and legal-control flags.
- Record retrieval activity in `sources/retrieval-log.yml` or local ignored
  manifests.
- Keep temporary downloads in ignored cache paths only.
- Purge temporary downloads when review no longer requires them.
- Do not cite local cache files as authoritative sources.

## Open Gaps

- No ADR currently authorizes migration.
- No automated parity check is defined here yet.
- No migrated source cards or concept cards are made canonical by this plan.
- Cache manifests are policy-defined but no manifest schema is committed yet.
