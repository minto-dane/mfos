# Source Grounding Remediation

Status: current

Canonical Source Cards remain under `docs/design/source-matrix/cards/` and the
canonical source index remains `docs/design/source-matrix/source-matrix.yml`.
The `sources/` tree is a public-safe workbench and does not replace the
canonical Source Matrix.

Current source grounding is structurally valid but semantically conditional:
canonical cards are draft, many card-local `mfos_mapping.mfos_specs` entries
remain empty, and fixture/golden vectors still need source-ref propagation
before semantic evaluator work.

No copied external manuals, PDFs, tables, record layouts, command syntax, macro
interfaces, or message tables were added.
