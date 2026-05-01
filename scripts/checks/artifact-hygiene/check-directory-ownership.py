#!/usr/bin/env python3
"""Check duplicate directory ownership decisions for high-risk MFOS roots."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg


EXPECTED = {
    "implementation": (True, "implementation_future"),
    "implementation/services": (False, "implementation_future"),
    "implementation/runtime": (False, "implementation_future"),
    "implementation/nucleus": (False, "implementation_future"),
    "implementation/pxm": (False, "implementation_future"),
    "implementation/guard": (False, "implementation_future"),
    "implementation/tools": (False, "implementation_future"),
    "services": (False, "implementation_future"),
    "nucleus": (False, "implementation_future"),
    "pxm": (False, "implementation_future"),
    "guard": (False, "implementation_future"),
    "tools": (True, "validation"),
    "docs/design/specs": (True, "canonical_current"),
    "specs": (False, "bridge"),
    "docs/design/source-matrix": (True, "canonical_registry"),
    "source-matrix": (False, "bridge"),
    "sources": (False, "bridge"),
    "docs/design/packs": (True, "canonical_registry"),
    "packs": (False, "bridge"),
    "prompts": (False, "bridge"),
    "formal/executable-semantics/dafny": (True, "canonical_current"),
}

METADATA_ONLY_ROOTS = {Path("services"), Path("nucleus"), Path("pxm"), Path("guard")}
METADATA_ALLOWED = {"README.md", ".mfos-dir.yml", "index.yml"}
TASK_REGISTRY = ROOT / "docs/design/registries/tasks.yaml"


def metadata(path: Path) -> dict[str, Any]:
    data = load_yaml(path)
    return data if isinstance(data, dict) else {}


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    for rel, (canonical, role) in EXPECTED.items():
        directory = ROOT / rel
        meta = directory / ".mfos-dir.yml"
        if not directory.exists():
            findings.append(Finding("ERROR", directory, "expected ownership directory missing"))
            continue
        if not meta.exists():
            findings.append(Finding("ERROR", meta, "ownership metadata missing"))
            continue
        data = metadata(meta)
        if data.get("canonical") is not canonical:
            findings.append(Finding("ERROR", meta, f"canonical must be {canonical!r}"))
        if data.get("role") != role:
            findings.append(Finding("ERROR", meta, f"role must be {role!r}"))

    for rel in METADATA_ONLY_ROOTS:
        directory = ROOT / rel
        for child in sorted(directory.iterdir() if directory.exists() else []):
            if child.is_file() and child.name not in METADATA_ALLOWED:
                findings.append(Finding("ERROR", child, "top-level bridge scaffold must remain metadata-only"))
            if child.is_dir():
                findings.append(Finding("ERROR", child, "top-level bridge scaffold must not contain implementation subdirectories"))

    if TASK_REGISTRY.exists():
        registry = metadata(TASK_REGISTRY)
        for task in registry.get("entries", []) if isinstance(registry.get("entries"), list) else []:
            if not isinstance(task, dict):
                continue
            task_id = str(task.get("task_id"))
            task_type = task.get("task_type")
            status = task.get("status")
            allowed_paths = [str(path) for path in task.get("allowed_paths", []) if isinstance(path, str)]
            if status == "ready" and task_type in {"hosted_prototype", "service"}:
                findings.append(Finding("ERROR", TASK_REGISTRY, f"{task_id}: hosted/service implementation task must not be ready in Phase 1"))
            if status == "ready" and any(path.startswith("services/") for path in allowed_paths):
                findings.append(Finding("ERROR", TASK_REGISTRY, f"{task_id}: ready task must not target noncanonical services/ bridge"))

    return emit(findings, args.mode, "Directory ownership check OK")


if __name__ == "__main__":
    raise SystemExit(main())
