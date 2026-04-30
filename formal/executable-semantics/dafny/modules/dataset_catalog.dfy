// MFOS Phase 1 Dafny executable semantics: dataset/catalog model.
// This is not datasetd, catalogd, storage, or POSIX behavior.

include "common.dfy"
include "errors.dfy"
include "types.dfy"
include "authorization.dfy"
include "audit.dfy"

module DatasetCatalog {
  import opened Common
  import opened Errors
  import opened Types
  import Authorization
  import Audit

  datatype DatasetOpenOutcome = DatasetOpenOutcome(
    handle: Option<DatasetHandle>,
    error_code: ErrorCode,
    decision: SecurityDecision,
    audit_records: seq<AuditRecord>,
    result_released: bool
  )

  predicate SymbolicDsnValid(dataset: Dataset) {
    ValidId(dataset.name_id) &&
    dataset.dataset_name.name_id == dataset.name_id &&
    dataset.dataset_name.canonical &&
    !dataset.dataset_name.posix_path_like
  }

  predicate DatasetNameIsMfosDsn(name: DatasetName) {
    ValidId(name.name_id) &&
    name.canonical &&
    !name.posix_path_like
  }

  function ValidateDatasetName(name: DatasetName): Result<DatasetName> {
    if DatasetNameIsMfosDsn(name) then ResultOk(name)
    else ResultErr(ErrorRank(MFOS_ERR_INVALID_DSN))
  }

  predicate CatalogTransactionCanExposeCommittedEntry(state: CatalogTransactionState) {
    state == CATALOG_TX_COMPLETE
  }

  predicate SystemDatasetInvariant(entry: CatalogEntry) {
    entry.dataset.system_marker.system_dataset ==> entry.dataset.system_marker.immutable
  }

  predicate CatalogEntryResolvable(entry: CatalogEntry) {
    entry.state == CATALOG_COMMITTED &&
    CatalogTransactionCanExposeCommittedEntry(entry.transaction_state) &&
    entry.integrity_valid &&
    entry.integrity_tag.verified &&
    ValidId(entry.integrity_tag.tag_id) &&
    ValidGeneration(entry.catalog_generation) &&
    ValidGeneration(entry.dataset_generation) &&
    entry.dataset.object_ref.generation == entry.dataset_generation &&
    SystemDatasetInvariant(entry) &&
    SymbolicDsnValid(entry.dataset)
  }

  function CatalogResolutionError(entry: CatalogEntry): ErrorCode {
    if entry.state == CATALOG_INTEGRITY_FAILED ||
       entry.state == CATALOG_PARTIAL_JOURNAL ||
       entry.transaction_state == CATALOG_TX_COMMITTED ||
       entry.transaction_state == CATALOG_TX_PARTIAL_JOURNAL ||
       entry.transaction_state == CATALOG_TX_INTEGRITY_FAILED ||
       !SystemDatasetInvariant(entry) ||
       !entry.integrity_valid ||
       !entry.integrity_tag.verified then MFOS_ERR_INTERNAL_CORRUPTION
    else MFOS_ERR_CATALOG_NOT_FOUND
  }

  function ResolveCatalog(entry: CatalogEntry): Result<CatalogEntry> {
    if CatalogEntryResolvable(entry) then ResultOk(entry)
    else ResultErr(ErrorRank(CatalogResolutionError(entry)))
  }

  function RecoverCatalogCandidate(entry: CatalogEntry): Result<CatalogEntry> {
    ResolveCatalog(entry)
  }

  function PolicyBindingFromDecision(decision: SecurityDecision): PolicyBinding {
    PolicyBinding(decision.subject, decision.object_ref, decision.operation, decision.resource_class,
      decision.policy_version, decision.result, decision.reason_code, decision.obligations)
  }

  function MakeObjectGenerationBinding(entry: CatalogEntry, decision: SecurityDecision): ObjectGenerationBinding {
    ObjectGenerationBinding(entry.dataset.object_ref, decision.policy_version,
      entry.catalog_generation, entry.dataset_generation, entry.integrity_tag)
  }

  predicate ObjectGenerationBindingMatchesEntry(binding: ObjectGenerationBinding, entry: CatalogEntry, decision: SecurityDecision) {
    binding.object_ref == entry.dataset.object_ref &&
    binding.policy_version == decision.policy_version &&
    binding.catalog_generation == entry.catalog_generation &&
    binding.dataset_generation == entry.dataset_generation &&
    binding.integrity_tag == entry.integrity_tag
  }

  function MakeDatasetHandle(entry: CatalogEntry, decision: SecurityDecision, handle_id: MfosId): DatasetHandle {
    DatasetHandle(handle_id, decision.subject, entry.dataset.object_ref, decision.operation,
      decision.policy_version, entry.catalog_generation, entry.dataset_generation,
      PolicyBindingFromDecision(decision), MakeObjectGenerationBinding(entry, decision), true)
  }

  predicate MayCreateDatasetHandle(entry: CatalogEntry, decision: SecurityDecision, satisfied: set<DecisionObligation>) {
    CatalogEntryResolvable(entry) &&
    decision.object_ref == entry.dataset.object_ref &&
    decision.context.object_generation == entry.catalog_generation &&
    decision.resource_class == RESOURCE_DATASET &&
    Authorization.CanCreateProtectedResourceHandle(decision, satisfied)
  }

  function DatasetOpenFailureError(entry: CatalogEntry, decision: SecurityDecision): ErrorCode {
    if !CatalogEntryResolvable(entry) then CatalogResolutionError(entry)
    else if decision.error_code != MFOS_OK then decision.error_code
    else if decision.result == DENY then MFOS_ERR_POLICY_DENIED
    else MFOS_ERR_UNAUTHORIZED
  }

  function CreateDatasetHandle(entry: CatalogEntry, decision: SecurityDecision, satisfied: set<DecisionObligation>, handle_id: MfosId): Result<DatasetHandle> {
    if MayCreateDatasetHandle(entry, decision, satisfied) then ResultOk(MakeDatasetHandle(entry, decision, handle_id))
    else ResultErr(ErrorRank(DatasetOpenFailureError(entry, decision)))
  }

  function ValidateDatasetHandle(handle: DatasetHandle, active_policy: PolicyVersion, entry: CatalogEntry): Result<DatasetHandle> {
    if HandleFresh(handle, active_policy, entry) then ResultOk(handle)
    else if handle.policy_version != active_policy then ResultErr(ErrorRank(MFOS_ERR_POLICY_VERSION_MISMATCH))
    else ResultErr(ErrorRank(MFOS_ERR_STALE_HANDLE))
  }

  function DeniedDatasetOpenWithAudit(decision: SecurityDecision, prior_records: seq<AuditRecord>, next_record_id: MfosId, audit_available: bool): DatasetOpenOutcome
    requires decision.result == DENY
    requires !IsSuccessError(decision.error_code)
    requires Authorization.RequiresAudit(decision)
    requires ValidCorrelationId(decision.context.correlation_id)
    requires ValidId(next_record_id)
  {
    var finalization := Audit.FinalizeDeniedOperation(decision, prior_records, next_record_id, audit_available);
    DatasetOpenOutcome(None, finalization.final_error, decision, finalization.records_after, finalization.result_released)
  }

  predicate HandleBoundToObjectGeneration(handle: DatasetHandle, entry: CatalogEntry, decision: SecurityDecision) {
    handle.active &&
    handle.subject == decision.subject &&
    handle.object_ref == entry.dataset.object_ref &&
    handle.operation == decision.operation &&
    handle.policy_version == decision.policy_version &&
    handle.catalog_generation == entry.catalog_generation &&
    handle.dataset_generation == entry.dataset_generation &&
    handle.policy_binding == PolicyBindingFromDecision(decision) &&
    ObjectGenerationBindingMatchesEntry(handle.object_generation_binding, entry, decision)
  }

  predicate HandleFresh(handle: DatasetHandle, active_policy: PolicyVersion, entry: CatalogEntry) {
    handle.active &&
    handle.policy_version == active_policy &&
    handle.catalog_generation == entry.catalog_generation &&
    handle.dataset_generation == entry.dataset_generation &&
    handle.object_generation_binding.catalog_generation == entry.catalog_generation &&
    handle.object_generation_binding.dataset_generation == entry.dataset_generation &&
    handle.object_generation_binding.policy_version == active_policy &&
    handle.object_generation_binding.object_ref == entry.dataset.object_ref &&
    handle.object_generation_binding.integrity_tag == entry.integrity_tag
  }

  predicate RetentionBlocksDelete(entry: CatalogEntry, operation: Operation) {
    (entry.dataset.retention_active || entry.dataset.retention_policy.active) &&
    (operation == OP_DELETE || operation == OP_PURGE)
  }

  predicate ImmutableSystemDatasetBlocksModify(entry: CatalogEntry, operation: Operation) {
    (entry.dataset.immutable_system || entry.dataset.system_marker.system_dataset) &&
    (operation == OP_WRITE || operation == OP_DELETE || operation == OP_PURGE)
  }

  function DatasetDeleteOrModify(entry: CatalogEntry, decision: SecurityDecision): Result<CatalogEntry> {
    if !SystemDatasetInvariant(entry) then ResultErr(ErrorRank(MFOS_ERR_INVALID_STATE))
    else if ImmutableSystemDatasetBlocksModify(entry, decision.operation) then ResultErr(ErrorRank(MFOS_ERR_IMMUTABLE))
    else if RetentionBlocksDelete(entry, decision.operation) then ResultErr(ErrorRank(MFOS_ERR_RETENTION_DENIED))
    else if !Authorization.DecisionAllowsProtectedEffect(decision) then ResultErr(ErrorRank(DatasetOpenFailureError(entry, decision)))
    else ResultOk(entry)
  }

  function TreatDatasetAsPosixFile(dataset: Dataset): Result<Dataset> {
    ResultErr(ErrorRank(MFOS_ERR_UNSUPPORTED))
  }

  lemma INV_DATASET_VALID_DSN_ACCEPTED(name: DatasetName)
    requires DatasetNameIsMfosDsn(name)
    ensures ValidateDatasetName(name).ResultOk?
  {
  }

  lemma INV_DATASET_MALFORMED_DSN_REJECTED(name: DatasetName)
    requires !DatasetNameIsMfosDsn(name)
    ensures ValidateDatasetName(name).ResultErr?
    ensures !IsSuccessError(MFOS_ERR_INVALID_DSN)
  {
  }

  lemma INV_CATALOG_COMMITTED_ONLY(entry: CatalogEntry)
    requires entry.state != CATALOG_COMMITTED ||
             !entry.integrity_valid ||
             !entry.integrity_tag.verified ||
             !SystemDatasetInvariant(entry) ||
             !CatalogTransactionCanExposeCommittedEntry(entry.transaction_state)
    ensures !CatalogEntryResolvable(entry)
  {
  }

  lemma INV_CATALOG_RESOLVE_SUCCESS_IMPLIES_COMMITTED(entry: CatalogEntry)
    requires ResolveCatalog(entry).ResultOk?
    ensures CatalogEntryResolvable(entry)
    ensures entry.state == CATALOG_COMMITTED
    ensures entry.integrity_valid
    ensures entry.integrity_tag.verified
    ensures SystemDatasetInvariant(entry)
    ensures CatalogTransactionCanExposeCommittedEntry(entry.transaction_state)
    ensures entry.transaction_state == CATALOG_TX_COMPLETE
  {
  }

  lemma INV_CATALOG_COMMITTED_ENTRY_RESOLVES(entry: CatalogEntry)
    requires CatalogEntryResolvable(entry)
    ensures ResolveCatalog(entry).ResultOk?
    ensures ResolveCatalog(entry).value == entry
  {
  }

  lemma INV_CATALOG_RESOLUTION_FAILURE_NOT_SUCCESS(entry: CatalogEntry)
    requires !CatalogEntryResolvable(entry)
    ensures ResolveCatalog(entry).ResultErr?
  {
  }

  lemma INV_CATALOG_UNCOMMITTED_CANNOT_RESOLVE(entry: CatalogEntry)
    requires entry.state == CATALOG_UNCOMMITTED || entry.state == CATALOG_STAGED
    ensures !CatalogEntryResolvable(entry)
    ensures ResolveCatalog(entry).ResultErr?
  {
  }

  lemma INV_CATALOG_ROLLED_BACK_CANNOT_RESOLVE(entry: CatalogEntry)
    requires entry.state == CATALOG_ROLLED_BACK
    ensures !CatalogEntryResolvable(entry)
    ensures ResolveCatalog(entry).ResultErr?
  {
  }

  lemma INV_CATALOG_MISSING_DELETED_RETIRED_CANNOT_RESOLVE(entry: CatalogEntry)
    requires entry.state == CATALOG_MISSING || entry.state == CATALOG_DELETED || entry.state == CATALOG_RETIRED
    ensures !CatalogEntryResolvable(entry)
    ensures ResolveCatalog(entry).ResultErr?
  {
  }

  lemma INV_CATALOG_INTEGRITY_FAILED_CANNOT_RESOLVE(entry: CatalogEntry)
    requires entry.state == CATALOG_INTEGRITY_FAILED || !entry.integrity_valid || !entry.integrity_tag.verified
    ensures !CatalogEntryResolvable(entry)
    ensures ResolveCatalog(entry).ResultErr?
    ensures CatalogResolutionError(entry) == MFOS_ERR_INTERNAL_CORRUPTION
  {
  }

  lemma INV_CATALOG_PARTIAL_JOURNAL_CANNOT_RESOLVE(entry: CatalogEntry)
    requires entry.state == CATALOG_PARTIAL_JOURNAL
    ensures !CatalogEntryResolvable(entry)
    ensures ResolveCatalog(entry).ResultErr?
    ensures CatalogResolutionError(entry) == MFOS_ERR_INTERNAL_CORRUPTION
  {
  }

  lemma INV_CATALOG_TX_PARTIAL_JOURNAL_CANNOT_RESOLVE(entry: CatalogEntry)
    requires entry.transaction_state == CATALOG_TX_PARTIAL_JOURNAL
    ensures !CatalogEntryResolvable(entry)
    ensures ResolveCatalog(entry).ResultErr?
    ensures CatalogResolutionError(entry) == MFOS_ERR_INTERNAL_CORRUPTION
  {
  }

  lemma INV_CATALOG_TX_ROLLBACK_REQUIRED_CANNOT_RESOLVE(entry: CatalogEntry)
    requires entry.transaction_state == CATALOG_TX_ROLLBACK_REQUIRED
    ensures !CatalogEntryResolvable(entry)
    ensures ResolveCatalog(entry).ResultErr?
  {
  }

  lemma INV_CATALOG_TX_COMMITTED_NOT_COMPLETE_CANNOT_RESOLVE(entry: CatalogEntry)
    requires entry.transaction_state == CATALOG_TX_COMMITTED
    ensures !CatalogEntryResolvable(entry)
    ensures ResolveCatalog(entry).ResultErr?
    ensures CatalogResolutionError(entry) == MFOS_ERR_INTERNAL_CORRUPTION
  {
  }

  lemma INV_CATALOG_CRASH_MID_COMMIT_PARTIAL_STATE_CANNOT_RESOLVE(entry: CatalogEntry)
    requires entry.transaction_state == CATALOG_TX_PARTIAL_JOURNAL ||
             entry.transaction_state == CATALOG_TX_ROLLBACK_REQUIRED ||
             entry.transaction_state == CATALOG_TX_COMMITTED ||
             entry.state == CATALOG_PARTIAL_JOURNAL ||
             entry.state == CATALOG_ROLLED_BACK ||
             entry.state == CATALOG_UNCOMMITTED
    ensures RecoverCatalogCandidate(entry).ResultErr?
    ensures !CatalogEntryResolvable(entry)
  {
  }

  lemma INV_CATALOG_CRASH_RECOVERY_COMPLETENESS_NOT_MODELED()
    ensures !IsSuccessError(MFOS_ERR_SPEC_GAP)
  {
    SpecGapIsFailClosed();
  }

  lemma INV_DATASET_NO_HANDLE_WITHOUT_ALLOW(entry: CatalogEntry, decision: SecurityDecision, satisfied: set<DecisionObligation>)
    requires !Authorization.DecisionAllowsProtectedEffect(decision)
    ensures !MayCreateDatasetHandle(entry, decision, satisfied)
    ensures CreateDatasetHandle(entry, decision, satisfied, 1).ResultErr?
  {
  }

  lemma INV_DATASET_HANDLE_BOUND_ON_CREATE(entry: CatalogEntry, decision: SecurityDecision, satisfied: set<DecisionObligation>, handle: DatasetHandle)
    requires MayCreateDatasetHandle(entry, decision, satisfied)
    requires HandleBoundToObjectGeneration(handle, entry, decision)
    ensures handle.active
    ensures handle.subject == decision.subject
    ensures handle.object_ref == entry.dataset.object_ref
    ensures handle.operation == decision.operation
    ensures handle.policy_version == decision.policy_version
    ensures handle.catalog_generation == entry.catalog_generation
    ensures handle.dataset_generation == entry.dataset_generation
    ensures handle.policy_binding == PolicyBindingFromDecision(decision)
    ensures ObjectGenerationBindingMatchesEntry(handle.object_generation_binding, entry, decision)
    ensures handle.object_generation_binding.catalog_generation == entry.catalog_generation
    ensures handle.object_generation_binding.dataset_generation == entry.dataset_generation
    ensures handle.object_generation_binding.policy_version == decision.policy_version
  {
  }

  lemma INV_DATASET_CREATE_HANDLE_BINDS_DECISION(entry: CatalogEntry, decision: SecurityDecision, satisfied: set<DecisionObligation>, handle_id: MfosId)
    requires MayCreateDatasetHandle(entry, decision, satisfied)
    ensures CreateDatasetHandle(entry, decision, satisfied, handle_id).ResultOk?
    ensures HandleBoundToObjectGeneration(MakeDatasetHandle(entry, decision, handle_id), entry, decision)
    ensures MakeDatasetHandle(entry, decision, handle_id).subject == decision.subject
    ensures MakeDatasetHandle(entry, decision, handle_id).operation == decision.operation
    ensures MakeDatasetHandle(entry, decision, handle_id).policy_version == decision.policy_version
    ensures MakeDatasetHandle(entry, decision, handle_id).catalog_generation == entry.catalog_generation
    ensures MakeDatasetHandle(entry, decision, handle_id).dataset_generation == entry.dataset_generation
  {
  }

  lemma INV_DATASET_OPEN_REQUIRES_SECURITY_DECISION(entry: CatalogEntry, decision: SecurityDecision, satisfied: set<DecisionObligation>)
    requires MayCreateDatasetHandle(entry, decision, satisfied)
    ensures Authorization.DecisionAllowsProtectedEffect(decision)
    ensures Authorization.DecisionWellFormed(decision)
    ensures decision.resource_class == RESOURCE_DATASET
  {
  }

  lemma INV_DATASET_OPEN_SUCCESS_REQUIRES_ALLOW_OR_ALLOW_WITH_AUDIT(entry: CatalogEntry, decision: SecurityDecision, satisfied: set<DecisionObligation>, handle_id: MfosId)
    requires CreateDatasetHandle(entry, decision, satisfied, handle_id).ResultOk?
    ensures decision.result == ALLOW || decision.result == ALLOW_WITH_AUDIT
    ensures Authorization.DecisionAllowsProtectedEffect(decision)
  {
  }

  lemma INV_DATASET_HANDLE_CREATION_CANNOT_BYPASS_AUTHORIZATION(entry: CatalogEntry, decision: SecurityDecision, satisfied: set<DecisionObligation>, handle_id: MfosId)
    requires CreateDatasetHandle(entry, decision, satisfied, handle_id).ResultOk?
    ensures Authorization.CanCreateProtectedResourceHandle(decision, satisfied)
    ensures Authorization.DecisionAllowsProtectedEffect(decision)
  {
  }

  lemma INV_DATASET_ALLOW_WITH_AUDIT_REQUIRES_SATISFIED_OBLIGATION(entry: CatalogEntry, decision: SecurityDecision, satisfied: set<DecisionObligation>)
    requires decision.result == ALLOW_WITH_AUDIT
    requires OBLIGATION_AUDIT in decision.obligations
    requires OBLIGATION_AUDIT !in satisfied
    ensures !MayCreateDatasetHandle(entry, decision, satisfied)
  {
  }

  lemma INV_DATASET_OPEN_DENY_PRODUCES_NO_HANDLE(entry: CatalogEntry, decision: SecurityDecision, satisfied: set<DecisionObligation>, handle_id: MfosId)
    requires decision.result == DENY
    ensures !MayCreateDatasetHandle(entry, decision, satisfied)
    ensures CreateDatasetHandle(entry, decision, satisfied, handle_id).ResultErr?
  {
  }

  lemma INV_DATASET_OPEN_DENY_USES_POLICY_DENIED(entry: CatalogEntry, binding: PolicyBinding, context: DecisionContext, satisfied: set<DecisionObligation>, handle_id: MfosId)
    requires CatalogEntryResolvable(entry)
    requires binding.subject.authenticated
    requires ValidId(binding.subject.principal.principal_id)
    requires ValidId(binding.object_ref.object_id)
    requires ValidPolicyVersion(binding.policy_version)
    requires ValidCorrelationId(context.correlation_id)
    requires binding.object_ref == entry.dataset.object_ref
    requires binding.operation == OP_READ
    requires binding.resource_class == RESOURCE_DATASET
    requires binding.result == DENY
    requires binding.reason_code == DATASET_READ_NOT_PERMITTED
    requires binding.policy_version == context.policy_version
    ensures DatasetOpenFailureError(entry, Authorization.EvaluateSecurityDecision(binding, context)) == MFOS_ERR_POLICY_DENIED
    ensures CreateDatasetHandle(entry, Authorization.EvaluateSecurityDecision(binding, context), satisfied, handle_id).ResultErr?
  {
  }

  lemma INV_DATASET_STALE_HANDLE_REJECTED(handle: DatasetHandle, active_policy: PolicyVersion, entry: CatalogEntry)
    requires handle.policy_version != active_policy ||
             handle.catalog_generation != entry.catalog_generation ||
             handle.dataset_generation != entry.dataset_generation ||
             !handle.active
    ensures !HandleFresh(handle, active_policy, entry)
  {
  }

  lemma INV_DATASET_STALE_HANDLE_AFTER_POLICY_CHANGE_REJECTED(handle: DatasetHandle, active_policy: PolicyVersion, entry: CatalogEntry)
    requires handle.policy_version != active_policy
    ensures !HandleFresh(handle, active_policy, entry)
    ensures ValidateDatasetHandle(handle, active_policy, entry).ResultErr?
  {
  }

  lemma INV_DATASET_STALE_HANDLE_AFTER_GENERATION_CHANGE_REJECTED(handle: DatasetHandle, active_policy: PolicyVersion, entry: CatalogEntry)
    requires handle.catalog_generation != entry.catalog_generation ||
             handle.dataset_generation != entry.dataset_generation
    ensures !HandleFresh(handle, active_policy, entry)
    ensures ValidateDatasetHandle(handle, active_policy, entry).ResultErr?
  {
  }

  lemma INV_DATASET_STALE_HANDLE_AFTER_CATALOG_GENERATION_CHANGE_REJECTED(handle: DatasetHandle, active_policy: PolicyVersion, entry: CatalogEntry)
    requires handle.catalog_generation != entry.catalog_generation
    ensures !HandleFresh(handle, active_policy, entry)
    ensures ValidateDatasetHandle(handle, active_policy, entry).ResultErr?
  {
  }

  lemma INV_DATASET_STALE_HANDLE_AFTER_DATASET_GENERATION_CHANGE_REJECTED(handle: DatasetHandle, active_policy: PolicyVersion, entry: CatalogEntry)
    requires handle.dataset_generation != entry.dataset_generation
    ensures !HandleFresh(handle, active_policy, entry)
    ensures ValidateDatasetHandle(handle, active_policy, entry).ResultErr?
  {
  }

  lemma INV_DATASET_OPEN_DENY_WITH_AUDIT_WRITES_BEFORE_RETURN(decision: SecurityDecision, prior_records: seq<AuditRecord>, next_record_id: MfosId)
    requires decision.result == DENY
    requires !IsSuccessError(decision.error_code)
    requires Authorization.RequiresAudit(decision)
    requires ValidCorrelationId(decision.context.correlation_id)
    requires ValidId(decision.subject.principal.principal_id)
    requires ValidId(decision.object_ref.object_id)
    requires ValidPolicyVersion(decision.policy_version)
    requires ValidId(next_record_id)
    ensures DeniedDatasetOpenWithAudit(decision, prior_records, next_record_id, true).handle.None?
    ensures DeniedDatasetOpenWithAudit(decision, prior_records, next_record_id, true).error_code == decision.error_code
    ensures !IsSuccessError(DeniedDatasetOpenWithAudit(decision, prior_records, next_record_id, true).error_code)
    ensures Audit.ExistsBeforeReturnAudit(decision, DeniedDatasetOpenWithAudit(decision, prior_records, next_record_id, true).audit_records)
    ensures Audit.RequiredAuditSatisfiedForFinalResult(decision, DeniedDatasetOpenWithAudit(decision, prior_records, next_record_id, true).audit_records)
    ensures DeniedDatasetOpenWithAudit(decision, prior_records, next_record_id, true).result_released
  {
    Audit.INV_AUDIT_DENY_TRANSITION_WRITES_BEFORE_RETURN(decision, prior_records, next_record_id);
  }

  lemma INV_DATASET_DENY_DECISION_NOT_MFOS_OK(decision: SecurityDecision)
    requires decision.result == DENY
    requires !IsSuccessError(decision.error_code)
    ensures decision.error_code != MFOS_OK
    ensures !IsSuccessError(decision.error_code)
  {
  }

  lemma INV_DATASET_AUDITED_DENY_DOES_NOT_BIND_MFOS_OK(decision: SecurityDecision, prior_records: seq<AuditRecord>, next_record_id: MfosId)
    requires decision.result == DENY
    requires !IsSuccessError(decision.error_code)
    requires Authorization.RequiresAudit(decision)
    requires ValidCorrelationId(decision.context.correlation_id)
    requires ValidId(decision.subject.principal.principal_id)
    requires ValidId(decision.object_ref.object_id)
    requires ValidPolicyVersion(decision.policy_version)
    requires ValidId(next_record_id)
    ensures DeniedDatasetOpenWithAudit(decision, prior_records, next_record_id, true).error_code != MFOS_OK
    ensures !IsSuccessError(DeniedDatasetOpenWithAudit(decision, prior_records, next_record_id, true).error_code)
  {
  }

  lemma INV_DATASET_OPEN_DENY_AUDIT_UNAVAILABLE_FAILS_CLOSED(decision: SecurityDecision, prior_records: seq<AuditRecord>, next_record_id: MfosId)
    requires decision.result == DENY
    requires !IsSuccessError(decision.error_code)
    requires Authorization.RequiresAudit(decision)
    requires ValidCorrelationId(decision.context.correlation_id)
    requires ValidId(next_record_id)
    ensures DeniedDatasetOpenWithAudit(decision, prior_records, next_record_id, false).handle.None?
    ensures DeniedDatasetOpenWithAudit(decision, prior_records, next_record_id, false).error_code == MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE
    ensures !DeniedDatasetOpenWithAudit(decision, prior_records, next_record_id, false).result_released
    ensures !IsSuccessError(DeniedDatasetOpenWithAudit(decision, prior_records, next_record_id, false).error_code)
  {
    Audit.INV_AUDIT_DENY_TRANSITION_FAILS_CLOSED_WHEN_UNAVAILABLE(decision, prior_records, next_record_id);
  }

  lemma INV_DATASET_CANNOT_BYPASS_AUDIT_WHEN_OBLIGATION_EXISTS(decision: SecurityDecision, records: seq<AuditRecord>)
    requires DecisionIsFailClosed(decision.result)
    requires Authorization.RequiresAudit(decision)
    requires !Audit.ExistsBeforeReturnAudit(decision, records)
    ensures !Audit.RequiredAuditSatisfiedForFinalResult(decision, records)
  {
    Audit.INV_AUTH_FAIL_CLOSED_RESULTS_CANNOT_BYPASS_AUDIT(decision, records);
  }

  lemma INV_DATASET_NOT_POSIX_FILE(dataset: Dataset)
    ensures TreatDatasetAsPosixFile(dataset).ResultErr?
    ensures !IsSuccessError(MFOS_ERR_UNSUPPORTED)
  {
    UnsupportedIsFailClosed();
  }

  lemma INV_DATASET_RETENTION_VIOLATION_NOT_SUCCESS(entry: CatalogEntry, decision: SecurityDecision)
    requires RetentionBlocksDelete(entry, decision.operation)
    requires SystemDatasetInvariant(entry)
    ensures DatasetDeleteOrModify(entry, decision).ResultErr?
    ensures !IsSuccessError(MFOS_ERR_RETENTION_DENIED)
  {
  }

  lemma INV_DATASET_IMMUTABLE_SYSTEM_MODIFICATION_NOT_SUCCESS(entry: CatalogEntry, decision: SecurityDecision)
    requires ImmutableSystemDatasetBlocksModify(entry, decision.operation)
    requires SystemDatasetInvariant(entry)
    ensures DatasetDeleteOrModify(entry, decision).ResultErr?
    ensures !IsSuccessError(MFOS_ERR_IMMUTABLE)
  {
  }

  lemma INV_DATASET_SYSTEM_DATASET_REQUIRES_IMMUTABLE(entry: CatalogEntry)
    requires entry.dataset.system_marker.system_dataset
    requires !entry.dataset.system_marker.immutable
    ensures !SystemDatasetInvariant(entry)
    ensures !CatalogEntryResolvable(entry)
    ensures ResolveCatalog(entry).ResultErr?
    ensures CatalogResolutionError(entry) == MFOS_ERR_INTERNAL_CORRUPTION
  {
  }

  lemma INV_DATASET_INVALID_SYSTEM_DATASET_STATE_REJECTED(entry: CatalogEntry, decision: SecurityDecision)
    requires entry.dataset.system_marker.system_dataset
    requires !entry.dataset.system_marker.immutable
    ensures DatasetDeleteOrModify(entry, decision).ResultErr?
    ensures !IsSuccessError(MFOS_ERR_INVALID_STATE)
  {
  }
}
