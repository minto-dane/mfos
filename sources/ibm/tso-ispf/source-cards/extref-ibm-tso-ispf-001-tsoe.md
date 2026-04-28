---
source_id: EXTREF-IBM-ZOS-TSO-E-INTRODUCTION-0001
legacy_source_ids: []
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: IBM z/OS TSO/E and ISPF
document_title: TSO/E General Functions
document_url:
- https://www.ibm.com/docs/en/zos/3.2.0?topic=guide-general-tsoe-functions
retrieved_at: '2026-04-28'
authority_status: preparatory_until_adr_migration
reference_purpose:
- source discovery
- concept mapping
- non-compatibility boundary definition
- requirement traceability
review_topics:
- interactive session boundary
- panel workflow boundary
- operator bypass prevention
mfos_mapping:
  mfos_components:
  - command-processor
  - panel-ui
  mfos_specs:
  - docs/design/specs/20-command-processor.md
  - docs/design/specs/21-panel-ui.md
  mfos_requirements:
  - MFOS-REQ-COMMAND-0001
  - MFOS-REQ-PANEL-0001
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

# EXTREF-IBM-ZOS-TSO-E-INTRODUCTION-0001 - TSO/E General Functions

Source: IBM Documentation  
URL: https://www.ibm.com/docs/en/zos/3.2.0?topic=guide-general-tsoe-functions  
Accessed: 2026-04-28

## Public-Safe Summary

IBM documents TSO/E as a z/OS base element that allows interactive work with the system, including communication, program development, data processing, and MVS access.

## MFOS Use

- Use this reference to ground TSO/E as an external interactive session and command environment.
- Treat TSO/E user identity, session state, and command behavior as external adapter context.

## Do Not Import

- Command syntax.
- Exit interfaces.
- LOGON procedure examples.
- Messages or prompts.

