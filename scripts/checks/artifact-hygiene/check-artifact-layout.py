#!/usr/bin/env python3
"""Check high-level artifact directory layout hygiene."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from pathlib import Path

from lib.mfos_lint import Finding, ROOT, emit, mode_arg


PHASE_GLOBS = ("phase-[0-9]*",)

REQUIRED_INDEXED_DIRS = [
    Path("reports"),
    Path("scripts"),
    Path("fuzz/targets"),
    Path("tasks"),
    Path("docs/design/tasks"),
    Path("tests/catalog"),
    Path("tests/fixtures"),
    Path("tests/golden"),
    Path("evidence/traceability"),
]

CANONICAL_ROOT_FILES_ALLOWED = {
    Path("reports"): {"README.md", "index.yml"},
    Path("scripts"): {
        ".mfos-dir.yml",
        "README.md",
        "index.yml",
        "install-dafny.sh",
        "check-formal-claim-coverage.py",
        "check-phase1-gap-triage.py",
        "check-semantic-coverage-mapping.py",
        "validate-all.sh",
        "validate-artifact-hygiene.sh",
        "validate-component-scaffold.sh",
        "validate-dafny-semantics.sh",
        "validate-dafny-semantics-scaffold.sh",
        "validate-language-formal-assurance.sh",
        "validate-naming-safety.sh",
    },
    Path("tasks"): {"README.md", "index.yml"},
}


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    for directory in REQUIRED_INDEXED_DIRS:
        full = ROOT / directory
        if not full.exists():
            findings.append(Finding("ERROR", full, "required artifact directory missing"))
            continue
        for required in ("README.md", "index.yml"):
            path = full / required
            if not path.exists():
                findings.append(Finding("ERROR", path, "required artifact directory metadata missing"))

    for directory, allowed_names in CANONICAL_ROOT_FILES_ALLOWED.items():
        full = ROOT / directory
        if not full.exists():
            continue
        for child in full.iterdir():
            if child.is_file() and child.name not in allowed_names:
                findings.append(Finding("ERROR", child, "unexpected root-level report artifact"))

    for pattern in PHASE_GLOBS:
        for path in sorted((ROOT / "tests/catalog").glob(f"{pattern}.yml")):
            findings.append(Finding("ERROR", path, "phase-specific catalog must be under tests/catalog/archive/<phase>/"))

        for path in sorted((ROOT / "evidence/traceability").glob(f"{pattern}.yml")):
            findings.append(Finding("ERROR", path, "phase-specific traceability must be under archive/ or generated/<phase>/"))

        for path in sorted((ROOT / "fuzz/targets").glob(f"{pattern}.yml")):
            findings.append(Finding("ERROR", path, "phase-specific fuzz plan must be under fuzz/targets/archive/<phase>/"))

        for path in sorted((ROOT / "tasks").glob(pattern)):
            findings.append(Finding("ERROR", path, "phase-specific task plan must be under tasks/archive/<phase>/"))

        for path in sorted((ROOT / "docs/design/tasks").glob(pattern)):
            findings.append(Finding("ERROR", path, "phase-specific design task must be under docs/design/tasks/archive/<phase>/"))

    for path in sorted(ROOT.rglob("__pycache__")):
        if ".git" not in path.parts:
            findings.append(Finding("ERROR", path, "generated Python bytecode cache must not remain in the repository worktree"))

    for pattern in ("*.pyc", "*.pyo"):
        for path in sorted(ROOT.rglob(pattern)):
            if ".git" not in path.parts:
                findings.append(Finding("ERROR", path, "generated Python bytecode artifact must not remain in the repository worktree"))

    return emit(findings, args.mode, "Artifact layout check OK")


if __name__ == "__main__":
    raise SystemExit(main())
