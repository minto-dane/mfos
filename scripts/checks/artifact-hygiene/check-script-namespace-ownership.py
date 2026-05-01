#!/usr/bin/env python3
"""Validate root script entrypoint and wrapper ownership metadata."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg


SCRIPT_INDEX = ROOT / "scripts/index.yml"
SCRIPTS_ROOT = ROOT / "scripts"
ROOT_METADATA = {".mfos-dir.yml", "README.md", "index.yml"}
PHASE_NAME_RE = re.compile(r"phase[-_]?\d+", re.IGNORECASE)


def walk_entries(value: Any) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    if isinstance(value, dict):
        if isinstance(value.get("path"), str):
            entries.append(value)
        for child in value.values():
            entries.extend(walk_entries(child))
    elif isinstance(value, list):
        for child in value:
            entries.extend(walk_entries(child))
    return entries


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []
    data = load_yaml(SCRIPT_INDEX) if SCRIPT_INDEX.exists() else {}
    entries = walk_entries(data)
    root_allowed = {
        Path(entry["path"]).name
        for entry in entries
        if entry.get("root_allowed") is True and Path(str(entry.get("path"))).parent == Path("scripts")
    } | ROOT_METADATA
    wrappers = {
        str(entry.get("wrapper")): str(entry.get("wrapper_target") or entry.get("target") or entry.get("path"))
        for entry in entries
        if entry.get("role") == "root_wrapper" and isinstance(entry.get("wrapper"), str)
    }

    for path in sorted(SCRIPTS_ROOT.iterdir() if SCRIPTS_ROOT.exists() else []):
        if not path.is_file():
            continue
        if path.name not in root_allowed:
            findings.append(Finding("ERROR", path, "root script file is not declared root_allowed in scripts/index.yml"))
        if path.name.startswith("check-") and path.suffix == ".py":
            rel = str(path.relative_to(ROOT))
            target = wrappers.get(rel)
            if target is None:
                findings.append(Finding("ERROR", path, "root check script must be declared as root_wrapper in scripts/index.yml"))
                continue
            text = path.read_text(encoding="utf-8")
            if "runpy.run_path" not in text:
                findings.append(Finding("ERROR", path, "root Python check wrapper must dispatch through runpy.run_path"))
            if "def " in text or "class " in text:
                findings.append(Finding("ERROR", path, "root Python check wrapper must not contain substantive definitions"))
            if target.replace("scripts/", "") not in text:
                findings.append(Finding("ERROR", path, f"root wrapper must contain exact target path: {target}"))
            if PHASE_NAME_RE.search(path.name) and not target.startswith("scripts/phases/"):
                findings.append(Finding("ERROR", path, "phase-specific root wrapper must target scripts/phases/"))

    return emit(findings, args.mode, "Script namespace ownership check OK")


if __name__ == "__main__":
    raise SystemExit(main())
