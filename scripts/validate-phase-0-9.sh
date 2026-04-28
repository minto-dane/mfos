#!/usr/bin/env bash
set -euo pipefail

python3 scripts/validate-test-catalogs.py
python3 scripts/validate-fixtures.py
python3 scripts/validate-oracles.py
python3 scripts/validate-golden-vectors.py
python3 scripts/validate-fuzz-corpus-plan.py
python3 scripts/check-phase-0-9-no-implementation.py
python3 scripts/generate-phase-0-9-traceability.py
