---
concept_id: INT-FBVBS-CONCEPT-MANIFEST-FRESHNESS-COMPATIBILITY-0001
source_ids:
  - INT-FBVBS-UPDATE-MANIFEST-DISCIPLINE-0001
  - INT-FBVBS-ASSURANCE-DISCIPLINE-0001
source_terms:
  - manifest set
  - freshness
  - compatibility window
summary: Short MFOS-facing abstraction of update manifest and compatibility controls.
mfos_terms:
  - MFOS update manifest
  - MFOS trusted-time policy
  - MFOS compatibility window
mfos_mapping:
  overlap:
    - generation checks
    - fail-closed missing windows
    - revocation and dependency verdicts
  divergence:
    - MFOS must define its own secure-clock and release-signing authority
mfos_divergence:
  - Source freshness policy is a gap, not a transferable complete design.
requirements:
  - unassigned-preparatory
negative_tests:
  - accepted artifact without manifest-set binding
  - missing compatibility window treated as compatible
prohibited_inference:
  - Do not treat source-local provenance as MFOS deployment authorization.
review_status: draft
citation_scope: source-card-id-only
cache_disposition: temporary_ignored_cache
legal_controls:
  public_safe: true
  no_affiliation_claim: true
  no_compatibility_claim: true
  no_conformance_claim: true
  no_certification_claim: true
  no_source_substitution: true
---

# Concept Card: Manifest Freshness And Compatibility

Concept:

Update and artifact acceptance should be controlled by version windows, generation monotonicity, trusted-time freshness, revocation, dependency, and signature metadata.

MFOS pattern:

1. A manifest set is the unit of update truth.
2. Each artifact acceptance decision records the manifest set, generation, freshness verdict, revocation verdict, and dependency verdict.
3. Compatibility windows are explicit and missing windows fail closed.
4. Release provenance is distinct from deployment authorization.

Derived from:

- `source-cards/030-update-manifest-discipline.md`
- `source-cards/010-assurance-discipline.md`

MFOS implementation sketch:

- `manifest_schema_version`
- `current_version`
- `minimum_accepted`
- `maximum_accepted`
- `generation`
- `minimum_generation`
- `expires_at`
- `trusted_time_required`
- `revocation_root`
- `dependency_set_digest`
- `signature_metadata`

Gap carried from source:

The upstream source does not fully close standalone update/artifact freshness or secure-clock policy. MFOS must own this policy before using the pattern for deployment authority.
