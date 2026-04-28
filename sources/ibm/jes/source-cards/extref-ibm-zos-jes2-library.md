---
source_id: EXTREF-IBM-ZOS-JES2-LIBRARY-0001
legacy_source_ids: []
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: IBM z/OS
document_title: z/OS JES2 library
document_url:
  - https://www.ibm.com/docs/en/zos/3.2.0?topic=zos-jes2
retrieved_at: "2026-04-27"
authority_status: preparatory_until_adr_migration
citation_scope: metadata_only_public_safe_reference
retrieval_metadata:
  retrieved_at: "2026-04-27"
  retrieved_by: MFOS source-grounding audit
  public_url: https://www.ibm.com/docs/en/zos/3.2.0?topic=zos-jes2
  source_version: z/OS 3.2.0 library page
  section_scope: job and spool operations reference index
  local_cache_manifest: not_committed; see sources/_cache/README.md
cache_disposition: no_local_cache
reference_purpose:
  - source discovery
  - concept mapping
  - non-compatibility boundary definition
  - independent MFOS design traceability
review_topics:
  - job subsystem commands
  - initialization and tuning references
  - messages
  - job and spool operations
mfos_mapping:
  mfos_components:
    - jobd
    - spoold
    - operatord
  mfos_specs:
    - docs/design/specs/09-job-spool.md
    - docs/design/specs/10-operator-console.md
  mfos_requirements:
    - MFOS-REQ-JOB-0002
    - MFOS-REQ-OPER-0002
    - MFOS-REQ-OPER-0003
mfos_divergence:
  - MFOS may use external batch-processing concepts as background only.
  - MFOS job and spool interfaces are independently specified and do not claim external command compatibility.
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
  - source_id: EXTREF-IBM-ZOS-JES2-LIBRARY-0001
    source_type: external_reference
    role: card_subject
requirement_refs:
  - MFOS-REQ-JOB-0002
  - MFOS-REQ-OPER-0002
  - MFOS-REQ-OPER-0003
review_status: draft
---

# Job Subsystem Library Reference

This workbench card is public-safe metadata only. It does not import external
job-control syntax, command syntax, message tables, or spool layouts.
