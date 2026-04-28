---
concept_id: SRC-WB-CONCEPT-DPM-PARTITION-RESOURCE-BOUNDARY-0001
source_ids:
- EXTREF-IBM-Z-DPM-OVERVIEW-0001
- EXTREF-IBM-Z-DPM-PARTITIONS-ADAPTERS-0001
status: draft
authority_status: preparatory_until_adr_migration
summary_scope: public_safe_mfos_mapping
mfos_terms:
- pxm
mfos_mapping:
  mfos_specs:
  - docs/design/specs/16-partition-manager.md
  mfos_requirements:
  - MFOS-REQ-PARTITION-0001
prohibited_inference:
- Do not treat this concept card as external documentation.
- Do not infer external compatibility from MFOS concept names.
review_status: draft
---

# DPM Partition Resource Boundary

## Concept

DPM provides an HMC-managed model for partitions and their processor, memory, network, storage, and cryptographic resource relationships.

## MFOS Semantics

MFOS may model a logical compute partition, resource intent, topology observation, and lifecycle status. These are independent from DPM unless an adapter binds them to a discovered HMC object.

## Compatibility-Risk Wording

Use cautious language:

- "MFOS can reference DPM partitions as external managed resources."
- "Resource changes require external DPM authorization and validation."
- "MFOS inventory is not a substitute for HMC or SE state."

Avoid saying:

- "Forbidden claim: MFOS implements DPM."
- "Forbidden claim: MFOS can guarantee partition activation."
- "Forbidden claim: MFOS resource counts are authoritative for the CPC."
