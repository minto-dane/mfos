#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-draft}"
if [[ "$MODE" == "--check" ]]; then
  MODE="draft"
fi
export PYTHONDONTWRITEBYTECODE=1

python3 scripts/checks/check-component-scaffold.py --mode "$MODE"
