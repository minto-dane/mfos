---
source_id: EXTREF-IBM-ZOS-SDSF-SECURITY-0001
legacy_source_ids: []
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: IBM z/OS SDSF
document_title: SDSF Security Boundary
document_url:
- https://www.ibm.com/docs/en/zos/3.2.0?topic=time-set-up-sdsf-server-security
- https://www.ibm.com/docs/en/zos/3.2.0?topic=resources-protecting-sdsf-function
retrieved_at: '2026-04-28'
authority_status: preparatory_until_adr_migration
reference_purpose:
- source discovery
- concept mapping
- non-compatibility boundary definition
- requirement traceability
review_topics:
- operations display boundary
- authority mediation
- panel/UI divergence
mfos_mapping:
  mfos_components:
  - operatord
  - panel-ui
  mfos_specs:
  - docs/design/specs/10-operator-console.md
  - docs/design/specs/21-panel-ui.md
  mfos_requirements:
  - MFOS-REQ-OPER-0001
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

# EXTREF-IBM-ZOS-SDSF-SECURITY-0001 - SDSF Security Boundary

Sources: IBM Documentation
URLs:

- https://www.ibm.com/docs/en/zos/3.2.0?topic=time-set-up-sdsf-server-security
- https://www.ibm.com/docs/en/zos/3.2.0?topic=resources-protecting-sdsf-function

Accessed: 2026-04-28

## Public-Safe Summary

IBM documents SDSF security as SAF-based. SDSF checks resources in SDSF and other SAF classes depending on the panel, object, or action involved.

## MFOS Use

- Use this reference to ground SDSF access as external authorization-controlled behavior.
- MFOS should store only high-level authorization outcomes or diagnostics, not SAF resource recipes.

## Compatibility-Risk Wording

An SDSF function can require authority to multiple external resources. MFOS should not infer availability from panel visibility alone.

## Do Not Import

- SAF resource names.
- RACF examples.
- Access-level matrices.
- Security trace command forms.
