# packs/

This top-level directory is a bridge and review aid. It is not the canonical
pack namespace. Current canonical pack contracts remain under
[docs/design/packs/](../docs/design/packs/) until an ADR changes ownership.

`pack-index.yml` is a bridge projection for validators and traceability tools.
AI work packets should be created here only when a reviewed implementation gate
authorizes work packet creation. Current pack definitions and split guidance are
in [docs/design/packs/PACKS.md](../docs/design/packs/PACKS.md).

Each pack must identify source IDs, requirement IDs, failure modes, audit
obligations, positive tests, negative tests, fuzz targets, and spec gaps.
