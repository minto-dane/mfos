# Citation Policy

Source Cards are public-safe bibliographic and traceability records. They store
source identity metadata such as URLs, publication numbers, retrieval dates,
version or section scope, review topics, MFOS mappings, divergence notes,
prohibited inferences, and legal controls.

Source Cards must not store copied source documents, long quotations, detailed
summaries, substitute documentation, copied tables, diagrams, record layouts,
command syntax, macro signatures, message tables, or other material that would
let the card replace the external source.

Every z/OS-inspired MFOS concept must cite a Source Matrix ID before it becomes
normative.

External product, project, organization, and specification names are used only
for bibliographic reference, source discovery, non-compatibility boundary
definition, and independent MFOS design traceability. Source Cards that use an
external mark must set `vendor_mark_used: true` and
`legal_controls.trademark_reference_only: true`, while keeping affiliation,
compatibility, conformance, certification, and source-substitution claims false.
