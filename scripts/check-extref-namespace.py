#!/usr/bin/env python3
"""Check external-reference namespace safety.

IBM-derived canonical source IDs must use EXTREF-IBM-*.
Legacy IBM-* IDs are allowed only as aliases in source cards/index records and
in naming alias or migration reports.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg, source_ids, text_files


OLD_IBM_ID_RE = re.compile(r"\bIBM-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}\b")
ALLOWED_OLD_ID_FILES = (
    "reports/naming-",
    "reports/naming-safety/",
    "docs/design/source-matrix/cards/",
    "docs/design/source-matrix/source-matrix.yml",
    "docs/design/source-matrix/source-matrix.yaml",
)

def allowed_old_id_context(path: Path, line: str) -> bool:
    rel = str(path.relative_to(ROOT))
    if rel.startswith(("reports/naming-", "reports/naming-safety/")):
        return True
    if any(rel.startswith(prefix) for prefix in ALLOWED_OLD_ID_FILES):
        return "legacy_source_ids" in line
    return False


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []
    known = source_ids()

    index_path = ROOT / "docs/design/source-matrix/source-matrix.yml"
    index = load_yaml(index_path)
    if not isinstance(index, dict):
        findings.append(Finding("ERROR", index_path, "source index must be a mapping"))
    else:
        for item in index.get("cards", []):
            if not isinstance(item, dict):
                continue
            source_id = str(item.get("source_id", ""))
            vendor = str(item.get("vendor", ""))
            if vendor == "IBM" and not source_id.startswith("EXTREF-IBM-"):
                findings.append(Finding("ERROR", index_path, f"IBM card has non-EXTREF canonical source_id: {source_id}"))
            if source_id.startswith("IBM-"):
                findings.append(Finding("ERROR", index_path, f"legacy IBM ID used as canonical source_id: {source_id}"))
            card_path = ROOT / str(item.get("card_path", ""))
            if card_path.exists():
                card = load_yaml(card_path)
                if isinstance(card, dict):
                    if card.get("source_id") != source_id:
                        findings.append(Finding("ERROR", card_path, f"source_id mismatch with index: {card.get('source_id')} != {source_id}"))
                    if vendor == "IBM" and not isinstance(card.get("legacy_source_ids"), list):
                        findings.append(Finding("ERROR", card_path, "IBM EXTREF card must retain legacy_source_ids alias list"))

    roots = [
        Path("README.md"),
        Path("README.ja.md"),
        Path("docs/design/specs"),
        Path("docs/design/registries"),
        Path("docs/design/assurance"),
        Path("docs/design/packs"),
        Path("packs"),
        Path("tasks"),
        Path("evidence/traceability"),
        Path("schemas"),
        Path("scripts"),
        Path("requirements"),
        Path("claims"),
        Path("ai"),
        Path("implementation"),
        Path("governance"),
        Path("adr"),
        Path("sources"),
        Path("reports"),
    ]
    for path in text_files(roots):
        text = path.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), 1):
            for match in OLD_IBM_ID_RE.findall(line):
                if not allowed_old_id_context(path, line):
                    findings.append(Finding("ERROR", path, f"legacy IBM source ID outside allowed alias context: {match}", lineno))
        if path.suffix in {".yml", ".yaml"}:
            try:
                data = yaml.safe_load(text)
            except Exception:
                continue
            def walk(value: object, owner: str = "") -> None:
                if isinstance(value, dict):
                    sid = value.get("source_id")
                    if isinstance(sid, str):
                        if sid.startswith("IBM-"):
                            findings.append(Finding("ERROR", path, f"legacy IBM source_id used as canonical value: {sid}"))
                        elif sid not in known and sid.startswith("EXTREF-"):
                            findings.append(Finding("ERROR", path, f"unknown EXTREF source_id: {sid}"))
                    for child in value.values():
                        walk(child, owner)
                elif isinstance(value, list):
                    for child in value:
                        walk(child, owner)
            walk(data)

    return emit(findings, args.mode, "EXTREF namespace check OK")


if __name__ == "__main__":
    raise SystemExit(main())
