---- MODULE CatalogTransaction ----
EXTENDS Naturals, TLC

\* Phase 0.8 design model for docs/design/specs/08-dataset-catalog.md.
\* This is not production code.

VARIABLES phase, entryState, journalState, audit, integrityOk, recovery, resolveResult

Vars == <<phase, entryState, journalState, audit, integrityOk, recovery, resolveResult>>

EntryStates == {"ABSENT", "PREPARED", "COMMITTED", "DELETING", "DELETED", "CORRUPT"}
JournalStates == {"NONE", "PREPARED_RECORD", "COMMIT_RECORD", "TORN_RECORD", "ROLLED_BACK"}

Init ==
  /\ phase = "BEGIN_TX"
  /\ entryState = "ABSENT"
  /\ journalState = "NONE"
  /\ audit = "PENDING"
  /\ integrityOk \in BOOLEAN
  /\ recovery = "NORMAL"
  /\ resolveResult = "NONE"

ValidateDsn ==
  /\ phase = "BEGIN_TX"
  /\ phase' = "VALIDATE_DSN"
  /\ UNCHANGED <<entryState, journalState, audit, integrityOk, recovery, resolveResult>>

AuthorizeUpdate ==
  /\ phase = "VALIDATE_DSN"
  /\ phase' = "AUTHORIZE_CATALOG_UPDATE"
  /\ UNCHANGED <<entryState, journalState, audit, integrityOk, recovery, resolveResult>>

PrepareEntry ==
  /\ phase = "AUTHORIZE_CATALOG_UPDATE"
  /\ entryState' = "PREPARED"
  /\ phase' = "PREPARE_ENTRY"
  /\ UNCHANGED <<journalState, audit, integrityOk, recovery, resolveResult>>

WriteJournal ==
  /\ phase = "PREPARE_ENTRY"
  /\ journalState' = "PREPARED_RECORD"
  /\ phase' = "WRITE_JOURNAL"
  /\ UNCHANGED <<entryState, audit, integrityOk, recovery, resolveResult>>

CommitEntry ==
  /\ phase = "WRITE_JOURNAL"
  /\ journalState = "PREPARED_RECORD"
  /\ journalState' = "COMMIT_RECORD"
  /\ entryState' = "COMMITTED"
  /\ phase' = "COMMIT_ENTRY"
  /\ UNCHANGED <<audit, integrityOk, recovery, resolveResult>>

WriteAudit ==
  /\ phase = "COMMIT_ENTRY"
  /\ audit' = "APPENDED"
  /\ phase' = "WRITE_AUDIT"
  /\ UNCHANGED <<entryState, journalState, integrityOk, recovery, resolveResult>>

Complete ==
  /\ phase = "WRITE_AUDIT"
  /\ audit = "APPENDED"
  /\ phase' = "COMPLETE"
  /\ recovery' = "COMPLETE"
  /\ UNCHANGED <<entryState, journalState, audit, integrityOk, resolveResult>>

TornJournalCrash ==
  /\ phase \in {"PREPARE_ENTRY", "WRITE_JOURNAL", "COMMIT_ENTRY"}
  /\ journalState' = "TORN_RECORD"
  /\ recovery' = "RECOVERING"
  /\ phase' = "RECOVER_SCAN_JOURNAL"
  /\ UNCHANGED <<entryState, audit, integrityOk, resolveResult>>

RollbackIncomplete ==
  /\ phase = "RECOVER_SCAN_JOURNAL"
  /\ journalState \in {"PREPARED_RECORD", "TORN_RECORD", "NONE"}
  /\ journalState' = "ROLLED_BACK"
  /\ entryState' = "ABSENT"
  /\ recovery' = "ROLLED_BACK"
  /\ phase' = "ROLLBACK_INCOMPLETE"
  /\ resolveResult' = "FAILED_CLOSED"
  /\ UNCHANGED <<audit, integrityOk>>

VerifyCommittedRecoveryOk ==
  /\ phase = "RECOVER_SCAN_JOURNAL"
  /\ journalState = "COMMIT_RECORD"
  /\ entryState = "COMMITTED"
  /\ integrityOk = TRUE
  /\ audit = "APPENDED"
  /\ recovery' = "COMPLETE"
  /\ phase' = "RECOVERY_COMPLETE"
  /\ UNCHANGED <<entryState, journalState, audit, integrityOk, resolveResult>>

VerifyCommittedRecoveryFail ==
  /\ phase = "RECOVER_SCAN_JOURNAL"
  /\ ~(journalState = "COMMIT_RECORD" /\ entryState = "COMMITTED" /\ integrityOk = TRUE /\ audit = "APPENDED")
  /\ recovery' = "ROLLED_BACK"
  /\ phase' = "ROLLBACK_INCOMPLETE"
  /\ entryState' \in {"ABSENT", "CORRUPT"}
  /\ journalState' \in {"ROLLED_BACK", "TORN_RECORD"}
  /\ resolveResult' = "FAILED_CLOSED"
  /\ UNCHANGED <<audit, integrityOk>>

ResolveOk ==
  /\ phase \in {"COMPLETE", "RECOVERY_COMPLETE"}
  /\ entryState = "COMMITTED"
  /\ journalState = "COMMIT_RECORD"
  /\ audit = "APPENDED"
  /\ integrityOk = TRUE
  /\ recovery = "COMPLETE"
  /\ resolveResult' = "OK"
  /\ UNCHANGED <<phase, entryState, journalState, audit, integrityOk, recovery>>

ResolveFail ==
  /\ ~(entryState = "COMMITTED" /\ journalState = "COMMIT_RECORD" /\ audit = "APPENDED" /\ integrityOk = TRUE /\ recovery = "COMPLETE")
  /\ resolveResult' = "FAILED_CLOSED"
  /\ UNCHANGED <<phase, entryState, journalState, audit, integrityOk, recovery>>

Next ==
  \/ ValidateDsn
  \/ AuthorizeUpdate
  \/ PrepareEntry
  \/ WriteJournal
  \/ CommitEntry
  \/ WriteAudit
  \/ Complete
  \/ TornJournalCrash
  \/ RollbackIncomplete
  \/ VerifyCommittedRecoveryOk
  \/ VerifyCommittedRecoveryFail
  \/ ResolveOk
  \/ ResolveFail

Spec == Init /\ [][Next]_Vars

CommittedEntryOnly ==
  resolveResult = "OK" =>
    /\ entryState = "COMMITTED"
    /\ journalState = "COMMIT_RECORD"
    /\ audit = "APPENDED"
    /\ integrityOk = TRUE
    /\ recovery = "COMPLETE"

PartialJournalNeverResolves ==
  journalState \in {"PREPARED_RECORD", "TORN_RECORD", "ROLLED_BACK", "NONE"} => resolveResult # "OK"

IntegrityFailureNeverResolves ==
  integrityOk = FALSE => resolveResult # "OK"

CompleteRequiresAudit ==
  phase = "COMPLETE" => audit = "APPENDED"

RollbackDoesNotResolve ==
  recovery = "ROLLED_BACK" => resolveResult # "OK"

====
