---
spec_id: "MFOS-SPEC-04-THREAT-MODEL"
title: "MFOS Threat Model Specification v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001", "EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001", "EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001", "EXTREF-IBM-Z-DPM-0001", "EXTREF-IBM-ZOS-JES-INTRODUCTION-0001", "EXTREF-IBM-ZOS-JES-JOB-FLOW-0001", "EXTREF-IBM-ZOS-JES2-LIBRARY-0001", "EXTREF-IBM-Z-LPAR-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001", "EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001", "EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001", "EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001", "EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001", "EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001", "EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001", "MS-VBS-001", "MS-VSM-001", "NIST-160-001", "NIST-193-001", "NIST-218-001", "SEL4-001", "SLSA-001", "TCG-001", "TUF-001", "X64-AMD-001", "X64-INTEL-001", "X64-LINUX-CET-001", "X64-LINUX-PKU-001"]
requirement_refs: ["MFOS-REQ-THR-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Threat Model Specification v0.1

Status: Draft design split

Owned area: `docs/design/specs/04-threat-model.md`

Audience: architecture agents, implementation agents, security reviewers, test engineers, formal methods engineers

MFOS is z/OS-inspired and source-grounded. MFOS does not claim z/OS, z/Architecture, RACF, JES, DFSMS, SMF, workload policy, APF, PR/SM, Windows VBS, or Linux compatibility.

## 1. Purpose

This document defines the MFOS threat model for the source-grounded enterprise OS design. It ties assets, actors, trust boundaries, abuse cases, mitigations, audit obligations, fail-closed conditions, invariants, tests, fuzz targets, and residual risks to the existing MFOS design split.

The threat model exists to prevent:

- Unauthorized access to datasets, catalogs, spool entries, jobs, operator commands, update artifacts, audit streams, AMF modules, partitions, devices, and Guard roots.
- System interfaces that permit bypass of `securityd`, `auditd`, typed handles, SVC/PCALL validation, or profile-specific Guard approval.
- Treating x64 hardware features as substitutes for MFOS authorization semantics.
- Treating audit as ordinary logging.
- Treating operator console commands as a root shell.
- Treating PXM as an enterprise policy engine.
- Treating Guard as a job, dataset, or business-policy interpreter.
- Claiming High-Assurance protection without Guard evidence.
- Fake success, silent fallback, or implementation of undefined behavior.

## 2. Scope

In scope:

- Baseline, Enterprise-Standalone, Enterprise-PXM, and High-Assurance profiles.
- MFOS nucleus, SVC, PCALL, typed handles, copy-in/copy-out, and service lifecycle.
- `securityd`, `auditd`, `catalogd`, `datasetd`, `jobd`, `spoold`, `operatord`, `workpolicyd`, `amfd`, and `uvsd`.
- PXM Core and implicit single-partition backend.
- PXM Guard for High-Assurance root objects.
- Optional POSIX subsystem and side-partition gateway risks.
- Update, boot, measured boot, supply chain, and recovery threats at the design level.
- AI implementation risks: hallucinated concepts, missing Source Matrix IDs, missing audit obligations, and no-fake-success violations.

Out of scope:

- z/OS compatibility threat claims.
- Exact IBM product security behavior.
- Exact Windows VBS/VSM behavior.
- Full cryptographic algorithm selection.
- Full formal proof.
- Physical side-channel resistance beyond residual risk tracking.
- Nation-state hardware implant prevention.
- Desktop application threat model inside a side partition.
- Full remote management plane protocol design.

## 3. Source Matrix References

| Source ID | Threat-model use |
| --- | --- |
| `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001` | System integrity source for unauthorized subjects not bypassing protection, security checks, or authorized state. |
| `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001` | Authorized-boundary negative testing for SVC, PCALL, AMF, and privileged parameter handling. |
| `EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001` | AMF/APF-inspired authorized module boundary and authority confusion threats. |
| `EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001`, `EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001` | Storage protection concepts mapped to MFOS storage domains with x64 divergence. |
| `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001` | Security manager, resource profile, access-list, and protected resource threats. |
| `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-JES-JOB-FLOW-0001`, `EXTREF-IBM-ZOS-JES2-LIBRARY-0001` | Job, queue, initiator, SYSIN/SYSOUT, and spool threats. |
| `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001` | Dataset and catalog naming, location, attributes, and managed resource threats. |
| `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001` | Audit/accounting evidence and security event threats. |
| `EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001` | Service class, workload policy, and dispatch hint misuse threats. |
| `EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001`, `EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001` | PCALL/cross-address-space authority and pointer-trust threats. |
| `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `EXTREF-IBM-Z-DPM-0001` | Partition lifecycle, activation profile, and management-plane threats. |
| `X64-INTEL-001`, `X64-AMD-001` | x64 paging, VMX/SVM, interrupt, IOMMU, executable mapping, and privilege boundary threats. |
| `X64-LINUX-PKU-001`, `X64-LINUX-CET-001` | PKU/CET limitations and overclaim threats. |
| `MS-VBS-001`, `MS-VSM-001` | Informative Guard isolation threats for High-Assurance only. |
| `TCG-001` | Measured boot, TPM event-log, and attestation threats. |
| `NIST-160-001`, `NIST-193-001`, `NIST-218-001` | Secure systems engineering, firmware resiliency, and secure development threats. |
| `TUF-001`, `SLSA-001` | Update metadata, rollback, freeze, mix-and-match, provenance, and build integrity threats. |
| `SEL4-001` | Assurance-boundary and proof-assumption discipline. |
| `FBVBS-001` | Requirements/evidence traceability, state-machine discipline, production proof obligations, no fake success. |

## 4. Non-Compatibility Statement

MFOS threat claims are MFOS claims. They are source-grounded, not compatibility claims.

Allowed wording:

- "MFOS system integrity is inspired by IBM-documented system integrity concepts."
- "MFOS jobs and spool are JES-inspired at the lifecycle level."
- "MFOS datasets and catalogs are DFSMS-inspired at the managed-resource level."
- "MFOS audit is SMF-inspired at the evidence and accounting level."
- "PXM is LPAR/DPM-inspired at the partition-management concept level."
- "PXM Guard uses VBS/VSM-like isolation concepts as informative High-Assurance input."

Prohibited wording:

- "MFOS is z/OS-compatible."
- "MFOS implements RACF, JES, DFSMS, SMF, workload policy, APF, or PR/SM."
- "MFOS provides z/OS storage key compatibility on x64."
- "MFOS Guard is Windows VBS-compatible."
- "PKU, PKS, CET, SMEP, SMAP, IOMMU, VMX, or SVM proves MFOS authorization."

## 5. Threat Modeling Method

MFOS uses a domain-specific threat model layered over STRIDE-like categories.

Generic categories:

- Spoofing.
- Tampering.
- Repudiation.
- Information disclosure.
- Denial of service.
- Elevation of privilege.

MFOS-specific categories:

- System-interface bypass.
- Authorized-state confusion.
- Caller-supplied identity trust.
- Dataset handle forgery or staleness.
- Catalog generation confusion.
- Spool disclosure or purge bypass.
- Job effective-principal confusion.
- Operator/root-shell confusion.
- Audit suppression, delay, truncation, or downgrade.
- AMF/admin privilege confusion.
- Update rollback, freeze, mix-and-match, or revoked signer acceptance.
- PXM/MFOS responsibility confusion.
- Guard scope inflation.
- Cross-partition leakage, DMA leakage, and interrupt-route leakage.
- Hardware feature overclaim.
- Semantic misuse of valid authority.
- Overbroad policy grants and unsafe operational delegation.
- AI hallucinated semantics, missing Source Matrix IDs, and fake success.

## 6. Security Objectives

| ID | Objective |
| --- | --- |
| `THR-OBJ-0001` | Unauthorized subjects cannot use MFOS system interfaces to bypass protected-resource policy. |
| `THR-OBJ-0002` | `securityd` remains the policy decision point for protected resource access. |
| `THR-OBJ-0003` | Required audit evidence is produced before security-sensitive results are returned. |
| `THR-OBJ-0004` | Dataset, catalog, spool, job, operator, AMF, update, partition, and Guard root operations are typed and generation-aware where required. |
| `THR-OBJ-0005` | Unsupported and unspecified behavior fails closed and cannot return success. |
| `THR-OBJ-0006` | PXM isolates partitions without interpreting MFOS enterprise semantics. |
| `THR-OBJ-0007` | Guard protects only selected High-Assurance roots and does not grow into an enterprise policy engine. |
| `THR-OBJ-0008` | Update and build integrity cannot be replaced by transport security or informal operator trust. |
| `THR-OBJ-0009` | AI-generated work remains traceable to requirement IDs, Source Matrix IDs, tests, and evidence. |

## 7. Assets

### 7.1 Identity and Policy Assets

| Asset | Security properties |
| --- | --- |
| `Principal` | Authenticity, status correctness, group/role integrity, emergency flags integrity. |
| `ProgramIdentity` | Digest correctness, signer binding, catalog generation binding, authority-class correctness. |
| `SecurityProfile` | Access rule integrity, default access correctness, audit-rule correctness. |
| Security policy root | Version integrity, transaction integrity, rollback resistance, auditability. |
| Authentication context | Freshness, auth strength, expiry, non-spoofability. |

### 7.2 Enterprise Resource Assets

| Asset | Security properties |
| --- | --- |
| `Dataset` | Confidentiality, integrity, retention, owner binding, catalog binding, policy binding. |
| `CatalogEntry` | DSN resolution integrity, generation correctness, location integrity, immutable/system flags. |
| `DatasetHandle` | Subject binding, operation binding, policy version binding, catalog generation binding, expiry. |
| `Job` | Submitter integrity, effective principal correctness, lifecycle correctness, accounting integrity. |
| `JobStep` | Program identity, DD resolution, return-code correctness, resource closure. |
| `SpoolEntry` | Owner binding, job binding, output class, retention, browse/purge/export authorization. |
| `WorkloadPolicy` | Active policy version, class limits, dispatch hints, overload behavior. |

### 7.3 System Control Assets

| Asset | Security properties |
| --- | --- |
| MFOS nucleus text/data | W^X, NX, typed handles, SVC dispatch integrity, page-table integrity. |
| SVC table | Entry integrity, dispatch versioning, unsupported/spec-gap separation. |
| PCALL endpoints | Endpoint type integrity, request bounds, identity propagation. |
| AMF registry | Signed module identity, authority class, revocation state, Guard sealing in High-Assurance. |
| Update metadata | Root/timestamp/snapshot/targets consistency, freshness, security epoch, signatures. |
| Activation profile | Measurement binding, CPU/memory/device constraints, profile version. |

### 7.4 Evidence and Recovery Assets

| Asset | Security properties |
| --- | --- |
| `AuditRecord` | Schema validity, sequence monotonicity, hash-chain continuity, timestamp and subject correctness. |
| Audit stream | Append-only behavior, retention, tamper detection, export integrity. |
| Guard audit root | High-Assurance root digest, version, measurement context. |
| Recovery partition state | Trustworthy recovery action, rollback constraints, forensics preservation. |
| Crash and fault records | Integrity, non-suppression, correlation to triggering operation. |

### 7.5 Partition and Hardware Assets

| Asset | Security properties |
| --- | --- |
| Partition memory | Isolation, zero before reuse, page-table binding. |
| Device assignment | IOMMU domain correctness, interrupt remapping, teardown completeness. |
| DMA-capable devices | Containment, ownership, teardown audit. |
| TPM event log | Measurement integrity, quote freshness, boot-chain evidence. |
| Firmware | Protected, detected, recoverable per profile capability. |

## 8. Actors

| Actor | Capability | Trust position |
| --- | --- | --- |
| Unauthenticated external user | Can submit network/console input if exposed. | Untrusted. |
| Authenticated principal | Can access authorized resources through MFOS interfaces. | Trusted only for granted operations. |
| Operator | Can issue operator commands. | Trusted only through session, authority class, audit, and confirmation policy. |
| Automation principal | Can submit operator commands through automation hooks. | Not more trusted than its principal profile. |
| User job | Can execute submitted work under effective principal. | Untrusted unless specifically authorized. |
| User subsystem | Can call exposed SVC/PCALL interfaces. | Untrusted by default. |
| Trusted service | Provides MFOS service behavior. | Trusted for declared endpoint contract only. |
| Authorized service or AMF module | Can extend privileged behavior under AMF authority. | High risk; not equivalent to unlimited admin. |
| `securityd` | Policy decision point. | TCB component. |
| `auditd` | Evidence service. | TCB component for audit evidence. |
| PXM Core | Partition lifecycle and isolation. | TCB for partition isolation, not enterprise policy. |
| PXM Guard | High-Assurance root protection. | Small HA TCB for selected roots. |
| Side partition | Linux/Desktop/service/recovery partition. | Untrusted for MFOS enterprise semantics unless explicitly mediated. |
| Update provider/build system | Supplies artifacts and metadata. | Untrusted until signatures, metadata, provenance, and policy pass. |
| Physical/local attacker | May reboot, tamper with devices, observe hardware. | Profile-dependent residual risk. |
| AI implementation agent | Generates code/spec/test changes. | Untrusted until lint, review, tests, and evidence pass. |

## 9. Trust Boundaries

```text
TB-001  user input -> operatord parser
TB-002  operator session -> securityd decision API
TB-003  user job -> SVC ABI
TB-004  SVC ABI -> nucleus typed object handles
TB-005  service caller -> PCALL endpoint
TB-006  jobd DD resolution -> catalogd/datasetd/securityd
TB-007  spool browse/export/purge -> spoold/securityd
TB-008  policy mutation -> securityd transaction
TB-009  audit producer -> auditd append protocol
TB-010  audit query/export -> securityd/auditd redaction boundary
TB-011  AMF artifact -> amfd verifier/loader
TB-012  executable mapping -> nucleus/Guard policy
TB-013  update bundle -> uvsd metadata verifier
TB-014  boot chain -> measured boot/PXM/MFOS load
TB-015  MFOS partition -> side partition gateway
TB-016  partition lifecycle call -> PXM Core
TB-017  device assignment -> IOMMU/interrupt-remapping boundary
TB-018  Guard call -> Guard root transition engine
TB-019  AI output -> source/spec/test/CI review gate
TB-020  recovery action -> recovery partition and audit boundary
```

Boundary rules:

- Data crossing a trust boundary MUST be typed, bounded, canonicalized, and associated with a correlation ID where security relevant.
- Caller-supplied identity, subject, decision, handle generation, audit hash, and partition state MUST NOT be trusted across a boundary.
- Every boundary that can affect a protected resource MUST define authorization and audit obligations.

## 10. Assumptions

| ID | Assumption |
| --- | --- |
| `THR-ASM-0001` | Baseline protects against unauthorized subjects using defined MFOS interfaces. |
| `THR-ASM-0002` | Baseline does not claim survival after arbitrary nucleus, `securityd`, `auditd`, or authorized module compromise. |
| `THR-ASM-0003` | Enterprise assumes Secure Boot, measured boot, TPM, IOMMU, and interrupt remapping according to profile requirements. |
| `THR-ASM-0004` | High-Assurance root protection requires PXM Guard and Guard evidence. |
| `THR-ASM-0005` | PKU/PKS/CET/SMEP/SMAP/NX/IOMMU are enforcement aids, not semantic authorization sources. |
| `THR-ASM-0006` | Cryptographic primitives are implemented correctly or imported from an approved cryptographic TCB with evidence. |
| `THR-ASM-0007` | Source Matrix IDs and spec IDs are mandatory for z/OS-inspired or high-assurance implementation work. |

## 11. Abuse Cases

| ID | Abuse case | Target | Required outcome |
| --- | --- | --- | --- |
| `ABUSE-001` | Caller forges a subject identity in SVC request. | Nucleus/securityd. | Trusted scheduler/service context overrides caller-supplied identity; request denied or corrected. |
| `ABUSE-002` | Job submits as `ALICE` without authority. | jobd/securityd. | Submit denied and audited before caller result. |
| `ABUSE-003` | `BOB` reads `USER.ALICE.INPUT`. | datasetd/catalogd. | No handle created; deny audited first. |
| `ABUSE-004` | Stale dataset handle is reused after policy update. | datasetd/nucleus. | `MFOS_ERR_STALE_HANDLE` or `MFOS_ERR_POLICY_VERSION_MISMATCH`. |
| `ABUSE-005` | Catalog generation is rolled back to old location. | catalogd/datasetd. | Integrity/generation mismatch detected; protected open fails closed. |
| `ABUSE-006` | Spool output is browsed by unauthorized operator. | spoold/operatord. | No content returned; deny audited. |
| `ABUSE-007` | Operator command executes as raw shell text. | operatord. | Raw text rejected; only typed commands can execute. |
| `ABUSE-008` | Automation uses internal service API to bypass command policy. | operatord/services. | Bypass denied and audited. |
| `ABUSE-009` | AMF module with revoked signer is loaded. | amfd/nucleus/Guard. | Load fails closed; no executable mapping. |
| `ABUSE-010` | AMF module requests undeclared SVC endpoint. | amfd/SVC table. | Registration denied; audit alert. |
| `ABUSE-011` | Update bundle mixes old targets with fresh timestamp. | uvsd. | Mix-and-match detected; activation denied. |
| `ABUSE-012` | Audit producer supplies precomputed record hash. | auditd. | auditd recomputes canonical hash and rejects mismatch. |
| `ABUSE-013` | Auditd unavailable during security deny. | securityd/caller. | Operation fails closed according to profile. |
| `ABUSE-014` | Side partition DMA reads MFOS memory. | PXM/IOMMU. | Device assignment denied or DMA blocked; fault audited. |
| `ABUSE-015` | Device is reassigned before teardown completion. | PXM. | Reassignment denied until CPU/IOMMU/interrupt/device/memory teardown complete. |
| `ABUSE-016` | Guard call attempts to change dataset policy semantics. | Guard. | Rejected as out of scope or spec gap. |
| `ABUSE-017` | Unsupported SVC is treated as a completed operation. | nucleus. | No-fake-success check fails; runtime returns `MFOS_ERR_UNSUPPORTED`. |
| `ABUSE-018` | AI adds z/OS-like feature without Source Matrix ID. | CI/review. | Source-matrix lint fails; feature is `SPEC_GAP`. |

### 11.1 Semantic Misuse Abuse Cases

Semantic misuse is valid authority used in a dangerous, unintended, or
operationally incorrect way. These cases are not always system-integrity
violations. They require policy lint, dual-control, confirmation, audit review,
approval workflow, recovery drills, and residual-risk tracking.

| ID | Abuse case | Target | Required outcome |
| --- | --- | --- | --- |
| `ABUSE-SEM-001` | Authorized operator issues destructive command against the wrong target. | operatord/catalogd/datasetd/PXM. | Command requires typed target display, confirmation or dual-control, audit, and recovery metadata. |
| `ABUSE-SEM-002` | Security administrator grants an overbroad resource profile. | securityd policy store. | Policy lint flags broad default access or wildcard destructive grants before activation. |
| `ABUSE-SEM-003` | AMF signer signs a vulnerable module. | amfd/nucleus/Guard. | Signature is not sufficient; module authority remains scoped, revocable, audited, and unsupported in production until AMF profile permits it. |
| `ABUSE-SEM-004` | Job submitter uses an allowed program to exfiltrate a permitted dataset through SYSOUT or export. | jobd/spoold/gateway. | Export and spool access remain protected resources; audit and data-egress policy apply. |
| `ABUSE-SEM-005` | workload policy starves security-critical batch, audit export, or recovery jobs. | workpolicyd/jobd/auditd. | workload policy lint and operator review prevent starvation of protected service classes. |
| `ABUSE-SEM-006` | Side-partition gateway exports more metadata than intended. | Linux/Desktop gateway. | Gateway export policy, redaction, and audit deny excessive metadata disclosure. |
| `ABUSE-SEM-007` | Break-glass access is reused repeatedly without incident closure. | securityd/operatord/auditd. | Break-glass requires reason, expiry, audit, review, and incident closure before repeated use is accepted. |
| `ABUSE-SEM-008` | Automation principal performs allowed command sequence that bypasses human review intent. | operatord/automation. | Automation is subject to the same authority, confirmation, dual-control, rate limits, and audit policy as interactive operation. |
| `ABUSE-SEM-009` | Policy update weakens audit or redaction rules while preserving apparent authorization correctness. | securityd/auditd. | Policy lint blocks audit weakening without explicit review and evidence. |
| `ABUSE-SEM-010` | Recovery workflow rolls back to a semantically valid but operationally unsafe configuration. | recovery partition/uvsd/securityd. | Recovery approval checks policy generation, audit trail, rollback constraints, and operator approval. |

## 12. Component-Specific Threats and Mitigations

### 12.1 Nucleus, SVC, PCALL, and Handles

| Threat ID | Threat | Mitigation | Verification |
| --- | --- | --- | --- |
| `THR-NUC-001` | Caller-supplied identity trusted by SVC. | Identity from scheduler/trusted context only. | Negative SVC identity tests. |
| `THR-NUC-002` | User pointer dereferenced in supervisor context. | Bounded copy-in/copy-out only. | Fuzz and code review. |
| `THR-NUC-003` | Wrong-type or stale handle accepted. | Typed handles with generation, rights, expiry. | Handle negative tests. |
| `THR-NUC-004` | Undefined SVC is treated as implemented. | `SPEC_GAP` for undefined and `UNSUPPORTED` for unimplemented; both fail closed. | No-fake-success CI. |
| `THR-NUC-005` | Writable executable mapping. | NX/W^X, mapping policy, Guard approval in HA. | W^X tests. |
| `THR-NUC-006` | PCALL accepts arbitrary cross-address-space pointers. | Typed endpoint and bounded payloads. | PCALL fuzz tests. |
| `THR-NUC-007` | PKU/PKS treated as primary integrity boundary. | Architecture lint and profile claim review. | Design review. |

### 12.2 securityd

| Threat ID | Threat | Mitigation | Verification |
| --- | --- | --- | --- |
| `THR-SEC-001` | Distributed services make final authorization decisions. | `securityd` is central PDP; services are PEPs. | Architecture review. |
| `THR-SEC-002` | Missing policy defaults to allow. | Missing/malformed/stale policy fails closed. | Negative policy tests. |
| `THR-SEC-003` | Decision not bound to subject/object/operation/context/version. | Decision schema binding. | Interface tests. |
| `THR-SEC-004` | Break-glass becomes permanent admin path. | Reason, expiry, identity, audit, optional Guard approval. | Emergency drills. |
| `THR-SEC-005` | Policy rollback hides unauthorized change. | Transaction versioning, audit, update epoch, Guard root in HA. | Rollback tests. |
| `THR-SEC-006` | Obligation ignored by enforcement point. | Decision result carries obligations; PEP must enforce. | Integration tests. |
| `THR-SEC-007` | Overbroad policy is syntactically valid but grants unsafe access. | Policy lint before activation; dual-control for risky grants. | Policy lint tests. |

### 12.3 auditd

| Threat ID | Threat | Mitigation | Verification |
| --- | --- | --- | --- |
| `THR-AUD-001` | Security deny returned before audit evidence. | Required deny audit ordering. | Ordering negative tests. |
| `THR-AUD-002` | Audit records are unstructured logs. | Schema-bound records and event classes. | Schema tests. |
| `THR-AUD-003` | Audit hash chain truncated or rewritten. | Monotonic sequence and hash chain. | Tamper tests. |
| `THR-AUD-004` | Caller supplies trusted record hash. | auditd canonicalizes and recomputes. | Fuzz tests. |
| `THR-AUD-005` | Spool/console output treated as audit evidence. | Only auditd records are evidence. | Documentation and negative tests. |
| `THR-AUD-006` | Audit query leaks sensitive data. | Query/export are protected resources with redaction. | Security tests. |
| `THR-AUD-007` | Audit failure silently degrades protected operations. | Profile-specific fail-closed policy. | Fault injection. |

### 12.4 catalogd and datasetd

| Threat ID | Threat | Mitigation | Verification |
| --- | --- | --- | --- |
| `THR-DATA-001` | Dataset treated as POSIX path/file wrapper. | DSN and catalog object model; POSIX cannot bypass. | Architecture review. |
| `THR-DATA-002` | Dataset handle issued without `securityd`. | `datasetd` calls `securityd` before handle creation. | Negative tests. |
| `THR-DATA-003` | Catalog entry resolved before commit. | Resolve committed entries only. | Transaction tests. |
| `THR-DATA-004` | Catalog location tampered. | Integrity tags, generation binding, recovery journal. | Fault injection. |
| `THR-DATA-005` | Retention bypass for delete/purge. | Retention policy enforced before deletion. | Retention tests. |
| `THR-DATA-006` | System dataset modified through normal path. | Immutable/system flags and authority class checks. | Negative tests. |
| `THR-DATA-007` | Dataset open succeeds when audit unavailable. | Fail closed when audit obligation exists. | Audit fault tests. |

### 12.5 jobd and spoold

| Threat ID | Threat | Mitigation | Verification |
| --- | --- | --- | --- |
| `THR-JOB-001` | Job effective principal forged or missing. | Establish effective principal before open/execute/spool. | Integration tests. |
| `THR-JOB-002` | Malformed JCL-like input reaches queue. | Parser validation and conversion gate. | Parser fuzz. |
| `THR-JOB-003` | DD resolution bypasses catalog/security. | DD resolution through catalogd/datasetd/securityd. | Negative tests. |
| `THR-JOB-004` | Job step leaks output through unprotected spool. | Spool entries are protected resources. | Spool security tests. |
| `THR-JOB-005` | Unauthorized spool browse/export/purge. | `spoold` uses `securityd` for browse/export/purge. | Negative tests. |
| `THR-JOB-006` | Cancel leaves dataset or spool handles open. | Cancel lifecycle closes or revokes resources. | Cancellation tests. |
| `THR-JOB-007` | Spool quota exhaustion causes silent data loss. | Explicit quota failure or incomplete-output policy. | Fault injection. |

### 12.6 operatord

| Threat ID | Threat | Mitigation | Verification |
| --- | --- | --- | --- |
| `THR-OPER-001` | Operator console becomes root shell. | Typed command grammar; no raw execution. | Boot and parser tests. |
| `THR-OPER-002` | Destructive command executes without confirmation. | Confirmation and dual-control obligations. | Operator drills. |
| `THR-OPER-003` | Automation bypasses operator policy. | Automation uses same parser/security/audit path. | Negative tests. |
| `THR-OPER-004` | Emergency mode disables audit or policy. | Emergency remains audited and time-bound. | Emergency negative tests. |
| `THR-OPER-005` | Raw command text leaks secrets in audit. | Store raw hash by default; schema redaction. | Audit tests. |
| `THR-OPER-006` | Target changes between resolve and execute. | Generation-aware target refs and revalidation. | Race tests. |
| `THR-OPER-007` | Authorized operator targets the wrong destructive resource. | Typed target summary, confirmation, dual-control, and recovery audit. | Operator semantic misuse drills. |

### 12.7 workpolicyd

| Threat ID | Threat | Mitigation | Verification |
| --- | --- | --- | --- |
| `THR-WPOL-001` | workload policy dispatch hint treated as security authorization. | workload policy never grants resource access. | Architecture test. |
| `THR-WPOL-002` | Unknown job class silently runs. | Explicit default or fail closed. | Negative tests. |
| `THR-WPOL-003` | Overload falls back to run-now. | Explicit overload action. | Policy tests. |
| `THR-WPOL-004` | Policy activation bypasses operator/security. | `operatord` + `securityd` + audit. | Activation tests. |
| `THR-WPOL-005` | z/OS external workload management compatibility is implied. | Non-compatibility lint and review. | Documentation review. |
| `THR-WPOL-006` | workload policy starves security-critical jobs. | Reserved service classes and policy lint for critical classes. | Starvation negative tests. |

### 12.8 amfd and AMF

| Threat ID | Threat | Mitigation | Verification |
| --- | --- | --- | --- |
| `THR-AMF-001` | AMF treated as admin/root privilege. | Authority class and explicit ABI. | Review and tests. |
| `THR-AMF-002` | Unsigned or revoked module loads. | Signature, digest, revocation, epoch checks. | Revocation tests. |
| `THR-AMF-003` | Module loads from mutable dataset. | Immutable system dataset or approved artifact store only. | Negative tests. |
| `THR-AMF-004` | AMF ABI accepts arbitrary pointers. | Bounded typed ABI only. | ABI fuzz. |
| `THR-AMF-005` | AMF disables audit. | Prohibit audit-disable authority. | Architecture review. |
| `THR-AMF-006` | AMF compromise overstated as contained in Baseline. | Claim separation; Guard root only in HA. | Claim review. |
| `THR-AMF-007` | AMF registry mismatch ignored. | Registry binding and Guard seal in HA. | Guard tests. |

### 12.9 uvsd, Updates, and Supply Chain

| Threat ID | Threat | Mitigation | Verification |
| --- | --- | --- | --- |
| `THR-UVS-001` | Unsigned artifact accepted. | Signature, hash, size verification. | Negative tests. |
| `THR-UVS-002` | Rollback to vulnerable generation. | Generation and security epoch checks. | Rollback tests. |
| `THR-UVS-003` | Freeze attack with stale metadata. | Timestamp freshness policy. | Freeze tests. |
| `THR-UVS-004` | Mix-and-match metadata view. | Root/timestamp/snapshot/targets consistency. | Consistency tests. |
| `THR-UVS-005` | Transport TLS treated as artifact integrity. | Artifact metadata is authoritative. | Architecture review. |
| `THR-UVS-006` | Build artifact lacks provenance. | SBOM and signed provenance for production. | Supply-chain audit. |
| `THR-UVS-007` | Activation measured digest differs from verified manifest. | Measurement binding before commit. | Measurement tests. |

### 12.10 PXM Core

| Threat ID | Threat | Mitigation | Verification |
| --- | --- | --- | --- |
| `THR-PXM-001` | PXM interprets dataset/job/security semantics. | PXM scope limited to lifecycle/isolation. | Architecture review. |
| `THR-PXM-002` | Partition memory reassigned without zeroing. | Revoke mappings, zero before reuse. | Memory reuse tests. |
| `THR-PXM-003` | Device assigned without IOMMU or interrupt remap. | Profile-required feature checks. | Platform negative tests. |
| `THR-PXM-004` | Device reassigned before teardown. | Teardown checklist required. | Teardown tests. |
| `THR-PXM-005` | Caller supplies fake partition state. | Authoritative PXM state machine. | State negative tests. |
| `THR-PXM-006` | Audit-required partition operation silently succeeds. | Audit or fail closed. | Fault injection. |
| `THR-PXM-007` | Implicit backend used for HA claim. | Profile conformance rejection. | Release review. |

### 12.11 PXM Guard

| Threat ID | Threat | Mitigation | Verification |
| --- | --- | --- | --- |
| `THR-GRD-001` | Guard grows into business policy engine. | Root-object-only scope. | Architecture review. |
| `THR-GRD-002` | Guard unavailable in HA but boot continues. | HA boot denied or recovery mode. | Boot tests. |
| `THR-GRD-003` | Root transition not audited. | Guard and auditd record transition. | Integration tests. |
| `THR-GRD-004` | Executable mapping violates root policy. | Guard authorization before mapping in HA. | Mapping tests. |
| `THR-GRD-005` | SVC table mismatch ignored. | Lockdown or panic-equivalent. | Fault injection. |
| `THR-GRD-006` | Attestation replayed. | Nonce-bound attestation. | Attestation tests. |
| `THR-GRD-007` | Guard secret released to wrong measurement. | Measurement-bound release. | Negative tests. |

### 12.12 Optional POSIX and Side Partition Gateways

| Threat ID | Threat | Mitigation | Verification |
| --- | --- | --- | --- |
| `THR-GW-001` | POSIX root bypasses MFOS securityd. | POSIX is optional and profile-limited; no bypass. | Negative tests. |
| `THR-GW-002` | Side partition reads MFOS dataset directly. | Audited gateway only; no direct protected-resource access. | Gateway tests. |
| `THR-GW-003` | Clipboard/browser/desktop path leaks data. | Side partition isolation and explicit export policy. | Integration tests. |
| `THR-GW-004` | Linux/Desktop compromise becomes MFOS compromise. | Partition isolation, IOMMU, audited gateway. | Partition tests. |
| `THR-GW-005` | Gateway exports excessive metadata under a valid request. | Export schema, redaction policy, and policy lint. | Metadata export negative tests. |

### 12.13 AI Implementation and Documentation

| Threat ID | Threat | Mitigation | Verification |
| --- | --- | --- | --- |
| `THR-AI-001` | AI invents z/OS-like concept without source. | Source Matrix lint. | CI. |
| `THR-AI-002` | AI writes code without requirement IDs. | Spec ID required check. | CI. |
| `THR-AI-003` | AI adds fake success or empty stub. | No-fake-success scanner. | CI and review. |
| `THR-AI-004` | AI omits negative tests for security path. | Negative test required gate. | CI. |
| `THR-AI-005` | AI overclaims PKU/PKS/Guard guarantees. | Claim review and prohibited wording lint. | Release review. |

## 13. Mitigation Baseline

All protected-resource flows MUST apply these mitigations unless a narrower spec explicitly strengthens them:

- Canonical object reference before authorization.
- Trusted subject context, never caller-supplied identity.
- `securityd` decision for protected access.
- Decision bound to subject, object, operation, context, policy version, and generation where applicable.
- Audit obligation generated by `securityd` or component spec.
- Deny audit before caller-visible denial for security-sensitive operations.
- Typed handles with rights, generation, expiry, and correlation ID.
- Bounded copy-in/copy-out for untrusted buffers.
- `MFOS_ERR_UNSUPPORTED` for specified but unimplemented behavior.
- `MFOS_ERR_SPEC_GAP` for undefined behavior.
- No silent fallback to allow, run-now, best-effort audit, or diagnostic-only evidence.

## 14. Audit Obligations

Threat-relevant audit events MUST include `correlation_id`, component ID, subject, object, operation, decision, reason code, policy version where applicable, source component, and profile.

| Threat area | Required audit events |
| --- | --- |
| Authentication/session | Session start/end, failed authentication, MFA requirement, break-glass entry/exit. |
| Authorization | Decision request/result, deny, allow-with-obligation, policy mismatch. |
| Dataset/catalog | Define, resolve, open allow/deny, close, update, delete, integrity failure, recovery. |
| Job/spool | Submit allow/deny, conversion, queue/select, step start/complete, DD resolve, spool create/browse/purge/export. |
| Operator | Parse, allow/deny, confirmation, dual-control, execute, result, automation, emergency. |
| workload policy | Policy validate/activate/deny, classify decision, overload, policy mismatch. |
| AMF | Load request, signature/digest/revocation result, authority class, registry update, Guard approval. |
| Update | Verify, stage, activate, commit, rollback/freeze/mix-and-match denial, recovery rollback. |
| Nucleus/SVC/PCALL | Invalid call, unsupported/spec-gap call, stale handle, copy failure, mapping violation. |
| PXM | Partition define/measure/load/activate/start/quiesce/recover/destroy, device assign/release/teardown. |
| Guard | Root seal/verify/transition, executable mapping, SVC table check, AMF approval, attestation. |
| Audit itself | Append failure, hash-chain mismatch, query/export/retention, tamper detection, recovery. |
| AI/CI | Source-matrix lint failure, no-fake-success failure, missing negative test, missing audit obligation. |
| Semantic misuse | Overbroad policy warning, destructive command confirmation, break-glass repetition, gateway export redaction, workload policy starvation warning. |

Audit ordering:

- Security-sensitive DENY MUST be audited before the caller receives final denial.
- Successful security-root, audit-root, AMF-registry, update, and partition root transitions MUST be audited before success is reported.
- If audit is unavailable and the profile requires audit for the operation, the operation MUST fail closed.

## 15. Fail-Closed Conditions

| Condition | Required behavior |
| --- | --- |
| Missing security profile for protected object | Deny or enter explicit bootstrap rule; never allow by default. |
| Missing, malformed, stale, or ambiguous policy | Deny or fail closed. |
| Missing required audit path | Return `MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE` or profile-defined recovery stop. |
| Caller-supplied identity conflicts with trusted context | Reject request and audit privilege-confusion attempt. |
| Unknown resource/operation pair | Return `MFOS_ERR_SPEC_GAP`. |
| Known but unimplemented operation | Return `MFOS_ERR_UNSUPPORTED`. |
| Parser malformed input for protected command/job/policy/update | Reject before side effects. |
| Dataset/catalog generation mismatch | Reject handle or open. |
| Stale handle or stale policy version | Reject and audit stale-use attempt. |
| AMF invalid signature, revoked signer, or stale security epoch | Reject load; no executable mapping. |
| Update rollback/freeze/mix-and-match | Reject activation and audit security-critical event. |
| IOMMU or interrupt remapping unavailable for required device assignment | Deny assignment. |
| PXM teardown incomplete | Deny reassignment. |
| Guard required but unavailable | HA boot denied or recovery mode. |
| Guard root mismatch | Lockdown, root transition denial, or panic-equivalent according to root type. |
| Audit hash-chain mismatch | Seal affected stream, alert, enter recovery workflow. |

## 16. Formal Invariants

```text
INV-THR-001:
  No protected-resource operation reaches success unless securityd returned
  ALLOW or ALLOW_WITH_AUDIT for the same subject, object, operation,
  context, and policy_version, or an explicitly specified bootstrap rule
  applies.

INV-THR-002:
  No required security-sensitive DENY is returned to a caller before an
  audit obligation is satisfied or the operation fails closed because audit
  is unavailable.

INV-THR-003:
  A dataset handle cannot become ACTIVE unless it is bound to subject,
  operation, policy_version, catalog_generation, dataset_generation, expiry,
  and correlation_id.

INV-THR-004:
  A job cannot open datasets, execute programs, or create protected spool
  output before effective_principal is established.

INV-THR-005:
  An operator command cannot execute unless raw command text has been parsed
  into a typed command object, targets are resolved, securityd authorization
  is obtained, and audit obligations are satisfied.

INV-THR-006:
  An AMF module cannot be executable unless signature, digest, manifest,
  catalog immutability, revocation, authority class, securityd decision, and
  profile-specific Guard checks have succeeded.

INV-THR-007:
  PXM cannot reassign partition memory until CPU mappings, IOMMU mappings,
  interrupt routes, and device ownership records are revoked and memory is
  zeroed.

INV-THR-008:
  PXM cannot interpret dataset, catalog, job, spool, security profile, or workload policy
  semantics.

INV-THR-009:
  Guard cannot interpret ordinary dataset policy, job scheduling, spool
  formatting, operator UI behavior, or business policy semantics.

INV-THR-010:
  Undefined behavior cannot produce success. It must return SPEC_GAP.

INV-THR-011:
  Specified but unimplemented behavior cannot produce success. It must return
  UNSUPPORTED.

INV-THR-012:
  High-Assurance root-protection claims cannot be made without Guard evidence
  for the relevant root object.
```

## 17. Positive Tests

| ID | Test |
| --- | --- |
| `THR-POS-001` | Authorized `ALICE` opens `USER.ALICE.INPUT`; `securityd`, `datasetd`, and `auditd` records align by correlation ID. |
| `THR-POS-002` | HELLO job runs as established effective principal, resolves DD through catalog/dataset/security, writes protected SYSOUT, completes RC=0. |
| `THR-POS-003` | Operator runs `DISPLAY SYSTEM`; command is typed, authorized, audited, and displayed. |
| `THR-POS-004` | workload policy classifies class `A` job with active policy version and returns explicit dispatch hint. |
| `THR-POS-005` | Signed AMF module from immutable approved store loads with correct authority class and audit. |
| `THR-POS-006` | Valid update bundle verifies root/timestamp/snapshot/targets/artifact metadata and stages without activation until approved. |
| `THR-POS-007` | PXM creates, measures, loads, activates, and starts a partition with audit records. |
| `THR-POS-008` | High-Assurance Guard seals security root and audit root and produces attestation with nonce. |
| `THR-POS-009` | Audit stream rollover preserves hash-chain continuity. |
| `THR-POS-010` | Source-matrix lint accepts a spec change with source IDs, requirements, negative tests, and audit obligations. |

## 18. Negative Tests

| ID | Test |
| --- | --- |
| `THR-NEG-001` | `BOB` reads `USER.ALICE.INPUT`; no dataset handle is created and denial is audited first. |
| `THR-NEG-002` | SVC request supplies forged principal; trusted context wins and request is denied. |
| `THR-NEG-003` | User pointer points to invalid or changing memory during SVC; copy-in/copy-out rejects safely. |
| `THR-NEG-004` | Undefined SVC number returns `MFOS_ERR_SPEC_GAP`, never success. |
| `THR-NEG-005` | Unimplemented known command returns `MFOS_ERR_UNSUPPORTED`, never success. |
| `THR-NEG-006` | Malformed JCL-like job does not reach queue. |
| `THR-NEG-007` | Unauthorized spool browse returns no content and audits denial first. |
| `THR-NEG-008` | Operator destructive command without confirmation has no side effects. |
| `THR-NEG-009` | Automation attempts direct internal service call and is denied as bypass. |
| `THR-NEG-010` | Revoked AMF signer fails closed and no executable pages are mapped. |
| `THR-NEG-011` | Update rollback/freeze/mix-and-match is rejected and audited. |
| `THR-NEG-012` | Device assignment without required IOMMU or interrupt remapping is denied. |
| `THR-NEG-013` | PXM memory reassignment before zeroing is denied. |
| `THR-NEG-014` | Guard-required HA boot with unavailable Guard is denied or enters recovery mode. |
| `THR-NEG-015` | Auditd unavailable for protected denial causes fail-closed behavior. |
| `THR-NEG-016` | Audit hash-chain mismatch triggers tamper recovery and no committed rewrite. |
| `THR-NEG-017` | AI-generated z/OS-like concept without Source Matrix ID fails source-matrix lint. |
| `THR-NEG-018` | Spec or code path with fake success fails no-fake-success CI. |
| `THR-NEG-019` | Overbroad default access policy fails policy lint before activation. |
| `THR-NEG-020` | Destructive operator command against wrong generation fails confirmation or dual-control. |
| `THR-NEG-021` | workload policy that starves security-critical class fails policy lint. |
| `THR-NEG-022` | Gateway export request that includes excessive metadata is denied or redacted and audited. |
| `THR-NEG-023` | Repeated break-glass use without incident closure is denied or escalated. |

## 19. Fuzz Targets

| ID | Target | Required property |
| --- | --- | --- |
| `THR-FUZZ-001` | SVC request decoder. | No panic, no forged identity, bounded copy only. |
| `THR-FUZZ-002` | PCALL request decoder. | Typed endpoint validation, no arbitrary pointer trust. |
| `THR-FUZZ-003` | Authorization decision request. | Unknown resource/operation fails closed. |
| `THR-FUZZ-004` | Audit record parser/canonicalizer. | Hash recomputation and schema bounds hold. |
| `THR-FUZZ-005` | DSN parser and catalog journal. | Invalid DSN no success; torn journal recovers. |
| `THR-FUZZ-006` | JCL-like parser and inline SYSIN. | Malformed input cannot reach queued state. |
| `THR-FUZZ-007` | Spool record stream. | Invalid sequence/length cannot leak content. |
| `THR-FUZZ-008` | Operator command parser. | Raw text cannot execute. |
| `THR-FUZZ-009` | workload policy parser. | Invalid policy cannot become active. |
| `THR-FUZZ-010` | AMF manifest parser. | Invalid source IDs, signatures, epochs, ABI fields fail closed. |
| `THR-FUZZ-011` | Update metadata parser. | Rollback/freeze/mix-and-match cannot verify. |
| `THR-FUZZ-012` | Activation profile parser. | Invalid resource/device constraints cannot activate. |
| `THR-FUZZ-013` | Guard call request. | Out-of-scope root operations fail spec gap. |
| `THR-FUZZ-014` | AI output lint. | Missing spec/source/test/audit metadata is detected. |

## 20. Fault-Injection Tests

| ID | Fault | Expected response |
| --- | --- | --- |
| `THR-FI-001` | auditd unavailable during dataset open deny. | Operation fails closed or returns audited recovery error by profile. |
| `THR-FI-002` | securityd unavailable during protected resource access. | Protected access denied or recovery mode only. |
| `THR-FI-003` | Catalog journal torn mid-commit. | Recovery leaves old or new committed state, never partial success. |
| `THR-FI-004` | Spool storage fills during SYSOUT capture. | Explicit step failure or incomplete-output state, no silent loss. |
| `THR-FI-005` | AMF registry update crashes mid-transaction. | Registry recovers to committed state or fails closed. |
| `THR-FI-006` | Update activation crash before commit. | Recovery rollback workflow. |
| `THR-FI-007` | PXM fault during device teardown. | Device remains unavailable until teardown evidence completes. |
| `THR-FI-008` | Guard root mismatch during SVC table verify. | Lockdown or panic-equivalent. |
| `THR-FI-009` | TPM event log unavailable in Enterprise. | Enterprise measured-boot claim denied; boot policy applies. |
| `THR-FI-010` | Remote audit export unavailable in Enterprise. | Local hash-chain continues and export backlog audited; profile policy controls degraded operation. |

## 21. Residual Risks

| ID | Residual risk | Current position |
| --- | --- | --- |
| `THR-RISK-001` | Baseline cannot claim protection after arbitrary nucleus or `securityd` compromise. | Explicit non-claim; HA Guard covers selected roots only. |
| `THR-RISK-002` | Authorized AMF module compromise remains high impact. | Minimize AMF, require signed/measured/revocable modules, Guard registry in HA. |
| `THR-RISK-003` | Firmware or hardware compromise can invalidate boot assumptions. | NIST-style protection/detection/recovery; residual risk remains. |
| `THR-RISK-004` | DMA/IOMMU behavior differs by platform and firmware. | Platform conformance tests required before passthrough production. |
| `THR-RISK-005` | Side channels and microarchitectural leakage are not fully modeled. | Track separately; do not claim comprehensive side-channel resistance. |
| `THR-RISK-006` | Formal verification scope may lag implementation. | Require invariants and staged formal models before production claims. |
| `THR-RISK-007` | Human operator misuse can still cause authorized damage. | Confirmation, dual-control, audit, training, and recovery drills mitigate. |
| `THR-RISK-008` | Audit evidence can be unavailable during catastrophic storage failure. | Profile-specific remote/OOB audit strategy required for stronger claims. |
| `THR-RISK-009` | Supply-chain trust depends on key governance and build-system control. | SLSA/TUF-style evidence; key ceremony remains separate operational spec. |
| `THR-RISK-010` | AI implementation agents may produce plausible but wrong design. | Source/spec/test/audit lint, review, and no-fake-success gates. |
| `THR-RISK-011` | Valid authority can still be used with unsafe business intent or wrong operational target. | Policy lint, confirmation, dual-control, approval workflow, audit review, and recovery drills mitigate but do not eliminate this risk. |

## 22. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| `MFOS-REQ-THR-0001` | Every protected resource threat must name assets, actor, boundary, mitigation, audit obligation, and test. | Threat-model review |
| `MFOS-REQ-THR-0002` | Threat mitigations must reference Source Matrix IDs when they rely on z/OS-inspired or high-assurance concepts. | Source-matrix lint |
| `MFOS-REQ-THR-0003` | Threat model must not claim compatibility with z/OS, IBM products, Windows VBS, or Linux. | Documentation review |
| `MFOS-REQ-THR-0004` | All security-sensitive boundaries must define fail-closed behavior. | Architecture review |
| `MFOS-REQ-THR-0005` | Abuse cases must include unauthorized access, stale handle, audit failure, update rollback, AMF revocation, PXM teardown, Guard mismatch, and AI fake success. | Test review |
| `MFOS-REQ-THR-0006` | Component specs must not introduce new protected-resource flows without updating this threat model or listing a threat-model spec gap. | PR review |
| `MFOS-REQ-THR-0007` | High-Assurance claims must be linked to Guard evidence and residual-risk statements. | Evidence review |
| `MFOS-REQ-THR-0008` | No hardware feature may be described as the semantic source of authorization. | Claim review |
| `MFOS-REQ-THR-0009` | Threat-model negative tests must be part of conformance planning. | CI/test plan review |
| `MFOS-REQ-THR-0010` | Threat-model residual risks must be reviewed before production readiness claims. | Release review |
| `MFOS-REQ-THR-0011` | Threat model must include semantic misuse cases for valid authority, overbroad policy, AMF signing, workload policy starvation, side gateway export, break-glass reuse, and automation misuse. | threat-model review |

## 23. Evidence Artifacts

Threat-model evidence MUST include:

- Source Matrix references used by each security-sensitive component.
- Requirements-to-threat traceability table.
- Threat-to-negative-test traceability table.
- Audit event samples for deny, policy change, update failure, AMF denial, PXM teardown denial, and Guard mismatch.
- Fuzz target registration list.
- Fault-injection test results.
- No-fake-success CI report.
- Source-matrix lint report.
- Residual-risk review record.
- Policy-lint report for semantic misuse cases.
- Operator semantic misuse drill report.
- Production readiness threat review.

## 24. Spec Gaps

| ID | Gap |
| --- | --- |
| `THR-GAP-001` | Complete authentication protocol threat model is not specified. |
| `THR-GAP-002` | Remote management plane protocol and operator approval workflow are not specified. |
| `THR-GAP-003` | Cryptographic algorithm, key storage, key rotation, and key ceremony details are not specified. |
| `THR-GAP-004` | Full side-channel and microarchitectural leakage model is not specified. |
| `THR-GAP-005` | Exact POSIX subsystem and Linux/Desktop gateway threat model is not specified. |
| `THR-GAP-006` | Physical attack resistance and secure enclosure assumptions are not specified. |
| `THR-GAP-007` | Distributed or sysplex-like multi-node threat model is not specified. |
| `THR-GAP-008` | Remote audit collector protocol and OOB audit path are not specified. |
| `THR-GAP-009` | Full formal TLA+/Alloy/Coq/Isabelle models are not written. |
| `THR-GAP-010` | Complete production incident response and forensics workflow is not specified. |
| `THR-GAP-011` | Full dependency risk scoring and vulnerability-response workflow are not specified. |
| `THR-GAP-012` | Hardware platform certification matrix is not specified. |

## 25. Inactive Future Implementation Prompt Template

Phase status: inactive future template. This section does not authorize production implementation, hosted daemon implementation, or portable semantic-core implementation.

```text
You are the MFOS threat-model implementation and review agent.

Use these Source Matrix IDs where relevant:
- EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
- EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001
- EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001
- EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001
- EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001
- EXTREF-IBM-ZOS-SECURITY-SERVER-0001
- EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001
- EXTREF-IBM-ZOS-JES-INTRODUCTION-0001
- EXTREF-IBM-ZOS-JES-JOB-FLOW-0001
- EXTREF-IBM-ZOS-JES2-LIBRARY-0001
- EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001
- EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001
- EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001
- EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001
- EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001
- EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001
- EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001
- EXTREF-IBM-Z-LPAR-INTRODUCTION-0001
- EXTREF-IBM-Z-DPM-0001
- X64-INTEL-001
- X64-AMD-001
- X64-LINUX-PKU-001
- X64-LINUX-CET-001
- MS-VBS-001
- MS-VSM-001
- TCG-001
- NIST-160-001
- NIST-193-001
- NIST-218-001
- TUF-001
- SLSA-001
- SEL4-001
- FBVBS-001

Rules:
- Do not claim z/OS, IBM product, Windows VBS, Linux, or z/Architecture compatibility.
- Treat MFOS concepts as source-grounded mappings with explicit divergence.
- Identify assets, actors, trust boundaries, abuse cases, mitigations, audit obligations, fail-closed behavior, invariants, tests, fuzz targets, and residual risks.
- securityd is the policy decision point.
- auditd is evidence, not ordinary logging.
- PXM is partition lifecycle and isolation only.
- Guard is High-Assurance selected-root protection only.
- Hardware features are enforcement aids, not authorization semantics.
- Unsupported behavior returns MFOS_ERR_UNSUPPORTED.
- Undefined behavior returns MFOS_ERR_SPEC_GAP.
- No fake success, empty stubs, or silent fallback.

Output:
1. Threat IDs covered
2. Source Matrix IDs used
3. Assets affected
4. Actors and trust boundaries
5. Abuse cases
6. Mitigations
7. Audit obligations
8. Fail-closed conditions
9. Formal invariants
10. Positive tests
11. Negative tests
12. Fuzz targets
13. Fault-injection tests
14. Residual risks
15. Spec gaps
16. Evidence artifacts
```
