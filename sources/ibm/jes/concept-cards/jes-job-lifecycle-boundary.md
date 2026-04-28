---
concept_id: SRC-WB-CONCEPT-JES-JOB-LIFECYCLE-BOUNDARY-0001
source_ids:
- EXTREF-IBM-ZOS-JES-FUNCTIONS-0001
- EXTREF-IBM-ZOS-JES-JOB-CONTROL-0001
status: draft
authority_status: preparatory_until_adr_migration
summary_scope: public_safe_mfos_mapping
mfos_terms:
- jobd
- spoold
- operatord
mfos_mapping:
  mfos_specs:
  - docs/design/specs/09-job-spool.md
  - docs/design/specs/10-operator-console.md
  mfos_requirements:
  - MFOS-REQ-JOB-0001
  - MFOS-REQ-SPOOL-0001
prohibited_inference:
- Do not treat this concept card as external documentation.
- Do not infer external compatibility from MFOS concept names.
review_status: draft
---

# JES Job Lifecycle Boundary

## Concept

JES is the external z/OS subsystem family that accepts, schedules, tracks, and manages batch job input and output.

## MFOS Semantics

MFOS may model a workload request, execution intent, submitted job reference, and observed completion state. These are independent of IBM JES internals.

## Compatibility-Risk Wording

Use cautious language:

- "MFOS can reference an externally submitted JES job by adapter-observed identifiers."
- "JES queue state and output availability are external observations."
- "JCL or JECL generation is adapter behavior, not a core MFOS semantic."

Avoid saying:

- "MFOS job state matches JES state."
- "MFOS validates JCL or JECL compatibility."
- "MFOS implements JES spool semantics."

