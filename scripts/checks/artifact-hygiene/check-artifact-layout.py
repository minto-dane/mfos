#!/usr/bin/env python3
"""Check high-level artifact directory layout hygiene."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

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
        "check-architecture-portability-policy.py",
        "check-cpu-feature-registry.py",
        "check-phase1-2-auth-audit-coverage.py",
        "check-phase1-3-dataset-catalog-coverage.py",
        "check-phase1-gap-triage.py",
        "check-roadmap-phase-alignment.py",
        "check-semantic-coverage-mapping.py",
        "check-x64-profile-policy.py",
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

ROOT_CHECK_WRAPPERS = {
    "check-architecture-portability-policy.py": "checks/check-architecture-portability-policy.py",
    "check-cpu-feature-registry.py": "checks/check-cpu-feature-registry.py",
    "check-formal-claim-coverage.py": "checks/formal-claims/check-formal-claim-coverage.py",
    "check-phase1-2-auth-audit-coverage.py": "phases/phase-1/check-phase1-2-auth-audit-coverage.py",
    "check-phase1-3-dataset-catalog-coverage.py": "phases/phase-1/check-phase1-3-dataset-catalog-coverage.py",
    "check-phase1-gap-triage.py": "phases/phase-1/check-phase1-gap-triage.py",
    "check-roadmap-phase-alignment.py": "checks/check-roadmap-phase-alignment.py",
    "check-semantic-coverage-mapping.py": "checks/semantic-coverage/check-semantic-coverage-mapping.py",
    "check-x64-profile-policy.py": "checks/check-x64-profile-policy.py",
}


def validate_root_check_wrappers(findings: list[Finding]) -> None:
    scripts_root = ROOT / "scripts"
    for path in sorted(scripts_root.glob("check-*.py")):
        expected_target = ROOT_CHECK_WRAPPERS.get(path.name)
        if expected_target is None:
            findings.append(Finding("ERROR", path, "root check script is not an indexed thin wrapper"))
            continue
        text = path.read_text(encoding="utf-8")
        if "def " in text or "class " in text:
            findings.append(Finding("ERROR", path, "root check wrapper must not contain substantive definitions"))
        if "runpy.run_path" not in text:
            findings.append(Finding("ERROR", path, "root check wrapper must dispatch through fixed runpy target"))
        if expected_target not in text:
            findings.append(Finding("ERROR", path, f"root check wrapper must target scripts/{expected_target}"))

    for name in sorted(ROOT_CHECK_WRAPPERS):
        path = scripts_root / name
        if not path.exists():
            findings.append(Finding("ERROR", path, "indexed root check wrapper missing"))


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

    validate_root_check_wrappers(findings)

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
