---
spec_id: "MFOS-SPEC-01-GLOSSARY"
title: "MFOS Glossary v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001", "EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001", "EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001", "EXTREF-IBM-Z-DPM-0001", "EXTREF-IBM-ZOS-JES-INTRODUCTION-0001", "EXTREF-IBM-ZOS-JES-JOB-FLOW-0001", "EXTREF-IBM-ZOS-JES2-LIBRARY-0001", "EXTREF-IBM-Z-LPAR-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001", "EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001", "EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001", "EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001", "EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001", "EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001", "EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001", "EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001", "EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001", "EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001", "EXTREF-IBM-Z-ARCHITECTURE-PRINCIPLES-0001", "MS-VBS-001", "MS-VSM-001", "NIST-160-001", "NIST-193-001", "NIST-218-001", "SEL4-001", "SLSA-001", "TCG-001", "TUF-001", "X64-AMD-001", "X64-INTEL-001", "X64-LINUX-CET-001", "X64-LINUX-PKU-001"]
requirement_refs: ["MFOS-REQ-GLOSS-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Glossary v0.1

Status: Draft specification

## 1. Purpose

This document defines the controlled vocabulary for MFOS design and implementation.

MFOS uses z/OS-inspired enterprise operating system concepts, x64 implementation mechanisms, and high-assurance evidence discipline. This glossary prevents AI agents and human contributors from inventing near-synonyms, implying compatibility, or mixing assurance boundaries.

MFOS is inspired by selected IBM-documented enterprise OS concepts, but it is not z/OS compatible.

## 2. Scope

In scope:

- canonical MFOS terms
- prohibited terms
- term overlap and divergence rules
- Source Matrix IDs for source-grounded concepts
- object-model vocabulary
- authority and integrity vocabulary
- profile vocabulary
- implementation and evidence vocabulary

Out of scope:

- full IBM terminology reproduction
- product compatibility vocabulary
- user-facing training guide
- localization glossary
- final CLI syntax

## 3. Non-objectives

This glossary MUST NOT be used to imply:

- MFOS implements z/OS
- MFOS implements RACF
- MFOS implements JES2 or JES3
- MFOS implements DFSMS
- MFOS implements SMF
- MFOS implements PR/SM
- MFOS implements Windows VBS
- MFOS emulates z/Architecture
- MFOS runs z/OS workloads

## 4. Source Matrix IDs

| Source ID | Glossary area |
| --- | --- |
| EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001 | system integrity, authorized/unauthorized boundary |
| EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001 | authorized boundary scanning and negative testing |
| EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001 | authorized program inspiration |
| EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001 | storage protection inspiration |
| EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001 | storage protection detail inspiration |
| EXTREF-IBM-ZOS-SECURITY-SERVER-0001 | RACF source family for security manager inspiration |
| EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001 | resource profile inspiration |
| EXTREF-IBM-ZOS-JES-INTRODUCTION-0001 | JES source family for job/spool inspiration |
| EXTREF-IBM-ZOS-JES-JOB-FLOW-0001 | job lifecycle inspiration |
| EXTREF-IBM-ZOS-JES2-LIBRARY-0001 | JES2 reference source family |
| EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001 | catalog inspiration |
| EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001 | dataset/storage management source family |
| EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | SMF-inspired audit/accounting |
| EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001 | security audit record inspiration |
| EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001 | workload/service class inspiration |
| EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001 | optional POSIX subsystem distinction |
| EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001 | optional UNIX-like subsystem source family |
| EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001 | PCALL/cross-memory inspiration |
| EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001 | cross-memory security inspiration |
| EXTREF-IBM-Z-LPAR-INTRODUCTION-0001 | partition inspiration |
| EXTREF-IBM-Z-DPM-0001 | partition management plane inspiration |
| EXTREF-IBM-Z-ARCHITECTURE-PRINCIPLES-0001 | architecture term contrast source |
| EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001 | update advisory model inspiration |
| X64-INTEL-001 | x64 Intel implementation vocabulary |
| X64-AMD-001 | AMD64 implementation vocabulary |
| X64-LINUX-PKU-001 | PKU limitations |
| X64-LINUX-CET-001 | CET vocabulary |
| MS-VBS-001 | VBS-like Guard comparison only |
| MS-VSM-001 | VSM/VTL-like Guard comparison only |
| TCG-001 | measured boot and TPM |
| TUF-001 | update metadata roles |
| SLSA-001 | provenance |
| FBVBS-001 | assurance discipline and traceability vocabulary |

## 5. Naming Rules

NR-GLOSS-001:

MFOS terms MUST be preferred over IBM product names unless the text is explicitly discussing source mapping.

NR-GLOSS-002:

When IBM-derived terms appear, the text MUST explain semantic overlap and MFOS divergence.

NR-GLOSS-003:

The suffix `-inspired` MAY be used for source-grounded concept families.

NR-GLOSS-004:

The suffix `-compatible` MUST NOT be used for IBM product or platform terms.

NR-GLOSS-005:

MFOS components ending in `d` are service daemons in the MFOS service architecture. They are not Unix daemons by implication and MUST still use MFOS authorization and audit rules.

## 6. Canonical Terms

### ActivationProfile

Canonical spelling: `ActivationProfile`

Definition:

A protected configuration object describing partition activation parameters such as image identity, logical CPU assignment, memory assignment, device assignment, measurement policy, and profile applicability.

Source Matrix IDs:

- EXTREF-IBM-Z-LPAR-INTRODUCTION-0001
- EXTREF-IBM-Z-DPM-0001
- FBVBS-001

MFOS divergence:

MFOS ActivationProfile is not a PR/SM or HMC profile. It is an MFOS/PXM object model term.

### AMF

Canonical spelling: `AMF`

Expansion:

Authorized Module Facility

Definition:

MFOS facility for loading and governing explicitly authorized OS extension modules.

Source Matrix IDs:

- EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001
- EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001

Overlap:

Inspired by the idea that some code is authorized to enter sensitive OS service paths.

Divergence:

AMF is not APF. AMF is not administrator privilege. AMF is not a broad kernel module ecosystem.

Allowed wording:

- AMF is APF-inspired.
- AMF is MFOS authorized module governance.

Prohibited wording:

- AMF is APF-compatible.
- AMF grants root.
- AMF is admin mode.

### AMF Registry

Definition:

Protected registry of approved AMF module identities, authority classes, signer policy, revocation state, security epoch, and measurement metadata.

Source Matrix IDs:

- EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001
- EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001
- MS-VSM-001 for High-Assurance Guard protection only

### AuditRecord

Definition:

Schema-validated evidence record emitted for security, job, dataset, catalog, spool, operator, partition, update, AMF, and Guard-relevant events.

Source Matrix IDs:

- EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001
- EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001
- FBVBS-001

Divergence:

AuditRecord is SMF-inspired but is not an SMF record and does not claim binary or semantic compatibility.

### auditd

Definition:

MFOS evidence service responsible for append-only audit records, schema validation, hash chaining, local durable storage, remote export where required, retention, and Guard-sealed audit root in High-Assurance profile.

Source Matrix IDs:

- EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001
- EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001
- FBVBS-001

### AuthorityClass

Definition:

Typed authority label used to constrain privileged operations, AMF module capabilities, operator commands, and service endpoints.

Source Matrix IDs:

- EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001
- EXTREF-IBM-ZOS-SECURITY-SERVER-0001

### AuthorizedModule

Definition:

Signed and measured executable component permitted to use an explicit AMF authority class through a defined ABI.

Source Matrix IDs:

- EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001
- EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001

### Authorized State

Definition:

MFOS condition in which an execution context has an explicitly granted authority class and enters a protected service path through a defined system interface.

Source Matrix IDs:

- EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
- EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001

Divergence:

MFOS does not use z/Architecture PSW key semantics. MFOS separates `ExecutionState` from `AuthorityClass`.

### Baseline Profile

Definition:

Minimum MFOS conformance profile for source-grounded enterprise semantics, mandatory authorization/audit discipline, and no fake success.

Source Matrix IDs:

- FBVBS-001
- NIST-160-001

### CatalogEntry

Definition:

Committed protected object mapping a DSN to dataset attributes, storage location, owner, generation, security profile, system/immutable flags, and integrity tag.

Source Matrix IDs:

- EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001
- EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001

Divergence:

MFOS CatalogEntry is not a DFSMS catalog entry.

### catalogd

Definition:

MFOS service responsible for DSN grammar, catalog entry creation, DSN resolution, generation tracking, transaction recovery, and catalog integrity checks.

Source Matrix IDs:

- EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001
- EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001

### CET

Expansion:

Control-flow Enforcement Technology

Definition:

x64 control-flow hardening feature family including shadow stack and indirect branch tracking on supported platforms.

Source Matrix IDs:

- X64-INTEL-001
- X64-LINUX-CET-001

Divergence:

CET is an implementation hardening mechanism, not an MFOS authorization model.

### Dataset

Definition:

Managed enterprise data object identified through a DSN and governed by catalog, security profile, retention, integrity, audit, allocation, and optional encryption policy.

Source Matrix IDs:

- EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001
- EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001
- EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001

Divergence:

An MFOS Dataset is not a POSIX file wrapper.

### datasetd

Definition:

MFOS service responsible for dataset allocation, open/close, record/block access, handle lifecycle, retention enforcement, integrity verification, secure deletion policy, and backup hooks.

Source Matrix IDs:

- EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001
- EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001

### DSN

Expansion:

Dataset Name

Definition:

Canonical name for a dataset in MFOS catalog operations.

Source Matrix IDs:

- EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001

Divergence:

The MFOS DSN grammar is defined by MFOS specs and does not claim full z/OS DSN grammar compatibility.

### Enterprise Profile

Definition:

MFOS profile adding production-oriented controls such as Secure Boot, Measured Boot, TPM use, remote audit export, TUF-like updates, SBOM, signed provenance, and stronger device isolation requirements.

Source Matrix IDs:

- TCG-001
- TUF-001
- SLSA-001
- NIST-218-001

### ExecutionState

Definition:

MFOS execution classification used to reason about privilege boundary and service entry.

Allowed values:

```text
USER_JOB
USER_SUBSYSTEM
TRUSTED_SERVICE
AUTHORIZED_SERVICE
SUPERVISOR
GUARD
PM_ROOT
```

Source Matrix IDs:

- EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
- EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001
- X64-INTEL-001
- X64-AMD-001

Divergence:

ExecutionState is not a PSW key and is not a z/Architecture mode.

### FBVBS

Definition:

Internal transfer source used for MFOS assurance discipline, evidence structure, traceability, state-machine rigor, and no-fake-success practices.

Source Matrix IDs:

- FBVBS-001

### Guard

Canonical spelling:

`PXM Guard` or `Guard`

Definition:

High-Assurance-only protection component that seals and verifies selected root objects such as security policy root, audit chain root, AMF registry, SVC table integrity, executable mapping policy, page-table policy, activation profile root, emergency state, and update policy root.

Source Matrix IDs:

- MS-VBS-001
- MS-VSM-001
- FBVBS-001

Divergence:

Guard is not Windows VBS. Guard MUST NOT implement dataset policy, job scheduling, spool formatting, or operator business semantics.

### GuardRoot

Definition:

Selected root object protected or verified by PXM Guard in High-Assurance profile.

Examples:

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

### High-Assurance Profile

Definition:

MFOS profile requiring PXM Guard, Guard-sealed root objects, remote attestation, stronger formal/evidence obligations, and independent TCB review.

Source Matrix IDs:

- MS-VBS-001
- MS-VSM-001
- FBVBS-001
- SEL4-001

### IOMMU

Definition:

Hardware-assisted DMA isolation mechanism used by PXM for device assignment boundaries and memory protection from devices.

Source Matrix IDs:

- X64-INTEL-001
- X64-AMD-001

### Job

Definition:

Submitted unit of work with submitter, effective principal, job class, service class, steps, return code, spool references, and audit correlation ID.

Source Matrix IDs:

- EXTREF-IBM-ZOS-JES-INTRODUCTION-0001
- EXTREF-IBM-ZOS-JES-JOB-FLOW-0001

Divergence:

MFOS Job is JES-inspired and does not claim JES2 or JES3 compatibility.

### JobClass

Definition:

Classification affecting job queueing, admission, and workload policy.

Source Matrix IDs:

- EXTREF-IBM-ZOS-JES-INTRODUCTION-0001
- EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001

### jobd

Definition:

MFOS service responsible for job submission, JCL-like subset parsing, job identity establishment, conversion, queue management, initiators, step execution, DD resolution, return code collection, restart metadata, cancellation, and accounting.

Source Matrix IDs:

- EXTREF-IBM-ZOS-JES-INTRODUCTION-0001
- EXTREF-IBM-ZOS-JES-JOB-FLOW-0001

### JCL-like

Definition:

MFOS-defined job control syntax inspired by JCL concepts but not compatible with JCL.

Source Matrix IDs:

- EXTREF-IBM-ZOS-JES-INTRODUCTION-0001
- EXTREF-IBM-ZOS-JES-JOB-FLOW-0001

Allowed wording:

- JCL-like subset
- JCL-inspired job declaration

Prohibited wording:

- JCL compatible
- runs JCL
- JES2 JCL support

### Linux/Desktop Side Partition

Definition:

Optional side partition used for desktop, browser, development tools, GPU stack, and other non-MFOS enterprise workloads.

Source Matrix IDs:

- EXTREF-IBM-Z-LPAR-INTRODUCTION-0001

Divergence:

MFOS does not embed the Linux desktop stack inside the MFOS partition as part of core design.

### Measured Boot

Definition:

Boot process that records measurements of firmware, boot, PXM, Guard, MFOS, and selected policy artifacts into a measurement log or TPM-backed context.

Source Matrix IDs:

- TCG-001

### Nucleus

Definition:

MFOS core supervisor component responsible for boot handoff, address spaces, SVC entry, typed object handles, IPC primitives, baseline scheduling, page table management, NX/W^X enforcement, copy-in/copy-out, service lifecycle, fault containment, kernel audit hook, and crash dump trigger.

Source Matrix IDs:

- X64-INTEL-001
- X64-AMD-001
- EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001

Divergence:

Nucleus is an MFOS term and is not the z/OS nucleus.

### Operator Console

Definition:

First interactive MFOS system interface with command grammar, authority checks, audit, confirmation, dual-control where required, state display, job control, dataset workflow, emergency mode, and automation hook.

Source Matrix IDs:

- EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
- EXTREF-IBM-ZOS-SECURITY-SERVER-0001
- EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001

Divergence:

The operator console is not a root shell.

### operatord

Definition:

MFOS service implementing operator console command parsing, authorization, audit, state display, job control, dataset definition workflows, emergency mode, and automation hooks.

### PCALL

Definition:

Typed, bounded, synchronous service-call ABI mediated by MFOS identity, authorization, and audit rules.

Source Matrix IDs:

- EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001
- EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001

Divergence:

PCALL is inspired by cross-memory service concepts but does not allow arbitrary cross-address-space pointer access in early MFOS.

### PKS

Definition:

Supervisor protection-key mechanism where supported by hardware and platform profile.

Source Matrix IDs:

- X64-INTEL-001

Divergence:

PKS MAY assist metadata protection but MUST NOT replace Guard or system integrity roots.

### PKU

Definition:

User-mode protection-key mechanism controlling data access through PTE keys and PKRU on supported x64 platforms.

Source Matrix IDs:

- X64-INTEL-001
- X64-LINUX-PKU-001

Divergence:

PKU is data-access oriented and MUST NOT be used as a storage-key compatibility claim or primary system integrity root.

### Principal

Definition:

Authenticated identity subject to security policy and audit. A Principal may have groups, roles, labels, status, expiry, and emergency access attributes.

Source Matrix IDs:

- EXTREF-IBM-ZOS-SECURITY-SERVER-0001
- EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001

### ProgramIdentity

Definition:

Executable identity including artifact location, signer, digest, catalog generation, AMF authorization state, authority class, allowed service classes, and measurement context.

Source Matrix IDs:

- EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001
- TCG-001

### Protected Resource

Definition:

Object that MUST NOT be accessed, modified, opened, browsed, purged, loaded, scheduled, activated, or destroyed without a defined authorization path and audit obligation.

Source Matrix IDs:

- EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
- EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001
- EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001

### PXM

Expansion:

Partition Manager

Definition:

Partition isolation layer responsible for partition lifecycle, activation profile, logical CPU assignment, memory domain assignment, IOMMU domain setup, interrupt remapping, device assignment, device teardown, partition audit, and recovery partition coordination.

Source Matrix IDs:

- EXTREF-IBM-Z-LPAR-INTRODUCTION-0001
- EXTREF-IBM-Z-DPM-0001
- FBVBS-001

Divergence:

PXM is not PR/SM. PXM does not understand MFOS job, dataset, spool, or security policy semantics.

### PXM_CALL

Definition:

Restricted ABI for partition operations such as create, measure, load, activate, start, quiesce, resume, recover, destroy, assign device, release device, and status query.

Source Matrix IDs:

- EXTREF-IBM-Z-LPAR-INTRODUCTION-0001
- FBVBS-001

### Recovery Partition

Definition:

Side partition used for offline repair, rollback, forensics, and backup restore.

Source Matrix IDs:

- EXTREF-IBM-Z-LPAR-INTRODUCTION-0001
- NIST-193-001

### SecurityProfile

Definition:

Protected policy object defining access rules for protected resources.

Source Matrix IDs:

- EXTREF-IBM-ZOS-SECURITY-SERVER-0001
- EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001

### securityd

Definition:

Central MFOS policy decision service for protected resource access, including principal registry, group/role registry, resource profiles, dataset access decisions, spool access decisions, job submission decisions, operator command decisions, AMF load decisions, partition operation decisions, emergency access, delegation, policy versioning, transaction/rollback, and audit obligation generation.

Source Matrix IDs:

- EXTREF-IBM-ZOS-SECURITY-SERVER-0001
- EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001

Divergence:

securityd is RACF-inspired but is not RACF.

### ServiceClass

Definition:

Workload classification with performance and business-importance meaning used by workpolicyd.

Source Matrix IDs:

- EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001

Divergence:

MFOS ServiceClass is external-workload-management-informed and does not claim full z/OS workload policy semantics.

### SMF-inspired

Definition:

Used only to describe audit/accounting design influenced by IBM SMF concepts.

Source Matrix IDs:

- EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001
- EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001

Prohibited wording:

- SMF-compatible
- emits SMF
- implements SMF

### SPOOL

Canonical object:

`SpoolEntry`

Definition:

Managed job input/output object for SYSIN/SYSOUT-like streams, output class, browse, purge, export, retention, quota, security, and audit.

Source Matrix IDs:

- EXTREF-IBM-ZOS-JES-INTRODUCTION-0001
- EXTREF-IBM-ZOS-JES-JOB-FLOW-0001

Divergence:

MFOS spool is JES-inspired and not JES-compatible.

### spoold

Definition:

MFOS service responsible for SYSIN storage, SYSOUT capture, spool ownership, output class, browse, purge, export, retention, quota, and securityd-mediated access.

### StorageDomain

Definition:

MFOS software-defined storage protection category used for design and enforcement mapping.

Allowed values:

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

Source Matrix IDs:

- EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001
- EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001
- X64-INTEL-001
- X64-AMD-001

Divergence:

StorageDomain is not a z/Architecture storage key.

### SVC

Definition:

MFOS supervisor call ABI for kernel object operations, typed handles, bounded copy-in/copy-out, and security/audit integration.

Source Matrix IDs:

- EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
- EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001
- X64-INTEL-001
- X64-AMD-001

Divergence:

SVC is an MFOS ABI term and does not claim binary or semantic compatibility with z/Architecture SVC.

### System Integrity

Definition:

MFOS property that unauthorized principals, programs, jobs, and subsystems cannot use defined system interfaces to bypass or alter security policy, dataset access control, catalog metadata, audit recording, spool access, job identity, operator command authority, authorized execution state, or system control objects.

Source Matrix IDs:

- EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001

Divergence:

Baseline system integrity does not include root-object survival after authorized module or nucleus compromise. That claim belongs to High-Assurance PXM Guard.

### TCB

Expansion:

Trusted Computing Base

Definition:

Components that must behave correctly for a named MFOS security or assurance claim to hold.

Source Matrix IDs:

- NIST-160-001
- SEL4-001
- FBVBS-001

### TUF-like Update Model

Definition:

MFOS update metadata model inspired by TUF roles and protections against rollback, freeze, mix-and-match, and key compromise.

Source Matrix IDs:

- TUF-001

Divergence:

MFOS may implement a TUF-like update model without claiming full TUF implementation unless a separate conformance spec proves it.

### UNSUPPORTED

Definition:

The behavior is specified, but this implementation does not implement it. It MUST fail closed with `MFOS_ERR_UNSUPPORTED`.

### SPEC_GAP

Definition:

The behavior is not specified. An implementation MUST NOT invent semantics and MUST fail closed with `MFOS_ERR_SPEC_GAP` or reject the change at spec review time.

### UVS

Expansion:

Update Verification Service

Definition:

MFOS service responsible for update metadata verification, artifact signature and hash/size checks, generation/security epoch checks, rollback/freeze/mix-and-match detection, revocation checks, dependencies, staged activation profile update, audit, and recovery rollback workflow.

Source Matrix IDs:

- TUF-001
- EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001 as update advisory inspiration only
- FBVBS-001

### workload policy

Expansion:

Workload Policy

Definition:

MFOS workload policy and dispatch-hint service using job class, service class, priority, resource cap, max concurrency, overload policy, report class, and future response-time/velocity-like goals.

Source Matrix IDs:

- EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001

Divergence:

MFOS workload policy is z/OS external-workload-management-informed and not z/OS external-workload-management-compatible.

### workpolicyd

Definition:

MFOS service implementing workload policy primitives and dispatch hints.

## 7. Prohibited Terms and Replacements

| Prohibited | Replacement |
| --- | --- |
| z/OS compatible | z/OS-inspired |
| RACF compatible | RACF-inspired securityd |
| JES2 compatible | JES-inspired job/spool model |
| DFSMS compatible | DFSMS-inspired dataset/catalog model |
| SMF compatible | SMF-inspired audit model |
| APF compatible | APF-inspired AMF |
| z/Architecture compatible | x64-native with z/Architecture concept mapping where documented |
| root shell | operator console |
| file | dataset, when referring to MFOS managed enterprise data |
| log | audit record, when evidence is meant |
| admin module | authorized module, when AMF is meant |
| storage key replacement | StorageDomain mapping or PKU/PKS helper |
| VBS clone | PXM Guard High-Assurance profile |

## 8. Protected Resources

The glossary names the following protected-resource terms:

- Principal
- Group
- Role
- ProgramIdentity
- AuthorizedModule
- SecurityProfile
- SecurityPolicyRoot
- AuditRecord
- AuditChainRoot
- Dataset
- CatalogEntry
- Volume
- SpoolEntry
- Job
- JobStep
- OperatorCommand
- WorkloadPolicy
- AMFRegistry
- UpdateArtifact
- UpdateMetadata
- Partition
- ActivationProfile
- DeviceAssignment
- GuardRoot

Any new glossary term representing a resource that affects authority, identity, evidence, executable code, partition state, or enterprise data MUST be explicitly marked as a protected resource or explicitly marked as non-protected with rationale.

## 9. System Interfaces

The glossary names the following system-interface terms:

- SVC
- PCALL
- PXM_CALL
- GUARD_CALL
- OperatorCommand
- DatasetOpen
- CatalogTransaction
- JobSubmit
- JobCancel
- SpoolBrowse
- SpoolPurge
- SecurityPolicyUpdate
- AuditQuery
- AMFLoad
- UpdateActivation
- DeviceAssignment
- PartitionLifecycleTransition

Any new glossary term representing a callable or commandable authority boundary MUST be added to the system-interface list before implementation.

## 10. Invariants

INV-GLOSS-001:

A glossary term derived from an IBM concept must include Source Matrix IDs and divergence.

INV-GLOSS-002:

A glossary term must not imply z/OS compatibility.

INV-GLOSS-003:

Terms for MFOS protected resources and system interfaces must be stable enough for requirement IDs, audit schemas, and test names.

INV-GLOSS-004:

Hardware mechanism terms must not be defined as policy decision points.

INV-GLOSS-005:

Guard terms must remain limited to selected root objects and High-Assurance claims.

## 11. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-GLOSS-0001 | Every IBM-derived glossary term MUST include Source Matrix IDs. | documentation review |
| MFOS-REQ-GLOSS-0002 | Every IBM-derived glossary term MUST include MFOS divergence. | documentation review |
| MFOS-REQ-GLOSS-0003 | The glossary MUST define prohibited compatibility wording and replacement wording. | release review |
| MFOS-REQ-GLOSS-0004 | Protected resource terms MUST be identifiable in the glossary. | spec lint |
| MFOS-REQ-GLOSS-0005 | System interface terms MUST be identifiable in the glossary. | spec lint |
| MFOS-REQ-GLOSS-0006 | New code-facing terms SHOULD use canonical spelling from this glossary. | code review |
| MFOS-REQ-GLOSS-0007 | Terms describing PKU, PKS, CET, IOMMU, Secure Boot, Measured Boot, or TPM MUST be described as mechanisms, not as MFOS semantic roots. | architecture review |
| MFOS-REQ-GLOSS-0008 | Guard-related terms MUST be explicitly scoped to High-Assurance unless the term is discussing optional Enterprise measurement helper behavior. | architecture review |

## 12. Failure Modes

FM-GLOSS-001:

If a spec uses an undefined term for a protected resource, spec review MUST fail.

FM-GLOSS-002:

If a spec uses prohibited compatibility wording, release review MUST fail.

FM-GLOSS-003:

If implementation introduces a new authority-bearing concept without a glossary entry, architecture review MUST fail.

FM-GLOSS-004:

If a hardware mechanism is described as replacing securityd, auditd, or Guard, architecture review MUST fail.

FM-GLOSS-005:

If an IBM-derived term lacks divergence, documentation review MUST fail.

## 13. Positive Tests

PT-GLOSS-001:

A document using `AMF` with EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, overlap, and divergence passes glossary lint.

PT-GLOSS-002:

A document using `JES-inspired job/spool model` with EXTREF-IBM-ZOS-JES-INTRODUCTION-0001 passes release wording lint.

PT-GLOSS-003:

A spec defining a new protected resource with source IDs, authorization rule, and audit obligation passes spec lint.

PT-GLOSS-004:

A Guard document limited to root objects and High-Assurance profile passes architecture review.

## 14. Negative Tests

NT-GLOSS-001:

A document saying `RACF compatible securityd` fails release wording lint.

NT-GLOSS-002:

A document saying `PKU provides z/OS storage key compatibility` fails architecture review.

NT-GLOSS-003:

A document adding `PrivilegedPlugin` without defining whether it is an AMF AuthorizedModule fails glossary review.

NT-GLOSS-004:

A document describing an audit log as ordinary debug output fails audit terminology review.

NT-GLOSS-005:

A document calling the first UI a root shell fails glossary review.

## 15. Fuzz Targets

No runtime parser is specified here.

Required lint/fuzz-like checks:

- `glossary_term_mutation_lint`: mutates canonical terms and validates that unknown authority-bearing terms are detected.
- `compatibility_phrase_lint`: injects prohibited compatibility terms and validates release failure.
- `source_id_presence_lint`: removes Source Matrix IDs from IBM-derived terms and validates failure.
- `hardware_claim_lint`: mutates PKU/PKS/CET/IOMMU claims into overclaims and validates failure.

## 16. Spec Gaps

SPEC-GAP-GLOSS-001:

The final machine-readable glossary schema is not defined.

SPEC-GAP-GLOSS-002:

The full DSN grammar term set is deferred to the dataset/catalog specification.

SPEC-GAP-GLOSS-003:

The full operator command vocabulary is deferred to the operator console specification.

SPEC-GAP-GLOSS-004:

The full audit record field dictionary is deferred to the audit schema specification.

SPEC-GAP-GLOSS-005:

The final multilingual terminology policy is not defined.

## 17. AI Prompt

Use this prompt when asking an AI agent to add or review MFOS terminology:

```text
You are the MFOS glossary reviewer.

MFOS is z/OS-inspired, not z/OS compatible.

For each term:
- use canonical MFOS spelling
- identify whether it is a protected resource, system interface, mechanism, profile, service, or evidence term
- include Source Matrix IDs for IBM-derived or hardware-derived concepts
- state exact semantic overlap
- state MFOS divergence
- list prohibited wording
- list allowed wording
- identify affected requirement IDs
- identify audit and authorization obligations if the term affects authority
- reject compatibility wording
- reject hardware overclaims
- reject Guard scope expansion beyond selected root objects
```
