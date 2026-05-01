#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-draft}"
if [[ "$MODE" == "--check" ]]; then
  MODE="draft"
fi

exec ./scripts/validators/validate-language-formal-assurance.sh "$MODE"
