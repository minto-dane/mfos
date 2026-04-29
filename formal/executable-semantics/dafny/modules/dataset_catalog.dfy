// MFOS Phase 1 Dafny executable semantics: dataset/catalog model.
// This is not datasetd, catalogd, storage, or POSIX behavior.

include "common.dfy"
include "errors.dfy"
include "types.dfy"
include "authorization.dfy"

module DatasetCatalog {
  import opened Common
  import opened Errors
  import opened Types
  import Authorization

  predicate SymbolicDsnValid(dataset: Dataset) {
    ValidId(dataset.name_id)
  }

  predicate CatalogEntryResolvable(entry: CatalogEntry) {
    entry.state == CATALOG_COMMITTED &&
    entry.integrity_valid &&
    ValidGeneration(entry.catalog_generation) &&
    ValidGeneration(entry.dataset_generation)
  }

  function ResolveCatalog(entry: CatalogEntry): Result<CatalogEntry> {
    if CatalogEntryResolvable(entry) then ResultOk(entry)
    else if entry.state == CATALOG_INTEGRITY_FAILED || entry.state == CATALOG_PARTIAL_JOURNAL || !entry.integrity_valid then ResultErr(ErrorRank(MFOS_ERR_INVALID_STATE))
    else ResultErr(ErrorRank(MFOS_ERR_CATALOG_NOT_FOUND))
  }

  predicate MayCreateDatasetHandle(entry: CatalogEntry, decision: SecurityDecision, satisfied: set<DecisionObligation>) {
    CatalogEntryResolvable(entry) &&
    decision.object_ref == entry.dataset.object_ref &&
    decision.context.object_generation == entry.catalog_generation &&
    decision.resource_class == RESOURCE_DATASET &&
    Authorization.CanCreateProtectedResourceHandle(decision, satisfied)
  }

  predicate HandleBoundToObjectGeneration(handle: DatasetHandle, entry: CatalogEntry, decision: SecurityDecision) {
    handle.active &&
    handle.subject == decision.subject &&
    handle.object_ref == entry.dataset.object_ref &&
    handle.operation == decision.operation &&
    handle.policy_version == decision.policy_version &&
    handle.catalog_generation == entry.catalog_generation &&
    handle.dataset_generation == entry.dataset_generation
  }

  predicate HandleFresh(handle: DatasetHandle, active_policy: PolicyVersion, entry: CatalogEntry) {
    handle.active &&
    handle.policy_version == active_policy &&
    handle.catalog_generation == entry.catalog_generation &&
    handle.dataset_generation == entry.dataset_generation
  }

  predicate RetentionBlocksDelete(entry: CatalogEntry, operation: Operation) {
    entry.dataset.retention_active && (operation == OP_DELETE || operation == OP_PURGE)
  }

  predicate ImmutableSystemDatasetBlocksModify(entry: CatalogEntry, operation: Operation) {
    entry.dataset.immutable_system && (operation == OP_WRITE || operation == OP_DELETE || operation == OP_PURGE)
  }

  lemma INV_CATALOG_COMMITTED_ONLY(entry: CatalogEntry)
    requires entry.state != CATALOG_COMMITTED || !entry.integrity_valid
    ensures !CatalogEntryResolvable(entry)
  {
  }

  lemma INV_CATALOG_UNCOMMITTED_CANNOT_RESOLVE(entry: CatalogEntry)
    requires entry.state == CATALOG_STAGED
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

  lemma INV_CATALOG_INTEGRITY_FAILED_CANNOT_RESOLVE(entry: CatalogEntry)
    requires entry.state == CATALOG_INTEGRITY_FAILED || !entry.integrity_valid
    ensures !CatalogEntryResolvable(entry)
    ensures ResolveCatalog(entry).ResultErr?
  {
  }

  lemma INV_CATALOG_PARTIAL_JOURNAL_CANNOT_RESOLVE(entry: CatalogEntry)
    requires entry.state == CATALOG_PARTIAL_JOURNAL
    ensures !CatalogEntryResolvable(entry)
    ensures ResolveCatalog(entry).ResultErr?
  {
  }

  lemma INV_DATASET_NO_HANDLE_WITHOUT_ALLOW(entry: CatalogEntry, decision: SecurityDecision, satisfied: set<DecisionObligation>)
    requires !Authorization.DecisionAllowsProtectedEffect(decision)
    ensures !MayCreateDatasetHandle(entry, decision, satisfied)
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
  {
  }

  lemma INV_DATASET_STALE_HANDLE_AFTER_GENERATION_CHANGE_REJECTED(handle: DatasetHandle, active_policy: PolicyVersion, entry: CatalogEntry)
    requires handle.catalog_generation != entry.catalog_generation ||
             handle.dataset_generation != entry.dataset_generation
    ensures !HandleFresh(handle, active_policy, entry)
  {
  }
}
