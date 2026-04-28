# MFOS Source Traceability Index v0.1

Status: design draft

This index maps major MFOS Source Matrix IDs to requirement namespaces, split
spec files, negative-test categories, evidence artifacts, and profile
applicability.

MFOS is z/OS-inspired. This index does not claim z/OS compatibility or
compatibility with IBM subsystems.

## Purpose

The purpose of this index is to give AI agents and reviewers a fast,
human-readable routing table:

- Source IDs identify why a concept is allowed in MFOS.
- Requirement namespaces identify where normative obligations belong.
- Split spec files identify where the detailed design must live.
- Negative-test categories identify what must fail safely.
- Evidence artifacts identify what proof must be produced before claims.
- Profile applicability identifies whether Baseline, Enterprise-Standalone,
  Enterprise-PXM, or High-Assurance must satisfy the obligation.

This file is an index, not the canonical source ledger. The source ledger is
`docs/design/source-matrix/source-matrix.yml`.

## Profile Key

| Code | Meaning |
| --- | --- |
| B | Baseline |
| ES | Enterprise-Standalone |
| EPXM | Enterprise-PXM |
| HA | High-Assurance |
| Opt | Optional or profile-limited |
| N/A | Not applicable |

## Evidence Artifact Classes

The artifact IDs below are planned evidence classes. Concrete evidence records
must follow the policy in `docs/design/source-matrix/traceability-policy.md`.

| Evidence class | Meaning |
| --- | --- |
| EVID-SRC-LINT-* | source ID, prohibited wording, and mapping lint results |
| EVID-ARCH-REVIEW-* | architecture review notes and approvals |
| EVID-SPEC-REVIEW-* | split spec review results |
| EVID-NEG-* | negative test output |
| EVID-FUZZ-* | fuzz target run summaries and corpus metadata |
| EVID-STATE-* | state-machine legal/illegal transition results |
| EVID-AUD-* | audit ordering, schema, hash-chain, and tamper evidence |
| EVID-CRASH-* | crash-recovery and rollback evidence |
| EVID-FAULT-* | fault-injection evidence |
| EVID-FORMAL-* | formal model output or proof review notes |
| EVID-SBOM-* | SBOM artifact |
| EVID-PROV-* | signed provenance artifact |
| EVID-ATTEST-* | measured boot or attestation artifact |
| EVID-PROD-GATE-* | production readiness gate record |

## Major Traceability Map

| Trace area | Source Matrix IDs | MFOS-REQ namespaces | Split spec files | Negative-test categories | Evidence artifacts | Profiles | Gaps |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Source grounding and compatibility guardrails | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-Z-ARCHITECTURE-PRINCIPLES-0001, FBVBS-001 | MFOS-REQ-SRC-*, MFOS-REQ-AI-*, MFOS-REQ-QUAL-* | `02-source-matrix.md`, `21-ai-implementation-contract.md`, `22-production-readiness.md` | missing source ID, prohibited compatibility wording, IBM term without divergence, fake success, SPEC_GAP treated as success | EVID-SRC-LINT-*, EVID-ARCH-REVIEW-*, EVID-SPEC-REVIEW-* | B/ES/EPXM/HA | Exact lint rule IDs pending. Canonical AI requirement IDs pending. |
| System integrity and authorized boundary testing | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001 | MFOS-REQ-SI-*, MFOS-REQ-AMF-*, MFOS-REQ-QUAL-* | `03-system-integrity.md`, `12-amf.md`, `15-svc-pcall.md`, `21-ai-implementation-contract.md` | unauthorized system interface success, accidental authority transfer, untrusted parameter confusion, unsupported call returns success | EVID-NEG-SI-*, EVID-FUZZ-SVC-*, EVID-ARCH-REVIEW-SI-* | B/ES/EPXM/HA | Exact SVC/PCALL/AMF boundary checklist pending. |
| Storage protection mapping and x64 divergence | EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001, EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001, EXTREF-IBM-Z-ARCHITECTURE-PRINCIPLES-0001, X64-INTEL-001, X64-AMD-001, X64-LINUX-PKU-001, X64-LINUX-CET-001 | MFOS-REQ-SI-*, MFOS-REQ-NUC-*, MFOS-REQ-QUAL-* | `03-system-integrity.md`, `14-nucleus.md`, `15-svc-pcall.md`, `17-guard.md` | storage-domain write bypass, W^X bypass, PKU/PKS overclaim, CET treated as authorization, user pointer direct dereference | EVID-NEG-STG-*, EVID-NEG-NUC-*, EVID-ARCH-REVIEW-X64-* | B/ES/EPXM/HA | StorageDomain enumeration, page-table policy, and CPU feature fallback matrix pending. |
| securityd and protected resource profiles | EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001 | MFOS-REQ-SEC-*, MFOS-REQ-AUD-*, MFOS-REQ-SRC-* | `06-authorization.md`, `07-audit.md`, `08-dataset-catalog.md`, `09-job-spool.md`, `10-operator-console.md` | securityd bypass, stale handle after policy change, local final authorization by service, missing audit obligation | EVID-NEG-SEC-*, EVID-AUD-SEC-*, EVID-SPEC-REVIEW-SEC-* | B/ES/EPXM/HA | Canonical profile language, authority taxonomy, and transaction schema pending. |
| auditd and evidence stream | EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001, FBVBS-001 | MFOS-REQ-AUD-*, MFOS-REQ-SEC-*, MFOS-REQ-QUAL-* | `07-audit.md`, `06-authorization.md`, `22-production-readiness.md` | DENY returned before audit, hash-chain tamper, audit unavailable but protected operation succeeds, spool output treated as audit evidence | EVID-AUD-SCHEMA-*, EVID-AUD-TAMPER-*, EVID-FAULT-AUD-* | B/ES/EPXM/HA | Audit encoding, redaction policy, retention policy, and remote export protocol pending. |
| catalogd and datasetd | EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001, EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | MFOS-REQ-CAT-*, MFOS-REQ-DATA-*, MFOS-REQ-SEC-*, MFOS-REQ-AUD-* | `08-dataset-catalog.md`, `06-authorization.md`, `07-audit.md`, `05-object-model.md` | open uncommitted catalog entry, unauthorized handle creation, stale dataset handle, retention bypass, dataset treated as POSIX file | EVID-NEG-CAT-*, EVID-NEG-DATA-*, EVID-CRASH-CAT-*, EVID-AUD-DATA-* | B/ES/EPXM/HA | DSN grammar, allocation model, transaction journal, retention semantics, and encryption hook IDs pending. |
| jobd and spoold | EXTREF-IBM-ZOS-JES-INTRODUCTION-0001, EXTREF-IBM-ZOS-JES-JOB-FLOW-0001, EXTREF-IBM-ZOS-JES2-LIBRARY-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | MFOS-REQ-JOB-*, MFOS-REQ-SPL-*, MFOS-REQ-SEC-*, MFOS-REQ-AUD-* | `09-job-spool.md`, `06-authorization.md`, `07-audit.md`, `10-operator-console.md` | job opens dataset before principal, malformed JCL-like input accepted, unauthorized spool browse/purge/export, SYSOUT visible to wrong subject | EVID-STATE-JOB-*, EVID-FUZZ-JCL-*, EVID-NEG-SPL-*, EVID-AUD-JOB-* | B/ES/EPXM/HA | JCL-like grammar, initiator rules, output classes, and spool retention policy pending. |
| operator console | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-JES2-LIBRARY-0001 | MFOS-REQ-OPER-*, MFOS-REQ-SEC-*, MFOS-REQ-AUD-* | `10-operator-console.md`, `06-authorization.md`, `07-audit.md`, `21-ai-implementation-contract.md` | command executes without authority, destructive command without confirmation, automation hook bypass, unknown command succeeds | EVID-FUZZ-OPER-*, EVID-NEG-OPER-*, EVID-AUD-OPER-* | B/ES/EPXM/HA | Initial operator command grammar and authority classes pending. |
| workload management | EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | MFOS-REQ-WPOL-*, MFOS-REQ-JOB-*, MFOS-REQ-AUD-* | `11-workload-policy.md`, `09-job-spool.md`, `07-audit.md` | priority bypasses authorization, overload policy suppresses audit, service class changes security outcome, invalid policy activation succeeds | EVID-NEG-WPOL-*, EVID-STATE-WPOL-*, EVID-SPEC-REVIEW-WPOL-* | B/ES/EPXM/HA | Phase-1 job class schema and later response-time or velocity-like goal IDs pending. |
| optional POSIX and Linux gateway | EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001, EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001, EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | MFOS-REQ-SI-*, MFOS-REQ-DATA-*, MFOS-REQ-SEC-*, MFOS-REQ-AUD-* | `18-linux-gateway.md`, `08-dataset-catalog.md`, `06-authorization.md`, `07-audit.md` | POSIX path bypasses catalog/securityd, root shell changes policy, side partition gateway bypasses audit, dataset reinterpreted as ordinary file | EVID-NEG-POSIX-*, EVID-NEG-GATEWAY-*, EVID-AUD-GATEWAY-* | Opt/ES/EPXM/HA | POSIX subsystem profile, path-to-dataset behavior, and Linux gateway protocol pending. |
| SVC and PCALL ABI | EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001, EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, X64-INTEL-001, X64-AMD-001 | MFOS-REQ-SI-*, MFOS-REQ-NUC-*, MFOS-REQ-QUAL-* | `15-svc-pcall.md`, `14-nucleus.md`, `03-system-integrity.md` | caller-supplied identity trusted, untrusted pointer dereference, payload length overflow, endpoint type confusion, unsupported endpoint succeeds | EVID-NEG-PCALL-*, EVID-FUZZ-PCALL-*, EVID-NEG-SVC-* | B/ES/EPXM/HA | Endpoint registry, sealed-buffer format, and service identity binding pending. |
| nucleus object and capability model | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001, EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001, X64-INTEL-001, X64-AMD-001, FBVBS-001 | MFOS-REQ-NUC-*, MFOS-REQ-SI-*, MFOS-REQ-AUD-* | `14-nucleus.md`, `03-system-integrity.md`, `05-object-model.md`, `15-svc-pcall.md` | typed handle forgery, copy-in/copy-out bypass, writable executable mapping, kernel audit hook missing, fault containment failure | EVID-NEG-NUC-*, EVID-FAULT-NUC-*, EVID-ARCH-REVIEW-NUC-* | B/ES/EPXM/HA | Capability handle format, scheduler identity binding, and crash dump evidence policy pending. |
| PXM partition lifecycle and device assignment | EXTREF-IBM-Z-LPAR-INTRODUCTION-0001, EXTREF-IBM-Z-DPM-0001, X64-INTEL-001, X64-AMD-001, FBVBS-001 | MFOS-REQ-PXM-*, MFOS-REQ-AUD-*, MFOS-REQ-QUAL-* | `16-pxm.md`, `07-audit.md`, `22-production-readiness.md` | invalid partition transition, device assigned without IOMMU, interrupt remapping missing, teardown incomplete, memory reused without zeroing, PXM interprets dataset policy | EVID-STATE-PXM-*, EVID-NEG-PXM-*, EVID-FAULT-PXM-*, EVID-AUD-PXM-* | ES/EPXM/HA; B uses implicit single partition | Activation profile schema, x64 backend split, and device model IDs pending. |
| PXM Guard root protection | MS-VBS-001, MS-VSM-001, X64-INTEL-001, X64-AMD-001, FBVBS-001 | MFOS-REQ-GRD-*, MFOS-REQ-AMF-*, MFOS-REQ-AUD-*, MFOS-REQ-QUAL-* | `17-guard.md`, `12-amf.md`, `07-audit.md`, `16-pxm.md` | Guard accepts root mismatch, executable mapping violates policy, AMF registry mismatch loads, SVC table mismatch ignored, Guard unavailable boot succeeds in HA, Guard interprets dataset policy | EVID-NEG-GRD-*, EVID-FAULT-GRD-*, EVID-ATTEST-GRD-*, EVID-AUD-GRD-* | HA required; E optional; B N/A | Guard call ABI, attestation claims, root transition schema, and unavailable-Guard policy pending. |
| AMF authorized module facility | EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, MS-VBS-001 | MFOS-REQ-AMF-*, MFOS-REQ-SEC-*, MFOS-REQ-AUD-*, MFOS-REQ-GRD-* | `12-amf.md`, `06-authorization.md`, `07-audit.md`, `17-guard.md` | invalid signature loads, revoked signer loads, mutable catalog artifact loads, arbitrary pointer ABI, audit disable authority, HA load without Guard approval | EVID-NEG-AMF-*, EVID-AUD-AMF-*, EVID-ATTEST-AMF-* | B/ES/EPXM/HA; HA adds Guard approval | AMF manifest, authority classes, revocation list format, and ABI details pending. |
| update verification and supply chain | TUF-001, EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001, NIST-218-001, SLSA-001, FBVBS-001 | MFOS-REQ-UVS-*, MFOS-REQ-QUAL-*, MFOS-REQ-AUD-* | `13-update.md`, `22-production-readiness.md`, `07-audit.md` | rollback accepted, freeze accepted, mix-and-match accepted, bad signature/hash/size accepted, revoked key accepted, security epoch downgrade accepted | EVID-NEG-UVS-*, EVID-CRASH-UVS-*, EVID-SBOM-*, EVID-PROV-* | B signed artifacts; E TUF-like; HA TUF-like plus Guard root | Metadata role schema, key rotation, dependency resolution, and recovery rollback workflow pending. |
| firmware, measured boot, and attestation | TCG-001, NIST-193-001, NIST-160-001, X64-INTEL-001, X64-AMD-001 | MFOS-REQ-PXM-*, MFOS-REQ-GRD-*, MFOS-REQ-QUAL-*, MFOS-REQ-UVS-* | `16-pxm.md`, `17-guard.md`, `13-update.md`, `22-production-readiness.md` | missing measurement accepted, stale attestation accepted, firmware recovery path absent, measured boot treated as runtime integrity proof | EVID-ATTEST-BOOT-*, EVID-FAULT-BOOT-*, EVID-PROD-GATE-* | ES/EPXM/HA required; B recommended/optional by profile | Measured component list, event-log schema, and firmware compromise assumptions pending. |
| formal assurance and proof boundaries | SEL4-001, NIST-160-001, FBVBS-001 | MFOS-REQ-QUAL-*, MFOS-REQ-SI-*, MFOS-REQ-PXM-*, MFOS-REQ-GRD-* | `04-threat-model.md`, `03-system-integrity.md`, `16-pxm.md`, `17-guard.md`, `22-production-readiness.md` | proof assumes unlisted hardware behavior, formal model omits unauthorized success, liveness without audit, invalid transition missing | EVID-FORMAL-SI-*, EVID-FORMAL-PXM-*, EVID-FORMAL-GRD-*, EVID-ARCH-REVIEW-* | B core state machines; E core plus security; HA core plus security plus Guard | Formal language selection and first model list pending. |
| quality gates and AI implementation discipline | NIST-218-001, SLSA-001, FBVBS-001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001 | MFOS-REQ-QUAL-*, MFOS-REQ-AI-*, MFOS-REQ-SRC-* | `21-ai-implementation-contract.md`, `22-production-readiness.md`, `02-source-matrix.md` | code without spec ID, source ID missing, no negative test, no audit obligation, unsafe without contract, production stub returns success | EVID-SRC-LINT-*, EVID-PROV-*, EVID-SBOM-*, EVID-PROD-GATE-* | B/ES/EPXM/HA with stricter ES/EPXM/HA evidence | CI rule IDs, dependency allowlist, unsafe inventory format, and provenance policy pending. |

## Requirement Namespace Routing

| Namespace | Primary source IDs | Primary split specs | Minimum negative-test routing | Evidence routing | Gap |
| --- | --- | --- | --- | --- | --- |
| MFOS-REQ-SRC-* | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-Z-ARCHITECTURE-PRINCIPLES-0001, FBVBS-001 | `02-source-matrix.md` | source ID missing, prohibited wording | EVID-SRC-LINT-*, EVID-SPEC-REVIEW-* | Exact lint IDs pending. |
| MFOS-REQ-SI-* | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001, EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001, EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001 | `03-system-integrity.md` | unauthorized success, bypass, unsupported success | EVID-NEG-SI-*, EVID-ARCH-REVIEW-SI-* | Complete system interface list pending. |
| MFOS-REQ-SEC-* | EXTREF-IBM-ZOS-SECURITY-SERVER-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001 | `06-authorization.md` | securityd bypass, stale handle, local decision | EVID-NEG-SEC-*, EVID-AUD-SEC-* | Profile language pending. |
| MFOS-REQ-AUD-* | EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001, FBVBS-001 | `07-audit.md` | deny-before-audit failure, tamper, unavailable audit | EVID-AUD-*, EVID-FAULT-AUD-* | Record encoding pending. |
| MFOS-REQ-CAT-* | EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001, EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001 | `08-dataset-catalog.md` | uncommitted entry, crash mid-transaction | EVID-NEG-CAT-*, EVID-CRASH-CAT-* | Journal format pending. |
| MFOS-REQ-DATA-* | EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001, EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001 | `08-dataset-catalog.md` | unauthorized handle, stale handle, retention bypass | EVID-NEG-DATA-*, EVID-AUD-DATA-* | Allocation and handle format pending. |
| MFOS-REQ-JOB-* | EXTREF-IBM-ZOS-JES-INTRODUCTION-0001, EXTREF-IBM-ZOS-JES-JOB-FLOW-0001, EXTREF-IBM-ZOS-JES2-LIBRARY-0001 | `09-job-spool.md` | malformed job, pre-principal dataset open | EVID-STATE-JOB-*, EVID-FUZZ-JCL-* | Parser grammar pending. |
| MFOS-REQ-SPL-* | EXTREF-IBM-ZOS-JES-INTRODUCTION-0001, EXTREF-IBM-ZOS-JES-JOB-FLOW-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | `09-job-spool.md` | unauthorized browse, purge, export | EVID-NEG-SPL-*, EVID-AUD-SPL-* | Output class and retention pending. |
| MFOS-REQ-OPER-* | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001, EXTREF-IBM-ZOS-JES2-LIBRARY-0001 | `10-operator-console.md` | command without authority, destructive command without confirmation | EVID-NEG-OPER-*, EVID-FUZZ-OPER-* | Command grammar pending. |
| MFOS-REQ-WPOL-* | EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | `11-workload-policy.md` | priority bypass, invalid policy activation | EVID-NEG-WPOL-*, EVID-STATE-WPOL-* | Phase-1 policy schema pending. |
| MFOS-REQ-AMF-* | EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001, EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001, EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | `12-amf.md` | invalid signature, revoked signer, unsafe ABI | EVID-NEG-AMF-*, EVID-AUD-AMF-* | Manifest and authority classes pending. |
| MFOS-REQ-UVS-* | TUF-001, EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001, NIST-218-001, SLSA-001 | `13-update.md` | rollback, freeze, mix-and-match, revoked key | EVID-NEG-UVS-*, EVID-PROV-* | Metadata schema pending. |
| MFOS-REQ-NUC-* | EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001, EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001, X64-INTEL-001, X64-AMD-001 | `14-nucleus.md`, `15-svc-pcall.md` | handle forgery, pointer misuse, W^X violation | EVID-NEG-NUC-*, EVID-FAULT-NUC-* | Handle format pending. |
| MFOS-REQ-PXM-* | EXTREF-IBM-Z-LPAR-INTRODUCTION-0001, EXTREF-IBM-Z-DPM-0001, X64-INTEL-001, X64-AMD-001, FBVBS-001 | `16-pxm.md` | invalid transition, teardown incomplete, memory reuse | EVID-STATE-PXM-*, EVID-NEG-PXM-* | Activation profile pending. |
| MFOS-REQ-GRD-* | MS-VBS-001, MS-VSM-001, X64-INTEL-001, X64-AMD-001, FBVBS-001 | `17-guard.md` | root mismatch, executable policy violation, Guard unavailable | EVID-NEG-GRD-*, EVID-ATTEST-GRD-* | Guard call ABI pending. |
| MFOS-REQ-AI-* | FBVBS-001, NIST-218-001, EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001 | `21-ai-implementation-contract.md` | fake success, missing spec ID, missing negative test | EVID-SRC-LINT-*, EVID-PROD-GATE-* | AI requirement canonical IDs pending. |
| MFOS-REQ-QUAL-* | NIST-160-001, NIST-218-001, SLSA-001, SEL4-001, FBVBS-001 | `22-production-readiness.md` | missing provenance, missing SBOM, unreviewed TCB change | EVID-SBOM-*, EVID-PROV-*, EVID-PROD-GATE-* | SLSA target level and review rules pending. |

## Profile Applicability Summary

| Profile | Source-driven minimums | Evidence required before profile claim | Gaps |
| --- | --- | --- | --- |
| Baseline | Source grounding, system integrity statement, securityd, auditd, dataset/catalog, job/spool, operator console, NX/W^X, no fake success | EVID-SRC-LINT-*, EVID-NEG-SI-*, EVID-NEG-SEC-*, EVID-AUD-*, EVID-PROD-GATE-* | Exact Baseline conformance checklist pending. |
| Enterprise-Standalone | Baseline plus measured boot, TPM where applicable, remote audit export, TUF-like update metadata, signed provenance, SBOM, and no cross-partition device-assignment claim | Baseline evidence plus EVID-ATTEST-BOOT-*, EVID-PROV-*, EVID-SBOM-*, EVID-NEG-UVS-* | Enterprise-Standalone update and attestation evidence schema pending. |
| Enterprise-PXM | Enterprise-Standalone plus PXM required, partition lifecycle claims, side-partition claims, and device assignment only after teardown evidence | Enterprise-Standalone evidence plus EVID-STATE-PXM-*, EVID-NEG-PXM-*, EVID-DEVICE-TEARDOWN-* | PXM hardware evidence and teardown schema pending. |
| High-Assurance | Enterprise-PXM plus Guard required, Guard-sealed security/audit/AMF roots, explicit proof boundaries | Enterprise-PXM evidence plus EVID-NEG-GRD-*, EVID-ATTEST-GRD-*, EVID-FORMAL-*, EVID-FAULT-GRD-* | Guard ABI, attestation claims, and formal proof scope pending. |

## Current Cross-Cutting Gaps

- Canonical requirement IDs are still design-draft references in several areas.
- Concrete test IDs and evidence IDs have not yet been registered.
- The source matrix YAML is not yet linted against split specs.
- IBM source version pins and section anchors are still pending.
- Profile-specific conformance checklists need finalization.
- Evidence storage location and retention policy are not yet specified.
- Formal model file paths are not yet mapped to requirement IDs.
- CI gates for no fake success, source IDs, audit obligations, and negative
  tests are not yet implemented.
