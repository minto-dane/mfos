---
source_id: EXTREF-IBM-ZOS-SMPE-ZONES-0001
legacy_source_ids: []
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: IBM z/OS SMP/E
document_title: SMP/E Zones
document_url:
- https://www.ibm.com/docs/en/zos/3.2.0?topic=processing-target-zone-distribution-zone
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

# EXTREF-IBM-ZOS-SMPE-ZONES-0001 - SMP/E Zones

Source: IBM Documentation
URL: https://www.ibm.com/docs/en/zos/3.2.0?topic=processing-target-zone-distribution-zone
Accessed: 2026-04-28

## Public-Safe Summary

IBM documents target and distribution zones as SMP/E inventory structures used when processing installed software and distribution libraries. The global zone contains information used to locate and process those zones.

## MFOS Use

- Use this reference to ground zone terminology at a conceptual inventory level.
- Store SMP/E zone names as external adapter context or observed metadata.

## Compatibility-Risk Wording

MFOS should not infer installed software compatibility from a zone name alone. Real SMP/E state depends on the CSI and related entries.

## Do Not Import

- DD statements or allocation syntax.
- Entry layouts.
- LIST output formats.
- Processing examples.
