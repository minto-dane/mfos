---
spec_id: "MFOS-SPEC-00-NORMATIVE-LANGUAGE"
title: "MFOS Normative Language and Conformance Profiles v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001", "EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001", "EXTREF-IBM-ZOS-JES-INTRODUCTION-0001", "EXTREF-IBM-Z-LPAR-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001", "MS-VBS-001", "MS-VSM-001", "NIST-160-001", "NIST-193-001", "NIST-218-001", "SEL4-001", "SLSA-001", "TCG-001", "TUF-001", "X64-AMD-001", "X64-INTEL-001", "X64-LINUX-CET-001", "X64-LINUX-PKU-001"]
requirement_refs: ["MFOS-REQ-AI-*", "MFOS-REQ-LANG-*", "MFOS-REQ-PROFILE-*", "MFOS-REQ-QUALITY-*", "MFOS-REQ-SOURCE-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Normative Language and Conformance Profiles v0.1

Status: Draft specification

## 1. Purpose

This document defines the normative language, conformance profiles, claim rules, evidence rules, and AI implementation contract used by MFOS specifications.

MFOS is an x64-native, source-grounded, z/OS-inspired enterprise operating system design. MFOS does not claim z/OS compatibility, z/Architecture compatibility, IBM API compatibility, or IBM product compatibility.

This document exists so implementation agents can distinguish:

- required behavior from optional behavior
- unsupported features from specification gaps
- baseline system integrity from High-Assurance Guard claims
- source-grounded concepts from internal MFOS design choices
- implementation evidence from informal status reports

## 2. Scope

This specification applies to all MFOS design, implementation, testing, review, and release artifacts.

In scope:

- normative terms
- conformance profile definitions
- source matrix use
- requirement ID use
- verification method vocabulary
- failure and error claim rules
- no-fake-success rule
- AI output obligations
- profile-specific evidence obligations
- rules for z/OS-inspired wording
- canonical language and localization synchronization rules

## 3. Non-objectives

MFOS specifications must not use this document to claim:

- z/OS compatibility
- z/Architecture emulation
- RACF compatibility
- JES2 or JES3 compatibility
- DFSMS compatibility
- z/OS UNIX compatibility
- Windows VBS compatibility
- seL4-equivalent formal verification
- production readiness without evidence
- High-Assurance conformance without PXM Guard evidence

## 4. Source Matrix IDs

This document depends on the following source families.

| Source ID | Use |
| --- | --- |
| EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001 | System integrity wording and unauthorized program boundary inspiration |
| EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001 | Authorized program and authorized state concept mapping |
| EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001 | Authorized boundary negative-test discipline |
| EXTREF-IBM-ZOS-SECURITY-SERVER-0001 | Security manager source family |
| EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | Audit/accounting source family |
| EXTREF-IBM-ZOS-JES-INTRODUCTION-0001 | Job/spool source family |
| EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001 | Dataset/catalog source family |
| EXTREF-IBM-Z-LPAR-INTRODUCTION-0001 | Partition concept inspiration |
| X64-INTEL-001 | Intel x64 system programming reality |
| X64-AMD-001 | AMD64 system programming reality |
| X64-LINUX-PKU-001 | PKU limitation reference |
| X64-LINUX-CET-001 | CET reference |
| MS-VBS-001 | VBS-like high-assurance reference only |
| MS-VSM-001 | VTL/VSM-like Guard reference only |
| TCG-001 | Measured boot and TPM reference |
| NIST-160-001 | System security engineering reference |
| NIST-218-001 | Secure development practice reference |
| NIST-193-001 | Firmware resiliency reference |
| SEL4-001 | Formal assurance boundary reference |
| SLSA-001 | Supply-chain provenance reference |
| TUF-001 | Update metadata and rollback/freeze protection reference |
| FBVBS-001 | Internal assurance discipline transfer source |

Rules:

- A z/OS-inspired concept in any MFOS spec MUST cite at least one IBM source matrix ID.
- An x64 hardware protection claim MUST cite an x64 source matrix ID.
- A VBS-like or VSM-like claim MUST be scoped to PXM Guard or High-Assurance profile unless an architecture review explicitly permits narrower use.
- FBVBS-001 MAY define MFOS assurance discipline, traceability structure, and evidence style, but MUST NOT be treated as a source for IBM semantics.

## 5. Normative Terms

The terms in this section are normative.

| Term | Meaning |
| --- | --- |
| MUST | Required for every implementation claiming the applicable profile. |
| MUST NOT | Prohibited. Implementations violating this cannot claim conformance. |
| REQUIRED | Equivalent to MUST. |
| SHALL | Equivalent to MUST. |
| SHALL NOT | Equivalent to MUST NOT. |
| SHOULD | Strongly recommended. A deviation requires an ADR, rationale, risk assessment, and test/evidence impact. |
| SHOULD NOT | Strongly discouraged. A deviation requires the same evidence as SHOULD. |
| MAY | Optional. The feature is permitted but does not automatically extend the assurance claim. |
| OPTIONAL | Equivalent to MAY. |
| RECOMMENDED | Equivalent to SHOULD. |
| PROHIBITED | Equivalent to MUST NOT. |
| NON-OBJECTIVE | Deliberately outside scope. Absence is not a defect. |
| UNSUPPORTED | The spec defines the behavior, but the current implementation does not implement it. The implementation MUST fail closed with a typed error. |
| SPEC_GAP | The spec does not define the behavior. The implementation MUST NOT invent behavior. |
| FAIL-CLOSED | The operation must deny, stop, or enter recovery without granting the requested authority or resource. |
| FAIL-SECURE | The system must preserve the protected security property before availability. |
| EVIDENCE REQUIRED | A claim is invalid until backed by tests, review records, proof artifacts, attestation, provenance, or other named evidence. |

The RFC 2119 family of words is intentionally mapped here in MFOS terms rather than relying on external style by implication.

### 5.1 Canonical Language

English is the canonical language for MFOS normative specifications.

Machine-readable artifacts MUST use English keys, IDs, enum names, error codes, ABI names, profile names, state names, status values, and ABI identifiers.

Japanese documents are auxiliary mirror and review material. Japanese text MAY clarify intent, rationale, examples, and review notes, but MUST NOT override, narrow, extend, weaken, or strengthen English normative requirements.

If English canonical text and Japanese mirror text conflict, the English canonical text wins. The conflicting Japanese translation unit MUST be marked stale or blocked until corrected from the current English canonical source.

Complete Japanese documentation MUST be synchronized by translation unit IDs, source hash checks, and language lint rules. The detailed mechanism is defined in `docs/design/specs/32-language-localization.md`.

## 6. Conformance Profiles

MFOS has four conformance profiles:

- Baseline
- Enterprise-Standalone
- Enterprise-PXM
- High-Assurance

### 6.1 Baseline

Purpose:

- development
- small deployments
- hosted semantic prototypes
- early nucleus bring-up

Baseline focuses on MFOS enterprise semantics:

- central authorization
- mandatory audit obligations
- job/dataset/catalog/spool/operator object model
- no fake success
- typed SVC/PCALL boundaries where applicable
- NX-capable platform required once a nucleus exists
- W^X policy required once executable mappings exist
- AMF specification present but AMF production load disabled

Baseline MAY run as an implicit single partition.

Baseline conformance MUST NOT be claimed if the nucleus runs on an x64 platform where NX is unavailable, disabled, or not enforceable by MFOS. W^X is an OS policy requirement, not a best-effort hardware feature. SMEP and SMAP remain profile-dependent hardening mechanisms when supported.

Baseline AMF mode is `Baseline-AMF-Disabled`: AMF load requests MUST return `MFOS_ERR_UNSUPPORTED` outside an explicitly non-production AMF test profile.

Baseline MUST NOT claim:

- Guard root protection
- resistance after authorized module compromise
- production-grade device passthrough assurance
- remote attestation completeness
- High-Assurance conformance
- production AMF module load support

### 6.2 Enterprise-Standalone

Purpose:

- production-oriented enterprise deployment
- measured boot
- remote audit export
- stronger update governance
- implicit single-partition operation

Enterprise-Standalone includes Baseline and adds:

- Secure Boot required
- Measured Boot required
- TPM required
- IOMMU required for platform DMA protection
- remote audit export required unless explicitly profiled out
- TUF-like update metadata required
- SBOM and signed provenance required
- dependency allowlist required
- no cross-partition device assignment claim
- no side-partition isolation claim
- no PXM passthrough production claim

Enterprise-Standalone does not require PXM. It MUST NOT claim partition lifecycle isolation, side-partition isolation, or cross-partition device assignment. AMF production load remains disabled unless the release separately claims `Enterprise-AMF`.

### 6.3 Enterprise-PXM

Purpose:

- production-oriented enterprise deployment with partition lifecycle claims
- side-partition isolation claims
- device assignment only after teardown evidence

Enterprise-PXM includes Enterprise-Standalone and adds:

- PXM required
- IOMMU required
- interrupt remapping required
- partition lifecycle claims allowed
- side-partition claims allowed
- device assignment claims allowed only after teardown tests and evidence
- partition audit required

Enterprise-PXM MAY use PXM Guard as a measurement helper, but Guard is not mandatory unless claiming a High-Assurance property.

### 6.4 High-Assurance

Purpose:

- critical infrastructure
- maximum evidence profile
- selected root object protection after partial OS compromise

High-Assurance adds:

- PXM required
- PXM Guard required
- Guard-sealed audit root required
- Guard-sealed security policy root required
- Guard involvement for AMF registry required
- remote attestation required
- SMEP/SMAP required by platform profile
- formal model coverage required for core state machines
- independent review required for TCB changes
- production proof obligations required before any production claim

High-Assurance MUST keep Guard scope small. Guard MUST protect selected root objects and MUST NOT implement job scheduling, dataset policy interpretation, spool rendering, or operator business semantics.

## 7. Profile Capability Matrix

| Capability | Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance |
| --- | --- | --- | --- | --- |
| z/OS-inspired semantics | MUST | MUST | MUST | MUST |
| z/OS compatibility claim | MUST NOT | MUST NOT | MUST NOT | MUST NOT |
| Source Matrix refs | MUST | MUST | MUST | MUST |
| Requirement IDs | MUST | MUST | MUST | MUST |
| securityd | MUST | MUST | MUST | MUST |
| auditd | MUST | MUST | MUST | MUST |
| audit hash chain | SHOULD | MUST | MUST | MUST |
| remote audit export | MAY | MUST | MUST | MUST |
| PXM | MAY as implicit backend | MUST NOT be required | MUST | MUST |
| PXM Guard | MUST NOT be required | MUST NOT be required | MAY | MUST |
| Secure Boot | SHOULD | MUST | MUST | MUST |
| Measured Boot | MAY | MUST | MUST | MUST |
| TPM | MAY | MUST | MUST | MUST |
| IOMMU | SHOULD for DMA protection | MUST for platform DMA protection | MUST | MUST |
| interrupt remapping | SHOULD when supported | SHOULD when supported | MUST | MUST |
| cross-partition device assignment claim | MUST NOT | MUST NOT | MAY with teardown evidence | MAY with teardown and Guard-scope evidence |
| NX-capable platform | MUST | MUST | MUST | MUST |
| W^X policy | MUST | MUST | MUST | MUST |
| SMEP/SMAP | SHOULD when available | MUST when supported by platform profile | MUST when supported by platform profile | MUST by platform profile |
| CET | SHOULD when available | SHOULD for trusted services | SHOULD for trusted services | SHOULD or MUST by platform profile |
| PKU | MAY for compartments | MAY for compartments | MAY for compartments | MAY for compartments |
| PKU as integrity root | MUST NOT | MUST NOT | MUST NOT | MUST NOT |
| PKS as Guard replacement | MUST NOT | MUST NOT | MUST NOT | MUST NOT |
| AMF production load | MUST NOT | MUST NOT unless Enterprise-AMF claimed | MUST NOT unless Enterprise-AMF claimed | MUST with Guard approval if AMF is in scope |
| AMF test profile | MAY | MAY | MAY | MAY |
| AMF revocation | SHOULD in spec only | MUST for Enterprise-AMF | MUST for Enterprise-AMF | MUST |
| AMF Guard approval | MUST NOT be required | MUST NOT be required | MAY only as helper | MUST |
| TUF-like updates | SHOULD | MUST | MUST | MUST |
| SBOM/provenance | SHOULD | MUST | MUST | MUST |
| formal methods | SHOULD for state machines | SHOULD for security paths | SHOULD for security and PXM paths | MUST for core and Guard paths |

## 8. Claim Rules

### 8.1 Compatibility Claims

MFOS artifacts MUST use allowed wording:

- z/OS-inspired
- IBM-concept-mapped
- source-grounded enterprise semantics
- RACF-inspired security manager
- JES-inspired job/spool subsystem
- DFSMS-inspired dataset/catalog model
- SMF-inspired audit model
- LPAR-inspired partition model

MFOS artifacts MUST NOT use prohibited wording:

- z/OS compatible
- RACF compatible
- JES2 compatible
- DFSMS compatible
- z/Architecture compatible
- z/OS clone
- IBM-compatible OS
- runs z/OS binaries
- implements RACF
- implements JES2
- implements DFSMS

### 8.2 Hardware Claims

Hardware features MUST be described as enforcement mechanisms or implementation aids, not as semantic roots.

PKU and PKS MUST NOT be described as:

- z/OS storage key compatibility
- complete storage-key replacement
- system integrity root
- audit root protection
- Guard replacement

CET MAY be described as a control-flow hardening mechanism when supported by the platform profile.

### 8.3 Assurance Claims

An assurance claim MUST name:

- profile
- protected asset
- threat boundary
- source matrix IDs
- requirement IDs
- implementation artifacts
- tests
- negative tests
- evidence artifacts
- residual risks

No implementation may claim production readiness until the production readiness gate is satisfied.

## 9. Requirement IDs

All normative requirements MUST have stable IDs.

Requirement ID format:

```text
MFOS-REQ-<AREA>-<NNNN>
```

Reserved areas:

| Area | Meaning |
| --- | --- |
| SRC | Source grounding |
| PROF | Conformance profile |
| GLOSS | glossary and terminology control |
| SI | System integrity |
| SEC | securityd |
| AUD | auditd |
| CAT | catalogd |
| DATA | datasetd |
| JOB | jobd |
| SPL | spoold |
| OPER | operatord |
| workload policy | workpolicyd |
| AMF | Authorized Module Facility |
| UVS | Update Verification Service |
| NUC | nucleus |
| ABI | SVC/PCALL ABI |
| PXM | Partition Manager |
| GRD | Guard |
| AI | AI implementation contract |
| QUAL | quality and supply chain |
| LANG | language policy and localization synchronization |

Rules:

- Code in production paths MUST reference applicable requirement IDs.
- Security-sensitive changes MUST include negative tests linked to requirement IDs.
- A new z/OS-inspired requirement MUST cite a Source Matrix ID.
- A requirement with no verification method is incomplete.

## 10. Verification Methods

Allowed verification method labels:

- inspection
- documentation review
- architecture review
- interface test
- unit test
- integration test
- negative test
- fuzz test
- crash test
- fault injection
- state-machine test
- model check
- proof review
- traceability audit
- release review
- supply-chain audit
- operator drill
- recovery drill
- attestation review
- source-matrix lint
- spec lint
- automated lint
- no-fake-success CI
- CI gate
- review checklist
- language lint
- semantic lint

Each requirement MUST list at least one verification method.

## 11. Protected Resources

This document defines the global protected-resource categories used by all specs.

| Resource | Protected because |
| --- | --- |
| PRINCIPAL | Identity and authority root |
| GROUP | Authority aggregation |
| ROLE | Operational authority aggregation |
| PROGRAM_IDENTITY | Executable identity and measurement |
| AUTHORIZED_MODULE | Extension authority boundary |
| SECURITY_PROFILE | Access policy |
| SECURITY_POLICY_ROOT | Policy trust root |
| AUDIT_RECORD | Evidence object |
| AUDIT_CHAIN_ROOT | Audit integrity root |
| DATASET | Managed enterprise data resource |
| CATALOG_ENTRY | Dataset name, metadata, and location authority |
| VOLUME | Storage allocation and containment object |
| SPOOL_ENTRY | Job input/output evidence and output resource |
| JOB | Unit of work and accounting |
| JOB_STEP | Executable step and return-code unit |
| OPERATOR_COMMAND | System interface with authority and audit |
| WORKLOAD_POLICY | Scheduling and resource governance |
| AMF_REGISTRY | Authorized module root |
| UPDATE_ARTIFACT | Executable or policy update input |
| UPDATE_METADATA | Update trust metadata |
| PARTITION | Isolation and lifecycle object |
| ACTIVATION_PROFILE | Partition configuration object |
| DEVICE_ASSIGNMENT | DMA/interrupt/resource ownership object |
| GUARD_ROOT | High-Assurance root object |

Protected resources MUST NOT be manipulated through untyped handles or caller-supplied identity claims.

## 12. System Interfaces

System interfaces are all entry points that can affect protected resources or authority.

Global system interface categories:

- SVC
- PCALL
- PXM_CALL
- GUARD_CALL
- operator command
- dataset open
- catalog transaction
- job submit
- job cancel
- spool browse
- spool purge
- security policy update
- audit query
- AMF load
- update activation
- device assignment
- partition lifecycle transition

Rules:

- A system interface MUST have a stable interface ID.
- A system interface MUST define its caller identity source.
- A system interface MUST reject caller-supplied effective identity unless the spec explicitly defines delegation.
- A system interface MUST define audit obligations.
- A system interface MUST distinguish UNSUPPORTED from SPEC_GAP.

## 13. Failure and Error Rules

MFOS implementations MUST use typed failure results.

Canonical result classes:

```text
MFOS_OK
MFOS_ERR_UNAUTHENTICATED
MFOS_ERR_UNAUTHORIZED
MFOS_ERR_POLICY_DENIED
MFOS_ERR_POLICY_VERSION_MISMATCH
MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE
MFOS_ERR_UNSUPPORTED
MFOS_ERR_SPEC_GAP
MFOS_ERR_INVALID_PARAMETER
MFOS_ERR_INVALID_DSN
MFOS_ERR_CATALOG_NOT_FOUND
MFOS_ERR_DATASET_LOCKED
MFOS_ERR_IMMUTABLE
MFOS_ERR_STALE_HANDLE
MFOS_ERR_AMF_SIGNATURE_INVALID
MFOS_ERR_AMF_REVOKED
MFOS_ERR_GUARD_REQUIRED
MFOS_ERR_GUARD_DENIED
MFOS_ERR_PARTITION_INVALID_STATE
MFOS_ERR_DEVICE_TEARDOWN_INCOMPLETE
MFOS_ERR_ROLLBACK_DETECTED
MFOS_ERR_FREEZE_DETECTED
MFOS_ERR_MIX_AND_MATCH_DETECTED
MFOS_ERR_INTERNAL_CORRUPTION
```

Rules:

- Unsupported implemented-as-success is prohibited.
- Undefined implemented-as-success is prohibited.
- Silent fallback from a protected operation to a weaker operation is prohibited.
- Audit-required operations MUST NOT complete successfully if their audit obligation cannot be satisfied.
- DENY decisions MUST be auditable before the caller receives a final result unless the profile-specific audit-failure policy explicitly enters recovery.

## 14. Invariants

INV-NORM-001:

Every normative MFOS requirement has a stable requirement ID, source references where applicable, and verification method.

INV-NORM-002:

No MFOS artifact claims z/OS compatibility or IBM product compatibility.

INV-NORM-003:

A system interface cannot return success for an unsupported or specification-gap operation.

INV-NORM-004:

A protected-resource operation cannot be implemented without an authorization rule and audit obligation.

INV-NORM-005:

High-Assurance claims cannot exist without PXM Guard scope, Guard root definition, tests, and evidence.

INV-NORM-006:

Hardware features are implementation mechanisms; they do not replace MFOS object-model authorization.

## 15. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-PROFILE-0001 | MFOS MUST define conformance as Baseline, Enterprise-Standalone, Enterprise-PXM, or High-Assurance. | documentation review |
| MFOS-REQ-PROFILE-0002 | Each conformance claim MUST name exactly one minimum profile. | release review |
| MFOS-REQ-PROFILE-0003 | Higher profile features MAY be implemented in lower profiles but MUST NOT be used to imply higher-profile conformance. | release review |
| MFOS-REQ-PROFILE-0004 | High-Assurance conformance MUST require PXM Guard. | architecture review |
| MFOS-REQ-PROFILE-0005 | Baseline conformance MUST require an NX-capable platform and W^X policy once a nucleus exists. | platform review / W^X negative test |
| MFOS-REQ-PROFILE-0006 | Enterprise-Standalone MUST NOT claim cross-partition device assignment, side-partition isolation, or PXM passthrough production. | release review |
| MFOS-REQ-PROFILE-0007 | Enterprise-PXM MUST require PXM, IOMMU, interrupt remapping, partition audit, and teardown evidence for device assignment claims. | PXM evidence review |
| MFOS-REQ-PROFILE-0008 | Baseline and Phase 1/2 implementations MUST return `MFOS_ERR_UNSUPPORTED` for AMF load unless running an explicitly non-production AMF test profile. | AMF negative test |
| MFOS-REQ-LANG-0001 | MFOS normative specifications MUST use English as the canonical language. | documentation review / spec lint |
| MFOS-REQ-LANG-0002 | Japanese documents MUST be auxiliary mirrors and MUST NOT override English canonical semantics. | documentation review / language lint |
| MFOS-REQ-LANG-0003 | Machine-readable keys, IDs, enum values, state names, ABI names, and error codes MUST remain English. | automated lint |
| MFOS-REQ-LANG-0004 | Japanese mirrors MUST use translation unit IDs and source hashes to track synchronization status. | language lint |
| MFOS-REQ-LANG-0005 | Japanese semantic corrections MUST be made by first patching English canonical content. | review checklist |
| MFOS-REQ-SOURCE-0001 | z/OS-inspired concepts MUST cite Source Matrix IDs. | source-matrix lint |
| MFOS-REQ-SOURCE-0002 | IBM terms reused as MFOS terms MUST document overlap and divergence. | documentation review |
| MFOS-REQ-SOURCE-0003 | MFOS MUST NOT claim z/OS compatibility. | release review |
| MFOS-REQ-SOURCE-0004 | IBM-source behavior not represented in MFOS MUST be documented as divergence or non-objective. | architecture review |
| MFOS-REQ-AI-0001 | AI-generated implementation output MUST list requirement IDs. | review checklist |
| MFOS-REQ-AI-0002 | AI-generated implementation output MUST list source matrix IDs for source-grounded concepts. | source-matrix lint |
| MFOS-REQ-AI-0003 | AI-generated output MUST list assumptions, spec gaps, unsupported features, invariants, audit obligations, and tests. | review checklist |
| MFOS-REQ-AI-0004 | AI-generated production-path code MUST NOT use fake success, empty stubs, or silent fallbacks. | no-fake-success CI |
| MFOS-REQ-QUALITY-0001 | Requirements, design, code, tests, and evidence MUST maintain bidirectional traceability. | traceability audit |
| MFOS-REQ-QUALITY-0002 | Security-sensitive PRs MUST include at least one negative test or a documented reason why no negative test is applicable. | CI gate |
| MFOS-REQ-QUALITY-0003 | TCB changes SHOULD require independent review in Baseline and MUST require it in Enterprise-Standalone, Enterprise-PXM, and High-Assurance. | review audit |
| MFOS-REQ-QUALITY-0004 | Production claims MUST be blocked until production readiness gates are satisfied. | release review |

## 16. Positive Tests

PT-NORM-001:

A spec containing an IBM-derived concept and a valid Source Matrix ID passes source-matrix lint.

PT-NORM-002:

A Baseline conformance statement that names required Baseline capabilities and excludes Guard claims passes profile lint.

PT-NORM-003:

An unsupported but specified operation returns `MFOS_ERR_UNSUPPORTED`.

PT-NORM-004:

A spec gap operation returns `MFOS_ERR_SPEC_GAP` or is rejected at build/spec lint time.

PT-NORM-005:

AI output containing requirement IDs, source IDs, assumptions, gaps, obligations, and tests passes output-format lint.

## 17. Negative Tests

NT-NORM-001:

A document containing "z/OS compatible" as a claim fails release lint.

NT-NORM-002:

A z/OS-inspired concept without an IBM Source Matrix ID fails source-matrix lint.

NT-NORM-003:

A protected-resource operation with no audit obligation fails spec lint.

NT-NORM-004:

A production path containing `todo!()`, `unimplemented!()`, fake success, or placeholder success fails no-fake-success CI.

NT-NORM-005:

A High-Assurance claim without Guard evidence fails release review.

NT-NORM-006:

A PKU/PKS statement claiming storage-key compatibility fails architecture review.

## 18. Fuzz Targets

No runtime parser is defined by this document.

Required lint/fuzz-like checks:

- `source_matrix_ref_lint`: randomly removes or mutates source IDs in sample specs and verifies failures.
- `claim_wording_lint`: mutates prohibited compatibility phrases and verifies detection.
- `requirement_id_lint`: mutates requirement ID formats and verifies detection.
- `ai_output_contract_lint`: mutates required AI output sections and verifies detection.

## 19. Spec Gaps

SPEC-GAP-NORM-001:

The exact machine-readable schema for requirements is not defined yet.

SPEC-GAP-NORM-002:

The final no-fake-success scanner implementation language and CI runner are not defined yet.

SPEC-GAP-NORM-003:

The complete production readiness evidence bundle format is not defined yet.

SPEC-GAP-NORM-004:

The exact policy for mixed-profile deployments is not defined yet.

SPEC-GAP-NORM-005:

The language synchronization manifest and language lint implementation are not defined in executable form yet.

## 20. AI Prompt

Use this prompt when asking an AI agent to modify MFOS specifications or implementation based on this document:

```text
You are working on MFOS, an x64-native, source-grounded, z/OS-inspired enterprise OS design.

Do not claim z/OS compatibility or IBM product compatibility.

For every change:
- list implemented requirement IDs
- list Source Matrix IDs for source-grounded concepts
- state profile applicability: Baseline, Enterprise-Standalone, Enterprise-PXM, High-Assurance
- distinguish UNSUPPORTED from SPEC_GAP
- define protected resources and system interfaces affected
- preserve authorization and audit obligations
- add positive tests and negative tests
- add fuzz targets for parsers
- avoid fake success, empty stubs, and silent fallback
- document assumptions, residual risks, and evidence artifacts

If the spec does not define behavior, return SPEC_GAP instead of inventing semantics.
```
