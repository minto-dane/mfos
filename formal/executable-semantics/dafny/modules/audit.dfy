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
    AuditRecord(record_id, 1, 1, decision.context.correlation_id, sequence, 1,
      decision.subject, decision.object_ref, decision.operation, decision.policy_version,
      decision.result, decision.error_code, decision.reason_code, before_return, true, sequence, sequence + 1)
  }

  predicate AuditRecordMinimumFields(record: AuditRecord) {
    ValidId(record.record_id) &&
    record.schema_version > 0 &&
    ValidId(record.component_id) &&
    ValidCorrelationId(record.correlation_id) &&
    record.record_type > 0 &&
    ValidId(record.subject.principal.principal_id) &&
    ValidId(record.object_ref.object_id) &&
    ValidPolicyVersion(record.policy_version) &&
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

  predicate AuditRecordBindsDecision(record: AuditRecord, decision: SecurityDecision) {
    record.correlation_id == decision.context.correlation_id &&
    record.subject == decision.subject &&
    record.object_ref == decision.object_ref &&
    record.operation == decision.operation &&
    record.policy_version == decision.policy_version &&
    record.decision_result == decision.result &&
    record.error_code == decision.error_code &&
    record.reason_code == decision.reason_code
  }

  predicate DenyBeforeReturn(decision: SecurityDecision, record: AuditRecord) {
    decision.result == DENY &&
    Authorization.RequiresAudit(decision) &&
    AuditEvidence(record) &&
    AuditRecordBindsDecision(record, decision) &&
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

  predicate RequiredAuditSatisfiedForFinalResult(decision: SecurityDecision, records: seq<AuditRecord>) {
    !Authorization.RequiresAudit(decision) || ExistsBeforeReturnAudit(decision, records)
  }

  predicate HashChainTamperCondition(previous: AuditRecord, next: AuditRecord) {
    previous.record_hash != next.previous_hash || !(previous.sequence < next.sequence)
  }

  predicate DuplicateAuditRecordId(left: AuditRecord, right: AuditRecord) {
    left.record_id == right.record_id
  }

  predicate AuditQueryAuthorized(decision: SecurityDecision) {
    decision.resource_class == RESOURCE_AUDIT_STREAM &&
    decision.operation == OP_QUERY &&
    Authorization.DecisionAllowsProtectedEffect(decision)
  }

  predicate RedactionPolicySatisfied(redaction_policy_valid: bool) {
    redaction_policy_valid
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
      AuditFinalization(DENY, MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE, prior_records, false)
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
    ensures AuditRecordBindsDecision(record, decision)
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
    requires ValidId(decision.subject.principal.principal_id)
    requires ValidId(decision.object_ref.object_id)
    requires ValidPolicyVersion(decision.policy_version)
    requires ValidId(next_record_id)
    ensures FinalizeDeniedOperation(decision, prior_records, next_record_id, true).final_result == DENY
    ensures FinalizeDeniedOperation(decision, prior_records, next_record_id, true).final_error == decision.error_code
    ensures !DecisionIsSuccess(FinalizeDeniedOperation(decision, prior_records, next_record_id, true).final_result)
    ensures ExistsBeforeReturnAudit(decision, FinalizeDeniedOperation(decision, prior_records, next_record_id, true).records_after)
    ensures RequiredAuditSatisfiedForFinalResult(decision, FinalizeDeniedOperation(decision, prior_records, next_record_id, true).records_after)
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
    ensures !IsSuccessError(FinalizeDeniedOperation(decision, prior_records, next_record_id, false).final_error)
    ensures !FinalizeDeniedOperation(decision, prior_records, next_record_id, false).result_released
  {
  }

  lemma INV_AUDIT_RECORD_HAS_REQUIRED_BINDINGS(decision: SecurityDecision, record_id: MfosId, sequence: SequenceNumber, before_return: bool)
    requires ValidId(record_id)
    requires ValidCorrelationId(decision.context.correlation_id)
    requires ValidId(decision.subject.principal.principal_id)
    requires ValidId(decision.object_ref.object_id)
    requires ValidPolicyVersion(decision.policy_version)
    ensures AuditRecordMinimumFields(ConstructAuditRecord(decision, record_id, sequence, before_return))
    ensures AuditRecordBindsDecision(ConstructAuditRecord(decision, record_id, sequence, before_return), decision)
  {
  }

  lemma INV_AUDIT_MISSING_CORRELATION_REJECTED(record: AuditRecord)
    requires !ValidCorrelationId(record.correlation_id)
    ensures !AuditRecordMinimumFields(record)
    ensures !AuditEvidence(record)
  {
  }

  lemma INV_AUDIT_HASH_CHAIN_VALID(records: seq<AuditRecord>)
    requires ValidHashChain(records)
    ensures forall i :: 0 < i < |records| ==> HashLinked(records[i - 1], records[i])
  {
  }

  lemma INV_AUDIT_HASH_CHAIN_MISMATCH_TAMPER(previous: AuditRecord, next: AuditRecord)
    requires HashChainTamperCondition(previous, next)
    ensures !HashLinked(previous, next)
  {
  }

  lemma INV_AUDIT_UNAUTHORIZED_QUERY_DENIED(decision: SecurityDecision)
    requires decision.resource_class == RESOURCE_AUDIT_STREAM
    requires decision.operation == OP_QUERY
    requires !Authorization.DecisionAllowsProtectedEffect(decision)
    ensures !AuditQueryAuthorized(decision)
  {
  }

  lemma INV_AUDIT_REDACTION_POLICY_FAILURE_DENIED(redaction_policy_valid: bool)
    requires !redaction_policy_valid
    ensures !RedactionPolicySatisfied(redaction_policy_valid)
  {
  }

  lemma INV_AUDIT_DUPLICATE_RECORD_ID_REJECTED(left: AuditRecord, right: AuditRecord)
    requires left.record_id == right.record_id
    ensures DuplicateAuditRecordId(left, right)
  {
  }

  lemma INV_AUDIT_NON_MONOTONIC_SEQUENCE_REJECTED(previous: AuditRecord, next: AuditRecord)
    requires !(previous.sequence < next.sequence)
    ensures HashChainTamperCondition(previous, next)
    ensures !HashLinked(previous, next)
  {
  }

  lemma INV_AUDIT_RECORD_BINDS_SECURITY_DECISION(decision: SecurityDecision, record_id: MfosId, sequence: SequenceNumber, before_return: bool)
    requires ValidId(record_id)
    requires ValidCorrelationId(decision.context.correlation_id)
    requires ValidId(decision.subject.principal.principal_id)
    requires ValidId(decision.object_ref.object_id)
    requires ValidPolicyVersion(decision.policy_version)
    ensures AuditRecordBindsDecision(ConstructAuditRecord(decision, record_id, sequence, before_return), decision)
    ensures ConstructAuditRecord(decision, record_id, sequence, before_return).policy_version == decision.policy_version
    ensures ConstructAuditRecord(decision, record_id, sequence, before_return).reason_code == decision.reason_code
  {
  }

  lemma INV_AUTH_AUDIT_DENY_WITH_OBLIGATION_LINKS_RECORD(decision: SecurityDecision, prior_records: seq<AuditRecord>, next_record_id: MfosId)
    requires decision.result == DENY
    requires Authorization.RequiresAudit(decision)
    requires ValidCorrelationId(decision.context.correlation_id)
    requires ValidId(decision.subject.principal.principal_id)
    requires ValidId(decision.object_ref.object_id)
    requires ValidPolicyVersion(decision.policy_version)
    requires ValidId(next_record_id)
    ensures ExistsBeforeReturnAudit(decision, FinalizeDeniedOperation(decision, prior_records, next_record_id, true).records_after)
    ensures RequiredAuditSatisfiedForFinalResult(decision, FinalizeDeniedOperation(decision, prior_records, next_record_id, true).records_after)
  {
    INV_AUDIT_DENY_TRANSITION_WRITES_BEFORE_RETURN(decision, prior_records, next_record_id);
  }

  lemma INV_AUTH_AUDIT_REQUIRED_UNAVAILABLE_PREVENTS_SUCCESS(decision: SecurityDecision, prior_records: seq<AuditRecord>, next_record_id: MfosId)
    requires decision.result == DENY
    requires Authorization.RequiresAudit(decision)
    requires ValidCorrelationId(decision.context.correlation_id)
    requires ValidId(next_record_id)
    ensures FinalizeDeniedOperation(decision, prior_records, next_record_id, false).final_error == MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE
    ensures !DecisionIsSuccess(FinalizeDeniedOperation(decision, prior_records, next_record_id, false).final_result)
    ensures !FinalizeDeniedOperation(decision, prior_records, next_record_id, false).result_released
  {
  }

  lemma INV_AUTH_FAIL_CLOSED_RESULTS_CANNOT_BYPASS_AUDIT(decision: SecurityDecision, records: seq<AuditRecord>)
    requires DecisionIsFailClosed(decision.result)
    requires Authorization.RequiresAudit(decision)
    requires !ExistsBeforeReturnAudit(decision, records)
    ensures !RequiredAuditSatisfiedForFinalResult(decision, records)
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
