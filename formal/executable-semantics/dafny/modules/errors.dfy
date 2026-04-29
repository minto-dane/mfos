// MFOS Phase 1 Dafny executable semantics: error taxonomy.
// Undefined behavior is SPEC_GAP. Specified but unsupported behavior is UNSUPPORTED.

include "common.dfy"

module Errors {
  import opened Common

  datatype ErrorCode =
    MFOS_OK
  | MFOS_ERR_UNAUTHENTICATED
  | MFOS_ERR_POLICY_DENIED
  | MFOS_ERR_UNAUTHORIZED
  | MFOS_ERR_UNSUPPORTED
  | MFOS_ERR_SPEC_GAP
  | MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE
  | MFOS_ERR_POLICY_VERSION_MISMATCH
  | MFOS_ERR_STALE_HANDLE
  | MFOS_ERR_CATALOG_NOT_FOUND
  | MFOS_ERR_INVALID_STATE
  | MFOS_ERR_INVALID_INPUT

  datatype ReasonCode =
    REASON_OK
  | DATASET_READ_NOT_PERMITTED
  | SUBJECT_NOT_AUTHENTICATED
  | STALE_POLICY_VERSION
  | STALE_OBJECT_GENERATION
  | AUDIT_UNAVAILABLE
  | CATALOG_ENTRY_NOT_COMMITTED
  | INVALID_LIFECYCLE_TRANSITION
  | UNSUPPORTED_DECLARATION
  | SPECIFICATION_GAP

  predicate IsSuccessError(error: ErrorCode) {
    error == MFOS_OK
  }

  predicate IsFailClosedError(error: ErrorCode) {
    error != MFOS_OK
  }

  predicate IsPolicyDenial(error: ErrorCode, reason: ReasonCode) {
    error == MFOS_ERR_POLICY_DENIED && reason == DATASET_READ_NOT_PERMITTED
  }

  predicate LegacyUnauthorizedAlias(error: ErrorCode) {
    error == MFOS_ERR_UNAUTHORIZED
  }

  function ErrorRank(error: ErrorCode): nat {
    match error
    case MFOS_OK => 0
    case MFOS_ERR_UNAUTHENTICATED => 1
    case MFOS_ERR_POLICY_DENIED => 2
    case MFOS_ERR_UNAUTHORIZED => 3
    case MFOS_ERR_UNSUPPORTED => 4
    case MFOS_ERR_SPEC_GAP => 5
    case MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE => 6
    case MFOS_ERR_POLICY_VERSION_MISMATCH => 7
    case MFOS_ERR_STALE_HANDLE => 8
    case MFOS_ERR_CATALOG_NOT_FOUND => 9
    case MFOS_ERR_INVALID_STATE => 10
    case MFOS_ERR_INVALID_INPUT => 11
  }

  function ToResult<T>(error: ErrorCode, value: T): Result<T> {
    if error == MFOS_OK then ResultOk(value) else ResultErr(ErrorRank(error))
  }

  lemma UnsupportedIsFailClosed()
    ensures IsFailClosedError(MFOS_ERR_UNSUPPORTED)
    ensures !IsSuccessError(MFOS_ERR_UNSUPPORTED)
  {
  }

  lemma SpecGapIsFailClosed()
    ensures IsFailClosedError(MFOS_ERR_SPEC_GAP)
    ensures !IsSuccessError(MFOS_ERR_SPEC_GAP)
  {
  }
}
