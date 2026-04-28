---
source_id: EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001
legacy_source_ids: []
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: IBM z/OS
document_title: z/OS UNIX System Services library
document_url:
  - https://www.ibm.com/docs/en/zos/latest?topic=zos-unix-system-services
retrieved_at: "2026-04-27"
authority_status: preparatory_until_adr_migration
citation_scope: metadata_only_public_safe_reference
retrieval_metadata:
  retrieved_at: "2026-04-27"
  retrieved_by: MFOS source-grounding audit
  public_url: https://www.ibm.com/docs/en/zos/latest?topic=zos-unix-system-services
  source_version: z/OS documentation library page; exact release must be confirmed during review
  section_scope: optional UNIX-like subsystem bibliography
  local_cache_manifest: sources/_cache/retrieval-manifest.local.yml
cache_disposition: no_local_cache
reference_purpose:
  - source discovery
  - concept mapping
  - non-compatibility boundary definition
  - independent MFOS design traceability
review_topics:
  - UNIX commands
  - file-system interface
  - callable services
  - planning guidance
mfos_mapping:
  mfos_components:
    - optional POSIX command/API review
    - non-primary UNIX subsystem scope
  mfos_specs:
    - docs/design/specs/18-linux-gateway.md
  mfos_requirements:
    - MFOS-REQ-SOURCE-0001
    - MFOS-REQ-SOURCE-0003
mfos_divergence:
  - MFOS does not make UNIX services the primary operating model.
  - Any POSIX-like subsystem remains optional and must not bypass MFOS dataset, authorization, or audit semantics.
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
  - source_id: EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001
    source_type: external_reference
    role: card_subject
requirement_refs:
  - MFOS-REQ-SOURCE-0001
  - MFOS-REQ-SOURCE-0003
review_status: draft
---

# Optional UNIX Services Library Reference

This workbench card is public-safe metadata only. It records why UNIX-like
interfaces remain optional and non-primary in MFOS.
