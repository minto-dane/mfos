# MFOS Operator, Auditor, and Security-Admin Training Drills v0.1

Status: Draft assurance training specification

Derived from:

- `docs/design/specs/25-operations-recovery.md`
- `docs/design/assurance/operator-runbooks.md`
- `docs/design/assurance/evidence-archive-spec.md`
- `docs/design/assurance/claim-registry-spec.md`

Audience: MFOS operators, security administrators, audit custodians, recovery operators, incident commanders, reviewers, test engineers, AI implementation agents

MFOS is z/OS-inspired and source-grounded. This document does not claim z/OS, z/Architecture, RACF, JES, DFSMS, SMF, workload policy, APF, PR/SM, Windows VBS, Linux, or UNIX compatibility.

## 1. Purpose

This document defines role-based MFOS operational training, recurring drills, evidence requirements, pass/fail criteria, and reviewer signoff.

Training is part of assurance. An MFOS operator is not considered production-qualified merely by reading runbooks. Operators, auditors, and security administrators must demonstrate that they can execute typed, authorized, audited procedures without bypassing `securityd`, `auditd`, recovery policy, update verification, PXM teardown rules, or Guard requirements.

## 2. Scope

In scope:

- Operator training.
- Auditor/audit-custodian training.
- Security-admin training.
- Recovery-operator training.
- Incident-commander training.
- Drill schedule.
- Drill pass/fail criteria.
- Drill evidence artifacts.
- Break-glass drills.
- Audit outage drills.
- Catalog recovery drills.
- Update rollback drills.
- AMF revocation drills.
- Guard lockdown drills.
- Reviewer signoff and remediation.
- Training gaps.

Out of scope:

- Exact production staffing model.
- HR certification process.
- Legal notification workflow.
- Concrete SIEM product integration.
- Physical data-center access training.
- Implementation of operator command parser.
- Compatibility with IBM operational training or command procedures.

## 3. Source Grounding

| Source ID | Training use |
| --- | --- |
| `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001` | Operators must not use system interfaces to bypass protected resources or authorized state. |
| `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001` | Drills include authorized-boundary confusion and negative tests. |
| `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001` | Security-admin training covers protected resources, profiles, and break-glass governance. |
| `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-JES-JOB-FLOW-0001`, `EXTREF-IBM-ZOS-JES2-LIBRARY-0001` | Operator training covers job/spool state and output handling. |
| `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001` | Recovery training covers dataset/catalog managed-resource recovery. |
| `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001` | Auditor training covers audit evidence, denied attempts, authorities used, and event reasons. |
| `EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001` | Operator training covers workload policy display, overload, and dispatch-hint interpretation. |
| `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `EXTREF-IBM-Z-DPM-0001` | Recovery training covers partition lifecycle and recovery partition discipline. |
| `MS-VBS-001`, `MS-VSM-001` | High-Assurance training covers Guard lockdown concepts without Windows compatibility claims. |
| `TCG-001` | Training covers measured boot, TPM event-log evidence, and attestation collection. |
| `TUF-001`, `SLSA-001` | Update drills cover rollback, freeze, mix-and-match, provenance, and artifact evidence. |
| `NIST-160-001`, `NIST-193-001`, `NIST-218-001` | Training follows secure systems, firmware resiliency, and secure-development operational discipline. |
| `FBVBS-001` | Training requires traceable evidence, negative tests, no fake success, and production proof obligations. |

## 4. Training Principles

`TRN-PRIN-0001` Role-specific competence:
  Training must test the exact role authority required by production operations.

`TRN-PRIN-0002` Pseudo-operator grammar only:
  Drill commands are pseudo-operator grammar, not shell commands and not implementation syntax.

`TRN-PRIN-0003` Evidence before credit:
  A drill run is not passed until evidence artifacts are captured, sealed, reviewed, and signed off.

`TRN-PRIN-0004` Negative path competence:
  Operators must demonstrate correct denial handling, not only successful recovery paths.

`TRN-PRIN-0005` Fail closed:
  Any trainee action that invents success, bypasses audit, bypasses `securityd`, disables Guard for High-Assurance, or hides evidence fails the drill.

`TRN-PRIN-0006` Separation of duties:
  Requester, approver, executor, audit reviewer, and final signoff roles must be distinct where the drill requires dual control.

`TRN-PRIN-0007` No compatibility claims:
  Trainees must use MFOS terminology and must not claim z/OS, IBM product, Windows VBS, Linux, or UNIX compatibility.

## 5. Roles and Required Training

| Role | Required modules | Recertification |
| --- | --- | --- |
| `OPERATOR_VIEWER` | Read-only display, incident declaration basics, evidence awareness. | Semiannual |
| `OPERATOR_CONTROLLER` | Job/spool operations, degraded boot, workload policy display, containment commands. | Quarterly |
| `SECURITY_ADMIN` | Security policy status, break-glass, AMF revocation, emergency approvals. | Quarterly |
| `AUDIT_CUSTODIAN` | Audit outage, export/replay, evidence bundle sealing, chain of custody. | Quarterly |
| `RECOVERY_OPERATOR` | Recovery partition, catalog recovery, update rollback, recovery plan execution. | Quarterly |
| `UPDATE_OPERATOR` | UVS metadata verification, rollback recovery, provenance evidence. | Quarterly |
| `GUARD_RECOVERY_OPERATOR` | Guard lockdown, root verification, HA recovery mode, attestation. | Quarterly for High-Assurance |
| `INCIDENT_COMMANDER` | Severity assignment, containment, evidence preservation, post-incident review. | Semiannual |
| `REVIEWER` | Drill review, evidence validation, residual-risk and claim signoff. | Semiannual |

Qualification rules:

- Production operators must pass all modules required by their assigned role.
- High-Assurance operations require Guard-specific training where Guard is in scope.
- A failed critical drill suspends the trainee's authority for that drill scope until remediation is passed.
- A missed recertification suspends production authority for the affected role.

## 6. Drill Schedule

| Drill ID | Drill | Roles | Minimum frequency | Required profile |
| --- | --- | --- | --- | --- |
| `TRN-BOOT-001` | Boot degraded: auditd unavailable | Operator, auditor | Every release candidate | Baseline+ |
| `TRN-BOOT-002` | Boot degraded: `securityd` unavailable | Operator, security-admin | Every release candidate | Baseline+ |
| `TRN-BOOT-003` | Boot degraded: Guard unavailable | Guard recovery, incident commander | Quarterly | High-Assurance |
| `TRN-AUD-001` | Audit export outage with local queue | Auditor | Quarterly | Enterprise+ |
| `TRN-AUD-002` | Audit export hash mismatch | Auditor, incident commander | Every release candidate | Enterprise+ |
| `TRN-CAT-001` | Catalog torn journal recovery | Recovery operator | Every release candidate | Baseline+ |
| `TRN-CAT-002` | Catalog recovery blocks dataset open | Operator, recovery operator | Every release candidate | Baseline+ |
| `TRN-UPD-001` | Update failed activation rollback | Update operator | Every release candidate | Baseline+ |
| `TRN-UPD-002` | Security epoch downgrade denied | Update operator, security-admin | Quarterly | Enterprise+ |
| `TRN-AMF-001` | AMF revoked signer load denial | Security-admin | Every release candidate | Baseline+ |
| `TRN-AMF-002` | AMF registry Guard transition | Security-admin, Guard recovery | Quarterly | High-Assurance |
| `TRN-GRD-001` | Guard SVC table mismatch lockdown | Guard recovery | Quarterly | High-Assurance |
| `TRN-GRD-002` | Guard audit root append failure | Guard recovery, auditor | Quarterly | High-Assurance |
| `TRN-BG-001` | Break-glass entry and expiry | Security-admin, incident commander | Quarterly | Baseline+ |
| `TRN-BG-002` | Break-glass out-of-scope denial | Security-admin, reviewer | Every release candidate | Baseline+ |
| `TRN-EVD-001` | Evidence bundle capture and seal | Auditor, incident commander | Every release candidate | Baseline+ |
| `TRN-PIR-001` | Post-incident review and claim decision | Incident commander, reviewer | Quarterly | Baseline+ |

Release-candidate gate:

- All `Every release candidate` drills must pass before a production-readiness claim.
- High-Assurance release candidates must also pass every High-Assurance drill marked quarterly if that drill has not passed in the current release cycle.

## 7. Drill Record Schema

```yaml
TrainingDrillRecord:
  drill_id: string
  run_id: uuid
  runbook_id: string
  profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  environment: LAB | STAGING | PRODUCTION_DRILL
  trainee: PrincipalRef
  role_under_test: string
  reviewer: PrincipalRef
  approver: PrincipalRef?
  started_at_utc: timestamp
  completed_at_utc: timestamp?
  incident_id: string
  drill_reason: string
  commands_executed:
    - pseudo_operator_command: string
      expected_result: string
      actual_result: string
      audit_record_ref: AuditRecordRef?
  evidence_artifacts: [EvidenceArtifactRef]
  negative_assertions: [string]
  deviations: [string]
  pass_fail: PASS | FAIL | CONDITIONAL_PASS
  remediation_required: bool
  reviewer_signoff:
    reviewer_id: string
    signed_at_utc: timestamp
    decision: APPROVED | REJECTED | CONDITIONAL
    notes: string
```

## 8. Universal Pass/Fail Criteria

Pass requires:

- Correct role and authenticated operator session.
- Correct incident or drill ID.
- Correct pseudo-operator procedure from the runbook.
- No use of shell commands, root shell assumptions, or ad hoc scripts as authority.
- Required `securityd` authorization decisions present.
- Required `auditd` evidence present.
- Required evidence bundle captured and sealed where applicable.
- Negative assertions verified.
- Fail-closed behavior observed where required.
- Reviewer signoff completed.

Fail conditions:

- Any protected resource is accessed without required authorization.
- Any required audit record is missing and not explained by a fail-closed recovery state.
- Break-glass lacks reason, scope, expiry, identity, approval where required, or exit evidence.
- Catalog recovery hides or deletes corrupt evidence.
- Update rollback uses unverified metadata or unauthorized security epoch downgrade.
- AMF revoked module loads or maps executable pages.
- Guard is disabled to pass a High-Assurance drill.
- Evidence bundle is missing, unsealed, or hash-invalid.
- Trainee claims z/OS, IBM product, Windows VBS, Linux, or UNIX compatibility.
- Trainee treats pseudo-operator grammar as implementation shell commands.

Conditional pass:

- Allowed only for non-security documentation defects.
- Requires reviewer notes, remediation due date, and no missing security evidence.
- Not allowed for High-Assurance Guard drills.

## 9. Evidence Artifact Requirements

Every drill must preserve:

- Drill record.
- Operator session record.
- Pseudo-operator command record.
- `securityd` decision records for protected actions.
- `auditd` stream head before and after the drill.
- Incident or drill ID correlation.
- Expected vs actual result list.
- Reviewer signoff.

Drill-specific evidence:

| Drill class | Required artifacts |
| --- | --- |
| Boot degraded | Boot status, service status, boot measurements, degraded mode, production claim decision. |
| Audit outage | Stream heads, backlog range, collector identity, retry/failover result, replay verification. |
| Securityd recovery | Active policy version, failed transaction IDs, protected-operation denial records. |
| Catalog recovery | Catalog journal head, corrupt range, last good commit, affected DSNs, revoked handles, validation result. |
| Update rollback | Active metadata, previous-good metadata, artifact measurements, security epoch decision, commit/abort result. |
| AMF revocation | Module manifest digest, artifact digest, signer ID, revocation record, denied reload, executable mapping denial. |
| Guard lockdown | Guard state, root type, expected/observed digest, root version, attestation nonce/result, audit root reconciliation. |
| Break-glass | Request, MFA/approval, reason, scope, expiry, emergency actions, exit, derived-handle revocation, post-review. |
| Evidence capture | Evidence bundle manifest, seal, export result, chain-of-custody entries, redaction policy. |
| Post-incident review | Timeline, root cause/unknowns, residual risks, claim decision, spec/test gap list. |

## 10. Training Modules

### 10.1 Operator Module

Required competence:

- Display system, service, job, spool, workload policy, audit, and partition status through pseudo-operator grammar.
- Declare incidents with severity, scope, and reason.
- Hold jobs or protected operations when instructed by runbook.
- Recognize fail-closed behavior and avoid manual bypass.
- Escalate to security-admin, auditor, recovery operator, or incident commander.

Required drills:

- `TRN-BOOT-001`
- `TRN-BOOT-002`
- `TRN-CAT-002`
- `TRN-BG-002`

### 10.2 Auditor Module

Required competence:

- Identify audit stream heads, backlog, export state, and hash-chain continuity.
- Distinguish audit evidence from diagnostic output and spool output.
- Seal evidence bundles.
- Verify chain of custody and redaction boundaries.
- Escalate audit tamper or export mismatch.

Required drills:

- `TRN-AUD-001`
- `TRN-AUD-002`
- `TRN-EVD-001`
- `TRN-GRD-002` for High-Assurance environments.

### 10.3 Security-Admin Module

Required competence:

- Evaluate protected-resource policy state without local authorization shortcuts.
- Enter and exit break-glass with reason, scope, expiry, and approvals.
- Revoke AMF module, signer, digest, or authority class.
- Verify denied reload and no executable mapping after revocation.
- Keep emergency actions within approved scope.

Required drills:

- `TRN-BG-001`
- `TRN-BG-002`
- `TRN-AMF-001`
- `TRN-UPD-002`

### 10.4 Recovery-Operator Module

Required competence:

- Activate recovery partition only through measured approved image.
- Capture evidence before mutation.
- Execute signed recovery plans.
- Run catalog recovery without hiding corruption.
- Validate repaired state and reconcile audit.

Required drills:

- `TRN-CAT-001`
- `TRN-CAT-002`
- `TRN-EVD-001`

### 10.5 Update-Operator Module

Required competence:

- Verify active and previous-good metadata sets.
- Distinguish approved rollback recovery from malicious rollback.
- Enforce generation and security epoch rules.
- Preserve failed activation evidence.

Required drills:

- `TRN-UPD-001`
- `TRN-UPD-002`

### 10.6 Guard-Recovery Module

Required competence:

- Identify Guard lockdown cause.
- Preserve root evidence.
- Verify root digests and versions.
- Perform dual-control recovery.
- Produce nonce-bound attestation before High-Assurance restoration.
- Refuse any path that disables Guard for High-Assurance claims.

Required drills:

- `TRN-BOOT-003`
- `TRN-GRD-001`
- `TRN-GRD-002`
- `TRN-AMF-002`

### 10.7 Incident-Commander Module

Required competence:

- Assign severity.
- Coordinate containment and evidence preservation.
- Decide production claim suspension/restoration.
- Lead post-incident review.
- File spec/test/drill gaps.

Required drills:

- `TRN-PIR-001`
- `TRN-EVD-001`
- `TRN-AUD-002`
- `TRN-BG-001`

## 11. Break-Glass Drill Requirements

Drill IDs:

- `TRN-BG-001`: entry, scoped action, expiry, exit.
- `TRN-BG-002`: out-of-scope denial.

Pseudo-operator drill flow:

```text
DRILL START ID(TRN-BG-001)
DECLARE INCIDENT SEVERITY(SEV-1) SCOPE(<scope>) REASON(DRILL)
REQUEST BREAK_GLASS SCOPE(<scope>) EXPIRY(<timestamp>) REASON(DRILL)
AUTHENTICATE OPERATOR MFA REQUIRED
REQUEST DUAL CONTROL APPROVAL BREAK_GLASS INCIDENT(<incident_id>)
ENTER BREAK_GLASS INCIDENT(<incident_id>) SCOPE(<scope>) EXPIRY(<timestamp>) REASON(DRILL)
EXECUTE APPROVED RECOVERY ACTION SCOPE(<scope>)
EXIT BREAK_GLASS INCIDENT(<incident_id>) REASON(DRILL_COMPLETE)
VERIFY BREAK_GLASS EXIT INCIDENT(<incident_id>)
DRILL COMPLETE
```

Pass criteria:

- Reason, scope, expiry, operator identity, and approval are present.
- Audit enter and exit records exist.
- Emergency action remains within approved scope.
- Expiry revokes derived authority.
- Post-review verifies all actions.

Fail criteria:

- Missing reason, scope, expiry, identity, approval, or audit.
- Action outside approved scope succeeds.
- Break-glass disables audit, securityd, Guard, UVS, catalog integrity checks, or PXM teardown checks.

Required evidence:

- Break-glass request.
- MFA result.
- Approval record.
- Audit enter and exit.
- Scoped action records.
- Derived handle/session revocation.
- Post-review signoff.

## 12. Audit Outage Drill Requirements

Drill IDs:

- `TRN-AUD-001`: remote export outage with safe local queue.
- `TRN-AUD-002`: export replay hash mismatch.

Pseudo-operator drill flow:

```text
DRILL START ID(TRN-AUD-001)
SIMULATE AUDIT EXPORT OUTAGE STREAM(<stream_id>)
DISPLAY AUDIT EXPORT
DISPLAY AUDIT BACKLOG
CAPTURE EVIDENCE AUDIT INCIDENT(<incident_id>)
EXPORT AUDIT RETRY STREAM(<stream_id>)
EXPORT AUDIT REPLAY STREAM(<stream_id>) FROM_LAST_EXPORTED
VERIFY AUDIT EXPORT STREAM(<stream_id>) COLLECTOR(<collector_id>)
DRILL COMPLETE
```

Pass criteria:

- Outage is detected and audited.
- Local stream head remains continuous.
- Backlog sequence range is recorded.
- Retry/replay/reconcile result is recorded.
- Diagnostic output is not treated as audit evidence.

Fail criteria:

- Security-critical events continue after local append failure.
- Export mismatch is ignored.
- Evidence lacks stream head or sequence range.

Required evidence:

- Outage record.
- Stream heads before/after.
- Backlog range.
- Collector identity.
- Replay verification.
- Incident or drill closure record.

## 13. Catalog Recovery Drill Requirements

Drill IDs:

- `TRN-CAT-001`: torn journal recovery.
- `TRN-CAT-002`: affected dataset opens fail closed while quiesced.

Pseudo-operator drill flow:

```text
DRILL START ID(TRN-CAT-001)
SIMULATE CATALOG TORN_JOURNAL CATALOG(<catalog_id>)
QUIESCE CATALOG <catalog_id>
CAPTURE EVIDENCE CATALOG <catalog_id> INCIDENT(<incident_id>)
REQUEST DATASET OPEN DSN(<dsn>) OPERATION(READ)
EXECUTE CATALOG RECOVERY PLAN <plan_id>
VERIFY CATALOG JOURNAL <catalog_id>
VERIFY CATALOG ENTRIES <catalog_id>
RELEASE CATALOG <catalog_id>
DRILL COMPLETE
```

Pass criteria:

- Affected catalog scope is quiesced.
- Affected dataset open fails closed.
- Corrupt journal range is preserved.
- Last good commit is identified.
- Committed entries and security profiles are revalidated.

Fail criteria:

- Corrupt evidence is deleted.
- Dataset open succeeds before validation.
- System dataset immutable flag mismatch is ignored.
- Recovery plan lacks authorization or signature.

Required evidence:

- Catalog journal head.
- Corrupt range.
- Last good commit.
- Affected DSNs and handle revocations.
- Recovery plan ID and approval.
- Validation result.

## 14. Update Rollback Drill Requirements

Drill IDs:

- `TRN-UPD-001`: failed activation recovery.
- `TRN-UPD-002`: security epoch downgrade denied.

Pseudo-operator drill flow:

```text
DRILL START ID(TRN-UPD-001)
SIMULATE UPDATE FAILED_ACTIVATION
FREEZE UPDATE STATE REASON(DRILL)
CAPTURE EVIDENCE UPDATE INCIDENT(<incident_id>)
VERIFY UPDATE METADATA ACTIVE
VERIFY UPDATE METADATA PREVIOUS_GOOD
VERIFY UPDATE SECURITY_EPOCH
STAGE UPDATE RECOVERY PLAN <plan_id>
MEASURE UPDATE RECOVERY ARTIFACTS PLAN(<plan_id>)
ACTIVATE UPDATE RECOVERY PLAN <plan_id>
VALIDATE COMPONENT HEALTH SCOPE(UPDATE_RECOVERY)
COMMIT UPDATE RECOVERY PLAN <plan_id>
DRILL COMPLETE
```

Pass criteria:

- Failed activation metadata is preserved.
- Previous-good metadata is verified.
- Security epoch policy is enforced.
- Recovery artifacts are measured.
- Rollback commit is audited.

Fail criteria:

- Rollback uses timestamps or operator assertion instead of verified metadata.
- Unauthorized security epoch downgrade succeeds.
- Artifact measurement mismatch is ignored.
- Required audit or Guard root update is missing.

Required evidence:

- Active metadata.
- Previous-good metadata.
- Artifact measurements.
- Security epoch decision.
- Recovery plan and approval.
- Activation/commit result.

## 15. AMF Revocation Drill Requirements

Drill IDs:

- `TRN-AMF-001`: revoked signer load denial.
- `TRN-AMF-002`: Guard-sealed AMF registry transition.

Pseudo-operator drill flow:

```text
DRILL START ID(TRN-AMF-001)
DISPLAY AMF MODULE <module_id>
CAPTURE EVIDENCE AMF MODULE(<module_id>) INCIDENT(<incident_id>)
REVOKE AMF SIGNER <signer_id> REASON(DRILL)
REQUEST AMF LOAD MODULE(<module_id>)
ASSERT RESULT(MFOS_ERR_AMF_REVOKED)
ASSERT EXECUTABLE_MAPPING_NOT_CREATED
DRILL COMPLETE
```

Pass criteria:

- Revocation record is present.
- Reload attempt is denied.
- No executable mapping is created.
- High-Assurance AMF registry root transition is Guard-approved where applicable.

Fail criteria:

- Revoked signer/digest can load.
- AMF module maps executable pages after revocation.
- Revocation lacks audit.
- Guard registry transition fails but HA claim remains active.

Required evidence:

- Module manifest digest.
- Artifact digest.
- Signer ID.
- Revocation record.
- Denied load record.
- Executable mapping denial.
- Guard AMF registry root transition for High-Assurance.

## 16. Guard Lockdown Drill Requirements

Drill IDs:

- `TRN-GRD-001`: SVC table mismatch lockdown.
- `TRN-GRD-002`: audit root append failure.

Pseudo-operator drill flow:

```text
DRILL START ID(TRN-GRD-001)
SIMULATE GUARD ROOT_MISMATCH ROOT(SVC_TABLE)
DISPLAY GUARD STATUS
ASSERT GUARD STATE(LOCKDOWN)
CAPTURE EVIDENCE GUARD INCIDENT(<incident_id>)
SELECT RECOVERY PLAN <plan_id> COMPONENT(GUARD) ROOT(SVC_TABLE)
REQUEST DUAL CONTROL APPROVAL PLAN(<plan_id>) REASON(DRILL)
EXECUTE GUARD RECOVERY PLAN <plan_id>
GUARD VERIFY ROOT SVC_TABLE VERSION(<root_version>)
ATTEST GUARD NONCE(<nonce>)
RECONCILE AUDIT ROOT
DRILL COMPLETE
```

Pass criteria:

- Guard enters lockdown or panic-equivalent state.
- Root mismatch evidence is preserved.
- Recovery uses approved plan and dual control.
- Nonce-bound attestation is present.
- Audit root reconciliation succeeds before HA restoration.

Fail criteria:

- Guard disabled to pass the drill.
- Root rollback succeeds without recovery policy.
- Missing attestation.
- Missing audit root reconciliation.
- High-Assurance claim restored without evidence.

Required evidence:

- Guard lockdown cause.
- Root type/version/digests.
- Measurement context.
- Recovery plan and approvals.
- Attestation nonce/result.
- Audit root reconciliation.
- Claim suspension/restoration decision.

## 17. Reviewer Signoff

Reviewer responsibilities:

- Verify trainee role and authority.
- Verify drill command sequence followed the approved runbook.
- Verify every required audit record exists.
- Verify evidence artifacts match expected hashes and references.
- Verify fail-closed behavior for negative assertions.
- Verify no compatibility claims were made.
- Verify no shell/root/ad hoc bypass was used.
- Record deviations and remediation.

Signoff decision:

| Decision | Meaning |
| --- | --- |
| `APPROVED` | Drill passed with required evidence. |
| `REJECTED` | Drill failed or evidence is insufficient. |
| `CONDITIONAL` | Only non-security documentation issue remains; remediation date required. |

Signoff pseudo-record:

```yaml
ReviewerSignoff:
  drill_id: string
  run_id: uuid
  reviewer_id: string
  reviewer_role: REVIEWER | AUDIT_CUSTODIAN | INCIDENT_COMMANDER | SECURITY_ADMIN
  decision: APPROVED | REJECTED | CONDITIONAL
  signed_at_utc: timestamp
  evidence_bundle_ref: EvidenceBundleRef
  audit_stream_head_before: AuditStreamHead
  audit_stream_head_after: AuditStreamHead
  deviations: [string]
  remediation_due_utc: timestamp?
  notes: string
```

Independence rules:

- A trainee MUST NOT approve their own drill.
- Break-glass drills require a reviewer who was not the requester or approver.
- Guard lockdown drills require High-Assurance reviewer competence.
- Audit outage drills require audit-custodian or equivalent reviewer competence.

## 18. Remediation

Failed drill remediation:

```text
FAIL_DRILL
  -> RECORD_FAILURE_REASON
  -> SUSPEND_ROLE_SCOPE
  -> ASSIGN_REMEDIATION
  -> RETRAIN
  -> RERUN_DRILL
  -> REVIEWER_SIGNOFF
  -> RESTORE_ROLE_SCOPE
```

Mandatory suspension triggers:

- Unauthorized protected-resource success.
- Missing required security-critical audit.
- Break-glass scope violation.
- AMF revoked module load success.
- Guard disabled during High-Assurance drill.
- Evidence tamper or missing evidence bundle.
- Attempt to hide catalog corruption.

## 19. Training Metrics

Track per release:

- Drill pass rate by role.
- Mean time to detect.
- Mean time to contain.
- Mean time to evidence capture.
- Mean time to recovery validation.
- Number of fail-closed assertions passed.
- Number of missing evidence artifacts.
- Number of spec gaps discovered.
- Number of runbook updates required.
- Number of claim suspensions/restorations.

Metrics MUST NOT be used to reward unsafe speed over evidence preservation or fail-closed behavior.

## 20. Training Gaps

| ID | Gap |
| --- | --- |
| `TRN-GAP-0001` | Exact operator command parser grammar is not finalized. |
| `TRN-GAP-0002` | Training simulator interface and fault-injection harness are not specified. |
| `TRN-GAP-0003` | Recovery plan file format and signature envelope are not finalized. |
| `TRN-GAP-0004` | Audit collector failover protocol is not finalized. |
| `TRN-GAP-0005` | Evidence archive retention/destruction policy is not finalized. |
| `TRN-GAP-0006` | MFA and identity-provider integration for drills is not finalized. |
| `TRN-GAP-0007` | Guard platform-specific recovery procedure is not finalized. |
| `TRN-GAP-0008` | Production training roster and staffing minimums are not specified. |
| `TRN-GAP-0009` | SIEM/SOC integration training is not specified. |
| `TRN-GAP-0010` | Legal/regulatory notification training is not specified. |
| `TRN-GAP-0011` | Side-partition incident response training is not specified. |
| `TRN-GAP-0012` | Long-term auditor qualification and reviewer independence policy needs governance approval. |

## 21. AI Training Drill Prompt

```text
You are an MFOS operator training and drill assurance agent.

Use:
- docs/design/specs/25-operations-recovery.md
- docs/design/assurance/operator-runbooks.md
- docs/design/assurance/operator-training-drills.md

Rules:
- Do not claim z/OS, IBM product, Windows VBS, Linux, UNIX, or z/Architecture compatibility.
- Commands must be pseudo-operator grammar only.
- Training must be role-specific.
- Every drill must have schedule, entry criteria, pass/fail criteria, evidence artifacts, negative assertions, and reviewer signoff.
- securityd remains the policy decision point.
- auditd remains the evidence service.
- Break-glass drills must verify reason, scope, expiry, identity, approval, audit enter, audit exit, and post-review.
- Audit outage drills must verify stream heads, backlog, replay, and no diagnostic-output-as-evidence.
- Catalog recovery drills must preserve corrupt ranges and fail closed for affected opens.
- Update rollback drills must verify metadata and security epoch policy.
- AMF revocation drills must prove revoked modules cannot load or map executable pages.
- Guard lockdown drills must not disable Guard and must require attestation before restoring High-Assurance claims.
- Reviewer signoff must verify evidence and independence.
- Unknown behavior returns MFOS_ERR_SPEC_GAP.
- Specified but unavailable behavior returns MFOS_ERR_UNSUPPORTED.
- No fake success, empty stubs, or silent fallback.

Output:
1. Drill IDs covered
2. Roles trained
3. Schedule and profile applicability
4. Pseudo-operator commands
5. Pass criteria
6. Fail criteria
7. Evidence artifacts
8. Negative assertions
9. Reviewer signoff
10. Remediation actions
11. Gaps
```
