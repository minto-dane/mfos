# tools/

Reserved future area for MFOS product and administrative tools. Current
validation and conformance-support tools belong under top-level `tools/`.

No Phase 1 implementation work belongs here. Future MFOS tools must not bypass
`securityd` or `auditd` semantics when they exercise protected operations.

Phase 1 is limited to non-production Dafny executable-semantics artifacts and
loader-only validation under `formal/executable-semantics/dafny/`.
Product/admin tool implementation, semantic-runner commands, hosted daemons,
Rust semantic-core work, generated production code, and Phase 1.4 implementation
artifacts remain forbidden until a later reviewed gate explicitly authorizes
them.
