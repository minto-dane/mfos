# Semantic Coverage Open Issues

Status date: 2026-04-29

## Nonblocking Issues

No Phase 1.1 Critical or Major issues remain.

Remaining nonblocking items:

- Per-fixture Dafny execution is not yet claimed. Phase 1.1 maps fixtures,
  oracles, and golden vectors to Dafny targets and keeps Python comparison
  non-semantic.
- Formal claims outside authorization and audit remain `C0_NONE` for Dafny in
  this Phase 1.1 closure because PXM/MFVM/CVM/cluster/update semantics are not
  authorized Phase 1.1 implementation targets.
- `C6_RELEASE_READY_MODEL` is not claimed for any domain.

## Boundary

```yaml
phase_1_1_blocker: false
production_implementation_allowed: false
rust_phase_1_canonical_semantics_allowed: false
hosted_daemon_implementation_allowed: false
semantic_runner_implementation_allowed: false
```
