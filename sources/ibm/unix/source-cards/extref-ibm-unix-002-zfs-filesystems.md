---
source_id: EXTREF-IBM-ZOS-UNIX-FILE-SYSTEMS-0001
legacy_source_ids: []
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: IBM z/OS UNIX System Services
document_title: zFS File Systems
document_url:
- https://www.ibm.com/docs/en/zos/3.2.0?topic=zos-file-system-zfs
retrieved_at: '2026-04-28'
authority_status: preparatory_until_adr_migration
reference_purpose:
- source discovery
- concept mapping
- non-compatibility boundary definition
- requirement traceability
review_topics:
- optional POSIX boundary
- file-system boundary
- host semantics divergence
mfos_mapping:
  mfos_components:
  - posix-subsystem
  - linux-gateway
  mfos_specs:
  - docs/design/specs/19-posix-subsystem.md
  - docs/design/specs/18-linux-gateway.md
  mfos_requirements:
  - MFOS-REQ-POSIX-0001
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

# EXTREF-IBM-ZOS-UNIX-FILE-SYSTEMS-0001 - zFS File Systems

Source: IBM Documentation
URL: https://www.ibm.com/docs/en/zos/3.2.0?topic=zos-file-system-zfs
Accessed: 2026-04-28

## Public-Safe Summary

IBM documents zFS as a z/OS UNIX file system whose mounted file systems contain files and directories accessible through z/OS UNIX APIs and can participate in the z/OS UNIX hierarchy.

## MFOS Use

- Use this reference to ground zFS as an external file-system implementation.
- Treat mount state, access control, and file-system attributes as external facts observed through system APIs or adapters.

## Compatibility-Risk Wording

MFOS path semantics should not assume that zFS mount topology, encoding behavior, or authorization behavior matches distributed UNIX systems.

## Do Not Import

- File-system creation syntax.
- Administration command options.
- Message identifiers or message text.
- Internal aggregate structures.
