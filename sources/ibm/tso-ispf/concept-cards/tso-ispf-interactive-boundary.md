---
concept_id: SRC-WB-CONCEPT-TSO-ISPF-INTERACTIVE-BOUNDARY-0001
source_ids:
- EXTREF-IBM-ZOS-TSO-E-INTRODUCTION-0001
- EXTREF-IBM-ZOS-ISPF-INTRODUCTION-0001
status: draft
authority_status: preparatory_until_adr_migration
summary_scope: public_safe_mfos_mapping
mfos_terms:
- command-processor
- panel-ui
mfos_mapping:
  mfos_specs:
  - docs/design/specs/20-command-processor.md
  - docs/design/specs/21-panel-ui.md
  mfos_requirements:
  - MFOS-REQ-COMMAND-0001
  - MFOS-REQ-PANEL-0001
prohibited_inference:
- Do not treat this concept card as external documentation.
- Do not infer external compatibility from MFOS concept names.
review_status: draft
---

# TSO/E And ISPF Interactive Boundary

## Concept

TSO/E provides an interactive z/OS session environment, and ISPF provides panel-driven dialogs and development utilities commonly used within that environment.

## MFOS Semantics

MFOS may model an interactive session request, user context, terminal action, or external command invocation. These do not imply TSO/E or ISPF compatibility unless an adapter explicitly provides it.

## Compatibility-Risk Wording

Use cautious language:

- "MFOS can reference TSO/E or ISPF as external execution contexts."
- "Command handling, case behavior, and panel behavior are external and installation-specific."
- "MFOS does not store or validate ISPF panel definitions or TSO/E exit behavior."

Avoid saying:

- "MFOS implements TSO/E."
- "MFOS commands are ISPF commands."
- "MFOS sessions are equivalent to TSO/E sessions."

