---
concept_id: SRC-WB-CONCEPT-ZOSMF-MANAGEMENT-API-BOUNDARY-0001
source_ids:
- EXTREF-IBM-ZOS-MANAGEMENT-FACILITY-TASKS-0001
- EXTREF-IBM-ZOS-MANAGEMENT-FACILITY-REST-SERVICES-0001
status: draft
authority_status: preparatory_until_adr_migration
summary_scope: public_safe_mfos_mapping
mfos_terms:
- management-api
mfos_mapping:
  mfos_specs:
  - docs/design/specs/22-management-api.md
  mfos_requirements:
  - MFOS-REQ-MGMTAPI-0001
prohibited_inference:
- Do not treat this concept card as external documentation.
- Do not infer external compatibility from MFOS concept names.
review_status: draft
---

# z/OSMF Management API Boundary

## Concept

z/OSMF provides a web and REST management interface for selected z/OS operational tasks and resources.

## MFOS Semantics

MFOS may model a management action request, external operation result, resource reference, and audit observation. These are independent from z/OSMF API contracts.

## Compatibility-Risk Wording

Use cautious language:

- "MFOS can call z/OSMF through an adapter when configured and authorized."
- "z/OSMF resource identifiers are external adapter data."
- "MFOS does not define z/OSMF REST request or response compatibility in core semantics."

Avoid saying:

- "MFOS implements z/OSMF."
- "MFOS guarantees z/OSMF operation availability."
- "MFOS stores z/OSMF API schemas as source grounding."

