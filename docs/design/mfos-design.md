# MFOS Source-Grounded High-Assurance Architecture v0.5

Document status: design canon candidate  
Review date: 2026-04-27  
Primary output path: `docs/design/mfos-design.md`  
Split design path: `docs/design/specs/`, `docs/design/source-matrix/`, `docs/design/prompts/`, `docs/design/assurance/`, `docs/design/tasks/`

MFOS is an independent project. References to external products and documents
are bibliographic references for source discovery, non-compatibility boundary
definition, and independent MFOS design traceability. MFOS is not affiliated
with, endorsed by, sponsored by, certified by, or approved by IBM, and it does
not claim compatibility with IBM products, interfaces, record layouts, command
syntax, macro interfaces, or documentation.

## 0. Executive Decision

MFOS is worth building, but only under a narrow and enforceable claim:

> MFOS is an x64-native, z/OS-inspired, source-grounded enterprise operating system that implements job, dataset, catalog, spool, operator, security, audit, workload, update, partition, and high-assurance root-object semantics as first-class design objects.

MFOS must not be described as a z/OS-compatible operating system, a z/Architecture emulator, a Linux clone, a UNIX-first OS, a Windows VBS clone, or a hypervisor-first research system.

Phase 0.10 adds MFVM as an MFOS-based VM management subsystem. MFVM runs in
the MFOS control plane, is less trusted than PXM Core, and requests PXM
operations through a capability-checked PXM Control API. MFVM is not an
independent hypervisor, not a nested hypervisor, not Hyper-V or KVM
compatibility work, and not a production implementation authorization. VMs are
PXM-managed VM partitions, not nested guests under MFVM.

MFOS succeeds if it can demonstrate this vertical slice before pursuing broad kernel features:

```text
operator submits a job
securityd authorizes dataset access
jobd converts and dispatches a step
datasetd opens a bound dataset handle
spoold captures SYSOUT
auditd records submit/open/execute/deny/complete evidence
operatord displays the job state and audit correlation
```

MFOS must be developed as a specification-first project. Implementation work is not allowed to invent enterprise OS semantics without a requirement ID, source matrix ID, audit obligation, and negative test.

## 1. Canonical Claim Model

MFOS has four claim layers. v0.5 splits Enterprise into standalone and PXM-backed profiles so device-assignment and side-partition claims cannot leak into a single-partition deployment.

### 1.1 Baseline Claim

Baseline MFOS claims source-grounded enterprise semantics:

```text
- z/OS-inspired system integrity model
- central security decision point
- mandatory audit obligations
- dataset/catalog/spool as protected resources
- operator console as the first privileged UI
- AMF specification present but production AMF load disabled by default
- typed SVC and PCALL interfaces
- no fake success
- NX-capable platform required
- W^X policy required
```

Baseline conformance MUST NOT be claimed if NX is unavailable, disabled, or not enforceable by the nucleus. Baseline does not claim protection after nucleus, authorized service, or AMF compromise. That is outside the baseline integrity statement.

### 1.2 Enterprise-Standalone Claim

Enterprise-Standalone adds operational trust without PXM partitioning claims:

```text
- Secure Boot required
- Measured Boot required
- TPM required
- IOMMU required for platform DMA protection
- no cross-partition device assignment claim
- no side-partition isolation claim
- remote audit export
- signed update metadata
- TUF-like rollback, freeze, and mix-and-match resistance
- SBOM and signed provenance
- partition-aware APIs
- implicit single partition allowed
```

Enterprise-Standalone may expose partition-aware APIs, but multi-partition operations and device-assignment operations MUST return `MFOS_ERR_UNSUPPORTED` unless a PXM backend is active.

### 1.3 Enterprise-PXM Claim

Enterprise-PXM adds partition lifecycle and side-partition claims:

```text
- all Enterprise-Standalone requirements
- PXM required
- IOMMU required
- interrupt remapping required
- partition lifecycle claims allowed
- side-partition isolation claims allowed
- device assignment claims allowed only after teardown tests pass
- partition audit required
```

Enterprise-PXM still does not allow PXM to interpret job, dataset, catalog, security, or workload policy semantics.

### 1.4 High-Assurance Claim

High-Assurance MFOS adds PXM Guard:

```text
- PXM required
- Guard required
- Guard-sealed security root
- Guard-sealed audit root
- Guard-approved AMF registry
- executable mapping approval
- SVC table integrity verification
- page table root constraints
- remote attestation
```

High-Assurance may claim protection of selected root objects after partial OS compromise, but only for the roots explicitly sealed by Guard.

### 1.5 AMF Claim Modes

AMF is deliberately split from baseline bring-up:

```text
Baseline-AMF-Disabled:
  AMF specification exists.
  AMF load requests return MFOS_ERR_UNSUPPORTED.
  No production AMF load is allowed.

Baseline-AMF-Test:
  Signed test-only AMF modules may load in non-production profile only.
  No production claim is allowed.

Enterprise-AMF:
  signed + measured + revocable + immutable source.
  securityd + amfd authorization required.

High-Assurance-AMF:
  Enterprise-AMF requirements
  + Guard-approved AMF registry
  + Guard-approved executable mapping.
```

## 2. Non-Compatibility Statement

MFOS is z/OS-inspired, not z/OS-compatible.

Allowed wording:

```text
z/OS-inspired
IBM Z concept-mapped
source-grounded enterprise semantics
JES-inspired job and spool model
RACF-inspired centralized security decision model
SMF-inspired audit evidence model
DFSMS-inspired catalog and dataset model
LPAR-inspired partition model
VBS/VSM-informed High-Assurance Guard profile
```

Prohibited wording:

```text
z/OS compatible
z/OS replacement
JES2 compatible
RACF compatible
DFSMS compatible
MVS compatible
z/Architecture compatible
storage-key compatible on x64
APF equivalent
RACF equivalent
SMF equivalent
Windows VBS clone
```

Every IBM-derived concept must state semantic overlap and MFOS divergence. Lack of divergence text is a documentation defect.

## 3. Normative Language

MFOS uses the following requirement terms.

```text
MUST:
  Required for the named conformance profile.

SHOULD:
  Strongly expected. Alternative requires an ADR, risk note, and evidence.

MAY:
  Optional. Does not become part of the assurance claim unless explicitly listed.

MUST NOT:
  Forbidden. Violation is a design defect, not an implementation detail.

NON-GOAL:
  Deliberately outside the design scope.

UNSUPPORTED:
  Specification exists, but implementation is not present.
  Must fail closed.

SPEC_GAP:
  Specification does not exist.
  Must not be implemented.
```

Japanese equivalents:

```text
必須       = MUST
推奨       = SHOULD
任意       = MAY
禁止       = MUST NOT
非目標     = NON-GOAL
未対応     = UNSUPPORTED
仕様未定義 = SPEC_GAP
```

Canonical language rules:

```text
Canonical language:
  English.

Machine-readable artifacts:
  English keys, IDs, enum names, error codes, ABI names, state names,
  requirement IDs, Source Matrix IDs, and evidence IDs.

Japanese documents:
  Explanatory and review material only unless a specific artifact is
  explicitly marked English/Japanese co-canonical by architecture review.
  Japanese text may clarify intent but must not override English canonical
  specs.

Conflict rule:
  If English canonical text and Japanese commentary conflict, the English
  canonical spec wins.

Synchronization rule:
  Complete Japanese mirror docs must reference the English source file,
  source section, source hash, translation unit ID, and last synchronized
  commit or artifact hash. CI must fail any Japanese mirror that changes
  normative semantics instead of updating the English canonical source.
```

## 4. Source Policy

MFOS treats sources in three classes.

```text
External Reference Source:
  Public external document used for bibliographic reference, source discovery,
  concept mapping, non-compatibility boundary definition, or independent MFOS
  design traceability. It does not by itself create compatibility, conformance,
  certification, or affiliation claims.
  Examples: IBM-published public documentation, Intel SDM, AMD APM, TUF spec,
  NIST SSDF.

Internal Transfer Source:
  Internal material whose discipline or structure is transferred into MFOS.
  Examples: FBVBS requirement/evidence structure, earlier MFOS drafts.
```

Rules:

```text
SRC-R-001  Any z/OS-inspired concept MUST cite a Source Matrix ID.
SRC-R-002  IBM product names MUST be used only for source mapping, not compatibility claims.
SRC-R-003  Hardware features MUST NOT be elevated into policy semantics.
SRC-R-004  Web source titles and URLs MUST be kept in source-matrix files.
SRC-R-005  Quoted text MUST be minimal; MFOS specs should paraphrase and map.
SRC-R-006  If a source is unavailable or ambiguous, affected requirements become SPEC_GAP.
SRC-R-007  Source Matrix YAML MUST be expressed as Source Cards, not only URL rows.
SRC-R-008  Source Cards MUST include prohibited inference and required negative tests.
SRC-R-009  Requirements MUST record source_type and semantic role for every source reference.
SRC-R-010  Source Cards MUST be public-safe bibliographic references, not summaries or substitutes for external documentation.
SRC-R-011  External vendor, product, project, organization, and specification names MUST be marked as trademark/reference-only use and MUST NOT imply affiliation, endorsement, certification, compatibility, conformance, or approval.
```

## 5. Source Matrix v0.5

Source Matrix Markdown is human-readable support material. Machine-readable Source Cards are the automation root:

```text
docs/design/source-matrix/source-matrix.yml
docs/design/source-matrix/cards/<SOURCE-ID>.yml
```

Every Source Card MUST include:

```yaml
source_id: EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
source_kind: bibliographic_reference
source_type: external_reference
semantic_role: design_background
vendor: IBM
vendor_mark_used: true
product_family: IBM z/OS
document_title: z/OS and system integrity
document_url:
  - https://www.ibm.com/docs/...
retrieved_at: 2026-04-27
reference_purpose:
  - source discovery
  - concept mapping
  - non-compatibility boundary definition
  - independent MFOS design traceability
review_topics:
  - system integrity
  - unauthorized program boundary
  - security checking
mfos_mapping:
  mfos_components:
    - MFOS System Integrity Statement
    - ExecutionState
    - AuthorityClass
  mfos_requirements:
    - MFOS-REQ-SYSINT-*
mfos_divergence:
  - MFOS does not reproduce z/Architecture PSW keys on x64.
prohibited_inference:
  - Do not claim z/OS compatibility.
  - Do not treat this card as external documentation.
required_negative_tests:
  - unauthorized SVC access
legal_controls:
  public_safe: true
  no_copied_text: true
  no_long_quotes: true
  no_tables_copied: true
  no_diagrams_copied: true
  no_record_layouts_copied: true
  no_command_syntax_copied: true
  no_macro_signatures_copied: true
  no_message_tables_copied: true
  attribution_required: true
  trademark_reference_only: true
  external_affiliation_claimed: false
  compatibility_claimed: false
  substitute_for_source: false
source_refs:
  - source_id: EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
    source_type: external_reference
    role: card_subject
requirement_refs:
  - MFOS-REQ-SYSINT-*
review_status: draft
```

Source Cards must remain public-safe bibliographic records. They must not store
copied source documents, detailed summaries, substitute documentation, copied
tables, diagrams, record layouts, command syntax, macro signatures, message
tables, or other material that would let the card replace the external source.

This table remains a compact reading aid. Split files may expand each row, but must not weaken it.

### 5.1 IBM and z/OS Sources

| Source ID | MFOS area | Source | MFOS use |
| --- | --- | --- | --- |
| EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001 | System integrity | [z/OS and system integrity](https://www.ibm.com/docs/en/zos-basic-skills?topic=zos-system-integrity) | Defines the baseline integrity meaning: unauthorized programs must not bypass protection, security checking, or obtain authorized state through system interfaces. |
| EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001 | Authorized boundary testing | [z/OS Authorized Code Scanner introduction](https://www.ibm.com/docs/en/zos/3.2.0?topic=zacsg-introduction) | Source for AMF/SVC/PCALL negative testing discipline. |
| EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001 | Authorized programs | [Authorized programs](https://www.ibm.com/docs/en/zos/3.2.0?topic=system-authorized-programs) | Source for separating supervisor state, key 0-7, and APF-authorized job-step task concepts before mapping them into AMF. |
| EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001 | Storage protection | [What is storage protection?](https://www.ibm.com/docs/en/zos-basic-skills?topic=storage-what-is-protection) | Source for storage key, PSW key, and fetch/store protection concepts. |
| EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001 | Storage protection detail | [Storage protection summary](https://www.ibm.com/docs/en/zos/3.1.0?topic=summary-storage-protection) | Public-safe background for memory-protection review topics; MFOS storage-domain definitions remain independently specified. |
| EXTREF-IBM-ZOS-SECURITY-SERVER-0001 | Security manager library | [z/OS Security Server RACF](https://www.ibm.com/docs/en/zos/3.2.0?topic=zos-security-server-racf) | Public-safe source family for authorization and audit review topics; MFOS must not copy commands, callable service interfaces, macros, or audit layouts. |
| EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001 | Resource authorization | [Authorizing users to access protected resources](https://www.ibm.com/docs/en/zos/3.1.0?topic=racf-authorizing-users-access-protected-resources) | Source for user/group/resource profile, access list, and default access mapping. |
| EXTREF-IBM-ZOS-JES-INTRODUCTION-0001 | Job subsystem | [What is JES?](https://www.ibm.com/docs/en/zos-basic-skills?topic=jobs-what-is-jes) | Source for receiving jobs, queues, initiators, SYSIN/SYSOUT, and spool semantics. |
| EXTREF-IBM-ZOS-JES-JOB-FLOW-0001 | Job lifecycle | [Job flow through the system](https://www.ibm.com/docs/en/zos-basic-skills?topic=jobs-job-flow-through-system) | Source for input, conversion, processing, output, print/punch, and purge lifecycle. |
| EXTREF-IBM-ZOS-JES2-LIBRARY-0001 | JES2 library | [z/OS JES2](https://www.ibm.com/docs/en/zos/3.2.0?topic=zos-jes2) | Public-safe source family for job/spool review topics; MFOS must not copy commands, messages, initialization procedures, or macros. |
| EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001 | Catalogs | [DFSMS catalogs](https://www.ibm.com/docs/en/zos/3.1.0?topic=dfsmsdfp-catalogs) | Source for catalog entries describing dataset attributes and locations so users need not supply physical location. |
| EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001 | Storage management | [z/OS DFSMS](https://www.ibm.com/docs/en/zos/3.2.0?topic=zos-dfsms) | Source family for dataset, catalog, allocation, storage administration, and access-method concepts. |
| EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | Audit/accounting | [Introduction to SMF](https://www.ibm.com/docs/en/zos/3.1.0?topic=smf-introduction) | Source for system/job-related records, billing, reliability, dataset activity, scheduling, and security maintenance use cases. |
| EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001 | RACF security records | [SMF type 80 RACF processing record](https://www.ibm.com/docs/en/zos/3.1.0?topic=records-record-type-80-racf-processing-record) | Source for security audit event fields, unauthorized attempts, authorized attempts, authorities used, and audit reasons. |
| EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001 | Workload management | [Defining service classes and performance goals](https://www.ibm.com/docs/SSLTBW_3.2.0/com.ibm.zos.v3r2.ieaw100/sclg.htm) | Source for service class, importance, response time, velocity-like, and discretionary goals. |
| EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001 | Optional POSIX subsystem | [Introduction to z/OS UNIX](https://www.ibm.com/docs/en/zos/3.1.0?topic=planning-introduction-zos-unix) | Source for treating UNIX as an operating environment within a larger enterprise OS, not as the MFOS primary model. |
| EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001 | UNIX Services library | [z/OS UNIX System Services](https://www.ibm.com/docs/en/zos/latest?topic=zos-unix-system-services) | Source family for optional POSIX subsystem command, file, callable-service, and planning details. |
| EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001 | Cross-memory communication | [Synchronous cross memory communication](https://www.ibm.com/docs/en/zos/3.1.0?topic=guide-synchronous-cross-memory-communication) | Source for PC instruction, PC routine, same/different address-space service calls, and authority concerns. |
| EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001 | Cross-memory security | [Controlling cross-memory communication](https://www.ibm.com/docs/en/zos-basic-skills?topic=integrity-controlling-cross-memory-communication) | Source for avoiding unsafe cross-address-space access semantics. |
| EXTREF-IBM-Z-LPAR-INTRODUCTION-0001 | Partitioning | [Introduction to Logical Partitions](https://www.ibm.com/support/pages/introduction-logical-partitions) | Source for logical machine image, physical resource partitioning, and activation profile mapping. |
| EXTREF-IBM-Z-DPM-0001 | Partition management | [Dynamic Partition Manager](https://www.ibm.com/docs/en/systems-hardware/zsystems/2964-N63?topic=cm-dynamic-partition-manager-dpm) | Source for object-oriented partition, network, storage, and capacity management plane mapping. |
| EXTREF-IBM-Z-ARCHITECTURE-PRINCIPLES-0001 | Machine terminology | [z/Architecture Principles of Operation listing](https://www.ibm.com/support/pages/zvm/library/other.html) | Source family for PSW, storage key, SVC, PC, and architectural terminology. |
| EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001 | Update advisory reference | [SECINT HOLDDATA with SMP/E RECEIVE ORDER](https://www.ibm.com/support/pages/secint-holddata-now-available-smpe-receive-order) | Informative source for security advisory distribution and update metadata design. |

### 5.2 x64, Assurance, and Supply-Chain Sources

| Source ID | MFOS area | Source | MFOS use |
| --- | --- | --- | --- |
| X64-INTEL-001 | x64 system programming | [Intel 64 and IA-32 SDM](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html) | External reference for x64 protection, paging, interrupt, VMX, MSR, CET, and related CPU semantics. |
| X64-AMD-001 | AMD64 system programming | [AMD64 APM Vol. 2](https://docs.amd.com/v/u/en-US/24593_3.44_APM_Vol2) | External reference for AMD64 system programming, SVM, NPT, and AMD-specific protection semantics. |
| X64-LINUX-PKU-001 | PKU implementation limits | [Linux memory protection keys](https://docs.kernel.org/core-api/protection-keys.html) | Informative source that x86 pkeys are PTE key plus thread-local PKRU, data-access only, and not instruction-fetch protection. |
| X64-LINUX-CET-001 | CET implementation reference | [Linux x86 CET shadow stack](https://docs.kernel.org/arch/x86/shstk.html) | Informative source for CET shadow stack and IBT deployment constraints. |
| MS-VBS-001 | VBS/HVCI reference | [Memory Integrity and VBS](https://learn.microsoft.com/en-us/windows-hardware/drivers/bringup/device-guard-and-credential-guard) | Informative source for hypervisor-protected code integrity and executable-page constraints. |
| MS-VSM-001 | VSM/VTL reference | [Virtual Secure Mode](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/tlfs/vsm) | Informative source for Guard-like isolation of root objects through higher-privilege memory controls. |
| TCG-001 | Measured boot | [TCG PC Client Platform Firmware Profile](https://trustedcomputinggroup.org/resource/pc-client-specific-platform-firmware-profile-specification/) | External reference for TPM event log and measured boot design. |
| NIST-160-001 | System security engineering | [NIST SP 800-160 Vol. 1 Rev. 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) | External reference for trustworthy secure systems engineering lifecycle. |
| NIST-218-001 | Secure development | [NIST SP 800-218 SSDF](https://csrc.nist.gov/pubs/sp/800/218/final) | External reference for minimum secure development practice. |
| NIST-193-001 | Firmware resiliency | [NIST SP 800-193](https://www.nist.gov/node/1336751) | External reference for firmware protection, detection, and recovery structure. |
| SEL4-001 | Formal assurance reference | [seL4 verification](https://sel4.org/Verification/) | Informative source for formal proof boundary discipline and explicit assumptions. |
| SLSA-001 | Supply chain | [SLSA specification](https://slsa.dev/spec/latest/) | External reference for build provenance and incremental supply-chain security levels. |
| TUF-001 | Update security | [The Update Framework specification](https://theupdateframework.github.io/specification/latest/) | External reference for root, timestamp, snapshot, targets, rollback, freeze, and mix-and-match defenses. |
| FBVBS-001 | Assurance discipline | Internal FBVBS specification | Internal transfer source for traceability, profile discipline, partition state machine, command page, update manifest, and production proof obligations. |

## 6. Architecture Overview

MFOS is partition-aware at every profile. Early boot may use an implicit single-partition backend, but APIs and object identities must still include partition context.

```text
Enterprise Management Plane
  policy distribution
  update distribution
  remote attestation
  audit collection
  operator approval workflow
  recovery orchestration

Hardware
  CPU / MMU / IOMMU / TPM / NIC / Storage / GPU

Firmware and Root of Trust
  UEFI / Secure Boot / Measured Boot / TPM event log
  firmware protection / detection / recovery

PXM Partition Manager
  partition lifecycle
  activation profile
  logical CPU / memory / device assignment
  IOMMU / interrupt remapping
  device teardown
  partition audit

PXM Guard [High-Assurance only]
  security root seal
  audit root seal
  AMF registry enforcement
  executable mapping policy
  SVC table integrity
  page table root constraints

MFOS Partition
  nucleus
  securityd
  auditd
  catalogd
  datasetd
  jobd
  spoold
  operatord
  workpolicyd
  amfd
  uvsd
  command-processor interface
  panel-ui interface
  optional POSIX subsystem

Side Partitions
  Linux/Desktop partition
  service partition
  recovery partition
```

## 7. First-Class Objects

MFOS first-class objects:

```text
Principal
Group
Role
ProgramIdentity
AuthorizedModule
Job
JobStep
JobClass
ServiceClass
ReportClass
Dataset
CatalogEntry
Volume
SpoolEntry
OperatorCommand
SecurityProfile
SecurityDecision
AuditRecord
WorkloadPolicy
Partition
ActivationProfile
GuardRoot
UpdateArtifact
EvidenceArtifact
```

Non-first-class objects:

```text
POSIX process as the primary abstraction
root shell as the first privileged interface
ordinary file as a substitute for dataset
driver plugin as a substitute for AMF
log line as a substitute for audit record
hypervisor VM as a substitute for enterprise semantics
```

## 8. Design Principles

1. IBM-published public documentation controls IBM-derived semantic mappings.
2. MFOS claims inspiration and mapping, not compatibility.
3. Object model and authorization model are the canonical design root.
4. Hardware features are enforcement aids, not policy definitions.
5. securityd is the central policy decision point.
6. auditd is an evidence service, not a logging convenience.
7. Dataset is a managed protected resource, not a POSIX file wrapper.
8. Operator console is a governed system interface, not a root shell.
9. AMF is OS extension authorization, not administrator privilege.
10. PXM performs partition isolation, not MFOS enterprise policy.
11. Guard protects selected roots only.
12. PM-present and PM-absent boots share one partition-aware API model.
13. Linux/Desktop belongs beside MFOS, not inside its integrity boundary.
14. Fake success, empty stubs, and silent fallback are prohibited.
15. Negative tests are required for security-sensitive paths.
16. Unsupported features fail closed with `MFOS_ERR_UNSUPPORTED`.
17. Undefined features are blocked as `MFOS_ERR_SPEC_GAP`.
18. Every parser is a fuzz target.
19. Every deny path that has audit obligation records evidence before returning.
20. Production claims require evidence, not only specification text.

## 9. z/OS Concept Mapping

### 9.1 System Integrity

Source: EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001

MFOS maps system integrity into this statement:

```text
An unauthorized principal, program, job, or subsystem must not use any
defined MFOS system interface to bypass security policy, dataset access
control, catalog metadata control, audit recording, spool access control,
job identity establishment, operator command authority, authorized
execution state, or system control object protection.
```

Baseline scope:

```text
Protect against unauthorized callers using legitimate system interfaces.
```

High-Assurance extension:

```text
Protect selected root objects after partial OS compromise by using PXM Guard.
```

Explicit divergence:

```text
MFOS does not reproduce z/Architecture PSW keys or storage keys on x64.
MFOS maps the authority idea to ExecutionState, AuthorityClass,
StorageDomain, typed handles, and Guard roots.
```

### 9.2 Authorized Programs and AMF

Sources: EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001

MFOS replaces APF with AMF: Authorized Module Facility.

```text
AMF is OS extension authorization.
AMF is not root, admin, plugin permission, or unrestricted kernel module loading.
```

AMF module requirements:

```text
- signed artifact
- measured artifact
- immutable catalog entry or approved artifact store
- explicit authority class
- explicit ABI
- no arbitrary pointer trust
- bounded copy-in/copy-out only
- audit required
- revocation support
- policy version binding
- Guard approval in High-Assurance profile
```

AMF negative-test classes:

```text
- revoked signer
- revoked digest
- stale security_epoch
- unsigned artifact
- mutable source location
- authority class mismatch
- arbitrary pointer ABI
- audit disable attempt
- Guard root mismatch
- unsupported ABI success attempt
```

### 9.3 Storage Key Concepts and x64 Reality

Sources: EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001, EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001, X64-INTEL-001, X64-AMD-001, X64-LINUX-PKU-001

MFOS execution states:

```text
USER_JOB
USER_SUBSYSTEM
TRUSTED_SERVICE
AUTHORIZED_SERVICE
SUPERVISOR
GUARD
PM_ROOT
```

MFOS storage domains:

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

```text
PKU MAY protect user-space compartments.
PKU MUST NOT be called a storage-key compatibility layer.
PKU MUST NOT protect system-integrity roots.
PKS MAY be used as a kernel metadata helper when available.
PKS MUST NOT replace Guard.
NX/W^X MUST be enforced in all profiles.
SMEP/SMAP SHOULD be used when available in Baseline and MUST be enforced by Enterprise-PXM and High-Assurance platform profiles when the CPU supports them.
CET SHOULD be used for trusted services when available.
```

### 9.4 RACF-Inspired securityd

Sources: EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001

securityd is the central policy decision point.

Protected resource classes:

```text
DATASET
CATALOG
SPOOL
JOB
PROGRAM
AMF_MODULE
OPERATOR_COMMAND
PARTITION
DEVICE
AUDIT_STREAM
UPDATE_ARTIFACT
GUARD_ROOT
```

Decision inputs:

```yaml
subject: SubjectRef
object: ObjectRef
operation: string
context:
  job_id: string?
  program_id: string?
  partition_id: string
  activation_profile_hash: sha384?
  emergency_state: bool
  network_origin: string?
policy_version: uint64
```

Decision results:

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

Invariant:

```text
INV-SECD-001:
  A protected resource handle must not exist unless securityd produced
  ALLOW or ALLOW_WITH_AUDIT for the same subject, object, operation,
  context, and policy_version.
```

### 9.5 JES-Inspired jobd and spoold

Sources: EXTREF-IBM-ZOS-JES-INTRODUCTION-0001, EXTREF-IBM-ZOS-JES-JOB-FLOW-0001, EXTREF-IBM-ZOS-JES2-LIBRARY-0001

jobd responsibilities:

```text
job submission
JCL-like subset parsing
job identity establishment
conversion
queue management
initiator management
step execution
DD resolution
return code collection
restart metadata
job cancellation
job accounting
```

spoold responsibilities:

```text
SYSIN storage
SYSOUT capture
spool entry ownership
output class
browse
purge
export
retention
spool quota
securityd-mediated access
```

Job lifecycle:

```text
SUBMITTED
  -> INPUT
  -> CONVERSION
  -> VALIDATED
  -> QUEUED
  -> SELECTED
  -> EXECUTING_STEP
  -> STEP_COMPLETE
  -> OUTPUT
  -> COMPLETE
  -> PURGE_PENDING
  -> PURGED
```

Failure states:

```text
JCL_ERROR
SECURITY_DENIED
DATASET_OPEN_DENIED
PROGRAM_LOAD_DENIED
STEP_FAILED
CANCELED
HELD
ABENDED
```

### 9.6 DFSMS-Inspired catalogd and datasetd

Sources: EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001, EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001

catalogd maps:

```text
DSN -> attributes + location + owner + security_profile + generation + integrity_tag
```

datasetd manages:

```text
allocation
open/close
record access
block access
access method
retention
encryption policy hook
integrity policy
backup hook
quota
secure deletion policy
```

Dataset open lifecycle:

```text
REQUEST_OPEN
  -> RESOLVE_CATALOG
  -> AUTHORIZE
  -> CREATE_HANDLE
  -> OPEN_ACTIVE
  -> CLOSE_REQUESTED
  -> HANDLE_REVOKED
  -> CLOSED
```

Invariant:

```text
INV-DATA-001:
  A dataset handle is bound to subject, operation, policy_version,
  catalog_entry_generation, and expiry.
```

### 9.7 SMF-Inspired auditd

Sources: EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001

auditd is an evidence service.

Audit trust levels:

```text
AUD-L0  diagnostic console output
AUD-L1  local auditd append log
AUD-L2  hash-chained local audit
AUD-L3  remote exported audit
AUD-L4  Guard-sealed audit root
AUD-L5  external/OOB authoritative audit path
```

Audit record minimum:

```yaml
AuditRecord:
  magic: "MFAR"
  schema_version: uint16
  record_id: uuid
  timestamp_utc: timestamp
  partition_id: uint64
  component_id: string
  correlation_id: uuid
  subject: SubjectRef
  object: ObjectRef
  operation: string
  decision: string
  reason_code: string
  policy_version: uint64
  activation_profile_hash: sha384?
  measurement_context: sha384?
  previous_hash: sha384
  payload_hash: sha384
  record_hash: sha384
  signature: signature?
```

Critical rule:

```text
DENY decisions with audit obligation must be recorded before the caller
receives the final result.
```

### 9.8 External Workload Management-Informed workpolicyd

Source: EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001

workpolicyd phases:

```text
Phase 1:
  job class
  priority
  max concurrent
  resource cap

Phase 2:
  service class
  report class
  importance
  velocity-like goal

Phase 3:
  response-time goal
  policy activation
  operator workload policy panel
```

workpolicyd does not authorize protected-resource access. It supplies scheduling and dispatch hints after securityd has authorized the work.

### 9.9 Optional z/OS UNIX-Inspired POSIX Subsystem

Sources: EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001, EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001

MFOS POSIX subsystem:

```text
optional
profile-limited
not the first user model
cannot bypass securityd
cannot bypass auditd
cannot reinterpret dataset as ordinary POSIX file
cannot introduce root shell as the primary privileged UI
```

### 9.10 PCALL and Cross-Memory Mapping

Sources: EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001, EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001

MFOS PCALL is a typed synchronous service call. Early MFOS must not implement arbitrary cross-address-space pointer access.

PCALL rules:

```text
- typed endpoint
- typed request
- bounded payload
- caller principal included by nucleus or trusted service context
- job identity included when applicable
- program identity included when applicable
- securityd remains final PDP
- audit obligation propagates
- unsupported call returns MFOS_ERR_UNSUPPORTED
- undefined call returns MFOS_ERR_SPEC_GAP
```

### 9.11 LPAR-Inspired PXM

Sources: EXTREF-IBM-Z-LPAR-INTRODUCTION-0001, EXTREF-IBM-Z-DPM-0001, FBVBS-001

PXM is a partition isolation layer, not MFOS enterprise semantics.

PXM responsibilities:

```text
partition create
partition measure
partition load
partition activate
partition start
partition quiesce
partition resume
partition recover
partition destroy
memory zero before reuse
logical CPU assignment
memory domain assignment
IOMMU domain setup
interrupt remapping
device assignment
device teardown
partition audit
service/recovery partition coordination
```

PXM must not:

```text
parse JCL
decide dataset access
interpret RACF-like profiles
manage spool content
schedule jobs
understand workload policy service classes
interpret operator business commands
own securityd policy
own auditd schema semantics
```

PXM lifecycle:

```text
DEFINED
  -> MEASURED
  -> LOADED
  -> ACTIVATED
  -> RUNNABLE
  -> RUNNING
  -> QUIESCED
  -> RUNNABLE

RUNNING/RUNNABLE/QUIESCED -> FAULTED
FAULTED -> RUNNABLE after recover
QUIESCED/FAULTED/ACTIVATED/LOADED/MEASURED/DEFINED -> DESTROYED
```

Invariant:

```text
INV-PXM-001:
  Partition memory cannot be reassigned until all CPU mappings,
  IOMMU mappings, interrupt routes, and device ownership records
  are revoked and the memory is zeroed.
```

### 9.12 VBS/VSM-Informed PXM Guard

Sources: MS-VBS-001, MS-VSM-001

Guard protects only selected root objects:

```text
GUARD_ROOT_SECURITY_POLICY
GUARD_ROOT_AUDIT_CHAIN
GUARD_ROOT_AMF_REGISTRY
GUARD_ROOT_SVC_TABLE
GUARD_ROOT_NUCLEUS_TEXT
GUARD_ROOT_EXECUTABLE_MAPPING_POLICY
GUARD_ROOT_PAGE_TABLE_POLICY
GUARD_ROOT_ACTIVATION_PROFILE
GUARD_ROOT_EMERGENCY_STATE
GUARD_ROOT_UPDATE_POLICY
```

Guard does not protect or interpret:

```text
ordinary dataset contents
job scheduling semantics
spool formatting
operator UI rendering
POSIX subsystem behavior
Linux desktop apps
normal business policy interpretation
```

Guard call API:

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

## 10. x64 Reality Mapping

MFOS maps IBM Z concepts to x64 conservatively.

Available x64 enforcement families:

```text
ring 0 / ring 3
page tables
user/supervisor page bit
read/write/execute controls
NX
SMEP
SMAP
CET
PKU
PKS where available
IOMMU
VT-x / AMD-V
EPT / NPT
TPM / measured boot
```

Rules:

```text
X64-R-001  x64 storage protection must not be described as z/OS storage-key compatibility.
X64-R-002  PKU is a compartment helper only.
X64-R-003  PKU must not protect instruction fetch on x86.
X64-R-004  PKRU user accessibility must be included in threat models.
X64-R-005  PKS availability must be profile-gated and CPU-feature-gated.
X64-R-006  IOMMU and interrupt remapping are mandatory for device assignment claims.
X64-R-007  EPT/NPT protections may support Guard, but Guard policy must remain explicitly modeled.
X64-R-008  CET support must be treated as platform-dependent until CPU and toolchain profiles are pinned.
```

## 11. Component Contracts

### 11.1 Nucleus

Responsibilities:

```text
NUC-R-001  boot handoff
NUC-R-002  address spaces
NUC-R-003  SVC entry
NUC-R-004  typed object handles
NUC-R-005  IPC primitive
NUC-R-006  scheduler baseline
NUC-R-007  page table management
NUC-R-008  NX/W^X enforcement
NUC-R-009  copy-in/copy-out
NUC-R-010  service lifecycle
NUC-R-011  fault containment
NUC-R-012  kernel audit hook
NUC-R-013  crash dump trigger
```

Non-responsibilities:

```text
RACF-like policy decision
dataset semantics
catalog semantics
spool formatting
job scheduling policy
workload policy
desktop
Linux compatibility
broad driver ecosystem
update policy semantics
```

### 11.2 securityd

Requirements:

```text
SECD-R-001  principal registry
SECD-R-002  group / role registry
SECD-R-003  resource profiles
SECD-R-004  dataset access decisions
SECD-R-005  spool access decisions
SECD-R-006  job submission decisions
SECD-R-007  operator command decisions
SECD-R-008  AMF load decisions
SECD-R-009  partition operation decisions
SECD-R-010  emergency access / break-glass
SECD-R-011  delegation
SECD-R-012  policy versioning
SECD-R-013  policy transaction / rollback
SECD-R-014  audit obligation generation
```

### 11.3 auditd

Requirements:

```text
AUD-R-001  append-only record stream
AUD-R-002  schema validation
AUD-R-003  hash chain
AUD-R-004  local durable store
AUD-R-005  remote export
AUD-R-006  audit query authorization
AUD-R-007  audit retention
AUD-R-008  audit failure policy
AUD-R-009  correlation ID management
AUD-R-010  Guard-sealed root in HA profile
```

### 11.4 catalogd

Requirements:

```text
CAT-R-001  DSN grammar
CAT-R-002  catalog entry creation
CAT-R-003  DSN resolution
CAT-R-004  system dataset marking
CAT-R-005  immutable catalog entry
CAT-R-006  generation tracking
CAT-R-007  volume mapping
CAT-R-008  catalog transaction
CAT-R-009  crash recovery
CAT-R-010  catalog integrity check
```

### 11.5 datasetd

Requirements:

```text
DATA-R-001  allocation
DATA-R-002  open/close
DATA-R-003  record access
DATA-R-004  block access
DATA-R-005  dataset handle lifecycle
DATA-R-006  retention enforcement
DATA-R-007  encryption policy hook
DATA-R-008  integrity tag verification
DATA-R-009  backup hook
DATA-R-010  secure deletion policy
```

### 11.6 jobd

Requirements:

```text
JOB-R-001  job submission
JOB-R-002  JCL-like subset parser
JOB-R-003  job identity establishment
JOB-R-004  conversion
JOB-R-005  queue management
JOB-R-006  initiator management
JOB-R-007  step execution
JOB-R-008  DD resolution
JOB-R-009  return code collection
JOB-R-010  restart metadata
JOB-R-011  job cancellation
JOB-R-012  job accounting
```

### 11.7 spoold

Requirements:

```text
SPL-R-001  SYSIN storage
SPL-R-002  SYSOUT capture
SPL-R-003  spool entry ownership
SPL-R-004  output class
SPL-R-005  browse
SPL-R-006  purge
SPL-R-007  export
SPL-R-008  retention
SPL-R-009  spool quota
SPL-R-010  securityd-mediated access
```

### 11.8 operatord

Requirements:

```text
OPER-R-001  first interactive interface
OPER-R-002  command grammar
OPER-R-003  command authorization
OPER-R-004  command audit
OPER-R-005  system state display
OPER-R-006  job control
OPER-R-007  dataset definition workflow
OPER-R-008  emergency mode
OPER-R-009  safe confirmation
OPER-R-010  automation hook
```

### 11.9 workpolicyd

Requirements:

```text
WPOL-R-001  job class
WPOL-R-002  service class
WPOL-R-003  priority
WPOL-R-004  resource cap
WPOL-R-005  dispatch hint
WPOL-R-006  max concurrency
WPOL-R-007  overload policy
WPOL-R-008  report class
WPOL-R-009  future response time goal
WPOL-R-010  future velocity-like goal
```

### 11.10 amfd

Requirements:

```text
AMF-R-001  AMF manifest parser
AMF-R-002  signature verification
AMF-R-003  artifact measurement
AMF-R-004  immutable catalog check
AMF-R-005  authority class check
AMF-R-006  ABI validation
AMF-R-007  revocation check
AMF-R-008  audit
AMF-R-009  Guard approval in HA
AMF-R-010  load failure fail-closed
```

### 11.11 uvsd

Sources: TUF-001, SLSA-001, NIST-218-001

Requirements:

```text
UVS-R-001  update metadata verification
UVS-R-002  artifact signature verification
UVS-R-003  artifact hash / size check
UVS-R-004  generation / security_epoch check
UVS-R-005  rollback prevention
UVS-R-006  freeze detection
UVS-R-007  mix-and-match detection
UVS-R-008  revocation check
UVS-R-009  dependency check
UVS-R-010  staged activation profile update
UVS-R-011  audit
UVS-R-012  recovery rollback workflow
```

## 12. Core Object Model

### 12.1 Principal

```yaml
Principal:
  principal_id: string
  auth_methods: [PASSWORD, CERTIFICATE, KERBEROS, PASSKEY, MFA_TOKEN]
  groups: [string]
  roles: [string]
  labels: [string]
  status: ACTIVE | DISABLED | LOCKED | EXPIRED
  expiry: timestamp?
  emergency_flags:
    break_glass_allowed: bool
    emergency_expiry: timestamp?
```

### 12.2 ProgramIdentity

```yaml
ProgramIdentity:
  program_id: string
  dsn_or_artifact_id: string
  signer: string?
  digest: sha384
  catalog_entry_generation: uint64
  amf_authorized: bool
  authority_class: string?
  allowed_service_classes: [string]
  measurement_context: string?
```

### 12.3 Job

```yaml
Job:
  job_id: string
  job_name: string
  submitter: PrincipalRef
  effective_principal: PrincipalRef
  program_identities: [ProgramIdentity]
  job_class: string
  service_class: string
  report_class: string?
  status: JobStatus
  steps: [JobStep]
  return_code: int?
  spool_refs: [SpoolEntryRef]
  audit_correlation_id: uuid
```

### 12.4 Dataset

```yaml
Dataset:
  dsn: string
  owner: PrincipalRef
  dataset_type: SEQ | PDS_LITE | SYSIN | SYSOUT | LOG | CAT | POLICY | MODULE
  catalog_entry: CatalogEntryRef
  security_profile: SecurityProfileRef
  retention_policy: RetentionPolicyRef
  encryption_policy: EncryptionPolicyRef?
  integrity_policy: IntegrityPolicyRef
  generation: uint64
  status: ACTIVE | MIGRATED | LOCKED | DELETING | DELETED
```

### 12.5 CatalogEntry

```yaml
CatalogEntry:
  dsn: string
  attributes: map
  location: [VolumeExtentRef]
  owner: PrincipalRef
  generation: uint64
  immutable: bool
  system_dataset: bool
  integrity_tag: sha384
  created_at: timestamp
  updated_at: timestamp
```

### 12.6 SpoolEntry

```yaml
SpoolEntry:
  spool_id: string
  job_id: string
  owner: PrincipalRef
  output_class: string
  sysout_dataset_ref: DatasetRef
  security_profile: SecurityProfileRef
  retention_policy: RetentionPolicyRef
  status: OPEN | CLOSED | HELD | PURGE_PENDING | PURGED
```

### 12.7 SecurityProfile

```yaml
SecurityProfile:
  profile_id: string
  resource_class: string
  resource_pattern: string
  owner: PrincipalRef
  default_access: NONE | READ | UPDATE | CONTROL | ALTER
  access_list:
    - subject: PrincipalRef | GroupRef | RoleRef
      access: NONE | READ | UPDATE | CONTROL | ALTER
      audit: NONE | SUCCESS | FAILURE | ALL
  labels: [string]
  policy_version: uint64
  created_at: timestamp
  updated_at: timestamp
```

### 12.8 Partition

```yaml
Partition:
  partition_id: uint64
  name: string
  profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  state: DEFINED | MEASURED | LOADED | ACTIVATED | RUNNABLE | RUNNING | QUIESCED | FAULTED | DEACTIVATED | DESTROYED
  activation_profile_hash: sha384
  assigned_cpus: [CpuRef]
  memory_domains: [MemoryDomainRef]
  iommu_domains: [IommuDomainRef]
  device_assignments: [DeviceAssignmentRef]
  audit_correlation_id: uuid
```

### 12.9 UpdateArtifact

```yaml
UpdateArtifact:
  component_type: nucleus | service | amf_module | policy_bundle | pxm_core | pxm_guard | recovery_image
  component_id: string
  component_version: semver
  target_arch: x86_64
  hash_algorithm: sha384
  hash_value: hex
  size: uint64
  generation: uint64
  security_epoch: uint64
  signing_key_id: string
  signature: string
  source_matrix_refs: [string]
```

## 13. State Machines

### 13.1 Boot / IPL

```text
POWER_ON
  -> FIRMWARE_INIT
  -> SECURE_BOOT_VERIFY
  -> MEASURE_BOOT_CHAIN
  -> PXM_LOAD            [Enterprise-PXM/HA]
  -> PXM_MEASURE         [Enterprise-PXM/HA]
  -> GUARD_INIT          [HA only]
  -> MFOS_LOAD
  -> MFOS_NUCLEUS_INIT
  -> SERVICE_START_AUDITD
  -> SERVICE_START_SECURITYD
  -> SERVICE_START_CATALOGD
  -> SERVICE_START_DATASETD
  -> SERVICE_START_SPOOLD
  -> SERVICE_START_JOBD
  -> SERVICE_START_OPERATORD
  -> OPERATOR_READY
```

Failure rules:

```text
auditd start failure:
  Baseline:
    enter OPERATOR_RECOVERY_MODE only
    no job submit
    no dataset open except explicitly marked recovery datasets
    no policy update
    no AMF load
    no update activation
  Enterprise-Standalone:
    enter OPERATOR_RECOVERY_MODE only unless recovery policy proves required audit sink availability
  Enterprise-PXM:
    enter OPERATOR_RECOVERY_MODE only unless PXM boot audit sink can be reconciled
  High-Assurance:
    boot stop or recovery mode

securityd start failure:
  all profiles:
    operator recovery mode only

Guard required but unavailable:
  High-Assurance:
    boot denied
```

### 13.2 Catalog Transaction

```text
BEGIN_TX
  -> VALIDATE_DSN
  -> AUTHORIZE_CATALOG_UPDATE
  -> PREPARE_ENTRY
  -> WRITE_JOURNAL
  -> COMMIT_ENTRY
  -> WRITE_AUDIT
  -> COMPLETE
```

Crash recovery:

```text
RECOVER_SCAN_JOURNAL
  -> ROLLBACK_INCOMPLETE
  -> VERIFY_COMMITTED
  -> REPAIR_ORPHAN_EXTENTS
  -> AUDIT_RECOVERY
```

### 13.3 Operator Command

```text
PARSE_COMMAND
  -> IDENTIFY_COMMAND
  -> RESOLVE_TARGET
  -> AUTHORIZE
  -> REQUIRE_CONFIRMATION?
  -> REQUIRE_DUAL_CONTROL?
  -> EXECUTE
  -> AUDIT
  -> DISPLAY_RESULT
```

### 13.4 AMF Load

```text
REQUEST_LOAD
  -> RESOLVE_ARTIFACT
  -> VERIFY_SIGNATURE
  -> VERIFY_MANIFEST
  -> CHECK_REVOCATION
  -> CHECK_CATALOG_IMMUTABILITY
  -> SECURITYD_AUTHORIZE
  -> GUARD_APPROVE?      [HA]
  -> MAP_RX
  -> REGISTER_AMF
  -> AUDIT
  -> READY
```

### 13.5 Update Lifecycle

```text
RECEIVE_METADATA
  -> VERIFY_ROOT
  -> VERIFY_TIMESTAMP
  -> VERIFY_SNAPSHOT
  -> VERIFY_TARGETS
  -> VERIFY_ARTIFACT
  -> CHECK_EPOCH
  -> CHECK_DEPENDENCIES
  -> STAGE
  -> APPROVE
  -> ACTIVATE_PROFILE_UPDATE
  -> REBOOT_OR_SWITCH
  -> MEASURE
  -> COMMIT
```

## 14. ABIs

### 14.1 SVC ABI

```text
caller:
  user job / user subsystem / trusted service

callee:
  MFOS nucleus

purpose:
  kernel object operation

rules:
  caller identity from scheduler context
  no caller-supplied identity accepted
  user pointers are opaque until validated
  bounded copy-in/copy-out only
  unsupported call returns MFOS_ERR_UNSUPPORTED
  undefined call returns MFOS_ERR_SPEC_GAP
  no success without audit if audit obligation exists
```

### 14.2 PCALL ABI

```text
caller:
  trusted service or nucleus-mediated caller

callee:
  trusted service endpoint

purpose:
  synchronous service call

rules:
  typed endpoint
  typed request
  bounded payload
  caller principal / job / program identity included
  securityd is final PDP
  audit obligation propagated
```

### 14.3 PXM CALL ABI

```text
CREATE_PARTITION
MEASURE_PARTITION
LOAD_PARTITION
ACTIVATE_PARTITION
START_PARTITION
QUIESCE_PARTITION
RESUME_PARTITION
RECOVER_PARTITION
DESTROY_PARTITION
ASSIGN_DEVICE
RELEASE_DEVICE
GET_PARTITION_STATUS
GET_FAULT_INFO
```

### 14.4 GUARD CALL ABI

```text
SEAL_ROOT
VERIFY_ROOT
AUTHORIZE_EXEC_MAPPING
AUTHORIZE_AMF_LOAD
APPEND_AUDIT_ROOT
ATTEST
```

## 15. Error Model

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

Error rules:

```text
UNSUPPORTED:
  Specification exists but implementation is absent.
  It must fail closed.

SPEC_GAP:
  Specification is absent.
  It must not be implemented.

INTERNAL_CORRUPTION:
  Integrity invariant failed.
  It must produce audit evidence if possible and enter recovery/lockdown
  according to profile.
```

## 16. Requirements Catalog

Requirement namespaces:

```text
MFOS-REQ-SRC-*   source grounding
MFOS-REQ-SI-*    system integrity
MFOS-REQ-SEC-*   securityd
MFOS-REQ-AUD-*   auditd
MFOS-REQ-CAT-*   catalogd
MFOS-REQ-DATA-*  datasetd
MFOS-REQ-JOB-*   jobd
MFOS-REQ-SPL-*   spoold
MFOS-REQ-OPER-*  operatord
MFOS-REQ-WPOL-*   workpolicyd
MFOS-REQ-AMF-*   authorized module facility
MFOS-REQ-UVS-*   update verification service
MFOS-REQ-NUC-*   nucleus
MFOS-REQ-PXM-*   partition manager
MFOS-REQ-GRD-*   guard
MFOS-REQ-AI-*    AI implementation contract
MFOS-REQ-QUAL-*  quality and supply chain
MFOS-REQ-PROF-*  conformance profile boundaries
MFOS-REQ-LANG-*  language and translation synchronization
MFOS-REQ-POLICY-LINT-* policy lint
MFOS-REQ-TEST-*  test strategy
MFOS-REQ-PROD-*  production readiness
```

Machine-readable requirements are canonical for automation:

```text
docs/design/registries/requirements.yaml
```

Every requirement entry MUST include requirement ID, source references with `source_type` and semantic role, profile applicability for `baseline`, `enterprise_standalone`, `enterprise_pxm`, and `high_assurance`, verification method, positive and negative tests, audit obligation, failure mode, required evidence, and status.

### 16.1 Source Grounding

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-SOURCE-0001 | z/OS-derived concepts MUST cite Source Matrix IDs. | inspection |
| MFOS-REQ-SOURCE-0002 | IBM terminology used as MFOS terminology MUST state overlap and divergence. | documentation review |
| MFOS-REQ-SOURCE-0003 | MFOS MUST NOT claim z/OS compatibility. | release review |
| MFOS-REQ-SOURCE-0004 | Behavior not grounded in IBM-published source documents MUST NOT be called z/OS-like. | architecture review |
| MFOS-REQ-SRC-0005 | Specs MUST paraphrase source concepts and avoid long quotations. | documentation review |

### 16.2 System Integrity

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-SYSINT-0001 | Unauthorized subjects MUST NOT bypass security policy, dataset access, audit, or authorized state through system interfaces. | negative test / proof |
| MFOS-REQ-SYSINT-0002 | System interfaces MUST be enumerated in specs. | inspection |
| MFOS-REQ-SYSINT-0003 | SVC, PCALL, operator command, dataset open, catalog update, and job submit MUST be system interfaces. | inspection |
| MFOS-REQ-SYSINT-0004 | Authorized state MUST be separated into ExecutionState and AuthorityClass. | model review |
| MFOS-REQ-SYSINT-0005 | Baseline MUST NOT claim root protection after authorized module compromise. | claim review |
| MFOS-REQ-SYSINT-0006 | High-Assurance root protection MUST be tied to PXM Guard. | evidence review |
| MFOS-REQ-SYSINT-0007 | Supervisor code MUST NOT directly dereference user pointers. | code review / fuzz |
| MFOS-REQ-SYSINT-0008 | copy-in/copy-out MUST use typed buffers and length bounds. | unit / negative test |
| MFOS-REQ-SYSINT-0009 | SVC/PCALL routines MUST safely handle untrusted input. | zACS-style negative test |
| MFOS-REQ-SYSINT-0010 | Unsupported system interfaces MUST NOT return success. | no-fake-success CI |

### 16.3 securityd

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-AUTH-0001 | securityd MUST be the central decision point for protected resource access. | architecture inspection |
| MFOS-REQ-AUTH-0002 | Decisions MUST include subject, object, operation, context, and policy_version. | interface test |
| MFOS-REQ-AUTH-0003 | Decisions MUST return obligations, not only allow/deny. | interface test |
| MFOS-REQ-AUTH-0004 | datasetd MUST NOT issue protected handles without securityd. | negative test |
| MFOS-REQ-AUTH-0005 | jobd MUST obtain decisions before submit and step execute. | integration test |
| MFOS-REQ-AUTH-0006 | operatord MUST obtain decisions before command execute. | command negative test |
| MFOS-REQ-SEC-0007 | AMF load MUST pass through securityd and amfd. | AMF negative test |
| MFOS-REQ-AUTH-0008 | Policy updates MUST be transactional and increment policy_version. | transaction test |
| MFOS-REQ-AUTH-0009 | Break-glass MUST include reason, expiry, operator identity, and audit. | emergency drill |
| MFOS-REQ-SEC-0010 | Policy rollback MUST require audit and approval. | rollback test |

### 16.4 auditd

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-AUDIT-0001 | Security decisions MUST include audit obligations. | traceability audit |
| MFOS-REQ-AUDIT-0002 | DENY with audit obligation MUST be recorded before final caller result. | negative test |
| MFOS-REQ-AUDIT-0003 | Audit records MUST include schema_version, record_id, timestamp, subject, object, operation, decision, reason_code, and policy_version. | schema test |
| MFOS-REQ-AUDIT-0004 | Audit log MUST include a hash chain. | tamper test |
| MFOS-REQ-AUDIT-0005 | auditd unavailable policy MUST be profile-specific. | fault injection |
| MFOS-REQ-AUD-0006 | Enterprise-Standalone, Enterprise-PXM, and High-Assurance MUST implement remote export. | integration test |
| MFOS-REQ-AUD-0007 | High-Assurance MUST use Guard-sealed audit root. | Guard test |
| MFOS-REQ-AUD-0008 | Spool output MUST NOT be treated as audit evidence. | documentation review |

### 16.5 Dataset and Catalog

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-CAT-0001 | DSN grammar MUST be specified. | parser test / fuzz |
| MFOS-REQ-CATALOG-0002 | catalogd MUST resolve only committed catalog entries. | transaction test / crash-recovery negative test |
| MFOS-REQ-CATALOG-0003 | Catalog entries MUST include owner, attributes, location, security_profile, generation, and integrity_tag. | schema test |
| MFOS-REQ-CATALOG-0004 | System datasets MUST support immutable flag. | negative test |
| MFOS-REQ-CAT-0005 | Catalog transactions MUST be crash recoverable. | crash test |
| MFOS-REQ-DATASET-0001 | Dataset handles MUST bind subject, operation, policy_version, and catalog_generation. | stale handle test |
| MFOS-REQ-DATASET-0002 | Unauthorized access MUST NOT create dataset handles. | negative test |
| MFOS-REQ-DATASET-0003 | Retention policy MUST affect purge/delete. | retention test |
| MFOS-REQ-DATASET-0004 | Encryption policy MUST bind to key service, TPM, or Guard profile. | integration test |
| MFOS-REQ-DATASET-0005 | Dataset MUST NOT be defined as a POSIX file wrapper. | architecture review |

Mandatory CAT-0002 negative tests:

```text
- resolve uncommitted catalog entry
- resolve rolled-back catalog entry
- resolve partially written journal entry
- resolve entry whose integrity_tag does not match
```

### 16.6 Job and Spool

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-JOB-0001 | Job lifecycle MUST include input, conversion, queue, execute, output, and purge phases. | state-machine test |
| MFOS-REQ-JOB-0002 | JCL-like parser MUST be fuzzed. | fuzz campaign |
| MFOS-REQ-JOB-0003 | Effective principal MUST be established before dataset open. | integration test |
| MFOS-REQ-JOB-0004 | DD resolution MUST pass through catalogd and securityd. | integration test |
| MFOS-REQ-JOB-0005 | Step failure MUST include return code or abend-like reason. | unit test |
| MFOS-REQ-SPOOL-0001 | Spool entry MUST be a protected resource. | security test |
| MFOS-REQ-SPL-0002 | Spool browse, purge, and export MUST require securityd decision. | negative test |
| MFOS-REQ-SPOOL-0003 | SYSOUT MUST include owner, job_id, output_class, and security_profile. | schema test |
| MFOS-REQ-SPOOL-0004 | Spool retention MUST affect purge. | retention test |

### 16.7 Operator

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-OPER-0001 | First privileged UI MUST be operator console, not root shell. | boot test |
| MFOS-REQ-OPER-0002 | Operator command grammar MUST be specified. | parser test / fuzz |
| MFOS-REQ-OPER-0003 | Operator commands MUST have authority classes. | schema review |
| MFOS-REQ-OPER-0004 | Destructive commands MUST support confirmation or dual control. | operator drill |
| MFOS-REQ-OPER-0005 | Operator commands MUST generate audit records. | audit test |
| MFOS-REQ-OPER-0006 | Automation hooks MUST NOT bypass operator authority and audit. | negative test |

### 16.8 AMF

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-AMF-0001 | AMF modules MUST be signed artifacts. | signature test |
| MFOS-REQ-AMF-0002 | AMF modules MUST load only from immutable system dataset or approved artifact store. | negative test |
| MFOS-REQ-AMF-0003 | AMF modules MUST declare explicit authority class. | manifest test |
| MFOS-REQ-AMF-0004 | AMF load MUST be audited. | audit test |
| MFOS-REQ-AMF-0005 | Revoked signer, digest, or security_epoch MUST fail closed. | revocation test |
| MFOS-REQ-AMF-0006 | High-Assurance MUST Guard-seal AMF registry. | Guard test |
| MFOS-REQ-AMF-0007 | AMF modules MUST NOT have audit-disable authority. | architecture review |
| MFOS-REQ-AMF-0008 | AMF ABI MUST NOT accept arbitrary pointers. | ABI review / fuzz |

### 16.9 PXM

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-PARTITION-0001 | MFOS MUST expose partition-aware APIs. | API test |
| MFOS-REQ-PARTITION-0002 | PM-free boot MUST be represented as implicit single-partition backend. | boot test |
| MFOS-REQ-PARTITION-0003 | PXM Core MUST be limited to partition lifecycle and isolation. | architecture review |
| MFOS-REQ-PARTITION-0004 | PXM MUST NOT interpret dataset/job/security semantics. | architecture review |
| MFOS-REQ-PARTITION-0005 | Enterprise-PXM and High-Assurance device assignment MUST require IOMMU domain and interrupt remapping; Enterprise-Standalone MUST NOT claim cross-partition device assignment. | device test |
| MFOS-REQ-PARTITION-0006 | Device reassignment MUST wait for teardown checklist completion. | negative test |
| MFOS-REQ-PARTITION-0007 | Destroyed partition memory MUST be zeroed before reuse. | memory reuse test |
| MFOS-REQ-PARTITION-0008 | Partition operations MUST generate audit records. | audit test |

### 16.10 Guard

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-GUARD-0001 | Guard MUST be required only in High-Assurance. | profile review |
| MFOS-REQ-GUARD-0002 | Guard scope MUST be limited to root objects. | architecture review |
| MFOS-REQ-GUARD-0003 | Guard MUST NOT interpret dataset policy. | architecture review |
| MFOS-REQ-GUARD-0004 | Security root transitions MUST be recorded by Guard and auditd. | integration test |
| MFOS-REQ-GUARD-0005 | Executable mappings MUST comply with Guard policy. | negative test |
| MFOS-REQ-GRD-0006 | SVC table mismatch MUST trigger lockdown or panic-equivalent. | fault injection |
| MFOS-REQ-GRD-0007 | AMF registry mismatch MUST deny AMF load and audit alert. | negative test |
| MFOS-REQ-GUARD-0008 | Guard unavailable boot policy MUST be profile-specific. | boot test |

### 16.11 Quality and Supply Chain

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-QUALITY-0001 | requirements, design, code, tests, and evidence MUST have bidirectional traceability. | traceability audit |
| MFOS-REQ-QUALITY-0002 | Security-sensitive PRs MUST include spec IDs and negative tests. | CI gate |
| MFOS-REQ-QUALITY-0003 | TCB changes MUST require independent review. | review audit |
| MFOS-REQ-QUALITY-0004 | unsafe code MUST have safety contracts. | code review |
| MFOS-REQ-QUALITY-0005 | Parsers MUST have fuzz targets. | fuzz campaign |
| MFOS-REQ-QUALITY-0006 | Release artifacts MUST include SBOM and signed provenance. | supply-chain audit |
| MFOS-REQ-QUALITY-0007 | no-fake-success CI MUST exist. | CI |
| MFOS-REQ-QUALITY-0008 | Build toolchain MUST be pinned. | build inspection |
| MFOS-REQ-QUALITY-0009 | Dependency allowlist MUST exist. | dependency audit |
| MFOS-REQ-QUALITY-0010 | Production claim MUST be blocked until production readiness gate passes. | release review |

## 17. Update Artifact Manifest

```yaml
manifest_version: 1
component_type: nucleus | service | amf_module | policy_bundle | pxm_core | pxm_guard | recovery_image
component_id: string
component_version: semver
target_arch: x86_64
target_vendor: intel | amd | any
required_cpu_features:
  - nx
  - smep
  - smap
  - cet?
  - pku?
  - pks?
  - iommu?
profile_applicability:
  - Baseline
  - Enterprise-Standalone
  - Enterprise-PXM
  - High-Assurance
hash:
  algorithm: sha384
  value: hex
size: uint64
generation: uint64
security_epoch: uint64
dependencies:
  - component_id: string
    min_version: semver
conflicts:
  - component_id: string
    max_version: semver
signing_key_id: string
signature: string
revocation_refs:
  - string
rollback_policy:
  min_generation: uint64
guard_required: bool
activation_profile_constraints:
  - string
audit_class: UPDATE_SECURITY_CRITICAL
source_matrix_refs:
  - EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
  - TUF-001
```

## 18. Repository and Design Structure

Target project structure:

```text
mfos/
  README.md
  adr/
  docs/
    design/
      mfos-design.md
      source-matrix/
        source-matrix.md
      specs/
        00-normative-language.md
        01-glossary.md
        02-source-matrix.md
        03-system-integrity.md
        04-threat-model.md
        05-object-model.md
        06-authorization.md
        07-audit.md
        08-dataset-catalog.md
        09-job-spool.md
        10-operator-console.md
        11-workload-policy.md
        12-amf.md
        13-update.md
        14-nucleus.md
        15-svc-pcall.md
        16-pxm.md
        17-guard.md
        18-linux-gateway.md
        19-assurance-case.md
        20-conformance.md
      prompts/
        ai-prompts.md
      assurance/
        assurance-case-template.md
      tasks/
        work-breakdown.md
  formal/
    tla/
    alloy/
    coq/
    isabelle/
  implementation/
    runtime/
    nucleus/
    services/
      securityd/
      auditd/
      catalogd/
      datasetd/
      jobd/
      spoold/
      operatord/
      workpolicyd/
      amfd/
      uvsd/
    pxm/
      core/
    guard/
    sidecars/
    interfaces/
    tools/
      mfctl/
      jobsubmit/
      auditdump/
      catalogck/
      policyc/
      manifestck/
    prototypes/
      deferred-semantic-contracts/   # planning only; no Phase 1 hosted daemon
  tests/
    unit/
    integration/
    negative/
    fuzz/
    conformance/
    crash-recovery/
    fault-injection/
    supply-chain/
  ci/
    no-fake-success/
    spec-id-lint/
    source-matrix-lint/
    audit-obligation-lint/
    unsafe-inventory/
```

## 19. Pack Split for AI Work

Each pack must contain:

```text
Purpose
Scope
Non-objectives
Source Matrix IDs
Requirements
Object model
State machine
Failure modes
Audit obligations
Positive tests
Negative tests
Fuzz targets
Spec gaps
AI prompt
```

Pack map:

```text
PACK-00  Normative Language + Profiles
PACK-01  Source Matrix + IBM Concept Mapping
PACK-02  Glossary
PACK-03  System Integrity Statement
PACK-04  Object Model
PACK-05  Authorization Model
PACK-06  Audit Schema
PACK-07  Dataset/Catalog
PACK-08  Job/Spool
PACK-09  Operator Console
PACK-10  AMF
PACK-11  Update Verification
PACK-12  Nucleus/SVC/PCALL
PACK-13  PXM
PACK-14  PXM Guard
PACK-15  Tests/Negative Tests
PACK-16  CI/No Fake Success
PACK-17  Prompts
PACK-18  Roadmap/Tasks
PACK-19  Assurance Case
```

## 20. First Vertical Slice

### 20.1 Success Path

```text
IPL
  -> operator console
  -> securityd
  -> auditd
  -> catalogd
  -> datasetd
  -> spoold
  -> jobd

operator:
  DEFINE USER ALICE
  DEFINE DATASET USER.ALICE.INPUT OWNER(ALICE) TYPE(SEQ)
  WRITE DATASET USER.ALICE.INPUT "HELLO MFOS"

  SUBMIT INLINE:
    //HELLO JOB USER=ALICE,CLASS=A
    //STEP1 EXEC PGM=ECHO
    //IN    DD DSN=USER.ALICE.INPUT,DISP=SHR
    //OUT   DD SYSOUT=*

expected:
  securityd allows READ
  datasetd opens handle
  jobd runs ECHO
  spoold captures SYSOUT
  auditd records submit/open/execute/spool/complete
  operator sees COMPLETE RC=0
```

### 20.2 Failure Path

```text
DEFINE USER BOB

SUBMIT INLINE:
  //BAD JOB USER=BOB,CLASS=A
  //STEP1 EXEC PGM=ECHO
  //IN    DD DSN=USER.ALICE.INPUT,DISP=SHR
  //OUT   DD SYSOUT=*

expected:
  securityd denies READ
  datasetd does not create handle
  auditd records OPEN_DENY before jobd receives final result
  jobd marks step failed
  spoold captures failure summary
  operator sees FAILED REASON=POLICY_DENIED
```

## 21. Implementation Roadmap

### Phase 0: Source and Spec Freeze

Exit criteria:

```text
Source Matrix v0.1 complete
Glossary v0.1 complete
System Integrity Statement v0.1 approved
Object Model v0.1 approved
Authorization Model v0.1 approved
Audit Schema v0.1 approved
no-fake-success policy in CI
```

### Phase 1: Dafny Executable-Semantics Scaffold And Loader-Only Validation

Creates Dafny executable-semantics scaffold artifacts and loader-only artifact
validation. It does not run hosted services, a semantic runner, or production
code.

All Phase 1 artifacts MUST be marked:

```text
implementation_profile: dafny_loader_only_artifact_validation
production_claim: false
hardware_enforcement_claim: false
system_integrity_claim: false
semantic_runner_claim: false
hosted_daemon_claim: false
```

Exit criteria:

```text
Dafny scaffold metadata validates
test catalogs, fixtures, golden vectors, and traceability load deterministically
HELLO job success remains a specified semantic contract, not a running service
BOB denied ALICE dataset remains a specified semantic contract
deny-before-return audit obligation is represented in oracle artifacts
no semantic runner, hosted daemon, or production code exists
```

### Phase 2: Minimal MFOS Nucleus

Exit criteria:

```text
boot to operator console
address space isolation
SVC ABI
typed handles
copy-in/copy-out
service launch
hosted services ported
NX/W^X enforced
user job cannot obtain a protected dataset handle without securityd
```

### Phase 3: Baseline Enterprise Semantics

Exit criteria:

```text
dataset/catalog/job/spool/operator/security/audit full vertical slice
AMF specification complete
AMF load path exists but production load remains disabled
signed AMF test modules allowed only in non-production AMF test profile
update verification basic signed artifacts
audit hash chain
workload policy basic job class
crash recovery
```

### Phase 4: Enterprise-Standalone Hardening

Exit criteria:

```text
Secure Boot integration
measured boot integration
TPM sealing for selected secrets
remote audit export
TUF-like update metadata
signed provenance
SBOM
Enterprise-AMF governance for production AMF claims
rollback/freeze/mix-and-match tests
```

### Phase 5: Enterprise-PXM Core Prototype

Exit criteria:

```text
MFOS runs under PXM
implicit backend and PXM backend share partition-aware API
IOMMU domain tested
interrupt remapping tested
Linux side partition lab
device teardown negative tests
```

### Phase 6: High-Assurance Guard

Exit criteria:

```text
Guard seals security root
Guard seals audit root
Guard enforces executable mapping policy
Guard verifies SVC table
AMF registry Guard approval
attestation evidence
Guard failure policy tested
```

## 22. Work Breakdown Structure

### 22.1 Documentation Tasks

```text
DOC-001  Register EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
DOC-002  Register EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001
DOC-003  Register EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001/002
DOC-004  Register EXTREF-IBM-ZOS-SECURITY-SERVER-0001/002
DOC-005  Register EXTREF-IBM-ZOS-JES-INTRODUCTION-0001/002/JES2-001
DOC-006  Register EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001/002
DOC-007  Register EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001/002
DOC-008  Register EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001
DOC-009  Register EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001/002
DOC-010  Register EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001/002
DOC-011  Register EXTREF-IBM-Z-LPAR-INTRODUCTION-0001/DPM-001
DOC-012  Register EXTREF-IBM-Z-ARCHITECTURE-PRINCIPLES-0001
DOC-013  Register X64-INTEL-001
DOC-014  Register X64-AMD-001
DOC-015  Register MS-VBS/MS-VSM
DOC-016  Register TUF/SLSA/NIST/TCG/seL4
DOC-017  Create Source Matrix lint rule
```

### 22.2 Specification Tasks

```text
SPEC-001  Normative Language v0.1
SPEC-002  Conformance Profiles v0.1
SPEC-003  Glossary v0.1
SPEC-004  IBM Concept Mapping v0.1
SPEC-005  System Integrity v0.1
SPEC-006  Threat Model v0.1
SPEC-007  Object Model v0.1
SPEC-008  Authorization Model v0.1
SPEC-009  Audit Schema v0.1
SPEC-010  Dataset/Catalog v0.1
SPEC-011  Job/Spool v0.1
SPEC-012  Operator Command v0.1
SPEC-013  AMF v0.1
SPEC-014  Update v0.1
SPEC-015  SVC/PCALL ABI v0.1
SPEC-016  PXM Lifecycle v0.1
SPEC-017  PXM Device Teardown v0.1
SPEC-018  Guard Root Object v0.1
SPEC-019  Linux Gateway v0.1
SPEC-020  Assurance Case v0.1
```

### 22.3 Formal Tasks

```text
FORMAL-001  authorization decision model
FORMAL-002  dataset open invariant
FORMAL-003  audit append invariant
FORMAL-004  catalog transaction model
FORMAL-005  job lifecycle model
FORMAL-006  spool access model
FORMAL-007  operator command model
FORMAL-008  AMF load model
FORMAL-009  update rollback/freeze model
FORMAL-010  PXM partition lifecycle model
FORMAL-011  device teardown model
FORMAL-012  Guard root transition model
```

### 22.4 Deferred Semantic Contract Tasks

```text
SEMCON-001  securityd contract fixture planning
SEMCON-002  auditd contract fixture planning
SEMCON-003  catalogd contract fixture planning
SEMCON-004  datasetd contract fixture planning
SEMCON-005  jobd contract fixture planning
SEMCON-006  spoold contract fixture planning
SEMCON-007  operatord contract fixture planning
SEMCON-008  workload-policy contract fixture planning
SEMCON-009  AMF disabled-mode contract fixture planning
SEMCON-010  UVS contract fixture planning
SEMCON-011  HELLO job success contract
SEMCON-012  unauthorized dataset access deny contract
SEMCON-013  audit chain tamper contract
SEMCON-014  catalog crash recovery contract
```

### 22.5 CI Tasks

```text
CI-001  spec ID required check
CI-002  source matrix ref required check
CI-003  no fake success scanner
CI-004  TODO/unimplemented scanner for production paths
CI-005  audit obligation checker
CI-006  negative test required checker
CI-007  unsafe inventory generator
CI-008  dependency allowlist checker
CI-009  SBOM generator
CI-010  signed provenance generator
CI-011  reproducible build diff report
CI-012  fuzz target registration checker
```

## 23. Threat Model Baseline

Actors:

```text
unauthenticated user
authenticated user
operator
security administrator
auditor
service developer
AMF module signer
compromised user job
compromised trusted service
compromised AMF module
compromised side partition
malicious update repository
malicious device / DMA actor
physical attacker outside assumed protection
firmware attacker outside Baseline, partially addressed by Enterprise resilience
```

Assets:

```text
security policy root
audit chain root
catalog root
dataset contents and metadata
spool entries
job identity
operator command authority
AMF registry
update root metadata
partition memory
device assignment state
Guard roots
```

Trust boundaries:

```text
user job -> SVC
user job -> PCALL service endpoint
trusted service -> securityd
trusted service -> auditd
operator console -> operatord
datasetd -> catalogd
jobd -> datasetd/spoold
MFOS partition -> PXM
MFOS partition -> Guard
MFOS partition -> side partition gateway
update repository -> uvsd
device DMA -> IOMMU domain
```

Mandatory abuse cases:

```text
unauthorized dataset open success
stale handle reuse after policy change
audit write failure ignored
operator command executed without authority
job submit identity spoofing
spool browse by non-owner
catalog crash leaves phantom committed entry
AMF load from mutable dataset
revoked update accepted
rollback metadata accepted
mix-and-match metadata accepted
PXM device reassigned before teardown
Guard root mismatch ignored
unsupported command returns success
PKU treated as instruction-fetch protection
```

## 24. Production Readiness Gate

MFOS may not claim production readiness until all gates pass:

```text
PROD-001  Source Matrix complete for all z/OS-inspired concepts
PROD-002  System Integrity negative tests pass
PROD-003  Unauthorized dataset access cannot produce handle
PROD-004  DENY audit record emitted before caller result
PROD-005  Catalog crash recovery passes
PROD-006  Spool browse/purge security enforced
PROD-007  Operator commands require authority and audit
PROD-008  AMF invalid signature/revoked signer fail closed
PROD-009  Update rollback/freeze/mix-and-match tests pass
PROD-010  SBOM and signed provenance produced
PROD-011  No fake success CI clean
PROD-012  Parser fuzz campaigns complete
PROD-013  PXM device teardown tested before passthrough production
PROD-014  Guard evidence exists before HA claim
PROD-015  Recovery drill completed
```

## 25. AI Implementation Contract

AI rules:

```text
AI-MFOS-001:
  Do not write code without spec IDs.

AI-MFOS-002:
  Do not use z/OS-derived concepts without Source Matrix IDs.

AI-MFOS-003:
  Do not write "z/OS compatible".

AI-MFOS-004:
  When IBM terminology is mapped to MFOS terminology, state overlap and divergence.

AI-MFOS-005:
  No fake success, empty stub, or silent fallback.

AI-MFOS-006:
  Unimplemented specified features return UNSUPPORTED and fail closed.

AI-MFOS-007:
  Undefined features return SPEC_GAP and must not be implemented.

AI-MFOS-008:
  Security-sensitive paths require negative tests in the same change.

AI-MFOS-009:
  Do not omit audit obligations.

AI-MFOS-010:
  Do not bypass securityd for authorization decisions.

AI-MFOS-011:
  unsafe code requires a safety contract.

AI-MFOS-012:
  Parsers require fuzz targets.

AI-MFOS-013:
  PXM must not interpret MFOS enterprise semantics.

AI-MFOS-014:
  Guard must not interpret job, dataset, or spool semantics.

AI-MFOS-015:
  PKU/PKS must not be the primary system-integrity boundary.
```

Required AI output format:

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

## 26. AI Prompt Library

### 26.1 IBM Concept Mapping Prompt

```text
You are the MFOS IBM Concept Mapping reviewer.
Review the following MFOS concept against IBM-published z/OS / IBM Z source
documents.

Output:
- MFOS concept
- IBM source concept
- IBM source document title
- IBM source URL or publication number
- Source Matrix ID
- exact semantic overlap
- MFOS divergence
- risk of misleading compatibility claim
- allowed wording
- prohibited wording
- requirements IDs to update
- negative tests required

Target:
<MFOS_CONCEPT>
```

### 26.2 Source-Grounded Requirement Prompt

```text
You are the MFOS requirements author.
Create MFOS requirements from the following official source review notes.

Constraints:
- Do not claim z/OS compatibility.
- Use z/OS-inspired only.
- Assign requirement IDs.
- Include source_document and source_section.
- State MFOS divergence.
- Include positive and negative tests.
- Include audit obligations.
- Separate Baseline, Enterprise-Standalone, Enterprise-PXM, and High-Assurance applicability.
- Mark implementation ambiguity as SPEC_GAP.

Input:
<SOURCE_REVIEW_NOTES>
```

### 26.3 Architecture Skeptical Review Prompt

```text
You are a strict MFOS architecture reviewer.
Do not defend the design. Find assumptions that will break later.

Focus:
- IBM-published source concept mismatch
- dangerous compatibility wording
- overconfidence in x64 hardware features
- PKU/PKS overclaiming
- PXM/Guard/MFOS responsibility confusion
- TCB growth
- audit bypass
- fake success
- missing negative tests
- profile mixing
- missing source IDs

Output:
- Critical issues
- Major issues
- Minor issues
- Required corrections
- Required requirements
- Required negative tests
- Required source documents
```

### 26.4 Negative Test Generation Prompt

```text
You are the MFOS negative test engineer.
Generate denial, failure, race, corruption, and recovery tests.

Required categories:
- unauthorized access
- stale handle
- policy version mismatch
- audit write failure
- malformed input
- replay attempt
- downgrade attempt
- concurrent update
- crash mid-transaction
- recovery consistency
- privilege confusion
- cross-partition misuse
- AMF revoked signer
- Guard root mismatch
- unsupported command success attempt

Spec:
<SPEC>
```

## 27. Deferred and Rejected Scope

Deferred:

```text
z/Architecture binary compatibility
z/OS API compatibility
full JES2/JES3 compatibility
full RACF compatibility
full DFSMS compatibility
full POSIX compatibility
Linux syscall compatibility
desktop compositor
GPU driver stack inside MFOS
broad third-party kernel driver ecosystem
full PM implementation before MFOS semantics
PXM Guard before Enterprise semantics
PKS-dependent design
JIT support
sysplex-like multi-node design
live migration
nested virtualization
```

May be removed entirely:

```text
MFOS embedded desktop
MFOS embedded Linux app runner
overbroad AMF authority
root shell first model
POSIX-first filesystem model
PKU/PKS storage-key-compatible wording
separate PM/no-PM OS codebases
Guard interpreting business semantics
```

## 28. Risk Register

| Risk | Severity | Mitigation |
| --- | ---: | --- |
| z/OS compatibility confusion | Critical | Pin "inspired, not compatible" wording across docs and release checks. |
| IBM concept mismatch | Critical | Mandatory source matrix and overlap/divergence fields. |
| TCB growth | Critical | Cap nucleus, PXM, and Guard responsibilities. |
| Guard complexity | Critical | Root objects only. |
| PKU/PKS overclaim | High | Exclude from canonical policy boundary. |
| AMF abuse | Critical | Signed, measured, revocable, explicit authority, Guard in HA. |
| Audit bypass | Critical | Audit obligation model and fail-closed paths. |
| Dataset/POSIX confusion | High | Dataset object model fixed. |
| Linux/Desktop integrity pollution | High | Side partition and audited gateway. |
| DMA leakage | Critical | IOMMU, interrupt remap, teardown checklist. |
| Update compromise | Critical | TUF-like metadata, signing, epoch, recovery. |
| Supply-chain attack | Critical | SLSA provenance, SBOM, reproducible builds. |
| AI hallucination | Critical | Spec IDs, source IDs, no-fake-success CI. |
| Overformalization | Medium | Stage formal methods by criticality. |
| Performance regression | Medium | No Guard/PXM call on ordinary syscall fast path. |
| Operator UX pressure | High | Operator grammar, authority, and audit mandatory. |
| Firmware compromise | High | NIST 800-193 style protection/detection/recovery. |

## 29. Immediate Next Document

The first deep split specification to stabilize is:

```text
docs/design/specs/03-system-integrity.md
```

Required chapter structure:

```text
1. Purpose
2. Non-Compatibility Statement
3. Source Matrix References
4. Authorized vs Unauthorized
5. Execution States
6. Storage Domains
7. Protected Resources
8. System Interfaces
9. Prohibited Circumventions
10. SVC Rules
11. PCALL Rules
12. AMF Rules
13. Securityd Authority
14. Auditd Authority
15. Dataset/Catalog/Spool Rules
16. Operator Command Rules
17. Partition-Aware Requirements
18. High-Assurance Guard Extensions
19. Failure Modes
20. Formal Invariants
21. Positive Tests
22. Negative Tests
23. Spec Gaps
```

Implementation rule:

```text
Do not start nucleus, securityd, datasetd, jobd, PXM, or Guard production
implementation until the relevant later gate exists. Phase 1 does not authorize
hosted semantic prototype work, semantic runner work, hosted daemons, or service
implementation.
```

## 30. Final Architecture Recommendation

MFOS should be built as:

```text
MFOS Core:
  z/OS-inspired enterprise semantics OS

Core objects:
  job
  dataset
  catalog
  spool
  operator command
  principal
  security profile
  audit record
  service class
  authorized module

Core services:
  securityd
  auditd
  catalogd
  datasetd
  jobd
  spoold
  operatord
  workpolicyd
  amfd
  uvsd

Core integrity:
  source-grounded system integrity
  central authorization
  mandatory audit
  no fake success
  AMF-disabled by default in baseline implementation
  typed SVC/PCALL
  NX required
  W^X required
  SMEP/SMAP SHOULD in Baseline when supported
  SMEP/SMAP required for Enterprise-PXM and High-Assurance platform profiles

Partition layer:
  PXM Core
  implicit single partition for early phases
  full partitioning for Enterprise-PXM and High-Assurance

High-assurance layer:
  PXM Guard
  selected root object protection only

Optional:
  POSIX subsystem
  Linux side partition
  desktop side partition
  gateway with audit
```

The winning architecture is not "everything in one OS." It is a source-grounded enterprise semantics OS with strict evidence discipline and a deliberately small high-assurance root protection profile.
