// MFOS Phase 1 Dafny executable semantics: first vertical slice contracts.

include "common.dfy"
include "errors.dfy"
include "types.dfy"
include "authorization.dfy"
include "audit.dfy"
include "dataset_catalog.dfy"
include "job_spool.dfy"
include "operator_console.dfy"

module FirstVerticalSlice {
  import opened Common
  import opened Errors
  import opened Types
  import Authorization
  import Audit
  import DatasetCatalog
  import JobSpool
  import OperatorConsole

  datatype SliceName = HELLO_JOB | BOB_DENIED_ALICE_DATASET
  datatype SliceAuditEvent =
    AUDIT_SUBMIT
  | AUDIT_OPEN
  | AUDIT_OPEN_DENY
  | AUDIT_EXECUTE
  | AUDIT_SPOOL
  | AUDIT_COMPLETE
  | AUDIT_FAILURE_SUMMARY

  datatype SliceResult = SliceResult(
    name: SliceName,
    final_state: JobState,
    return_code: nat,
    error_code: ErrorCode,
    reason_code: ReasonCode,
    decision_result: DecisionResult,
    dataset_handle_created: bool,
    dataset_handle_after_allow: bool,
    audit_before_final_result: bool,
    spool_summary_exists: bool,
    operator_display_failed: bool,
    audit_sequence: seq<SliceAuditEvent>
  )

  function HelloJobResult(): SliceResult {
    SliceResult(HELLO_JOB, JOB_COMPLETE, 0, MFOS_OK, REASON_OK, ALLOW, true, true, false, true, false,
      [AUDIT_SUBMIT, AUDIT_OPEN, AUDIT_EXECUTE, AUDIT_SPOOL, AUDIT_COMPLETE])
  }

  function BobDeniedAliceDatasetResult(): SliceResult {
    SliceResult(BOB_DENIED_ALICE_DATASET, JOB_FAILED, 8, MFOS_ERR_POLICY_DENIED,
      DATASET_READ_NOT_PERMITTED, DENY, false, false, true, true, true,
      [AUDIT_SUBMIT, AUDIT_OPEN_DENY, AUDIT_FAILURE_SUMMARY])
  }

  predicate HelloJobAuditSequence(events: seq<SliceAuditEvent>) {
    events == [AUDIT_SUBMIT, AUDIT_OPEN, AUDIT_EXECUTE, AUDIT_SPOOL, AUDIT_COMPLETE]
  }

  predicate OpenDenyBeforeFinalDenial(events: seq<SliceAuditEvent>) {
    |events| >= 2 && events[1] == AUDIT_OPEN_DENY
  }

  predicate SliceHandleCreatedOnlyAfterAllow(result: SliceResult) {
    result.dataset_handle_created ==> (
      (result.decision_result == ALLOW || result.decision_result == ALLOW_WITH_AUDIT) &&
      result.dataset_handle_after_allow)
  }

  predicate SliceDenyPreventsDatasetHandle(result: SliceResult) {
    result.decision_result == DENY ==> !result.dataset_handle_created
  }

  predicate HelloJobComplete(result: SliceResult) {
    result.name == HELLO_JOB &&
    result.final_state == JOB_COMPLETE &&
    result.return_code == 0 &&
    result.error_code == MFOS_OK &&
    result.decision_result == ALLOW &&
    result.dataset_handle_created &&
    result.dataset_handle_after_allow &&
    result.spool_summary_exists &&
    SliceHandleCreatedOnlyAfterAllow(result) &&
    HelloJobAuditSequence(result.audit_sequence)
  }

  predicate BobDeniedPath(result: SliceResult) {
    result.name == BOB_DENIED_ALICE_DATASET &&
    result.final_state == JOB_FAILED &&
    result.decision_result == DENY &&
    result.error_code == MFOS_ERR_POLICY_DENIED &&
    result.reason_code == DATASET_READ_NOT_PERMITTED &&
    !result.dataset_handle_created &&
    SliceDenyPreventsDatasetHandle(result) &&
    result.audit_before_final_result &&
    OpenDenyBeforeFinalDenial(result.audit_sequence) &&
    result.spool_summary_exists &&
    result.operator_display_failed
  }

  lemma HelloJobContract()
    ensures HelloJobComplete(HelloJobResult())
    ensures HelloJobResult().final_state == JOB_COMPLETE
    ensures HelloJobResult().return_code == 0
    ensures HelloJobResult().dataset_handle_created
    ensures HelloJobResult().dataset_handle_after_allow
    ensures SliceHandleCreatedOnlyAfterAllow(HelloJobResult())
    ensures HelloJobAuditSequence(HelloJobResult().audit_sequence)
  {
  }

  lemma BobDeniedAliceDatasetContract()
    ensures BobDeniedPath(BobDeniedAliceDatasetResult())
    ensures BobDeniedAliceDatasetResult().error_code == MFOS_ERR_POLICY_DENIED
    ensures BobDeniedAliceDatasetResult().reason_code == DATASET_READ_NOT_PERMITTED
    ensures !BobDeniedAliceDatasetResult().dataset_handle_created
    ensures SliceDenyPreventsDatasetHandle(BobDeniedAliceDatasetResult())
    ensures BobDeniedAliceDatasetResult().audit_before_final_result
    ensures OpenDenyBeforeFinalDenial(BobDeniedAliceDatasetResult().audit_sequence)
    ensures BobDeniedAliceDatasetResult().spool_summary_exists
  {
  }

  lemma SpecGapUnsupportedNeverComplete(error: ErrorCode)
    requires error == MFOS_ERR_SPEC_GAP || error == MFOS_ERR_UNSUPPORTED
    ensures IsFailClosedError(error)
    ensures !IsSuccessError(error)
  {
    if error == MFOS_ERR_SPEC_GAP {
      SpecGapIsFailClosed();
    } else {
      UnsupportedIsFailClosed();
    }
  }
}
