---
source_id: INT-FBVBS-TRANSFER-RULES-0001
source_kind: repository_reference
source_type: internal_transfer
semantic_role: transfer_governance_pattern
vendor: minto-dane
document_title: FBVBS adopt adapt reject transfer rules
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
  section_scope: document governance, traceability, workstream closure
  local_cache_manifest: not_committed; see sources/_cache/README.md
cache_disposition: temporary_ignored_cache
reference_purpose:
  - internal transfer rubric
  - source-grounding governance
review_topics:
  - adopt adapt reject
  - design-root ownership
  - source gaps
mfos_mapping:
  mfos_components:
    - source-grounding
  mfos_specs: []
  mfos_requirements:
    - unassigned-preparatory
mfos_divergence:
  - MFOS acceptance requires MFOS ownership, not only upstream structure.
prohibited_inference:
  - Do not transfer FBVBS claims without MFOS design-root review.
  - Do not convert gaps into requirements without owner assignment.
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
  - source_id: INT-FBVBS-TRANSFER-RULES-0001
    source_type: internal_transfer
    source_version: 30e6fb54c76eaec83d03f79e1fd96c030cca504b
    paths:
      - plan/document-catalog.md
      - plan/fbvbs-design-traceability.md
      - plan/standalone/implementation/standalone-implementation-plan.md
requirement_refs:
  - unassigned-preparatory
review_status: draft
---

# Source Card: Adopt Adapt Reject Transfer Rules

Grounding revision: `30e6fb54c76eaec83d03f79e1fd96c030cca504b`

Upstream anchors:

- `plan/document-catalog.md`
- `plan/fbvbs-design-traceability.md`
- `plan/standalone/implementation/standalone-implementation-plan.md`
- `plan/standalone/architecture/standalone-runtime-architecture.md`

Public-safe MFOS mapping note:

FBVBS uses document authority levels, design-root traceability, supersession records, and workstream exit criteria to keep derived specs from becoming unreviewed requirements. It also marks incomplete areas directly instead of allowing release evidence to imply closure.

MFOS transfer rules:

| Rule | Use when | MFOS action |
|---|---|---|
| Adopt | The pattern is structural and source-independent | Bring the governance or assurance mechanism into MFOS with MFOS names |
| Adapt | The pattern depends on FBVBS object names, ABI calls, or tooling layout | Re-express it against MFOS objects and schemas |
| Reject | The source claim is profile-specific, incomplete, or outside MFOS scope | Record why it is not transferred |
| Gap | The source names an unresolved area | Preserve it as a gap until MFOS owns a design root |

Adopt candidates:

- Authority levels for documents.
- Design-root traceability.
- Validator family taxonomy.
- Compatibility windows and reserved-field discipline.
- Evidence-pack manifest and retention integrity model.

Adapt candidates:

- Partition lifecycle contracts.
- Operator command classes.
- State manifest shape.
- Incident timeline and recovery approval artifacts.
- Release provenance and signature metadata.

Reject candidates:

- FBVBS conformance terminology.
- FreeBSD or hypervisor-specific service labels.
- Standalone-ready claims beyond the evidence actually present.
- UI profile choices as ABI truth.

Minimum MFOS acceptance bar:

An imported pattern is accepted only when it has an MFOS owner, an MFOS design root, a validator or review hook, and an explicit evidence artifact.
