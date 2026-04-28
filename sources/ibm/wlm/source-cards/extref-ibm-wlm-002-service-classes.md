---
source_id: EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001
legacy_source_ids: []
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: IBM z/OS workload management
document_title: Service Classes And Reporting
document_url:
- https://www.ibm.com/docs/en/zos/3.2.0?topic=tabs-service-classes
- https://www.ibm.com/docs/en/zos/3.2.0?topic=management-defining-report-classes
retrieved_at: '2026-04-28'
authority_status: preparatory_until_adr_migration
reference_purpose:
- source discovery
- concept mapping
- non-compatibility boundary definition
- requirement traceability
review_topics:
- service classes
- goal policy
- reporting class divergence
mfos_mapping:
  mfos_components:
  - wlmd
  - jobd
  mfos_specs:
  - docs/design/specs/11-workload-management.md
  mfos_requirements:
  - MFOS-REQ-WLM-0001
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

# EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001 - Service Classes And Reporting

Sources: IBM Documentation
URLs:

- https://www.ibm.com/docs/en/zos/3.2.0?topic=tabs-service-classes
- https://www.ibm.com/docs/en/zos/3.2.0?topic=management-defining-report-classes

Accessed: 2026-04-28

## Public-Safe Summary

IBM documents service classes as named groups of work with related performance goals, resource requirements, or business importance. IBM also documents report classes as reporting groupings that can cross service-class boundaries.

## MFOS Use

- Use service class and report class as external WLM terms.
- MFOS may store a desired workload tier, but an adapter must translate that to local WLM policy context.

## Compatibility-Risk Wording

Report grouping can affect the meaning of performance data. MFOS should distinguish observed reporting labels from scheduling intent.

## Do Not Import

- Numeric limits beyond conceptual constraints.
- Panel field definitions.
- Report formats.
- Service definition syntax.
