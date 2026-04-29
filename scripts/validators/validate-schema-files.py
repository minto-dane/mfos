#!/usr/bin/env python3
"""Validate that design schema artifacts are parseable and policy-bound."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg


SCHEMA_ROOTS = [
    ROOT / "schemas",
    ROOT / "schemas/mfos",
]


def _implementation_guarded(data: dict[str, object]) -> bool:
    if data.get("implementation_allowed") is False:
        return True
    props = data.get("properties")
    if isinstance(props, dict):
        implementation_allowed = props.get("implementation_allowed")
        if isinstance(implementation_allowed, dict) and implementation_allowed.get("const") is False:
            return True
    x_mfos = data.get("x-mfos")
    if isinstance(x_mfos, dict) and x_mfos.get("implementation_allowed") is False:
        return True
    return False


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []
    seen: set[Path] = set()

    for root in SCHEMA_ROOTS:
        if not root.exists():
            continue
        for path in sorted(root.glob("*.schema.yml")):
            if path in seen:
                continue
            seen.add(path)
            data = load_yaml(path)
            if not isinstance(data, dict):
                findings.append(Finding("ERROR", path, "schema artifact must be a mapping"))
                continue
            if "type" not in data:
                findings.append(Finding("WARN", path, "schema artifact missing type"))
            if data.get("type") == "object":
                if not isinstance(data.get("required"), list) or not data.get("required"):
                    findings.append(Finding("WARN", path, "object schema missing non-empty required list"))
                if not isinstance(data.get("properties"), dict) or not data.get("properties"):
                    findings.append(Finding("WARN", path, "object schema missing non-empty properties"))
            if "schema_id" not in data and "$id" not in data:
                findings.append(Finding("WARN", path, "schema artifact should declare schema_id or $id"))
            if not _implementation_guarded(data):
                findings.append(Finding("WARN", path, "schema artifact should explicitly forbid implementation"))

    if not seen:
        findings.append(Finding("ERROR", ROOT / "schemas", "no schema artifacts found"))

    return emit(findings, args.mode, f"Schema artifact validation OK: {len(seen)} schemas checked")


if __name__ == "__main__":
    raise SystemExit(main())
