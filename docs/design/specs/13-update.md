---
spec_id: "MFOS-SPEC-13-UPDATE"
title: "MFOS Update Verification Specification v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001", "MS-VBS-001", "MS-VSM-001", "NIST-193-001", "NIST-218-001", "SLSA-001", "TCG-001", "TUF-001"]
requirement_refs: ["MFOS-REQ-UPDATE-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Update Verification Specification v0.1

Status: Draft  
Owner: MFOS architecture  
Profile applicability: Baseline, Enterprise-Standalone, Enterprise-PXM, High-Assurance  
Source basis: user-provided MFOS Source-Grounded High-Assurance Architecture v0.3

## 1. Purpose

This document specifies UVS, the MFOS Update Verification Service.

UVS verifies update metadata and artifacts before staging or activation. Its job is to prevent unauthorized update, rollback, freeze, mix-and-match, stale security epoch, dependency confusion, and unsigned artifact installation.

MFOS update verification is source-grounded and high-assurance oriented. It does not claim compatibility with z/OS SMP/E, z/OS HOLDDATA, Windows Update, Linux package managers, or any other update ecosystem.

## 2. Scope

UVS covers:

- Update metadata verification.
- Artifact manifest verification.
- Signature, hash, size, generation, and security epoch checks.
- Rollback, freeze, and mix-and-match detection.
- Dependency and conflict checks.
- Profile-specific activation requirements.
- Staged activation profile updates.
- Audit obligations.
- Recovery rollback workflow.
- High-Assurance Guard root interaction.
- Failure modes, tests, negative tests, fuzz targets, and open spec gaps.

## 3. Non-Objectives

UVS MUST NOT:

- Decide normal dataset access policy.
- Decide job scheduling or workload policy.
- Replace securityd.
- Replace auditd.
- Parse arbitrary vendor package formats.
- Trust transport security as sufficient update integrity.
- Treat checksum-only verification as security verification.
- Activate unsigned artifacts.
- Silently downgrade security policy.
- Claim SMP/E compatibility.

## 4. Source Matrix References

Required source IDs for this spec:

- TUF-001: root, targets, snapshot, timestamp role separation; rollback, freeze, mix-and-match, and key-compromise resistance.
- SLSA-001: provenance expectations for release artifacts.
- NIST-218-001: secure software development baseline.
- NIST-193-001: firmware resilience and recovery framing.
- TCG-001: measured boot and TPM event-log reference.
- EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001: update advisory model inspiration only; no compatibility claim.
- EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001: system integrity claim discipline.
- MS-VBS-001: executable mapping reference for High-Assurance profile only.
- MS-VSM-001: Guard root protection reference for High-Assurance profile only.
- FBVBS-001: signed manifest, freshness, production proof obligations, and no-fake-success discipline.

## 5. Terminology

UVS:
  Update Verification Service.

Update bundle:
  Collection of update metadata and target artifacts presented as one candidate update transaction.

Artifact manifest:
  Signed metadata for one MFOS component artifact.

Root metadata:
  Metadata that defines trusted update keys and roles.

Targets metadata:
  Metadata that binds target component IDs to hashes, sizes, versions, and custom MFOS constraints.

Snapshot metadata:
  Metadata that binds a consistent set of metadata versions.

Timestamp metadata:
  Fresh metadata with short expiry used to detect freeze attacks.

Security epoch:
  Monotonic integer used to reject stale security-critical updates, keys, policies, modules, and rollback attempts.

Activation profile update:
  Change to boot, partition, service, Guard, or component activation constraints.

Staged update:
  Verified update that is persisted but not active.

Committed update:
  Update that has been activated, measured, audited, and accepted as the current generation.

## 6. Update Trust Boundaries

Update crosses these boundaries:

- External distribution source to UVS.
- UVS to securityd for authorization and approval workflow.
- UVS to auditd for evidence.
- UVS to catalogd/datasetd or artifact store for staged artifact persistence.
- UVS to amfd for AMF module updates.
- UVS to nucleus for service/nucleus activation.
- UVS to PXM for partition and activation profile updates.
- UVS to PXM Guard in High-Assurance profile.
- UVS to recovery partition for rollback and repair workflow.

Transport MAY provide confidentiality or availability, but transport MUST NOT be the root of update integrity.

## 7. Component Types

UVS supports these component types:

```text
nucleus
trusted_service
amf_module
policy_bundle
catalog_schema
operator_command_set
pxm_core
pxm_guard
recovery_image
firmware_advisory
source_matrix_bundle
conformance_test_bundle
```

Unsupported component types MUST return `MFOS_ERR_UNSUPPORTED`. Undefined component types MUST return `MFOS_ERR_SPEC_GAP`.

## 8. Update Artifact Manifest

```yaml
UpdateArtifactManifest:
  manifest_version: 1
  component_type: nucleus | trusted_service | amf_module | policy_bundle | catalog_schema | operator_command_set | pxm_core | pxm_guard | recovery_image | firmware_advisory | source_matrix_bundle | conformance_test_bundle
  component_id: string
  component_version: semver
  target_arch: x86_64
  target_vendor: intel | amd | any
  required_cpu_features:
    - nx
    - smep?
    - smap?
    - cet?
    - pku?
    - pks?
    - iommu?
  profile_applicability:
    - Baseline
    - Enterprise-Standalone
    - Enterprise-PXM
    - High-Assurance
  hash:
    algorithm: sha384
    value: hex
  size: uint64
  generation: uint64
  security_epoch: uint64
  dependencies:
    - component_id: string
      min_version: semver
      max_version: semver?
  conflicts:
    - component_id: string
      min_version: semver?
      max_version: semver?
  signing_key_id: string
  signature: string
  revocation_refs:
    - string
  rollback_policy:
    min_generation: uint64
    min_security_epoch: uint64
  guard_required: bool
  activation_profile_constraints:
    - string
  reboot_required: bool
  recovery_required: bool
  audit_class: UPDATE_SECURITY_CRITICAL | UPDATE_NORMAL | UPDATE_RECOVERY
  source_matrix_refs:
    - TUF-001
    - SLSA-001
```

## 9. Update Bundle Metadata

```yaml
UpdateBundle:
  bundle_id: string
  metadata_version: uint64
  created_at: timestamp
  expires_at: timestamp
  root_metadata_ref: string
  timestamp_metadata_ref: string
  snapshot_metadata_ref: string
  targets_metadata_ref: string
  target_manifests:
    - UpdateArtifactManifest
  required_security_epoch: uint64
  consistent_snapshot_id: string
  distribution_channel: stable | emergency | recovery | test
  profile_applicability:
    - Baseline
    - Enterprise-Standalone
    - Enterprise-PXM
    - High-Assurance
  source_matrix_refs:
    - TUF-001
```

## 10. Update Verification API and ABI

### 10.1 UVS_VERIFY_BUNDLE

```yaml
UVSVerifyBundleRequest:
  subject: SubjectRef
  bundle_ref: ArtifactRef
  profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  current_generation: uint64
  current_security_epoch: uint64
  current_policy_version: uint64
  activation_profile_hash: sha384
  nonce: bytes?
  correlation_id: uuid
```

```yaml
UVSVerifyBundleResponse:
  status: MFOS_OK | MFOS_ERR_*
  reason_code: string
  verified_bundle_id: string?
  target_count: uint32
  required_approvals:
    - securityd
    - operator_confirmation
    - dual_control
    - guard
  staged_update_token: string?
  audit_record_id: uuid
```

### 10.2 UVS_STAGE_UPDATE

```yaml
UVSStageUpdateRequest:
  verified_bundle_id: string
  subject: SubjectRef
  storage_target: DatasetRef | ArtifactStoreRef
  correlation_id: uuid
```

```yaml
UVSStageUpdateResponse:
  status: MFOS_OK | MFOS_ERR_*
  reason_code: string
  staged_update_id: string?
  staged_generation: uint64?
  audit_record_id: uuid
```

### 10.3 UVS_ACTIVATE_UPDATE

```yaml
UVSActivateUpdateRequest:
  staged_update_id: string
  subject: SubjectRef
  activation_window: immediate | next_boot | recovery_boot
  approvals:
    - ApprovalRef
  correlation_id: uuid
```

```yaml
UVSActivateUpdateResponse:
  status: MFOS_OK | MFOS_ERR_*
  reason_code: string
  activation_transaction_id: string?
  reboot_required: bool
  audit_record_id: uuid
```

### 10.4 UVS_COMMIT_UPDATE

```yaml
UVSCommitUpdateRequest:
  activation_transaction_id: string
  measured_components:
    - component_id: string
      digest: sha384
      generation: uint64
      security_epoch: uint64
  boot_measurement_context: sha384?
  guard_attestation_ref: string?
  correlation_id: uuid
```

```yaml
UVSCommitUpdateResponse:
  status: MFOS_OK | MFOS_ERR_*
  reason_code: string
  committed_generation: uint64?
  committed_security_epoch: uint64?
  audit_record_id: uuid
```

## 11. Update Lifecycle State Machine

```text
RECEIVE_METADATA
  -> VERIFY_ROOT
  -> VERIFY_TIMESTAMP
  -> VERIFY_SNAPSHOT
  -> VERIFY_TARGETS
  -> VERIFY_MANIFESTS
  -> VERIFY_ARTIFACT_HASH_SIZE
  -> CHECK_SIGNATURES
  -> CHECK_REVOCATION
  -> CHECK_GENERATION
  -> CHECK_SECURITY_EPOCH
  -> CHECK_DEPENDENCIES
  -> CHECK_CONFLICTS
  -> CHECK_PROFILE_APPLICABILITY
  -> SECURITYD_AUTHORIZE
  -> GUARD_APPROVE?          [High-Assurance or guard_required]
  -> STAGE
  -> APPROVE
  -> ACTIVATE_PROFILE_UPDATE
  -> REBOOT_OR_SWITCH
  -> MEASURE
  -> COMMIT
```

Failure states:

```text
METADATA_MISSING
ROOT_INVALID
TIMESTAMP_EXPIRED
SNAPSHOT_INCONSISTENT
TARGETS_INVALID
MANIFEST_INVALID
HASH_MISMATCH
SIZE_MISMATCH
SIGNATURE_INVALID
REVOCATION_UNKNOWN
REVOKED
ROLLBACK_DETECTED
FREEZE_DETECTED
MIX_AND_MATCH_DETECTED
GENERATION_STALE
SECURITY_EPOCH_STALE
DEPENDENCY_UNSATISFIED
CONFLICT_DETECTED
PROFILE_NOT_APPLICABLE
SECURITY_DENIED
GUARD_REQUIRED
GUARD_DENIED
STAGE_FAILED
ACTIVATION_FAILED
MEASUREMENT_MISMATCH
COMMIT_FAILED
RECOVERY_REQUIRED
UNSUPPORTED
SPEC_GAP
```

Invalid update lifecycle transitions:

| Attempted transition | Required result |
| --- | --- |
| `RECEIVE_METADATA -> VERIFY_TARGETS` without `VERIFY_ROOT`, `VERIFY_TIMESTAMP`, and `VERIFY_SNAPSHOT` | Return `MFOS_ERR_SPEC_GAP` or the specific metadata error; no stage. |
| `VERIFY_TIMESTAMP` with expired or stale timestamp followed by `VERIFY_SNAPSHOT`, `STAGE`, or `ACTIVATE_PROFILE_UPDATE` | Return `MFOS_ERR_FREEZE_DETECTED`; no stage or activation. |
| `VERIFY_TARGETS -> STAGE` without a verified snapshot-consistent targets view | Return `MFOS_ERR_MIX_AND_MATCH_DETECTED`; no stage. |
| `VERIFY_MANIFESTS -> STAGE` without `VERIFY_ARTIFACT_HASH_SIZE` and `CHECK_SIGNATURES` | Return signature, hash, or size error; no stage. |
| `CHECK_GENERATION` failure followed by `STAGE` or `ACTIVATE_PROFILE_UPDATE` | Return `MFOS_ERR_ROLLBACK_DETECTED`; no stage or activation. |
| `CHECK_SECURITY_EPOCH` failure followed by `STAGE` or `ACTIVATE_PROFILE_UPDATE` | Return `MFOS_ERR_ROLLBACK_DETECTED`; no stage or activation. |
| `SECURITYD_AUTHORIZE` deny followed by `STAGE` or `APPROVE` | Return `MFOS_ERR_POLICY_DENIED`; no stage or approval. |
| `GUARD_APPROVE?` required but skipped before `ACTIVATE_PROFILE_UPDATE` | Return `MFOS_ERR_GUARD_REQUIRED`; no activation. |
| `STAGE -> ACTIVATE_PROFILE_UPDATE` without `APPROVE` | Return `MFOS_ERR_UNAUTHORIZED`; no activation. |
| `ACTIVATE_PROFILE_UPDATE -> COMMIT` without `MEASURE` | Enter recovery workflow; do not commit. |
| `MEASURE` mismatch followed by `COMMIT` | Enter recovery workflow; do not commit. |

## 12. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-UPDATE-0001 | UVS MUST verify update metadata before artifact trust. | metadata test |
| MFOS-REQ-UPDATE-0002 | UVS MUST verify artifact signature, hash, and size. | artifact test |
| MFOS-REQ-UPDATE-0003 | UVS MUST verify generation and security epoch. | rollback test |
| MFOS-REQ-UPDATE-0004 | UVS MUST reject rollback attempts. | negative test |
| MFOS-REQ-UPDATE-0005 | UVS MUST reject freeze attacks using timestamp expiry or freshness policy. | freeze test |
| MFOS-REQ-UPDATE-0006 | UVS MUST reject mix-and-match metadata views. | consistency test |
| MFOS-REQ-UPDATE-0007 | UVS MUST reject revoked targets, keys, signers, and security epochs. | revocation test |
| MFOS-REQ-UPDATE-0008 | UVS MUST check dependencies and conflicts before staging. | dependency test |
| MFOS-REQ-UPDATE-0009 | UVS MUST stage verified artifacts before activation. | integration test |
| MFOS-REQ-UPDATE-0010 | UVS MUST bind staged update state to bundle ID, generation, security epoch, target digests, and policy version. | state test |
| MFOS-REQ-UPDATE-0011 | UVS MUST require securityd authorization before staging security-sensitive updates. | integration test |
| MFOS-REQ-UPDATE-0012 | UVS MUST require audit records for verify, stage, activate, commit, rollback, and failure events. | audit test |
| MFOS-REQ-UPDATE-0013 | High-Assurance update roots and activation profile transitions MUST be Guard-approved and Guard-sealed. | Guard test |
| MFOS-REQ-UPDATE-0014 | UVS MUST NOT trust transport security as artifact integrity. | architecture review |
| MFOS-REQ-UPDATE-0015 | UVS MUST NOT activate unsigned artifacts. | negative test |
| MFOS-REQ-UPDATE-0016 | UVS MUST distinguish unsupported component types from spec gaps. | error test |
| MFOS-REQ-UPDATE-0017 | UVS MUST provide a recovery rollback workflow for failed activation. | recovery drill |
| MFOS-REQ-UPDATE-0018 | UVS MUST produce evidence suitable for production readiness gates. | evidence review |
| MFOS-REQ-UPDATE-0019 | UVS MUST reject activation when measured component digests do not match verified manifests. | measurement test |
| MFOS-REQ-UPDATE-0020 | UVS MUST fail closed for security-critical update ambiguity. | no-fake-success CI |

## 13. Invariants

```text
INV-UVS-001:
  No artifact MAY be staged unless metadata role verification, manifest
  verification, signature verification, hash/size verification, revocation,
  generation, security_epoch, dependency, conflict, profile, securityd, and
  required audit checks have succeeded.

INV-UVS-002:
  No update MAY be activated unless it was previously staged from the same
  verified bundle ID, target digest set, generation, security_epoch, and
  policy_version.

INV-UVS-003:
  Committed generation and committed security_epoch MUST be monotonic except
  for an explicit recovery workflow that is separately authorized, audited,
  and profile-approved.

INV-UVS-004:
  Timestamp expiry or freshness failure prevents normal activation.

INV-UVS-005:
  A snapshot/targets mismatch prevents staging and activation.

INV-UVS-006:
  High-Assurance update root transition is not authoritative unless
  Guard-approved and auditd-recorded.
```

## 14. Securityd Obligations

securityd MUST decide:

- Whether the subject MAY verify, stage, activate, commit, or rollback updates.
- Whether the update is security-critical.
- Whether dual control or operator confirmation is required.
- Whether emergency or recovery channel use is allowed.
- Whether a policy bundle MAY replace the current policy.
- Whether an AMF module update MAY proceed to amfd.
- Whether profile downgrade is allowed. Default is deny.

Decision input:

```yaml
UpdateAuthorizationRequest:
  subject: SubjectRef
  operation: VERIFY | STAGE | ACTIVATE | COMMIT | ROLLBACK | RECOVERY
  bundle_id: string
  component_ids:
    - string
  component_types:
    - string
  generation: uint64
  security_epoch: uint64
  current_generation: uint64
  current_security_epoch: uint64
  policy_version: uint64
  profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  distribution_channel: stable | emergency | recovery | test
  correlation_id: uuid
```

## 15. Audit Obligations

Update audit records MUST include:

- `schema_version`.
- `record_id`.
- `timestamp_utc`.
- `component_id = uvsd`.
- `correlation_id`.
- `subject`.
- `operation`.
- `bundle_id`.
- `component_ids`.
- `component_types`.
- `decision`.
- `reason_code`.
- `policy_version`.
- `generation`.
- `security_epoch`.
- `metadata_versions`.
- `target_digests`.
- `activation_profile_hash`.
- `measurement_context` when available.
- `guard_seal_version` when applicable.
- `previous_hash`.
- `record_hash`.

Events that MUST be audited:

- Metadata received.
- Metadata verification success or failure.
- Signature/hash/size success or failure.
- Revocation decision.
- Rollback/freeze/mix-and-match detection.
- Dependency or conflict failure.
- Securityd decision.
- Guard decision.
- Stage start and completion.
- Activation start and completion.
- Measurement mismatch.
- Commit.
- Recovery rollback.

DENY or failure results MUST be audited before returning the final result. If audit is unavailable for a security-critical update, UVS MUST fail closed or enter profile-defined recovery mode; it MUST NOT return normal update success.

## 16. Failure Modes

| Failure | Required behavior |
| --- | --- |
| Metadata missing | Return `MFOS_ERR_INVALID_PARAMETER`; no stage. |
| Root metadata invalid | Return `MFOS_ERR_POLICY_DENIED`; no stage. |
| Timestamp expired | Return `MFOS_ERR_FREEZE_DETECTED`; no stage. |
| Snapshot mismatch | Return `MFOS_ERR_MIX_AND_MATCH_DETECTED`; no stage. |
| Target hash mismatch | Return `MFOS_ERR_INTERNAL_CORRUPTION`; no stage. |
| Invalid artifact signature | Return `MFOS_ERR_AMF_SIGNATURE_INVALID` for AMF module or typed signature error for other component; no stage. |
| Generation rollback | Return `MFOS_ERR_ROLLBACK_DETECTED`; no stage. |
| Security epoch stale | Return `MFOS_ERR_ROLLBACK_DETECTED`; no stage. |
| Revocation metadata unavailable | Enterprise-Standalone/Enterprise-PXM/High-Assurance fail closed for security-critical updates. |
| Dependency unsatisfied | Return `MFOS_ERR_POLICY_DENIED`; no stage. |
| Conflict detected | Return `MFOS_ERR_POLICY_DENIED`; no stage. |
| Profile downgrade | Deny unless explicit recovery workflow authorizes it. |
| Audit unavailable | Security-critical update fails closed or enters recovery mode by profile. |
| Guard required but unavailable | Return `MFOS_ERR_GUARD_REQUIRED`; High-Assurance activation denied. |
| Measurement mismatch after boot | Enter recovery workflow; do not commit. |
| Commit journal corrupt | Enter recovery workflow; audit if possible. |

## 17. Positive Tests

- `uvs_valid_bundle_verifies`.
- `uvs_valid_bundle_stages`.
- `uvs_valid_staged_update_activates_next_boot`.
- `uvs_commit_matches_measured_digests`.
- `uvs_enterprise_revocation_metadata_valid`.
- `uvs_securityd_allows_authorized_operator_activation`.
- `uvs_high_assurance_guard_approved_update_commits`.
- `uvs_recovery_rollback_authorized_and_audited`.

## 18. Negative Tests

- `uvs_rejects_unsigned_artifact`.
- `uvs_rejects_invalid_signature`.
- `uvs_rejects_hash_mismatch`.
- `uvs_rejects_size_mismatch`.
- `uvs_rejects_expired_timestamp`.
- `uvs_rejects_snapshot_targets_mismatch`.
- `uvs_rejects_rollback_generation`.
- `uvs_rejects_stale_security_epoch`.
- `uvs_rejects_mix_and_match_metadata`.
- `uvs_rejects_missing_revocation_for_security_critical_update`.
- `uvs_rejects_revoked_signer`.
- `uvs_rejects_revoked_target_digest`.
- `uvs_rejects_dependency_unsatisfied`.
- `uvs_rejects_conflicting_component`.
- `uvs_rejects_profile_downgrade_without_recovery`.
- `uvs_rejects_activation_without_staging`.
- `uvs_rejects_commit_on_measurement_mismatch`.
- `uvs_fails_closed_when_securityd_unavailable`.
- `uvs_fails_closed_when_audit_required_but_unavailable`.
- `uvs_high_assurance_rejects_without_guard_approval`.
- `uvs_rejects_fake_success_for_unknown_component_type`.

## 19. Fuzz Targets

- `fuzz_update_root_metadata`.
- `fuzz_update_timestamp_metadata`.
- `fuzz_update_snapshot_metadata`.
- `fuzz_update_targets_metadata`.
- `fuzz_update_artifact_manifest_yaml`.
- `fuzz_update_artifact_manifest_json`.
- `fuzz_update_dependency_solver`.
- `fuzz_update_revocation_metadata`.
- `fuzz_update_bundle_decoder`.
- `fuzz_update_journal_recovery`.

Fuzz targets MUST never accept malformed metadata as valid. Parser failures MUST be explicit typed errors.

## 20. Conformance Profiles

### Baseline

- Signed artifacts required.
- Hash and size checks required.
- Basic generation check required.
- Local audit required.
- TUF-like metadata MAY be minimal.
- Recovery workflow MAY be manual.

### Enterprise-Standalone

- TUF-like root/timestamp/snapshot/targets metadata required.
- Revocation metadata required.
- Security epoch required.
- Remote audit export required.
- SBOM and signed provenance required for release artifacts.
- Rollback/freeze/mix-and-match tests required.

### Enterprise-PXM

- All Enterprise-Standalone update requirements apply.
- Activation profile updates must include PXM partition context where applicable.
- PXM or boot audit sink must record partition-impacting update activation.

### High-Assurance

- Guard-sealed update root required.
- Guard approval required for security-critical activation.
- Remote attestation evidence required.
- Recovery workflow MUST preserve audit chain or explicitly record break in recovery evidence.
- Production claim requires evidence artifacts.

## 21. Recovery Workflow

```text
DETECT_ACTIVATION_FAILURE
  -> ENTER_RECOVERY_MODE
  -> LOAD_RECOVERY_PARTITION_OR_IMAGE
  -> VERIFY_LAST_KNOWN_GOOD_METADATA
  -> SECURITYD_AUTHORIZE_RECOVERY
  -> GUARD_APPROVE?              [High-Assurance]
  -> RESTORE_LAST_KNOWN_GOOD
  -> MEASURE_RESTORED_COMPONENTS
  -> AUDIT_RECOVERY
  -> RESUME_OR_OPERATOR_READY
```

Recovery MUST NOT silently downgrade security epoch. Any authorized rollback MUST be explicitly marked as recovery, audited, and excluded from normal monotonic update success metrics.

## 22. Evidence Artifacts

UVS implementations MUST produce:

- Verified bundle report.
- Manifest verification report.
- Signature verification report.
- Revocation check report.
- Rollback/freeze/mix-and-match test report.
- Dependency/conflict report.
- Activation transaction journal.
- Measurement comparison report.
- Audit record IDs.
- Guard approval or denial evidence for High-Assurance.
- Recovery drill report for production readiness.

## 23. Spec Gaps

- Concrete metadata wire format is not fixed.
- Concrete signature algorithms, threshold rules, and key rotation are not fixed.
- Policy bundle semantic validation is not specified here.
- Firmware update execution is out of scope; only firmware advisory and resilience hooks are referenced.
- Distributed update mirror selection is not specified.
- Delta update format is not specified.
- Online service restart orchestration is not fully specified.
- Recovery partition implementation is not specified here.
- Exact SBOM format and provenance attestation format are not fixed.

## 24. Inactive Future Implementation Prompt Template

Phase status: inactive future template. This section does not authorize production implementation, hosted daemon implementation, or portable semantic-core implementation.

```text
Future authorized implementation agents would implement MFOS UVS, the Update Verification Service.

Implement only the requirement IDs listed in the task. Do not claim z/OS,
SMP/E, Windows Update, or Linux package-manager compatibility.

Required output:
1. Implemented Requirement IDs
2. Source Matrix IDs
3. Assumptions
4. Spec Gaps
5. Unsupported Features
6. Security Invariants
7. Audit Obligations
8. Failure Modes
9. Tests Added
10. Negative Tests Added
11. Fuzz Targets Added
12. Unsafe Code Justification
13. Review Checklist
14. Evidence Artifacts

Rules:
- Verify metadata before trusting artifacts.
- Verify signatures, hashes, sizes, generations, and security epochs.
- Reject rollback, freeze, and mix-and-match attempts.
- Use securityd for authorization.
- Use auditd for all update decisions and state transitions.
- Use Guard for High-Assurance update roots and activation transitions.
- Do not treat transport security as artifact integrity.
- Do not return success for missing, unsupported, or undefined behavior.
- Use MFOS_ERR_UNSUPPORTED for specified but unimplemented features.
- Use MFOS_ERR_SPEC_GAP for unspecified behavior.
- Add negative tests and fuzz targets with parser or verifier code.
```
