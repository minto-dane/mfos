# Virtualization and Confidential Workload Remediation

Status: current

Expanded draft specifications and planning artifacts:

- `docs/design/specs/36-hypervisor-class-virtualization.md`
- `docs/design/specs/37-confidential-vm.md`
- `docs/design/specs/42-mfvm.md`
- `schemas/mfos/vm-*.schema.yml`
- `schemas/mfos/cvm-*.schema.yml`
- `tests/catalog/hypervisor-class-virtualization.yml`
- `tests/catalog/confidential-vm.yml`
- `tests/catalog/mfvm.yml`

These documents reserve MFOS-owned planning vocabulary and Phase 0.10
requirements only. They do not authorize implementation, hardware-enforcement
claims, compatibility claims, attestation services, secret release, device
models, migration, MFVM daemon work, PXM work, or production virtualization
work.

MFVM is recorded as MFOS-based and less trusted than PXM. VMs are recorded as
PXM-managed VM partitions, not nested guests under MFVM.
