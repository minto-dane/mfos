// MFOS Phase 1 Dafny executable semantics: operator console model.
// This is not operatord, a shell, or a hosted control plane.

include "common.dfy"
include "errors.dfy"
include "types.dfy"
include "authorization.dfy"
include "audit.dfy"

module OperatorConsole {
  import opened Common
  import opened Errors
  import opened Types
  import Authorization
  import Audit

  predicate CommandRequiresConfirmation(command: OperatorCommand) {
    command.authority == AUTH_DESTRUCTIVE || command.authority == AUTH_CANCEL
  }

  predicate CommandConfirmationSatisfied(command: OperatorCommand) {
    !CommandRequiresConfirmation(command) || command.confirmed
  }

  predicate OperatorCommandAuthorized(command: OperatorCommand, decision: SecurityDecision) {
    decision.resource_class == RESOURCE_OPERATOR_COMMAND &&
    (decision.operation == OP_DISPLAY || decision.operation == OP_DEFINE ||
      decision.operation == OP_SUBMIT || decision.operation == OP_CANCEL) &&
    Authorization.DecisionAllowsProtectedEffect(decision) &&
    CommandConfirmationSatisfied(command)
  }

  predicate AuditedOperatorCommand(command: OperatorCommand, decision: SecurityDecision, record: AuditRecord) {
    command.audited &&
    OperatorCommandAuthorized(command, decision) &&
    Audit.AuditEvidence(record) &&
    record.correlation_id == decision.context.correlation_id
  }

  predicate DualControlSatisfied(approval_count: nat) {
    approval_count >= 2
  }

  predicate DualControlCommandAuthorized(command: OperatorCommand, decision: SecurityDecision, approval_count: nat) {
    OperatorCommandAuthorized(command, decision) && DualControlSatisfied(approval_count)
  }

  predicate EmergencyModeAllowed(has_reason: bool, has_expiry: bool) {
    has_reason && has_expiry
  }

  predicate RootShellAsFirstPrivilegedUi(proposed: bool) {
    false
  }

  lemma INV_OPERATOR_NO_COMMAND_WITHOUT_AUTH(command: OperatorCommand, decision: SecurityDecision)
    requires !Authorization.DecisionAllowsProtectedEffect(decision)
    ensures !OperatorCommandAuthorized(command, decision)
  {
  }

  lemma INV_OPERATOR_NO_COMMAND_WITHOUT_AUDIT(command: OperatorCommand, decision: SecurityDecision, record: AuditRecord)
    requires command.audited
    requires !Audit.AuditEvidence(record)
    ensures !AuditedOperatorCommand(command, decision, record)
  {
  }

  lemma INV_OPERATOR_DESTRUCTIVE_WITHOUT_CONFIRMATION_DENIED(command: OperatorCommand, decision: SecurityDecision)
    requires CommandRequiresConfirmation(command)
    requires !command.confirmed
    ensures !OperatorCommandAuthorized(command, decision)
  {
  }

  lemma INV_OPERATOR_DUAL_CONTROL_SINGLE_APPROVAL_DENIED(command: OperatorCommand, decision: SecurityDecision)
    ensures !DualControlCommandAuthorized(command, decision, 1)
  {
  }

  lemma INV_OPERATOR_EMERGENCY_WITHOUT_REASON_OR_EXPIRY_DENIED(has_reason: bool, has_expiry: bool)
    requires !has_reason || !has_expiry
    ensures !EmergencyModeAllowed(has_reason, has_expiry)
  {
  }

  lemma INV_OPERATOR_ROOT_SHELL_NOT_FIRST_UI()
    ensures !RootShellAsFirstPrivilegedUi(true)
  {
  }
}
