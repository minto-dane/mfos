#!/usr/bin/env python3
"""Check that Phase 0.9 artifacts do not introduce implementation code."""

from __future__ import annotations

import sys
from pathlib import Path

from mfos_phase09 import ROOT, rel


PHASE09_ROOTS = [
    ROOT / "docs/design/specs",
    ROOT / "tests/catalog",
    ROOT / "tests/fixtures",
    ROOT / "tests/golden",
    ROOT / "fuzz/corpora",
    ROOT / "fuzz/targets",
    ROOT / "evidence/traceability",
    ROOT / "reports",
]
FORBIDDEN_SUFFIXES = {".rs", ".c", ".cc", ".cpp", ".h", ".hpp", ".go", ".java", ".kt", ".ts", ".js", ".sh"}
FORBIDDEN_PATTERNS = [
    "fn main(",
    "int main(",
    "class SemanticRunner",
    "def run_fixture(",
    "def evaluate_semantics(",
    "MFOS_ERR_UNSUPPORTED as success",
    "MFOS_ERR_SPEC_GAP as success",
]


def main() -> int:
    errors: list[str] = []
    for root in PHASE09_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix in FORBIDDEN_SUFFIXES and not str(path).endswith("validate-phase-0-9.sh"):
                errors.append(f"{rel(path)}: Phase 0.9 artifact must not introduce implementation source file")
                continue
            if path.suffix not in {".md", ".yml", ".yaml", ".txt"}:
                continue
            text = path.read_text(encoding="utf-8")
            for pattern in FORBIDDEN_PATTERNS:
                if pattern in text:
                    errors.append(f"{rel(path)}: forbidden implementation or fake-success pattern: {pattern}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Phase 0.9 no-implementation check OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
