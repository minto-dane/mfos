---
source_id: EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001
legacy_source_ids: []
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: IBM z/OS
document_title: z/OS DFSMS library
document_url:
  - https://www.ibm.com/docs/en/zos/3.2.0?topic=zos-dfsms
retrieved_at: "2026-04-27"
authority_status: preparatory_until_adr_migration
citation_scope: metadata_only_public_safe_reference
retrieval_metadata:
  retrieved_at: "2026-04-27"
  retrieved_by: MFOS source-grounding audit
  public_url: https://www.ibm.com/docs/en/zos/3.2.0?topic=zos-dfsms
  source_version: z/OS 3.2.0 library page
  section_scope: dataset and storage management library index
  local_cache_manifest: sources/_cache/retrieval-manifest.local.yml
cache_disposition: no_local_cache
reference_purpose:
  - source discovery
  - concept mapping
  - non-compatibility boundary definition
  - independent MFOS design traceability
review_topics:
  - dataset allocation
  - dataset usage
  - catalog management
  - storage administration
  - advanced services
mfos_mapping:
  mfos_components:
    - datasetd
    - catalogd
    - Dataset
    - CatalogEntry
  mfos_specs:
    - docs/design/specs/08-dataset-catalog.md
  mfos_requirements:
    - MFOS-REQ-DATASET-0002
    - MFOS-REQ-DATASET-0003
    - MFOS-REQ-DATASET-0004
    - MFOS-REQ-DATASET-0005
mfos_divergence:
  - MFOS datasetd is a managed resource service, not an implementation of the referenced product family.
  - MFOS dataset semantics are independently specified and are not a POSIX file wrapper.
prohibited_inference:
  - Do not claim compatibility with the referenced external system.
  - Do not reproduce external documentation text, tables, record layouts, command syntax, or macro interfaces.
  - Do not treat this source card as a substitute for external documentation.
legal_controls:
  public_safe: true
  no_copied_text: true
  no_long_quotes: true
  no_tables_copied: true
  no_diagrams_copied: true
  no_record_layouts_copied: true
  no_command_syntax_copied: true
  no_macro_signatures_copied: true
  no_message_tables_copied: true
  attribution_required: true
  trademark_reference_only: true
  external_affiliation_claimed: false
  compatibility_claimed: false
  substitute_for_source: false
source_refs:
  - source_id: EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001
    source_type: external_reference
    role: card_subject
requirement_refs:
  - MFOS-REQ-DATASET-0002
  - MFOS-REQ-DATASET-0003
  - MFOS-REQ-DATASET-0004
  - MFOS-REQ-DATASET-0005
review_status: draft
---

# Dataset And Storage Management Library Reference

This workbench card is public-safe metadata only. It preserves traceability
without copying external documentation or implying compatibility.
