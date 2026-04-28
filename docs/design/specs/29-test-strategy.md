---
spec_id: "MFOS-SPEC-29-TEST-STRATEGY"
title: "MFOS Test Strategy v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001", "EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001", "EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001", "EXTREF-IBM-Z-DPM-0001", "EXTREF-IBM-ZOS-JES-INTRODUCTION-0001", "EXTREF-IBM-ZOS-JES-JOB-FLOW-0001", "EXTREF-IBM-ZOS-JES2-LIBRARY-0001", "EXTREF-IBM-Z-LPAR-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001", "EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001", "EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001", "EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001", "EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001", "EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001", "EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001", "MS-VBS-001", "MS-VSM-001", "NIST-160-001", "NIST-193-001", "NIST-218-001", "SEL4-001", "SLSA-001", "TCG-001", "TUF-001", "X64-AMD-001", "X64-INTEL-001", "X64-LINUX-CET-001", "X64-LINUX-PKU-001"]
requirement_refs: ["MFOS-REQ-TEST-*"]
claim_refs: []
test_refs: ["TEST-GAP-*"]
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Test Strategy v0.1

Status: Draft design split

Owner area: `docs/design/specs/29-test-strategy.md`

This document defines the MFOS test strategy across design, hosted prototype, nucleus, services, PXM, Guard, supply chain, conformance, and release gates. MFOS is source-grounded and z/OS-inspired; this test strategy does not authorize claims of compatibility with IBM z/OS, IBM subsystems, z/Architecture binaries, or IBM APIs.

## 1. Purpose

MFOS testing exists to prove four things:

1. Required behavior works.
2. Forbidden behavior fails closed.
3. Security-sensitive decisions produce evidence.
4. Release and profile claims do not exceed tested evidence.

The highest-value MFOS tests are negative, ordering, crash, and traceability tests. A green happy-path test is insufficient for protected resources.

## 2. Scope

This strategy covers:

- Unit tests.
- Integration tests.
- Negative tests.
- Fuzz tests.
- Conformance tests.
- Crash-recovery tests.
- Fault-injection tests.
- Supply-chain tests.
- Formal-model tests.
- Release-gate tests.
- Evidence artifacts.
- CI gates.
- Profile applicability.

This strategy does not define:

- Concrete test runner commands.
- Final programming language harnesses.
- Hardware lab scheduling.
- Final fuzz campaign duration thresholds.
- Final proof assistant choice.
- Complete production evidence schema.

## 3. Source Matrix References

| Source ID | Test-strategy use |
| --- | --- |
| `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001` | System integrity negative-test baseline. |
| `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001` | Authorized-boundary and untrusted-parameter negative testing. |
| `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001` | Security manager, protected resource, profile, and authorization tests. |
| `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001` | Audit/accounting evidence tests. |
| `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001` | Dataset/catalog tests. |
| `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-JES-JOB-FLOW-0001`, `EXTREF-IBM-ZOS-JES2-LIBRARY-0001` | Job/spool lifecycle tests. |
| `EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001` | Workload policy and service-class tests. |
| `EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001` | AMF authorized-module tests. |
| `EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001`, `EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001` | PCALL and cross-address-space boundary tests. |
| `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `EXTREF-IBM-Z-DPM-0001` | PXM partition lifecycle and management-plane tests. |
| `X64-INTEL-001`, `X64-AMD-001` | x64 nucleus, paging, virtualization, and platform tests. |
| `X64-LINUX-PKU-001`, `X64-LINUX-CET-001` | PKU/CET limitation and mechanism tests. |
| `TCG-001` | Measured boot, TPM event log, and attestation tests. |
| `TUF-001` | Update rollback, freeze, and mix-and-match tests. |
| `SLSA-001` | Provenance and build-integrity tests. |
| `NIST-160-001`, `NIST-218-001`, `NIST-193-001` | Secure engineering, SSDF, and recovery tests. |
| `SEL4-001` | Proof-boundary discipline and formal evidence framing. |
| `MS-VBS-001`, `MS-VSM-001` | High-Assurance Guard comparison tests only. |
| `FBVBS-001` | Traceability, state-machine, evidence, production-proof, and no-fake-success testing. |

## 4. Test Principles

1. Every security-sensitive change MUST include negative tests.
2. Every protected-resource test MUST assert absence of forbidden side effects.
3. Every parser or binary-interface change MUST include fuzz target registration.
4. Every authorization test MUST bind subject, object, operation, context, and policy version.
5. Every DENY-with-audit test MUST verify audit-before-result ordering.
6. Every crash-recovery test MUST verify committed state, rolled-back state, and audit/recovery evidence.
7. Every `UNSUPPORTED` and `SPEC_GAP` path MUST be tested as fail-closed.
8. Every profile claim MUST map to tests and evidence.
9. Debug logs, console output, and spool output MUST NOT satisfy audit evidence tests.
10. Hardware mechanism tests MUST NOT replace authorization or audit tests.

## 5. Test Class Matrix

| Test class | Purpose | Required profiles | Primary CI gates | Evidence artifact |
| --- | --- | --- | --- | --- |
| Unit | Validate local functions, schemas, state transitions, and typed errors. | B/ES/EPXM/HA | `CI-001`, `CI-003` | `evidence/tests/unit/<suite>.json` |
| Integration | Validate service-to-service workflows and ordering. | B/ES/EPXM/HA | `CI-001`, `CI-005` | `evidence/tests/integration/<suite>.json` |
| Negative | Prove forbidden behavior fails closed with no side effects. | B/ES/EPXM/HA | `CI-003`, `CI-006` | `evidence/tests/negative/<suite>.json` |
| Fuzz | Exercise parsers, ABIs, manifests, command pages, and record decoders. | B/ES/EPXM/HA where parser exists | `CI-012` | `evidence/fuzz/<target>.md` |
| Conformance | Prove profile requirement status and supported/unsupported features. | B/ES/EPXM/HA by claim | `CI-014`, `CI-015` | `evidence/conformance/<release>.md` |
| Crash-recovery | Prove transaction and recovery state after interruption. | B/ES/EPXM/HA for stateful services | `CI-005`, `CI-006` | `evidence/tests/crash-recovery/<suite>.json` |
| Fault-injection | Prove fail-closed behavior under dependency, hardware, storage, audit, or Guard faults. | B/ES/EPXM/HA; stronger in ES/EPXM/HA | `CI-003`, `CI-005`, `CI-006` | `evidence/tests/fault-injection/<suite>.json` |
| Supply-chain | Prove dependency, SBOM, provenance, update, and reproducibility controls. | ES/EPXM/HA required; B recommended | `CI-008`, `CI-009`, `CI-010`, `CI-011` | `evidence/supply-chain/<release>/` |
| Formal-model | Check state-machine and invariant models against implementation traces. | B recommended; HA required for core/security/Guard | `CI-015` | `evidence/formal/<model>.md` |
| Release-gate | Prove production and profile gates pass before claims. | B/ES/EPXM/HA releases | `CI-013`, `CI-014`, `CI-015` | `evidence/release/<release>.md` |

## 6. Requirement Namespace Coverage

| Requirement namespace | Required test classes | Source IDs | Required evidence | Profile applicability |
| --- | --- | --- | --- | --- |
| `MFOS-REQ-PROFILE-*` | conformance, release-gate | `FBVBS-001`, `NIST-160-001` | conformance statement, profile claim review | B/ES/EPXM/HA |
| `MFOS-REQ-SOURCE-*` | conformance, release-gate, negative wording tests | concept-specific IBM IDs, `FBVBS-001` | source matrix lint, wording lint | B/ES/EPXM/HA |
| `MFOS-REQ-GLOSS-*` | unit lint, conformance | concept-specific IBM/x64 IDs | glossary lint report | B/ES/EPXM/HA |
| `MFOS-REQ-THR-*` | negative, fault-injection, formal-model | `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `FBVBS-001` | threat-to-test traceability | B/ES/EPXM/HA |
| `MFOS-REQ-SYSINT-*` | negative, integration, fuzz, formal-model, release-gate | `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, x64 IDs | system-integrity negative report | B/ES/EPXM/HA |
| `MFOS-REQ-OBJ-*` | unit, negative, fuzz, conformance | object-model source IDs | schema/fuzz evidence | B/ES/EPXM/HA |
| `MFOS-REQ-AUTH-*` | unit, integration, negative, fuzz, formal-model | `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001`, `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `FBVBS-001` | authorization trace report | B/ES/EPXM/HA |
| `MFOS-REQ-AUDIT-*` | unit, integration, negative, fuzz, crash-recovery, fault-injection | `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001`, `FBVBS-001` | audit-chain and ordering reports | B/ES/EPXM/HA; remote export ES/EPXM/HA; Guard root HA |
| `MFOS-REQ-CATALOG-*` | unit, integration, negative, fuzz, crash-recovery | `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001` | catalog transaction/recovery report | B/ES/EPXM/HA |
| `MFOS-REQ-DATASET-*` | unit, integration, negative, fuzz, fault-injection | `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001` | dataset handle and integrity report | B/ES/EPXM/HA |
| `MFOS-REQ-JOB-*` | unit, integration, negative, fuzz, conformance | `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-JES-JOB-FLOW-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001` | job lifecycle report | B/ES/EPXM/HA |
| `MFOS-REQ-SPOOL-*` | unit, integration, negative, fault-injection | `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001` | spool access report | B/ES/EPXM/HA |
| `MFOS-REQ-OPER-*` | unit, integration, negative, fuzz, release-gate | `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001` | operator drill report | B/ES/EPXM/HA |
| `MFOS-REQ-WPOL-*` | unit, integration, negative, conformance | `EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001`, `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001` | workload policy report | B/ES/EPXM/HA |
| `MFOS-REQ-AMF-*` | unit, integration, negative, fuzz, fault-injection, release-gate | `EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, x64 IDs | AMF load/revocation report | B/ES/EPXM/HA; Guard registry HA |
| `MFOS-REQ-UPDATE-*` | unit, integration, negative, fuzz, supply-chain, crash-recovery | `TUF-001`, `SLSA-001`, `NIST-218-001`, `NIST-193-001` | update attack report | B/ES/EPXM/HA; TUF-like ES/EPXM/HA |
| `MFOS-REQ-NUCLEUS-*` | unit, integration, negative, fuzz, fault-injection, formal-model | `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, x64 IDs, `FBVBS-001` | nucleus isolation/ABI report | B/ES/EPXM/HA |
| `MFOS-REQ-SVC-*` | unit, negative, fuzz, formal-model | `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, x64 IDs | SVC ABI report | B/ES/EPXM/HA |
| `MFOS-REQ-PCALL-*` | unit, integration, negative, fuzz, formal-model | `EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001`, `EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001`, `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001` | PCALL endpoint report | B/ES/EPXM/HA |
| `MFOS-REQ-PARTITION-*` | unit, integration, negative, fuzz, fault-injection, formal-model, conformance | `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `EXTREF-IBM-Z-DPM-0001`, x64 IDs, `TCG-001` | partition/device teardown report | ES/EPXM/HA when PXM claimed; HA required |
| `MFOS-REQ-GUARD-*` | unit, integration, negative, fuzz, fault-injection, formal-model, release-gate | `MS-VBS-001`, `MS-VSM-001`, `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, x64 IDs | Guard root/attestation report | HA |
| `MFOS-REQ-LGW-*` | integration, negative, fuzz, fault-injection, conformance | `EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001`, `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001` | gateway boundary report | ES/EPXM/HA; Dev exceptions explicit |
| `MFOS-REQ-AI-*` | lint, negative, release-gate | `FBVBS-001`, `NIST-218-001` | AI contract lint report | B/ES/EPXM/HA |
| `MFOS-REQ-QUALITY-*` | supply-chain, conformance, release-gate | `NIST-160-001`, `NIST-218-001`, `SLSA-001`, `SEL4-001` | quality/supply-chain evidence | B/ES/EPXM/HA; supply-chain ES/EPXM/HA |
| `MFOS-REQ-CONF-*` | conformance, release-gate | `FBVBS-001` | conformance matrix | B/ES/EPXM/HA |
| `MFOS-REQ-PROD-*` | release-gate, negative, supply-chain, fault-injection | production readiness source IDs | production gate evidence | B/ES/EPXM/HA production claims |
| `MFOS-REQ-FM-*` | formal-model, trace checking | `SEL4-001`, `NIST-160-001`, `FBVBS-001` | model output and review | HA required for core/security/Guard |

## 7. CI Gate Mapping

| CI gate | Test responsibility | Minimum profile | Fails when |
| --- | --- | --- | --- |
| `CI-001` spec ID required | Unit/integration/negative/conformance tests must name `MFOS-REQ-*`. | B/ES/EPXM/HA | test or code lacks requirement traceability |
| `CI-002` source matrix refs | Source-grounded tests must cite Source Matrix IDs. | B/ES/EPXM/HA | IBM/x64/update/supply-chain concept lacks source ID |
| `CI-003` no fake success | Negative/fault/release tests prove no fake success. | B/ES/EPXM/HA | unsupported, spec gap, or dependency failure returns success |
| `CI-004` TODO/unimplemented | Release-gate tests scan production paths. | B/ES/EPXM/HA | production path has unapproved placeholder |
| `CI-005` audit obligation | Integration and release tests verify audit obligations. | B/ES/EPXM/HA | protected operation lacks required audit |
| `CI-006` negative test required | Security-sensitive changes need negative tests. | B/ES/EPXM/HA | negative test absent or no side-effect assertion |
| `CI-007` unsafe inventory | Unit/fuzz/review tests cover unsafe code contracts. | B/ES/EPXM/HA | unsafe block lacks contract/evidence |
| `CI-008` dependency allowlist | Supply-chain tests validate dependencies. | B/ES/EPXM/HA; release ES/EPXM/HA | unapproved dependency |
| `CI-009` SBOM | Supply-chain release tests produce SBOM. | ES/EPXM/HA required; B recommended | SBOM missing or incomplete |
| `CI-010` signed provenance | Supply-chain release tests produce provenance. | ES/EPXM/HA required; B recommended | provenance missing or invalid |
| `CI-011` reproducible build diff | Supply-chain release tests compare builds. | ES/EPXM/HA | unexplained non-reproducibility |
| `CI-012` fuzz registration | Fuzz tests register parser/binary-interface targets. | B/ES/EPXM/HA where parser exists | parser or ABI lacks fuzz target |
| `CI-013` prohibited wording | Release-gate tests scan docs and release material. | B/ES/EPXM/HA | forbidden external-compatibility wording appears |
| `CI-014` profile claim | Conformance/release tests validate claimed profile. | B/ES/EPXM/HA | claim exceeds evidence |
| `CI-015` evidence manifest | Release-gate tests verify evidence references. | B/ES/EPXM/HA release candidates | evidence missing, stale, or not linked |

## 8. Evidence Manifest

Every test report MUST be machine-readable or have a machine-readable index:

```yaml
TestEvidence:
  evidence_id: string
  test_id: string
  test_class: unit | integration | negative | fuzz | conformance | crash_recovery | fault_injection | supply_chain | formal_model | release_gate
  requirement_ids: [string]
  source_matrix_ids: [string]
  profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance | Dev
  component: string
  test_command: string?
  result: PASS | FAIL | BLOCKED | SKIPPED
  skip_reason: string?
  unsupported_features: [string]
  spec_gaps: [string]
  side_effect_assertions: [string]
  audit_record_refs: [string]
  artifacts: [string]
  reviewer: string?
  timestamp_utc: string
```

Rules:

- `SKIPPED` is never a pass.
- `BLOCKED` blocks the related claim.
- Negative tests MUST list side-effect assertions.
- Audit-sensitive tests MUST list audit record references or a justified audit-failure result.
- Release-gate evidence MUST include a requirement status matrix.

## 9. Profile-Specific Strategy

### Baseline

Baseline requires:

- Unit and integration tests for core hosted or nucleus-backed services.
- Negative tests for all security-sensitive paths.
- Fuzz target registration for every implemented parser or binary interface.
- Audit ordering tests for protected-resource deny paths.
- No-fake-success and spec-gap tests.
- Conformance tests for the claimed Baseline scope.

Baseline does not require:

- PXM hardware tests unless PXM is claimed.
- Guard tests unless optional Guard helper behavior is claimed.
- Remote audit export tests unless implemented.
- SBOM/provenance as hard conformance, though they are recommended.

### Enterprise-Standalone

Enterprise-Standalone adds:

- Secure/measured boot test evidence.
- TPM and measurement-binding tests where secrets or attestations are claimed.
- Remote audit export tests.
- TUF-like update metadata tests.
- Rollback, freeze, and mix-and-match tests.
- AMF revocation tests.
- SBOM, signed provenance, dependency allowlist, reproducible build diff tests.
- Platform DMA protection tests where claimed.

### Enterprise-PXM

Enterprise-PXM adds all Enterprise-Standalone tests plus:

- PXM partition lifecycle tests.
- IOMMU and interrupt remapping tests for cross-partition device assignment.
- Device teardown negative tests.
- Side-partition isolation tests.
- Partition audit tests.

### High-Assurance

High-Assurance adds:

- PXM required tests.
- Guard root transition tests.
- Guard sealed security root and audit root tests.
- Guard executable mapping and SVC table verification tests.
- Guard AMF registry tests.
- Attestation nonce tests.
- Formal model evidence for core, security, and Guard state machines.
- Independent review evidence for TCB changes.

## 10. Security-Sensitive Test Requirements

The following changes always require negative tests:

```text
authorization decision
audit append/query/export/retention
dataset handle issue
catalog transaction
job effective identity
spool browse/export/purge
operator command execution
workload policy activation
AMF load/registry/update
update stage/activate/commit/rollback
SVC/PCALL entry
nucleus mapping or handle logic
PXM partition or device operation
Guard root transition
Linux/Desktop gateway operation
release or conformance claim
```

Required negative categories:

| Category | Required absence assertion |
| --- | --- |
| Unauthorized access | no handle, no content, no state transition |
| Stale handle | handle rejected, no access, audit when required |
| Policy version mismatch | no side effect, typed failure |
| Audit write failure | no protected success unless profile explicitly permits degraded non-security path |
| Malformed input | no object creation, no commit |
| Replay attempt | request/token/sequence rejected |
| Downgrade/rollback/freeze/mix-and-match | artifact or root not activated |
| Concurrent update | one committed outcome or fail-closed recovery |
| Crash mid-transaction | committed state is consistent, incomplete state rolled back |
| Privilege confusion | caller identity/role/authority not broadened |
| Cross-partition misuse | partition boundary preserved |
| AMF invalid/revoked | no module registered, no executable mapping |
| Guard root mismatch | no root advanced, lockdown/fail-closed as specified |
| Unsupported/spec-gap success attempt | no success, typed error |
| Device teardown incomplete | no reassignment, no memory reuse |

## 11. Fuzz Strategy

Fuzz targets are required for:

| Target | Requirement namespaces | Primary evidence |
| --- | --- | --- |
| DSN grammar | `MFOS-REQ-CATALOG-*`, `MFOS-REQ-DATASET-*` | DSN fuzz report |
| JCL-like job syntax | `MFOS-REQ-JOB-*` | job parser fuzz report |
| Operator command grammar | `MFOS-REQ-OPER-*` | operator fuzz report |
| Policy language and decision request | `MFOS-REQ-AUTH-*` | policy fuzz report |
| Object schemas | `MFOS-REQ-OBJ-*` | schema fuzz report |
| Audit records and payloads | `MFOS-REQ-AUDIT-*` | audit fuzz report |
| AMF manifest | `MFOS-REQ-AMF-*` | AMF manifest fuzz report |
| Update metadata and artifact manifest | `MFOS-REQ-UPDATE-*` | update fuzz report |
| SVC request decoding | `MFOS-REQ-SVC-*`, `MFOS-REQ-NUCLEUS-*` | SVC fuzz report |
| PCALL request decoding | `MFOS-REQ-PCALL-*` | PCALL fuzz report |
| PXM command pages and activation profiles | `MFOS-REQ-PARTITION-*` | PXM fuzz report |
| Guard calls and root payloads | `MFOS-REQ-GUARD-*` | Guard fuzz report |
| Gateway requests/tokens | `MFOS-REQ-LGW-*` | gateway fuzz report |

Fuzz failures MUST be triaged as:

- parser bug
- resource exhaustion bug
- spec ambiguity
- acceptable rejection
- implementation bug
- harness bug

Spec ambiguity becomes `SPEC_GAP` and must not be converted to runtime success.

## 12. Formal-Model Strategy

Formal-model tests bridge `24-formal-methods.md` and implementation:

| Model | Requirements | Required profile | Test output |
| --- | --- | --- | --- |
| `FORMAL-001` authorization decision | `MFOS-REQ-AUTH-*`, `MFOS-REQ-SYSINT-*` | HA required; B/E recommended | model check + trace checker |
| `FORMAL-002` dataset open invariant | `MFOS-REQ-DATASET-*`, `MFOS-REQ-OBJ-*` | HA required; B/E recommended | stale-handle proof/test |
| `FORMAL-003` audit append invariant | `MFOS-REQ-AUDIT-*` | HA required; B/E recommended | audit-before-result model |
| `FORMAL-004` catalog transaction | `MFOS-REQ-CATALOG-*` | ES/EPXM/HA recommended | crash transition model |
| `FORMAL-005` job lifecycle | `MFOS-REQ-JOB-*` | HA recommended | lifecycle model |
| `FORMAL-006` spool access | `MFOS-REQ-SPOOL-*` | HA recommended | access model |
| `FORMAL-007` operator command | `MFOS-REQ-OPER-*` | HA recommended | command transition model |
| `FORMAL-008` AMF load | `MFOS-REQ-AMF-*` | HA required when AMF HA claimed | load model |
| `FORMAL-009` update rollback/freeze | `MFOS-REQ-UPDATE-*` | ES/EPXM/HA recommended | update attack model |
| `FORMAL-010` PXM lifecycle | `MFOS-REQ-PARTITION-*` | HA required | partition state model |
| `FORMAL-011` device teardown | `MFOS-REQ-PARTITION-*` | HA required for passthrough | teardown model |
| `FORMAL-012` Guard root transition | `MFOS-REQ-GUARD-*` | HA required | root transition model |

Formal evidence is not a substitute for executable tests. It is an additional gate for claims involving invariants, state transitions, and High-Assurance roots.

## 13. Release-Gate Strategy

Release-gate tests aggregate lower-level tests into claims:

| Gate | Required test classes | Blocking evidence |
| --- | --- | --- |
| `PROD-001` Source Matrix complete | conformance, release-gate | source matrix lint, wording lint |
| `PROD-002` System Integrity negative tests | negative, fuzz, formal-model | system integrity report |
| `PROD-003` Unauthorized dataset no handle | integration, negative | dataset deny evidence |
| `PROD-004` DENY audit before result | integration, negative, fault-injection | audit ordering evidence |
| `PROD-005` Catalog crash recovery | crash-recovery, fault-injection | catalog recovery evidence |
| `PROD-006` Spool security | integration, negative | spool access evidence |
| `PROD-007` Operator authority/audit | integration, negative, release-gate | operator drill evidence |
| `PROD-008` AMF invalid/revoked fail closed | negative, fuzz, fault-injection | AMF evidence |
| `PROD-009` Update attack tests | negative, supply-chain, crash-recovery | update evidence |
| `PROD-010` SBOM/provenance | supply-chain | SBOM and provenance |
| `PROD-011` no fake success | negative, release-gate | CI-003 report |
| `PROD-012` parser fuzz campaigns | fuzz | fuzz campaign report |
| `PROD-013` PXM device teardown | negative, fault-injection, formal-model | teardown evidence |
| `PROD-014` Guard evidence | integration, negative, formal-model, release-gate | Guard root evidence |
| `PROD-015` Recovery drill | crash-recovery, fault-injection, release-gate | recovery drill record |

## 14. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| `MFOS-REQ-TEST-0001` | Every test suite MUST list requirement IDs. | `CI-001` |
| `MFOS-REQ-TEST-0002` | Source-grounded test suites MUST list Source Matrix IDs. | `CI-002` |
| `MFOS-REQ-TEST-0003` | Security-sensitive changes MUST include negative tests with side-effect absence assertions. | `CI-006` / review |
| `MFOS-REQ-TEST-0004` | Parser and binary-interface changes MUST include fuzz target registration. | `CI-012` |
| `MFOS-REQ-TEST-0005` | Protected-resource integration tests MUST verify audit obligations. | `CI-005` |
| `MFOS-REQ-TEST-0006` | `UNSUPPORTED` and `SPEC_GAP` paths MUST be tested as fail-closed. | `CI-003` |
| `MFOS-REQ-TEST-0007` | Release-gate tests MUST include evidence artifact manifests. | `CI-015` |
| `MFOS-REQ-TEST-0008` | Conformance tests MUST verify profile applicability and unsupported feature status. | `CI-014` |
| `MFOS-REQ-TEST-0009` | Crash-recovery tests MUST validate committed state, rolled-back state, and recovery evidence. | crash-recovery review |
| `MFOS-REQ-TEST-0010` | Fault-injection tests MUST verify fail-closed behavior for required dependencies. | fault-injection review |
| `MFOS-REQ-TEST-0011` | Supply-chain tests MUST verify dependency allowlist, SBOM, provenance, and reproducible-build status where applicable. | supply-chain audit |
| `MFOS-REQ-TEST-0012` | Formal-model tests MUST map model invariants to implementation traces before High-Assurance claims. | formal evidence review |

## 15. Strategy Gaps

| Gap ID | Gap | Impact |
| --- | --- | --- |
| `TEST-GAP-001` | Final test runner and report schema are not implemented. | Blocks automated evidence collection. |
| `TEST-GAP-002` | Fuzz campaign duration and coverage thresholds are not defined. | Blocks final production fuzz sufficiency claims. |
| `TEST-GAP-003` | Formal tool choice and CI harness are not fixed. | Blocks automated formal-model gates. |
| `TEST-GAP-004` | Hardware lab matrix for PXM/Guard/platform tests is incomplete. | Blocks platform-specific Enterprise-Standalone/Enterprise-PXM/HA claims. |
| `TEST-GAP-005` | Remote audit collector and supply-chain signing infrastructure are not finalized. | Blocks full Enterprise release testing. |
| `TEST-GAP-006` | Evidence artifact manifest checker is specified but not implemented. | Blocks reliable release-gate automation. |

## 16. AI Test-Author Prompt

```text
You are writing MFOS tests.

Constraints:
- Edit only files assigned to you.
- Do not make external compatibility claims.
- Every test must list requirement IDs.
- Source-grounded tests must list Source Matrix IDs.
- Security-sensitive tests must include negative cases.
- Negative tests must assert absence of success side effects.
- Parser and ABI tests must include fuzz target registration.
- Protected-resource tests must verify authorization and audit obligations.
- Unsupported behavior must fail closed as UNSUPPORTED.
- Undefined behavior must fail closed as SPEC_GAP.
- Evidence artifacts must be named even if not generated in this task.

Required output:
1. Requirement IDs
2. Source Matrix IDs
3. Test Classes
4. Profiles Covered
5. Positive Tests
6. Negative Tests
7. Fuzz Targets
8. Crash/Fault Tests
9. Evidence Artifacts
10. Gaps and Blockers
```
