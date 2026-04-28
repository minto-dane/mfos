# Source Grounding Open Issues

## P0 Before Semantic Evaluator

- Propagate `source_refs` into all current fixtures.
- Propagate `source_refs` and `target_requirements` into all current
  golden/oracle vectors.
- Reconcile planned `010x` requirement tests with current `09xx`
  executable-spec artifacts.
- Refactor or explicitly re-bound job-control stream syntax and JCL/DD-style
  MFOS-owned identifiers.

## P1 Before Unqualified Semantic Freeze

- Add card-local `mfos_mapping.mfos_specs` and test links to Source Cards.
- Complete targeted source review for pin-review cards.
- Add claim-to-requirement coverage for the 24 split requirements.
- Move evidence from draft placeholders to verified evidence only when actual
  verifier outputs and hashes exist.

## P2 Hygiene

- Keep `sources/` populated but noncanonical until an ADR-backed canonical
  migration and automated parity validator exist. The current manual parity
  report is `sources/source-matrix-parity.yml`.
- Keep archived Phase 0.8 catalogs out of current validation and current
  readiness claims.
