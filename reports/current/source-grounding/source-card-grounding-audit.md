# Source Card Grounding Audit

Audited 37 Source Cards under `docs/design/source-matrix/cards/`.

Findings:

- All 37 cards are public-safe bibliographic/reference cards.
- No forbidden legacy fields were found: `canonical_concepts`,
  `normative_source`, `detailed_summary`, `source_summary`, `copied_excerpt`,
  `record_layouts`, `command_syntax`, or `macro_signatures`.
- All 37 cards have `review_topics`, `mfos_divergence`,
  `prohibited_inference`, `legal_controls`, `requirement_refs`, and
  `required_negative_tests`.
- All 37 cards are still `review_status: draft`.
- All 37 cards have empty direct `mfos_mapping.mfos_specs`; source-to-spec
  mapping is currently reverse-inferred from specs and traceability.
- No card reaches SG6 or SG7.

The Source Card layer is adequate for structural traceability, but not for an
unqualified source-grounded semantic freeze. The freeze must remain
conditional until targeted source review marks cards reviewed and card-local
spec/test links are added.

