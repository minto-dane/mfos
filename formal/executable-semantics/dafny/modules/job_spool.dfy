// MFOS Phase 1 Dafny executable semantics: job/spool model.
// This is not jobd, spoold, a scheduler, or a service.

include "common.dfy"
include "errors.dfy"
include "types.dfy"
include "authorization.dfy"
include "dataset_catalog.dfy"
include "audit.dfy"

module JobSpool {
  import opened Common
  import opened Errors
  import opened Types
  import Authorization
  import DatasetCatalog
  import Audit

  predicate EffectivePrincipalEstablished(job: Job) {
    ValidId(job.effective_principal.principal_id) && ValidSubject(job.owner)
  }

  predicate RequestedPrincipalValid(ctx: JobSubmitContext) {
    match ctx.requested_principal
    case None => true
    case Some(principal) => ValidId(principal.principal_id)
  }

  predicate SubmitDecisionAllows(ctx: JobSubmitContext) {
    ctx.submit_decision.subject == ctx.submitter &&
    ctx.submit_decision.resource_class == RESOURCE_JOB &&
    ctx.submit_decision.operation == OP_SUBMIT &&
    ctx.submit_decision.policy_version == ctx.policy_version &&
    ctx.submit_decision.context.policy_version == ctx.policy_version &&
    ctx.submit_decision.context.correlation_id == ctx.correlation_id &&
    Authorization.DecisionAllowsProtectedEffect(ctx.submit_decision)
  }

  predicate SubmitAsDecisionAllows(ctx: JobSubmitContext) {
    match ctx.requested_principal
    case None => true
    case Some(principal) =>
      principal == ctx.submitter.principal ||
      (
        ctx.submit_as_decision.Some? &&
        ctx.submit_as_decision.value.subject == ctx.submitter &&
        ctx.submit_as_decision.value.object_ref.object_id == principal.principal_id &&
        ctx.submit_as_decision.value.resource_class == RESOURCE_JOB &&
        ctx.submit_as_decision.value.operation == OP_SUBMIT &&
        ctx.submit_as_decision.value.policy_version == ctx.policy_version &&
        ctx.submit_as_decision.value.context.policy_version == ctx.policy_version &&
        ctx.submit_as_decision.value.context.correlation_id == ctx.correlation_id &&
        Authorization.DecisionAllowsProtectedEffect(ctx.submit_as_decision.value)
      )
  }

  predicate CanEstablishEffectivePrincipal(ctx: JobSubmitContext) {
    ValidId(ctx.job_id) &&
    ValidSubject(ctx.submitter) &&
    ValidPolicyVersion(ctx.policy_version) &&
    ValidCorrelationId(ctx.correlation_id) &&
    RequestedPrincipalValid(ctx) &&
    SubmitDecisionAllows(ctx) &&
    SubmitAsDecisionAllows(ctx)
  }

  function EstablishEffectivePrincipal(ctx: JobSubmitContext): Option<EffectivePrincipal> {
    if CanEstablishEffectivePrincipal(ctx) then
      match ctx.requested_principal
      case None => Some(EffectivePrincipal(ctx.submitter.principal, ctx.job_id, ctx.policy_version, ctx.correlation_id))
      case Some(principal) => Some(EffectivePrincipal(principal, ctx.job_id, ctx.policy_version, ctx.correlation_id))
    else None
  }

  predicate EffectivePrincipalBoundToJob(job: Job, effective: EffectivePrincipal) {
    ValidId(effective.principal.principal_id) &&
    effective.job_id == job.job_id &&
    effective.principal == job.effective_principal &&
    ValidPolicyVersion(effective.policy_version) &&
    ValidCorrelationId(effective.correlation_id)
  }

  predicate JobContextHasEffectivePrincipal(ctx: JobContext) {
    ctx.effective.Some? &&
    EffectivePrincipalBoundToJob(ctx.job, ctx.effective.value) &&
    ctx.effective.value.policy_version == ctx.policy_version &&
    ctx.effective.value.correlation_id == ctx.correlation_id
  }

  predicate EffectiveJobContextValid(effective_context: EffectiveJobContext) {
    JobContextHasEffectivePrincipal(effective_context.context) &&
    effective_context.context.effective.value == effective_context.effective &&
    EffectivePrincipalBoundToJob(effective_context.context.job, effective_context.effective) &&
    effective_context.effective.policy_version == effective_context.context.policy_version &&
    effective_context.effective.correlation_id == effective_context.context.correlation_id
  }

  predicate IsSuccessDecision(decision: SecurityDecision) {
    DecisionIsSuccess(decision.result) && IsSuccessError(decision.error_code)
  }

  predicate IsNonSuccessDecision(decision: SecurityDecision) {
    !DecisionIsSuccess(decision.result) && !IsSuccessError(decision.error_code)
  }

  predicate ValidAllowDecision(decision: SecurityDecision) {
    Authorization.DecisionAllowsProtectedEffect(decision)
  }

  predicate ValidDenyDecision(decision: SecurityDecision) {
    Authorization.DecisionWellFormed(decision) &&
    decision.result == DENY &&
    !IsSuccessError(decision.error_code)
  }

  predicate IsBoundDDDecision(ctx: JobContext, dd: DD, decision: SecurityDecision) {
    JobContextHasEffectivePrincipal(ctx) &&
    Authorization.DecisionWellFormed(decision) &&
    decision.subject.principal == ctx.effective.value.principal &&
    decision.object_ref == dd.object_ref &&
    decision.operation == dd.operation &&
    decision.resource_class == RESOURCE_DATASET &&
    decision.policy_version == ctx.policy_version &&
    decision.context.policy_version == ctx.policy_version &&
    decision.context.correlation_id == ctx.correlation_id &&
    decision.context.correlation_id == ctx.effective.value.correlation_id
  }

  predicate BoundDDDecisionValid(bound: BoundDDDecision) {
    EffectiveJobContextValid(bound.context) &&
    IsBoundDDDecision(bound.context.context, bound.dd, bound.decision)
  }

  predicate BoundDDDecisionMatchesEntry(bound: BoundDDDecision, entry: CatalogEntry) {
    bound.dd.object_ref == entry.dataset.object_ref &&
    bound.decision.object_ref == entry.dataset.object_ref &&
    bound.decision.context.object_generation == entry.catalog_generation
  }

  predicate DDResolutionThroughCatalogAndAuth(bound: BoundDDDecision, entry: CatalogEntry, satisfied: set<DecisionObligation>) {
    BoundDDDecisionValid(bound) &&
    BoundDDDecisionMatchesEntry(bound, entry) &&
    DatasetCatalog.MayCreateDatasetHandle(entry, bound.decision, satisfied)
  }

  predicate DatasetOpenAllowedForJob(bound: BoundDDDecision, entry: CatalogEntry, satisfied: set<DecisionObligation>) {
    DDResolutionPreconditions(bound, entry, satisfied)
  }

  predicate DDResolutionPreconditions(bound: BoundDDDecision, entry: CatalogEntry, satisfied: set<DecisionObligation>) {
    DDResolutionThroughCatalogAndAuth(bound, entry, satisfied) &&
    ValidAllowDecision(bound.decision)
  }

  predicate BoundDDDecisionDeniesWithAudit(bound: BoundDDDecision, entry: CatalogEntry) {
    BoundDDDecisionValid(bound) &&
    BoundDDDecisionMatchesEntry(bound, entry) &&
    ValidDenyDecision(bound.decision) &&
    Authorization.RequiresAudit(bound.decision)
  }

  function DDResolutionFailureError(bound: BoundDDDecision, entry: CatalogEntry): ErrorCode {
    if !EffectiveJobContextValid(bound.context) then MFOS_ERR_UNAUTHENTICATED
    else if !IsBoundDDDecision(bound.context.context, bound.dd, bound.decision) then MFOS_ERR_POLICY_DENIED
    else if !DatasetCatalog.SymbolicDsnValid(entry.dataset) then MFOS_ERR_INVALID_DSN
    else if !BoundDDDecisionMatchesEntry(bound, entry) then MFOS_ERR_CATALOG_NOT_FOUND
    else DatasetCatalog.DatasetOpenFailureError(entry, bound.decision)
  }

  function ResolveDDForJob(bound: BoundDDDecision, entry: CatalogEntry, satisfied: set<DecisionObligation>, handle_id: MfosId): Result<DatasetHandle> {
    if !DDResolutionPreconditions(bound, entry, satisfied) then
      ResultErr(ErrorRank(DDResolutionFailureError(bound, entry)))
    else
      DatasetCatalog.CreateDatasetHandle(entry, bound.decision, satisfied, handle_id)
  }

  function DeniedDDResolutionWithAudit(bound: BoundDDDecision, entry: CatalogEntry, prior_records: seq<AuditRecord>, next_record_id: MfosId, audit_available: bool): DDResolutionResult
    requires BoundDDDecisionDeniesWithAudit(bound, entry)
    requires ValidId(next_record_id)
  {
    var outcome := DatasetCatalog.DeniedDatasetOpenWithAudit(bound.decision, prior_records, next_record_id, audit_available);
    DDResolutionResult(
      DDResolution(bound.dd, outcome.handle, outcome.error_code, bound.decision.reason_code,
        if outcome.error_code == MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE then DD_FAILURE_AUDIT_UNAVAILABLE else DD_FAILURE_AUTHORIZATION_DENIED),
      outcome.audit_records,
      outcome.result_released)
  }

  predicate ValidJobTransition(from_state: JobState, to_state: JobState) {
    (from_state == JOB_DEFINED && to_state == JOB_SUBMITTED) ||
    (from_state == JOB_SUBMITTED && to_state == JOB_VALIDATED) ||
    (from_state == JOB_VALIDATED && to_state == JOB_READY) ||
    (from_state == JOB_READY && to_state == JOB_EXECUTING) ||
    (from_state == JOB_EXECUTING && to_state == JOB_RUNNING) ||
    (from_state == JOB_RUNNING && to_state == JOB_COMPLETE) ||
    (from_state == JOB_RUNNING && to_state == JOB_FAILED) ||
    (from_state == JOB_EXECUTING && to_state == JOB_FAILED) ||
    (from_state == JOB_SUBMITTED && to_state == JOB_CANCELLED) ||
    (from_state == JOB_VALIDATED && to_state == JOB_CANCELLED) ||
    (from_state == JOB_READY && to_state == JOB_CANCELLED) ||
    (from_state == JOB_EXECUTING && to_state == JOB_CANCELLED) ||
    (from_state == JOB_RUNNING && to_state == JOB_CANCELLED) ||
    (from_state == JOB_READY && to_state == JOB_HELD) ||
    (from_state == JOB_HELD && to_state == JOB_READY)
  }

  function TransitionJobState(from_state: JobState, to_state: JobState): JobValidationResult {
    if ValidJobTransition(from_state, to_state) then
      JobValidationResult(true, to_state, MFOS_OK, REASON_OK)
    else
      JobValidationResult(false, from_state, MFOS_ERR_INVALID_STATE, INVALID_LIFECYCLE_TRANSITION)
  }

  predicate ValidStepTransition(from_state: StepState, to_state: StepState) {
    (from_state == STEP_PENDING && to_state == STEP_READY) ||
    (from_state == STEP_READY && to_state == STEP_RUNNING) ||
    (from_state == STEP_RUNNING && to_state == STEP_COMPLETE) ||
    (from_state == STEP_RUNNING && to_state == STEP_FAILED)
  }

  predicate StepTerminal(step: JobStep) {
    step.state == STEP_COMPLETE || step.state == STEP_FAILED
  }

  predicate AllStepsTerminal(steps: seq<JobStep>) {
    forall i :: 0 <= i < |steps| ==> StepTerminal(steps[i])
  }

  predicate JobCanComplete(job: Job) {
    job.state == JOB_RUNNING && AllStepsTerminal(job.steps)
  }

  predicate JobCanStartExecution(ctx: JobContext) {
    ctx.job.state == JOB_READY && JobContextHasEffectivePrincipal(ctx)
  }

  predicate JobStepCanRun(ctx: JobContext, step: JobStep) {
    JobContextHasEffectivePrincipal(ctx) &&
    (ctx.job.state == JOB_EXECUTING || ctx.job.state == JOB_RUNNING) &&
    step.state == STEP_READY
  }

  function FailureReturnCode(reason: JobFailureReason): nat {
    match reason
    case JOB_FAILURE_NONE => 0
    case JOB_FAILURE_INVALID_TRANSITION => 16
    case JOB_FAILURE_MISSING_EFFECTIVE_PRINCIPAL => 12
    case JOB_FAILURE_DD_RESOLUTION_DENIED => 8
    case JOB_FAILURE_DD_RESOLUTION_INVALID => 12
    case JOB_FAILURE_AUDIT_UNAVAILABLE => 12
    case JOB_FAILURE_SPEC_GAP => 16
    case JOB_FAILURE_UNSUPPORTED => 16
  }

  function JobFailurePlaceholder(reason: JobFailureReason, error: ErrorCode): JobExecutionPlaceholder {
    JobExecutionPlaceholder(JOB_FAILED, FailureReturnCode(reason), reason, error)
  }

  predicate SpoolEntryProtected(spool: SpoolEntry) {
    spool.protected && ValidId(spool.spool_id) && ValidSubject(spool.owner)
  }

  predicate ValidSpoolOperation(operation: Operation) {
    operation == OP_QUERY || operation == OP_PURGE || operation == OP_EXPORT
  }

  predicate ValidSpoolAllowDecision(decision: SecurityDecision) {
    Authorization.DecisionAllowsProtectedEffect(decision)
  }

  predicate ValidSpoolDenyDecision(decision: SecurityDecision) {
    Authorization.DecisionWellFormed(decision) &&
    decision.result == DENY &&
    !IsSuccessError(decision.error_code)
  }

  predicate IsBoundSpoolDecision(ctx: SpoolAccessContext, spool: SpoolEntry, operation: Operation, decision: SecurityDecision) {
    SpoolEntryProtected(spool) &&
    ValidSpoolOperation(operation) &&
    ValidSubject(ctx.subject) &&
    ValidPolicyVersion(ctx.policy_version) &&
    ValidCorrelationId(ctx.correlation_id) &&
    Authorization.DecisionWellFormed(decision) &&
    decision.subject == ctx.subject &&
    decision.object_ref.object_id == spool.spool_id &&
    ValidGeneration(decision.object_ref.generation) &&
    decision.object_ref.generation == decision.context.object_generation &&
    decision.operation == operation &&
    decision.resource_class == RESOURCE_SPOOL &&
    decision.policy_version == ctx.policy_version &&
    decision.context.policy_version == ctx.policy_version &&
    decision.context.correlation_id == ctx.correlation_id
  }

  predicate BoundSpoolDecisionValid(bound: BoundSpoolDecision) {
    IsBoundSpoolDecision(bound.context, bound.spool, bound.operation, bound.decision)
  }

  predicate BoundSpoolDecisionDeniesWithAudit(bound: BoundSpoolDecision) {
    BoundSpoolDecisionValid(bound) &&
    ValidSpoolDenyDecision(bound.decision) &&
    Authorization.RequiresAudit(bound.decision)
  }

  predicate SpoolBrowseAllowed(spool: SpoolEntry, decision: SecurityDecision) {
    SpoolEntryProtected(spool) &&
    decision.subject == spool.owner &&
    decision.object_ref.object_id == spool.spool_id &&
    decision.object_ref.generation == decision.context.object_generation &&
    decision.resource_class == RESOURCE_SPOOL &&
    decision.operation == OP_QUERY &&
    Authorization.DecisionAllowsProtectedEffect(decision)
  }

  predicate SpoolBrowseCanReturnContent(bound: BoundSpoolDecision, records: seq<AuditRecord>) {
    BoundSpoolDecisionValid(bound) &&
    bound.operation == OP_QUERY &&
    ValidSpoolAllowDecision(bound.decision) &&
    Audit.RequiredAuditSatisfiedForFinalResult(bound.decision, records)
  }

  predicate SpoolPurgeDeniedWithoutAuthority(decision: SecurityDecision) {
    decision.resource_class == RESOURCE_SPOOL &&
    decision.operation == OP_PURGE &&
    !Authorization.DecisionAllowsProtectedEffect(decision)
  }

  predicate SpoolPurgeCanRemoveContent(bound: BoundSpoolDecision, records: seq<AuditRecord>) {
    BoundSpoolDecisionValid(bound) &&
    bound.operation == OP_PURGE &&
    !bound.spool.retained &&
    ValidSpoolAllowDecision(bound.decision) &&
    Audit.RequiredAuditSatisfiedForFinalResult(bound.decision, records)
  }

  predicate SpoolExportCanComplete(bound: BoundSpoolDecision, records: seq<AuditRecord>) {
    BoundSpoolDecisionValid(bound) &&
    bound.operation == OP_EXPORT &&
    ValidSpoolAllowDecision(bound.decision) &&
    Authorization.RequiresAudit(bound.decision) &&
    Audit.RequiredAuditSatisfiedForFinalResult(bound.decision, records)
  }

  predicate SpoolEvidenceIsAuditEvidence(evidence: SpoolEvidence, record: AuditRecord) {
    false
  }

  function DeniedSpoolAccessWithAudit(bound: BoundSpoolDecision, prior_records: seq<AuditRecord>, next_record_id: MfosId, audit_available: bool): SpoolAccessResult
    requires BoundSpoolDecisionDeniesWithAudit(bound)
    requires ValidId(next_record_id)
  {
    var outcome := Audit.FinalizeDeniedOperation(bound.decision, prior_records, next_record_id, audit_available);
    SpoolAccessResult(outcome.final_error, bound.decision.reason_code, outcome.records_after,
      outcome.result_released, false, false, false)
  }

  function ExportSpoolAccess(bound: BoundSpoolDecision, prior_records: seq<AuditRecord>, next_record_id: MfosId, audit_available: bool): SpoolAccessResult
    requires BoundSpoolDecisionValid(bound)
    requires bound.operation == OP_EXPORT
    requires ValidSpoolAllowDecision(bound.decision)
    requires Authorization.RequiresAudit(bound.decision)
    requires ValidId(next_record_id)
  {
    var outcome := Audit.FinalizeRequiredAuditedOperation(bound.decision, prior_records, next_record_id, audit_available);
    SpoolAccessResult(outcome.final_error, bound.decision.reason_code, outcome.records_after,
      outcome.result_released, false, false, outcome.result_released && outcome.final_error == MFOS_OK)
  }

  function RejectInvalidSpoolAuditEvidence(bound: BoundSpoolDecision, prior_records: seq<AuditRecord>): SpoolAccessResult {
    SpoolAccessResult(MFOS_ERR_INVALID_AUDIT_RECORD, AUDIT_RECORD_INVALID, prior_records, false, false, false, false)
  }

  lemma INV_JOB_EFFECTIVE_PRINCIPAL_BEFORE_OPEN(ctx: JobContext, dd: DD, decision: SecurityDecision)
    requires !JobContextHasEffectivePrincipal(ctx)
    ensures !IsBoundDDDecision(ctx, dd, decision)
  {
  }

  lemma INV_JOB_CONTEXT_EFFECTIVE_PRINCIPAL_BEFORE_OPEN(bound: BoundDDDecision, entry: CatalogEntry, satisfied: set<DecisionObligation>, handle_id: MfosId)
    requires !JobContextHasEffectivePrincipal(bound.context.context)
    ensures !BoundDDDecisionValid(bound)
    ensures !DDResolutionPreconditions(bound, entry, satisfied)
    ensures ResolveDDForJob(bound, entry, satisfied, handle_id).ResultErr?
  {
  }

  lemma INV_JOB_SUBMIT_NO_PRINCIPAL_FAILS_CLOSED(ctx: JobSubmitContext)
    requires !CanEstablishEffectivePrincipal(ctx)
    ensures EstablishEffectivePrincipal(ctx).None?
  {
  }

  lemma INV_JOB_DEFAULT_EFFECTIVE_PRINCIPAL_IS_SUBMITTER(ctx: JobSubmitContext)
    requires CanEstablishEffectivePrincipal(ctx)
    requires ctx.requested_principal.None?
    ensures EstablishEffectivePrincipal(ctx).Some?
    ensures EstablishEffectivePrincipal(ctx).value.principal == ctx.submitter.principal
    ensures EstablishEffectivePrincipal(ctx).value.job_id == ctx.job_id
    ensures EstablishEffectivePrincipal(ctx).value.policy_version == ctx.policy_version
    ensures EstablishEffectivePrincipal(ctx).value.correlation_id == ctx.correlation_id
  {
  }

  lemma INV_JOB_SUBMIT_AS_REQUIRES_AUTHORIZATION(ctx: JobSubmitContext, requested: Principal)
    requires ctx.requested_principal == Some(requested)
    requires requested != ctx.submitter.principal
    requires !ctx.submit_as_decision.Some? || !Authorization.DecisionAllowsProtectedEffect(ctx.submit_as_decision.value)
    ensures !SubmitAsDecisionAllows(ctx)
    ensures !CanEstablishEffectivePrincipal(ctx)
    ensures EstablishEffectivePrincipal(ctx).None?
  {
  }

  lemma INV_JOB_EFFECTIVE_PRINCIPAL_BINDS_POLICY_AND_CORRELATION(ctx: JobSubmitContext)
    requires CanEstablishEffectivePrincipal(ctx)
    ensures EstablishEffectivePrincipal(ctx).Some?
    ensures EstablishEffectivePrincipal(ctx).value.policy_version == ctx.policy_version
    ensures EstablishEffectivePrincipal(ctx).value.correlation_id == ctx.correlation_id
    ensures EstablishEffectivePrincipal(ctx).value.job_id == ctx.job_id
  {
  }

  lemma INV_JOB_NO_QUEUE_WITHOUT_EFFECTIVE_PRINCIPAL(ctx: JobContext)
    requires !JobContextHasEffectivePrincipal(ctx)
    ensures !JobCanStartExecution(ctx)
  {
  }

  lemma INV_JOB_DD_DECISION_REQUIRES_EFFECTIVE_CONTEXT(bound: BoundDDDecision)
    requires BoundDDDecisionValid(bound)
    ensures EffectiveJobContextValid(bound.context)
    ensures JobContextHasEffectivePrincipal(bound.context.context)
    ensures bound.context.context.effective.value == bound.context.effective
    ensures bound.context.effective.policy_version == bound.context.context.policy_version
    ensures bound.context.effective.correlation_id == bound.context.context.correlation_id
  {
  }

  lemma INV_JOB_DD_BOUND_DECISION_BINDS_REQUEST(bound: BoundDDDecision)
    requires BoundDDDecisionValid(bound)
    ensures bound.decision.subject.principal == bound.context.effective.principal
    ensures bound.decision.object_ref == bound.dd.object_ref
    ensures bound.decision.operation == bound.dd.operation
    ensures bound.decision.resource_class == RESOURCE_DATASET
    ensures bound.decision.policy_version == bound.context.context.policy_version
    ensures bound.decision.context.policy_version == bound.context.context.policy_version
    ensures bound.decision.context.correlation_id == bound.context.context.correlation_id
    ensures Authorization.DecisionWellFormed(bound.decision)
  {
  }

  lemma INV_JOB_DD_CROSS_REQUEST_AUTHORIZATION_REPLAY_BLOCKED(ctx: JobContext, dd: DD, decision: SecurityDecision)
    requires decision.context.correlation_id != ctx.correlation_id
    ensures !IsBoundDDDecision(ctx, dd, decision)
  {
  }

  lemma INV_JOB_DD_DENY_MFOS_OK_INVALID(decision: SecurityDecision)
    requires decision.result == DENY
    requires decision.error_code == MFOS_OK
    ensures !ValidDenyDecision(decision)
    ensures !IsNonSuccessDecision(decision)
  {
  }

  lemma INV_JOB_DD_VALID_ALLOW_AND_DENY_DISTINGUISHABLE(decision: SecurityDecision)
    ensures ValidAllowDecision(decision) ==> !ValidDenyDecision(decision)
    ensures ValidDenyDecision(decision) ==> !ValidAllowDecision(decision)
  {
  }

  lemma INV_JOB_DD_RESOLUTION_THROUGH_CATALOG_AND_AUTH(bound: BoundDDDecision, entry: CatalogEntry, satisfied: set<DecisionObligation>)
    requires DDResolutionPreconditions(bound, entry, satisfied)
    ensures DatasetCatalog.CatalogEntryResolvable(entry)
    ensures Authorization.DecisionAllowsProtectedEffect(bound.decision)
    ensures DatasetCatalog.MayCreateDatasetHandle(entry, bound.decision, satisfied)
    ensures BoundDDDecisionValid(bound)
    ensures BoundDDDecisionMatchesEntry(bound, entry)
    ensures bound.decision.subject.principal == bound.context.effective.principal
    ensures bound.decision.object_ref == bound.dd.object_ref
    ensures bound.decision.object_ref == entry.dataset.object_ref
    ensures bound.decision.operation == bound.dd.operation
    ensures bound.decision.context.object_generation == entry.catalog_generation
    ensures bound.decision.context.correlation_id == bound.context.context.correlation_id
  {
  }

  lemma INV_JOB_DD_RESOLUTION_CANNOT_BYPASS_CATALOG(bound: BoundDDDecision, entry: CatalogEntry, satisfied: set<DecisionObligation>, handle_id: MfosId)
    requires !DatasetCatalog.CatalogEntryResolvable(entry)
    ensures !DDResolutionPreconditions(bound, entry, satisfied)
    ensures ResolveDDForJob(bound, entry, satisfied, handle_id).ResultErr?
  {
  }

  lemma INV_JOB_DD_RESOLUTION_CANNOT_BYPASS_AUTHORIZATION(bound: BoundDDDecision, entry: CatalogEntry, satisfied: set<DecisionObligation>, handle_id: MfosId)
    requires !Authorization.CanCreateProtectedResourceHandle(bound.decision, satisfied)
    ensures !DDResolutionPreconditions(bound, entry, satisfied)
    ensures ResolveDDForJob(bound, entry, satisfied, handle_id).ResultErr?
  {
  }

  lemma INV_JOB_DD_SUCCESS_CREATES_BOUND_DATASET_HANDLE(bound: BoundDDDecision, entry: CatalogEntry, satisfied: set<DecisionObligation>, handle_id: MfosId)
    requires DDResolutionPreconditions(bound, entry, satisfied)
    ensures ResolveDDForJob(bound, entry, satisfied, handle_id).ResultOk?
    ensures DatasetCatalog.HandleBoundToObjectGeneration(DatasetCatalog.MakeDatasetHandle(entry, bound.decision, handle_id), entry, bound.decision)
    ensures DatasetCatalog.MakeDatasetHandle(entry, bound.decision, handle_id).subject.principal == bound.context.effective.principal
    ensures DatasetCatalog.MakeDatasetHandle(entry, bound.decision, handle_id).object_ref == bound.dd.object_ref
    ensures DatasetCatalog.MakeDatasetHandle(entry, bound.decision, handle_id).operation == bound.dd.operation
    ensures DatasetCatalog.MakeDatasetHandle(entry, bound.decision, handle_id).policy_version == bound.context.context.policy_version
    ensures bound.decision.context.correlation_id == bound.context.context.correlation_id
  {
    DatasetCatalog.INV_DATASET_CREATE_HANDLE_BINDS_DECISION(entry, bound.decision, satisfied, handle_id);
  }

  lemma INV_JOB_DD_DENY_PRODUCES_NO_HANDLE(bound: BoundDDDecision, entry: CatalogEntry, satisfied: set<DecisionObligation>, handle_id: MfosId)
    requires bound.decision.result == DENY
    ensures ResolveDDForJob(bound, entry, satisfied, handle_id).ResultErr?
  {
  }

  lemma INV_JOB_UNAUTHORIZED_DATASET_STEP_FAILS_CLOSED(bound: BoundDDDecision, entry: CatalogEntry, satisfied: set<DecisionObligation>, handle_id: MfosId)
    requires bound.decision.result == DENY
    ensures ResolveDDForJob(bound, entry, satisfied, handle_id).ResultErr?
    ensures !IsSuccessError(DatasetCatalog.DatasetOpenFailureError(entry, bound.decision))
  {
    DatasetCatalog.INV_DATASET_DENY_DECISION_NOT_MFOS_OK(entry, bound.decision);
  }

  lemma INV_JOB_DD_MALFORMED_DSN_FAILS(bound: BoundDDDecision, entry: CatalogEntry, satisfied: set<DecisionObligation>, handle_id: MfosId)
    requires !DatasetCatalog.SymbolicDsnValid(entry.dataset)
    ensures ResolveDDForJob(bound, entry, satisfied, handle_id).ResultErr?
    ensures DDResolutionFailureError(bound, entry) == MFOS_ERR_INVALID_DSN ||
      !EffectiveJobContextValid(bound.context) ||
      !IsBoundDDDecision(bound.context.context, bound.dd, bound.decision)
  {
  }

  lemma INV_JOB_DD_UNRESOLVED_CATALOG_FAILS(bound: BoundDDDecision, entry: CatalogEntry, satisfied: set<DecisionObligation>, handle_id: MfosId)
    requires !DatasetCatalog.CatalogEntryResolvable(entry)
    ensures ResolveDDForJob(bound, entry, satisfied, handle_id).ResultErr?
  {
  }

  lemma INV_JOB_DD_UNCOMMITTED_CATALOG_FAILS(bound: BoundDDDecision, entry: CatalogEntry, satisfied: set<DecisionObligation>, handle_id: MfosId)
    requires entry.state == CATALOG_UNCOMMITTED || entry.state == CATALOG_STAGED
    ensures ResolveDDForJob(bound, entry, satisfied, handle_id).ResultErr?
  {
    DatasetCatalog.INV_CATALOG_UNCOMMITTED_CANNOT_RESOLVE(entry);
  }

  lemma INV_JOB_DD_ROLLED_BACK_CATALOG_FAILS(bound: BoundDDDecision, entry: CatalogEntry, satisfied: set<DecisionObligation>, handle_id: MfosId)
    requires entry.state == CATALOG_ROLLED_BACK
    ensures ResolveDDForJob(bound, entry, satisfied, handle_id).ResultErr?
  {
    DatasetCatalog.INV_CATALOG_ROLLED_BACK_CANNOT_RESOLVE(entry);
  }

  lemma INV_JOB_DD_PARTIAL_JOURNAL_CATALOG_FAILS(bound: BoundDDDecision, entry: CatalogEntry, satisfied: set<DecisionObligation>, handle_id: MfosId)
    requires entry.state == CATALOG_PARTIAL_JOURNAL
    requires DatasetCatalog.SymbolicDsnValid(entry.dataset)
    ensures ResolveDDForJob(bound, entry, satisfied, handle_id).ResultErr?
  {
    DatasetCatalog.INV_CATALOG_PARTIAL_JOURNAL_CANNOT_RESOLVE(entry);
  }

  lemma INV_JOB_DD_INTEGRITY_FAILED_CATALOG_FAILS(bound: BoundDDDecision, entry: CatalogEntry, satisfied: set<DecisionObligation>, handle_id: MfosId)
    requires entry.state == CATALOG_INTEGRITY_FAILED || !entry.integrity_valid || !entry.integrity_tag.verified
    requires DatasetCatalog.SymbolicDsnValid(entry.dataset)
    ensures ResolveDDForJob(bound, entry, satisfied, handle_id).ResultErr?
  {
    DatasetCatalog.INV_CATALOG_INTEGRITY_FAILED_CANNOT_RESOLVE(entry);
  }

  lemma INV_JOB_DD_STALE_HANDLE_AFTER_POLICY_CHANGE_FAILS(handle: DatasetHandle, active_policy: PolicyVersion, entry: CatalogEntry)
    requires handle.policy_version != active_policy
    ensures DatasetCatalog.ValidateDatasetHandle(handle, active_policy, entry).ResultErr?
  {
    DatasetCatalog.INV_DATASET_STALE_HANDLE_AFTER_POLICY_CHANGE_REJECTED(handle, active_policy, entry);
  }

  lemma INV_JOB_DD_DENY_WITH_AUDIT_LINKS_BEFORE_RETURN(bound: BoundDDDecision, entry: CatalogEntry, prior_records: seq<AuditRecord>, next_record_id: MfosId)
    requires BoundDDDecisionDeniesWithAudit(bound, entry)
    requires ValidId(next_record_id)
    ensures DeniedDDResolutionWithAudit(bound, entry, prior_records, next_record_id, true).resolution.handle.None?
    ensures DeniedDDResolutionWithAudit(bound, entry, prior_records, next_record_id, true).resolution.error_code == bound.decision.error_code
    ensures Audit.RequiredAuditSatisfiedForFinalResult(bound.decision, DeniedDDResolutionWithAudit(bound, entry, prior_records, next_record_id, true).audit_records)
    ensures DeniedDDResolutionWithAudit(bound, entry, prior_records, next_record_id, true).result_released
  {
    DatasetCatalog.INV_DATASET_OPEN_DENY_WITH_AUDIT_WRITES_BEFORE_RETURN(bound.decision, prior_records, next_record_id);
  }

  lemma INV_JOB_DD_DENY_AUDIT_UNAVAILABLE_FAILS_CLOSED(bound: BoundDDDecision, entry: CatalogEntry, prior_records: seq<AuditRecord>, next_record_id: MfosId)
    requires BoundDDDecisionDeniesWithAudit(bound, entry)
    requires ValidId(next_record_id)
    ensures DeniedDDResolutionWithAudit(bound, entry, prior_records, next_record_id, false).resolution.handle.None?
    ensures DeniedDDResolutionWithAudit(bound, entry, prior_records, next_record_id, false).resolution.error_code == MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE
    ensures !DeniedDDResolutionWithAudit(bound, entry, prior_records, next_record_id, false).result_released
    ensures !IsSuccessError(DeniedDDResolutionWithAudit(bound, entry, prior_records, next_record_id, false).resolution.error_code)
  {
    DatasetCatalog.INV_DATASET_OPEN_DENY_AUDIT_UNAVAILABLE_FAILS_CLOSED(bound.decision, prior_records, next_record_id);
  }

  lemma INV_SPOOL_PROTECTED_RESOURCE(spool: SpoolEntry)
    requires SpoolEntryProtected(spool)
    ensures spool.protected
    ensures ValidId(spool.spool_id)
    ensures ValidSubject(spool.owner)
  {
  }

  lemma INV_SPOOL_DECISION_BINDS_ENTRY(bound: BoundSpoolDecision)
    requires BoundSpoolDecisionValid(bound)
    ensures bound.decision.subject == bound.context.subject
    ensures bound.decision.object_ref.object_id == bound.spool.spool_id
    ensures ValidGeneration(bound.decision.object_ref.generation)
    ensures bound.decision.object_ref.generation == bound.decision.context.object_generation
    ensures bound.decision.operation == bound.operation
    ensures bound.decision.resource_class == RESOURCE_SPOOL
    ensures bound.decision.policy_version == bound.context.policy_version
    ensures bound.decision.context.policy_version == bound.context.policy_version
    ensures bound.decision.context.correlation_id == bound.context.correlation_id
    ensures Authorization.DecisionWellFormed(bound.decision)
  {
  }

  lemma INV_SPOOL_CROSS_REQUEST_AUTHORIZATION_REPLAY_BLOCKED(ctx: SpoolAccessContext, spool: SpoolEntry, operation: Operation, decision: SecurityDecision)
    requires decision.context.correlation_id != ctx.correlation_id
    ensures !IsBoundSpoolDecision(ctx, spool, operation, decision)
  {
  }

  lemma INV_SPOOL_STALE_GENERATION_REPLAY_BLOCKED(ctx: SpoolAccessContext, spool: SpoolEntry, operation: Operation, decision: SecurityDecision)
    requires decision.object_ref.object_id == spool.spool_id
    requires decision.object_ref.generation != decision.context.object_generation
    ensures !IsBoundSpoolDecision(ctx, spool, operation, decision)
  {
  }

  lemma INV_SPOOL_OWNER_BROWSE_ALLOWED(bound: BoundSpoolDecision, records: seq<AuditRecord>)
    requires BoundSpoolDecisionValid(bound)
    requires bound.operation == OP_QUERY
    requires bound.context.subject == bound.spool.owner
    requires ValidSpoolAllowDecision(bound.decision)
    requires Audit.RequiredAuditSatisfiedForFinalResult(bound.decision, records)
    ensures SpoolBrowseAllowed(bound.spool, bound.decision)
    ensures SpoolBrowseCanReturnContent(bound, records)
  {
  }

  lemma INV_SPOOL_BROWSE_BY_NON_OWNER_DENIED(spool: SpoolEntry, decision: SecurityDecision)
    requires decision.subject != spool.owner
    ensures !SpoolBrowseAllowed(spool, decision)
  {
  }

  lemma INV_SPOOL_BROWSE_BY_NON_OWNER_RETURNS_NO_CONTENT(bound: BoundSpoolDecision, records: seq<AuditRecord>)
    requires bound.context.subject != bound.spool.owner
    requires !ValidSpoolAllowDecision(bound.decision)
    ensures !SpoolBrowseCanReturnContent(bound, records)
  {
  }

  lemma INV_SPOOL_BROWSE_WITHOUT_AUTHORITY_DENIED(spool: SpoolEntry, decision: SecurityDecision)
    requires !Authorization.DecisionAllowsProtectedEffect(decision)
    ensures !SpoolBrowseAllowed(spool, decision)
  {
  }

  lemma INV_SPOOL_BROWSE_CANNOT_BYPASS_AUTHORIZATION(bound: BoundSpoolDecision, records: seq<AuditRecord>)
    requires !Authorization.DecisionAllowsProtectedEffect(bound.decision)
    ensures !SpoolBrowseCanReturnContent(bound, records)
  {
  }

  lemma INV_SPOOL_PURGE_WITHOUT_AUTHORITY_DENIED(decision: SecurityDecision)
    requires decision.resource_class == RESOURCE_SPOOL
    requires decision.operation == OP_PURGE
    requires !Authorization.DecisionAllowsProtectedEffect(decision)
    ensures SpoolPurgeDeniedWithoutAuthority(decision)
  {
  }

  lemma INV_SPOOL_PURGE_REQUIRES_AUTHORITY_AND_RETENTION(bound: BoundSpoolDecision, records: seq<AuditRecord>)
    requires bound.operation == OP_PURGE
    requires !ValidSpoolAllowDecision(bound.decision) || bound.spool.retained
    ensures !SpoolPurgeCanRemoveContent(bound, records)
  {
  }

  lemma INV_SPOOL_EXPORT_REQUIRES_AUTHORITY_AND_AUDIT(bound: BoundSpoolDecision, records: seq<AuditRecord>)
    requires bound.operation == OP_EXPORT
    requires !ValidSpoolAllowDecision(bound.decision) || !Authorization.RequiresAudit(bound.decision) || !Audit.RequiredAuditSatisfiedForFinalResult(bound.decision, records)
    ensures !SpoolExportCanComplete(bound, records)
  {
  }

  lemma INV_SPOOL_EXPORT_WITHOUT_AUDIT_DENIED(bound: BoundSpoolDecision, records: seq<AuditRecord>)
    requires bound.operation == OP_EXPORT
    requires !Authorization.RequiresAudit(bound.decision) || !Audit.RequiredAuditSatisfiedForFinalResult(bound.decision, records)
    ensures !SpoolExportCanComplete(bound, records)
  {
  }

  lemma INV_SPOOL_EXPORT_AUDIT_UNAVAILABLE_FAILS_CLOSED(bound: BoundSpoolDecision, prior_records: seq<AuditRecord>, next_record_id: MfosId)
    requires BoundSpoolDecisionValid(bound)
    requires bound.operation == OP_EXPORT
    requires ValidSpoolAllowDecision(bound.decision)
    requires Authorization.RequiresAudit(bound.decision)
    requires ValidId(next_record_id)
    ensures ExportSpoolAccess(bound, prior_records, next_record_id, false).error_code == MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE
    ensures !ExportSpoolAccess(bound, prior_records, next_record_id, false).result_released
    ensures !ExportSpoolAccess(bound, prior_records, next_record_id, false).export_completed
    ensures !IsSuccessError(ExportSpoolAccess(bound, prior_records, next_record_id, false).error_code)
  {
    Audit.INV_AUDIT_REQUIRED_TRANSITION_FAILS_CLOSED_WHEN_UNAVAILABLE(bound.decision, prior_records, next_record_id);
  }

  lemma INV_SPOOL_DENY_PRODUCES_NO_SUCCESSFUL_ACCESS(bound: BoundSpoolDecision, records: seq<AuditRecord>)
    requires bound.decision.result == DENY
    ensures !SpoolBrowseCanReturnContent(bound, records)
    ensures !SpoolPurgeCanRemoveContent(bound, records)
    ensures !SpoolExportCanComplete(bound, records)
  {
  }

  lemma INV_SPOOL_DENY_WITH_AUDIT_LINKS_BEFORE_RETURN(bound: BoundSpoolDecision, prior_records: seq<AuditRecord>, next_record_id: MfosId)
    requires BoundSpoolDecisionDeniesWithAudit(bound)
    requires ValidId(next_record_id)
    ensures DeniedSpoolAccessWithAudit(bound, prior_records, next_record_id, true).error_code == bound.decision.error_code
    ensures DeniedSpoolAccessWithAudit(bound, prior_records, next_record_id, true).result_released
    ensures Audit.RequiredAuditSatisfiedForFinalResult(bound.decision, DeniedSpoolAccessWithAudit(bound, prior_records, next_record_id, true).audit_records)
    ensures !DeniedSpoolAccessWithAudit(bound, prior_records, next_record_id, true).content_released
    ensures !DeniedSpoolAccessWithAudit(bound, prior_records, next_record_id, true).purge_completed
    ensures !DeniedSpoolAccessWithAudit(bound, prior_records, next_record_id, true).export_completed
  {
    Audit.INV_AUDIT_DENY_TRANSITION_WRITES_BEFORE_RETURN(bound.decision, prior_records, next_record_id);
  }

  lemma INV_SPOOL_DENY_AUDIT_UNAVAILABLE_FAILS_CLOSED(bound: BoundSpoolDecision, prior_records: seq<AuditRecord>, next_record_id: MfosId)
    requires BoundSpoolDecisionDeniesWithAudit(bound)
    requires ValidId(next_record_id)
    ensures DeniedSpoolAccessWithAudit(bound, prior_records, next_record_id, false).error_code == MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE
    ensures !DeniedSpoolAccessWithAudit(bound, prior_records, next_record_id, false).result_released
    ensures !DeniedSpoolAccessWithAudit(bound, prior_records, next_record_id, false).content_released
    ensures !DeniedSpoolAccessWithAudit(bound, prior_records, next_record_id, false).purge_completed
    ensures !DeniedSpoolAccessWithAudit(bound, prior_records, next_record_id, false).export_completed
    ensures !IsSuccessError(DeniedSpoolAccessWithAudit(bound, prior_records, next_record_id, false).error_code)
  {
    Audit.INV_AUDIT_DENY_TRANSITION_FAILS_CLOSED_WHEN_UNAVAILABLE(bound.decision, prior_records, next_record_id);
  }

  lemma INV_SPOOL_EVIDENCE_NOT_AUDIT_EVIDENCE(evidence: SpoolEvidence, record: AuditRecord, bound: BoundSpoolDecision, prior_records: seq<AuditRecord>)
    requires BoundSpoolDecisionValid(bound)
    requires bound.operation == OP_EXPORT
    requires ValidSpoolAllowDecision(bound.decision)
    requires Authorization.RequiresAudit(bound.decision)
    ensures !SpoolEvidenceIsAuditEvidence(evidence, record)
    ensures RejectInvalidSpoolAuditEvidence(bound, prior_records).error_code == MFOS_ERR_INVALID_AUDIT_RECORD
    ensures !RejectInvalidSpoolAuditEvidence(bound, prior_records).result_released
    ensures !RejectInvalidSpoolAuditEvidence(bound, prior_records).content_released
    ensures !RejectInvalidSpoolAuditEvidence(bound, prior_records).purge_completed
    ensures !RejectInvalidSpoolAuditEvidence(bound, prior_records).export_completed
    ensures !IsSuccessError(RejectInvalidSpoolAuditEvidence(bound, prior_records).error_code)
  {
  }

  lemma INV_SPOOL_ENTRY_NOT_AUDIT_EVIDENCE(spool: SpoolEntry, record: AuditRecord)
    ensures !Audit.SpoolEntryIsAuditEvidence(spool, record)
  {
    Audit.INV_AUDIT_SPOOL_NOT_EVIDENCE(spool, record);
  }

  lemma INV_SPOOL_DIAGNOSTIC_LOG_LINE_NOT_AUDIT_EVIDENCE(record: AuditRecord)
    ensures !Audit.DiagnosticLogLineIsAuditRecord(true, record)
  {
    Audit.INV_AUDIT_LOG_LINE_NOT_RECORD(record);
  }

  lemma INV_SPOOL_SPEC_GAP_NOT_SUCCESS(decision: SecurityDecision, prior_records: seq<AuditRecord>, next_record_id: MfosId)
    requires decision.result == SPEC_GAP
    requires decision.error_code == MFOS_ERR_SPEC_GAP
    requires Authorization.RequiresAudit(decision)
    requires ValidCorrelationId(decision.context.correlation_id)
    requires ValidId(decision.subject.principal.principal_id)
    requires ValidId(decision.object_ref.object_id)
    requires ValidPolicyVersion(decision.policy_version)
    requires ValidId(next_record_id)
    ensures !ValidSpoolAllowDecision(decision)
    ensures !IsSuccessError(decision.error_code)
    ensures Audit.FinalizeRequiredAuditedOperation(decision, prior_records, next_record_id, true).final_error == MFOS_ERR_SPEC_GAP
    ensures Audit.FinalizeRequiredAuditedOperation(decision, prior_records, next_record_id, true).result_released
    ensures Audit.RequiredAuditSatisfiedForFinalResult(decision, Audit.FinalizeRequiredAuditedOperation(decision, prior_records, next_record_id, true).records_after)
  {
    Audit.INV_AUDIT_REQUIRED_TRANSITION_WRITES_BEFORE_RETURN_WHEN_AVAILABLE(decision, prior_records, next_record_id);
  }

  lemma INV_SPOOL_UNSUPPORTED_NOT_SUCCESS(decision: SecurityDecision, prior_records: seq<AuditRecord>, next_record_id: MfosId)
    requires decision.result == UNSUPPORTED
    requires decision.error_code == MFOS_ERR_UNSUPPORTED
    requires Authorization.RequiresAudit(decision)
    requires ValidCorrelationId(decision.context.correlation_id)
    requires ValidId(decision.subject.principal.principal_id)
    requires ValidId(decision.object_ref.object_id)
    requires ValidPolicyVersion(decision.policy_version)
    requires ValidId(next_record_id)
    ensures !ValidSpoolAllowDecision(decision)
    ensures !IsSuccessError(decision.error_code)
    ensures Audit.FinalizeRequiredAuditedOperation(decision, prior_records, next_record_id, true).final_error == MFOS_ERR_UNSUPPORTED
    ensures Audit.FinalizeRequiredAuditedOperation(decision, prior_records, next_record_id, true).result_released
    ensures Audit.RequiredAuditSatisfiedForFinalResult(decision, Audit.FinalizeRequiredAuditedOperation(decision, prior_records, next_record_id, true).records_after)
  {
    Audit.INV_AUDIT_REQUIRED_TRANSITION_WRITES_BEFORE_RETURN_WHEN_AVAILABLE(decision, prior_records, next_record_id);
  }

  lemma INV_JOB_INVALID_LIFECYCLE_REJECTED(from_state: JobState, to_state: JobState)
    requires !ValidJobTransition(from_state, to_state)
    ensures !ValidJobTransition(from_state, to_state)
    ensures TransitionJobState(from_state, to_state).accepted == false
    ensures TransitionJobState(from_state, to_state).error_code == MFOS_ERR_INVALID_STATE
    ensures TransitionJobState(from_state, to_state).reason_code == INVALID_LIFECYCLE_TRANSITION
  {
  }

  lemma INV_JOB_VALID_SUBMIT_REACHES_READY()
    ensures ValidJobTransition(JOB_SUBMITTED, JOB_VALIDATED)
    ensures ValidJobTransition(JOB_VALIDATED, JOB_READY)
    ensures TransitionJobState(JOB_SUBMITTED, JOB_VALIDATED).accepted
    ensures TransitionJobState(JOB_VALIDATED, JOB_READY).accepted
    ensures TransitionJobState(JOB_VALIDATED, JOB_READY).next_state == JOB_READY
  {
  }

  lemma INV_JOB_CANNOT_EXECUTE_BEFORE_VALIDATION(ctx: JobContext)
    requires ctx.job.state == JOB_DEFINED || ctx.job.state == JOB_SUBMITTED
    ensures !JobCanStartExecution(ctx)
    ensures !ValidJobTransition(ctx.job.state, JOB_EXECUTING)
    ensures !ValidJobTransition(ctx.job.state, JOB_RUNNING)
  {
  }

  lemma INV_JOB_STEP_CANNOT_RUN_BEFORE_EFFECTIVE_PRINCIPAL(ctx: JobContext, step: JobStep)
    requires !JobContextHasEffectivePrincipal(ctx)
    ensures !JobStepCanRun(ctx, step)
  {
  }

  lemma INV_JOB_COMPLETION_REQUIRES_TERMINAL_STEPS(job: Job)
    requires !AllStepsTerminal(job.steps)
    ensures !JobCanComplete(job)
  {
  }

  lemma INV_JOB_FAILED_CANNOT_COMPLETE_WITHOUT_RECOVERY()
    ensures !ValidJobTransition(JOB_FAILED, JOB_COMPLETE)
  {
  }

  lemma INV_JOB_CANCELLED_CANNOT_EXECUTE_FURTHER()
    ensures !ValidJobTransition(JOB_CANCELLED, JOB_EXECUTING)
    ensures !ValidJobTransition(JOB_CANCELLED, JOB_RUNNING)
  {
  }

  lemma INV_JOB_RETURN_CODE_DETERMINISTIC(reason: JobFailureReason, error: ErrorCode)
    ensures JobFailurePlaceholder(reason, error).return_code == FailureReturnCode(reason)
    ensures JobFailurePlaceholder(reason, error) == JobFailurePlaceholder(reason, error)
  {
  }

  lemma INV_JOB_FAILURE_REASON_EXPLICIT(reason: JobFailureReason, error: ErrorCode)
    requires reason != JOB_FAILURE_NONE
    ensures JobFailurePlaceholder(reason, error).failure_reason == reason
    ensures JobFailurePlaceholder(reason, error).final_state == JOB_FAILED
  {
  }

  lemma INV_JOB_SPEC_GAP_NOT_SUCCESS()
    ensures !IsSuccessError(MFOS_ERR_SPEC_GAP)
  {
    SpecGapIsFailClosed();
  }

  lemma INV_JOB_UNSUPPORTED_NOT_SUCCESS()
    ensures !IsSuccessError(MFOS_ERR_UNSUPPORTED)
  {
    UnsupportedIsFailClosed();
  }
}
