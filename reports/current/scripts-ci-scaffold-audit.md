# Scripts / CI Scaffold Audit

Validation scripts found: `38`

GitHub workflows found: `2`

`scripts/` now uses categorized subdirectories:

- `scripts/validators/`
- `scripts/checks/`
- `scripts/checks/artifact-hygiene/`
- `scripts/checks/naming-safety/`
- `scripts/generators/`
- `scripts/phases/`
- `scripts/lib/`

`validate-all.sh` includes source, requirement, spec, pack, traceability, Phase 0.9, artifact hygiene, evidence-status, and naming-safety checks.

CI invokes `./scripts/validate-all.sh --check` through `.github/workflows/design-validation.yml`.
The workflow labels this as draft check-mode validation because release-mode
evidence gates intentionally remain closed.

CodeQL workflow records the private repository upload limitation and skips upload-only analysis unless `MFOS_ENABLE_PRIVATE_CODEQL=true`.

Recommended action: keep CI invoking stable root entrypoints and avoid adding
new top-level script files unless they are compatibility entrypoints.
