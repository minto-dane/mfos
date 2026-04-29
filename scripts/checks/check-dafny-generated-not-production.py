#!/usr/bin/env python3
"""Ensure Dafny generated output stays out of production paths."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, mode_arg


PRODUCTION_ROOTS = [
    ROOT / "implementation",
    ROOT / "services",
    ROOT / "nucleus",
    ROOT / "pxm",
    ROOT / "guard",
    ROOT / "runtime",
]


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []
    for root in PRODUCTION_ROOTS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if path.is_file() and ("dafny" in path.name.lower() or "generated" in path.parts):
                findings.append(Finding("ERROR", path, "Dafny generated artifacts must not appear in production paths"))
    return emit(findings, args.mode, "Dafny generated output production-path check OK")


if __name__ == "__main__":
    raise SystemExit(main())
