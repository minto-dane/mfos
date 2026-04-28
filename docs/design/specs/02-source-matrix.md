---
spec_id: "MFOS-SPEC-02-SOURCE-MATRIX"
title: "MFOS Source Matrix and IBM Concept Mapping Specification v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001", "EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001", "EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001", "EXTREF-IBM-Z-DPM-0001", "EXTREF-IBM-ZOS-JES-INTRODUCTION-0001", "EXTREF-IBM-ZOS-JES-JOB-FLOW-0001", "EXTREF-IBM-ZOS-JES2-LIBRARY-0001", "EXTREF-IBM-Z-LPAR-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001", "EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001", "EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001", "EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001", "EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001", "EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001", "EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001", "EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001", "EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001", "EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001", "MS-VBS-001", "MS-VSM-001", "NIST-160-001", "NIST-193-001", "NIST-218-001", "SEL4-001", "SLSA-001", "TCG-001", "TUF-001", "X64-AMD-001", "X64-INTEL-001", "X64-LINUX-CET-001", "X64-LINUX-PKU-001"]
requirement_refs: ["MFOS-REQ-SOURCE-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Source Matrix and IBM Concept Mapping Specification v0.1

Status: design draft

This split spec defines how MFOS source IDs and IBM concept mappings are used by
requirements, designs, tests, reviews, and AI implementation work.

MFOS is z/OS-inspired. MFOS does not claim z/OS compatibility.

## Purpose

The purpose of this specification is to make source-grounded design mandatory
before implementation:

- Define the workflow for adding and using Source Matrix IDs.
- Define how IBM concepts may be mapped into MFOS terminology.
- Require semantic overlap, divergence, allowed wording, prohibited wording,
  verification obligations, and negative tests.
- Prevent AI-generated architecture drift, invented z/OS-like vocabulary,
  compatibility claims, hardware-feature overclaims, and fake success.
- Provide a reusable AI prompt for creating new mapping packs.

The canonical source-ID ledger is:

```text
docs/design/source-matrix/source-matrix.md
```

## Scope

This spec applies to:

- All z/OS-inspired MFOS concepts.
- All IBM-derived terms used in MFOS documents.
- All specs that reference system integrity, authorized state, storage domains,
  AMF, securityd, auditd, catalogd, datasetd, jobd, spoold, operatord, workpolicyd,
  z/OS UNIX-inspired optional subsystems, PXM, or PXM Guard.
- All requirements, tests, AI prompts, and implementation tasks that depend on
  source-grounded concepts.

This spec also applies when a non-IBM source is used to constrain an IBM-derived
mapping. Example: PKU/PKS may be discussed only as x64 helpers and must not be
described as storage-key compatibility.

## Non-objectives

This spec does not:

- Implement any MFOS service.
- Define complete service schemas; those belong in component specs.
- Claim z/OS, JES, RACF, DFSMS, SMF, workload policy, APF, PR/SM, or VBS compatibility.
- Permit IBM terminology to be reused without divergence analysis.
- Permit hardware features to replace the MFOS authorization or audit model.
- Permit PXM to interpret MFOS job, dataset, catalog, spool, security, or workload policy
  semantics.
- Permit Guard to interpret business policy or ordinary dataset/job/spool
  semantics.

## Normative Inputs

The following source groups are normative for this spec:

| Group | Source IDs | Required use |
| --- | --- | --- |
| IBM system integrity and authorization | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001 | Define unauthorized vs authorized behavior and negative boundary tests. |
| IBM storage protection terminology | EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001, EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001 | Define the source concept; require x64 divergence before mapping. |
| IBM security manager | EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001 | Define securityd profile and decision concepts. |
| IBM jobs and spool | EXTREF-IBM-ZOS-JES-INTRODUCTION-0001, EXTREF-IBM-ZOS-JES-JOB-FLOW-0001, EXTREF-IBM-ZOS-JES2-LIBRARY-0001 | Define jobd/spoold lifecycle and protected spool concepts. |
| IBM dataset and catalog | EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001, EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001 | Define catalogd/datasetd naming, resolution, attributes, and location concepts. |
| IBM audit and accounting | EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001 | Define auditd as evidence and security event recording. |
| IBM workload management | EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001 | Define service-class and goal vocabulary for workpolicyd. |
| IBM UNIX subsystem | EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001, EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001 | Constrain POSIX to optional subsystem status. |
| IBM cross-memory concepts | EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001, EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001 | Constrain PCALL and prohibit unsafe cross-address-space pointer trust. |
| IBM partition concepts | EXTREF-IBM-Z-LPAR-INTRODUCTION-0001, EXTREF-IBM-Z-DPM-0001 | Define PXM lifecycle and management-plane analogy. |
| x64 hardware reality | X64-INTEL-001, X64-AMD-001, X64-LINUX-PKU-001, X64-LINUX-CET-001 | Constrain implementation claims on x64. |
| Guard inspiration | MS-VBS-001, MS-VSM-001 | Constrain High-Assurance-only Guard claims. |
| Assurance and supply chain | TCG-001, NIST-160-001, NIST-218-001, NIST-193-001, SLSA-001, TUF-001, SEL4-001, FBVBS-001 | Define measured boot, update, provenance, assurance, and evidence discipline. |

## Mapping Record Format

Every IBM concept mapping must use this record shape:

```yaml
mapping_id: MFOS-MAP-AREA-NNNN
mfos_concept: string
source_concepts:
  - source_id: string
    source_term: string
    source_title: string
semantic_overlap:
  - string
mfos_divergence:
  - string
allowed_wording:
  - string
prohibited_wording:
  - string
requirements:
  - string
verification_obligations:
  - string
negative_tests:
  - string
audit_obligations:
  - string
spec_gaps:
  - string
profile_applicability:
  baseline: required | recommended | optional | prohibited | not_applicable
  enterprise: required | recommended | optional | prohibited | not_applicable
  high_assurance: required | recommended | optional | prohibited | not_applicable
```

## Mapping Rules

MFOS-MAP-RULE-0001:
  A z/OS-inspired concept must not enter a spec without at least one Source
  Matrix ID.

MFOS-MAP-RULE-0002:
  If an IBM term becomes an MFOS term, the spec must state exact overlap and
  divergence.

MFOS-MAP-RULE-0003:
  If a concept is inspired by IBM documentation but intentionally differs, the
  allowed wording must use "inspired", "mapped", "derived concept", or
  "source-grounded analogy", not "compatible".

MFOS-MAP-RULE-0004:
  Source IDs must be present in requirements, tests, review prompts, and code
  comments for security-sensitive implementation paths.

MFOS-MAP-RULE-0005:
  If no source ID exists for a proposed z/OS-like behavior, the behavior is a
  `SPEC_GAP` and must not be implemented as if specified.

MFOS-MAP-RULE-0006:
  If a behavior is specified but not implemented, it must fail closed with
  `UNSUPPORTED`.

MFOS-MAP-RULE-0007:
  No mapping may make PKU, PKS, CET, SMEP, SMAP, NX, IOMMU, VT-x, AMD-V, EPT,
  or NPT the semantic source of MFOS authorization. These features are
  enforcement aids only.

MFOS-MAP-RULE-0008:
  PXM mappings must stop at partition lifecycle and isolation. PXM must not map
  job, dataset, catalog, spool, security profile, or workload policy semantics.

MFOS-MAP-RULE-0009:
  Guard mappings must stop at selected High-Assurance root objects. Guard must
  not map ordinary dataset policy, job scheduling, spool formatting, or
  operator UI behavior.

MFOS-MAP-RULE-0010:
  Every mapping that affects a protected resource must include audit
  obligations and at least one negative test.

## Source ID Tables

The canonical source tables live in `docs/design/source-matrix/source-matrix.md`.
This spec depends on the following IDs:

| Area | Required source IDs |
| --- | --- |
| System integrity | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001 |
| Storage domains | EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001, EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001, X64-LINUX-PKU-001, X64-INTEL-001, X64-AMD-001 |
| securityd | EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001 |
| auditd | EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001, FBVBS-001 |
| catalogd/datasetd | EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001, EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 |
| jobd/spoold | EXTREF-IBM-ZOS-JES-INTRODUCTION-0001, EXTREF-IBM-ZOS-JES-JOB-FLOW-0001, EXTREF-IBM-ZOS-JES2-LIBRARY-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 |
| operatord | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-JES2-LIBRARY-0001 |
| workpolicyd | EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 |
| Optional POSIX | EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001, EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001, EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001 |
| SVC/PCALL | EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001, EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, X64-INTEL-001, X64-AMD-001 |
| PXM | EXTREF-IBM-Z-LPAR-INTRODUCTION-0001, EXTREF-IBM-Z-DPM-0001, FBVBS-001, X64-INTEL-001, X64-AMD-001 |
| PXM Guard | MS-VBS-001, MS-VSM-001, FBVBS-001, X64-INTEL-001, X64-AMD-001 |
| Update verification | TUF-001, EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001, NIST-218-001, SLSA-001, FBVBS-001 |
| Measured boot and firmware resilience | TCG-001, NIST-193-001, NIST-160-001 |

## IBM Concept Mapping Records

### MFOS-MAP-SI-0001: System Integrity

MFOS concept:
  MFOS System Integrity Statement.

Source concepts:
  EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001 system integrity, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001 authorized boundary scanning,
  EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001 authorized programs.

Semantic overlap:
  Unauthorized subjects must not use system interfaces to bypass protection,
  security checks, audit requirements, or authorized state boundaries.

MFOS divergence:
  MFOS expresses subjects as principals, programs, jobs, subsystems, and
  services. MFOS Baseline does not claim protection after authorized module or
  nucleus compromise. That stronger claim belongs only to High-Assurance Guard
  and selected root objects.

Allowed wording:
  "MFOS has a source-grounded system integrity statement inspired by IBM z/OS
  system integrity concepts."

Prohibited wording:
  "MFOS provides z/OS system integrity compatibility."

Verification obligations:
  The system interface list must be explicit. SVC, PCALL, operator command,
  dataset open, catalog update, job submit, AMF load, and update activation
  must have authorization and audit obligations.

Negative tests:
  Unauthorized SVC succeeds; PCALL trusts caller-supplied identity; operator
  command executes without decision; unsupported interface returns success.

Spec gaps:
  Exact initial list of system interfaces belongs in the system-integrity spec.

### MFOS-MAP-STG-0001: Storage Protection to ExecutionState and StorageDomain

MFOS concept:
  ExecutionState and StorageDomain.

Source concepts:
  EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001 and EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001 storage protection, storage key, PSW key, and
  fetch-protection concepts.

Semantic overlap:
  Both designs separate execution authority from access to protected storage
  domains and require enforcement at defined boundaries.

MFOS divergence:
  MFOS does not implement z/Architecture storage keys. x64 PKU and PKS are
  optional helpers with important limits; PKU is data-access oriented and not an
  instruction-fetch or system-integrity root. MFOS maps the concept into named
  software domains and x64 page-table protections.

Allowed wording:
  "MFOS maps storage-key concepts into software-defined storage domains on x64."

Prohibited wording:
  "MFOS implements z/OS storage keys" or "PKU/PKS are storage-key compatible."

Verification obligations:
  Specs must list the domains, access rules, enforcement mechanisms, and
  failure modes. Hardware claims must cite Intel or AMD documentation plus PKU
  or CET references where applicable.

Negative tests:
  User job writes service-private domain; trusted service maps writable and
  executable pages at once; PKU bypass is treated as impossible.

Spec gaps:
  Initial domain-to-page-table policy and CPU feature fallback matrix.

### MFOS-MAP-AMF-0001: APF to AMF

MFOS concept:
  Authorized Module Facility.

Source concepts:
  EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001 authorized programs and EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001 authorized code scanning.

Semantic overlap:
  Both identify code that has special OS extension authority beyond ordinary
  user execution.

MFOS divergence:
  AMF is not administrator privilege. AMF modules must be signed, measured,
  revocable, bound to explicit authority classes, loaded through an explicit
  ABI, audited, and fail-closed on invalid or revoked artifacts. High-Assurance
  AMF loads require Guard approval.

Allowed wording:
  "AMF is APF-inspired OS extension authorization."

Prohibited wording:
  "AMF is APF-compatible" or "AMF grants root/admin rights."

Verification obligations:
  AMF load must verify signature, manifest, revocation, catalog immutability,
  securityd authorization, optional Guard approval, RX mapping, registration,
  and audit.

Negative tests:
  Invalid signature loads; revoked signer loads; AMF module disables audit;
  AMF ABI accepts arbitrary untrusted pointer.

Spec gaps:
  Initial authority classes and AMF manifest schema.

### MFOS-MAP-SEC-0001: RACF to securityd

MFOS concept:
  securityd.

Source concepts:
  EXTREF-IBM-ZOS-SECURITY-SERVER-0001 RACF documentation family and EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001 protected resource
  authorization.

Semantic overlap:
  Both centralize decisions around principals, groups, protected resources,
  profiles, access authorities, and resource-specific authorization.

MFOS divergence:
  securityd returns typed decisions with obligations. Results include ALLOW,
  DENY, ALLOW_WITH_AUDIT, REQUIRE_MFA, REQUIRE_DUAL_CONTROL,
  REQUIRE_BREAK_GLASS, REQUIRE_GUARD_APPROVAL, REQUIRE_OPERATOR_CONFIRMATION,
  UNSUPPORTED, and SPEC_GAP.

Allowed wording:
  "securityd is RACF-inspired."

Prohibited wording:
  "securityd is RACF-compatible."

Verification obligations:
  A protected resource handle must not exist unless securityd produced an
  applicable ALLOW or ALLOW_WITH_AUDIT for the same subject, object, operation,
  context, and policy version.

Negative tests:
  Dataset handle issued without securityd decision; stale handle survives policy
  version change; service makes local final authorization decision.

Spec gaps:
  Complete profile language and policy transaction schema.

### MFOS-MAP-AUD-0001: SMF to auditd

MFOS concept:
  auditd.

Source concepts:
  EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 SMF introduction and EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001 RACF type 80 processing record.

Semantic overlap:
  Both collect evidence for system, job, dataset, resource, and security
  activity, including denied security events.

MFOS divergence:
  auditd is not a general log daemon. MFOS requires schema validation, hash
  chaining, fail-closed behavior when audit is mandatory, remote export for
  higher profiles, and Guard-sealed audit roots in High-Assurance.

Allowed wording:
  "auditd is SMF-inspired evidence collection."

Prohibited wording:
  "auditd is SMF-compatible" or "spool output is audit evidence."

Verification obligations:
  DENY decisions must be recorded before the caller receives the result. Audit
  records must include schema version, record ID, timestamp, subject, object,
  operation, decision, reason code, policy version, previous hash, payload hash,
  and record hash.

Negative tests:
  DENY returned before audit; audit hash-chain tamper goes undetected; required
  audit failure still allows protected operation.

Spec gaps:
  Initial binary encoding, redaction policy, and remote export protocol.

### MFOS-MAP-CATDATA-0001: DFSMS to catalogd/datasetd

MFOS concept:
  catalogd and datasetd.

Source concepts:
  EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001 DFSMS catalogs and EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001 DFSMS documentation family.

Semantic overlap:
  Both treat datasets as managed resources with names, attributes, catalog
  entries, locations, and storage-management behavior.

MFOS divergence:
  A MFOS dataset is not a POSIX file wrapper. Catalog entries include owner,
  attributes, location, security profile, generation, immutable/system flags,
  and integrity tags. Dataset handles bind subject, operation, policy version,
  catalog generation, and expiry.

Allowed wording:
  "catalogd/datasetd are DFSMS-inspired managed dataset services."

Prohibited wording:
  "MFOS datasets are POSIX files" or "catalogd is DFSMS-compatible."

Verification obligations:
  datasetd cannot open persistent datasets unless catalogd resolves a committed
  catalog entry and securityd authorizes the operation.

Negative tests:
  Open uncommitted catalog entry; open without security decision; stale handle
  after policy change; delete despite retention policy.

Spec gaps:
  DSN grammar, initial dataset types, allocation model, and crash recovery log.

### MFOS-MAP-JOBSPL-0001: JES to jobd/spoold

MFOS concept:
  jobd and spoold.

Source concepts:
  EXTREF-IBM-ZOS-JES-INTRODUCTION-0001 JES, EXTREF-IBM-ZOS-JES-JOB-FLOW-0001 job flow, and EXTREF-IBM-ZOS-JES2-LIBRARY-0001 JES2 documentation.

Semantic overlap:
  Both model job submission, conversion, queues, initiators, SYSIN, SYSOUT,
  output processing, and spool retention as first-class enterprise OS behavior.

MFOS divergence:
  MFOS implements a small JCL-like subset and job lifecycle. It does not claim
  JCL, JES, or JES2 compatibility.

Allowed wording:
  "jobd/spoold are JES-inspired."

Prohibited wording:
  "jobd is JES-compatible" or "MFOS supports JES2 commands."

Verification obligations:
  Job effective principal must be established before any dataset, program, or
  spool resource is opened. Spool browse, purge, and export require securityd
  authorization.

Negative tests:
  Job opens dataset before principal; unauthorized spool browse succeeds; JCL
  parser accepts malformed dangerous input; SYSOUT is visible to wrong user.

Spec gaps:
  JCL-like grammar, initial initiator rules, output classes, and purge policy.

### MFOS-MAP-OPER-0001: Operator Console

MFOS concept:
  operatord and operator command grammar.

Source concepts:
  EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001 system integrity, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001 resource authorization, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001
  audit, and EXTREF-IBM-ZOS-JES2-LIBRARY-0001 command-oriented operational reference.

Semantic overlap:
  Operator commands are privileged system interfaces that affect jobs,
  datasets, security state, and operational state.

MFOS divergence:
  The operator console is not a root shell. Commands have grammar, authority
  class, authorization decisions, audit records, confirmation, and optional
  dual-control workflows.

Allowed wording:
  "operatord is an audited operator command interface."

Prohibited wording:
  "operator console is a root shell."

Verification obligations:
  No command executes without command ID, subject, authorization decision, and
  audit record.

Negative tests:
  Destructive command executes without confirmation; automation hook bypasses
  authority; unknown command returns success.

Spec gaps:
  Initial command grammar and authority classes.

### MFOS-MAP-WORKLOAD-POLICY-0001: workload policy to workpolicyd

MFOS concept:
  workpolicyd.

Source concepts:
  EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001 service classes and performance goals.

Semantic overlap:
  Both group work using classes, goals, resource expectations, and business
  importance.

MFOS divergence:
  MFOS workpolicyd starts with job class, priority, max concurrency, and resource caps.
  Response-time and velocity-like goals are later phases.

Allowed wording:
  "workpolicyd is external-workload-management-informed."

Prohibited wording:
  "workpolicyd is z/OS external-workload-management-compatible."

Verification obligations:
  workpolicyd must not make security decisions. workpolicyd dispatch hints cannot override
  securityd denial or audit obligations.

Negative tests:
  High-priority job bypasses dataset authorization; workload policy causes unaudited
  execution.

Spec gaps:
  Phase-1 job class schema and future service-class policy activation model.

### MFOS-MAP-UNIX-0001: z/OS UNIX to Optional POSIX

MFOS concept:
  Optional POSIX subsystem.

Source concepts:
  EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001 z/OS UNIX introduction and EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001 z/OS UNIX System
  Services documentation family.

Semantic overlap:
  Both allow a UNIX-like operating environment inside a larger enterprise OS.

MFOS divergence:
  POSIX is not the primary MFOS interface. It is optional, profile-limited, and
  cannot bypass securityd, auditd, dataset/catalog semantics, or operator
  authority.

Allowed wording:
  "MFOS may include a restricted optional POSIX subsystem."

Prohibited wording:
  "MFOS is UNIX-first" or "POSIX root bypasses MFOS policy."

Verification obligations:
  POSIX subsystem calls touching protected resources must resolve through MFOS
  object, authorization, and audit paths.

Negative tests:
  POSIX path opens dataset without catalog/securityd; root shell changes policy
  without audit.

Spec gaps:
  Path-to-dataset mapping, if any, is intentionally unspecified.

### MFOS-MAP-XMEM-0001: Cross-Memory to PCALL

MFOS concept:
  PCALL.

Source concepts:
  EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001 synchronous cross-memory communication and EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001
  cross-memory controls.

Semantic overlap:
  Both provide controlled synchronous entry to service routines that may operate
  across address-space boundaries.

MFOS divergence:
  MFOS PCALL uses typed endpoints, typed requests, bounded payloads, caller
  identity from the scheduler/service context, and sealed buffers. Early MFOS
  must not implement arbitrary cross-address-space pointer access.

Allowed wording:
  "PCALL is inspired by controlled cross-memory service entry concepts."

Prohibited wording:
  "PCALL implements z/OS PC instruction compatibility."

Verification obligations:
  PCALL must validate endpoint, payload type, size, caller identity, audit
  obligation, and failure mode.

Negative tests:
  PCALL trusts caller-supplied identity; PCALL dereferences untrusted pointer;
  unsupported endpoint returns success.

Spec gaps:
  Endpoint registry, sealed-buffer format, and service identity binding.

### MFOS-MAP-PXM-0001: LPAR/DPM to PXM

MFOS concept:
  PXM Partition Manager.

Source concepts:
  EXTREF-IBM-Z-LPAR-INTRODUCTION-0001 logical partitions, EXTREF-IBM-Z-DPM-0001 Dynamic Partition Manager, and
  FBVBS-001 partition state-machine discipline.

Semantic overlap:
  Both define logical machine images with lifecycle, activation profiles,
  assigned processors, storage, I/O, and management-plane operations.

MFOS divergence:
  PXM is x64-native and must not understand MFOS enterprise semantics. PM-less
  boot is represented as an implicit single partition backend, not a separate
  OS design.

Allowed wording:
  "PXM is LPAR-inspired in partition lifecycle and management-plane concepts."

Prohibited wording:
  "PXM implements PR/SM" or "PXM schedules MFOS jobs."

Verification obligations:
  PXM operations must audit partition lifecycle events. Device assignment must
  require IOMMU domain setup and interrupt remapping where the profile requires
  them. Memory cannot be reassigned until mappings are revoked and memory is
  zeroed.

Negative tests:
  Device assigned without teardown; memory reused without zeroing; partition
  state transition skips measurement or activation; PXM interprets dataset
  policy.

Spec gaps:
  Initial activation profile schema and x64 backend split.

### MFOS-MAP-GRD-0001: VBS/VSM to PXM Guard

MFOS concept:
  PXM Guard.

Source concepts:
  MS-VBS-001 VBS/Memory Integrity, MS-VSM-001 Virtual Secure Mode, and
  FBVBS-001 root-object assurance discipline.

Semantic overlap:
  Both use a higher-privilege protection layer to protect selected security
  roots from lower-privilege OS components.

MFOS divergence:
  Guard is mandatory only in High-Assurance. Guard protects selected root
  objects: security policy root, audit chain root, AMF registry, SVC table,
  nucleus text, executable mapping policy, page-table policy, activation
  profile, emergency state, and update policy. Guard does not understand
  ordinary dataset, job, spool, operator UI, or business policy semantics.

Allowed wording:
  "PXM Guard is VBS/VSM-inspired for selected High-Assurance root objects."

Prohibited wording:
  "MFOS implements Windows VBS" or "Guard is required for Baseline."

Verification obligations:
  Root transitions must be recorded by Guard and auditd. Guard mismatch must
  fail secure. Guard API must stay small and root-object focused.

Negative tests:
  Guard accepts mismatched SVC table; Guard authorizes executable writable page;
  Guard grants AMF load with mismatched registry root; Guard interprets dataset
  access policy.

Spec gaps:
  Guard call ABI binary format and attestation claim set.

### MFOS-MAP-UVS-0001: TUF/SMP/E Reference to uvsd

MFOS concept:
  Update Verification Service.

Source concepts:
  TUF-001 roles and metadata, EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001 security advisory metadata
  reference, NIST-218-001 secure development, SLSA-001 provenance, and
  FBVBS-001 manifest discipline.

Semantic overlap:
  Update correctness depends on signed metadata, freshness, version or epoch
  checks, consistent views, and provenance.

MFOS divergence:
  MFOS update verification is not tied to SMP/E transport. uvsd verifies
  metadata, artifact hashes and sizes, dependency and conflict declarations,
  security epoch, rollback prevention, freeze detection, mix-and-match
  detection, revocation, staged activation, and audit.

Allowed wording:
  "uvsd uses a TUF-like metadata model and takes update advisory discipline as
  an informative enterprise reference."

Prohibited wording:
  "MFOS implements SMP/E" or "signature alone is sufficient update security."

Verification obligations:
  Update must fail closed on rollback, freeze, mix-and-match, invalid signature,
  bad hash, bad size, revoked key, dependency failure, or security epoch
  downgrade.

Negative tests:
  Old timestamp accepted; target metadata mixed across snapshots; artifact hash
  mismatch accepted; security epoch downgrade accepted.

Spec gaps:
  Initial metadata role schema, key rotation policy, and recovery rollback
  workflow.

## Allowed Wording

The following forms are allowed:

- "z/OS-inspired"
- "IBM-documented concept mapping"
- "RACF-inspired securityd"
- "JES-inspired jobd/spoold"
- "DFSMS-inspired catalogd/datasetd"
- "SMF-inspired auditd"
- "external-workload-management-informed workpolicyd"
- "APF-inspired AMF"
- "LPAR-inspired PXM"
- "VBS/VSM-inspired Guard for High-Assurance root objects"
- "x64-native implementation with source-grounded divergence"

## Prohibited Wording

The following forms are prohibited:

- "z/OS-compatible"
- "JES-compatible"
- "RACF-compatible"
- "DFSMS-compatible"
- "SMF-compatible"
- "external-workload-management-compatible"
- "APF-compatible"
- "PR/SM-compatible"
- "VBS-compatible"
- "storage-key compatible via PKU/PKS"
- "dataset is a POSIX file"
- "operator console is a root shell"
- "AMF is admin privilege"
- "auditd is just logging"
- "Guard protects everything"

## Verification Obligations

MFOS-REQ-SOURCE-0001:
  A z/OS-inspired concept in any spec must include Source Matrix IDs.
  Verification: documentation inspection and source-matrix lint.

MFOS-REQ-SOURCE-0002:
  IBM-derived terms must include overlap and divergence.
  Verification: architecture review.

MFOS-REQ-SOURCE-0003:
  Compatibility claims are prohibited.
  Verification: release text scan and review.

MFOS-REQ-SOURCE-0004:
  Source-derived protected-resource operations must include authorization,
  audit, failure modes, and negative tests.
  Verification: spec review and test traceability.

MFOS-REQ-SOURCE-0005:
  Hardware features must be described as enforcement aids, not semantic
  authorization sources.
  Verification: architecture review.

MFOS-REQ-SOURCE-0006:
  PXM and Guard mappings must include scope caps.
  Verification: PXM/Guard review.

MFOS-REQ-SOURCE-0007:
  AI-generated code or tests must list implemented requirement IDs and source
  IDs.
  Verification: CI lint and review checklist.

MFOS-REQ-SOURCE-0008:
  `UNSUPPORTED` and `SPEC_GAP` must be distinct.
  Verification: no-fake-success lint and negative tests.

## Negative Tests Required by This Spec

Source-grounding negative tests:

- Spec introduces z/OS-like concept without Source Matrix ID.
- Spec uses IBM term without overlap and divergence.
- Spec includes "z/OS-compatible" or component compatibility wording.
- Spec claims PKU/PKS storage-key compatibility.
- Spec lets PXM decide dataset, job, catalog, spool, security, or workload policy.
- Spec lets Guard interpret ordinary dataset/job/spool semantics.
- Spec describes audit as ordinary logging.
- Spec describes operator console as root shell.
- Spec describes AMF as administrator privilege.
- AI output returns success for an unsupported or unspecified behavior.

System-boundary negative tests:

- Unauthorized dataset access creates handle.
- Unauthorized spool browse succeeds.
- Operator command executes without authority and audit.
- AMF load succeeds without signature, measurement, revocation check, or audit.
- DENY result returns before audit record is durable according to profile.
- PCALL trusts caller-supplied identity.
- Update accepts rollback, freeze, or mix-and-match metadata.
- PXM reassigns memory before mapping revocation and zeroing.
- Guard accepts mismatched root object.

## Spec Gaps

The following gaps are intentionally left open for later specs:

- Exact version pins and section anchors for each online IBM documentation
  source.
- Complete machine-readable source matrix schema.
- Lint implementation for source IDs, prohibited wording, and compatibility
  claims.
- Mapping from all source IDs to final MFOS requirement IDs.
- Per-component split specs for system integrity, object model, authorization,
  audit, dataset/catalog, job/spool, operator console, AMF, update, SVC/PCALL,
  PXM, Guard, and conformance.
- Formal model references for source-mapping invariants.
- Policy for deprecating or replacing source IDs when upstream documentation
  changes.

## AI Prompt

Use this prompt to create or review a new MFOS source-mapping pack:

```text
You are the MFOS IBM Concept Mapping reviewer.

Input:
<MFOS_CONCEPT_OR_SPEC>

Rules:
- MFOS is z/OS-inspired, not z/OS-compatible.
- Do not claim compatibility with JES, RACF, DFSMS, SMF, workload policy, APF, PR/SM, or
  Windows VBS/VSM.
- Use only Source Matrix IDs from docs/design/source-matrix/source-matrix.md.
- If no Source Matrix ID applies, mark the behavior SPEC_GAP.
- For every IBM-derived term, write semantic overlap and MFOS divergence.
- For every protected-resource operation, require securityd authorization and
  auditd obligations unless a later approved spec explicitly says otherwise.
- For every unsupported specified feature, require UNSUPPORTED fail-closed.
- Prohibit fake success, empty stubs, and silent fallback.
- Treat x64 hardware features as enforcement aids, not semantic authorization.
- Keep PXM limited to partition lifecycle and isolation.
- Keep Guard limited to selected High-Assurance root objects.

Output:
1. Mapping ID
2. MFOS concept
3. Source Matrix IDs
4. IBM source concepts
5. Semantic overlap
6. MFOS divergence
7. Allowed wording
8. Prohibited wording
9. Requirements to add or update
10. Verification obligations
11. Audit obligations
12. Negative tests
13. Spec gaps
14. Profile applicability
```
