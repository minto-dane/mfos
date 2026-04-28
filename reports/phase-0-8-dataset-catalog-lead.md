# Phase 0.8 Dataset/Catalog Lead Report

Date: 2026-04-27

Status: Draft semantic freeze complete for owned artifacts.

## Scope

Owned artifacts updated or added:

- `docs/design/specs/08-dataset-catalog.md`
- `schemas/mfos/dataset.schema.yml`
- `schemas/mfos/catalog-entry.schema.yml`
- `schemas/mfos/dataset-handle.schema.yml`
- `schemas/mfos/object-generation-binding.schema.yml`
- `formal/tla/dataset-open/`
- `formal/tla/catalog-transaction/`
- `tests/catalog/phase-0-8-dataset-catalog-tests.yml`
- `reports/phase-0-8-dataset-catalog-lead.md`

No production code was written.

## Source Refs

Phase 0.8 dataset/catalog freeze artifacts use EXTREF source refs only:

- `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`
- `EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001`
- `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`
- `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001`
- `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`
- `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001`

## Frozen Decisions

- Dataset is a managed MFOS object, not a POSIX file wrapper, inode, mount target, or raw volume handle.
- Phase 0.8 DSN grammar is the uppercase qualifier subset:
  `^[A-Z][A-Z0-9_-]{0,7}(\\.[A-Z][A-Z0-9_-]{0,7})*$`, maximum DSN length 255.
- `MFOS-REQ-CATALOG-0002` remains a MUST: `catalogd` resolves only committed catalog entries.
- Uncommitted, rolled-back, partially journaled, orphaned, deleted, corrupt, or integrity-failed entries never resolve.
- `CatalogEntry`, `Dataset`, `DatasetHandle`, and `ObjectGenerationBinding` now have closed logical schemas.
- System datasets are immutable once committed.
- Dataset handles bind subject, operation, policy version, catalog generation, dataset generation, expiry, correlation ID, policy binding, and `ObjectGenerationBinding`.
- Retention blocks delete/purge until policy allows it.
- Encryption is a Phase 0.8 placeholder. Required encryption must fail closed when the key-service profile is unspecified or unavailable.
- Integrity tags are SHA-384 logical tags over canonical metadata; exact byte encoding remains an evidence item before implementation.
- Crash recovery must expose only old committed, new fully committed, or no entry.

## Formal Artifacts

`formal/tla/dataset-open/` models:

- no active handle without committed catalog resolution
- no active handle without ALLOW
- no active handle without audit
- no active handle without generation binding
- deny/fail-closed paths create no handle

`formal/tla/catalog-transaction/` models:

- committed-entry-only resolution
- partial journal never resolves
- integrity failure never resolves
- transaction completion requires audit
- rollback never resolves

These are design artifacts. Model-check output or reviewed transition traces are still required evidence.

## Test Coverage

`tests/catalog/phase-0-8-dataset-catalog-tests.yml` covers:

- DSN positive and negative grammar cases
- committed-entry resolve
- uncommitted, rolled-back, partial-journal, and integrity-tag negative cases
- immutable system dataset denial
- authorized handle creation with `ObjectGenerationBinding`
- authorization deny with no handle
- stale handle rejection
- raw volume/POSIX bypass rejection
- retention allow/block paths
- encryption placeholder fail-closed behavior
- deny audit ordering and audit-unavailable failure
- schema conformance
- fuzz decisions and deferred crypto fuzzing

## Evidence Required

Before implementation or conformance claims, Phase 0.8 needs:

- schema validation report for all four `schemas/mfos` files
- catalog transaction model-check or reviewed trace report
- dataset open model-check or reviewed trace report
- catalog crash-recovery report
- dataset handle binding report
- deny-no-handle and audit-ordering reports
- audit samples for resolve deny, open allow, open deny, stale handle, immutable denial, retention denial, and integrity failure
- fuzz corpus manifests for DSN, catalog entry decode, dataset open request, and object generation binding

## Residual Gaps

- Concrete canonical byte encoding for `integrity_tag`.
- Full `FB`, `VB`, and future record-format behavior.
- `PDS_LITE` member namespace and concurrency.
- Volume manager and extent allocator ABI.
- Encryption key-service ABI and cryptographic provider policy.
- Backup hook ABI.
- Dataset migration behavior.
- Secure deletion guarantees by storage backend.
- Multi-partition catalog replication.

## Notes

The existing requirements registry already preserves `MFOS-REQ-CATALOG-0002` as a MUST committed-entry-only requirement. This report does not alter registries or production paths.
