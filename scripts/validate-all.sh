#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-draft}"
GENERATE_TRACEABILITY=1

if [[ "$MODE" == "--check" ]]; then
  MODE="draft"
  GENERATE_TRACEABILITY=0
fi

if [[ "${2:-}" == "--check" ]]; then
  GENERATE_TRACEABILITY=0
fi

if [[ "$GENERATE_TRACEABILITY" == "0" ]]; then
  export MFOS_VALIDATE_NO_WRITE=1
fi
export PYTHONDONTWRITEBYTECODE=1

python3 scripts/validators/validate-source-cards.py
python3 scripts/validators/validate-schema-files.py --mode "$MODE"
python3 scripts/validators/validate-requirements.py
python3 scripts/checks/check-prohibited-terms.py
python3 scripts/checks/check-no-fake-success.py
python3 scripts/validators/validate-spec-front-matter.py --mode "$MODE"
python3 scripts/checks/check-architecture-portability-policy.py --mode "$MODE"
python3 scripts/checks/check-x64-profile-policy.py --mode "$MODE"
python3 scripts/checks/check-cpu-feature-registry.py --mode "$MODE"
python3 scripts/checks/check-roadmap-phase-alignment.py --mode "$MODE"
python3 scripts/validators/validate-packs.py --mode "$MODE"
python3 scripts/checks/check-source-grounding.py --mode "$MODE"
python3 scripts/checks/check-audit-obligations.py --mode "$MODE"
python3 scripts/checks/check-spec-gap-misuse.py --mode "$MODE"
python3 scripts/validators/validate-claims.py --mode "$MODE"
./scripts/validators/validate-language-formal-assurance.sh "$MODE"
./scripts/validate-dafny-semantics-scaffold.sh "$MODE"
./scripts/validate-dafny-semantics.sh "$MODE"
python3 scripts/check-semantic-coverage-mapping.py
python3 scripts/check-formal-claim-coverage.py
python3 scripts/check-phase1-gap-triage.py
python3 scripts/check-phase1-2-auth-audit-coverage.py
if [[ "$GENERATE_TRACEABILITY" == "1" ]]; then
  python3 scripts/checks/check-registry-links.py --mode "$MODE"
else
  python3 scripts/checks/check-registry-links.py --mode "$MODE"
fi
python3 scripts/phases/phase-0-8/check-traceability.py --mode "$MODE"
if [[ "$GENERATE_TRACEABILITY" == "1" ]]; then
  ./scripts/phases/phase-0-9/validate.sh
else
  ./scripts/phases/phase-0-9/validate.sh --check
fi
mapfile -t PYTHON_SOURCES < <(find scripts tools -name '*.py' -type f | sort)
if [[ "${#PYTHON_SOURCES[@]}" -gt 0 ]]; then
  python3 -m py_compile "${PYTHON_SOURCES[@]}"
  find scripts tools -type d -name __pycache__ -prune -exec rm -rf {} +
fi
./scripts/validate-artifact-hygiene.sh "$MODE"
./scripts/validate-component-scaffold.sh "$MODE"
python3 scripts/checks/check-phase1-red-team.py --mode "$MODE"
python3 scripts/checks/check-evidence-status.py --mode "$MODE"
./scripts/validate-naming-safety.sh "$MODE"
if [[ "$GENERATE_TRACEABILITY" == "1" ]]; then
  python3 scripts/generators/generate-traceability.py
  python3 scripts/generators/generate-semantic-coverage.py
  python3 scripts/generators/generate-auth-audit-coverage.py
fi
