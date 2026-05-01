#!/usr/bin/env python3
"""Detect undeclared duplicate ownership across high-risk directories."""

from __future__ import annotations

from collections import defaultdict
import sys
from pathlib import Path
from typing import Any

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg


SCRIPT_INDEX = ROOT / "scripts/index.yml"
HIGH_RISK_ROOTS = [ROOT / "scripts", ROOT / "implementation", ROOT / "formal", ROOT / "tools"]


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


def indexed_paths() -> tuple[set[tuple[str, str]], set[str]]:
    data = load_yaml(SCRIPT_INDEX) if SCRIPT_INDEX.exists() else {}
    pairs: set[tuple[str, str]] = set()
    paths: set[str] = set()
    for entry in walk_entries(data):
        if isinstance(entry.get("path"), str):
            paths.add(str(entry["path"]))
        wrapper = entry.get("wrapper")
        target = entry.get("wrapper_target") or entry.get("target") or entry.get("path")
        if isinstance(wrapper, str) and isinstance(target, str):
            pairs.add((wrapper, target))
            paths.add(wrapper)
            paths.add(target)
    return pairs, paths


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []
    pairs, indexed = indexed_paths()

    for retired in ("services", "nucleus", "pxm", "guard"):
        if (ROOT / retired).exists():
            findings.append(Finding("ERROR", ROOT / retired, "retired top-level implementation bridge reappeared"))

    by_name: dict[str, list[Path]] = defaultdict(list)
    for root in HIGH_RISK_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix in {".py", ".sh"}:
                by_name[path.name].append(path)

    for name, paths in sorted(by_name.items()):
        if len(paths) < 2:
            continue
        rels = [str(path.relative_to(ROOT)) for path in paths]
        root_scripts = [rel for rel in rels if Path(rel).parent == Path("scripts")]
        for root_script in root_scripts:
            allowed = any(wrapper == root_script and target in rels for wrapper, target in pairs)
            if not allowed:
                findings.append(Finding("ERROR", ROOT / root_script, f"duplicate script basename without declared wrapper target: {name}"))
        if not root_scripts and not all(rel in indexed for rel in rels):
            findings.append(Finding("WARN", paths[0], f"duplicate basename across high-risk directories should be indexed explicitly: {', '.join(rels)}"))

    return emit(findings, args.mode, "Cross-directory duplicate ownership check OK")


if __name__ == "__main__":
    raise SystemExit(main())
