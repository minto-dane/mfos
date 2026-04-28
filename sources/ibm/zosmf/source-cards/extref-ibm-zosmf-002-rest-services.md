---
source_id: EXTREF-IBM-ZOS-MANAGEMENT-FACILITY-REST-SERVICES-0001
legacy_source_ids: []
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: IBM z/OSMF
document_title: z/OSMF REST Services
document_url:
- https://www.ibm.com/docs/en/zos/3.2.0?topic=guide-using-zosmf-rest-services
- https://www.ibm.com/docs/en/zos/3.2.0?topic=services-zos-data-set-file-rest-interface
- https://www.ibm.com/docs/en/zos/3.2.0?topic=services-zos-jobs-rest-interface
retrieved_at: '2026-04-28'
authority_status: preparatory_until_adr_migration
reference_purpose:
- source discovery
- concept mapping
- non-compatibility boundary definition
- requirement traceability
review_topics:
- management API boundary
- operator/API authorization
- non-compatibility boundary
mfos_mapping:
  mfos_components:
  - management-api
  mfos_specs:
  - docs/design/specs/22-management-api.md
  mfos_requirements:
  - MFOS-REQ-MGMTAPI-0001
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

# EXTREF-IBM-ZOS-MANAGEMENT-FACILITY-REST-SERVICES-0001 - z/OSMF REST Services

Sources: IBM Documentation
URLs:

- https://www.ibm.com/docs/en/zos/3.2.0?topic=guide-using-zosmf-rest-services
- https://www.ibm.com/docs/en/zos/3.2.0?topic=services-zos-data-set-file-rest-interface
- https://www.ibm.com/docs/en/zos/3.2.0?topic=services-zos-jobs-rest-interface

Accessed: 2026-04-28

## Public-Safe Summary

IBM documents z/OSMF REST services as secured HTTP APIs for working with z/OS resources. IBM documents service areas including data sets, UNIX files, file systems, and jobs.

## MFOS Use

- Use this reference to ground z/OSMF as an external management API surface.
- Keep REST request construction, authentication, authorization, and response parsing in adapters.

## Compatibility-Risk Wording

z/OSMF operations depend on configured services, authenticated identities, SAF authorization, z/OS level, JES type, and local setup. MFOS should treat failures and unavailable functions as normal external outcomes.

## Do Not Import

- REST paths or endpoint syntax.
- Header names and examples.
- JSON schemas.
- Sample requests or responses.
