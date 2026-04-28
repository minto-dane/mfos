---
concept_id: SRC-WB-CONCEPT-DFSMS-STORAGE-POLICY-BOUNDARY-0001
source_ids:
- EXTREF-IBM-ZOS-DFSMS-OVERVIEW-0001
- EXTREF-IBM-ZOS-DFSMS-STORAGE-MANAGEMENT-0001
status: draft
authority_status: preparatory_until_adr_migration
summary_scope: public_safe_mfos_mapping
mfos_terms:
- catalogd
- datasetd
mfos_mapping:
  mfos_specs:
  - docs/design/specs/08-dataset-catalog.md
  mfos_requirements:
  - MFOS-REQ-CATALOG-0001
  - MFOS-REQ-DATASET-0001
prohibited_inference:
- Do not treat this concept card as external documentation.
- Do not infer external compatibility from MFOS concept names.
review_status: draft
---

# DFSMS Storage Policy Boundary

## Concept

DFSMS and SMS define the external z/OS storage-management context for data sets, storage classes, management classes, data classes, and storage groups.

## MFOS Semantics

MFOS may describe storage intent, placement preferences, lifecycle state, and retention hints. These are MFOS-owned concepts unless an explicit adapter maps them to an external z/OS installation.

## Compatibility-Risk Wording

Use cautious language:

- "MFOS records storage intent that may need translation for an IBM SMS-managed environment."
- "Real allocation, migration, backup, and retention behavior remains installation-specific and controlled by IBM DFSMS/SMS policy."
- "MFOS does not emulate ACS routines, DFSMShsm command behavior, or DFSMS utility processing."

Avoid saying:

- "MFOS is compatible with SMS allocation."
- "MFOS implements DFSMS policy."
- "MFOS predicts DFSMShsm outcomes."

