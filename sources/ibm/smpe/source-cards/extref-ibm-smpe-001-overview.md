---
source_id: EXTREF-IBM-ZOS-SMPE-OVERVIEW-0001
legacy_source_ids: []
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: IBM z/OS SMP/E
document_title: SMP/E Overview
document_url:
- https://www.ibm.com/docs/en/zos/3.2.0?topic=zos-smpe
retrieved_at: '2026-04-28'
authority_status: preparatory_until_adr_migration
reference_purpose:
- source discovery
- concept mapping
- non-compatibility boundary definition
- requirement traceability
review_topics:
- software inventory
- maintenance zones
- security update advisory boundary
mfos_mapping:
  mfos_components:
  - uvsd
  - supply-chain
  mfos_specs:
  - docs/design/specs/13-update.md
  mfos_requirements:
  - MFOS-REQ-UPDATE-0001
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

# EXTREF-IBM-ZOS-SMPE-OVERVIEW-0001 - SMP/E Overview

Source: IBM Documentation
URL: https://www.ibm.com/docs/en/zos/3.2.0?topic=zos-smpe
Accessed: 2026-04-28

## Public-Safe Summary

IBM describes z/OS SMP/E as a tool for installing and maintaining software and managing the inventory of installed software.

## MFOS Use

- Use this reference to ground SMP/E as the external software installation and maintenance inventory authority on z/OS.
- MFOS may track desired software state or observed installed-product facts independently of SMP/E processing.

## Do Not Import

- SMP/E command syntax.
- Reports or return-code tables.
- Messages.
- MCS statement details.
