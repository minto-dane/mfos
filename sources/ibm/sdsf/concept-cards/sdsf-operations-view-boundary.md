---
concept_id: SRC-WB-CONCEPT-SDSF-OPERATIONS-VIEW-BOUNDARY-0001
source_ids:
- EXTREF-IBM-ZOS-SDSF-INTRODUCTION-0001
- EXTREF-IBM-ZOS-SDSF-SECURITY-0001
status: draft
authority_status: preparatory_until_adr_migration
summary_scope: public_safe_mfos_mapping
mfos_terms:
- operatord
- panel-ui
mfos_mapping:
  mfos_specs:
  - docs/design/specs/10-operator-console.md
  - docs/design/specs/21-panel-ui.md
  mfos_requirements:
  - MFOS-REQ-OPER-0001
prohibited_inference:
- Do not treat this concept card as external documentation.
- Do not infer external compatibility from MFOS concept names.
review_status: draft
---

# SDSF Operations View Boundary

## Concept

SDSF presents operational views and controls for z/OS resources, including JES jobs and output, system resources, logs, and devices.

## MFOS Semantics

MFOS may model an operations view, row observation, user action request, and external authorization result. These are not SDSF panel internals.

## Compatibility-Risk Wording

Use cautious language:

- "MFOS can record SDSF-derived observations with source and time."
- "SDSF actions depend on SAF authorization and underlying subsystem state."
- "MFOS does not define SDSF panel behavior or command compatibility."

Avoid saying:

- "Forbidden claim: MFOS implements SDSF panels."
- "Forbidden claim: MFOS action availability equals SDSF authorization."
- "Forbidden claim: MFOS owns JES output state displayed through SDSF."
