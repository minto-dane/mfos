# Dafny Conformance Harness

This is a non-production Phase 1 conformance-support harness. It checks that
fixtures, embedded oracles, and golden vectors are structurally comparable to
Dafny model output.

The harness does not implement the future semantic-runner contract, does not
start a daemon, and does not act as an MFOS service.

If the Dafny toolchain is unavailable, verification status must be recorded as
`blocked_by_missing_toolchain`; success must not be claimed.
