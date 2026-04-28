#!/usr/bin/env python3
"""Check source ID references and basic source-grounding coverage."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

import re
from pathlib import Path

from lib.mfos_lint import SOURCE_ID_RE, Finding, ROOT, emit, mode_arg, parse_front_matter, source_ids, text_files


TRIGGER_RE = re.compile(
    r"\b(z/OS|MVS|JCL|JES2?|RACF|DFSMS|SMF|WLM|APF|PSW|storage key|SVC|PC instruction|cross-memory|LPAR|PR/SM|DPM|z/OS UNIX|SYSIN|SYSOUT|spool|catalog|dataset|operator command|authorized program|authorized module)\b",
    re.IGNORECASE,
)
SOURCE_SECTION_RE = re.compile(r"source matrix|source ids?|source references?", re.IGNORECASE)


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    known = source_ids()
    findings: list[Finding] = []
    roots = [
        Path("docs/design/specs"),
        Path("docs/design/source-matrix"),
        Path("docs/design/assurance"),
        Path("docs/design/packs"),
        Path("docs/design/tasks"),
        Path("requirements"),
        Path("claims"),
        Path("packs"),
        Path("specs"),
    ]

    for path in text_files(roots):
        text = path.read_text(encoding="utf-8", errors="replace")
        file_sources = set(SOURCE_ID_RE.findall(text))
        for lineno, line in enumerate(text.splitlines(), 1):
            for source_id in SOURCE_ID_RE.findall(line):
                if source_id not in known:
                    findings.append(Finding("ERROR", path, f"unknown Source Matrix ID: {source_id}", lineno))
        if path.is_relative_to(ROOT / "docs/design/specs") and path.name != "27-spec-front-matter.md":
            if TRIGGER_RE.search(text) and not file_sources:
                findings.append(Finding("WARN", path, "z/OS-inspired terms appear without any Source Matrix IDs"))
            elif TRIGGER_RE.search(text) and not SOURCE_SECTION_RE.search(text):
                findings.append(Finding("WARN", path, "z/OS-inspired terms appear without an explicit source-reference section heading"))
            front_matter, _ = parse_front_matter(path)
            strict_line_local = isinstance(front_matter, dict) and front_matter.get("statement_source_grounding") == "line_local"
            if args.mode == "release" and strict_line_local:
                in_fence = False
                for lineno, line in enumerate(text.splitlines(), 1):
                    stripped = line.strip()
                    if stripped.startswith("```"):
                        in_fence = not in_fence
                        continue
                    if in_fence or not TRIGGER_RE.search(line):
                        continue
                    if SOURCE_ID_RE.search(line):
                        continue
                    if stripped.startswith(("#", "|", "-", "*")) or stripped.endswith(":"):
                        continue
                    if re.search(r"Source IDs?|Source Matrix|source references?", line, re.IGNORECASE):
                        continue
                    findings.append(Finding("WARN", path, "release-mode z/OS-derived statement lacks line-local Source Matrix ID", lineno))

    return emit(findings, args.mode, "Source grounding check OK")


if __name__ == "__main__":
    raise SystemExit(main())
