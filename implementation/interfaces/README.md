# interfaces/

Operator console, command-processor, panel-ui, management-api, POSIX subsystem,
and Linux gateway interface material. Interfaces cannot bypass central
authorization and audit.

No Phase 1 implementation work belongs here. Phase 1 is limited to Dafny
executable-semantics scaffold work and loader-only artifact validation under
`formal/executable-semantics/dafny/`. Interface implementation, hosted service
adapters, semantic runners, Rust semantic-core work, generated production code,
and production code remain forbidden until a later reviewed gate explicitly
authorizes them.
