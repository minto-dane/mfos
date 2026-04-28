---
source_id: EXTREF-IBM-ZOS-DFSMS-STORAGE-MANAGEMENT-0001
legacy_source_ids: []
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: IBM z/OS DFSMS
document_title: SMS Policy Model
document_url:
- https://www.ibm.com/docs/en/zos/3.2.0?topic=dfsms-storage-management-subsystem-sms
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

# EXTREF-IBM-ZOS-DFSMS-STORAGE-MANAGEMENT-0001 - SMS Policy Model

Source: IBM Documentation  
URL: https://www.ibm.com/docs/en/zos/3.2.0?topic=dfsms-storage-management-subsystem-sms  
Accessed: 2026-04-28

## Public-Safe Summary

IBM describes SMS as a DFSMS facility for centralized external-storage management according to an active storage-management policy. IBM also describes ISMF as the interactive interface for defining SMS configurations and related class-selection routines.

## MFOS Use

- Use this reference to ground terms such as SMS, storage policy, SMS configuration, and class selection at a conceptual level.
- Represent MFOS storage policy as independent metadata and decision logic.
- When discussing interoperability risk, say that IBM SMS policy remains authoritative for real z/OS allocation and management outcomes.

## Do Not Import

- ACS routine source, pseudo-code, or generated object details.
- SAF profile names beyond broad security-boundary discussion.
- Data-set allocation syntax or examples.

