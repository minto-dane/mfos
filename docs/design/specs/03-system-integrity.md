---
spec_id: "MFOS-SPEC-03-SYSTEM-INTEGRITY"
title: "MFOS System Integrity Specification v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001", "EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001", "EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001", "EXTREF-IBM-Z-DPM-0001", "EXTREF-IBM-ZOS-JES-INTRODUCTION-0001", "EXTREF-IBM-ZOS-JES-JOB-FLOW-0001", "EXTREF-IBM-Z-LPAR-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001", "EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001", "EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001", "EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001", "EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001", "EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001", "EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001", "MS-VBS-001", "MS-VSM-001", "NIST-160-001", "TCG-001", "X64-AMD-001", "X64-INTEL-001", "X64-LINUX-CET-001", "X64-LINUX-PKU-001"]
requirement_refs: ["MFOS-REQ-SYSINT-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
statement_source_grounding: "line_local"
---
# MFOS System Integrity Specification v0.1

Status: Draft specification

## 1. Purpose

This document defines the MFOS system integrity model.

Source IDs: `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `FBVBS-001`.
Requirement IDs: `MFOS-REQ-SYSINT-0001`, `MFOS-REQ-SYSINT-0002`, `MFOS-REQ-SYSINT-0010`, `MFOS-REQ-SYSINT-0011`, `MFOS-REQ-SYSINT-0012`, `MFOS-REQ-SYSINT-0013`.

MFOS system integrity means that unauthorized principals, programs, jobs, and subsystems cannot use defined system interfaces to bypass or alter:

- security policy
- dataset access control
- catalog metadata
- audit recording
- spool access
- job identity
- operator command authority
- authorized execution state
- system control objects

This model is inspired by IBM-documented z/OS system integrity concepts (`EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`), but MFOS does not claim z/OS compatibility.

This document is an architecture and assurance specification. It is not permission to start production implementation. Any implementation input derived from this document must also satisfy the pre-implementation gate for requirements, source references, object model, state machine, failure modes, audit obligations, tests, evidence, claim boundary, pack contract, and red-team review.

## 2. Scope

In scope:

- authorized vs unauthorized execution concepts
- ExecutionState
- AuthorityClass
- StorageDomain
- protected resources
- system interfaces
- SVC rules
- PCALL rules
- AMF rules
- securityd authority
- auditd authority
- dataset/catalog/spool rules
- operator command rules
- partition-aware integrity requirements
- High-Assurance Guard extensions
- invariants
- failure modes
- positive tests
- negative tests
- fuzz targets

Out of scope:

- binary compatibility with z/OS or z/Architecture
- exact z/OS PSW key behavior
- exact z/OS storage key behavior
- RACF compatibility
- JES2/JES3 compatibility
- DFSMS compatibility
- Windows VBS compatibility
- full formal proof
- production readiness

## 3. Non-Compatibility Statement

MFOS is z/OS-inspired and source-grounded (`EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`).

Source IDs: `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001`, `X64-LINUX-PKU-001`, `MS-VBS-001`, `MS-VSM-001`.
Requirement IDs: `MFOS-REQ-SYSINT-0005`, `MFOS-REQ-SYSINT-0006`, `MFOS-REQ-SYSINT-0018`, `MFOS-REQ-SYSINT-0019`, `MFOS-REQ-SYSINT-0020`.

MFOS is not:

- z/OS compatible
- z/Architecture compatible
- a z/OS clone
- a RACF implementation
- a JES2 or JES3 implementation
- a DFSMS implementation
- an SMF implementation
- a Windows VBS implementation

Allowed wording:

- "MFOS maps selected IBM-documented enterprise OS concepts onto an x64-native design."
- "MFOS system integrity is inspired by IBM system integrity concepts."
- "MFOS AMF is APF-inspired."
- "MFOS securityd is RACF-inspired."

Prohibited wording:

- "MFOS is z/OS compatible."
- "MFOS implements RACF."
- "MFOS implements JES2."
- "MFOS provides z/OS storage keys on x64."
- "PKU provides z/OS storage key compatibility."

IBM product names in this document identify source-mapping anchors only. They do not grant compatibility claims, replacement claims, conformance claims, endorsement claims, or implementation permission.

## 4. Source Matrix References

| Source ID | Use in this spec | Primary requirement IDs |
| --- | --- | --- |
| EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001 | System integrity inspiration and unauthorized program boundary | `MFOS-REQ-SYSINT-0001`, `MFOS-REQ-SYSINT-0005` |
| EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001 | Authorized boundary testing and untrusted parameter discipline | `MFOS-REQ-SYSINT-0007`, `MFOS-REQ-SYSINT-0008`, `MFOS-REQ-SYSINT-0009` |
| EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001 | Authorized program inspiration and AMF mapping | `MFOS-REQ-SYSINT-0004`, `MFOS-REQ-SYSINT-0017` |
| EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001 | Storage protection inspiration | `MFOS-REQ-SYSINT-0004`, `MFOS-REQ-SYSINT-0020` |
| EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001 | Storage key detail inspiration | `MFOS-REQ-SYSINT-0004`, `MFOS-REQ-SYSINT-0020` |
| EXTREF-IBM-ZOS-SECURITY-SERVER-0001 | Security manager source family | `MFOS-REQ-SYSINT-0012` |
| EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001 | Resource profile and access control inspiration | `MFOS-REQ-SYSINT-0001`, `MFOS-REQ-SYSINT-0012`, `MFOS-REQ-SYSINT-0014` |
| EXTREF-IBM-ZOS-JES-INTRODUCTION-0001 | Job/spool system interface inspiration | `MFOS-REQ-SYSINT-0003`, `MFOS-REQ-SYSINT-0015` |
| EXTREF-IBM-ZOS-JES-JOB-FLOW-0001 | Job lifecycle and spool flow inspiration | `MFOS-REQ-SYSINT-0015` |
| EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001 | Catalog and dataset naming/location inspiration | `MFOS-REQ-SYSINT-0003`, `MFOS-REQ-SYSINT-0014` |
| EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001 | Dataset/storage management source family | `MFOS-REQ-SYSINT-0014` |
| EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | Audit/accounting evidence inspiration | `MFOS-REQ-SYSINT-0013` |
| EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001 | Security audit record inspiration | `MFOS-REQ-SYSINT-0013` |
| EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001 | Workload class inspiration | `MFOS-REQ-SYSINT-0001` |
| EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001 | PCALL inspiration | `MFOS-REQ-SYSINT-0003`, `MFOS-REQ-SYSINT-0009` |
| EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001 | Cross-memory security inspiration | `MFOS-REQ-SYSINT-0009` |
| EXTREF-IBM-Z-LPAR-INTRODUCTION-0001 | Partition isolation inspiration | `MFOS-REQ-SYSINT-0018` |
| EXTREF-IBM-Z-DPM-0001 | Partition management plane inspiration | `MFOS-REQ-SYSINT-0018` |
| X64-INTEL-001 | x64 protection, paging, VMX, CET, PKU/PKS reality | `MFOS-REQ-SYSINT-0020` |
| X64-AMD-001 | AMD64 protection, paging, SVM/NPT reality | `MFOS-REQ-SYSINT-0020` |
| X64-LINUX-PKU-001 | PKU limitation reference | `MFOS-REQ-SYSINT-0020` |
| X64-LINUX-CET-001 | CET reference | `MFOS-REQ-SYSINT-0020` |
| MS-VBS-001 | Guard comparison for High-Assurance only | `MFOS-REQ-SYSINT-0006`, `MFOS-REQ-SYSINT-0019` |
| MS-VSM-001 | VSM/VTL-like Guard comparison for High-Assurance only | `MFOS-REQ-SYSINT-0006`, `MFOS-REQ-SYSINT-0019` |
| TCG-001 | Measured boot and TPM measurement reference | `MFOS-REQ-SYSINT-0006` |
| NIST-160-001 | Secure systems engineering reference | `MFOS-REQ-SYSINT-0005`, `MFOS-REQ-SYSINT-0006` |
| FBVBS-001 | Requirements, evidence, state-machine, and no-fake-success discipline | `MFOS-REQ-SYSINT-0010`, `MFOS-REQ-SYSINT-0011` |

## 5. System Integrity Definition

MFOS System Integrity:

```text
An unauthorized subject must not be able to use a defined MFOS system
interface to bypass, corrupt, forge, suppress, or acquire authority over
protected resources, security decisions, audit evidence, authorized
execution state, partition state, or system control objects.
```

Subject categories:

- Principal
- ProgramIdentity
- Job
- JobStep
- User subsystem
- Trusted service
- Authorized service
- Operator session
- AMF module
- Side partition gateway
- Recovery partition service

Protected integrity properties:

- no unauthorized allow
- no forged subject identity
- no forged effective principal
- no dataset handle without authorization
- no catalog mutation without authorization
- no spool browse/purge/export without authorization
- no operator command execution without authorization and audit
- no AMF load without signature, manifest, securityd decision, and profile-specific approval
- no audit-required result returned before required audit processing
- no unsupported success
- no specification-gap behavior invented at runtime

## 6. Authorized vs Unauthorized

Source IDs: `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001`, `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001`.
Requirement IDs: `MFOS-REQ-SYSINT-0001`, `MFOS-REQ-SYSINT-0004`, `MFOS-REQ-SYSINT-0012`, `MFOS-REQ-SYSINT-0013`, `MFOS-REQ-SYSINT-0017`.

### 6.1 Unauthorized Subject

A subject is unauthorized for an operation when it lacks a valid securityd decision granting that exact subject, object, operation, context, and policy version.

Unauthorized includes:

- unauthenticated principal
- disabled principal
- locked principal
- expired principal
- subject with missing effective principal
- subject with stale policy version
- subject with insufficient AuthorityClass
- program with missing or mismatched ProgramIdentity
- job before effective principal establishment
- AMF module without valid authorization
- service calling outside its declared endpoint authority
- operator session without command authority
- side partition gateway without explicit gateway policy
- privileged execution context without a matching AuthorityClass
- previously authorized subject using an expired, revoked, stale, or mismatched security decision

### 6.2 Authorized Subject

A subject is authorized only when all applicable conditions hold:

- identity source is trusted
- effective principal is established
- securityd returns `ALLOW` or `ALLOW_WITH_AUDIT`
- decision inputs match subject, object, operation, context, and policy version
- audit obligations are satisfied or explicitly in progress according to profile rule
- relevant handle is bound to decision context
- AuthorityClass requirements are met
- AMF requirements are met where executable extension authority is involved
- Guard approval is present when required by High-Assurance profile

Authorization is scoped to one operation. A decision that allows one resource, operation, policy version, or context MUST NOT be reused for another resource, operation, policy version, or context.

### 6.3 AuthorityClass

AuthorityClass is separate from ExecutionState.

Examples:

- `DATASET_READ`
- `DATASET_UPDATE`
- `CATALOG_DEFINE`
- `CATALOG_UPDATE`
- `SPOOL_BROWSE`
- `SPOOL_PURGE`
- `JOB_SUBMIT`
- `JOB_CANCEL`
- `OPERATOR_DISPLAY`
- `OPERATOR_DEFINE`
- `OPERATOR_DESTRUCTIVE`
- `SECURITY_POLICY_UPDATE`
- `AUDIT_QUERY`
- `AMF_LOAD`
- `PARTITION_OPERATE`
- `GUARD_ROOT_TRANSITION`

Rules:

- AuthorityClass MUST be explicit.
- AuthorityClass MUST be auditable.
- AuthorityClass MUST NOT be inferred from UID-like values or root-shell status.
- AMF authority MUST NOT imply general administrator authority.
- AuthorityClass MUST NOT be inferred from `ExecutionState` alone.
- AuthorityClass MUST NOT be accepted from caller-controlled request fields.

## 7. Execution States

Source IDs: `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001`, `EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001`, `EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `EXTREF-IBM-Z-DPM-0001`, `MS-VBS-001`, `MS-VSM-001`.
Requirement IDs: `MFOS-REQ-SYSINT-0004`, `MFOS-REQ-SYSINT-0005`, `MFOS-REQ-SYSINT-0006`, `MFOS-REQ-SYSINT-0018`, `MFOS-REQ-SYSINT-0019`, `MFOS-REQ-SYSINT-0020`.

MFOS defines these execution states:

```text
USER_JOB
USER_SUBSYSTEM
TRUSTED_SERVICE
AUTHORIZED_SERVICE
SUPERVISOR
GUARD
PM_ROOT
```

Meanings:

| ExecutionState | Meaning |
| --- | --- |
| USER_JOB | ordinary job step execution |
| USER_SUBSYSTEM | optional subsystem code without privileged service authority |
| TRUSTED_SERVICE | service with declared endpoints but no arbitrary system authority |
| AUTHORIZED_SERVICE | service or AMF module with explicit AuthorityClass through AMF/securityd |
| SUPERVISOR | nucleus execution context |
| GUARD | High-Assurance Guard context |
| PM_ROOT | PXM partition manager root context |

Rules:

- ExecutionState alone MUST NOT authorize a protected operation.
- A transition into a more privileged ExecutionState MUST occur only through a defined system interface.
- Caller-supplied ExecutionState MUST be ignored.
- ExecutionState transitions MUST be auditable when they grant, revoke, or depend on an AuthorityClass.
- Baseline system integrity MUST NOT claim protection after nucleus compromise or authorized service compromise.
- SUPERVISOR MUST use typed copy-in/copy-out for untrusted buffers.
- GUARD MUST NOT interpret job, dataset, spool, or business policy semantics.
- PM_ROOT MUST NOT interpret MFOS enterprise semantics.
- Hardware mechanisms such as NX, W^X, SMEP, SMAP, CET, PKU, PKS, IOMMU, VMX, SVM, EPT, and NPT MAY enforce parts of an ExecutionState boundary, but they MUST NOT define MFOS authorization semantics.

## 8. Storage Domains

Source IDs: `EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001`, `EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001`, `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `X64-INTEL-001`, `X64-AMD-001`, `X64-LINUX-PKU-001`, `X64-LINUX-CET-001`, `MS-VSM-001`.
Requirement IDs: `MFOS-REQ-SYSINT-0004`, `MFOS-REQ-SYSINT-0007`, `MFOS-REQ-SYSINT-0008`, `MFOS-REQ-SYSINT-0020`.

MFOS defines these software storage domains:

```text
USER_PRIVATE
JOB_SHARED
SERVICE_PRIVATE
SECURITY_ROOT
AUDIT_ROOT
CATALOG_ROOT
SPOOL_ROOT
NUCLEUS_TEXT
NUCLEUS_DATA
DEVICE_DMA
PARTITION_METADATA
```

Rules:

- StorageDomain is not a z/Architecture storage key.
- StorageDomain is a software-defined MFOS classification used for policy, review, testing, and enforcement mapping.
- x64 page tables, NX, W^X, supervisor/user bits, SMEP, SMAP, IOMMU, and optional PKU/PKS/CET MAY enforce parts of this model.
- PKU MUST NOT be used as an instruction-fetch protection mechanism.
- PKU MUST NOT be used as a system integrity root.
- PKS MUST NOT replace Guard.
- DEVICE_DMA memory MUST be isolated by IOMMU for Enterprise-Standalone, Enterprise-PXM, and High-Assurance device assignment.
- NUCLEUS_TEXT MUST be executable and not writable after initialization except through a defined update or patch mechanism.
- SECURITY_ROOT and AUDIT_ROOT require Guard protection only in High-Assurance profile.
- Direct cross-domain pointer use from untrusted subjects is prohibited. Cross-domain transfer MUST use typed handles, typed requests, and bounded copy-in/copy-out.

## 9. Protected Resources

Source IDs: `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001`, `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001`, `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-JES-JOB-FLOW-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001`, `EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001`, `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `EXTREF-IBM-Z-DPM-0001`, `MS-VBS-001`, `MS-VSM-001`.
Requirement IDs: `MFOS-REQ-SYSINT-0001`, `MFOS-REQ-SYSINT-0012`, `MFOS-REQ-SYSINT-0013`, `MFOS-REQ-SYSINT-0014`, `MFOS-REQ-SYSINT-0015`, `MFOS-REQ-SYSINT-0016`, `MFOS-REQ-SYSINT-0017`, `MFOS-REQ-SYSINT-0018`, `MFOS-REQ-SYSINT-0019`.

System integrity applies to these protected resources:

| Resource | Integrity concern |
| --- | --- |
| Principal | forged or escalated identity |
| Group | unauthorized authority aggregation |
| Role | unauthorized operational authority |
| ProgramIdentity | forged executable identity |
| AuthorizedModule | unauthorized extension authority |
| SecurityProfile | policy bypass or corruption |
| SecurityPolicyRoot | root policy rollback, replay, or tamper |
| AuditRecord | evidence omission or forgery |
| AuditChainRoot | audit-chain rollback, replay, or tamper |
| Dataset | unauthorized data access or mutation |
| CatalogEntry | unauthorized name/location/attribute mutation |
| Volume | unauthorized allocation or exposure |
| SpoolEntry | unauthorized browse, purge, export, or tamper |
| Job | forged work identity or status |
| JobStep | forged execution result |
| OperatorCommand | unauthorized system operation |
| WorkloadPolicy | unauthorized scheduling influence |
| AMFRegistry | unauthorized extension approval |
| UpdateArtifact | malicious code or policy update |
| UpdateMetadata | rollback/freeze/mix-and-match |
| Partition | isolation and lifecycle control |
| ActivationProfile | unauthorized partition configuration |
| DeviceAssignment | DMA or interrupt boundary bypass |
| GuardRoot | High-Assurance root tamper |
| SvcTable | service entry tamper |
| PageTableRoot | unauthorized executable or writable mapping |

Rules:

- A protected resource MUST have an owning component.
- A protected resource MUST have authorization rules.
- A protected resource MUST have audit obligations.
- A protected resource MUST have failure modes.
- A protected resource MUST NOT be operated through an untyped raw pointer from user space.
- Protected resource handles MUST bind the subject, object, operation, policy version, generation where applicable, and expiry where applicable.
- A protected resource deny decision with an audit obligation MUST be recorded according to the relevant audit-before-return rule before a final caller-visible result is returned.

## 10. System Interfaces

Source IDs: `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001`, `EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001`, `EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001`, `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-JES-JOB-FLOW-0001`, `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `EXTREF-IBM-Z-DPM-0001`, `MS-VBS-001`, `MS-VSM-001`, `FBVBS-001`.
Requirement IDs: `MFOS-REQ-SYSINT-0002`, `MFOS-REQ-SYSINT-0003`, `MFOS-REQ-SYSINT-0007`, `MFOS-REQ-SYSINT-0008`, `MFOS-REQ-SYSINT-0009`, `MFOS-REQ-SYSINT-0010`, `MFOS-REQ-SYSINT-0011`, `MFOS-REQ-SYSINT-0012`, `MFOS-REQ-SYSINT-0013`, `MFOS-REQ-SYSINT-0016`, `MFOS-REQ-SYSINT-0018`, `MFOS-REQ-SYSINT-0019`.

System integrity applies to these system interfaces:

| Interface | Owner | Integrity requirement | Source IDs | Requirement IDs |
| --- | --- | --- | --- | --- |
| SVC | nucleus | typed handles, bounded copy-in/copy-out, no caller identity trust | `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001` | `MFOS-REQ-SYSINT-0003`, `MFOS-REQ-SYSINT-0007`, `MFOS-REQ-SYSINT-0008`, `MFOS-REQ-SYSINT-0009` |
| PCALL | nucleus/services | typed endpoint, typed request, propagated audit obligation | `EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001`, `EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001` | `MFOS-REQ-SYSINT-0003`, `MFOS-REQ-SYSINT-0009` |
| PXM_CALL | PXM | partition-only operation scope | `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `EXTREF-IBM-Z-DPM-0001` | `MFOS-REQ-SYSINT-0003`, `MFOS-REQ-SYSINT-0018` |
| GUARD_CALL | Guard | root-object-only operation scope | `MS-VBS-001`, `MS-VSM-001` | `MFOS-REQ-SYSINT-0006`, `MFOS-REQ-SYSINT-0019` |
| OperatorCommand | operatord | parse, authorize, audit, confirm where required | `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001` | `MFOS-REQ-SYSINT-0003`, `MFOS-REQ-SYSINT-0012`, `MFOS-REQ-SYSINT-0013`, `MFOS-REQ-SYSINT-0016` |
| DatasetOpen | datasetd | catalog resolve, securityd authorize, handle bind | `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001` | `MFOS-REQ-SYSINT-0003`, `MFOS-REQ-SYSINT-0012`, `MFOS-REQ-SYSINT-0014` |
| CatalogTransaction | catalogd | authorize, journal, commit, audit | `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001` | `MFOS-REQ-SYSINT-0003`, `MFOS-REQ-SYSINT-0012`, `MFOS-REQ-SYSINT-0013` |
| JobSubmit | jobd | establish submitter/effective principal, audit | `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-JES-JOB-FLOW-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001` | `MFOS-REQ-SYSINT-0003`, `MFOS-REQ-SYSINT-0015` |
| JobCancel | jobd | command authority and audit | `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001` | `MFOS-REQ-SYSINT-0003`, `MFOS-REQ-SYSINT-0012`, `MFOS-REQ-SYSINT-0013` |
| SpoolBrowse | spoold | protected read decision | `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001` | `MFOS-REQ-SYSINT-0003`, `MFOS-REQ-SYSINT-0012` |
| SpoolPurge | spoold | destructive decision and retention check | `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001` | `MFOS-REQ-SYSINT-0003`, `MFOS-REQ-SYSINT-0012`, `MFOS-REQ-SYSINT-0013` |
| SecurityPolicyUpdate | securityd | transaction, version, rollback control, audit | `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001`, `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001` | `MFOS-REQ-SYSINT-0012`, `MFOS-REQ-SYSINT-0013` |
| AuditQuery | auditd | query authorization and redaction | `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001` | `MFOS-REQ-SYSINT-0012`, `MFOS-REQ-SYSINT-0013` |
| AMFLoad | amfd | signature, manifest, revocation, securityd, Guard where required | `EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `MS-VBS-001` | `MFOS-REQ-SYSINT-0004`, `MFOS-REQ-SYSINT-0017`, `MFOS-REQ-SYSINT-0019` |
| UpdateActivation | uvsd | metadata verification, anti-rollback, audit | `FBVBS-001`, `NIST-160-001`, `TCG-001` | `MFOS-REQ-SYSINT-0010`, `MFOS-REQ-SYSINT-0011`, `MFOS-REQ-SYSINT-0013` |
| DeviceAssignment | PXM | IOMMU, interrupt remap, teardown checklist | `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `EXTREF-IBM-Z-DPM-0001`, `X64-INTEL-001`, `X64-AMD-001` | `MFOS-REQ-SYSINT-0018`, `MFOS-REQ-SYSINT-0020` |
| PartitionLifecycleTransition | PXM | state-machine enforcement and audit | `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `EXTREF-IBM-Z-DPM-0001`, `FBVBS-001` | `MFOS-REQ-SYSINT-0018` |

Rules:

- Every system interface MUST reject invalid parameters.
- Every system interface MUST distinguish `UNSUPPORTED` from `SPEC_GAP`.
- Every system interface MUST fail closed for authorization ambiguity.
- Every security-sensitive system interface MUST have negative tests.
- Every security-sensitive system interface MUST establish the trusted caller context before parsing caller-supplied identity fields.
- Every protected-resource operation MUST obtain a securityd decision for the exact subject, object, operation, context, and policy_version before creating handles, changing state, exposing contents, or assigning devices.
- Every audit-required deny MUST be submitted to auditd before the caller receives the final denial result, unless the profile-specific audit failure policy transfers the system into recovery-only mode.
- `MFOS_ERR_UNSUPPORTED` and `MFOS_ERR_SPEC_GAP` MUST be terminal for the requested operation: no weaker fallback operation, partial result, or implicit success is allowed.
- If securityd or auditd is unavailable for an operation that requires it, the owning component MUST fail closed or enter the applicable recovery-only mode; it MUST NOT locally decide that the operation is safe.

### 10.1 Prohibited Circumventions

The following paths are prohibited system integrity circumventions. This table is normative for the front-half system integrity model and does not add implementation permission.

| Prohibited path | Source IDs | Requirement IDs | Required behavior |
| --- | --- | --- | --- |
| Caller supplies or forges principal, job identity, ExecutionState, AuthorityClass, or policy version | `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001` | `MFOS-REQ-SYSINT-0001`, `MFOS-REQ-SYSINT-0004`, `MFOS-REQ-SYSINT-0012` | reject or fail closed; do not create protected handles |
| Supervisor, service, SVC, or PCALL code dereferences untrusted caller pointers directly | `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001`, `EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001` | `MFOS-REQ-SYSINT-0007`, `MFOS-REQ-SYSINT-0008`, `MFOS-REQ-SYSINT-0009` | use typed copy-in/copy-out or reject |
| Component other than securityd makes the final authorization decision for a protected resource | `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001`, `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001` | `MFOS-REQ-SYSINT-0012` | reject final allow; return a deny or specification-gap result according to interface rules |
| Required audit evidence is replaced by debug output, spool output, or ordinary logs | `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001`, `FBVBS-001` | `MFOS-REQ-SYSINT-0013` | fail closed when audit obligation cannot be satisfied |
| Dataset, catalog, spool, job, or operator resource is accessed using an unbound or stale handle | `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001`, `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001` | `MFOS-REQ-SYSINT-0014`, `MFOS-REQ-SYSINT-0015`, `MFOS-REQ-SYSINT-0016` | reject and audit where required |
| AMF load path grants administrator authority or executable extension authority without complete AMF checks | `EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `MS-VBS-001` | `MFOS-REQ-SYSINT-0004`, `MFOS-REQ-SYSINT-0017` | fail closed; AMF-disabled mode returns `MFOS_ERR_UNSUPPORTED` |
| PXM interprets dataset, job, spool, operator, or security policy semantics | `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `EXTREF-IBM-Z-DPM-0001` | `MFOS-REQ-SYSINT-0018` | reject as out of scope for PXM |
| Guard interprets dataset, job, spool, operator, or business policy semantics | `MS-VBS-001`, `MS-VSM-001` | `MFOS-REQ-SYSINT-0019` | reject as out of scope for Guard |
| PKU, PKS, CET, SMEP, SMAP, NX, W^X, IOMMU, VMX, SVM, EPT, or NPT is treated as a substitute for securityd authorization or auditd evidence | `X64-INTEL-001`, `X64-AMD-001`, `X64-LINUX-PKU-001`, `X64-LINUX-CET-001` | `MFOS-REQ-SYSINT-0020` | reject the claim or design change; keep hardware as enforcement aid only |
| Undefined or unsupported interface behavior returns a completed operation result | `FBVBS-001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001` | `MFOS-REQ-SYSINT-0010`, `MFOS-REQ-SYSINT-0011` | return `MFOS_ERR_UNSUPPORTED` or `MFOS_ERR_SPEC_GAP` and fail closed |

## 11. SVC Rules

SVC caller:

- USER_JOB
- USER_SUBSYSTEM
- TRUSTED_SERVICE

SVC callee:

- MFOS nucleus

Required SVC properties:

- caller identity from scheduler context
- no caller-supplied identity accepted
- typed object handles
- object handle lookup validates handle type, generation, subject binding, operation, and expiry before use
- user pointers treated as opaque until validated
- bounded copy-in/copy-out only
- input lengths checked before allocation or copy
- output lengths checked before writeback
- unsupported call returns `MFOS_ERR_UNSUPPORTED`
- undefined call returns `MFOS_ERR_SPEC_GAP`
- audit obligation propagated
- no success without required audit
- no state mutation before parameter validation and authorization preconditions complete
- no output buffer writeback until the operation has reached a committed result state

SVC MUST NOT:

- dereference user pointers directly in supervisor context
- trust user-provided effective principal
- permit untyped kernel object handle forging
- silently downgrade to a weaker operation
- return success for missing implementations
- convert `MFOS_ERR_UNSUPPORTED`, `MFOS_ERR_SPEC_GAP`, `MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE`, or `MFOS_ERR_POLICY_DENIED` into `MFOS_OK`
- create a protected resource handle unless the owning service or nucleus path has a matching securityd decision and required audit obligation state

## 12. PCALL Rules

PCALL caller:

- trusted service
- nucleus-mediated caller
- authorized service where endpoint policy permits

PCALL callee:

- typed trusted service endpoint

Required PCALL properties:

- typed endpoint
- typed request
- endpoint registry entry with declared operations, AuthorityClass requirements, and audit obligations
- bounded payload
- caller principal included from trusted context
- job identity included where applicable
- ProgramIdentity included where applicable
- policy_version included where applicable
- securityd remains final PDP for protected resources
- audit obligation propagated
- no arbitrary cross-address-space pointer access
- sealed or copied buffers only; raw caller address spaces are not shared with callees
- callee response includes explicit decision/result and reason code; silent fallback is not allowed

PCALL MUST NOT:

- expose raw service memory to caller
- accept caller-forged identity
- let callee invent final authorization for protected resources
- bypass auditd obligation
- let a trusted service become a shadow policy decision point for Dataset, CatalogEntry, SpoolEntry, Job, OperatorCommand, AMFRegistry, Partition, DeviceAssignment, or GuardRoot
- proceed when the endpoint registration, payload type, policy_version, or audit obligation is missing or ambiguous

## 13. AMF Rules

AMF is the Authorized Module Facility (`EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`).

AMF phase rule:

- In AMF-disabled mode, every AMF load request MUST return `MFOS_ERR_UNSUPPORTED`.
- In AMF-disabled mode, amfd MUST NOT map executable pages, create an AMF registry entry, enter `AUTHORIZED_SERVICE`, or grant any AuthorityClass.
- In AMF-disabled mode, the unsupported load attempt is auditable; missing audit handling MUST fail closed according to the profile audit failure policy.
- Test-only AMF behavior, if later specified, MUST be explicitly marked non-production and MUST NOT create a production AMF claim.
- Production AMF load is outside Phase 1 and remains blocked until the AMF specification, requirements, negative tests, evidence paths, and pack gate are complete.

AMF module load requires:

- signed artifact
- measured artifact
- valid manifest
- immutable catalog entry or approved artifact store
- explicit authority class
- explicit ABI
- revocation check
- security epoch check
- securityd authorization
- audit obligation handling
- Guard approval in High-Assurance profile

AMF module ABI rules:

- no arbitrary pointer trust
- copy-in/copy-out only
- typed requests
- bounded payloads
- explicit AuthorityClass
- no audit-disable authority
- revocation support
- policy version binding

AMF MUST NOT:

- mean root privilege
- mean administrator privilege
- grant broad kernel extension authority by default
- load from mutable unapproved datasets
- succeed on invalid signature
- succeed on revoked signer or digest
- succeed when manifest, security epoch, policy_version, AuthorityClass, audit obligation, or immutable artifact binding is missing
- bypass Guard approval when High-Assurance requires it
- write directly to securityd policy roots, auditd chain roots, catalog roots, SVC tables, page table roots, or Guard roots except through an explicitly specified interface and AuthorityClass
- use writable-and-executable mappings or create executable mappings before verification, authorization, and audit preconditions are complete

## 14. securityd Authority

securityd is the central policy decision point for protected resource access.

securityd decision input:

```text
subject
object
operation
context
policy_version
```

Required decision metadata:

```text
decision_id
decision_time
policy_version
obligations_hash
valid_until
reason_code
```

securityd decision result:

```text
ALLOW
DENY
ALLOW_WITH_AUDIT
REQUIRE_MFA
REQUIRE_DUAL_CONTROL
REQUIRE_BREAK_GLASS
REQUIRE_GUARD_APPROVAL
REQUIRE_OPERATOR_CONFIRMATION
UNSUPPORTED
SPEC_GAP
```

Rules:

- securityd MUST generate audit obligations.
- securityd MUST version policies.
- securityd MUST support transaction semantics for policy updates.
- securityd MUST fail closed on policy corruption.
- securityd MUST fail closed on ambiguous policy.
- Other services MUST NOT make final authorization decisions for protected resources.
- A decision is valid only for the exact subject, object, operation, context, policy_version, and validity interval recorded in the decision.
- Services MUST treat `DENY`, `UNSUPPORTED`, `SPEC_GAP`, expired decisions, policy_version mismatch, and missing obligations as non-authorizing results.
- `REQUIRE_MFA`, `REQUIRE_DUAL_CONTROL`, `REQUIRE_BREAK_GLASS`, `REQUIRE_GUARD_APPROVAL`, and `REQUIRE_OPERATOR_CONFIRMATION` are not authorization to execute; they are pending states until the required control is completed and audited.
- securityd unavailability MUST NOT be interpreted by callers as allow-by-default.
- securityd MUST NOT own audit record storage, catalog transaction state, spool contents, job scheduling policy, PXM partition state, or Guard root transitions.

## 15. auditd Authority

auditd is the evidence service.

Audit trust levels:

```text
AUD-L0 diagnostic console output
AUD-L1 local auditd append log
AUD-L2 hash-chained local audit
AUD-L3 remote exported audit
AUD-L4 Guard-sealed audit root
AUD-L5 external/OOB authoritative audit path
```

Rules:

- auditd MUST validate record schema.
- auditd MUST support append-only record streams.
- auditd SHOULD support hash chaining in Baseline and MUST support it in Enterprise-Standalone, Enterprise-PXM, and High-Assurance.
- DENY decisions MUST be audited before caller receives final result unless the profile-specific audit failure policy enters recovery.
- auditd unavailable MUST trigger profile-specific fail-closed behavior.
- spool output MUST NOT be treated as audit evidence.
- debug logs MUST NOT be treated as audit evidence.
- Required audit records MUST include correlation_id, subject, object, operation, decision/result, reason_code, policy_version, and schema_version.
- Security-sensitive audit records SHOULD include decision_id when the event is tied to a securityd decision.
- Audit write failure for a required security event MUST prevent the protected operation from completing, except for explicitly marked recovery-only operations.
- auditd MUST NOT make final authorization decisions; audit query authorization still goes through securityd.
- Audit redaction MUST NOT remove fields required to verify denial-before-return, policy_version, or subject/object binding.

## 16. Dataset, Catalog, and Spool Rules

Dataset rules:

- datasetd MUST NOT issue persistent dataset handles without catalogd resolution.
- datasetd MUST NOT issue protected dataset handles without securityd authorization.
- dataset handles MUST bind subject, operation, policy_version, catalog generation, and expiry.
- stale handles MUST be rejected.
- retention policy MUST affect purge/delete operations.
- datasetd MUST NOT open, read, write, delete, export, or allocate a protected dataset through a POSIX file fallback or ordinary file wrapper.
- datasetd MUST NOT create a handle when catalogd returns uncommitted, rolled-back, recovery-pending, or integrity-failed catalog state.
- datasetd MUST record or propagate the audit obligation for open allow, open deny, stale handle, policy mismatch, and destructive dataset operations.
- dataset handle creation MUST occur after catalog resolution, securityd authorization, and required audit obligation setup.

Catalog rules:

- catalogd MUST resolve only committed catalog entries.
- catalogd MUST journal transactions before commit.
- catalogd MUST reject invalid DSNs.
- system dataset mutation MUST require explicit authority.
- immutable catalog entries MUST reject mutation except through defined update/recovery workflows.
- catalogd MUST fail closed on ambiguous transaction state, journal checksum mismatch, generation mismatch, or recovery-in-progress state.
- catalogd MUST NOT expose dataset location metadata to unauthorized callers.
- catalogd recovery MUST complete or quarantine incomplete entries before normal resolution resumes.

Spool rules:

- spool entries are protected resources.
- browse, purge, and export MUST go through securityd.
- purge MUST respect retention.
- SYSOUT capture MUST bind owner, job_id, output_class, and security profile.
- spoold MUST NOT return spool content before authorization and required redaction policy are resolved.
- spoold MUST audit browse denials before returning the final denial result.
- spoold purge is destructive and MUST require explicit AuthorityClass, retention check, and audit obligation handling.
- spool output MUST NOT be used as replacement evidence for auditd records.

## 17. Operator Command Rules

Operator console is a system interface, not a root shell.

Required command lifecycle:

```text
PARSE_COMMAND
IDENTIFY_COMMAND
RESOLVE_TARGET
AUTHORIZE
REQUIRE_CONFIRMATION?
REQUIRE_DUAL_CONTROL?
AUDIT_INTENT?
EXECUTE
AUDIT_RESULT
DISPLAY_RESULT
```

Rules:

- Every operator command MUST have command_id.
- Every operator command MUST have AuthorityClass.
- Every operator command MUST be authorized through securityd.
- Every operator command MUST emit audit records.
- Destructive commands MUST support confirmation or dual-control.
- Automation hooks MUST NOT bypass authority or audit.
- Emergency mode MUST require reason, operator identity, expiry, and audit.
- Operator commands MUST NOT run through a general-purpose root shell or bypass the command registry.
- Command parsing and target resolution MUST complete before authorization; execution MUST NOT start while the target is ambiguous.
- A denied operator command MUST be audited before the denial is displayed unless the profile-specific audit failure policy enters recovery-only mode.
- Destructive commands MUST audit intent before execution and audit result after execution where auditd is available.
- `REQUIRE_OPERATOR_CONFIRMATION` and `REQUIRE_DUAL_CONTROL` are pending states, not permission to execute.
- Automation hooks MUST run under an explicit ProgramIdentity and AuthorityClass and MUST be subject to the same securityd and auditd requirements as interactive operators.

## 18. Partition-Aware Requirements

MFOS is always partition-aware at the API and object model level.

Baseline MAY use an implicit single partition backend.

PXM responsibilities:

- partition lifecycle
- activation profile
- logical CPU assignment
- memory domain assignment
- IOMMU domain setup
- interrupt remapping
- device assignment
- device teardown
- partition audit
- recovery partition coordination

PXM MUST NOT:

- parse JCL-like job syntax
- decide dataset access
- interpret securityd profiles
- manage spool content
- schedule jobs
- interpret workload policy service classes
- interpret operator business commands
- own securityd policy
- own auditd schema semantics
- inspect dataset names, job classes, spool classes, operator command verbs, or security profile contents to decide partition operations
- translate MFOS enterprise authorization failures into partition success
- provide a backdoor path to access MFOS protected resources from a side partition

Partition state machine:

```text
DEFINED
MEASURED
LOADED
ACTIVATED
RUNNABLE
RUNNING
QUIESCED
FAULTED
DEACTIVATED
DESTROYED
```

Critical invariant:

```text
Partition memory cannot be reassigned until all CPU mappings,
IOMMU mappings, interrupt routes, and device ownership records
are revoked and the memory is zeroed.
```

PXM fail-closed rules:

- PXM_CALL MUST accept only partition lifecycle, activation profile, CPU, memory, device, interrupt, IOMMU, audit, and recovery operations.
- Device assignment MUST fail closed when IOMMU domain setup, interrupt remapping, ownership record creation, or audit obligation handling is incomplete.
- Device teardown MUST fail closed until DMA is quiesced, interrupts are blocked or remapped away, device ownership is revoked, dirty state is reconciled, and assigned memory is zeroed or quarantined.
- A side partition gateway MUST use MFOS gateway policy and securityd decisions for MFOS resource exchange; PXM MUST only enforce partition/device isolation for that gateway.

## 19. High-Assurance Guard Extensions

PXM Guard is mandatory only in High-Assurance profile.

Guard protects:

- `GUARD_ROOT_SECURITY_POLICY`
- `GUARD_ROOT_AUDIT_CHAIN`
- `GUARD_ROOT_AMF_REGISTRY`
- `GUARD_ROOT_SVC_TABLE`
- `GUARD_ROOT_NUCLEUS_TEXT`
- `GUARD_ROOT_EXECUTABLE_MAPPING_POLICY`
- `GUARD_ROOT_PAGE_TABLE_POLICY`
- `GUARD_ROOT_ACTIVATION_PROFILE`
- `GUARD_ROOT_EMERGENCY_STATE`
- `GUARD_ROOT_UPDATE_POLICY`

Guard does not protect or interpret:

- ordinary dataset contents
- job scheduling semantics
- spool formatting
- operator UI rendering
- POSIX subsystem behavior
- Linux desktop applications
- normal business policy interpretation

Guard calls:

```text
GUARD_MEASURE_COMPONENT(component_id, digest, metadata)
GUARD_SEAL_ROOT(root_type, digest, version)
GUARD_VERIFY_ROOT(root_type, digest, version)
GUARD_AUTHORIZE_EXEC_MAPPING(page_range, code_identity, policy_version)
GUARD_AUTHORIZE_AMF_LOAD(module_id, digest, signer, authority_class)
GUARD_VERIFY_SVC_TABLE(table_digest)
GUARD_APPEND_AUDIT_ROOT(record_seq, chain_hash)
GUARD_ENTER_EMERGENCY_MODE(reason, operator_identity)
GUARD_EXIT_EMERGENCY_MODE(operator_identity)
GUARD_RELEASE_SECRET(secret_id, measurement_context)
GUARD_ATTEST(nonce, requested_claims)
```

Rules:

- Guard MUST remain small.
- Guard MUST protect root objects only.
- Guard MUST fail secure on root mismatch.
- Guard MUST audit root transitions through auditd and Guard root state.
- Guard MUST NOT become a job, dataset, spool, or policy engine.
- Guard MUST NOT parse JCL, DSN grammar, spool formats, operator command grammar, security profile language, workload policy, POSIX paths, or Linux desktop metadata.
- Guard decisions MUST be limited to root object measurement, sealing, verification, executable mapping authorization, AMF registry authorization, SVC table verification, audit root append, emergency-state root transition, secret release, and attestation.
- Guard unavailability in a profile that requires Guard MUST block the protected operation or enter recovery-only mode; callers MUST NOT fall back to Baseline semantics for a High-Assurance root claim.
- Guard approval is not a replacement for securityd authorization or auditd evidence unless a specific Guard root transition is the protected operation.
- Guard root mismatch MUST produce lockdown, boot denial, or recovery-only behavior; it MUST NOT produce a best-effort warning followed by normal operation.

## 20. Failure Modes

Failure handling is part of the integrity boundary (`EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `FBVBS-001`). A failure path that creates
a handle, commits a catalog entry, executes an operator command, maps executable code (`EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`),
or suppresses an audit obligation is an integrity failure even if it later
returns an error (`EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `FBVBS-001`).

### 20.1 `UNSUPPORTED` vs `SPEC_GAP`

| Classification | Meaning | Required behavior | Side effects allowed | Registry tests |
| --- | --- | --- | --- | --- |
| `UNSUPPORTED` | The behavior is defined by this specification or a referenced split spec, but this profile or implementation does not provide it. | Return `MFOS_ERR_UNSUPPORTED`; fail closed; emit audit when the request is security-sensitive or security-relevant. | No protected-resource handle, executable mapping, registry entry, authority transition, committed mutation, or partition state change. | `TEST-MFOS-SYSINT-UNSUPPORTED-ERROR-0010`, `NEG-MFOS-SYSINT-UNSUPPORTED-SUCCESS-0010`, `NEG-MFOS-AMF-LOAD-DISABLED-0021` |
| `SPEC_GAP` | No canonical behavior, ABI, state machine, or error mapping exists yet. | Return `MFOS_ERR_SPEC_GAP` before side effects, or block implementation at the pre-implementation gate. | No runtime semantics may be invented; no protected operation may complete. | `TEST-MFOS-SYSINT-SPEC-GAP-ERROR-0011`, `NEG-MFOS-SYSINT-SPEC-GAP-SUCCESS-0011` |

`UNSUPPORTED` MUST NOT be used to hide an undefined behavior. `SPEC_GAP` MUST
NOT be used for a defined but disabled feature such as AMF-disabled production
load. AMF-disabled production load is `UNSUPPORTED`.

### 20.2 General Failure Table

| Failure mode | Required behavior | Primary error or gate | Registry tests |
| --- | --- | --- | --- |
| unauthenticated subject | deny and audit where possible | `MFOS_ERR_UNAUTHENTICATED` | `NEG-MFOS-DATASET-0001`, `NEG-MFOS-SYSINT-DATASET-BYPASS-0001` |
| missing effective principal | deny before resource open | `MFOS_ERR_UNAUTHENTICATED` or `MFOS_ERR_INVALID_PARAMETER` | `NEG-MFOS-SYSINT-JOB-NO-PRINCIPAL-0015` |
| forged caller identity | ignore caller-supplied identity and use trusted context | `MFOS_ERR_UNAUTHORIZED` | `NEG-MFOS-SYSINT-SVC-FORGED-IDENTITY-0009` |
| policy unavailable or corrupted | fail closed except recovery-only operations | `MFOS_ERR_POLICY_DENIED` or recovery gate | `NEG-MFOS-AUTH-PDP-BYPASS-0001` |
| auditd unavailable | apply profile-specific audit failure policy | `MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE` or recovery gate | `NEG-MFOS-AUDIT-UNAVAILABLE-0005`, `TEST-MFOS-AUDIT-RECOVERY-MODE-0005` |
| unsupported system interface | return `MFOS_ERR_UNSUPPORTED`; no protected side effect | `MFOS_ERR_UNSUPPORTED` | `NEG-MFOS-SYSINT-UNSUPPORTED-SUCCESS-0010` |
| specification gap | return `MFOS_ERR_SPEC_GAP` or block implementation | `MFOS_ERR_SPEC_GAP` or pre-implementation gate | `NEG-MFOS-SYSINT-SPEC-GAP-SUCCESS-0011` |
| invalid user pointer | reject without dereference or partial authority | `MFOS_ERR_INVALID_PARAMETER` | `NEG-MFOS-SYSINT-RAW-POINTER-0007` |
| copy-in length overflow | reject before allocation, copy, or endpoint dispatch | `MFOS_ERR_INVALID_PARAMETER` | `NEG-MFOS-SYSINT-COPY-OVERFLOW-0008`, `NEG-MFOS-SYSINT-PCALL-OVERSIZE-0008` |
| stale handle | reject and audit where security-relevant | `MFOS_ERR_STALE_HANDLE` | `NEG-MFOS-SYSINT-DATASET-HANDLE-BINDING-0014`, `NEG-MFOS-DATASET-STALE-HANDLE-0001` |
| policy version mismatch | reject and audit | `MFOS_ERR_POLICY_VERSION_MISMATCH` | `NEG-MFOS-DATASET-POLICY-VERSION-0001` |
| catalog not found | reject without dataset handle | `MFOS_ERR_CATALOG_NOT_FOUND` | `NEG-MFOS-DATASET-UNAUTHORIZED-OPEN-0002` |
| catalog transaction crash | recover journal before serving committed state | recovery gate | `NEG-MFOS-CATALOG-UNCOMMITTED-0002`, `NEG-MFOS-CATALOG-PARTIAL-JOURNAL-0002` |
| invalid DSN | reject before authorization side effects | `MFOS_ERR_INVALID_DSN` | `NEG-MFOS-DATASET-UNAUTHORIZED-OPEN-0002` |
| AMF invalid signature or manifest | fail closed and audit | `MFOS_ERR_AMF_SIGNATURE_INVALID` or `MFOS_ERR_INVALID_PARAMETER` | `NEG-MFOS-SYSINT-AMF-BOUNDARY-0017` |
| AMF revoked signer or digest | fail closed and audit | `MFOS_ERR_AMF_REVOKED` | `NEG-MFOS-SYSINT-AMF-BOUNDARY-0017` |
| AMF load while AMF-disabled | no executable mapping, no registry entry, no authority transition | `MFOS_ERR_UNSUPPORTED` | `NEG-MFOS-AMF-LOAD-DISABLED-0021` |
| SVC table mismatch in High-Assurance | lockdown or panic-equivalent recovery path | Guard lockdown gate | `NEG-MFOS-SYSINT-GUARD-SCOPE-0019` |
| Guard required but unavailable | deny boot or enter recovery, profile-dependent | boot/recovery gate | `NEG-MFOS-SYSINT-HA-CLAIM-NO-GUARD-0006` |
| partition invalid transition | reject transition and audit | `MFOS_ERR_PARTITION_INVALID_STATE` | `TEST-MFOS-SYSINT-PXM-LIFECYCLE-0018` |
| device teardown incomplete | reject reassignment | `MFOS_ERR_DEVICE_TEARDOWN_INCOMPLETE` | `NEG-MFOS-PARTITION-DEVICE-TEARDOWN-0006` |

### 20.3 Invalid Transition Table

| Interface or lifecycle | Invalid transition | Required response | Registry tests |
| --- | --- | --- | --- |
| SVC | user caller provides subject identity and requests a protected operation | ignore supplied identity; authorize only trusted scheduler context; deny if trusted context is insufficient | `NEG-MFOS-SYSINT-SVC-FORGED-IDENTITY-0009`, `NEG-MFOS-SYSINT-SVC-BYPASS-0001` |
| SVC/PCALL | raw pointer or oversized payload reaches privileged dereference | reject before dereference, allocation, endpoint dispatch, or audit suppression | `NEG-MFOS-SYSINT-RAW-POINTER-0007`, `NEG-MFOS-SYSINT-COPY-OVERFLOW-0008`, `NEG-MFOS-SYSINT-PCALL-OVERSIZE-0008` |
| DatasetOpen | DENY or missing principal transitions to handle creation | no handle; denial is auditable before final result according to profile policy | `NEG-MFOS-DATASET-DENY-NO-HANDLE-0002`, `NEG-MFOS-DATASET-DENY-WITHOUT-AUDIT-0006`, `NEG-MFOS-SYSINT-DATASET-BYPASS-0001` |
| CatalogTransaction | uncommitted or rolled-back entry transitions to resolved dataset location | reject resolve; recovery must settle journal before committed state is served | `NEG-MFOS-CATALOG-UNCOMMITTED-0002`, `NEG-MFOS-CATALOG-ROLLED-BACK-0002`, `NEG-MFOS-CATALOG-PARTIAL-JOURNAL-0002` |
| OperatorCommand | destructive command skips confirmation or dual-control | command does not execute; audit obligation remains | `NEG-MFOS-SYSINT-OPERATOR-DESTRUCTIVE-NO-CONFIRM-0016` |
| OperatorCommand | privileged root-shell style operation bypasses command grammar | reject; operator console remains a governed system interface | `NEG-MFOS-SYSINT-OPERATOR-ROOT-SHELL-0016` |
| AMFLoad | disabled, invalid, revoked, or unaudited module transitions to executable mapping or authorized state | fail closed; no RX mapping, AMF registry entry, or authority transition | `NEG-MFOS-SYSINT-AMF-BOUNDARY-0017`, `NEG-MFOS-AMF-LOAD-DISABLED-0021` |
| UpdateActivation | rollback, freeze, or mix-and-match metadata transitions to staged or activated update | reject before activation; audit security-relevant failure | `NEG-MFOS-UPDATE-ROLLBACK-0004`, `NEG-MFOS-UPDATE-FREEZE-0005`, `NEG-MFOS-UPDATE-MIXMATCH-0006` |
| PXM_CALL | partition manager receives MFOS enterprise policy operation | reject; PXM remains partition lifecycle and isolation only | `NEG-MFOS-SYSINT-PXM-SEMANTICS-0018` |
| DeviceAssignment | reassignment occurs before CPU mappings, IOMMU mappings, interrupt routes, ownership, and zeroing are complete | reject reassignment | `NEG-MFOS-PARTITION-DEVICE-TEARDOWN-0006`, `NEG-MFOS-PARTITION-MEMORY-BEFORE-ZERO-0017` |
| GUARD_CALL | Guard receives job, dataset, spool, or business policy operation | reject; Guard remains selected root-object protection only | `NEG-MFOS-SYSINT-GUARD-SCOPE-0019` |
| Hardware enforcement | PKU/PKS/CET/IOMMU claim substitutes for authorization or audit | architecture review fails; implementation remains blocked | `NEG-MFOS-SYSINT-HW-OVERCLAIM-0020`, `NEG-MFOS-SYSINT-PKU-STORAGE-KEY-0020` |

Boot failure rules:

- auditd start failure in Baseline: enter operator recovery mode only; normal operations MUST NOT start.
- auditd start failure in Enterprise-Standalone: enter operator recovery mode; security operations MUST fail closed.
- auditd start failure in Enterprise-PXM: enter operator recovery mode; security and partition operations MUST fail closed.
- auditd start failure in High-Assurance: boot MUST stop or enter recovery mode.
- securityd start failure in all profiles: operator recovery mode only.
- Guard required but unavailable in High-Assurance: boot denied or recovery mode only.

Baseline recovery mode MUST NOT allow job submit, ordinary dataset open, policy (`EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`)
update, AMF load, update activation, partition device assignment, or operator
destructive commands. Recovery dataset access, if any, MUST be explicitly (`EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`)
marked recovery-only and later reconciled with auditd.

## 21. Formal Invariants

| Invariant ID | Statement | Requirement refs | Registry tests |
| --- | --- | --- | --- |
| INV-SI-001 | An unauthorized subject cannot obtain a protected resource handle. | `MFOS-REQ-SYSINT-0001`, `MFOS-REQ-SYSINT-0012`, `MFOS-REQ-SYSINT-0014` | `NEG-MFOS-SYSINT-DATASET-BYPASS-0001`, `NEG-MFOS-SYSINT-DATASET-HANDLE-BINDING-0014` |
| INV-SI-002 | A protected resource handle is valid only for the subject, object, operation, context, policy_version, generation, and expiry for which it was created. | `MFOS-REQ-SYSINT-0014` | `NEG-MFOS-SYSINT-DATASET-HANDLE-BINDING-0014`, `NEG-MFOS-DATASET-STALE-HANDLE-0001` |
| INV-SI-003 | securityd is the final policy decision point for protected resource access. | `MFOS-REQ-SYSINT-0012` | `NEG-MFOS-AUTH-PDP-BYPASS-0001`, `NEG-MFOS-SYSINT-PXM-SEMANTICS-0018` |
| INV-SI-004 | DENY decisions are auditable before the caller receives final result, subject to profile-specific audit failure policy. | `MFOS-REQ-SYSINT-0013`, `MFOS-REQ-AUDIT-0002` | `NEG-MFOS-DATASET-DENY-WITHOUT-AUDIT-0006`, `NEG-MFOS-AUDIT-DENY-BEFORE-RETURN-0002` |
| INV-SI-005 | SVC and PCALL do not trust caller-supplied identity or raw pointers. | `MFOS-REQ-SYSINT-0007`, `MFOS-REQ-SYSINT-0008`, `MFOS-REQ-SYSINT-0009` | `NEG-MFOS-SYSINT-RAW-POINTER-0007`, `NEG-MFOS-SYSINT-SVC-FORGED-IDENTITY-0009`, `NEG-MFOS-SYSINT-PCALL-OVERSIZE-0008` |
| INV-SI-006 | `UNSUPPORTED` and `SPEC_GAP` operations cannot complete protected operations. | `MFOS-REQ-SYSINT-0010`, `MFOS-REQ-SYSINT-0011` | `NEG-MFOS-SYSINT-UNSUPPORTED-SUCCESS-0010`, `NEG-MFOS-SYSINT-SPEC-GAP-SUCCESS-0011` |
| INV-SI-007 | AMF module load cannot reach READY unless signature, manifest, revocation, catalog/artifact, securityd, audit, and profile-specific Guard checks pass. | `MFOS-REQ-SYSINT-0017` | `NEG-MFOS-SYSINT-AMF-BOUNDARY-0017`, `NEG-MFOS-AMF-LOAD-DISABLED-0021` |
| INV-SI-008 | PXM cannot interpret MFOS enterprise semantics. | `MFOS-REQ-SYSINT-0018` | `NEG-MFOS-SYSINT-PXM-SEMANTICS-0018` |
| INV-SI-009 | Guard cannot interpret job, dataset, spool, or business policy semantics. | `MFOS-REQ-SYSINT-0019` | `NEG-MFOS-SYSINT-GUARD-SCOPE-0019` |
| INV-SI-010 | Partition memory cannot be reassigned until CPU mappings, IOMMU mappings, interrupt routes, and device ownership records are revoked and memory is zeroed. | `MFOS-REQ-PARTITION-0017` | `NEG-MFOS-PARTITION-MEMORY-BEFORE-ZERO-0017` |
| INV-SI-011 | PKU/PKS/CET/IOMMU mechanisms cannot replace securityd authorization or auditd evidence. | `MFOS-REQ-SYSINT-0020` | `NEG-MFOS-SYSINT-HW-OVERCLAIM-0020`, `NEG-MFOS-SYSINT-PKU-STORAGE-KEY-0020` |

State-machine models derived from this section MUST treat the invalid
transitions in section 20.3 as excluded transitions, not as recoverable ordinary
states. If an invalid transition is observed in an implementation trace, the
trace is evidence against the relevant invariant.

## 22. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-SYSINT-0001 | Unauthorized subjects MUST NOT bypass security policy, dataset access, audit, authorized state, or system control objects through system interfaces. | negative test / model check |
| MFOS-REQ-SYSINT-0002 | The system interface list MUST be fixed in specification before implementation. | inspection |
| MFOS-REQ-SYSINT-0003 | SVC, PCALL, operator command, dataset open, catalog update, job submit, spool browse/purge, AMF load, update activation, PXM_CALL, and GUARD_CALL MUST be treated as system interfaces. | inspection |
| MFOS-REQ-SYSINT-0004 | Authorized state MUST be modeled as ExecutionState plus AuthorityClass, not as a single privilege bit. | model review |
| MFOS-REQ-SYSINT-0005 | Baseline system integrity MUST NOT claim root protection after authorized module or nucleus compromise. | claim review |
| MFOS-REQ-SYSINT-0006 | High-Assurance root protection claims MUST bind to PXM Guard root objects and evidence. | evidence review |
| MFOS-REQ-SYSINT-0007 | Supervisor code MUST NOT directly dereference untrusted user pointers. | code review / fuzz test |
| MFOS-REQ-SYSINT-0008 | copy-in/copy-out MUST use typed buffers and length bounds. | unit test / negative test |
| MFOS-REQ-SYSINT-0009 | SVC and PCALL routines MUST treat all caller input as untrusted. | zACS-style negative test |
| MFOS-REQ-SYSINT-0010 | Unsupported system interfaces MUST NOT return success. | no-fake-success CI |
| MFOS-REQ-SYSINT-0011 | Spec-gap behavior MUST NOT be implemented as invented runtime semantics. | spec review / CI |
| MFOS-REQ-SYSINT-0012 | securityd MUST be the final policy decision point for protected resources. | architecture review / integration test |
| MFOS-REQ-SYSINT-0013 | auditd MUST be used for required evidence records; debug logs and spool output MUST NOT substitute for audit evidence. | audit test |
| MFOS-REQ-SYSINT-0014 | Dataset handles MUST bind subject, operation, policy_version, catalog generation, and expiry. | stale handle test |
| MFOS-REQ-SYSINT-0015 | Job effective principal MUST be established before any dataset, program, or spool resource is opened. | integration test |
| MFOS-REQ-SYSINT-0016 | Operator commands MUST execute only after parse, target resolution, securityd authorization, required confirmation/dual-control, and audit obligation handling. | command negative test |
| MFOS-REQ-SYSINT-0017 | AMF load MUST fail closed on invalid signature, invalid manifest, revoked signer/digest, missing authority class, or missing audit obligation. | AMF negative test |
| MFOS-REQ-SYSINT-0018 | PXM MUST be limited to partition lifecycle and isolation responsibilities. | architecture review |
| MFOS-REQ-SYSINT-0019 | Guard MUST be limited to selected root objects in High-Assurance profile. | architecture review |
| MFOS-REQ-SYSINT-0020 | PKU, PKS, CET, SMEP, SMAP, NX, W^X, IOMMU, VMX, SVM, EPT, and NPT MUST be represented as mechanisms, not as substitutes for MFOS authorization semantics. | architecture review |

## 23. Positive Tests

Positive tests in this spec are conformance tests for allowed or explicitly
defined non-mutating behavior. Every listed test MUST exist in
`docs/design/registries/tests.yaml`.

| Local ID | Registry ID | Requirement refs | Expected observation |
| --- | --- | --- | --- |
| PT-SI-001 | `TEST-MFOS-SYSINT-AUTHORIZED-0001` | `MFOS-REQ-SYSINT-0001` | An authorized subject follows a defined system interface without bypassing securityd or auditd obligations. |
| PT-SI-002 | `TEST-MFOS-DATASET-0001` | `MFOS-REQ-SYSINT-0001`, `MFOS-REQ-AUTH-0004` | ALICE can read her authorized dataset through the hosted semantic path and receives a bound handle only after authorization. |
| PT-SI-003 | `TEST-MFOS-SYSINT-INTERFACE-REGISTRY-0002` | `MFOS-REQ-SYSINT-0002` | The system interface registry is fixed before implementation. |
| PT-SI-004 | `TEST-MFOS-SYSINT-INTERFACE-REGISTRY-0003` | `MFOS-REQ-SYSINT-0003` | SVC, PCALL, operator, dataset, catalog, job, spool, AMF, update, PXM, and Guard interfaces are classified as system interfaces. |
| PT-SI-005 | `TEST-MFOS-SYSINT-AUTHORITY-0004` | `MFOS-REQ-SYSINT-0004` | Authorized state is represented as ExecutionState plus AuthorityClass. |
| PT-SI-006 | `TEST-MFOS-SYSINT-COPYIN-0007` | `MFOS-REQ-SYSINT-0007`, `MFOS-REQ-SYSINT-0008` | Trusted copy-in/copy-out uses typed bounded buffers. |
| PT-SI-007 | `TEST-MFOS-SYSINT-SVC-TRUSTED-CONTEXT-0009` | `MFOS-REQ-SYSINT-0009` | A supported SVC uses trusted caller context rather than caller-supplied identity. |
| PT-SI-008 | `TEST-MFOS-SYSINT-UNSUPPORTED-ERROR-0010` | `MFOS-REQ-SYSINT-0010` | A defined but unavailable operation returns `MFOS_ERR_UNSUPPORTED` and produces no protected side effect. |
| PT-SI-009 | `TEST-MFOS-SYSINT-SPEC-GAP-ERROR-0011` | `MFOS-REQ-SYSINT-0011` | An undefined operation is blocked by `MFOS_ERR_SPEC_GAP` or by the pre-implementation gate. |
| PT-SI-010 | `TEST-MFOS-SYSINT-JOB-PRINCIPAL-0015` | `MFOS-REQ-SYSINT-0015` | A job establishes effective principal before opening dataset, program, or spool resources. |
| PT-SI-011 | `TEST-MFOS-SYSINT-OPERATOR-DISPLAY-0016` | `MFOS-REQ-SYSINT-0016` | An operator with `OPERATOR_DISPLAY` runs a non-destructive display command after parse, authorization, audit, and execution. |
| PT-SI-012 | `TEST-MFOS-SYSINT-PXM-LIFECYCLE-0018` | `MFOS-REQ-SYSINT-0018` | PXM accepts a legal partition lifecycle transition without interpreting enterprise policy. |
| PT-SI-013 | `TEST-MFOS-SYSINT-GUARD-EVIDENCE-0006` | `MFOS-REQ-SYSINT-0006` | High-Assurance root protection claims bind to Guard evidence. |
| PT-SI-014 | `TEST-MFOS-SYSINT-GUARD-ROOT-0019` | `MFOS-REQ-SYSINT-0019` | Guard operations are limited to selected root objects. |
| PT-SI-015 | `TEST-MFOS-SYSINT-HW-MECHANISM-0020` | `MFOS-REQ-SYSINT-0020` | Hardware features are documented as enforcement mechanisms, not authorization semantics. |

## 24. Negative Tests

Negative tests prove that invalid transitions and prohibited substitutions do
not complete protected operations. Every listed test MUST exist in
`docs/design/registries/tests.yaml`.

| Local ID | Registry ID | Requirement refs | Prohibited outcome |
| --- | --- | --- | --- |
| NT-SI-001 | `NEG-MFOS-DATASET-0001` | `MFOS-REQ-SYSINT-0001`, `MFOS-REQ-AUTH-0004` | BOB obtains a handle to ALICE's dataset. |
| NT-SI-002 | `NEG-MFOS-SYSINT-SVC-BYPASS-0001` | `MFOS-REQ-SYSINT-0001`, `MFOS-REQ-SYSINT-0003`, `MFOS-REQ-SYSINT-0007` | SVC bypasses protected interface, pointer, or authorization rules. |
| NT-SI-003 | `NEG-MFOS-SYSINT-DATASET-BYPASS-0001` | `MFOS-REQ-SYSINT-0001`, `MFOS-REQ-DATASET-0002`, `MFOS-REQ-CATALOG-0002`, `MFOS-REQ-AUTH-0004`, `MFOS-REQ-AUDIT-0002` | Unauthorized dataset access creates a usable handle or bypasses audit. |
| NT-SI-004 | `NEG-MFOS-SYSINT-AUDIT-BYPASS-0001` | `MFOS-REQ-SYSINT-0001` | Audit-required denial reaches caller without required audit handling. |
| NT-SI-005 | `NEG-MFOS-SYSINT-UNREGISTERED-INTERFACE-0002` | `MFOS-REQ-SYSINT-0002`, `MFOS-REQ-SYSINT-0003` | An unregistered system interface is treated as implemented behavior. |
| NT-SI-006 | `NEG-MFOS-SYSINT-AMF-ADMIN-CONFUSION-0004` | `MFOS-REQ-SYSINT-0004` | AMF authority is treated as general administrator authority. |
| NT-SI-007 | `NEG-MFOS-SYSINT-BASELINE-OVERCLAIM-0005` | `MFOS-REQ-SYSINT-0005` | Baseline claim implies protection after nucleus or authorized module compromise. |
| NT-SI-008 | `NEG-MFOS-SYSINT-HA-CLAIM-NO-GUARD-0006` | `MFOS-REQ-SYSINT-0006` | High-Assurance root protection is claimed without Guard root evidence. |
| NT-SI-009 | `NEG-MFOS-SYSINT-RAW-POINTER-0007` | `MFOS-REQ-SYSINT-0007`, `MFOS-REQ-SYSINT-0008`, `MFOS-REQ-SYSINT-0009` | Supervisor code directly dereferences untrusted caller memory. |
| NT-SI-010 | `NEG-MFOS-SYSINT-COPY-OVERFLOW-0008` | `MFOS-REQ-SYSINT-0008` | Copy-in overflow reaches allocation, copy, or endpoint dispatch. |
| NT-SI-011 | `NEG-MFOS-SYSINT-PCALL-OVERSIZE-0008` | `MFOS-REQ-SYSINT-0008`, `MFOS-REQ-SYSINT-0009` | Oversized PCALL payload is accepted as a trusted request. |
| NT-SI-012 | `NEG-MFOS-SYSINT-SVC-FORGED-IDENTITY-0009` | `MFOS-REQ-SYSINT-0009` | Caller-supplied identity becomes effective identity. |
| NT-SI-013 | `NEG-MFOS-SYSINT-UNSUPPORTED-SUCCESS-0010` | `MFOS-REQ-SYSINT-0010`, `MFOS-REQ-SYSINT-0011`, `MFOS-REQ-AI-0005` | Defined unavailable operation completes a protected action. |
| NT-SI-014 | `NEG-MFOS-SYSINT-SPEC-GAP-SUCCESS-0011` | `MFOS-REQ-SYSINT-0011` | Undefined behavior is implemented as runtime semantics. |
| NT-SI-015 | `NEG-MFOS-SYSINT-LOG-AS-AUDIT-0013` | `MFOS-REQ-SYSINT-0013`, `MFOS-REQ-AUDIT-0002` | Debug logs satisfy audit evidence obligations. |
| NT-SI-016 | `NEG-MFOS-SYSINT-SPOOL-AS-AUDIT-0013` | `MFOS-REQ-SYSINT-0013` | Spool output satisfies audit evidence obligations. |
| NT-SI-017 | `NEG-MFOS-SYSINT-DATASET-HANDLE-BINDING-0014` | `MFOS-REQ-SYSINT-0014`, `MFOS-REQ-DATASET-0001` | Dataset handle is reused outside its decision binding. |
| NT-SI-018 | `NEG-MFOS-SYSINT-JOB-NO-PRINCIPAL-0015` | `MFOS-REQ-SYSINT-0015` | Job opens resources before effective principal exists. |
| NT-SI-019 | `NEG-MFOS-SYSINT-OPERATOR-DESTRUCTIVE-NO-CONFIRM-0016` | `MFOS-REQ-SYSINT-0016` | Destructive operator command executes without required confirmation. |
| NT-SI-020 | `NEG-MFOS-SYSINT-OPERATOR-ROOT-SHELL-0016` | `MFOS-REQ-SYSINT-0016` | Root-shell style operation bypasses operator command governance. |
| NT-SI-021 | `NEG-MFOS-SYSINT-AMF-BOUNDARY-0017` | `MFOS-REQ-SYSINT-0017`, `MFOS-REQ-AMF-0021` | AMF failure path creates executable mapping, registry entry, or authorized state. |
| NT-SI-022 | `NEG-MFOS-SYSINT-PXM-SEMANTICS-0018` | `MFOS-REQ-SYSINT-0018`, `MFOS-REQ-SYSINT-0012` | PXM interprets MFOS enterprise policy semantics. |
| NT-SI-023 | `NEG-MFOS-SYSINT-GUARD-SCOPE-0019` | `MFOS-REQ-SYSINT-0019` | Guard interprets job, dataset, spool, or business policy semantics. |
| NT-SI-024 | `NEG-MFOS-SYSINT-HW-OVERCLAIM-0020` | `MFOS-REQ-SYSINT-0020` | Hardware feature claim replaces authorization or audit semantics. |
| NT-SI-025 | `NEG-MFOS-SYSINT-PKU-STORAGE-KEY-0020` | `MFOS-REQ-SYSINT-0020` | PKU/PKS is treated as z/Architecture storage-key compatibility. |
| NT-SI-026 | `NEG-MFOS-CATALOG-UNCOMMITTED-0002` | `MFOS-REQ-CATALOG-0002` | catalogd resolves an uncommitted entry. |
| NT-SI-027 | `NEG-MFOS-PARTITION-DEVICE-TEARDOWN-0006` | `MFOS-REQ-PARTITION-0005`, `MFOS-REQ-PARTITION-0006`, `MFOS-REQ-PARTITION-0016`, `MFOS-REQ-PARTITION-0017` | Device reassignment occurs before teardown completion. |

## 25. Fuzz Targets

Required fuzz targets:

- `svc_request_fuzz`: malformed SVC numbers, handle values, lengths, pointer-like fields, and identity fields.
- `pcall_request_fuzz`: endpoint IDs, payload lengths, type tags, policy_version, and caller context.
- `operator_command_fuzz`: command grammar, target resolution, destructive command modifiers, confirmation flags.
- `dsn_fuzz`: DSN grammar, invalid names, boundary length, escaped characters if later allowed.
- `jcl_like_fuzz`: job cards, DD statements, malformed principal fields, malformed SYSOUT fields.
- `amf_manifest_fuzz`: signature metadata, authority class, ABI version, dependency list, revocation refs.
- `catalog_transaction_fuzz`: transaction states, generation numbers, immutable/system flags.
- `update_manifest_fuzz`: security_epoch, generation, target hashes, size, dependency/conflict lists.
- `pxm_call_fuzz`: partition IDs, state transitions, device IDs, teardown checklist flags.
- `guard_call_fuzz`: root type, digest, version, nonce, code identity.

Fuzz failure rule:

No fuzz input may produce unauthorized success, missing audit for an audit-required denial, memory unsafety, panic in production parser path, or untyped handle creation.

## 26. Spec Gaps

Spec gaps block implementation of the undefined behavior. They do not block
documentation, source-card review, requirement reservation, or negative test
planning. They also do not convert a defined disabled feature into `SPEC_GAP`.

| Gap ID | Missing canonical artifact | Required handling until closed | Related registry tests |
| --- | --- | --- | --- |
| SPEC-GAP-SI-001 | Exact SVC numeric ABI | SVC numbers outside the defined registry return `MFOS_ERR_SPEC_GAP` or are rejected by the pre-implementation gate. | `TEST-MFOS-SYSINT-SPEC-GAP-ERROR-0011`, `NEG-MFOS-SYSINT-SPEC-GAP-SUCCESS-0011` |
| SPEC-GAP-SI-002 | Exact PCALL wire format | PCALL implementation is blocked except for parser/fuzz planning and explicit placeholder negative tests. | `NEG-MFOS-SYSINT-PCALL-OVERSIZE-0008` |
| SPEC-GAP-SI-003 | Exact operator command grammar | Operator implementation is blocked beyond documented grammar stubs and lintable command registry planning. | `NEG-MFOS-SYSINT-OPERATOR-ROOT-SHELL-0016` |
| SPEC-GAP-SI-004 | Exact DSN grammar | Dataset/catalog implementation must not infer DSN syntax beyond registered grammar constraints. | `NEG-MFOS-CATALOG-UNCOMMITTED-0002`, `NEG-MFOS-DATASET-UNAUTHORIZED-OPEN-0002` |
| SPEC-GAP-SI-005 | Exact AMF manifest schema | Production AMF load remains disabled; AMF-disabled requests use `MFOS_ERR_UNSUPPORTED`, not `MFOS_ERR_SPEC_GAP`. | `NEG-MFOS-SYSINT-AMF-BOUNDARY-0017`, `NEG-MFOS-AMF-LOAD-DISABLED-0021` |
| SPEC-GAP-SI-006 | Exact audit record binary format | Binary audit encoding implementation is blocked; audit obligations and schema-level records remain required. | `NEG-MFOS-SYSINT-LOG-AS-AUDIT-0013`, `NEG-MFOS-SYSINT-SPOOL-AS-AUDIT-0013` |
| SPEC-GAP-SI-007 | Exact Guard call binary ABI | Guard implementation is blocked except root-object model and claim/evidence planning. | `TEST-MFOS-SYSINT-GUARD-ROOT-0019`, `NEG-MFOS-SYSINT-GUARD-SCOPE-0019` |
| SPEC-GAP-SI-008 | Exact PXM device teardown checklist schema | Device reassignment implementation is blocked unless teardown evidence fields are fully specified by PXM spec. | `NEG-MFOS-PARTITION-DEVICE-TEARDOWN-0006` |
| SPEC-GAP-SI-009 | Exact formal model language and model-checking toolchain | Formal proof claims are blocked; invariants remain normative review obligations. | `TEST-MFOS-SYSINT-CLAIM-BOUNDARY-0005` |
| SPEC-GAP-SI-010 | Exact profile-specific audit failure policy | Profiles may enter recovery-only gates, but ordinary operation must not proceed without the audit failure policy required by the audit spec. | `NEG-MFOS-AUDIT-UNAVAILABLE-0005`, `TEST-MFOS-AUDIT-RECOVERY-MODE-0005` |

Closure rule:

- Closing a spec gap requires updating the owning split spec, requirement refs,
  tests, evidence expectations, and pack contract before implementation begins.
- A spec gap closure MUST NOT weaken the non-compatibility statement, securityd
  authority, auditd evidence role, AMF-disabled default, PXM scope, or Guard
  root-object scope.
- Any implementation agent encountering an unclosed spec gap MUST produce a
  `SPEC_GAP_REPORT` instead of code.

## 27. AI Prompt

Use this prompt when asking an AI agent to implement or review MFOS system integrity behavior:

```text
You are the MFOS system integrity implementation/review agent.

MFOS is z/OS-inspired, not z/OS compatible.

Before writing code or approving a design:
- list applicable requirement IDs
- list Source Matrix IDs
- identify protected resources
- identify system interfaces
- identify subjects, objects, operations, context, and policy_version
- show how securityd remains the final policy decision point
- show auditd obligations and failure handling
- distinguish ExecutionState from AuthorityClass
- reject caller-supplied identity
- reject direct dereference of untrusted user pointers
- use typed handles and bounded copy-in/copy-out
- distinguish UNSUPPORTED from SPEC_GAP
- prevent fake success, empty stubs, and silent fallback
- add positive tests and negative tests
- add fuzz targets for parsers or binary interfaces
- document invariants, failure modes, assumptions, and evidence
- keep PXM limited to partition isolation
- keep Guard limited to selected High-Assurance root objects
- do not use PKU/PKS as a system integrity root

If behavior is undefined by spec, return SPEC_GAP instead of inventing semantics.
```
