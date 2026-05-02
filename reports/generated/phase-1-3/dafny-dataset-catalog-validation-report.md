# Dafny Dataset/Catalog Validation Report

Status: current.

The current Phase 1.3 Dafny module set verifies with `184 verified, 0 errors`.

Validated commands passed locally:

- `./scripts/validate-all.sh --check`
- `./scripts/validate-naming-safety.sh release`
- `./scripts/validate-artifact-hygiene.sh`
- `./scripts/validate-component-scaffold.sh`
- `./scripts/validate-language-formal-assurance.sh`
- `./scripts/validate-dafny-semantics.sh --require-dafny`
- `python3 scripts/checks/semantic-coverage/check-semantic-coverage-mapping.py`
- `python3 scripts/checks/formal-claims/check-formal-claim-coverage.py`
- `python3 scripts/phases/phase-1/check-phase1-gap-triage.py`
- `python3 scripts/phases/phase-1/check-phase1-2-auth-audit-coverage.py`
- `python3 scripts/phases/phase-1/check-phase1-3-dataset-catalog-coverage.py`
- `python3 -m py_compile $(find scripts tools -name '*.py' -type f | sort)`
- `git diff --check`
