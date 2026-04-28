# Phase 1 Open Issues

Status: nonblocking for Phase 1 Portable Semantic Core + Conformance Harness.

These issues do not authorize production implementation and do not block the
Phase 1 semantic-core/conformance-harness start after PR #5 review.

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

- Production implementation.
- Hosted daemon implementation.
- Hardware enforcement claims.
- Public release claims.
- External compatibility claims.
