# MFOS Source Matrix v0.1

Status: design draft

This document is the source-ID ledger for MFOS design work. It records the
sources that may be used to ground MFOS concepts, requirements, negative tests,
and implementation prompts.

MFOS is z/OS-inspired. MFOS is not z/OS-compatible, not a z/Architecture
emulator, and not a reimplementation of IBM products or APIs.

## Purpose

The purpose of this source matrix is to keep MFOS work source-grounded and
AI-friendly:

- Assign stable source IDs for IBM, x64, high-assurance, and internal transfer
  sources.
- Separate normative, informative, and internal transfer material.
- Identify which MFOS concepts each source may ground.
- Prevent invented z/OS-like terminology from entering the architecture.
- Require explicit semantic overlap and divergence before IBM terminology is
  used in MFOS specifications.
- Make source IDs usable by specs, requirements, tests, code comments, review
  checklists, and AI implementation prompts.

## Scope

This matrix covers source grounding for the MFOS design areas listed below:

- System integrity and authorized state.
- Storage protection concepts and their x64 divergence.
- RACF-inspired security manager behavior.
- JES-inspired job and spool behavior.
- DFSMS-inspired dataset and catalog behavior.
- SMF-inspired audit and accounting behavior.
- external-workload-management-informed workload management behavior.
- z/OS UNIX as an optional subsystem reference.
- Cross-memory communication concepts used to constrain MFOS PCALL.
- LPAR and DPM concepts used to shape PXM.
- x64 hardware reality: Intel, AMD, Linux PKU, Linux CET.
- VBS/VSM-inspired Guard concepts for the High-Assurance profile only.
- Supply-chain, update, firmware resilience, and formal-assurance references.
- Language, unsafe-code, no_std, and compiler control-flow hardening references.
- FBVBS as an internal transfer source for traceability and assurance
  discipline.

## Non-objectives

This matrix does not:

- Claim z/OS compatibility.
- Claim JES, RACF, DFSMS, SMF, workload policy, APF, or z/OS UNIX compatibility.
- Replace IBM, Intel, AMD, Microsoft, NIST, TCG, seL4, SLSA, or TUF
  documentation.
- Replace Rust, LLVM/Clang, GCC, Linux kernel, Kani, Verus, AWS, GitHub, or
  NIST documentation.
- Authorize copying IBM behavior that is not explicitly mapped and reviewed.
- Permit long quotations from vendor documentation.
- Make hardware features such as PKU, PKS, CET, SMEP, or SMAP the primary
  source of MFOS system integrity.
- Put VBS-like Guard behavior into the MFOS Baseline profile.

## Source Classes

Normative Source:
  A source that may ground MFOS requirements and conformance claims. Examples:
  IBM-published public documentation, Intel SDM, AMD APM, TCG specifications,
  NIST publications, Microsoft-published documentation for VBS/VSM concepts,
  Rust Reference documentation for MFOS language policy, TUF, and SLSA
  specifications.

Informative Source:
  A source used for comparison, implementation understanding, or review
  discipline. Informative sources do not by themselves create MFOS conformance
  requirements.

Internal Transfer Source:
  Internal project material whose structure or assurance discipline is reused
  in MFOS. Internal transfer sources must not be used to invent IBM semantics.

## Source ID Rules

- Every z/OS-inspired MFOS concept must cite at least one Source Matrix ID.
- Every IBM-derived term used as an MFOS term must document semantic overlap
  and MFOS divergence.
- If a source supports only an analogy, the spec must say so explicitly.
- If a behavior is not grounded by a source and is not purely internal MFOS
  design, it must be marked `SPEC_GAP`.
- AI-generated requirements, code, tests, and prompts must list source IDs.
- Source IDs may be updated by adding new rows; do not silently redefine an
  existing ID.

## IBM / z/OS Source IDs

| Source ID | Class | MFOS area | Source title or publication | Source location | MFOS use |
| --- | --- | --- | --- | --- | --- |
| EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001 | Normative | System integrity | z/OS and system integrity | https://www.ibm.com/docs/en/zos-basic-skills?topic=zos-system-integrity | Grounds the MFOS System Integrity Statement: unauthorized subjects must not bypass protection, security checks, audit, or authorized state through system interfaces. |
| EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001 | Normative | Authorized boundary testing | z/OS Authorized Code Scanner introduction and overview | https://www.ibm.com/docs/en/zos/3.2.0?topic=zacsg-introduction and https://www.ibm.com/docs/en/zos/3.2.0?topic=guide-overview | Grounds zACS-style negative tests for SVC, PCALL, AMF, privileged entry points, untrusted parameters, and accidental authority transfer. |
| EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001 | Normative | Authorized module model | Authorized programs | https://www.ibm.com/docs/en/zos/3.2.0?topic=system-authorized-programs | Grounds AMF as OS extension authorization, not administrator privilege. |
| EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001 | Normative | Storage domains | What is storage protection? | https://www.ibm.com/docs/en/zos-basic-skills?topic=storage-what-is-protection | Grounds storage-key and PSW-key concepts that MFOS maps to software-defined execution states and storage domains. |
| EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001 | Normative | Storage protection details | Storage protection summary | https://www.ibm.com/docs/en/zos/3.1.0?topic=summary-storage-protection | Grounds storage key, fetch-protection, reference, and change-bit vocabulary used only as mapped concepts. |
| EXTREF-IBM-ZOS-SECURITY-SERVER-0001 | Normative | Security manager | z/OS Security Server RACF library | https://www.ibm.com/docs/en/zos/3.2.0?topic=zos-security-server-racf | Grounds the RACF-inspired document family for securityd: profiles, callable services, commands, macros, auditing, and administration. |
| EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001 | Normative | Resource profiles | Authorizing users to access protected resources | https://www.ibm.com/docs/en/zos/3.1.0?topic=racf-authorizing-users-access-protected-resources | Grounds the securityd model of principals, groups, resource profiles, access lists, default access, and authorization decisions. |
| EXTREF-IBM-ZOS-JES-INTRODUCTION-0001 | Normative | Job subsystem | What is JES? | https://www.ibm.com/docs/en/zos-basic-skills?topic=jobs-what-is-jes | Grounds job submission, queueing, initiators, SYSIN, SYSOUT, and spool concepts. |
| EXTREF-IBM-ZOS-JES-JOB-FLOW-0001 | Normative | Job lifecycle | Job flow through the system | https://www.ibm.com/docs/de/zos-basic-skills?topic=jobs-job-flow-through-system | Grounds the INPUT, CONVERSION, PROCESSING, OUTPUT, print/punch, and PURGE lifecycle concepts that MFOS maps into jobd/spoold states. |
| EXTREF-IBM-ZOS-JES2-LIBRARY-0001 | Normative | JES2 detail | z/OS JES2 library | https://www.ibm.com/docs/en/zos/3.2.0?topic=zos-jes2 | Grounds detailed JES2 command, initialization, tuning, macro, message, and data-area review for future jobd/spoold specs. |
| EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001 | Normative | Catalog model | DFSMSdfp Catalogs | https://www.ibm.com/docs/en/zos/3.1.0?topic=dfsmsdfp-catalogs | Grounds catalogd as the service mapping dataset names to attributes, location, owner, generation, and integrity metadata. |
| EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001 | Normative | Dataset and storage management | z/OS DFSMS library | https://www.ibm.com/docs/en/zos/3.2.0?topic=zos-dfsms | Grounds datasetd/catalogd specification review for allocation, catalog management, data sets, storage administration, and advanced services. |
| EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | Normative | Audit and accounting | Introduction to SMF | https://www.ibm.com/docs/en/zos/3.1.0?topic=smf-introduction | Grounds auditd as evidence, accounting, reliability, configuration, job, dataset, resource, and security activity collection. |
| EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001 | Normative | Security audit records | Record type 80: RACF processing record | https://www.ibm.com/docs/en/zos/3.1.0?topic=records-record-type-80-racf-processing-record | Grounds MFOS security audit record fields such as unauthorized attempts, event code, user identity, authorities used, and audit reason. |
| EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001 | Normative | Workload management | Defining service classes and performance goals | https://www.ibm.com/docs/SSLTBW_3.2.0/com.ibm.zos.v3r2.ieaw100/sclg.htm | Grounds service classes, goals, importance, response-time goals, velocity-like goals, discretionary work, and workpolicyd phase planning. |
| EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001 | Normative | Optional POSIX subsystem | Introduction to z/OS UNIX | https://www.ibm.com/docs/en/zos/3.1.0?topic=planning-introduction-zos-unix | Grounds the statement that UNIX-like behavior is an optional subsystem, not the primary MFOS model. |
| EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001 | Normative | UNIX subsystem detail | z/OS UNIX System Services library | https://www.ibm.com/docs/en/zos/latest?topic=zos-unix-system-services | Grounds future optional subsystem details for commands, file-system interfaces, callable services, planning, and user guidance. |
| EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001 | Normative | PCALL and cross-address-space control | Synchronous cross memory communication | https://www.ibm.com/docs/en/zos/3.1.0?topic=guide-synchronous-cross-memory-communication | Grounds PC instruction and PC routine concepts used to constrain MFOS PCALL. |
| EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001 | Normative | Cross-memory security | Controlling cross-memory communication | https://www.ibm.com/docs/en/zos-basic-skills?topic=integrity-controlling-cross-memory-communication | Grounds MFOS refusal to expose arbitrary cross-address-space pointers early; PCALL must use typed endpoints and sealed buffers. |
| EXTREF-IBM-Z-LPAR-INTRODUCTION-0001 | Normative | PXM partition model | Introduction to Logical Partitions | https://www.ibm.com/support/pages/introduction-logical-partitions | Grounds PXM partition lifecycle, activation profiles, processors, storage, I/O, and logical machine image concepts. |
| EXTREF-IBM-Z-DPM-0001 | Normative | PXM management plane | Dynamic Partition Manager | https://www.ibm.com/docs/en/systems-hardware/zsystems/2964-N63?topic=cm-dynamic-partition-manager-dpm | Grounds object-oriented partition, adapter, network, storage, capacity, and management-plane concepts. |
| EXTREF-IBM-Z-ARCHITECTURE-PRINCIPLES-0001 | Normative | z/Architecture terminology | z/Architecture Principles of Operation, SA22-7832-14 | https://www.ibm.com/support/pages/zvm/library/other.html | Grounds terminology review for PSW, storage key, SVC, PC, and z/Architecture differences from x64. |
| EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001 | Informative | Update security advisory model | SECINT HOLDDATA is now available with SMP/E RECEIVE ORDER | https://www.ibm.com/support/pages/secint-holddata-now-available-smpe-receive-order | Informs update/security advisory handling and the distinction between update transport and security-relevant metadata. |

## x64 / High-Assurance / Supply-Chain Source IDs

| Source ID | Class | MFOS area | Source title | Source location | MFOS use |
| --- | --- | --- | --- | --- | --- |
| X64-INTEL-001 | Normative | Intel x64 system programming | Intel 64 and IA-32 Architectures Software Developer Manuals | https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html | Grounds Intel protection, memory management, interrupts, VMX, EPT, MSRs, CET, PKU, PKS where applicable. |
| X64-AMD-001 | Normative | AMD64 system programming | AMD64 Architecture Programmer's Manual Volume 2: System Programming | https://docs.amd.com/v/u/en-US/24593_3.44_APM_Vol2 | Grounds AMD64 protection, SVM, NPT, paging, interrupts, and system programming differences. |
| X64-LINUX-PKU-001 | Informative | PKU behavior | Linux kernel memory protection keys documentation | https://docs.kernel.org/core-api/protection-keys.html | Grounds the MFOS warning that x86 pkeys are data-access controls, not instruction-fetch controls or z/OS storage-key compatibility. |
| X64-LINUX-CET-001 | Informative | CET behavior | Linux x86 CET shadow stack documentation | https://docs.kernel.org/arch/x86/shstk.html | Grounds CET as control-flow hardening and not a full authorization or storage-domain mechanism. |
| EXTREF-RUST-UNSAFE-REFERENCE-0001 | Normative | Rust unsafe policy | The Rust Reference: the unsafe keyword | https://doc.rust-lang.org/reference/unsafe-keyword.html | Grounds MFOS unsafe-boundary review and evidence planning without copying Rust reference text. |
| EXTREF-RUST-NO-STD-REFERENCE-0001 | Normative | Rust no_std policy | The Rust Reference: the no_std attribute | https://doc.rust-lang.org/reference/names/preludes.html#the-no_std-attribute | Grounds no_std/freestanding runtime-contract planning. |
| EXTREF-RUST-CF-PROTECTION-0001 | Informative | Rust cf-protection planning | The Rust Unstable Book: cf_protection | https://doc.rust-lang.org/unstable-book/compiler-flags/cf-protection.html | Grounds Rust x86 CET feature-profile planning only; no production enforcement claim. |
| EXTREF-CLANG-CFI-0001 | Informative | C/C++ boundary hardening | Clang Control Flow Integrity documentation | https://clang.llvm.org/docs/ControlFlowIntegrity.html | Grounds Clang CFI as defense-in-depth evidence for approved C/C++ boundaries. |
| EXTREF-CLANG-KCFI-0001 | Informative | Kernel CFI planning | Clang Kernel Control Flow Integrity documentation | https://clang.llvm.org/docs/ControlFlowIntegrity.html#fsanitize-kcfi | Grounds KCFI planning for future kernel-oriented indirect-call hardening. |
| EXTREF-GCC-CF-PROTECTION-0001 | Informative | GCC cf-protection planning | GCC Program Instrumentation Options: fcf-protection | https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html | Grounds GCC x86 GNU/Linux CET instrumentation planning only. |
| MS-VBS-001 | Normative | Guard inspiration | Memory Integrity and Virtualization-Based Security | https://learn.microsoft.com/en-us/windows-hardware/drivers/bringup/device-guard-and-credential-guard | Grounds High-Assurance-only Guard concepts around isolated protection for code integrity and executable page policy. |
| MS-VSM-001 | Normative | Guard inspiration | Virtual Secure Mode | https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/tlfs/vsm | Grounds VTL-like separation ideas for Guard root objects, with explicit divergence from Windows VSM. |
| TCG-001 | Normative | Measured boot | TCG PC Client Platform Firmware Profile Specification | https://trustedcomputinggroup.org/resource/pc-client-specific-platform-firmware-profile-specification/ | Grounds TPM, firmware measurements, measured boot, and event log expectations. |
| NIST-160-001 | Normative | Secure systems engineering | NIST SP 800-160 Vol. 1 Rev. 1 | https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final | Grounds lifecycle-level trustworthy secure systems engineering. |
| NIST-218-001 | Normative | Secure software development | NIST SP 800-218 SSDF | https://csrc.nist.gov/pubs/sp/800/218/final | Grounds secure development practice requirements and quality gates. |
| NIST-193-001 | Normative | Firmware resilience | NIST SP 800-193 Platform Firmware Resiliency Guidelines | https://www.nist.gov/node/1336751 | Grounds protection, detection, and recovery requirements for firmware and boot resilience. |
| SEL4-001 | Informative | Formal assurance boundary | seL4 verification material | https://sel4.org/Verification/ | Informs how MFOS must state verified properties, assumptions, and out-of-scope hardware or boot assumptions. |
| SLSA-001 | Normative | Supply chain | SLSA specification and provenance page | https://slsa.dev/spec/v1.2/ and https://slsa.dev/spec/v1.2/provenance | Grounds build provenance, hosted build, hardened build, and supply-chain integrity claims. |
| TUF-001 | Normative | Update security | The Update Framework Specification | https://theupdateframework.github.io/specification/v1.0.26/ and https://theupdateframework.io/docs/metadata/ | Grounds root, targets, snapshot, timestamp roles and rollback, freeze, mix-and-match, and key-compromise defenses. |
| FBVBS-001 | Internal Transfer | Assurance discipline | FBVBS uploaded specification | Internal project document | Transfers requirement IDs, profiles, state machines, command-page discipline, update manifests, evidence, and production proof obligations into MFOS. |

## Primary Concept-to-Source Map

| MFOS concept | Required source IDs | Use |
| --- | --- | --- |
| System integrity | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001, EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001, EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001 | Define what unauthorized subjects cannot bypass, and require negative tests for authorized boundaries. |
| Authorized module facility (AMF) | EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, X64-INTEL-001, X64-AMD-001 | Map APF-inspired authorization into signed, measured, revocable MFOS modules. |
| securityd | EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001 | Define principal, group, resource profile, access decision, obligation, and security audit model. |
| auditd | EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001, FBVBS-001 | Define evidence streams, hash chains, security records, failure policy, and Guard-sealed roots in High-Assurance. |
| catalogd/datasetd | EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001, EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | Define dataset names, catalog resolution, dataset handles, security checks, retention, integrity, and audit obligations. |
| jobd/spoold | EXTREF-IBM-ZOS-JES-INTRODUCTION-0001, EXTREF-IBM-ZOS-JES-JOB-FLOW-0001, EXTREF-IBM-ZOS-JES2-LIBRARY-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | Define job submission, conversion, queueing, execution, SYSIN, SYSOUT, spool retention, browse, purge, and audit. |
| operatord | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-JES2-LIBRARY-0001 | Define operator command authority, audit, grammar, confirmation, and denial behavior. |
| workpolicyd | EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | Define service classes, job classes, importance, resource goals, and reporting. |
| Optional POSIX subsystem | EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001, EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001, EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001 | Define POSIX as optional and profile-limited; it cannot bypass MFOS security or audit. |
| SVC and PCALL | EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001, EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, X64-INTEL-001, X64-AMD-001 | Define typed, bounded, nucleus-mediated service calls and prohibit unsafe cross-address-space pointer trust. |
| PXM | EXTREF-IBM-Z-LPAR-INTRODUCTION-0001, EXTREF-IBM-Z-DPM-0001, FBVBS-001, X64-INTEL-001, X64-AMD-001 | Define partition lifecycle, activation profiles, CPU/memory/device assignment, IOMMU, interrupt remapping, and partition audit. |
| PXM Guard | MS-VBS-001, MS-VSM-001, FBVBS-001, X64-INTEL-001, X64-AMD-001 | Define High-Assurance-only root object protection, executable mapping policy, AMF registry sealing, SVC table integrity, and attestation. |
| Update verification | TUF-001, EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001, NIST-218-001, SLSA-001, FBVBS-001 | Define metadata verification, rollback/freeze/mix-and-match defense, security epoch, provenance, and evidence. |
| Firmware and measured boot | TCG-001, NIST-193-001, NIST-160-001 | Define measured boot, TPM event logs, firmware resilience, recovery, and assumptions. |
| Language and toolchain hardening | EXTREF-RUST-UNSAFE-REFERENCE-0001, EXTREF-RUST-NO-STD-REFERENCE-0001, EXTREF-RUST-CF-PROTECTION-0001, EXTREF-CLANG-CFI-0001, EXTREF-CLANG-KCFI-0001, EXTREF-GCC-CF-PROTECTION-0001, X64-LINUX-CET-001, EXTREF-INTEL-CET-0001, EXTREF-KANI-RUST-VERIFIER-0001, EXTREF-VERUS-RUST-VERIFICATION-0001, EXTREF-GITHUB-CODEQL-0001 | Define unsafe-boundary review, no_std runtime contracts, CFI/CET evidence limits, static-analysis evidence, and proof-tool caveats. |

## Semantic Mapping Summary

| IBM concept | MFOS mapping | Semantic overlap | MFOS divergence |
| --- | --- | --- | --- |
| z/OS system integrity | MFOS System Integrity Statement | Both prevent unauthorized programs or subjects from bypassing protection, security checks, and authorized state through system interfaces. | MFOS is x64-native and object/capability oriented; compromise of authorized code is not a Baseline system-integrity claim and belongs to High-Assurance Guard. |
| APF authorized program | AMF authorized module | Both distinguish special OS extension authority from ordinary user authority. | AMF requires signed artifacts, measurement, revocation, explicit ABI, copy-in/copy-out, audit, and optional Guard approval. AMF is not administrator privilege. |
| Storage key / PSW key | ExecutionState and StorageDomain | Both separate execution authority from access to protected storage-like domains. | MFOS does not emulate z/Architecture storage keys. x64 PKU/PKS are optional helpers and cannot be called storage-key compatibility. |
| RACF resource profile | securityd resource profile | Both use principals, groups, protected resources, access lists, and authorization decisions. | securityd decision results include obligations such as audit, MFA, dual control, Guard approval, and unsupported/spec-gap handling. |
| JES job and spool | jobd and spoold | Both treat jobs, queues, initiators, SYSIN/SYSOUT, output processing, and spool as first-class operational concepts. | MFOS implements a source-grounded subset and does not claim JES/JES2 command or JCL compatibility. |
| DFSMS catalog | catalogd | Both resolve dataset names to attributes and locations so users do not manage raw placement directly. | MFOS catalog entries include explicit owner, security profile, generation, integrity tag, and immutable/system flags. |
| SMF | auditd | Both collect system, job, dataset, resource, and security event evidence. | MFOS auditd requires schema validation, hash chains, fail-closed behavior for required audit, and optional Guard-sealed roots. |
| workload policy service class | workpolicyd service class | Both group work with similar goals, importance, and resource expectations. | MFOS starts with job class, priority, max concurrency, and resource caps before response-time or velocity-like goals. |
| z/OS UNIX | Optional POSIX subsystem | Both allow UNIX-like APIs and shell behavior inside a larger enterprise OS environment. | MFOS POSIX is optional, restricted, and cannot reinterpret datasets as ordinary POSIX files or bypass securityd/auditd. |
| LPAR / PR/SM | PXM partition | Both model logical machine images with assigned processors, storage, I/O, lifecycle, and activation profiles. | PXM is an x64 partition layer and must not understand MFOS job, dataset, or security policy semantics. |
| VBS/VSM isolation | PXM Guard | Both use a higher-privilege protection layer to protect selected roots from lower layers. | Guard exists only for High-Assurance claims and protects selected root objects only; it is not Windows VBS/VSM compatibility. |

## Allowed and Prohibited Wording

Allowed wording:

- "MFOS is z/OS-inspired."
- "MFOS maps selected IBM-documented enterprise OS concepts into an x64-native
  high-assurance design."
- "securityd is RACF-inspired, not RACF-compatible."
- "jobd/spoold are JES-inspired, not JES-compatible."
- "catalogd/datasetd are DFSMS-inspired, not DFSMS-compatible."
- "PXM is LPAR-inspired in lifecycle and management concepts."
- "PXM Guard is VBS/VSM-inspired for selected High-Assurance root objects."
- "PKU/PKS may assist compartments or metadata protection where available."

Prohibited wording:

- "MFOS is z/OS-compatible."
- "MFOS implements z/OS."
- "MFOS is JES-compatible", "RACF-compatible", "DFSMS-compatible",
  "SMF-compatible", "external-workload-management-compatible", or "APF-compatible".
- "PKU/PKS provide z/OS storage-key compatibility."
- "PXM implements PR/SM."
- "PXM Guard implements Windows VBS/VSM."
- "Dataset is just a POSIX file."
- "Operator console is a root shell."
- "AMF is admin privilege."
- "Audit log is ordinary logging."

## Verification Obligations

Every spec or implementation that cites this source matrix must satisfy these
obligations:

- List all source IDs used.
- State semantic overlap and divergence for every IBM-derived concept.
- Include at least one negative test for every authorization boundary.
- Include audit obligations for every protected resource operation.
- Use `UNSUPPORTED` for specified but unimplemented behavior.
- Use `SPEC_GAP` for behavior not yet specified.
- Prohibit success responses from empty stubs or silent fallbacks.
- Prohibit final authorization decisions outside securityd.
- Prohibit audit bypass for security-relevant decisions.
- Keep PXM free of MFOS enterprise semantics.
- Keep Guard limited to selected High-Assurance root objects.

## Required Negative Test Themes

- Unauthorized subject obtains dataset handle.
- Unauthorized subject browses, purges, or exports spool entry.
- Job opens dataset before effective principal is established.
- Operator command executes without authorization decision.
- DENY result returns before audit record is emitted.
- AMF load succeeds with invalid signature.
- AMF load succeeds with revoked signer or digest.
- SVC or PCALL trusts caller-supplied identity.
- SVC or PCALL dereferences untrusted pointer directly.
- Catalog resolves uncommitted or rolled-back entry.
- Dataset stale handle works after policy version change.
- PXM assigns device without IOMMU domain and interrupt remapping.
- PXM reassigns memory before mappings are revoked and memory zeroed.
- Guard accepts mismatched security root, audit root, AMF registry, or SVC table.
- Update accepts rollback, freeze, or mix-and-match metadata.
- AI-generated implementation fails to return `MFOS_ERR_UNSUPPORTED` or `MFOS_ERR_SPEC_GAP` for unsupported or unspecified behavior.

## Spec Gaps

The following items need later source review before production claims:

- Exact IBM publication numbers, section names, and version pins for every IBM
  source row.
- A machine-readable source matrix format, such as YAML or JSON, generated from
  this Markdown without changing source IDs.
- Per-source citation review to confirm that all summaries are paraphrases and
  remain within citation policy.
- A formal rule for when an informative source may become normative.
- A source freshness review cadence for vendor manuals and online docs.
- A complete mapping from source IDs to requirement IDs after the split specs
  are written.

## AI Prompt

Use this prompt when asking an AI system to extend or review source-grounded
MFOS material:

```text
You are the MFOS source-grounding reviewer.

Task:
Review the proposed MFOS concept, requirement, test, or implementation note
against the MFOS Source Matrix.

Constraints:
- Do not claim z/OS compatibility.
- Do not claim JES, RACF, DFSMS, SMF, workload policy, APF, PR/SM, or VBS compatibility.
- Require Source Matrix IDs for all z/OS-inspired concepts.
- Require semantic overlap and MFOS divergence for IBM-derived terms.
- Mark missing source grounding as SPEC_GAP.
- Mark specified but unimplemented behavior as UNSUPPORTED.
- Reject fake success, empty stubs, and silent fallback.
- Reject securityd bypass and auditd bypass.
- Keep PXM free of MFOS enterprise semantics.
- Keep Guard limited to High-Assurance root objects.

Output:
1. Source IDs used
2. Missing source IDs
3. Semantic overlap
4. MFOS divergence
5. Allowed wording
6. Prohibited wording
7. Requirement IDs affected
8. Verification obligations
9. Negative tests required
10. Spec gaps

Input:
<MFOS_TEXT>
```

## Phase 0.10 External Reference Additions

The following public-safe reference cards were added for PXM/MFVM, confidential VM, language-safety, and formal-assurance planning. They are reference and comparison sources only; they do not create compatibility claims.

| Source ID | Purpose |
| --- | --- |
| `EXTREF-MICROSOFT-HYPERV-TLFS-0001` | Microsoft Hyper-V Hypervisor Top-Level Functional Specification |
| `EXTREF-MICROSOFT-HYPERV-OVERVIEW-0001` | Hyper-V virtualization in Windows Server and Windows |
| `EXTREF-MICROSOFT-HYPERV-VSM-0001` | Virtual Secure Mode |
| `EXTREF-LINUX-KVM-API-0001` | The Definitive KVM API Documentation |
| `EXTREF-LINUX-KVM-VFIO-0001` | VFIO - Virtual Function I/O |
| `EXTREF-LINUX-KVM-CAPABILITIES-0001` | KVM capability discovery documentation |
| `EXTREF-INTEL-TDX-OVERVIEW-0001` | Intel Trust Domain Extensions overview |
| `EXTREF-INTEL-TDX-LINUX-DOC-0001` | Intel Trust Domain Extensions in Linux |
| `EXTREF-INTEL-TDX-ATTESTATION-0001` | Intel Trust Domain Extensions attestation documentation |
| `EXTREF-INTEL-CET-0001` | A Technical Look at Intel Control-Flow Enforcement Technology |
| `EXTREF-RUST-UNSAFE-REFERENCE-0001` | The Rust Reference: the unsafe keyword |
| `EXTREF-RUST-NO-STD-REFERENCE-0001` | The Rust Reference: the no_std attribute |
| `EXTREF-RUST-CF-PROTECTION-0001` | The Rust Unstable Book: cf_protection |
| `EXTREF-CLANG-CFI-0001` | Clang Control Flow Integrity documentation |
| `EXTREF-CLANG-KCFI-0001` | Clang Kernel Control Flow Integrity documentation |
| `EXTREF-GCC-CF-PROTECTION-0001` | GCC Program Instrumentation Options: fcf-protection |
| `EXTREF-AMD-SEV-OVERVIEW-0001` | AMD Secure Encrypted Virtualization overview |
| `EXTREF-AMD-SEV-ES-0001` | AMD SEV Encrypted State overview |
| `EXTREF-AMD-SEV-SNP-0001` | AMD SEV-SNP strengthening VM isolation white paper |
| `EXTREF-AMD-SEV-TIO-0001` | AMD SEV-TIO Trusted I/O white paper |
| `EXTREF-LINUX-AMD-SEV-KVM-DOC-0001` | Linux KVM AMD memory encryption documentation |
| `EXTREF-KANI-RUST-VERIFIER-0001` | The Kani Rust Verifier |
| `EXTREF-VERUS-RUST-VERIFICATION-0001` | Verus Tutorial and Reference |
| `EXTREF-AWS-AUTOMATED-REASONING-0001` | What is Automated Reasoning? |
| `EXTREF-GITHUB-CODEQL-0001` | About code scanning with CodeQL |
| `EXTREF-NIST-SECURE-SYSTEMS-ENGINEERING-0001` | NIST SP 800-160 Vol. 1 Rev. 1 |
| `EXTREF-NIST-SSDF-0001` | NIST SP 800-218 Secure Software Development Framework |
