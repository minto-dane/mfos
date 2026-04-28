#!/usr/bin/env python3
"""Detect wording that treats UNSUPPORTED or SPEC_GAP as success."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

import re
from pathlib import Path

from lib.mfos_lint import Finding, emit, mode_arg, text_files


MISUSE_PATTERNS = [
    re.compile(r"\b(?:UNSUPPORTED|MFOS_ERR_UNSUPPORTED|SPEC_GAP|MFOS_ERR_SPEC_GAP)\b.{0,80}\b(?:may|can|allowed to|permits?)\b.{0,40}\b(?:success|succeed|pass|allow|OK|MFOS_OK)\b", re.IGNORECASE),
    re.compile(r"\b(?:returns?|yields?)\s+(?:success|OK|MFOS_OK)\b.{0,80}\b(?:UNSUPPORTED|MFOS_ERR_UNSUPPORTED|SPEC_GAP|MFOS_ERR_SPEC_GAP)\b", re.IGNORECASE),
    re.compile(r"\b(?:UNSUPPORTED|MFOS_ERR_UNSUPPORTED|SPEC_GAP|MFOS_ERR_SPEC_GAP)\b.{0,80}\b(?:returns?|yields?)\s+(?:success|OK|MFOS_OK)\b", re.IGNORECASE),
]
SAFE_CONTEXT = re.compile(r"\b(?:must not|not |never|negative|test must fail|prohibited|detect|reject|absence|cannot|no success|not success|fail closed|failure|treats? .{0,30} as success|around)\b", re.IGNORECASE)


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []
    roots = [
        Path("docs/design"),
        Path("requirements"),
        Path("claims"),
        Path("packs"),
        Path("specs"),
        Path("prompts"),
        Path("ci"),
        Path("implementation"),
    ]
    for path in text_files(roots):
        severity = "BLOCK" if "implementation" in path.parts else "WARN"
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if "UNSUPPORTED" not in line and "SPEC_GAP" not in line:
                continue
            if SAFE_CONTEXT.search(line):
                continue
            if any(pattern.search(line) for pattern in MISUSE_PATTERNS):
                findings.append(Finding(severity, path, "possible UNSUPPORTED/SPEC_GAP success-path wording", lineno))
    return emit(findings, args.mode, "SPEC_GAP/UNSUPPORTED misuse check OK")


if __name__ == "__main__":
    raise SystemExit(main())
