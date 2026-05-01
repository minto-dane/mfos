# PXM/MFVM Requirements Docs Expansion Report

Status date: 2026-04-28
Status: current expansion complete

## Summary

Phase 0.10 records design-only MFVM requirements as an MFOS-based VM
management subsystem and expands the requirements base for PXM,
hypervisor-class virtualization, Confidential VM profiles, datacenter/cluster
operations, language verification, automated reasoning, and secure operations.

No production implementation, hosted daemon, semantic runner, semantic-core, PXM implementation, MFVM implementation, VM runtime, CVM launch code, or cluster scheduler was added.

## Architecture Decision

- PXM Core is the trusted hardware-facing partition/resource authority.
- MFVM is an MFOS-based VM management subsystem in the MFOS control plane.
- MFVM is less trusted than PXM.
- VMs are PXM-managed VM partitions, not nested guests under MFVM.
- Confidential VM trust roots are hardware/profile/PXM/securityd/auditd/attestation-verifier bounded; MFVM only coordinates.

## Files Added or Expanded

- `docs/design/specs/16-pxm.md`
- `docs/design/specs/36-hypervisor-class-virtualization.md`
- `docs/design/specs/37-confidential-vm.md`
- `docs/design/specs/38-datacenter-cluster-operations.md`
- `docs/design/specs/39-language-and-verification-policy.md`
- `docs/design/specs/40-automated-reasoning-program.md`
- `docs/design/specs/41-performance-and-secure-operations.md`
- `docs/design/specs/42-mfvm.md`
- `docs/design/registries/requirements.yaml`
- `docs/design/source-matrix/cards/EXTREF-*.yml`
- `packs/pack-index.yml`
- `formal/registry.yml`
- `tests/catalog/{pxm,mfvm,hypervisor-class-virtualization,confidential-vm,datacenter-cluster,language-verification,automated-reasoning,performance-secure-operations}.yml`

## Pack ID Decision

The request named PACK-25 through PACK-29 for new domains, but the repository already uses those IDs for existing canonical packs. To avoid silent duplicate ownership, Phase 0.10 updates existing `PACK-14` for PXM and adds `PACK-31` through `PACK-36` for MFVM, Confidential VM, datacenter cluster, language verification, automated reasoning, and performance/secure operations.

## Source Grounding

Public-safe EXTREF cards were added for Microsoft Hyper-V references, Linux KVM references, Intel TDX/CET references, AMD SEV-family references, Kani, Verus, AWS automated reasoning, GitHub CodeQL, and NIST references. Source Cards remain bibliographic/reference-control cards and do not reproduce external documentation text, tables, record layouts, command syntax, diagrams, code, or macro signatures.

## Phase Gates

```yaml
phase_1_loader_allowed: true
phase_1_core_semantic_evaluator_allowed: false
phase_1_pxm_mfvm_cvm_cluster_semantic_evaluator_allowed: false
production_implementation_allowed: false
hosted_daemon_implementation_allowed: false
semantic_runner_implementation_allowed: false
public_release_allowed: false
requires_ip_attorney_review_before_public_release: true
```
