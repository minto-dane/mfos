---
source_id: EXTREF-IBM-ZOS-WLM-OVERVIEW-0001
legacy_source_ids: []
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: IBM z/OS workload management
document_title: MVS Workload Management
document_url:
- https://www.ibm.com/docs/en/zos/3.2.0?topic=management-what-is-mvs-workload
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

# EXTREF-IBM-ZOS-WLM-OVERVIEW-0001 - MVS Workload Management

Source: IBM Documentation  
URL: https://www.ibm.com/docs/en/zos/3.2.0?topic=management-what-is-mvs-workload  
Accessed: 2026-04-28

## Public-Safe Summary

IBM describes z/OS workload management as a policy-driven facility that uses business-oriented performance goals and importance to guide system resource management and reporting.

## MFOS Use

- Use this reference to ground the external idea of goal-oriented workload management.
- Keep MFOS scheduling, admission, and prioritization rules separate from IBM WLM resource-management behavior.

## Compatibility-Risk Wording

WLM can only meet goals when resources are available; MFOS should not promise that a workload category maps to an achieved z/OS WLM outcome.

## Do Not Import

- WLM commands.
- Service definition exports.
- Report data structures.
- Callable-service details.

