# sidecars/

Reserved future area for side partitions such as Linux desktop, service,
recovery, and diagnostics partitions. Sidecars do not live inside MFOS
enterprise semantics.

No Phase 1 implementation work belongs here. Phase 1 is limited to Dafny
executable-semantics scaffold work and loader-only artifact validation under
`formal/executable-semantics/dafny/`. Sidecar implementation, hosted daemon
work, semantic runner work, Rust semantic-core work, generated production code,
and production code remain forbidden until a later reviewed gate explicitly
authorizes them.
