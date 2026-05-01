# Source Scaffold Audit

Canonical Source Matrix: `docs/design/source-matrix/source-matrix.yml`

Canonical Source Cards: `docs/design/source-matrix/cards/`

Top-level `source-matrix/` is a bridge. Top-level `sources/` is planned source/concept-card scaffold and is largely empty. This is not a Phase 1 blocker because current Source Cards are populated and validated under `docs/design/source-matrix/`.

Source card count: `37`

Removed public-safe fields found in current Source Cards: `0`

Private cache controls:

- `reference-cache/README.md`
- `reference-cache/.gitignore`
- `sources/_cache/README.md`
- `sources/_cache/DO_NOT_COMMIT.md`

Recommended action: keep `sources/` planned until an ADR promotes or removes it. Do not place copied external documents there.
