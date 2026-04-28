# Scripts / CI Scaffold Audit

Validation scripts found: `38`

GitHub workflows found: `2`

`validate-all.sh` includes source, requirement, spec, pack, traceability, Phase 0.9, artifact hygiene, evidence-status, and naming-safety checks.

CI invokes `./scripts/validate-all.sh --check` through `.github/workflows/design-validation.yml`.

CodeQL workflow records the private repository upload limitation and skips upload-only analysis unless `MFOS_ENABLE_PRIVATE_CODEQL=true`.

Recommended action: either remove empty `ci/linters/*` placeholders or index them as mirrors of scripts-based validators.
