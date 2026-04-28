# Citation Policy

Source Cards are public-safe bibliographic and traceability records. They store
source identity metadata such as URLs, publication numbers, retrieval dates,
version or section scope, review topics, MFOS mappings, divergence notes,
prohibited inferences, and legal controls.

Until an accepted ADR migrates source-card authority, citations in normative
MFOS design material must resolve through `docs/design/source-matrix`. Records
under `sources/` may prepare or cross-index those citations, but they are not
the source of record.

Source Cards must not store copied source documents, long quotations, detailed
summaries, substitute documentation, copied tables, diagrams, record layouts,
command syntax, macro signatures, message tables, or other material that would
let the card replace the external source.

Every z/OS-inspired MFOS concept must cite a Source Matrix ID before it becomes
normative.

Concept cards must separate:

- external source terms used for bibliographic traceability
- short public-safe paraphrases of the reviewed concept
- MFOS-owned terms and requirements
- divergence from the external source
- prohibited inferences, including compatibility or affiliation claims

For IBM and other public sources, cite the public landing page or official
documentation URL, the document title, product or publication identity, version
or section scope when known, and retrieval date. Do not cite a local cached
copy as the authority; local cache entries are temporary research aids only.

External product, project, organization, and specification names are used only
for bibliographic reference, source discovery, non-compatibility boundary
definition, and independent MFOS design traceability. Source Cards that use an
external mark must set `vendor_mark_used: true` and
`legal_controls.trademark_reference_only: true`, while keeping affiliation,
compatibility, conformance, certification, and source-substitution claims false.

Citation review must fail closed when a source record:

- lacks a stable public URL or retrieval note
- omits divergence or prohibited-inference fields
- stores copied source text beyond a short fair-use citation needed for
  identification
- reads like a replacement manual
- implies MFOS implements, emulates, certifies against, or is supported by an
  external vendor product
