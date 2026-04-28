---
spec_id: "MFOS-SPEC-21-AI-IMPLEMENTATION-CONTRACT"
title: "MFOS AI Implementation Contract v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001", "MS-VBS-001", "MS-VSM-001", "NIST-160-001", "NIST-218-001", "SLSA-001", "TUF-001", "X64-AMD-001", "X64-INTEL-001", "X64-LINUX-PKU-001"]
requirement_refs: ["MFOS-REQ-AI-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS AI Implementation Contract v0.1

Status: Draft  
Owner: MFOS architecture  
Profile applicability: Baseline, Enterprise-Standalone, Enterprise-PXM, High-Assurance  
Source basis: user-provided MFOS Source-Grounded High-Assurance Architecture v0.3

## 1. Purpose

This document defines the mandatory contract for AI agents that design, implement, review, test, or summarize MFOS work.

MFOS is an x64-native, source-grounded, z/OS-inspired enterprise operating system design. AI agents must preserve that framing. They must not invent enterprise OS semantics, imply z/OS compatibility, bypass the source matrix, skip audit obligations, or return fake success.

The contract exists to make every AI-produced change reviewable by requirement ID, source ID, invariant, negative test, and evidence artifact.

## 2. Scope

This specification applies to:

- architecture changes
- requirements changes
- service implementation
- nucleus implementation
- PXM and Guard implementation
- parser implementation
- update and release tooling
- test generation
- fuzz target generation
- CI/lint rules
- code review
- release notes and conformance claims
- status summaries produced by AI agents

## 3. Non-Objectives

This contract does not:

- grant permission to claim z/OS compatibility
- replace MFOS specifications
- replace human review for TCB changes
- allow AI agents to invent behavior for spec gaps
- allow implementation before required source and requirement IDs exist
- allow production claims before the production readiness gate passes
- define final CI runner implementation
- define final machine-readable traceability schema

## 4. Source Matrix References

Required source IDs for this contract:

- EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001: system integrity claim discipline.
- EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001: authorized-boundary negative-test discipline.
- EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001: AMF/APF-inspired authorized module boundary.
- EXTREF-IBM-ZOS-SECURITY-SERVER-0001: security manager inspiration for securityd policy centrality.
- EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001: audit evidence inspiration for auditd obligations.
- X64-INTEL-001: x64 mechanism reality.
- X64-AMD-001: AMD64 mechanism reality.
- X64-LINUX-PKU-001: PKU limitation reference.
- MS-VBS-001: High-Assurance Guard comparison only.
- MS-VSM-001: High-Assurance Guard comparison only.
- NIST-160-001: secure systems engineering.
- NIST-218-001: secure development practice.
- SLSA-001: provenance and build integrity.
- TUF-001: signed metadata and anti-rollback update discipline.
- FBVBS-001: traceability, evidence, state-machine, production proof, and no-fake-success discipline.

## 5. Contract Principles

AI-MFOS-P-001:

Specification comes before implementation.

AI-MFOS-P-002:

Source-grounded concepts require Source Matrix IDs.

AI-MFOS-P-003:

MFOS is z/OS-inspired, not z/OS compatible.

AI-MFOS-P-004:

securityd is the final policy decision point for protected resource authorization.

AI-MFOS-P-005:

auditd is the evidence service. Debug logs, console output, and spool output are not substitutes for audit evidence.

AI-MFOS-P-006:

Unsupported specified behavior fails closed as `MFOS_ERR_UNSUPPORTED`.

AI-MFOS-P-007:

Unspecified behavior fails closed as `MFOS_ERR_SPEC_GAP` or is blocked before implementation.

AI-MFOS-P-008:

Positive tests prove the intended path. Negative tests prove the security boundary.

AI-MFOS-P-009:

Hardware mechanisms help enforcement but do not replace MFOS authorization, audit, or Guard roots.

AI-MFOS-P-010:

PXM and Guard must stay small and must not absorb MFOS enterprise semantics.

## 6. Mandatory AI Output Format

Every AI implementation, review, or test-generation response that changes MFOS artifacts must include these sections, in this order:

```text
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
```

Section rules:

| Section | Required content |
| --- | --- |
| Implemented Requirement IDs | Stable requirement IDs or explicit statement that the change is documentation-only and why no implementation IDs apply. |
| Source Matrix IDs | Source IDs for IBM-derived, x64-derived, update, supply-chain, Guard, or assurance concepts. |
| Assumptions | Explicit assumptions that affect behavior, tests, deployment, or assurance claims. |
| Spec Gaps | `SPEC_GAP-*` items encountered or created. No invented behavior is allowed. |
| Unsupported Features | Specified features intentionally not implemented, with `MFOS_ERR_UNSUPPORTED` behavior where applicable. |
| Security Invariants | Invariants preserved or added. |
| Audit Obligations | Required audit records, deny-before-result rules, correlation IDs, and audit failure behavior. |
| Failure Modes | Typed errors, fail-closed behavior, recovery behavior, and degraded-mode rules. |
| Tests Added | Positive, integration, conformance, state-machine, crash, or recovery tests. |
| Negative Tests Added | Unauthorized, malformed, stale, rollback, replay, downgrade, privilege-confusion, or boundary-bypass tests. |
| Fuzz Targets Added | Parser, ABI, manifest, command, DSN, JCL-like, policy, update, PXM, or Guard fuzz targets. |
| Unsafe Code Justification | Safety contract for every unsafe block, or `None`. |
| Review Checklist | Human review points, TCB impact, source/requirement traceability, and release claim impact. |
| Evidence Artifacts | Test reports, fuzz reports, audit record IDs, provenance, SBOM, attestation, formal model outputs, or review records. |

The mandatory output format is itself a release and review artifact. Omitting sections is a contract failure.

## 7. AI Rules

AI-MFOS-001:

Do not write implementation code without applicable spec IDs.

AI-MFOS-002:

Do not use z/OS-derived concepts without Source Matrix IDs.

AI-MFOS-003:

Do not write or imply "z/OS compatible."

AI-MFOS-004:

When IBM terminology is mapped to MFOS terminology, state semantic overlap and MFOS divergence.

AI-MFOS-005:

Do not use fake success, empty stubs, or silent fallback.

AI-MFOS-006:

Unimplemented specified features must return `UNSUPPORTED` and fail closed.

AI-MFOS-007:

Undefined features must return `SPEC_GAP` or be blocked before implementation.

AI-MFOS-008:

Security-sensitive paths require negative tests in the same change.

AI-MFOS-009:

Do not omit audit obligations.

AI-MFOS-010:

Do not bypass securityd for protected-resource authorization decisions.

AI-MFOS-011:

Unsafe code requires a safety contract before it is accepted.

AI-MFOS-012:

Parsers require fuzz targets.

AI-MFOS-013:

PXM must not interpret MFOS enterprise semantics.

AI-MFOS-014:

Guard must not interpret job, dataset, catalog, spool, or ordinary business policy semantics.

AI-MFOS-015:

PKU and PKS must not be the primary system-integrity boundary.

AI-MFOS-016:

Do not treat transport security, checksums, debug logs, or console output as security evidence.

AI-MFOS-017:

Do not broaden a conformance or production claim without evidence artifacts.

AI-MFOS-018:

Do not edit unrelated files or revert work owned by another agent.

AI-MFOS-019:

Do not weaken profile requirements to make an implementation pass.

AI-MFOS-020:

Do not introduce new protected resources or system interfaces without glossary, requirement, authorization, audit, and negative-test updates.

## 8. Prohibited Patterns

The following patterns are prohibited in production paths:

- `todo!()` as reachable behavior
- `unimplemented!()` as reachable behavior
- placeholder success
- returning `OK` after skipping validation
- silent fallback to allow
- silent fallback to weaker policy
- caller-supplied identity overriding trusted context
- caller-supplied effective principal accepted without delegation spec
- direct dereference of untrusted user pointers
- unbounded copy-in/copy-out
- raw untyped protected-resource handles
- authorization decisions outside securityd for protected resources
- missing deny audit where audit obligation exists
- treating spool output as audit evidence
- treating debug logs as audit evidence
- AMF load without signature verification
- AMF load without revocation check
- Guard approval bypass in High-Assurance where required
- PXM interpreting datasets, jobs, workload policy service classes, or security profiles
- Guard interpreting datasets, jobs, spool entries, or ordinary business policy
- PKU/PKS described as z/OS storage key compatibility
- z/OS, RACF, JES2, DFSMS, SMF, or z/Architecture compatibility claims

The following patterns are prohibited in design documents and release material:

- "z/OS compatible"
- "RACF compatible"
- "JES2 compatible"
- "DFSMS compatible"
- "SMF compatible"
- "z/Architecture compatible"
- "VBS clone"
- "world's most secure OS" without scoped evidence
- "production ready" before the production readiness gate passes
- "High-Assurance" without Guard evidence

## 9. CI and Lint Obligations

AI-authored changes must preserve or introduce the relevant CI/lint obligations.

| CI ID | Obligation | Required for |
| --- | --- | --- |
| CI-001 | Spec ID required check | production-path code and security-sensitive docs |
| CI-002 | Source Matrix reference required check | source-grounded concepts |
| CI-003 | no-fake-success scanner | all production paths |
| CI-004 | TODO/unimplemented scanner | all production paths |
| CI-005 | audit obligation checker | protected-resource and system-interface changes |
| CI-006 | negative test required checker | security-sensitive changes |
| CI-007 | unsafe inventory generator | low-level, kernel, PXM, Guard, parser, and FFI code |
| CI-008 | dependency allowlist checker | any dependency change |
| CI-009 | SBOM generator | release artifacts |
| CI-010 | signed provenance generator | release artifacts |
| CI-011 | reproducible build diff report | release candidates |
| CI-012 | fuzz target registration checker | parser and binary-interface changes |
| CI-013 | prohibited compatibility wording checker | all docs and release material |
| CI-014 | profile claim checker | conformance and release claims |
| CI-015 | evidence artifact manifest checker | release candidates |

CI/lint must fail closed. A missing scanner result is not a pass.

## 10. Negative-Test Requirements

Security-sensitive AI changes must add or update negative tests for every applicable category:

- unauthorized access
- stale handle
- policy version mismatch
- audit write failure
- malformed input
- replay attempt
- downgrade attempt
- rollback attempt
- freeze attempt
- mix-and-match attempt
- concurrent update
- crash mid-transaction
- recovery consistency
- privilege confusion
- caller identity forgery
- cross-partition misuse
- AMF invalid signature
- AMF revoked signer or digest
- Guard root mismatch
- unsupported command success attempt
- spec-gap implementation attempt
- device teardown incomplete
- parser overlong input
- malformed manifest

Negative tests must assert absence of success side effects. It is not enough to assert an error code.

Examples of required absence assertions:

- no dataset handle created
- no catalog entry committed
- no spool content returned
- no AMF module registered
- no executable mapping created
- no partition memory reassigned
- no Guard root advanced
- no release claim emitted

## 11. Evidence Artifacts

AI changes must identify expected evidence artifacts.

Common evidence artifacts:

- requirement traceability report
- Source Matrix lint report
- compatibility wording lint report
- no-fake-success scan report
- TODO/unimplemented scan report
- audit obligation lint report
- negative test report
- fuzz registration report
- fuzz corpus/crash report
- unsafe inventory
- safety contract review
- state-machine model output
- proof review record
- integration test report
- crash-recovery test report
- fault-injection test report
- SBOM
- signed provenance
- reproducible build diff report
- dependency allowlist report
- remote audit export report
- attestation report
- Guard approval/denial evidence
- recovery drill record
- independent review record

Evidence artifacts must be named in AI output even if the artifact is not produced by the current change. Missing expected evidence must be listed as a gap or blocker.

## 12. Release Claim Rules

AI agents must not broaden release claims.

Allowed claims require evidence:

- Baseline conformance
- Enterprise conformance
- High-Assurance conformance
- production readiness
- AMF safety
- update security
- Guard root protection
- partition isolation
- system integrity

Rules:

- A release claim must name the profile.
- A release claim must name the protected assets and boundaries.
- A release claim must cite requirement IDs and Source Matrix IDs.
- A release claim must list evidence artifacts.
- A release claim must list residual risks.
- A release claim must not imply z/OS compatibility.
- High-Assurance claims require Guard evidence.
- Production readiness claims require all production gates in `22-production-readiness.md`.

## 13. Unsafe Code Contract

Any unsafe code must include:

- requirement ID
- source ID where hardware or ABI behavior is involved
- invariant protected by the unsafe block
- caller obligations
- callee obligations
- memory aliasing assumptions
- lifetime assumptions
- concurrency assumptions
- failure behavior
- test coverage
- negative tests
- fuzz targets if input parsing or ABI decoding is involved
- review owner

Unsafe code without this contract is prohibited.

## 14. Parser and Fuzz Contract

AI agents must add fuzz targets for:

- DSN grammar
- JCL-like job syntax
- operator command grammar
- policy language
- AMF manifest
- update metadata
- artifact manifest
- SVC request decoding
- PCALL request decoding
- PXM command pages
- Guard calls
- audit record decoding
- catalog transaction journal decoding

Parser failures must not create protected-resource side effects.

## 15. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-AI-0001 | AI-generated implementation code MUST cite applicable requirement IDs. | CI-001 / review checklist |
| MFOS-REQ-AI-0002 | AI-generated source-grounded design MUST cite Source Matrix IDs. | CI-002 |
| MFOS-REQ-AI-0003 | AI output MUST NOT claim or imply z/OS compatibility. | CI-013 / release review |
| MFOS-REQ-AI-0004 | IBM terminology mapped to MFOS terminology MUST include overlap and divergence. | documentation review |
| MFOS-REQ-AI-0005 | AI-generated production paths MUST NOT use fake success, empty stubs, or silent fallback. | CI-003 / negative test |
| MFOS-REQ-AI-0006 | Specified but unimplemented behavior MUST fail closed as `UNSUPPORTED`. | negative test |
| MFOS-REQ-AI-0007 | Undefined behavior MUST fail closed as `SPEC_GAP` or be blocked before implementation. | spec review / negative test |
| MFOS-REQ-AI-0008 | Security-sensitive changes MUST include negative tests in the same change. | CI-006 |
| MFOS-REQ-AI-0009 | AI changes affecting protected resources MUST specify audit obligations. | CI-005 |
| MFOS-REQ-AI-0010 | AI changes MUST NOT bypass securityd for protected-resource authorization. | architecture review / integration test |
| MFOS-REQ-AI-0011 | Unsafe code MUST include a safety contract. | CI-007 / code review |
| MFOS-REQ-AI-0012 | Parser changes MUST include fuzz targets or documented deferral as a blocker. | CI-012 |
| MFOS-REQ-AI-0013 | PXM changes MUST NOT add MFOS enterprise semantics. | architecture review |
| MFOS-REQ-AI-0014 | Guard changes MUST NOT add job, dataset, catalog, spool, or ordinary business policy semantics. | architecture review |
| MFOS-REQ-AI-0015 | PKU/PKS MUST NOT be treated as the primary system-integrity boundary. | architecture review |
| MFOS-REQ-AI-0016 | AI output for changes MUST include the mandatory 14-section output format. | review checklist |
| MFOS-REQ-AI-0017 | Release-affecting AI output MUST list evidence artifacts and residual risks. | release review |
| MFOS-REQ-AI-0018 | AI agents MUST NOT edit unrelated files or revert other agents' work. | review checklist |

## 16. Invariants

INV-AI-001:

No AI-produced implementation can be accepted without requirement traceability.

INV-AI-002:

No AI-produced z/OS-inspired concept can be accepted without Source Matrix traceability.

INV-AI-003:

No AI-produced protected-resource path can be accepted without authorization and audit obligations.

INV-AI-004:

No AI-produced unsupported or spec-gap path can return success.

INV-AI-005:

No AI-produced release claim can exceed available evidence.

INV-AI-006:

No AI-produced Guard or PXM change can expand those components into MFOS enterprise semantics.

## 17. Failure Modes

| Failure mode | Required behavior |
| --- | --- |
| Missing requirement ID | CI/review failure |
| Missing Source Matrix ID for source-grounded concept | CI/review failure |
| Compatibility wording | release/review failure |
| Missing audit obligation | CI/review failure |
| Missing negative test for security-sensitive path | CI/review failure |
| Fake success detected | CI failure |
| Reachable `todo!()` or `unimplemented!()` in production path | CI failure |
| Unsafe code without safety contract | review failure |
| Parser change without fuzz target | CI/review failure |
| Production claim without gates | release failure |
| High-Assurance claim without Guard evidence | release failure |
| AI edit outside ownership scope | review failure and manual reconciliation |

## 18. Positive Tests

PT-AI-001:

An AI change with requirement IDs, Source Matrix IDs, audit obligations, tests, negative tests, and evidence artifacts passes contract lint.

PT-AI-002:

A specified but unsupported feature returns `MFOS_ERR_UNSUPPORTED` and produces no success side effects.

PT-AI-003:

A spec-gap request returns `MFOS_ERR_SPEC_GAP` or is blocked before implementation.

PT-AI-004:

A parser change with a fuzz target registration passes fuzz target lint.

PT-AI-005:

A release note that says "z/OS-inspired, not z/OS compatible" and lists evidence passes release wording lint.

## 19. Negative Tests

NT-AI-001:

An implementation response without the mandatory 14 output sections fails contract lint.

NT-AI-002:

Code containing reachable placeholder success fails no-fake-success CI.

NT-AI-003:

Code containing reachable `todo!()` or `unimplemented!()` fails production-path lint.

NT-AI-004:

A protected-resource implementation with no securityd decision fails audit/authorization lint.

NT-AI-005:

A protected-resource implementation with no audit obligation fails audit obligation lint.

NT-AI-006:

A security-sensitive change without negative tests fails CI.

NT-AI-007:

An AMF implementation that loads a revoked digest fails negative tests.

NT-AI-008:

A PXM implementation that parses dataset policy fails architecture review.

NT-AI-009:

A Guard implementation that schedules jobs or interprets dataset ACLs fails architecture review.

NT-AI-010:

A release claim containing "z/OS compatible" fails release wording lint.

## 20. Fuzz and Lint Targets

Contract-specific lint targets:

- `ai_output_contract_lint`
- `requirement_id_lint`
- `source_matrix_ref_lint`
- `compatibility_wording_lint`
- `fake_success_lint`
- `todo_unimplemented_lint`
- `audit_obligation_lint`
- `negative_test_presence_lint`
- `unsafe_contract_lint`
- `fuzz_target_registration_lint`
- `profile_claim_lint`
- `evidence_artifact_lint`

Parser fuzz targets are defined by the component specs and tracked by this contract.

## 21. Spec Gaps

SPEC-GAP-AI-001:

The machine-readable AI output schema is not defined.

SPEC-GAP-AI-002:

The final list of production-path directories for no-fake-success scanning is not defined.

SPEC-GAP-AI-003:

The exact syntax for requirement ID comments in code is not defined.

SPEC-GAP-AI-004:

The exact CI implementation for ownership-scope enforcement is not defined.

SPEC-GAP-AI-005:

The final evidence artifact manifest schema is not defined.

SPEC-GAP-AI-006:

The exact threshold for fuzz campaign sufficiency is deferred to component and production readiness specs.

## 22. AI Prompt

Use this prompt for AI implementation tasks:

```text
Future authorized agents would implement or review MFOS.

MFOS is z/OS-inspired, not z/OS compatible.

You must output these sections:
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
- Do not write code without spec IDs.
- Do not use source-grounded concepts without Source Matrix IDs.
- Do not claim z/OS compatibility.
- State IBM overlap and MFOS divergence for mapped terms.
- Do not use fake success, empty stubs, or silent fallback.
- Use UNSUPPORTED for specified but unimplemented behavior.
- Use SPEC_GAP for unspecified behavior.
- Add negative tests for security-sensitive changes.
- Do not omit audit obligations.
- Do not bypass securityd.
- Add safety contracts for unsafe code.
- Add fuzz targets for parsers and binary interfaces.
- Keep PXM out of MFOS enterprise semantics.
- Keep Guard limited to selected High-Assurance root objects.
- Do not use PKU/PKS as the primary system-integrity boundary.
```
