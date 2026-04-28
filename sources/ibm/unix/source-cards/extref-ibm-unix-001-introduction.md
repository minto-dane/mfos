---
source_id: EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001
legacy_source_ids: []
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: IBM z/OS UNIX System Services
document_title: z/OS UNIX Introduction
document_url:
- https://www.ibm.com/docs/en/zos/3.2.0?topic=planning-introduction-zos-unix
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

# EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001 - z/OS UNIX Introduction

Source: IBM Documentation
URL: https://www.ibm.com/docs/en/zos/3.2.0?topic=planning-introduction-zos-unix
Accessed: 2026-04-28

## Public-Safe Summary

IBM describes z/OS UNIX as a UNIX operating environment implemented within z/OS. It provides open-system APIs and an interactive shell interface while integrating with z/OS services and security.

## MFOS Use

- Use this reference to ground z/OS UNIX as an external environment for files, directories, shells, processes, and APIs.
- Keep MFOS file and process abstractions portable unless an adapter explicitly targets z/OS UNIX.

## Do Not Import

- Callable service signatures.
- Shell command syntax.
- Security setup commands.
- Error-code tables.
