---
spec_id: MFOS-SPEC-37-CONFIDENTIAL-VM
title: MFOS Confidential VM Architecture
canonical_language: en-US
japanese_mirror: missing
status: draft
owner: MFOS architecture
last_reviewed: '2026-04-28'
source_refs:
- EXTREF-INTEL-TDX-OVERVIEW-0001
- EXTREF-INTEL-TDX-LINUX-DOC-0001
- EXTREF-INTEL-TDX-ATTESTATION-0001
- EXTREF-AMD-SEV-OVERVIEW-0001
- EXTREF-AMD-SEV-ES-0001
- EXTREF-AMD-SEV-SNP-0001
- EXTREF-AMD-SEV-TIO-0001
- EXTREF-LINUX-AMD-SEV-KVM-DOC-0001
- EXTREF-MICROSOFT-HYPERV-VSM-0001
- TCG-001
- NIST-160-001
- NIST-193-001
- FBVBS-001
requirement_refs:
- MFOS-REQ-CVM-*
- MFOS-REQ-PXM-*
- MFOS-REQ-MFVM-*
- MFOS-REQ-FORMAL-*
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs:
- PACK-14
- PACK-31
- PACK-32
- PACK-35
spec_gap_policy: implementation_must_not_infer_or_fill_gaps
---

# MFOS Confidential VM Architecture

Status: Draft Phase 0.10 requirements expansion. This is specification-only and does not authorize confidential VM launch code, attestation service implementation, secret-release implementation, device-assignment implementation, hosted daemon, semantic runner, or production claim.

## 1. Purpose

Define MFOS confidential VM concepts, trust boundaries, profile abstraction, launch/attestation/secret-release obligations, and failure modes before any implementation work is assigned.

## 2. Scope

In scope: ConfidentialVM object model, CVM profile abstraction, launch measurement, attestation evidence, secret release decision, private/shared memory transition planning, device assignment constraints, migration/recovery constraints, and formal proof obligations.

## 3. Non-objectives

Out of scope: hardware launch code, external attestation protocol implementation, external verifier format reproduction, external cloud service compatibility, trusted I/O implementation, and production confidentiality claims.

## 4. Source References

- EXTREF-INTEL-TDX-OVERVIEW-0001
- EXTREF-INTEL-TDX-LINUX-DOC-0001
- EXTREF-INTEL-TDX-ATTESTATION-0001
- EXTREF-AMD-SEV-OVERVIEW-0001
- EXTREF-AMD-SEV-ES-0001
- EXTREF-AMD-SEV-SNP-0001
- EXTREF-AMD-SEV-TIO-0001
- EXTREF-LINUX-AMD-SEV-KVM-DOC-0001
- EXTREF-MICROSOFT-HYPERV-VSM-0001
- TCG-001
- NIST-160-001
- NIST-193-001
- FBVBS-001

## 5. Non-compatibility Statement

MFOS is an independent project. External virtualization, confidential-computing, assurance, and operations references are design background only. MFOS does not claim compatibility with Hyper-V, KVM, Intel TDX services, AMD SEV services, any external VM API, any external attestation format, or any external management plane.


## 6. Confidential VM Object Model

A ConfidentialVM binds a VMPartition, CVMProfile, CVMLaunchMeasurement, CVMAttestationEvidence, CVMSecretReleaseDecision, private/shared memory transition log, audit correlation, and lifecycle state. Phase 0.10 defines schema and requirements only.

## 7. CVM Profile Abstraction

A CVM Profile identifies the hardware feature family, launch prerequisites, measurement evidence requirements, attestation evidence requirements, memory encryption properties, CPU-state protection expectations, private/shared transition rules, and unsupported capabilities.

## 8. CVM_PROFILE_INTEL_TDX

CVM_PROFILE_INTEL_TDX is an MFOS feature-profile name for Intel TDX-informed planning. It is not a product claim, certification claim, or external verifier compatibility claim.

## 9. CVM_PROFILE_AMD_SEV

CVM_PROFILE_AMD_SEV is an MFOS feature-profile name for AMD SEV-informed planning. It is not a certification claim or external service compatibility claim.

## 10. CVM_PROFILE_AMD_SEV_ES

CVM_PROFILE_AMD_SEV_ES is an MFOS feature-profile name for AMD encrypted-state planning. It remains draft until launch, debug, CPU-state, and failure-mode evidence are defined.

## 11. CVM_PROFILE_AMD_SEV_SNP

CVM_PROFILE_AMD_SEV_SNP is an MFOS feature-profile name for AMD SNP-informed planning, including memory integrity and attestation requirements. No production memory-integrity claim is made.

## 12. Optional Trusted I/O Placeholder

SEV-TIO and TDISP-related planning remains placeholder-only. No trusted I/O implementation or device-assignment guarantee is authorized in Phase 0.10.

## 13. Guest Launch Flow

The abstract flow is REQUEST, AUTHORIZE, VERIFY_IMAGE, RESERVE_RESOURCES, MEASURE, PXM_LAUNCH_PRIMITIVE, ATTESTATION_AVAILABLE, SECRET_RELEASE_ELIGIBLE, RUNNING. Missing measurement or attestation produces fail-closed behavior.

## 14. Guest Measurement

Launch measurement is a required evidence object for CVM launch eligibility. It must bind image identity, configuration identity, resource identity, CVM profile, PXM capability state, and audit correlation.

## 15. Attestation Evidence

Attestation evidence is required before secret release. MFOS does not define external attestation wire formats in this phase.

## 16. Secret Release Policy

securityd authorizes secret release. uvsd verifies artifacts where applicable. auditd records evidence. Secret release without attestation is prohibited.

## 17. Encrypted Memory Policy

Encrypted memory is represented as a profile capability and trust boundary. MFOS does not claim hardware protection until platform evidence and profile-specific requirements pass later gates.

## 18. Private/Shared Memory Transition

Private/shared transitions must be explicit, auditable, profile-valid, and linked to a VMPartition and CVMProfile. Ambiguous transition state is MFOS_ERR_SPEC_GAP.

## 19. Guest CPU State Protection

CPU-state protection is profile-specific. MFOS must not generalize one profile's guarantees to another profile.

## 20. Memory Integrity Policy

Memory integrity claims require profile-specific evidence. Missing evidence blocks semantic evaluator and production work.

## 21. Host/PXM/MFVM Trust Boundaries

MFVM coordinates. PXM performs privileged launch operations. CPU/firmware/profile components provide hardware trust functions. securityd authorizes and auditd records. MFVM is not the confidential VM trust root.

## 22. MFVM Launch Coordination Role

MFVM prepares management intent, resource request, image reference, policy context, and operator workflow. It cannot bypass PXM capability checks or directly perform privileged launch primitives.

## 23. PXM Enforcement Role

PXM validates VM partition identity, RAM ownership, second-stage translation ownership, device assignment constraints, launch prerequisites, and audit obligation completion.

## 24. securityd Authorization Role

securityd authorizes CVM launch, secret release, attestation query, device assignment, recovery action, and operator commands.

## 25. auditd Evidence Role

auditd records launch request, launch denial, measurement record, attestation acceptance/rejection, secret release decision, private/shared transition, device assignment, teardown, and recovery events.

## 26. Attestation Verifier Role

The attestation verifier determines whether evidence satisfies a policy before secret release. It is not implemented in Phase 0.10.

## 27. CVM Device Assignment Constraints

Confidential device assignment requires profile-specific requirements, teardown proof, IOMMU and interrupt remapping evidence, and audit. Missing trusted-I/O support must fail closed.

## 28. CVM Migration Constraints

Migration is blocked until source grounding, measurements, attestation continuity, secret handling, rollback resistance, and recovery evidence are defined.

## 29. CVM Recovery Constraints

Recovery requires evidence-preserving failure handling. Secret release must not resume from ambiguous or unverifiable state.

## 30. Failure Modes

Required failure modes include MFOS_ERR_SPEC_GAP, MFOS_ERR_UNSUPPORTED, MFOS_ERR_POLICY_DENIED, MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE, MFOS_ERR_ATTESTATION_REQUIRED, MFOS_ERR_MEASUREMENT_REQUIRED, and MFOS_ERR_INTEGRITY_CHECK_FAILED.

## 31. Negative Tests

Negative tests must include launch without policy approval, launch without measurement, secret release without attestation, private/shared transition without profile rule, MFVM privileged-root attempt, device assignment without teardown proof, unsupported profile, and recovery from ambiguous state.

## 32. Formal Proof Obligations

Formal obligations include cvm_launch_requires_measurement, cvm_secret_release_requires_attestation, private_shared_memory_transition_validity, pxm_capability_required_for_resource_operation, and mfvm_cannot_bypass_pxm.

## 33. Evidence Requirements

Evidence includes source grounding, requirement traceability, profile matrix, schema review, negative-test catalog, formal obligation registry, audit obligation mapping, and red-team review.

## 34. Spec Gaps

- GAP-MFOS-CVM-001: profile-specific launch and attestation formats are not frozen.
- GAP-MFOS-CVM-002: trusted I/O is placeholder-only.
- GAP-MFOS-CVM-003: no CVM semantic evaluator, launch code, or secret-release implementation is allowed.
