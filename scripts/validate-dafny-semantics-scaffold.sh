#!/usr/bin/env bash
set -euo pipefail

case "${1:-draft}" in
  --check)
    MODE="draft"
    ;;
  *)
    MODE="${1:-draft}"
    ;;
esac

python3 scripts/validators/validate-dafny-semantics-scaffold.py --mode "$MODE"
