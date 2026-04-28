---
spec_id: "MFOS-SPEC-25-OPERATIONS-RECOVERY"
title: "MFOS Operations, Recovery, and Incident Response Specification v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001", "EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001", "EXTREF-IBM-Z-DPM-0001", "EXTREF-IBM-ZOS-JES-INTRODUCTION-0001", "EXTREF-IBM-ZOS-JES-JOB-FLOW-0001", "EXTREF-IBM-ZOS-JES2-LIBRARY-0001", "EXTREF-IBM-Z-LPAR-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001", "EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001", "EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001", "MS-VBS-001", "MS-VSM-001", "NIST-160-001", "NIST-193-001", "NIST-218-001", "SLSA-001", "TCG-001", "TUF-001", "X64-AMD-001", "X64-INTEL-001"]
requirement_refs: ["MFOS-REQ-OPS-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Operations, Recovery, and Incident Response Specification v0.1

Status: Draft design split

Owned area: `docs/design/specs/25-operations-recovery.md`

Audience: operators, recovery engineers, incident responders, architecture agents, implementation agents, security reviewers, test engineers

MFOS is z/OS-inspired and source-grounded. MFOS does not claim z/OS, z/Architecture, RACF, JES, DFSMS, SMF, workload policy, APF, PR/SM, Windows VBS, Linux, or UNIX compatibility.

## 1. Purpose

This specification defines MFOS operational procedures, recovery workflows, incident response behavior, operator drills, evidence preservation, and fail-closed rules.

It exists to ensure that MFOS operations are as source-grounded and testable as MFOS implementation:

- Operators use typed, authorized, audited procedures, not ad hoc root shells.
- Recovery partition activity is constrained, measured, authorized, and auditable.
- Audit export outages have explicit profile-dependent behavior.
- Catalog recovery never hides corruption or invents success.
- Update rollback recovery follows verified metadata, security epochs, and audit evidence.
- Guard lockdown recovery is narrow, evidence-preserving, and High-Assurance-specific.
- Break-glass does not disable security or audit.
- Incident response preserves evidence before repair when safety permits.
- Every drill has entry criteria, procedure, expected evidence, and negative tests.

## 2. Scope

In scope:

- Operations model and operator roles.
- Operator drills and recovery drills.
- Recovery partition role, activation, limits, and handoff.
- Audit export outage behavior.
- Catalog recovery and dataset integrity recovery.
- Update rollback recovery and failed activation recovery.
- Guard lockdown recovery.
- Break-glass operation.
- Evidence preservation and chain of custody.
- Incident severity, containment, eradication, recovery, and post-incident review.
- Fail-closed behavior.
- Negative tests, fault-injection drills, runbook fuzz targets, spec gaps, and AI prompt.

Out of scope:

- Full SOC/SIEM product integration.
- Exact cryptographic algorithm selection.
- Long-term archive storage product selection.
- Physical security procedures for a data center.
- Human resources or legal notification workflow.
- Full remote management plane protocol.
- Full POSIX/Linux desktop incident response inside a side partition.
- Compatibility with IBM operational procedures or command sets.

## 3. Source Matrix References

| Source ID | Operations/recovery use |
| --- | --- |
| `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001` | System integrity boundary: operations must not let unauthorized subjects bypass protection or authorized state. |
| `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001` | Negative tests for authorized boundary confusion during emergency and recovery. |
| `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001` | Security-manager-inspired policy, protected resources, break-glass, and audit-relevant access decisions. |
| `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-JES-JOB-FLOW-0001`, `EXTREF-IBM-ZOS-JES2-LIBRARY-0001` | Job and spool operations, cancel, hold, output retention, and operator-visible work state. |
| `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001` | Dataset/catalog recovery, catalog entries, locations, and managed storage concepts. |
| `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001` | Audit/accounting evidence and security event records. |
| `EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001` | Operational handling of service classes, overload, and workload policy changes. |
| `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `EXTREF-IBM-Z-DPM-0001` | Partition activation, recovery partition, and partition lifecycle management analogies. |
| `X64-INTEL-001`, `X64-AMD-001` | Platform recovery constraints, paging, virtualization, IOMMU, and interrupt remapping reality. |
| `MS-VBS-001`, `MS-VSM-001` | Informative Guard lockdown and isolated-root recovery concepts for High-Assurance only. |
| `TCG-001` | Measured boot, TPM event log, and attestation evidence preservation. |
| `NIST-160-001`, `NIST-193-001`, `NIST-218-001` | Secure system engineering, firmware resiliency, and secure development/response discipline. |
| `TUF-001` | Update rollback, freeze, mix-and-match, root/targets/snapshot/timestamp metadata recovery. |
| `SLSA-001` | Provenance and supply-chain evidence for incident response. |
| `FBVBS-001` | State-machine discipline, evidence obligations, production proof obligations, no fake success. |

## 4. Non-Compatibility Statement

Operational procedures in this document are MFOS procedures. They are not IBM z/OS operational procedures, RACF procedures, JES procedures, DFSMS procedures, SMF procedures, PR/SM procedures, or Windows VBS procedures.

Allowed wording:

- "MFOS operator recovery workflow."
- "SMF-inspired audit evidence handling."
- "DFSMS-inspired catalog recovery model."
- "LPAR/DPM-inspired recovery partition concept."
- "VBS/VSM-like Guard lockdown concept for High-Assurance only."

Prohibited wording:

- "z/OS-compatible operation."
- "RACF-compatible recovery."
- "JES-compatible spool operations."
- "DFSMS-compatible catalog repair."
- "Windows VBS-compatible lockdown recovery."

## 5. Operational Principles

`OPS-PRIN-0001` Typed operations only:
  Operational action MUST be represented as a typed operator command, recovery plan, PXM call, Guard call, or UVS operation.

`OPS-PRIN-0002` Securityd remains the policy decision point:
  Operational urgency does not allow services to make final protected-resource authorization decisions locally.

`OPS-PRIN-0003` Audit is evidence:
  Console output, spool output, screenshots, and diagnostic logs are not authoritative audit evidence unless auditd records them as evidence.

`OPS-PRIN-0004` Preserve before repair:
  When safety permits, volatile state, audit head, measurements, policy versions, and affected object metadata MUST be preserved before repair.

`OPS-PRIN-0005` Break-glass is constrained:
  Break-glass is time-bound, reason-bound, identity-bound, auditable, and profile-aware. It is not a root shell and does not disable audit.

`OPS-PRIN-0006` Recovery partition is not a policy bypass:
  The recovery partition can inspect and repair only through approved recovery plans, measurements, security decisions, and audit obligations.

`OPS-PRIN-0007` Fail closed before guessing:
  If the safe operational state is unknown, MFOS MUST deny, hold, lock down, or enter recovery mode rather than invent success.

`OPS-PRIN-0008` Profile claims require evidence:
  Enterprise-Standalone, Enterprise-PXM, and High-Assurance operations require the boot, audit, update, PXM, and Guard evidence required by those profiles.

## 6. Roles and Authorities

| Role | Purpose | Required controls |
| --- | --- | --- |
| `OPERATOR_VIEWER` | Display system, job, spool, dataset, workload policy, and partition state. | Authenticated session, audit. |
| `OPERATOR_CONTROLLER` | Submit/cancel jobs, hold/release work, browse authorized spool. | securityd decision, audit, target generation checks. |
| `SECURITY_ADMIN` | Manage principals, profiles, emergency access, and security policy. | MFA recommended, dual-control for destructive policy changes, audit. |
| `RECOVERY_OPERATOR` | Execute approved recovery procedures. | Recovery role, reason, correlation ID, audit, recovery plan. |
| `INCIDENT_COMMANDER` | Coordinate incident response and declare severity/state transitions. | Explicit appointment, audit, evidence ledger. |
| `AUDIT_CUSTODIAN` | Export, seal, preserve, and verify audit evidence. | Audit stream authority, redaction policy, chain-of-custody record. |
| `UPDATE_OPERATOR` | Stage, activate, roll back, or recover updates. | UVS authority, update metadata verification, audit. |
| `PXM_OPERATOR` | Operate partitions and device assignment. | PXM authority, IOMMU/teardown evidence, audit. |
| `GUARD_RECOVERY_OPERATOR` | Perform approved High-Assurance Guard recovery. | Guard recovery policy, dual-control, audit, attestation. |

Separation rules:

- The requester and approver for dual-control recovery actions MUST be distinct principals unless an approved emergency policy says otherwise.
- `RECOVERY_OPERATOR` MUST NOT gain implicit `SECURITY_ADMIN` authority.
- `AUDIT_CUSTODIAN` MUST NOT rewrite committed records.
- `PXM_OPERATOR` MUST NOT interpret MFOS dataset, job, spool, catalog, or security policy semantics.
- `GUARD_RECOVERY_OPERATOR` MUST NOT request ordinary dataset, job, spool, or workload policy decisions from Guard.

## 7. Operational States

```text
NORMAL
  -> DEGRADED
  -> INCIDENT_DECLARED
  -> CONTAINMENT
  -> EVIDENCE_PRESERVATION
  -> RECOVERY_PLANNING
  -> RECOVERY_EXECUTION
  -> VALIDATION
  -> RESTORED
  -> POST_INCIDENT_REVIEW
  -> NORMAL
```

Exceptional states:

```text
AUDIT_EXPORT_OUTAGE
CATALOG_RECOVERY
UPDATE_ROLLBACK_RECOVERY
GUARD_LOCKDOWN
BREAK_GLASS_ACTIVE
RECOVERY_PARTITION_ACTIVE
HA_RECOVERY_MODE
PRODUCTION_CLAIM_SUSPENDED
```

State rules:

- `INCIDENT_DECLARED` requires incident ID, severity, commander, time, scope, and audit record.
- `EVIDENCE_PRESERVATION` MUST occur before destructive repair unless safety or availability policy explicitly overrides it.
- `BREAK_GLASS_ACTIVE` MUST have reason, expiry, operator identity, policy version, and audit.
- `GUARD_LOCKDOWN` in High-Assurance suspends affected root transitions until recovery policy permits action.
- `PRODUCTION_CLAIM_SUSPENDED` is required when profile evidence is missing, corrupt, or unverified.

## 8. Incident Severity

| Severity | Examples | Required response |
| --- | --- | --- |
| `SEV-0` | Active integrity failure, Guard root mismatch, audit root corruption, unauthorized protected-resource success. | Immediate containment, evidence preservation, incident commander, recovery partition or lockdown as applicable. |
| `SEV-1` | Security-critical update failure, catalog corruption affecting system datasets, audit export outage with local queue risk. | Containment, operator drill, recovery plan, management notification. |
| `SEV-2` | Single job/spool/dataset failure with no policy bypass. | Component recovery and audit review. |
| `SEV-3` | Degraded non-security operation, transient remote export outage with safe local backlog. | Monitor, audit, scheduled remediation. |
| `SEV-4` | Drill, test, or diagnostic event. | Mark as drill/test and preserve evidence appropriate to environment. |

Severity assignment MUST be audited and MAY be upgraded but MUST NOT be silently downgraded.

## 9. Recovery Partition Role

The recovery partition is a constrained side partition for offline repair, evidence capture, rollback support, and forensics. It is not a normal administrative desktop and not a bypass around MFOS policy.

Responsibilities:

- Boot from measured, approved recovery image.
- Verify MFOS partition image, activation profile, audit stream heads, catalog journals, update metadata, and Guard roots where applicable.
- Capture evidence bundles before repair when safety permits.
- Execute signed recovery plans.
- Coordinate rollback or repair with PXM, uvsd, auditd, catalogd, and Guard according to profile.
- Produce recovery audit records or boot-time recovery audit records that reconcile into auditd.

Non-responsibilities:

- Parse or decide ordinary dataset access policy.
- Browse business datasets for convenience.
- Modify security policy without securityd/approved recovery policy.
- Rewrite audit records.
- Bypass update verification.
- Disable Guard to recover High-Assurance systems.
- Provide a general-purpose Linux/Desktop workstation.

Activation lifecycle:

```text
RECOVERY_REQUEST
  -> AUTHORIZE_RECOVERY
  -> MEASURE_RECOVERY_IMAGE
  -> ACTIVATE_RECOVERY_PARTITION
  -> MOUNT_AFFECTED_STATE_READ_ONLY
  -> CAPTURE_EVIDENCE
  -> SELECT_RECOVERY_PLAN
  -> AUTHORIZE_PLAN
  -> EXECUTE_PLAN
  -> VALIDATE_REPAIRED_STATE
  -> RECONCILE_AUDIT
  -> DEACTIVATE_RECOVERY_PARTITION
```

Failure states:

```text
RECOVERY_UNAUTHORIZED
RECOVERY_IMAGE_MEASUREMENT_MISMATCH
RECOVERY_PLAN_SIGNATURE_INVALID
EVIDENCE_CAPTURE_FAILED
AUDIT_RECONCILIATION_FAILED
GUARD_RECOVERY_DENIED
VALIDATION_FAILED
SPEC_GAP
```

## 10. Audit Export Outage Behavior

Audit export outage means auditd cannot deliver records to the configured remote collector, OOB path, or enterprise audit sink.

Outage states:

```text
EXPORT_HEALTHY
  -> EXPORT_DEGRADED
  -> EXPORT_OUTAGE_CONFIRMED
  -> LOCAL_QUEUE_ACCUMULATING
  -> LOCAL_QUEUE_PRESSURE
  -> EXPORT_RESTORED
  -> REPLAY_AND_RECONCILE
  -> EXPORT_HEALTHY
```

Profile behavior:

| Profile | Required behavior |
| --- | --- |
| Baseline | Continue local audit when durable local store is available. Security-sensitive operations fail closed if required local audit append fails. Remote export MAY be unsupported. |
| Enterprise | Queue locally, alert operator, audit outage, track backlog, and fail selected operations if local queue capacity or retention threshold is exceeded. |
| High-Assurance | Continue only if local Guard-sealed audit root and policy permit delayed export; otherwise enter recovery or lockdown for security-critical operations. |

Required operator actions:

- `DISPLAY AUDIT EXPORT` to view collector, stream, backlog, last exported sequence, last local sequence, and failure reason.
- `EXPORT AUDIT RETRY` to retry with same collector configuration.
- `EXPORT AUDIT FAILOVER <collector_id>` only if policy authorizes failover.
- `SEAL AUDIT STREAM <stream_id>` when local stream must be preserved before repair.
- `DECLARE INCIDENT` when outage exceeds profile threshold or evidence continuity is at risk.

Fail-closed conditions:

- Local durable audit append fails for security-critical event.
- Local queue reaches policy threshold and operation requires export before success.
- High-Assurance Guard audit root append fails.
- Collector identity or export key validation fails.
- Export replay detects hash-chain mismatch.

## 11. Catalog Recovery

Catalog recovery repairs catalog transaction state without hiding corruption or granting access based on unverified metadata.

Entry criteria:

- Catalog journal replay reports torn transaction, orphan extent, generation mismatch, integrity tag mismatch, or committed entry inconsistency.
- `datasetd` or `catalogd` returns protected failure requiring recovery.
- Recovery drill explicitly requests catalog recovery in a test environment.

Recovery lifecycle:

```text
CAT_RECOVERY_REQUEST
  -> QUIESCE_CATALOG_MUTATIONS
  -> CAPTURE_CATALOG_EVIDENCE
  -> SCAN_JOURNAL
  -> IDENTIFY_LAST_GOOD_COMMIT
  -> ROLLBACK_INCOMPLETE_TX
  -> VERIFY_COMMITTED_ENTRIES
  -> REPAIR_ORPHAN_EXTENTS
  -> REBUILD_SECONDARY_INDEXES
  -> REVALIDATE_SECURITY_PROFILES
  -> REVALIDATE_DATASET_HANDLES
  -> WRITE_RECOVERY_AUDIT
  -> RELEASE_CATALOG
```

Rules:

- Recovery MUST NOT rewrite committed history to hide corruption.
- Recovery MUST preserve corrupt journal ranges as evidence.
- Persistent dataset opens MUST fail closed while the affected catalog scope is quiesced.
- Existing handles for affected catalog generations MUST be revoked or revalidated.
- System dataset entries require immutable/system flag verification before release.
- High-Assurance catalog roots, if Guard-protected by policy, require Guard verification before release.

Required evidence:

- Catalog ID, generation range, journal head, last good commit, corrupt range, recovery plan ID, operator identity, policy version, affected DSNs, affected handles, and validation result.

## 12. Update Rollback Recovery

Update rollback recovery handles failed activation, detected rollback attempts, freeze attacks, mix-and-match metadata, or post-activation health failure.

Recovery lifecycle:

```text
UPDATE_RECOVERY_REQUEST
  -> FREEZE_UPDATE_STATE
  -> CAPTURE_UPDATE_EVIDENCE
  -> VERIFY_ACTIVE_METADATA_SET
  -> VERIFY_PREVIOUS_GOOD_METADATA_SET
  -> CHECK_SECURITY_EPOCH_POLICY
  -> AUTHORIZE_ROLLBACK_OR_REPAIR
  -> STAGE_RECOVERY_ARTIFACTS
  -> MEASURE_RECOVERY_ARTIFACTS
  -> ACTIVATE_RECOVERY_PROFILE
  -> BOOT_OR_SWITCH
  -> VALIDATE_COMPONENT_HEALTH
  -> COMMIT_OR_ABORT_RECOVERY
  -> WRITE_RECOVERY_AUDIT
```

Rollback rules:

- Rollback to older generation is denied unless update policy explicitly permits it for recovery.
- Rollback to older security epoch is denied unless approved emergency recovery policy permits it and records security exception evidence.
- Rollback MUST use verified metadata, not file timestamps or operator assertion.
- Failed activation MUST preserve both failed target metadata and previous-good metadata.
- High-Assurance update policy root transitions require Guard approval.
- Recovery MUST distinguish malicious rollback attempt from approved rollback recovery.

Fail-closed conditions:

- Previous-good metadata cannot be verified.
- Security epoch downgrade is not authorized.
- Artifact measurement differs from recovery manifest.
- Required audit or Guard root update cannot be recorded.
- Dependency/conflict checks are incomplete.

## 13. Guard Lockdown Recovery

Guard lockdown recovery applies only when Guard is enabled or required. High-Assurance recovery cannot proceed by disabling Guard.

Lockdown causes:

- SVC table mismatch.
- Security policy root mismatch.
- Audit root append failure.
- AMF registry root mismatch.
- Executable mapping policy violation.
- Page table policy root mismatch.
- Activation profile root mismatch.
- Emergency state root inconsistency.
- Update policy root mismatch.
- Guard metadata corruption.

Recovery lifecycle:

```text
GUARD_LOCKDOWN_DETECTED
  -> FREEZE_AFFECTED_ROOT_TRANSITIONS
  -> CAPTURE_GUARD_EVIDENCE
  -> ENTER_HA_RECOVERY_MODE
  -> AUTHORIZE_GUARD_RECOVERY
  -> VERIFY_MEASUREMENTS
  -> SELECT_ROOT_RECOVERY_PLAN
  -> APPLY_ROOT_REPAIR_OR_RESEAL
  -> REVERIFY_AFFECTED_ROOTS
  -> ATTEST_RECOVERED_STATE
  -> RECONCILE_AUDIT_ROOT
  -> EXIT_LOCKDOWN_OR_REMAIN_LOCKED
```

Rules:

- Guard recovery MUST be dual-control unless an approved High-Assurance emergency policy says otherwise.
- Guard recovery MUST include nonce-bound attestation before returning to High-Assurance ready.
- Guard recovery MUST NOT interpret dataset contents, job scheduling, spool formatting, workload policy, or ordinary operator UI state.
- Guard root rollback is denied unless recovery policy explicitly permits it and records the old and new root digests.
- If audit root reconciliation fails, the system remains in lockdown or recovery mode.
- If the suspected cause is active compromise, recovery MUST prefer containment and evidence capture over rapid return to service.

Required evidence:

- Guard state, root type, old digest, observed digest, expected digest, security epoch, policy version, measurement context, transition ID, recovery plan ID, operator identities, approval IDs, attestation nonce, attestation result, audit record refs.

## 14. Break-Glass Operation

Break-glass exists for urgent recovery when normal policy blocks necessary repair. It is not an audit bypass, not a compatibility mode, and not a general superuser shell.

Entry lifecycle:

```text
BREAK_GLASS_REQUEST
  -> AUTHENTICATE_OPERATOR
  -> REQUIRE_REASON
  -> SET_EXPIRY
  -> SECURITYD_AUTHORIZE
  -> REQUIRE_MFA?
  -> REQUIRE_DUAL_CONTROL?
  -> GUARD_APPROVE?        [High-Assurance when policy requires]
  -> AUDIT_ENTER
  -> BREAK_GLASS_ACTIVE
```

Exit lifecycle:

```text
EXIT_REQUEST_OR_EXPIRY
  -> REVOKE_BREAK_GLASS_RIGHTS
  -> REVALIDATE_AFFECTED_OBJECTS
  -> GUARD_VERIFY?         [High-Assurance when roots affected]
  -> AUDIT_EXIT
  -> POST_BREAK_GLASS_REVIEW
```

Rules:

- Reason, expiry, operator identity, policy version, correlation ID, and affected scope are mandatory.
- Break-glass authority MUST be scoped to resources and operations named in the approved request.
- Break-glass MUST NOT disable auditd, securityd, Guard, update verification, catalog integrity checks, or PXM teardown checks.
- Break-glass actions MUST be easy to find in audit query/export.
- Break-glass expiry MUST revoke derived handles, sessions, and recovery rights.
- Post-break-glass review MUST verify every action against declared reason and scope.

## 15. Evidence Preservation

Evidence preservation is required for incidents, recovery, and production-readiness claims.

Evidence bundle:

```yaml
EvidenceBundle:
  incident_id: string
  bundle_id: uuid
  profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  created_at_utc: timestamp
  created_by: PrincipalRef
  correlation_id: uuid
  components:
    audit_stream_heads: [AuditStreamHead]
    exported_audit_refs: [AuditExportRef]
    guard_root_refs: [GuardRootRef]
    tpm_event_log_ref: string?
    activation_profile_hash: sha384?
    update_metadata_refs: [UpdateMetadataRef]
    catalog_journal_refs: [CatalogJournalRef]
    spool_refs: [SpoolEntryRef]
    job_refs: [JobRef]
    crash_dump_refs: [CrashDumpRef]
    pxm_partition_state_refs: [PartitionStateRef]
    operator_command_refs: [OperatorCommandRef]
  chain_of_custody:
    - actor: PrincipalRef
      action: CREATE | SEAL | EXPORT | TRANSFER | VERIFY | ARCHIVE
      timestamp_utc: timestamp
      reason: string
```

Rules:

- Evidence MUST be append-only or sealed once captured.
- Redaction applies to export views, not committed audit records.
- Recovery MUST NOT overwrite evidence required to diagnose corruption.
- High-Assurance evidence MUST include Guard root state when Guard roots are involved.
- If evidence cannot be preserved, the incident record MUST state the reason, affected evidence class, and residual risk.

## 16. Operator Drills

Each drill MUST run through operator console or approved recovery tooling, use a drill incident ID, and produce evidence.

| Drill ID | Scenario | Frequency | Success criteria |
| --- | --- | --- | --- |
| `DRILL-OPS-0001` | Unauthorized dataset read denial. | Every release candidate. | Deny before handle, deny audit before caller result. |
| `DRILL-OPS-0002` | Audit export outage. | Quarterly Enterprise-Standalone/Enterprise-PXM/HA. | Local queue, alert, backlog tracking, replay/reconcile, no chain gap. |
| `DRILL-OPS-0003` | Catalog torn journal recovery. | Every release candidate. | Affected opens fail closed; recovery preserves corrupt range; committed state valid. |
| `DRILL-OPS-0004` | Update failed activation recovery. | Every release candidate. | Verified previous-good metadata, rollback policy enforced, audit present. |
| `DRILL-OPS-0005` | Guard SVC-table mismatch lockdown. | Quarterly HA. | Lockdown or panic-equivalent, evidence capture, approved reseal or remain locked. |
| `DRILL-OPS-0006` | Break-glass with expiry. | Quarterly. | Reason, approval, scoped rights, audit enter/exit, expiry revokes rights. |
| `DRILL-OPS-0007` | Recovery partition activation. | Semiannual Enterprise-Standalone/Enterprise-PXM/HA. | Recovery image measured, state mounted read-only first, evidence captured, plan authorized. |
| `DRILL-OPS-0008` | Spool retention purge denial. | Every release candidate. | Unauthorized/early purge denied and audited. |
| `DRILL-OPS-0009` | PXM device teardown failure. | Quarterly Enterprise-Standalone/Enterprise-PXM/HA. | Device not reassigned until teardown complete. |
| `DRILL-OPS-0010` | Audit hash-chain tamper. | Every release candidate. | Stream degraded/sealed, tamper audit, recovery workflow begins. |

Drill record:

```yaml
OperatorDrillRecord:
  drill_id: string
  run_id: uuid
  profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  started_at_utc: timestamp
  completed_at_utc: timestamp?
  operator: PrincipalRef
  incident_id: string
  commands_executed: [OperatorCommandRef]
  audit_records: [AuditRecordRef]
  expected_results: [string]
  actual_results: [string]
  deviations: [string]
  pass: bool
```

## 17. Incident Response Workflow

```text
DETECT
  -> TRIAGE
  -> DECLARE_INCIDENT
  -> ASSIGN_SEVERITY
  -> CONTAIN
  -> PRESERVE_EVIDENCE
  -> ANALYZE
  -> SELECT_RECOVERY_PLAN
  -> AUTHORIZE_RECOVERY
  -> EXECUTE_RECOVERY
  -> VALIDATE
  -> RESTORE_SERVICE
  -> POST_INCIDENT_REVIEW
```

Containment examples:

- Hold affected jobs.
- Quiesce catalog mutations.
- Revoke affected dataset handles.
- Hold spool export.
- Disable affected AMF module by revocation.
- Freeze update activation.
- Quiesce or destroy affected side partition after evidence capture.
- Enter Guard lockdown or HA recovery mode.
- Suspend production claim until evidence is restored.

Post-incident review MUST record:

- Root cause or current unknowns.
- Affected assets and profile claims.
- Timeline from audit records.
- Commands and recovery plans executed.
- Evidence bundle refs.
- Tests that would have caught the issue.
- Spec gaps discovered.
- Required source matrix updates.
- Required CI/drill additions.

## 18. Fail-Closed Behavior

| Condition | Required behavior |
| --- | --- |
| securityd unavailable | Protected operations denied; recovery/operator display subset only. |
| auditd unavailable for required event | Security-sensitive operation returns `MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE` or enters recovery by profile. |
| Audit export unavailable | Follow profile outage behavior; do not treat diagnostics as remote evidence. |
| Catalog corruption | Quiesce affected scope; dataset opens fail closed until recovery validates state. |
| Dataset integrity tag mismatch | No handle; preserve evidence; recovery or incident workflow. |
| Update metadata inconsistent | No activation; preserve metadata set; rollback recovery only through UVS policy. |
| Recovery image measurement mismatch | Recovery partition activation denied. |
| Recovery plan invalid or unsigned | Recovery denied. |
| Break-glass missing reason/expiry | Denied. |
| Break-glass audit cannot be written | Denied or HA recovery stop. |
| Guard required but unavailable | HA boot denied or approved HA recovery mode only. |
| Guard root mismatch | Lockdown or panic-equivalent; recovery workflow required. |
| PXM teardown incomplete | Device/memory reassignment denied. |
| Unknown recovery command | `MFOS_ERR_SPEC_GAP`; no side effects. |
| Specified but unimplemented recovery operation | `MFOS_ERR_UNSUPPORTED`; no side effects. |

## 19. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| `MFOS-REQ-OPS-0001` | Operations and recovery actions MUST be typed, authorized, and audited. | Operator drill |
| `MFOS-REQ-OPS-0002` | Recovery partition MUST boot from measured approved image before touching affected state. | Recovery drill |
| `MFOS-REQ-OPS-0003` | Recovery partition MUST mount affected state read-only before evidence capture unless policy explicitly authorizes write-first safety action. | Recovery negative test |
| `MFOS-REQ-OPS-0004` | Audit export outage behavior MUST be defined per profile. | Fault injection |
| `MFOS-REQ-OPS-0005` | Catalog recovery MUST preserve corrupt ranges and must not rewrite committed records to hide corruption. | Crash recovery test |
| `MFOS-REQ-OPS-0006` | Update rollback recovery MUST use verified metadata and security epoch policy. | Rollback test |
| `MFOS-REQ-OPS-0007` | Guard lockdown recovery MUST not disable Guard to restore High-Assurance claims. | HA recovery test |
| `MFOS-REQ-OPS-0008` | Break-glass MUST include reason, expiry, operator identity, scope, approval where required, and audit. | Emergency drill |
| `MFOS-REQ-OPS-0009` | Break-glass MUST NOT disable securityd, auditd, Guard, UVS, or catalog integrity checks. | Negative test |
| `MFOS-REQ-OPS-0010` | Evidence bundles MUST include audit stream heads and affected root/object metadata. | Evidence review |
| `MFOS-REQ-OPS-0011` | Production claims MUST be suspended when required profile evidence is missing or corrupt. | Release review |
| `MFOS-REQ-OPS-0012` | Operator drills MUST have pass/fail criteria and audit evidence. | Drill review |
| `MFOS-REQ-OPS-0013` | Unknown recovery operations MUST return `MFOS_ERR_SPEC_GAP`. | No-fake-success CI |
| `MFOS-REQ-OPS-0014` | Specified but unavailable recovery operations MUST return `MFOS_ERR_UNSUPPORTED`. | No-fake-success CI |
| `MFOS-REQ-OPS-0015` | Incident response MUST preserve evidence before destructive repair unless explicit safety policy overrides it. | Incident drill |

## 20. Invariants

```text
INV-OPS-001:
  No recovery action that mutates protected state may execute without
  operator identity, recovery plan ID, authorization decision, correlation ID,
  and audit obligation.

INV-OPS-002:
  Break-glass cannot disable securityd, auditd, Guard, UVS, catalog
  integrity checks, or PXM teardown checks.

INV-OPS-003:
  Recovery partition cannot write affected MFOS state before evidence capture
  unless an explicit write-first safety policy is authorized and audited.

INV-OPS-004:
  Catalog recovery cannot release affected datasets until committed entries,
  generations, security profiles, and integrity tags are verified or the
  affected entries remain locked.

INV-OPS-005:
  Update rollback recovery cannot activate an older generation or security
  epoch unless verified metadata and approved recovery policy allow it.

INV-OPS-006:
  High-Assurance Guard lockdown cannot return to High-Assurance ready state
  without Guard root verification, audit reconciliation, and nonce-bound
  attestation.

INV-OPS-007:
  Audit export outage cannot convert diagnostic output into audit evidence.

INV-OPS-008:
  Unknown recovery behavior cannot produce success; it must return SPEC_GAP.

INV-OPS-009:
  Specified but unimplemented recovery behavior cannot produce success; it
  must return UNSUPPORTED.
```

## 21. Positive Tests

| ID | Test |
| --- | --- |
| `OPS-POS-0001` | Operator declares SEV-2 incident, preserves evidence bundle, runs approved recovery plan, and closes post-incident review. |
| `OPS-POS-0002` | Recovery partition activates from measured image and mounts affected catalog read-only before evidence capture. |
| `OPS-POS-0003` | Enterprise audit export outage queues locally, alerts operator, restores export, replays backlog, and verifies sequence continuity. |
| `OPS-POS-0004` | Catalog torn journal recovery rolls back incomplete transaction and verifies committed entries. |
| `OPS-POS-0005` | Failed update activation recovers to verified previous-good metadata without security epoch downgrade. |
| `OPS-POS-0006` | Guard lockdown drill captures root mismatch evidence and remains locked until approved reseal and attestation. |
| `OPS-POS-0007` | Break-glass scoped dataset repair expires and revokes derived handles. |
| `OPS-POS-0008` | Evidence bundle includes audit heads, operator commands, update metadata, catalog journal refs, and chain of custody. |
| `OPS-POS-0009` | Production claim is suspended when HA Guard evidence is missing and restored only after evidence validation. |

## 22. Negative Tests

| ID | Test |
| --- | --- |
| `OPS-NEG-0001` | Recovery plan without signature is rejected with no state mutation. |
| `OPS-NEG-0002` | Recovery image measurement mismatch prevents recovery partition activation. |
| `OPS-NEG-0003` | Recovery partition attempts write before evidence capture without write-first policy; denied. |
| `OPS-NEG-0004` | Audit export outage with full local queue blocks configured security-critical operations. |
| `OPS-NEG-0005` | Catalog recovery attempts to delete corrupt journal range; denied and incident escalated. |
| `OPS-NEG-0006` | Dataset open during affected catalog quiesce; fails closed. |
| `OPS-NEG-0007` | Update rollback attempts security epoch downgrade without recovery policy; denied. |
| `OPS-NEG-0008` | Guard lockdown recovery attempts to disable Guard; denied. |
| `OPS-NEG-0009` | Break-glass request without reason or expiry; denied. |
| `OPS-NEG-0010` | Break-glass action outside approved scope; denied and audited. |
| `OPS-NEG-0011` | Operator attempts destructive recovery command without dual-control when required; denied. |
| `OPS-NEG-0012` | Unknown recovery command returns `MFOS_ERR_SPEC_GAP` and has no side effects. |
| `OPS-NEG-0013` | Unimplemented recovery command returns `MFOS_ERR_UNSUPPORTED` and has no side effects. |
| `OPS-NEG-0014` | Evidence export hash mismatch; export rejected and tamper workflow begins. |
| `OPS-NEG-0015` | PXM device reassignment before teardown completion; denied. |

## 23. Fault-Injection Drills

| ID | Fault | Expected response |
| --- | --- | --- |
| `OPS-FI-0001` | auditd local durable append failure during security deny. | Caller receives audit-unavailable/fail-closed result; incident or recovery state by profile. |
| `OPS-FI-0002` | Remote audit collector outage for Enterprise stream. | Local queue, alert, backlog, replay/reconcile. |
| `OPS-FI-0003` | Local audit queue capacity exhausted. | Security-critical operations fail closed according to policy. |
| `OPS-FI-0004` | Catalog journal torn after write journal before commit. | Recovery rolls back incomplete transaction. |
| `OPS-FI-0005` | Update activation crash before commit. | Recovery freezes update state and validates previous-good metadata. |
| `OPS-FI-0006` | Guard audit root append failure. | HA root operation fails closed or enters lockdown/recovery. |
| `OPS-FI-0007` | Recovery partition loses audit reconciliation path. | Recovery cannot complete production restore until reconciliation or explicit residual risk review. |
| `OPS-FI-0008` | Break-glass expiry service delayed. | Expired rights rejected by policy version/expiry checks. |
| `OPS-FI-0009` | TPM event log unavailable during Enterprise recovery validation. | Enterprise measured-boot evidence claim suspended. |
| `OPS-FI-0010` | Operator command target changes after approval. | Command revalidates target generation or fails closed. |

## 24. Fuzz Targets

| ID | Target | Required property |
| --- | --- | --- |
| `OPS-FUZZ-0001` | Recovery plan parser. | Malformed plans cannot execute or mutate state. |
| `OPS-FUZZ-0002` | Evidence bundle parser. | Hash, refs, and chain-of-custody are bounded and validated. |
| `OPS-FUZZ-0003` | Incident declaration command. | Missing severity, commander, scope, or reason rejected. |
| `OPS-FUZZ-0004` | Break-glass request parser. | Missing reason/expiry/scope denied. |
| `OPS-FUZZ-0005` | Audit export replay metadata. | Sequence gaps and hash mismatches detected. |
| `OPS-FUZZ-0006` | Catalog recovery journal scanner inputs. | Torn/corrupt input cannot produce partial success. |
| `OPS-FUZZ-0007` | Update recovery metadata set. | Rollback/freeze/mix-and-match cannot verify. |
| `OPS-FUZZ-0008` | Guard lockdown recovery request. | Out-of-scope Guard recovery operations fail spec gap. |

## 25. Evidence Artifacts

Operations and recovery evidence MUST include:

- Operator command audit records.
- securityd decision records.
- auditd stream heads before and after recovery.
- Remote export status and backlog records.
- Recovery partition measurement and activation profile.
- Recovery plan manifest, signature, and approval IDs.
- Catalog journal snapshots and recovery result.
- Update metadata set, artifact measurements, rollback decision, and security epoch result.
- Guard root digests, transition IDs, lockdown cause, recovery attestation, and audit root reconciliation for HA.
- Break-glass enter/exit records, reason, expiry, scope, and post-review.
- Incident timeline and post-incident review.
- Residual risk acceptances, if any.

## 26. Spec Gaps

| ID | Gap |
| --- | --- |
| `OPS-GAP-0001` | Concrete recovery plan file format and signature envelope are not specified. |
| `OPS-GAP-0002` | Remote audit collector protocol and failover selection are not specified. |
| `OPS-GAP-0003` | OOB audit path requirements for AUD-L5 are not specified. |
| `OPS-GAP-0004` | Exact recovery partition OS/image composition is not specified. |
| `OPS-GAP-0005` | Full operator authentication and MFA backend are not specified. |
| `OPS-GAP-0006` | Long-term evidence archive storage, retention, and destruction policy are not specified. |
| `OPS-GAP-0007` | Legal/regulatory notification workflow is not specified. |
| `OPS-GAP-0008` | Full SIEM integration schema is not specified. |
| `OPS-GAP-0009` | Hardware platform recovery certification matrix is not specified. |
| `OPS-GAP-0010` | Full side partition incident response workflow is not specified. |
| `OPS-GAP-0011` | Exact Guard isolation recovery mechanism per x64 platform is not specified. |
| `OPS-GAP-0012` | Complete post-incident RCA template is not specified. |

## 27. Inactive Future Implementation Prompt Template

Phase status: inactive future template. This section does not authorize production implementation, hosted daemon implementation, or portable semantic-core implementation.

```text
Future authorized agents would implement or review MFOS operations, recovery, and incident response behavior.

Use this spec:
- docs/design/specs/25-operations-recovery.md

Use these Source Matrix IDs when relevant:
- EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
- EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001
- EXTREF-IBM-ZOS-SECURITY-SERVER-0001
- EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001
- EXTREF-IBM-ZOS-JES-INTRODUCTION-0001
- EXTREF-IBM-ZOS-JES-JOB-FLOW-0001
- EXTREF-IBM-ZOS-JES2-LIBRARY-0001
- EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001
- EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001
- EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001
- EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001
- EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001
- EXTREF-IBM-Z-LPAR-INTRODUCTION-0001
- EXTREF-IBM-Z-DPM-0001
- X64-INTEL-001
- X64-AMD-001
- MS-VBS-001
- MS-VSM-001
- TCG-001
- NIST-160-001
- NIST-193-001
- NIST-218-001
- TUF-001
- SLSA-001
- FBVBS-001

Rules:
- Do not claim z/OS, IBM product, Windows VBS, Linux, UNIX, or z/Architecture compatibility.
- Use typed operator commands, recovery plans, PXM calls, Guard calls, and UVS operations.
- Do not use root shell or ad hoc scripts as the authoritative recovery path.
- securityd remains the policy decision point.
- auditd remains the evidence service.
- Recovery partition is constrained and measured; it is not a policy bypass.
- Break-glass must include reason, expiry, identity, scope, approval when required, and audit.
- Catalog recovery must preserve corrupt ranges and must not hide corruption.
- Update rollback recovery must use verified metadata and security epoch policy.
- Guard lockdown recovery must not disable Guard to restore High-Assurance claims.
- Preserve evidence before destructive repair unless explicit safety policy overrides it.
- Unsupported behavior returns MFOS_ERR_UNSUPPORTED.
- Undefined behavior returns MFOS_ERR_SPEC_GAP.
- No fake success, empty stubs, or silent fallback.

Output:
1. Implemented requirement IDs
2. Source Matrix IDs
3. Operational assumptions
4. Recovery plan or drill IDs
5. Authorization decisions required
6. Audit obligations
7. Fail-closed conditions
8. Evidence artifacts
9. Positive tests
10. Negative tests
11. Fault-injection drills
12. Fuzz targets
13. Spec gaps
14. Residual risks
15. Review checklist
```
