# Roadmap Phase Alignment Report

Status: current
Date: 2026-04-30

## Alignment

- Current Phase 1 remains Dafny executable semantics plus conformance-harness
  validation.
- Hosted Semantic Prototype is superseded for current Phase 1 work.
- Rust semantic-core is not a Phase 1 canonical semantic implementation.
- PXM/MFVM/CVM/TEE/SGX/cluster implementation remains future-gated.
- Architecture backend implementation and CPU feature detection remain
  future-gated.

## Roadmap Changes

- Replaced active Hosted Semantic Prototype phase wording with Verified
  Executable Semantics + Conformance Harness.
- Added x86-64-first, not x86-64-only policy to roadmap guardrails.
- Added x86-64-v4 optional profile policy to roadmap guardrails.
- Added SGX optional enclave/TEE and not-CVM policy to roadmap guardrails.
- Added CPU Feature Registry and target profile prerequisites before
  hardware-facing backend work.

## Validator

`scripts/checks/check-roadmap-phase-alignment.py` rejects roadmap and prompt
language that presents Hosted Semantic Prototype or Rust semantic-core as
current Phase 1 work.
