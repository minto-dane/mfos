---
source_id: INT-FBVBS-ASSURANCE-DISCIPLINE-0001
source_kind: repository_reference
source_type: internal_transfer
semantic_role: assurance_pattern
vendor: minto-dane
document_title: FBVBS assurance discipline transfer card
document_url:
  - https://github.com/minto-dane/fbvbs
retrieved_at: "2026-04-28"
authority_status: preparatory_until_adr_migration
citation_scope: path_and_commit_only
retrieval_metadata:
  retrieved_at: "2026-04-28"
  retrieved_by: FBVBS Internal Source Grounding Worker
  public_url: https://github.com/minto-dane/fbvbs
  landing_page_url: https://github.com/minto-dane/fbvbs
  source_version: 30e6fb54c76eaec83d03f79e1fd96c030cca504b
  section_scope: validators, compatibility, traceability
  local_cache_manifest: temporary clone at /tmp/fbvbs-upstream, not committed
cache_disposition: temporary_ignored_cache
reference_purpose:
  - concept mapping
  - assurance transfer screening
review_topics:
  - assurance gates
  - validator families
  - traceability
mfos_mapping:
  mfos_components:
    - assurance
    - source-grounding
  mfos_specs: []
  mfos_requirements:
    - unassigned-preparatory
mfos_divergence:
  - MFOS validators must target MFOS-owned design roots and schemas.
prohibited_inference:
  - Do not infer FBVBS production readiness from validator taxonomy.
  - Do not copy FBVBS tool outputs as MFOS evidence.
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
  no_affiliation_claim: true
  no_compatibility_claim: true
  no_conformance_claim: true
  no_certification_claim: true
  no_source_substitution: true
  external_affiliation_claimed: false
  compatibility_claimed: false
  substitute_for_source: false
source_refs:
  - source_id: INT-FBVBS-ASSURANCE-DISCIPLINE-0001
    source_type: internal_transfer
    source_version: 30e6fb54c76eaec83d03f79e1fd96c030cca504b
    paths:
      - plan/standalone/assurance/verification-and-validator-suite.md
      - plan/standalone/assurance/compatibility-and-versioning.md
      - plan/fbvbs-design-traceability.md
requirement_refs:
  - unassigned-preparatory
review_status: draft
---

# Source Card: Assurance Discipline

Grounding revision: `30e6fb54c76eaec83d03f79e1fd96c030cca504b`

Upstream anchors:

- `plan/standalone/assurance/verification-and-validator-suite.md`
- `plan/standalone/assurance/compatibility-and-versioning.md`
- `plan/fbvbs-design-traceability.md`
- `hypervisor/tools/compatibility/check_standalone_compatibility_changes.py`
- `hypervisor/tools/compatibility/check_standalone_reserved_fields.py`
- `hypervisor/tools/fuzz/*`

Public-safe MFOS mapping note:

FBVBS treats assurance as a suite of gates, not as a final report. The suite groups semantic drift and proof-readiness checks, ABI robustness checks, lifecycle validators, storage and ownership validators, and operational incident validators. Gate levels distinguish always-on checks from heavier campaigns.

Transferable mechanism:

1. Define assurance families before tool names.
2. Attach each validator to a design root.
3. Make compatibility and reserved-field checks part of the default gate.
4. Separate quick CI gates from heavier review gates.
5. Record drift categories where proof stubs or model variants exist.

MFOS adoption rule:

- Adopt: validator-family taxonomy, always-on vs heavy gate split, and traceability-to-design-root requirement.
- Adapt: FBVBS-specific tools become MFOS validators over MFOS partitions, manifests, and operator artifacts.
- Reject: any claim that a passing validator suite alone proves production readiness.

Evidence expectations for MFOS:

- Validator output should include tool identity, schema version, checked design root, inputs, verdict, reason codes, and unresolved warnings.
- Compatibility drift should be reviewable as structured data, not prose only.

Known source gap to preserve:

- Upstream still marks real-hardware IOMMU/interrupt-remapping closure and final host deprivilege as incomplete, so MFOS should not infer those are solved by the assurance structure.
