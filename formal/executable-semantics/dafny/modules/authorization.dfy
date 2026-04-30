// MFOS Phase 1 Dafny executable semantics: authorization model.
// This is not securityd and not a production policy engine.

include "common.dfy"
include "errors.dfy"
include "types.dfy"

module Authorization {
  import opened Common
  import opened Errors
  import opened Types

  datatype AuthorizationEvidence = AuthorizationEvidence(
    mfa_present: bool,
    dual_control_approval_count: nat,
    break_glass_reason_present: bool,
    break_glass_expiry_present: bool,
    guard_approval_present: bool,
    operator_confirmation_present: bool,
    delegation_fresh: bool,
    wildcard_scope_valid: bool
  )

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

  predicate DecisionBindsRequest(binding: PolicyBinding, context: DecisionContext, decision: SecurityDecision) {
    decision.subject == binding.subject &&
    decision.object_ref == binding.object_ref &&
    decision.operation == binding.operation &&
    decision.resource_class == binding.resource_class &&
    decision.policy_version == binding.policy_version &&
    decision.context == context
  }

  predicate MfaSatisfied(evidence: AuthorizationEvidence) {
    evidence.mfa_present
  }

  predicate DualControlSatisfied(evidence: AuthorizationEvidence) {
    evidence.dual_control_approval_count >= 2
  }

  predicate BreakGlassSatisfied(evidence: AuthorizationEvidence) {
    evidence.break_glass_reason_present && evidence.break_glass_expiry_present
  }

  predicate GuardApprovalSatisfied(evidence: AuthorizationEvidence) {
    evidence.guard_approval_present
  }

  predicate OperatorConfirmationSatisfied(evidence: AuthorizationEvidence) {
    evidence.operator_confirmation_present
  }

  predicate AdditionalRequirementSatisfied(decision: SecurityDecision, evidence: AuthorizationEvidence) {
    match decision.result
    case REQUIRE_MFA => MfaSatisfied(evidence)
    case REQUIRE_DUAL_CONTROL => DualControlSatisfied(evidence)
    case REQUIRE_BREAK_GLASS => BreakGlassSatisfied(evidence)
    case REQUIRE_GUARD_APPROVAL => GuardApprovalSatisfied(evidence)
    case REQUIRE_OPERATOR_CONFIRMATION => OperatorConfirmationSatisfied(evidence)
    case _ => false
  }

  predicate DelegationFresh(evidence: AuthorizationEvidence) {
    evidence.delegation_fresh
  }

  predicate ScopedWildcardPolicy(evidence: AuthorizationEvidence) {
    evidence.wildcard_scope_valid
  }

  predicate PendingAuthorizationDecision(decision: SecurityDecision) {
    decision.result == REQUIRE_MFA ||
    decision.result == REQUIRE_DUAL_CONTROL ||
    decision.result == REQUIRE_BREAK_GLASS ||
    decision.result == REQUIRE_GUARD_APPROVAL ||
    decision.result == REQUIRE_OPERATOR_CONFIRMATION
  }

  predicate RequiredObligationsConsistent(decision: SecurityDecision) {
    (decision.result == REQUIRE_MFA ==> OBLIGATION_MFA in decision.obligations) &&
    (decision.result == REQUIRE_DUAL_CONTROL ==> OBLIGATION_DUAL_CONTROL in decision.obligations) &&
    (decision.result == REQUIRE_BREAK_GLASS ==> OBLIGATION_BREAK_GLASS_REASON in decision.obligations && OBLIGATION_BREAK_GLASS_EXPIRY in decision.obligations) &&
    (decision.result == REQUIRE_GUARD_APPROVAL ==> OBLIGATION_GUARD_APPROVAL in decision.obligations) &&
    (decision.result == REQUIRE_OPERATOR_CONFIRMATION ==> OBLIGATION_OPERATOR_CONFIRMATION in decision.obligations)
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
    requires binding.subject.authenticated
    requires binding.policy_version == context.policy_version
    requires binding.result == SPEC_GAP
    ensures !DecisionIsSuccess(EvaluateSecurityDecision(binding, context).result)
    ensures EvaluateSecurityDecision(binding, context).error_code == MFOS_ERR_SPEC_GAP
  {
  }

  lemma INV_AUTH_UNSUPPORTED_NOT_SUCCESS(binding: PolicyBinding, context: DecisionContext)
    requires binding.subject.authenticated
    requires binding.policy_version == context.policy_version
    requires binding.result == UNSUPPORTED
    ensures !DecisionIsSuccess(EvaluateSecurityDecision(binding, context).result)
    ensures EvaluateSecurityDecision(binding, context).error_code == MFOS_ERR_UNSUPPORTED
  {
  }

  lemma INV_AUTH_DENY_NOT_SUCCESS(binding: PolicyBinding, context: DecisionContext)
    requires binding.subject.authenticated
    requires binding.policy_version == context.policy_version
    requires binding.result == DENY
    ensures !DecisionIsSuccess(EvaluateSecurityDecision(binding, context).result)
    ensures EvaluateSecurityDecision(binding, context).error_code == MFOS_ERR_POLICY_DENIED
  {
  }

  lemma INV_AUTH_DENY_MAPS_POLICY_DENIED(binding: PolicyBinding, context: DecisionContext)
    requires binding.subject.authenticated
    requires binding.policy_version == context.policy_version
    requires binding.result == DENY
    ensures EvaluateSecurityDecision(binding, context).error_code == MFOS_ERR_POLICY_DENIED
    ensures EvaluateSecurityDecision(binding, context).reason_code == binding.reason_code
  {
  }

  lemma INV_AUTH_EVALUATED_DENY_IS_FAIL_CLOSED(binding: PolicyBinding, context: DecisionContext)
    requires EvaluateSecurityDecision(binding, context).result == DENY
    ensures !IsSuccessError(EvaluateSecurityDecision(binding, context).error_code)
    ensures FailClosedAuthorization(EvaluateSecurityDecision(binding, context))
  {
  }

  lemma INV_AUTH_POLICY_VERSION_BOUND(binding: PolicyBinding, context: DecisionContext)
    ensures EvaluateSecurityDecision(binding, context).policy_version == binding.policy_version
  {
  }

  lemma INV_AUTH_DECISION_BINDS_REQUEST(binding: PolicyBinding, context: DecisionContext)
    ensures DecisionBindsRequest(binding, context, EvaluateSecurityDecision(binding, context))
  {
  }

  lemma INV_AUTH_ALLOW_BINDS_DECISION_CONTEXT(binding: PolicyBinding, context: DecisionContext)
    requires binding.subject.authenticated
    requires ValidId(binding.subject.principal.principal_id)
    requires ValidId(binding.object_ref.object_id)
    requires ValidPolicyVersion(binding.policy_version)
    requires ValidCorrelationId(context.correlation_id)
    requires binding.policy_version == context.policy_version
    requires binding.result == ALLOW
    ensures DecisionAllowsProtectedEffect(EvaluateSecurityDecision(binding, context))
    ensures DecisionBindsRequest(binding, context, EvaluateSecurityDecision(binding, context))
  {
  }

  lemma INV_AUTH_ALLOW_MAPPING(binding: PolicyBinding, context: DecisionContext)
    requires binding.subject.authenticated
    requires ValidId(binding.subject.principal.principal_id)
    requires ValidId(binding.object_ref.object_id)
    requires ValidPolicyVersion(binding.policy_version)
    requires ValidCorrelationId(context.correlation_id)
    requires binding.policy_version == context.policy_version
    requires binding.result == ALLOW
    ensures EvaluateSecurityDecision(binding, context).result == ALLOW
    ensures EvaluateSecurityDecision(binding, context).error_code == MFOS_OK
    ensures EvaluateSecurityDecision(binding, context).reason_code == REASON_OK
    ensures DecisionAllowsProtectedEffect(EvaluateSecurityDecision(binding, context))
    ensures DecisionBindsRequest(binding, context, EvaluateSecurityDecision(binding, context))
  {
  }

  lemma INV_AUTH_ALLOW_WITH_AUDIT_BINDS_DECISION_CONTEXT(binding: PolicyBinding, context: DecisionContext)
    requires binding.subject.authenticated
    requires ValidId(binding.subject.principal.principal_id)
    requires ValidId(binding.object_ref.object_id)
    requires ValidPolicyVersion(binding.policy_version)
    requires ValidCorrelationId(context.correlation_id)
    requires binding.policy_version == context.policy_version
    requires binding.result == ALLOW_WITH_AUDIT
    requires OBLIGATION_AUDIT in binding.obligations
    ensures DecisionAllowsProtectedEffect(EvaluateSecurityDecision(binding, context))
    ensures RequiresAudit(EvaluateSecurityDecision(binding, context))
    ensures DecisionBindsRequest(binding, context, EvaluateSecurityDecision(binding, context))
  {
  }

  lemma INV_AUTH_ALLOW_WITH_AUDIT_MAPPING(binding: PolicyBinding, context: DecisionContext)
    requires binding.subject.authenticated
    requires ValidId(binding.subject.principal.principal_id)
    requires ValidId(binding.object_ref.object_id)
    requires ValidPolicyVersion(binding.policy_version)
    requires ValidCorrelationId(context.correlation_id)
    requires binding.policy_version == context.policy_version
    requires binding.result == ALLOW_WITH_AUDIT
    requires OBLIGATION_AUDIT in binding.obligations
    ensures EvaluateSecurityDecision(binding, context).result == ALLOW_WITH_AUDIT
    ensures EvaluateSecurityDecision(binding, context).error_code == MFOS_OK
    ensures EvaluateSecurityDecision(binding, context).reason_code == REASON_OK
    ensures RequiresAudit(EvaluateSecurityDecision(binding, context))
    ensures DecisionAllowsProtectedEffect(EvaluateSecurityDecision(binding, context))
    ensures DecisionBindsRequest(binding, context, EvaluateSecurityDecision(binding, context))
  {
  }

  lemma INV_AUTH_PENDING_REQUIREMENTS_DO_NOT_ALLOW_EFFECT(decision: SecurityDecision, satisfied: set<DecisionObligation>)
    requires PendingAuthorizationDecision(decision)
    ensures !DecisionIsSuccess(decision.result)
    ensures !DecisionAllowsProtectedEffect(decision)
    ensures !CanCreateProtectedResourceHandle(decision, satisfied)
  {
  }

  lemma INV_AUTH_REQUIRE_MFA_NOT_SUCCESS_UNTIL_EVIDENCE(binding: PolicyBinding, context: DecisionContext, evidence: AuthorizationEvidence)
    requires binding.subject.authenticated
    requires binding.policy_version == context.policy_version
    requires binding.result == REQUIRE_MFA
    requires !evidence.mfa_present
    ensures !DecisionIsSuccess(EvaluateSecurityDecision(binding, context).result)
    ensures !AdditionalRequirementSatisfied(EvaluateSecurityDecision(binding, context), evidence)
  {
  }

  lemma INV_AUTH_REQUIRE_MFA_PENDING(binding: PolicyBinding, context: DecisionContext)
    requires binding.subject.authenticated
    requires binding.policy_version == context.policy_version
    requires binding.result == REQUIRE_MFA
    requires OBLIGATION_MFA in binding.obligations
    ensures PendingAuthorizationDecision(EvaluateSecurityDecision(binding, context))
    ensures RequiredObligationsConsistent(EvaluateSecurityDecision(binding, context))
    ensures !DecisionAllowsProtectedEffect(EvaluateSecurityDecision(binding, context))
  {
  }

  lemma INV_AUTH_REQUIRE_DUAL_CONTROL_NOT_SUCCESS_UNTIL_EVIDENCE(binding: PolicyBinding, context: DecisionContext, evidence: AuthorizationEvidence)
    requires binding.subject.authenticated
    requires binding.policy_version == context.policy_version
    requires binding.result == REQUIRE_DUAL_CONTROL
    requires evidence.dual_control_approval_count < 2
    ensures !DecisionIsSuccess(EvaluateSecurityDecision(binding, context).result)
    ensures !AdditionalRequirementSatisfied(EvaluateSecurityDecision(binding, context), evidence)
  {
  }

  lemma INV_AUTH_REQUIRE_DUAL_CONTROL_PENDING(binding: PolicyBinding, context: DecisionContext)
    requires binding.subject.authenticated
    requires binding.policy_version == context.policy_version
    requires binding.result == REQUIRE_DUAL_CONTROL
    requires OBLIGATION_DUAL_CONTROL in binding.obligations
    ensures PendingAuthorizationDecision(EvaluateSecurityDecision(binding, context))
    ensures RequiredObligationsConsistent(EvaluateSecurityDecision(binding, context))
    ensures !DecisionAllowsProtectedEffect(EvaluateSecurityDecision(binding, context))
  {
  }

  lemma INV_AUTH_REQUIRE_BREAK_GLASS_NOT_SUCCESS_WITHOUT_REASON(binding: PolicyBinding, context: DecisionContext, evidence: AuthorizationEvidence)
    requires binding.subject.authenticated
    requires binding.policy_version == context.policy_version
    requires binding.result == REQUIRE_BREAK_GLASS
    requires !evidence.break_glass_reason_present
    ensures !DecisionIsSuccess(EvaluateSecurityDecision(binding, context).result)
    ensures !AdditionalRequirementSatisfied(EvaluateSecurityDecision(binding, context), evidence)
  {
  }

  lemma INV_AUTH_REQUIRE_BREAK_GLASS_NOT_SUCCESS_WITHOUT_EXPIRY(binding: PolicyBinding, context: DecisionContext, evidence: AuthorizationEvidence)
    requires binding.subject.authenticated
    requires binding.policy_version == context.policy_version
    requires binding.result == REQUIRE_BREAK_GLASS
    requires !evidence.break_glass_expiry_present
    ensures !DecisionIsSuccess(EvaluateSecurityDecision(binding, context).result)
    ensures !AdditionalRequirementSatisfied(EvaluateSecurityDecision(binding, context), evidence)
  {
  }

  lemma INV_AUTH_REQUIRE_BREAK_GLASS_PENDING(binding: PolicyBinding, context: DecisionContext)
    requires binding.subject.authenticated
    requires binding.policy_version == context.policy_version
    requires binding.result == REQUIRE_BREAK_GLASS
    requires OBLIGATION_BREAK_GLASS_REASON in binding.obligations
    requires OBLIGATION_BREAK_GLASS_EXPIRY in binding.obligations
    ensures PendingAuthorizationDecision(EvaluateSecurityDecision(binding, context))
    ensures RequiredObligationsConsistent(EvaluateSecurityDecision(binding, context))
    ensures !DecisionAllowsProtectedEffect(EvaluateSecurityDecision(binding, context))
  {
  }

  lemma INV_AUTH_REQUIRE_GUARD_APPROVAL_NOT_SUCCESS_UNTIL_EVIDENCE(binding: PolicyBinding, context: DecisionContext, evidence: AuthorizationEvidence)
    requires binding.subject.authenticated
    requires binding.policy_version == context.policy_version
    requires binding.result == REQUIRE_GUARD_APPROVAL
    requires !evidence.guard_approval_present
    ensures !DecisionIsSuccess(EvaluateSecurityDecision(binding, context).result)
    ensures !AdditionalRequirementSatisfied(EvaluateSecurityDecision(binding, context), evidence)
  {
  }

  lemma INV_AUTH_REQUIRE_GUARD_APPROVAL_PENDING(binding: PolicyBinding, context: DecisionContext)
    requires binding.subject.authenticated
    requires binding.policy_version == context.policy_version
    requires binding.result == REQUIRE_GUARD_APPROVAL
    requires OBLIGATION_GUARD_APPROVAL in binding.obligations
    ensures PendingAuthorizationDecision(EvaluateSecurityDecision(binding, context))
    ensures RequiredObligationsConsistent(EvaluateSecurityDecision(binding, context))
    ensures !DecisionAllowsProtectedEffect(EvaluateSecurityDecision(binding, context))
  {
  }

  lemma INV_AUTH_REQUIRE_OPERATOR_CONFIRMATION_NOT_SUCCESS_UNTIL_EVIDENCE(binding: PolicyBinding, context: DecisionContext, evidence: AuthorizationEvidence)
    requires binding.subject.authenticated
    requires binding.policy_version == context.policy_version
    requires binding.result == REQUIRE_OPERATOR_CONFIRMATION
    requires !evidence.operator_confirmation_present
    ensures !DecisionIsSuccess(EvaluateSecurityDecision(binding, context).result)
    ensures !AdditionalRequirementSatisfied(EvaluateSecurityDecision(binding, context), evidence)
  {
  }

  lemma INV_AUTH_REQUIRE_OPERATOR_CONFIRMATION_PENDING(binding: PolicyBinding, context: DecisionContext)
    requires binding.subject.authenticated
    requires binding.policy_version == context.policy_version
    requires binding.result == REQUIRE_OPERATOR_CONFIRMATION
    requires OBLIGATION_OPERATOR_CONFIRMATION in binding.obligations
    ensures PendingAuthorizationDecision(EvaluateSecurityDecision(binding, context))
    ensures RequiredObligationsConsistent(EvaluateSecurityDecision(binding, context))
    ensures !DecisionAllowsProtectedEffect(EvaluateSecurityDecision(binding, context))
  {
  }

  lemma INV_AUTH_STALE_POLICY_VERSION_DENIED(binding: PolicyBinding, context: DecisionContext)
    requires binding.subject.authenticated
    requires binding.policy_version != context.policy_version
    ensures EvaluateSecurityDecision(binding, context).result == DENY
    ensures EvaluateSecurityDecision(binding, context).error_code == MFOS_ERR_POLICY_VERSION_MISMATCH
    ensures !DecisionIsSuccess(EvaluateSecurityDecision(binding, context).result)
  {
  }

  lemma INV_AUTH_EXPIRED_DELEGATION_REJECTED(evidence: AuthorizationEvidence)
    requires !evidence.delegation_fresh
    ensures !DelegationFresh(evidence)
  {
  }

  lemma INV_AUTH_POLICY_LINT_WILDCARD_REJECTED(evidence: AuthorizationEvidence)
    requires !evidence.wildcard_scope_valid
    ensures !ScopedWildcardPolicy(evidence)
  {
  }

  lemma INV_AUTH_EVALUATED_DECISION_NO_HANDLE_UNLESS_ALLOW(binding: PolicyBinding, context: DecisionContext, satisfied: set<DecisionObligation>)
    requires !DecisionIsSuccess(EvaluateSecurityDecision(binding, context).result)
    ensures !CanCreateProtectedResourceHandle(EvaluateSecurityDecision(binding, context), satisfied)
  {
  }

  lemma INV_AUTH_FAIL_CLOSED_DECISION_NO_HANDLE(decision: SecurityDecision, satisfied: set<DecisionObligation>)
    requires FailClosedAuthorization(decision)
    ensures !CanCreateProtectedResourceHandle(decision, satisfied)
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
