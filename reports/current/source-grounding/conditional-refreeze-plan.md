# Conditional Refreeze Plan

The structural freeze remains valid. The semantic freeze is conditional.

Immediate downgrade:

- Phase 1 may load and validate artifacts only.
- Phase 1 may not implement Portable Semantic Core behavior, semantic
  evaluator logic, semantic runner commands, hosted daemons, or production
  services.
- `09-job-spool` is blocked for semantic evaluator work until the
  external-looking control-stream grammar and MFOS-owned JCL/DD-style
  identifiers are refactored or explicitly re-bounded.

Before semantic evaluator work:

1. Add direct spec/test refs to Source Cards.
2. Propagate source refs and target requirements into fixtures and
   golden/oracle vectors.
3. Align planned `010x` requirement tests with current `09xx` executable-spec
   artifacts, or add a machine-readable alias map.
4. Complete targeted source review for pin-review cards.

## Phase 0.10 Addendum

PXM, MFVM, Confidential VM, datacenter/cluster, language verification, automated reasoning, and performance/secure operations are structurally documented but semantically provisional. Phase 1 may validate loader-visible artifacts for these domains only. PXM/MFVM/CVM/cluster semantic evaluator work remains blocked until source grounding, profile-specific semantics, formal obligations, negative tests, and evidence mature.
