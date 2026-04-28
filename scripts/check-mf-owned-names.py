#!/usr/bin/env python3
"""Check MFOS-owned names for product-name leakage.

This intentionally checks identifiers and file paths, not ordinary explanatory
prose. External product names may appear in source-reference and legal contexts.
"""

from __future__ import annotations

import re
from pathlib import Path

from mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg, text_files


FORBIDDEN = [
    "ibm",
    "zos",
    "z-os",
    "z_os",
    "mvs",
    "wlm",
    "racf",
    "jes",
    "jes2",
    "dfsms",
    "smf",
    "apf",
    "prsm",
    "pr-sm",
    "lpar",
    "zarchitecture",
    "z-architecture",
    "zarch",
    "zvm",
    "z-vm",
    "sdsf",
    "ispf",
    "tsoe",
    "tso-e",
    "tso",
    "zosmf",
    "zos-mf",
]
TOKEN_RE = re.compile("|".join(re.escape(token) for token in FORBIDDEN), re.IGNORECASE)

ALLOWED_PATH_PARTS = {
    "source-matrix",
    "sources",
    "NOTICE.md",
    "non-compatibility-statement.md",
    "legal-risk-policy.md",
    "source-reference-policy.md",
    "prohibited-wording-list.md",
}
ALLOWED_PREFIXES = (
    "reports/naming-",
    "reports/naming-safety/",
    "docs/design/source-matrix/",
    "sources/",
    "governance/",
    "adr/",
)
IDENTIFIER_KEYS = {
    "requirement_id",
    "test_id",
    "evidence_id",
    "claim_id",
    "schema_id",
    "spec_id",
    "pack_id",
    "component",
    "component_name",
    "service",
    "service_name",
    "binary",
    "command",
    "crate",
    "module",
}


def is_allowed_path(path: Path) -> bool:
    rel = str(path.relative_to(ROOT))
    if any(rel.startswith(prefix) for prefix in ALLOWED_PREFIXES):
        return True
    return any(part in ALLOWED_PATH_PARTS for part in path.parts)


def check_identifier(path: Path, key: str, value: object, findings: list[Finding]) -> None:
    if not isinstance(value, str):
        return
    if key.startswith("legacy_") or key in {"source_id", "legacy_source_ids", "source_refs", "source_matrix_ids"}:
        return
    if key in IDENTIFIER_KEYS and TOKEN_RE.search(value):
        findings.append(Finding("ERROR", path, f"MFOS-owned identifier contains external-product token: {key}={value}"))


def walk_identifiers(path: Path, value: object, findings: list[Finding]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            check_identifier(path, str(key), child, findings)
            walk_identifiers(path, child, findings)
    elif isinstance(value, list):
        for child in value:
            walk_identifiers(path, child, findings)


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    for path in sorted((ROOT / ".").rglob("*")):
        rel = str(path.relative_to(ROOT))
        if not path.is_dir() or "__pycache__" in path.parts or rel.startswith(".git/"):
            continue
        if is_allowed_path(path):
            continue
        for part in path.parts:
            if TOKEN_RE.search(part):
                findings.append(Finding("ERROR", path, f"MFOS-owned directory contains external-product token: {part}"))
                break

    for path in text_files([Path(".")]):
        rel = str(path.relative_to(ROOT))
        if "__pycache__" in path.parts or rel.startswith(".git/"):
            continue
        if not is_allowed_path(path):
            for part in path.parts:
                if TOKEN_RE.search(part):
                    findings.append(Finding("ERROR", path, f"MFOS-owned path contains external-product token: {part}"))
                    break
        if path.suffix not in {".yml", ".yaml", ".json"}:
            continue
        try:
            data = load_yaml(path)
        except SystemExit:
            continue
        if not is_allowed_path(path):
            walk_identifiers(path, data, findings)

    return emit(findings, args.mode, "MFOS-owned name check OK")


if __name__ == "__main__":
    raise SystemExit(main())
