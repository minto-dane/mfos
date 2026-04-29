# formal/

Formal models for state machines and invariants. Initial targets:

- authorization decision and audit obligation
- dataset open invariant
- catalog transaction recovery
- audit append chain
- PXM lifecycle and device teardown
- Guard root transitions

Phase 0.10 defines split canonical draft registries:
`formal/claim-registry.yml`, `formal/proof-obligations.yml`,
`formal/tool-registry.yml`, `formal/model-registry.yml`, and
`formal/evidence-registry.yml`. `formal/registry.yml` is an aggregate
compatibility view for older tooling and reports. Entries in all formal
registries are planned or draft unless a linked proof artifact and review
status say otherwise.

Kani and Verus are tracked as future candidate tools for selected Rust proof
obligations unless a later reviewed proof phase moves a specific obligation
from candidate status to accepted evidence with pinned toolchain, assumptions,
output, and review.

No proof artifact, semantic runner, PXM implementation, MFVM implementation,
Confidential VM launch implementation, or production assurance claim is
created by this directory.
