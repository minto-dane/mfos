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
    "implementation/services": (True, "implementation_future"),
    "implementation/runtime": (False, "implementation_future"),
    "implementation/nucleus": (True, "implementation_future"),
    "implementation/pxm": (True, "implementation_future"),
    "implementation/guard": (True, "implementation_future"),
    "implementation/tools": (False, "implementation_future"),
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

RETIRED_TOP_LEVEL_IMPLEMENTATION_ROOTS = {Path("services"), Path("nucleus"), Path("pxm"), Path("guard")}
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

    for rel in RETIRED_TOP_LEVEL_IMPLEMENTATION_ROOTS:
        directory = ROOT / rel
        if directory.exists():
            findings.append(Finding("ERROR", directory, "retired top-level implementation bridge must not exist"))

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
                findings.append(Finding("ERROR", TASK_REGISTRY, f"{task_id}: ready task must not target retired services/ bridge"))

    return emit(findings, args.mode, "Directory ownership check OK")


if __name__ == "__main__":
    raise SystemExit(main())
