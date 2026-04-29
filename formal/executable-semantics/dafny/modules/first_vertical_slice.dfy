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

  datatype SliceResult = SliceResult(
    name: SliceName,
    final_state: JobState,
    return_code: nat,
    error_code: ErrorCode,
    reason_code: ReasonCode,
    dataset_handle_created: bool,
    audit_before_final_result: bool,
    spool_summary_exists: bool,
    operator_display_failed: bool
  )

  function HelloJobResult(): SliceResult {
    SliceResult(HELLO_JOB, JOB_COMPLETE, 0, MFOS_OK, REASON_OK, true, false, true, false)
  }

  function BobDeniedAliceDatasetResult(): SliceResult {
    SliceResult(BOB_DENIED_ALICE_DATASET, JOB_FAILED, 8, MFOS_ERR_POLICY_DENIED,
      DATASET_READ_NOT_PERMITTED, false, true, true, true)
  }

  predicate HelloJobComplete(result: SliceResult) {
    result.name == HELLO_JOB &&
    result.final_state == JOB_COMPLETE &&
    result.return_code == 0 &&
    result.error_code == MFOS_OK
  }

  predicate BobDeniedPath(result: SliceResult) {
    result.name == BOB_DENIED_ALICE_DATASET &&
    result.final_state == JOB_FAILED &&
    result.error_code == MFOS_ERR_POLICY_DENIED &&
    result.reason_code == DATASET_READ_NOT_PERMITTED &&
    !result.dataset_handle_created &&
    result.audit_before_final_result &&
    result.spool_summary_exists &&
    result.operator_display_failed
  }

  lemma HelloJobContract()
    ensures HelloJobComplete(HelloJobResult())
    ensures HelloJobResult().final_state == JOB_COMPLETE
    ensures HelloJobResult().return_code == 0
  {
  }

  lemma BobDeniedAliceDatasetContract()
    ensures BobDeniedPath(BobDeniedAliceDatasetResult())
    ensures BobDeniedAliceDatasetResult().error_code == MFOS_ERR_POLICY_DENIED
    ensures BobDeniedAliceDatasetResult().reason_code == DATASET_READ_NOT_PERMITTED
    ensures !BobDeniedAliceDatasetResult().dataset_handle_created
    ensures BobDeniedAliceDatasetResult().audit_before_final_result
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
