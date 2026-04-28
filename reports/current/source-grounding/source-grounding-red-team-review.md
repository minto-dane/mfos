# Source Grounding Red Team Review

## Critical

1. `reports/phases/phase-1/readiness-report.md` over-authorized Phase 1
   Portable Semantic Core and semantic runner work while PACK-05 through
   PACK-09 still block `portable_semantic_core` and `executable_spec`.
   This is corrected in Phase 0.9.7 status/reporting by downgrading Phase 1 to
   loader-only until source-grounding gaps close.

2. `docs/design/specs/09-job-spool.md` freezes an external-looking
   job-control stream grammar. This creates compatibility and copied-command
   syntax risk. PACK-08 is not ready for semantic evaluator work.

## Major

1. Source Cards are safe reference cards but remain `review_status: draft` and
   have no direct `mfos_mapping.mfos_specs` or card-local test links.
2. Current fixtures lack direct `source_refs`.
3. Current golden/oracle vectors lack direct `source_refs` and
   `target_requirements`.
4. Planned `010x` requirement test IDs and current `09xx` executable-spec
   catalog IDs are not reconciled.
5. Job/spool MFOS-owned IDs still contain external-looking JCL/DD terms.
6. Some golden vectors are too generic to prove domain semantics and must not
   be treated as semantic proof.
7. The runner contract has more shape than its registry/evidence maturity
   supports; it remains provisional.

## Minor

1. Dataset/catalog vocabulary still carries compatibility-impression risk even
   with non-compatibility text.
2. Archive Phase 0.8 catalogs contain external-looking examples; they are
   superseded but should be retained only as historical artifacts.

## Result

No production implementation or semantic runner implementation was found.
Semantic freeze must be conditional, and Phase 1 semantic evaluator work must
remain blocked.

