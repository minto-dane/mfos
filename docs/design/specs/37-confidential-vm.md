---
spec_id: "MFOS-SPEC-37-CONFIDENTIAL-VM"
title: "MFOS Confidential VM Planning Boundary"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-28"
source_refs: ["X64-INTEL-001", "X64-AMD-001", "TCG-001", "NIST-160-001", "NIST-193-001", "MS-VBS-001", "MS-VSM-001", "FBVBS-001"]
requirement_refs: ["MFOS-REQ-CVM-*", "MFOS-REQ-PARTITION-*", "MFOS-REQ-GUARD-*", "MFOS-REQ-AUDIT-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Confidential VM Planning Boundary

Status: Draft scaffold. This document defines future planning language only. It
does not authorize confidential-computing implementation, attestation service
implementation, secret-release implementation, or hardware-enforcement claims.

## 1. Purpose

MFOS may later support confidential workload partitions. Phase 0.x only reserves
the design boundary so future work does not confuse hardware features with MFOS
policy definition.

## 2. Source References

- `X64-INTEL-001`
- `X64-AMD-001`
- `TCG-001`
- `NIST-160-001`
- `NIST-193-001`
- `MS-VBS-001`
- `MS-VSM-001`
- `FBVBS-001`

These sources provide background for measurement, attestation, firmware
resilience, and assurance structure. They do not define an MFOS compatibility
target or a hardware-security claim.

## 3. Reserved MFOS-Owned Concepts

Future `MFOS-REQ-CVM-*` requirements may cover:

- confidential VM object model
- measured launch contract
- attestation evidence bundle
- secret-release authorization
- private/shared memory transition policy
- guest CPU-state protection claim boundary
- encrypted memory claim boundary
- trusted I/O placeholder policy
- recovery and migration constraints

## 4. Non-Claims

MFOS does not currently claim:

- host exclusion for confidential workloads
- memory-integrity enforcement by hardware
- trusted I/O enforcement
- confidential device assignment
- remote attestation compatibility with external verifier formats
- production-grade confidential workload isolation

## 5. Guard Boundary

Future confidential VM claims MUST NOT expand Guard into interpreting dataset,
job, spool, or operator business semantics. Guard may only protect selected root
objects after explicit root-object specs, evidence, and red-team review.

## 6. Spec Gaps

`GAP-MFOS-CVM-0001`: confidential workload source cards are not complete enough
for semantic freeze.

`GAP-MFOS-CVM-0002`: no confidential VM launch, attestation, or secret-release
runner may be implemented in Phase 1.
