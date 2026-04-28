#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-draft}"

if [[ "$MODE" == "--check" ]]; then
  MODE="draft"
fi

if [[ "${2:-}" == "--check" ]]; then
  :
fi

python3 scripts/checks/artifact-hygiene/check-artifact-layout.py --mode "$MODE"
python3 scripts/checks/artifact-hygiene/check-phase-name-policy.py --mode "$MODE"
python3 scripts/checks/artifact-hygiene/check-artifact-indexes.py --mode "$MODE"
python3 scripts/checks/artifact-hygiene/check-orphaned-artifacts.py --mode "$MODE"
