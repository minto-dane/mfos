#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-draft}"
if [[ "$MODE" == "--check" ]]; then
  MODE="draft"
fi

python3 scripts/checks/check-component-scaffold.py --mode "$MODE"
