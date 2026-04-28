---
spec_id: "MFOS-SPEC-19-ASSURANCE-CASE"
title: "MFOS Design Specification 19: Assurance Case"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001", "EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001", "MS-VBS-001", "MS-VSM-001", "NIST-160-001", "NIST-193-001", "NIST-218-001", "SEL4-001", "SLSA-001", "TCG-001", "TUF-001", "X64-AMD-001", "X64-INTEL-001"]
requirement_refs: ["MFOS-REQ-ASSUR-*", "MFOS-REQ-AUDIT-*", "MFOS-REQ-DATASET-*", "MFOS-REQ-GUARD-*", "MFOS-REQ-OBJ-*", "MFOS-REQ-AUTH-*", "MFOS-REQ-SYSINT-*"]
claim_refs: ["MFOS-CLAIM-BASELINE-AUDIT-DENY-BEFORE-RESULT-*", "MFOS-CLAIM-BASELINE-AUDIT-HASH-CHAIN-*", "MFOS-CLAIM-BASELINE-AUTH-PDP-*", "MFOS-CLAIM-BASELINE-SYSINT-DATASET-*", "MFOS-CLAIM-HA-GUARD-AUDIT-ROOT-*", "MFOS-CLAIM-HA-GUARD-ROOT-TRANSITION-*"]
test_refs: []
evidence_refs: ["EV-MFOS-AUDIT-DENY-BEFORE-RESULT-*", "EV-MFOS-AUDIT-HASH-CHAIN-*", "EV-MFOS-DATASET-DENY-NO-HANDLE-*", "EV-MFOS-GUARD-ATTESTATION-*", "EV-MFOS-GUARD-AUDIT-ROOT-SEAL-*"]
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Design Specification 19: Assurance Case

Status: Draft v0.1

Audience: architecture agents, implementation agents, security reviewers, test engineers, release reviewers, evidence auditors

MFOS is a source-grounded, z/OS-inspired enterprise operating system design. This specification defines how MFOS claims are argued, traced, reviewed, tested, and evidenced. It does not claim z/OS compatibility, z/Architecture compatibility, IBM API compatibility, or IBM product compatibility.

## 1. Purpose

The assurance case exists to prevent MFOS from becoming a set of informal security claims. Every meaningful claim must be connected to requirements, source matrix references, design specifications, implementation artifacts, tests, negative tests, review records, and release evidence.

The assurance case is the structured answer to:

- What does MFOS claim?
- Which profile does the claim apply to?
- What is the threat boundary?
- Which requirements define the claim?
- Which evidence supports the claim?
- Which assumptions remain outside the claim?
- Which gaps block stronger claims?

## 2. Scope

In scope:

- Claim model.
- Assurance profiles.
- Evidence artifact taxonomy.
- Traceability rules.
- Production readiness gate.
- High-Assurance Guard evidence rules.
- AI implementation contract references.
- Review checklists.
- Negative test expectations.
- Residual risk handling.

Out of scope:

- Claiming compatibility with z/OS or IBM products.
- Certifying against a third-party standard.
- Proving all MFOS code correct.
- Treating documentation as evidence without executable or review artifacts.
- Treating positive tests as sufficient security evidence.

## 3. Source Matrix References

| Source ID | Use |
| --- | --- |
| EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001 | System integrity claim framing and unauthorized-boundary inspiration. |
| EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001 | Authorized-boundary negative test discipline. |
| EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | Audit and accounting evidence inspiration. |
| X64-INTEL-001 | x64 protection claim grounding. |
| X64-AMD-001 | AMD64 protection claim grounding. |
| MS-VBS-001 | High-Assurance executable mapping and code-integrity reference only. |
| MS-VSM-001 | High-Assurance Guard isolation reference only. |
| TCG-001 | Measured boot and TPM evidence reference. |
| NIST-160-001 | Secure system engineering lifecycle reference. |
| NIST-218-001 | Secure development practice reference. |
| NIST-193-001 | Firmware resiliency and recovery reference. |
| SEL4-001 | Formal-assurance boundary discipline reference. |
| SLSA-001 | Build provenance and supply-chain evidence reference. |
| TUF-001 | Update metadata and rollback/freeze/mix-and-match evidence reference. |
| FBVBS-001 | Internal transfer source for traceability, evidence, state-machine, and production proof discipline. |

## 4. Claim Model

### 4.1 Claim Levels

| Level | Meaning | Evidence required |
| --- | --- | --- |
| CLAIM-L0 | Design intent only. | Design section and assumptions. |
| CLAIM-L1 | Requirements defined. | Requirement IDs, source IDs, state machines, failure modes. |
| CLAIM-L2 | Tested behavior. | Positive tests, negative tests, fuzz targets where applicable. |
| CLAIM-L3 | Reviewed implementation. | Code review, architecture review, unsafe review, traceability audit. |
| CLAIM-L4 | Release evidence. | CI results, SBOM, signed provenance, reproducible build report, audit evidence. |
| CLAIM-L5 | High-Assurance evidence. | Formal model or proof artifact, Guard evidence, attestation, independent review. |

MFOS production readiness requires the relevant claims to reach the level named in the conformance profile and production gate. A claim cannot be raised by wording alone.

### 4.2 Profile Claims

Baseline claim:

```text
MFOS Baseline claims source-grounded enterprise semantics:
central authorization, mandatory audit obligations, object handles,
dataset/catalog/job/spool/operator models, signed AMF artifacts, typed
SVC/PCALL boundaries, fail-closed unsupported behavior, and no fake success.
```

Enterprise claim:

```text
MFOS Enterprise adds production-oriented evidence:
measured boot, TPM-bound selected secrets, TUF-like updates, remote audit
export, SBOM, signed provenance, dependency allowlist, update rollback and
freeze tests, and stronger device-assignment prerequisites.
```

High-Assurance claim:

```text
MFOS High-Assurance adds PXM Guard evidence for selected root objects:
security policy root, audit chain root, AMF registry, SVC table integrity,
executable mapping policy, activation profile root, update root, and
emergency state. Guard scope remains small and must not interpret job,
dataset, spool, or operator business semantics.
```

### 4.3 Claim Tree Structure

Assurance arguments MUST be represented as claim trees when a claim is used for
implementation approval, conformance review, or production readiness. A claim
tree makes assumptions, subclaims, evidence, and explicit non-claims visible.

```yaml
AssuranceClaimTree:
  claim_id: string
  claim: string
  profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  claim_level: CLAIM-L0 | CLAIM-L1 | CLAIM-L2 | CLAIM-L3 | CLAIM-L4 | CLAIM-L5
  source_matrix_ids: [string]
  supported_by:
    requirements: [string]
    subclaims: [string]
    design_refs:
      - path: string
        section: string
    tests:
      positive: [string]
      negative: [string]
      fuzz: [string]
      fault_injection: [string]
    evidence: [string]
    review_records: [string]
  assumptions: [string]
  audit_obligations: [string]
  failure_modes: [string]
  invariants: [string]
  not_claimed: [string]
  residual_risks: [string]
  blocking_gaps: [string]
  status: DRAFT | BLOCKED | REVIEWED | EVIDENCED | RETIRED
```

Rules:

- A parent claim MUST NOT be stronger than its weakest required subclaim.
- `not_claimed` entries are mandatory when a reader could reasonably infer a broader claim.
- High-Assurance claim trees MUST include Guard evidence for each protected root named by the claim.
- A claim tree MUST include negative test evidence for protected-resource behavior.
- Audit-related claims MUST include audit record samples or audit-ordering evidence.
- Compatibility with z/OS, z/Architecture, IBM APIs, or IBM products MUST NOT appear as a claim or subclaim.

### 4.4 Claim Tree Examples

Baseline dataset-access claim:

```yaml
claim_id: MFOS-CLAIM-BASELINE-SYSINT-DATASET-0001
claim: >
  Unauthorized subjects cannot obtain a protected dataset handle through
  defined MFOS system interfaces.
profile: Baseline
claim_level: CLAIM-L2
source_matrix_ids:
  - EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
  - EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001
  - EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001
  - EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001
supported_by:
  requirements:
    - MFOS-REQ-SYSINT-0001
    - MFOS-REQ-AUTH-0004
    - MFOS-REQ-DATASET-0002
    - MFOS-REQ-AUDIT-0002
    - MFOS-REQ-OBJ-0014
    - MFOS-REQ-OBJ-0015
  subclaims:
    - MFOS-CLAIM-BASELINE-AUTH-PDP-001
    - MFOS-CLAIM-BASELINE-AUDIT-DENY-BEFORE-RESULT-001
  design_refs:
    - path: docs/design/specs/05-object-model.md
      section: SecurityDecision, PolicyBinding, ObjectGenerationBinding
    - path: docs/design/specs/08-dataset-catalog.md
      section: Dataset open lifecycle
  tests:
    positive:
      - OBJ-POS-010
    negative:
      - OBJ-NEG-013
      - OBJ-NEG-014
      - THR-NEG-001
    fuzz:
      - OBJ-FUZZ-011
    fault_injection:
      - THR-FI-001
  evidence:
    - EV-MFOS-DATASET-DENY-NO-HANDLE-0001
    - EV-MFOS-AUDIT-DENY-BEFORE-RESULT-0001
  review_records:
    - REV-SEC-DATASET-HANDLE-001
assumptions:
  - Nucleus supplies trusted caller context to SVC and PCALL.
  - securityd policy store uses committed policy state.
  - auditd is available or the profile fail-closed policy applies.
audit_obligations:
  - DATASET_OPEN_DENY before caller-visible denial
failure_modes:
  - MFOS_ERR_POLICY_DENIED
  - MFOS_ERR_STALE_HANDLE
  - MFOS_ERR_POLICY_VERSION_MISMATCH
  - MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE
invariants:
  - INV-OBJ-001
  - INV-OBJ-011
  - INV-OBJ-012
not_claimed:
  - Protection after arbitrary nucleus compromise.
  - Protection after malicious authorized module compromise.
  - Compatibility with z/OS dataset access behavior.
residual_risks:
  - Overbroad policy can authorize harmful access unless policy lint and review catch it.
blocking_gaps:
  - Concrete SecurityDecision signature or MAC format is not fixed.
status: DRAFT
```

High-Assurance Guard root claim:

```yaml
claim_id: MFOS-CLAIM-HA-GUARD-AUDIT-ROOT-0001
claim: >
  In the High-Assurance profile, the audit chain root cannot be transitioned
  without Guard verification and audit evidence.
profile: High-Assurance
claim_level: CLAIM-L5
source_matrix_ids:
  - EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001
  - MS-VSM-001
  - FBVBS-001
supported_by:
  requirements:
    - MFOS-REQ-AUDIT-0007
    - MFOS-REQ-GUARD-0004
    - MFOS-REQ-ASSUR-0007
  subclaims:
    - MFOS-CLAIM-BASELINE-AUDIT-HASH-CHAIN-001
    - MFOS-CLAIM-HA-GUARD-ROOT-TRANSITION-0001
  tests:
    positive:
      - THR-POS-008
    negative:
      - THR-NEG-014
      - THR-NEG-016
    fuzz:
      - THR-FUZZ-013
    fault_injection:
      - THR-FI-008
  evidence:
    - EV-MFOS-GUARD-AUDIT-ROOT-SEAL-0001
    - EV-MFOS-GUARD-ATTESTATION-0001
    - EV-MFOS-AUDIT-HASH-CHAIN-0001
assumptions:
  - Guard TCB and isolation assumptions hold for the claimed platform profile.
  - Attestation nonce freshness is enforced.
not_claimed:
  - Guard interprets ordinary dataset, job, spool, or business policy semantics.
  - High-Assurance claim applies when Guard is unavailable.
blocking_gaps:
  - Exact Guard attestation claim format belongs in Guard specs.
status: DRAFT
```

## 5. Non-Compatibility Claim Rule

All assurance artifacts must use this rule:

```text
MFOS may describe itself as z/OS-inspired and source-grounded.
MFOS must not claim z/OS compatibility, z/Architecture compatibility,
IBM API compatibility, RACF compatibility, JES compatibility, DFSMS
compatibility, SMP/E compatibility, or IBM product compatibility.
```

Any release note, README, test report, or AI output that implies compatibility must be corrected before it can support an assurance claim.

## 6. Traceability Model

Every security-sensitive claim must link:

```text
Source Matrix ID
  -> Requirement ID
  -> Design spec section
  -> Implementation artifact
  -> Positive test
  -> Negative test
  -> Fuzz target when parser/input boundary exists
  -> Audit obligation
  -> Review record
  -> Evidence artifact
```

Traceability statuses:

| Status | Meaning |
| --- | --- |
| UNTRACED | Missing source, requirement, test, or evidence link. |
| PARTIAL | Some links exist but at least one required artifact is missing. |
| TESTED | Required positive and negative tests exist and pass. |
| REVIEWED | Tests pass and review record exists. |
| EVIDENCED | Release evidence exists and is archived. |
| BLOCKED | A spec gap or unresolved risk prevents the claim. |

## 7. Evidence Artifact Taxonomy

### 7.1 Design Evidence

- Source matrix entry.
- Concept mapping note with overlap and divergence.
- Requirement table.
- State machine.
- ABI or manifest schema.
- Threat model section.
- Failure-mode table.
- Formal invariant list.
- Spec gap list.

### 7.2 Test Evidence

- Unit test report.
- Integration test report.
- Negative test report.
- Fuzz corpus and crash report.
- Fault-injection report.
- Crash-recovery report.
- Conformance test report.
- No-fake-success scanner report.

### 7.3 Review Evidence

- Architecture review record.
- Security review record.
- Code review record.
- Unsafe code inventory and safety contract review.
- TCB change review.
- Source-grounding review.
- Release claim review.

### 7.4 Runtime Evidence

- Audit hash-chain report.
- DENY-before-result audit proof.
- Operator command audit records.
- AMF load audit records.
- Update activation audit records.
- Recovery drill audit records.
- Guard root transition records for High-Assurance.

### 7.5 Supply-Chain Evidence

- Pinned toolchain record.
- Dependency allowlist.
- SBOM.
- Signed provenance.
- Reproducible build diff report.
- Artifact signature report.
- Update metadata verification report.

### 7.6 High-Assurance Evidence

- PXM partition lifecycle conformance report.
- Device teardown negative test report.
- Guard seal evidence.
- Guard SVC table verification evidence.
- Guard executable mapping evidence.
- Guard AMF registry approval evidence.
- Attestation report.
- Formal model or proof artifact.

## 8. Assurance Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-ASSUR-0001 | Every assurance claim must name its applicable profile. | claim review |
| MFOS-REQ-ASSUR-0002 | Every security-sensitive claim must trace to requirement IDs and source matrix IDs. | traceability audit |
| MFOS-REQ-ASSUR-0003 | Every security-sensitive claim must include negative test evidence. | evidence review |
| MFOS-REQ-ASSUR-0004 | Parser and external-input claims must include fuzz target evidence. | fuzz review |
| MFOS-REQ-ASSUR-0005 | Audit-related claims must include audit obligation and audit record evidence. | audit review |
| MFOS-REQ-ASSUR-0006 | Production claims must pass all production readiness gates. | release review |
| MFOS-REQ-ASSUR-0007 | High-Assurance claims must include PXM Guard evidence for each protected root. | Guard evidence review |
| MFOS-REQ-ASSUR-0008 | Unsupported behavior must fail closed and must not be presented as complete. | no-fake-success CI |
| MFOS-REQ-ASSUR-0009 | SPEC_GAP behavior must not be implemented as a success path. | spec gap review |
| MFOS-REQ-ASSUR-0010 | Compatibility wording must be reviewed before release. | release wording review |
| MFOS-REQ-ASSUR-0011 | TCB changes must receive independent review before assurance level increases. | TCB review |
| MFOS-REQ-ASSUR-0012 | Supply-chain claims must include SBOM and signed provenance. | supply-chain audit |
| MFOS-REQ-ASSUR-0013 | Security-sensitive claims used for implementation approval, conformance review, or production readiness must be represented as claim trees. | claim-tree review |

## 9. Production Readiness Gate

MFOS may not claim production readiness until every gate is marked PASS with evidence.

| Gate | Requirement | Minimum evidence |
| --- | --- | --- |
| PROD-001 | Source Matrix complete for all z/OS-inspired concepts. | source matrix lint report and concept mapping review. |
| PROD-002 | System Integrity negative tests pass. | negative test report for system interfaces. |
| PROD-003 | Unauthorized dataset access cannot produce handle. | dataset open negative test and handle inventory report. |
| PROD-004 | DENY audit record emitted before caller result. | audit ordering test and audit hash-chain record. |
| PROD-005 | Catalog crash recovery passes. | crash-recovery test report. |
| PROD-006 | Spool browse/purge security enforced. | spool negative test report. |
| PROD-007 | Operator commands require authority and audit. | operator parser/auth/audit test report. |
| PROD-008 | AMF invalid signature/revoked signer fail closed. | AMF revocation negative test report. |
| PROD-009 | Update rollback/freeze/mix-and-match tests pass. | UVS update attack test report. |
| PROD-010 | SBOM and signed provenance produced. | SBOM and provenance artifacts. |
| PROD-011 | No fake success CI clean. | CI scanner report. |
| PROD-012 | Parser fuzz campaigns complete. | fuzz target list, corpus summary, crash status. |
| PROD-013 | PXM device teardown tested before passthrough production. | device teardown negative test report. |
| PROD-014 | Guard evidence exists before HA claim. | Guard root seal, verify, and attestation evidence. |
| PROD-015 | Recovery drill completed. | recovery drill report and audit records. |

## 10. Mandatory Negative Test Expectations

Each implementation change in a security-sensitive path must include at least one negative test unless the task is purely documentation.

Required categories:

- Unauthorized access.
- Stale handle.
- Policy version mismatch.
- Audit write failure.
- Malformed input.
- Replay attempt.
- Downgrade attempt.
- Concurrent update.
- Crash mid-transaction.
- Recovery consistency.
- Privilege confusion.
- Cross-partition misuse.
- AMF revoked signer.
- Guard root mismatch.
- Unsupported command success attempt.

Negative tests must assert denial, typed failure, audit behavior, and absence of leaked handles or state transitions.

## 11. AI Implementation Contract Reference

All assurance evidence must check the AI contract:

- AI-MFOS-001: spec IDs required.
- AI-MFOS-002: source matrix IDs required for z/OS-derived concepts.
- AI-MFOS-003: no compatibility claim.
- AI-MFOS-005: no fake success, empty stub, or silent fallback.
- AI-MFOS-006: unsupported specified features fail closed.
- AI-MFOS-007: spec gaps do not become behavior.
- AI-MFOS-008: security-sensitive paths require negative tests.
- AI-MFOS-009: audit obligations are mandatory.
- AI-MFOS-010: securityd is not bypassed.
- AI-MFOS-011: unsafe code requires safety contract.
- AI-MFOS-012: parsers require fuzz targets.
- AI-MFOS-013: PXM does not interpret enterprise semantics.
- AI-MFOS-014: Guard does not interpret job, dataset, or spool semantics.
- AI-MFOS-015: PKU/PKS are not primary integrity boundaries.

Required AI output format is defined in [ai-prompts.md](../prompts/ai-prompts.md) and the template in [assurance-case-template.md](../assurance/assurance-case-template.md).

## 12. Review Checklists

### 12.1 Assurance Claim Review

- Claim has a unique claim ID.
- Claim has a profile.
- Claim does not imply compatibility.
- Claim has source matrix IDs.
- Claim has requirement IDs.
- Claim has explicit assumptions.
- Claim has explicit non-objectives.
- Claim has positive and negative tests.
- Claim has audit obligations.
- Claim has failure modes.
- Claim has evidence artifacts.
- Claim has residual risks.
- Claim has owner and review date.

### 12.2 Security Review

- securityd is final PDP for protected resources.
- auditd records DENY before caller-visible result.
- no fake success path exists.
- unsupported and SPEC_GAP are separated.
- user-controlled input is bounded and validated.
- stale handle paths are denied.
- policy version mismatch is denied.
- AMF and update revocation paths fail closed.
- PXM/Guard scope is not inflated.
- PKU/PKS are not overclaimed.

### 12.3 Release Review

- Production gates are PASS or explicitly out of scope for non-production release.
- Evidence artifacts are archived.
- SBOM and provenance exist when Enterprise or higher is claimed.
- Compatibility wording check is clean.
- No unresolved Critical or High risks block the claim.
- Spec gaps are listed and not hidden in release notes.

## 13. Claim Record Schema

```yaml
AssuranceClaim:
  claim_id: string
  title: string
  profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  claim_level: CLAIM-L0 | CLAIM-L1 | CLAIM-L2 | CLAIM-L3 | CLAIM-L4 | CLAIM-L5
  statement: string
  non_compatibility_statement: string
  source_matrix_ids:
    - string
  requirement_ids:
    - string
  design_refs:
    - path: string
      section: string
  implementation_refs:
    - path: string
      symbol: string?
  evidence_artifacts:
    - artifact_id: string
      artifact_type: string
      path: string
  positive_tests:
    - string
  negative_tests:
    - string
  fuzz_targets:
    - string
  audit_obligations:
    - string
  invariants:
    - string
  assumptions:
    - string
  supported_by:
    requirements:
      - string
    subclaims:
      - string
    tests:
      positive:
        - string
      negative:
        - string
      fuzz:
        - string
      fault_injection:
        - string
  residual_risks:
    - string
  not_claimed:
    - string
  blocking_gaps:
    - string
  spec_gaps:
    - string
  review_records:
    - string
  status: DRAFT | BLOCKED | REVIEWED | EVIDENCED | RETIRED
```

## 14. Spec Gaps

- Concrete evidence artifact storage path is not fixed.
- Claim ID registry is not yet implemented.
- Automated traceability graph format is not fixed.
- Machine-readable claim-tree registry is not yet implemented.
- Formal proof acceptance criteria are not yet defined for every core state machine.
- Independent reviewer policy is not yet specified.
- Evidence retention period is not yet specified.
- Mapping to external certification frameworks is intentionally out of scope.
