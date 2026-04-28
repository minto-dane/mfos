---- MODULE SpoolAccess ----

\* Phase 0.8 abstract spool access model.
\* This is a design artifact, not production implementation.

VARIABLES
  state,
  createAuthorized,
  accessAuthorized,
  auditSatisfied,
  retentionEligible,
  contentPresent,
  contentReturned,
  result

vars ==
  << state, createAuthorized, accessAuthorized, auditSatisfied,
     retentionEligible, contentPresent, contentReturned, result >>

SpoolStates ==
  { "CREATE_REQUESTED", "AUTHORIZING_CREATE", "OPEN", "WRITING", "CLOSED",
    "HELD", "BROWSE_ACTIVE", "EXPORTING", "PURGE_PENDING", "PURGED",
    "FAILED", "SPEC_GAP", "UNSUPPORTED",
    "AUDIT_REQUIRED_BUT_UNAVAILABLE" }

Results ==
  { "NONE", "OK", "DENY", "STALE_REF", "RETENTION_DENIED",
    "UNSUPPORTED", "SPEC_GAP", "AUDIT_UNAVAILABLE",
    "INVALID_TRANSITION" }

TerminalStates ==
  { "PURGED", "FAILED", "SPEC_GAP", "UNSUPPORTED",
    "AUDIT_REQUIRED_BUT_UNAVAILABLE" }

Init ==
  /\ state = "CREATE_REQUESTED"
  /\ createAuthorized = FALSE
  /\ accessAuthorized = FALSE
  /\ auditSatisfied = FALSE
  /\ retentionEligible = FALSE
  /\ contentPresent = FALSE
  /\ contentReturned = FALSE
  /\ result = "NONE"

BeginCreateAuth ==
  /\ state = "CREATE_REQUESTED"
  /\ state' = "AUTHORIZING_CREATE"
  /\ UNCHANGED << createAuthorized, accessAuthorized, auditSatisfied,
                  retentionEligible, contentPresent, contentReturned,
                  result >>

CreateAllow ==
  /\ state = "AUTHORIZING_CREATE"
  /\ createAuthorized' = TRUE
  /\ auditSatisfied' = TRUE
  /\ state' = "OPEN"
  /\ result' = "OK"
  /\ UNCHANGED << accessAuthorized, retentionEligible, contentPresent,
                  contentReturned >>

CreateDeny ==
  /\ state = "AUTHORIZING_CREATE"
  /\ createAuthorized' = FALSE
  /\ auditSatisfied' = TRUE
  /\ state' = "FAILED"
  /\ result' = "DENY"
  /\ UNCHANGED << accessAuthorized, retentionEligible, contentPresent,
                  contentReturned >>

WriteFirstRecord ==
  /\ state = "OPEN"
  /\ createAuthorized
  /\ state' = "WRITING"
  /\ contentPresent' = TRUE
  /\ UNCHANGED << createAuthorized, accessAuthorized, auditSatisfied,
                  retentionEligible, contentReturned, result >>

CloseOpenEntry ==
  /\ state = "OPEN"
  /\ createAuthorized
  /\ state' = "CLOSED"
  /\ UNCHANGED << createAuthorized, accessAuthorized, auditSatisfied,
                  retentionEligible, contentPresent, contentReturned,
                  result >>

WriteNextRecord ==
  /\ state = "WRITING"
  /\ contentPresent
  /\ state' = "WRITING"
  /\ UNCHANGED << createAuthorized, accessAuthorized, auditSatisfied,
                  retentionEligible, contentPresent, contentReturned,
                  result >>

CloseWrittenEntry ==
  /\ state = "WRITING"
  /\ state' = "CLOSED"
  /\ UNCHANGED << createAuthorized, accessAuthorized, auditSatisfied,
                  retentionEligible, contentPresent, contentReturned,
                  result >>

HoldClosed ==
  /\ state = "CLOSED"
  /\ state' = "HELD"
  /\ UNCHANGED << createAuthorized, accessAuthorized, auditSatisfied,
                  retentionEligible, contentPresent, contentReturned,
                  result >>

ReleaseHeld ==
  /\ state = "HELD"
  /\ state' = "CLOSED"
  /\ UNCHANGED << createAuthorized, accessAuthorized, auditSatisfied,
                  retentionEligible, contentPresent, contentReturned,
                  result >>

BrowseAllow ==
  /\ state \in { "CLOSED", "HELD" }
  /\ contentPresent
  /\ accessAuthorized' = TRUE
  /\ auditSatisfied' = TRUE
  /\ contentReturned' = TRUE
  /\ state' = "BROWSE_ACTIVE"
  /\ result' = "OK"
  /\ UNCHANGED << createAuthorized, retentionEligible, contentPresent >>

BrowseCloseToClosed ==
  /\ state = "BROWSE_ACTIVE"
  /\ state' = "CLOSED"
  /\ contentReturned' = FALSE
  /\ UNCHANGED << createAuthorized, accessAuthorized, auditSatisfied,
                  retentionEligible, contentPresent, result >>

BrowseDeny ==
  /\ state \in { "CLOSED", "HELD" }
  /\ accessAuthorized' = FALSE
  /\ auditSatisfied' = TRUE
  /\ contentReturned' = FALSE
  /\ result' = "DENY"
  /\ UNCHANGED << state, createAuthorized, retentionEligible, contentPresent >>

ExportAllow ==
  /\ state \in { "CLOSED", "HELD" }
  /\ contentPresent
  /\ accessAuthorized' = TRUE
  /\ auditSatisfied' = TRUE
  /\ state' = "EXPORTING"
  /\ result' = "OK"
  /\ UNCHANGED << createAuthorized, retentionEligible, contentPresent,
                  contentReturned >>

ExportComplete ==
  /\ state = "EXPORTING"
  /\ state' = "CLOSED"
  /\ UNCHANGED << createAuthorized, accessAuthorized, auditSatisfied,
                  retentionEligible, contentPresent, contentReturned,
                  result >>

ExportDeny ==
  /\ state \in { "CLOSED", "HELD" }
  /\ accessAuthorized' = FALSE
  /\ auditSatisfied' = TRUE
  /\ contentReturned' = FALSE
  /\ result' = "DENY"
  /\ UNCHANGED << state, createAuthorized, retentionEligible, contentPresent >>

RetentionBecomesEligible ==
  /\ state \in { "CLOSED", "HELD" }
  /\ retentionEligible' = TRUE
  /\ UNCHANGED << state, createAuthorized, accessAuthorized, auditSatisfied,
                  contentPresent, contentReturned, result >>

PurgeAllow ==
  /\ state \in { "CLOSED", "HELD" }
  /\ retentionEligible
  /\ accessAuthorized' = TRUE
  /\ auditSatisfied' = TRUE
  /\ state' = "PURGE_PENDING"
  /\ result' = "OK"
  /\ UNCHANGED << createAuthorized, retentionEligible, contentPresent,
                  contentReturned >>

PurgeComplete ==
  /\ state = "PURGE_PENDING"
  /\ retentionEligible
  /\ accessAuthorized
  /\ auditSatisfied
  /\ state' = "PURGED"
  /\ contentPresent' = FALSE
  /\ contentReturned' = FALSE
  /\ UNCHANGED << createAuthorized, accessAuthorized, auditSatisfied,
                  retentionEligible, result >>

PurgeRetentionDeny ==
  /\ state \in { "CLOSED", "HELD" }
  /\ ~retentionEligible
  /\ auditSatisfied' = TRUE
  /\ contentReturned' = FALSE
  /\ result' = "RETENTION_DENIED"
  /\ UNCHANGED << state, createAuthorized, accessAuthorized,
                  retentionEligible, contentPresent >>

PurgeAuthDeny ==
  /\ state \in { "CLOSED", "HELD" }
  /\ retentionEligible
  /\ accessAuthorized' = FALSE
  /\ auditSatisfied' = TRUE
  /\ contentReturned' = FALSE
  /\ result' = "DENY"
  /\ UNCHANGED << state, createAuthorized, retentionEligible, contentPresent >>

StaleReference ==
  /\ state = "PURGED"
  /\ contentReturned' = FALSE
  /\ result' = "STALE_REF"
  /\ UNCHANGED << state, createAuthorized, accessAuthorized, auditSatisfied,
                  retentionEligible, contentPresent >>

AuditUnavailable ==
  /\ state \notin TerminalStates
  /\ state' = "AUDIT_REQUIRED_BUT_UNAVAILABLE"
  /\ auditSatisfied' = FALSE
  /\ contentReturned' = FALSE
  /\ result' = "AUDIT_UNAVAILABLE"
  /\ UNCHANGED << createAuthorized, accessAuthorized, retentionEligible,
                  contentPresent >>

UnsupportedReject ==
  /\ state \notin TerminalStates
  /\ state' = "UNSUPPORTED"
  /\ contentReturned' = FALSE
  /\ result' = "UNSUPPORTED"
  /\ UNCHANGED << createAuthorized, accessAuthorized, auditSatisfied,
                  retentionEligible, contentPresent >>

SpecGapReject ==
  /\ state \notin TerminalStates
  /\ state' = "SPEC_GAP"
  /\ contentReturned' = FALSE
  /\ result' = "SPEC_GAP"
  /\ UNCHANGED << createAuthorized, accessAuthorized, auditSatisfied,
                  retentionEligible, contentPresent >>

InvalidTransitionRejected ==
  /\ result' = "INVALID_TRANSITION"
  /\ contentReturned' = FALSE
  /\ UNCHANGED << state, createAuthorized, accessAuthorized, auditSatisfied,
                  retentionEligible, contentPresent >>

Next ==
  \/ BeginCreateAuth
  \/ CreateAllow
  \/ CreateDeny
  \/ WriteFirstRecord
  \/ CloseOpenEntry
  \/ WriteNextRecord
  \/ CloseWrittenEntry
  \/ HoldClosed
  \/ ReleaseHeld
  \/ BrowseAllow
  \/ BrowseCloseToClosed
  \/ BrowseDeny
  \/ ExportAllow
  \/ ExportComplete
  \/ ExportDeny
  \/ RetentionBecomesEligible
  \/ PurgeAllow
  \/ PurgeComplete
  \/ PurgeRetentionDeny
  \/ PurgeAuthDeny
  \/ StaleReference
  \/ AuditUnavailable
  \/ UnsupportedReject
  \/ SpecGapReject
  \/ InvalidTransitionRejected

Spec == Init /\ [][Next]_vars

TypeOK ==
  /\ state \in SpoolStates
  /\ createAuthorized \in BOOLEAN
  /\ accessAuthorized \in BOOLEAN
  /\ auditSatisfied \in BOOLEAN
  /\ retentionEligible \in BOOLEAN
  /\ contentPresent \in BOOLEAN
  /\ contentReturned \in BOOLEAN
  /\ result \in Results

ContentRequiresAuthorizationAndAudit ==
  contentReturned => accessAuthorized /\ auditSatisfied /\ contentPresent

PurgedHasNoContent ==
  state = "PURGED" => ~contentPresent /\ ~contentReturned

PurgeRequiresRetentionAuthorizationAndAudit ==
  state = "PURGED" => retentionEligible /\ accessAuthorized /\ auditSatisfied

DenyReturnsNoContent ==
  result \in { "DENY", "STALE_REF", "RETENTION_DENIED", "UNSUPPORTED",
               "SPEC_GAP", "AUDIT_UNAVAILABLE", "INVALID_TRANSITION" }
    => ~contentReturned

====
