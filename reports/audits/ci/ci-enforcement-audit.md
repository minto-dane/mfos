# CI Enforcement Audit: Evidence Status and Design Validation

Date: 2026-04-27  
Scope: local validation and CI connection only.  
Production implementation: not started.

## Summary

This pass adds deterministic enforcement for evidence status. Draft evidence remains
allowed during design phases, but it cannot be represented as verified proof. In
release mode, assurance claims are blocked unless every linked evidence record is
registered, `verified` or `archived`, hash-backed, and verification metadata is
complete.

The draft-safe validation path is now connected to `./scripts/validate-all.sh`.
A simple GitHub Actions workflow was added to run the same draft-safe design
validation in CI.

## Files Changed

- `.github/workflows/design-validation.yml`
- `scripts/check-evidence-status.py`
- `scripts/validate-all.sh`
- `docs/design/assurance/claim-tree.yml`
- `docs/design/registries/evidence.yaml`
- `evidence/traceability/current/claim-to-requirement.yml`
- `evidence/traceability/current/gap-report.yml`
- `evidence/traceability/current/requirement-to-evidence.yml`
- `evidence/traceability/current/requirement-to-spec.yml`
- `evidence/traceability/current/requirement-to-test.yml`
- `evidence/traceability/current/source-to-requirement.yml`
- `evidence/traceability/current/pack-to-artifacts.yml`
- `reports/generated/traceability.md`
- `reports/audits/ci/ci-enforcement-audit.md`

## Enforcement Added

`scripts/check-evidence-status.py` checks:

- Evidence status is one of `draft`, `collected`, `verified`, `archived`,
  `rejected`, `expired`, or `superseded`.
- `draft` evidence must not use `verification.result: pass`.
- `draft` evidence must not use release, production, or High-Assurance retention
  class.
- `draft` evidence must not bind to `release_ids`.
- Claim-linked draft evidence is reported as warning in draft mode.
- `verified` or `archived` evidence requires:
  - `artifact.sha384`
  - `verification.result: pass`
  - `verification.verifier`
  - `verification.verified_at_utc`
  - `verification.verification_method`
- `rejected`, `expired`, and `superseded` evidence cannot support claims.
- Release mode requires every claim evidence reference to resolve to verified or
  archived evidence.

## Claim/Evidence Cleanup

The claim tree had legacy evidence IDs that were not registered in the evidence
registry. Those were replaced with registered draft evidence where matching
draft evidence already existed.

Three missing High-Assurance placeholders were added as draft evidence records:

- `MFOS-EVID-GRD-ROOT-0001`
- `MFOS-EVID-GRD-AUDIT-0007`
- `MFOS-EVID-ATTESTATION-HA-0001`

These are traceability placeholders only. They are not verified evidence.

## CI Connection

`.github/workflows/design-validation.yml` runs:

```bash
./scripts/validate-all.sh
```

The workflow installs `pyyaml` and runs in draft-safe mode. It does not run
release mode because release-mode validation is expected to fail until real
artifacts, digests, and verification records exist.

## Validation Commands

```bash
./scripts/validate-all.sh
python3 scripts/check-evidence-status.py --mode release
python3 -m py_compile scripts/*.py
```

## Validation Results

Draft-safe validation:

```yaml
validate_all: passed
source_cards: "37 cards"
requirements: "106 entries"
spec_front_matter: "35 specs checked, 0 warnings"
packs: "31 packs checked, 0 warnings"
source_grounding: "0 warnings"
claims: "5 claims checked, 0 warnings"
evidence_status: "36 entries checked, 38 draft warnings"
traceability: regenerated
```

Release-mode evidence status check:

```yaml
result: expected_failure
errors: 18
warnings: 20
reason: all claim evidence remains draft and therefore cannot support release-mode claims
```

Python compile:

```yaml
result: passed
```

## Remaining Gaps

- Release-mode claims are blocked until evidence records are backed by real
  artifacts, SHA-384 digests, verification methods, verifier identity, and
  verification timestamps.
- Draft-safe validation still reports registry coverage warnings for
  requirements that do not yet have test/evidence registry links.
- The CI workflow currently runs draft-safe validation only. Release validation
  should be added as a separate manual or release-gate job after verified
  evidence archives exist.

## Gate Judgment

```yaml
production_implementation_allowed: false
hosted_semantic_prototype_allowed: only_for_packs_that_pass_pre_implementation_gate
release_claims_allowed: false
next_step: continue registry coverage and verified evidence archive work
```
