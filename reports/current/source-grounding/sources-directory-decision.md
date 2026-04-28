# Sources Directory Decision

Do not promote `sources/` to canonical in Phase 0.9.8.

`docs/design/source-matrix/source-matrix.yml` and
`docs/design/source-matrix/cards/` remain the canonical source index and Source
Card ledger. `sources/` is now a populated public-safe workbench with source
cards, concept cards, indexes, mapping notes, retrieval metadata, and a manual
parity report at `sources/source-matrix-parity.yml`. It remains noncanonical
until an ADR-backed migration updates validators, generated traceability, pack
references, docs, and indexes together.

Population of `sources/` improves review depth but does not strengthen the
semantic freeze by itself. Promotion should happen only through an ADR-backed
migration that updates validators, generated traceability, pack references,
docs, and indexes in one pass.
