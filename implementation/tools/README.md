# tools/

Reserved future area for MFOS product and administrative tools. Current
validation and conformance-support tools belong under top-level `tools/`.

No Phase 1 implementation work belongs here. Future MFOS tools must not bypass
`securityd` or `auditd` semantics when they exercise protected operations.
