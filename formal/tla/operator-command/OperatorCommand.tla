---- MODULE OperatorCommand ----
EXTENDS Naturals, FiniteSets

\* Phase 0.8 design model for MFOS operator command semantics.
\* This is a state-machine artifact, not production code.

CONSTANTS
  Commands,
  Subjects,
  Authorities,
  Targets,
  Policies,
  AutomationCommands,
  DestructiveCommands,
  ConfirmationCommands,
  DualControlCommands,
  EmergencyCommands,
  RootShellLikeCommands,
  NoSubject,
  NoAuthority,
  NoTarget,
  NoPolicy

VARIABLES
  state,
  subject,
  authority,
  target,
  policy,
  decision,
  auditPre,
  auditResult,
  confirmationSatisfied,
  dualApprovedBy,
  emergencyActive,
  sideEffect

vars ==
  << state, subject, authority, target, policy, decision, auditPre,
     auditResult, confirmationSatisfied, dualApprovedBy, emergencyActive,
     sideEffect >>

States == {
  "RECEIVED",
  "PARSED",
  "TARGET_RESOLVED",
  "AUTHZ_REQUESTED",
  "AUTHZ_DENIED",
  "CONFIRMATION_PENDING",
  "DUAL_CONTROL_PENDING",
  "AUDIT_PENDING",
  "EXECUTING",
  "COMPLETE",
  "DENIED",
  "FAILED_CLOSED",
  "UNSUPPORTED",
  "SPEC_GAP",
  "CANCELED",
  "EXPIRED"
}

TerminalStates == {
  "COMPLETE",
  "DENIED",
  "FAILED_CLOSED",
  "UNSUPPORTED",
  "SPEC_GAP",
  "CANCELED",
  "EXPIRED"
}

AllowDecisions == {
  "MFOS_AUTH_ALLOW",
  "MFOS_AUTH_ALLOW_WITH_OBLIGATIONS"
}
NonAllowDecisions == {
  "MFOS_AUTH_DENY",
  "MFOS_AUTH_REQUIRE_MFA",
  "MFOS_AUTH_REQUIRE_DUAL_CONTROL",
  "MFOS_AUTH_REQUIRE_BREAK_GLASS",
  "MFOS_AUTH_REQUIRE_GUARD_APPROVAL",
  "MFOS_AUTH_REQUIRE_OPERATOR_CONFIRMATION",
  "MFOS_AUTH_UNSUPPORTED",
  "MFOS_AUTH_SPEC_GAP",
  "MFOS_AUTH_NONE"
}

Init ==
  /\ state = [c \in Commands |-> "RECEIVED"]
  /\ subject = [c \in Commands |-> NoSubject]
  /\ authority = [c \in Commands |-> NoAuthority]
  /\ target = [c \in Commands |-> NoTarget]
  /\ policy = [c \in Commands |-> NoPolicy]
  /\ decision = [c \in Commands |-> "MFOS_AUTH_NONE"]
  /\ auditPre = [c \in Commands |-> FALSE]
  /\ auditResult = [c \in Commands |-> FALSE]
  /\ confirmationSatisfied = [c \in Commands |-> FALSE]
  /\ dualApprovedBy = [c \in Commands |-> NoSubject]
  /\ emergencyActive = [c \in Commands |-> FALSE]
  /\ sideEffect = [c \in Commands |-> FALSE]

Parse(c) ==
  /\ state[c] = "RECEIVED"
  /\ c \notin RootShellLikeCommands
  /\ \E s \in Subjects:
       subject' = [subject EXCEPT ![c] = s]
  /\ \E a \in Authorities:
       authority' = [authority EXCEPT ![c] = a]
  /\ \E p \in Policies:
       policy' = [policy EXCEPT ![c] = p]
  /\ state' = [state EXCEPT ![c] = "PARSED"]
  /\ UNCHANGED << target, decision, auditPre, auditResult,
                  confirmationSatisfied, dualApprovedBy, emergencyActive,
                  sideEffect >>

RejectRootShellLike(c) ==
  /\ state[c] = "RECEIVED"
  /\ c \in RootShellLikeCommands
  /\ state' = [state EXCEPT ![c] = "FAILED_CLOSED"]
  /\ auditResult' = [auditResult EXCEPT ![c] = TRUE]
  /\ UNCHANGED << target, subject, authority, policy, decision, auditPre,
                  confirmationSatisfied, dualApprovedBy, emergencyActive,
                  sideEffect >>

ResolveTarget(c) ==
  /\ state[c] = "PARSED"
  /\ \E t \in Targets:
       target' = [target EXCEPT ![c] = t]
  /\ state' = [state EXCEPT ![c] = "TARGET_RESOLVED"]
  /\ UNCHANGED << subject, authority, policy, decision, auditPre,
                  auditResult, confirmationSatisfied, dualApprovedBy,
                  emergencyActive, sideEffect >>

AuthorizeAllow(c) ==
  /\ state[c] = "TARGET_RESOLVED"
  /\ \E d \in AllowDecisions:
       decision' = [decision EXCEPT ![c] = d]
  /\ state' = [state EXCEPT ![c] = "AUDIT_PENDING"]
  /\ UNCHANGED << target, subject, authority, policy, auditPre,
                  auditResult, confirmationSatisfied, dualApprovedBy,
                  emergencyActive, sideEffect >>

AuthorizeDeny(c) ==
  /\ state[c] = "TARGET_RESOLVED"
  /\ \E d \in NonAllowDecisions \ {"MFOS_AUTH_NONE"}:
       decision' = [decision EXCEPT ![c] = d]
  /\ state' = [state EXCEPT ![c] = "DENIED"]
  /\ auditResult' = [auditResult EXCEPT ![c] = TRUE]
  /\ UNCHANGED << target, subject, authority, policy, auditPre,
                  confirmationSatisfied, dualApprovedBy, emergencyActive,
                  sideEffect >>

RequireConfirmation(c) ==
  /\ state[c] = "AUDIT_PENDING"
  /\ c \in ConfirmationCommands
  /\ ~confirmationSatisfied[c]
  /\ state' = [state EXCEPT ![c] = "CONFIRMATION_PENDING"]
  /\ UNCHANGED << target, subject, authority, policy, decision, auditPre,
                  auditResult, confirmationSatisfied, dualApprovedBy,
                  emergencyActive, sideEffect >>

Confirm(c) ==
  /\ state[c] = "CONFIRMATION_PENDING"
  /\ confirmationSatisfied' = [confirmationSatisfied EXCEPT ![c] = TRUE]
  /\ state' = [state EXCEPT ![c] = "AUDIT_PENDING"]
  /\ UNCHANGED << target, subject, authority, policy, decision, auditPre,
                  auditResult, dualApprovedBy, emergencyActive, sideEffect >>

RequireDualControl(c) ==
  /\ state[c] = "AUDIT_PENDING"
  /\ c \in DualControlCommands
  /\ dualApprovedBy[c] = NoSubject
  /\ state' = [state EXCEPT ![c] = "DUAL_CONTROL_PENDING"]
  /\ UNCHANGED << target, subject, authority, policy, decision, auditPre,
                  auditResult, confirmationSatisfied, dualApprovedBy,
                  emergencyActive, sideEffect >>

ApproveDualControl(c) ==
  /\ state[c] = "DUAL_CONTROL_PENDING"
  /\ \E a \in Subjects:
       /\ a # subject[c]
       /\ dualApprovedBy' = [dualApprovedBy EXCEPT ![c] = a]
  /\ state' = [state EXCEPT ![c] = "AUDIT_PENDING"]
  /\ UNCHANGED << target, subject, authority, policy, decision, auditPre,
                  auditResult, confirmationSatisfied, emergencyActive,
                  sideEffect >>

EnterEmergency(c) ==
  /\ state[c] = "AUDIT_PENDING"
  /\ c \in EmergencyCommands
  /\ ~emergencyActive[c]
  /\ emergencyActive' = [emergencyActive EXCEPT ![c] = TRUE]
  /\ state' = [state EXCEPT ![c] = "AUDIT_PENDING"]
  /\ UNCHANGED << target, subject, authority, policy, decision, auditPre,
                  auditResult, confirmationSatisfied, dualApprovedBy,
                  sideEffect >>

WritePreEffectAudit(c) ==
  /\ state[c] = "AUDIT_PENDING"
  /\ ~auditPre[c]
  /\ decision[c] \in AllowDecisions
  /\ (c \in ConfirmationCommands => confirmationSatisfied[c])
  /\ (c \in DualControlCommands => dualApprovedBy[c] \in Subjects /\ dualApprovedBy[c] # subject[c])
  /\ auditPre' = [auditPre EXCEPT ![c] = TRUE]
  /\ UNCHANGED << state, target, subject, authority, policy, decision,
                  auditResult, confirmationSatisfied, dualApprovedBy,
                  emergencyActive, sideEffect >>

Execute(c) ==
  /\ state[c] = "AUDIT_PENDING"
  /\ decision[c] \in AllowDecisions
  /\ subject[c] \in Subjects
  /\ authority[c] \in Authorities
  /\ target[c] \in Targets
  /\ policy[c] \in Policies
  /\ auditPre[c]
  /\ (c \in ConfirmationCommands => confirmationSatisfied[c])
  /\ (c \in DualControlCommands => dualApprovedBy[c] \in Subjects /\ dualApprovedBy[c] # subject[c])
  /\ c \notin RootShellLikeCommands
  /\ state' = [state EXCEPT ![c] = "EXECUTING"]
  /\ sideEffect' = [sideEffect EXCEPT ![c] = TRUE]
  /\ UNCHANGED << target, subject, authority, policy, decision, auditPre,
                  auditResult, confirmationSatisfied, dualApprovedBy,
                  emergencyActive >>

Complete(c) ==
  /\ state[c] = "EXECUTING"
  /\ auditResult' = [auditResult EXCEPT ![c] = TRUE]
  /\ state' = [state EXCEPT ![c] = "COMPLETE"]
  /\ UNCHANGED << target, subject, authority, policy, decision, auditPre,
                  confirmationSatisfied, dualApprovedBy, emergencyActive,
                  sideEffect >>

Expire(c) ==
  /\ state[c] \in {"CONFIRMATION_PENDING", "DUAL_CONTROL_PENDING", "AUDIT_PENDING"}
  /\ state' = [state EXCEPT ![c] = "EXPIRED"]
  /\ auditResult' = [auditResult EXCEPT ![c] = TRUE]
  /\ UNCHANGED << target, subject, authority, policy, decision, auditPre,
                  confirmationSatisfied, dualApprovedBy, emergencyActive,
                  sideEffect >>

Next ==
  \E c \in Commands:
       Parse(c)
    \/ RejectRootShellLike(c)
    \/ ResolveTarget(c)
    \/ AuthorizeAllow(c)
    \/ AuthorizeDeny(c)
    \/ RequireConfirmation(c)
    \/ Confirm(c)
    \/ RequireDualControl(c)
    \/ ApproveDualControl(c)
    \/ EnterEmergency(c)
    \/ WritePreEffectAudit(c)
    \/ Execute(c)
    \/ Complete(c)
    \/ Expire(c)

Spec == Init /\ [][Next]_vars

TypeOK ==
  /\ state \in [Commands -> States]
  /\ subject \in [Commands -> Subjects \cup {NoSubject}]
  /\ authority \in [Commands -> Authorities \cup {NoAuthority}]
  /\ target \in [Commands -> Targets \cup {NoTarget}]
  /\ policy \in [Commands -> Policies \cup {NoPolicy}]
  /\ decision \in [Commands -> AllowDecisions \cup NonAllowDecisions]
  /\ auditPre \in [Commands -> BOOLEAN]
  /\ auditResult \in [Commands -> BOOLEAN]
  /\ confirmationSatisfied \in [Commands -> BOOLEAN]
  /\ dualApprovedBy \in [Commands -> Subjects \cup {NoSubject}]
  /\ emergencyActive \in [Commands -> BOOLEAN]
  /\ sideEffect \in [Commands -> BOOLEAN]

NoExecuteWithoutAuthority ==
  \A c \in Commands:
    sideEffect[c] =>
      /\ subject[c] \in Subjects
      /\ authority[c] \in Authorities
      /\ target[c] \in Targets
      /\ policy[c] \in Policies
      /\ decision[c] \in AllowDecisions
      /\ auditPre[c]

ConfirmationBeforeDestructiveEffect ==
  \A c \in Commands:
    /\ c \in ConfirmationCommands
    /\ sideEffect[c]
    => confirmationSatisfied[c]

DualControlDistinctApprover ==
  \A c \in Commands:
    /\ c \in DualControlCommands
    /\ sideEffect[c]
    => /\ dualApprovedBy[c] \in Subjects
       /\ dualApprovedBy[c] # subject[c]

AutomationNoBypass ==
  \A c \in AutomationCommands:
    sideEffect[c] =>
      /\ decision[c] \in AllowDecisions
      /\ auditPre[c]
      /\ target[c] \in Targets
      /\ authority[c] \in Authorities

EmergencyNoAuditBypass ==
  \A c \in EmergencyCommands:
    sideEffect[c] => auditPre[c]

RootShellNeverSucceeds ==
  \A c \in RootShellLikeCommands:
    /\ state[c] # "EXECUTING"
    /\ state[c] # "COMPLETE"
    /\ ~sideEffect[c]

TerminalNoEffectCreation ==
  \A c \in Commands:
    state[c] \in {"DENIED", "FAILED_CLOSED", "UNSUPPORTED", "SPEC_GAP", "CANCELED", "EXPIRED"}
    => ~sideEffect[c]

=============================================================================
