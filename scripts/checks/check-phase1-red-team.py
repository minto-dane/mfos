#!/usr/bin/env python3
"""Phase 1 red-team validation for executable-semantics boundaries."""

from __future__ import annotations

from pathlib import Path
import re
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, mode_arg


DAFNY_DIR = ROOT / "formal" / "executable-semantics" / "dafny"
PHASE1_TOOL_DIRS = [
    ROOT / "tools" / "semantic-fixture-normalizer",
    ROOT / "tools" / "dafny-conformance-harness",
]

CODE_SUFFIXES = {
    ".c",
    ".cc",
    ".cpp",
    ".cxx",
    ".go",
    ".h",
    ".hpp",
    ".java",
    ".js",
    ".py",
    ".rs",
    ".sh",
    ".ts",
}
FORBIDDEN_CODE_ROOTS = [
    ROOT / "implementation" / "nucleus",
    ROOT / "implementation" / "services",
    ROOT / "implementation" / "pxm",
    ROOT / "implementation" / "guard",
    ROOT / "implementation" / "runtime",
    ROOT / "implementation" / "prototypes",
    ROOT / "implementation" / "tools",
    ROOT / "nucleus",
    ROOT / "services",
    ROOT / "pxm",
    ROOT / "guard",
]
ALLOWED_SCAFFOLD_FILES = {"README.md", ".mfos-dir.yml", "index.yml"}

RUST_SEMANTIC_CORE_PATH = re.compile(
    r"(?:^|/)(?:semantic[-_]?core|portable[-_]?semantic[-_]?core|rust[-_]?semantic[-_]?core)(?:/|$)",
    re.IGNORECASE,
)
DAEMON_PATH = re.compile(r"(?:^|/)(?:daemon|server|service-adapter|hosted-semantic)(?:/|$)", re.IGNORECASE)
DAEMON_CONTENT = re.compile(
    r"\b(?:listen|bind|serve_forever|HTTPServer|socketserver|uvicorn|fastapi|flask|actix|tokio::net|TcpListener)\b"
)
SPEC_SUCCESS = re.compile(
    r"\b(?:UNSUPPORTED|MFOS_ERR_UNSUPPORTED|SPEC_GAP|MFOS_ERR_SPEC_GAP)\b.{0,80}"
    r"\b(?:success|succeed|passes|MFOS_OK|Ok\s*\(|return\s+0)\b",
    re.IGNORECASE,
)
SAFE_SPEC_SUCCESS = re.compile(
    r"\b(?:must not|never|not |no |fake-success|check|detect|reject|rejected|forbid|forbidden|"
    r"prohibit|fail closed|failure|convert|converting?|reported as success|NEG-MFOS-[A-Z0-9-]*SUCCESS)\b",
    re.IGNORECASE,
)

YAML_IN_DAFNY = re.compile(r"\b(?:yaml|yml|Yaml|YAML|safe_load|parseYaml|parse_yaml)\b")
EXTERNAL_DAFNY_MODULE = re.compile(
    r"^\s*(?:module|abstract\s+module)\s+.*\b(?:IBM|ZOS|Z\/OS|MVS|RACF|JCL|CICS|DB2|IMS|VTAM)\b",
    re.IGNORECASE,
)
PY_LOADER_BUSINESS_LOGIC = re.compile(
    r"\b(?:authorize|schedule|dispatch|allocate|mount|catalog|spool|execute|interpret|evaluate|transition)\w*\s*\(",
    re.IGNORECASE,
)
PY_LOADER_FILES = [
    ROOT / "scripts" / "validators" / "validate-fixture-golden-loader.py",
]


def _is_allowed_scaffold_file(path: Path) -> bool:
    return path.name in ALLOWED_SCAFFOLD_FILES or path.suffix in {".md", ".yml", ".yaml", ".txt"}


def _check_forbidden_code(findings: list[Finding]) -> None:
    for root in FORBIDDEN_CODE_ROOTS:
        if not root.exists():
            continue
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            rel = path.relative_to(ROOT).as_posix()
            if path.suffix == ".rs" or RUST_SEMANTIC_CORE_PATH.search(rel):
                findings.append(Finding("ERROR", path, "Phase 1 must not add Rust semantic-core artifacts"))
                continue
            if path.name in ALLOWED_SCAFFOLD_FILES or path.suffix in {".md", ".yml", ".yaml", ".txt"}:
                continue
            if path.suffix in CODE_SUFFIXES or path.name in {"Cargo.toml", "Makefile", "Dockerfile"}:
                findings.append(Finding("ERROR", path, "Phase 1 must not add production or prototype implementation code"))


def _check_hosted_daemon(findings: list[Finding]) -> None:
    roots = [ROOT / "implementation", ROOT / "services"]
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            rel = path.relative_to(ROOT).as_posix()
            if path.name in ALLOWED_SCAFFOLD_FILES or path.suffix in {".md", ".yml", ".yaml", ".txt"}:
                continue
            if DAEMON_PATH.search(rel):
                findings.append(Finding("ERROR", path, "Phase 1 must not add hosted daemon or hosted semantic prototype code"))
                continue
            if path.suffix in CODE_SUFFIXES:
                for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                    if DAEMON_CONTENT.search(line):
                        findings.append(Finding("ERROR", path, "Phase 1 must not add listener/server daemon behavior", lineno))


def _check_dafny_boundaries(findings: list[Finding]) -> None:
    if not DAFNY_DIR.exists():
        findings.append(Finding("ERROR", DAFNY_DIR, "Phase 1 Dafny scaffold directory is missing"))
        return
    for path in sorted(p for p in DAFNY_DIR.rglob("*") if p.is_file()):
        if _is_allowed_scaffold_file(path):
            continue
        if path.suffix not in {".dfy", ".dafny", ".py"}:
            findings.append(Finding("ERROR", path, "unexpected Phase 1 Dafny scaffold artifact type"))
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if path.suffix in {".dfy", ".dafny"}:
                if YAML_IN_DAFNY.search(line):
                    findings.append(Finding("ERROR", path, "Dafny artifacts must not parse YAML", lineno))
                if EXTERNAL_DAFNY_MODULE.search(line):
                    findings.append(Finding("ERROR", path, "Dafny module names must not use external product/platform names", lineno))
            elif path.suffix == ".py" and PY_LOADER_BUSINESS_LOGIC.search(line):
                findings.append(Finding("ERROR", path, "Python loaders must stay metadata-only and not encode business semantics", lineno))

    for root in PHASE1_TOOL_DIRS:
        if not root.exists():
            findings.append(Finding("ERROR", root, "required Phase 1 tool directory missing"))
            continue
        for path in sorted(p for p in root.rglob("*.py") if p.is_file()):
            for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if DAEMON_CONTENT.search(line):
                    findings.append(Finding("ERROR", path, "Phase 1 tools must not add listener/server daemon behavior", lineno))
                if PY_LOADER_BUSINESS_LOGIC.search(line):
                    findings.append(Finding("ERROR", path, "Phase 1 Python tools must not encode MFOS business semantics", lineno))


def _check_python_loaders(findings: list[Finding]) -> None:
    loader_files = set(PY_LOADER_FILES)
    validators = ROOT / "scripts" / "validators"
    if validators.exists():
        loader_files.update(path for path in validators.glob("*loader*.py") if path.is_file())
    for path in sorted(loader_files):
        if not path.exists():
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if PY_LOADER_BUSINESS_LOGIC.search(line):
                findings.append(Finding("ERROR", path, "Python loaders must stay metadata-only and not encode business semantics", lineno))


def _check_spec_gap_success(findings: list[Finding]) -> None:
    roots = [ROOT / "formal", ROOT / "implementation", ROOT / "tests", ROOT / "docs" / "design" / "specs"]
    suffixes = {".md", ".yml", ".yaml", ".txt", ".py", ".rs", ".dfy", ".dafny"}
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(p for p in root.rglob("*") if p.is_file() and p.suffix in suffixes):
            for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if ("UNSUPPORTED" not in line and "SPEC_GAP" not in line) or SAFE_SPEC_SUCCESS.search(line):
                    continue
                if SPEC_SUCCESS.search(line):
                    findings.append(Finding("ERROR", path, "SPEC_GAP/UNSUPPORTED must not be treated as success", lineno))


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    _check_forbidden_code(findings)
    _check_hosted_daemon(findings)
    _check_dafny_boundaries(findings)
    _check_python_loaders(findings)
    _check_spec_gap_success(findings)

    return emit(findings, args.mode, "Phase 1 red-team validation OK")


if __name__ == "__main__":
    raise SystemExit(main())
