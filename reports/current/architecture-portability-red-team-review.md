# Architecture Portability Red-Team Review

Status: current
Date: 2026-04-30

## Critical Findings

None remaining after local policy validators.

## Major Findings

None remaining after local policy validators.

## Checks Performed

- x86-64-first did not become x86-64-only.
- Future non-x86 support is not claimed as implemented.
- Architecture-neutral semantics are separated from architecture-specific
  enforcement.
- x86-64-v4 is optional and not baseline.
- CPU Feature Registry is design-time policy, not an implementation detector.
- CPU target profiles reference registry feature IDs.
- TDX and SEV-SNP are CVM profiles.
- SGX is TEE/enclave profile, not CVM.
- SGX attestation mode remains separate from SGX feature presence.
- Hyper-V and KVM compatibility is not claimed.
- Phase 1 Dafny policy remains preserved.
- Production implementation remains forbidden.

## Residual Risk

Future implementation agents must not treat planned profile entries as hardware
support. Implementation claims still require source cards, specs, requirements,
tests, CI, binary/runtime evidence, and reviewed backend code.
