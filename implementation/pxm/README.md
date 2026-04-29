# pxm/

PXM partition manager. PXM provides partition lifecycle and isolation. It must
not interpret MFOS job, dataset, catalog, spool, security, audit, or workload policy
semantics.

No Phase 1 implementation work belongs here. Phase 1 is limited to Dafny
executable-semantics scaffold work and loader-only artifact validation under
`formal/executable-semantics/dafny/`. PXM, MFVM, CVM, partition, device,
hardware-enforcement, hosted daemon, semantic runner, Rust semantic-core,
generated production code, and production implementation work remain forbidden
until a later reviewed gate explicitly authorizes them.
