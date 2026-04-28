# Phase 1 Open Issues

Status: blocking for Phase 1 semantic evaluator and Portable Semantic Core
behavior implementation.

These issues do not block loader-only artifact validation and traceability
repair. They do block semantic-core behavior, semantic evaluator, and semantic
runner implementation.

## Blocking Before Semantic Evaluator

- Current fixtures lack direct `source_refs`.
- Current golden/oracle vectors lack direct `source_refs` and
  `target_requirements`.
- Planned `010x` requirement test IDs and current `09xx` executable-spec
  catalog IDs are not reconciled.
- PACK-08 job/spool uses external-looking job-control stream syntax and
  JCL/DD-style MFOS-owned identifiers that need refactor or explicit
  re-bounding.

## Minor

- Concrete byte-level fuzz seed files must be created during Phase 1 or later.
- Release-mode evidence gates remain intentionally closed until verified
  evidence artifacts, digests, verifier outputs, and review metadata exist.
- Source Cards still need deeper publication/section/version pinning where
  local metadata could not verify exact references.
- Japanese mirror mechanics remain incomplete; English remains canonical.
- Pre-Phase 0.9 planning catalogs contain legacy `MFOS_ERR_UNAUTHORIZED`
  wording and should be cleaned during broader error-model grooming. Phase 1
  executable-spec artifacts already use `MFOS_ERR_UNAUTHENTICATED` and
  `MFOS_ERR_POLICY_DENIED` for the paths they exercise.

## Still Blocked

- Portable Semantic Core behavior implementation.
- Semantic evaluator implementation.
- Semantic runner command implementation.
- Production implementation.
- Hosted daemon implementation.
- Hardware enforcement claims.
- Public release claims.
- External compatibility claims.
