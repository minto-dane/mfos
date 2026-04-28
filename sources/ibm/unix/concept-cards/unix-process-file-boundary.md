---
concept_id: SRC-WB-CONCEPT-UNIX-PROCESS-FILE-BOUNDARY-0001
source_ids:
- EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001
- EXTREF-IBM-ZOS-UNIX-FILE-SYSTEMS-0001
status: draft
authority_status: preparatory_until_adr_migration
summary_scope: public_safe_mfos_mapping
mfos_terms:
- posix-subsystem
- linux-gateway
mfos_mapping:
  mfos_specs:
  - docs/design/specs/19-posix-subsystem.md
  - docs/design/specs/18-linux-gateway.md
  mfos_requirements:
  - MFOS-REQ-POSIX-0001
prohibited_inference:
- Do not treat this concept card as external documentation.
- Do not infer external compatibility from MFOS concept names.
review_status: draft
---

# z/OS UNIX Process And File Boundary

## Concept

z/OS UNIX provides shell, process, and hierarchical file-system concepts within z/OS.

## MFOS Semantics

MFOS may model portable process launch, file references, directory paths, and environment metadata. z/OS UNIX-specific behavior belongs in an adapter layer.

## Compatibility-Risk Wording

Use cautious language:

- "MFOS path references may require z/OS UNIX-specific translation and authorization."
- "Observed process state is external to MFOS."
- "z/OS UNIX files can share z/OS security and operational constraints that differ from distributed UNIX systems."

Avoid saying:

- "MFOS POSIX behavior matches z/OS UNIX."
- "MFOS can infer mount state from a path string."
- "MFOS implements z/OS UNIX callable services."

