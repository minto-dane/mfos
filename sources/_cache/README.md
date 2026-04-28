# sources/_cache/

Ignored local cache for retrieval manifests and temporary external-source
research artifacts.

Only these policy files are committed:

- `sources/_cache/README.md`
- `sources/_cache/DO_NOT_COMMIT.md`

All other files in this directory are ignored local scratch files. They may be
used while reviewing IBM or other public sources, but they are not repository
artifacts and must not become source authority.

Allowed local-only cache content:

- retrieval manifests
- checksum manifests
- short review disposition notes without copied source text
- temporary downloads needed to verify public metadata

Do not commit:

- downloaded PDFs
- HTML mirrors
- EPUBs
- screenshots
- copied excerpts
- copied tables, diagrams, command syntax, macro signatures, message catalogs,
  record layouts, or examples
- archives of public documentation

Committed source grounding belongs in public-safe metadata files such as
`sources/retrieval-log.yml`, Source Cards, Concept Cards, and the current
canonical `docs/design/source-matrix` records.
