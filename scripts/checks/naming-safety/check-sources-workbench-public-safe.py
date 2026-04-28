#!/usr/bin/env python3
"""Validate populated sources/ workbench records are public-safe.

This checker intentionally treats sources/ as noncanonical workbench material.
It validates public-safety and migration metadata without requiring the
canonical docs/design/source-matrix card shape.
"""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

import re
from typing import Any

import yaml

from lib.mfos_lint import Finding, ROOT, emit, mode_arg


SOURCES = ROOT / "sources"
REMOVED_FIELDS = {
    "canonical_concepts",
    "normative_source",
    "detailed_summary",
    "source_summary",
    "copied_excerpt",
    "record_layouts",
    "command_syntax",
    "macro_signatures",
}
REQUIRED_LEGAL_CONTROLS = {
    "public_safe": True,
    "no_copied_text": True,
    "no_long_quotes": True,
    "no_tables_copied": True,
    "no_diagrams_copied": True,
    "no_record_layouts_copied": True,
    "no_command_syntax_copied": True,
    "no_macro_signatures_copied": True,
    "no_message_tables_copied": True,
    "attribution_required": True,
    "external_affiliation_claimed": False,
    "compatibility_claimed": False,
    "substitute_for_source": False,
}
SOURCE_CARD_REQUIRED = {
    "source_id",
    "source_kind",
    "source_type",
    "semantic_role",
    "vendor",
    "document_title",
    "document_url",
    "retrieved_at",
    "reference_purpose",
    "review_topics",
    "mfos_mapping",
    "mfos_divergence",
    "prohibited_inference",
    "legal_controls",
    "review_status",
}
SOURCE_ID_RE = re.compile(r"\b(?:(?:EXTREF|X64|MS|TCG|NIST|SEL4|SLSA|TUF|INT|FBVBS)-[A-Z0-9-]+-\d{3,4}|(?:TCG|SEL4|SLSA|TUF|FBVBS)-\d{3,4})\b")
OLD_IBM_ID_RE = re.compile(r"\bIBM-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}\b")
LONG_BLOCKQUOTE_RE = re.compile(r"^>\s+\S+(?:\s+\S+){25,}")
SUBSTITUTE_RE = re.compile(r"\bthis card is a substitute\b", re.IGNORECASE)
SAFE_POLICY_LINE_RE = re.compile(r"\b(no_|do not|must not|prohibited|forbidden|legal_controls|not copied|not reproduce)\b", re.IGNORECASE)


def parse_markdown_front_matter(path: Path) -> dict[str, Any] | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return None
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return None
    data = yaml.safe_load(parts[1])
    return data if isinstance(data, dict) else None


def load_record(path: Path, findings: list[Finding]) -> dict[str, Any] | None:
    try:
        if path.suffix in {".yml", ".yaml"}:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else None
        if path.suffix == ".md":
            data = parse_markdown_front_matter(path)
            if data is None:
                findings.append(Finding("ERROR", path, "source-card markdown must have YAML front matter"))
            return data
    except Exception as exc:
        findings.append(Finding("ERROR", path, f"cannot parse source-card metadata: {exc}"))
    return None


def check_legal_controls(path: Path, record: dict[str, Any], findings: list[Finding]) -> None:
    controls = record.get("legal_controls")
    if not isinstance(controls, dict):
        findings.append(Finding("ERROR", path, "missing legal_controls mapping"))
        return
    for key, expected in REQUIRED_LEGAL_CONTROLS.items():
        if controls.get(key) is not expected:
            findings.append(Finding("ERROR", path, f"legal_controls.{key} must be {expected}"))


def check_single_card(path: Path, record: dict[str, Any], findings: list[Finding]) -> None:
    for field in sorted(REMOVED_FIELDS & set(record)):
        findings.append(Finding("ERROR", path, f"prohibited source-card field present: {field}"))
    missing = sorted(SOURCE_CARD_REQUIRED - set(record))
    if missing:
        findings.append(Finding("ERROR", path, f"missing source-card fields: {', '.join(missing)}"))
    sid = record.get("source_id")
    if not isinstance(sid, str) or not SOURCE_ID_RE.fullmatch(sid):
        findings.append(Finding("ERROR", path, f"invalid source_id for sources workbench card: {sid!r}"))
    if record.get("authority_status") not in {"preparatory_until_adr_migration", "canonical_in_docs_design_source_matrix"}:
        findings.append(Finding("ERROR", path, "authority_status must keep sources/ noncanonical before ADR migration"))
    if not isinstance(record.get("mfos_divergence"), list) or not record.get("mfos_divergence"):
        findings.append(Finding("ERROR", path, "mfos_divergence must be a non-empty list"))
    if not isinstance(record.get("prohibited_inference"), list) or not record.get("prohibited_inference"):
        findings.append(Finding("ERROR", path, "prohibited_inference must be a non-empty list"))
    check_legal_controls(path, record, findings)


def check_bundle(path: Path, record: dict[str, Any], findings: list[Finding]) -> None:
    check_legal_controls(path, record, findings)
    cards = record.get("source_cards")
    if not isinstance(cards, list) or not cards:
        findings.append(Finding("ERROR", path, "source card bundle must contain source_cards list"))
        return
    for index, card in enumerate(cards, 1):
        if not isinstance(card, dict):
            findings.append(Finding("ERROR", path, f"source_cards[{index}] must be a mapping"))
            continue
        for field in sorted(REMOVED_FIELDS & set(card)):
            findings.append(Finding("ERROR", path, f"source_cards[{index}] has prohibited field: {field}"))
        for key in ("source_id", "vendor", "document_title", "review_topics", "mfos_mapping", "prohibited_inference", "status"):
            if key not in card:
                findings.append(Finding("ERROR", path, f"source_cards[{index}] missing {key}"))
        if "mfos_divergence" not in card and "divergence" not in card:
            findings.append(Finding("ERROR", path, f"source_cards[{index}] missing mfos_divergence/divergence"))


def check_text_safety(path: Path, findings: list[Finding]) -> None:
    if path.name in {"source-card.schema.yml", "concept-card.schema.yml"}:
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    safe_until = 0
    for lineno, line in enumerate(text.splitlines(), 1):
        if SAFE_POLICY_LINE_RE.search(line):
            safe_until = lineno + 2
        if LONG_BLOCKQUOTE_RE.search(line):
            findings.append(Finding("ERROR", path, "long block quote may copy external documentation", lineno))
        if SUBSTITUTE_RE.search(line):
            findings.append(Finding("ERROR", path, "source card says it is a source substitute; use negative imperative wording", lineno))
        if OLD_IBM_ID_RE.search(line) and "legacy_source_ids" not in line:
            findings.append(Finding("ERROR", path, "legacy IBM-style source ID outside legacy_source_ids alias", lineno))
        for field in REMOVED_FIELDS:
            if re.search(rf"^\s*{re.escape(field)}\s*:", line) and lineno > safe_until:
                findings.append(Finding("ERROR", path, f"prohibited field-like line: {field}", lineno))


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    if not SOURCES.exists():
        return emit(findings, args.mode, "Sources workbench public-safety check OK")

    for path in sorted(SOURCES.rglob("*")):
        if not path.is_file() or "_cache" in path.parts:
            continue
        if path.suffix not in {".md", ".yml", ".yaml", ".txt"}:
            findings.append(Finding("ERROR", path, "sources workbench may not commit external/binary cache artifact"))
            continue
        check_text_safety(path, findings)

    for path in sorted(SOURCES.glob("**/source-cards/*")):
        if not path.is_file():
            continue
        record = load_record(path, findings)
        if record is None:
            continue
        if isinstance(record.get("source_cards"), list):
            check_bundle(path, record, findings)
        else:
            check_single_card(path, record, findings)

    return emit(findings, args.mode, "Sources workbench public-safety check OK")


if __name__ == "__main__":
    raise SystemExit(main())
