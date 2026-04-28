---
source_id: EXTREF-IBM-ZOS-JES-JOB-CONTROL-0001
legacy_source_ids: []
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: IBM z/OS JES
document_title: JCL And JECL Boundary
document_url:
- https://www.ibm.com/docs/en/zos/3.2.0?topic=statements-jcl
- https://www.ibm.com/docs/en/zos/3.2.0?topic=ijcs-jecl-statements
retrieved_at: '2026-04-28'
authority_status: preparatory_until_adr_migration
reference_purpose:
- source discovery
- concept mapping
- non-compatibility boundary definition
- requirement traceability
review_topics:
- batch job lifecycle
- spool boundary
- job-control boundary risk
mfos_mapping:
  mfos_components:
  - jobd
  - spoold
  - operatord
  mfos_specs:
  - docs/design/specs/09-job-spool.md
  - docs/design/specs/10-operator-console.md
  mfos_requirements:
  - MFOS-REQ-JOB-0001
  - MFOS-REQ-SPOOL-0001
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

# EXTREF-IBM-ZOS-JES-JOB-CONTROL-0001 - JCL And JECL Boundary

Sources: IBM Documentation
URLs:

- https://www.ibm.com/docs/en/zos/3.2.0?topic=statements-jcl
- https://www.ibm.com/docs/en/zos/3.2.0?topic=ijcs-jecl-statements

Accessed: 2026-04-28

## Public-Safe Summary

IBM documents JCL as the job-control language used to describe batch work and JES-related processing attributes. IBM separately documents job-entry control language material for JES-specific control.

## MFOS Use

- Use this card only to justify that batch workload definitions and JES control metadata are external inputs with platform-specific meaning.
- Store MFOS job specifications in MFOS-owned form.
- If an adapter emits z/OS batch material, keep that generation boundary explicit and versioned.

## Compatibility-Risk Wording

Say that real JES interpretation depends on IBM z/OS level, JES type, installation exits, security configuration, and local policy.

## Do Not Import

- Statement lists.
- Parameter syntax.
- Examples.
- JES2 or JES3 command forms.
