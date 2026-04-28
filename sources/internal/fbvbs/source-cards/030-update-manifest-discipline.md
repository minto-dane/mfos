---
source_id: INT-FBVBS-UPDATE-MANIFEST-DISCIPLINE-0001
source_kind: repository_reference
source_type: internal_transfer
semantic_role: update_manifest_pattern
vendor: minto-dane
document_title: FBVBS update manifest discipline transfer card
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
  section_scope: manifest verification, freshness, rollback, provenance
  local_cache_manifest: not_committed; see sources/_cache/README.md
cache_disposition: temporary_ignored_cache
reference_purpose:
  - update discipline concept mapping
  - gap transfer screening
review_topics:
  - update manifest
  - artifact freshness
  - rollback detection
  - release provenance
mfos_mapping:
  mfos_components:
    - update
    - release
  mfos_specs: []
  mfos_requirements:
    - unassigned-preparatory
mfos_divergence:
  - MFOS must define its own trusted-time and deployment authorization policy.
prohibited_inference:
  - Do not infer a complete update framework from this source.
  - Do not treat repository-local provenance as MFOS deployment authorization.
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
  - source_id: INT-FBVBS-UPDATE-MANIFEST-DISCIPLINE-0001
    source_type: internal_transfer
    source_version: 30e6fb54c76eaec83d03f79e1fd96c030cca504b
    paths:
      - hypervisor/src/security.c
      - hypervisor/tools/release/generate_provenance.py
      - hypervisor/tools/release/release_readiness.py
      - plan/standalone/architecture/standalone-runtime-architecture.md
requirement_refs:
  - unassigned-preparatory
review_status: draft
---

# Source Card: Update Manifest Discipline

Grounding revision: `30e6fb54c76eaec83d03f79e1fd96c030cca504b`

Upstream anchors:

- `hypervisor/src/security.c`
- `hypervisor/include/fbvbs_abi.h`
- `hypervisor/tests/c/security/test_fault_injection.c`
- `hypervisor/tools/release/generate_provenance.py`
- `hypervisor/tools/release/release_readiness.py`
- `hypervisor/tools/release/sign_release_artifacts.py`
- `plan/standalone/architecture/standalone-runtime-architecture.md`
- `plan/fbvbs-design-traceability.md`

Public-safe MFOS mapping note:

FBVBS has runtime paths for manifest verification, generation matching, rollback detection, trusted-time freshness checks, revocation, dependency checks, and snapshot consistency. Release tooling separately produces provenance, readiness summaries, and detached signatures. The standalone planning documents still call out update/artifact freshness and secure-clock discipline as insufficiently specified for standalone closure.

Transferable mechanism:

1. Bind artifact use to a verified manifest set, not to a bare hash alone.
2. Carry generation and minimum-generation checks to detect rollback.
3. Fail closed when trusted time is unavailable for freshness-sensitive decisions.
4. Track revocation and dependency failures as explicit reason classes.
5. Separate repository-local provenance from producer-facing release signing.

MFOS adoption rule:

- Adopt: generation windows, rollback/freshness failure classes, revocation checks, and signed release metadata.
- Adapt: FBVBS UVS and artifact catalog structures into MFOS package/update manifest structures.
- Reject: treating source-local release provenance as sufficient for MFOS deployment authority.

MFOS gap marker:

The source explicitly leaves standalone update/artifact freshness and secure-clock policy underdeveloped. MFOS should create its own update manifest discipline instead of relying on this card as a complete source.
