#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-draft}"

exec ./scripts/validators/validate-language-formal-assurance.sh "$MODE"
