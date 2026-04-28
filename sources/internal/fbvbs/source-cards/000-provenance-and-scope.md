---
source_id: INT-FBVBS-PROVENANCE-SCOPE-0001
source_kind: repository_reference
source_type: internal_transfer
semantic_role: design_background
vendor: minto-dane
document_title: FBVBS repository provenance and standalone scope
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
  section_scope: repository governance, standalone profile index, traceability
  local_cache_manifest: not_committed; see sources/_cache/README.md
cache_disposition: temporary_ignored_cache
reference_purpose:
  - source discovery
  - concept mapping
  - internal MFOS transfer screening
review_topics:
  - provenance
  - document authority
  - standalone profile scope
mfos_mapping:
  mfos_components:
    - source-grounding
  mfos_specs: []
  mfos_requirements:
    - unassigned-preparatory
mfos_divergence:
  - MFOS must define its own design roots and conformance terms.
prohibited_inference:
  - Do not claim MFOS compatibility or conformance with FBVBS.
  - Do not treat this card as a substitute for the source repository.
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
  - source_id: INT-FBVBS-PROVENANCE-SCOPE-0001
    source_type: internal_transfer
    source_version: 30e6fb54c76eaec83d03f79e1fd96c030cca504b
    paths:
      - plan/README.md
      - plan/document-catalog.md
      - plan/fbvbs-design-traceability.md
      - plan/standalone/README.md
requirement_refs:
  - unassigned-preparatory
review_status: draft
---

# Source Card: Provenance And Scope

Source: `https://github.com/minto-dane/fbvbs`

Inspected revision: `30e6fb54c76eaec83d03f79e1fd96c030cca504b` (`dev`)

Public-safe summary: FBVBS is organized around a retained-C microhypervisor foundation plus a standalone profile. The active standalone references are layered as architecture, subsystem specs, operations, assurance, and implementation planning. The repository distinguishes authoritative design roots from derived specs, validation docs, operational policy, and implementation plans.

Key upstream paths:

- `plan/README.md`
- `plan/document-catalog.md`
- `plan/fbvbs-design-traceability.md`
- `plan/standalone/README.md`
- `plan/standalone/architecture/standalone-runtime-architecture.md`
- `plan/standalone/implementation/standalone-implementation-plan.md`

Transfer value for MFOS:

- Use a typed document hierarchy so implementation plans cannot silently become requirements.
- Require every derived assurance artifact to name its design root and dependency chain.
- Keep profile-specific claims separate from shared foundation claims.

Transfer boundary:

- Do not import FBVBS names as MFOS requirements.
- Do not treat the standalone profile as production-complete; upstream marks hardware closure, host deprivilege, OOB audit chain closure, and update/artifact freshness as gaps.

MFOS disposition: adopt the governance pattern, adapt the terminology, reject direct conformance claims.
