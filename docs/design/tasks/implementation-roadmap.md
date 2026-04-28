# MFOS Implementation Roadmap v0.1

Status: Draft design split

Owner area: `docs/design/tasks/implementation-roadmap.md`

This roadmap extracts and expands Phase 0 through Phase 6 from `docs/design/mfos-design.md` and the split specs. It is written for concurrent AI-assisted development: tasks are small, ownership is explicit, and no agent may overwrite another agent's files or invent missing semantics.

MFOS is source-grounded and z/OS-inspired. It MUST NOT claim compatibility with IBM z/OS, z/Architecture binaries, z/OS APIs, RACF, JES, DFSMS, SMF, workload policy, or JCL.

## 1. Roadmap Principles

1. Documentation and source grounding lead implementation.
2. Hosted semantic prototype precedes nucleus work.
3. `securityd` is the final policy decision point for protected resources.
4. `auditd` is evidence, not diagnostic logging.
5. Dataset/catalog/job/spool/operator semantics are first-class, not POSIX wrappers.
6. PXM is partition lifecycle and isolation, not enterprise OS policy.
7. Guard is High-Assurance root-object protection only.
8. `UNSUPPORTED` and `SPEC_GAP` are distinct and fail closed.
9. No phase may claim production readiness without the production gates.
10. AI agents may work concurrently only when ownership and dependencies are explicit.

## 2. Dependency Spine

```text
Source Matrix
  -> Glossary
  -> System Integrity
  -> Object Model
  -> Authorization Model
  -> Audit Schema
  -> Dataset/Catalog + Job/Spool + Operator
  -> Hosted Vertical Slice
  -> Nucleus + SVC/PCALL
  -> AMF Spec/Disabled Path + Update + workload policy
  -> Enterprise-Standalone Hardening
  -> PXM Core
  -> Guard
```

Hard blockers:

- No protected resource implementation without relevant `MFOS-REQ-*` IDs.
- No source-grounded concept without Source Matrix IDs.
- No security-sensitive implementation without negative tests.
- No successful protected operation without audit obligation handling.
- No PXM device passthrough without IOMMU, interrupt remapping, and teardown tests.
- No High-Assurance claim without Guard evidence.

## 3. Phase Summary

| Phase | Name | Primary objective | Main outputs | Profile target |
| --- | --- | --- | --- | --- |
| 0 | Source and Spec Freeze | Fix source grounding, definitions, requirements, and no-fake-success gates. | Source Matrix, specs, requirement catalog, CI lint seeds. | Baseline design |
| 1 | Hosted Semantic Prototype | Prove enterprise semantics outside the kernel. | Hosted `securityd`, `auditd`, `catalogd`, `datasetd`, `jobd`, `spoold`, `operatord`. | Baseline semantics |
| 2 | Minimal MFOS Nucleus | Boot to operator console with typed handles and SVC/PCALL. | Nucleus, address spaces, service launcher, hosted services ported. | Baseline OS |
| 3 | Baseline Core Semantics | Complete the core vertical slice on MFOS. | Dataset/catalog/job/spool/operator/security/audit plus update/workload policy basics; AMF spec complete but production load disabled. | Baseline conformance candidate |
| 4 | Enterprise-Standalone Hardening | Add measured boot, update hardening, provenance, remote audit, and Enterprise-AMF governance readiness. | Secure/measured boot, TPM bindings, TUF-like metadata, SBOM/provenance, AMF governance evidence. | Enterprise-Standalone candidate |
| 5 | PXM Core Prototype | Run MFOS under partition-aware isolation with device lifecycle discipline. | PXM backend, partition APIs, IOMMU/interrupt remap tests, side partition lab. | Enterprise-PXM candidate |
| 6 | High-Assurance Guard | Protect selected roots after partial OS compromise. | Guard roots, executable mapping policy, SVC table verification, attestation. | High-Assurance candidate |

## 4. Phase 0: Source and Spec Freeze

### Objectives

- Complete Source Matrix v0.1 and concept mappings.
- Freeze normative language and conformance profile semantics.
- Freeze the System Integrity Statement.
- Freeze Object Model, Authorization Model, and Audit Schema v0.1.
- Create requirement catalog and roadmap indices.
- Establish CI seeds for no-fake-success, spec IDs, source IDs, audit obligations, and negative-test requirements.

### Entry Criteria

- `docs/design/mfos-design.md` exists.
- Split specs directory exists.
- Source Matrix skeleton exists.
- No implementation work depends on undefined protected-resource semantics.

### Exit Criteria

```text
Source Matrix v0.1 complete
Glossary v0.1 complete
System Integrity Statement v0.1 approved
Object Model v0.1 approved
Authorization Model v0.1 approved
Audit Schema v0.1 approved
Requirements Catalog v0.1 created
Implementation Roadmap v0.1 created
no-fake-success policy specified for CI
```

### Dependency Ordering

1. Source Matrix and glossary.
2. Normative language and profile semantics.
3. System integrity and threat model.
4. Object, authorization, and audit specs.
5. Dataset/catalog, job/spool, operator, workload policy, AMF, update, nucleus, SVC/PCALL, PXM, Guard, Linux gateway specs.
6. Requirement catalog and roadmap.
7. CI lint specs.

### Phase 0 Task Backlog

| Task | Output | Depends on | AI-safe assignment |
| --- | --- | --- | --- |
| `DOC-001` through `DOC-016` | Source Matrix registrations | none | One source group per agent; edit only assigned source file. |
| `DOC-017` | Source Matrix lint rule spec | Source Matrix IDs | CI/spec agent only. |
| `SPEC-001` through `SPEC-020` | Split specs v0.1 | relevant sources | One spec file per agent. |
| `FORMAL-001` through `FORMAL-012` | draft formal models | state machines | Formal agents work in `formal/` only. |
| `CI-001` through `CI-006` | lint rule definitions | requirement catalog | CI agents work in `ci/` only. |

### Required Evidence

- Source Matrix coverage report.
- Glossary prohibited-wording review.
- Spec review checklist.
- Requirement catalog coverage report.
- CI lint dry-run evidence.

### Phase 0 Gaps

- Threat model split spec is still a blocker for complete abuse-case traceability.
- Formal model language and storage layout are not fixed.
- CI scripts are not yet implemented.

## 5. Phase 1: Hosted Semantic Prototype

Runs on Linux/BSD/macOS for semantics only. This phase intentionally avoids kernel work.

### Objectives

- Implement hosted `securityd`, `auditd`, `catalogd`, `datasetd`, `jobd`, `spoold`, and `operatord`.
- Prove the first vertical slice:
  - operator defines ALICE and dataset.
  - ALICE job reads input and writes SYSOUT.
  - BOB job is denied.
  - DENY audit is durable before result.
- Establish parser fuzz targets for JCL-like input, DSN, operator command, policy, object schemas, and audit records.
- Establish catalog transaction and crash recovery behavior.

### Entry Criteria

- Phase 0 exit criteria met for Object Model, Authorization, Audit, Dataset/Catalog, Job/Spool, and Operator specs.
- Error model includes `UNSUPPORTED` and `SPEC_GAP`.
- Hosted service process model chosen.
- Test harness can run unit, integration, negative, fuzz smoke, crash-recovery, and fault-injection tests.

### Exit Criteria

```text
securityd/auditd/catalogd/datasetd/jobd/spoold/operatord hosted services run
HELLO job success
BOB cannot read ALICE dataset
DENY is audited before final result returns
catalog crash recovery test passes
JCL-like, DSN, operator, policy, object, and audit parser fuzz targets exist
no fake success scanner runs against hosted code
```

### Dependency Ordering

1. Shared object schemas and typed errors.
2. `auditd` append-only local store and schema validation.
3. `securityd` decision API with obligations.
4. `catalogd` committed entry transactions.
5. `datasetd` handle issue and stale-handle rejection.
6. `spoold` SYSIN/SYSOUT protected resources.
7. `jobd` parser, conversion, queue, initiator, DD resolution.
8. `operatord` command parser and vertical slice workflow.
9. Integration tests and fuzz registration.

### Phase 1 Task Backlog

| Task | Output | Depends on | AI-safe assignment |
| --- | --- | --- | --- |
| `HOST-001` | hosted `securityd` prototype | `MFOS-REQ-AUTH-*`, object schemas | One agent owns service package and tests. |
| `HOST-002` | hosted `auditd` prototype | `MFOS-REQ-AUDIT-*` | Must finish schema before integration. |
| `HOST-003` | hosted `catalogd` prototype | `MFOS-REQ-CATALOG-*` | Own catalog package and crash tests. |
| `HOST-004` | hosted `datasetd` prototype | `HOST-001`, `HOST-003` | Must not bypass `securityd`. |
| `HOST-005` | hosted `jobd` prototype | `HOST-001`, `HOST-004`, `HOST-006` | Parser work separate from executor work. |
| `HOST-006` | hosted `spoold` prototype | `HOST-001`, `HOST-002` | Own spool package and negative tests. |
| `HOST-007` | hosted `operatord` prototype | `HOST-001`, `HOST-002`, service APIs | Own command grammar and operator drills. |
| `HOST-008` | minimal `workpolicyd` prototype | job classes | Non-blocking until Phase 3 except dispatch hint stub must fail closed. |
| `HOST-009` | AMF disabled-mode contract tests | AMF spec | AMF load returns `MFOS_ERR_UNSUPPORTED`; no module mapping or registry entry. |
| `HOST-010` | `uvsd` prototype | update manifest schema | Basic signed artifact path first. |
| `HOST-011` | HELLO job integration | services running | Integration agent only. |
| `HOST-012` | unauthorized dataset deny integration | services running | Must verify no handle exists. |
| `HOST-013` | audit chain tamper test | `HOST-002` | Fault-injection agent. |
| `HOST-014` | catalog crash recovery test | `HOST-003` | Crash-recovery agent. |

### Required Evidence

- Hosted integration transcript for ALICE/BOB vertical slice.
- Audit chain records for submit/open/execute/deny/complete.
- Negative-test report showing unauthorized dataset access creates no handle.
- Fuzz target registry.
- Catalog recovery report.

### Phase 1 Gaps

- Hosted transport and serialization may differ from kernel ABI.
- Durable storage is a semantic approximation until nucleus storage is available.
- AMF production load is not part of Phase 1; only disabled-mode contract behavior is tested.
- UVS is a basic prototype only.

## 6. Phase 2: Minimal MFOS Nucleus

### Objectives

- Boot MFOS to operator console.
- Implement address spaces, typed handles, SVC ABI, copy-in/copy-out, and service launcher.
- Port hosted service semantics onto MFOS service runtime.
- Require an NX-capable platform and enforce W^X and user/supervisor separation.
- Ensure user jobs cannot obtain protected dataset handles without `securityd`.
- Keep AMF load disabled with `MFOS_ERR_UNSUPPORTED`.

### Entry Criteria

- Phase 1 vertical slice passes in hosted mode.
- SVC/PCALL ABI specs are frozen enough to implement.
- Nucleus object and capability model is approved.
- Boot handoff and memory map assumptions are documented.

### Exit Criteria

```text
boot to operator console
address space isolation
SVC ABI
typed handles
bounded copy-in/copy-out
service launch and supervision
hosted services ported or bridged
NX-capable platform verified and W^X enforced
user job cannot obtain protected dataset handle without securityd
AMF load returns MFOS_ERR_UNSUPPORTED and creates no mapping or registry entry
unsupported SVCs return UNSUPPORTED
undefined SVCs return SPEC_GAP
```

### Dependency Ordering

1. Boot handoff and memory map parser.
2. Page table manager and NX/W^X.
3. Address spaces and scheduler baseline.
4. SVC entry validation.
5. Typed object handles.
6. Bounded copy-in/copy-out.
7. IPC and PCALL sealed buffers.
8. Service launcher and fault containment.
9. Kernel audit hook.
10. Operator console boot path.

### Phase 2 Task Backlog

| Task | Output | Depends on | AI-safe assignment |
| --- | --- | --- | --- |
| `NUC-001` | boot handoff | boot spec | Boot agent only. |
| `NUC-002` | memory map parser | `NUC-001` | Parser agent must add fuzz target. |
| `NUC-003` | page table manager | `NUC-002` | Memory agent owns mappings. |
| `NUC-004` | NX/W^X enforcement | `NUC-003` | Requires negative tests. |
| `NUC-005` | address space support | `NUC-003` | Isolation agent. |
| `NUC-006` | scheduler baseline | `NUC-005` | Minimal scheduling only. |
| `NUC-007` | SVC entry | `NUC-005` | ABI agent owns SVC tests. |
| `NUC-008` | typed object handles | `NUC-007` | Handle agent owns stale/wrong-type tests. |
| `NUC-009` | copy-in/copy-out | `NUC-007` | Must not dereference untrusted pointers directly. |
| `NUC-010` | IPC/PCALL primitive | `NUC-009` | PCALL agent owns sealed-buffer tests. |
| `NUC-011` | service launcher | `NUC-010` | Service runtime agent. |
| `NUC-012` | fault containment | `NUC-011` | Fault-injection agent. |
| `NUC-013` | crash dump trigger | `NUC-012` | Crash agent. |
| `NUC-014` | audit hook | `NUC-011`, `auditd` | Audit agent. |

### Required Evidence

- Boot transcript.
- Address-space isolation tests.
- SVC/PCALL ABI tests.
- copy-in/copy-out negative tests.
- W^X mapping negative tests.
- User job `securityd` bypass negative test.

### Phase 2 Gaps

- Full driver ecosystem is out of scope.
- Formal proof is not required for exit but state machine models should exist.
- PXM remains implicit single-partition unless Phase 5 work begins separately.

## 7. Phase 3: Baseline Core Semantics

### Objectives

- Complete the core MFOS vertical slice on the actual nucleus runtime.
- Complete the AMF specification and disabled load path.
- Keep AMF production load disabled.
- Add UVS basic signed update artifacts.
- Add audit hash chain.
- Add workload policy basic job class.
- Add crash recovery for catalog, audit, and critical service state.

### Entry Criteria

- Phase 2 exit criteria met.
- Hosted semantic tests can run against nucleus-backed services.
- Basic storage persistence is available.
- `securityd` and `auditd` are reliable enough for protected operations.

### Exit Criteria

```text
dataset/catalog/job/spool/operator/security/audit full vertical slice
AMF specification complete
AMF load path exists but production load remains disabled
signed AMF test modules allowed only in explicit non-production AMF-Test profile
update verification basic signed artifacts
audit hash chain
workload policy basic job class
catalog, audit, and service crash recovery
no fake success CI clean
negative tests for protected-resource bypass pass
```

### Dependency Ordering

1. Nucleus-backed `auditd` hash-chain store.
2. Nucleus-backed `securityd` policy store.
3. Catalog and dataset persistent transactions.
4. Job and spool integration.
5. Operator workflows for define user, define dataset, submit job, browse SYSOUT.
6. workload policy job class and max concurrency.
7. AMF manifest/governance specification and disabled-mode load path.
8. UVS signed artifact verification.
9. Crash recovery and fault injection.

### Phase 3 Task Backlog

| Task | Output | Depends on | AI-safe assignment |
| --- | --- | --- | --- |
| `SECD-001` through `SECD-008` | principal registry, profile parser, auth, transactions, break-glass | Phase 1/2 securityd | Security agents own only `securityd` package. |
| `AUD-001` through `AUD-006` | audit schema, append log, hash chain, query, failure policy, export stub | Phase 2 storage | Audit agents own only `auditd`. |
| `CAT-001` through `CAT-006` | DSN grammar, catalog schema, define/resolve, journal, recovery | audit/security ready | Catalog agents own only `catalogd`. |
| `DATA-001` through `DATA-005` | sequential datasets, handles, stale rejection, retention, integrity tag | catalog/security ready | Dataset agents own only `datasetd`. |
| `JOB-001` through `JOB-008` | parser, submit, conversion, queue, initiator, DD resolution, step execution, RC | data/spool/security ready | Job agents own only `jobd`. |
| `SPL-001` through `SPL-004` | SYSOUT capture, browse, purge, retention | security/audit ready | Spool agents own only `spoold`. |
| `OPER-001` through `OPER-008` | console boot, parser, display, define, submit, cancel, emergency | services ready | Operator agents own only `operatord`. |
| `WPOL-001` through `WPOL-004` | job class, priority, max concurrency, service class placeholder | jobd ready | workload policy agent only. |
| `AMF-001` through `AMF-004` | manifest, signature, revocation, disabled load-control path | security/audit/nucleus mapping ready | AMF agent only; production load remains disabled. |
| `UVS-001` through `UVS-005` | metadata, artifact verification, rollback/freeze/mix-and-match detection | audit/security ready | UVS agent only. |

### Required Evidence

- Full vertical slice transcript.
- Audit hash-chain verification report.
- AMF disabled-mode unsupported-load negative tests.
- AMF-Test invalid signature/revoked signer negative tests only if the non-production AMF-Test profile is implemented.
- UVS unsigned/rollback/freeze/mix-and-match negative tests.
- workload policy job class scheduling tests.
- Crash recovery reports.

### Phase 3 Gaps

- Enterprise-Standalone remote audit export may still be pending until Phase 4.
- Guard approval is not required unless explicitly testing HA path.
- Production AMF load remains out of scope until Phase 4 Enterprise-AMF governance.
- Advanced workload policy goals remain deferred.

## 8. Phase 4: Enterprise-Standalone Hardening

### Objectives

- Integrate Secure Boot and Measured Boot.
- Bind selected secrets to TPM or measured context.
- Implement remote audit export.
- Implement TUF-like metadata for update verification.
- Produce SBOM and signed provenance.
- Add Enterprise-AMF governance if AMF production load is in scope.
- Run rollback, freeze, mix-and-match, and supply-chain negative tests.

### Entry Criteria

- Phase 3 Baseline vertical slice passes.
- Update manifest schema is stable.
- Audit stream schema and hash chain are stable.
- Build/release process is pinned enough to produce provenance.

### Exit Criteria

```text
Secure Boot integration
measured boot integration
TPM sealing for selected secrets
remote audit export
TUF-like update metadata
signed provenance
SBOM
Enterprise-AMF governance evidence if AMF production load is in scope
rollback/freeze/mix-and-match tests
dependency allowlist
reproducible build diff report
```

### Dependency Ordering

1. Build toolchain pinning.
2. SBOM and dependency allowlist.
3. Signed provenance.
4. Update metadata roles and freshness policy.
5. Measured boot event capture.
6. TPM sealing for selected secrets.
7. Remote audit export.
8. Enterprise-AMF governance for signed, measured, revocable, immutable-source, securityd-authorized, auditd-recorded AMF load if in scope.
9. Enterprise-Standalone recovery drill.

### Phase 4 Task Backlog

| Task | Output | Depends on | AI-safe assignment |
| --- | --- | --- | --- |
| `CI-007` | unsafe inventory generator | source tree stable | CI agent. |
| `CI-008` | dependency allowlist checker | dependency manifest | CI agent. |
| `CI-009` | SBOM generator | build pipeline | Supply-chain agent. |
| `CI-010` | signed provenance generator | build pipeline | Supply-chain agent. |
| `CI-011` | reproducible build diff report | pinned toolchain | Build agent. |
| `CI-012` | fuzz target registration checker | fuzz manifests | CI/fuzz agent. |
| `UVS-001` through `UVS-005` hardened | TUF-like freshness and consistency | Phase 3 UVS | Update agent. |
| `AUD-006` hardened | remote audit export | Phase 3 auditd | Audit agent. |
| `AMF-ENT-001` | Enterprise-AMF governance evidence | Phase 3 AMF disabled path | AMF agent; only if production AMF load is in scope. |

### Required Evidence

- Secure/measured boot report.
- TPM sealing report.
- Remote audit export transcript.
- SBOM.
- Signed provenance.
- Update attack negative-test report.
- Supply-chain audit report.
- Enterprise-AMF governance report if AMF production load is in scope.

### Phase 4 Gaps

- TPM policy and key hierarchy need a dedicated security design.
- Remote collector trust model is not yet fixed.
- Firmware recovery is framed but not fully implemented.

## 9. Phase 5: PXM Core Prototype

### Objectives

- Run MFOS under PXM.
- Keep implicit backend and PXM backend behind the same partition-aware API.
- Implement partition lifecycle state machine.
- Test IOMMU domain setup and interrupt remapping.
- Establish Linux/Desktop side partition lab.
- Verify device teardown negative tests before any passthrough production claim.

### Entry Criteria

- Phase 3 Baseline semantics stable.
- Phase 4 hardening has enough measured boot/audit evidence to support partition operation records.
- PXM lifecycle and device teardown specs are approved.
- Hardware lab has documented Intel/AMD capability matrix.

### Exit Criteria

```text
MFOS runs under PXM
implicit backend and PXM backend share partition-aware API
partition lifecycle state machine tests pass
IOMMU domain tested
interrupt remapping tested
Linux side partition lab
device teardown negative tests
partition audit evidence
```

### Dependency Ordering

1. Partition-aware API adapter around implicit backend.
2. Activation profile parser.
3. Partition lifecycle state machine.
4. Measurement and audit for partition operations.
5. VT-x and AMD-V lab skeletons.
6. EPT/NPT memory domain prototype.
7. IOMMU domain manager.
8. Interrupt remapping.
9. Device assignment model.
10. Device teardown checklist.
11. Recovery partition coordination.
12. Side partition gateway lab.

### Phase 5 Task Backlog

| Task | Output | Depends on | AI-safe assignment |
| --- | --- | --- | --- |
| `PXM-001` | partition lifecycle implementation | PXM spec | PXM lifecycle agent. |
| `PXM-002` | activation profile parser | object/update specs | Parser agent with fuzz target. |
| `PXM-003` | implicit single-partition backend | nucleus API | API agent. |
| `PXM-004` | partition-aware MFOS API | `PXM-003` | API agent. |
| `PXM-005` | VT-x lab skeleton | hardware lab | Intel lab agent. |
| `PXM-006` | AMD-V lab skeleton | hardware lab | AMD lab agent. |
| `PXM-007` | EPT/NPT memory domain | `PXM-005`/`PXM-006` | Memory virtualization agent. |
| `PXM-008` | IOMMU domain manager | hardware support | Device isolation agent. |
| `PXM-009` | interrupt remapping | `PXM-008` | Interrupt agent. |
| `PXM-010` | device assignment model | `PXM-008`, `PXM-009` | Device agent. |
| `PXM-011` | device teardown checklist | `PXM-010` | Fault-injection agent. |
| `PXM-012` | partition audit | auditd integration | Audit agent. |
| `PXM-013` | recovery partition coordination | recovery policy | Recovery agent. |

### Required Evidence

- Partition lifecycle test report.
- Activation profile parser fuzz report.
- IOMMU/interrupt remapping report.
- Device teardown negative-test report.
- Partition memory zeroing evidence.
- Linux side partition lab notes.

### Phase 5 Gaps

- PXM is hardware-sensitive; Intel and AMD support must be tracked separately.
- Device passthrough cannot be production until teardown, IOMMU, and interrupt tests pass.
- Side partition gateway identity mapping remains a separate spec gap.

## 10. Phase 6: High-Assurance Guard

### Objectives

- Seal security root.
- Seal audit root.
- Enforce executable mapping policy.
- Verify SVC table.
- Require Guard approval for High-Assurance AMF registry and executable mapping paths when AMF is in scope.
- Provide attestation evidence.
- Test Guard failure policy and lockdown behavior.

### Entry Criteria

- Phase 5 PXM Core is stable enough to host Guard.
- Guard root object spec is approved.
- Security policy root and audit root schemas are stable.
- AMF registry and SVC table digests are stable.
- High-Assurance profile boot policy is defined.

### Exit Criteria

```text
Guard seals security root
Guard seals audit root
Guard enforces executable mapping policy
Guard verifies SVC table
Guard-approved AMF registry
Guard-approved AMF executable mapping when AMF is in scope
attestation evidence
Guard failure policy tested
rollback/replay/root mismatch negative tests pass
High-Assurance claim evidence package exists
```

### Dependency Ordering

1. Guard call ABI.
2. Guard root metadata store.
3. Security root seal/verify.
4. Audit root append and seal.
5. AMF registry seal and executable mapping approval when AMF is in scope.
6. SVC table verification.
7. Executable mapping policy.
8. Attestation.
9. Emergency state.
10. Failure policy and lockdown tests.

### Phase 6 Task Backlog

| Task | Output | Depends on | AI-safe assignment |
| --- | --- | --- | --- |
| `GRD-001` | Guard root model | Guard spec | Guard model agent. |
| `GRD-002` | Guard call ABI | root model | ABI agent. |
| `GRD-003` | security root seal | securityd policy root | Security/Guard agent. |
| `GRD-004` | audit root seal | auditd root | Audit/Guard agent. |
| `GRD-005` | AMF registry seal | AMF registry | AMF/Guard agent. |
| `GRD-006` | SVC table verify | SVC table digest | Nucleus/Guard agent. |
| `GRD-007` | executable mapping policy | mapping policy | Mapping/Guard agent. |
| `GRD-008` | attestation | measurement context | Attestation agent. |
| `GRD-009` | failure policy | all roots | Fault-injection agent. |
| `GRD-010` | lockdown tests | failure policy | Negative-test agent. |

### Required Evidence

- Guard root transition audit records.
- Guard sealed security root evidence.
- Guard sealed audit root evidence.
- SVC table mismatch fault-injection report.
- AMF registry mismatch negative-test report.
- Executable mapping negative-test report.
- Attestation transcript with nonce.

### Phase 6 Gaps

- Guard ABI and attestation claim format are not final.
- Secret release policy is not final.
- External/OOB audit path remains optional and deferred.

## 11. AI-Safe Task Assignment Guidance

### 11.1 Ownership

Every assignment MUST specify:

```text
owned files or directories
read-only files or directories
forbidden files or directories
implemented requirement IDs
source matrix IDs
expected tests
expected evidence artifacts
```

An AI agent MUST NOT edit files outside its ownership, even if it sees errors elsewhere. It may report the issue as a gap or blocker.

### 11.2 Task Size

Use tasks that fit one of these shapes:

- One spec file.
- One parser plus tests.
- One service API plus unit tests.
- One negative-test family.
- One state machine and model tests.
- One CI lint rule.
- One evidence report.

Avoid assigning "build securityd" or "implement PXM" as a single task.

### 11.3 Required Agent Output

Every implementation or review agent MUST return:

```text
1. Implemented Requirement IDs
2. Source Matrix IDs
3. Files Changed
4. Assumptions
5. Spec Gaps
6. Unsupported Features
7. Security Invariants
8. Audit Obligations
9. Failure Modes
10. Tests Added
11. Negative Tests Added
12. Fuzz Targets Added
13. Unsafe Code Justification
14. Evidence Artifacts
```

### 11.4 Concurrency Rules

- Multiple agents may read the same specs.
- Only one agent may own a writable file or package at a time.
- Shared schema changes require a coordination task before service agents update consumers.
- If a task needs a new requirement ID, it must pause and update the requirement catalog through a catalog-owner task.
- If a task hits a `SPEC_GAP`, it must fail closed and record the gap instead of inventing behavior.
- If another agent changed a file, do not revert it. Re-read and adapt or report a conflict.

### 11.5 Security-Sensitive Task Rules

Security-sensitive tasks include:

```text
authorization decisions
audit append or query
dataset handle issue
catalog update
job effective identity
operator command execution
AMF load or disabled-mode AMF load request
update activation
SVC/PCALL entry
PXM partition/device operation
Guard root transition
Linux/Desktop gateway operation
```

For these tasks:

- Negative tests are mandatory.
- Audit obligations are mandatory.
- `UNSUPPORTED` and `SPEC_GAP` behavior must be tested.
- Caller-supplied identity must be treated as untrusted unless bound by trusted context.
- Success must not be returned after a required downstream failure.

## 12. Global Gates

### 12.1 Phase Promotion Gate

A phase may promote only when:

- Exit criteria pass.
- All phase-critical negative tests pass.
- No fake success scanner is clean for the phase scope.
- Requirement coverage report lists all implemented `MFOS-REQ-*` IDs.
- Source Matrix lint passes for source-grounded concepts.
- Evidence artifacts exist for implemented security-sensitive requirements.

### 12.2 Production Readiness Gate

Production claims are blocked until:

```text
PROD-001  Source Matrix complete for all source-grounded concepts
PROD-002  System Integrity negative tests pass
PROD-003  Unauthorized dataset access cannot produce handle
PROD-004  DENY audit record emitted before caller result
PROD-005  Catalog crash recovery passes
PROD-006  Spool browse/purge security enforced
PROD-007  Operator commands require authority and audit
PROD-008  AMF unsupported-load or invalid signature/revoked signer fail closed
PROD-009  Update rollback/freeze/mix-and-match tests pass
PROD-010  SBOM and signed provenance produced
PROD-011  No fake success CI clean
PROD-012  Parser fuzz campaigns complete
PROD-013  PXM device teardown tested before passthrough production
PROD-014  Guard evidence exists before High-Assurance claim
PROD-015  Recovery drill completed
```

## 13. Roadmap Gaps

| Gap ID | Gap | Impact |
| --- | --- | --- |
| `ROADMAP-GAP-001` | Threat model split spec is not present in the current split set. | Blocks complete abuse-case traceability. |
| `ROADMAP-GAP-002` | Formal model file ownership and language choices are not assigned. | Blocks formal evidence scheduling. |
| `ROADMAP-GAP-003` | CI lint scripts are specified but not implemented. | Blocks automated enforcement. |
| `ROADMAP-GAP-004` | Hosted service transport and serialization are not fixed. | May cause rework before nucleus port. |
| `ROADMAP-GAP-005` | Kernel boot target, loader, and hardware baseline are not fixed. | Blocks precise Phase 2 engineering tasks. |
| `ROADMAP-GAP-006` | TPM, measured boot, and key hierarchy need a dedicated Enterprise-Standalone security design. | Blocks Phase 4 implementation detail. |
| `ROADMAP-GAP-007` | PXM hardware lab matrix is not complete. | Blocks Phase 5 schedule confidence. |
| `ROADMAP-GAP-008` | Guard ABI, attestation format, and secret release policy are not final. | Blocks Phase 6 implementation. |
| `ROADMAP-GAP-009` | Evidence schema is conventional but not tool-enforced. | Blocks reliable phase promotion automation. |
| `ROADMAP-GAP-010` | Side partition identity mapping and gateway token format are not final. | Blocks Linux/Desktop gateway production use. |
