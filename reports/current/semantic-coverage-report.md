# Phase 1.1 Semantic Coverage Truthfulness Report

This report records the post-review truthfulness remediation for Phase 1.1 Dafny semantic coverage.
Coverage levels are now derived from explicit per-test mappings; domain-wide symbol stamping and last-symbol fallback are prohibited.

## Result

- `phase_1_1_semantic_coverage_complete`: `false`
- `phase_1_1_core_domain_coverage_status`: `mixed_verified_and_partial`
- `phase_1_1_formal_claim_coverage_complete`: `false`
- `negative_semantics_complete`: `false`
- `audit_deny_before_return_transition_backed`: `true`
- `dafny_verification_result`: `97 verified, 0 errors`

## Coverage Distribution

```yaml
requirements:
  C0_NONE: 16
  C5_CONFORMANCE_LINKED: 2
tests:
  C0_NONE: 12
  C2_PARTIAL_SEMANTIC: 14
  C3_FULL_SEMANTIC: 16
  C4_VERIFIED_PROPERTY: 30
  C5_CONFORMANCE_LINKED: 2
fixtures:
  C0_NONE: 12
  C2_PARTIAL_SEMANTIC: 14
  C3_FULL_SEMANTIC: 16
  C4_VERIFIED_PROPERTY: 30
  C5_CONFORMANCE_LINKED: 2
oracles:
  C0_NONE: 12
  C2_PARTIAL_SEMANTIC: 14
  C3_FULL_SEMANTIC: 16
  C4_VERIFIED_PROPERTY: 30
  C5_CONFORMANCE_LINKED: 2
formal_claims:
  C0_NONE: 9
  C3_FULL_SEMANTIC: 2
```

## Domain Levels

```yaml
authorization: C0_NONE
audit: C0_NONE
dataset_catalog: C0_NONE
job_spool: C0_NONE
operator_console: C0_NONE
```

The first vertical slice remains `C5_CONFORMANCE_LINKED`. Other core domains contain a mix of verified properties and partial gaps, so Phase 1.1 is not claimed complete.
