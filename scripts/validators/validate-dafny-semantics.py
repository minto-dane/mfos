#!/usr/bin/env python3
"""Validate Phase 1 Dafny executable-semantics artifacts."""

from __future__ import annotations

from pathlib import Path
import re
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, mode_arg


DAFNY_DIR = ROOT / "formal" / "executable-semantics" / "dafny"
MODULE_DIR = DAFNY_DIR / "modules"
REQUIRED_MODULES = {
    "common.dfy",
    "errors.dfy",
    "types.dfy",
    "authorization.dfy",
    "audit.dfy",
    "dataset_catalog.dfy",
    "job_spool.dfy",
    "operator_console.dfy",
    "first_vertical_slice.dfy",
}

FORBIDDEN_HOST_SEMANTICS = re.compile(
    r"\b(?:filesystem|wall[- ]clock|process\s+id|pid|host\s+user|username|socket|random|safe_load|yaml|yml)\b",
    re.IGNORECASE,
)
EXTERNAL_MODULE_NAME = re.compile(
    r"^\s*(?:module|abstract\s+module)\s+.*\b(?:IBM|ZOS|MVS|RACF|JES|DFSMS|SMF|HYPERV|KVM)\b",
    re.IGNORECASE,
)
SPEC_SUCCESS = re.compile(
    r"\b(?:MFOS_ERR_SPEC_GAP|MFOS_ERR_UNSUPPORTED|SPEC_GAP|UNSUPPORTED)\b.{0,80}"
    r"\b(?:MFOS_OK|success|successful|passes|return\s+0)\b",
    re.IGNORECASE,
)
SAFE_SPEC_SUCCESS = re.compile(r"\b(?:not|never|must not|forbidden|fail[- ]closed|blocked|reject|converted into success)\b", re.IGNORECASE)
LOWER_SNAKE_DAFNY = re.compile(r"^[a-z][a-z0-9_]*\.dfy$")


def _check_required_files(findings: list[Finding]) -> None:
    for rel in [
        "README.md",
        ".mfos-dir.yml",
        "tests/README.md",
        "generated/README.md",
        "generated/DO_NOT_USE_IN_PRODUCTION.md",
    ]:
        path = DAFNY_DIR / rel
        if not path.exists():
            findings.append(Finding("ERROR", path, "required Dafny semantics artifact missing"))

    if not MODULE_DIR.exists():
        findings.append(Finding("ERROR", MODULE_DIR, "Dafny module directory missing"))
        return

    present = {path.name for path in MODULE_DIR.glob("*.dfy")}
    lowered: dict[str, Path] = {}
    for path in sorted(MODULE_DIR.glob("*.dfy")):
        if not LOWER_SNAKE_DAFNY.match(path.name):
            findings.append(Finding("ERROR", path, "canonical Dafny module files must use lower_snake_case.dfy"))
        lower_name = path.name.lower()
        if lower_name in lowered:
            findings.append(Finding("ERROR", path, f"case-only duplicate Dafny module also matches {lowered[lower_name]}"))
        lowered[lower_name] = path
    for name in sorted(REQUIRED_MODULES - present):
        findings.append(Finding("ERROR", MODULE_DIR / name, "required Dafny module missing"))
    for name in sorted(present - REQUIRED_MODULES):
        findings.append(Finding("WARN", MODULE_DIR / name, "unexpected Dafny module not in Phase 1 module list"))


def _check_dafny_text(findings: list[Finding]) -> None:
    for path in sorted(MODULE_DIR.glob("*.dfy")):
        text = path.read_text(encoding="utf-8", errors="replace")
        if "module " not in text:
            findings.append(Finding("ERROR", path, "Dafny artifact lacks module declaration"))
        for lineno, line in enumerate(text.splitlines(), 1):
            if EXTERNAL_MODULE_NAME.search(line):
                findings.append(Finding("ERROR", path, "module/type name must not use external product identifiers", lineno))
            if FORBIDDEN_HOST_SEMANTICS.search(line):
                findings.append(Finding("ERROR", path, "Dafny semantics must not reference host/YAML/random semantics", lineno))
            if ("UNSUPPORTED" in line or "SPEC_GAP" in line or "MFOS_ERR_UNSUPPORTED" in line or "MFOS_ERR_SPEC_GAP" in line):
                if SPEC_SUCCESS.search(line) and not SAFE_SPEC_SUCCESS.search(line):
                    findings.append(Finding("ERROR", path, "SPEC_GAP/UNSUPPORTED must not be success", lineno))


def _check_first_vertical_slice(findings: list[Finding]) -> None:
    path = MODULE_DIR / "first_vertical_slice.dfy"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    required = [
        "BobDeniedAliceDatasetResult",
        "MFOS_ERR_POLICY_DENIED",
        "DATASET_READ_NOT_PERMITTED",
        "dataset_handle_created",
        "audit_before_final_result",
    ]
    for marker in required:
        if marker not in text:
            findings.append(Finding("ERROR", path, f"first vertical slice missing marker: {marker}"))


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []
    _check_required_files(findings)
    _check_dafny_text(findings)
    _check_first_vertical_slice(findings)
    return emit(findings, args.mode, "Dafny executable-semantics artifact validation OK")


if __name__ == "__main__":
    raise SystemExit(main())
