#!/usr/bin/env bash
set -euo pipefail

GENERATE_TRACEABILITY=1
if [[ "${1:-}" == "--check" ]]; then
  GENERATE_TRACEABILITY=0
fi

python3 scripts/validators/validate-test-catalogs.py
python3 scripts/validators/validate-fixtures.py
python3 scripts/validators/validate-oracles.py
python3 scripts/validators/validate-golden-vectors.py
python3 scripts/validators/validate-fuzz-corpus-plan.py
python3 scripts/phases/phase-0-9/check-no-implementation.py
if [[ "$GENERATE_TRACEABILITY" == "1" ]]; then
  python3 scripts/phases/phase-0-9/generate-traceability.py
fi
