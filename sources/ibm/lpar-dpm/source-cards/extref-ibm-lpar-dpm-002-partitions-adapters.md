---
source_id: EXTREF-IBM-Z-DPM-PARTITIONS-ADAPTERS-0001
legacy_source_ids: []
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: IBM Z partition management
document_title: DPM Partitions And Adapters
document_url:
- https://www.ibm.com/docs/en/help-ibm-hmc-z17?topic=dpm-partitions-systems
- https://www.ibm.com/docs/en/help-ibm-hmc-z17?topic=dpm-adapters-systems-partitions
retrieved_at: '2026-04-28'
authority_status: preparatory_until_adr_migration
reference_purpose:
- source discovery
- concept mapping
- non-compatibility boundary definition
- requirement traceability
review_topics:
- partition object model
- resource assignment
- management-plane divergence
mfos_mapping:
  mfos_components:
  - pxm
  mfos_specs:
  - docs/design/specs/16-partition-manager.md
  mfos_requirements:
  - MFOS-REQ-PARTITION-0001
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

# EXTREF-IBM-Z-DPM-PARTITIONS-ADAPTERS-0001 - DPM Partitions And Adapters

Sources: IBM Documentation
URLs:

- https://www.ibm.com/docs/en/help-ibm-hmc-z17?topic=dpm-partitions-systems
- https://www.ibm.com/docs/en/help-ibm-hmc-z17?topic=dpm-adapters-systems-partitions

Accessed: 2026-04-28

## Public-Safe Summary

IBM documents DPM partitions as virtual representations of hardware resources for workloads. IBM also documents adapters as network, storage, or cryptographic resources used by partitions.

## MFOS Use

- Use this reference to ground partition, processor, memory, network, storage, and crypto resource concepts.
- Keep MFOS topology and capacity records independent from live HMC state.

## Compatibility-Risk Wording

Partition startability, resource attachment, and adapter availability are external DPM/HMC facts and can vary by system, authorization, configuration, and hardware level.

## Do Not Import

- Task sequences.
- Adapter feature tables.
- API object schemas.
- Configuration examples.
