// MFOS Phase 1 Dafny executable semantics: audit model.
// This is symbolic evidence logic, not auditd storage.

include "common.dfy"
include "errors.dfy"
include "types.dfy"
include "authorization.dfy"

module Audit {
  import opened Common
  import opened Errors
  import opened Types
  import Authorization

  datatype AuditFinalization = AuditFinalization(
    final_result: DecisionResult,
    final_error: ErrorCode,
    records_after: seq<AuditRecord>,
    result_released: bool
  )

  function ConstructAuditRecord(decision: SecurityDecision, record_id: MfosId, sequence: SequenceNumber, before_return: bool): AuditRecord {
    AuditRecord(record_id, decision.context.correlation_id, sequence, 1,
      decision.result, decision.error_code, decision.reason_code, before_return, true, sequence, sequence + 1)
  }

  predicate AuditRecordMinimumFields(record: AuditRecord) {
    ValidId(record.record_id) &&
    ValidCorrelationId(record.correlation_id) &&
    record.record_type > 0 &&
    record.record_hash > 0
  }

  predicate AuditEvidence(record: AuditRecord) {
    AuditRecordMinimumFields(record) && record.durable
  }

  predicate HashLinked(previous: AuditRecord, next: AuditRecord) {
    previous.record_hash == next.previous_hash &&
    previous.sequence < next.sequence
  }

  predicate ValidHashChain(records: seq<AuditRecord>) {
    (forall i :: 0 <= i < |records| ==> AuditEvidence(records[i])) &&
    (forall i :: 0 < i < |records| ==> HashLinked(records[i - 1], records[i]))
  }

  predicate DenyBeforeReturn(decision: SecurityDecision, record: AuditRecord) {
    decision.result == DENY &&
    Authorization.RequiresAudit(decision) &&
    AuditEvidence(record) &&
    record.correlation_id == decision.context.correlation_id &&
    record.decision_result == DENY &&
    record.error_code == decision.error_code &&
    record.reason_code == decision.reason_code &&
    record.before_return
  }

  predicate ExistsBeforeReturnAudit(decision: SecurityDecision, records: seq<AuditRecord>) {
    exists i :: 0 <= i < |records| && DenyBeforeReturn(decision, records[i])
  }

  predicate DenyWithAuditObligationSatisfiedBeforeReturn(decision: SecurityDecision, records: seq<AuditRecord>) {
    decision.result == DENY &&
    Authorization.RequiresAudit(decision) &&
    ExistsBeforeReturnAudit(decision, records)
  }

  predicate AuditFailurePolicyFailClosed(audit_available: bool, decision: SecurityDecision) {
    !audit_available && Authorization.RequiresAudit(decision)
  }

  function FinalizeDeniedOperation(decision: SecurityDecision, prior_records: seq<AuditRecord>, next_record_id: MfosId, audit_available: bool): AuditFinalization
    requires decision.result == DENY
    requires Authorization.RequiresAudit(decision)
    requires ValidCorrelationId(decision.context.correlation_id)
    requires ValidId(next_record_id)
  {
    if audit_available then
      var record := ConstructAuditRecord(decision, next_record_id, |prior_records| + 1, true);
      AuditFinalization(DENY, decision.error_code, prior_records + [record], true)
    else
      AuditFinalization(DENY, MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE, prior_records, true)
  }

  predicate DiagnosticLogLineIsAuditRecord(is_log_line: bool, record: AuditRecord) {
    !is_log_line && AuditEvidence(record)
  }

  predicate SpoolEntryIsAuditEvidence(spool: SpoolEntry, record: AuditRecord) {
    false
  }

  lemma INV_AUDIT_DENY_BEFORE_RETURN(decision: SecurityDecision, record: AuditRecord)
    requires DenyBeforeReturn(decision, record)
    ensures record.before_return
    ensures AuditEvidence(record)
    ensures record.decision_result == DENY
  {
  }

  lemma INV_AUDIT_DENY_WITH_OBLIGATION_HAS_BEFORE_RETURN_RECORD(decision: SecurityDecision, records: seq<AuditRecord>)
    requires DenyWithAuditObligationSatisfiedBeforeReturn(decision, records)
    ensures ExistsBeforeReturnAudit(decision, records)
  {
  }

  lemma INV_AUDIT_DENY_TRANSITION_WRITES_BEFORE_RETURN(decision: SecurityDecision, prior_records: seq<AuditRecord>, next_record_id: MfosId)
    requires decision.result == DENY
    requires Authorization.RequiresAudit(decision)
    requires ValidCorrelationId(decision.context.correlation_id)
    requires ValidId(next_record_id)
    ensures FinalizeDeniedOperation(decision, prior_records, next_record_id, true).final_result == DENY
    ensures FinalizeDeniedOperation(decision, prior_records, next_record_id, true).final_error == decision.error_code
    ensures !DecisionIsSuccess(FinalizeDeniedOperation(decision, prior_records, next_record_id, true).final_result)
    ensures ExistsBeforeReturnAudit(decision, FinalizeDeniedOperation(decision, prior_records, next_record_id, true).records_after)
  {
    var record := ConstructAuditRecord(decision, next_record_id, |prior_records| + 1, true);
    assert FinalizeDeniedOperation(decision, prior_records, next_record_id, true).records_after == prior_records + [record];
    assert 0 <= |prior_records| < |prior_records + [record]|;
    assert (prior_records + [record])[|prior_records|] == record;
    assert DenyBeforeReturn(decision, record);
    assert ExistsBeforeReturnAudit(decision, prior_records + [record]);
  }

  lemma INV_AUDIT_DENY_TRANSITION_FAILS_CLOSED_WHEN_UNAVAILABLE(decision: SecurityDecision, prior_records: seq<AuditRecord>, next_record_id: MfosId)
    requires decision.result == DENY
    requires Authorization.RequiresAudit(decision)
    requires ValidCorrelationId(decision.context.correlation_id)
    requires ValidId(next_record_id)
    ensures FinalizeDeniedOperation(decision, prior_records, next_record_id, false).final_result == DENY
    ensures FinalizeDeniedOperation(decision, prior_records, next_record_id, false).final_error == MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE
    ensures !DecisionIsSuccess(FinalizeDeniedOperation(decision, prior_records, next_record_id, false).final_result)
  {
  }

  lemma INV_AUDIT_LOG_LINE_NOT_RECORD(record: AuditRecord)
    ensures !DiagnosticLogLineIsAuditRecord(true, record)
  {
  }

  lemma INV_AUDIT_SPOOL_NOT_EVIDENCE(spool: SpoolEntry, record: AuditRecord)
    ensures !SpoolEntryIsAuditEvidence(spool, record)
  {
  }
}
