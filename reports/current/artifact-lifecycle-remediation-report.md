# Artifact Lifecycle Remediation Report

Status: current.

## Scope

Repository-wide artifact lifecycle boundaries were remediated for report
placement, generated/archive/phase separation, duplicate directory ownership,
and future implementation scaffolds.

## Remediation

- Moved phase-specific reports from `reports/current/` to
  `reports/phases/<phase-id>/`.
- Moved generated Phase 1.1 through Phase 1.3 reports to
  `reports/generated/phase-*`.
- Moved superseded and PR-review reports to `reports/archive/`.
- Added ownership metadata for reports lifecycle roots, current report packages,
  design packs, prompts, AI contracts, and implementation subdirectories.
- Gated ready hosted/service tasks in `docs/design/registries/tasks.yaml` as
  blocked future implementation tasks.
- Added lifecycle, current-report, generated-placement, index-integrity, and
  directory-ownership validators.

## Validation

Passed locally:

- `./scripts/validate-all.sh --check`
- `./scripts/validate-naming-safety.sh release`
- `./scripts/validate-artifact-hygiene.sh`
- `./scripts/validate-component-scaffold.sh`
- `./scripts/validate-language-formal-assurance.sh`
- `./scripts/validate-dafny-semantics.sh --require-dafny`
- `python3 scripts/check-semantic-coverage-mapping.py`
- `python3 scripts/check-formal-claim-coverage.py`
- `python3 scripts/check-phase1-gap-triage.py`
- `python3 scripts/check-phase1-2-auth-audit-coverage.py`
- `python3 scripts/check-phase1-3-dataset-catalog-coverage.py`
- `python3 scripts/check-architecture-portability-policy.py`
- `python3 scripts/check-x64-profile-policy.py`
- `python3 scripts/check-cpu-feature-registry.py`
- `python3 scripts/check-roadmap-phase-alignment.py`
- `python3 -m py_compile $(find scripts tools -name '*.py' -type f | sort)`
- `git diff --check`

Phase 1.4 remains planning-only. Production implementation, Rust semantic-core,
hosted daemons, semantic runners, and service implementations remain forbidden.
