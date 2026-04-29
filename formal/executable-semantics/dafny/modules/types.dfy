// MFOS Phase 1 Dafny executable semantics: shared MFOS-owned object types.

include "common.dfy"
include "errors.dfy"

module Types {
  import opened Common
  import opened Errors

  datatype Principal = Principal(principal_id: MfosId)
  datatype Subject = Subject(principal: Principal, authenticated: bool)
  datatype ProgramIdentity = ProgramIdentity(program_id: MfosId, authorized: bool)
  datatype ObjectRef = ObjectRef(object_id: MfosId, generation: Generation)

  datatype Operation =
    OP_READ
  | OP_WRITE
  | OP_CREATE
  | OP_DELETE
  | OP_QUERY
  | OP_EXPORT
  | OP_PURGE
  | OP_SUBMIT
  | OP_CANCEL
  | OP_DISPLAY
  | OP_DEFINE

  datatype ProtectedResourceClass =
    RESOURCE_DATASET
  | RESOURCE_CATALOG
  | RESOURCE_JOB
  | RESOURCE_SPOOL
  | RESOURCE_OPERATOR_COMMAND
  | RESOURCE_AUDIT_STREAM
  | RESOURCE_SECURITY_POLICY
  | RESOURCE_SYSTEM_OBJECT

  datatype DecisionResult =
    ALLOW
  | DENY
  | ALLOW_WITH_AUDIT
  | REQUIRE_MFA
  | REQUIRE_DUAL_CONTROL
  | REQUIRE_BREAK_GLASS
  | REQUIRE_GUARD_APPROVAL
  | REQUIRE_OPERATOR_CONFIRMATION
  | UNSUPPORTED
  | SPEC_GAP

  datatype DecisionObligation =
    OBLIGATION_AUDIT
  | OBLIGATION_MFA
  | OBLIGATION_DUAL_CONTROL
  | OBLIGATION_BREAK_GLASS_REASON
  | OBLIGATION_BREAK_GLASS_EXPIRY
  | OBLIGATION_GUARD_APPROVAL
  | OBLIGATION_OPERATOR_CONFIRMATION

  datatype DecisionContext = DecisionContext(
    correlation_id: CorrelationId,
    policy_version: PolicyVersion,
    object_generation: Generation,
    deterministic_seed: DeterministicSeed
  )

  datatype SecurityDecision = SecurityDecision(
    subject: Subject,
    object_ref: ObjectRef,
    operation: Operation,
    resource_class: ProtectedResourceClass,
    result: DecisionResult,
    error_code: ErrorCode,
    reason_code: ReasonCode,
    policy_version: PolicyVersion,
    obligations: set<DecisionObligation>,
    context: DecisionContext
  )

  datatype SecurityProfile = SecurityProfile(profile_id: MfosId, policy_version: PolicyVersion)

  datatype PolicyBinding = PolicyBinding(
    subject: Subject,
    object_ref: ObjectRef,
    operation: Operation,
    resource_class: ProtectedResourceClass,
    policy_version: PolicyVersion,
    result: DecisionResult,
    reason_code: ReasonCode,
    obligations: set<DecisionObligation>
  )

  datatype ObjectGenerationBinding = ObjectGenerationBinding(
    object_ref: ObjectRef,
    policy_version: PolicyVersion
  )

  datatype AuditRecord = AuditRecord(
    record_id: MfosId,
    correlation_id: CorrelationId,
    sequence: SequenceNumber,
    record_type: MfosId,
    decision_result: DecisionResult,
    error_code: ErrorCode,
    reason_code: ReasonCode,
    before_return: bool,
    durable: bool,
    previous_hash: nat,
    record_hash: nat
  )

  datatype Dataset = Dataset(name_id: MfosId, object_ref: ObjectRef, immutable_system: bool, retention_active: bool)

  datatype CatalogEntryState =
    CATALOG_MISSING
  | CATALOG_STAGED
  | CATALOG_COMMITTED
  | CATALOG_ROLLED_BACK
  | CATALOG_PARTIAL_JOURNAL
  | CATALOG_INTEGRITY_FAILED

  datatype CatalogEntry = CatalogEntry(
    dataset: Dataset,
    state: CatalogEntryState,
    catalog_generation: Generation,
    dataset_generation: Generation,
    integrity_valid: bool
  )

  datatype DatasetHandle = DatasetHandle(
    handle_id: MfosId,
    subject: Subject,
    object_ref: ObjectRef,
    operation: Operation,
    policy_version: PolicyVersion,
    catalog_generation: Generation,
    dataset_generation: Generation,
    active: bool
  )

  datatype JobState = JOB_DEFINED | JOB_SUBMITTED | JOB_RUNNING | JOB_COMPLETE | JOB_FAILED | JOB_CANCELLED
  datatype StepState = STEP_PENDING | STEP_RUNNING | STEP_COMPLETE | STEP_FAILED

  datatype DD = DD(dd_id: MfosId, object_ref: ObjectRef, operation: Operation)
  datatype JobStep = JobStep(step_id: MfosId, state: StepState, rc: nat, dd_refs: seq<DD>)
  datatype Job = Job(job_id: MfosId, owner: Subject, effective_principal: Principal, state: JobState, steps: seq<JobStep>)

  datatype SpoolEntry = SpoolEntry(spool_id: MfosId, owner: Subject, job_id: MfosId, protected: bool, retained: bool)

  datatype OperatorAuthority = AUTH_DISPLAY | AUTH_DEFINE | AUTH_SUBMIT | AUTH_CANCEL | AUTH_DESTRUCTIVE
  datatype OperatorCommand = OperatorCommand(command_id: MfosId, authority: OperatorAuthority, audited: bool, confirmed: bool)

  datatype State = State(
    policy_version: PolicyVersion,
    catalog_generation: Generation,
    audit_sequence: SequenceNumber,
    job_state: JobState
  )

  datatype Evidence = Evidence(evidence_id: MfosId, correlation_id: CorrelationId, present: bool)

  predicate ValidSubject(subject: Subject) {
    ValidId(subject.principal.principal_id) && subject.authenticated
  }

  predicate DecisionIsSuccess(result: DecisionResult) {
    result == ALLOW || result == ALLOW_WITH_AUDIT
  }

  predicate DecisionIsFailClosed(result: DecisionResult) {
    result != ALLOW && result != ALLOW_WITH_AUDIT
  }
}
