---
spec_id: "MFOS-SPEC-31-RELEASE-DISTRIBUTION-ROLLBACK"
title: "MFOS Design Specification 31: Release Distribution and Rollback"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-Z-DPM-0001", "EXTREF-IBM-Z-LPAR-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "MS-VBS-001", "MS-VSM-001", "NIST-193-001", "NIST-218-001", "SLSA-001", "TCG-001", "TUF-001"]
requirement_refs: ["MFOS-REQ-DIST-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Design Specification 31: Release Distribution and Rollback

Status: Draft v0.1

Audience: update engineers, release managers, recovery engineers, operators, security reviewers, evidence auditors, implementation agents

MFOS is source-grounded and z/OS-inspired. This specification defines MFOS release distribution and rollback behavior. It does not claim z/OS compatibility, z/Architecture compatibility, IBM API compatibility, RACF compatibility, JES compatibility, DFSMS compatibility, SMP/E compatibility, or IBM product compatibility.

## 1. Purpose

This document defines how MFOS release artifacts move from a reviewed release candidate into controlled distribution channels, how MFOS stages and activates those artifacts, and how rollback or recovery is authorized when activation fails or when a release is withdrawn.

It complements:

- [13-update.md](13-update.md), which defines UVS verification of signed metadata and artifacts.
- [25-operations-recovery.md](25-operations-recovery.md), which defines operational recovery and recovery partition behavior.
- [release-review-workflow.md](../assurance/release-review-workflow.md), which defines release review and independent approval.
- [evidence-archive-spec.md](../assurance/evidence-archive-spec.md), which defines release evidence storage.

## 2. Scope

In scope:

- Release artifact channels.
- TUF-like signed metadata relationships.
- UVS interaction.
- Distribution manifest schema.
- Activation profile update handling.
- Staged rollout states.
- Rollback authorization.
- Recovery partition coordination.
- Audit obligations.
- Failure modes.
- Positive and negative tests.
- Evidence artifacts.
- Spec gaps.
- AI implementation prompt.

Out of scope:

- External package manager compatibility.
- Vendor-specific update network protocols.
- Full CDN implementation.
- Customer notification process.
- Incident response beyond release rollback coordination.
- Runtime hot patching.
- Live migration.
- Legal approval process.

## 3. Source Matrix References

| Source ID | Use |
| --- | --- |
| `TUF-001` | TUF-like metadata roles, rollback, freeze, mix-and-match, key compromise, consistent snapshot reference. |
| `SLSA-001` | Provenance and artifact integrity for release distribution. |
| `NIST-218-001` | Secure software development practice and release discipline. |
| `NIST-193-001` | Firmware/platform resilience framing for recovery and rollback. |
| `TCG-001` | Measured boot, TPM event log, and attestation evidence interaction. |
| `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001` | System integrity claim discipline and unauthorized bypass prevention. |
| `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001` | Audit/accounting evidence inspiration. |
| `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `EXTREF-IBM-Z-DPM-0001` | Partition and recovery partition operational inspiration. |
| `MS-VBS-001`, `MS-VSM-001` | High-Assurance Guard root and executable mapping reference only. |
| `FBVBS-001` | Internal state-machine, signed manifest, evidence, production proof, and no-fake-success discipline. |

## 4. Non-Compatibility Statement

MFOS release distribution and rollback are MFOS-defined workflows. They are not SMP/E, HOLDDATA, z/OSMF, RACF, JES, DFSMS, Windows Update, Linux package manager, or cloud package repository compatibility layers.

Allowed wording:

- "TUF-like MFOS release metadata."
- "MFOS UVS release verification."
- "MFOS recovery partition rollback workflow."
- "High-Assurance Guard-approved activation profile transition."

Prohibited wording:

- "z/OS-compatible update."
- "SMP/E-compatible rollback."
- "HOLDDATA-compatible advisory."
- "RACF-compatible update authorization."
- "Windows Update-compatible MFOS release."

## 5. Design Principles

`DIST-PRIN-0001` Metadata before artifact trust:
  MFOS distribution clients, operators, and UVS MUST verify signed metadata before trusting release artifacts.

`DIST-PRIN-0002` Transport is not integrity:
  TLS, VPN, mirror pinning, or private network placement MUST NOT be treated as release artifact integrity.

`DIST-PRIN-0003` Rollback is recovery, not ordinary downgrade:
  Rollback to an older generation or security epoch is denied unless an approved recovery policy, signed metadata, authorization decision, and audit obligation permit it.

`DIST-PRIN-0004` Activation profile is a protected object:
  Boot, partition, service, Guard, device, and recovery activation profile changes MUST be signed, staged, authorized, audited, and profile-checked.

`DIST-PRIN-0005` Staged rollout is explicit:
  Canary, ring, and emergency rollout state MUST be represented in release metadata and audit records.

`DIST-PRIN-0006` Recovery partition is not a bypass:
  Recovery partition rollback MUST verify metadata, measurements, policy, and audit obligations before mutating protected state.

`DIST-PRIN-0007` Claims follow evidence:
  A release may reduce or suspend a production or High-Assurance claim when distribution, activation, attestation, or rollback evidence is incomplete.

`DIST-PRIN-0008` Fail closed:
  Unknown distribution behavior returns `MFOS_ERR_SPEC_GAP`; specified but unimplemented distribution behavior returns `MFOS_ERR_UNSUPPORTED`.

## 6. Actors and Components

| Actor or component | Role |
| --- | --- |
| `release_manager` | Publishes reviewed release to channels and owns release withdrawal decisions. |
| `release_signer` | Signs release metadata and artifact manifests. |
| `UPDATE_OPERATOR` | Requests stage, activate, rollback, or recovery operations. |
| `RECOVERY_OPERATOR` | Executes approved recovery partition rollback plans. |
| `securityd` | Final authorization decision point for distribution, activation, rollback, and recovery operations. |
| `auditd` | Evidence service for release, rollout, activation, rollback, and failure records. |
| `uvsd` | Verifies TUF-like metadata, artifact manifests, revocation, generation, epoch, and activation constraints. |
| `operatord` | Presents typed operator commands for release operations. |
| `PXM` | Coordinates partition activation, quiesce, recovery partition, and device state where applicable. |
| `PXM Guard` | High-Assurance root approval for update roots and activation profile transitions. |
| `recovery partition` | Offline measured recovery environment for rollback/repair workflows. |
| `evidence archive` | Stores release, rollout, rollback, and recovery evidence artifacts. |

## 7. Artifact Channels

MFOS supports these distribution channels:

| Channel | Purpose | Profile use | Default policy |
| --- | --- | --- | --- |
| `stable` | Normal reviewed release. | Baseline, Enterprise-Standalone, Enterprise-PXM, High-Assurance. | Requires reviewed release metadata. |
| `candidate` | Release candidate testing. | Development and pre-production. | Not production unless explicitly approved. |
| `canary` | Limited production exposure. | Enterprise-Standalone, Enterprise-PXM, and High-Assurance with evidence. | Requires staged rollout policy. |
| `ring-0` | Internal or first deployment ring. | Enterprise-Standalone, Enterprise-PXM, and High-Assurance. | Requires rollback plan. |
| `ring-1` | Broader controlled deployment. | Enterprise-Standalone, Enterprise-PXM, and High-Assurance. | Requires ring-0 health evidence. |
| `ring-2` | General controlled deployment. | Enterprise-Standalone, Enterprise-PXM, and High-Assurance. | Requires prior ring success evidence. |
| `emergency` | Security-critical update. | All profiles with stricter audit. | Requires emergency approval and short expiry. |
| `recovery` | Previous-good or repair artifacts. | Enterprise-Standalone, Enterprise-PXM, and High-Assurance. | Requires recovery policy and recovery partition coordination. |
| `test` | Non-production test artifacts. | Development only. | Must not satisfy production gates. |
| `offline` | Air-gapped import. | Enterprise-Standalone, Enterprise-PXM, and High-Assurance optional. | Requires manifest verification and operator import audit. |

Rules:

- A channel is not trusted merely because it is private.
- Channel metadata must bind channel name, release ID, metadata generation, security epoch, and expiry.
- Emergency and recovery channels must have shorter metadata expiry than stable channels.
- Test channel artifacts must not be accepted by production activation policy.

## 8. Signed Metadata Relationship to UVS

Release distribution uses TUF-like roles as inputs to UVS:

```text
root metadata
  -> timestamp metadata
  -> snapshot metadata
  -> targets metadata
  -> MFOS release distribution manifest
  -> update artifact manifests
  -> artifacts
```

UVS remains the verifier. Distribution tooling may fetch, cache, mirror, or present artifacts, but must not decide artifact trust.

Metadata role responsibilities:

| Role | MFOS use |
| --- | --- |
| root | Defines trusted update keys and role thresholds. |
| timestamp | Provides freshness and freeze attack detection. |
| snapshot | Provides a consistent view of metadata versions. |
| targets | Binds release artifacts to hashes, sizes, versions, custom constraints, channels, and profiles. |
| release distribution manifest | Binds rollout policy, activation profile updates, rollback policy, recovery image refs, and evidence refs. |
| artifact manifest | Binds component artifact digest, size, generation, security epoch, dependencies, conflicts, and profile applicability. |

## 9. Release Distribution Manifest

```yaml
ReleaseDistributionManifest:
  manifest_version: 1
  release_id: string
  release_version: semver
  release_generation: uint64
  security_epoch: uint64
  created_at_utc: timestamp
  expires_at_utc: timestamp
  channels:
    - stable
  claimed_profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance | none
  source_matrix_refs:
    - TUF-001
    - SLSA-001
  metadata_refs:
    root: string
    timestamp: string
    snapshot: string
    targets: string
  artifact_manifests:
    - manifest_ref: string
      component_id: string
      component_type: nucleus | trusted_service | amf_module | policy_bundle | catalog_schema | operator_command_set | pxm_core | pxm_guard | recovery_image | firmware_advisory | source_matrix_bundle | conformance_test_bundle
      digest: sha384
      generation: uint64
      security_epoch: uint64
  activation_profile_update:
    required: bool
    profile_id: string?
    profile_digest: sha384?
    old_profile_digest: sha384?
    constraints:
      - string
    guard_required: bool
  rollout_policy:
    rollout_id: string
    strategy: all_at_once | canary | rings | emergency | manual
    max_parallel_partitions: uint32
    min_health_window: duration
    auto_advance: bool
    rollback_on_health_failure: bool
  rollback_policy:
    rollback_allowed: bool
    min_generation: uint64
    min_security_epoch: uint64
    allowed_targets:
      - release_id: string
        generation: uint64
        security_epoch: uint64
        digest_set: sha384
    require_dual_control: bool
    require_recovery_partition: bool
    require_guard_approval: bool
  recovery:
    recovery_image_ref: string?
    recovery_plan_ref: string?
    previous_good_release_ref: string?
  evidence_refs:
    sbom_ref: string?
    provenance_ref: string?
    release_review_ref: string?
    conformance_statement_ref: string?
    production_gate_ref: string?
  signature:
    signing_key_id: string
    signature: string
```

Rules:

- `release_generation` and `security_epoch` are monotonic for normal activation.
- `expires_at_utc` must be enforced by UVS.
- `rollback_policy.rollback_allowed` does not itself authorize rollback; it only declares whether rollback can be requested under recovery policy.
- High-Assurance `activation_profile_update.guard_required` must be true for Guard-protected root transitions.

## 10. Artifact Store and Mirror Rules

Distribution store responsibilities:

- Store immutable artifacts by digest.
- Store signed metadata by version and role.
- Preserve old metadata required for recovery policies.
- Expose channel heads without altering metadata contents.
- Reject artifact replacement under existing digest path.

Mirror responsibilities:

- Mirror metadata and artifacts without modifying signed bytes.
- Preserve consistent snapshot paths when used.
- Report mirror freshness and last successful sync.
- Never rewrite timestamp metadata to extend expiry.

Offline import responsibilities:

- Import metadata and artifacts as a bundle.
- Verify media hash before presenting to UVS.
- Record operator identity, source, media ID, and chain of custody.
- Treat imported artifacts as untrusted until UVS verifies metadata and artifacts.

## 11. Activation Profile Updates

Activation profile updates may change:

- Boot component selection.
- Service startup generation.
- AMF registry generation.
- PXM partition image refs.
- PXM memory, CPU, or device assignment constraints.
- Guard root policy refs.
- Recovery image refs.
- Rollback previous-good refs.

Activation profile update lifecycle:

```text
PROFILE_UPDATE_RECEIVED
  -> VERIFY_METADATA
  -> VERIFY_PROFILE_DIGEST
  -> CHECK_POLICY_VERSION
  -> SECURITYD_AUTHORIZE
  -> GUARD_APPROVE?          [High-Assurance or guard_required]
  -> STAGE_PROFILE
  -> ACTIVATE_PROFILE
  -> MEASURE_AFTER_BOOT_OR_SWITCH
  -> COMMIT_PROFILE
```

Invariants:

```text
INV-DIST-AP-001:
  Activation profile update cannot be committed unless the exact profile
  digest verified by UVS is the profile digest measured after activation.

INV-DIST-AP-002:
  High-Assurance activation profile root transition is not valid unless
  Guard approved the transition and auditd recorded it.
```

## 12. Staged Rollout Model

Rollout states:

```text
ROLLOUT_DEFINED
  -> ROLLOUT_METADATA_VERIFIED
  -> ROLLOUT_STAGED
  -> ROLLOUT_CANARY_ACTIVE
  -> ROLLOUT_RING_ACTIVE
  -> ROLLOUT_PAUSED
  -> ROLLOUT_ADVANCED
  -> ROLLOUT_COMPLETE
```

Failure and exception states:

```text
ROLLOUT_HEALTH_FAILED
ROLLOUT_ROLLBACK_REQUESTED
ROLLOUT_ROLLBACK_AUTHORIZED
ROLLOUT_RECOVERY_REQUIRED
ROLLOUT_WITHDRAWN
ROLLOUT_REJECTED
```

Rollout health inputs:

- Boot success.
- UVS commit success.
- auditd availability.
- securityd availability.
- DENY-before-result test sample where applicable.
- service health checks.
- operator smoke tests.
- partition health.
- Guard root verification for High-Assurance.
- attestation result for High-Assurance.

Rules:

- Rollout advance requires health evidence for the previous stage.
- Auto-advance must be disabled for High-Assurance unless an explicit policy permits it.
- Rollout pause must be audited.
- Rollout withdrawal must update channel metadata and audit the withdrawal.
- A rollout stage must not mask a failed activation as success.

## 13. Rollback Authorization

Rollback is a protected operation mediated by `securityd` and `uvsd`.

Authorization inputs:

```yaml
RollbackAuthorizationRequest:
  subject: SubjectRef
  operation: ROLLBACK_REQUEST | ROLLBACK_AUTHORIZE | ROLLBACK_EXECUTE | ROLLBACK_COMMIT
  current_release_id: string
  current_generation: uint64
  current_security_epoch: uint64
  target_release_id: string
  target_generation: uint64
  target_security_epoch: uint64
  rollback_reason: activation_failure | health_failure | security_withdrawal | operator_recovery | incident_recovery | drill
  recovery_policy_ref: string
  release_manifest_digest: sha384
  target_manifest_digest: sha384
  activation_profile_hash: sha384
  profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  dual_control_approval_ids:
    - string
  guard_required: bool
  correlation_id: uuid
```

Authorization outcomes:

```text
ALLOW
DENY
REQUIRE_DUAL_CONTROL
REQUIRE_RECOVERY_PARTITION
REQUIRE_GUARD_APPROVAL
REQUIRE_SECURITY_EXCEPTION
UNSUPPORTED
SPEC_GAP
```

Rules:

- Rollback to an older generation is denied unless release metadata and recovery policy allow it.
- Rollback to an older security epoch is denied unless an approved emergency recovery policy allows it and records a security exception.
- Rollback must distinguish malicious rollback attempt from approved rollback recovery.
- Dual control is required for production rollback unless a pre-approved emergency policy says otherwise.
- High-Assurance rollback requires Guard approval for protected roots and nonce-bound attestation before restoring High-Assurance claim.

## 14. Rollback Lifecycle

```text
ROLLBACK_REQUESTED
  -> PRESERVE_EVIDENCE
  -> VERIFY_CURRENT_STATE
  -> VERIFY_TARGET_METADATA
  -> VERIFY_TARGET_ARTIFACTS
  -> CHECK_ROLLBACK_POLICY
  -> SECURITYD_AUTHORIZE
  -> REQUIRE_DUAL_CONTROL?
  -> QUIESCE_AFFECTED_SCOPE
  -> GUARD_APPROVE?              [High-Assurance or guard_required]
  -> ACTIVATE_RECOVERY_PARTITION? [if required]
  -> STAGE_ROLLBACK
  -> SWITCH_ACTIVATION_PROFILE
  -> MEASURE_ROLLED_BACK_STATE
  -> VERIFY_HEALTH
  -> COMMIT_ROLLBACK
  -> AUDIT_AND_EXPORT_EVIDENCE
```

Failure states:

```text
ROLLBACK_METADATA_INVALID
ROLLBACK_TARGET_MISMATCH
ROLLBACK_POLICY_DENIED
ROLLBACK_SECURITY_DENIED
ROLLBACK_DUAL_CONTROL_MISSING
ROLLBACK_GUARD_DENIED
ROLLBACK_RECOVERY_IMAGE_INVALID
ROLLBACK_MEASUREMENT_MISMATCH
ROLLBACK_HEALTH_FAILED
ROLLBACK_AUDIT_UNAVAILABLE
ROLLBACK_RECOVERY_REQUIRED
```

## 15. Recovery Partition Coordination

Recovery partition rollback is required when:

- the MFOS partition cannot boot to UVS safely.
- activation profile state is corrupt.
- audit state must be preserved before rollback.
- Guard lockdown requires out-of-band recovery.
- PXM partition state prevents normal activation.
- recovery policy requires offline rollback.

Recovery partition workflow:

```text
RECOVERY_ROLLBACK_REQUEST
  -> AUTHORIZE_RECOVERY
  -> MEASURE_RECOVERY_IMAGE
  -> START_RECOVERY_PARTITION
  -> MOUNT_AFFECTED_STATE_READ_ONLY
  -> CAPTURE_EVIDENCE_BUNDLE
  -> VERIFY_RELEASE_METADATA
  -> VERIFY_PREVIOUS_GOOD_ARTIFACTS
  -> VERIFY_ACTIVATION_PROFILE
  -> SECURITYD_OR_RECOVERY_POLICY_AUTHORIZE
  -> GUARD_APPROVE?              [High-Assurance]
  -> APPLY_ROLLBACK_PLAN
  -> MEASURE_RESTORED_STATE
  -> RECONCILE_AUDIT_RECORDS
  -> QUIESCE_RECOVERY_PARTITION
  -> START_MFOS_PARTITION
  -> VALIDATE_AND_COMMIT
```

Rules:

- Recovery partition must boot from a measured approved recovery image.
- Affected state must be mounted read-only before evidence capture unless explicit safety policy allows write-first action.
- Recovery partition must not browse business datasets for convenience.
- Recovery partition must not rewrite audit records.
- Recovery partition must not disable UVS, securityd, auditd, or Guard.
- Recovery partition rollback must reconcile recovery audit records into auditd or preserve a documented audit break.

## 16. Audit Obligations

Release distribution audit records must cover:

- Channel metadata publish.
- Channel metadata withdrawal.
- Release metadata fetch.
- Offline import.
- UVS verify result.
- Stage request and stage result.
- Activation profile update request.
- Activation profile stage, activate, and commit.
- Rollout stage start, pause, advance, complete, and withdraw.
- Rollout health failure.
- Rollback request.
- Rollback authorization decision.
- Dual-control approval.
- Guard approval or denial.
- Recovery partition activation.
- Evidence preservation.
- Rollback stage, switch, measure, health, commit, or failure.
- Production or High-Assurance claim suspension or restoration.

Audit record fields:

```yaml
ReleaseDistributionAuditRecord:
  schema_version: uint16
  record_id: uuid
  timestamp_utc: timestamp
  component_id: uvsd | operatord | auditd | pxm | guard | recovery_partition
  correlation_id: uuid
  subject: SubjectRef
  operation: string
  decision: string
  reason_code: string
  release_id: string
  channel: stable | candidate | canary | ring-0 | ring-1 | ring-2 | emergency | recovery | test | offline
  generation: uint64
  security_epoch: uint64
  metadata_versions:
    root: uint64?
    timestamp: uint64?
    snapshot: uint64?
    targets: uint64?
  release_manifest_digest: sha384
  artifact_digest_set: sha384?
  activation_profile_hash: sha384?
  rollout_id: string?
  rollback_id: string?
  recovery_plan_id: string?
  policy_version: uint64
  guard_seal_version: uint64?
  previous_hash: sha384
  record_hash: sha384
```

DENY or failure records for rollback, activation, and channel withdrawal must be emitted before caller-visible success or failure when audit is available. If audit is unavailable for a security-critical operation, the operation fails closed or enters profile-defined recovery mode.

## 17. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-DIST-0001 | Release distribution must verify signed metadata before artifact trust. | metadata test |
| MFOS-REQ-DIST-0002 | Transport security must not be treated as artifact integrity. | architecture review |
| MFOS-REQ-DIST-0003 | Channel metadata must bind channel, release ID, generation, security epoch, and expiry. | schema test |
| MFOS-REQ-DIST-0004 | Test channel artifacts must not activate under production policy. | negative test |
| MFOS-REQ-DIST-0005 | Release distribution manifest must bind rollout, activation profile, rollback policy, and evidence refs. | manifest test |
| MFOS-REQ-DIST-0006 | Activation profile updates must be signed, staged, authorized, audited, and profile checked. | integration test |
| MFOS-REQ-DIST-0007 | High-Assurance activation profile root transitions must require Guard approval. | Guard test |
| MFOS-REQ-DIST-0008 | Rollout advancement must require health evidence for the previous stage. | staged rollout test |
| MFOS-REQ-DIST-0009 | Rollout pause, withdrawal, and health failure must be audited. | audit test |
| MFOS-REQ-DIST-0010 | Rollback to older generation or security epoch must be denied unless recovery policy authorizes it. | rollback negative test |
| MFOS-REQ-DIST-0011 | Production rollback must require securityd authorization and dual control unless emergency policy permits otherwise. | authorization test |
| MFOS-REQ-DIST-0012 | Recovery partition rollback must boot measured approved recovery image before mutating protected state. | recovery drill |
| MFOS-REQ-DIST-0013 | Recovery partition must capture evidence before write unless explicit safety policy allows write-first action. | recovery negative test |
| MFOS-REQ-DIST-0014 | Rollback must reconcile recovery audit records or preserve a documented audit break. | audit recovery test |
| MFOS-REQ-DIST-0015 | Distribution and rollback operations must not return fake success for unsupported or undefined behavior. | no-fake-success CI |
| MFOS-REQ-DIST-0016 | Channel withdrawal must prevent new activation while preserving artifacts needed for recovery. | withdrawal test |
| MFOS-REQ-DIST-0017 | High-Assurance rollback must require Guard approval and attestation before restoring High-Assurance claim. | HA rollback test |
| MFOS-REQ-DIST-0018 | Offline import must record chain of custody and verify metadata before staging. | offline import test |

## 18. Invariants

```text
INV-DIST-001:
  No release artifact can be staged unless UVS verified signed metadata,
  artifact digest, size, generation, security_epoch, revocation, dependency,
  conflict, profile, and audit requirements.

INV-DIST-002:
  No normal activation can commit a lower generation or security_epoch than
  the current committed state.

INV-DIST-003:
  Authorized rollback is the only path that may activate an older generation,
  and it must include recovery policy, securityd authorization, audit, and
  profile-specific approvals.

INV-DIST-004:
  Channel withdrawal prevents new activation but does not delete artifacts
  still required for recovery or evidence.

INV-DIST-005:
  High-Assurance release, activation profile, and rollback root transitions
  are invalid without Guard approval and attestation evidence where claimed.

INV-DIST-006:
  Recovery partition cannot mutate protected state before evidence capture
  unless an explicit safety policy authorizes and audits the exception.
```

## 19. Failure Modes

| Failure | Required behavior |
| --- | --- |
| Missing metadata | No stage; return `MFOS_ERR_INVALID_PARAMETER`; audit failure. |
| Invalid metadata signature | No stage; return typed signature error; audit failure. |
| Timestamp expired | No stage; return `MFOS_ERR_FREEZE_DETECTED`. |
| Snapshot/targets mismatch | No stage; return `MFOS_ERR_MIX_AND_MATCH_DETECTED`. |
| Artifact digest mismatch | No stage; return `MFOS_ERR_INTERNAL_CORRUPTION`; preserve evidence. |
| Channel metadata stale | No new activation; fetch fresh metadata or hold. |
| Test channel in production policy | Deny activation; audit policy violation. |
| Rollout health failure | Pause rollout; evaluate rollback policy; audit. |
| Channel withdrawal | Stop new activation; preserve recovery artifacts. |
| Activation profile measurement mismatch | Do not commit; enter recovery workflow. |
| Rollback target not in signed policy | Deny rollback; audit. |
| Rollback security epoch downgrade without emergency policy | Deny rollback; audit security exception attempt. |
| Missing dual control | Deny production rollback; audit. |
| Recovery image measurement mismatch | Deny recovery partition activation. |
| Recovery audit reconciliation failure | Remain in recovery or claim-suspended state. |
| Guard required but unavailable | Deny High-Assurance activation or rollback. |
| Attestation mismatch | Do not restore High-Assurance claim. |
| Unknown distribution operation | Return `MFOS_ERR_SPEC_GAP`; no side effects. |
| Specified but unimplemented distribution operation | Return `MFOS_ERR_UNSUPPORTED`; no side effects. |

## 20. Positive Tests

| ID | Test |
| --- | --- |
| `DIST-POS-0001` | Stable channel release metadata verifies and stages through UVS. |
| `DIST-POS-0002` | Activation profile update stages, activates, measures, and commits with audit. |
| `DIST-POS-0003` | Canary rollout advances only after health evidence is present. |
| `DIST-POS-0004` | Channel withdrawal prevents new activation while preserving recovery artifact access. |
| `DIST-POS-0005` | Approved rollback to previous-good generation succeeds through recovery policy and audit. |
| `DIST-POS-0006` | Recovery partition rollback captures evidence, verifies metadata, applies plan, reconciles audit, and restarts MFOS. |
| `DIST-POS-0007` | Offline import verifies media chain of custody and stages after UVS verification. |
| `DIST-POS-0008` | High-Assurance activation profile update succeeds with Guard approval and attestation. |

## 21. Negative Tests

| ID | Test |
| --- | --- |
| `DIST-NEG-0001` | Artifact received over trusted transport without valid metadata is rejected. |
| `DIST-NEG-0002` | Expired timestamp metadata blocks stage. |
| `DIST-NEG-0003` | Mix-and-match snapshot/targets metadata blocks stage. |
| `DIST-NEG-0004` | Test channel artifact cannot activate under production policy. |
| `DIST-NEG-0005` | Rollout advance without health evidence is denied. |
| `DIST-NEG-0006` | Channel withdrawal cannot delete previous-good artifacts required for rollback. |
| `DIST-NEG-0007` | Rollback to unsigned target is denied. |
| `DIST-NEG-0008` | Rollback to older security epoch without approved emergency policy is denied. |
| `DIST-NEG-0009` | Production rollback without dual control is denied. |
| `DIST-NEG-0010` | Recovery partition write before evidence capture is denied without safety exception. |
| `DIST-NEG-0011` | Recovery image measurement mismatch denies recovery partition activation. |
| `DIST-NEG-0012` | High-Assurance rollback without Guard approval is denied. |
| `DIST-NEG-0013` | Attestation mismatch prevents restoring High-Assurance claim. |
| `DIST-NEG-0014` | Unknown distribution command returns `MFOS_ERR_SPEC_GAP`. |
| `DIST-NEG-0015` | Specified but unavailable staged rollout strategy returns `MFOS_ERR_UNSUPPORTED`. |
| `DIST-NEG-0016` | Audit unavailable for security-critical rollback causes fail-closed or recovery mode. |

## 22. Fuzz Targets

- `fuzz_release_distribution_manifest`.
- `fuzz_channel_metadata`.
- `fuzz_rollout_policy`.
- `fuzz_rollback_policy`.
- `fuzz_activation_profile_update`.
- `fuzz_offline_import_bundle`.
- `fuzz_recovery_plan_ref`.
- `fuzz_release_audit_record`.

Fuzz targets must assert that malformed metadata, overflowed lengths, unknown enum values, nonzero reserved fields, and inconsistent digest sets never return success.

## 23. Evidence Artifacts

Required evidence artifacts:

- Release distribution manifest verification report.
- Channel metadata verification report.
- UVS verification report.
- Artifact hash and signature verification report.
- SBOM and signed provenance refs for Enterprise-Standalone, Enterprise-PXM, and High-Assurance release artifacts.
- Staged rollout health evidence.
- Channel withdrawal evidence.
- Activation profile update evidence.
- Rollback authorization evidence.
- Dual-control approval evidence.
- Recovery partition measurement evidence.
- Recovery audit reconciliation evidence.
- Guard approval evidence for High-Assurance.
- Attestation evidence for restoring High-Assurance claim.
- Negative test report.
- Fuzz report.
- No-fake-success report.
- Evidence archive entries for release, rollback, and recovery artifacts.

## 24. Operator Commands

Operator commands are illustrative MFOS commands, not compatibility claims:

```text
DISPLAY RELEASE CHANNEL(<channel>)
VERIFY RELEASE(<release_id>) CHANNEL(<channel>)
STAGE RELEASE(<release_id>) CHANNEL(<channel>)
ACTIVATE RELEASE(<release_id>) WINDOW(NEXT_BOOT|IMMEDIATE|RECOVERY_BOOT)
PAUSE ROLLOUT(<rollout_id>)
ADVANCE ROLLOUT(<rollout_id>) RING(<ring>)
WITHDRAW RELEASE(<release_id>) REASON(<reason>)
REQUEST ROLLBACK CURRENT(<release_id>) TARGET(<release_id>) REASON(<reason>)
AUTHORIZE ROLLBACK(<rollback_id>) APPROVAL(<approval_id>)
START RECOVERY ROLLBACK(<rollback_id>) PLAN(<recovery_plan_id>)
DISPLAY ROLLBACK(<rollback_id>)
```

Rules:

- Every command requires operator identity.
- Every command requires securityd authorization.
- Every command has an audit obligation.
- Destructive or claim-affecting commands require confirmation or dual control.
- Unknown commands return `MFOS_ERR_SPEC_GAP`.
- Specified but unavailable commands return `MFOS_ERR_UNSUPPORTED`.

## 25. Inactive Future Implementation Prompt Template

Phase status: inactive future template. This section does not authorize production implementation, hosted daemon implementation, or portable semantic-core implementation.

```text
Future authorized agents would implement or review MFOS release distribution and rollback.

Do not claim z/OS compatibility, z/Architecture compatibility, IBM API
compatibility, RACF compatibility, JES compatibility, DFSMS compatibility,
SMP/E compatibility, Windows Update compatibility, or Linux package-manager
compatibility.

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
- UVS verifies signed metadata and artifacts before staging or activation.
- Transport security is not artifact integrity.
- Rollback to older generation or security_epoch requires recovery policy,
  securityd authorization, audit, and profile-specific approvals.
- Recovery partition is not a policy bypass.
- High-Assurance activation or rollback requires Guard evidence and attestation
  where root claims are restored.
- Channel withdrawal stops new activation but preserves recovery artifacts.
- Unsupported specified behavior returns MFOS_ERR_UNSUPPORTED.
- Undefined behavior returns MFOS_ERR_SPEC_GAP.
- Add negative tests for rollback, channel, audit, recovery partition, and
  High-Assurance failure paths.
```

## 26. Spec Gaps

- Concrete TUF-like metadata wire format remains defined by UVS, not duplicated here.
- Exact channel server protocol is not specified.
- CDN, mirror, and offline media implementation are not specified.
- Release signing key hierarchy is not fixed.
- Rollout health check plugin ABI is not specified.
- Ring assignment policy is not specified.
- Exact attestation verifier implementation is not specified.
- Cross-release artifact garbage collection policy is not specified.
- Multi-node coordinated rollout is out of scope.
- Live rollback without reboot is out of scope.
- Legal/customer notification for release withdrawal is out of scope.

