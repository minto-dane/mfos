#!/usr/bin/env python3
"""Check for unguarded compatibility wording in project text files."""

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
    Path("README.md"),
    Path("README.ja.md"),
    Path("docs"),
    Path("reports"),
    Path("tasks"),
    Path("evidence"),
    Path("ai"),
    Path("governance"),
    Path("adr"),
    Path("sources"),
    Path("source-matrix"),
    Path("requirements"),
    Path("specs"),
    Path("prompts"),
    Path("packs"),
    Path("ci"),
    Path("implementation"),
]

TEXT_SUFFIXES = {".md", ".yml", ".yaml", ".txt"}

PATTERNS = [
    re.compile(r"\bIBM\s+official\b", re.IGNORECASE),
    re.compile(r"\bofficial\s+IBM\b", re.IGNORECASE),
    re.compile(r"\bofficial\s+IBM[- ]published\b", re.IGNORECASE),
    re.compile(r"\bofficial\s+MFOS\b", re.IGNORECASE),
    re.compile(r"\bMFOS\s+official\b", re.IGNORECASE),
    re.compile(r"\bIBM\s+(?:approval|affiliation|sponsorship|endorsement)\b", re.IGNORECASE),
    re.compile(r"\b(?:approved|endorsed|sponsored)\s+by\s+IBM\b", re.IGNORECASE),
    re.compile(r"IBM\s*公式"),
    re.compile(r"公式資料"),
    re.compile(r"公式概念"),
    re.compile(r"公式の"),
    re.compile(r"公式MFOS"),
    re.compile(r"IBM\s*による\s*(?:承認|提携|後援|推奨|公認)"),
    re.compile(r"\bz/OS[- ]compatible\b", re.IGNORECASE),
    re.compile(r"\bRACF[- ]compatible\b", re.IGNORECASE),
    re.compile(r"\bJES[- ]compatible\b", re.IGNORECASE),
    re.compile(r"\bDFSMS[- ]compatible\b", re.IGNORECASE),
    re.compile(r"\bAPF[- ]compatible\b", re.IGNORECASE),
    re.compile(r"\bPR/SM[- ]compatible\b", re.IGNORECASE),
]

SAFE_MARKERS = (
    "not ",
    "not:",
    "does not",
    "do not",
    "must not",
    "fail",
    "prohibit",
    "prohibited",
    "reject",
    "rejected",
    "forbidden",
    "non-compat",
    "negative",
    "lint",
    "avoid implying",
    "avoids implying",
    "without implying",
    "does not imply",
    "do not imply",
    "must not imply",
    "must not claim",
    "no claim",
    "not claim",
    "not claimed",
    "禁止",
    "主張しません",
    "主張してはならない",
    "主張しない",
    "示唆してはならない",
    "誤解を避ける",
)

SAFE_BLOCK_MARKERS = (
    "prohibited",
    "non-compat",
    "negative test",
    "negative_tests",
    "lint",
    "must not",
    "do not",
    "does not",
    "is not:",
    "avoid implying",
    "without implying",
    "reviewed current",
    "禁止",
    "主張しません",
    "主張してはならない",
    "主張しない",
    "示唆してはならない",
)

SAFE_FIELD_PREFIXES = (
    "prohibited_inference:",
    "prohibited_claims:",
    "prohibited_wording:",
    "prohibited_terms:",
    "negative_tests:",
    "required_negative_tests:",
    "allowed_contexts:",
    "allowlisted_contexts:",
    "prohibited wording",
    "禁止表現",
)


def iter_files() -> list[Path]:
    files: list[Path] = []
    for root in ROOTS:
        if root.is_file():
            files.append(root)
        elif root.is_dir():
            files.extend(path for path in root.rglob("*") if path.is_file())
    return sorted(path for path in files if path.suffix in TEXT_SUFFIXES)


def main() -> int:
    findings: list[str] = []

    for path in iter_files():
        in_prohibited_block = False
        safe_context_until = 0
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            stripped = line.strip().lower()
            if any(marker in stripped for marker in SAFE_BLOCK_MARKERS):
                safe_context_until = lineno + 40

            if stripped.startswith(SAFE_FIELD_PREFIXES):
                in_prohibited_block = True
            elif line and not line.startswith((" ", "-", "\t")) and ":" in line:
                in_prohibited_block = False

            if not any(pattern.search(line) for pattern in PATTERNS):
                continue

            lower = line.lower()
            if in_prohibited_block or lineno <= safe_context_until or any(marker in lower for marker in SAFE_MARKERS):
                continue

            findings.append(f"{path}:{lineno}: {line.strip()}")

    if findings:
        print("Unguarded compatibility wording found:", file=sys.stderr)
        for finding in findings:
            print(f"- {finding}", file=sys.stderr)
        return 1

    print("Prohibited wording check OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
