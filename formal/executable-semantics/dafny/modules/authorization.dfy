// MFOS Phase 1 Dafny executable semantics: authorization model.
// This is not securityd and not a production policy engine.

include "common.dfy"
include "errors.dfy"
include "types.dfy"

module Authorization {
  import opened Common
  import opened Errors
  import opened Types

  function EvaluateSecurityDecision(binding: PolicyBinding, context: DecisionContext): SecurityDecision {
    if !binding.subject.authenticated then
      SecurityDecision(binding.subject, binding.object_ref, binding.operation, binding.resource_class,
        DENY, MFOS_ERR_UNAUTHENTICATED, SUBJECT_NOT_AUTHENTICATED, binding.policy_version, {}, context)
    else if binding.policy_version != context.policy_version then
      SecurityDecision(binding.subject, binding.object_ref, binding.operation, binding.resource_class,
        DENY, MFOS_ERR_POLICY_VERSION_MISMATCH, STALE_POLICY_VERSION, binding.policy_version, {}, context)
    else if binding.result == UNSUPPORTED then
      SecurityDecision(binding.subject, binding.object_ref, binding.operation, binding.resource_class,
        UNSUPPORTED, MFOS_ERR_UNSUPPORTED, UNSUPPORTED_DECLARATION, binding.policy_version, binding.obligations, context)
    else if binding.result == SPEC_GAP then
      SecurityDecision(binding.subject, binding.object_ref, binding.operation, binding.resource_class,
        SPEC_GAP, MFOS_ERR_SPEC_GAP, SPECIFICATION_GAP, binding.policy_version, binding.obligations, context)
    else if binding.result == DENY then
      SecurityDecision(binding.subject, binding.object_ref, binding.operation, binding.resource_class,
        DENY, MFOS_ERR_POLICY_DENIED, binding.reason_code, binding.policy_version, binding.obligations, context)
    else
      SecurityDecision(binding.subject, binding.object_ref, binding.operation, binding.resource_class,
        binding.result, MFOS_OK, REASON_OK, binding.policy_version, binding.obligations, context)
  }

  predicate DecisionWellFormed(decision: SecurityDecision) {
    ValidSubject(decision.subject) &&
    ValidId(decision.object_ref.object_id) &&
    ValidPolicyVersion(decision.policy_version) &&
    ValidCorrelationId(decision.context.correlation_id) &&
    decision.policy_version == decision.context.policy_version
  }

  predicate DecisionAllowsProtectedEffect(decision: SecurityDecision) {
    DecisionWellFormed(decision) &&
    DecisionIsSuccess(decision.result) &&
    decision.error_code == MFOS_OK
  }

  predicate RequiredObligationsSatisfied(decision: SecurityDecision, satisfied: set<DecisionObligation>) {
    decision.obligations <= satisfied
  }

  predicate CanCreateProtectedResourceHandle(decision: SecurityDecision, satisfied: set<DecisionObligation>) {
    DecisionAllowsProtectedEffect(decision) &&
    RequiredObligationsSatisfied(decision, satisfied)
  }

  predicate RequiresAudit(decision: SecurityDecision) {
    OBLIGATION_AUDIT in decision.obligations
  }

  predicate FailClosedAuthorization(decision: SecurityDecision) {
    DecisionIsFailClosed(decision.result) && IsFailClosedError(decision.error_code)
  }

  lemma INV_AUTH_NO_HANDLE_WITHOUT_ALLOW(decision: SecurityDecision, satisfied: set<DecisionObligation>)
    requires !DecisionAllowsProtectedEffect(decision)
    ensures !CanCreateProtectedResourceHandle(decision, satisfied)
  {
  }

  lemma INV_AUTH_SPEC_GAP_NOT_SUCCESS(binding: PolicyBinding, context: DecisionContext)
    requires binding.result == SPEC_GAP
    ensures !DecisionIsSuccess(EvaluateSecurityDecision(binding, context).result)
    ensures EvaluateSecurityDecision(binding, context).error_code == MFOS_ERR_SPEC_GAP
  {
  }

  lemma INV_AUTH_UNSUPPORTED_NOT_SUCCESS(binding: PolicyBinding, context: DecisionContext)
    requires binding.result == UNSUPPORTED
    ensures !DecisionIsSuccess(EvaluateSecurityDecision(binding, context).result)
    ensures EvaluateSecurityDecision(binding, context).error_code == MFOS_ERR_UNSUPPORTED
  {
  }

  lemma PolicyDeniedMappingForDatasetRead(binding: PolicyBinding, context: DecisionContext)
    requires binding.subject.authenticated
    requires binding.operation == OP_READ
    requires binding.resource_class == RESOURCE_DATASET
    requires binding.result == DENY
    requires binding.reason_code == DATASET_READ_NOT_PERMITTED
    requires binding.policy_version == context.policy_version
    ensures EvaluateSecurityDecision(binding, context).error_code == MFOS_ERR_POLICY_DENIED
    ensures EvaluateSecurityDecision(binding, context).reason_code == DATASET_READ_NOT_PERMITTED
  {
  }
}
