#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-draft}"

python3 scripts/check-artifact-layout.py --mode "$MODE"
python3 scripts/check-phase-name-policy.py --mode "$MODE"
python3 scripts/check-artifact-indexes.py --mode "$MODE"
python3 scripts/check-orphaned-artifacts.py --mode "$MODE"
