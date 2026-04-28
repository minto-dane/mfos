---
spec_id: "MFOS-SPEC-20-CONFORMANCE"
title: "MFOS Design Specification 20: Conformance"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "NIST-160-001", "NIST-218-001"]
requirement_refs: ["MFOS-REQ-CONF-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Design Specification 20: Conformance

Status: Draft v0.1

Audience: implementation agents, conformance test authors, release reviewers, assurance reviewers

This document defines how an implementation claims MFOS conformance. MFOS is z/OS-inspired and source-grounded, but this conformance model does not claim z/OS compatibility, z/Architecture compatibility, IBM API compatibility, or IBM product compatibility.

## 1. Purpose

Conformance gives implementation agents and reviewers a fixed way to answer:

- Which MFOS profile is implemented?
- Which requirements are satisfied?
- Which features are unsupported?
- Which behaviors remain spec gaps?
- Which tests and evidence must exist?
- Which claims are forbidden?

## 2. Conformance Profiles

MFOS has four profiles:

- Baseline.
- Enterprise-Standalone.
- Enterprise-PXM.
- High-Assurance.

An implementation may claim a lower profile while implementing optional pieces from a higher profile. Optional implementation does not automatically grant a higher-profile claim.

## 3. Forbidden Claims

All profiles MUST NOT claim:

- z/OS compatibility.
- z/Architecture compatibility.
- IBM API compatibility.
- RACF compatibility.
- JES2 or JES3 compatibility.
- DFSMS compatibility.
- SMP/E compatibility.
- Windows VBS compatibility.
- seL4-equivalent verification.
- Production readiness without production gate evidence.
- High-Assurance without PXM Guard evidence.

## 4. Baseline Conformance

Baseline requires:

- Source matrix references for z/OS-inspired concepts.
- Normative language and profile compliance.
- Glossary and object model alignment.
- System integrity requirements.
- Central authorization through securityd.
- Mandatory audit obligations through auditd.
- Dataset/catalog model.
- Job/spool model.
- Operator console model.
- AMF specification with AMF load disabled by default.
- Update verification for signed artifacts.
- Typed SVC/PCALL where nucleus work exists.
- NX-capable platform and W^X policy once a nucleus exists.
- No fake success.
- Negative tests for security-sensitive paths.

Baseline may use implicit single partition mode.

Baseline must not claim:

- Guard root protection.
- Resistance after authorized module compromise.
- Production-grade device passthrough assurance.
- Complete remote attestation.
- Production AMF load support.

## 5. Enterprise-Standalone Conformance

Enterprise-Standalone includes all Baseline requirements and adds:

- Secure Boot requirement.
- Measured Boot requirement.
- TPM requirement for profile claims that bind secrets or measurements.
- IOMMU for platform DMA protection.
- Remote audit export.
- TUF-like update metadata.
- Rollback, freeze, and mix-and-match update tests.
- SBOM.
- Signed provenance.
- Dependency allowlist.
- Pinned toolchain.
- Production-oriented recovery drill.

Enterprise-Standalone does not require PXM. It must not claim cross-partition device assignment, side-partition isolation, PXM passthrough production, or partition lifecycle isolation beyond implicit single partition.

Enterprise-Standalone may separately claim Enterprise-AMF only when the AMF specification evidence, signed and measured artifacts, revocation, immutable source, securityd authorization, auditd records, and production readiness evidence exist.

## 6. Enterprise-PXM Conformance

Enterprise-PXM includes all Enterprise-Standalone requirements and adds:

- PXM required.
- IOMMU required.
- Interrupt remapping required.
- Partition lifecycle evidence.
- Partition audit.
- PXM device teardown evidence before any device assignment claim.
- Side-partition isolation claims only for evidenced partition boundaries.

Enterprise-PXM may separately claim Enterprise-AMF under the same Enterprise-AMF conditions as Enterprise-Standalone. Guard remains optional unless a High-Assurance claim is made.

## 7. High-Assurance Conformance

High-Assurance includes all Enterprise-PXM requirements and adds:

- PXM required.
- PXM Guard required.
- Guard-sealed security policy root.
- Guard-sealed audit root.
- Guard involvement for AMF registry.
- Guard executable mapping policy.
- Guard SVC table verification where claimed.
- Remote attestation evidence.
- Formal model coverage for core state machines.
- Independent review for TCB changes.
- High-Assurance production proof obligations.

Guard must remain small. Guard must not interpret job scheduling, dataset policy, spool formatting, operator business commands, or workload policy service classes.

## 8. Requirement Status Vocabulary

| Status | Meaning |
| --- | --- |
| SATISFIED | Implemented, tested, reviewed, and evidenced for the claimed profile. |
| PARTIAL | Some required behavior exists but evidence is incomplete. |
| UNSUPPORTED | Specified behavior is intentionally not implemented and fails closed. |
| SPEC_GAP | Behavior is not specified and must not be implemented as success. |
| NOT_APPLICABLE | Requirement does not apply to the claimed profile or configuration. |
| BLOCKED | Cannot be claimed because of missing evidence, risk, or unresolved design conflict. |

## 9. Conformance Matrix

| Capability | Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance |
| --- | --- | --- | --- | --- |
| Source Matrix references | MUST | MUST | MUST | MUST |
| Requirement IDs | MUST | MUST | MUST | MUST |
| No compatibility claim | MUST | MUST | MUST | MUST |
| securityd central PDP | MUST | MUST | MUST | MUST |
| auditd evidence service | MUST | MUST | MUST | MUST |
| DENY-before-result audit | MUST | MUST | MUST | MUST |
| no fake success | MUST | MUST | MUST | MUST |
| negative tests | MUST | MUST | MUST | MUST |
| parser fuzz targets | MUST when parser exists | MUST | MUST | MUST |
| dataset/catalog semantics | MUST | MUST | MUST | MUST |
| job/spool semantics | MUST | MUST | MUST | MUST |
| operator authority and audit | MUST | MUST | MUST | MUST |
| NX-capable platform | MUST | MUST | MUST | MUST |
| W^X policy | MUST | MUST | MUST | MUST |
| AMF production load | MUST NOT | MUST NOT unless Enterprise-AMF claimed | MUST NOT unless Enterprise-AMF claimed | MUST with Guard approval if AMF is in scope |
| AMF test profile | MAY | MAY | MAY | MAY |
| AMF revocation | SHOULD in spec only | MUST for Enterprise-AMF | MUST for Enterprise-AMF | MUST |
| update signature/hash checks | MUST | MUST | MUST | MUST |
| TUF-like metadata | SHOULD | MUST | MUST | MUST |
| SBOM and provenance | SHOULD | MUST | MUST | MUST |
| Secure Boot | SHOULD | MUST | MUST | MUST |
| Measured Boot | MAY | MUST | MUST | MUST |
| TPM | MAY | MUST | MUST | MUST |
| IOMMU | SHOULD for DMA protection | MUST for platform DMA protection | MUST | MUST |
| interrupt remapping | SHOULD when supported | SHOULD when supported | MUST | MUST |
| PXM | MAY implicit | MUST NOT be required | MUST | MUST |
| PXM Guard | MUST NOT be required | MUST NOT be required | MAY | MUST |
| Guard evidence | NOT_APPLICABLE | NOT_APPLICABLE unless claimed | if claimed | MUST |
| formal model coverage | SHOULD core | SHOULD core/security | SHOULD core/security/PXM | MUST core/security/Guard |

## 10. Conformance Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-CONF-0001 | An implementation must name exactly one claimed profile per release artifact. | release review |
| MFOS-REQ-CONF-0002 | A release may implement optional higher-profile features without claiming that profile. | claim review |
| MFOS-REQ-CONF-0003 | A conformance claim must include a requirements status matrix. | conformance audit |
| MFOS-REQ-CONF-0004 | UNSUPPORTED features must fail closed with typed errors. | no-fake-success CI |
| MFOS-REQ-CONF-0005 | SPEC_GAP behaviors must not be implemented as success paths. | spec review |
| MFOS-REQ-CONF-0006 | Security-sensitive satisfied requirements must include negative tests. | evidence review |
| MFOS-REQ-CONF-0007 | Parser conformance must include fuzz target registration. | fuzz review |
| MFOS-REQ-CONF-0008 | Production readiness claim must pass PROD-001 through PROD-015. | release gate |
| MFOS-REQ-CONF-0009 | High-Assurance conformance must include Guard evidence for every claimed Guard root. | HA review |
| MFOS-REQ-CONF-0010 | Release wording must pass compatibility claim review. | release wording review |
| MFOS-REQ-CONF-0011 | Conformance claims MUST distinguish Enterprise-Standalone from Enterprise-PXM. | release review |
| MFOS-REQ-CONF-0012 | Baseline conformance MUST require NX-capable platform evidence and W^X policy evidence once a nucleus exists. | platform / memory mapping review |
| MFOS-REQ-CONF-0013 | AMF load support MUST be reported as Baseline-AMF-Disabled, AMF-Test, Enterprise-AMF, or High-Assurance-AMF. | AMF conformance review |

## 11. Conformance Test Suites

Required suites:

- `source_matrix_lint`.
- `spec_id_lint`.
- `no_fake_success`.
- `audit_obligation_lint`.
- `negative_test_required`.
- `parser_fuzz_registration`.
- `securityd_mediation`.
- `audit_deny_before_result`.
- `dataset_catalog_conformance`.
- `job_spool_conformance`.
- `operator_console_conformance`.
- `amf_conformance` for AMF mode declarations; production AMF load tests only when Enterprise-AMF or High-Assurance-AMF is claimed.
- `uvs_conformance`.
- `svc_pcall_conformance`.
- `pxm_conformance` when PXM is claimed.
- `guard_conformance` when High-Assurance is claimed.
- `supply_chain_conformance` for Enterprise-Standalone, Enterprise-PXM, and High-Assurance.

## 12. Production Readiness Gate

Production readiness is not identical to conformance. A development build may satisfy many requirements but still fail production readiness.

Required production gates:

- PROD-001 Source Matrix complete for all z/OS-inspired concepts.
- PROD-002 System Integrity negative tests pass.
- PROD-003 Unauthorized dataset access cannot produce handle.
- PROD-004 DENY audit record emitted before caller result.
- PROD-005 Catalog crash recovery passes.
- PROD-006 Spool browse/purge security enforced.
- PROD-007 Operator commands require authority and audit.
- PROD-008 AMF unsupported-load or AMF invalid signature/revoked signer fail closed, depending on AMF mode.
- PROD-009 Update rollback/freeze/mix-and-match tests pass.
- PROD-010 SBOM and signed provenance produced.
- PROD-011 No fake success CI clean.
- PROD-012 Parser fuzz campaigns complete.
- PROD-013 PXM device teardown tested before passthrough production.
- PROD-014 Guard evidence exists before HA claim.
- PROD-015 Recovery drill completed.

## 13. Conformance Statement Schema

```yaml
MFOSConformanceStatement:
  statement_id: string
  release_id: string
  claimed_profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  amf_mode: Baseline-AMF-Disabled | AMF-Test | Enterprise-AMF | High-Assurance-AMF
  non_compatibility_statement: string
  build_artifacts:
    - artifact_id: string
      digest: sha384
  requirement_status:
    - requirement_id: string
      status: SATISFIED | PARTIAL | UNSUPPORTED | SPEC_GAP | NOT_APPLICABLE | BLOCKED
      evidence_refs:
        - string
  production_gates:
    - gate_id: string
      status: PASS | FAIL | NOT_APPLICABLE
      evidence_refs:
        - string
  unsupported_features:
    - feature: string
      failure_mode: string
      tests:
        - string
  spec_gaps:
    - gap_id: string
      description: string
      blocked_claims:
        - string
  review_records:
    - string
  sbom_ref: string?
  provenance_ref: string?
  attestation_ref: string?
```

## 14. Review Checklists

### 13.1 Profile Review

- Claimed profile is explicit.
- Higher-profile features are marked optional unless all profile requirements pass.
- Unsupported features fail closed.
- SPEC_GAP items are not implemented as success.
- Production gates are not conflated with draft conformance.

### 13.2 Evidence Review

- Requirements status matrix exists.
- Every SATISFIED security requirement has tests.
- Every security requirement has negative tests.
- Every parser has fuzz target registration.
- Audit obligations are tested.
- CI reports are attached.
- Supply-chain artifacts exist when required.

### 13.3 Release Wording Review

- No z/OS compatibility claim.
- No IBM product compatibility claim.
- No overclaim of PKU/PKS.
- No Baseline claim of Guard protection.
- No High-Assurance claim without Guard evidence.
- No production claim without gate evidence.

## 15. Spec Gaps

- Exact conformance report file path is not fixed.
- Machine-readable requirement registry is not yet defined.
- External certification mapping is not defined.
- Formal proof acceptance criteria are not fully defined.
- Hardware feature matrix rules need platform-specific profiles.
- Versioning rules for conformance statements are not fixed.
