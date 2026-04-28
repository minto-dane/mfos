---- MODULE JobLifecycle ----
EXTENDS Naturals

\* Phase 0.8 abstract job lifecycle model.
\* This is a design artifact, not production implementation.

VARIABLES
  jobState,
  stepState,
  submitAuthorized,
  auditSatisfied,
  hasEffectivePrincipal,
  ddResolved,
  programAuthorized,
  resourceOpen,
  spoolOpen,
  result

vars ==
  << jobState, stepState, submitAuthorized, auditSatisfied,
     hasEffectivePrincipal, ddResolved, programAuthorized,
     resourceOpen, spoolOpen, result >>

JobStates ==
  { "RECEIVED", "INPUT", "CONVERTING", "JOB_CONTROL_STREAM_ERROR", "VALIDATED",
    "SECURITY_DENIED", "QUEUED", "SELECTED", "EXECUTING", "OUTPUT",
    "COMPLETE", "FAILED", "ABENDED", "CANCELING", "CANCELED", "HELD",
    "PURGE_PENDING", "PURGED", "SPEC_GAP", "UNSUPPORTED",
    "AUDIT_REQUIRED_BUT_UNAVAILABLE" }

StepStates ==
  { "PENDING", "RESOLVING_DD", "AUTHORIZING_PROGRAM", "OPENING_RESOURCES",
    "READY", "EXECUTING", "CAPTURING_OUTPUT_STREAM", "CLOSING_RESOURCES",
    "COMPLETE", "FAILED", "ABENDED", "CANCELING", "CANCELED",
    "SPEC_GAP", "UNSUPPORTED", "AUDIT_REQUIRED_BUT_UNAVAILABLE" }

Results ==
  { "NONE", "OK", "DENY", "FAILED", "ABENDED", "CANCELED",
    "UNSUPPORTED", "SPEC_GAP", "AUDIT_UNAVAILABLE",
    "INVALID_TRANSITION" }

TerminalJobStates ==
  { "JOB_CONTROL_STREAM_ERROR", "SECURITY_DENIED", "COMPLETE", "FAILED", "ABENDED",
    "CANCELED", "PURGED", "SPEC_GAP", "UNSUPPORTED",
    "AUDIT_REQUIRED_BUT_UNAVAILABLE" }

TerminalStepStates ==
  { "COMPLETE", "FAILED", "ABENDED", "CANCELED", "SPEC_GAP",
    "UNSUPPORTED", "AUDIT_REQUIRED_BUT_UNAVAILABLE" }

Init ==
  /\ jobState = "RECEIVED"
  /\ stepState = "PENDING"
  /\ submitAuthorized = FALSE
  /\ auditSatisfied = FALSE
  /\ hasEffectivePrincipal = FALSE
  /\ ddResolved = FALSE
  /\ programAuthorized = FALSE
  /\ resourceOpen = FALSE
  /\ spoolOpen = FALSE
  /\ result = "NONE"

ReceiveInput ==
  /\ jobState = "RECEIVED"
  /\ jobState' = "INPUT"
  /\ UNCHANGED << stepState, submitAuthorized, auditSatisfied,
                  hasEffectivePrincipal, ddResolved, programAuthorized,
                  resourceOpen, spoolOpen, result >>

StartConversion ==
  /\ jobState = "INPUT"
  /\ jobState' = "CONVERTING"
  /\ UNCHANGED << stepState, submitAuthorized, auditSatisfied,
                  hasEffectivePrincipal, ddResolved, programAuthorized,
                  resourceOpen, spoolOpen, result >>

JclReject ==
  /\ jobState \in { "INPUT", "CONVERTING" }
  /\ jobState' = "JOB_CONTROL_STREAM_ERROR"
  /\ result' = "FAILED"
  /\ UNCHANGED << stepState, submitAuthorized, auditSatisfied,
                  hasEffectivePrincipal, ddResolved, programAuthorized,
                  resourceOpen, spoolOpen >>

SubmitAllow ==
  /\ jobState = "CONVERTING"
  /\ submitAuthorized' = TRUE
  /\ auditSatisfied' = TRUE
  /\ hasEffectivePrincipal' = TRUE
  /\ jobState' = "VALIDATED"
  /\ result' = "OK"
  /\ UNCHANGED << stepState, ddResolved, programAuthorized,
                  resourceOpen, spoolOpen >>

SubmitDeny ==
  /\ jobState = "CONVERTING"
  /\ submitAuthorized' = FALSE
  /\ auditSatisfied' = TRUE
  /\ hasEffectivePrincipal' = FALSE
  /\ jobState' = "SECURITY_DENIED"
  /\ result' = "DENY"
  /\ UNCHANGED << stepState, ddResolved, programAuthorized,
                  resourceOpen, spoolOpen >>

AuditUnavailable ==
  /\ jobState \notin TerminalJobStates
  /\ auditSatisfied' = FALSE
  /\ jobState' = "AUDIT_REQUIRED_BUT_UNAVAILABLE"
  /\ stepState' =
       IF stepState \in TerminalStepStates
       THEN stepState
       ELSE "AUDIT_REQUIRED_BUT_UNAVAILABLE"
  /\ result' = "AUDIT_UNAVAILABLE"
  /\ resourceOpen' = FALSE
  /\ spoolOpen' = FALSE
  /\ UNCHANGED << submitAuthorized, hasEffectivePrincipal, ddResolved,
                  programAuthorized >>

Enqueue ==
  /\ jobState = "VALIDATED"
  /\ submitAuthorized
  /\ auditSatisfied
  /\ hasEffectivePrincipal
  /\ jobState' = "QUEUED"
  /\ UNCHANGED << stepState, submitAuthorized, auditSatisfied,
                  hasEffectivePrincipal, ddResolved, programAuthorized,
                  resourceOpen, spoolOpen, result >>

SelectJob ==
  /\ jobState = "QUEUED"
  /\ jobState' = "SELECTED"
  /\ UNCHANGED << stepState, submitAuthorized, auditSatisfied,
                  hasEffectivePrincipal, ddResolved, programAuthorized,
                  resourceOpen, spoolOpen, result >>

StartJobExecution ==
  /\ jobState = "SELECTED"
  /\ jobState' = "EXECUTING"
  /\ stepState' = "RESOLVING_DD"
  /\ UNCHANGED << submitAuthorized, auditSatisfied, hasEffectivePrincipal,
                  ddResolved, programAuthorized, resourceOpen, spoolOpen,
                  result >>

ResolveDd ==
  /\ jobState = "EXECUTING"
  /\ stepState = "RESOLVING_DD"
  /\ hasEffectivePrincipal
  /\ ddResolved' = TRUE
  /\ stepState' = "AUTHORIZING_PROGRAM"
  /\ UNCHANGED << jobState, submitAuthorized, auditSatisfied,
                  hasEffectivePrincipal, programAuthorized, resourceOpen,
                  spoolOpen, result >>

DdDeny ==
  /\ jobState = "EXECUTING"
  /\ stepState = "RESOLVING_DD"
  /\ auditSatisfied
  /\ ddResolved' = FALSE
  /\ stepState' = "FAILED"
  /\ jobState' = "FAILED"
  /\ result' = "DENY"
  /\ UNCHANGED << submitAuthorized, auditSatisfied, hasEffectivePrincipal,
                  programAuthorized, resourceOpen, spoolOpen >>

AuthorizeProgram ==
  /\ jobState = "EXECUTING"
  /\ stepState = "AUTHORIZING_PROGRAM"
  /\ ddResolved
  /\ hasEffectivePrincipal
  /\ auditSatisfied
  /\ programAuthorized' = TRUE
  /\ stepState' = "OPENING_RESOURCES"
  /\ UNCHANGED << jobState, submitAuthorized, auditSatisfied,
                  hasEffectivePrincipal, ddResolved, resourceOpen,
                  spoolOpen, result >>

ProgramDeny ==
  /\ jobState = "EXECUTING"
  /\ stepState = "AUTHORIZING_PROGRAM"
  /\ auditSatisfied
  /\ programAuthorized' = FALSE
  /\ stepState' = "FAILED"
  /\ jobState' = "FAILED"
  /\ result' = "DENY"
  /\ UNCHANGED << submitAuthorized, auditSatisfied, hasEffectivePrincipal,
                  ddResolved, resourceOpen, spoolOpen >>

OpenResources ==
  /\ jobState = "EXECUTING"
  /\ stepState = "OPENING_RESOURCES"
  /\ hasEffectivePrincipal
  /\ ddResolved
  /\ programAuthorized
  /\ resourceOpen' = TRUE
  /\ spoolOpen' = TRUE
  /\ stepState' = "READY"
  /\ UNCHANGED << jobState, submitAuthorized, auditSatisfied,
                  hasEffectivePrincipal, ddResolved, programAuthorized,
                  result >>

ExecuteStep ==
  /\ jobState = "EXECUTING"
  /\ stepState = "READY"
  /\ resourceOpen
  /\ spoolOpen
  /\ stepState' = "EXECUTING"
  /\ UNCHANGED << jobState, submitAuthorized, auditSatisfied,
                  hasEffectivePrincipal, ddResolved, programAuthorized,
                  resourceOpen, spoolOpen, result >>

StepNormalExit ==
  /\ jobState = "EXECUTING"
  /\ stepState = "EXECUTING"
  /\ stepState' = "CAPTURING_OUTPUT_STREAM"
  /\ UNCHANGED << jobState, submitAuthorized, auditSatisfied,
                  hasEffectivePrincipal, ddResolved, programAuthorized,
                  resourceOpen, spoolOpen, result >>

StepAbend ==
  /\ jobState = "EXECUTING"
  /\ stepState = "EXECUTING"
  /\ stepState' = "ABENDED"
  /\ jobState' = "ABENDED"
  /\ resourceOpen' = FALSE
  /\ spoolOpen' = FALSE
  /\ result' = "ABENDED"
  /\ UNCHANGED << submitAuthorized, auditSatisfied, hasEffectivePrincipal,
                  ddResolved, programAuthorized >>

CloseResources ==
  /\ jobState = "EXECUTING"
  /\ stepState = "CAPTURING_OUTPUT_STREAM"
  /\ stepState' = "CLOSING_RESOURCES"
  /\ resourceOpen' = FALSE
  /\ spoolOpen' = FALSE
  /\ UNCHANGED << jobState, submitAuthorized, auditSatisfied,
                  hasEffectivePrincipal, ddResolved, programAuthorized,
                  result >>

StepComplete ==
  /\ jobState = "EXECUTING"
  /\ stepState = "CLOSING_RESOURCES"
  /\ ~resourceOpen
  /\ ~spoolOpen
  /\ stepState' = "COMPLETE"
  /\ jobState' = "OUTPUT"
  /\ result' = "OK"
  /\ UNCHANGED << submitAuthorized, auditSatisfied, hasEffectivePrincipal,
                  ddResolved, programAuthorized, resourceOpen, spoolOpen >>

JobComplete ==
  /\ jobState = "OUTPUT"
  /\ auditSatisfied
  /\ jobState' = "COMPLETE"
  /\ result' = "OK"
  /\ UNCHANGED << stepState, submitAuthorized, auditSatisfied,
                  hasEffectivePrincipal, ddResolved, programAuthorized,
                  resourceOpen, spoolOpen >>

CancelJob ==
  /\ jobState \in { "QUEUED", "SELECTED", "EXECUTING", "HELD" }
  /\ jobState' = "CANCELING"
  /\ stepState' =
       IF stepState \in TerminalStepStates
       THEN stepState
       ELSE "CANCELING"
  /\ resourceOpen' = FALSE
  /\ spoolOpen' = FALSE
  /\ result' = "CANCELED"
  /\ UNCHANGED << submitAuthorized, auditSatisfied, hasEffectivePrincipal,
                  ddResolved, programAuthorized >>

CancelComplete ==
  /\ jobState = "CANCELING"
  /\ ~resourceOpen
  /\ ~spoolOpen
  /\ jobState' = "CANCELED"
  /\ stepState' =
       IF stepState = "CANCELING"
       THEN "CANCELED"
       ELSE stepState
  /\ UNCHANGED << submitAuthorized, auditSatisfied, hasEffectivePrincipal,
                  ddResolved, programAuthorized, resourceOpen, spoolOpen,
                  result >>

RequestPurge ==
  /\ jobState \in { "COMPLETE", "FAILED", "ABENDED", "CANCELED", "HELD" }
  /\ auditSatisfied
  /\ jobState' = "PURGE_PENDING"
  /\ UNCHANGED << stepState, submitAuthorized, auditSatisfied,
                  hasEffectivePrincipal, ddResolved, programAuthorized,
                  resourceOpen, spoolOpen, result >>

PurgeComplete ==
  /\ jobState = "PURGE_PENDING"
  /\ jobState' = "PURGED"
  /\ UNCHANGED << stepState, submitAuthorized, auditSatisfied,
                  hasEffectivePrincipal, ddResolved, programAuthorized,
                  resourceOpen, spoolOpen, result >>

UnsupportedReject ==
  /\ jobState \notin TerminalJobStates
  /\ jobState' = "UNSUPPORTED"
  /\ stepState' =
       IF stepState \in TerminalStepStates
       THEN stepState
       ELSE "UNSUPPORTED"
  /\ resourceOpen' = FALSE
  /\ spoolOpen' = FALSE
  /\ result' = "UNSUPPORTED"
  /\ UNCHANGED << submitAuthorized, auditSatisfied, hasEffectivePrincipal,
                  ddResolved, programAuthorized >>

SpecGapReject ==
  /\ jobState \notin TerminalJobStates
  /\ jobState' = "SPEC_GAP"
  /\ stepState' =
       IF stepState \in TerminalStepStates
       THEN stepState
       ELSE "SPEC_GAP"
  /\ resourceOpen' = FALSE
  /\ spoolOpen' = FALSE
  /\ result' = "SPEC_GAP"
  /\ UNCHANGED << submitAuthorized, auditSatisfied, hasEffectivePrincipal,
                  ddResolved, programAuthorized >>

InvalidTransitionRejected ==
  /\ result' = "INVALID_TRANSITION"
  /\ UNCHANGED << jobState, stepState, submitAuthorized, auditSatisfied,
                  hasEffectivePrincipal, ddResolved, programAuthorized,
                  resourceOpen, spoolOpen >>

Next ==
  \/ ReceiveInput
  \/ StartConversion
  \/ JclReject
  \/ SubmitAllow
  \/ SubmitDeny
  \/ AuditUnavailable
  \/ Enqueue
  \/ SelectJob
  \/ StartJobExecution
  \/ ResolveDd
  \/ DdDeny
  \/ AuthorizeProgram
  \/ ProgramDeny
  \/ OpenResources
  \/ ExecuteStep
  \/ StepNormalExit
  \/ StepAbend
  \/ CloseResources
  \/ StepComplete
  \/ JobComplete
  \/ CancelJob
  \/ CancelComplete
  \/ RequestPurge
  \/ PurgeComplete
  \/ UnsupportedReject
  \/ SpecGapReject
  \/ InvalidTransitionRejected

Spec == Init /\ [][Next]_vars

TypeOK ==
  /\ jobState \in JobStates
  /\ stepState \in StepStates
  /\ submitAuthorized \in BOOLEAN
  /\ auditSatisfied \in BOOLEAN
  /\ hasEffectivePrincipal \in BOOLEAN
  /\ ddResolved \in BOOLEAN
  /\ programAuthorized \in BOOLEAN
  /\ resourceOpen \in BOOLEAN
  /\ spoolOpen \in BOOLEAN
  /\ result \in Results

NoQueuedWithoutAuthorization ==
  jobState \in { "QUEUED", "SELECTED", "EXECUTING", "OUTPUT", "COMPLETE" }
    => submitAuthorized /\ auditSatisfied /\ hasEffectivePrincipal

NoOpenBeforeEffectivePrincipal ==
  (resourceOpen \/ spoolOpen) => hasEffectivePrincipal

TerminalJobDoesNotExecute ==
  jobState \in TerminalJobStates => stepState # "EXECUTING"

FailureResultNotComplete ==
  result \in { "DENY", "FAILED", "ABENDED", "CANCELED", "UNSUPPORTED",
               "SPEC_GAP", "AUDIT_UNAVAILABLE" }
    => jobState # "COMPLETE"

====
