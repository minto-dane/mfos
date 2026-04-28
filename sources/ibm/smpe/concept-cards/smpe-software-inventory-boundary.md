---
concept_id: SRC-WB-CONCEPT-SMPE-SOFTWARE-INVENTORY-BOUNDARY-0001
source_ids:
- EXTREF-IBM-ZOS-SMPE-OVERVIEW-0001
- EXTREF-IBM-ZOS-SMPE-ZONES-0001
status: draft
authority_status: preparatory_until_adr_migration
summary_scope: public_safe_mfos_mapping
mfos_terms:
- uvsd
- supply-chain
mfos_mapping:
  mfos_specs:
  - docs/design/specs/13-update.md
  mfos_requirements:
  - MFOS-REQ-UPDATE-0001
prohibited_inference:
- Do not treat this concept card as external documentation.
- Do not infer external compatibility from MFOS concept names.
review_status: draft
---

# SMP/E Software Inventory Boundary

## Concept

SMP/E is the external z/OS software installation, service, and inventory-management authority.

## MFOS Semantics

MFOS may model desired software, discovered products, update intent, and maintenance evidence. These are not equivalent to SMP/E CSI contents.

## Compatibility-Risk Wording

Use cautious language:

- "MFOS can record an observed SMP/E zone reference as external evidence."
- "SMP/E APPLY or ACCEPT state must be verified by the external system."
- "MFOS software inventory does not replace the SMP/E CSI."

Avoid saying:

- "MFOS validates SMP/E requisites."
- "MFOS reproduces SMP/E inventory."
- "MFOS can derive service status from product names alone."

