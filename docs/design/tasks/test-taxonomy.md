# MFOS Test Taxonomy v0.1

Status: Draft design split

Owner area: `docs/design/tasks/test-taxonomy.md`

This task document turns `docs/design/specs/29-test-strategy.md` into an assignment-ready taxonomy for AI agents and reviewers. It defines test IDs, ownership boundaries, evidence names, profile applicability, and requirement/source mappings.

MFOS is source-grounded and z/OS-inspired. Test names and reports MUST NOT imply external platform compatibility.

## 1. Test ID Scheme

Use stable IDs:

```text
<AREA>-<CLASS>-<NNNN>
```

Where:

```text
AREA:
  SRC, GLOSS, THR, SI, OBJ, SEC, AUD, CAT, DATA, JOB, SPL,
  OPER, workload policy, AMF, UVS, NUC, SVC, PCALL, PXM, GRD, LGW,
  AI, QUAL, CONF, PROD, FM

CLASS:
  UNIT
  INT
  NEG
  FUZZ
  CONF
  CRASH
  FAULT
  SUPPLY
  FORMAL
  REL
```

Examples:

```text
SEC-NEG-0001
AUD-INT-0001
CAT-CRASH-0001
UVS-SUPPLY-0001
GRD-FORMAL-0001
PROD-REL-0014
```

Rules:

- A test ID MUST be unique.
- A test file MAY contain multiple test IDs only when they share setup and evidence.
- A negative test MUST include at least one absence assertion.
- A fuzz target MUST have a `FUZZ` ID even if it also backs unit tests.
- Release-gate tests use `PROD-REL-*`.

## 2. Directory Taxonomy

The intended repository layout is:

```text
tests/
  unit/
  integration/
  negative/
  fuzz/
  conformance/
  crash-recovery/
  fault-injection/
  supply-chain/
  formal-model/
  release-gate/
```

Evidence layout:

```text
evidence/
  tests/
    unit/
    integration/
    negative/
    conformance/
    crash-recovery/
    fault-injection/
  fuzz/
  formal/
  supply-chain/
  release/
  production/
```

## 3. Taxonomy by Test Class

| Class | Required when | Test ID examples | CI gates | Evidence |
| --- | --- | --- | --- | --- |
| Unit | local schema, parser helpers, state transition, typed error, policy rule | `OBJ-UNIT-0001`, `SEC-UNIT-0001`, `AUD-UNIT-0001` | `CI-001`, `CI-003` | `evidence/tests/unit/*.json` |
| Integration | services interact or ordering matters | `DATA-INT-0001`, `JOB-INT-0001`, `OPER-INT-0001` | `CI-001`, `CI-005` | `evidence/tests/integration/*.json` |
| Negative | protected resource, system interface, profile claim, update, AMF, PXM, Guard | `SEC-NEG-0001`, `PXM-NEG-0001` | `CI-003`, `CI-006` | `evidence/tests/negative/*.json` |
| Fuzz | parser, decoder, manifest, command grammar, ABI, command page, token | `JOB-FUZZ-0001`, `SVC-FUZZ-0001` | `CI-012` | `evidence/fuzz/*.md` |
| Conformance | profile or requirement status claim | `CONF-CONF-0001` | `CI-014`, `CI-015` | `evidence/conformance/*.md` |
| Crash-recovery | transaction, journal, activation, update, recovery workflow | `CAT-CRASH-0001`, `UVS-CRASH-0001` | `CI-005`, `CI-006` | `evidence/tests/crash-recovery/*.json` |
| Fault-injection | required dependency, storage, audit, platform, Guard, IOMMU failure | `AUD-FAULT-0001`, `GRD-FAULT-0001` | `CI-003`, `CI-005`, `CI-006` | `evidence/tests/fault-injection/*.json` |
| Supply-chain | dependencies, SBOM, provenance, reproducibility, update metadata | `QUAL-SUPPLY-0001`, `UVS-SUPPLY-0001` | `CI-008` through `CI-011` | `evidence/supply-chain/*` |
| Formal-model | invariant/model checking and trace checking | `FM-FORMAL-0001` | `CI-015` | `evidence/formal/*.md` |
| Release-gate | production/profile release gates | `PROD-REL-0001` | `CI-013`, `CI-014`, `CI-015` | `evidence/release/*.md` |

## 4. Area Taxonomy

### 4.1 Source, Glossary, Threat, and Claims

| Area | Requirement namespaces | Source IDs | Required classes | Profiles | Evidence |
| --- | --- | --- | --- | --- | --- |
| `SRC` | `MFOS-REQ-SOURCE-*` | concept-specific IBM IDs, `FBVBS-001` | unit lint, negative wording, conformance, release-gate | B/ES/EPXM/HA | source matrix lint report |
| `GLOSS` | `MFOS-REQ-GLOSS-*` | glossary source IDs | unit lint, conformance | B/ES/EPXM/HA | glossary lint report |
| `THR` | `MFOS-REQ-THR-*` | threat model source IDs | negative, fault, formal, conformance | B/ES/EPXM/HA | threat-to-test matrix |
| `CONF` | `MFOS-REQ-CONF-*` | `FBVBS-001` | conformance, release-gate | B/ES/EPXM/HA | conformance statement |
| `PROD` | `MFOS-REQ-PROD-*`, `PROD-*` | production gate source IDs | release-gate, negative, supply-chain | B/ES/EPXM/HA production | production gate package |

Seed tests:

| Test ID | Purpose | Requirements | CI |
| --- | --- | --- | --- |
| `SRC-REL-0001` | Scan release text for prohibited compatibility wording. | `MFOS-REQ-SOURCE-0003`, `MFOS-REQ-AI-0003` | `CI-013` |
| `SRC-UNIT-0001` | Require Source Matrix ID for source-grounded concept entries. | `MFOS-REQ-SOURCE-0001` | `CI-002` |
| `THR-NEG-0001` | Verify every listed abuse case maps to at least one negative test. | `MFOS-REQ-THR-0009` | `CI-006` |
| `CONF-CONF-0001` | Verify a release names exactly one claimed profile. | `MFOS-REQ-CONF-0001` | `CI-014` |

### 4.2 System Integrity, Object Model, Authorization, and Audit

| Area | Requirement namespaces | Source IDs | Required classes | Profiles | Evidence |
| --- | --- | --- | --- | --- | --- |
| `SI` | `MFOS-REQ-SYSINT-*` | `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001`, x64 IDs | negative, integration, fuzz, formal, release-gate | B/ES/EPXM/HA | system integrity report |
| `OBJ` | `MFOS-REQ-OBJ-*` | object-model source IDs | unit, negative, fuzz, conformance | B/ES/EPXM/HA | object schema report |
| `SEC` | `MFOS-REQ-AUTH-*` | `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001` | unit, integration, negative, fuzz, formal | B/ES/EPXM/HA | authorization trace report |
| `AUD` | `MFOS-REQ-AUDIT-*` | `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001`, `FBVBS-001` | unit, integration, negative, fuzz, crash, fault | B/ES/EPXM/HA; export ES/EPXM/HA; Guard HA | audit chain report |

Seed tests:

| Test ID | Purpose | Requirements | CI |
| --- | --- | --- | --- |
| `SI-NEG-0001` | Unauthorized subject cannot bypass protected resource controls through system interface. | `MFOS-REQ-SYSINT-0001` | `CI-003`, `CI-006` |
| `SI-NEG-0002` | Unsupported system interface returns `UNSUPPORTED`, not success. | `MFOS-REQ-SYSINT-0010` | `CI-003` |
| `OBJ-UNIT-0001` | Protected object schema requires object type and object ID. | `MFOS-REQ-OBJ-0001` | `CI-001` |
| `OBJ-NEG-0001` | Unknown object class returns `SPEC_GAP`, not success. | `MFOS-REQ-OBJ-0010` | `CI-003` |
| `SEC-INT-0001` | `securityd` decision includes subject/object/operation/context/policy version. | `MFOS-REQ-AUTH-0002` | `CI-001` |
| `SEC-NEG-0001` | BOB cannot read ALICE dataset; no dataset handle exists. | `MFOS-REQ-AUTH-0004`, `MFOS-REQ-DATASET-0002` | `CI-006` |
| `SEC-NEG-0002` | Caller-supplied identity cannot override trusted context. | `MFOS-REQ-AUTH-0015` | `CI-006` |
| `AUD-INT-0001` | DENY audit is durable before caller receives final denial. | `MFOS-REQ-AUDIT-0002` | `CI-005` |
| `AUD-NEG-0001` | Spool output cannot satisfy audit evidence. | `MFOS-REQ-AUDIT-0008` | `CI-006` |
| `AUD-FAULT-0001` | Required audit append failure causes fail-closed protected operation. | `MFOS-REQ-AUDIT-0005` | `CI-005`, `CI-006` |

### 4.3 Dataset, Catalog, Job, Spool, Operator, and workload policy

| Area | Requirement namespaces | Source IDs | Required classes | Profiles | Evidence |
| --- | --- | --- | --- | --- | --- |
| `CAT` | `MFOS-REQ-CATALOG-*` | `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001` | unit, integration, negative, fuzz, crash | B/ES/EPXM/HA | catalog transaction report |
| `DATA` | `MFOS-REQ-DATASET-*` | `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001` | unit, integration, negative, fault | B/ES/EPXM/HA | dataset handle report |
| `JOB` | `MFOS-REQ-JOB-*` | `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-JES-JOB-FLOW-0001` | unit, integration, negative, fuzz, conformance | B/ES/EPXM/HA | job lifecycle report |
| `SPL` | `MFOS-REQ-SPOOL-*` | `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001` | unit, integration, negative, fault | B/ES/EPXM/HA | spool security report |
| `OPER` | `MFOS-REQ-OPER-*` | operator source IDs | unit, integration, negative, fuzz, release-gate | B/ES/EPXM/HA | operator drill report |
| `WLM` | `MFOS-REQ-WPOL-*` | `EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001` | unit, integration, negative, conformance | B/ES/EPXM/HA | workload policy report |

Seed tests:

| Test ID | Purpose | Requirements | CI |
| --- | --- | --- | --- |
| `CAT-FUZZ-0001` | DSN grammar fuzz target. | `MFOS-REQ-CATALOG-0001` | `CI-012` |
| `CAT-CRASH-0001` | Crash after journal write recovers without phantom committed entry. | `MFOS-REQ-CATALOG-0005` | `CI-006` |
| `DATA-NEG-0001` | Unauthorized dataset open creates no handle. | `MFOS-REQ-DATASET-0002` | `CI-006` |
| `DATA-NEG-0002` | Stale catalog generation rejects dataset handle. | `MFOS-REQ-DATASET-0001` | `CI-006` |
| `JOB-FUZZ-0001` | JCL-like parser fuzz target. | `MFOS-REQ-JOB-0002` | `CI-012` |
| `JOB-NEG-0001` | Job conversion failure does not enqueue executable work. | `MFOS-REQ-JOB-0007` | `CI-006` |
| `SPL-NEG-0001` | Unauthorized spool browse returns no content. | `MFOS-REQ-SPOOL-0002` | `CI-006` |
| `OPER-FUZZ-0001` | Operator command grammar fuzz target. | `MFOS-REQ-OPER-0002` | `CI-012` |
| `OPER-NEG-0001` | Raw command text cannot execute directly. | `MFOS-REQ-OPER-0009` | `CI-006` |
| `WPOL-NEG-0001` | workload policy dispatch hint cannot grant dataset access. | `MFOS-REQ-WPOL-0012`, `MFOS-REQ-SYSINT-0012` | `CI-006` |

### 4.4 AMF, Update, Nucleus, SVC, and PCALL

| Area | Requirement namespaces | Source IDs | Required classes | Profiles | Evidence |
| --- | --- | --- | --- | --- | --- |
| `AMF` | `MFOS-REQ-AMF-*` | `EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, x64 IDs | unit, integration, negative, fuzz, fault, release-gate | B/ES/EPXM/HA; Guard registry HA | AMF evidence |
| `UVS` | `MFOS-REQ-UPDATE-*` | `TUF-001`, `SLSA-001`, `NIST-218-001` | unit, integration, negative, fuzz, crash, supply-chain | B/ES/EPXM/HA; TUF-like ES/EPXM/HA | update evidence |
| `NUC` | `MFOS-REQ-NUCLEUS-*` | `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, x64 IDs | unit, integration, negative, fuzz, fault, formal | B/ES/EPXM/HA | nucleus evidence |
| `SVC` | `MFOS-REQ-SVC-*` | `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`, x64 IDs | unit, negative, fuzz, formal | B/ES/EPXM/HA | SVC ABI report |
| `PCALL` | `MFOS-REQ-PCALL-*` | `EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001`, `EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001` | unit, integration, negative, fuzz, formal | B/ES/EPXM/HA | PCALL report |

Seed tests:

| Test ID | Purpose | Requirements | CI |
| --- | --- | --- | --- |
| `AMF-NEG-0001` | Invalid signature fails closed; no module registered. | `MFOS-REQ-AMF-0001`, `MFOS-REQ-AMF-0020` | `CI-006` |
| `AMF-NEG-0002` | Revoked signer fails closed; no executable mapping. | `MFOS-REQ-AMF-0005` | `CI-006` |
| `AMF-FUZZ-0001` | AMF manifest fuzz target. | `MFOS-REQ-AMF-0008` | `CI-012` |
| `UVS-NEG-0001` | Unsigned artifact cannot activate. | `MFOS-REQ-UPDATE-0015` | `CI-006` |
| `UVS-SUPPLY-0001` | Rollback, freeze, and mix-and-match metadata are rejected. | `MFOS-REQ-UPDATE-0004`, `MFOS-REQ-UPDATE-0005`, `MFOS-REQ-UPDATE-0006` | `CI-008` |
| `UVS-CRASH-0001` | Crash before update commit enters recovery rollback workflow. | `MFOS-REQ-UPDATE-0017` | `CI-006` |
| `NUC-NEG-0001` | Writable executable mapping request is rejected. | `MFOS-REQ-NUCLEUS-0020` | `CI-006` |
| `SVC-FUZZ-0001` | SVC request decoder fuzz target. | `MFOS-REQ-SVC-0010` | `CI-012` |
| `SVC-NEG-0001` | SVC caller identity is derived from nucleus context, not request payload. | `MFOS-REQ-SVC-0002` | `CI-006` |
| `PCALL-NEG-0001` | Arbitrary cross-address-space pointer access is rejected. | `MFOS-REQ-PCALL-0004` | `CI-006` |

### 4.5 PXM, Guard, Linux Gateway, AI, and Quality

| Area | Requirement namespaces | Source IDs | Required classes | Profiles | Evidence |
| --- | --- | --- | --- | --- | --- |
| `PXM` | `MFOS-REQ-PARTITION-*` | `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `EXTREF-IBM-Z-DPM-0001`, x64 IDs, `TCG-001` | unit, integration, negative, fuzz, fault, formal, conformance | ES/EPXM/HA when claimed; HA required | PXM evidence |
| `GRD` | `MFOS-REQ-GUARD-*` | `MS-VBS-001`, `MS-VSM-001`, `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, x64 IDs | unit, integration, negative, fuzz, fault, formal, release-gate | HA | Guard evidence |
| `LGW` | `MFOS-REQ-LGW-*` | `EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001`, `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`, `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001` | integration, negative, fuzz, fault, conformance | ES/EPXM/HA; Dev explicit | gateway evidence |
| `AI` | `MFOS-REQ-AI-*` | `FBVBS-001`, `NIST-218-001` | lint, negative, release-gate | B/ES/EPXM/HA | AI contract lint |
| `QUAL` | `MFOS-REQ-QUALITY-*` | `NIST-160-001`, `NIST-218-001`, `SLSA-001`, `SEL4-001` | supply-chain, conformance, release-gate | B/ES/EPXM/HA; supply-chain ES/EPXM/HA | quality evidence |

Seed tests:

| Test ID | Purpose | Requirements | CI |
| --- | --- | --- | --- |
| `PXM-NEG-0001` | Device reassignment denied before teardown checklist completion. | `MFOS-REQ-PARTITION-0006` | `CI-006` |
| `PXM-FAULT-0001` | Missing IOMMU/interrupt remap fails closed for passthrough assignment. | `MFOS-REQ-PARTITION-0016` | `CI-006` |
| `PXM-FORMAL-0001` | Partition lifecycle model rejects invalid transitions. | `MFOS-REQ-PARTITION-0010` | `CI-015` |
| `GRD-NEG-0001` | Guard refuses dataset policy interpretation request. | `MFOS-REQ-GUARD-0003` | `CI-006` |
| `GRD-NEG-0002` | SVC table mismatch triggers lockdown or panic-equivalent path. | `MFOS-REQ-GUARD-0006` | `CI-006` |
| `GRD-FORMAL-0001` | Guard root transition model rejects rollback. | `MFOS-REQ-GUARD-0011` | `CI-015` |
| `LGW-NEG-0001` | Linux root does not map to MFOS operator authority. | `MFOS-REQ-LGW-0009` | `CI-006` |
| `AI-REL-0001` | AI output missing requirement IDs fails review lint. | `MFOS-REQ-AI-0001` | `CI-001` |
| `QUAL-SUPPLY-0001` | Release artifact includes SBOM, signed provenance, dependency allowlist, and reproducible diff status. | `MFOS-REQ-QUALITY-0006`, `MFOS-REQ-QUALITY-0008`, `MFOS-REQ-QUALITY-0009` | `CI-008` through `CI-011` |

## 5. Release-Gate Test Taxonomy

| Test ID | Gate | Required classes | Profiles | Evidence |
| --- | --- | --- | --- | --- |
| `PROD-REL-0001` | `PROD-001` Source Matrix complete | release-gate, conformance | B/ES/EPXM/HA | `evidence/production/PROD-001-source-matrix.md` |
| `PROD-REL-0002` | `PROD-002` System Integrity negative tests | negative, formal | B/ES/EPXM/HA | `evidence/production/PROD-002-system-integrity.md` |
| `PROD-REL-0003` | `PROD-003` Unauthorized dataset no handle | integration, negative | B/ES/EPXM/HA | `evidence/production/PROD-003-dataset-deny.md` |
| `PROD-REL-0004` | `PROD-004` DENY audit before result | integration, negative, fault | B/ES/EPXM/HA | `evidence/production/PROD-004-audit-ordering.md` |
| `PROD-REL-0005` | `PROD-005` Catalog crash recovery | crash-recovery | B/ES/EPXM/HA | `evidence/production/PROD-005-catalog-recovery.md` |
| `PROD-REL-0006` | `PROD-006` Spool security | integration, negative | B/ES/EPXM/HA | `evidence/production/PROD-006-spool-security.md` |
| `PROD-REL-0007` | `PROD-007` Operator authority and audit | integration, negative | B/ES/EPXM/HA | `evidence/production/PROD-007-operator.md` |
| `PROD-REL-0008` | `PROD-008` AMF invalid/revoked fail closed | negative, fault | B/ES/EPXM/HA | `evidence/production/PROD-008-amf.md` |
| `PROD-REL-0009` | `PROD-009` Update attack tests | negative, supply-chain, crash | B/ES/EPXM/HA | `evidence/production/PROD-009-update.md` |
| `PROD-REL-0010` | `PROD-010` SBOM and signed provenance | supply-chain | ES/EPXM/HA required; B recommended | `evidence/production/PROD-010-provenance.md` |
| `PROD-REL-0011` | `PROD-011` No fake success CI clean | negative, release-gate | B/ES/EPXM/HA | `evidence/production/PROD-011-no-fake-success.md` |
| `PROD-REL-0012` | `PROD-012` Parser fuzz campaigns | fuzz | B/ES/EPXM/HA | `evidence/production/PROD-012-fuzz.md` |
| `PROD-REL-0013` | `PROD-013` PXM device teardown | negative, fault, formal | ES/EPXM/HA when PXM claimed | `evidence/production/PROD-013-pxm-teardown.md` |
| `PROD-REL-0014` | `PROD-014` Guard evidence | integration, negative, formal | HA | `evidence/production/PROD-014-guard.md` |
| `PROD-REL-0015` | `PROD-015` Recovery drill | crash, fault, release-gate | B/ES/EPXM/HA | `evidence/production/PROD-015-recovery.md` |

## 6. Assignment Templates

### 6.1 Unit Test Assignment

```text
Owned files:
  tests/unit/<area>/
  evidence/tests/unit/<area>.json

Required:
  - requirement IDs
  - Source Matrix IDs if source-grounded
  - typed error assertions
  - no fake success assertions where applicable
```

### 6.2 Negative Test Assignment

```text
Owned files:
  tests/negative/<area>/
  evidence/tests/negative/<area>.json

Required:
  - unauthorized or malformed input
  - expected typed failure
  - absence of success side effects
  - audit record references when audit is required
  - UNSUPPORTED/SPEC_GAP coverage if relevant
```

### 6.3 Fuzz Assignment

```text
Owned files:
  tests/fuzz/<target>/
  evidence/fuzz/<target>.md

Required:
  - fuzz target ID
  - corpus seed source
  - parser/decoder under test
  - max input size policy
  - crash triage categories
  - side-effect isolation statement
```

### 6.4 Release-Gate Assignment

```text
Owned files:
  tests/release-gate/<gate>/
  evidence/production/<gate>.md

Required:
  - gate ID
  - profile claim
  - requirement status matrix
  - evidence references
  - unsupported features
  - spec gaps
  - residual risks
```

## 7. Test Evidence Minimal Schema

```yaml
TestCase:
  test_id: string
  title: string
  test_class: string
  requirement_ids: [string]
  source_matrix_ids: [string]
  profile_applicability: [Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance | Dev]
  component: string
  setup: string
  action: string
  expected_result: string
  absence_assertions: [string]
  audit_expectations: [string]
  ci_gates: [string]
  evidence_artifacts: [string]
  gaps: [string]
```

## 8. Taxonomy Gaps

| Gap ID | Gap | Impact |
| --- | --- | --- |
| `TAX-GAP-001` | Test runner framework is not selected. | Test IDs and evidence schemas are stable, but execution commands are placeholders. |
| `TAX-GAP-002` | Evidence manifest checker is not implemented. | CI cannot yet enforce all evidence links. |
| `TAX-GAP-003` | Some component specs use existing test IDs that may need migration to this taxonomy. | Requires later alias table. |
| `TAX-GAP-004` | Fuzz duration, corpus quality, and coverage thresholds are not defined. | Blocks production fuzz sufficiency claims. |
| `TAX-GAP-005` | Hardware lab topology for PXM/Guard tests is not defined. | Blocks platform-specific ES/EPXM/HA test scheduling. |
| `TAX-GAP-006` | Formal trace-checker format is not defined. | Blocks automated formal-model evidence. |
| `TAX-GAP-007` | Remote audit export test harness is not defined. | Blocks Enterprise audit export gate automation. |

## 9. AI Test Assignment Prompt

```text
You are assigned MFOS tests.

Use docs/design/specs/29-test-strategy.md and docs/design/tasks/test-taxonomy.md.

Constraints:
- Edit only assigned test and evidence files.
- Do not make external compatibility claims.
- Every test needs requirement IDs.
- Source-grounded tests need Source Matrix IDs.
- Negative tests must assert absence of success side effects.
- Protected-resource tests must verify securityd and auditd obligations.
- Parser or ABI changes require fuzz target registration.
- UNSUPPORTED and SPEC_GAP must fail closed.

Return:
1. Test IDs
2. Requirement IDs
3. Source Matrix IDs
4. Profiles Covered
5. CI Gates Covered
6. Evidence Artifacts
7. Negative Side-Effect Assertions
8. Fuzz Targets
9. Gaps and Blockers
```
