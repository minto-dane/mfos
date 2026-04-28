# ADR-0006: Canonical Paths and Implementation Root

Status: Proposed  
Date: 2026-04-27

## Decision

The current canonical Phase 0.6 design corpus remains under `docs/design/`.
Top-level directories such as `sources/`, `requirements/`, `specs/`,
`source-matrix/`, `claims/`, and `packs/` are bridge or future promotion paths
until a reviewed migration ADR changes the canonical source of truth.

OS body implementation areas are grouped under:

```text
implementation/
  runtime/
  nucleus/
  services/
  pxm/
  guard/
  sidecars/
  interfaces/
  tools/
  prototypes/
```

MFOS does not use a single top-level `src/` directory because it is not a
single program. Each implementation component may contain its own local `src/`
directory after the pre-implementation gate permits code.

## Canonical Sources of Truth

| Artifact family | Current canonical path | Notes |
| --- | --- | --- |
| Design canon | `docs/design/mfos-design.md` | Human-readable design canon candidate. |
| Split specs | `docs/design/specs/*.md` | English canonical; Japanese mirrors are explanatory. |
| Source Cards | `docs/design/source-matrix/cards/*.yml` | Machine-readable source grounding. |
| Source Card index | `docs/design/source-matrix/source-matrix.yml` | v0.5 source ledger index. |
| Requirements | `docs/design/registries/requirements.yaml` | v0.5 priority requirement registry. |
| Pack overview | `docs/design/packs/PACKS.md` | Human-readable pack plan. |
| Reports | `reports/` | Phase audit output and review records. |

## Consequences

- Do not silently move canonical specs from `docs/design` to top-level `specs/`.
- Do not create competing requirement ledgers without traceability migration.
- Generated traceability may live under `evidence/traceability/`.
- Local validators may read current canonical paths and emit reports.
- Production implementation remains blocked until relevant specs pass the
  pre-implementation gate.

## Non-Claims

This ADR does not imply production readiness. It does not authorize nucleus,
service, PXM, Guard, or AMF production implementation.

