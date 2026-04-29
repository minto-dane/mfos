# Fixed-Point Issue Ledger

Branch: `fix/pre-phase1-fixedpoint-closure`

## Summary

- Critical before fixes: `1`
- Major before fixes: `12`
- Critical remaining: `0`
- Major remaining: `0`
- Phase 1 blockers remaining: `0`
- Minor/Informational deferred: `2`

## Issues

### FP-0001 - Source grounding audit counted 37 cards after the ledger grew to 65

- Severity: `Major`
- Category: `source_grounding`
- Status: `fixed`
- Phase 1 blocker: `false`
- Fix: Updated Source Card grounding audit to 65 cards and classified SG6/SG7 absence as conditional semantic-evaluator blocker, not Phase 1 loader blocker.
- Notes: Semantic evaluator remains conditional.

### FP-0002 - Current scaffold inventories referenced removed hosted semantic prototype paths

- Severity: `Major`
- Category: `reports`
- Status: `fixed`
- Phase 1 blocker: `false`
- Fix: Filtered missing directories from inventories and removed stale hosted-semantic next-action references.

### FP-0003 - Canonical test registry referenced a nonexistent fake-success fixture path

- Severity: `Major`
- Category: `tests`
- Status: `fixed`
- Phase 1 blocker: `false`
- Fix: Cleared fixture list and added fixture_policy explaining no executable fake-success fixture is stored.

### FP-0004 - No-implementation validator did not forbid Python or shell implementation files in scaffold roots

- Severity: `Major`
- Category: `validation`
- Status: `fixed`
- Phase 1 blocker: `false`
- Fix: Added .py and .sh to forbidden suffixes for Phase 0.9 no-implementation scan.
- Notes: No existing implementation source files were present.

### FP-0005 - Design README reading order omitted Phase 0.9/0.10/Phase 1 specs

- Severity: `Major`
- Category: `docs`
- Status: `fixed`
- Phase 1 blocker: `false`
- Fix: Added specs 30-first-vertical-slice through 43-Dafny policy to the reading order.

### FP-0006 - Schema artifact validator produced draft warnings for current MFOS schemas

- Severity: `Major`
- Category: `schemas`
- Status: `fixed`
- Phase 1 blocker: `false`
- Fix: Updated validator and four schemas; draft schema validation now has no warnings.

### FP-0007 - CI and root README local-check guidance was stale

- Severity: `Minor`
- Category: `ci`
- Status: `fixed`
- Phase 1 blocker: `false`
- Fix: Updated README and ci/README guidance.

### FP-0008 - Expected evidence IDs in Phase 0.9 artifacts are planned and not registry-backed evidence artifacts

- Severity: `Minor`
- Category: `evidence`
- Status: `accepted_deferred`
- Phase 1 blocker: `false`
- Fix: Generated Phase 0.9 gap report records 74 missing_evidence entries; no fake evidence was created.
- Notes: Blocks semantic evaluator/production claims, not loader-only validation.

### FP-0009 - Source Cards remain draft and no card reaches SG6/SG7

- Severity: `Minor`
- Category: `source_grounding`
- Status: `accepted_deferred`
- Phase 1 blocker: `false`
- Fix: Updated source-grounding audit and fixedpoint reports to state loader-only scope remains allowed while semantic evaluator remains conditional.
- Notes: Not a Phase 1 Dafny scaffold blocker.

### FP-0010 - Forbidden scope booleans were inverted in current readiness YAML

- Severity: `Critical`
- Category: `phase_gate`
- Status: `fixed`
- Phase 1 blocker: `false`
- Fix: Set forbidden_scope values to true for current readiness gate reports.

### FP-0011 - Pack index routed design-only packs to implementation output paths

- Severity: `Major`
- Category: `packs`
- Status: `fixed`
- Phase 1 blocker: `false`
- Fix: Updated PACK-13, PACK-15, and PACK-16 outputs and normalized implementation_allowed flags across pack-index entries.

### FP-0012 - PACK-34 and PACK-35 referenced test IDs absent from current catalogs

- Severity: `Major`
- Category: `tests`
- Status: `fixed`
- Phase 1 blocker: `false`
- Fix: PACK-34 now references TEST-MFOS-LANG-0101 and NEG-MFOS-LANG-0103; PACK-35 references TEST-MFOS-FORMAL-0101 and NEG-MFOS-FORMAL-0108.

### FP-0013 - Formal proof obligations mixed later Rust tools into accepted current tool refs

- Severity: `Major`
- Category: `formal`
- Status: `fixed`
- Phase 1 blocker: `false`
- Fix: Split accepted current tools from future candidates and documented aggregate vs split formal registries.
- Notes: No proof is claimed.

### FP-0014 - Source cards referenced non-registered requirement IDs after namespace cleanup

- Severity: `Major`
- Category: `source_grounding`
- Status: `fixed`
- Phase 1 blocker: `false`
- Fix: Updated source-card mfos_requirements and requirement_refs to registered WPOL, LANG, FORMAL, ASSURANCE, CVM, and OPS IDs.

### FP-0015 - Implementation leaf README files did not all restate Phase 1 prohibition boundaries

- Severity: `Major`
- Category: `implementation_scaffold`
- Status: `fixed`
- Phase 1 blocker: `false`
- Fix: Added explicit Phase 1 prohibition text to Guard, interfaces, nucleus, PXM, and runtime README files.
