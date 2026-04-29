#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DAFNY_VERSION="4.11.0"
DAFNY_TAG="v${DAFNY_VERSION}"
DAFNY_ASSET="dafny-${DAFNY_VERSION}-x64-ubuntu-22.04.zip"
DAFNY_SHA256="a46a9ff7cdd720f7955854c78e95df13f4cfe6b80691b05f8654fe19e8267179"
INSTALL_ROOT="${MFOS_TOOLS_DIR:-${ROOT}/.tools}/dafny/${DAFNY_VERSION}"
DAFNY_DIR="${INSTALL_ROOT}/dafny"
DAFNY_BIN="${DAFNY_DIR}/dafny"
DAFNY_URL="https://github.com/dafny-lang/dafny/releases/download/${DAFNY_TAG}/${DAFNY_ASSET}"

if [[ "${1:-}" == "--print-bin" ]]; then
  echo "$DAFNY_BIN"
  exit 0
fi

if [[ -x "$DAFNY_BIN" ]]; then
  "$DAFNY_BIN" --version
  exit 0
fi

tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

archive="${tmpdir}/${DAFNY_ASSET}"
curl -fsSL "$DAFNY_URL" -o "$archive"
echo "${DAFNY_SHA256}  ${archive}" | sha256sum -c -

rm -rf "$INSTALL_ROOT"
mkdir -p "$INSTALL_ROOT"
python3 - "$archive" "$INSTALL_ROOT" <<'PY'
import sys
import zipfile
from pathlib import Path

archive = Path(sys.argv[1])
target = Path(sys.argv[2])
with zipfile.ZipFile(archive) as zip_file:
    zip_file.extractall(target)
PY

chmod +x "$DAFNY_BIN"
chmod +x "$DAFNY_DIR"/DafnyDriver 2>/dev/null || true
chmod +x "$DAFNY_DIR"/DafnyServer 2>/dev/null || true
chmod +x "$DAFNY_DIR"/z3/bin/z3-* 2>/dev/null || true

"$DAFNY_BIN" --version
