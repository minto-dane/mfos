---- MODULE DatasetOpen ----
EXTENDS Naturals, TLC

\* Phase 0.8 design model for docs/design/specs/08-dataset-catalog.md.
\* This is not production code.

VARIABLES phase, catalogState, decision, audit, binding, handleState, result

Vars == <<phase, catalogState, decision, audit, binding, handleState, result>>

CatalogStates == {
  "COMMITTED_OK",
  "MISSING",
  "UNCOMMITTED",
  "ROLLED_BACK",
  "PARTIAL_JOURNAL",
  "INTEGRITY_BAD"
}

Init ==
  /\ phase = "REQUEST_OPEN"
  /\ catalogState \in CatalogStates
  /\ decision = "UNKNOWN"
  /\ audit = "PENDING"
  /\ binding = "NONE"
  /\ handleState = "NONE"
  /\ result = "NONE"

ValidateDsn ==
  /\ phase = "REQUEST_OPEN"
  /\ phase' = "VALIDATE_DSN"
  /\ UNCHANGED <<catalogState, decision, audit, binding, handleState, result>>

ResolveCatalogOk ==
  /\ phase = "VALIDATE_DSN"
  /\ catalogState = "COMMITTED_OK"
  /\ phase' = "RESOLVE_CATALOG"
  /\ UNCHANGED <<catalogState, decision, audit, binding, handleState, result>>

ResolveCatalogFail ==
  /\ phase = "VALIDATE_DSN"
  /\ catalogState # "COMMITTED_OK"
  /\ phase' = "CATALOG_NOT_FOUND"
  /\ result' = "FAILED_CLOSED"
  /\ handleState' = "NONE"
  /\ UNCHANGED <<catalogState, decision, audit, binding>>

AuthorizeAllow ==
  /\ phase = "RESOLVE_CATALOG"
  /\ decision = "UNKNOWN"
  /\ decision' = "ALLOW"
  /\ phase' = "AUTHORIZE"
  /\ UNCHANGED <<catalogState, audit, binding, handleState, result>>

AuthorizeDeny ==
  /\ phase = "RESOLVE_CATALOG"
  /\ decision = "UNKNOWN"
  /\ decision' = "DENY"
  /\ phase' = "POLICY_DENIED"
  /\ result' = "DENIED"
  /\ handleState' = "NONE"
  /\ UNCHANGED <<catalogState, audit, binding>>

EstablishAudit ==
  /\ phase = "AUTHORIZE"
  /\ decision = "ALLOW"
  /\ audit' = "APPENDED"
  /\ phase' = "ESTABLISH_AUDIT_OBLIGATION"
  /\ UNCHANGED <<catalogState, decision, binding, handleState, result>>

AuditFailure ==
  /\ phase = "AUTHORIZE"
  /\ decision = "ALLOW"
  /\ audit' = "FAILED"
  /\ result' = "FAILED_CLOSED"
  /\ phase' = "AUDIT_REQUIRED_BUT_UNAVAILABLE"
  /\ handleState' = "NONE"
  /\ UNCHANGED <<catalogState, decision, binding>>

VerifyGeneration ==
  /\ phase = "ESTABLISH_AUDIT_OBLIGATION"
  /\ audit = "APPENDED"
  /\ phase' = "VERIFY_GENERATION"
  /\ UNCHANGED <<catalogState, decision, audit, binding, handleState, result>>

VerifyIntegrity ==
  /\ phase = "VERIFY_GENERATION"
  /\ catalogState = "COMMITTED_OK"
  /\ phase' = "VERIFY_INTEGRITY_TAG"
  /\ UNCHANGED <<catalogState, decision, audit, binding, handleState, result>>

BindObjectGeneration ==
  /\ phase = "VERIFY_INTEGRITY_TAG"
  /\ binding' = "BOUND"
  /\ phase' = "BIND_OBJECT_GENERATION"
  /\ UNCHANGED <<catalogState, decision, audit, handleState, result>>

CreateHandle ==
  /\ phase = "BIND_OBJECT_GENERATION"
  /\ catalogState = "COMMITTED_OK"
  /\ decision = "ALLOW"
  /\ audit = "APPENDED"
  /\ binding = "BOUND"
  /\ handleState' = "ACTIVE"
  /\ result' = "OK"
  /\ phase' = "OPEN_ACTIVE"
  /\ UNCHANGED <<catalogState, decision, audit, binding>>

CloseHandle ==
  /\ phase = "OPEN_ACTIVE"
  /\ handleState = "ACTIVE"
  /\ phase' = "CLOSED"
  /\ handleState' = "CLOSED"
  /\ UNCHANGED <<catalogState, decision, audit, binding, result>>

Next ==
  \/ ValidateDsn
  \/ ResolveCatalogOk
  \/ ResolveCatalogFail
  \/ AuthorizeAllow
  \/ AuthorizeDeny
  \/ EstablishAudit
  \/ AuditFailure
  \/ VerifyGeneration
  \/ VerifyIntegrity
  \/ BindObjectGeneration
  \/ CreateHandle
  \/ CloseHandle

Spec == Init /\ [][Next]_Vars

NoActiveHandleWithoutCommittedCatalog ==
  handleState = "ACTIVE" => catalogState = "COMMITTED_OK"

NoActiveHandleWithoutAllow ==
  handleState = "ACTIVE" => decision = "ALLOW"

NoActiveHandleWithoutAudit ==
  handleState = "ACTIVE" => audit = "APPENDED"

NoActiveHandleWithoutGenerationBinding ==
  handleState = "ACTIVE" => binding = "BOUND"

DenyOrFailClosedCreatesNoHandle ==
  result \in {"DENIED", "FAILED_CLOSED"} => handleState = "NONE"

====
