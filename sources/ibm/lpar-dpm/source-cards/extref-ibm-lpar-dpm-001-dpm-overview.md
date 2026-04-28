---
source_id: EXTREF-IBM-Z-DPM-OVERVIEW-0001
legacy_source_ids: []
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: IBM Z partition management
document_title: Dynamic Partition Manager Overview
document_url:
- https://www.ibm.com/docs/en/systems-hardware/zsystems/3932-A02?topic=management-dynamic-partition-manager-dpm
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

# EXTREF-IBM-Z-DPM-OVERVIEW-0001 - Dynamic Partition Manager Overview

Source: IBM Documentation
URL: https://www.ibm.com/docs/en/systems-hardware/zsystems/3932-A02?topic=management-dynamic-partition-manager-dpm
Accessed: 2026-04-28

## Public-Safe Summary

IBM describes Dynamic Partition Manager as an HMC-centered management model for IBM zSystems that builds on PR/SM logical partitioning and integrates partition, I/O, network, storage, resource adjustment, monitoring, and automation capabilities.

## MFOS Use

- Use this reference to ground DPM as an external hardware and partition-management authority.
- Treat DPM objects as external resources discovered or controlled by an adapter.

## Do Not Import

- HMC Web Services API schemas.
- Request or response payloads.
- Operation lists beyond high-level object categories.
- Role or authorization procedures.
