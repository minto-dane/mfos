#!/usr/bin/env python3
"""Check that Source Cards remain public-safe reference cards."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

import re
from pathlib import Path

from lib.mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg, text_files


CARD_DIR = ROOT / "docs/design/source-matrix/cards"
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
REQUIRED_CONTROLS = {
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
GUIDANCE_ROOTS = [
    Path("README.md"),
    Path("docs/design/mfos-design.md"),
    Path("docs/design/source-matrix"),
    Path("sources"),
]
FIELD_LINE_RE = re.compile(r"^\s*(?P<field>[A-Za-z_][A-Za-z0-9_]*):")
STALE_SUMMARY_RE = re.compile(r"\bSource Cards?\b.*\b(?:store|include|contain)\b.*\bsummar", re.IGNORECASE)


def is_allowed_removed_field_context(lines: list[str], index: int) -> bool:
    window = "\n".join(lines[max(0, index - 5) : min(len(lines), index + 3)]).lower()
    return any(marker in window for marker in ("removed public fields", "prohibited in source cards", "prohibited source card field"))


def check_public_guidance(findings: list[Finding]) -> None:
    for path in text_files(GUIDANCE_ROOTS):
        if CARD_DIR in path.parents:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        for index, line in enumerate(lines):
            lineno = index + 1
            field_match = FIELD_LINE_RE.match(line)
            if field_match and field_match.group("field") in REMOVED_FIELDS and not is_allowed_removed_field_context(lines, index):
                findings.append(Finding("ERROR", path, f"stale Source Card example uses prohibited field: {field_match.group('field')}", lineno))
            if "source_type: normative" in line:
                findings.append(Finding("ERROR", path, "stale Source Card example uses source_type: normative", lineno))
            if STALE_SUMMARY_RE.search(line):
                findings.append(Finding("ERROR", path, "stale Source Card guidance describes storing summaries", lineno))


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    check_public_guidance(findings)

    for path in sorted(CARD_DIR.glob("*.yml")):
        data = load_yaml(path)
        if not isinstance(data, dict):
            findings.append(Finding("ERROR", path, "source card must be a mapping"))
            continue
        sid = str(data.get("source_id", path.stem))
        for field in sorted(REMOVED_FIELDS & set(data)):
            findings.append(Finding("ERROR", path, f"{sid}: prohibited Source Card field present: {field}"))
        controls = data.get("legal_controls")
        if not isinstance(controls, dict):
            findings.append(Finding("ERROR", path, f"{sid}: missing legal_controls mapping"))
            continue
        for key, expected in REQUIRED_CONTROLS.items():
            if controls.get(key) is not expected:
                findings.append(Finding("ERROR", path, f"{sid}: legal_controls.{key} must be {expected}"))
        title = str(data.get("document_title", ""))
        if len(title.split()) > 40:
            findings.append(Finding("WARN", path, f"{sid}: document_title is unusually long for a reference card"))
        for field in ("mfos_divergence", "prohibited_inference"):
            values = data.get(field)
            if not isinstance(values, list) or not values:
                findings.append(Finding("ERROR", path, f"{sid}: {field} must be a non-empty list"))

    return emit(findings, args.mode, "Source Card public-safety check OK")


if __name__ == "__main__":
    raise SystemExit(main())
