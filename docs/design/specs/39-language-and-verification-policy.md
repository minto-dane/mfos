---
spec_id: MFOS-SPEC-39-LANGUAGE-AND-VERIFICATION-POLICY
title: MFOS Language and Verification Policy
canonical_language: en-US
japanese_mirror: missing
status: draft
owner: MFOS architecture
last_reviewed: '2026-04-28'
source_refs:
- EXTREF-RUST-UNSAFE-REFERENCE-0001
- EXTREF-RUST-NO-STD-REFERENCE-0001
- EXTREF-RUST-CF-PROTECTION-0001
- EXTREF-CLANG-CFI-0001
- EXTREF-CLANG-KCFI-0001
- EXTREF-GCC-CF-PROTECTION-0001
- EXTREF-INTEL-CET-0001
- X64-LINUX-CET-001
- EXTREF-KANI-RUST-VERIFIER-0001
- EXTREF-VERUS-RUST-VERIFICATION-0001
- EXTREF-DAFNY-REFERENCE-0001
- EXTREF-GITHUB-CODEQL-0001
- EXTREF-NIST-SECURE-SYSTEMS-ENGINEERING-0001
- EXTREF-NIST-SSDF-0001
- SLSA-001
- X64-INTEL-001
- X64-AMD-001
- FBVBS-001
requirement_refs:
- MFOS-REQ-DAFNY-*
- MFOS-REQ-LANG-*
- MFOS-REQ-FORMAL-*
- MFOS-REQ-ASSURANCE-*
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs:
- PACK-34
- PACK-35
spec_gap_policy: implementation_must_not_infer_or_fill_gaps
---

# MFOS Language and Verification Policy

Status: Draft Phase 0.10 requirements expansion. This document defines policy and evidence planning only. It does not authorize production code, unsafe-code acceptance, toolchain enforcement claims, proof claims, semantic runner implementation, or production assurance claims.

## 1. Purpose

Define MFOS language, toolchain, control-flow, and verification-policy requirements before any implementation work is assigned.

## 2. Scope

In scope: safe language policy, Rust default, no_std policy, unsafe boundary policy, Dafny executable-semantics policy, Kani, Verus, TLA+, Alloy, proof placeholders, CFI, CET, clang CFI, assembly contracts, VMX/SVM wrapper contracts, toolchain pinning, sanitizers, fuzzing, static analysis, CodeQL, proof obligations, and evidence.

## 3. Non-objectives

Out of scope: implementation, proof completion, verified kernel claim, complete memory-safety claim, complete CFI claim, or tool certification claim.

## 4. Source References

- EXTREF-INTEL-CET-0001
- EXTREF-RUST-UNSAFE-REFERENCE-0001
- EXTREF-RUST-NO-STD-REFERENCE-0001
- EXTREF-RUST-CF-PROTECTION-0001
- EXTREF-CLANG-CFI-0001
- EXTREF-CLANG-KCFI-0001
- EXTREF-GCC-CF-PROTECTION-0001
- X64-LINUX-CET-001
- EXTREF-KANI-RUST-VERIFIER-0001
- EXTREF-VERUS-RUST-VERIFICATION-0001
- EXTREF-DAFNY-REFERENCE-0001
- EXTREF-GITHUB-CODEQL-0001
- EXTREF-NIST-SECURE-SYSTEMS-ENGINEERING-0001
- EXTREF-NIST-SSDF-0001
- SLSA-001
- X64-INTEL-001
- X64-AMD-001
- FBVBS-001

These Source Matrix IDs are public-safe reference cards. They are not copied external documentation and do not define external compatibility.

## 5. Phase 0.10 Assurance Limits

This specification defines future policy, profile names, and evidence gates only. A profile assignment, tool name, hardware feature name, or planned proof obligation is not evidence that an implementation exists or that the property has been achieved.

No MFOS document may infer production readiness from this specification. Any implementation task that depends on a missing language profile, unsafe boundary decision, proof artifact, CFI/CET measurement, or toolchain record must stop with `MFOS_ERR_SPEC_GAP`.

Phase 1 uses Dafny as the canonical executable-semantics artifact language. Phase 1 does not authorize a Rust semantic core, Portable Semantic Core, semantic runner, hosted daemon, generated production code, PXM/MFVM/CVM/cluster implementation, or production service behavior. Rust remains the future implementation-policy default for many components, but later Rust production code must conform to reviewed Phase 1 artifacts and must not replace Dafny as the Phase 1 executable-semantics authority.

## 6. Language Assurance Profiles

Language Assurance Profiles define the minimum policy posture for future implementation units. They are planning labels, not completed assurance claims.

| Profile | Intended use | Language posture | Required planning evidence before implementation |
| --- | --- | --- | --- |
| LAP-0 Declarative | Schemas, registries, requirements, policy data, source cards | Data-only artifacts with schema validation | Schema reference, owner, validation command, traceability to requirements |
| LAP-1 Managed Safe | Control-plane services, CLIs, test tools, orchestration helpers | Safe language subset by default; no privileged or freestanding assumptions | Language selection rationale, dependency policy, static analysis plan, tests |
| LAP-2 Rust Safe Core | Security-sensitive services, parsers, policy engines, resource managers | Rust default; safe Rust unless an approved unsafe boundary exists | Rust toolchain plan, `forbid(unsafe_code)` or documented exception, fuzz/property test plan, CodeQL/static-analysis plan |
| LAP-3 Rust no_std / Freestanding | Kernel-adjacent, boot, hypervisor-adjacent, device, or partition-management code | Rust candidate under `no_std` or freestanding runtime constraints; unsafe only through approved contracts | Runtime contract, panic/allocation/concurrency model, ABI contract, unsafe inventory, proof-obligation stubs |
| LAP-4 Explicit Low-level Exception | Assembly, VMX/SVM transitions, CPU entry/exit paths, unavoidable C/C++ boundary shims | Exception-only profile; not a general implementation language approval | Architecture source refs, boundary contract, reviewer approval, negative tests, CFI/CET evidence plan where applicable, red-team review gate |

The default planning target is LAP-2 for security-sensitive Rust-capable code and LAP-1 for ordinary managed tooling. LAP-3 and LAP-4 require explicit requirement IDs and cannot be selected by convenience.

## 6.1 Canonical Language Assurance Profile Names

The following names are the canonical MFOS-owned profile names used by packs,
requirements, future implementation prompts, and evidence records.

### MFOS-LANG-RUST-SAFE

Target components include securityd policy core, auditd core, catalogd core,
datasetd core, jobd core, spoold core, operatord command core, wlmd policy core,
uvsd validation core, MFVM management plane core, future Rust implementation
modules after the appropriate phase gate, parsers, validators, and tools where
appropriate.

Requirements:

- Safe Rust default.
- `unsafe_code` forbidden where feasible.
- Result-based error model.
- Deterministic tests.
- Property tests.
- Fuzz targets for parsers and decoders.
- Kani harnesses for critical pure functions where feasible.
- Verus for selected high-value pure modules where feasible.

### MFOS-LANG-RUST-TCB-NOSTD

Target components include PXM Core, PXM Guard, MFOS nucleus, low-level object
handle core, PXM Control API validator, CVM primitive validator, and critical
memory/resource ownership logic.

Requirements:

- Rust `no_std`.
- `panic=abort`.
- No unwinding.
- Fixed toolchain.
- Custom target as needed.
- No hidden allocation unless explicitly approved.
- Unsafe isolated behind reviewed abstractions.
- Unsafe inventory mandatory.
- Kani proof harnesses for bounded validators.
- Verus preferred for ownership, capability, and handle invariants.
- TLA+ model for state machines.
- Binary hardening evidence where applicable.

### MFOS-LANG-HARDWARE-BOUNDARY

Target components include early boot, VMX/SVM entry/exit, MSR/control-register
access, interrupt/trap entry, context switch, CPU feature probing, and low-level
instruction wrappers.

Permitted languages are assembly and minimal Rust unsafe wrappers. Requirements:

- No policy logic.
- No business semantics.
- No string parsing.
- No allocation.
- Explicit preconditions.
- Explicit postconditions.
- Register clobber contract.
- Stack discipline contract.
- Calling convention contract.
- Disassembly review.
- Symbol map evidence.
- Independent review.

### MFOS-LANG-C-CXX-EXCEPTION

Target components are limited to vendor boundary, required C ABI boundary,
unavoidable toolchain integration, and architecture startup glue if Rust/assembly
alternatives are not feasible.

Requirements:

- ADR required.
- No policy logic.
- No business semantics.
- No security decision logic.
- No audit decision logic.
- No parser unless separately justified.
- Clang CFI/KCFI where applicable.
- CET where applicable.
- LTO where required.
- Sanitizers in non-production CI where feasible.
- CodeQL.
- Static analysis.
- Safety contract.
- Independent review.
- Binary hardening evidence.

### MFOS-HARDENING-CFI-CET-EVIDENCE

Target components include C/C++ exception boundaries, Rust binaries where the
toolchain and profile support relevant features, hosted tools where applicable,
service binaries where applicable, and PXM/nucleus binaries only where
platform/toolchain support is proven.

Requirements:

- Record compiler flags.
- Record linker flags.
- Record LTO status.
- Record target features.
- Record CET, CFI, CFG, and KCFI status.
- Validate emitted binary properties.
- List unprotected objects.
- Justify exceptions.
- Store evidence artifacts.
- Fail release gate if a hardening claim lacks evidence.

## 7. Component Language Matrix

The following matrix is provisional for Phase 0.10. It constrains planning and review language; it does not start production work or freeze final implementation choices.

| Component area | Baseline profile | Preferred candidate | Restricted alternatives | Required evidence before implementation |
| --- | --- | --- | --- | --- |
| Requirements, registries, schemas, packs | LAP-0 | YAML, Markdown, schema languages | Generated code only after generator policy exists | Schema validation, traceability, source-card links |
| Assurance tooling and validators | LAP-1 | Rust or managed scripting where existing repo practice requires it | C/C++ forbidden; shell limited to glue | Tests, static analysis where available, dependency review |
| User-space control-plane services | LAP-2 | Rust safe core | Managed runtime only with explicit service contract | Threat model, tests, fuzzing for parsers, CodeQL/static analysis |
| Policy engines and authorization logic | LAP-2 | Rust safe core plus model/proof hooks | C/C++ forbidden; unsafe requires exception | Requirement links, model links, negative tests, proof obligations |
| Audit and evidence pipeline | LAP-2 | Rust safe core | Managed runtime only for offline tools | Tamper-evidence requirements, serialization tests, review records |
| PXM object and lifecycle management | LAP-2 or LAP-3 | Rust; `no_std` only if required by placement | C/C++ forbidden except audited FFI shim | Object model, lifecycle model, unsafe inventory, red-team review |
| MFVM management plane | LAP-2 | Rust safe core | C/C++ forbidden except audited boundary shim | VM lifecycle tests, policy tests, source refs, evidence registry links |
| Kernel-adjacent runtime support | LAP-3 | Rust `no_std` candidate | Assembly only for defined ABI stubs | Runtime contract, ABI contract, sanitizer/static-analysis plan, proof obligations |
| VMX/SVM entry, exit, and CPU-state wrappers | LAP-4 | Minimal Rust wrapper plus assembly where unavoidable | C/C++ only by exception; handwritten assembly requires contract | Architecture refs, register/memory/fault contracts, negative tests, red-team gate |
| C/C++ third-party boundary | LAP-4 | Avoided by default | C or C++ only as an approved exception | Exception record, clang CFI plan, ABI contract, memory ownership contract, replacement plan |

If a component does not fit this matrix, the correct Phase 0.10 result is a spec gap, not an inferred language choice.

## 7.1 Component Language Matrix

The following component assignments are canonical Phase 0.10 planning defaults.
They remain implementation-disabled until the relevant downstream phase gates
explicitly allow implementation.

| Component | Primary profile | Boundary profile | Verification plan | C/C++ allowed |
| --- | --- | --- | --- | --- |
| PXM Core | MFOS-LANG-RUST-TCB-NOSTD | MFOS-LANG-HARDWARE-BOUNDARY | TLA+, Kani, Verus | false_by_default |
| PXM Guard | MFOS-LANG-RUST-TCB-NOSTD | none unless later approved | TLA+, Kani, Verus | false_by_default |
| MFOS nucleus | MFOS-LANG-RUST-TCB-NOSTD | MFOS-LANG-HARDWARE-BOUNDARY | TLA+, Kani | false_by_default |
| MFVM | MFOS-LANG-RUST-SAFE | none unless later approved | TLA+, Kani, property_tests | false_by_default |
| securityd | MFOS-LANG-RUST-SAFE | none unless later approved | Kani, Verus_selected, property_tests, golden_vectors | false_by_default |
| auditd | MFOS-LANG-RUST-SAFE | none unless later approved | Kani, property_tests, golden_vectors | false_by_default |
| catalogd | MFOS-LANG-RUST-SAFE | none unless later approved | TLA+, Kani, fuzzing, crash_recovery_tests | false_by_default |
| datasetd | MFOS-LANG-RUST-SAFE | none unless later approved | Kani, property_tests, fuzzing | false_by_default |
| jobd | MFOS-LANG-RUST-SAFE | none unless later approved | TLA+, fuzzing, golden_vectors | false_by_default |
| spoold | MFOS-LANG-RUST-SAFE | none unless later approved | property_tests, golden_vectors | false_by_default |
| operatord | MFOS-LANG-RUST-SAFE | none unless later approved | fuzzing, golden_vectors | false_by_default |
| uvsd | MFOS-LANG-RUST-SAFE | none unless later approved | Kani, property_tests, rollback/freeze/mix-and-match vectors | false_by_default |
| parsers | MFOS-LANG-RUST-SAFE | none unless later approved | fuzzing, property_tests, golden_vectors | false_by_default |
| tools/scripts | Rust_or_Python | not applicable | schema validation, py_compile/static checks | C/C++ forbidden |

Python remains allowed for non-TCB validation tools. Long-term critical
validators should migrate to Rust where feasible, but this migration is not a
Phase 0.10 implementation authorization.

## 7.2 Phase 1 Executable-semantics Matrix Addendum

Phase 1 executable semantics are Dafny-first and loader-only.

| Phase 1 area | Canonical artifact | Allowed Phase 1 activity | Forbidden Phase 1 activity |
| --- | --- | --- | --- |
| Executable semantics | Dafny source plus MFOS metadata | scaffold creation, artifact metadata validation, dependency/reference validation | Rust semantic-core implementation, semantic evaluation, semantic-runner commands, hosted daemons, production generated code |
| Supporting models | TLA+ and Alloy | model planning and registry linkage | product behavior, service implementation, production enforcement |
| Later implementation | Rust after separate gate | conformance planning only | replacing Dafny as Phase 1 canonical executable semantics |

The detailed Dafny Executable-semantics Policy is `docs/design/specs/43-dafny-executable-semantics-policy.md`. Missing Dafny behavior remains `MFOS_ERR_SPEC_GAP`; unsupported declarations remain `MFOS_ERR_UNSUPPORTED`.

## 8. Safe Language Policy

MFOS defaults to safe implementation languages where feasible. Deviations require requirement IDs, source refs, unsafe boundary review, tests, and evidence before implementation.

Rust is the default language candidate for most future security-sensitive implementation work. This is a policy direction, not an implementation start, proof claim, or acceptance of any concrete crate, compiler, runtime, or target.

## 9. Rust no_std Policy

Low-level components may require `no_std` or freestanding constraints. Those constraints require a separate runtime contract before implementation.

The runtime contract must address panic behavior, allocation, synchronization, interrupt or preemption assumptions, initialization order, CPU feature discovery, target triples, linker scripts, and auditability of build flags. Missing answers are spec gaps.

## 10. Unsafe Exception Policy

Unsafe Rust is forbidden by default for LAP-1 and LAP-2 planning. Unsafe Rust may be planned only through an exception record that includes:

- requirement IDs and source refs
- caller and callee safety contracts
- memory ownership and aliasing rules
- concurrency, interrupt, and privilege assumptions
- input validation and failure behavior
- tests, fuzz/property coverage where applicable, and review status
- explicit not-claimed boundaries

An unsafe exception is not accepted evidence of memory safety. Unknown unsafe behavior is `MFOS_ERR_SPEC_GAP` for implementation planning.

## 11. Assembly Boundary Policy

Assembly boundaries require register, memory, calling convention, privilege, fault, CPU-feature, stack, and audit contracts before implementation.

Assembly must be minimized, isolated behind named interfaces, and linked to architecture source refs. Inline assembly and standalone assembly have the same evidence burden. Assembly that changes privilege level, CPU control state, interrupt state, or VMX/SVM state requires a red-team review gate before implementation planning can proceed.

## 12. C/C++ Exception Policy

C and C++ are not default MFOS implementation languages. They are allowed only as explicit LAP-4 exceptions for unavoidable third-party ABI boundaries, toolchain bootstrap constraints, or architecture interfaces where no safer candidate is viable.

Each C/C++ exception must include a boundary contract, ownership model, lifetime model, compiler and linker flags, sanitizer plan, clang CFI or equivalent review plan where applicable, replacement or containment plan, and reviewer sign-off. The exception must state that it does not authorize general C/C++ production code.

## 13. Kani Proof Harness Policy

Kani may be used for Rust model checking and bounded proof harnesses. No proof exists until a proof artifact is linked and reviewed.

Kani evidence must identify the function or module under analysis, bounded assumptions, unsupported language features, harness inputs, tool version, command line, result status, and requirements covered.

## 14. Verus Proof Policy

Verus may be used for specification and proof of selected Rust logic. No implementation is verified merely because a Verus plan exists.

Verus evidence must link specification functions, executable functions, assumptions, proof status, tool version, and reviewed limitations. A verified subset must not be described as a verified component unless the component boundary is formally defined.

## 14.1 Dafny Executable-semantics Policy

Dafny is the canonical executable-semantics artifact language for Phase 1. This is a specification and loader-validation decision, not an implementation authorization.

Dafny artifacts may become reviewed executable-semantics sources after a Phase 1 task creates them under `formal/executable-semantics/dafny/`. Phase 1 tooling may validate artifact shape, declared requirement links, source references, dependency declarations, and proof-status metadata. Phase 1 tooling must not evaluate MFOS behavior, operate as a semantic runner, start a hosted daemon, or produce production code.

Dafny verification output is evidence only when linked to source, requirements, assumptions, tool version, result, and review status. A Dafny plan or scaffold does not prove a component, service, partition primitive, VM primitive, or production runtime.

## 15. TLA+ State-machine Policy

TLA+ remains a state-machine modeling option for authorization, audit, catalog, dataset open, job lifecycle, operator command, PXM lifecycle, update, and device teardown.

TLA+ models are design evidence only until they are linked to requirements, assumptions, checked invariants, model-checker output, and implementation conformance evidence.

## 16. Alloy Model Policy

Alloy may be used for relation-heavy models such as policy reachability, network reachability, and object ownership.

Alloy evidence must record scopes, predicates, assertions, counterexample disposition, and requirements covered. Alloy results must not be treated as exhaustive proof outside the modeled scope.

## 17. Coq/Lean/Isabelle Placeholder Policy

Coq, Lean, and Isabelle are placeholder options only. They must not be listed as completed evidence unless proof artifacts exist.

## 18. CFI Evidence Policy

Control-flow integrity is a future defense-in-depth requirement. CFI does not define MFOS security policy and cannot substitute for securityd/auditd obligations.

A CFI claim requires all of the following evidence:

- scoped component boundary and threat model
- compiler, linker, flags, target, and LTO mode where relevant
- list of included and excluded binaries, libraries, and exception paths
- negative tests or fault-injection evidence for representative invalid control transfers
- CI logs showing the configured CFI build and tests
- limitations, bypass assumptions, and unsupported code paths

Without that evidence, MFOS may only say that CFI is planned or required for future evaluation. MFOS must not claim complete control-flow integrity at Phase 0.10.

## 19. CET Evidence Policy

Intel CET may inform feature-profile planning. CET names are permitted as feature names, but no CET enforcement claim is made until platform evidence and tests exist.

A CET evidence record must identify the specific mechanism under discussion, platform and firmware assumptions, compiler/linker support, runtime enablement state, binary notes or equivalent inspection output, test method, and unsupported paths. CET availability does not prove CFI coverage for MFOS and must not be used as a substitute for component-specific CFI evidence.

## 20. clang CFI for C/C++ Boundaries

C/C++ boundaries are restricted and require clang CFI or equivalent policy review only after a boundary contract is approved. This does not authorize C/C++ production code.

For any approved C/C++ boundary, clang CFI evidence must include build flags, LTO configuration, type-visibility assumptions, sanitizer interactions, excluded translation units, test output, and known limitations.

## 21. VMX/SVM Wrapper Contracts

VMX/SVM wrapper work is forbidden until PXM requirements, object model, proof obligations, and red-team review pass later gates.

Any future wrapper contract must describe register state, memory ownership, VMCS/VMCB state, host/guest transition invariants, fault paths, audit events, CPU feature discovery, and recovery behavior.

## 22. Toolchain Pinning

Toolchain pinning must record compiler, linker, verification tool, sanitizer, and static-analysis versions before release claims.

Pinned records must include target triples, optimization levels, relevant feature flags, build profile, lockfile or provenance data where applicable, and CI identity. A tool version alone is not evidence that the intended policy was enforced.

## 23. Sanitizer Policy

Sanitizers are validation aids, not production proof. Sanitizer findings must be triaged and linked to evidence.

Sanitizer evidence must identify the sanitizer configuration, test corpus, disabled checks, unsupported targets, findings, fixes, and residual risk.

## 24. Fuzzing Policy

Fuzzing is required for parsers and decoders identified by specs and packs. Fuzzing does not replace negative tests or formal obligations.

Fuzzing evidence must include corpus source, target function, seed policy, runtime or coverage criteria, crash disposition, minimization status, and links to fixed defects.

## 25. Static Analysis Policy

Static analysis is mandatory where available and must be recorded as evidence, including limitations.

Static-analysis evidence must record tool name, version, rule set, scope, suppressions, findings, triage owner, and unresolved issues.

## 26. CodeQL Policy

CodeQL is a code scanning tool reference. CodeQL reports are not a complete security review and do not authorize public release alone.

CodeQL evidence must identify query packs, language scope, disabled queries, alert disposition, and the CI run that produced the report.

## 27. Proof Obligations

Proof obligations must link claims, requirements, models, assumptions, not-claimed boundaries, and evidence paths.

Each proof obligation must state the property, scope, artifact type, tool, assumptions, required reviewer role, current status, and explicit non-goals. A proof obligation in planned or draft state is not proof evidence.

## 28. Evidence Requirements

Evidence includes source refs, requirement traceability, proof obligation registry, model registry, tool registry, CI output, review status, and red-team findings.

Evidence records must be reproducible enough for review and narrow enough to avoid accidental whole-system claims. Evidence must include limitations and must distinguish planned, generated, reviewed, accepted, rejected, and superseded states.

## 29. Overclaim Bans

MFOS documents, packs, reports, and future release notes must not claim any of the following unless accepted evidence exists for the exact stated scope:

- complete memory safety
- complete control-flow integrity
- CET enforcement
- clang CFI enforcement
- verified kernel correctness
- verified hypervisor correctness
- verified authorization correctness
- verified audit-chain correctness
- verified VM isolation
- verified PXM correctness
- production proof coverage
- tool certification
- absence of undefined behavior
- absence of exploitable vulnerabilities
- C/C++ safety equivalence to safe Rust

Allowed Phase 0.10 wording is limited to planning language such as "candidate", "planned", "required evidence", "future gate", "policy direction", and "not yet claimed". Ambiguous wording that could imply completed enforcement or proof must be treated as a documentation defect.

## 30. Spec Gaps

- GAP-MFOS-LANG-001: final implementation language profile is not frozen.
- GAP-MFOS-LANG-002: unsafe boundary acceptance criteria remain draft.
- GAP-MFOS-LANG-003: final component-to-profile assignment is provisional.
- GAP-MFOS-LANG-004: C/C++ exception acceptance workflow is not frozen.
- GAP-MFOS-LANG-005: assembly and VMX/SVM boundary review checklist is not frozen.
- GAP-MFOS-FORMAL-001: proof acceptance criteria remain draft.
- GAP-MFOS-FORMAL-002: proof obligation registry schema and lifecycle states remain draft.
- GAP-MFOS-ASSURANCE-001: CFI/CET evidence acceptance criteria remain draft.
