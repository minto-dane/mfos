---
spec_id: MFOS-SPEC-INDEX
title: MFOS Split Specification Index v0.1
canonical_language: en-US
japanese_mirror: missing
status: draft
owner: MFOS architecture
last_reviewed: '2026-04-28'
source_refs:
- FBVBS-001
- EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001
- EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001
- EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001
- EXTREF-IBM-Z-DPM-0001
- EXTREF-IBM-ZOS-JES-INTRODUCTION-0001
- EXTREF-IBM-ZOS-JES-JOB-FLOW-0001
- EXTREF-IBM-ZOS-JES2-LIBRARY-0001
- EXTREF-IBM-Z-LPAR-INTRODUCTION-0001
- EXTREF-IBM-ZOS-SECURITY-SERVER-0001
- EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001
- EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
- EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001
- EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001
- EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001
- EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001
- EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001
- EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001
- EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001
- EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001
- EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001
- EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001
- EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001
- EXTREF-IBM-Z-ARCHITECTURE-PRINCIPLES-0001
- MS-VBS-001
- MS-VSM-001
- NIST-160-001
- NIST-193-001
- NIST-218-001
- SEL4-001
- SLSA-001
- TCG-001
- TUF-001
- X64-AMD-001
- X64-INTEL-001
- X64-LINUX-CET-001
- X64-LINUX-PKU-001
- EXTREF-MICROSOFT-HYPERV-OVERVIEW-0001
- EXTREF-MICROSOFT-HYPERV-TLFS-0001
- EXTREF-MICROSOFT-HYPERV-VSM-0001
- EXTREF-LINUX-KVM-API-0001
- EXTREF-LINUX-KVM-CAPABILITIES-0001
- EXTREF-LINUX-KVM-VFIO-0001
- EXTREF-INTEL-TDX-OVERVIEW-0001
- EXTREF-INTEL-TDX-LINUX-DOC-0001
- EXTREF-INTEL-TDX-ATTESTATION-0001
- EXTREF-INTEL-CET-0001
- EXTREF-AMD-SEV-OVERVIEW-0001
- EXTREF-AMD-SEV-ES-0001
- EXTREF-AMD-SEV-SNP-0001
- EXTREF-AMD-SEV-TIO-0001
- EXTREF-LINUX-AMD-SEV-KVM-DOC-0001
- EXTREF-KANI-RUST-VERIFIER-0001
- EXTREF-VERUS-RUST-VERIFICATION-0001
- EXTREF-DAFNY-REFERENCE-0001
- EXTREF-AWS-AUTOMATED-REASONING-0001
- EXTREF-GITHUB-CODEQL-0001
- EXTREF-NIST-SECURE-SYSTEMS-ENGINEERING-0001
- EXTREF-NIST-SSDF-0001
- EXTREF-X86-64-MICROARCH-LEVELS-0001
- EXTREF-GLIBC-HWCAPS-X86-64-V4-0001
- EXTREF-GCC-X86-64-V4-0001
- EXTREF-RUST-TARGET-TIER-POLICY-0001
- EXTREF-SEL4-MULTIARCH-SUPPORTED-PLATFORMS-0001
- EXTREF-SEL4-ARCH-CONFIGURATION-0001
- EXTREF-INTEL-SGX-OVERVIEW-0001
- EXTREF-INTEL-SGX-ATTESTATION-0001
- EXTREF-INTEL-SGX-DCAP-0001
- EXTREF-CLANG-CFI-0001
- EXTREF-CLANG-KCFI-0001
- EXTREF-GCC-CF-PROTECTION-0001
- EXTREF-RUST-CF-PROTECTION-0001
requirement_refs: []
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: implementation_must_not_infer_or_fill_gaps
---
# MFOS Split Specification Index v0.1

Status: Draft index
Owner: MFOS architecture
Scope: `docs/design/specs/*.md`

This index lists the current MFOS split specifications and routes implementation agents to the correct source material. It covers the numbered specs from `00` through `45`, including executable-spec artifacts, deferred planning scaffolds, the Dafny executable-semantics scaffold policy, and architecture portability / x86-64 target-profile policy. Phase provenance and implementation gates are kept in the routing addenda below rather than in the high-level index summary.

MFOS is source-grounded and z/OS-inspired. This index does not claim z/OS compatibility, IBM product compatibility, z/Architecture compatibility, RACF compatibility, JES compatibility, DFSMS compatibility, SMF compatibility, Windows VBS compatibility, or Linux compatibility.

## How To Use This Index

Before implementation work:

1. Read `00-normative-language.md`, `01-glossary.md`, and `02-source-matrix.md`.
2. Read the component spec for the subsystem being changed.
3. Read `21-ai-implementation-contract.md` and follow the mandatory AI output format.
4. For release-affecting work, read `22-production-readiness.md`.
5. Do not implement behavior marked as a spec gap.
6. Do not return success for unsupported behavior.
7. Do not bypass `securityd` or `auditd` obligations.

Status values:

- `Draft`: split spec exists but is not frozen.
- `Future candidate`: enough design detail exists for later work after the
  current non-production Dafny and source-grounding gates close. This is not an
  implementation authorization.
- `Blocked for production`: production claims require additional evidence, CI, or formalization.

The downstream-target column is a routing aid only. It does not authorize
hosted prototype or implementation, semantic evaluator, Portable Semantic Core, daemon, nucleus,
PXM, Guard, or production work.

Phase 1 non-production Dafny executable-semantics and conformance-harness work
is allowed under Spec `43`. Product semantic evaluators, future semantic-runner
commands, hosted daemons, Rust semantic-core work, and production work remain
blocked.

## Split Specification Map

| Spec | Purpose | Owning subsystem | Upstream source IDs | Future implementation targets, not authorization | Prerequisite specs | Completion status and gaps |
| --- | --- | --- | --- | --- | --- | --- |
| [00-normative-language.md](00-normative-language.md) | Defines normative terms, profiles, claim rules, requirement namespaces, verification vocabulary, protected resource categories, and no-fake-success rules. | Architecture governance, conformance, release policy | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-JES-INTRODUCTION-0001, EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001, EXTREF-IBM-Z-LPAR-INTRODUCTION-0001, X64-INTEL-001, X64-AMD-001, MS-VBS-001, MS-VSM-001, TCG-001, NIST-160-001, NIST-218-001, NIST-193-001, SEL4-001, SLSA-001, TUF-001, FBVBS-001 | spec lint, profile claim lint, no-fake-success CI, release review, all specs | None | Draft. Gaps: machine-readable requirement schema, no-fake-success scanner, production evidence bundle, mixed-profile deployment policy. Also needs later registration of `OBJ`, `SVC`, `PCALL`, `GLOSS`, `PROD`, and any other split-introduced namespaces if the global namespace table is frozen. |
| [01-glossary.md](01-glossary.md) | Defines controlled MFOS vocabulary, canonical names, prohibited terms, protected resources, system interfaces, and IBM-term divergence rules. | Architecture terminology, documentation lint | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001, EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001, EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-JES-INTRODUCTION-0001, EXTREF-IBM-ZOS-JES-JOB-FLOW-0001, EXTREF-IBM-ZOS-JES2-LIBRARY-0001, EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001, EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001, EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001, EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001, EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001, EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001, EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001, EXTREF-IBM-Z-LPAR-INTRODUCTION-0001, EXTREF-IBM-Z-DPM-0001, EXTREF-IBM-Z-ARCHITECTURE-PRINCIPLES-0001, EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001, X64-INTEL-001, X64-AMD-001, X64-LINUX-PKU-001, X64-LINUX-CET-001, MS-VBS-001, MS-VSM-001, TCG-001, TUF-001, SLSA-001, FBVBS-001 | glossary lint, compatibility wording lint, source ID lint, docs review | 00 | Draft. Gaps: machine-readable glossary schema, DSN term set, operator command vocabulary, audit field dictionary, multilingual policy. |
| [02-source-matrix.md](02-source-matrix.md) | Defines Source Matrix and IBM concept mapping workflow, allowed/prohibited wording, source classification, and source-grounded review duties. | Source matrix governance, docs lint, architecture review | IBM source family IDs, x64 IDs, MS-VBS/MS-VSM, TCG, NIST, SLSA, TUF, SEL4, FBVBS | `docs/design/source-matrix/source-matrix.md`, source-matrix lint, concept mapping reviews, AI prompts | 00, 01 | Draft. Gaps: exact version pins and section anchors, complete machine-readable source matrix schema, formal source-mapping invariants. |
| [03-system-integrity.md](03-system-integrity.md) | Defines MFOS system integrity, authorized/unauthorized subjects, ExecutionState, AuthorityClass, StorageDomain, protected resources, system interfaces, SVC/PCALL/AMF/securityd/auditd rules, PXM and Guard integrity boundaries. | Cross-cutting integrity model, nucleus, securityd, auditd, AMF, PXM, Guard | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001, EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001, EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-JES-INTRODUCTION-0001, EXTREF-IBM-ZOS-JES-JOB-FLOW-0001, EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001, EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001, EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001, EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001, EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001, EXTREF-IBM-Z-LPAR-INTRODUCTION-0001, EXTREF-IBM-Z-DPM-0001, X64-INTEL-001, X64-AMD-001, X64-LINUX-PKU-001, X64-LINUX-CET-001, MS-VBS-001, MS-VSM-001, TCG-001, NIST-160-001, FBVBS-001 | nucleus SVC enforcement, PCALL, typed handles, securityd, auditd, datasetd, catalogd, spoold, operatord, amfd, uvsd, PXM, Guard, negative tests | 00, 01, 02 | Draft. Specification-only semantic baseline; not ready for implementation or Phase 1 semantic execution. Gaps: exact SVC ABI, PCALL wire format, operator grammar, DSN grammar, AMF manifest schema, audit binary format, Guard ABI, PXM teardown schema, formal model toolchain, audit failure policy. |
| [04-threat-model.md](04-threat-model.md) | Defines MFOS assets, actors, trust boundaries, abuse cases, mitigations, audit obligations, fail-closed conditions, residual risks, tests, and fuzz targets. | Security architecture, test engineering, formal methods | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001, EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001, EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-JES-INTRODUCTION-0001, EXTREF-IBM-ZOS-JES-JOB-FLOW-0001, EXTREF-IBM-ZOS-JES2-LIBRARY-0001, EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001, EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001, EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001, EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001, EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001, EXTREF-IBM-Z-LPAR-INTRODUCTION-0001, EXTREF-IBM-Z-DPM-0001, X64-INTEL-001, X64-AMD-001, X64-LINUX-PKU-001, X64-LINUX-CET-001, MS-VBS-001, MS-VSM-001, TCG-001, NIST-160-001, NIST-193-001, NIST-218-001, TUF-001, SLSA-001, SEL4-001, FBVBS-001 | abuse-case tests, boundary negative tests, fault injection, formal threat properties | 00, 01, 02, 03 | Draft. Gaps: exact IBM product behavior excluded, Windows VBS/VSM behavior excluded, crypto algorithms, full formal proof, remote management protocol, production readiness threat review. |
| [05-object-model.md](05-object-model.md) | Defines first-class MFOS objects, IDs, schemas, lifecycle states, handle binding, references, protected object invariants, and serialization expectations. | Shared object model for all services | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-JES-INTRODUCTION-0001, EXTREF-IBM-ZOS-JES-JOB-FLOW-0001, EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001, EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001, EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001, EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001, EXTREF-IBM-Z-LPAR-INTRODUCTION-0001, EXTREF-IBM-Z-DPM-0001, TUF-001, FBVBS-001 | common schema crate/module, securityd request types, audit records, catalog/dataset/job/spool/operator/AMF/update/PXM/Guard object types | 00, 01, 02, 03, 04 | Draft. Specification-only schema baseline; not ready for implementation. Gaps: concrete serialization, DSN grammar, policy expression grammar, crypto algorithms, operator grammar, volume extent format, PXM device schema, Guard attestation claims, POSIX mapping. |
| [06-authorization.md](06-authorization.md) | Defines `securityd` as central policy decision point, decision input/result model, obligations, policy transactions, break-glass, cache invalidation, and fail-closed authorization rules. | `securityd`, policy compiler, authorization client libraries | EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001, EXTREF-IBM-Z-LPAR-INTRODUCTION-0001, MS-VSM-001, FBVBS-001 | securityd future contract planning, policy parser, decision API, negative tests, audit obligation integration | 00, 01, 02, 03, 04, 05, 07 | Draft. Phase 0.8 specification-only freeze; not ready for implementation or Phase 1 semantic execution. Gaps: concrete policy language, bootstrap policy, external identity provider, MFA/dual-control token formats, decision cache protocol, audit redaction language, Guard approval token schema, distributed policy management, POSIX mapping. |
| [07-audit.md](07-audit.md) | Defines `auditd`, audit record schema, append-only ingestion, sequencing, hash chain, retention, query/export authorization, audit failure policy, and Guard-sealed audit roots. | `auditd`, audit client libraries, audit storage/export tooling | EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, TCG-001, MS-VSM-001, FBVBS-001 | auditd future contract planning, audit schema, hash-chain store, remote export, query API, tamper tests | 00, 01, 02, 03, 04, 05, 06 | Draft. Phase 0.8 specification-only freeze; not ready for implementation or Phase 1 semantic execution. Gaps include concrete binary/on-disk encoding, retention storage policy, remote export transport, redaction language, failure-mode profile finalization, Guard audit root ABI, SIEM integration, recovery/tamper response details. |
| [08-dataset-catalog.md](08-dataset-catalog.md) | Defines datasets and catalogs as first-class managed resources with DSN grammar, catalog transactions, dataset allocation/open/close, handle binding, retention, integrity, recovery, security, and audit. | `catalogd`, `datasetd` | EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001, EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001 | catalogd/datasetd future contract planning, DSN parser, catalog journal, dataset handle validation, crash recovery tests | 00, 01, 02, 03, 04, 05, 06, 07 | Draft. Phase 0.8 specification-only freeze; not ready for implementation or Phase 1 semantic execution. Gaps: exact DSN grammar beyond initial uppercase qualifier subset, full record-format behavior for `FB`, `VB`, and blocked formats, volume layout, encryption/key service integration, backup/migration behavior, POSIX mapping excluded. |
| [09-job-spool.md](09-job-spool.md) | Defines MFOS job processing, JCL-like subset, job lifecycle, DD-like resource resolution, SYSIN/SYSOUT, spool browse/purge/export, retention, accounting, and audit. | `jobd`, `spoold` | EXTREF-IBM-ZOS-JES-INTRODUCTION-0001, EXTREF-IBM-ZOS-JES-JOB-FLOW-0001, EXTREF-IBM-ZOS-JES2-LIBRARY-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001, EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001 | jobd/spoold future contract planning, JCL-like parser, queue/initiator model, SYSOUT capture, spool authorization tests | 00, 01, 02, 03, 04, 05, 06, 07, 08, 11 | Draft. Phase 0.8 specification-only freeze; not ready for HELLO-job semantic contract implementation or Phase 1 implementation. Gaps: complete JCL-like grammar and diagnostics, procedure/library handling excluded, full initiator policy, workload policy interaction contract, detailed restart semantics, output formatting/export formats. |
| [10-operator-console.md](10-operator-console.md) | Defines operator console as first interactive interface, command grammar, authority classes, command lifecycle, confirmation, dual control, emergency mode, automation hooks, and audit. | `operatord`, operator TUI/CLI, automation hooks | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001, EXTREF-IBM-ZOS-JES-INTRODUCTION-0001, EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001, EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001 | operatord parser, command dispatcher, console boot path, operator drills, command negative tests | 00, 01, 02, 03, 04, 05, 06, 07, 08, 09, 11 | Draft. Phase 0.8 specification-only freeze; not ready for operator-console semantic contract implementation or Phase 1 implementation. Gaps: complete command grammar and quoting, panel/TUI behavior, full authority taxonomy, automation API, recovery-mode subset, command result formatting. |
| [11-workload-policy.md](11-workload-policy.md) | Defines `workpolicyd` workload classification, job classes, service classes, report classes, priority, max concurrency, resource caps, dispatch hints, overload policy, activation, audit, and accounting. | `workpolicyd`, jobd scheduling integration, operator workload policy commands | EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001, EXTREF-IBM-ZOS-JES-INTRODUCTION-0001, EXTREF-IBM-ZOS-JES-JOB-FLOW-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001 | workpolicyd future contract planning, job class policy, dispatch hints, workload policy operator display, workload policy audit events | 00, 01, 02, 03, 04, 05, 06, 07, 09, 10 | Draft. Candidate future work after loader-only and source-grounding gates close. Gaps: exact service-class goal algorithms, velocity/response-time algorithms, scheduler feedback contract, overload tuning, policy activation UI. |
| [12-amf.md](12-amf.md) | Defines AMF authorized module governance: signed artifacts, manifests, authority classes, load lifecycle, revocation, registry, executable mapping, audit, and Guard approval. | `amfd`, AMF manifest tooling, module loader, Guard integration | EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001, X64-INTEL-001, X64-AMD-001, MS-VBS-001, MS-VSM-001, TUF-001, SLSA-001, NIST-218-001, FBVBS-001 | AMF future contract planning, manifest parser, signature verifier, revocation checks, AMF registry, executable mapping tests | 00, 01, 02, 03, 04, 05, 06, 07, 13, 15, 17 | Draft. Blocked for production. Gaps: concrete signature algorithms and key formats, manifest binary/canonical encoding, ABI versioning details, registry persistence, revocation distribution, Guard approval token details. |
| [13-update.md](13-update.md) | Defines UVS update verification, metadata roles, artifact manifests, signatures/hashes/sizes, generation/security epoch, rollback/freeze/mix-and-match detection, staging, activation, recovery, audit, and Guard interaction. | `uvsd`, update tooling, recovery workflow, release artifacts | TUF-001, SLSA-001, NIST-218-001, NIST-193-001, TCG-001, EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001, EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, MS-VBS-001, MS-VSM-001, FBVBS-001 | UVS future contract planning, manifest verifier, artifact store, activation journal, rollback tests, release pipeline | 00, 01, 02, 03, 04, 05, 06, 07, 12, 16, 17, 22 | Draft. Blocked for production. Gaps: metadata wire format, signature algorithms/threshold/key rotation, policy bundle validation, distributed mirror selection, delta updates, service restart orchestration, recovery partition implementation, SBOM/provenance formats. |
| [14-nucleus.md](14-nucleus.md) | Defines MFOS nucleus responsibilities: boot handoff, address spaces, page tables, scheduler baseline, SVC dispatch, typed handles, copy-in/copy-out, IPC/PCALL primitives, service lifecycle, memory protection, fault containment, audit hooks, and partition-aware APIs. | nucleus, kernel core, service launcher | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001, EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001, EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001, X64-INTEL-001, X64-AMD-001, X64-LINUX-PKU-001, X64-LINUX-CET-001, TCG-001, FBVBS-001 | boot path, memory manager, handle table, SVC dispatcher, IPC transport, service launcher, kernel audit hook | 00, 01, 02, 03, 04, 05, 07, 15, 16 | Draft. Blocked for production, enough for design prototype. Gaps: boot protocol wire format, scheduler policy, exact page-table layout, service image format, crash dump format, formal handle-rights model. |
| [15-svc-pcall.md](15-svc-pcall.md) | Defines SVC and PCALL ABIs, frame layout concepts, endpoint model, typed buffer/handle passing, identity propagation, authorization propagation, audit propagation, errors, endpoint manifests, and replay/fuzz rules. | nucleus ABI, trusted service IPC, securityd/auditd clients | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001, EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001, X64-INTEL-001, X64-AMD-001, FBVBS-001 | SVC dispatcher, PCALL transport, sealed buffers, endpoint manifest parser, ABI fuzz tests | 00, 01, 02, 03, 04, 05, 06, 07, 14 | Draft. Candidate future ABI work after loader-only and source-grounding gates close. Gaps: concrete binary frame layout/alignment, handle table encoding, endpoint manifest canonical format, sequence/replay formal model, timeout/cancellation policy. |
| [16-pxm.md](16-pxm.md) | Defines PXM Partition Manager: partition lifecycle, activation profiles, PXM call ABI, logical CPU/memory/device assignment, IOMMU/interrupt mapping, teardown, audit, implicit single partition backend, and recovery coordination. | PXM core, implicit partition backend, device assignment manager | EXTREF-IBM-Z-LPAR-INTRODUCTION-0001, EXTREF-IBM-Z-DPM-0001, X64-INTEL-001, X64-AMD-001, TCG-001, NIST-193-001, FBVBS-001 | PXM lifecycle engine, activation profile parser, implicit backend, VMX/SVM lab skeletons, IOMMU manager, device teardown tests | 00, 01, 02, 03, 04, 05, 06, 07, 14, 15 | Draft. Blocked for production passthrough. Gaps: VMX/SVM strategy, EPT/NPT ownership model, vendor IOMMU programming, interrupt remapping programming, recovery partition coordination, formal model path/syntax. |
| [17-guard.md](17-guard.md) | Defines PXM Guard for High-Assurance: selected root object sealing/verification, root transitions, executable mapping policy, AMF approval, SVC table verification, audit root append, emergency state, secret release, and attestation. | PXM Guard, HA root protection, attestation | MS-VBS-001, MS-VSM-001, EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001, EXTREF-IBM-Z-LPAR-INTRODUCTION-0001, X64-INTEL-001, X64-AMD-001, TCG-001, NIST-160-001, SEL4-001, FBVBS-001 | Guard call ABI, root registry, attestation, AMF registry seal, executable mapping checks, SVC table checks, Guard fault injection | 00, 01, 02, 03, 04, 05, 07, 12, 13, 16 | Draft. Blocked for High-Assurance production. Gaps: platform isolation mechanism, VMX/SVM/VTL-like strategy, Guard memory layout, crypto/key hierarchy, attestation evidence format, secret derivation, panic-equivalent behavior, boot audit sink, formal model path/syntax. |
| [18-linux-gateway.md](18-linux-gateway.md) | Defines Linux/Desktop Gateway for side partition integration through typed, authorized, audited exchanges while keeping desktop/browser/GPU/driver risk out of MFOS core. | gateway service, Linux/Desktop side partition integration, operator approval hooks | EXTREF-IBM-Z-LPAR-INTRODUCTION-0001, EXTREF-IBM-Z-DPM-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001, EXTREF-IBM-ZOS-JES-INTRODUCTION-0001, X64-INTEL-001, X64-AMD-001, FBVBS-001 | gateway channel, export/import workflow, spool browse/export workflow, job submit handoff, approval UI hooks, redaction/import policy | 00, 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 16 | Draft. Blocked for production gateway. Gaps: transport mechanism, shared-memory layout, Linux identity provider integration, malware/content scanning engine, redaction policy, clipboard policy grammar, dataset/external format mapping, GUI app behavior, remote desktop behavior, network gateway, backpressure, formal model path/syntax. |
| [19-assurance-case.md](19-assurance-case.md) | Defines how MFOS claims are argued, traced, reviewed, tested, evidenced, and limited by assumptions and gaps. | assurance case, evidence audit, release review | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, X64-INTEL-001, X64-AMD-001, MS-VBS-001, MS-VSM-001, TCG-001, NIST-160-001, NIST-218-001, NIST-193-001, SEL4-001, SLSA-001, TUF-001, FBVBS-001 | assurance graph, evidence taxonomy, claim registry, traceability audit, release evidence review | 00, 01, 02, 03, 04, 21, 22 | Draft. Blocked for production evidence. Gaps: evidence artifact storage path, claim ID registry, automated traceability graph format, formal proof acceptance criteria, independent reviewer policy, evidence retention period, external certification mapping out of scope. |
| [20-conformance.md](20-conformance.md) | Defines how an implementation claims Baseline, Enterprise-Standalone, Enterprise-PXM, or High-Assurance conformance, including requirement status, forbidden claims, profile matrices, conformance suites, and report shape. | conformance governance, conformance tests, release review | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, TCG-001, NIST-160-001, NIST-218-001, SLSA-001, TUF-001, MS-VSM-001, SEL4-001, FBVBS-001 | conformance report generator, profile claim checker, conformance test suites, release wording review | 00, 01, 02, 03, 04, 19, 21, 22 | Draft. Blocked for formal conformance claims. Gaps: conformance report file path, external certification mapping, proof acceptance criteria, hardware feature matrix rules, conformance statement versioning. |
| [21-ai-implementation-contract.md](21-ai-implementation-contract.md) | Defines mandatory AI implementation/review output format, prohibited patterns, CI/lint obligations, negative-test requirements, evidence artifacts, release claim rules, unsafe code contract, and parser/fuzz contract. | AI governance, CI/lint, review process | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, X64-INTEL-001, X64-AMD-001, X64-LINUX-PKU-001, MS-VBS-001, MS-VSM-001, NIST-160-001, NIST-218-001, SLSA-001, TUF-001, FBVBS-001 | AI output checker, requirement/source lint, no-fake-success scanner, unsafe inventory, fuzz target registration, release claim lint | 00, 01, 02, 03, 04, 22 | Draft. Ready for CI design. Gaps: machine-readable AI output schema, production-path scanner scope, requirement-ID comment syntax, ownership-scope CI, evidence manifest schema, fuzz sufficiency thresholds. |
| [22-production-readiness.md](22-production-readiness.md) | Defines production readiness gates, release claim rules, evidence artifact manifest, CI/lint obligations, required negative tests, release blockers, profile-specific gates, and production review prompt. | release governance, production readiness, supply chain, evidence review | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-JES-INTRODUCTION-0001, EXTREF-IBM-ZOS-JES-JOB-FLOW-0001, EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001, EXTREF-IBM-Z-LPAR-INTRODUCTION-0001, EXTREF-IBM-Z-DPM-0001, X64-INTEL-001, X64-AMD-001, X64-LINUX-PKU-001, MS-VBS-001, MS-VSM-001, TCG-001, NIST-160-001, NIST-218-001, NIST-193-001, SLSA-001, TUF-001, SEL4-001, FBVBS-001 | release candidate gate, SBOM/provenance pipeline, evidence manifest, production negative tests, recovery drills, Guard/PXM evidence checks | 00, 01, 02, 03, 04, 07, 13, 16, 17, 21 | Draft. Blocked for production until gates are implemented. Gaps: final evidence manifest schema, fuzz campaign threshold, waiver process, SBOM format, signed provenance format/signing infrastructure, attestation claim format, production-path scanner list, independent TCB review workflow, global registration of `MFOS-REQ-PROD-*`. |
| [23-requirements-catalog.md](23-requirements-catalog.md) | Consolidates requirement namespaces, default source IDs, profile applicability, verification methods, related tests, evidence artifacts, and known gaps for AI agents and evidence tooling. | requirements catalog, traceability, evidence tooling | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-JES-INTRODUCTION-0001, EXTREF-IBM-ZOS-JES-JOB-FLOW-0001, EXTREF-IBM-ZOS-JES2-LIBRARY-0001, EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001, EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001, EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001, EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001, EXTREF-IBM-Z-LPAR-INTRODUCTION-0001, EXTREF-IBM-Z-DPM-0001, EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001, EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001, EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001, X64-INTEL-001, X64-AMD-001, MS-VBS-001, MS-VSM-001, TCG-001, NIST-160-001, NIST-193-001, NIST-218-001, TUF-001, SLSA-001, FBVBS-001 | requirements registry, evidence file generator, traceability audit, source coverage report, profile matrix | 00, 01, 02, 03, 04, 05 through 22 | Draft. Ready for traceability tooling design. Gaps: one-row-per-requirement automation from Source Matrix, evidence directory/schema enforcement, uniform test ID traceability, formal model ID coverage, profile applicability confirmation. Note: current gap text still mentions threat-model split as missing; this index treats that as stale because `04-threat-model.md` exists. |
| [24-formal-methods.md](24-formal-methods.md) | Defines staged formal methods scope, candidate models, state variables, actions, invariants, liveness, negative properties, evidence artifacts, and trace mapping for high-risk semantics. | formal methods, model checking, proof planning, model trace validation | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001, EXTREF-IBM-ZOS-JES-INTRODUCTION-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001, EXTREF-IBM-Z-LPAR-INTRODUCTION-0001, TUF-001, MS-VSM-001, SEL4-001, NIST-160-001, FBVBS-001 | TLA+/Alloy-style models, formal evidence artifacts, model trace fixtures, model-to-test mapping, proof acceptance inputs | 00, 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 12, 13, 16, 17, 19, 20 | Draft. Ready for candidate model authoring. Gaps: final tool choice/syntax, trace schema/runner, exact MFA/dual-control schema, ABI safety contract, executable mapping transition, activation profile schema, scheduler fairness, PCIe/IOMMU invalidation ordering, interrupt remapping hardware model, Guard isolation/attestation/digest/emergency/audit payload details. |
| [25-operations-recovery.md](25-operations-recovery.md) | Defines operations, recovery, incident response, operator drills, recovery partition activity, audit export outage behavior, catalog/update/Guard recovery, break-glass, evidence preservation, and fail-closed procedures. | operations, recovery, incident response, operator/recovery runbooks | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-JES-INTRODUCTION-0001, EXTREF-IBM-ZOS-JES-JOB-FLOW-0001, EXTREF-IBM-ZOS-JES2-LIBRARY-0001, EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001, EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001, EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001, EXTREF-IBM-Z-LPAR-INTRODUCTION-0001, EXTREF-IBM-Z-DPM-0001, X64-INTEL-001, X64-AMD-001, MS-VBS-001, MS-VSM-001, TCG-001, NIST-160-001, NIST-193-001, NIST-218-001, TUF-001, SLSA-001, FBVBS-001 | operations runbooks, recovery plan parser, incident response drills, audit outage handling, catalog/update/Guard recovery workflows | 00, 01, 02, 03, 04, 06, 07, 08, 09, 10, 13, 16, 17, 19, 20, 22, 23 | Draft. Blocked for production operations. Gaps: recovery plan format/signature envelope, remote audit collector protocol/failover, OOB audit path, recovery partition image composition, MFA backend, evidence archive retention/destruction, legal/regulatory workflow, SIEM schema, hardware recovery matrix, side partition incident response, per-platform Guard recovery, RCA template. |
| [26-hardware-profile.md](26-hardware-profile.md) | Defines x64 hardware/profile matrix, required and optional CPU/platform features, Intel/AMD distinctions, PKU/PKS/CET limits, IOMMU/interrupt remapping gates, TPM/measured boot requirements, detection APIs, tests, and evidence. | hardware profile, platform qualification, PXM/Guard readiness | X64-INTEL-001, X64-AMD-001, X64-LINUX-PKU-001, X64-LINUX-CET-001, TCG-001, MS-VBS-001, MS-VSM-001, FBVBS-001 | hardware detector, platform report, PXM lab matrix, Guard platform gating, release hardware evidence | 00, 01, 02, 03, 04, 16, 17, 22 | Draft. Gaps: exact CPUID/MSR tables, report serialization, TPM event schemas, VMX/EPT and SVM/NPT backend requirements, IOMMU/device validation models, CET/PKS policy, ATS/PRI/PASID/SR-IOV policy. |
| [27-spec-front-matter.md](27-spec-front-matter.md) | Defines common front matter and section schema for split specs, including source IDs, requirement namespaces, owned files, profile applicability, audit/test/fuzz/evidence links, reviewers, and lint rules. | documentation governance, spec lint, source/requirement traceability | FBVBS-001, NIST-160-001, NIST-218-001 | spec lint, docs migration, source freshness metadata, review automation | 00, 01, 02, 21, 22, 23 | Draft. Gaps: existing specs not retrofitted, parser/linter not implemented, canonical registries pending, waiver format unresolved. |
| [28-machine-readable-registries.md](28-machine-readable-registries.md) | Defines registry schemas for requirements, tests, evidence, glossary terms, AI output, task IDs, and conformance claims. | machine-readable governance, CI/evidence tooling | FBVBS-001, SLSA-001, NIST-218-001, TUF-001 | `docs/design/registries/*.yaml`, validation tooling, evidence manifest, traceability graph | 00, 01, 02, 21, 22, 23, 27 | Draft. Gaps: JSON Schema/CUE files absent, legacy IDs not migrated, registry signing/waiver/formal trace/source freshness not finalized. |
| [29-test-strategy.md](29-test-strategy.md) | Defines unit, integration, negative, fuzz, conformance, crash-recovery, fault-injection, supply-chain, formal-model, and release-gate test strategy. | test architecture, CI, release gates | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, TUF-001, SLSA-001, FBVBS-001 | test taxonomy, CI test suites, evidence generation, release readiness tests | 00, 01, 02, 03, 04, 19, 20, 21, 22, 23, 24, 28 | Draft. Gaps: runner/report schema, fuzz thresholds, formal harness, PXM/Guard hardware lab matrix, remote audit and signing infrastructure, evidence checker. |
| [30-attestation-measured-boot.md](30-attestation-measured-boot.md) | Defines measured boot and attestation design, TPM event log expectations, component measurements, activation profile hash binding, Guard root claims, audit correlation, remote attestation, nonces/freshness, tests, and evidence. | measured boot, attestation, Guard/Enterprise evidence | TCG-001, X64-INTEL-001, X64-AMD-001, MS-VSM-001, NIST-193-001, FBVBS-001 | TPM event parser, attestation bundle, remote verifier, Guard root evidence, boot audit reconciliation | 00, 01, 02, 03, 04, 07, 16, 17, 22, 26 | Draft. Gaps: event formats/PCR policy, measurement_context canonicalization, verifier trust anchors, quote/signature format, nonce replay cache, boot audit sink and bundle serialization. |
| [31-release-distribution-rollback.md](31-release-distribution-rollback.md) | Defines release channels, TUF-like signed metadata relationship to UVS, release distribution manifest, activation profile updates, staged rollout, rollback authorization, recovery partition coordination, audit, tests, and evidence. | release distribution, rollback, UVS/recovery integration | TUF-001, SLSA-001, NIST-218-001, NIST-193-001, TCG-001, EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001, FBVBS-001 | release channel tooling, uvsd metadata verification, staged rollout controller, rollback workflow, recovery partition integration | 00, 01, 02, 04, 07, 13, 16, 17, 22, 25, 30 | Draft. Gaps: concrete metadata wire format, channel server/mirror/offline media protocols, signing key hierarchy, rollout health ABI, ring policy, attestation verifier, artifact garbage collection. |
| [32-language-localization.md](32-language-localization.md) | Defines English canonical language, Japanese auxiliary mirror rules, conflict handling, translation unit IDs, source hashes, language lint, semantic drift prevention, and synchronization workflow. | documentation governance, localization, release lint | FBVBS-001, NIST-160-001, NIST-218-001 | Japanese mirror generation, language-lint CI, source-hash manifest, release wording review | 00, 01, 02, 21, 22, 27 | Draft. Gaps: `translation-units.yaml`, `sync-status.yaml`, source-hash generator, language-lint CI, Japanese reviewer roster, complete Japanese mirrors. |
| [33-policy-lint.md](33-policy-lint.md) | Defines policy lint as a first-class security control for overly broad default access, wildcard dataset ALTER grants, broad AMF authority, emergency roles without expiry, spool export without audit, and policy update without dual control. | securityd policy tooling, operator/security admin review, CI policy gates | EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, FBVBS-001 | policy lint engine, policy activation gate, security-admin review workflow, policy negative tests | 00, 01, 02, 04, 05, 06, 07, 21, 22, 23 | Draft. Gaps: concrete policy grammar, sensitive dataset taxonomy, warning acceptance workflow, policy diff algorithm, central policy lint registry. |
| [31-executable-spec-test-harness.md](31-executable-spec-test-harness.md) | Defines Phase 0.9 executable-spec test harness artifact contracts without runner implementation. | executable-spec test architecture, schema validation | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | test catalog validation, fixture/oracle/golden-vector validation | 06, 07, 08, 09, 10, 29, 30-first-vertical-slice-contract | Draft. Phase 0.9 artifact contract only; runner implementation is prohibited. |
| [32-conformance-fixture-format.md](32-conformance-fixture-format.md) | Defines deterministic Phase 0.9 fixture format and fixture boundary rules. | fixture authors, validation tooling | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | `tests/fixtures/**`, `schemas/test-fixture.schema.yml` | 31-executable-spec-test-harness | Draft. Fixture loader implementation is prohibited. |
| [33-semantic-runner-contract.md](33-semantic-runner-contract.md) | Defines future semantic runner command contract and output obligations for a later reviewed gate. | future runner contract, conformance harness design | EXTREF-DAFNY-REFERENCE-0001, EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | future `mfos-semantic-runner` contract only | 31-executable-spec-test-harness, 32-conformance-fixture-format, 34-oracle-definition-format, 43-dafny-executable-semantics-policy | Draft. Runner command implementation is explicitly prohibited in Phase 0.9 and Phase 1. |
| [34-oracle-definition-format.md](34-oracle-definition-format.md) | Defines oracle and golden-vector formats for expected decisions, audit sequence, state transitions, failures, and final state. | oracle authors, golden-vector validation | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | `tests/golden/**`, `schemas/oracle.schema.yml` | 31-executable-spec-test-harness, 32-conformance-fixture-format | Draft. Oracle evaluator implementation is prohibited. |
| [35-fuzz-corpus-plan.md](35-fuzz-corpus-plan.md) | Defines Phase 0.9 fuzz corpus planning for MFOS-defined parsers and fixture formats. | fuzz planning, parser test design | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001, EXTREF-IBM-ZOS-JES-INTRODUCTION-0001, EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | `fuzz/targets/fuzz-target-plan.yml`, `fuzz/corpora/*/seed-plan.yml` | 29-test-strategy, 31-executable-spec-test-harness | Draft. Fuzzer implementation is prohibited. |
| [36-hypervisor-class-virtualization.md](36-hypervisor-class-virtualization.md) | Reserves MFOS-owned virtualization planning concepts without importing external hypervisor APIs or compatibility claims. | virtualization planning, partition-resource accounting, future device assignment policy | X64-INTEL-001, X64-AMD-001, MS-VBS-001, MS-VSM-001, NIST-160-001, FBVBS-001 | registered draft `MFOS-REQ-VIRT-*` planning requirements | 03, 04, 16, 26 | Draft scaffold. No virtualization implementation, VM control API, device model, snapshot, or migration work is authorized. |
| [37-confidential-vm.md](37-confidential-vm.md) | Reserves confidential workload planning boundaries for measurement, attestation, secret release, and private/shared memory policy. | confidential workload planning, attestation boundaries, Guard claim boundaries | X64-INTEL-001, X64-AMD-001, TCG-001, NIST-160-001, NIST-193-001, MS-VBS-001, MS-VSM-001, FBVBS-001 | registered draft `MFOS-REQ-CVM-*` planning requirements | 03, 04, 17, 26, 30, 36 | Draft scaffold. No confidential workload implementation, hardware-enforcement claim, or secret-release service is authorized. |
| [38-datacenter-cluster-operations.md](38-datacenter-cluster-operations.md) | Reserves datacenter and cluster operations concepts for node identity, membership, policy distribution, audit collection, updates, and runbooks. | operations planning, cluster governance, future management-plane policy | NIST-160-001, NIST-218-001, SLSA-001, TCG-001, EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001, FBVBS-001 | registered draft `MFOS-REQ-CLUSTER-*` and `MFOS-REQ-OPS-*` planning requirements | 07, 11, 13, 25, 30, 31 | Draft scaffold. No cluster scheduler, quorum service, or distributed control plane is authorized. |
| [39-language-and-verification-policy.md](39-language-and-verification-policy.md) | Reserves language, unsafe-boundary, control-flow, hardware-aid, and proof-tool policy areas. | language policy, verification policy, unsafe-boundary review | X64-INTEL-001, X64-AMD-001, X64-LINUX-CET-001, X64-LINUX-PKU-001, NIST-160-001, NIST-218-001, FBVBS-001 | registered draft `MFOS-REQ-LANG-*`, `MFOS-REQ-FORMAL-*`, and `MFOS-REQ-ASSURANCE-*` planning requirements | 03, 04, 21, 22, 24 | Draft scaffold. No language safety, CFI, hardware-aid, or proof-coverage claim is authorized. |
| [40-automated-reasoning-program.md](40-automated-reasoning-program.md) | Reserves automated-reasoning program structure, proof obligation fields, model registry expectations, and evidence boundaries. | formal assurance planning, model registry, proof obligation governance | NIST-160-001, NIST-218-001, SEL4-001, TUF-001, EXTREF-DAFNY-REFERENCE-0001, FBVBS-001 | draft formal claim, proof-obligation, model, tool, and evidence registries | 19, 20, 24, 39 | Draft scaffold. No verified implementation or release proof evidence is claimed. |
| [41-performance-and-secure-operations.md](41-performance-and-secure-operations.md) | Reserves performance budget, secure operations, benchmark, rollback drill, and release operations evidence policies. | secure operations planning, performance evidence, release operations | NIST-160-001, NIST-218-001, NIST-193-001, SLSA-001, TUF-001, TCG-001, X64-INTEL-001, X64-AMD-001, EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001, FBVBS-001 | registered draft `MFOS-REQ-PERF-*` and `MFOS-REQ-OPS-*` planning requirements | 11, 13, 22, 25, 26, 30, 31, 38 | Draft scaffold. No performance, scalability, availability, or production operations claim is authorized. |

| [42-mfvm.md](42-mfvm.md) | Defines MFVM as an MFOS-based VM management subsystem, less trusted than PXM, using PXM Control API and MFOS governance services. | MFVM control plane, PXM request planning, VM management governance | EXTREF-MICROSOFT-HYPERV-OVERVIEW-0001, EXTREF-MICROSOFT-HYPERV-TLFS-0001, EXTREF-LINUX-KVM-API-0001, EXTREF-LINUX-KVM-CAPABILITIES-0001, EXTREF-LINUX-KVM-VFIO-0001, EXTREF-INTEL-TDX-OVERVIEW-0001, EXTREF-AMD-SEV-SNP-0001, EXTREF-NIST-SECURE-SYSTEMS-ENGINEERING-0001, FBVBS-001 | registered draft `MFOS-REQ-MFVM-*`, `MFOS-REQ-VIRT-*`, `MFOS-REQ-CVM-*`, and `MFOS-REQ-CLUSTER-*` planning requirements | 16, 36, 37, 38, 41 | Draft. No MFVM implementation, PXM implementation, VM runtime, hosted daemon, semantic runner, or production work is authorized. |
| [43-dafny-executable-semantics-policy.md](43-dafny-executable-semantics-policy.md) | Defines Phase 1 Dafny executable-semantics policy, non-production model artifacts, and conformance-harness boundaries. | Dafny executable-semantics artifacts, fixture/oracle/golden comparison, verification status reporting | EXTREF-DAFNY-REFERENCE-0001, EXTREF-AWS-AUTOMATED-REASONING-0001, EXTREF-NIST-SECURE-SYSTEMS-ENGINEERING-0001, EXTREF-NIST-SSDF-0001, FBVBS-001 | registered draft `MFOS-REQ-DAFNY-*` and `MFOS-REQ-SEMSPEC-*` requirements | 31, 33, 39, 40 | Current Phase 1 policy. No semantic runner, Rust semantic-core, hosted daemon, production implementation, PXM/MFVM/CVM/cluster implementation, or production generated-code path is authorized. |
| [44-architecture-portability-policy.md](44-architecture-portability-policy.md) | Defines x86-64-first but not x86-64-only architecture policy, architecture-neutral semantics, architecture-specific enforcement, platform concerns, and future non-x86 claim gates. | architecture policy, CPU/backend boundaries, roadmap and AI guardrails | FBVBS-001, X64-INTEL-001, X64-AMD-001, EXTREF-RUST-TARGET-TIER-POLICY-0001, EXTREF-SEL4-MULTIARCH-SUPPORTED-PLATFORMS-0001, EXTREF-SEL4-ARCH-CONFIGURATION-0001, EXTREF-NIST-SECURE-SYSTEMS-ENGINEERING-0001 | registered draft `MFOS-REQ-ARCH-*` and `MFOS-REQ-CPUFEAT-*` requirements | 26, 28, 39, 43 | Current documentation policy. No AArch64/RISC-V implementation, architecture backend, CPU feature detector, hardware path, hosted daemon, or production work is authorized. |
| [45-x86-64-target-profiles.md](45-x86-64-target-profiles.md) | Defines x86-64 baseline, server-modern, v4 performance, max-feature, TDX CVM, SEV-SNP CVM, SGX TEE, and CET/CFI hardening evidence profiles. | CPU Feature Registry, CPU Target Profile Registry, validation policy, profile evidence | X64-INTEL-001, X64-AMD-001, X64-LINUX-CET-001, TCG-001, NIST-193-001, EXTREF-X86-64-MICROARCH-LEVELS-0001, EXTREF-GLIBC-HWCAPS-X86-64-V4-0001, EXTREF-GCC-X86-64-V4-0001, EXTREF-INTEL-TDX-OVERVIEW-0001, EXTREF-INTEL-TDX-ATTESTATION-0001, EXTREF-AMD-SEV-OVERVIEW-0001, EXTREF-AMD-SEV-ES-0001, EXTREF-AMD-SEV-SNP-0001, EXTREF-AMD-SEV-TIO-0001, EXTREF-INTEL-SGX-OVERVIEW-0001, EXTREF-INTEL-SGX-ATTESTATION-0001, EXTREF-INTEL-SGX-DCAP-0001, EXTREF-INTEL-CET-0001, EXTREF-CLANG-CFI-0001, EXTREF-CLANG-KCFI-0001, EXTREF-GCC-CF-PROTECTION-0001, EXTREF-RUST-CF-PROTECTION-0001, EXTREF-LINUX-KVM-API-0001, EXTREF-MICROSOFT-HYPERV-TLFS-0001 | registered draft `MFOS-REQ-X64-*`, `MFOS-REQ-X64-V4-*`, `MFOS-REQ-X64-CVM-*`, `MFOS-REQ-X64-TEE-*`, `MFOS-REQ-HARDENING-*`, and `MFOS-REQ-CPUFEAT-*` requirements | 26, 28, 30, 36, 37, 39, 44 | Current documentation policy. x86-64-v4 is optional, SGX is TEE not CVM, Hyper-V/KVM compatibility is not claimed, and no hardware/runtime implementation is authorized. |

## Numbering Gaps

The current split set has overlapping historical numbers because
executable-spec artifacts were split into separate files without renaming the
earlier release/localization/policy-lint specs. Phase provenance is retained in
the affected specs and reports, while this overlap remains a documentation
routing gap only; `spec_id` remains unique and machine validation keys off
`spec_id`.

If a future number is skipped, the gap is a planning gap only; it is not permission to place undefined semantics into unrelated specs.

## Cross-Spec Dependency Order

Recommended read and implementation order:

1. Governance base: `00`, `01`, `02`
2. Integrity and threat base: `03`, `04`
3. Shared model and evidence base: `05`, `06`, `07`
4. Enterprise semantic services: `08`, `09`, `10`, `11`
5. Extension and update controls: `12`, `13`
6. Nucleus and ABI: `14`, `15`
7. Partition and high-assurance isolation: `16`, `17`
8. Side integration: `18`
9. Assurance and conformance: `19`, `20`
10. AI and release governance: `21`, `22`
11. Requirements catalog: `23`
12. Formal methods: `24`
13. Operations and recovery: `25`
14. Hardware profile and measured boot: `26`, `30`
15. Spec/registry schemas and testing: `27`, `28`, `29`
16. Release distribution and rollback: `31`
17. Language/localization and policy lint: `32`, `33`
18. Deferred virtualization, confidential workload, cluster, verification, and secure-operations scaffolds: `36`, `37`, `38`, `39`, `40`, `41`
19. MFVM and Phase 1 Dafny executable-semantics policy: `42`, `43`
20. Architecture portability and x86-64 target profiles: `44`, `45`

## Implementation Target Matrix

| Target | Governing specs |
| --- | --- |
| Requirement/source lint | 00, 01, 02, 21, 22 |
| No-fake-success CI | 00, 02, 03, 21, 22 |
| securityd | 03, 04, 05, 06, 07, 08, 09, 10, 12, 13 |
| auditd | 03, 04, 05, 06, 07, 08, 09, 10, 12, 13, 16, 17, 18 |
| catalogd | 03, 04, 05, 06, 07, 08 |
| datasetd | 03, 04, 05, 06, 07, 08 |
| jobd | 03, 04, 05, 06, 07, 09, 11 |
| spoold | 03, 04, 05, 06, 07, 09, 10, 18 |
| operatord | 03, 04, 05, 06, 07, 10, 11, 16, 17, 18 |
| workpolicyd | 05, 06, 07, 09, 10, 11 |
| amfd | 03, 04, 05, 06, 07, 12, 13, 15, 17 |
| uvsd | 03, 04, 05, 06, 07, 12, 13, 16, 17, 22 |
| nucleus | 03, 04, 05, 07, 14, 15, 16 |
| SVC/PCALL | 03, 04, 05, 06, 07, 14, 15 |
| PXM core | 03, 04, 05, 06, 07, 14, 15, 16, 18, 22 |
| PXM Guard | 03, 04, 05, 07, 12, 13, 16, 17, 22 |
| Linux/Desktop gateway | 03, 04, 05, 06, 07, 08, 09, 10, 16, 18 |
| Assurance case | 00, 01, 02, 03, 04, 19, 21, 22, 24 |
| Conformance tests | 00, 01, 02, 03, 04, 19, 20, 21, 22, 24 |
| Requirements catalog and traceability | 00, 01, 02, 03, 04, 05 through 22, 23 |
| Formal models | 03, 04, 05, 06, 07, 08, 09, 10, 12, 13, 16, 17, 19, 20, 24 |
| Operations and recovery | 03, 04, 06, 07, 08, 09, 10, 13, 16, 17, 19, 20, 22, 23, 25 |
| Hardware/profile qualification | 03, 04, 14, 16, 17, 22, 26, 30 |
| Architecture portability and CPU target profiles | 26, 28, 30, 36, 37, 39, 44, 45 |
| Spec and registry tooling | 00, 01, 02, 21, 22, 23, 27, 28, 44, 45 |
| Test strategy and taxonomy | 03, 04, 19, 20, 21, 22, 23, 24, 29 |
| Attestation and measured boot | 07, 13, 16, 17, 22, 26, 30 |
| Release pipeline | 00, 01, 02, 04, 07, 13, 19, 20, 21, 22, 23, 25, 30, 31 |
| Language and Japanese mirror workflow | 00, 01, 02, 21, 22, 27, 32 |
| Policy lint | 04, 05, 06, 07, 21, 22, 23, 33 |
| Hypervisor-class virtualization planning | 03, 04, 16, 26, 36 |
| Confidential workload planning | 03, 04, 17, 26, 30, 36, 37 |
| Datacenter and cluster operations planning | 07, 11, 13, 25, 30, 31, 38 |
| Language and verification policy planning | 03, 04, 21, 22, 24, 39 |
| Automated reasoning program planning | 19, 20, 24, 39, 40 |
| Performance and secure operations planning | 11, 13, 22, 25, 26, 30, 31, 38, 41 |
| Dafny executable semantics and conformance harness | 31, 33, 39, 40, 43 |
| CPU Feature Registry and x86-64 target-profile validation | 26, 28, 44, 45 |

## Global Gaps To Track

These gaps recur across multiple specs and should be resolved by dedicated follow-up specs or amendments:

- Machine-readable schemas for requirements, glossary, source matrix, AI output, and evidence manifest.
- Concrete serialization choices for shared object schemas, audit records, manifests, and ABI frames.
- Exact SVC, PCALL, PXM_CALL, GUARD_CALL, and gateway transport binary formats.
- Final DSN grammar, JCL-like grammar, operator command grammar, policy grammar, redaction grammar, and clipboard/import/export policy grammars.
- Cryptographic algorithm choices, key hierarchy, threshold signing, revocation distribution, and attestation claim format.
- Production-path scanner scope and CI implementation for no-fake-success, TODO/unimplemented detection, source ID enforcement, ownership enforcement, and release evidence checking.
- Formal model toolchain, file locations, and proof/model-checking coverage criteria.
- Domain gate criteria for any semantic evaluator, especially language,
  verification, automated reasoning, and secure-operations policy domains.
- Fuzz campaign duration, corpus quality bar, and coverage thresholds.
- Recovery partition implementation and recovery drill evidence format.
- Independent TCB review workflow.
- Claim ID registry, conformance report path, and automated traceability graph format.
- Formal trace schema/runner and model acceptance criteria.
- Requirements catalog automation and uniform test ID traceability.
- Operations/recovery runbook formats, remote audit collector failover, OOB audit path, and evidence archive policy.
- Registration of requirement namespaces introduced after `00`, especially `OBJ`, `SVC`, `PCALL`, `GLOSS`, `PROD`, `LANG`, and `POLICY-LINT`.
- Registration of deferred planning namespaces introduced by `36` through `41`, especially `VIRT`, `CVM`, `CLUSTER`, `OPS`, `PERF`, `FORMAL`, and `ASSURANCE`.
- Complete Japanese mirror generation and language drift CI.
- Policy lint grammar, policy diff algorithm, and activation gate implementation.

## Index Maintenance Rules

- Add new split specs to this index in the same change that creates them.
- Do not list planned specs as complete until their files exist.
- Do not move gap ownership into an unrelated subsystem to make a row look complete.
- Keep source IDs explicit enough for AI routing; component specs remain authoritative for detailed citations.
- Keep compatibility wording negative and explicit: MFOS is inspired by selected source concepts and does not claim product compatibility.

## Planning And Phase-Gate Routing Addendum

Specs `36` through `42` are draft/provisional requirements-expansion specs
originating from the Phase 0.10 planning work. They strengthen planning for PXM,
MFVM, Confidential VM, datacenter/cluster, language verification, automated
reasoning, and secure operations, but they do not authorize implementation.
Spec `43` narrows Phase 1 to non-production Dafny executable-semantics
artifacts and deterministic conformance-harness validation. Product semantic
evaluator work is conditional and requires a later reviewed domain gate; Rust
semantic-core, future semantic-runner commands, hosted daemon,
PXM/MFVM/CVM/cluster evaluator, and production work remain blocked until later
gates close.
Specs `44` and `45` add architecture-portability and x86-64 target-profile
policy. They make MFOS x86-64-first, not x86-64-only; keep x86-64-v4 optional;
model TDX and SEV-SNP as Confidential VM profiles; model SGX as an optional
enclave/TEE profile; and require machine-readable CPU feature/profile
registries before hardware-facing backend implementation.
