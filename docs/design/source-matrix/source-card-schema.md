# MFOS Source Card Schema v0.6

Status: draft

Source Cards are public-safe bibliographic and traceability records. They are
not copies, summaries, record-layout databases, command references, macro
references, or substitutes for external documentation.

## Required Shape

```yaml
source_id: EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001
legacy_source_ids:
  - IBM-SMF-001
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: "IBM z/OS"
document_title: "Introduction to SMF"
document_url:
  - https://www.ibm.com/docs/...
retrieved_at: "2026-04-27"

reference_purpose:
  - source discovery
  - concept mapping
  - non-compatibility boundary definition
  - independent MFOS design traceability

review_topics:
  - audit evidence
  - system activity recording

mfos_mapping:
  mfos_components:
    - auditd
  mfos_specs:
    - docs/design/specs/07-audit.md
  mfos_requirements:
    - MFOS-REQ-AUDIT-0001

mfos_divergence:
  - "MFOS auditd is independently specified."
  - "MFOS does not claim compatibility with the referenced external system."

prohibited_inference:
  - "Do not claim compatibility with the referenced external system."
  - "Do not reproduce external record layouts."
  - "Do not reproduce external documentation text."
  - "Do not treat this card as external documentation."

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
```

## Removed Public Fields

The following fields are prohibited in Source Cards:

- `canonical_concepts`
- `normative_source`
- `detailed_summary`
- `source_summary`
- `copied_excerpt`
- `record_layouts`
- `command_syntax`
- `macro_signatures`

Use `review_topics` for short review labels and `mfos_mapping` for MFOS
traceability only.
