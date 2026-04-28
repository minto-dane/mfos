---
source_id: EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001
legacy_source_ids: []
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: IBM z/OS
document_title: Controlling cross-memory communication
document_url:
  - https://www.ibm.com/docs/en/zos-basic-skills?topic=integrity-controlling-cross-memory-communication
retrieved_at: "2026-04-27"
authority_status: preparatory_until_adr_migration
citation_scope: metadata_only_public_safe_reference
retrieval_metadata:
  retrieved_at: "2026-04-27"
  retrieved_by: MFOS source-grounding audit
  public_url: https://www.ibm.com/docs/en/zos-basic-skills?topic=integrity-controlling-cross-memory-communication
  source_version: z/OS Basic Skills documentation path; release not pinned in URL
  section_scope: cross-memory communication control topic
  local_cache_manifest: sources/_cache/retrieval-manifest.local.yml
cache_disposition: no_local_cache
reference_purpose:
  - source discovery
  - concept mapping
  - non-compatibility boundary definition
  - independent MFOS design traceability
review_topics:
  - cross-memory authority
  - address-space isolation
  - common area risk
  - security controls
mfos_mapping:
  mfos_components:
    - cross-service buffer control
    - pointer rejection
    - copy-in/copy-out discipline
  mfos_specs:
    - docs/design/specs/03-system-integrity.md
    - docs/design/specs/15-svc-pcall.md
  mfos_requirements:
    - MFOS-REQ-SYSINT-0007
    - MFOS-REQ-SYSINT-0008
    - MFOS-REQ-SYSINT-0009
mfos_divergence:
  - MFOS must not expose arbitrary cross-address-space pointer access in early phases.
  - MFOS independently specifies any future cross-service buffer model.
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
  - source_id: EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001
    source_type: external_reference
    role: card_subject
requirement_refs:
  - MFOS-REQ-SYSINT-0007
  - MFOS-REQ-SYSINT-0008
  - MFOS-REQ-SYSINT-0009
review_status: draft
---

# Cross-Memory Control Reference

This workbench card is public-safe metadata only. It records source identity,
MFOS mapping, divergence, and prohibited inference. It is not external
documentation and is not canonical until a source-layout ADR says otherwise.
