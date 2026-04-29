#!/usr/bin/env bash
set -euo pipefail

MODE="draft"
REQUIRE_DAFNY="${MFOS_REQUIRE_DAFNY:-0}"

for arg in "$@"; do
  case "$arg" in
    --check)
      MODE="draft"
      ;;
    --require-dafny)
      REQUIRE_DAFNY="1"
      ;;
    draft|release)
      MODE="$arg"
      ;;
    *)
      echo "Unknown argument: $arg" >&2
      exit 2
      ;;
  esac
done
export PYTHONDONTWRITEBYTECODE=1
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PINNED_DAFNY="${ROOT}/.tools/dafny/4.11.0/dafny/dafny"

python3 scripts/validators/validate-dafny-semantics-scaffold.py --mode "$MODE"
python3 scripts/validators/validate-dafny-semantics.py --mode "$MODE"
python3 scripts/validators/validate-fixture-golden-loader.py
python3 scripts/checks/check-phase1-no-rust-semantic-core.py --mode "$MODE"
python3 scripts/checks/check-dafny-generated-not-production.py --mode "$MODE"
python3 scripts/checks/check-semantic-fixture-normalizer.py --mode "$MODE"

mapfile -t DAFNY_MODULES < <(find formal/executable-semantics/dafny/modules -type f -name '*.dfy' | sort)
if [[ "${#DAFNY_MODULES[@]}" -eq 0 ]]; then
  echo "No Dafny modules found under formal/executable-semantics/dafny/modules" >&2
  exit 1
fi

if [[ -n "${DAFNY:-}" && -x "${DAFNY:-}" ]]; then
  "$DAFNY" verify "${DAFNY_MODULES[@]}"
elif [[ -x "$PINNED_DAFNY" ]]; then
  "$PINNED_DAFNY" verify "${DAFNY_MODULES[@]}"
elif command -v dafny >/dev/null 2>&1; then
  dafny verify "${DAFNY_MODULES[@]}"
else
  echo "Dafny verification skipped: blocked_by_missing_toolchain"
  if [[ "$REQUIRE_DAFNY" == "1" ]]; then
    echo "Dafny verification required but the dafny command is unavailable" >&2
    exit 1
  fi
fi
