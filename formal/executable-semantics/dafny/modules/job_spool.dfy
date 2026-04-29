// MFOS Phase 1 Dafny executable semantics: job/spool model.
// This is not jobd, spoold, a scheduler, or a service.

include "common.dfy"
include "errors.dfy"
include "types.dfy"
include "authorization.dfy"
include "dataset_catalog.dfy"

module JobSpool {
  import opened Common
  import opened Errors
  import opened Types
  import Authorization
  import DatasetCatalog

  predicate EffectivePrincipalEstablished(job: Job) {
    ValidId(job.effective_principal.principal_id) && ValidSubject(job.owner)
  }

  predicate DDResolutionThroughCatalogAndAuth(entry: CatalogEntry, decision: SecurityDecision, satisfied: set<DecisionObligation>) {
    DatasetCatalog.CatalogEntryResolvable(entry) &&
    Authorization.CanCreateProtectedResourceHandle(decision, satisfied) &&
    decision.resource_class == RESOURCE_DATASET
  }

  predicate DatasetOpenAllowedForJob(job: Job, entry: CatalogEntry, decision: SecurityDecision, satisfied: set<DecisionObligation>) {
    EffectivePrincipalEstablished(job) &&
    DDResolutionThroughCatalogAndAuth(entry, decision, satisfied)
  }

  predicate ValidJobTransition(from_state: JobState, to_state: JobState) {
    (from_state == JOB_DEFINED && to_state == JOB_SUBMITTED) ||
    (from_state == JOB_SUBMITTED && to_state == JOB_RUNNING) ||
    (from_state == JOB_RUNNING && to_state == JOB_COMPLETE) ||
    (from_state == JOB_RUNNING && to_state == JOB_FAILED) ||
    (from_state == JOB_SUBMITTED && to_state == JOB_CANCELLED) ||
    (from_state == JOB_RUNNING && to_state == JOB_CANCELLED)
  }

  predicate SpoolEntryProtected(spool: SpoolEntry) {
    spool.protected && ValidId(spool.spool_id) && ValidSubject(spool.owner)
  }

  predicate SpoolBrowseAllowed(spool: SpoolEntry, decision: SecurityDecision) {
    SpoolEntryProtected(spool) &&
    decision.subject == spool.owner &&
    decision.resource_class == RESOURCE_SPOOL &&
    decision.operation == OP_QUERY &&
    Authorization.DecisionAllowsProtectedEffect(decision)
  }

  predicate SpoolPurgeDeniedWithoutAuthority(decision: SecurityDecision) {
    decision.resource_class == RESOURCE_SPOOL &&
    decision.operation == OP_PURGE &&
    !Authorization.DecisionAllowsProtectedEffect(decision)
  }

  lemma INV_JOB_EFFECTIVE_PRINCIPAL_BEFORE_OPEN(job: Job, entry: CatalogEntry, decision: SecurityDecision, satisfied: set<DecisionObligation>)
    requires !EffectivePrincipalEstablished(job)
    ensures !DatasetOpenAllowedForJob(job, entry, decision, satisfied)
  {
  }

  lemma INV_JOB_DD_RESOLUTION_THROUGH_CATALOG_AND_AUTH(job: Job, entry: CatalogEntry, decision: SecurityDecision, satisfied: set<DecisionObligation>)
    requires DatasetOpenAllowedForJob(job, entry, decision, satisfied)
    ensures DatasetCatalog.CatalogEntryResolvable(entry)
    ensures Authorization.DecisionAllowsProtectedEffect(decision)
  {
  }

  lemma INV_SPOOL_PROTECTED_RESOURCE(spool: SpoolEntry)
    requires SpoolEntryProtected(spool)
    ensures spool.protected
  {
  }

  lemma INV_SPOOL_BROWSE_BY_NON_OWNER_DENIED(spool: SpoolEntry, decision: SecurityDecision)
    requires decision.subject != spool.owner
    ensures !SpoolBrowseAllowed(spool, decision)
  {
  }

  lemma INV_SPOOL_BROWSE_WITHOUT_AUTHORITY_DENIED(spool: SpoolEntry, decision: SecurityDecision)
    requires !Authorization.DecisionAllowsProtectedEffect(decision)
    ensures !SpoolBrowseAllowed(spool, decision)
  {
  }

  lemma INV_SPOOL_PURGE_WITHOUT_AUTHORITY_DENIED(decision: SecurityDecision)
    requires decision.resource_class == RESOURCE_SPOOL
    requires decision.operation == OP_PURGE
    requires !Authorization.DecisionAllowsProtectedEffect(decision)
    ensures SpoolPurgeDeniedWithoutAuthority(decision)
  {
  }

  lemma INV_JOB_INVALID_LIFECYCLE_REJECTED(from_state: JobState, to_state: JobState)
    requires !ValidJobTransition(from_state, to_state)
    ensures !ValidJobTransition(from_state, to_state)
  {
  }
}
