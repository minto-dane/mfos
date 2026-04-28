# sources/

This directory is the public-safe source-grounding workbench for MFOS. It is
not yet the canonical Source Matrix.

Until an accepted ADR explicitly migrates source-card authority, the canonical
machine-readable source inventory remains:

- `docs/design/source-matrix/source-matrix.yml`
- `docs/design/source-matrix/cards/`
- `docs/design/source-matrix/source-card-schema.md`

The `sources/` tree is a bridge layer for future source cards, concept cards,
retrieval manifests, and migration planning. Content here may prepare, index,
or audit source grounding, but it must not override the canonical
`docs/design/source-matrix` records before ADR migration.

`sources/source-matrix-parity.yml` records the current workbench candidate for
each canonical Source Matrix card. That parity file is a review aid only; it is
not an authority transfer and does not upgrade source cards to reviewed status.

## Workbench Scope

Use this directory for:

- public-safe bibliographic source metadata
- concept cards that cite source IDs
- source-to-MFOS mapping notes
- retrieval logs and cache manifests
- citation, copyright, and source-governance policy
- migration plans for moving canonical authority out of `docs/design`

Do not use this directory for:

- copied IBM PDFs, manuals, HTML mirrors, EPUBs, screenshots, or datasets
- long quotations from external documents
- substitute documentation that would let a reader avoid the external source
- implementation code
- MFOS requirements without requirement IDs
- compatibility, conformance, certification, affiliation, or product-support
  claims about external vendors

## Authority Model

`sources/registry.yml` and `sources/source-grounding-index.yml` define the
current bridge authority. The short version is:

1. `docs/design/source-matrix` is canonical today.
2. `sources/` is the public-safe workbench and future home.
3. `_cache/` is an ignored local cache for retrieval manifests and temporary
   research artifacts only.
4. No external source document is committed to this repository.
5. No card in `sources/` becomes normative until an ADR names it as canonical
   and migration checks confirm parity with the current Source Matrix.

## IBM and Public Sources

IBM and other public sources may be retrieved only for research. Commit only
metadata, short paraphrased mappings, source IDs, URLs, product/publication
identity, retrieval dates, review topics, divergence notes, prohibited
inferences, and legal-control flags.

Downloaded source material belongs outside git or in ignored cache paths while
being reviewed. Cache manifests may record retrieval facts, checksums, and
review disposition; they must not embed copied source text or source documents.
