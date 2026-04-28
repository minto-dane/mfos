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

python3 scripts/validate-source-cards.py
python3 scripts/validate-requirements.py
python3 scripts/check-prohibited-terms.py
python3 scripts/check-no-fake-success.py
python3 scripts/validate-spec-front-matter.py --mode "$MODE"
python3 scripts/validate-packs.py --mode "$MODE"
python3 scripts/check-source-grounding.py --mode "$MODE"
python3 scripts/check-audit-obligations.py --mode "$MODE"
python3 scripts/check-spec-gap-misuse.py --mode "$MODE"
python3 scripts/validate-claims.py --mode "$MODE"
python3 scripts/check-registry-links.py --mode "$MODE"
python3 scripts/check-phase-0-8-traceability.py --mode "$MODE"
./scripts/validate-phase-0-9.sh
./scripts/validate-artifact-hygiene.sh "$MODE"
python3 scripts/check-evidence-status.py --mode "$MODE"
./scripts/validate-naming-safety.sh "$MODE"
if [[ "$GENERATE_TRACEABILITY" == "1" ]]; then
  python3 scripts/generate-traceability.py
fi
