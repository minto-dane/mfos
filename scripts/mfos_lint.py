#!/usr/bin/env python3
"""Shared helpers for MFOS validation scripts."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE_INDEX = ROOT / "docs/design/source-matrix/source-matrix.yml"
REQUIREMENTS = ROOT / "docs/design/registries/requirements.yaml"
TESTS = ROOT / "docs/design/registries/tests.yaml"
EVIDENCE = ROOT / "docs/design/registries/evidence.yaml"
SPECS_DIR = ROOT / "docs/design/specs"

SOURCE_ID_RE = re.compile(
    r"\b(?:EXTREF-[A-Z0-9-]+-\d{4}|(?:X64|MS|TCG|NIST|SEL4|SLSA|TUF|FBVBS)(?:-[A-Z0-9]+)*-\d{3})\b"
)
REQ_ID_RE = re.compile(r"\bMFOS-REQ-[A-Z0-9]+-(?:\d{4}|\*)\b")
TEST_ID_RE = re.compile(r"\b(?:TEST|NEG)-MFOS-[A-Z0-9]+-[A-Z0-9-]*\d{4}\b")
EVID_ID_RE = re.compile(r"\bEV-MFOS-[A-Z0-9]+-[A-Z0-9-]*\d{4}\b")


@dataclass(frozen=True)
class Finding:
    severity: str
    path: Path
    message: str
    line: int | None = None

    def format(self) -> str:
        rel = self.path.relative_to(ROOT) if self.path.is_absolute() and self.path.is_relative_to(ROOT) else self.path
        suffix = f":{self.line}" if self.line else ""
        return f"{self.severity}: {rel}{suffix}: {self.message}"


def mode_arg() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("draft", "review", "release"),
        default="draft",
        help="draft fails errors only; release also fails warnings",
    )
    return parser


def load_yaml(path: Path) -> object:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"YAML parse failed: {path}: {exc}") from exc


def source_ids() -> set[str]:
    index = load_yaml(SOURCE_INDEX)
    if not isinstance(index, dict):
        return set()
    return {
        item["source_id"]
        for item in index.get("cards", [])
        if isinstance(item, dict) and isinstance(item.get("source_id"), str)
    }


def source_types() -> dict[str, str]:
    index = load_yaml(SOURCE_INDEX)
    if not isinstance(index, dict):
        return {}
    return {
        item["source_id"]: item.get("source_type", "")
        for item in index.get("cards", [])
        if isinstance(item, dict) and isinstance(item.get("source_id"), str)
    }


def requirement_ids() -> set[str]:
    catalog = load_yaml(REQUIREMENTS)
    if not isinstance(catalog, dict):
        return set()
    return {
        entry["requirement_id"]
        for entry in catalog.get("entries", [])
        if isinstance(entry, dict) and isinstance(entry.get("requirement_id"), str)
    }


def registry_entries(path: Path) -> list[dict[str, object]]:
    data = load_yaml(path)
    if not isinstance(data, dict):
        return []
    return [entry for entry in data.get("entries", []) if isinstance(entry, dict)]


def markdown_files(roots: Iterable[Path]) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        root = ROOT / root
        if root.is_file() and root.suffix == ".md":
            files.append(root)
        elif root.is_dir():
            files.extend(path for path in root.rglob("*.md") if path.is_file())
    return sorted(files)


def text_files(roots: Iterable[Path]) -> list[Path]:
    suffixes = {".md", ".yml", ".yaml", ".txt"}
    files: list[Path] = []
    for root in roots:
        root = ROOT / root
        if root.is_file() and root.suffix in suffixes:
            files.append(root)
        elif root.is_dir():
            files.extend(path for path in root.rglob("*") if path.is_file() and path.suffix in suffixes)
    return sorted(files)


def emit(findings: list[Finding], mode: str, ok_message: str) -> int:
    errors = [f for f in findings if f.severity in {"BLOCK", "ERROR"}]
    warnings = [f for f in findings if f.severity == "WARN"]
    for finding in findings:
        print(finding.format(), file=sys.stderr if finding.severity in {"BLOCK", "ERROR"} else sys.stdout)
    if errors or (mode == "release" and warnings):
        print(f"Validation failed: {len(errors)} errors, {len(warnings)} warnings", file=sys.stderr)
        return 1
    print(f"{ok_message}: {len(warnings)} warnings")
    return 0


def has_front_matter(text: str) -> bool:
    return text.startswith("---\n")


def parse_front_matter(path: Path) -> tuple[dict[str, object] | None, str | None]:
    text = path.read_text(encoding="utf-8")
    if not has_front_matter(text):
        return None, None
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return None, "front matter opener has no closing delimiter"
    try:
        data = yaml.safe_load(parts[1])
    except Exception as exc:
        return None, str(exc)
    if not isinstance(data, dict):
        return None, "front matter is not a mapping"
    return data, None
