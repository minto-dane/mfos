# Architecture Portability Policy Report

Status: current
Date: 2026-04-30

## Scope

This report records documentation, registry, validation, and roadmap policy
changes only. It does not authorize production code, Rust semantic-core work,
Dafny semantic changes, architecture backends, CPU feature detection, PXM/MFVM,
CVM/TEE/SGX runtime work, cluster runtime work, hosted daemons, or hardware
paths.

## Policy

- MFOS is x86-64-first for initial implementation planning.
- MFOS is not x86-64-only.
- Architecture-neutral semantics remain independent from CPU architecture.
- Architecture-specific enforcement is separated from enterprise semantics.
- Platform-specific concerns are separated from CPU architecture concerns.
- Future AArch64, RISC-V, or other non-x86 support may be designed, but is not
  claimed as implemented.

## Artifacts

- `docs/design/specs/44-architecture-portability-policy.md`
- `docs/design/specs/45-x86-64-target-profiles.md`
- `docs/design/registries/cpu-feature-registry.yml`
- `docs/design/registries/cpu-target-profiles.yml`
- `schemas/mfos/cpu-feature-profile.schema.yml`

## Non-Claims

- No non-x86 architecture backend is implemented.
- No Hyper-V or KVM compatibility is claimed.
- CPU features do not define MFOS authorization, audit, dataset/catalog,
  job/spool/operator, update, or management-plane semantics.
