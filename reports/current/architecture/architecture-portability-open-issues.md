# Architecture Portability Open Issues

Status: current
Date: 2026-04-30

## Nonblocking Open Issues

- `ARCH-OPEN-0001`: Future AArch64 and RISC-V design work needs source cards,
  requirements, CPU feature registries, target profiles, tests, CI, evidence,
  and backend specs before any implementation claim.
- `CPUFEAT-OPEN-0001`: Exact x86-64-v2/v3/v4 feature membership remains
  source-grounded by external Source Cards; MFOS does not copy external feature
  tables into design docs.
- `CPUFEAT-OPEN-0002`: CPU feature detection implementation is intentionally
  absent and must remain absent until a later architecture backend gate.
- `X64-OPEN-0001`: v4 optimized artifact evidence, negative detection tests,
  and binary instruction audits are required before any v4 support claim.
- `TEE-OPEN-0001`: SGX TCB use requires ADR, threat model, attestation policy,
  side-channel risk analysis, and evidence before implementation.

## Blocking Issues

None for this documentation, registry, validation, and policy change.
