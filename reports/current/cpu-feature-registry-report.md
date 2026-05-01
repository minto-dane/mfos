# CPU Feature Registry Report

Status: current
Date: 2026-04-30

## Scope

The CPU Feature Registry is a design-time registry. It records feature identity,
source grounding, profile membership, evidence expectations, usage
restrictions, fallback behavior, attestation separation, and review status. It
is not a CPU feature detector and does not implement capability discovery.

## Registry Files

- `docs/design/registries/cpu-feature-registry.yml`
- `docs/design/registries/cpu-target-profiles.yml`
- `schemas/mfos/cpu-feature-profile.schema.yml`

## Coverage

The registry contains x86-64 profile-level entries, execution protection,
virtualization, IOMMU/interrupt remapping, TDX, SEV/SEV-ES/SEV-SNP/SEV-TIO,
SGX, SGX attestation modes, CET/CFI, v4/vector policy, XSAVE state-management,
NUMA, and TPM/measured-boot platform entries.

## Validation Policy

`scripts/checks/check-cpu-feature-registry.py` verifies required fields, source
references, target-profile feature references, v4 baseline exclusions, CVM/v4
separation, SGX/TEE separation, SGX attestation separation, and no implemented
feature-detection overclaim.

## Remaining Design Gaps

- Exact v2/v3/v4 feature membership remains source-card governed and is not
  copied into MFOS tables.
- Future non-x86 registries require separate source cards, profiles, tests, CI,
  and evidence.
