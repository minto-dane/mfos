#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-draft}"
export PYTHONDONTWRITEBYTECODE=1

python3 scripts/checks/naming-safety/check-extref-namespace.py --mode "$MODE"
python3 scripts/checks/naming-safety/check-source-card-public-safe.py --mode "$MODE"
python3 scripts/checks/naming-safety/check-sources-workbench-public-safe.py --mode "$MODE"
python3 scripts/checks/naming-safety/check-requirement-namespace.py --mode "$MODE"
python3 scripts/checks/naming-safety/check-mf-owned-names.py --mode "$MODE"
python3 scripts/checks/naming-safety/check-no-compatibility-claims.py --mode "$MODE"
python3 scripts/checks/naming-safety/check-no-copied-external-docs.py --mode "$MODE"
