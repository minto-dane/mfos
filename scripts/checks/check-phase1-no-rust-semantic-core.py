#!/usr/bin/env python3
"""Reject Rust semantic-core artifacts in Phase 1."""

from __future__ import annotations

from pathlib import Path
import re
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, mode_arg


SEMANTIC_CORE = re.compile(r"(?:^|/)(?:rust[-_]?semantic[-_]?core|semantic[-_]?core|portable[-_]?semantic[-_]?core)(?:/|$)", re.IGNORECASE)


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []
    for path in sorted(ROOT.rglob("*")):
        if ".git" in path.parts or not path.exists():
            continue
        if path == Path(__file__).resolve():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if SEMANTIC_CORE.search(rel):
            findings.append(Finding("ERROR", path, "Phase 1 must not create Rust semantic-core or Portable Semantic Core artifacts"))
        if path.is_file() and path.suffix == ".rs":
            if path.is_relative_to(ROOT / "formal" / "executable-semantics"):
                findings.append(Finding("ERROR", path, "Rust files are forbidden under Phase 1 executable semantics"))
    return emit(findings, args.mode, "Phase 1 Rust semantic-core absence check OK")


if __name__ == "__main__":
    raise SystemExit(main())
