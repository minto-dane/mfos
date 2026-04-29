---
spec_id: MFOS-SPEC-40-AUTOMATED-REASONING-PROGRAM
title: MFOS Automated Reasoning Program
canonical_language: en-US
japanese_mirror: missing
status: draft
owner: MFOS architecture
last_reviewed: '2026-04-28'
source_refs:
- EXTREF-AWS-AUTOMATED-REASONING-0001
- EXTREF-DAFNY-REFERENCE-0001
- EXTREF-KANI-RUST-VERIFIER-0001
- EXTREF-VERUS-RUST-VERIFICATION-0001
- EXTREF-GITHUB-CODEQL-0001
- EXTREF-NIST-SECURE-SYSTEMS-ENGINEERING-0001
- EXTREF-NIST-SSDF-0001
- TUF-001
- FBVBS-001
requirement_refs:
- MFOS-REQ-DAFNY-*
- MFOS-REQ-FORMAL-*
- MFOS-REQ-ASSURANCE-*
- MFOS-REQ-PXM-*
- MFOS-REQ-MFVM-*
- MFOS-REQ-CVM-*
- MFOS-REQ-CLUSTER-*
claim_refs:
- MFOS-FC-AUTHORIZATION-NO-HANDLE-WITHOUT-ALLOW
- MFOS-FC-AUDIT-DENY-BEFORE-RETURN
- MFOS-FC-UPDATE-NO-ROLLBACK
- MFOS-FC-PARTITION-MEMORY-OWNERSHIP
- MFOS-FC-PXM-CAPABILITY-REQUIRED-FOR-RESOURCE-OPERATION
- MFOS-FC-MFVM-CANNOT-BYPASS-PXM
- MFOS-FC-CVM-LAUNCH-REQUIRES-MEASUREMENT
- MFOS-FC-CVM-SECRET-RELEASE-REQUIRES-ATTESTATION
- MFOS-FC-PRIVATE-SHARED-MEMORY-TRANSITION-VALIDITY
- MFOS-FC-CLUSTER-POLICY-DISTRIBUTION-INTEGRITY
- MFOS-FC-CLUSTER-ATTESTATION-COLLECTION-INTEGRITY
test_refs: []
evidence_refs:
- EV-MFOS-FORMAL-0101
- EV-MFOS-FORMAL-0102
- EV-MFOS-FORMAL-0103
- EV-MFOS-FORMAL-0104
- EV-MFOS-FORMAL-0105
- EV-MFOS-FORMAL-0106
- EV-MFOS-FORMAL-0107
- EV-MFOS-FORMAL-0108
- EV-MFOS-FORMAL-0109
- EV-MFOS-FORMAL-0110
- EV-MFOS-FORMAL-0111
implementation_allowed: false
downstream_packs:
- PACK-35
spec_gap_policy: implementation_must_not_infer_or_fill_gaps
---

# MFOS Automated Reasoning Program

Status: Draft Phase 0.10 requirements expansion. This document defines a formal-assurance program scaffold only. It does not claim any proof is complete.

## 1. Purpose

Define the registry, review, evidence, and tool-policy structure for MFOS formal claims, models, proof obligations, proof harnesses, model checking, and automated reasoning.

## 2. Scope

In scope: automated reasoning charter, formal claim registry, model registry, proof obligation registry, proof harness registry, Dafny, TLA+, Alloy, Kani, Verus, proof evidence, proof CI, and reasoning domains.

## 3. Non-objectives

Out of scope: completed proofs, production proof claims, proof-driven implementation, or replacing tests and red-team review with formal plans.

## 4. Automated Reasoning Charter

Automated reasoning is used to reduce ambiguity in high-risk semantics. It is evidence only when tied to a requirement, model, assumptions, result, and review status.

## 5. Formal Claim Registry

The formal claim registry records claim IDs, requirement refs, protected assets, assumptions, not-claimed boundaries, proof obligations, model refs, tests, and evidence refs.

The machine-readable claim registry is `formal/claim-registry.yml`. Its initial planned claim IDs are:

| Claim ID | Scope | Status |
| --- | --- | --- |
| `MFOS-FC-AUTHORIZATION-NO-HANDLE-WITHOUT-ALLOW` | authorization handle issuance requires allow | planned |
| `MFOS-FC-AUDIT-DENY-BEFORE-RETURN` | deny-path audit ordering | planned |
| `MFOS-FC-UPDATE-NO-ROLLBACK` | update freshness and rollback prevention | planned |
| `MFOS-FC-PARTITION-MEMORY-OWNERSHIP` | PXM partition memory ownership | planned |
| `MFOS-FC-PXM-CAPABILITY-REQUIRED-FOR-RESOURCE-OPERATION` | PXM capability-gated resource operations | planned |
| `MFOS-FC-MFVM-CANNOT-BYPASS-PXM` | MFVM effects mediated by PXM | planned |
| `MFOS-FC-CVM-LAUNCH-REQUIRES-MEASUREMENT` | CVM launch measurement requirement | planned |
| `MFOS-FC-CVM-SECRET-RELEASE-REQUIRES-ATTESTATION` | CVM secret release requires attestation | planned |
| `MFOS-FC-PRIVATE-SHARED-MEMORY-TRANSITION-VALIDITY` | CVM private/shared transition validity | planned |
| `MFOS-FC-CLUSTER-POLICY-DISTRIBUTION-INTEGRITY` | cluster policy distribution integrity | planned |
| `MFOS-FC-CLUSTER-ATTESTATION-COLLECTION-INTEGRITY` | cluster attestation collection integrity | planned |

These entries are planned claims only. They do not assert completed proof, production correctness, hardware enforcement, or external compatibility.

## 6. Formal Model Registry

The model registry records model path, tool family, modeled state, excluded behavior, assumptions, and review status.

The machine-readable model registry is `formal/model-registry.yml`. Planned model paths may point to future model locations; such paths are not evidence until model content, tool output, and review status are recorded.

## 7. Proof Obligation Registry

Proof obligations define the statement to prove or model-check, acceptance criteria, owner, phase, expected evidence, and blocking status.

The machine-readable proof obligation registry is `formal/proof-obligations.yml`. Its initial planned proof obligation IDs are:

| Proof Obligation ID | Linked Claim | Status |
| --- | --- | --- |
| `MFOS-PO-AUTHORIZATION-NO-HANDLE-WITHOUT-ALLOW` | `MFOS-FC-AUTHORIZATION-NO-HANDLE-WITHOUT-ALLOW` | planned |
| `MFOS-PO-AUDIT-DENY-BEFORE-RETURN` | `MFOS-FC-AUDIT-DENY-BEFORE-RETURN` | planned |
| `MFOS-PO-UPDATE-NO-ROLLBACK` | `MFOS-FC-UPDATE-NO-ROLLBACK` | planned |
| `MFOS-PO-PARTITION-MEMORY-OWNERSHIP` | `MFOS-FC-PARTITION-MEMORY-OWNERSHIP` | planned |
| `MFOS-PO-PXM-CAPABILITY-REQUIRED-FOR-RESOURCE-OPERATION` | `MFOS-FC-PXM-CAPABILITY-REQUIRED-FOR-RESOURCE-OPERATION` | planned |
| `MFOS-PO-MFVM-CANNOT-BYPASS-PXM` | `MFOS-FC-MFVM-CANNOT-BYPASS-PXM` | planned |
| `MFOS-PO-CVM-LAUNCH-REQUIRES-MEASUREMENT` | `MFOS-FC-CVM-LAUNCH-REQUIRES-MEASUREMENT` | planned |
| `MFOS-PO-CVM-SECRET-RELEASE-REQUIRES-ATTESTATION` | `MFOS-FC-CVM-SECRET-RELEASE-REQUIRES-ATTESTATION` | planned |
| `MFOS-PO-PRIVATE-SHARED-MEMORY-TRANSITION-VALIDITY` | `MFOS-FC-PRIVATE-SHARED-MEMORY-TRANSITION-VALIDITY` | planned |
| `MFOS-PO-CLUSTER-POLICY-DISTRIBUTION-INTEGRITY` | `MFOS-FC-CLUSTER-POLICY-DISTRIBUTION-INTEGRITY` | planned |
| `MFOS-PO-CLUSTER-ATTESTATION-COLLECTION-INTEGRITY` | `MFOS-FC-CLUSTER-ATTESTATION-COLLECTION-INTEGRITY` | planned |

Proof obligations with `proof_artifact: null` and `proof_claimed: false` are planning records only.

## 8. Proof Harness Registry

Proof harness entries bind implementation-independent harness plans to requirements. Harness plans do not authorize production implementation.

## 9. Model Checking Policy

Model checking must record assumptions, finite bounds where applicable, liveness/safety properties, and counterexample handling.

## 10. TLA+ Policy

TLA+ is preferred for state-machine invariants and transition safety where applicable.

## 11. Alloy Policy

Alloy is preferred for relational reachability and ownership constraints where applicable.

## 12. Kani Policy

Kani is a candidate for bounded Rust proof harnesses after implementation contracts exist.

## 13. Verus Policy

Verus is a candidate for selected verified Rust components after requirements and proof obligations mature.

## 13.1 Dafny Policy

Dafny is the canonical executable-semantics artifact language for Phase 1. Its Phase 1 role is non-production executable semantic modeling, proof-oriented specification, deterministic conformance checks, and traceability review. Dafny does not authorize semantic-runner command implementation, hosted daemon implementation, Rust semantic-core implementation, generated production code, or production service behavior.

Dafny output is not accepted proof evidence unless it is linked to reviewed source, requirement refs, assumptions, tool version, result status, and human review. The presence of a Dafny scaffold or planned Dafny artifact must not be described as proving MFOS behavior.

## 13.2 Tool Registry

The machine-readable tool registry is `formal/tool-registry.yml`. Tools are listed as planned validation aids only; tool presence is not evidence without versioned output, assumptions, and human review.

## 14. Coq/Lean/Isabelle Placeholder

These tools are future options only and no proof coverage is claimed.

## 15. Access Control Reasoning

Access control reasoning must prove or model-check that protected handles require valid SecurityDecision results.

## 16. Network Reachability Reasoning

Network reachability reasoning is planned for cluster and VM network segmentation only after network object models mature.

## 17. Audit Chain Reasoning

Audit reasoning covers deny-before-return, append order assumptions, hash-chain continuity, and tamper detection boundaries.

## 18. Update Rollback Reasoning

Update reasoning covers rollback, freeze, mix-and-match, activation profile binding, and recovery evidence.

## 19. Partition Memory Ownership Reasoning

Partition memory ownership reasoning covers PXM allocation, reuse, zeroing, second-stage translation, and ownership transfer.

## 20. PXM Capability Reasoning

PXM capability reasoning covers mandatory capabilities for resource operations and rejects overbroad MFVM requests.

## 21. MFVM Cannot Bypass PXM Reasoning

MFVM cannot bypass PXM reasoning is a required formal claim before any MFVM semantic evaluator or implementation.

## 22. Confidential VM Launch Reasoning

Confidential VM reasoning covers launch measurement, attestation, secret release, private/shared transition, and recovery constraints.

## 23. Cluster Policy Distribution Reasoning

Cluster reasoning covers policy versioning, distribution integrity, stale policy rejection, and audit obligations.

## 24. Proof CI

Proof CI is planned but not required to pass until proof artifacts exist. CI must not turn planned proofs into claimed evidence.

## 25. Proof Evidence

Proof evidence must include tool version, model/harness path, assumptions, results, counterexample status, reviewer, and linked requirements.

The machine-readable proof evidence registry is `formal/evidence-registry.yml`. Initial evidence entries are planned placeholders only and have no artifact path.

## 26. Proof Failure Triage

Failed proof or model check results block the claim unless the claim is downgraded or the requirement is marked blocked_by_source_gap/spec_gap.

## 27. Human Review

Human review remains required for proof scope, assumptions, excluded behavior, and claim wording.

## 28. Evidence Requirements

Evidence includes formal/registry.yml, source refs, linked specs, requirement refs, tests, model output, CI output, and red-team review.

## 29. Spec Gaps

- GAP-MFOS-FORMAL-002: proof CI is not active for new Phase 0.10 claims.
- GAP-MFOS-FORMAL-003: no PXM/MFVM/CVM proof artifact exists.
