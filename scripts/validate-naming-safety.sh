#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-draft}"

python3 scripts/check-extref-namespace.py --mode "$MODE"
python3 scripts/check-source-card-public-safe.py --mode "$MODE"
python3 scripts/check-requirement-namespace.py --mode "$MODE"
python3 scripts/check-mf-owned-names.py --mode "$MODE"
python3 scripts/check-no-compatibility-claims.py --mode "$MODE"
python3 scripts/check-no-copied-external-docs.py --mode "$MODE"
