#!/usr/bin/env python3
"""Validate the current naming-safe Source Card ledger."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

import sys
from pathlib import Path

import yaml


ROOT = Path("docs/design/source-matrix")
INDEX_PATH = ROOT / "source-matrix.yml"
CARD_DIR = ROOT / "cards"

REQUIRED_FIELDS = {
    "source_id",
    "source_kind",
    "source_type",
    "semantic_role",
    "vendor",
    "document_title",
    "document_url",
    "retrieved_at",
    "review_topics",
    "mfos_mapping",
    "mfos_divergence",
    "prohibited_inference",
    "legal_controls",
    "source_refs",
    "requirement_refs",
    "review_status",
}

SOURCE_TYPES = {"external_reference", "internal_transfer"}
REMOVED_PUBLIC_FIELDS = {
    "canonical_concepts",
    "normative_source",
    "detailed_summary",
    "source_summary",
    "copied_excerpt",
    "record_layouts",
    "command_syntax",
    "macro_signatures",
}


def load_yaml(path: Path) -> object:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - CLI error path
        raise SystemExit(f"YAML parse failed: {path}: {exc}") from exc


def non_empty(value: object) -> bool:
    return value is not None and value != "" and value != []


def main() -> int:
    if not INDEX_PATH.exists():
        print(f"missing source card index: {INDEX_PATH}", file=sys.stderr)
        return 1

    index = load_yaml(INDEX_PATH)
    if not isinstance(index, dict):
        print(f"source card index is not a mapping: {INDEX_PATH}", file=sys.stderr)
        return 1

    cards = index.get("cards")
    if not isinstance(cards, list) or not cards:
        print("source card index has no cards", file=sys.stderr)
        return 1

    errors: list[str] = []
    seen: set[str] = set()

    for item in cards:
        if not isinstance(item, dict):
            errors.append("index contains non-mapping card entry")
            continue
        source_id = item.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            errors.append("index card entry lacks source_id")
            continue
        if source_id in seen:
            errors.append(f"duplicate source_id in index: {source_id}")
        seen.add(source_id)

        card_path = Path(item.get("card_path", "")) if item.get("card_path") else CARD_DIR / f"{source_id}.yml"
        if not card_path.exists():
            errors.append(f"missing card file for {source_id}: {card_path}")
            continue

        card = load_yaml(card_path)
        if not isinstance(card, dict):
            errors.append(f"card is not a mapping: {card_path}")
            continue

        missing = sorted(field for field in REQUIRED_FIELDS if field not in card)
        if missing:
            errors.append(f"{source_id}: missing fields: {', '.join(missing)}")

        for field in REQUIRED_FIELDS:
            if field in card and not non_empty(card[field]):
                errors.append(f"{source_id}: field is empty: {field}")
        removed = sorted(field for field in REMOVED_PUBLIC_FIELDS if field in card)
        if removed:
            errors.append(f"{source_id}: removed public-safe fields still present: {', '.join(removed)}")

        if card.get("source_id") != source_id:
            errors.append(f"{source_id}: source_id mismatch in {card_path}")

        if card.get("source_type") not in SOURCE_TYPES:
            errors.append(f"{source_id}: invalid source_type: {card.get('source_type')}")

        for list_field in ("review_topics", "mfos_divergence", "prohibited_inference"):
            if list_field in card and not isinstance(card[list_field], list):
                errors.append(f"{source_id}: {list_field} must be a list")

        mapping = card.get("mfos_mapping")
        if mapping is not None and not isinstance(mapping, dict):
            errors.append(f"{source_id}: mfos_mapping must be a mapping")
        controls = card.get("legal_controls")
        if not isinstance(controls, dict):
            errors.append(f"{source_id}: legal_controls must be a mapping")
        else:
            for flag in (
                "public_safe",
                "no_copied_text",
                "no_long_quotes",
                "no_tables_copied",
                "no_diagrams_copied",
                "no_record_layouts_copied",
                "no_command_syntax_copied",
                "no_macro_signatures_copied",
                "no_message_tables_copied",
                "attribution_required",
                "external_affiliation_claimed",
                "compatibility_claimed",
                "substitute_for_source",
            ):
                if flag not in controls:
                    errors.append(f"{source_id}: legal_controls.{flag} missing")
            for false_flag in ("external_affiliation_claimed", "compatibility_claimed", "substitute_for_source"):
                if controls.get(false_flag) is not False:
                    errors.append(f"{source_id}: legal_controls.{false_flag} must be false")
        if source_id.startswith("EXTREF-IBM-"):
            legacy = card.get("legacy_source_ids")
            if not isinstance(legacy, list) or not any(str(item).startswith("IBM-") for item in legacy):
                errors.append(f"{source_id}: EXTREF IBM card must retain legacy IBM-* source ID alias")
        if isinstance(card.get("source_refs"), list):
            for ref in card["source_refs"]:
                if isinstance(ref, dict) and ref.get("source_id") == source_id and ref.get("source_type") != card.get("source_type"):
                    errors.append(f"{source_id}: self source_ref source_type does not match card source_type")

    indexed_paths = {
        str(Path(item.get("card_path", "")))
        for item in cards
        if isinstance(item, dict) and item.get("card_path")
    }
    extra_cards = {
        str(path)
        for path in CARD_DIR.glob("*.yml")
        if str(path) not in indexed_paths
    }
    if extra_cards:
        errors.append(f"card files not indexed: {', '.join(sorted(extra_cards))}")

    if errors:
        print("Source Card validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Source Card validation OK: {len(seen)} cards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
