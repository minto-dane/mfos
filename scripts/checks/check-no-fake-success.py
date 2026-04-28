#!/usr/bin/env python3
"""Scan implementation areas for obvious fake-success placeholders."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

import re
import sys
from pathlib import Path


ROOTS = [
    Path("implementation/nucleus"),
    Path("implementation/services"),
    Path("implementation/pxm"),
    Path("implementation/guard"),
    Path("implementation/runtime"),
    Path("implementation/prototypes"),
    Path("implementation/tools"),
]

CODE_SUFFIXES = {".rs", ".c", ".h", ".cpp", ".hpp", ".py", ".sh"}

PATTERNS = [
    re.compile(r"\btodo!\s*\("),
    re.compile(r"\bunimplemented!\s*\("),
    re.compile(r"\bpanic!\s*\(\s*[\"']TODO"),
    re.compile(r"\breturn\s+MFOS_OK\s*;\s*//\s*(stub|todo|placeholder)", re.IGNORECASE),
    re.compile(r"\bOk\(\s*\)\s*//\s*(stub|todo|placeholder)", re.IGNORECASE),
    re.compile(r"fake\s+success", re.IGNORECASE),
    re.compile(r"silent\s+fallback", re.IGNORECASE),
]


def main() -> int:
    findings: list[str] = []
    for root in ROOTS:
        if not root.exists():
            continue
        for path in sorted(p for p in root.rglob("*") if p.is_file() and p.suffix in CODE_SUFFIXES):
            for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if any(pattern.search(line) for pattern in PATTERNS):
                    findings.append(f"{path}:{lineno}: {line.strip()}")

    if findings:
        print("Fake-success placeholders found:", file=sys.stderr)
        for finding in findings:
            print(f"- {finding}", file=sys.stderr)
        return 1

    print("No fake-success placeholders found in implementation areas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
