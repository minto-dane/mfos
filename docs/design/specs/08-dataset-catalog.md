---
spec_id: "MFOS-SPEC-08-DATASET-CATALOG"
title: "MFOS Dataset and Catalog Specification Phase 0.8 Freeze"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001", "EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001"]
requirement_refs: ["MFOS-REQ-CATALOG-*", "MFOS-REQ-DATASET-*"]
claim_refs: []
test_refs: ["TEST-MFOS-CATALOG-COMMITTED-0002", "NEG-MFOS-CATALOG-UNCOMMITTED-0002", "NEG-MFOS-CATALOG-ROLLED-BACK-0002", "NEG-MFOS-CATALOG-PARTIAL-JOURNAL-0002", "NEG-MFOS-CATALOG-INTEGRITY-TAG-0002", "TEST-MFOS-DATASET-HANDLE-0001", "NEG-MFOS-DATASET-DENY-NO-HANDLE-0002", "TEST-MFOS-DATASET-FUZZ-0001"]
evidence_refs: ["EV-MFOS-CATALOG-TX-0002", "EV-MFOS-CATALOG-CRASH-0002", "EV-MFOS-DATASET-HANDLE-0001", "EV-MFOS-DATASET-NO-HANDLE-0002", "EV-MFOS-DATASET-AUD-ORDER-0006"]
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Dataset and Catalog Specification Phase 0.8 Freeze

Status: Draft Phase 0.8 semantic freeze

Owned components: `catalogd`, `datasetd`

Primary source matrix IDs: `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001`

Related requirements: `MFOS-REQ-CATALOG-*`, `MFOS-REQ-DATASET-*`, `MFOS-REQ-AUTH-*`, `MFOS-REQ-AUDIT-*`, `MFOS-REQ-SYSINT-*`, `MFOS-REQ-AI-*`

## 1. Purpose

This specification defines MFOS datasets and catalogs as first-class enterprise OS objects. A dataset is not a POSIX file wrapper. A catalog entry binds a dataset name to controlled metadata, location, ownership, integrity state, security profile, and generation.

Phase 0.8 freezes logical semantics only. It authorizes schema, model, test, and evidence planning work; it does not authorize production code or runtime success paths.

MFOS is z/OS-inspired, not z/OS-compatible. The source-grounded overlap is the enterprise idea that named datasets are managed resources resolved through catalogs and governed by security and audit policy. MFOS diverges by defining a new x64-native object model, new service ABIs, and a smaller initial dataset type set.

## 2. Scope

In scope:

- Dataset name grammar.
- Dataset, CatalogEntry, DatasetHandle, and ObjectGenerationBinding logical schemas.
- Catalog entry creation, lookup, transaction, recovery, and integrity checking.
- Dataset allocation, open, close, handle binding, retention, integrity tag hooks, and secure deletion policy.
- Committed-entry-only catalog resolution.
- Immutable system dataset behavior.
- Encryption policy placeholder semantics.
- Securityd-mediated authorization for all protected dataset and catalog operations.
- Auditd evidence for create, resolve, open, deny, write, close, retain, delete, recover, and integrity-check events.

Out of scope:

- z/OS catalog binary compatibility.
- z/OS DFSMS API compatibility.
- Full VSAM, GDG, PDS, PDSE, HFS, or zFS compatibility.
- POSIX pathname semantics as the primary namespace.
- Linux filesystem mounts, POSIX inode identity, or direct POSIX syscall access to MFOS datasets.
- Direct block-device access by jobs.
- Dataset policy decisions inside PXM or Guard.

## 3. Non-Compatibility Statement

MFOS MUST NOT claim z/OS catalog, DFSMS, RACF, SMF, or dataset compatibility. MFOS MAY say "z/OS-inspired dataset and catalog semantics" when the relevant Source Matrix IDs are listed and the MFOS divergence is explicit.

Prohibited wording:

- "z/OS-compatible datasets"
- "DFSMS-compatible catalog"
- "RACF-compatible profiles"
- "SMF-compatible records"

Allowed wording:

- "Source-grounded, z/OS-inspired dataset/catalog model"
- "RACF-inspired security profile decision through securityd"
- "SMF-inspired audit evidence through auditd"

## 4. Component Responsibilities

### 4.1 catalogd

`catalogd` owns the persistent namespace for datasets.

Responsibilities:

- `CAT-R-001` DSN grammar validation.
- `CAT-R-002` Catalog entry creation.
- `CAT-R-003` DSN resolution.
- `CAT-R-004` System dataset marking.
- `CAT-R-005` Immutable catalog entry enforcement.
- `CAT-R-006` Generation tracking.
- `CAT-R-007` Volume and extent mapping.
- `CAT-R-008` Catalog transaction management.
- `CAT-R-009` Crash recovery.
- `CAT-R-010` Catalog integrity checking.

Non-responsibilities:

- Final access authorization.
- Dataset block or record IO.
- Job DD interpretation beyond catalog lookup.
- POSIX path resolution.
- PXM partition lifecycle.

### 4.2 datasetd

`datasetd` owns dataset allocation and access handles.

Responsibilities:

- `DATA-R-001` Allocation.
- `DATA-R-002` Open and close.
- `DATA-R-003` Record access.
- `DATA-R-004` Block access for service-owned internals.
- `DATA-R-005` Dataset handle lifecycle.
- `DATA-R-006` Retention enforcement.
- `DATA-R-007` Encryption policy hook.
- `DATA-R-008` Integrity tag verification.
- `DATA-R-009` Backup hook.
- `DATA-R-010` Secure deletion policy.

Non-responsibilities:

- Catalog namespace ownership.
- Final access authorization.
- Spool formatting.
- Job scheduling.
- Operator command parsing.

## 5. Object Model

### 5.1 DatasetName

```yaml
DatasetName:
  dsn: string
  qualifiers: [string]
  canonical: string
  class_hint: USER | SYS | TEMP | SPOOL | POLICY | MODULE | AUDIT | CATALOG
```

Rules:

- DSNs MUST be canonicalized before lookup.
- DSNs MUST be compared by canonical form.
- DSNs MUST NOT be treated as POSIX paths.
- A DSN parser failure MUST return `MFOS_ERR_INVALID_DSN`.
- Phase 0.8 freezes the DSN grammar below. Any extension outside this grammar is a SPEC_GAP until this specification is revised.

Phase 0.8 grammar:

```text
DSN        := QUAL ( "." QUAL )*
QUAL       := ALPHA ( ALPHA | DIGIT | "_" | "-" )*
ALPHA      := "A".."Z"
DIGIT      := "0".."9"
MAX_QUAL   := 8 characters
MAX_DSN    := 255 characters
MIN_QUALS  := 1
```

Grammar rules:

- Empty qualifiers, leading dots, trailing dots, repeated dots, spaces, slashes, backslashes, colons, NUL bytes, and POSIX path segments are invalid.
- Lowercase input MAY be normalized to uppercase by operator tooling before it crosses the `catalogd` service boundary.
- `catalogd` input MUST already be canonical uppercase or fail with `MFOS_ERR_INVALID_DSN`.
- Full z/OS naming rules are not claimed.

### 5.2 CatalogEntry

```yaml
CatalogEntry:
  schema_version: 1
  dsn: string
  canonical_dsn: string
  entry_id: uuid
  dataset_id: uuid
  owner: PrincipalRef
  attributes:
    dataset_type: SEQ | PDS_LITE | SYSIN | SYSOUT | LOG | CAT | POLICY | MODULE
    record_format: FB | VB | BYTE_STREAM
    record_length: uint32?
    block_size: uint32?
    allocation_unit: BLOCK | EXTENT | OBJECT
  location:
    volume_refs: [VolumeRef]
    extent_refs: [VolumeExtentRef]
    storage_class: string?
  security_profile: SecurityProfileRef
  retention_policy: RetentionPolicyRef
  encryption_policy:
    mode: UNENCRYPTED | KEY_SERVICE_PLACEHOLDER
    key_profile_ref: string?
    status: PLACEHOLDER_ONLY | CONFIGURED
  integrity_policy: IntegrityPolicyRef
  generation: uint64
  immutable: bool
  system_dataset: bool
  integrity_tag:
    algorithm: SHA384
    value: hex
  state: PREPARED | COMMITTED | DELETING | DELETED | CORRUPT
  created_at_utc: timestamp
  updated_at_utc: timestamp
```

CatalogEntry rules:

- `catalogd` MUST resolve only entries whose state is `COMMITTED` and whose `integrity_tag` verifies over the canonical entry payload.
- `PREPARED`, rolled-back, partially journaled, `DELETING`, `DELETED`, `CORRUPT`, orphaned, or integrity-failed entries MUST NOT resolve.
- A `system_dataset: true` entry MUST also have `immutable: true` at commit time.
- Once committed, a system dataset entry MUST reject owner, location, security profile, retention, encryption, integrity, and deletion changes with `MFOS_ERR_IMMUTABLE` unless an explicit recovery-mode transaction is defined in a later reviewed specification.
- `location` is an MFOS storage reference. It MUST NOT contain a POSIX path, inode, host filesystem path, or caller-supplied raw block-device escape.
- `integrity_tag` is a logical SHA-384 tag over canonical catalog metadata. The exact canonical byte encoding is a Phase 0.8 evidence requirement, not production code.

### 5.3 Dataset

```yaml
Dataset:
  schema_version: 1
  dsn: string
  canonical_dsn: string
  dataset_id: uuid
  owner: PrincipalRef
  dataset_type: SEQ | PDS_LITE | SYSIN | SYSOUT | LOG | CAT | POLICY | MODULE
  catalog_entry: CatalogEntryRef
  security_profile: SecurityProfileRef
  retention_policy: RetentionPolicyRef
  encryption_policy: EncryptionPolicyRef?
  integrity_policy: IntegrityPolicyRef
  generation: uint64
  status: ACTIVE | MIGRATED | LOCKED | DELETING | DELETED | CORRUPT
```

Dataset rules:

- A dataset is a managed MFOS resource with record/block semantics defined by MFOS, not a POSIX file, path, inode, or mount target.
- Persistent datasets MUST be reachable through a committed `CatalogEntry`; raw volume references MUST NOT be accepted as substitutes for catalog resolution.
- `generation` increments on committed dataset metadata or content mutations that invalidate existing handles.
- `encryption_policy` is a placeholder binding in Phase 0.8. If an entry requires a configured key service before access and that service is unspecified or unavailable, access MUST fail closed with `MFOS_ERR_SPEC_GAP` or a profile-specific fail-closed encryption error.

### 5.4 DatasetHandle

```yaml
DatasetHandle:
  schema_version: 1
  handle_id: uuid
  dsn: string
  canonical_dsn: string
  dataset_id: uuid
  subject: SubjectRef
  operation: READ | WRITE | UPDATE | CREATE | DELETE | CONTROL
  policy_version: uint64
  catalog_entry_generation: uint64
  dataset_generation: uint64
  policy_binding_ref: PolicyBindingRef
  object_generation_binding: ObjectGenerationBinding
  issued_at_utc: timestamp
  expires_at_utc: timestamp
  correlation_id: uuid
  audit_obligation_id: uuid
  state: ACTIVE | CLOSING | REVOKED | CLOSED
```

Handle rules:

- A handle MUST be bound to the subject, operation, policy version, catalog generation, dataset generation, expiry, and correlation ID.
- A handle MUST carry the `ObjectGenerationBinding` used at authorization time.
- A stale handle MUST be rejected with `MFOS_ERR_STALE_HANDLE`.
- A policy version mismatch MUST be rejected with `MFOS_ERR_POLICY_VERSION_MISMATCH`.
- A handle MUST NOT be issued before required audit obligations are established.
- A caller-supplied handle-like token, cached handle, or deferred handle MUST NOT be accepted unless it validates against committed object generation state.

### 5.5 ObjectGenerationBinding

```yaml
ObjectGenerationBinding:
  binding_id: uuid
  dsn: string
  catalog_entry_id: uuid
  dataset_id: uuid
  committed_catalog_entry_generation: uint64
  committed_dataset_generation: uint64
  security_policy_generation: uint64
  policy_version: uint64
  observed_at_utc: timestamp
  integrity_tag:
    algorithm: SHA384
    value: hex
```

Rules:

- `ObjectGenerationBinding` MUST be created from committed catalog and dataset state after catalog resolution and before handle issuance.
- Generation values MUST come from `catalogd`, `datasetd`, and `securityd`; caller-supplied generation values are advisory only and MUST NOT establish authority.
- A mismatch between the binding and current committed state MUST reject use with `MFOS_ERR_STALE_HANDLE` or `MFOS_ERR_POLICY_VERSION_MISMATCH`.
- The binding MUST be referenced in allow, deny, stale-handle, and integrity-failure audit evidence where available.

### 5.6 Volume and Extent

```yaml
VolumeRef:
  volume_id: string
  volume_type: BLOCK | OBJECT | MEMORY
  partition_id: uint64
  integrity_domain: string

VolumeExtentRef:
  volume_id: string
  offset: uint64
  length: uint64
  allocation_generation: uint64
```

## 6. State Machines

### 6.1 Catalog Transaction

```text
BEGIN_TX
  -> VALIDATE_DSN
  -> AUTHORIZE_CATALOG_UPDATE
  -> PREPARE_ENTRY
  -> WRITE_JOURNAL
  -> COMMIT_ENTRY
  -> WRITE_AUDIT
  -> COMPLETE
```

Resolution rule:

```text
CATALOG_RESOLVE_OK(dsn) iff
  catalog entry exists for canonical dsn
  and entry.state = COMMITTED
  and entry.integrity_tag verifies
  and recovery state is not blocking that entry
```

No other catalog transaction state is a committed entry for `MFOS-REQ-CATALOG-0002`.

Failure states:

```text
INVALID_DSN
POLICY_DENIED
IMMUTABLE_DENIED
JOURNAL_WRITE_FAILED
AUDIT_REQUIRED_BUT_UNAVAILABLE
CATALOG_CORRUPT
ROLLBACK_REQUIRED
SPEC_GAP
```

Invalid catalog transaction transitions:

| Attempted transition | Required result |
| --- | --- |
| `BEGIN_TX -> PREPARE_ENTRY` without `VALIDATE_DSN` | Return `MFOS_ERR_INVALID_DSN` or `MFOS_ERR_SPEC_GAP`; no journal entry and no catalog mutation. |
| `VALIDATE_DSN -> PREPARE_ENTRY` without `AUTHORIZE_CATALOG_UPDATE` | Return `MFOS_ERR_POLICY_DENIED`; no prepared entry and deny audit before final result. |
| `PREPARE_ENTRY -> COMMIT_ENTRY` without `WRITE_JOURNAL` | Return `MFOS_ERR_INTERNAL_CORRUPTION`; no committed entry MUST be resolved. |
| `WRITE_JOURNAL -> COMPLETE` without `COMMIT_ENTRY` | Enter `ROLLBACK_REQUIRED`; recovery MUST remove the incomplete candidate. |
| `COMMIT_ENTRY -> COMPLETE` without required audit for a protected catalog update | Return `MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE`; success MUST NOT be reported and recovery MUST expose the incomplete audit state. |
| `RECOVER_SCAN_JOURNAL -> VERIFY_COMMITTED` while a partial journal entry remains | Continue rollback or return `MFOS_ERR_INTERNAL_CORRUPTION`; partial entries MUST NOT resolve. |
| `VERIFY_COMMITTED -> CATALOG_RESOLVE_OK` after `integrity_tag` mismatch | Return `MFOS_ERR_INTERNAL_CORRUPTION`; affected entry MUST NOT resolve. |

Recovery state machine:

```text
RECOVER_SCAN_JOURNAL
  -> ROLLBACK_INCOMPLETE
  -> VERIFY_COMMITTED
  -> REPAIR_ORPHAN_EXTENTS
  -> AUDIT_RECOVERY
  -> RECOVERY_COMPLETE
```

Recovery rules:

- Recovery MUST leave each DSN resolving to either the prior committed entry, a later fully committed and integrity-verified entry, or no entry.
- Recovery MUST NOT expose a prepared entry, torn journal record, orphan extent, or unverified integrity tag as committed.
- If recovery cannot determine a safe committed state, protected catalog and dataset operations for the affected DSN MUST fail closed.
- Crash recovery evidence MUST include the scanned journal generation, affected DSNs, action taken, and correlation IDs for emitted recovery audit records.

### 6.2 Dataset Open

```text
REQUEST_OPEN
  -> VALIDATE_DSN
  -> RESOLVE_CATALOG
  -> AUTHORIZE
  -> ESTABLISH_AUDIT_OBLIGATION
  -> VERIFY_GENERATION
  -> VERIFY_INTEGRITY_TAG
  -> BIND_OBJECT_GENERATION
  -> CREATE_HANDLE
  -> OPEN_ACTIVE
  -> CLOSE_REQUESTED
  -> HANDLE_REVOKED
  -> CLOSED
```

Failure states:

```text
INVALID_DSN
CATALOG_NOT_FOUND
POLICY_DENIED
POLICY_VERSION_MISMATCH
DATASET_LOCKED
RETENTION_DENIED
INTEGRITY_TAG_MISMATCH
AUDIT_REQUIRED_BUT_UNAVAILABLE
STALE_HANDLE
SPEC_GAP
```

Invalid dataset open transitions:

| Attempted transition | Required result |
| --- | --- |
| `REQUEST_OPEN -> AUTHORIZE` without `RESOLVE_CATALOG` | Return `MFOS_ERR_CATALOG_NOT_FOUND` or `MFOS_ERR_SPEC_GAP`; no handle. |
| `RESOLVE_CATALOG -> CREATE_HANDLE` without `AUTHORIZE` | Return `MFOS_ERR_POLICY_DENIED`; no handle and deny audit before final result. |
| `AUTHORIZE(DENY) -> CREATE_HANDLE` | Return `MFOS_ERR_POLICY_DENIED`; no handle. |
| `AUTHORIZE -> CREATE_HANDLE` without required audit obligation established | Return `MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE`; no handle. |
| `VERIFY_GENERATION` failure followed by `CREATE_HANDLE` or `OPEN_ACTIVE` | Return `MFOS_ERR_STALE_HANDLE` or `MFOS_ERR_POLICY_VERSION_MISMATCH`; no handle. |
| `VERIFY_INTEGRITY_TAG` failure followed by `CREATE_HANDLE` or `OPEN_ACTIVE` | Return `MFOS_ERR_INTERNAL_CORRUPTION`; no handle and integrity failure audit. |
| `VERIFY_GENERATION -> CREATE_HANDLE` without `BIND_OBJECT_GENERATION` | Return `MFOS_ERR_STALE_HANDLE` or `MFOS_ERR_SPEC_GAP`; no handle. |
| `OPEN_ACTIVE -> CLOSED` without `CLOSE_REQUESTED` or `HANDLE_REVOKED` | Return `MFOS_ERR_INVALID_PARAMETER`; handle state MUST remain authoritative. |

### 6.3 Dataset Deletion

```text
REQUEST_DELETE
  -> RESOLVE_CATALOG
  -> AUTHORIZE_DELETE
  -> CHECK_IMMUTABLE_SYSTEM_FLAG
  -> CHECK_RETENTION
  -> MARK_DELETING
  -> REVOKE_OPEN_HANDLES
  -> SECURE_DELETE_OR_TOMBSTONE
  -> UPDATE_CATALOG
  -> WRITE_AUDIT
  -> DELETED
```

## 7. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| `MFOS-REQ-CATALOG-0001` | DSN grammar MUST be specified and parser-tested. | Parser tests and fuzzing |
| `MFOS-REQ-CATALOG-0002` | `catalogd` MUST resolve only committed catalog entries and MUST NOT resolve uncommitted, rolled-back, partially journaled, integrity-failed, or orphaned entries. | Transaction tests; crash-recovery negative tests for uncommitted, rolled-back, partial-journal, and integrity-tag-mismatched entries |
| `MFOS-REQ-CATALOG-0003` | Catalog entries MUST include owner, attributes, location, security profile, generation, and integrity tag. | Schema tests |
| `MFOS-REQ-CATALOG-0004` | System datasets MUST be immutable once committed. | Negative tests |
| `MFOS-REQ-CATALOG-0005` | Catalog transactions MUST be crash recoverable. | Crash-recovery tests |
| `MFOS-REQ-CATALOG-0006` | Catalog entry generation MUST increase on committed metadata updates. | Unit tests |
| `MFOS-REQ-CATALOG-0007` | Catalog update MUST require securityd authorization. | Integration tests |
| `MFOS-REQ-CATALOG-0008` | Catalog corruption detection MUST fail closed for protected datasets. | Fault injection |
| `MFOS-REQ-DATASET-0001` | Dataset handles MUST bind subject, operation, policy version, catalog generation, dataset generation, and expiry. | Handle tests |
| `MFOS-REQ-DATASET-0002` | Unauthorized access MUST NOT create a dataset handle. | Negative tests |
| `MFOS-REQ-DATASET-0003` | Retention policy MUST affect delete and purge. | Retention tests |
| `MFOS-REQ-DATASET-0004` | Encryption policy MUST be linked to the configured key service profile. | Integration tests |
| `MFOS-REQ-DATASET-0005` | Dataset MUST NOT be defined as a POSIX file wrapper. | Architecture review |
| `MFOS-REQ-DATASET-0006` | Dataset open DENY MUST be audited before the caller receives the denial. | Ordering tests |
| `MFOS-REQ-DATASET-0007` | Dataset integrity tag mismatch MUST fail closed. | Fault injection |
| `MFOS-REQ-DATASET-0008` | Secure deletion MUST produce an audit record or return a fail-closed error. | Security tests |

## 8. Security Invariants

```text
INV-CAT-001:
  datasetd cannot open a persistent dataset unless catalogd resolves
  the DSN to a committed catalog entry.

INV-CAT-001A:
  catalogd cannot return CATALOG_RESOLVE_OK for PREPARED, rolled-back,
  partially journaled, integrity-failed, orphaned, DELETING, DELETED,
  or CORRUPT entries.

INV-CAT-002:
  catalogd cannot commit a protected catalog entry update without a
  securityd ALLOW or ALLOW_WITH_AUDIT decision for the exact subject,
  DSN, operation, context, and policy_version.

INV-DATA-001:
  dataset handle is bound to subject, operation, policy_version,
  catalog_entry_generation, dataset_generation, and expiry.

INV-DATA-002:
  unauthorized dataset access cannot create an ACTIVE handle.

INV-DATA-003:
  a DENY decision for dataset access MUST be durably submitted to auditd
  before the denial is returned to the caller.

INV-DATA-004:
  a dataset is never authorized through POSIX path, inode, mount, or raw
  volume identity in place of DSN catalog resolution.

INV-DATA-005:
  system_dataset implies immutable for committed catalog entries.
```

## 9. Audit Obligations

Every catalog and dataset operation MUST carry a `correlation_id`.

Required audit events:

| Event | Required fields |
| --- | --- |
| `CATALOG_DEFINE_REQUEST` | subject, dsn, owner, attributes, policy_version, correlation_id |
| `CATALOG_DEFINE_ALLOW` | decision, reason_code, catalog_generation |
| `CATALOG_DEFINE_DENY` | decision, reason_code, policy_version |
| `CATALOG_RESOLVE` | subject, dsn, result, catalog_generation |
| `CATALOG_UPDATE_COMMIT` | old_generation, new_generation, integrity_tag |
| `CATALOG_RECOVERY` | recovery_action, affected_entries, reason_code |
| `DATASET_ALLOCATE` | dsn, owner, dataset_type, location_ref |
| `DATASET_OPEN_ALLOW` | subject, dsn, operation, handle_id, policy_version, object_generation_binding |
| `DATASET_OPEN_DENY` | subject, dsn, operation, reason_code, policy_version |
| `DATASET_CLOSE` | handle_id, bytes_read, bytes_written, result |
| `DATASET_DELETE_REQUEST` | subject, dsn, retention_policy |
| `DATASET_DELETE_DENY` | reason_code, retention_policy, policy_version |
| `DATASET_INTEGRITY_FAILURE` | dsn, expected_tag, observed_tag |
| `DATASET_RETENTION_BLOCK` | dsn, retention_policy, requested_action, policy_version |
| `DATASET_IMMUTABLE_DENY` | dsn, system_dataset, requested_action, policy_version |

Audit failure policy:

- Baseline: protected dataset operations MUST fail closed when an audit obligation is required and auditd is unavailable.
- Enterprise: all protected dataset and catalog mutations MUST fail closed when auditd is unavailable.
- High-Assurance: Guard-sealed audit-root updates are required for security-root, policy, module, and audit datasets.

## 10. Failure Modes

| Error | Meaning | Required behavior |
| --- | --- | --- |
| `MFOS_ERR_INVALID_DSN` | DSN rejected by grammar. | No catalog lookup; audit malformed input if security-relevant. |
| `MFOS_ERR_CATALOG_NOT_FOUND` | No committed entry exists. | No handle; audit for protected lookup contexts. |
| `MFOS_ERR_POLICY_DENIED` | securityd denied operation. | Audit before returning denial. |
| `MFOS_ERR_POLICY_VERSION_MISMATCH` | Caller used stale policy context. | No handle; caller MUST retry with current policy. |
| `MFOS_ERR_DATASET_LOCKED` | Dataset state prevents operation. | No handle; audit lock conflict. |
| `MFOS_ERR_IMMUTABLE` | Immutable catalog entry or dataset mutation denied. | No mutation; audit denial. |
| `MFOS_ERR_RETENTION_DENIED` | Retention policy blocks delete or purge. | No deletion; audit retention denial. |
| `MFOS_ERR_STALE_HANDLE` | Handle generation or expiry no longer valid. | Revoke handle; audit stale-use attempt. |
| `MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE` | Audit obligation cannot be met. | Fail closed. |
| `MFOS_ERR_INTERNAL_CORRUPTION` | Catalog or integrity metadata inconsistent. | Lock affected objects; start recovery flow. |
| `MFOS_ERR_ENCRYPTION_POLICY_UNAVAILABLE` | Required encryption/key-service profile is unavailable or unspecified. | Fail closed when encryption is required; do not silently downgrade to unencrypted access. |
| `MFOS_ERR_SPEC_GAP` | Requested behavior is not specified. | Do not implement success path. |

## 11. Positive Tests

- Define `USER.ALICE.INPUT` as owner `ALICE`, type `SEQ`, committed catalog entry exists.
- Resolve `USER.ALICE.INPUT` and verify generation and location are returned.
- Open `USER.ALICE.INPUT` for READ as `ALICE`; handle is active and bound to current policy version.
- Verify the active handle contains an `ObjectGenerationBinding` matching committed catalog and dataset generations.
- Close an active read handle; audit record contains bytes read and correlation ID.
- Update catalog metadata; generation increments and old generation is rejected.
- Delete an expired temporary dataset; retention allows deletion and audit records deletion.
- Recover from crash after `WRITE_JOURNAL` before `COMMIT_ENTRY`; incomplete entry is rolled back.
- Validate CatalogEntry, Dataset, DatasetHandle, and ObjectGenerationBinding examples against the Phase 0.8 schemas.

## 12. Negative Tests

- `BOB` attempts READ on `USER.ALICE.INPUT`; no handle is created and denial is audited first.
- Malformed DSN `USER/ALICE/INPUT` returns `MFOS_ERR_INVALID_DSN`.
- Dataset open attempts to bypass catalogd using a raw volume reference; request is denied.
- Open with stale `policy_version`; returns `MFOS_ERR_POLICY_VERSION_MISMATCH`.
- Use a handle after catalog generation changes; returns `MFOS_ERR_STALE_HANDLE`.
- Attempt to modify immutable system dataset catalog entry; returns `MFOS_ERR_IMMUTABLE`.
- Attempt to unset `immutable` on a committed system dataset; returns `MFOS_ERR_IMMUTABLE`.
- Auditd unavailable during protected open; returns `MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE`.
- Integrity tag mismatch on open; no handle is created.
- Retention policy blocks delete; dataset remains active and denial is audited.
- Required encryption profile is marked `KEY_SERVICE_PLACEHOLDER`; access fails closed when the operation requires configured encryption.
- Crash during catalog commit; recovery leaves either old committed entry or new committed entry, never partial success.
- Resolve uncommitted catalog entry; returns `MFOS_ERR_CATALOG_NOT_FOUND` or fail-closed equivalent and no dataset handle.
- Resolve rolled-back catalog entry; returns `MFOS_ERR_CATALOG_NOT_FOUND` and no dataset handle.
- Resolve partially written journal entry; returns `MFOS_ERR_INTERNAL_CORRUPTION` or enters recovery, and no dataset handle.
- Resolve entry whose `integrity_tag` does not match; returns `MFOS_ERR_INTERNAL_CORRUPTION` and no dataset handle.

## 13. Fuzz Decisions

- `fuzz_dsn_parser`: random DSNs, Unicode bytes, separators, overlong qualifiers, empty qualifiers.
- `fuzz_catalog_entry_decode`: malformed catalog records, truncated records, invalid generations.
- `fuzz_dataset_manifest`: attributes, retention, encryption, and integrity policy references.
- `fuzz_dataset_open_request`: invalid subject, object, operation, context, and stale policy versions.
- `fuzz_recovery_journal`: torn writes, reordered records, duplicate commits, orphan extents.
- `fuzz_object_generation_binding`: stale, missing, caller-forged, and mismatched generation snapshots.

Fuzz target requirements:

- No panic on malformed input.
- No success for invalid DSN.
- No handle creation unless authorization and audit obligations are satisfied.
- No catalog resolve success unless the entry is committed and integrity-verified.
- Corpus MUST include valid examples from the positive test path.
- Encryption fuzzing in Phase 0.8 is limited to policy-reference validation. Cryptographic implementation fuzzing is deferred until the key-service ABI exists.

## 14. Evidence Requirements

Phase 0.8 evidence MUST remain design/test evidence until production implementation is authorized.

Required evidence artifacts:

- Schema validation evidence for `schemas/mfos/dataset.schema.yml`, `schemas/mfos/catalog-entry.schema.yml`, `schemas/mfos/dataset-handle.schema.yml`, and `schemas/mfos/object-generation-binding.schema.yml`.
- Catalog transaction model-check or reviewed transition trace evidence showing that uncommitted, rolled-back, partial-journal, and integrity-failed entries never resolve.
- Dataset open model-check or reviewed transition trace evidence showing no ACTIVE handle without committed catalog resolution, authorization, audit obligation, generation binding, and integrity verification.
- Positive and negative test plan evidence from `tests/catalog/dataset-catalog.yml`.
- Crash recovery evidence for torn journal, duplicate commit, missing audit marker, orphan extent, and integrity-tag mismatch cases.
- Audit evidence samples for catalog resolve deny, dataset open allow, dataset open deny, stale handle, immutable system dataset denial, retention denial, and integrity failure.
- Fuzz decision evidence listing enabled targets, deferred targets, seed corpus paths, and minimum acceptance criteria.

## 15. Spec Gaps

- Future DSN grammar extensions beyond the frozen Phase 0.8 uppercase qualifier subset.
- Full record-format behavior for `FB`, `VB`, and future blocked formats.
- PDS_LITE member namespace and concurrency model.
- Volume manager interface and extent allocator ABI.
- Encryption key service ABI, cryptographic provider selection, and profile-specific failure policy details beyond the placeholder fail-closed rule.
- Backup hook ABI.
- Dataset migration behavior.
- Secure deletion guarantees on SSD, object storage, and virtual disks.
- Multi-partition catalog replication.

## 16. Inactive Future Implementation Prompt Template

Phase status: inactive future template. This section does not authorize production implementation, hosted daemon implementation, or portable semantic-core implementation.

```text
Future authorized implementation agents would implement MFOS catalogd/datasetd behavior.

Use these spec IDs:
- MFOS-REQ-CATALOG-0001 through MFOS-REQ-CATALOG-0008
- MFOS-REQ-DATASET-0001 through MFOS-REQ-DATASET-0008

Source Matrix IDs:
- EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001
- EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001
- EXTREF-IBM-ZOS-SECURITY-SERVER-0001
- EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001
- EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001
- EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001

Rules:
- Do not claim z/OS compatibility.
- Dataset is not a POSIX file wrapper.
- catalogd resolves only committed catalog entries.
- CatalogEntry, Dataset, DatasetHandle, and ObjectGenerationBinding schemas are design contracts.
- datasetd MUST call securityd before creating a protected handle.
- DENY MUST be audited before returning the result.
- A protected handle requires committed catalog resolution, generation binding, integrity verification, and audit obligation establishment.
- Unsupported behavior returns MFOS_ERR_UNSUPPORTED.
- Unspecified behavior returns MFOS_ERR_SPEC_GAP.
- No fake success, empty stubs, or silent fallback.

Deliver:
1. Implemented requirement IDs
2. Source Matrix IDs
3. Assumptions
4. Spec gaps
5. Unsupported features
6. Security invariants
7. Audit obligations
8. Failure modes
9. Tests added
10. Negative tests added
11. Fuzz targets added
12. Unsafe code justification
13. Review checklist
14. Evidence artifacts
```

## Phase 0.8 Core Semantics Freeze

This section freezes the Dataset/Catalog semantics for Phase 0.8. It is a design-level freeze only and does not authorize production implementation, hosted daemon implementation, Portable Semantic Core implementation, or executable specs.

### Frozen Requirement Set

- `MFOS-REQ-CATALOG-0101`
- `MFOS-REQ-CATALOG-0102`
- `MFOS-REQ-DATASET-0101`
- `MFOS-REQ-DATASET-0102`
- `MFOS-REQ-DATASET-0103`

### Machine-Readable Artifacts

- Pack contract: `docs/design/packs/PACK-07-*/pack.yml`
- State machine: `formal/tla/dataset-open/state-machine.yml and formal/tla/catalog-transaction/state-machine.yml`
- Test catalog: `tests/catalog/dataset-catalog.yml`
- Requirement mirror: `requirements/by-domain/`
- Evidence traceability: `evidence/traceability/current/`

### Freeze Rules

- Undefined behavior returns `MFOS_ERR_SPEC_GAP`.
- Specified but unimplemented behavior returns `MFOS_ERR_UNSUPPORTED`.
- Deny paths with audit obligations must define deny-before-return behavior.
- Security-sensitive behavior requires a negative test catalog entry.
- No fake success, empty stub, or silent fallback is allowed.
