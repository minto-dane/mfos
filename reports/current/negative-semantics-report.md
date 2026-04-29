# Negative Semantics Report

Status date: 2026-04-29

## Summary

Phase 1.1 added explicit Dafny predicates and lemmas for the required negative
semantic properties. Dafny verification passes with `45 verified, 0 errors`.

## Covered Negative Properties

| Property | Dafny coverage |
| --- | --- |
| `SPEC_GAP` is never success. | `INV_AUTH_SPEC_GAP_NOT_SUCCESS`, `SpecGapUnsupportedNeverComplete` |
| `UNSUPPORTED` is never success. | `INV_AUTH_UNSUPPORTED_NOT_SUCCESS`, `SpecGapUnsupportedNeverComplete` |
| DENY with audit obligation requires before-return audit. | `DenyWithAuditObligationSatisfiedBeforeReturn`, `INV_AUDIT_DENY_WITH_OBLIGATION_HAS_BEFORE_RETURN_RECORD` |
| No `DatasetHandle` without `ALLOW` or `ALLOW_WITH_AUDIT`. | `MayCreateDatasetHandle`, `INV_DATASET_NO_HANDLE_WITHOUT_ALLOW` |
| Catalog resolves only committed entries. | `CatalogEntryResolvable`, `INV_CATALOG_COMMITTED_ONLY` |
| Uncommitted catalog entry cannot resolve. | `INV_CATALOG_UNCOMMITTED_CANNOT_RESOLVE` |
| Rolled-back catalog entry cannot resolve. | `INV_CATALOG_ROLLED_BACK_CANNOT_RESOLVE` |
| Integrity-failed catalog entry cannot resolve. | `INV_CATALOG_INTEGRITY_FAILED_CANNOT_RESOLVE` |
| Stale handle after policy change is rejected. | `INV_DATASET_STALE_HANDLE_AFTER_POLICY_CHANGE_REJECTED` |
| Stale handle after generation change is rejected. | `INV_DATASET_STALE_HANDLE_AFTER_GENERATION_CHANGE_REJECTED` |
| Job cannot open dataset before effective principal exists. | `INV_JOB_EFFECTIVE_PRINCIPAL_BEFORE_OPEN` |
| DD resolution must go through catalog and authorization. | `INV_JOB_DD_RESOLUTION_THROUGH_CATALOG_AND_AUTH` |
| Spool browse by non-owner is denied. | `INV_SPOOL_BROWSE_BY_NON_OWNER_DENIED` |
| Spool purge without authority is denied. | `INV_SPOOL_PURGE_WITHOUT_AUTHORITY_DENIED` |
| Operator command cannot execute without authorization. | `INV_OPERATOR_NO_COMMAND_WITHOUT_AUTH` |
| Destructive operator command without confirmation is denied. | `INV_OPERATOR_DESTRUCTIVE_WITHOUT_CONFIRMATION_DENIED` |
| Dual-control command with single approval is denied. | `INV_OPERATOR_DUAL_CONTROL_SINGLE_APPROVAL_DENIED` |
| Emergency mode without reason/expiry is denied. | `INV_OPERATOR_EMERGENCY_WITHOUT_REASON_OR_EXPIRY_DENIED` |
| Root shell cannot be first privileged UI. | `INV_OPERATOR_ROOT_SHELL_NOT_FIRST_UI` |

## First Vertical Slice

The first vertical slice now records explicit symbolic audit sequences:

- HELLO job: submit, open, execute, spool, complete.
- BOB denied ALICE dataset: submit, open-deny, failure-summary.

BOB denied remains mapped to:

```yaml
decision: DENY
error_code: MFOS_ERR_POLICY_DENIED
reason_code: DATASET_READ_NOT_PERMITTED
dataset_handle_created: false
audit_before_final_result: true
```

## Boundary

No production implementation, Rust semantic-core, semantic runner, hosted daemon,
service implementation, nucleus, PXM, Guard, MFVM, CVM, or cluster implementation
was added.
