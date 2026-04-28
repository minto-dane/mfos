#!/usr/bin/env python3
"""Shared Phase 0.9 executable-spec artifact helpers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterable

import yaml


ROOT = Path(__file__).resolve().parents[2]
CATALOG_DIR = ROOT / "tests/catalog"
FIXTURE_DIR = ROOT / "tests/fixtures"
GOLDEN_DIR = ROOT / "tests/golden"
FUZZ_PLAN = ROOT / "fuzz/targets/fuzz-target-plan.yml"

REQ_RE = re.compile(r"^MFOS-REQ-[A-Z0-9]+-\d{4}$")
SOURCE_RE = re.compile(r"^EXTREF-[A-Z0-9-]+-\d{4}$")
TEST_RE = re.compile(r"^(TEST|NEG)-MFOS-[A-Z0-9]+-[A-Z0-9-]*\d{4}$")
FIXTURE_RE = re.compile(r"^FIXTURE-MFOS-[A-Z0-9]+-[A-Z0-9-]*\d{4}$")
GOLDEN_RE = re.compile(r"^GOLDEN-MFOS-[A-Z0-9]+-[A-Z0-9-]*\d{4}$")
ORACLE_RE = re.compile(r"^ORACLE-MFOS-[A-Z0-9]+-[A-Z0-9-]*\d{4}$")
FUZZ_RE = re.compile(r"^FUZZ-MFOS-[A-Z0-9]+-[A-Z0-9-]*\d{4}$")

FORBIDDEN_OWNED_TOKENS = re.compile(
    r"\b(?:IBM|ZOS|Z-OS|Z_OS|MVS|RACF|JES|JES2|DFSMS|SMF|APF|PRSM|LPAR|"
    r"ZARCHITECTURE|Z-ARCHITECTURE|ZARCH|ZVM|Z-VM|SDSF|ISPF|TSOE|TSO-E|ZOSMF|ZOS-MF)\b",
    re.IGNORECASE,
)
HOST_SEMANTICS = re.compile(
    r"(?:/home/|/Users/|C:\\\\|/tmp/|pid\s*[:=]|process_id\s*[:=]|host_user\s*[:=])",
    re.IGNORECASE,
)
WALL_CLOCK = re.compile(r"\b20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")

PHASE09_CATALOGS = [
    "authorization.yml",
    "audit.yml",
    "dataset-catalog.yml",
    "job-spool.yml",
    "operator-console.yml",
    "first-vertical-slice.yml",
    "negative.yml",
    "failure-modes.yml",
    "conformance-index.yml",
]


def load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        raise ValueError(f"{path}: YAML parse failed: {exc}") from exc


def write_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=False), encoding="utf-8")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def phase09_catalog_paths() -> list[Path]:
    return [CATALOG_DIR / name for name in PHASE09_CATALOGS]


def entries_from_catalog(path: Path) -> list[dict[str, Any]]:
    data = load_yaml(path)
    entries = data.get("entries", [])
    return [entry for entry in entries if isinstance(entry, dict)]


def all_catalog_entries(paths: Iterable[Path] | None = None) -> list[tuple[Path, dict[str, Any]]]:
    out: list[tuple[Path, dict[str, Any]]] = []
    for path in paths or phase09_catalog_paths():
        if path.exists():
            for entry in entries_from_catalog(path):
                out.append((path, entry))
    return out


def yaml_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(
        path
        for path in root.rglob("*.yml")
        if path.is_file()
        and path.name not in {"index.yml", ".mfos-dir.yml"}
        and "archive" not in path.parts
    )


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def has_before_return(records: Any) -> bool:
    return any(isinstance(record, dict) and record.get("before_return") is True for record in as_list(records))


def is_phase_one_or_later(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    return value.startswith("Phase 1") or value.startswith("Phase 2") or value.startswith("Phase 3")


def text_of(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""
