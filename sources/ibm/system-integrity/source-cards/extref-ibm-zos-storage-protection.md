---
source_id: EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001
legacy_source_ids: []
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: IBM z/OS
document_title: What is storage protection?
document_url:
  - https://www.ibm.com/docs/en/zos-basic-skills?topic=storage-what-is-protection
retrieved_at: "2026-04-27"
authority_status: preparatory_until_adr_migration
citation_scope: metadata_only_public_safe_reference
retrieval_metadata:
  retrieved_at: "2026-04-27"
  retrieved_by: MFOS source-grounding audit
  public_url: https://www.ibm.com/docs/en/zos-basic-skills?topic=storage-what-is-protection
  source_version: z/OS Basic Skills documentation path; release not pinned in URL
  section_scope: storage protection overview topic
  local_cache_manifest: sources/_cache/retrieval-manifest.local.yml
cache_disposition: no_local_cache
reference_purpose:
  - source discovery
  - concept mapping
  - non-compatibility boundary definition
  - independent MFOS design traceability
review_topics:
  - storage protection
  - protection-key comparison concept
  - fetch-protection concept
  - protected storage domain
mfos_mapping:
  mfos_components:
    - StorageDomain
    - typed handles
    - page-table protection policy
  mfos_specs:
    - docs/design/specs/03-system-integrity.md
    - docs/design/specs/14-nucleus.md
  mfos_requirements:
    - MFOS-REQ-SOURCE-0002
    - MFOS-REQ-SYSINT-0004
    - MFOS-REQ-NUCLEUS-0007
    - MFOS-REQ-NUCLEUS-0008
mfos_divergence:
  - MFOS does not reproduce z/Architecture storage keys on x64.
  - MFOS maps the external concept into MFOS-owned storage domains, typed handles, page-table protections, and optional hardware helpers.
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
  - source_id: EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001
    source_type: external_reference
    role: card_subject
requirement_refs:
  - MFOS-REQ-SOURCE-0002
  - MFOS-REQ-SYSINT-0004
  - MFOS-REQ-NUCLEUS-0007
  - MFOS-REQ-NUCLEUS-0008
review_status: draft
---

# Storage Protection Reference

This workbench card is public-safe metadata only. It documents divergence from
external hardware and operating-system behavior.
