---
spec_id: "MFOS-SPEC-23-REQUIREMENTS-CATALOG"
title: "MFOS Requirements Catalog v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001", "EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001", "EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001", "EXTREF-IBM-Z-DPM-0001", "EXTREF-IBM-ZOS-JES-INTRODUCTION-0001", "EXTREF-IBM-ZOS-JES-JOB-FLOW-0001", "EXTREF-IBM-ZOS-JES2-LIBRARY-0001", "EXTREF-IBM-Z-LPAR-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001", "EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001", "EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001", "EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001", "EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001", "EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001", "EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001", "EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001", "EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001", "EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001", "MS-VBS-001", "MS-VSM-001", "NIST-160-001", "NIST-193-001", "NIST-218-001", "SEL4-001", "SLSA-001", "TCG-001", "TUF-001", "X64-AMD-001", "X64-INTEL-001", "X64-LINUX-CET-001", "X64-LINUX-PKU-001"]
requirement_refs: ["MFOS-REQ-AI-*", "MFOS-REQ-AMF-*", "MFOS-REQ-AUDIT-*", "MFOS-REQ-CATALOG-*", "MFOS-REQ-DATASET-*", "MFOS-REQ-GLOSS-*", "MFOS-REQ-GUARD-*", "MFOS-REQ-JOB-*", "MFOS-REQ-LGW-*", "MFOS-REQ-NUCLEUS-*", "MFOS-REQ-OBJ-*", "MFOS-REQ-OPER-*", "MFOS-REQ-PCALL-*", "MFOS-REQ-PROFILE-*", "MFOS-REQ-PARTITION-*", "MFOS-REQ-QUALITY-*", "MFOS-REQ-AUTH-*", "MFOS-REQ-SYSINT-*", "MFOS-REQ-SPOOL-*", "MFOS-REQ-SOURCE-*", "MFOS-REQ-SVC-*", "MFOS-REQ-UPDATE-*", "MFOS-REQ-WPOL-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Requirements Catalog v0.1

Status: Draft design split

Owner area: `docs/design/specs/23-requirements-catalog.md`

This catalog consolidates the requirements from `docs/design/mfos-design.md` and the split design specs. It is the index used by AI agents, reviewers, tests, and evidence tooling to avoid invented semantics, fake success, missing audit, and untraceable implementation.

MFOS is source-grounded and z/OS-inspired. It MUST NOT claim compatibility with IBM z/OS, z/Architecture binaries, z/OS APIs, RACF, JES, DFSMS, SMF, workload policy, or JCL.

## 1. Catalog Rules

Each requirement record has:

- Requirement ID.
- Requirement text.
- Source Matrix IDs where known.
- Verification method.
- Profile applicability.
- Related tests or test family.
- Evidence artifact.
- Known gaps.

Requirement IDs are stable. If a requirement changes meaning, create a new ID or record an ADR that explains the compatibility impact for tests and evidence.

## 2. Profile Legend

| Profile label | Meaning |
| --- | --- |
| B | Baseline. Required for hosted semantics and early MFOS correctness unless explicitly scoped higher. |
| ES | Enterprise-Standalone. Adds measured boot, stronger update, remote audit, provenance, and platform DMA protection without PXM partition claims. |
| EPXM | Enterprise-PXM. Adds PXM lifecycle, side-partition, and device-assignment claims when PXM evidence exists. |
| HA | High-Assurance. Requires PXM Guard and root-object evidence. |
| Dev | Non-production development mode only. Cannot support production or High-Assurance claims. |

Profile notation:

- `B/ES/EPXM/HA`: required in all conformance profiles.
- `ES/EPXM/HA`: required in Enterprise-Standalone, Enterprise-PXM, and High-Assurance.
- `HA`: required only in High-Assurance.
- `B optional; ES/EPXM/HA required`: optional in Baseline, required above it.

## 3. Evidence Artifact Conventions

Evidence artifacts SHOULD use these names until the assurance-case spec replaces them:

```text
evidence/requirements/<REQ-ID>.md
evidence/tests/<TEST-ID>.json
evidence/reviews/<REQ-ID>-review.md
evidence/fuzz/<FUZZ-ID>.md
evidence/formal/<MODEL-ID>.md
evidence/ci/<CI-CHECK-ID>.json
evidence/provenance/<release-id>/
evidence/attestation/<attestation-id>.json
```

For each implemented requirement, the evidence file MUST list:

```text
implemented_requirement_ids
source_matrix_ids
design_spec_refs
code_refs
positive_tests
negative_tests
fuzz_targets
audit_obligations
failure_modes
unsupported_features
spec_gaps
review_status
```

## 4. Namespace Defaults

These defaults apply to all rows in a namespace unless a row says otherwise.

| Namespace | Owning specs | Default source IDs | Default profiles | Default evidence | Known gaps |
| --- | --- | --- | --- | --- | --- |
| `MFOS-REQ-PROFILE-*` | `00-normative-language.md` | `FBVBS-001`, `NIST-160-001` | B/ES/EPXM/HA | conformance review | profile claim granularity, production gate binding |
| `MFOS-REQ-SOURCE-*` | `02-source-matrix.md`, `00-normative-language.md` | IBM source IDs by concept, `FBVBS-001` | B/ES/EPXM/HA | source-matrix lint report | source coverage completeness, quote policy automation |
| `MFOS-REQ-GLOSS-*` | `01-glossary.md` | IBM source IDs by term, x64 source IDs by mechanism | B/ES/EPXM/HA | glossary lint report | canonical term lint, alias policy |
| `MFOS-REQ-SYSINT-*` | `03-system-integrity.md` | `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001`, `EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001`, `X64-INTEL-001`, `X64-AMD-001`, `FBVBS-001` | B/ES/EPXM/HA; Guard claims HA | integrity evidence pack | formal boundary model, exact SVC inventory, platform feature matrix |
| `MFOS-REQ-OBJ-*` | `05-object-model.md` | `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001`, `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `TUF-001`, `FBVBS-001` | B/ES/EPXM/HA; Guard-root fields HA | object schema test report | concrete serialization, DSN grammar, Guard claim format |
| `MFOS-REQ-AUTH-*` | `06-authorization.md` | `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `FBVBS-001` | B/ES/EPXM/HA; Guard obligations HA | authorization trace report | policy language, bootstrap policy, MFA token schema |
| `MFOS-REQ-AUDIT-*` | `07-audit.md` | `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001`, `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `FBVBS-001` | B/ES/EPXM/HA; remote export ES/EPXM/HA; Guard root HA | audit-chain evidence | canonical encoding, remote export protocol, redaction language |
| `MFOS-REQ-CATALOG-*` | `08-dataset-catalog.md` | `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001` | B/ES/EPXM/HA | catalog transaction evidence | exact DSN grammar, extent format |
| `MFOS-REQ-DATASET-*` | `08-dataset-catalog.md` | `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001` | B/ES/EPXM/HA; encryption hardening ES/EPXM/HA | dataset handle evidence | key service profile, secure deletion backend |
| `MFOS-REQ-JOB-*` | `09-job-spool.md` | `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-JES-JOB-FLOW-0001`, `EXTREF-IBM-ZOS-JES2-LIBRARY-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001` | B/ES/EPXM/HA | job lifecycle evidence | JCL-like subset grammar, restart model |
| `MFOS-REQ-SPOOL-*` | `09-job-spool.md` | `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001` | B/ES/EPXM/HA | spool access evidence | spool retention/purge policy details |
| `MFOS-REQ-OPER-*` | `10-operator-console.md` | `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001` | B/ES/EPXM/HA | operator drill evidence | command grammar completion, automation API |
| `MFOS-REQ-WPOL-*` | `11-workload-policy.md` | `EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001`, `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001` | B/ES/EPXM/HA; advanced goals later | workload policy evidence | response-time/velocity semantics deferred |
| `MFOS-REQ-AMF-*` | `12-amf.md` | `EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `X64-INTEL-001`, `X64-AMD-001`, `MS-VBS-001`, `MS-VSM-001`, `TUF-001`, `SLSA-001`, `NIST-218-001`, `FBVBS-001` | B/ES/EPXM/HA; Guard registry HA | AMF load evidence | signature algorithms, manifest encoding, revocation transport |
| `MFOS-REQ-UPDATE-*` | `13-update.md` | `TUF-001`, `SLSA-001`, `NIST-218-001`, `NIST-193-001`, `TCG-001`, `EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001`, `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `FBVBS-001` | B/ES/EPXM/HA; TUF-like metadata ES/EPXM/HA; Guard roots HA | update verification evidence | repository protocol, root key ceremony |
| `MFOS-REQ-NUCLEUS-*` | `14-nucleus.md` | `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001`, `EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001`, `X64-INTEL-001`, `X64-AMD-001`, `TCG-001`, `NIST-160-001`, `FBVBS-001` | B/ES/EPXM/HA | nucleus boot and isolation evidence | exact ABI, scheduler policy, platform feature fallback |
| `MFOS-REQ-SVC-*` | `15-svc-pcall.md` | `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001`, `X64-INTEL-001`, `X64-AMD-001`, `FBVBS-001` | B/ES/EPXM/HA | SVC ABI evidence | call table freeze, typed buffer format |
| `MFOS-REQ-PCALL-*` | `15-svc-pcall.md` | `EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001`, `EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001`, `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `FBVBS-001` | B/ES/EPXM/HA | PCALL endpoint evidence | endpoint manifest format, sealed buffer format |
| `MFOS-REQ-PARTITION-*` | `16-pxm.md` | `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `EXTREF-IBM-Z-DPM-0001`, `X64-INTEL-001`, `X64-AMD-001`, `TCG-001`, `NIST-160-001`, `NIST-193-001`, `FBVBS-001` | B optional; E recommended/required by feature; HA required | partition lifecycle evidence | hardware lab coverage, IOMMU backend matrix |
| `MFOS-REQ-GUARD-*` | `17-guard.md` | `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `MS-VBS-001`, `MS-VSM-001`, `X64-INTEL-001`, `X64-AMD-001`, `FBVBS-001` | HA; optional measurement helper in E | Guard root evidence | Guard ABI, attestation format, secret release policy |
| `MFOS-REQ-LGW-*` | `18-linux-gateway.md` | `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001`, `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `EXTREF-IBM-Z-DPM-0001`, `X64-INTEL-001`, `X64-AMD-001`, `NIST-160-001`, `FBVBS-001` | ES/EPXM/HA side partition; Dev exceptions explicit | gateway boundary evidence | identity mapping, channel protocol, clipboard policy |
| `MFOS-REQ-AI-*` | `00-normative-language.md`, `mfos-design.md` | `FBVBS-001`, `NIST-218-001`, `SLSA-001` | B/ES/EPXM/HA | AI output checklist | automated prompt-output lint |
| `MFOS-REQ-QUALITY-*` | `00-normative-language.md`, `mfos-design.md` | `NIST-160-001`, `NIST-218-001`, `SLSA-001`, `SEL4-001`, `FBVBS-001` | B/ES/EPXM/HA; provenance ES/EPXM/HA | quality gate evidence | exact MC/DC target, independent review workflow |

## 5. Requirements by Namespace

### 5.1 Profiles and Source Grounding

Sources: `FBVBS-001`, `NIST-160-001`, IBM source IDs by concept.

Gaps: profile claim automation, source coverage completeness, Source Matrix lint implementation.

| ID | Requirement | Verification | Profiles | Related tests | Evidence |
| --- | --- | --- | --- | --- | --- |
| `MFOS-REQ-PROFILE-0001` | MFOS MUST define conformance as Baseline, Enterprise-Standalone, Enterprise-PXM, or High-Assurance. | documentation review | B/ES/EPXM/HA | `CONF-PROF-0001` | conformance profile review |
| `MFOS-REQ-PROFILE-0002` | Each conformance claim MUST name exactly one minimum profile. | release review | B/ES/EPXM/HA | release text scan | release review record |
| `MFOS-REQ-PROFILE-0003` | Higher-profile features MAY be implemented in lower profiles but MUST NOT imply higher-profile conformance. | release review | B/ES/EPXM/HA | conformance negative review | profile claim matrix |
| `MFOS-REQ-PROFILE-0004` | High-Assurance conformance MUST require PXM Guard. | architecture review | HA | Guard profile review | HA conformance evidence |
| `MFOS-REQ-SOURCE-0001` | z/OS-inspired concepts MUST cite Source Matrix IDs. | source-matrix lint | B/ES/EPXM/HA | `CI-002` | source-matrix lint report |
| `MFOS-REQ-SOURCE-0002` | IBM-derived terms MUST include semantic overlap and MFOS divergence. | architecture review | B/ES/EPXM/HA | source review checklist | concept mapping record |
| `MFOS-REQ-SOURCE-0003` | MFOS MUST NOT claim compatibility with IBM z/OS. | release review | B/ES/EPXM/HA | release text scan | prohibited-wording report |
| `MFOS-REQ-SOURCE-0004` | Source-derived protected-resource operations MUST include authorization, audit, failure modes, and negative tests. | spec review | B/ES/EPXM/HA | traceability lint | spec review record |
| `MFOS-REQ-SOURCE-0005` | Hardware features MUST be described as enforcement aids, not semantic authorization sources. | architecture review | B/ES/EPXM/HA | x64 claim review | hardware mapping review |
| `MFOS-REQ-SOURCE-0006` | PXM and Guard mappings MUST include scope caps. | PXM/Guard review | ES/EPXM/HA | scope negative review | boundary review record |
| `MFOS-REQ-SOURCE-0007` | AI-generated code or tests MUST list implemented requirement IDs and source IDs. | CI lint / review | B/ES/EPXM/HA | `CI-001`, `CI-002` | AI output checklist |
| `MFOS-REQ-SOURCE-0008` | `UNSUPPORTED` and `SPEC_GAP` MUST be distinct. | no-fake-success lint | B/ES/EPXM/HA | `CI-003` | error-model evidence |

### 5.2 Glossary

Sources: IBM source IDs by term, `X64-INTEL-001`, `X64-AMD-001`, `MS-VBS-001`, `MS-VSM-001`.

Gaps: canonical term lint, alias policy, multilingual term policy.

| ID | Requirement | Verification | Profiles | Related tests | Evidence |
| --- | --- | --- | --- | --- | --- |
| `MFOS-REQ-GLOSS-0001` | Every IBM-derived glossary term MUST include Source Matrix IDs. | documentation review | B/ES/EPXM/HA | glossary lint | glossary evidence |
| `MFOS-REQ-GLOSS-0002` | Every IBM-derived glossary term MUST include MFOS divergence. | documentation review | B/ES/EPXM/HA | concept mapping review | glossary evidence |
| `MFOS-REQ-GLOSS-0003` | The glossary MUST define prohibited compatibility wording and replacement wording. | release review | B/ES/EPXM/HA | release text scan | wording evidence |
| `MFOS-REQ-GLOSS-0004` | Protected resource terms MUST be identifiable in the glossary. | spec lint | B/ES/EPXM/HA | glossary resource lint | glossary index |
| `MFOS-REQ-GLOSS-0005` | System interface terms MUST be identifiable in the glossary. | spec lint | B/ES/EPXM/HA | glossary interface lint | glossary index |
| `MFOS-REQ-GLOSS-0006` | New code-facing terms SHOULD use canonical spelling from the glossary. | code review | B/ES/EPXM/HA | naming lint | code review evidence |
| `MFOS-REQ-GLOSS-0007` | PKU, PKS, CET, IOMMU, Secure Boot, Measured Boot, and TPM terms MUST be mechanisms, not semantic roots. | architecture review | B/ES/EPXM/HA | hardware-claim review | glossary review |
| `MFOS-REQ-GLOSS-0008` | Guard terms MUST be scoped to High-Assurance unless explicitly marked as optional Enterprise measurement helpers. | architecture review | ES/EPXM/HA | Guard scope review | glossary review |

### 5.3 System Integrity

Sources: `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001`, `EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001`, `EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001`, `X64-INTEL-001`, `X64-AMD-001`, `X64-LINUX-PKU-001`, `X64-LINUX-CET-001`, `FBVBS-001`.

Gaps: exact system-interface registry, formal model coverage, platform feature fallback matrix.

| ID | Requirement | Verification | Profiles | Related tests | Evidence |
| --- | --- | --- | --- | --- | --- |
| `MFOS-REQ-SYSINT-0001` | Unauthorized subjects MUST NOT bypass security policy, dataset access, audit, authorized state, or system control objects through system interfaces. | negative test / model check | B/ES/EPXM/HA | system-integrity negative suite | integrity proof/evidence |
| `MFOS-REQ-SYSINT-0002` | System interface list MUST be fixed in specification before implementation. | inspection | B/ES/EPXM/HA | spec-id lint | interface registry |
| `MFOS-REQ-SYSINT-0003` | SVC, PCALL, operator command, dataset open, catalog update, job submit, spool operations, AMF load, update activation, PXM_CALL, and GUARD_CALL MUST be system interfaces. | inspection | B/ES/EPXM/HA | interface registry test | system-interface inventory |
| `MFOS-REQ-SYSINT-0004` | Authorized state MUST be modeled as ExecutionState plus AuthorityClass, not as a single privilege bit. | model review | B/ES/EPXM/HA | authority model test | model review record |
| `MFOS-REQ-SYSINT-0005` | Baseline system integrity MUST NOT claim root protection after authorized module or nucleus compromise. | claim review | B/ES/EPXM/HA | release claim scan | integrity claim review |
| `MFOS-REQ-SYSINT-0006` | High-Assurance root protection claims MUST bind to PXM Guard root objects and evidence. | evidence review | HA | Guard evidence review | Guard-root evidence |
| `MFOS-REQ-SYSINT-0007` | Supervisor code MUST NOT directly dereference untrusted user pointers. | code review / fuzz | B/ES/EPXM/HA | pointer negative tests | unsafe review |
| `MFOS-REQ-SYSINT-0008` | copy-in/copy-out MUST use typed buffers and length bounds. | unit / negative test | B/ES/EPXM/HA | copy-bound tests | ABI evidence |
| `MFOS-REQ-SYSINT-0009` | SVC and PCALL routines MUST treat all caller input as untrusted. | zACS-style negative test | B/ES/EPXM/HA | boundary fuzz tests | zACS-style evidence |
| `MFOS-REQ-SYSINT-0010` | Unsupported system interfaces MUST NOT return success. | no-fake-success CI | B/ES/EPXM/HA | `CI-003` | CI report |
| `MFOS-REQ-SYSINT-0011` | Spec-gap behavior MUST NOT be implemented as invented runtime semantics. | spec review / CI | B/ES/EPXM/HA | spec-gap negative tests | spec-gap register |
| `MFOS-REQ-SYSINT-0012` | `securityd` MUST be the final policy decision point for protected resources. | architecture review / integration test | B/ES/EPXM/HA | authorization bypass tests | PDP review |
| `MFOS-REQ-SYSINT-0013` | `auditd` MUST be used for required evidence; debug logs and spool output MUST NOT substitute for audit evidence. | audit test | B/ES/EPXM/HA | audit substitution negative tests | audit evidence |
| `MFOS-REQ-SYSINT-0014` | Dataset handles MUST bind subject, operation, policy version, catalog generation, and expiry. | stale handle test | B/ES/EPXM/HA | stale-handle tests | handle evidence |
| `MFOS-REQ-SYSINT-0015` | Job effective principal MUST be established before any dataset, program, or spool resource is opened. | integration test | B/ES/EPXM/HA | job identity tests | job trace evidence |
| `MFOS-REQ-SYSINT-0016` | Operator commands MUST execute only after parse, target resolution, securityd authorization, required confirmation/dual control, and audit handling. | command negative test | B/ES/EPXM/HA | operator negative suite | command evidence |
| `MFOS-REQ-SYSINT-0017` | AMF load MUST fail closed on invalid signature, invalid manifest, revoked signer/digest, missing authority class, or missing audit obligation. | AMF negative test | B/ES/EPXM/HA | AMF fail-closed tests | AMF evidence |
| `MFOS-REQ-SYSINT-0018` | PXM MUST be limited to partition lifecycle and isolation responsibilities. | architecture review | ES/EPXM/HA | PXM scope review | boundary evidence |
| `MFOS-REQ-SYSINT-0019` | Guard MUST be limited to selected root objects in High-Assurance profile. | architecture review | HA | Guard scope negative tests | Guard boundary evidence |
| `MFOS-REQ-SYSINT-0020` | PKU, PKS, CET, SMEP, SMAP, NX, W^X, IOMMU, VMX, SVM, EPT, and NPT MUST be mechanisms, not substitutes for MFOS authorization semantics. | architecture review | B/ES/EPXM/HA | hardware claim review | x64 mapping evidence |

### 5.4 Object Model

Sources: `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001`, `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `TUF-001`, `FBVBS-001`.

Gaps: concrete serialization, DSN grammar, policy grammar, signature algorithms, Guard claim format, POSIX mapping.

| ID | Requirement | Verification | Profiles | Related tests | Evidence |
| --- | --- | --- | --- | --- | --- |
| `MFOS-REQ-OBJ-0001` | Every protected object MUST have a canonical object type and object ID. | schema test | B/ES/EPXM/HA | `OBJ-POS-001`, schema fuzz | object schema report |
| `MFOS-REQ-OBJ-0002` | Protected object access MUST be represented as subject/object/operation/context. | interface test | B/ES/EPXM/HA | authorization interface tests | object access model |
| `MFOS-REQ-OBJ-0003` | Dataset objects MUST include catalog, security profile, retention, integrity, and generation metadata. | schema test | B/ES/EPXM/HA | dataset schema tests | dataset object evidence |
| `MFOS-REQ-OBJ-0004` | Dataset handles MUST bind subject, operation, policy version, catalog generation, dataset generation, and expiry. | negative test | B/ES/EPXM/HA | `OBJ-NEG-002`, `OBJ-NEG-003` | handle evidence |
| `MFOS-REQ-OBJ-0005` | Job objects MUST include submitter, effective principal, status, steps, spool refs, and audit correlation ID. | schema test | B/ES/EPXM/HA | job schema tests | job object evidence |
| `MFOS-REQ-OBJ-0006` | Spool entries MUST be protected resources with owner, job ID, output class, security profile, and retention policy. | security test | B/ES/EPXM/HA | spool schema/security tests | spool object evidence |
| `MFOS-REQ-OBJ-0007` | Operator commands MUST be typed objects with authority class and audit class. | parser test | B/ES/EPXM/HA | operator parser tests | command object evidence |
| `MFOS-REQ-OBJ-0008` | AMF module objects MUST include manifest digest, artifact digest, signer, authority class, ABI version, and revocation refs. | manifest test | B/ES/EPXM/HA | AMF manifest tests | AMF object evidence |
| `MFOS-REQ-OBJ-0009` | Policy version changes MUST invalidate stale authorization-sensitive handles. | stale handle test | B/ES/EPXM/HA | stale-cache/handle tests | invalidation evidence |
| `MFOS-REQ-OBJ-0010` | Unknown object classes and operation pairs MUST fail with `MFOS_ERR_SPEC_GAP`. | negative test | B/ES/EPXM/HA | `OBJ-NEG-010` | error-model evidence |
| `MFOS-REQ-OBJ-0011` | Specified but unimplemented object operations MUST fail with `MFOS_ERR_UNSUPPORTED`. | no-fake-success test | B/ES/EPXM/HA | `OBJ-NEG-011` | CI evidence |
| `MFOS-REQ-OBJ-0012` | High-Assurance root object claims MUST reference `GuardRoot` evidence. | evidence review | HA | `OBJ-NEG-012` | GuardRoot evidence |

### 5.5 Authorization and securityd

Sources: `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001`, `FBVBS-001`.

Gaps: policy expression grammar, bootstrap policy, external authentication, MFA/dual-control token schemas, cache invalidation protocol, Guard approval token.

| ID | Requirement | Verification | Profiles | Related tests | Evidence |
| --- | --- | --- | --- | --- | --- |
| `MFOS-REQ-AUTH-0001` | `securityd` MUST be the central decision point for protected resource access. | architecture inspection | B/ES/EPXM/HA | PDP bypass tests | authorization architecture evidence |
| `MFOS-REQ-AUTH-0002` | Decision input MUST include subject, object, operation, context, and policy version. | interface test | B/ES/EPXM/HA | `SEC-POS-001`, request schema fuzz | decision schema evidence |
| `MFOS-REQ-AUTH-0003` | Decision result MUST support obligations beyond allow/deny. | interface test | B/ES/EPXM/HA | obligation parser tests | obligation evidence |
| `MFOS-REQ-AUTH-0004` | `datasetd` MUST NOT issue protected dataset handles without an allow decision. | negative test | B/ES/EPXM/HA | `SEC-NEG-002` | dataset authorization evidence |
| `MFOS-REQ-AUTH-0005` | `jobd` MUST obtain authorization before job submit, step execute, program load, and DD resolution. | integration test | B/ES/EPXM/HA | job authorization tests | job auth trace |
| `MFOS-REQ-AUTH-0006` | `operatord` MUST obtain authorization before executing operator commands. | command negative test | B/ES/EPXM/HA | operator auth tests | command auth trace |
| `MFOS-REQ-AUTH-0007` | AMF load MUST pass through `securityd` and `amfd`; High-Assurance load may also require Guard. | AMF negative test | B/ES/EPXM/HA; Guard HA | AMF authorization tests | AMF auth evidence |
| `MFOS-REQ-AUTH-0008` | Policy updates MUST be transactional and increment policy version. | transaction test | B/ES/EPXM/HA | `SEC-POS-005` | policy transaction evidence |
| `MFOS-REQ-AUTH-0009` | Break-glass MUST require reason, expiry, operator identity, authorization, and audit. | emergency drill | B/ES/EPXM/HA | `SEC-NEG-011`, `SEC-NEG-012` | break-glass drill record |
| `MFOS-REQ-AUTH-0010` | Policy rollback MUST require authorization, approval, and audit. | rollback test | B/ES/EPXM/HA | rollback negative tests | rollback evidence |
| `MFOS-REQ-AUTH-0011` | Missing, malformed, unsupported, or undefined policy MUST fail closed. | negative test | B/ES/EPXM/HA | policy fuzz/negative tests | fail-closed evidence |
| `MFOS-REQ-AUTH-0012` | Denied protected-resource decisions MUST not create handles or side effects. | negative test | B/ES/EPXM/HA | `SEC-NEG-001` | deny-side-effect evidence |
| `MFOS-REQ-AUTH-0013` | Required audit obligations MUST be emitted before caller result or effect as specified. | audit integration test | B/ES/EPXM/HA | `SEC-NEG-006` | audit-ordering evidence |
| `MFOS-REQ-AUTH-0014` | Decision caches MUST be invalidated on policy version change. | cache invalidation test | B/ES/EPXM/HA | `SEC-NEG-017` | cache evidence |
| `MFOS-REQ-AUTH-0015` | Caller-supplied identity MUST NOT override trusted scheduler, service, or operator-session identity. | zACS-style negative test | B/ES/EPXM/HA | `SEC-NEG-003` | identity binding evidence |

### 5.6 Audit and auditd

Sources: `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001`, `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `FBVBS-001`.

Gaps: canonical encoding, signature/key hierarchy, remote collector protocol, storage format, redaction language, time-source trust policy, AUD-L5 design.

| ID | Requirement | Verification | Profiles | Related tests | Evidence |
| --- | --- | --- | --- | --- | --- |
| `MFOS-REQ-AUDIT-0001` | Security decisions MUST carry audit obligations. | traceability audit | B/ES/EPXM/HA | audit obligation lint | audit obligation matrix |
| `MFOS-REQ-AUDIT-0002` | Required deny audit MUST be emitted before caller receives final denied result. | negative test | B/ES/EPXM/HA | `AUD-NEG-001` | audit ordering evidence |
| `MFOS-REQ-AUDIT-0003` | Audit record MUST include schema version, record ID, sequence, timestamp, subject, object, operation, decision, reason code, and hashes. | schema test | B/ES/EPXM/HA | `AUD-POS-001`, schema fuzz | audit schema evidence |
| `MFOS-REQ-AUDIT-0004` | Audit log MUST provide a hash chain at AUD-L2 and above. | tamper test | B/ES/EPXM/HA; AUD-L2+ | `AUD-POS-003`, `AUD-NEG-008` | hash-chain evidence |
| `MFOS-REQ-AUDIT-0005` | Audit failure policy MUST be defined per profile. | fault injection | B/ES/EPXM/HA | audit failure injection | failure policy evidence |
| `MFOS-REQ-AUDIT-0006` | Enterprise-Standalone, Enterprise-PXM, and High-Assurance profiles MUST implement remote export capability. | integration test | ES/EPXM/HA | export integration tests | remote export evidence |
| `MFOS-REQ-AUDIT-0007` | High-Assurance profile MUST bind audit root to Guard evidence. | Guard test | HA | `AUD-POS-010`, `AUD-NEG-011` | Guard audit-root evidence |
| `MFOS-REQ-AUDIT-0008` | Spool output MUST NOT be treated as audit evidence. | documentation review | B/ES/EPXM/HA | `AUD-NEG-005` | audit/spool separation review |
| `MFOS-REQ-AUDIT-0009` | Audit query/export MUST be authorized through `securityd`. | security test | B/ES/EPXM/HA | `AUD-NEG-006` | audit query auth evidence |
| `MFOS-REQ-AUDIT-0010` | Redaction MUST affect query/export views only, not committed records. | query test | B/ES/EPXM/HA | redaction view tests | redaction evidence |
| `MFOS-REQ-AUDIT-0011` | Hash chain mismatch MUST be detected during append or recovery. | tamper test | B/ES/EPXM/HA | `AUD-NEG-008`, `AUD-NEG-009` | tamper evidence |
| `MFOS-REQ-AUDIT-0012` | Required audit records MUST be schema-bound and size-bounded. | fuzz/schema test | B/ES/EPXM/HA | `AUD-FUZZ-*` | fuzz report |
| `MFOS-REQ-AUDIT-0013` | Audit stream rollover MUST preserve chain continuity. | rollover test | B/ES/EPXM/HA | rollover tests | rollover evidence |
| `MFOS-REQ-AUDIT-0014` | Recovery MUST not rewrite committed records to hide corruption. | crash recovery test | B/ES/EPXM/HA | recovery corruption tests | recovery evidence |
| `MFOS-REQ-AUDIT-0015` | Guard root transition records MUST include root type, version, digest, and measurement context. | Guard integration test | HA | Guard root audit tests | Guard transition evidence |

### 5.7 Dataset and Catalog

Sources: `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `FBVBS-001`.

Gaps: complete DSN grammar, physical extent format, key service binding, secure deletion backend.

| ID | Requirement | Verification | Profiles | Related tests | Evidence |
| --- | --- | --- | --- | --- | --- |
| `MFOS-REQ-CATALOG-0001` | DSN grammar MUST be specified and parser-tested. | parser/fuzz test | B/ES/EPXM/HA | DSN parser fuzz | DSN grammar evidence |
| `MFOS-REQ-CATALOG-0002` | `catalogd` MUST resolve only committed catalog entries. | transaction test | B/ES/EPXM/HA | catalog transaction tests | catalog commit evidence |
| `MFOS-REQ-CATALOG-0003` | Catalog entries MUST include owner, attributes, location, security profile, generation, and integrity tag. | schema test | B/ES/EPXM/HA | catalog schema tests | catalog schema evidence |
| `MFOS-REQ-CATALOG-0004` | System datasets MUST support immutable flag. | negative test | B/ES/EPXM/HA | immutable update negative tests | immutable evidence |
| `MFOS-REQ-CATALOG-0005` | Catalog transactions MUST be crash recoverable. | crash test | B/ES/EPXM/HA | catalog crash recovery | recovery evidence |
| `MFOS-REQ-CATALOG-0006` | Catalog entry generation MUST increase on committed metadata updates. | unit test | B/ES/EPXM/HA | generation tests | generation evidence |
| `MFOS-REQ-CATALOG-0007` | Catalog update MUST require `securityd` authorization. | integration test | B/ES/EPXM/HA | catalog auth tests | catalog auth evidence |
| `MFOS-REQ-CATALOG-0008` | Catalog corruption detection MUST fail closed for protected datasets. | fault injection | B/ES/EPXM/HA | corruption injection | fail-closed evidence |
| `MFOS-REQ-DATASET-0001` | Dataset handles MUST bind subject, operation, policy version, catalog generation, dataset generation, and expiry. | handle test | B/ES/EPXM/HA | stale handle tests | handle evidence |
| `MFOS-REQ-DATASET-0002` | Unauthorized access MUST NOT create a dataset handle. | negative test | B/ES/EPXM/HA | unauthorized open tests | deny evidence |
| `MFOS-REQ-DATASET-0003` | Retention policy MUST affect delete and purge. | retention test | B/ES/EPXM/HA | retention negative tests | retention evidence |
| `MFOS-REQ-DATASET-0004` | Encryption policy MUST be linked to configured key service profile. | integration test | ES/EPXM/HA required; B optional | key service tests | encryption-policy evidence |
| `MFOS-REQ-DATASET-0005` | Dataset MUST NOT be defined as a POSIX file wrapper. | architecture review | B/ES/EPXM/HA | dataset/POSIX review | architecture evidence |
| `MFOS-REQ-DATASET-0006` | Dataset open DENY MUST be audited before caller receives denial. | ordering test | B/ES/EPXM/HA | deny ordering tests | audit ordering evidence |
| `MFOS-REQ-DATASET-0007` | Dataset integrity tag mismatch MUST fail closed. | fault injection | B/ES/EPXM/HA | integrity mismatch tests | integrity evidence |
| `MFOS-REQ-DATASET-0008` | Secure deletion MUST produce an audit record or return a fail-closed error. | security test | B/ES/EPXM/HA | secure deletion tests | deletion evidence |

### 5.8 Job and Spool

Sources: `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-JES-JOB-FLOW-0001`, `EXTREF-IBM-ZOS-JES2-LIBRARY-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `FBVBS-001`.

Gaps: JCL-like subset grammar, restart metadata, spool quota and retention details.

| ID | Requirement | Verification | Profiles | Related tests | Evidence |
| --- | --- | --- | --- | --- | --- |
| `MFOS-REQ-JOB-0001` | Job lifecycle MUST include input, conversion, queueing, execution, output, and purge phases. | state-machine test | B/ES/EPXM/HA | job lifecycle tests | state-machine evidence |
| `MFOS-REQ-JOB-0002` | JCL-like parser MUST be fuzzed. | fuzz campaign | B/ES/EPXM/HA | JCL parser fuzz | fuzz evidence |
| `MFOS-REQ-JOB-0003` | Job effective principal MUST be established before dataset, program, or spool open. | integration test | B/ES/EPXM/HA | job identity tests | identity evidence |
| `MFOS-REQ-JOB-0004` | DD resolution MUST pass through `catalogd`, `datasetd`, and `securityd` as applicable. | integration test | B/ES/EPXM/HA | DD resolution tests | resolution evidence |
| `MFOS-REQ-JOB-0005` | Step failure MUST include return code or abend-like reason. | unit test | B/ES/EPXM/HA | step failure tests | step evidence |
| `MFOS-REQ-JOB-0006` | Job submit MUST require `securityd` authorization. | negative test | B/ES/EPXM/HA | unauthorized submit tests | submit auth evidence |
| `MFOS-REQ-JOB-0007` | Job conversion failure MUST NOT enqueue executable work. | parser test | B/ES/EPXM/HA | conversion failure tests | queue evidence |
| `MFOS-REQ-JOB-0008` | Job cancellation MUST close or revoke protected resource handles. | integration test | B/ES/EPXM/HA | cancel cleanup tests | cancellation evidence |
| `MFOS-REQ-JOB-0009` | Job accounting record MUST include submit, start, complete, CPU, IO, and result fields when available. | schema test | B/ES/EPXM/HA | accounting schema tests | accounting evidence |
| `MFOS-REQ-SPOOL-0001` | Spool entry MUST be a protected resource. | security test | B/ES/EPXM/HA | spool resource tests | spool security evidence |
| `MFOS-REQ-SPOOL-0002` | Spool browse, purge, and export MUST require `securityd` decisions. | negative test | B/ES/EPXM/HA | spool unauthorized tests | spool auth evidence |
| `MFOS-REQ-SPOOL-0003` | SYSOUT MUST include owner, job ID, output class, and security profile. | schema test | B/ES/EPXM/HA | SYSOUT schema tests | SYSOUT evidence |
| `MFOS-REQ-SPOOL-0004` | Spool retention MUST affect purge. | retention test | B/ES/EPXM/HA | purge retention tests | retention evidence |
| `MFOS-REQ-SPOOL-0005` | Spool DENY MUST be audited before returning denial. | ordering test | B/ES/EPXM/HA | deny ordering tests | audit ordering evidence |
| `MFOS-REQ-SPOOL-0006` | SYSOUT capture failure MUST fail the step or mark output incomplete according to explicit policy. | fault injection | B/ES/EPXM/HA | SYSOUT fault tests | output failure evidence |

### 5.9 Operator Console and workload policy

Sources: `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001`, `FBVBS-001`.

Gaps: full command grammar, automation API, advanced workload policy goals, overload policy details.

| ID | Requirement | Verification | Profiles | Related tests | Evidence |
| --- | --- | --- | --- | --- | --- |
| `MFOS-REQ-OPER-0001` | First interactive UI after boot MUST be operator console, not root shell. | boot test | B/ES/EPXM/HA | console boot tests | boot evidence |
| `MFOS-REQ-OPER-0002` | Operator command grammar MUST be specified and parser-tested. | parser/fuzz test | B/ES/EPXM/HA | command parser fuzz | grammar evidence |
| `MFOS-REQ-OPER-0003` | Operator commands MUST have authority classes. | schema review | B/ES/EPXM/HA | command schema tests | authority evidence |
| `MFOS-REQ-OPER-0004` | Destructive commands MUST be able to require confirmation or dual control. | operator drill | B/ES/EPXM/HA | destructive command drill | drill evidence |
| `MFOS-REQ-OPER-0005` | Operator commands MUST generate audit records. | audit test | B/ES/EPXM/HA | operator audit tests | command audit evidence |
| `MFOS-REQ-OPER-0006` | Automation hooks MUST NOT bypass operator authority or audit. | negative test | B/ES/EPXM/HA | automation bypass tests | automation evidence |
| `MFOS-REQ-OPER-0007` | Command DENY MUST be audited before display. | ordering test | B/ES/EPXM/HA | command deny ordering tests | audit ordering evidence |
| `MFOS-REQ-OPER-0008` | Emergency mode MUST require reason, identity, expiry, and audit. | emergency drill | B/ES/EPXM/HA | emergency drill | emergency evidence |
| `MFOS-REQ-OPER-0009` | Raw command text MUST NOT be directly executed. | code review / test | B/ES/EPXM/HA | raw command negative tests | parser boundary evidence |
| `MFOS-REQ-OPER-0010` | Unsupported commands MUST fail closed, not silently succeed. | no-fake-success CI | B/ES/EPXM/HA | unsupported command tests | CI evidence |
| `MFOS-REQ-WPOL-0001` | `workpolicyd` MUST support job classes. | unit test | B/ES/EPXM/HA | workload policy unit tests | job class evidence |
| `MFOS-REQ-WPOL-0002` | `workpolicyd` MUST support priority and max concurrency per job class. | queue test | B/ES/EPXM/HA | queue tests | queue evidence |
| `MFOS-REQ-WPOL-0003` | `workpolicyd` MUST return typed dispatch hints to `jobd`. | interface test | B/ES/EPXM/HA | dispatch interface tests | dispatch evidence |
| `MFOS-REQ-WPOL-0004` | `workpolicyd` MUST support service class identifiers in policy and decisions. | schema test | B/ES/EPXM/HA | service class schema tests | policy evidence |
| `MFOS-REQ-WPOL-0005` | `workpolicyd` MUST support report class labels for accounting. | audit test | B/ES/EPXM/HA | report class audit tests | accounting evidence |
| `MFOS-REQ-WPOL-0006` | workload policy activation MUST require `securityd` authorization. | negative test | B/ES/EPXM/HA | workload policy auth tests | activation evidence |
| `MFOS-REQ-WPOL-0007` | workload policy activation MUST be audited before success is returned. | ordering test | B/ES/EPXM/HA | activation audit tests | audit evidence |
| `MFOS-REQ-WPOL-0008` | Unknown job class MUST fail closed or map only through explicit default policy. | negative test | B/ES/EPXM/HA | unknown class tests | fail-closed evidence |
| `MFOS-REQ-WPOL-0009` | Overload behavior MUST be explicit: hold, defer, reject, or run low priority. | policy test | B/ES/EPXM/HA | overload policy tests | overload evidence |
| `MFOS-REQ-WPOL-0010` | MFOS MUST NOT claim IBM z/OS workload policy velocity or response-time compatibility. | documentation review | B/ES/EPXM/HA | release text scan | claim review evidence |
| `MFOS-REQ-WPOL-0011` | Active policy version MUST be included in every workload policy decision. | interface test | B/ES/EPXM/HA | policy version tests | decision evidence |
| `MFOS-REQ-WPOL-0012` | `jobd` MUST not reinterpret workload policy beyond typed dispatch hints. | architecture review | B/ES/EPXM/HA | jobd/WLM boundary tests | boundary evidence |

### 5.10 AMF

Sources: `EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `X64-INTEL-001`, `X64-AMD-001`, `MS-VBS-001`, `MS-VSM-001`, `TUF-001`, `SLSA-001`, `NIST-218-001`, `FBVBS-001`.

Gaps: manifest canonical encoding, signature algorithms, revocation distribution, executable mapping API, AMF registry persistence.

| ID | Requirement | Verification | Profiles | Related tests | Evidence |
| --- | --- | --- | --- | --- | --- |
| `MFOS-REQ-AMF-0001` | AMF module artifacts MUST be signed. | signature test | B/ES/EPXM/HA | signature tests | signature evidence |
| `MFOS-REQ-AMF-0002` | AMF modules MAY load only from immutable system datasets or approved artifact-store entries. | negative test | B/ES/EPXM/HA | mutable source negative tests | load-source evidence |
| `MFOS-REQ-AMF-0003` | AMF modules MUST declare an explicit authority class. | manifest test | B/ES/EPXM/HA | manifest tests | authority evidence |
| `MFOS-REQ-AMF-0004` | AMF load MUST produce an audit record. | audit test | B/ES/EPXM/HA | AMF audit tests | audit evidence |
| `MFOS-REQ-AMF-0005` | Revoked signer, revoked digest, or stale security epoch MUST fail closed. | revocation test | B/ES/EPXM/HA | revocation tests | revocation evidence |
| `MFOS-REQ-AMF-0006` | High-Assurance AMF registry MUST be Guard-sealed. | Guard test | HA | Guard registry tests | Guard evidence |
| `MFOS-REQ-AMF-0007` | AMF modules MUST NOT have authority to disable audit. | architecture review | B/ES/EPXM/HA | authority negative tests | AMF authority review |
| `MFOS-REQ-AMF-0008` | AMF ABI MUST NOT accept arbitrary pointers. | ABI review/fuzz | B/ES/EPXM/HA | ABI fuzz tests | ABI evidence |
| `MFOS-REQ-AMF-0009` | AMF manifest MUST declare Source Matrix references for authorized-state concepts. | source-matrix lint | B/ES/EPXM/HA | manifest lint | source evidence |
| `MFOS-REQ-AMF-0010` | AMF load MUST call `securityd` before executable mapping. | integration test | B/ES/EPXM/HA | mapping auth tests | auth evidence |
| `MFOS-REQ-AMF-0011` | AMF load MUST call `auditd` before reporting READY. | integration test | B/ES/EPXM/HA | READY ordering tests | audit ordering evidence |
| `MFOS-REQ-AMF-0012` | AMF load MUST call PXM Guard before executable mapping when profile is High-Assurance or manifest requires Guard. | Guard negative test | HA; manifest-required | Guard approval tests | Guard approval evidence |
| `MFOS-REQ-AMF-0013` | AMF module executable mappings MUST be RX only after signature, digest, manifest, policy, and revocation checks pass. | memory mapping test | B/ES/EPXM/HA | mapping order tests | mapping evidence |
| `MFOS-REQ-AMF-0014` | AMF module pages MUST never be writable and executable at the same time. | W^X test | B/ES/EPXM/HA | W^X negative tests | memory safety evidence |
| `MFOS-REQ-AMF-0015` | AMF registry entries MUST bind module digest, manifest digest, authority class, policy version, catalog generation, and security epoch. | registry schema test | B/ES/EPXM/HA | registry tests | registry evidence |
| `MFOS-REQ-AMF-0016` | AMF registry update MUST be transactional. | crash test | B/ES/EPXM/HA | registry crash tests | transaction evidence |
| `MFOS-REQ-AMF-0017` | AMF load MUST reject missing or malformed Source Matrix IDs. | lint negative test | B/ES/EPXM/HA | source-id negative tests | lint evidence |
| `MFOS-REQ-AMF-0018` | AMF module cannot register SVC or PCALL endpoint outside declared authority class. | negative test | B/ES/EPXM/HA | endpoint authority tests | endpoint evidence |
| `MFOS-REQ-AMF-0019` | AMF module compromise MUST NOT be claimed as contained by Baseline system integrity. | claim review | B/ES/EPXM/HA | release claim scan | claim evidence |
| `MFOS-REQ-AMF-0020` | AMF failure paths MUST return typed failure and MUST NOT return fake success. | no-fake-success CI | B/ES/EPXM/HA | AMF failure tests | CI evidence |

### 5.11 Update Verification Service

Sources: `TUF-001`, `SLSA-001`, `NIST-218-001`, `NIST-193-001`, `TCG-001`, `EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001`, `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `FBVBS-001`.

Gaps: exact repository protocol, key ceremony, target delegation policy, recovery image trust, transport profile.

| ID | Requirement | Verification | Profiles | Related tests | Evidence |
| --- | --- | --- | --- | --- | --- |
| `MFOS-REQ-UPDATE-0001` | UVS MUST verify update metadata before artifact trust. | metadata test | B/ES/EPXM/HA; TUF-like ES/EPXM/HA | metadata tests | metadata evidence |
| `MFOS-REQ-UPDATE-0002` | UVS MUST verify artifact signature, hash, and size. | artifact test | B/ES/EPXM/HA | artifact tests | artifact evidence |
| `MFOS-REQ-UPDATE-0003` | UVS MUST verify generation and security epoch. | rollback test | B/ES/EPXM/HA | epoch tests | rollback evidence |
| `MFOS-REQ-UPDATE-0004` | UVS MUST reject rollback attempts. | negative test | B/ES/EPXM/HA | rollback negative tests | rollback evidence |
| `MFOS-REQ-UPDATE-0005` | UVS MUST reject freeze attacks using timestamp expiry or freshness policy. | freeze test | ES/EPXM/HA required; B optional | freeze tests | freshness evidence |
| `MFOS-REQ-UPDATE-0006` | UVS MUST reject mix-and-match metadata views. | consistency test | ES/EPXM/HA required; B optional | consistency tests | snapshot evidence |
| `MFOS-REQ-UPDATE-0007` | UVS MUST reject revoked targets, keys, signers, and security epochs. | revocation test | B/ES/EPXM/HA | revocation tests | revocation evidence |
| `MFOS-REQ-UPDATE-0008` | UVS MUST check dependencies and conflicts before staging. | dependency test | B/ES/EPXM/HA | dependency tests | dependency evidence |
| `MFOS-REQ-UPDATE-0009` | UVS MUST stage verified artifacts before activation. | integration test | B/ES/EPXM/HA | staging tests | staging evidence |
| `MFOS-REQ-UPDATE-0010` | UVS MUST bind staged update state to bundle ID, generation, security epoch, target digests, and policy version. | state test | B/ES/EPXM/HA | state binding tests | state evidence |
| `MFOS-REQ-UPDATE-0011` | UVS MUST require `securityd` authorization before staging security-sensitive updates. | integration test | B/ES/EPXM/HA | update auth tests | authorization evidence |
| `MFOS-REQ-UPDATE-0012` | UVS MUST require audit records for verify, stage, activate, commit, rollback, and failure events. | audit test | B/ES/EPXM/HA | update audit tests | audit evidence |
| `MFOS-REQ-UPDATE-0013` | High-Assurance update roots and activation profile transitions MUST be Guard-approved and Guard-sealed. | Guard test | HA | Guard update tests | Guard evidence |
| `MFOS-REQ-UPDATE-0014` | UVS MUST NOT trust transport security as artifact integrity. | architecture review | B/ES/EPXM/HA | transport bypass tests | architecture evidence |
| `MFOS-REQ-UPDATE-0015` | UVS MUST NOT activate unsigned artifacts. | negative test | B/ES/EPXM/HA | unsigned artifact tests | signature evidence |
| `MFOS-REQ-UPDATE-0016` | UVS MUST distinguish unsupported component types from spec gaps. | error test | B/ES/EPXM/HA | error model tests | error evidence |
| `MFOS-REQ-UPDATE-0017` | UVS MUST provide a recovery rollback workflow for failed activation. | recovery drill | B/ES/EPXM/HA | recovery drill | recovery evidence |
| `MFOS-REQ-UPDATE-0018` | UVS MUST produce evidence suitable for production readiness gates. | evidence review | B/ES/EPXM/HA | production gate review | readiness evidence |
| `MFOS-REQ-UPDATE-0019` | UVS MUST reject activation when measured component digests do not match verified manifests. | measurement test | ES/EPXM/HA required; B optional | measurement tests | measurement evidence |
| `MFOS-REQ-UPDATE-0020` | UVS MUST fail closed for security-critical update ambiguity. | no-fake-success CI | B/ES/EPXM/HA | ambiguity negative tests | CI evidence |

### 5.12 Nucleus, SVC, and PCALL

Sources: `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001`, `EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001`, `EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001`, `X64-INTEL-001`, `X64-AMD-001`, `TCG-001`, `NIST-160-001`, `FBVBS-001`.

Gaps: exact ABI encoding, call table freeze, scheduler policy, typed buffer format, endpoint manifest format.

| ID | Requirement | Verification | Profiles | Related tests | Evidence |
| --- | --- | --- | --- | --- | --- |
| `MFOS-REQ-NUCLEUS-0001` | Nucleus MUST implement boot handoff validation. | boot test | B/ES/EPXM/HA | boot tests | boot evidence |
| `MFOS-REQ-NUCLEUS-0002` | Nucleus MUST maintain address spaces with user/supervisor separation. | isolation test | B/ES/EPXM/HA | isolation tests | isolation evidence |
| `MFOS-REQ-NUCLEUS-0003` | Nucleus MUST implement SVC entry and dispatch validation. | ABI test | B/ES/EPXM/HA | SVC ABI tests | ABI evidence |
| `MFOS-REQ-NUCLEUS-0004` | Nucleus MUST implement typed object handles. | handle test | B/ES/EPXM/HA | handle tests | handle evidence |
| `MFOS-REQ-NUCLEUS-0005` | Nucleus MUST implement IPC primitive with bounded payloads. | IPC test | B/ES/EPXM/HA | IPC tests | IPC evidence |
| `MFOS-REQ-NUCLEUS-0006` | Nucleus MUST implement baseline scheduler sufficient for services and jobs. | scheduler test | B/ES/EPXM/HA | scheduler tests | scheduler evidence |
| `MFOS-REQ-NUCLEUS-0007` | Nucleus MUST manage page tables and mapping rights. | mapping test | B/ES/EPXM/HA | mapping tests | page-table evidence |
| `MFOS-REQ-NUCLEUS-0008` | Nucleus MUST enforce NX and W^X. | W^X test | B/ES/EPXM/HA | W^X negative tests | mapping evidence |
| `MFOS-REQ-NUCLEUS-0009` | Nucleus MUST use copy-in/copy-out for untrusted buffers. | negative test | B/ES/EPXM/HA | copy-in/out tests | buffer evidence |
| `MFOS-REQ-NUCLEUS-0010` | Nucleus MUST implement service lifecycle supervision. | integration test | B/ES/EPXM/HA | service lifecycle tests | service evidence |
| `MFOS-REQ-NUCLEUS-0011` | Nucleus MUST contain service faults and produce fault records. | fault injection | B/ES/EPXM/HA | fault tests | fault evidence |
| `MFOS-REQ-NUCLEUS-0012` | Nucleus MUST expose kernel audit hooks without replacing `auditd`. | audit test | B/ES/EPXM/HA | audit hook tests | audit evidence |
| `MFOS-REQ-NUCLEUS-0013` | Nucleus MUST trigger crash dump on unrecoverable internal corruption. | crash test | B/ES/EPXM/HA | crash tests | crash evidence |
| `MFOS-REQ-NUCLEUS-0014` | Nucleus MUST expose partition-aware APIs even in implicit single partition mode. | API test | B/ES/EPXM/HA | partition API tests | API evidence |
| `MFOS-REQ-NUCLEUS-0015` | Nucleus MUST NOT decide final protected-resource authorization. | architecture review | B/ES/EPXM/HA | PDP bypass tests | boundary evidence |
| `MFOS-REQ-NUCLEUS-0016` | Nucleus MUST return `MFOS_ERR_UNSUPPORTED` for specified but unimplemented SVCs. | no-fake-success CI | B/ES/EPXM/HA | unsupported SVC tests | CI evidence |
| `MFOS-REQ-NUCLEUS-0017` | Nucleus MUST return `MFOS_ERR_SPEC_GAP` for undefined SVCs or ABIs. | no-fake-success CI | B/ES/EPXM/HA | spec-gap SVC tests | CI evidence |
| `MFOS-REQ-NUCLEUS-0018` | Nucleus MUST reject stale, wrong-type, wrong-generation, or rights-insufficient handles. | negative test | B/ES/EPXM/HA | handle negative tests | handle evidence |
| `MFOS-REQ-NUCLEUS-0019` | Nucleus MUST NOT treat PKU/PKS as primary system-integrity boundary. | design review | B/ES/EPXM/HA | hardware claim review | x64 mapping evidence |
| `MFOS-REQ-NUCLEUS-0020` | Nucleus MUST NOT map writable executable pages. | mapping negative test | B/ES/EPXM/HA | W^X tests | memory mapping evidence |
| `MFOS-REQ-SVC-0001` | SVC ABI MUST be versioned. | ABI test | B/ES/EPXM/HA | SVC ABI tests | ABI evidence |
| `MFOS-REQ-SVC-0002` | SVC caller identity MUST be derived from nucleus context. | negative test | B/ES/EPXM/HA | identity spoof tests | identity evidence |
| `MFOS-REQ-SVC-0003` | SVC MUST validate call ID, category, flags, lengths, handles, and reserved fields before dispatch. | ABI test | B/ES/EPXM/HA | ABI validation tests | validation evidence |
| `MFOS-REQ-SVC-0004` | SVC MUST use bounded copy-in/copy-out for user buffers. | negative test | B/ES/EPXM/HA | buffer tests | buffer evidence |
| `MFOS-REQ-SVC-0005` | SVC MUST distinguish unsupported specified calls from spec gaps. | error test | B/ES/EPXM/HA | error model tests | error evidence |
| `MFOS-REQ-SVC-0006` | SVC MUST NOT return success when a required downstream service fails. | no-fake-success CI | B/ES/EPXM/HA | downstream failure tests | CI evidence |
| `MFOS-REQ-SVC-0007` | SVC gateway calls MUST NOT implement final protected-resource authorization in the nucleus. | architecture review | B/ES/EPXM/HA | PDP bypass tests | boundary evidence |
| `MFOS-REQ-SVC-0008` | SVC MUST propagate audit obligations. | audit test | B/ES/EPXM/HA | audit propagation tests | audit evidence |
| `MFOS-REQ-SVC-0009` | SVC MUST reject stale, wrong-type, or rights-insufficient handles. | negative test | B/ES/EPXM/HA | handle tests | handle evidence |
| `MFOS-REQ-SVC-0010` | SVC MUST zero or reject reserved fields according to ABI rules. | fuzz test | B/ES/EPXM/HA | reserved-field fuzz | fuzz evidence |
| `MFOS-REQ-PCALL-0001` | PCALL ABI MUST be versioned. | ABI test | B/ES/EPXM/HA | PCALL ABI tests | ABI evidence |
| `MFOS-REQ-PCALL-0002` | PCALL endpoints MUST be declared in endpoint manifests. | manifest test | B/ES/EPXM/HA | endpoint manifest tests | manifest evidence |
| `MFOS-REQ-PCALL-0003` | PCALL MUST use typed endpoints and typed request/response schemas. | interface test | B/ES/EPXM/HA | PCALL interface tests | schema evidence |
| `MFOS-REQ-PCALL-0004` | PCALL MUST NOT allow arbitrary cross-address-space pointer access. | negative test | B/ES/EPXM/HA | pointer negative tests | boundary evidence |
| `MFOS-REQ-PCALL-0005` | PCALL caller identity MUST be derived from trusted context. | negative test | B/ES/EPXM/HA | identity spoof tests | identity evidence |
| `MFOS-REQ-PCALL-0006` | PCALL MUST call `securityd` when endpoint manifest requires authorization. | integration test | B/ES/EPXM/HA | PCALL auth tests | authorization evidence |
| `MFOS-REQ-PCALL-0007` | PCALL MUST propagate audit obligations and record endpoint failures. | audit test | B/ES/EPXM/HA | audit propagation tests | audit evidence |
| `MFOS-REQ-PCALL-0008` | PCALL MUST reject sealed buffer overflow, direction mismatch, and stale generation. | negative test | B/ES/EPXM/HA | sealed buffer tests | buffer evidence |
| `MFOS-REQ-PCALL-0009` | PCALL endpoint failure MUST return typed error and not fake success. | no-fake-success CI | B/ES/EPXM/HA | endpoint failure tests | CI evidence |
| `MFOS-REQ-PCALL-0010` | PCALL endpoint registration by AMF module MUST be constrained by AMF authority class. | AMF integration test | B/ES/EPXM/HA | AMF endpoint tests | authority evidence |

### 5.13 PXM and Guard

Sources: `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `EXTREF-IBM-Z-DPM-0001`, `X64-INTEL-001`, `X64-AMD-001`, `TCG-001`, `NIST-160-001`, `NIST-193-001`, `MS-VBS-001`, `MS-VSM-001`, `FBVBS-001`.

Gaps: hardware lab backend, IOMMU/interrupt-remap matrix, Guard ABI, attestation claim format, secret release policy.

| ID | Requirement | Verification | Profiles | Related tests | Evidence |
| --- | --- | --- | --- | --- | --- |
| `MFOS-REQ-PARTITION-0001` | MFOS MUST expose partition-aware APIs even under implicit single-partition backend. | API test | B/ES/EPXM/HA | partition API tests | API evidence |
| `MFOS-REQ-PARTITION-0002` | Implicit backend MUST represent running MFOS as one partition and return `UNSUPPORTED` for unavailable multi-partition operations. | boot test | B/ES/EPXM/HA | implicit backend tests | boot evidence |
| `MFOS-REQ-PARTITION-0003` | PXM Core MUST be limited to partition lifecycle and isolation. | architecture review | EPXM/HA; B/ES implicit API only | PXM scope review | boundary evidence |
| `MFOS-REQ-PARTITION-0004` | PXM MUST NOT interpret dataset, job, spool, catalog, security profile, or workload policy semantics. | architecture review | EPXM/HA | semantics boundary tests | boundary evidence |
| `MFOS-REQ-PARTITION-0005` | PXM device assignment MUST require IOMMU domain setup and interrupt remapping in Enterprise-PXM and High-Assurance profiles; Enterprise-Standalone MUST NOT claim cross-partition device assignment. | device test | EPXM/HA | device assignment tests | IOMMU evidence |
| `MFOS-REQ-PARTITION-0006` | PXM MUST deny device reassignment until teardown checklist completion is recorded. | negative test | EPXM/HA | teardown negative tests | teardown evidence |
| `MFOS-REQ-PARTITION-0007` | PXM MUST zero destroyed or released partition memory before reassignment. | memory reuse test | EPXM/HA | memory reuse tests | zeroing evidence |
| `MFOS-REQ-PARTITION-0008` | PXM partition operations MUST generate audit records. | audit test | EPXM/HA | partition audit tests | audit evidence |
| `MFOS-REQ-PARTITION-0009` | Activation profile parsing MUST fail closed on unknown required fields, invalid ranges, or forbidden device combinations. | parser negative test | EPXM/HA | activation profile fuzz | parser evidence |
| `MFOS-REQ-PARTITION-0010` | Partition state transitions MUST follow the legal transition table. | state-machine test | EPXM/HA | PXM state tests | state-machine evidence |
| `MFOS-REQ-PARTITION-0011` | PXM calls MUST reject caller-supplied partition state claims and use authoritative PXM state. | privilege confusion test | EPXM/HA | state spoof tests | authority evidence |
| `MFOS-REQ-PARTITION-0012` | PXM calls MUST include caller identity, sequence number, correlation ID, and command version. | ABI test | EPXM/HA | PXM ABI tests | ABI evidence |
| `MFOS-REQ-PARTITION-0013` | PXM MUST distinguish `UNSUPPORTED` from `SPEC_GAP`. | error model test | EPXM/HA | PXM error tests | error evidence |
| `MFOS-REQ-PARTITION-0014` | PXM MUST record image and activation profile measurements before activation in Enterprise-PXM and High-Assurance profiles. | measurement test | EPXM/HA | measurement tests | measurement evidence |
| `MFOS-REQ-PARTITION-0015` | PXM MUST coordinate with recovery partition policy before RECOVER transitions. | recovery drill | EPXM/HA | recovery drill | recovery evidence |
| `MFOS-REQ-PARTITION-0016` | PXM MUST fail closed when required IOMMU or interrupt-remapping features are absent for passthrough device assignment. | platform negative test | EPXM/HA | platform feature tests | platform evidence |
| `MFOS-REQ-PARTITION-0017` | PXM MUST revoke CPU mappings, IOMMU mappings, interrupt routes, and device ownership before memory is zeroed and reused. | teardown test | EPXM/HA | teardown tests | teardown evidence |
| `MFOS-REQ-PARTITION-0018` | PXM MUST expose all partition state changes to `auditd` or equivalent boot-time audit sink. | audit integration test | EPXM/HA | partition audit tests | audit evidence |
| `MFOS-REQ-PARTITION-0019` | High-Assurance PXM MUST call Guard for Guard-required root-object transitions. | Guard integration test | HA | Guard integration tests | Guard evidence |
| `MFOS-REQ-PARTITION-0020` | PXM MUST NOT present successful partition operation if required audit obligation cannot be satisfied under active profile. | audit failure test | ES/EPXM/HA | audit failure tests | fail-closed evidence |
| `MFOS-REQ-GUARD-0001` | Guard MUST be required only for High-Assurance conformance. | profile review | HA | Guard profile tests | profile evidence |
| `MFOS-REQ-GUARD-0002` | Guard scope MUST be limited to root objects listed in the Guard spec. | architecture review | HA | scope negative tests | scope evidence |
| `MFOS-REQ-GUARD-0003` | Guard MUST NOT interpret dataset, job, spool, catalog, or workload policy semantics. | architecture review | HA | semantics negative tests | boundary evidence |
| `MFOS-REQ-GUARD-0004` | Security policy root transitions MUST be recorded by both Guard and `auditd`. | integration test | HA | root transition tests | transition evidence |
| `MFOS-REQ-GUARD-0005` | Executable mappings MUST NOT violate Guard executable mapping policy. | negative test | HA | executable mapping tests | mapping evidence |
| `MFOS-REQ-GUARD-0006` | SVC table mismatch MUST trigger lockdown or panic-equivalent failure policy. | fault injection | HA | SVC mismatch tests | lockdown evidence |
| `MFOS-REQ-GUARD-0007` | AMF registry mismatch MUST deny AMF load and generate audit alert. | negative test | HA | AMF registry tests | alert evidence |
| `MFOS-REQ-GUARD-0008` | Guard unavailable boot behavior MUST be defined per profile. | boot test | HA | Guard boot tests | boot evidence |
| `MFOS-REQ-GUARD-0009` | Guard calls MUST use typed bounded payloads and reject reserved nonzero fields. | ABI test | HA | Guard ABI fuzz | ABI evidence |
| `MFOS-REQ-GUARD-0010` | Guard MUST bind root versions to security epoch and policy version. | rollback test | HA | root version tests | root evidence |
| `MFOS-REQ-GUARD-0011` | Guard MUST reject rollback to older root version unless approved recovery policy allows it. | rollback negative test | HA | rollback tests | rollback evidence |
| `MFOS-REQ-GUARD-0012` | Guard MUST reject root transition requests with stale measurement context. | replay negative test | HA | stale measurement tests | replay evidence |
| `MFOS-REQ-GUARD-0013` | Guard MUST authorize High-Assurance AMF loads before executable mapping. | AMF integration test | HA | AMF Guard tests | AMF Guard evidence |
| `MFOS-REQ-GUARD-0014` | Guard MUST append audit root updates monotonically by record sequence. | audit chain test | HA | audit-root tests | audit root evidence |
| `MFOS-REQ-GUARD-0015` | Guard MUST distinguish `UNSUPPORTED` from `SPEC_GAP`. | error model test | HA | Guard error tests | error evidence |
| `MFOS-REQ-GUARD-0016` | Guard MUST NOT return success if required audit evidence cannot be recorded. | audit failure test | HA | audit failure tests | fail-closed evidence |
| `MFOS-REQ-GUARD-0017` | Guard MUST provide attestation over selected claims and caller-provided nonce. | attestation test | HA | attestation tests | attestation evidence |
| `MFOS-REQ-GUARD-0018` | Guard secret release MUST be bound to measurement context and root state. | secret release test | HA | secret release tests | secret evidence |
| `MFOS-REQ-GUARD-0019` | Guard emergency mode entry MUST require reason, operator identity, expiry, and audit. | emergency drill | HA | emergency tests | emergency evidence |
| `MFOS-REQ-GUARD-0020` | Guard emergency mode exit MUST audit the exit and reverify affected roots. | emergency drill | HA | emergency exit tests | emergency evidence |

### 5.14 Linux/Desktop Gateway

Sources: `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001`, `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `EXTREF-IBM-Z-DPM-0001`, `X64-INTEL-001`, `X64-AMD-001`, `NIST-160-001`, `FBVBS-001`.

Gaps: identity mapping, channel protocol, token signature, clipboard policy, desktop-side attestation.

| ID | Requirement | Verification | Profiles | Related tests | Evidence |
| --- | --- | --- | --- | --- | --- |
| `MFOS-REQ-LGW-0001` | Linux/Desktop integration MUST use a side partition or explicitly marked non-production development mode. | architecture review | ES/EPXM/HA; Dev exception | gateway architecture review | side-partition evidence |
| `MFOS-REQ-LGW-0002` | Gateway MUST NOT mount MFOS datasets directly in Linux/Desktop. | negative test | ES/EPXM/HA | direct mount negative tests | boundary evidence |
| `MFOS-REQ-LGW-0003` | Every protected resource gateway operation MUST call `securityd` before target service access. | integration test | ES/EPXM/HA | gateway auth tests | auth evidence |
| `MFOS-REQ-LGW-0004` | Every gateway operation with a security decision MUST create audit evidence. | audit test | ES/EPXM/HA | gateway audit tests | audit evidence |
| `MFOS-REQ-LGW-0005` | DENY decisions MUST be audited before final result returns when audit is available. | negative test | ES/EPXM/HA | deny ordering tests | ordering evidence |
| `MFOS-REQ-LGW-0006` | Gateway requests MUST include subject, operation, object when applicable, policy version, channel ID, payload hash, and correlation ID. | ABI test | ES/EPXM/HA | gateway ABI tests | ABI evidence |
| `MFOS-REQ-LGW-0007` | Gateway tokens MUST bind subject, object, operation, policy version, channel ID, expiry, and audit obligation. | token test | ES/EPXM/HA | token binding tests | token evidence |
| `MFOS-REQ-LGW-0008` | Gateway tokens MUST be rejected outside the endpoint that issued them. | negative test | ES/EPXM/HA | token replay tests | token evidence |
| `MFOS-REQ-LGW-0009` | Linux root MUST NOT map automatically to MFOS operator authority. | privilege confusion test | ES/EPXM/HA | root confusion tests | identity evidence |
| `MFOS-REQ-LGW-0010` | Gateway payloads MUST be bounded by endpoint profile limits. | parser test | ES/EPXM/HA | payload fuzz | parser evidence |
| `MFOS-REQ-LGW-0011` | Gateway imports MUST validate content type, payload length, payload hash, target object, and authorization before object creation. | import test | ES/EPXM/HA | import tests | import evidence |
| `MFOS-REQ-LGW-0012` | Gateway exports MUST apply authorization, redaction policy when present, and audit before data release. | export test | ES/EPXM/HA | export tests | export evidence |
| `MFOS-REQ-LGW-0013` | Spool browse/export through gateway MUST be mediated by `spoold` and `securityd`. | integration test | ES/EPXM/HA | spool gateway tests | spool evidence |
| `MFOS-REQ-LGW-0014` | Job submission through gateway MUST be mediated by `jobd` and `securityd`. | integration test | ES/EPXM/HA | job gateway tests | job evidence |
| `MFOS-REQ-LGW-0015` | Clipboard bridge operations MUST be explicitly enabled by policy and audited. | clipboard negative test | ES/EPXM/HA | clipboard tests | clipboard evidence |
| `MFOS-REQ-LGW-0016` | Gateway MUST distinguish `UNSUPPORTED` from `SPEC_GAP`. | error model test | ES/EPXM/HA | error tests | error evidence |
| `MFOS-REQ-LGW-0017` | Gateway MUST reject replayed request IDs or stale gateway tokens. | replay test | ES/EPXM/HA | replay tests | replay evidence |
| `MFOS-REQ-LGW-0018` | Gateway MUST fail closed when `auditd` is unavailable and active profile requires audit. | fault injection | ES/EPXM/HA | audit failure tests | failure evidence |
| `MFOS-REQ-LGW-0019` | Gateway MUST NOT accept caller-supplied MFOS identity without authenticated identity mapping. | identity negative test | ES/EPXM/HA | identity spoof tests | identity evidence |
| `MFOS-REQ-LGW-0020` | Gateway MUST audit channel open, close, fault, import, export, job submit, spool browse, deny, unsupported, and spec-gap events. | audit review | ES/EPXM/HA | gateway audit coverage | audit evidence |

### 5.15 AI and Quality

Sources: `FBVBS-001`, `NIST-160-001`, `NIST-218-001`, `SLSA-001`, `SEL4-001`.

Gaps: exact CI implementation, unsafe inventory schema, coverage thresholds, independent-review workflow, provenance signer policy.

| ID | Requirement | Verification | Profiles | Related tests | Evidence |
| --- | --- | --- | --- | --- | --- |
| `MFOS-REQ-AI-0001` | AI-generated implementation output MUST list requirement IDs. | review checklist | B/ES/EPXM/HA | `CI-001` | AI output evidence |
| `MFOS-REQ-AI-0002` | AI-generated implementation output MUST list Source Matrix IDs for source-grounded concepts. | source-matrix lint | B/ES/EPXM/HA | `CI-002` | source lint evidence |
| `MFOS-REQ-AI-0003` | AI-generated output MUST list assumptions, spec gaps, unsupported features, invariants, audit obligations, and tests. | review checklist | B/ES/EPXM/HA | AI checklist tests | review evidence |
| `MFOS-REQ-AI-0004` | AI-generated production-path code MUST NOT use fake success, empty stubs, or silent fallbacks. | no-fake-success CI | B/ES/EPXM/HA | `CI-003`, `CI-004` | CI evidence |
| `MFOS-REQ-QUALITY-0001` | Requirements, design, code, tests, and evidence MUST maintain bidirectional traceability. | traceability audit | B/ES/EPXM/HA | traceability audit | traceability evidence |
| `MFOS-REQ-QUALITY-0002` | Security-sensitive PRs MUST include a negative test or documented reason why none applies. | CI gate | B/ES/EPXM/HA | `CI-006` | PR gate evidence |
| `MFOS-REQ-QUALITY-0003` | TCB changes SHOULD require independent review in Baseline and MUST require it in Enterprise-Standalone, Enterprise-PXM, and High-Assurance. | review audit | B optional; ES/EPXM/HA required | review gate tests | review evidence |
| `MFOS-REQ-QUALITY-0004` | Production claims MUST be blocked until production readiness gates are satisfied. | release review | B/ES/EPXM/HA | production gate tests | release evidence |
| `MFOS-REQ-QUALITY-0005` | Parsers MUST have fuzz targets. | fuzz campaign | B/ES/EPXM/HA | `CI-012` | fuzz registration evidence |
| `MFOS-REQ-QUALITY-0006` | Release artifacts MUST include SBOM and signed provenance. | supply-chain audit | ES/EPXM/HA required; B recommended | `CI-009`, `CI-010` | provenance evidence |
| `MFOS-REQ-QUALITY-0007` | no-fake-success CI MUST exist. | CI | B/ES/EPXM/HA | `CI-003` | CI evidence |
| `MFOS-REQ-QUALITY-0008` | Build toolchain MUST be pinned. | build inspection | B/ES/EPXM/HA | build reproducibility tests | toolchain evidence |
| `MFOS-REQ-QUALITY-0009` | Dependency allowlist MUST exist. | dependency audit | B/ES/EPXM/HA | `CI-008` | dependency evidence |
| `MFOS-REQ-QUALITY-0010` | Production readiness gate MUST pass before production claims. | release review | B/ES/EPXM/HA | production gate tests | readiness evidence |

## 6. Production Readiness Requirements

These are gate IDs, not substitutes for detailed requirements above.

| Gate | Requirement covered | Evidence artifact |
| --- | --- | --- |
| `PROD-001` | Source Matrix complete for all source-grounded concepts. | `evidence/production/PROD-001-source-matrix.md` |
| `PROD-002` | System integrity negative tests pass. | `evidence/production/PROD-002-system-integrity.md` |
| `PROD-003` | Unauthorized dataset access cannot produce handle. | `evidence/production/PROD-003-dataset-deny.md` |
| `PROD-004` | DENY audit record emitted before caller result. | `evidence/production/PROD-004-audit-ordering.md` |
| `PROD-005` | Catalog crash recovery passes. | `evidence/production/PROD-005-catalog-recovery.md` |
| `PROD-006` | Spool browse/purge security enforced. | `evidence/production/PROD-006-spool-security.md` |
| `PROD-007` | Operator commands require authority and audit. | `evidence/production/PROD-007-operator.md` |
| `PROD-008` | AMF invalid signature and revoked signer fail closed. | `evidence/production/PROD-008-amf.md` |
| `PROD-009` | Update rollback, freeze, and mix-and-match tests pass. | `evidence/production/PROD-009-update.md` |
| `PROD-010` | SBOM and signed provenance produced. | `evidence/production/PROD-010-provenance.md` |
| `PROD-011` | No fake success CI clean. | `evidence/production/PROD-011-no-fake-success.md` |
| `PROD-012` | Parser fuzz campaigns complete. | `evidence/production/PROD-012-fuzz.md` |
| `PROD-013` | PXM device teardown tested before passthrough production. | `evidence/production/PROD-013-pxm-teardown.md` |
| `PROD-014` | Guard evidence exists before High-Assurance claim. | `evidence/production/PROD-014-guard.md` |
| `PROD-015` | Recovery drill completed. | `evidence/production/PROD-015-recovery.md` |

## 7. Catalog Gaps

| Gap ID | Gap | Blocking effect |
| --- | --- | --- |
| `REQCAT-GAP-001` | Exact one-row-per-requirement source mapping needs automation from the Source Matrix. | Blocks fully automated source coverage reports. |
| `REQCAT-GAP-002` | Evidence directory and schema are conventional here but not yet enforced by tooling. | Blocks reliable CI evidence checks. |
| `REQCAT-GAP-003` | Some split specs define positive/negative test IDs while others define only test families. | Blocks uniform test traceability until test specs are created. |
| `REQCAT-GAP-004` | Formal model IDs are not yet assigned for all state machines. | Blocks formal traceability claims. |
| `REQCAT-GAP-005` | Profile applicability has conservative defaults but needs confirmation during conformance spec work. | Blocks final conformance matrix. |
| `REQCAT-GAP-006` | Threat model spec is not yet split into `04-threat-model.md`. | Blocks complete abuse-case to requirement traceability. |

## 8. AI Assignment Prompt

```text
Future authorized agents would implement or review MFOS requirements.

Constraints:
- Work only in files explicitly assigned to you.
- Do not claim compatibility with IBM z/OS or IBM subsystems.
- List every implemented MFOS-REQ ID.
- List Source Matrix IDs for source-grounded concepts.
- For every security-sensitive path, include negative tests.
- For every authorization decision, include audit obligations.
- Return UNSUPPORTED for specified but unimplemented behavior.
- Return SPEC_GAP for undefined behavior.
- Do not introduce fake success, empty stubs, or silent fallbacks.
- Produce evidence artifacts following docs/design/specs/23-requirements-catalog.md.

Required output:
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
