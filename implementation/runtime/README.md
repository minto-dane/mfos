# runtime/

Shared runtime types, ABIs, generated IDs, and serialization support. This
directory is downstream of specs and requirements.

No Phase 1 implementation work belongs here. Phase 1 is limited to Dafny
executable-semantics scaffold work and loader-only artifact validation under
`formal/executable-semantics/dafny/`. Runtime ABI implementation, generated
production code, semantic runner work, Rust semantic-core work, hosted daemons,
and production code remain forbidden until a later reviewed gate explicitly
authorizes them.
