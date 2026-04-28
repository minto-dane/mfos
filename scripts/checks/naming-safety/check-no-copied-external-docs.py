#!/usr/bin/env python3
"""Heuristic guard against copying external documentation into the repo."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

import re
from pathlib import Path

from lib.mfos_lint import Finding, emit, mode_arg, text_files


RISK_PATTERNS = [
    re.compile(r"\brecord layout\b", re.IGNORECASE),
    re.compile(r"\bmacro signature\b", re.IGNORECASE),
    re.compile(r"\bcommand syntax\b", re.IGNORECASE),
    re.compile(r"\bcopied excerpt\b", re.IGNORECASE),
]
SAFE_RE = re.compile(r"\b(no_|do not|did not|does not|must not|prohibit|prohibited|forbidden|lint|check|legal_controls|not copied|not reproduce|intentionally omit|intentionally avoid|intentionally exclude|intentionally excludes|excluded)\b", re.IGNORECASE)
LONG_QUOTE_RE = re.compile(r"^>\s+\S+(?:\s+\S+){35,}")
ROOTS = [Path("README.md"), Path("docs"), Path("sources"), Path("schemas"), Path("requirements"), Path("packs"), Path("ai"), Path("governance"), Path("adr")]


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    for path in text_files(ROOTS):
        if "reports" in path.parts:
            continue
        safe_until = 0
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if SAFE_RE.search(line):
                safe_until = lineno + 8
            if LONG_QUOTE_RE.search(line):
                findings.append(Finding("ERROR", path, "long block quote may copy external documentation", lineno))
            for pattern in RISK_PATTERNS:
                if pattern.search(line) and lineno > safe_until and not SAFE_RE.search(line):
                    findings.append(Finding("WARN", path, f"external-doc-copy risk term outside explicit prohibition: {pattern.pattern}", lineno))

    return emit(findings, args.mode, "External-doc copy guard OK")


if __name__ == "__main__":
    raise SystemExit(main())
