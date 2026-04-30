---
spec_id: MFOS-SPEC-36-HYPERVISOR-CLASS-VIRTUALIZATION
title: MFOS Hypervisor-Class Virtualization
canonical_language: en-US
japanese_mirror: missing
status: draft
owner: MFOS architecture
last_reviewed: '2026-04-28'
source_refs:
- EXTREF-MICROSOFT-HYPERV-OVERVIEW-0001
- EXTREF-MICROSOFT-HYPERV-TLFS-0001
- EXTREF-LINUX-KVM-API-0001
- EXTREF-LINUX-KVM-CAPABILITIES-0001
- EXTREF-LINUX-KVM-VFIO-0001
- X64-INTEL-001
- X64-AMD-001
- NIST-160-001
- FBVBS-001
requirement_refs:
- MFOS-REQ-PXM-*
- MFOS-REQ-MFVM-*
- MFOS-REQ-VIRT-*
- MFOS-REQ-PERF-*
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs:
- PACK-14
- PACK-31
- PACK-36
spec_gap_policy: implementation_must_not_infer_or_fill_gaps
---

# MFOS Hypervisor-Class Virtualization

Status: Draft Phase 0.10 requirements expansion. This document is specification-only. It does not authorize a hypervisor, VM runtime, device model, migration engine, snapshot engine, hosted daemon, semantic runner, or production implementation.

## 1. Purpose

Define MFOS-owned virtualization vocabulary and requirements for future VM partition management while preserving the PXM/MFVM trust boundary. The purpose is to describe what later design phases must prove, test, and evidence before any implementation is assigned.

Spec `45` owns x86-64 target profiles for TDX, SEV-SNP, and SGX. This
virtualization planning spec must treat Intel SGX as an enclave/TEE profile, not
as a Confidential VM or VM-wide virtualization profile.

## 2. Scope

In scope: VM object model, VM partition lifecycle, vCPU and RAM accounting, virtual storage/network abstractions, capability discovery, device assignment constraints, resource pools, PXM Control API boundaries, audit obligations, performance budget placeholders, and negative-test planning.

## 3. Non-objectives

Out of scope: implementation, external hypervisor API cloning, external VM configuration format reproduction, nested virtualization as a requirement, live migration implementation, snapshot implementation, and production performance claims.

## 4. Source References

- EXTREF-MICROSOFT-HYPERV-OVERVIEW-0001
- EXTREF-MICROSOFT-HYPERV-TLFS-0001
- EXTREF-LINUX-KVM-API-0001
- EXTREF-LINUX-KVM-CAPABILITIES-0001
- EXTREF-LINUX-KVM-VFIO-0001
- X64-INTEL-001
- X64-AMD-001
- NIST-160-001
- FBVBS-001

These sources are public-safe reference cards and source IDs only. They are not copied external documentation and are not substitutes for external documentation.

## 5. Non-compatibility Statement

MFOS is an independent project. External virtualization, confidential-computing, assurance, and operations references are design background only. MFOS does not claim compatibility with Hyper-V, KVM, Intel TDX services, AMD SEV services, any external VM API, any external attestation format, or any external management plane.


## 6. MFOS-owned Terminology

MFOS-owned terms in this domain are PXM Core, PXM Control API, MFVM, VM Partition, VM Resource Pool, VM Image Resource, VM Config, VM Placement Decision, VM Capability Set, VCPUModel, VMMemoryReservation, and VMDeviceAttachment. These names are independently specified MFOS terms.

## 7. PXM and MFVM Layering

PXM Core is the trusted hardware-facing partition and resource authority. MFVM is the MFOS-based VM management subsystem in the MFOS control plane. MFVM may request PXM operations, but PXM validates capabilities, resource bounds, memory ownership, device ownership, interrupt remapping, IOMMU domains, and audit obligations.

## 8. MFVM as MFOS-based VM Management Subsystem

MFVM is not an independent hypervisor root and does not directly own VMX/SVM roots. MFVM integrates with securityd, auditd, operatord, catalogd, datasetd, wlmd, uvsd, the management API, and policy lint before forwarding bounded requests to the PXM Control API.

## 9. VM Object Model

A VM object references a VMPartition, VMConfig, VMResourcePool, VMImageResource, VMCapabilitySet, VCPUModel, VMMemoryReservation, zero or more VMDeviceAttachment records, authorization bindings, audit correlation, and lifecycle status. This model is schema-only in Phase 0.10.

## 10. VM Partition Lifecycle

Required lifecycle states are REQUESTED, ADMITTED, RESOURCES_RESERVED, CONFIGURED, READY_TO_LAUNCH, RUNNING, PAUSED, STOPPING, STOPPED, FAILED, and TEARDOWN_COMPLETE. Invalid transitions must fail closed and produce audit evidence.

## 11. vCPU Model

The vCPU model captures vCPU count, CPU feature profile, scheduling class, quota/reservation, topology hints, and accounting tags. It does not define executable CPU virtualization code.

## 12. VM Capability Discovery

MFVM may discover available VM capabilities only through approved MFOS capability registries and PXM-reported capabilities. MFVM must not infer hardware capability by probing privileged hardware roots directly.

## 13. CPU Capability Discovery

PXM owns low-level CPU capability discovery for VM primitives. MFVM consumes sanitized capability sets and must treat unknown or unsupported features as MFOS_ERR_UNSUPPORTED or MFOS_ERR_SPEC_GAP according to whether the behavior is specified.

## 14. RAM Reservation, Quota, and Accounting

PXM enforces RAM ownership, zero-before-reuse, reservation, quota, and accounting. MFVM records management intent and resource-pool assignment but cannot map arbitrary memory or override PXM ownership.

## 15. VM Data and Storage Resource Model

VM images and configuration resources are MFOS-managed resources. VM image artifacts must be verified by uvsd and governed by securityd before use. Dataset-backed images use catalogd/datasetd metadata only when the dataset/catalog specs authorize that path.

## 16. Virtual Storage Model

The virtual storage model is a future abstraction with identity, source artifact, access mode, integrity tag, retention policy, and audit obligation. No external virtual disk layout is reproduced here.

## 17. Virtual Network Model

The virtual network model reserves network attachment, segmentation, policy class, audit tags, and future reachability reasoning. It does not define a packet datapath implementation.

## 18. Virtual MMU Abstraction

PXM owns second-stage translation setup, teardown, and ownership checks. MFVM never receives arbitrary mapping authority.

## 19. Virtual Interrupt Abstraction

PXM owns interrupt remapping and interrupt-delivery safety. MFVM may request bounded virtual interrupt configuration through the PXM Control API.

## 20. Timer Model

Timer configuration must be capability-bound and audited when it affects VM execution scheduling, accounting, or isolation boundaries.

## 21. Inter-partition Communication

Any future inter-partition communication must be explicitly authorized, audited, bounded by object identity, and separated from dataset/job/spool/operator semantics.

## 22. VM State Save/Restore Model

State save/restore is a placeholder. A future spec must define authorization, confidentiality, integrity, image provenance, rollback prevention, and evidence before implementation.

## 23. Snapshot Placeholder

Snapshot support is not implemented or authorized. Snapshot metadata must not be treated as audit evidence or update provenance.

## 24. Migration Placeholder

Migration is a placeholder. Future migration requirements must define source/destination attestation, resource ownership transfer, audit continuity, rollback policy, and failure recovery.

## 25. Device Model

The device model reserves identity, ownership, assignment state, teardown state, IOMMU domain, interrupt remapping, firmware trust status, and audit correlation. PXM enforces safety.

## 26. Device Assignment Model

Device assignment may be informed by external device-assignment documentation, but MFOS defines its own model. PXM must validate teardown before reuse and must fail closed on stale ownership, stale interrupt mappings, or stale IOMMU domains.

## 27. Nested Virtualization Non-goal

MFVM does not require nested virtualization. VMs are PXM-managed VM partitions, not nested guests under MFVM.

## 28. Performance Budgets

Performance budgets are declarative planning objects for VM exits, scheduling overhead, audit overhead, memory placement, and I/O path overhead. No benchmark or production throughput claim is made.

## 29. Security Boundaries

MFVM compromise must not imply PXM isolation root compromise. PXM capability validation, securityd authorization, auditd evidence, and uvsd verification are separate obligations.

## 30. Audit Obligations

VM create, resource reservation, device assignment, launch, stop, failed launch, teardown, capability denial, and overbroad request rejection require audit planning records.

## 31. Failure Modes

Required failure modes include MFOS_ERR_UNSUPPORTED, MFOS_ERR_SPEC_GAP, MFOS_ERR_UNAUTHORIZED, MFOS_ERR_POLICY_VERSION_MISMATCH, MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE, MFOS_ERR_RESOURCE_QUOTA_EXCEEDED, MFOS_ERR_STALE_HANDLE, and MFOS_ERR_INTEGRITY_CHECK_FAILED.

## 32. Negative Tests

Negative tests must include overbroad MFVM request, MFVM direct privileged-root request, memory overcommit beyond policy, stale device ownership, missing IOMMU teardown, missing interrupt remapping, unauthorized image use, unsupported capability, and snapshot/migration invoked before specification.

## 33. Evidence Requirements

Evidence requirements include source traceability, requirement traceability, pack contract, schema review, negative-test catalog, audit obligation mapping, formal obligation mapping, and red-team review.

## 34. Spec Gaps

- GAP-MFOS-VIRT-001: no executable VM primitive exists.
- GAP-MFOS-VIRT-002: snapshot and migration remain placeholders.
- GAP-MFOS-VIRT-003: PXM hardware capability schema is draft.
- GAP-MFOS-VIRT-004: Phase 1 may validate loaders only; no virtualization semantic evaluator is allowed.
