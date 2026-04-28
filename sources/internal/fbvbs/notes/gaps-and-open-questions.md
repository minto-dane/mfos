# Gaps And Open Questions

Grounding source: FBVBS `dev` at `30e6fb54c76eaec83d03f79e1fd96c030cca504b`

## Source Gaps To Preserve

1. Real-hardware IOMMU, DMA remap, and interrupt remap closure remains a blocker in the source planning docs.
2. Final host deprivilege and launch handoff are not closed end to end.
3. Append-only OOB audit chain and incident evidence runtime linkage are not fully closed.
4. Standalone update/artifact freshness and secure-clock policy are explicitly underdeveloped.
5. Hardware validation and residual-risk evidence are not complete enough for a standalone-ready claim.
6. Live migration, checkpoint, replication, HA orchestration, and fleet primitives are out of current runtime scope.

## MFOS Open Questions

1. What is the MFOS authoritative design-root catalog?
2. Which MFOS objects need lifecycle command contracts first?
3. What trusted-time source and freshness window model will MFOS accept for update manifests?
4. Which MFOS evidence artifacts must be mandatory for release, incident, and support contexts?
5. Which validators are always-on versus heavy gates?
6. Who owns compatibility windows and reserved-field promotion in MFOS?

## Non-Transfer Notes

- Do not transfer FBVBS conformance labels as MFOS conformance labels.
- Do not transfer FreeBSD-specific or hypervisor-specific service semantics.
- Do not treat FBVBS release-readiness tooling as sufficient for MFOS release authorization.
