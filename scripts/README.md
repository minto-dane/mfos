# scripts/

Local validation, lint, generation, and bootstrap entrypoints.

The root of this directory is reserved for stable convenience entrypoints and
metadata. Individual checks live under categorized subdirectories:

- `validators/`: schema and artifact validators.
- `checks/`: policy and repository-safety checks.
- `checks/naming-safety/`: external-reference and naming-safety checks.
- `checks/artifact-hygiene/`: repository artifact layout checks.
- `generators/`: deterministic generated-artifact writers.
- `phases/`: phase-specific validation helpers.
- `lib/`: shared validation helpers.
- `bootstrap/`: scaffold/bootstrap maintenance scripts.

Python validators and checks are invoked with `python3 <path>` through the
stable shell entrypoints. They are not required to be directly executable.

Current useful checks:

```bash
python3 scripts/validators/validate-source-cards.py
python3 scripts/validators/validate-requirements.py
python3 scripts/validators/validate-claims.py
python3 scripts/validators/validate-spec-front-matter.py
python3 scripts/validators/validate-packs.py
python3 scripts/checks/check-prohibited-terms.py
python3 scripts/checks/check-no-fake-success.py
python3 scripts/checks/check-source-grounding.py
python3 scripts/checks/check-audit-obligations.py
python3 scripts/checks/check-spec-gap-misuse.py
python3 scripts/generators/generate-traceability.py
./scripts/validate-all.sh
./scripts/validate-artifact-hygiene.sh
./scripts/validate-naming-safety.sh release
```

`./scripts/validate-all.sh` is the stable convenience entrypoint. It runs the
local draft-mode validation suite and regenerates traceability matrices unless
`--check` is supplied.

Use `--mode release` on validators that support it only after draft warnings
have been resolved. Phase 0.6 remains a design-enforcement phase and does not
authorize production implementation.
