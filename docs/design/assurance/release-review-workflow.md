# MFOS Release and Independent Review Workflow v0.1

Status: Draft

Audience: release managers, independent reviewers, security reviewers, evidence auditors, CI authors, implementation agents

This document defines the MFOS release candidate and independent review workflow. MFOS is source-grounded and z/OS-inspired, but this workflow must not be used to claim z/OS compatibility, z/Architecture compatibility, IBM API compatibility, RACF compatibility, JES compatibility, DFSMS compatibility, SMP/E compatibility, or IBM product compatibility.

## 1. Purpose

The release workflow ensures that MFOS release claims are supported by reviewed requirements, source grounding, tests, negative tests, fuzz evidence, audit evidence, supply-chain evidence, and assurance records.

The workflow exists to prevent:

- Production claims without production gate evidence.
- High-Assurance claims without PXM Guard evidence.
- Security-sensitive releases without independent review.
- TCB changes entering a release without targeted review.
- Stale source mappings supporting current claims.
- SBOM, provenance, or attestation gaps being hidden.
- Waivers turning into silent acceptance of unsafe behavior.
- Release wording implying compatibility that MFOS does not claim.

## 2. Scope

In scope:

- Release candidate states.
- Release approval state machine.
- Reviewer roles and independence requirements.
- TCB change review.
- Evidence archive and claim registry checks.
- Waiver rules.
- Production readiness gates.
- High-Assurance claim gates.
- SBOM, provenance, and attestation checks.
- Source freshness checks.
- Failure outcomes and required follow-up states.
- AI prompt for release reviewers.

Out of scope:

- External certification workflow.
- Legal approval workflow outside release wording checks.
- Runtime update rollout policy.
- Customer communication process.
- Incident response after release.

## 3. Inputs and Outputs

Required inputs:

- Release candidate ID.
- Claimed profile: Baseline, Enterprise, or High-Assurance.
- Conformance statement.
- Claim registry records.
- Evidence archive manifest.
- Production gate records.
- Source matrix and source freshness report.
- CI report bundle.
- Test and negative test reports.
- Fuzz reports for parsers and external input boundaries.
- SBOM and signed provenance for Enterprise-Standalone, Enterprise-PXM, and High-Assurance.
- Attestation evidence for High-Assurance.
- TCB change list.
- Waiver request list.

Required outputs:

- Release review record.
- Reviewer approval records.
- Gate decision matrix.
- Waiver decision records.
- Release wording review record.
- Updated claim registry status.
- Updated evidence archive references.
- Release decision: APPROVE, APPROVE_WITH_LIMITED_CLAIM, REJECT, HOLD, or ESCALATE.

## 4. Release Candidate States

```text
RC_DRAFT
  -> RC_CUT
  -> RC_EVIDENCE_COLLECTION
  -> RC_AUTOMATED_GATES
  -> RC_INDEPENDENT_REVIEW
  -> RC_SECURITY_REVIEW
  -> RC_RELEASE_WORDING_REVIEW
  -> RC_DECISION
  -> RELEASED
```

Failure and exception states:

```text
RC_REJECTED
RC_HELD
RC_ESCALATED
RC_SUPERSEDED
RC_LIMITED_CLAIM
RC_REWORK_REQUIRED
```

## 5. State Transition Rules

| Current | Trigger | Next | Required |
| --- | --- | --- | --- |
| RC_DRAFT | release manager cuts candidate | RC_CUT | release_id, claimed profile, artifact list |
| RC_CUT | artifacts built | RC_EVIDENCE_COLLECTION | hashes, build logs, initial evidence archive |
| RC_EVIDENCE_COLLECTION | evidence complete enough for automation | RC_AUTOMATED_GATES | claim registry links, test reports, source report |
| RC_AUTOMATED_GATES | automated checks pass or produce waivers | RC_INDEPENDENT_REVIEW | CI, lint, tests, no-fake-success, source freshness |
| RC_INDEPENDENT_REVIEW | independent review complete | RC_SECURITY_REVIEW | TCB and high-risk review disposition |
| RC_SECURITY_REVIEW | security review complete | RC_RELEASE_WORDING_REVIEW | Critical/High issues resolved or validly waived |
| RC_RELEASE_WORDING_REVIEW | wording clean | RC_DECISION | no prohibited compatibility wording |
| RC_DECISION | approved | RELEASED | signed release decision and archive seal |
| any review state | blocking issue found | RC_REWORK_REQUIRED | issue record and owner |
| any review state | non-waivable gate fails | RC_REJECTED | failure record |
| any review state | unresolved external decision | RC_HELD | hold reason |
| any review state | higher authority required | RC_ESCALATED | escalation record |
| RC_REWORK_REQUIRED | replacement candidate cut | RC_SUPERSEDED | supersession link |
| RC_DECISION | reduced profile accepted | RC_LIMITED_CLAIM | limited claim record |

Rules:

- A release candidate must not skip `RC_AUTOMATED_GATES`.
- A release candidate must not reach `RELEASED` with pending required approvals.
- A release candidate must not move from `RC_DECISION` to `RELEASED` until the evidence archive is sealed.
- `RC_LIMITED_CLAIM` may release only after release wording clearly states the reduced claim.

## 6. Reviewer Roles

| Role | Responsibility | Independence |
| --- | --- | --- |
| release_manager | Owns release process and final coordination. | May be project maintainer. |
| architecture_reviewer | Checks design consistency, scope, and profile boundaries. | Peer or independent. |
| security_reviewer | Reviews security-sensitive requirements, threats, and failures. | Peer or independent; independent for production claims. |
| source_grounding_reviewer | Verifies source matrix IDs, source freshness, and wording. | Independent for production claims. |
| evidence_auditor | Verifies evidence archive completeness and hashes. | Independent for production claims. |
| conformance_reviewer | Checks conformance profile and requirement status matrix. | Peer or independent. |
| test_reviewer | Reviews positive, negative, fuzz, crash, and fault-injection evidence. | Peer or independent. |
| supply_chain_reviewer | Verifies SBOM, signed provenance, dependency allowlist, and build evidence. | Independent for Enterprise-Standalone, Enterprise-PXM, and High-Assurance. |
| tcb_reviewer | Reviews trusted computing base changes and unsafe code. | Independent. |
| high_assurance_reviewer | Reviews PXM, Guard, formal, and attestation evidence. | Independent. |
| release_wording_reviewer | Verifies public and internal wording avoids prohibited claims. | Peer or independent. |

## 7. Reviewer Approval Rules

Minimum approvals:

| Release claim | Required approvals |
| --- | --- |
| Baseline non-production | release manager, conformance reviewer, security reviewer for security-sensitive changes |
| Baseline production | release manager, security reviewer, evidence auditor, release wording reviewer |
| Enterprise | release manager, security reviewer, evidence auditor, conformance reviewer, supply-chain reviewer, release wording reviewer |
| High-Assurance | all Enterprise reviewers plus high-assurance reviewer and independent TCB reviewer |

Approval states:

```text
pending
approved
changes_requested
rejected
superseded
expired
```

Rules:

- Authors may not approve their own security-sensitive changes.
- Independent review is required for TCB changes in production, Enterprise, and High-Assurance releases.
- A reviewer approval must reference evidence artifact IDs.
- A reviewer approval must expire if the reviewed artifact is superseded.
- A `changes_requested` or `rejected` approval blocks release.

## 8. TCB Change Review

TCB change review is required when a release modifies:

- nucleus privileged code.
- SVC or PCALL dispatch, ABI, or validation.
- securityd decision logic or policy transaction logic.
- auditd append, hash chain, export, or failure policy.
- catalogd committed metadata path.
- datasetd protected handle creation or validation.
- jobd identity establishment before resource access.
- spoold protected browse, purge, or export path.
- operatord authorization, confirmation, or emergency command logic.
- AMF manifest, signature, revocation, registry, or executable mapping path.
- UVS update metadata, rollback, freeze, mix-and-match, or activation path.
- PXM partition lifecycle, memory assignment, IOMMU, interrupt remapping, or device teardown.
- PXM Guard root seal, verify, executable mapping policy, SVC table verification, AMF registry approval, or attestation.
- unsafe code in any security-sensitive path.
- build, signing, provenance, or release pipeline logic.

TCB review must check:

- Requirement IDs.
- Source matrix IDs.
- Threat boundary.
- New or changed invariants.
- Negative tests.
- Fuzz targets for changed parsers.
- Audit obligations.
- Failure modes.
- Unsafe safety contracts.
- No-fake-success behavior.
- Evidence archive links.

TCB changes cannot be waived for High-Assurance release claims unless the claim is reduced so the changed TCB path is outside the claim.

## 9. Evidence Checks

The evidence auditor must verify:

- Evidence archive manifest exists.
- Archive manifest hash verifies.
- Required artifact hashes verify.
- Required artifact signatures verify.
- Required provenance exists.
- Claim registry references valid artifact IDs.
- Requirement IDs are linked to tests and evidence.
- Source matrix IDs are linked where source-grounded terms are used.
- Security-sensitive claims include negative tests.
- Parser and external input claims include fuzz evidence.
- Audit claims include audit record evidence.
- Production gates have gate evidence records.
- Unresolved gaps are indexed.
- Waivers are recorded and signed where applicable.
- Release wording review evidence exists.

Evidence cannot be counted twice for incompatible claims. For example, a Baseline local audit test cannot by itself support a High-Assurance Guard-sealed audit root claim.

## 10. Automated Gate Checks

Required automated checks:

- `source_matrix_lint`.
- `spec_id_lint`.
- `release_wording_lint`.
- `no_fake_success`.
- `todo_unimplemented_production_path`.
- `audit_obligation_lint`.
- `negative_test_required`.
- `parser_fuzz_registration`.
- `unsafe_inventory`.
- `dependency_allowlist`.
- `sbom_presence`.
- `signed_provenance_presence`.
- `claim_registry_validation`.
- `evidence_archive_validation`.
- `production_gate_matrix_validation`.

High-Assurance additional checks:

- `guard_root_evidence_presence`.
- `pxm_lifecycle_evidence_presence`.
- `attestation_evidence_presence`.
- `formal_evidence_presence`.
- `independent_tcb_review_presence`.

## 11. Production Claim Gates

Production claims must evaluate all gates:

| Gate | Required release check |
| --- | --- |
| PROD-001 | Source Matrix complete for all source-grounded inspired concepts. |
| PROD-002 | System Integrity negative tests pass. |
| PROD-003 | Unauthorized dataset access cannot produce handle. |
| PROD-004 | DENY audit record emitted before caller result. |
| PROD-005 | Catalog crash recovery passes. |
| PROD-006 | Spool browse/purge security enforced. |
| PROD-007 | Operator commands require authority and audit. |
| PROD-008 | AMF invalid signature and revoked signer fail closed. |
| PROD-009 | Update rollback, freeze, and mix-and-match tests pass. |
| PROD-010 | SBOM and signed provenance are produced and archived. |
| PROD-011 | No fake success CI is clean. |
| PROD-012 | Parser fuzz campaigns are complete or explicitly scoped. |
| PROD-013 | PXM device teardown is tested before passthrough production. |
| PROD-014 | Guard evidence exists before High-Assurance claim. |
| PROD-015 | Recovery drill completed and audited. |

Gate status values:

```text
pass
fail
not_applicable
blocked
waived_limited_claim
```

Rules:

- `pass` requires evidence artifact IDs and reviewer approval where required.
- `not_applicable` requires rationale and approval.
- `waived_limited_claim` is allowed only when release wording removes the affected claim.
- `fail` or `blocked` prevents production release.
- High-Assurance claims must not mark PROD-014 as not applicable.

## 12. High-Assurance Claim Gates

High-Assurance release claims require:

- Enterprise gates pass.
- PXM partition lifecycle evidence.
- PXM device assignment and teardown evidence for device claims.
- Guard security root seal and verify evidence.
- Guard audit root seal and verify evidence.
- Guard AMF registry evidence where AMF is claimed.
- Guard executable mapping evidence where executable mapping protection is claimed.
- Guard SVC table verification evidence where SVC integrity is claimed.
- Remote attestation evidence.
- Formal model or proof evidence for claimed root transitions.
- Independent TCB review.
- High-Assurance reviewer approval.

High-Assurance failure rules:

- Missing Guard evidence downgrades or rejects the High-Assurance claim.
- Open Guard-root gaps block the High-Assurance claim.
- Guard scope expansion into job, dataset, spool, or operator business semantics blocks approval until corrected.
- Attestation evidence mismatch rejects the claim.

## 13. SBOM, Provenance, and Attestation Checks

### 13.1 SBOM

Required for Enterprise-Standalone, Enterprise-PXM, and High-Assurance release claims.

Checks:

- SBOM artifact exists.
- SBOM artifact hash verifies.
- SBOM covers release artifacts and dependencies.
- Dependency allowlist result is attached.
- Unknown dependencies are resolved or block release.

### 13.2 Signed Provenance

Required for Enterprise-Standalone, Enterprise-PXM, and High-Assurance release claims.

Checks:

- Provenance artifact exists.
- Provenance signature verifies.
- Provenance binds release artifacts by digest.
- Builder or workflow identity is present.
- Source revision is present when available.
- Toolchain ID is present when available.
- Reproducible build report is attached when required by profile.

### 13.3 Attestation

Required for High-Assurance release claims.

Checks:

- Attestation artifact exists.
- Attestation signature verifies.
- Nonce or freshness input is recorded.
- Measurement context matches claimed artifacts.
- Guard root claims match measurements.
- PXM and Guard versions match release manifest.
- Any mismatch produces `RC_REJECTED` or `RC_LIMITED_CLAIM`.

## 14. Source Freshness Checks

Source freshness checks prevent stale source mappings from supporting current claims.

Required checks:

- Source matrix entries include retrieval or review date.
- Source matrix entries include source document title, URL or publication number, and source ID.
- Source-grounded concepts in release notes and specs link to source IDs.
- Source-grounded concepts changed since last release have source-grounding review.
- x64 hardware claims cite current Intel/AMD or project-approved platform source IDs.
- VBS/VSM-like language is scoped to High-Assurance Guard only.
- Update, supply-chain, and secure development claims cite current project-approved TUF, SLSA, NIST, or TCG source IDs.
- IBM terminology mappings include overlap and MFOS divergence.

Freshness status:

```text
fresh
review_due
stale
unknown
not_applicable
```

Release rules:

- `stale` or `unknown` source status blocks production claims for affected concepts.
- `review_due` may pass only with source-grounding reviewer approval and a follow-up issue.
- High-Assurance root claims cannot rely on `review_due`, `stale`, or `unknown` source status.
- Source freshness checks do not require a compatibility claim and must not introduce one.

## 15. Waiver Rules

Waivers are controlled exceptions. They are not evidence that a claim is true.

Waiver classes:

| Class | Meaning |
| --- | --- |
| test_waiver | A test is temporarily missing or flaky. |
| evidence_waiver | Evidence exists outside the archive or is incomplete. |
| source_waiver | Source freshness review is due but not complete. |
| supply_chain_waiver | SBOM/provenance/dependency artifact is incomplete. |
| profile_waiver | Claim profile is reduced or scoped. |
| release_waiver | Non-production release proceeds with explicit limitation. |

Non-waivable for production claims:

- No fake success failure.
- Missing securityd mediation for protected resource.
- Missing audit for required DENY-before-result.
- Unauthorized dataset handle creation.
- AMF revoked signer accepted.
- Update rollback/freeze/mix-and-match accepted.
- Critical unresolved security gap.
- Release wording that implies prohibited compatibility.

Non-waivable for High-Assurance claims:

- Missing PXM Guard.
- Missing Guard evidence for claimed root.
- Open Guard-root gap.
- Missing independent TCB review.
- Attestation mismatch.
- Guard scope inflation into enterprise semantics.

Waiver record:

```yaml
ReleaseWaiver:
  waiver_id: string
  release_id: string
  waiver_class: test_waiver | evidence_waiver | source_waiver | supply_chain_waiver | profile_waiver | release_waiver
  affected_claim_ids:
    - string
  affected_gate_ids:
    - PROD-001
  severity: critical | high | medium | low
  rationale: string
  compensating_controls:
    - string
  expires_at: date
  approved_by:
    - reviewer_id: string
      role: release | security | evidence | high_assurance | supply_chain | source_grounding
  release_wording_required: bool
  status: requested | approved | rejected | expired | superseded
```

Waivers must expire. Waivers must be archived as evidence artifacts and linked from the claim registry.

## 16. Failure Outcomes

| Failure | Outcome |
| --- | --- |
| Missing required evidence | RC_REWORK_REQUIRED or RC_REJECTED for non-waivable gate. |
| Failed negative test | RC_REJECTED for production security claim. |
| No-fake-success failure | RC_REJECTED. |
| Source freshness stale | RC_HELD or RC_REWORK_REQUIRED. |
| Missing SBOM for Enterprise | RC_REWORK_REQUIRED or RC_LIMITED_CLAIM below Enterprise. |
| Missing signed provenance for Enterprise | RC_REWORK_REQUIRED or RC_LIMITED_CLAIM below Enterprise. |
| Missing attestation for High-Assurance | RC_REWORK_REQUIRED or RC_LIMITED_CLAIM below High-Assurance. |
| TCB review rejected | RC_REJECTED or RC_REWORK_REQUIRED. |
| Waiver rejected | RC_REWORK_REQUIRED or RC_REJECTED. |
| Release wording violation | RC_REWORK_REQUIRED; repeated violation escalates. |
| Critical unresolved gap | RC_REJECTED for production claim. |
| High-Assurance Guard-root gap | RC_REJECTED for High-Assurance claim. |

Failure records must include owner, required fix, blocked claim IDs, blocked gate IDs, and evidence needed for retry.

## 17. Release Decision Record

```yaml
ReleaseDecision:
  release_id: string
  candidate_id: string
  decision: approve | approve_with_limited_claim | reject | hold | escalate
  claimed_profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance | none
  approved_profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance | none
  decision_at_utc: timestamp
  decision_by: string
  non_compatibility_statement: string
  claim_ids:
    - string
  evidence_archive_manifest: string
  claim_registry_ref: string
  production_gate_summary:
    - gate_id: PROD-001
      status: pass | fail | not_applicable | blocked | waived_limited_claim
  reviewer_approvals:
    - approval_id: string
  waivers:
    - waiver_id: string
  unresolved_gaps:
    - gap_id: string
  release_wording_review_ref: string
  sbom_ref: string?
  provenance_ref: string?
  attestation_ref: string?
  required_followups:
    - string
  signature:
    signing_key_id: string?
    signature: string?
```

## 18. Release Wording Rules

Release wording must say what is claimed and what is not claimed.

Required checks:

- No z/OS compatibility claim.
- No z/Architecture compatibility claim.
- No IBM API or IBM product compatibility claim.
- No RACF, JES, DFSMS, SMP/E compatibility claim.
- No statement that PKU/PKS are z/OS storage-key equivalents.
- No Baseline statement that claims Guard root protection.
- No Enterprise statement that implies High-Assurance.
- No High-Assurance statement without root-specific Guard evidence.
- No production wording unless production gates pass.

Allowed wording:

```text
MFOS is source-grounded and z/OS-inspired.
MFOS implements MFOS-defined enterprise semantics for jobs, datasets,
catalogs, spool, operator commands, security decisions, audit evidence,
workload policy, authorized modules, updates, and partition-aware operation.
```

## 19. Workflow Checklist

Release manager:

- [ ] Release candidate ID created.
- [ ] Claimed profile selected.
- [ ] Artifact list complete.
- [ ] Evidence archive initialized.
- [ ] Claim registry updated.
- [ ] Reviewers assigned.

Automated gates:

- [ ] Source matrix lint passed.
- [ ] Spec ID lint passed.
- [ ] No fake success passed.
- [ ] Negative test required check passed.
- [ ] Audit obligation check passed.
- [ ] Parser fuzz registration passed.
- [ ] Unsafe inventory reviewed.
- [ ] Evidence archive validation passed.
- [ ] Claim registry validation passed.

Independent review:

- [ ] TCB changes reviewed.
- [ ] Security-sensitive paths reviewed.
- [ ] Source freshness reviewed.
- [ ] SBOM reviewed where required.
- [ ] Signed provenance reviewed where required.
- [ ] Attestation reviewed for High-Assurance.
- [ ] Waivers approved or rejected.
- [ ] Release wording reviewed.

Decision:

- [ ] Production gates recorded.
- [ ] HA gates recorded if applicable.
- [ ] Failure outcomes closed or release rejected.
- [ ] Evidence archive sealed.
- [ ] Release decision signed.

## 20. AI Prompt

```text
You are the MFOS release and independent review coordinator.
Review the supplied release candidate against the MFOS release workflow.

Do not claim z/OS compatibility, z/Architecture compatibility, IBM API
compatibility, RACF compatibility, JES compatibility, DFSMS compatibility,
SMP/E compatibility, or IBM product compatibility.

Input:
- release candidate ID
- claimed profile
- changed files and TCB change list
- conformance statement
- claim registry records
- evidence archive manifest
- production gate records
- CI reports
- test, negative test, fuzz, crash, and fault-injection reports
- SBOM
- signed provenance
- attestation evidence
- source freshness report
- waiver requests

Output:
1. Release candidate state
2. Claimed profile and approved profile
3. Reviewer roles required
4. TCB change review result
5. Evidence archive check result
6. Claim registry check result
7. Production gate matrix
8. High-Assurance gate matrix
9. SBOM/provenance/attestation result
10. Source freshness result
11. Waiver decisions
12. Release wording findings
13. Failure outcomes
14. Required fixes
15. Final decision

Rules:
- Do not approve production with failed non-waivable gates.
- Do not approve High-Assurance without Guard evidence and attestation.
- Do not approve Enterprise without SBOM and signed provenance unless the
  claim is reduced below Enterprise.
- Do not accept stale source grounding for production claims.
- Treat compatibility wording violations as release blockers.
```

## 21. Spec Gaps

- Exact release signing key hierarchy is not defined.
- Reviewer assignment authority is not defined.
- External legal review is outside this workflow.
- Source freshness age thresholds are not fixed.
- CI job names are normative examples but not implemented here.
- Waiver approval quorum is role-based but not numerically defined.
- Attestation verifier implementation is not specified.
- Release artifact distribution and rollback process are out of scope.

