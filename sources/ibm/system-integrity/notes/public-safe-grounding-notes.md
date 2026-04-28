# Public-Safe Grounding Notes

## Review Position

The system-integrity cards are source-discovery and MFOS mapping artifacts only.
They intentionally avoid IBM implementation details, command syntax, macro
interfaces, copied examples, and scanner output. IBM URLs are pointers for human
review, not embedded source substitutes.

## Requirements Hooks

- `MFOS-REQ-SYSINT-0001` through `MFOS-REQ-SYSINT-0009` need explicit interface, state-transition, and fail-closed tests.
- `MFOS-REQ-AMF-0001`, `MFOS-REQ-AMF-0003`, `MFOS-REQ-AMF-0004`, and `MFOS-REQ-AMF-0007` need signed-module, revocation, and audit coverage.
- `MFOS-REQ-NUCLEUS-0005` needs PCALL sealed-buffer validation.

## Negative Tests

- Unauthorized requests must not bypass protection, security decisions, or authorized-state controls.
- AMF must reject unsigned, revoked, or authority-confused modules.
- PCALL must reject foreign pointers, unsealed buffers, and unregistered endpoints.
- Public review must reject claims that MFOS implements APF, SVC, PC instruction, zACS, or z/OS compatibility.

## Key Gaps

- Exact IBM publication identifiers remain absent for Basic Skills topics.
- MFOS still needs a public system-integrity statement written entirely in MFOS-native terms.
- Storage-protection terminology needs a reviewed divergence table before broader use.
- Scanner-style testing needs a safe-public reporting format that excludes exploit mechanics and sensitive output.
