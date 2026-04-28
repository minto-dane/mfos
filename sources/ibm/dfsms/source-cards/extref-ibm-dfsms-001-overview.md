---
source_id: EXTREF-IBM-ZOS-DFSMS-OVERVIEW-0001
legacy_source_ids: []
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: IBM z/OS DFSMS
document_title: DFSMS Family Overview
document_url:
- https://www.ibm.com/docs/en/zos/3.2.0?topic=zos-dfsms
retrieved_at: '2026-04-28'
authority_status: preparatory_until_adr_migration
reference_purpose:
- source discovery
- concept mapping
- non-compatibility boundary definition
- requirement traceability
review_topics:
- dataset/catalog boundary
- storage-management policy
- data lifecycle
mfos_mapping:
  mfos_components:
  - catalogd
  - datasetd
  mfos_specs:
  - docs/design/specs/08-dataset-catalog.md
  mfos_requirements:
  - MFOS-REQ-CATALOG-0001
  - MFOS-REQ-DATASET-0001
mfos_divergence:
- MFOS behavior is independently specified in MFOS-owned specs.
- This source card does not import external interfaces, record layouts, command syntax,
  or product behavior.
- External marks are used only for bibliographic reference and source discovery.
prohibited_inference:
- Do not claim compatibility with the referenced external system.
- Do not reproduce external documentation text, tables, record layouts, command syntax,
  or macro interfaces.
- Do not use this source card as a substitute for external documentation.
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
review_status: draft
---

# EXTREF-IBM-ZOS-DFSMS-OVERVIEW-0001 - DFSMS Family Overview

Source: IBM Documentation  
URL: https://www.ibm.com/docs/en/zos/3.2.0?topic=zos-dfsms  
Accessed: 2026-04-28

## Public-Safe Summary

IBM documents DFSMS as a z/OS storage-management family that includes DFSMSdfp as a base element and optional features for data movement, hierarchical storage management, removable media, and transactional VSAM services.

## MFOS Use

- Use this reference to identify DFSMS as the external storage-management domain that owns policy, placement, migration, backup, and media-management concepts on z/OS.
- Model MFOS storage behavior with MFOS-owned abstractions; do not imply that MFOS reproduces IBM component internals.

## Do Not Import

- Command syntax.
- Utility option lists.
- Control-block, record-layout, or macro details.
- Message identifiers or message text.

