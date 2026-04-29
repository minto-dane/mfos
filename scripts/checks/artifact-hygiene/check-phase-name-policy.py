#!/usr/bin/env python3
"""Enforce phase-name placement policy for repository artifacts."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

import re
from pathlib import Path

from lib.mfos_lint import Finding, ROOT, emit, mode_arg


PHASE_RE = re.compile(r"phase-\d+(?:-\d+)*", re.IGNORECASE)

CANONICAL_ROOTS = [
    Path("specs"),
    Path("requirements"),
    Path("schemas"),
    Path("claims"),
    Path("tests/catalog"),
    Path("tests/fixtures"),
    Path("tests/golden"),
    Path("packs"),
    Path("services"),
    Path("runtime"),
    Path("interfaces"),
    Path("implementation"),
    Path("docs/design/specs"),
    Path("docs/design/tasks"),
    Path("fuzz/targets"),
    Path("scripts"),
    Path("tasks"),
    Path("reports/current"),
]

ALLOWED_PREFIXES = (
    "reports/phases/",
    "reports/archive/",
    "reports/current/fixedpoint/",
    "evidence/archive/",
    "evidence/traceability/archive/",
    "evidence/traceability/generated/",
    "migration/",
    "archive/",
    "docs/design/history/",
    "docs/design/tasks/archive/",
    "fuzz/targets/archive/",
    "scripts/phases/",
    "tasks/archive/",
    "tests/catalog/archive/",
    "tests/fixtures/archive/",
    "tests/golden/archive/",
)


def is_allowed(path: Path) -> bool:
    rel = str(path.relative_to(ROOT))
    return rel.startswith(ALLOWED_PREFIXES)


def in_canonical_root(path: Path) -> bool:
    try:
        rel = path.relative_to(ROOT)
    except ValueError:
        return False
    for root in CANONICAL_ROOTS:
        try:
            rel.relative_to(root)
            return True
        except ValueError:
            continue
    return False


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    for path in sorted(ROOT.rglob("*")):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if not path.is_file():
            continue
        if not in_canonical_root(path) or is_allowed(path):
            continue
        if PHASE_RE.search(path.name):
            findings.append(Finding("ERROR", path, "phase-specific filename in canonical artifact directory"))

    return emit(findings, args.mode, "Phase-name policy check OK")


if __name__ == "__main__":
    raise SystemExit(main())
