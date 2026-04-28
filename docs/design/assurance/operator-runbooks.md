# MFOS Operator, Security, Audit, and Recovery Runbooks v0.1

Status: Draft assurance runbook set

Derived from: `docs/design/specs/25-operations-recovery.md`

Audience: MFOS operators, security administrators, audit custodians, recovery operators, incident commanders, test engineers, AI implementation agents

MFOS is z/OS-inspired and source-grounded. These runbooks do not claim z/OS, z/Architecture, RACF, JES, DFSMS, SMF, workload policy, APF, PR/SM, Windows VBS, Linux, or UNIX compatibility.

## 1. Purpose

This document turns the MFOS operations, recovery, and incident response specification into AI-friendly operator runbooks. It is intentionally procedural, but every command shown here is pseudo-operator grammar only. It is not an implementation contract for a concrete CLI parser.

The runbooks cover:

- Boot degraded modes.
- Audit export outage.
- `securityd` recovery mode.
- Catalog recovery.
- Update rollback recovery.
- AMF revocation.
- Guard lockdown.
- Break-glass entry and exit.
- Evidence capture.
- Post-incident review.

## 2. Source Grounding

| Source ID | Runbook use |
| --- | --- |
| `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001` | Prevent operational bypass of system integrity and protected resources. |
| `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001` | Negative drills for authorized-boundary confusion during emergency/recovery. |
| `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001` | Security-manager-inspired protected resource and emergency-access governance. |
| `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-JES-JOB-FLOW-0001`, `EXTREF-IBM-ZOS-JES2-LIBRARY-0001` | Job/spool operational state and output handling. |
| `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001` | Dataset/catalog recovery model. |
| `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001` | Audit/accounting evidence and security event handling. |
| `EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001` | Workload policy display and overload operational handling. |
| `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `EXTREF-IBM-Z-DPM-0001` | Recovery partition and partition lifecycle analogy. |
| `MS-VBS-001`, `MS-VSM-001` | Informative Guard lockdown/recovery concepts for High-Assurance only. |
| `TCG-001` | Measured boot and TPM event-log evidence. |
| `TUF-001`, `SLSA-001` | Update rollback, metadata, provenance, and supply-chain evidence. |
| `NIST-160-001`, `NIST-193-001`, `NIST-218-001` | Secure operations, firmware resiliency, and incident discipline. |
| `FBVBS-001` | Evidence, state-machine, no-fake-success, and production proof obligations. |

## 3. Command Notation

Commands in this file are pseudo-operator grammar.

Rules:

- They describe required operational intent, not exact implementation.
- They MUST be parsed into typed operator command objects before execution.
- They MUST pass `securityd` authorization when protected.
- They MUST produce audit evidence when required.
- They MUST return `MFOS_ERR_UNSUPPORTED` when specified but unavailable.
- They MUST return `MFOS_ERR_SPEC_GAP` when undefined.
- They MUST NOT be treated as root shell commands or scripts.

Pseudo placeholders:

```text
<incident_id>        incident identifier
<reason>             human-readable reason captured in audit
<scope>              bounded object/resource scope
<stream_id>          audit stream identifier
<collector_id>       remote audit collector identifier
<catalog_id>         catalog identifier
<dsn>                dataset name
<bundle_id>          evidence bundle identifier
<policy_id>          security, workload, update, or recovery policy identifier
<plan_id>            signed recovery plan identifier
<module_id>          AMF module identifier
<digest>             cryptographic digest
<partition_id>       partition identifier
<root_type>          Guard root type
<root_version>       Guard root version
<nonce>              attestation nonce
```

## 4. Universal Operator Checks

Before any runbook:

```text
DISPLAY SYSTEM
DISPLAY SERVICES
DISPLAY SECURITY STATUS
DISPLAY AUDIT STATUS
DISPLAY PARTITION MFOS
DISPLAY INCIDENT CURRENT
```

Required checks:

- Operator session is authenticated.
- Role matches the runbook.
- Incident ID exists for incident/recovery actions.
- Correlation ID is assigned.
- Audit path status is known.
- Profile is known: `Baseline`, `Enterprise`, or `High-Assurance`.
- Recovery actions have signed plan IDs when they mutate protected state.

Universal fail-closed rules:

- No incident or drill ID for recovery action: deny.
- No operator identity: deny.
- Required audit unavailable: deny or enter profile-defined recovery mode.
- Unknown command: `MFOS_ERR_SPEC_GAP`.
- Known but unavailable command: `MFOS_ERR_UNSUPPORTED`.
- Target generation changed after approval: revalidate or deny.

## 5. Runbook Record

Every runbook execution MUST produce a record.

```yaml
RunbookRecord:
  runbook_id: string
  run_id: uuid
  incident_id: string
  drill: bool
  profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  operator: PrincipalRef
  approver: PrincipalRef?
  started_at_utc: timestamp
  completed_at_utc: timestamp?
  scope: string
  reason: string
  commands:
    - pseudo_command: string
      expected_result: string
      actual_result: string?
      audit_record_ref: AuditRecordRef?
  evidence_bundle_ref: EvidenceBundleRef?
  deviations: [string]
  pass: bool?
```

## 6. Runbook Index

| ID | Runbook | Primary role |
| --- | --- | --- |
| `RB-BOOT-001` | Boot degraded modes | `OPERATOR_CONTROLLER` |
| `RB-AUD-001` | Audit export outage | `AUDIT_CUSTODIAN` |
| `RB-SEC-001` | `securityd` recovery mode | `SECURITY_ADMIN` |
| `RB-CAT-001` | Catalog recovery | `RECOVERY_OPERATOR` |
| `RB-UPD-001` | Update rollback recovery | `UPDATE_OPERATOR` |
| `RB-AMF-001` | AMF revocation | `SECURITY_ADMIN` |
| `RB-GRD-001` | Guard lockdown recovery | `GUARD_RECOVERY_OPERATOR` |
| `RB-BG-001` | Break-glass entry and exit | `SECURITY_ADMIN` |
| `RB-EVD-001` | Evidence capture | `AUDIT_CUSTODIAN` |
| `RB-PIR-001` | Post-incident review | `INCIDENT_COMMANDER` |

## 7. RB-BOOT-001: Boot Degraded Modes

Purpose:
  Safely classify and handle boot states where MFOS reaches recovery, degraded, or partial service rather than normal operator-ready state.

Entry criteria:

- Boot stops before `OPERATOR_READY`.
- `auditd`, `securityd`, Guard, measured boot, TPM, catalog, or service launch reports degraded state.
- Operator receives boot-degraded console.

Pseudo-operator procedure:

```text
DISPLAY BOOT STATUS
DISPLAY BOOT MEASUREMENTS
DISPLAY SERVICES
DISPLAY AUDIT STATUS
DISPLAY SECURITY STATUS
DISPLAY GUARD STATUS
DISPLAY CATALOG STATUS
DECLARE INCIDENT SEVERITY(SEV-1) SCOPE(BOOT) REASON(<reason>)
CAPTURE EVIDENCE BOOT INCIDENT(<incident_id>)
```

Branch: auditd degraded:

```text
DISPLAY AUDIT STATUS DETAIL
CAPTURE EVIDENCE AUDIT INCIDENT(<incident_id>)
ENTER RECOVERY MODE COMPONENT(AUDITD) REASON(<reason>)
```

Branch: securityd unavailable:

```text
DISPLAY SECURITY STATUS DETAIL
ENTER RECOVERY MODE COMPONENT(SECURITYD) REASON(<reason>)
HOLD PROTECTED OPERATIONS SCOPE(ALL)
```

Branch: Guard unavailable in High-Assurance:

```text
DISPLAY GUARD STATUS DETAIL
ENTER HA RECOVERY MODE REASON(<reason>)
CAPTURE EVIDENCE GUARD INCIDENT(<incident_id>)
```

Expected evidence:

- Boot status record.
- Measurement record or measurement failure.
- Service start/failure records.
- Audit stream head or boot audit sink head.
- Guard status and root states for High-Assurance.
- Incident declaration record.

Fail-closed:

- `securityd` unavailable: protected operations remain denied; only recovery/display subset is available.
- `auditd` unavailable for required event: security-sensitive operations remain denied.
- Guard required but unavailable in High-Assurance: boot denied or HA recovery mode only.
- Missing measured boot evidence in Enterprise-Standalone/Enterprise-PXM/High-Assurance: production claim suspended.

Negative drill:

```text
DRILL START ID(DRILL-BOOT-SECURITYD-MISSING)
SIMULATE BOOT FAILURE COMPONENT(SECURITYD)
ASSERT PROTECTED OPERATION DATASET_OPEN RETURNS(MFOS_ERR_UNAUTHORIZED)
ASSERT OPERATOR COMMAND DISPLAY_SYSTEM ALLOWED
ASSERT INCIDENT DECLARED
DRILL COMPLETE
```

## 8. RB-AUD-001: Audit Export Outage

Purpose:
  Preserve audit evidence and enforce profile-specific behavior when remote export fails.

Entry criteria:

- `DISPLAY AUDIT EXPORT` reports degraded/outage.
- Remote collector unreachable.
- Export replay reports sequence or hash mismatch.
- Local backlog exceeds threshold.

Pseudo-operator procedure:

```text
DISPLAY AUDIT EXPORT
DISPLAY AUDIT STREAMS
DISPLAY AUDIT BACKLOG
DECLARE INCIDENT SEVERITY(SEV-1) SCOPE(AUDIT_EXPORT) REASON(<reason>)
CAPTURE EVIDENCE AUDIT INCIDENT(<incident_id>)
SEAL AUDIT STREAM <stream_id>
EXPORT AUDIT RETRY STREAM(<stream_id>)
```

Failover branch:

```text
DISPLAY AUDIT COLLECTORS
EXPORT AUDIT FAILOVER STREAM(<stream_id>) COLLECTOR(<collector_id>) REASON(<reason>)
DISPLAY AUDIT EXPORT
```

Reconcile branch:

```text
EXPORT AUDIT REPLAY STREAM(<stream_id>) FROM_LAST_EXPORTED
VERIFY AUDIT EXPORT STREAM(<stream_id>) COLLECTOR(<collector_id>)
DISPLAY AUDIT BACKLOG
RESOLVE INCIDENT <incident_id> RESULT(EXPORT_RESTORED)
```

Expected evidence:

- Outage detection audit record.
- Local stream head before retry/failover.
- Collector identity and failure reason.
- Backlog count and sequence range.
- Replay/reconcile result.
- Hash-chain continuity proof.

Fail-closed:

- Local durable append failure: security-critical operations fail closed.
- Local queue full and policy requires remote export: selected operations fail closed.
- Collector identity validation failure: failover denied.
- Export replay hash mismatch: incident escalates to audit tamper workflow.

Negative drill:

```text
DRILL START ID(DRILL-AUDIT-EXPORT-HASH-MISMATCH)
SIMULATE AUDIT EXPORT HASH_MISMATCH STREAM(<stream_id>)
EXPORT AUDIT REPLAY STREAM(<stream_id>)
ASSERT RESULT(AUDIT_TAMPER_DETECTED)
ASSERT INCIDENT SEVERITY_AT_LEAST(SEV-1)
ASSERT NO DIAGNOSTIC_OUTPUT_MARKED_AUDIT_EVIDENCE
DRILL COMPLETE
```

## 9. RB-SEC-001: securityd Recovery Mode

Purpose:
  Keep protected resources fail-closed while restoring or validating `securityd`.

Entry criteria:

- `securityd` unavailable, degraded, corrupt policy, stale policy version, or failed policy transaction.
- Boot enters security recovery mode.
- Authorization decisions cannot be trusted.

Pseudo-operator procedure:

```text
DISPLAY SECURITY STATUS
DISPLAY SECURITY POLICY ACTIVE
DECLARE INCIDENT SEVERITY(SEV-0) SCOPE(SECURITYD) REASON(<reason>)
HOLD PROTECTED OPERATIONS SCOPE(ALL)
CAPTURE EVIDENCE SECURITY INCIDENT(<incident_id>)
VERIFY SECURITY POLICY ROOT
VERIFY SECURITY POLICY TRANSACTIONS
```

Recovery branch:

```text
SELECT RECOVERY PLAN <plan_id> COMPONENT(SECURITYD)
AUTHORIZE RECOVERY PLAN <plan_id> REASON(<reason>)
EXECUTE RECOVERY PLAN <plan_id>
VERIFY SECURITYD STATUS
VERIFY SECURITY POLICY ACTIVE
RELEASE PROTECTED OPERATIONS SCOPE(<scope>)
```

High-Assurance branch:

```text
DISPLAY GUARD ROOT SECURITY_POLICY
GUARD VERIFY ROOT SECURITY_POLICY VERSION(<root_version>)
ATTEST GUARD NONCE(<nonce>)
```

Expected evidence:

- Last known good policy version.
- Failed transaction IDs.
- Security root digest where applicable.
- Recovery plan manifest and approval.
- Denied protected operations during outage.
- Securityd restored status.

Fail-closed:

- Missing security profile: deny.
- Policy malformed/stale/ambiguous: deny.
- Recovery plan unsigned: deny recovery.
- High-Assurance security root mismatch: enter Guard lockdown recovery.

Negative drill:

```text
DRILL START ID(DRILL-SECD-POLICY-MISSING)
SIMULATE SECURITYD POLICY_MISSING
REQUEST DATASET OPEN DSN(<dsn>) OPERATION(READ)
ASSERT RESULT(MFOS_ERR_UNAUTHORIZED)
ASSERT DATASET_HANDLE_NOT_CREATED
ASSERT AUDIT_OR_RECOVERY_RECORD_PRESENT
DRILL COMPLETE
```

## 10. RB-CAT-001: Catalog Recovery

Purpose:
  Recover catalog transaction state while preserving corrupt evidence and preventing unauthorized dataset opens.

Entry criteria:

- Catalog journal torn mid-transaction.
- Catalog generation mismatch.
- Orphan extents detected.
- Integrity tag mismatch.
- System dataset catalog entry inconsistency.

Pseudo-operator procedure:

```text
DISPLAY CATALOG STATUS
DISPLAY CATALOG JOURNAL <catalog_id>
DECLARE INCIDENT SEVERITY(SEV-1) SCOPE(CATALOG:<catalog_id>) REASON(<reason>)
QUIESCE CATALOG <catalog_id>
CAPTURE EVIDENCE CATALOG <catalog_id> INCIDENT(<incident_id>)
DISPLAY DATASET HANDLES SCOPE(CATALOG:<catalog_id>)
REVOKE DATASET HANDLES SCOPE(CATALOG:<catalog_id>) REASON(CATALOG_RECOVERY)
```

Recovery branch:

```text
SELECT RECOVERY PLAN <plan_id> COMPONENT(CATALOGD) TARGET(<catalog_id>)
AUTHORIZE RECOVERY PLAN <plan_id> REASON(<reason>)
EXECUTE CATALOG RECOVERY PLAN <plan_id>
VERIFY CATALOG JOURNAL <catalog_id>
VERIFY CATALOG ENTRIES <catalog_id>
VERIFY DATASET SECURITY PROFILES SCOPE(CATALOG:<catalog_id>)
RELEASE CATALOG <catalog_id>
```

Expected evidence:

- Catalog journal head.
- Last good commit.
- Corrupt range.
- Affected DSNs and handle IDs.
- Recovery plan ID.
- Verification result.
- Audit record proving affected opens failed closed while quiesced.

Fail-closed:

- Persistent dataset open under quiesced catalog: deny.
- Corrupt range cannot be preserved: incident remains open.
- Security profile cannot be revalidated: affected entries remain locked.
- System dataset immutable flag mismatch: keep locked and escalate.

Negative drill:

```text
DRILL START ID(DRILL-CATALOG-TORN-JOURNAL)
SIMULATE CATALOG TORN_JOURNAL CATALOG(<catalog_id>)
QUIESCE CATALOG <catalog_id>
REQUEST DATASET OPEN DSN(<dsn>) OPERATION(READ)
ASSERT RESULT(MFOS_ERR_CATALOG_NOT_FOUND OR MFOS_ERR_INTERNAL_CORRUPTION)
EXECUTE CATALOG RECOVERY PLAN <plan_id>
ASSERT CORRUPT_RANGE_PRESERVED
ASSERT COMMITTED_ENTRIES_VERIFIED
DRILL COMPLETE
```

## 11. RB-UPD-001: Update Rollback Recovery

Purpose:
  Recover from failed update activation, rollback attempts, freeze attacks, mix-and-match metadata, or post-activation health failure.

Entry criteria:

- UVS reports rollback, freeze, mix-and-match, dependency conflict, measurement mismatch, or failed activation.
- Component health checks fail after activation.
- Operator declares update recovery incident.

Pseudo-operator procedure:

```text
DISPLAY UPDATE STATUS
DISPLAY UPDATE METADATA ACTIVE
DISPLAY UPDATE METADATA PREVIOUS_GOOD
DECLARE INCIDENT SEVERITY(SEV-1) SCOPE(UPDATE) REASON(<reason>)
FREEZE UPDATE STATE REASON(<reason>)
CAPTURE EVIDENCE UPDATE INCIDENT(<incident_id>)
VERIFY UPDATE METADATA ACTIVE
VERIFY UPDATE METADATA PREVIOUS_GOOD
VERIFY UPDATE SECURITY_EPOCH
```

Rollback branch:

```text
SELECT RECOVERY PLAN <plan_id> COMPONENT(UVSD) MODE(ROLLBACK)
AUTHORIZE RECOVERY PLAN <plan_id> REASON(<reason>)
STAGE UPDATE RECOVERY PLAN <plan_id>
MEASURE UPDATE RECOVERY ARTIFACTS PLAN(<plan_id>)
ACTIVATE UPDATE RECOVERY PLAN <plan_id>
VALIDATE COMPONENT HEALTH SCOPE(UPDATE_RECOVERY)
COMMIT UPDATE RECOVERY PLAN <plan_id>
```

High-Assurance branch:

```text
DISPLAY GUARD ROOT UPDATE_POLICY
GUARD VERIFY ROOT UPDATE_POLICY VERSION(<root_version>)
GUARD AUTHORIZE ROOT TRANSITION UPDATE_POLICY PLAN(<plan_id>)
ATTEST GUARD NONCE(<nonce>)
```

Expected evidence:

- Active metadata set.
- Previous-good metadata set.
- Artifact hashes and sizes.
- Security epoch check.
- Rollback authorization.
- Measurement results.
- Guard update policy root transition in High-Assurance.

Fail-closed:

- Previous-good metadata unverifiable: deny rollback.
- Security epoch downgrade unauthorized: deny rollback.
- Artifact measurement mismatch: deny activation.
- Required audit or Guard root update fails: deny recovery commit.

Negative drill:

```text
DRILL START ID(DRILL-UPDATE-SECURITY-EPOCH-DOWNGRADE)
SIMULATE UPDATE ROLLBACK SECURITY_EPOCH_DOWNGRADE
AUTHORIZE RECOVERY PLAN <plan_id> MODE(ROLLBACK)
ASSERT RESULT(MFOS_ERR_ROLLBACK_DETECTED OR MFOS_ERR_POLICY_DENIED)
ASSERT UPDATE_NOT_ACTIVATED
ASSERT AUDIT_SECURITY_CRITICAL_PRESENT
DRILL COMPLETE
```

## 12. RB-AMF-001: AMF Revocation

Purpose:
  Revoke an authorized module signer, digest, authority class, or registry entry and ensure future load/execute paths fail closed.

Entry criteria:

- AMF signer compromised.
- Module digest revoked.
- Authority class overbroad.
- AMF module implicated in incident.
- AMF registry mismatch detected.

Pseudo-operator procedure:

```text
DISPLAY AMF MODULE <module_id>
DISPLAY AMF REGISTRY
DECLARE INCIDENT SEVERITY(SEV-0) SCOPE(AMF:<module_id>) REASON(<reason>)
CAPTURE EVIDENCE AMF MODULE(<module_id>) INCIDENT(<incident_id>)
HOLD AMF MODULE <module_id> REASON(<reason>)
REVOKE AMF MODULE <module_id> REASON(<reason>)
REVOKE AMF DIGEST <digest> REASON(<reason>)
```

Signer branch:

```text
REVOKE AMF SIGNER <signer_id> REASON(<reason>)
VERIFY AMF REVOCATION MODULE(<module_id>)
REQUEST AMF LOAD MODULE(<module_id>)
ASSERT AMF LOAD DENIED
```

High-Assurance branch:

```text
DISPLAY GUARD ROOT AMF_REGISTRY
GUARD VERIFY ROOT AMF_REGISTRY VERSION(<root_version>)
GUARD AUTHORIZE ROOT TRANSITION AMF_REGISTRY REASON(<reason>)
ATTEST GUARD NONCE(<nonce>)
```

Expected evidence:

- Module manifest digest.
- Artifact digest.
- Signer ID.
- Authority class.
- Revocation decision.
- Registry generation before/after.
- Denied reload attempt.
- Guard AMF registry root transition in High-Assurance.

Fail-closed:

- Revocation metadata cannot be written: hold module and deny load.
- Guard registry transition fails in High-Assurance: remain locked/held.
- Attempted load of revoked digest: deny, no executable mapping.

Negative drill:

```text
DRILL START ID(DRILL-AMF-REVOKED-SIGNER)
REVOKE AMF SIGNER <signer_id> REASON(DRILL)
REQUEST AMF LOAD MODULE(<module_id>)
ASSERT RESULT(MFOS_ERR_AMF_REVOKED)
ASSERT EXECUTABLE_MAPPING_NOT_CREATED
ASSERT AUDIT_AMF_DENY_PRESENT
DRILL COMPLETE
```

## 13. RB-GRD-001: Guard Lockdown Recovery

Purpose:
  Preserve evidence and safely handle Guard root mismatch, SVC table mismatch, audit root append failure, executable mapping violation, or Guard metadata corruption.

Entry criteria:

- Guard enters `LOCKDOWN`.
- Guard reports root mismatch.
- High-Assurance boot cannot reach Guard ready state.
- Guard audit root append fails.
- SVC table mismatch detected.

Pseudo-operator procedure:

```text
DISPLAY GUARD STATUS
DISPLAY GUARD ROOTS
DECLARE INCIDENT SEVERITY(SEV-0) SCOPE(GUARD) REASON(<reason>)
FREEZE GUARD ROOT TRANSITIONS SCOPE(<scope>)
CAPTURE EVIDENCE GUARD INCIDENT(<incident_id>)
ENTER HA RECOVERY MODE REASON(<reason>)
```

Recovery branch:

```text
SELECT RECOVERY PLAN <plan_id> COMPONENT(GUARD) ROOT(<root_type>)
REQUEST DUAL CONTROL APPROVAL PLAN(<plan_id>) REASON(<reason>)
AUTHORIZE RECOVERY PLAN <plan_id> REASON(<reason>)
VERIFY GUARD MEASUREMENTS
EXECUTE GUARD RECOVERY PLAN <plan_id>
GUARD VERIFY ROOT <root_type> VERSION(<root_version>)
ATTEST GUARD NONCE(<nonce>)
RECONCILE AUDIT ROOT
EXIT HA RECOVERY MODE REASON(<reason>)
```

Expected evidence:

- Lockdown cause.
- Root type and version.
- Expected and observed root digest.
- Measurement context.
- Recovery plan and dual-control approval.
- Nonce-bound attestation.
- Audit root reconciliation result.

Fail-closed:

- Attempt to disable Guard: deny.
- Guard rollback without recovery policy: deny.
- Audit root reconciliation fails: remain in lockdown/recovery.
- Attestation fails: production High-Assurance claim remains suspended.

Negative drill:

```text
DRILL START ID(DRILL-GUARD-SVC-MISMATCH)
SIMULATE GUARD ROOT_MISMATCH ROOT(SVC_TABLE)
ASSERT GUARD STATE(LOCKDOWN)
CAPTURE EVIDENCE GUARD INCIDENT(<incident_id>)
EXECUTE GUARD RECOVERY PLAN <plan_id>
ASSERT ATTESTATION_PRESENT
ASSERT AUDIT_ROOT_RECONCILED
DRILL COMPLETE
```

## 14. RB-BG-001: Break-Glass Entry and Exit

Purpose:
  Temporarily grant scoped emergency authority for recovery while preserving authorization and audit.

Entry criteria:

- Normal policy blocks necessary repair.
- Incident commander approves emergency path.
- Reason, scope, expiry, and operator identity are known.

Pseudo-operator entry:

```text
DECLARE INCIDENT SEVERITY(SEV-1) SCOPE(<scope>) REASON(<reason>)
REQUEST BREAK_GLASS SCOPE(<scope>) EXPIRY(<timestamp>) REASON(<reason>)
AUTHENTICATE OPERATOR MFA REQUIRED
REQUEST DUAL CONTROL APPROVAL BREAK_GLASS INCIDENT(<incident_id>)
ENTER BREAK_GLASS INCIDENT(<incident_id>) SCOPE(<scope>) EXPIRY(<timestamp>) REASON(<reason>)
DISPLAY BREAK_GLASS STATUS
```

High-Assurance entry:

```text
GUARD AUTHORIZE EMERGENCY_MODE INCIDENT(<incident_id>) SCOPE(<scope>)
GUARD VERIFY ROOT EMERGENCY_STATE
```

Pseudo-operator exit:

```text
DISPLAY BREAK_GLASS STATUS
EXIT BREAK_GLASS INCIDENT(<incident_id>) REASON(RECOVERY_COMPLETE)
REVOKE BREAK_GLASS DERIVED_HANDLES INCIDENT(<incident_id>)
VERIFY BREAK_GLASS EXIT INCIDENT(<incident_id>)
DISPLAY AUDIT BREAK_GLASS INCIDENT(<incident_id>)
```

Post-review:

```text
REVIEW BREAK_GLASS INCIDENT(<incident_id>)
VERIFY ACTIONS WITHIN_SCOPE INCIDENT(<incident_id>)
VERIFY EXPIRY ENFORCED INCIDENT(<incident_id>)
APPROVE POST_INCIDENT REVIEW INCIDENT(<incident_id>)
```

Expected evidence:

- Entry request.
- MFA result.
- Dual-control approval.
- Scope and expiry.
- Guard emergency-state root transition when required.
- Every emergency command.
- Exit and derived handle revocation.
- Post-review result.

Fail-closed:

- Missing reason: deny.
- Missing expiry: deny.
- Missing audit: deny.
- Action outside scope: deny.
- Expired break-glass token/session/handle: deny.

Negative drill:

```text
DRILL START ID(DRILL-BREAK-GLASS-OUT-OF-SCOPE)
ENTER BREAK_GLASS INCIDENT(<incident_id>) SCOPE(DATASET:<dsn>) EXPIRY(<timestamp>) REASON(DRILL)
REQUEST OPERATOR COMMAND SCOPE(AMF) COMMAND(REVOKE_AMF_MODULE)
ASSERT RESULT(MFOS_ERR_UNAUTHORIZED)
ASSERT AUDIT_BREAK_GLASS_DENY_PRESENT
EXIT BREAK_GLASS INCIDENT(<incident_id>)
DRILL COMPLETE
```

## 15. RB-EVD-001: Evidence Capture

Purpose:
  Capture evidence before destructive repair or profile-claim restoration.

Entry criteria:

- Incident declared.
- Recovery action planned.
- Audit tamper, catalog corruption, update failure, AMF revocation, Guard lockdown, or degraded boot detected.

Pseudo-operator procedure:

```text
DISPLAY INCIDENT <incident_id>
CREATE EVIDENCE BUNDLE INCIDENT(<incident_id>) SCOPE(<scope>)
CAPTURE AUDIT STREAM_HEADS INCIDENT(<incident_id>)
CAPTURE OPERATOR COMMANDS INCIDENT(<incident_id>)
CAPTURE SECURITY DECISIONS INCIDENT(<incident_id>)
CAPTURE BOOT MEASUREMENTS INCIDENT(<incident_id>)
CAPTURE UPDATE METADATA INCIDENT(<incident_id>)
CAPTURE CATALOG JOURNAL SCOPE(<scope>) INCIDENT(<incident_id>)
CAPTURE PXM PARTITION STATE INCIDENT(<incident_id>)
CAPTURE GUARD ROOTS INCIDENT(<incident_id>)
SEAL EVIDENCE BUNDLE INCIDENT(<incident_id>)
VERIFY EVIDENCE BUNDLE INCIDENT(<incident_id>)
```

Export branch:

```text
EXPORT EVIDENCE BUNDLE INCIDENT(<incident_id>) DESTINATION(<collector_id>)
VERIFY EVIDENCE EXPORT INCIDENT(<incident_id>)
RECORD CHAIN_OF_CUSTODY INCIDENT(<incident_id>) ACTION(EXPORT)
```

Expected evidence:

- Evidence bundle ID.
- Stream heads.
- Hashes for captured metadata.
- Chain-of-custody entries.
- Export/verification records.
- Redaction policy for export views.

Fail-closed:

- Evidence bundle cannot be sealed: incident remains open.
- Hash mismatch on export: reject export and start tamper workflow.
- Missing Guard root for HA Guard incident: HA claim remains suspended.

Negative drill:

```text
DRILL START ID(DRILL-EVIDENCE-EXPORT-HASH-MISMATCH)
CREATE EVIDENCE BUNDLE INCIDENT(<incident_id>) SCOPE(DRILL)
SIMULATE EVIDENCE EXPORT HASH_MISMATCH
VERIFY EVIDENCE EXPORT INCIDENT(<incident_id>)
ASSERT RESULT(AUDIT_TAMPER_DETECTED)
ASSERT INCIDENT_NOT_CLOSED
DRILL COMPLETE
```

## 16. RB-PIR-001: Post-Incident Review

Purpose:
  Close the loop after incident response and identify spec, test, source, drill, and production-claim updates.

Entry criteria:

- Recovery validation complete or incident contained with accepted residual risk.
- Evidence bundle sealed.
- Incident commander starts review.

Pseudo-operator procedure:

```text
DISPLAY INCIDENT <incident_id>
DISPLAY EVIDENCE BUNDLE INCIDENT(<incident_id>)
DISPLAY AUDIT TIMELINE INCIDENT(<incident_id>)
DISPLAY RECOVERY ACTIONS INCIDENT(<incident_id>)
REVIEW INCIDENT ROOT_CAUSE INCIDENT(<incident_id>)
REVIEW INCIDENT RESIDUAL_RISK INCIDENT(<incident_id>)
REVIEW INCIDENT PROFILE_CLAIMS INCIDENT(<incident_id>)
REVIEW INCIDENT SPEC_GAPS INCIDENT(<incident_id>)
REVIEW INCIDENT TEST_GAPS INCIDENT(<incident_id>)
APPROVE POST_INCIDENT REVIEW INCIDENT(<incident_id>)
RESOLVE INCIDENT <incident_id> RESULT(<result>)
```

Required review questions:

- Which asset, boundary, or invariant failed?
- Was protected-resource access ever incorrectly allowed?
- Were DENY records emitted before caller-visible denial?
- Did audit evidence remain continuous?
- Did recovery preserve corrupt or suspicious state?
- Did break-glass stay within scope and expiry?
- Did Guard remain enabled for High-Assurance claims?
- Are production claims still valid?
- Which negative test or drill must be added?
- Which spec gap must be filed?

Expected evidence:

- Timeline.
- Root cause or unknown statement.
- Residual risk statement.
- Spec gap list.
- Test/drill additions.
- Claim suspension or restoration decision.
- Approval record.

Fail-closed:

- Evidence bundle missing: incident cannot fully close.
- Audit timeline has unexplained gap: incident cannot fully close.
- HA Guard evidence missing after Guard-related incident: High-Assurance claim remains suspended.
- Residual risk unapproved: production claim remains suspended.

Negative drill:

```text
DRILL START ID(DRILL-POST-INCIDENT-MISSING-EVIDENCE)
SIMULATE INCIDENT CLOSED_WITHOUT_EVIDENCE
APPROVE POST_INCIDENT REVIEW INCIDENT(<incident_id>)
ASSERT RESULT(MFOS_ERR_POLICY_DENIED)
ASSERT INCIDENT_REMAINS_OPEN
DRILL COMPLETE
```

## 17. Drill Matrix

| Drill | Runbook | Required profile | Required evidence |
| --- | --- | --- | --- |
| Boot degraded auditd unavailable | `RB-BOOT-001` | Baseline+ | Boot status, audit failure, degraded mode record. |
| Boot degraded securityd unavailable | `RB-BOOT-001`, `RB-SEC-001` | Baseline+ | Protected operations denied, recovery mode record. |
| Boot degraded Guard unavailable | `RB-BOOT-001`, `RB-GRD-001` | High-Assurance | HA recovery or boot denial, Guard evidence. |
| Audit export outage | `RB-AUD-001` | Enterprise+ | Backlog, retry/failover, replay continuity. |
| securityd recovery mode | `RB-SEC-001` | Baseline+ | Policy root/version, denied protected operations. |
| Catalog recovery | `RB-CAT-001` | Baseline+ | Journal evidence, corrupt range preserved. |
| Update rollback | `RB-UPD-001` | Baseline+ | Verified metadata, epoch decision, activation result. |
| AMF revocation | `RB-AMF-001` | Baseline+ | Revocation, denied reload, no executable mapping. |
| Guard lockdown | `RB-GRD-001` | High-Assurance | Root mismatch, lockdown, attestation. |
| Break-glass entry/exit | `RB-BG-001` | Baseline+ | Reason, scope, expiry, approvals, exit. |
| Evidence capture | `RB-EVD-001` | Baseline+ | Sealed bundle, chain of custody. |
| Post-incident review | `RB-PIR-001` | Baseline+ | Timeline, residual risk, spec/test gaps. |

## 18. Runbook Fail-Closed Summary

| Condition | Required result |
| --- | --- |
| Required audit unavailable | Deny operation or enter profile-defined recovery mode. |
| securityd unavailable | Protected operations denied; recovery/display subset only. |
| Recovery plan unsigned or invalid | Deny recovery action. |
| Recovery image measurement mismatch | Deny recovery partition activation. |
| Catalog corrupt and not recovered | Dataset opens in affected scope fail closed. |
| Update metadata unverifiable | Deny activation or rollback commit. |
| AMF revoked signer/digest | Deny load; no executable mapping. |
| Guard required but unavailable | HA boot denied or HA recovery mode only. |
| Guard root mismatch | Lockdown or panic-equivalent until approved recovery. |
| Break-glass missing reason/scope/expiry | Deny entry. |
| Evidence capture fails | Keep incident open and suspend affected profile claim. |
| Post-incident review lacks evidence | Incident cannot fully close. |

## 19. Runbook Gaps

| ID | Gap |
| --- | --- |
| `RB-GAP-0001` | Exact operator command parser grammar is not finalized. |
| `RB-GAP-0002` | Concrete recovery plan file format and signature envelope are not finalized. |
| `RB-GAP-0003` | Remote audit collector failover protocol is not finalized. |
| `RB-GAP-0004` | Recovery partition image composition and minimal tool list are not finalized. |
| `RB-GAP-0005` | MFA and identity provider integration for emergency operations is not finalized. |
| `RB-GAP-0006` | Evidence archive retention and destruction workflow is not finalized. |
| `RB-GAP-0007` | Guard platform-specific recovery mechanism is not finalized. |
| `RB-GAP-0008` | AMF quarantine versus revocation operational distinction needs a dedicated policy. |
| `RB-GAP-0009` | Production operator training frequency and signoff policy are not finalized. |
| `RB-GAP-0010` | SIEM/SOC integration fields are not finalized. |

## 20. AI Runbook Prompt

```text
You are an MFOS operations and recovery runbook agent.

Use:
- docs/design/specs/25-operations-recovery.md
- docs/design/assurance/operator-runbooks.md

Rules:
- Do not claim z/OS, IBM product, Windows VBS, Linux, UNIX, or z/Architecture compatibility.
- Commands must be pseudo-operator grammar only, not implementation shell commands.
- Every recovery action must have role, entry criteria, procedure, expected evidence, fail-closed behavior, and negative drill.
- securityd remains the policy decision point.
- auditd remains the evidence service.
- Break-glass must include reason, scope, expiry, identity, approval when required, audit enter, audit exit, and post-review.
- Recovery partition must be measured, constrained, and evidence-preserving.
- Catalog recovery must preserve corrupt ranges and must not hide corruption.
- Update rollback must use verified metadata and security epoch policy.
- AMF revocation must prevent future load and executable mapping.
- Guard lockdown recovery must not disable Guard to restore High-Assurance claims.
- Evidence capture must happen before destructive repair unless explicit safety policy overrides it.
- Unknown behavior returns MFOS_ERR_SPEC_GAP.
- Specified but unavailable behavior returns MFOS_ERR_UNSUPPORTED.
- No fake success, empty stubs, or silent fallback.

Output:
1. Runbook IDs covered
2. Source Matrix IDs used
3. Roles required
4. Entry criteria
5. Pseudo-operator commands
6. Expected audit evidence
7. Evidence bundle contents
8. Fail-closed behavior
9. Negative drills
10. Remaining gaps
11. Review checklist
```
