---
spec_id: MFOS-SPEC-44-ARCHITECTURE-PORTABILITY-POLICY
title: MFOS Architecture Portability Policy
canonical_language: en-US
japanese_mirror: missing
status: draft
owner: MFOS architecture
last_reviewed: '2026-04-30'
source_refs:
- FBVBS-001
- X64-INTEL-001
- X64-AMD-001
- EXTREF-RUST-TARGET-TIER-POLICY-0001
- EXTREF-SEL4-MULTIARCH-SUPPORTED-PLATFORMS-0001
- EXTREF-SEL4-ARCH-CONFIGURATION-0001
- EXTREF-NIST-SECURE-SYSTEMS-ENGINEERING-0001
requirement_refs:
- MFOS-REQ-ARCH-*
- MFOS-REQ-CPUFEAT-*
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs:
- PACK-14
- PACK-31
- PACK-32
- PACK-34
- PACK-36
spec_gap_policy: implementation_must_not_infer_or_fill_gaps
---

# MFOS Architecture Portability Policy

Status: Draft architecture policy. This document defines documentation, registry,
and validation policy only. It does not authorize production code, Rust
semantic-core work, Dafny semantic changes, nucleus work, PXM/MFVM/CVM/TEE/SGX
runtime work, cluster runtime work, architecture backends, CPU feature detection,
hardware paths, hosted daemons, or service implementation.

## 1. Purpose

MFOS is x86-64-first for initial implementation planning, but it is not
x86-64-only. The initial implementation, validation, early PXM planning, early
hardware profiles, and first production-oriented implementation planning target
x86-64 first because the current source cards and hardware-profile work are
x86-64 grounded by `X64-INTEL-001` and `X64-AMD-001`.

The policy goal is to keep MFOS enterprise semantics independent from CPU
architecture while making the architecture/backend boundary explicit before any
hardware-facing implementation is assigned.

## 2. Scope

In scope:

- Architecture-neutral versus architecture-specific responsibility boundaries.
- CPU architecture versus platform-specific responsibility boundaries.
- Future non-x86 architecture claim rules.
- Registry and validation gates that prevent architecture overclaims.
- AI-agent guardrails for roadmap, pack, and prompt materials.

Out of scope:

- Implementing architecture backends.
- Implementing CPU feature discovery.
- Implementing boot, trap, interrupt, page-table, VMX/SVM, IOMMU/SMMU, CVM,
  TEE, enclave, or runtime paths.
- Claiming AArch64, RISC-V, or other non-x86 support.

## 3. Source References

- `FBVBS-001`
- `X64-INTEL-001`
- `X64-AMD-001`
- `EXTREF-RUST-TARGET-TIER-POLICY-0001`
- `EXTREF-SEL4-MULTIARCH-SUPPORTED-PLATFORMS-0001`
- `EXTREF-SEL4-ARCH-CONFIGURATION-0001`
- `EXTREF-NIST-SECURE-SYSTEMS-ENGINEERING-0001`

These references are source-grounding and process references only. They do not
create external compatibility claims, proof claims, or implementation claims.

## 4. x86-64-First Policy

MFOS initial implementation planning targets x86-64 first.

This means:

- Initial hardware profile planning is x86-64.
- Early PXM/MFVM/CVM profile planning is x86-64.
- CPU Feature Registry coverage starts with x86-64 and platform entries.
- First binary-evidence and profile-evidence policies are x86-64.
- Architecture-specific enforcement planning references x86-64 source cards
  until later non-x86 source cards and requirements exist.

This does not mean that MFOS enterprise semantics are x86-64 semantics.

## 5. Not x86-64-Only

MFOS must not become x86-64-only by accident.

The dataset, catalog, job, spool, operator, authorization, audit, update,
MFVM-management, conformance, and formal semantic models must not depend on an
x86-64 instruction, register, privilege mode, page-table format, virtualization
primitive, enclave primitive, or confidential-computing primitive.

Any future architecture backend must implement or enforce the same reviewed
MFOS enterprise semantics rather than rewriting those semantics for the CPU.

## 6. Architecture-Neutral Semantics

Architecture-neutral semantics include:

- Authorization.
- Audit.
- Dataset and catalog semantics.
- Job, spool, and operator semantics.
- Update verification semantics.
- MFVM management-plane semantics.
- Conformance fixtures, oracles, and golden vectors.
- Formal claims that do not depend on a specific CPU feature.

CPU features can provide enforcement aids or profile evidence. They must not
define whether an MFOS authorization, audit, dataset, catalog, job, spool,
operator, update, or management-plane transition is semantically valid.

## 7. Architecture-Specific Enforcement

Architecture-specific enforcement includes:

- Privilege mode transitions.
- Trap and interrupt entry.
- Page table and translation structures.
- CPU feature discovery.
- VMX/SVM or equivalent virtualization primitives.
- IOMMU/SMMU or equivalent DMA isolation.
- Timer and interrupt-controller details.
- Confidential-computing primitives.
- Enclave/TEE primitives.
- Architecture-specific hardening features.
- CPU state management.

These mechanisms enforce or support selected MFOS policies only after source
cards, requirements, profiles, tests, CI, and evidence exist. They do not
change the architecture-neutral semantics.

## 8. Platform-Specific Layer

Platform-specific concerns are separate from CPU architecture concerns.

The platform-specific layer includes:

- Boot and firmware interface.
- UEFI/ACPI or equivalent discovery.
- Device topology.
- NUMA topology.
- PCIe and device assignment.
- TPM or attestation hardware.
- Node identity.
- Datacenter platform policy.

Platform evidence can satisfy selected target-profile requirements, but a
platform feature does not imply a CPU feature, and a CPU feature does not imply
platform enablement.

## 9. Future Non-x86 Architecture Policy

Future AArch64, RISC-V, or other architecture support may be designed, but it
must not be claimed as implemented until all of the following exist:

- Public-safe Source Cards.
- Architecture-specific specs.
- Requirements.
- CPU feature registry entries.
- CPU target profile registry entries.
- Tests and negative tests.
- CI coverage.
- Evidence records.
- Architecture/backend implementation paths.
- Review status that explicitly permits the claim.

No AArch64, RISC-V, or other non-x86 backend is present in the current tree.
MFOS enterprise semantics must not require rewriting for future architecture
backends.

## 10. Registry Gates

Architecture and profile claims are gated by:

- `docs/design/registries/cpu-feature-registry.yml`
- `docs/design/registries/cpu-target-profiles.yml`
- `schemas/mfos/cpu-feature-profile.schema.yml`
- `docs/design/specs/45-x86-64-target-profiles.md`

The CPU Feature Registry is design-time governance. It is not a CPU feature
detector, runtime capability API, boot path, or implementation stub.

## 11. AI and Roadmap Guardrails

AI agents must treat current Phase 1 as non-production Dafny executable
semantics plus conformance-harness validation only. Phase 1 does not authorize
hosted semantic prototypes, hosted daemons, service implementations,
Rust/Portable semantic-core work, semantic-runner commands, PXM/MFVM/CVM/cluster
implementation, hypervisor backends, CVM/TEE/SGX runtime work, architecture
backends, CPU feature detection, or production/generated production code.

Roadmap, pack, prompt, and task documents must not describe old Hosted Semantic
Prototype or Rust semantic-core plans as current Phase 1 work. Historical
references must be marked superseded or inactive.

## 12. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| `MFOS-REQ-ARCH-0001` | MFOS MUST separate architecture-neutral semantics from architecture-specific enforcement. | architecture policy validator |
| `MFOS-REQ-ARCH-0002` | MFOS initial implementation target MUST be x86-64. | profile registry review |
| `MFOS-REQ-ARCH-0003` | Future non-x86 architectures MUST be supported through explicit architecture/backend boundaries, not semantic rewrites. | architecture review |
| `MFOS-REQ-ARCH-0004` | MFOS MUST NOT claim non-x86 architecture support without source cards, specs, tests, CI, and evidence. | roadmap/profile validator |

## 13. Failure Modes

| Failure | Required result |
| --- | --- |
| Architecture-specific mechanism used as enterprise semantics | Claim rejected; implementation task stops with `MFOS_ERR_SPEC_GAP`. |
| Optional CPU feature treated as global | Profile claim rejected. |
| Non-x86 support claimed without evidence | Roadmap/profile validation fails. |
| Platform feature treated as CPU architecture support | Profile claim rejected. |
| CPU feature presence treated as a security claim | Evidence review fails. |

## 14. Negative Tests

- `NEG-MFOS-ARCH-0001`: authorization semantics depend on an x86-64 feature;
  test must fail.
- `NEG-MFOS-ARCH-0002`: AArch64 or RISC-V support is marked implemented without
  source cards, tests, CI, and evidence; validation must fail.
- `NEG-MFOS-ARCH-0003`: platform attestation is treated as CPU feature
  presence; validation must fail.
- `NEG-MFOS-ARCH-0004`: a CPU feature claim changes dataset/catalog semantics;
  validation must fail.

## 15. Evidence Requirements

Evidence required before architecture/backend implementation:

- Source-card coverage.
- Requirement coverage.
- CPU Feature Registry entry.
- CPU Target Profile Registry entry.
- Positive and negative tests.
- CI validation.
- Binary evidence where a build/profile claim is made.
- Runtime/platform evidence where a platform capability claim is made.
- ADR for any TCB use of optional high-performance instructions.

## 16. Spec Gaps

- `ARCH-GAP-0001`: no non-x86 Source Card set exists.
- `ARCH-GAP-0002`: no architecture backend implementation exists.
- `ARCH-GAP-0003`: no CPU feature detection implementation exists.
- `ARCH-GAP-0004`: no production x86-64 hardware path exists.
