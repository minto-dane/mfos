---
source_id: EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001
legacy_source_ids: []
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: IBM z/OS
document_title: SECINT HOLDDATA is now available with SMP/E RECEIVE ORDER
document_url:
  - https://www.ibm.com/support/pages/secint-holddata-now-available-smpe-receive-order
retrieved_at: "2026-04-27"
authority_status: preparatory_until_adr_migration
citation_scope: metadata_only_public_safe_reference
retrieval_metadata:
  retrieved_at: "2026-04-27"
  retrieved_by: MFOS source-grounding audit
  public_url: https://www.ibm.com/support/pages/secint-holddata-now-available-smpe-receive-order
  source_version: IBM Support page; release not pinned in URL
  section_scope: security advisory metadata and receive-order update topic
  local_cache_manifest: sources/_cache/retrieval-manifest.local.yml
cache_disposition: no_local_cache
reference_purpose:
  - source discovery
  - concept mapping
  - non-compatibility boundary definition
  - independent MFOS design traceability
review_topics:
  - security advisory metadata
  - update advisory workflow
  - maintenance metadata separation
mfos_mapping:
  mfos_components:
    - uvsd advisory metadata
    - security_epoch
    - update policy bundle
  mfos_specs:
    - docs/design/specs/13-update.md
  mfos_requirements:
    - MFOS-REQ-UPDATE-0004
    - MFOS-REQ-UPDATE-0008
    - MFOS-REQ-QUALITY-0006
mfos_divergence:
  - MFOS does not implement the referenced update tooling.
  - MFOS uses independently specified update metadata, security epochs, and signed provenance.
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
  - source_id: EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001
    source_type: external_reference
    role: card_subject
requirement_refs:
  - MFOS-REQ-UPDATE-0004
  - MFOS-REQ-UPDATE-0008
  - MFOS-REQ-QUALITY-0006
review_status: draft
---

# Security Advisory Metadata Reference

This workbench card is public-safe metadata only. It records update-advisory
source identity without importing external tooling behavior.
