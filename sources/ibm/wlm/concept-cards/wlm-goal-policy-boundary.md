---
concept_id: SRC-WB-CONCEPT-WLM-GOAL-POLICY-BOUNDARY-0001
source_ids:
- EXTREF-IBM-ZOS-WLM-OVERVIEW-0001
- EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001
status: draft
authority_status: preparatory_until_adr_migration
summary_scope: public_safe_mfos_mapping
mfos_terms:
- wlmd
- jobd
mfos_mapping:
  mfos_specs:
  - docs/design/specs/11-workload-policy.md
  mfos_requirements:
  - MFOS-REQ-WPOL-0001
prohibited_inference:
- Do not treat this concept card as external documentation.
- Do not infer external compatibility from MFOS concept names.
review_status: draft
---

# WLM Goal Policy Boundary

## Concept

WLM is the external z/OS authority for goal-oriented resource management across workloads in an image or sysplex.

## MFOS Semantics

MFOS may model desired service intent, workload priority, operational importance, and observed performance status. These concepts do not imply a direct WLM service definition.

## Compatibility-Risk Wording

Use cautious language:

- "MFOS workload intent can be mapped by an adapter to installation-specific WLM policy."
- "Observed WLM service or report class names are external labels."
- "MFOS does not calculate WLM performance index or enforce WLM dispatching."

Avoid saying:

- "Forbidden claim: MFOS implements WLM."
- "Forbidden claim: MFOS guarantees WLM goal achievement."
- "Forbidden claim: MFOS report classes are equivalent to IBM report classes."
