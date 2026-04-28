# MFOS Assurance Claim Registry Specification v0.1

Status: Draft

Audience: assurance authors, release reviewers, security reviewers, implementation agents, evidence auditors

This document defines the MFOS assurance claim registry. MFOS is source-grounded and z/OS-inspired, but registered claims must not state or imply z/OS compatibility, z/Architecture compatibility, IBM API compatibility, RACF compatibility, JES compatibility, DFSMS compatibility, SMP/E compatibility, or IBM product compatibility.

## 1. Purpose

The claim registry is the authoritative index of MFOS assurance and conformance claims. It records claim IDs, profile applicability, requirement and source links, evidence artifacts, reviewer approvals, release gate status, unresolved gaps, and claim lifecycle state.

The registry prevents orphan claims and release wording drift. If a claim is not in the registry, it is not an MFOS assurance claim.

## 2. Scope

In scope:

- Claim ID allocation.
- Claim classes and lifecycle.
- Claim registry layout.
- Claim record schema.
- Relationship to evidence archive.
- Relationship to requirements, tests, source IDs, and production gates.
- Reviewer approvals.
- Profile claims.
- Unresolved gaps and blocked claims.
- Release claim checks.
- AI prompt for claim registry authors.

Out of scope:

- External certification mapping.
- Legal warranty wording.
- Runtime audit log schema.
- Evidence artifact storage layout beyond references to the evidence archive.

## 3. Registry Location

Recommended repository path:

```text
docs/design/assurance/claims/
  registry.yaml
  claims/
    MFOS-CLAIM-BASELINE-SYSINT-0001.yaml
    MFOS-CLAIM-BASELINE-AUDIT-0001.yaml
    MFOS-CLAIM-HA-GUARD-0001.yaml
```

Recommended release archive path:

```text
artifacts/assurance/<release_id>/claims/
```

## 4. Claim ID Format

```text
MFOS-CLAIM-<PROFILE>-<DOMAIN>-<NNNN>
```

Profile codes:

| Profile | Meaning |
| --- | --- |
| BASELINE | Baseline profile claim. |
| ENTERPRISE-STANDALONE | Enterprise profile without partition-manager claims. |
| ENTERPRISE-PXM | Enterprise profile with partition-manager claims. |
| HA | High-Assurance profile claim. |
| PROD | Production-readiness gate claim. |

Domain codes use MFOS-owned names such as SOURCE, SYSINT, AUTH, AUDIT,
CATALOG, DATASET, JOB, SPOOL, OPER, workload policy, AMF, UPDATE, NUCLEUS, SVC, PCALL,
PARTITION, GUARD, SUPPLY, CONFORMANCE, and READINESS.

Examples:

```text
MFOS-CLAIM-BASELINE-SYSINT-0001
MFOS-CLAIM-BASELINE-AUDIT-0002
MFOS-CLAIM-PROD-READINESS-0001
MFOS-CLAIM-HA-GUARD-0001
```

## 5. Claim Classes

| Class | Meaning |
| --- | --- |
| design_claim | A design-level property supported by specs and requirements. |
| implementation_claim | A property supported by code and tests. |
| test_claim | A property supported by specific test suites. |
| audit_claim | A property supported by audit evidence. |
| supply_chain_claim | A property supported by SBOM, provenance, signatures, or build evidence. |
| conformance_claim | A profile conformance statement. |
| production_claim | A production readiness statement. |
| high_assurance_claim | A Guard/PXM/formal/attestation backed claim. |
| negative_claim | A denial property, such as unauthorized dataset open cannot produce a handle. |

## 6. Claim Levels

| Level | Meaning |
| --- | --- |
| CLAIM-L0 | Design intent only. |
| CLAIM-L1 | Requirements and source links exist. |
| CLAIM-L2 | Positive and negative tests exist and pass. |
| CLAIM-L3 | Implementation and tests are reviewed. |
| CLAIM-L4 | Release evidence is archived. |
| CLAIM-L5 | High-Assurance evidence exists, including Guard/PXM/formal/attestation where applicable. |

Claim level must not exceed the weakest required evidence link.

## 7. Claim Lifecycle

```text
DRAFT
  -> READY_FOR_REVIEW
  -> REVIEWED
  -> EVIDENCED
  -> RELEASED
  -> RETIRED
```

Failure and exception states:

```text
BLOCKED
REJECTED
SUPERSEDED
EXPIRED
```

Rules:

- `DRAFT` claims may be incomplete.
- `READY_FOR_REVIEW` claims must have requirement IDs, source IDs, scope, assumptions, and initial evidence links.
- `REVIEWED` claims must have required reviewer approvals.
- `EVIDENCED` claims must link to hash-verified evidence artifacts.
- `RELEASED` claims must link to a release archive and production gate state if production is claimed.
- `BLOCKED` claims must list unresolved gaps.

## 8. Registry Index Schema

```yaml
ClaimRegistry:
  registry_version: 1
  registry_id: string
  updated_at_utc: timestamp
  updated_by: string
  non_compatibility_statement: string
  claim_index:
    - claim_id: string
      path: string
      title: string
      claim_class: string
      profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
      status: DRAFT | READY_FOR_REVIEW | REVIEWED | EVIDENCED | RELEASED | RETIRED | BLOCKED | REJECTED | SUPERSEDED | EXPIRED
  release_claims:
    - release_id: string
      claimed_profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
      claim_ids:
        - string
  unresolved_gaps_ref: string
  evidence_archive_refs:
    - release_id: string
      archive_manifest: string
  registry_hash:
    algorithm: sha384
    value: hex
  registry_signature:
    signing_key_id: string?
    signature: string?
    signed_at_utc: timestamp?
```

The `non_compatibility_statement` must prohibit compatibility claims with z/OS and IBM products.

## 9. Claim Record Schema

```yaml
AssuranceClaimRecord:
  claim_id: string
  title: string
  claim_class: design_claim | implementation_claim | test_claim | audit_claim | supply_chain_claim | conformance_claim | production_claim | high_assurance_claim | negative_claim
  profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  claim_level: CLAIM-L0 | CLAIM-L1 | CLAIM-L2 | CLAIM-L3 | CLAIM-L4 | CLAIM-L5
  status: DRAFT | READY_FOR_REVIEW | REVIEWED | EVIDENCED | RELEASED | RETIRED | BLOCKED | REJECTED | SUPERSEDED | EXPIRED
  statement: string
  non_compatibility_statement: string
  scope:
    in_scope:
      - string
    out_of_scope:
      - string
  source_matrix_ids:
    - string
  requirement_ids:
    - string
  ai_contract_ids:
    - AI-MFOS-001
  design_refs:
    - path: string
      section: string?
  implementation_refs:
    - path: string
      symbol: string?
  tests:
    positive:
      - test_id: string
    negative:
      - test_id: string
    fuzz:
      - target_id: string
    fault_injection:
      - test_id: string
    crash_recovery:
      - test_id: string
  audit_obligations:
    - operation: string
      ordering: before_result | after_commit | periodic | not_applicable
      evidence_artifact_ids:
        - string
  invariants:
    - string
  failure_modes:
    - string
  evidence_artifacts:
    - artifact_id: string
      required: bool
  production_gates:
    - gate_id: PROD-001
      status: pass | fail | not_applicable | blocked
      evidence_artifact_ids:
        - string
  profile_claims:
    baseline: supported | not_supported | not_applicable | blocked
    enterprise: supported | not_supported | not_applicable | blocked
    high_assurance: supported | not_supported | not_applicable | blocked
  reviewer_approvals:
    - approval_id: string
  assumptions:
    - assumption_id: string
      text: string
      impact_if_false: string
  unsupported_features:
    - feature: string
      failure_mode: string
      evidence_artifact_ids:
        - string
  spec_gaps:
    - gap_id: string
  residual_risks:
    - risk_id: string
      severity: critical | high | medium | low
      mitigation: string
      accepted_by: string?
  supersedes:
    - claim_id: string
  superseded_by: string?
  provenance:
    created_by: string
    created_at_utc: timestamp
    updated_by: string
    updated_at_utc: timestamp
    source_revision: string?
  hash:
    algorithm: sha384
    value: hex
  signature:
    required: bool
    signing_key_id: string?
    signature: string?
    signed_at_utc: timestamp?
```

## 10. Required Claim Relationships

Every active claim must link to:

- At least one requirement ID.
- At least one design reference.
- At least one source matrix ID when source-grounded terms are used.
- At least one evidence artifact for CLAIM-L2 or higher.
- Reviewer approval for CLAIM-L3 or higher.
- Release archive evidence for CLAIM-L4 or higher.
- Guard/PXM/formal/attestation evidence for CLAIM-L5 when applicable.

Security-sensitive claims must include:

- negative tests.
- audit obligations when operation produces a security decision or protected state transition.
- failure modes.
- no-fake-success evidence or gate reference.

## 11. Reviewer Approval Requirements

| Claim type | Required reviewers |
| --- | --- |
| design_claim | architecture reviewer. |
| implementation_claim | code reviewer and security reviewer when security-sensitive. |
| test_claim | test reviewer. |
| audit_claim | audit reviewer and security reviewer. |
| supply_chain_claim | supply-chain reviewer. |
| conformance_claim | conformance reviewer and release reviewer. |
| production_claim | release reviewer, security reviewer, and evidence auditor. |
| high_assurance_claim | high-assurance reviewer, security reviewer, and independent TCB reviewer. |
| negative_claim | security reviewer and test reviewer. |

Reviewer approval states:

```text
pending
approved
changes_requested
rejected
superseded
```

Claims must not move to `RELEASED` with pending, rejected, or changes-requested required approvals.

## 12. Release Gate Relationship

Production claims must link to all gates:

- PROD-001 Source Matrix complete for all z/OS-inspired concepts.
- PROD-002 System Integrity negative tests pass.
- PROD-003 Unauthorized dataset access cannot produce handle.
- PROD-004 DENY audit record emitted before caller result.
- PROD-005 Catalog crash recovery passes.
- PROD-006 Spool browse/purge security enforced.
- PROD-007 Operator commands require authority and audit.
- PROD-008 AMF invalid signature/revoked signer fail closed.
- PROD-009 Update rollback/freeze/mix-and-match tests pass.
- PROD-010 SBOM and signed provenance produced.
- PROD-011 No fake success CI clean.
- PROD-012 Parser fuzz campaigns complete.
- PROD-013 PXM device teardown tested before passthrough production.
- PROD-014 Guard evidence exists before HA claim.
- PROD-015 Recovery drill completed.

Rules:

- A production claim must not be `RELEASED` unless every applicable gate is `pass`.
- A gate marked `not_applicable` must include rationale and reviewer approval.
- High-Assurance claims must treat PROD-014 as applicable.

## 13. Profile Claim Rules

Baseline:

- May be supported by design, implementation, positive tests, negative tests, and local evidence.
- Must not claim Guard root protection.

Enterprise:

- Requires Baseline support plus supply-chain, update, remote audit, and measured boot evidence where claimed.
- Requires SBOM and signed provenance for release claims.

High-Assurance:

- Requires Enterprise support plus PXM, Guard, formal or model evidence, attestation, and independent review.
- Must not rely on Guard for job, dataset, spool, or operator business semantics.
- Must not accept open Guard-root gaps as non-blocking.

Optional higher-profile features do not upgrade a claim profile by themselves.

## 14. Unresolved Gap Handling

Gap states:

```text
open
accepted_risk
blocked
resolved
superseded
```

Rules:

- Critical gaps block production claims.
- High gaps block production claims unless accepted by release and security owners.
- High-Assurance Guard-root gaps block High-Assurance claims.
- Accepted risk must have an expiry date.
- Resolved gaps must link to evidence artifacts.
- Claims must list all gaps that block or weaken the claim.

## 15. Release Wording Checks

Every release claim must link to release wording review evidence.

The review must verify:

- No compatibility claim with z/OS or IBM products.
- No statement that MFOS implements RACF, JES, DFSMS, SMP/E, or z/OS APIs.
- No overclaim that PKU/PKS provide z/OS storage-key equivalence.
- No Baseline claim of Guard root protection.
- No production claim without gate evidence.
- No High-Assurance claim without Guard evidence.

## 16. Claim Registry Validation Checklist

- Registry index exists.
- Registry index hash verifies.
- Claim IDs are unique.
- Claim records have non-compatibility statements.
- Claim profiles are explicit.
- Claim levels do not exceed evidence.
- Requirement IDs are present.
- Source matrix IDs are present where needed.
- Evidence artifact IDs exist in the evidence archive.
- Security-sensitive claims have negative tests.
- Parser/input claims have fuzz targets.
- Audit claims have audit evidence.
- Reviewer approvals are complete.
- Production claims map to PROD-001 through PROD-015.
- High-Assurance claims include Guard evidence.
- Unresolved gaps are linked.
- Release wording review is linked.

## 17. AI Prompt

```text
You are the MFOS assurance claim registrar.
Create or review claim registry records for the supplied MFOS claims.

Do not claim z/OS compatibility, z/Architecture compatibility, IBM API
compatibility, RACF compatibility, JES compatibility, DFSMS compatibility,
SMP/E compatibility, or IBM product compatibility.

For each claim, output:
- claim_id
- title
- claim_class
- profile
- claim_level
- status
- statement
- non_compatibility_statement
- in_scope and out_of_scope
- source_matrix_ids
- requirement_ids
- AI contract IDs
- design_refs
- implementation_refs
- positive tests
- negative tests
- fuzz targets
- audit obligations
- invariants
- failure modes
- evidence_artifacts
- production gates
- profile claim status
- reviewer approvals required
- assumptions
- unsupported features
- spec gaps
- residual risks
- release wording review status

Validation rules:
- Do not raise claim level above available evidence.
- Claims using source-grounded concepts need source matrix IDs.
- Security-sensitive claims need negative tests.
- Claims with audit decisions need audit evidence.
- Enterprise release claims need SBOM and signed provenance.
- High-Assurance claims need PXM/Guard/formal/attestation evidence.
- Unresolved Critical or High gaps must block or explicitly mark the claim.
```

## 18. Spec Gaps

- Concrete registry storage path is recommended but not enforced.
- Machine-readable schema validation is not implemented.
- Claim ID allocation authority is not assigned.
- Reviewer independence policy is defined by role but not by organization.
- Signature key hierarchy is not specified.
- Automated traceability graph generation is not specified.
- External auditor export format is not defined.
