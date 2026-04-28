---
spec_id: "MFOS-SPEC-22-PRODUCTION-READINESS"
title: "MFOS Production Readiness Gate v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001", "EXTREF-IBM-Z-DPM-0001", "EXTREF-IBM-ZOS-JES-INTRODUCTION-0001", "EXTREF-IBM-ZOS-JES-JOB-FLOW-0001", "EXTREF-IBM-Z-LPAR-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001", "EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001", "MS-VBS-001", "MS-VSM-001", "NIST-160-001", "NIST-193-001", "NIST-218-001", "SEL4-001", "SLSA-001", "TCG-001", "TUF-001", "X64-AMD-001", "X64-INTEL-001", "X64-LINUX-PKU-001"]
requirement_refs: ["MFOS-REQ-PROD-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Production Readiness Gate v0.1

Status: Draft  
Owner: MFOS architecture  
Profile applicability: Baseline, Enterprise-Standalone, Enterprise-PXM, High-Assurance  
Source basis: user-provided MFOS Source-Grounded High-Assurance Architecture v0.3

## 1. Purpose

This document defines the MFOS production readiness gate.

MFOS may not claim production readiness until the applicable gates in this specification pass with evidence. The gate separates "a specification exists" from "a deployable production claim is supported."

MFOS is z/OS-inspired, not z/OS compatible. No production gate may be interpreted as a compatibility claim for z/OS, RACF, JES2/JES3, DFSMS, SMF, z/Architecture, Windows VBS, or any IBM product.

## 2. Scope

This specification covers:

- production readiness gates
- profile-specific release claim rules
- required evidence artifacts
- CI/lint obligations for release candidates
- negative-test requirements
- supply-chain release obligations
- audit and recovery readiness
- Guard evidence required before High-Assurance claims
- release blocker handling

## 3. Non-Objectives

This document does not:

- define every component's detailed implementation
- replace component conformance tests
- authorize z/OS compatibility claims
- authorize High-Assurance claims without Guard evidence
- authorize production device passthrough without PXM teardown evidence
- define final SBOM or provenance file formats
- define the final release signing infrastructure
- waive source-grounding requirements

## 4. Source Matrix References

Required source IDs for this gate:

- EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001: system integrity claim discipline.
- EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001: authorized-boundary negative testing.
- EXTREF-IBM-ZOS-SECURITY-SERVER-0001: security manager inspiration and access-control centrality.
- EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001: protected resource authorization inspiration.
- EXTREF-IBM-ZOS-JES-INTRODUCTION-0001: job/spool inspiration.
- EXTREF-IBM-ZOS-JES-JOB-FLOW-0001: job lifecycle inspiration.
- EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001: catalog and dataset inspiration.
- EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001: audit/accounting evidence inspiration.
- EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001: security audit record inspiration.
- EXTREF-IBM-Z-LPAR-INTRODUCTION-0001: partition isolation inspiration.
- EXTREF-IBM-Z-DPM-0001: partition management plane inspiration.
- X64-INTEL-001: x64 mechanism reality.
- X64-AMD-001: AMD64 mechanism reality.
- X64-LINUX-PKU-001: PKU limitation reference.
- MS-VBS-001: High-Assurance Guard comparison only.
- MS-VSM-001: High-Assurance Guard comparison only.
- TCG-001: measured boot and TPM evidence.
- NIST-160-001: secure systems engineering.
- NIST-218-001: secure development practice.
- NIST-193-001: firmware resilience and recovery.
- SLSA-001: provenance and build integrity.
- TUF-001: update rollback, freeze, and mix-and-match resistance.
- SEL4-001: formal assurance boundary reference.
- FBVBS-001: traceability, production proof obligations, evidence discipline, and no-fake-success gates.

## 5. Release Claim Rules

This specification introduces the draft requirement namespace `MFOS-REQ-PROD-*` for production readiness requirements. The namespace must be added to the global normative-language registry before the production readiness spec can be treated as frozen.

RCR-001:

MFOS release material must say "z/OS-inspired" or "source-grounded enterprise semantics" and must not say or imply "z/OS compatible."

RCR-002:

A production claim must name the profile:

- Baseline production
- Enterprise-Standalone production
- Enterprise-PXM production
- High-Assurance production

RCR-003:

A profile claim must list:

- requirement IDs
- Source Matrix IDs
- protected resources
- threat boundaries
- system interfaces covered
- tests and negative tests
- fuzz campaigns
- evidence artifacts
- residual risks
- unsupported features
- spec gaps

RCR-004:

High-Assurance claims require PXM Guard evidence. A release without Guard evidence may still claim Baseline, Enterprise-Standalone, or Enterprise-PXM readiness if those gates pass, but must not imply High-Assurance readiness.

RCR-005:

Production readiness must fail closed. Missing evidence is a release blocker, not a pass.

RCR-006:

Release notes must distinguish:

- implemented behavior
- unsupported specified behavior
- spec gaps
- non-objectives
- residual risks

RCR-007:

Hardware feature availability must be stated as platform applicability, not as a universal guarantee.

RCR-008:

PKU, PKS, CET, SMEP, SMAP, NX, W^X, IOMMU, VMX, SVM, EPT, and NPT may be cited as mechanisms only. They do not replace MFOS authorization or audit semantics.

## 6. Gate Summary

MFOS may not claim production readiness until every applicable gate passes:

```text
PROD-001  Source Matrix complete for all z/OS-inspired concepts
PROD-002  System Integrity negative tests pass
PROD-003  Unauthorized dataset access cannot produce handle
PROD-004  DENY audit record emitted before caller result
PROD-005  Catalog crash recovery passes
PROD-006  Spool browse/purge security enforced
PROD-007  Operator commands require authority and audit
PROD-008  AMF unsupported-load or invalid signature/revoked signer fail closed
PROD-009  Update rollback/freeze/mix-and-match tests pass
PROD-010  SBOM and signed provenance produced
PROD-011  No fake success CI clean
PROD-012  Parser fuzz campaigns complete
PROD-013  PXM device teardown tested before passthrough production
PROD-014  Guard evidence exists before High-Assurance claim
PROD-015  Recovery drill completed
```

## 7. Gate Details

### PROD-001 Source Matrix Complete

Requirement:

All z/OS-inspired, IBM-derived, x64-derived, update, supply-chain, and assurance concepts in release scope must have Source Matrix IDs.

Acceptance evidence:

- source matrix completeness report
- source-matrix lint pass
- compatibility wording lint pass
- documentation review record

Negative tests:

- remove a required Source Matrix ID and verify release lint fails
- add "z/OS compatible" wording and verify release lint fails

### PROD-002 System Integrity Negative Tests Pass

Requirement:

System integrity negative tests must pass for SVC, PCALL, operator command, dataset open, catalog update, job submit, spool browse/purge, disabled-mode AMF load request or production AMF load where claimed, update activation, PXM_CALL, and Guard where applicable.

Acceptance evidence:

- system integrity test report
- zACS-style boundary test report
- authorization bypass negative test report
- audit bypass negative test report

Negative tests:

- caller identity forgery
- direct user pointer misuse
- unsupported system interface success attempt
- spec-gap behavior implementation attempt

### PROD-003 Unauthorized Dataset Access Cannot Produce Handle

Requirement:

Unauthorized dataset access must not create a dataset handle or any side effect equivalent to access.

Acceptance evidence:

- dataset authorization integration test report
- stale handle test report
- policy version mismatch test report
- audit record IDs for deny events

Negative tests:

- BOB reads ALICE dataset
- stale handle reuse after policy update
- malformed DSN authorization confusion
- catalog generation mismatch

### PROD-004 DENY Audit Before Caller Result

Requirement:

A deny decision with audit obligation must be recorded before the caller receives the final denied result.

Acceptance evidence:

- audit ordering test report
- audit chain verification report
- fault injection report for auditd unavailable behavior
- record IDs and correlation IDs

Negative tests:

- auditd unavailable during deny
- audit write failure
- audit chain tamper attempt
- caller receives denial before audit path completes

### PROD-005 Catalog Crash Recovery Passes

Requirement:

Catalog transactions must recover consistently after crash at defined transaction points.

Acceptance evidence:

- catalog crash recovery test report
- transaction journal replay report
- orphan extent repair report where applicable
- recovery audit records

Negative tests:

- crash after journal write before commit
- crash after commit before audit
- corrupt generation number
- immutable catalog entry mutation attempt

### PROD-006 Spool Browse/Purge Security Enforced

Requirement:

Spool browse, purge, and export must require securityd decisions and must respect retention policy.

Acceptance evidence:

- spool authorization test report
- retention enforcement test report
- spool audit record IDs

Negative tests:

- unauthorized browse
- unauthorized purge
- purge before retention expiry
- export without authority

### PROD-007 Operator Commands Require Authority and Audit

Requirement:

Operator commands must parse, resolve target, authorize through securityd, require confirmation/dual-control where applicable, execute only after authorization, and audit.

Acceptance evidence:

- operator command conformance report
- destructive command drill report
- emergency mode drill report
- command audit record IDs

Negative tests:

- destructive command without confirmation
- command authority mismatch
- automation hook bypass attempt
- emergency mode without reason or expiry

### PROD-008 AMF Unsupported Load or Invalid Signature and Revocation Fail Closed

Requirement:

If the release uses `Baseline-AMF-Disabled`, AMF load must return `MFOS_ERR_UNSUPPORTED` and must not create an executable mapping, registry entry, or success result.

If the release claims `AMF-Test`, the release must be explicitly non-production.

If the release claims `Enterprise-AMF` or `High-Assurance-AMF`, AMF module load must fail closed for invalid signature, invalid manifest, revoked signer, revoked digest, missing authority class, stale security epoch, missing audit obligation, or missing Guard approval where Guard is required.

Acceptance evidence:

- AMF mode declaration
- unsupported-load negative test for `Baseline-AMF-Disabled`
- AMF load test report
- signature verification report
- revocation test report
- AMF audit records
- Guard approval evidence for High-Assurance

Negative tests:

- AMF load in `Baseline-AMF-Disabled`
- invalid signature
- revoked signer
- revoked digest
- mutable dataset load
- authority class mismatch
- Guard denial in High-Assurance

### PROD-009 Update Rollback, Freeze, and Mix-and-Match Tests Pass

Requirement:

UVS must reject rollback, freeze, mix-and-match, stale security epoch, unsigned artifact, hash/size mismatch, and dependency confusion attempts.

Acceptance evidence:

- update verification test report
- rollback/freeze/mix-and-match test report
- manifest verification report
- dependency/conflict report
- activation transaction journal

Negative tests:

- older generation update
- expired timestamp metadata
- mismatched snapshot and targets metadata
- artifact hash mismatch
- dependency downgrade

### PROD-010 SBOM and Signed Provenance Produced

Requirement:

Release artifacts must include SBOM and signed provenance.

Acceptance evidence:

- SBOM
- signed provenance
- reproducible build diff report
- dependency allowlist report
- build toolchain pin report

Negative tests:

- missing SBOM
- unsigned provenance
- dependency outside allowlist
- unpinned toolchain
- unreproducible build without approved exception

### PROD-011 No Fake Success CI Clean

Requirement:

No fake success, empty stub, silent fallback, reachable placeholder success, or reachable production-path `todo!()`/`unimplemented!()` may exist in release scope.

Acceptance evidence:

- no-fake-success scan report
- TODO/unimplemented scan report
- unsupported/spec-gap negative test report

Negative tests:

- injected placeholder success is detected
- injected reachable `todo!()` is detected
- unsupported interface success attempt fails
- spec-gap operation success attempt fails

### PROD-012 Parser Fuzz Campaigns Complete

Requirement:

All release-scope parsers and binary-interface decoders must have fuzz targets and complete the configured fuzz campaign threshold.

Acceptance evidence:

- fuzz target registry
- fuzz campaign report
- crash triage report
- corpus seed manifest

Required fuzz targets:

- DSN grammar
- JCL-like syntax
- operator command grammar
- policy language
- AMF manifest
- update metadata
- artifact manifest
- SVC request decoding
- PCALL request decoding
- PXM command pages
- Guard calls where applicable
- audit record decoding
- catalog transaction journal

Negative tests:

- overlong input
- invalid UTF-8 or invalid byte sequences where applicable
- malformed length fields
- unknown required fields
- recursive or deeply nested payload
- parser panic attempt

### PROD-013 PXM Device Teardown Tested Before Passthrough Production

Requirement:

No passthrough device assignment may be production-enabled until PXM device teardown, IOMMU domain revocation, interrupt route revocation, ownership record cleanup, and memory zeroing are tested.

Acceptance evidence:

- PXM device assignment test report
- device teardown checklist report
- IOMMU domain test report
- interrupt remapping test report
- memory reuse zeroing test report
- partition audit record IDs

Negative tests:

- reassignment before teardown completion
- stale interrupt route
- stale IOMMU mapping
- DMA after release
- memory reuse before zeroing

### PROD-014 Guard Evidence Exists Before High-Assurance Claim

Requirement:

High-Assurance release claims require Guard evidence for selected root objects.

Acceptance evidence:

- Guard root seal report
- security policy root transition evidence
- audit chain root evidence
- AMF registry approval evidence
- SVC table verification evidence
- executable mapping policy evidence
- attestation report
- Guard fault-injection report

Negative tests:

- root rollback attempt
- stale measurement context
- SVC table digest mismatch
- AMF registry mismatch
- executable mapping denial
- Guard unavailable at boot

### PROD-015 Recovery Drill Completed

Requirement:

Release candidates must complete recovery drills for boot failure, audit/security service failure, catalog recovery, update rollback, and partition recovery where applicable.

Acceptance evidence:

- recovery drill report
- recovery partition report where applicable
- rollback workflow report
- forensics/export report where applicable
- post-recovery audit chain verification

Negative tests:

- securityd unavailable at boot
- auditd unavailable at boot
- update activation failure
- catalog corruption recovery
- partition fault recovery
- Guard required but unavailable in High-Assurance

## 8. CI and Lint Obligations

Release candidates must pass:

- CI-001 spec ID required check
- CI-002 source matrix ref required check
- CI-003 no fake success scanner
- CI-004 TODO/unimplemented scanner for production paths
- CI-005 audit obligation checker
- CI-006 negative test required checker
- CI-007 unsafe inventory generator
- CI-008 dependency allowlist checker
- CI-009 SBOM generator
- CI-010 signed provenance generator
- CI-011 reproducible build diff report
- CI-012 fuzz target registration checker
- CI-013 prohibited compatibility wording checker
- CI-014 profile claim checker
- CI-015 evidence artifact manifest checker

Release CI rules:

- Missing CI output is failure.
- Skipped CI must be explicitly approved and recorded as a release blocker or waiver.
- Waivers for security gates require independent review and expiry.
- High-Assurance gate waivers are not allowed for Guard root evidence.

## 9. Evidence Artifact Manifest

Each release candidate must produce an evidence artifact manifest with:

```yaml
release_id: string
profile_claim: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
amf_mode: Baseline-AMF-Disabled | AMF-Test | Enterprise-AMF | High-Assurance-AMF
source_matrix_report: path
requirement_traceability_report: path
compatibility_wording_report: path
test_reports:
  positive: [path]
  negative: [path]
  integration: [path]
  crash_recovery: [path]
  fault_injection: [path]
fuzz_reports: [path]
audit_evidence:
  audit_record_ids: [string]
  audit_chain_report: path
supply_chain:
  sbom: path
  signed_provenance: path
  reproducible_build_report: path
  dependency_allowlist_report: path
pxm_evidence:
  required: bool
  reports: [path]
guard_evidence:
  required: bool
  reports: [path]
recovery_drill_reports: [path]
unsupported_features: [string]
spec_gaps: [string]
residual_risks: [string]
approvals: [string]
```

The manifest schema is draft. Missing required entries are release blockers unless explicitly marked non-applicable by profile and reviewed.

## 10. Negative-Test Minimum Set

Every production release candidate must include negative tests covering:

- unauthorized dataset access
- stale dataset handle
- policy version mismatch
- audit write failure
- malformed SVC request
- malformed PCALL request
- malformed operator command
- malformed DSN
- malformed JCL-like input
- catalog crash mid-transaction
- unauthorized spool browse
- unauthorized spool purge
- operator authority mismatch
- destructive command without confirmation
- AMF disabled-mode load success attempt
- AMF invalid signature where Enterprise-AMF or High-Assurance-AMF is claimed
- AMF revoked signer or digest where Enterprise-AMF or High-Assurance-AMF is claimed
- update rollback
- update freeze
- update mix-and-match
- missing SBOM/provenance detection
- fake success injection
- TODO/unimplemented injection
- parser overlong input
- PXM invalid state transition
- PXM teardown incomplete where PXM is release scope
- Guard root mismatch where High-Assurance is claimed
- recovery drill failure

Negative tests must verify both:

- correct error or denial
- absence of success side effects

## 11. Release Blockers

The following are unconditional release blockers:

- z/OS compatibility claim
- missing Source Matrix coverage for release-scope z/OS-inspired concepts
- unauthorized dataset access creates a handle
- deny audit ordering failure
- fake success in production path
- reachable production-path `todo!()` or `unimplemented!()`
- AMF load succeeds in `Baseline-AMF-Disabled`
- AMF invalid signature accepted when Enterprise-AMF or High-Assurance-AMF is claimed
- revoked AMF signer or digest accepted when Enterprise-AMF or High-Assurance-AMF is claimed
- update rollback/freeze/mix-and-match accepted
- missing SBOM for Enterprise-Standalone, Enterprise-PXM, or High-Assurance
- missing signed provenance for Enterprise-Standalone, Enterprise-PXM, or High-Assurance
- missing Guard evidence for High-Assurance
- PXM device passthrough or device assignment claim without teardown evidence
- recovery drill not completed
- missing evidence manifest

## 12. Profile-Specific Gates

Baseline production:

- PROD-001 through PROD-012 required.
- NX-capable platform and W^X policy evidence required once a nucleus exists.
- AMF mode must be `Baseline-AMF-Disabled`; AMF load must return `MFOS_ERR_UNSUPPORTED`.
- PROD-013 not applicable because PXM passthrough production is not in Baseline scope.
- PROD-014 not applicable unless High-Assurance claims are made.
- PROD-015 required for release-scope recovery paths.

Enterprise-Standalone production:

- PROD-001 through PROD-012 required.
- PROD-010 required.
- remote audit export evidence required.
- measured boot/TPM evidence required.
- IOMMU evidence required for platform DMA protection.
- no cross-partition device assignment, side-partition isolation, or PXM passthrough claim allowed.
- PROD-013 not applicable.
- PROD-014 not applicable unless Guard claims are made.
- PROD-015 required.
- AMF mode must be `Baseline-AMF-Disabled` unless the release separately claims `Enterprise-AMF`.

Enterprise-PXM production:

- PROD-001 through PROD-013 required.
- PROD-010 required.
- remote audit export evidence required.
- measured boot/TPM evidence required.
- PXM, IOMMU, interrupt remapping, partition audit, and device teardown evidence required.
- side-partition and device assignment claims allowed only within evidenced PXM scope.
- PROD-014 not applicable unless Guard claims are made.
- PROD-015 required.
- AMF mode must be `Baseline-AMF-Disabled` unless the release separately claims `Enterprise-AMF`.

High-Assurance production:

- PROD-001 through PROD-015 required.
- Guard evidence is mandatory.
- Remote attestation evidence is mandatory.
- Independent TCB review is mandatory.
- High-Assurance-AMF requires Guard-approved AMF registry and executable mapping evidence when AMF is in scope.
- Guard gate waivers are not allowed.

## 13. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-PROD-0001 | Production readiness MUST require all applicable PROD gates to pass. | release review |
| MFOS-REQ-PROD-0002 | Release material MUST NOT claim or imply z/OS compatibility. | CI-013 |
| MFOS-REQ-PROD-0003 | Release claims MUST name profile, evidence, unsupported features, spec gaps, and residual risks. | release review |
| MFOS-REQ-PROD-0004 | Missing release evidence MUST be treated as a blocker unless explicitly non-applicable by profile. | evidence manifest review |
| MFOS-REQ-PROD-0005 | Production release candidates MUST pass no-fake-success CI. | CI-003 |
| MFOS-REQ-PROD-0006 | Production release candidates MUST include required negative-test reports. | CI-006 / release review |
| MFOS-REQ-PROD-0007 | Enterprise-Standalone, Enterprise-PXM, and High-Assurance release artifacts MUST include SBOM and signed provenance. | CI-009 / CI-010 |
| MFOS-REQ-PROD-0008 | High-Assurance claims MUST require Guard evidence. | release review |
| MFOS-REQ-PROD-0009 | PXM passthrough production MUST require teardown evidence. | release review |
| MFOS-REQ-PROD-0010 | Recovery drills MUST be completed before production claim. | recovery drill review |
| MFOS-REQ-PROD-0011 | Release CI/lint skips MUST be recorded as blockers or reviewed waivers with expiry. | release review |
| MFOS-REQ-PROD-0012 | Negative tests MUST assert absence of success side effects. | test review |
| MFOS-REQ-PROD-0013 | Baseline production MUST require NX-capable platform evidence and W^X policy evidence once a nucleus exists. | platform / memory mapping review |
| MFOS-REQ-PROD-0014 | Production releases MUST declare AMF mode and enforce the corresponding unsupported-load or AMF governance gates. | AMF release review |

## 14. Invariants

INV-PROD-001:

Production readiness cannot be claimed while any applicable gate is failing, missing, or unknown.

INV-PROD-002:

A High-Assurance claim cannot exist without Guard evidence.

INV-PROD-003:

An Enterprise-Standalone, Enterprise-PXM, or High-Assurance supply-chain claim cannot exist without SBOM and signed provenance.

INV-PROD-004:

Unauthorized access, audit bypass, AMF unsupported-load bypass, AMF signature bypass, update rollback, fake success, and recovery failure are release blockers.

INV-PROD-005:

Release material cannot imply z/OS compatibility.

## 15. Failure Modes

| Failure mode | Required behavior |
| --- | --- |
| Gate result missing | release blocked |
| Evidence artifact missing | release blocked unless non-applicable by profile |
| Compatibility wording detected | release blocked |
| Negative test missing | release blocked |
| Fuzz target missing for parser in scope | release blocked |
| SBOM/provenance missing for Enterprise-Standalone/Enterprise-PXM/High-Assurance | release blocked |
| Guard evidence missing for High-Assurance | release blocked |
| PXM teardown evidence missing for passthrough production | release blocked |
| Recovery drill failure | release blocked |
| CI unavailable | release blocked or waiver with expiry where allowed |
| Waiver expired | release blocked |

## 16. Positive Tests

PT-PROD-001:

A Baseline release candidate with PROD-001 through PROD-012 evidence and no prohibited claims passes Baseline release review.

PT-PROD-002:

An Enterprise-Standalone release candidate with SBOM, signed provenance, update security tests, remote audit evidence, measured boot/TPM evidence, platform DMA protection evidence, and required negative tests passes Enterprise-Standalone release review.

PT-PROD-003:

An Enterprise-PXM release candidate with Enterprise-Standalone evidence plus PXM lifecycle, IOMMU, interrupt remapping, partition audit, and device teardown evidence passes Enterprise-PXM release review.

PT-PROD-004:

A High-Assurance release candidate with Guard root evidence, attestation evidence, and all PROD gates passes High-Assurance release review.

PT-PROD-005:

A release evidence manifest with all required entries passes evidence manifest lint.

## 17. Negative Tests

NT-PROD-001:

Release notes containing "z/OS compatible" fail release wording lint.

NT-PROD-002:

A release candidate missing Source Matrix coverage for an IBM-derived concept fails release review.

NT-PROD-003:

A release candidate where unauthorized dataset access creates a handle fails PROD-003.

NT-PROD-004:

A release candidate where deny audit occurs after caller result fails PROD-004.

NT-PROD-005:

A Baseline release candidate where AMF load succeeds fails PROD-008.

NT-PROD-006:

A release candidate claiming Enterprise-AMF or High-Assurance-AMF while accepting AMF invalid signature fails PROD-008.

NT-PROD-007:

A release candidate accepting update rollback fails PROD-009.

NT-PROD-008:

A release candidate missing SBOM or signed provenance fails Enterprise-Standalone, Enterprise-PXM, or High-Assurance release review.

NT-PROD-009:

A High-Assurance release candidate missing Guard evidence fails PROD-014.

NT-PROD-009:

A passthrough release candidate missing PXM teardown evidence fails PROD-013.

NT-PROD-010:

A release candidate with a fake-success injection passes unit tests but fails no-fake-success CI and release review.

## 18. Fuzz and Lint Targets

Release lint targets:

- `production_gate_lint`
- `evidence_manifest_lint`
- `profile_claim_lint`
- `compatibility_wording_lint`
- `source_matrix_completeness_lint`
- `requirement_traceability_lint`
- `no_fake_success_lint`
- `todo_unimplemented_lint`
- `negative_test_presence_lint`
- `fuzz_target_registration_lint`
- `supply_chain_artifact_lint`
- `guard_evidence_lint`
- `pxm_teardown_evidence_lint`
- `recovery_drill_lint`

Release fuzz campaign targets are listed in PROD-012.

## 19. Spec Gaps

SPEC-GAP-PROD-001:

The final evidence artifact manifest schema is not fixed.

SPEC-GAP-PROD-002:

The final fuzz campaign duration, coverage threshold, and corpus quality bar are not fixed.

SPEC-GAP-PROD-003:

The final release waiver process and approval authority are not fixed.

SPEC-GAP-PROD-004:

The exact SBOM format is not fixed.

SPEC-GAP-PROD-005:

The exact signed provenance format and signing infrastructure are not fixed.

SPEC-GAP-PROD-006:

The final remote attestation claim format is not fixed.

SPEC-GAP-PROD-007:

The exact production-path directory list for scanners is not fixed.

SPEC-GAP-PROD-008:

The final independent TCB review workflow is not fixed.

SPEC-GAP-PROD-009:

The `MFOS-REQ-PROD-*` namespace is introduced here but is not yet registered in the global normative-language namespace table.

## 20. AI Prompt

Use this prompt for production readiness review:

```text
You are the MFOS production readiness reviewer.

MFOS is z/OS-inspired, not z/OS compatible.

Review the release candidate against:
- PROD-001 through PROD-015
- profile-specific gates
- release claim rules
- prohibited compatibility wording
- required CI/lint outputs
- required negative tests
- required fuzz campaign evidence
- required supply-chain artifacts
- required audit evidence
- PXM teardown evidence where passthrough is in scope
- Guard evidence where High-Assurance is claimed
- recovery drill evidence

Output:
1. Profile Claim Reviewed
2. Gates Passed
3. Gates Failed
4. Missing Evidence
5. Unsupported Features
6. Spec Gaps
7. Residual Risks
8. Release Blockers
9. Waivers Requested
10. Final Recommendation

Do not approve production readiness if any applicable gate is failing, missing, or unknown.
Do not approve High-Assurance without Guard evidence.
Do not approve any release material that implies z/OS compatibility.
```
