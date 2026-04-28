---- MODULE AuditAppend ----
EXTENDS Naturals, TLC

\* Phase 0.8 design model for MFOS audit append semantics.
\* Source refs:
\* - EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001
\* - EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001
\* - EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
\* - EXTREF-IBM-ZOS-SECURITY-SERVER-0001
\* - EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001

CONSTANTS
  Hashes,
  RequiredEvents,
  HighAssurance,
  MaxSeq

VARIABLES
  phase,
  seq,
  headHash,
  requiredAudit,
  durable,
  resultVisible,
  failedClosed,
  exported,
  exportRequired,
  guardRequired,
  guardSealed,
  queryRequested,
  queryAuthorized,
  queryResultVisible,
  committedRecordMutated,
  streamStatus

Phases ==
  {"Idle", "Received", "Validated", "Sequenced", "Hashed", "Durable",
   "ExportPending", "Exported", "GuardPending", "Guarded", "Returned",
   "Rejected", "FailedClosed", "Degraded", "Recovering", "Sealed"}

StreamStatuses == {"Active", "Degraded", "Recovering", "Sealed"}

TypeOK ==
  /\ phase \in Phases
  /\ seq \in 0..MaxSeq
  /\ headHash \in Hashes
  /\ requiredAudit \in BOOLEAN
  /\ durable \in BOOLEAN
  /\ resultVisible \in BOOLEAN
  /\ failedClosed \in BOOLEAN
  /\ exported \in BOOLEAN
  /\ exportRequired \in BOOLEAN
  /\ guardRequired \in BOOLEAN
  /\ guardSealed \in BOOLEAN
  /\ queryRequested \in BOOLEAN
  /\ queryAuthorized \in BOOLEAN
  /\ queryResultVisible \in BOOLEAN
  /\ committedRecordMutated \in BOOLEAN
  /\ streamStatus \in StreamStatuses

Init ==
  /\ phase = "Idle"
  /\ seq = 0
  /\ headHash \in Hashes
  /\ requiredAudit = FALSE
  /\ durable = FALSE
  /\ resultVisible = FALSE
  /\ failedClosed = FALSE
  /\ exported = FALSE
  /\ exportRequired = FALSE
  /\ guardRequired = FALSE
  /\ guardSealed = FALSE
  /\ queryRequested = FALSE
  /\ queryAuthorized = FALSE
  /\ queryResultVisible = FALSE
  /\ committedRecordMutated = FALSE
  /\ streamStatus = "Active"

Receive(req, exp, guard) ==
  /\ phase = "Idle"
  /\ streamStatus = "Active"
  /\ req \in BOOLEAN
  /\ exp \in BOOLEAN
  /\ guard \in BOOLEAN
  /\ phase' = "Received"
  /\ requiredAudit' = req
  /\ exportRequired' = exp
  /\ guardRequired' = guard
  /\ UNCHANGED <<seq, headHash, durable, resultVisible, failedClosed, exported,
      guardSealed, queryRequested, queryAuthorized, queryResultVisible,
      committedRecordMutated, streamStatus>>

Validate ==
  /\ phase = "Received"
  /\ phase' = "Validated"
  /\ UNCHANGED <<seq, headHash, requiredAudit, durable, resultVisible,
      failedClosed, exported, exportRequired, guardRequired, guardSealed,
      queryRequested, queryAuthorized, queryResultVisible,
      committedRecordMutated, streamStatus>>

Reject ==
  /\ phase \in {"Received", "Validated"}
  /\ phase' = "Rejected"
  /\ failedClosed' = requiredAudit
  /\ resultVisible' = FALSE
  /\ UNCHANGED <<seq, headHash, requiredAudit, durable, exported,
      exportRequired, guardRequired, guardSealed, queryRequested,
      queryAuthorized, queryResultVisible, committedRecordMutated,
      streamStatus>>

AssignSequence ==
  /\ phase = "Validated"
  /\ seq < MaxSeq
  /\ seq' = seq + 1
  /\ phase' = "Sequenced"
  /\ UNCHANGED <<headHash, requiredAudit, durable, resultVisible, failedClosed,
      exported, exportRequired, guardRequired, guardSealed, queryRequested,
      queryAuthorized, queryResultVisible, committedRecordMutated,
      streamStatus>>

HashRecord ==
  /\ phase = "Sequenced"
  /\ \E h \in Hashes : h # headHash /\ headHash' = h
  /\ phase' = "Hashed"
  /\ UNCHANGED <<seq, requiredAudit, durable, resultVisible, failedClosed,
      exported, exportRequired, guardRequired, guardSealed, queryRequested,
      queryAuthorized, queryResultVisible, committedRecordMutated,
      streamStatus>>

DurableAppend ==
  /\ phase = "Hashed"
  /\ durable' = TRUE
  /\ phase' = "Durable"
  /\ UNCHANGED <<seq, headHash, requiredAudit, resultVisible, failedClosed,
      exported, exportRequired, guardRequired, guardSealed, queryRequested,
      queryAuthorized, queryResultVisible, committedRecordMutated,
      streamStatus>>

ExportStart ==
  /\ phase = "Durable"
  /\ exportRequired
  /\ phase' = "ExportPending"
  /\ UNCHANGED <<seq, headHash, requiredAudit, durable, resultVisible,
      failedClosed, exported, exportRequired, guardRequired, guardSealed,
      queryRequested, queryAuthorized, queryResultVisible,
      committedRecordMutated, streamStatus>>

ExportOk ==
  /\ phase = "ExportPending"
  /\ exported' = TRUE
  /\ phase' = "Exported"
  /\ UNCHANGED <<seq, headHash, requiredAudit, durable, resultVisible,
      failedClosed, exportRequired, guardRequired, guardSealed,
      queryRequested, queryAuthorized, queryResultVisible,
      committedRecordMutated, streamStatus>>

ExportFailAllowed ==
  /\ phase = "ExportPending"
  /\ exported' = FALSE
  /\ phase' = "Durable"
  /\ UNCHANGED <<seq, headHash, requiredAudit, durable, resultVisible,
      failedClosed, exportRequired, guardRequired, guardSealed,
      queryRequested, queryAuthorized, queryResultVisible,
      committedRecordMutated, streamStatus>>

GuardStart ==
  /\ phase \in {"Durable", "Exported"}
  /\ guardRequired
  /\ phase' = "GuardPending"
  /\ UNCHANGED <<seq, headHash, requiredAudit, durable, resultVisible,
      failedClosed, exported, exportRequired, guardRequired, guardSealed,
      queryRequested, queryAuthorized, queryResultVisible,
      committedRecordMutated, streamStatus>>

GuardOk ==
  /\ phase = "GuardPending"
  /\ guardSealed' = TRUE
  /\ phase' = "Guarded"
  /\ UNCHANGED <<seq, headHash, requiredAudit, durable, resultVisible,
      failedClosed, exported, exportRequired, guardRequired, queryRequested,
      queryAuthorized, queryResultVisible, committedRecordMutated,
      streamStatus>>

GuardFailClosed ==
  /\ phase = "GuardPending"
  /\ failedClosed' = TRUE
  /\ resultVisible' = FALSE
  /\ phase' = "FailedClosed"
  /\ UNCHANGED <<seq, headHash, requiredAudit, durable, exported,
      exportRequired, guardRequired, guardSealed, queryRequested,
      queryAuthorized, queryResultVisible, committedRecordMutated,
      streamStatus>>

ReturnResult ==
  /\ phase \in {"Durable", "Exported", "Guarded"}
  /\ requiredAudit => durable
  /\ guardRequired => guardSealed
  /\ resultVisible' = TRUE
  /\ phase' = "Returned"
  /\ UNCHANGED <<seq, headHash, requiredAudit, durable, failedClosed, exported,
      exportRequired, guardRequired, guardSealed, queryRequested,
      queryAuthorized, queryResultVisible, committedRecordMutated,
      streamStatus>>

AppendFailClosed ==
  /\ phase \in {"Received", "Validated", "Sequenced", "Hashed"}
  /\ requiredAudit
  /\ failedClosed' = TRUE
  /\ resultVisible' = FALSE
  /\ phase' = "FailedClosed"
  /\ UNCHANGED <<seq, headHash, requiredAudit, durable, exported,
      exportRequired, guardRequired, guardSealed, queryRequested,
      queryAuthorized, queryResultVisible, committedRecordMutated,
      streamStatus>>

TamperDetected ==
  /\ phase \in {"Durable", "Returned"}
  /\ streamStatus' = "Degraded"
  /\ phase' = "Degraded"
  /\ UNCHANGED <<seq, headHash, requiredAudit, durable, resultVisible,
      failedClosed, exported, exportRequired, guardRequired, guardSealed,
      queryRequested, queryAuthorized, queryResultVisible,
      committedRecordMutated>>

StartRecovery ==
  /\ streamStatus = "Degraded"
  /\ streamStatus' = "Recovering"
  /\ phase' = "Recovering"
  /\ UNCHANGED <<seq, headHash, requiredAudit, durable, resultVisible,
      failedClosed, exported, exportRequired, guardRequired, guardSealed,
      queryRequested, queryAuthorized, queryResultVisible,
      committedRecordMutated>>

SealStream ==
  /\ phase \in {"Durable", "Returned", "Recovering"}
  /\ streamStatus' = "Sealed"
  /\ phase' = "Sealed"
  /\ UNCHANGED <<seq, headHash, requiredAudit, durable, resultVisible,
      failedClosed, exported, exportRequired, guardRequired, guardSealed,
      queryRequested, queryAuthorized, queryResultVisible,
      committedRecordMutated>>

RequestQuery ==
  /\ ~queryRequested
  /\ queryRequested' = TRUE
  /\ UNCHANGED <<phase, seq, headHash, requiredAudit, durable, resultVisible,
      failedClosed, exported, exportRequired, guardRequired, guardSealed,
      queryAuthorized, queryResultVisible, committedRecordMutated,
      streamStatus>>

AuthorizeQuery ==
  /\ queryRequested
  /\ queryAuthorized' = TRUE
  /\ UNCHANGED <<phase, seq, headHash, requiredAudit, durable, resultVisible,
      failedClosed, exported, exportRequired, guardRequired, guardSealed,
      queryRequested, queryResultVisible, committedRecordMutated,
      streamStatus>>

ReturnQueryResult ==
  /\ queryRequested
  /\ queryAuthorized
  /\ queryResultVisible' = TRUE
  /\ UNCHANGED <<phase, seq, headHash, requiredAudit, durable, resultVisible,
      failedClosed, exported, exportRequired, guardRequired, guardSealed,
      queryRequested, queryAuthorized, committedRecordMutated, streamStatus>>

Next ==
  \/ \E req \in BOOLEAN, exp \in BOOLEAN, guard \in BOOLEAN :
       Receive(req, exp, guard)
  \/ Validate
  \/ Reject
  \/ AssignSequence
  \/ HashRecord
  \/ DurableAppend
  \/ ExportStart
  \/ ExportOk
  \/ ExportFailAllowed
  \/ GuardStart
  \/ GuardOk
  \/ GuardFailClosed
  \/ ReturnResult
  \/ AppendFailClosed
  \/ TamperDetected
  \/ StartRecovery
  \/ SealStream
  \/ RequestQuery
  \/ AuthorizeQuery
  \/ ReturnQueryResult

DenyBeforeReturnInv ==
  requiredAudit /\ resultVisible => durable

NoGuardClaimWithoutSealInv ==
  guardRequired /\ resultVisible => guardSealed

QueryAuthorizationInv ==
  queryResultVisible => queryAuthorized

CommittedRecordImmutableInv ==
  ~committedRecordMutated

NoRequiredAuditSuccessAfterRejectInv ==
  requiredAudit /\ phase = "Rejected" => ~resultVisible

SealedStreamNoOrdinaryAppendInv ==
  streamStatus = "Sealed" => phase = "Sealed"

Spec ==
  Init /\ [][Next]_<<phase, seq, headHash, requiredAudit, durable, resultVisible,
    failedClosed, exported, exportRequired, guardRequired, guardSealed,
    queryRequested, queryAuthorized, queryResultVisible, committedRecordMutated,
    streamStatus>>

====
