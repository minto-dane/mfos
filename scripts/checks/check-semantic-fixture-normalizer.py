#!/usr/bin/env python3
"""Check that Phase 1 fixture normalizer tooling stays metadata-only."""

from __future__ import annotations

from pathlib import Path
import re
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, mode_arg


TOOL_ROOTS = [
    ROOT / "tools" / "semantic-fixture-normalizer",
    ROOT / "tools" / "dafny-conformance-harness",
]
BUSINESS_LOGIC = re.compile(
    r"\b(?:authorize|authenticate|decide|schedule|dispatch|allocate|mount|open_dataset|execute_job|run_step|purge_spool)\s*\(",
    re.IGNORECASE,
)
HOSTED = re.compile(r"\b(?:HTTPServer|socketserver|serve_forever|listen|bind|uvicorn|flask|fastapi)\b")


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []
    for root in TOOL_ROOTS:
        if not root.exists():
            findings.append(Finding("ERROR", root, "required Phase 1 tool directory missing"))
            continue
        for path in sorted(root.rglob("*.py")):
            for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if BUSINESS_LOGIC.search(line):
                    findings.append(Finding("ERROR", path, "normalizer/harness must not encode MFOS business semantics", lineno))
                if HOSTED.search(line):
                    findings.append(Finding("ERROR", path, "normalizer/harness must not implement hosted daemon behavior", lineno))
    return emit(findings, args.mode, "Semantic fixture normalizer boundary check OK")


if __name__ == "__main__":
    raise SystemExit(main())
