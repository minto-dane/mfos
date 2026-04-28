#!/usr/bin/env python3
"""Detect unguarded external-product compatibility or affiliation claims."""

from __future__ import annotations

import re
from pathlib import Path

from mfos_lint import Finding, ROOT, emit, mode_arg, text_files


EXTERNAL_RE = re.compile(r"\b(IBM|z/OS|RACF|JES2?|DFSMS|SMF|MVS|IBM Z|z/Architecture|APF|PR/SM|LPAR|SDSF|ISPF|TSO/E|TSO|zOSMF|z/OSMF)\b", re.IGNORECASE)
RISK_RE = re.compile(
    r"\b("
    r"(?:is|are|be|being|claims?|supports?|provides?)\s+(?:[a-z0-9_./-]+\s+){0,8}(?:compatible|equivalent|replacement)"
    r"|compatible\s+with"
    r"|equivalent\s+to"
    r"|replacement\s+for"
    r"|(?:certified|approved|endorsed|sponsored)\s+by\s+IBM"
    r"|IBM\s+(?:certified|approved|endorsed|sponsored)"
    r")\b",
    re.IGNORECASE,
)
SAFE_RE = re.compile(r"\b(not|no|does not|do not|must not|without|disclaim|disclaimer|prohibit|prohibited|non-compatibility|not affiliated|not endorsed|not sponsored|not certified|not approved)\b", re.IGNORECASE)
ALLOWED_PREFIXES = (
    "reports/naming-",
    "docs/design/source-matrix/",
    "NOTICE.md",
    "governance/non-compatibility-statement.md",
    "docs/design/legal-risk-policy.md",
)


def allowed_file(path: Path) -> bool:
    rel = str(path.relative_to(ROOT))
    return any(rel == prefix.rstrip("/") or rel.startswith(prefix) for prefix in ALLOWED_PREFIXES)


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    roots = [
        Path("README.md"),
        Path("README.ja.md"),
        Path("docs"),
        Path("governance"),
        Path("adr"),
        Path("sources"),
        Path("requirements"),
        Path("specs"),
        Path("packs"),
        Path("prompts"),
        Path("ai"),
        Path("implementation"),
        Path("schemas"),
    ]
    for path in text_files(roots):
        if allowed_file(path):
            continue
        safe_until = 0
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if re.search(r"prohibited wording|prohibited_inference|must not|do not|non-compat", line, re.IGNORECASE):
                safe_until = lineno + 20
            if not (EXTERNAL_RE.search(line) and RISK_RE.search(line)):
                continue
            if lineno <= safe_until or SAFE_RE.search(line):
                continue
            findings.append(Finding("ERROR", path, "unguarded external compatibility/affiliation wording", lineno))

    return emit(findings, args.mode, "Compatibility-claim check OK")


if __name__ == "__main__":
    raise SystemExit(main())
