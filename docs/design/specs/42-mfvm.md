---
spec_id: MFOS-SPEC-42-MFVM
title: MFOS Virtual Machine Manager
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
- EXTREF-INTEL-TDX-OVERVIEW-0001
- EXTREF-AMD-SEV-SNP-0001
- EXTREF-NIST-SECURE-SYSTEMS-ENGINEERING-0001
- FBVBS-001
requirement_refs:
- MFOS-REQ-MFVM-*
- MFOS-REQ-PXM-*
- MFOS-REQ-VIRT-*
- MFOS-REQ-CVM-*
- MFOS-REQ-CLUSTER-*
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs:
- PACK-31
- PACK-32
- PACK-33
spec_gap_policy: implementation_must_not_infer_or_fill_gaps
---

# MFOS Virtual Machine Manager

Status: Draft Phase 0.10 requirements expansion. This specification is design-only and does not authorize MFVM implementation, hosted daemon implementation, semantic runner implementation, VM runtime implementation, PXM implementation, or production code.

## 1. Purpose

Define MFVM as an MFOS-based VM management subsystem that coordinates VM management workflows while remaining less trusted than PXM Core.

## 2. Scope

In scope: MFVM trust boundary, service decomposition, image/config/resource metadata workflow, placement recommendations, confidential VM coordination, operator/management API integration, securityd/auditd/catalogd/datasetd/wlmd/uvsd integration, PXM Control API usage, capability limits, failure modes, negative tests, evidence, and spec gaps.

## 3. Non-objectives

MFVM is not an independent hypervisor, not a nested hypervisor, not a PXM replacement, not a direct owner of VMX/SVM roots, not a cluster scheduler trust root, and not a bypass around securityd, auditd, uvsd, or PXM.

## 4. Source References

- EXTREF-MICROSOFT-HYPERV-OVERVIEW-0001
- EXTREF-MICROSOFT-HYPERV-TLFS-0001
- EXTREF-LINUX-KVM-API-0001
- EXTREF-LINUX-KVM-CAPABILITIES-0001
- EXTREF-LINUX-KVM-VFIO-0001
- EXTREF-INTEL-TDX-OVERVIEW-0001
- EXTREF-AMD-SEV-SNP-0001
- EXTREF-NIST-SECURE-SYSTEMS-ENGINEERING-0001
- FBVBS-001

These Source Matrix IDs are public-safe reference cards. They are not copied external documentation and do not define external compatibility.

## 5. MFVM Is MFOS-based

MFVM runs in the MFOS control plane and uses MFOS governance services. It is not a separate product compatibility layer.

## 5. MFVM Is Not a Hypervisor Root

MFVM cannot perform privileged VM primitives directly. PXM Core performs hardware-facing partition and VM primitive operations.

## 6. MFVM Is Less Trusted Than PXM

MFVM compromise must not imply PXM isolation root compromise. PXM validates every PXM Control API request independently.

## 7. MFVM Service Decomposition

The MFVM management subsystem is decomposed into planning components: Control Service, Image Service, Placement Service, Device Coordination Service, Confidential VM Coordination Service, management API, and operator integration. These are design components, not implemented daemons.

## 8. MFVM Control Service

The Control Service validates management intent, collects policy context, prepares PXM requests, and records audit obligations.

## 9. MFVM Image Service

The Image Service references VM image resources governed by securityd, verified by uvsd, and stored or cataloged using MFOS-managed resources where applicable.

## 10. MFVM Placement Service

The Placement Service produces VM Placement Decisions. Placement is recommendation/governance data and is not a PXM trust root.

## 11. MFVM Device Coordination Service

The Device Coordination Service prepares device attachment requests. PXM owns assignment safety, IOMMU domains, interrupt remapping, teardown, and reuse checks.

## 12. MFVM Confidential VM Coordination Service

The Confidential VM Coordination Service prepares launch intent, profile selection, measurement request, attestation request, and secret-release workflow. PXM performs privileged launch primitives.

## 13. MFVM Management API

The management API is a governed interface requiring identity, authorization, audit, idempotency, and policy-version handling.

## 14. MFVM Operator Commands

Operator commands for VM lifecycle, resource-pool management, image registration, placement review, CVM launch coordination, and recovery must go through operatord and securityd.

## 15. MFVM securityd Integration

securityd authorizes VM create, modify, launch, stop, device attach, image use, placement override, attestation query, and secret release.

## 16. MFVM auditd Integration

auditd records VM lifecycle, denied requests, image verification, PXM request emission, PXM rejection, CVM measurement, attestation decision, secret release decision, placement override, and emergency actions.

## 17. MFVM catalogd/datasetd Integration

VM image/config/resource metadata may use catalogd/datasetd only where dataset/catalog specs authorize the resource. Ordinary host files are not substitutes for MFOS-managed resources.

## 18. MFVM wlmd Integration

wlmd supplies workload/resource policy context. MFVM does not implement independent workload policy semantics.

## 19. MFVM uvsd Integration

uvsd verifies image/artifact metadata before MFVM requests launch or activation workflows.

## 20. MFVM PXM Control API Usage

MFVM submits bounded PXMControlRequest objects. PXM validates caller capability, target object, resource bounds, memory/device ownership, confidential VM prerequisites, and audit obligations.

## 21. MFVM Capability Limits

MFVM must not map arbitrary memory, bypass IOMMU or interrupt remapping, directly own VMX/SVM roots, suppress audit, create unbounded device access, or reinterpret enterprise semantics.

## 22. MFVM Failure Modes

Failure modes include MFOS_ERR_POLICY_DENIED, MFOS_ERR_UNSUPPORTED, MFOS_ERR_SPEC_GAP, MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE, MFOS_ERR_POLICY_VERSION_MISMATCH, MFOS_ERR_STALE_HANDLE, MFOS_ERR_RESOURCE_QUOTA_EXCEEDED, MFOS_ERR_ATTESTATION_REQUIRED, and MFOS_ERR_MEASUREMENT_REQUIRED.

## 23. Negative Tests

Negative tests include MFVM direct privileged-root request, overbroad PXM request, launch without securityd authorization, launch without uvsd verification, image use without catalog/dataset authorization where applicable, bypassed audit, PXM rejection ignored, placement treated as security enforcement, and CVM secret release without attestation.

## 24. Evidence Requirements

Evidence includes source cards, requirements, schemas, pack contracts, test catalogs, traceability, formal obligations, red-team review, and validation output.

## 25. Spec Gaps

- GAP-MFOS-MFVM-001: no MFVM service implementation is authorized.
- GAP-MFOS-MFVM-002: PXM Control API wire format remains draft.
- GAP-MFOS-MFVM-003: no PXM/MFVM/CVM/cluster semantic evaluator is allowed in Phase 1.
