----------------------------- MODULE MFOSAuthorization -----------------------------
EXTENDS Naturals, Sequences

\* Artifact ID: MFOS-FORMAL-AUTH-0001
\* Owning spec: MFOS-SPEC-06-AUTHORIZATION
\* Phase 0.8 design-state machine. This is not production implementation.

DecisionResults ==
  { "MFOS_AUTH_ALLOW",
    "MFOS_AUTH_ALLOW_WITH_OBLIGATIONS",
    "MFOS_AUTH_DENY",
    "MFOS_AUTH_REQUIRE_MFA",
    "MFOS_AUTH_REQUIRE_DUAL_CONTROL",
    "MFOS_AUTH_REQUIRE_BREAK_GLASS",
    "MFOS_AUTH_REQUIRE_OPERATOR_CONFIRMATION",
    "MFOS_AUTH_REQUIRE_GUARD_APPROVAL",
    "MFOS_AUTH_UNSUPPORTED",
    "MFOS_AUTH_SPEC_GAP",
    "MFOS_AUTH_ERROR" }

AllowResults ==
  { "MFOS_AUTH_ALLOW", "MFOS_AUTH_ALLOW_WITH_OBLIGATIONS" }

RequireResults ==
  { "MFOS_AUTH_REQUIRE_MFA",
    "MFOS_AUTH_REQUIRE_DUAL_CONTROL",
    "MFOS_AUTH_REQUIRE_BREAK_GLASS",
    "MFOS_AUTH_REQUIRE_OPERATOR_CONFIRMATION",
    "MFOS_AUTH_REQUIRE_GUARD_APPROVAL" }

TerminalDenyResults ==
  { "MFOS_AUTH_DENY",
    "MFOS_AUTH_UNSUPPORTED",
    "MFOS_AUTH_SPEC_GAP",
    "MFOS_AUTH_ERROR" }

States ==
  { "MFOS_AUTH_STATE_REQUEST_RECEIVED",
    "MFOS_AUTH_STATE_VALIDATE_REQUEST",
    "MFOS_AUTH_STATE_CANONICALIZE_SUBJECT",
    "MFOS_AUTH_STATE_CANONICALIZE_OBJECT",
    "MFOS_AUTH_STATE_LOAD_POLICY",
    "MFOS_AUTH_STATE_EVALUATE_BINDINGS",
    "MFOS_AUTH_STATE_BUILD_OBLIGATIONS",
    "MFOS_AUTH_STATE_RETURN_DECISION",
    "MFOS_AUTH_STATE_SATISFY_PRE_EFFECT_OBLIGATIONS",
    "MFOS_AUTH_STATE_BIND_HANDLE",
    "MFOS_AUTH_STATE_EFFECT_ALLOWED",
    "MFOS_AUTH_STATE_DENIED_TERMINAL",
    "MFOS_AUTH_STATE_BEGIN_POLICY_TX",
    "MFOS_AUTH_STATE_VALIDATE_POLICY_SCHEMA",
    "MFOS_AUTH_STATE_AUTHORIZE_POLICY_CHANGE",
    "MFOS_AUTH_STATE_STAGE_POLICY",
    "MFOS_AUTH_STATE_RUN_POLICY_LINT",
    "MFOS_AUTH_STATE_REQUIRE_APPROVALS",
    "MFOS_AUTH_STATE_AUDIT_PRECOMMIT",
    "MFOS_AUTH_STATE_COMMIT_POLICY_VERSION",
    "MFOS_AUTH_STATE_INVALIDATE_DECISION_CACHE",
    "MFOS_AUTH_STATE_AUDIT_COMMIT",
    "MFOS_AUTH_STATE_POLICY_ACTIVE",
    "MFOS_AUTH_STATE_REQUEST_EMERGENCY_ACCESS",
    "MFOS_AUTH_STATE_AUTHENTICATE_OPERATOR",
    "MFOS_AUTH_STATE_AUTHORIZE_EMERGENCY_ACCESS",
    "MFOS_AUTH_STATE_REQUIRE_REASON",
    "MFOS_AUTH_STATE_SET_EXPIRY",
    "MFOS_AUTH_STATE_AUDIT_BEFORE_ENABLE",
    "MFOS_AUTH_STATE_ENABLE_EMERGENCY_CONTEXT",
    "MFOS_AUTH_STATE_MONITOR_EMERGENCY_USE",
    "MFOS_AUTH_STATE_EXPIRE_OR_REVOKE",
    "MFOS_AUTH_STATE_AUDIT_CLOSE",
    "MFOS_AUTH_STATE_INCIDENT_REVIEW_REQUIRED" }

VARIABLES
  state,
  result,
  obligationsSatisfied,
  auditReady,
  effectApplied,
  handleBound,
  policyVersion,
  policyEpoch,
  securityEpoch,
  cacheValid,
  delegationValid,
  emergencyActive,
  emergencyExpired,
  dualControlSatisfied,
  guardApprovalSatisfied,
  lintPassed,
  rollbackRequested

vars ==
  << state,
     result,
     obligationsSatisfied,
     auditReady,
     effectApplied,
     handleBound,
     policyVersion,
     policyEpoch,
     securityEpoch,
     cacheValid,
     delegationValid,
     emergencyActive,
     emergencyExpired,
     dualControlSatisfied,
     guardApprovalSatisfied,
     lintPassed,
     rollbackRequested >>

InitCommon ==
  /\ result = "MFOS_AUTH_ERROR"
  /\ obligationsSatisfied = FALSE
  /\ auditReady = FALSE
  /\ effectApplied = FALSE
  /\ handleBound = FALSE
  /\ policyVersion = 1
  /\ policyEpoch = 1
  /\ securityEpoch = 1
  /\ cacheValid = FALSE
  /\ delegationValid = TRUE
  /\ emergencyActive = FALSE
  /\ emergencyExpired = FALSE
  /\ dualControlSatisfied = FALSE
  /\ guardApprovalSatisfied = FALSE
  /\ lintPassed = FALSE
  /\ rollbackRequested = FALSE

Init ==
  /\ state \in { "MFOS_AUTH_STATE_REQUEST_RECEIVED",
                 "MFOS_AUTH_STATE_BEGIN_POLICY_TX",
                 "MFOS_AUTH_STATE_REQUEST_EMERGENCY_ACCESS" }
  /\ InitCommon

DecisionPath ==
  \/ /\ state = "MFOS_AUTH_STATE_REQUEST_RECEIVED"
     /\ state' = "MFOS_AUTH_STATE_VALIDATE_REQUEST"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_VALIDATE_REQUEST"
     /\ state' = "MFOS_AUTH_STATE_CANONICALIZE_SUBJECT"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_CANONICALIZE_SUBJECT"
     /\ state' = "MFOS_AUTH_STATE_CANONICALIZE_OBJECT"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_CANONICALIZE_OBJECT"
     /\ state' = "MFOS_AUTH_STATE_LOAD_POLICY"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_LOAD_POLICY"
     /\ state' = "MFOS_AUTH_STATE_EVALUATE_BINDINGS"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_EVALUATE_BINDINGS"
     /\ result' \in DecisionResults
     /\ state' = "MFOS_AUTH_STATE_BUILD_OBLIGATIONS"
     /\ UNCHANGED << obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_BUILD_OBLIGATIONS"
     /\ state' = "MFOS_AUTH_STATE_RETURN_DECISION"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>

EffectPath ==
  \/ /\ state = "MFOS_AUTH_STATE_RETURN_DECISION"
     /\ result \in AllowResults
     /\ state' = "MFOS_AUTH_STATE_SATISFY_PRE_EFFECT_OBLIGATIONS"
     /\ UNCHANGED << result, auditReady, effectApplied, handleBound,
                    policyVersion, policyEpoch, securityEpoch, cacheValid,
                    delegationValid, emergencyActive, emergencyExpired,
                    dualControlSatisfied, guardApprovalSatisfied, lintPassed,
                    rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_SATISFY_PRE_EFFECT_OBLIGATIONS"
     /\ obligationsSatisfied' = TRUE
     /\ auditReady' = TRUE
     /\ state' = "MFOS_AUTH_STATE_BIND_HANDLE"
     /\ UNCHANGED << result, effectApplied, handleBound, policyVersion,
                    policyEpoch, securityEpoch, cacheValid, delegationValid,
                    emergencyActive, emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_BIND_HANDLE"
     /\ result \in AllowResults
     /\ obligationsSatisfied
     /\ handleBound' = TRUE
     /\ state' = "MFOS_AUTH_STATE_EFFECT_ALLOWED"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    policyVersion, policyEpoch, securityEpoch, cacheValid,
                    delegationValid, emergencyActive, emergencyExpired,
                    dualControlSatisfied, guardApprovalSatisfied, lintPassed,
                    rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_EFFECT_ALLOWED"
     /\ result \in AllowResults
     /\ handleBound
     /\ obligationsSatisfied
     /\ effectApplied' = TRUE
     /\ UNCHANGED << state, result, obligationsSatisfied, auditReady,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>

DenyPath ==
  /\ state = "MFOS_AUTH_STATE_RETURN_DECISION"
  /\ result \in (TerminalDenyResults \cup RequireResults)
  /\ state' = "MFOS_AUTH_STATE_DENIED_TERMINAL"
  /\ effectApplied' = FALSE
  /\ handleBound' = FALSE
  /\ UNCHANGED << result, obligationsSatisfied, auditReady, policyVersion,
                 policyEpoch, securityEpoch, cacheValid, delegationValid,
                 emergencyActive, emergencyExpired, dualControlSatisfied,
                 guardApprovalSatisfied, lintPassed, rollbackRequested >>

PolicyTransaction ==
  \/ /\ state = "MFOS_AUTH_STATE_BEGIN_POLICY_TX"
     /\ state' = "MFOS_AUTH_STATE_VALIDATE_POLICY_SCHEMA"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_VALIDATE_POLICY_SCHEMA"
     /\ state' = "MFOS_AUTH_STATE_AUTHORIZE_POLICY_CHANGE"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_AUTHORIZE_POLICY_CHANGE"
     /\ state' = "MFOS_AUTH_STATE_STAGE_POLICY"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_STAGE_POLICY"
     /\ state' = "MFOS_AUTH_STATE_RUN_POLICY_LINT"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_RUN_POLICY_LINT"
     /\ lintPassed' = TRUE
     /\ state' = "MFOS_AUTH_STATE_REQUIRE_APPROVALS"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_REQUIRE_APPROVALS"
     /\ dualControlSatisfied' = TRUE
     /\ auditReady' = TRUE
     /\ state' = "MFOS_AUTH_STATE_AUDIT_PRECOMMIT"
     /\ UNCHANGED << result, obligationsSatisfied, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, guardApprovalSatisfied, lintPassed,
                    rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_AUDIT_PRECOMMIT"
     /\ auditReady
     /\ state' = "MFOS_AUTH_STATE_COMMIT_POLICY_VERSION"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_COMMIT_POLICY_VERSION"
     /\ policyVersion' = policyVersion + 1
     /\ policyEpoch' = policyEpoch + 1
     /\ state' = "MFOS_AUTH_STATE_INVALIDATE_DECISION_CACHE"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, securityEpoch, cacheValid, delegationValid,
                    emergencyActive, emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_INVALIDATE_DECISION_CACHE"
     /\ cacheValid' = FALSE
     /\ state' = "MFOS_AUTH_STATE_AUDIT_COMMIT"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    delegationValid, emergencyActive, emergencyExpired,
                    dualControlSatisfied, guardApprovalSatisfied, lintPassed,
                    rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_AUDIT_COMMIT"
     /\ auditReady
     /\ state' = "MFOS_AUTH_STATE_POLICY_ACTIVE"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>

EmergencyLifecycle ==
  \/ /\ state = "MFOS_AUTH_STATE_REQUEST_EMERGENCY_ACCESS"
     /\ state' = "MFOS_AUTH_STATE_AUTHENTICATE_OPERATOR"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_AUTHENTICATE_OPERATOR"
     /\ result' \in AllowResults
     /\ auditReady' = TRUE
     /\ state' = "MFOS_AUTH_STATE_AUTHORIZE_EMERGENCY_ACCESS"
     /\ UNCHANGED << obligationsSatisfied, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_AUTHORIZE_EMERGENCY_ACCESS"
     /\ result \in AllowResults
     /\ state' = "MFOS_AUTH_STATE_REQUIRE_REASON"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_REQUIRE_REASON"
     /\ state' = "MFOS_AUTH_STATE_SET_EXPIRY"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_SET_EXPIRY"
     /\ emergencyExpired = FALSE
     /\ state' = "MFOS_AUTH_STATE_AUDIT_BEFORE_ENABLE"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_AUDIT_BEFORE_ENABLE"
     /\ auditReady
     /\ emergencyActive' = TRUE
     /\ state' = "MFOS_AUTH_STATE_ENABLE_EMERGENCY_CONTEXT"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyExpired,
                    dualControlSatisfied, guardApprovalSatisfied, lintPassed,
                    rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_ENABLE_EMERGENCY_CONTEXT"
     /\ state' = "MFOS_AUTH_STATE_MONITOR_EMERGENCY_USE"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_MONITOR_EMERGENCY_USE"
     /\ emergencyExpired' = TRUE
     /\ emergencyActive' = FALSE
     /\ cacheValid' = FALSE
     /\ state' = "MFOS_AUTH_STATE_EXPIRE_OR_REVOKE"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    delegationValid, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_EXPIRE_OR_REVOKE"
     /\ auditReady
     /\ state' = "MFOS_AUTH_STATE_AUDIT_CLOSE"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>
  \/ /\ state = "MFOS_AUTH_STATE_AUDIT_CLOSE"
     /\ state' = "MFOS_AUTH_STATE_INCIDENT_REVIEW_REQUIRED"
     /\ UNCHANGED << result, obligationsSatisfied, auditReady, effectApplied,
                    handleBound, policyVersion, policyEpoch, securityEpoch,
                    cacheValid, delegationValid, emergencyActive,
                    emergencyExpired, dualControlSatisfied,
                    guardApprovalSatisfied, lintPassed, rollbackRequested >>

Next ==
  DecisionPath \/ EffectPath \/ DenyPath \/ PolicyTransaction \/ EmergencyLifecycle

Spec == Init /\ [][Next]_vars

MFOS_REACH_AUTH_DECISION_START ==
  state = "MFOS_AUTH_STATE_REQUEST_RECEIVED"

MFOS_REACH_POLICY_TX_START ==
  state = "MFOS_AUTH_STATE_BEGIN_POLICY_TX"

MFOS_REACH_EMERGENCY_START ==
  state = "MFOS_AUTH_STATE_REQUEST_EMERGENCY_ACCESS"

MFOS_INV_AUTH_0001_NoEffectWithoutAllow ==
  effectApplied => result \in AllowResults

MFOS_INV_AUTH_0002_HandleRequiresAllowAndObligations ==
  handleBound => /\ result \in AllowResults
                 /\ obligationsSatisfied

MFOS_INV_AUTH_0003_DenyRequireUnsupportedGapNoEffect ==
  result \in (TerminalDenyResults \cup RequireResults) => ~effectApplied

MFOS_INV_AUTH_0004_AuditBeforeEffectForObligatedAllow ==
  effectApplied => auditReady

MFOS_INV_AUTH_0005_EmergencyExpiryClearsEmergencyAndCache ==
  emergencyExpired => /\ ~emergencyActive
                      /\ ~cacheValid

MFOS_INV_AUTH_0006_DualControlBeforePolicyCommit ==
  state \in { "MFOS_AUTH_STATE_AUDIT_PRECOMMIT",
              "MFOS_AUTH_STATE_COMMIT_POLICY_VERSION",
              "MFOS_AUTH_STATE_POLICY_ACTIVE" } => dualControlSatisfied

MFOS_INV_AUTH_0007_LintBeforePolicyCommit ==
  state \in { "MFOS_AUTH_STATE_AUDIT_PRECOMMIT",
              "MFOS_AUTH_STATE_COMMIT_POLICY_VERSION",
              "MFOS_AUTH_STATE_POLICY_ACTIVE" } => lintPassed

MFOS_INV_AUTH_0008_RollbackStillIncrementsPolicyVersion ==
  rollbackRequested => policyVersion >= 1

=============================================================================
