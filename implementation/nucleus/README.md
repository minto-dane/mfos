# nucleus/

Reserved future MFOS nucleus implementation area. Production nucleus work should
wait until the relevant system-integrity, object, authorization, audit,
SVC/PCALL, and hardware profile specs are reviewed.

No Phase 1 implementation work belongs here. Phase 1 is limited to Dafny
executable-semantics scaffold work and loader-only artifact validation under
`formal/executable-semantics/dafny/`. Nucleus implementation, hardware-facing
execution work, hosted daemon work, semantic runner work, Rust semantic-core
work, generated production code, and production code remain forbidden until a
later reviewed gate explicitly authorizes them.
