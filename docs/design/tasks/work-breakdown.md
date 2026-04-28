# MFOS Work Breakdown v0.1

Status: Draft

Audience: AI implementation agents, architecture agents, test engineers, reviewers

This document splits MFOS work into AI-friendly task IDs. Tasks must preserve MFOS source-grounded design discipline and must not claim z/OS compatibility or IBM product compatibility.

## 1. Task Rules

Every implementation task must include:

- Requirement IDs.
- Source Matrix IDs.
- Design spec references.
- Audit obligations.
- Failure modes.
- Positive tests.
- Negative tests.
- Fuzz targets when parsing or external input exists.
- Evidence artifacts.
- Review checklist.

Security-sensitive implementation tasks must not be accepted without negative tests.

## 2. AI Contract References

Task owners must enforce:

- AI-MFOS-001 spec IDs required.
- AI-MFOS-002 source matrix IDs required for z/OS-derived concepts.
- AI-MFOS-003 no compatibility claim.
- AI-MFOS-005 no fake success.
- AI-MFOS-006 unsupported features fail closed.
- AI-MFOS-007 spec gaps do not become behavior.
- AI-MFOS-008 negative tests required for security-sensitive paths.
- AI-MFOS-009 audit obligations required.
- AI-MFOS-010 no securityd bypass.
- AI-MFOS-011 unsafe code requires safety contract.
- AI-MFOS-012 parsers require fuzz targets.
- AI-MFOS-013 PXM does not interpret enterprise semantics.
- AI-MFOS-014 Guard does not interpret job, dataset, or spool semantics.
- AI-MFOS-015 PKU/PKS are not primary integrity boundaries.

## 3. Documentation Tasks

| ID | Task | Outputs | Evidence |
| --- | --- | --- | --- |
| DOC-001 | Register EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001. | source matrix row and concept mapping. | source lint pass. |
| DOC-002 | Register EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001. | AMF/source mapping. | source lint pass. |
| DOC-003 | Register EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001/002. | storage domain divergence note. | concept review. |
| DOC-004 | Register EXTREF-IBM-ZOS-SECURITY-SERVER-0001/002. | securityd mapping. | source review. |
| DOC-005 | Register EXTREF-IBM-ZOS-JES-INTRODUCTION-0001/002/JES2-001. | job/spool mapping. | source review. |
| DOC-006 | Register EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001/002. | dataset/catalog mapping. | source review. |
| DOC-007 | Register EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001/002. | auditd mapping. | source review. |
| DOC-008 | Register EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001. | workpolicyd mapping. | source review. |
| DOC-009 | Register EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001/002. | optional POSIX mapping. | source review. |
| DOC-010 | Register EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001/002. | PCALL mapping. | source review. |
| DOC-011 | Register EXTREF-IBM-Z-LPAR-INTRODUCTION-0001/DPM-001. | PXM mapping. | source review. |
| DOC-012 | Register EXTREF-IBM-Z-ARCHITECTURE-PRINCIPLES-0001. | terminology divergence note. | source review. |
| DOC-013 | Register X64-INTEL-001. | x64 claim source. | source review. |
| DOC-014 | Register X64-AMD-001. | AMD64 claim source. | source review. |
| DOC-015 | Register MS-VBS/MS-VSM. | Guard-only reference note. | profile review. |
| DOC-016 | Register TUF/SLSA/NIST/TCG/seL4. | assurance and supply-chain references. | source review. |
| DOC-017 | Create Source Matrix lint rule. | CI rule. | lint report. |

## 4. Specification Tasks

| ID | Task | Outputs | Evidence |
| --- | --- | --- | --- |
| SPEC-001 | Normative Language v0.1. | `00-normative-language.md`. | architecture review. |
| SPEC-002 | Conformance Profiles v0.1. | `20-conformance.md`. | profile review. |
| SPEC-003 | Glossary v0.1. | `01-glossary.md`. | terminology review. |
| SPEC-004 | IBM Concept Mapping v0.1. | source mapping spec. | source review. |
| SPEC-005 | System Integrity v0.1. | `03-system-integrity.md`. | negative test plan. |
| SPEC-006 | Threat Model v0.1. | threat model spec. | abuse case review. |
| SPEC-007 | Object Model v0.1. | `05-object-model.md`. | schema review. |
| SPEC-008 | Authorization Model v0.1. | `06-authorization.md`. | PDP review. |
| SPEC-009 | Audit Schema v0.1. | `07-audit.md`. | audit schema review. |
| SPEC-010 | Dataset/Catalog v0.1. | `08-dataset-catalog.md`. | parser and crash tests. |
| SPEC-011 | Job/Spool v0.1. | `09-job-spool.md`. | lifecycle tests. |
| SPEC-012 | Operator Command v0.1. | `10-operator-console.md`. | parser and auth tests. |
| SPEC-013 | AMF v0.1. | `12-amf.md`. | AMF negative tests. |
| SPEC-014 | Update v0.1. | `13-update.md`. | rollback/freeze tests. |
| SPEC-015 | SVC/PCALL ABI v0.1. | `15-svc-pcall.md`. | ABI fuzz plan. |
| SPEC-016 | PXM Lifecycle v0.1. | `16-pxm.md`. | state-machine tests. |
| SPEC-017 | PXM Device Teardown v0.1. | PXM teardown section. | teardown negative tests. |
| SPEC-018 | Guard Root Object v0.1. | `17-guard.md`. | Guard evidence plan. |
| SPEC-019 | Linux Gateway v0.1. | `18-linux-gateway.md`. | gateway negative tests. |
| SPEC-020 | Assurance Case v0.1. | `19-assurance-case.md`. | evidence review. |
| SPEC-021 | AI Prompt Library v0.1. | `ai-prompts.md`. | prompt review. |

## 5. Formal Tasks

| ID | Task | Target invariant | Evidence |
| --- | --- | --- | --- |
| FORMAL-001 | Authorization decision model. | unauthorized allow impossible. | model report. |
| FORMAL-002 | Dataset open invariant. | no handle without securityd allow. | model report. |
| FORMAL-003 | Audit append invariant. | required DENY audited before result. | model report. |
| FORMAL-004 | Catalog transaction model. | no phantom committed entry. | model report. |
| FORMAL-005 | Job lifecycle model. | invalid transitions rejected. | model report. |
| FORMAL-006 | Spool access model. | browse/purge requires decision. | model report. |
| FORMAL-007 | Operator command model. | command cannot execute unaudited. | model report. |
| FORMAL-008 | AMF load model. | revoked/unsigned module cannot reach READY. | model report. |
| FORMAL-009 | Update rollback/freeze model. | stale metadata cannot activate. | model report. |
| FORMAL-010 | PXM partition lifecycle model. | invalid transition rejected. | model report. |
| FORMAL-011 | Device teardown model. | no reassignment before teardown. | model report. |
| FORMAL-012 | Guard root transition model. | root mismatch cannot be accepted. | model report. |

## 6. Hosted Prototype Tasks

| ID | Task | Required negative tests | Evidence |
| --- | --- | --- | --- |
| HOST-001 | securityd hosted prototype. | unauthorized resource deny. | unit/integration report. |
| HOST-002 | auditd hosted prototype. | tamper and write failure. | hash-chain report. |
| HOST-003 | catalogd hosted prototype. | invalid DSN and crash mid-commit. | parser/crash report. |
| HOST-004 | datasetd hosted prototype. | stale handle and unauthorized open. | negative test report. |
| HOST-005 | jobd hosted prototype. | identity spoof and invalid lifecycle. | negative test report. |
| HOST-006 | spoold hosted prototype. | non-owner browse/purge. | negative test report. |
| HOST-007 | operatord hosted prototype. | unauthorized command execute. | parser/auth report. |
| HOST-008 | workpolicyd minimal prototype. | invalid class and quota overrun. | unit report. |
| HOST-009 | amfd prototype. | invalid signature and revoked signer. | AMF report. |
| HOST-010 | uvsd prototype. | rollback/freeze/mix-and-match. | UVS report. |
| HOST-011 | HELLO job success integration. | none beyond success path. | integration report. |
| HOST-012 | Unauthorized dataset access deny integration. | BOB cannot read ALICE dataset. | negative report. |
| HOST-013 | Audit chain tamper test. | tamper detected. | tamper report. |
| HOST-014 | Catalog crash recovery test. | crash mid-transaction. | recovery report. |

## 7. CI Tasks

| ID | Task | Blocks |
| --- | --- | --- |
| CI-001 | spec ID required check. | code without requirement ID. |
| CI-002 | source matrix ref required check. | z/OS-derived concept without source ID. |
| CI-003 | no fake success scanner. | empty success, silent fallback, fake OK. |
| CI-004 | TODO/unimplemented scanner for production paths. | production path placeholders. |
| CI-005 | audit obligation checker. | missing audit for security-sensitive path. |
| CI-006 | negative test required checker. | security path without negative test. |
| CI-007 | unsafe inventory generator. | unsafe without safety contract. |
| CI-008 | dependency allowlist checker. | unapproved dependency. |
| CI-009 | SBOM generator. | missing SBOM for release. |
| CI-010 | signed provenance generator. | missing provenance for release. |
| CI-011 | reproducible build diff report. | unexplained build difference. |
| CI-012 | fuzz target registration checker. | parser without fuzz target. |

## 8. Nucleus and Service Tasks

| ID | Task | Required evidence |
| --- | --- | --- |
| NUC-001 | boot handoff. | boot validation tests. |
| NUC-002 | memory map parser. | parser fuzz target. |
| NUC-003 | page table manager. | W^X tests. |
| NUC-004 | NX/W^X. | mapping negative tests. |
| NUC-005 | address space. | isolation tests. |
| NUC-006 | scheduler baseline. | lifecycle tests. |
| NUC-007 | SVC entry. | ABI fuzz and negative tests. |
| NUC-008 | typed object handles. | stale/wrong-type tests. |
| NUC-009 | copy-in/copy-out. | overflow and bad pointer tests. |
| NUC-010 | IPC. | bounded message tests. |
| NUC-011 | service launcher. | service fault test. |
| NUC-012 | fault containment. | fault injection report. |
| NUC-013 | crash dump. | crash trigger report. |
| NUC-014 | audit hook. | audit ordering report. |

| ID | Task | Required evidence |
| --- | --- | --- |
| SECD-001 | principal registry. | auth tests. |
| SECD-002 | profile language parser. | fuzz target. |
| SECD-003 | dataset auth. | unauthorized open deny. |
| SECD-004 | spool auth. | browse/purge deny. |
| SECD-005 | operator auth. | command deny. |
| SECD-006 | AMF auth. | revoked module deny. |
| SECD-007 | policy transaction. | rollback/crash tests. |
| SECD-008 | break-glass. | expiry and audit tests. |
| AUD-001 | audit schema. | schema tests. |
| AUD-002 | append log. | append tests. |
| AUD-003 | hash chain. | tamper tests. |
| AUD-004 | query API. | authorization tests. |
| AUD-005 | failure policy. | fault injection. |
| AUD-006 | remote export. | integration tests. |
| CAT-001 | DSN grammar. | fuzz target. |
| CAT-002 | catalog schema. | schema tests. |
| CAT-003 | define dataset. | auth/audit tests. |
| CAT-004 | resolve dataset. | not found tests. |
| CAT-005 | transaction journal. | crash tests. |
| CAT-006 | crash recovery. | recovery tests. |
| DATA-001 | sequential dataset. | read/write tests. |
| DATA-002 | dataset handles. | stale handle tests. |
| DATA-003 | stale handle rejection. | negative tests. |
| DATA-004 | retention. | purge denial tests. |
| DATA-005 | integrity tag. | tamper tests. |
| JOB-001 | JCL-like parser. | fuzz target. |
| JOB-002 | job submit. | identity spoof deny. |
| JOB-003 | conversion. | malformed JCL deny. |
| JOB-004 | queue. | invalid transition tests. |
| JOB-005 | initiator. | concurrency tests. |
| JOB-006 | DD resolution. | unauthorized dataset deny. |
| JOB-007 | step execution. | return code tests. |
| JOB-008 | return code. | failure propagation tests. |
| SPL-001 | SYSOUT capture. | capture tests. |
| SPL-002 | spool browse. | non-owner deny. |
| SPL-003 | spool purge. | retention deny. |
| SPL-004 | retention. | purge tests. |
| OPER-001 | console boot. | boot UI test. |
| OPER-002 | command parser. | fuzz target. |
| OPER-003 | DISPLAY SYSTEM. | auth/audit tests. |
| OPER-004 | DEFINE USER. | authority tests. |
| OPER-005 | DEFINE DATASET. | auth/audit tests. |
| OPER-006 | SUBMIT JOB. | identity/audit tests. |
| OPER-007 | CANCEL JOB. | authority tests. |
| OPER-008 | emergency mode. | break-glass tests. |
| WPOL-001 | job class. | invalid class tests. |
| WPOL-002 | priority. | scheduling tests. |
| WPOL-003 | max concurrency. | quota tests. |
| WPOL-004 | service class placeholder. | unsupported fail-closed tests. |
| AMF-001 | manifest parser. | fuzz target. |
| AMF-002 | signature verifier. | invalid signature tests. |
| AMF-003 | revocation check. | revoked signer tests. |
| AMF-004 | load control. | mutable dataset deny. |
| UVS-001 | TUF-like metadata. | metadata fuzz. |
| UVS-002 | artifact verification. | hash/signature tests. |
| UVS-003 | rollback detection. | rollback tests. |
| UVS-004 | freeze detection. | expired metadata tests. |
| UVS-005 | mix-and-match detection. | snapshot mismatch tests. |

## 9. PXM and Guard Tasks

| ID | Task | Required evidence |
| --- | --- | --- |
| PXM-001 | partition lifecycle spec. | state-machine tests. |
| PXM-002 | activation profile parser. | fuzz target. |
| PXM-003 | implicit single partition backend. | API parity tests. |
| PXM-004 | partition-aware MFOS API. | API tests. |
| PXM-005 | VT-x lab skeleton. | lab report. |
| PXM-006 | AMD-V lab skeleton. | lab report. |
| PXM-007 | EPT/NPT memory domain. | mapping tests. |
| PXM-008 | IOMMU domain manager. | isolation tests. |
| PXM-009 | interrupt remapping. | interrupt tests. |
| PXM-010 | device assignment model. | assignment tests. |
| PXM-011 | device teardown checklist. | teardown negative tests. |
| PXM-012 | partition audit. | audit tests. |
| PXM-013 | recovery partition. | recovery drill. |
| GRD-001 | Guard root model. | root transition model. |
| GRD-002 | Guard call ABI. | ABI tests. |
| GRD-003 | security root seal. | seal/verify tests. |
| GRD-004 | audit root seal. | audit root tests. |
| GRD-005 | AMF registry seal. | AMF Guard tests. |
| GRD-006 | SVC table verify. | mismatch tests. |
| GRD-007 | executable mapping policy. | W^X/Guard tests. |
| GRD-008 | attestation. | attestation evidence. |
| GRD-009 | failure policy. | fail-secure tests. |
| GRD-010 | lockdown tests. | fault injection. |

## 10. Assurance and Conformance Tasks

| ID | Task | Required evidence |
| --- | --- | --- |
| ASSUR-001 | Create claim registry. | claim index. |
| ASSUR-002 | Instantiate assurance case template for system integrity. | reviewed claim. |
| ASSUR-003 | Instantiate assurance case template for DENY-before-result audit. | audit evidence. |
| ASSUR-004 | Instantiate assurance case template for dataset handle denial. | negative evidence. |
| ASSUR-005 | Instantiate assurance case template for AMF fail-closed. | AMF evidence. |
| ASSUR-006 | Instantiate assurance case template for update rollback/freeze. | UVS evidence. |
| ASSUR-007 | Instantiate HA Guard root claims. | Guard evidence. |
| CONF-001 | Build requirements status matrix. | conformance report. |
| CONF-002 | Build production gate matrix. | gate report. |
| CONF-003 | Run release wording review. | wording report. |
| CONF-004 | Archive evidence artifacts. | evidence index. |

## 11. Task Completion Output

Every agent completing a task must return:

```text
1. Completed Task IDs
2. Implemented Requirement IDs
3. Source Matrix IDs
4. Files Changed
5. Assumptions
6. Spec Gaps
7. Unsupported Features
8. Security Invariants
9. Audit Obligations
10. Tests Added
11. Negative Tests Added
12. Fuzz Targets Added
13. Evidence Artifacts
14. Review Checklist
```

## 12. Current Gaps

- Task dependency graph is not machine-readable yet.
- Task owner assignment is not defined.
- Priority and milestone metadata are not fixed.
- CI task implementation details are not specified.
- Formal tool choice is not fixed.
- Evidence archive layout is not fixed.

