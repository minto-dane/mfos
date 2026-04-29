#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-draft}"

python3 scripts/validators/validate-language-profiles.py --mode "$MODE"
python3 scripts/validators/validate-formal-registry.py --mode "$MODE"
python3 scripts/validators/validate-proof-obligations.py --mode "$MODE"
python3 scripts/checks/check-unsafe-inventory.py --mode "$MODE"
python3 scripts/checks/check-assembly-boundaries.py --mode "$MODE"
python3 scripts/checks/check-c-cxx-exceptions.py --mode "$MODE"
python3 scripts/checks/check-hardening-evidence.py --mode "$MODE"
python3 scripts/checks/check-no-proof-overclaim.py --mode "$MODE"
