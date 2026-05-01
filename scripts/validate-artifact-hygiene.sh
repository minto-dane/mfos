#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-draft}"

if [[ "$MODE" == "--check" ]]; then
  MODE="draft"
fi

if [[ "${2:-}" == "--check" ]]; then
  :
fi
export PYTHONDONTWRITEBYTECODE=1

python3 scripts/checks/artifact-hygiene/check-artifact-layout.py --mode "$MODE"
python3 scripts/checks/artifact-hygiene/check-artifact-lifecycle-boundaries.py --mode "$MODE"
python3 scripts/checks/artifact-hygiene/check-build-directory-policy.py --mode "$MODE"
python3 scripts/checks/artifact-hygiene/check-phase-name-policy.py --mode "$MODE"
python3 scripts/checks/artifact-hygiene/check-reports-current-policy.py --mode "$MODE"
python3 scripts/checks/artifact-hygiene/check-current-domain-structure.py --mode "$MODE"
python3 scripts/checks/artifact-hygiene/check-report-domain-indexes.py --mode "$MODE"
python3 scripts/checks/artifact-hygiene/check-reports-current-lifecycle-metadata.py --mode "$MODE"
python3 scripts/checks/artifact-hygiene/check-generated-artifact-placement.py --mode "$MODE"
python3 scripts/checks/artifact-hygiene/check-artifact-indexes.py --mode "$MODE"
python3 scripts/checks/artifact-hygiene/check-index-integrity.py --mode "$MODE"
python3 scripts/checks/artifact-hygiene/check-directory-ownership.py --mode "$MODE"
python3 scripts/checks/artifact-hygiene/check-script-namespace-ownership.py --mode "$MODE"
python3 scripts/checks/artifact-hygiene/check-cross-directory-duplicates.py --mode "$MODE"
python3 scripts/checks/artifact-hygiene/check-flat-directory-pressure.py --mode "$MODE"
python3 scripts/checks/artifact-hygiene/check-orphaned-artifacts.py --mode "$MODE"
