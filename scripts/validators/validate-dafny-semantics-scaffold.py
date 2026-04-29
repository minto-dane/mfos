#!/usr/bin/env python3
"""Validate the Dafny executable-semantics scaffold boundary."""

from __future__ import annotations

from pathlib import Path
import re
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, SPECS_DIR, emit, load_yaml, mode_arg, parse_front_matter


SCAFFOLD_DIR = ROOT / "formal" / "executable-semantics" / "dafny"
README = SCAFFOLD_DIR / "README.md"
METADATA = SCAFFOLD_DIR / ".mfos-dir.yml"
PHASE_1_POLICY_FILES = [
    ROOT / "docs" / "design" / "STATUS.md",
    ROOT / "reports" / "phases" / "phase-1" / "readiness-report.md",
    ROOT / "reports" / "phases" / "phase-1" / "open-issues.md",
    ROOT / "reports" / "phases" / "phase-1" / "pxm-mfvm-readiness-after-refactor.md",
    ROOT / "reports" / "phases" / "phase-1" / "pack-readiness-recheck.md",
    ROOT / "reports" / "phases" / "phase-1" / "pack-readiness-recheck.yml",
]

STANDARD_FRONT_MATTER = {
    "spec_id",
    "title",
    "canonical_language",
    "japanese_mirror",
    "status",
    "owner",
    "last_reviewed",
    "source_refs",
    "requirement_refs",
    "claim_refs",
    "test_refs",
    "evidence_refs",
    "implementation_allowed",
    "downstream_packs",
    "spec_gap_policy",
}

BOUNDARY_CONCEPTS = {
    "Dafny executable-semantics scaffold path": (
        "formal/executable-semantics/dafny",
    ),
    "validation-only scope": (
        "validation-only",
        "validation only",
        "loader-only artifact validation",
        "loader only artifact validation",
    ),
    "no Rust semantic-core implementation": (
        "does not authorize rust semantic-core implementation",
        "does not authorize rust semantic core implementation",
        "does not authorize a rust semantic core",
        "phase 1 does not authorize a rust semantic core",
        "no rust semantic-core implementation",
        "no rust semantic core implementation",
    ),
    "no semantic runner implementation": (
        "does not authorize semantic runner implementation",
        "does not authorize semantic-runner implementation",
        "does not authorize a semantic runner",
        "does not authorize semantic runner commands",
        "phase 1 does not authorize a semantic runner",
        "no semantic runner implementation",
        "no semantic-runner implementation",
    ),
    "no hosted daemon implementation": (
        "does not authorize hosted daemon implementation",
        "does not authorize hosted daemons",
        "does not authorize a hosted daemon",
        "phase 1 does not authorize a hosted daemon",
        "no hosted daemon implementation",
        "no hosted daemons",
    ),
}

FORBIDDEN_METADATA_FLAGS = {
    "production",
    "hosted_daemon",
    "semantic_runner",
    "portable_semantic_core",
    "hosted_semantic_prototype",
    "rust_semantic_core",
}

REQUIRED_DAFNY_PATTERNS = [
    re.compile(r"\.dafny\s+files?\s+(?:are\s+)?required\b", re.IGNORECASE),
    re.compile(r"\brequires?\s+\.dafny\s+files?\b", re.IGNORECASE),
    re.compile(r"\bmust\s+(?:contain|include|provide)\s+\.dafny\s+files?\b", re.IGNORECASE),
]

SAFE_REQUIRED_DAFNY_MARKERS = (
    "no .dafny files are required",
    "no .dafny files required",
    ".dafny files are not required",
    "does not require .dafny",
    "do not require .dafny",
    "optional",
)

PHASE_1_TRUE_FLAG = re.compile(
    r"\b(?:phase_1_)?(?:rust_)?(?:portable_)?(?:semantic_core|semantic_runner|hosted_daemon)"
    r"(?:_implementation)?_allowed:\s*true\b",
    re.IGNORECASE,
)

PHASE_1_PERMISSION_PATTERNS = [
    re.compile(
        r"\bphase\s*1\b.{0,120}\b(?:may|can|is allowed to|is permitted to|is authorized to)\s+"
        r"(?:implement|start|build|run|execute|add|ship|enable).{0,120}\b"
        r"(?:rust\s+semantic[- ]core|semantic[- ]core|semantic[- ]runner|hosted\s+daemon)s?\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:rust\s+semantic[- ]core|semantic[- ]core|semantic[- ]runner|hosted\s+daemon)s?\b"
        r".{0,100}\b(?:implementation|work|commands?|daemon(?:s)?)\s+"
        r"(?:allowed|permitted|authorized|enabled)\b",
        re.IGNORECASE,
    ),
]

SAFE_PERMISSION_MARKERS = (
    "false",
    "not ",
    "not_",
    "no ",
    "may not",
    "must not",
    "does not",
    "do not",
    "cannot",
    "blocked",
    "prohibit",
    "prohibited",
    "forbidden",
    "limited to",
    "loader-only",
)


def _find_spec_43() -> Path | None:
    candidates = sorted(SPECS_DIR.glob("43-*.md"))
    dafny_candidates = [
        path
        for path in candidates
        if "dafny" in path.name.lower()
        and ("semantic" in path.name.lower() or "semantics" in path.name.lower())
    ]
    if dafny_candidates:
        return dafny_candidates[0]

    for path in candidates:
        text = path.read_text(encoding="utf-8", errors="replace").lower()
        if "dafny" in text and "semantic" in text:
            return path
    return None


def _has_any(text: str, phrases: tuple[str, ...]) -> bool:
    lower = text.lower()
    return any(phrase in lower for phrase in phrases)


def _check_spec_43(findings: list[Finding]) -> None:
    spec = _find_spec_43()
    if spec is None:
        findings.append(Finding("ERROR", SPECS_DIR / "43-*.md", "missing spec 43 Dafny executable-semantics scaffold"))
        return

    text = spec.read_text(encoding="utf-8", errors="replace")
    fm, error = parse_front_matter(spec)
    if error:
        findings.append(Finding("ERROR", spec, error))
        return
    if fm is None:
        findings.append(Finding("ERROR", spec, "missing front matter"))
        return

    missing = sorted(STANDARD_FRONT_MATTER - set(fm))
    if missing:
        findings.append(Finding("ERROR", spec, f"front matter missing fields: {', '.join(missing)}"))

    spec_id = fm.get("spec_id")
    if not isinstance(spec_id, str) or not spec_id.startswith("MFOS-SPEC-43-") or "DAFNY" not in spec_id.upper():
        findings.append(Finding("ERROR", spec, f"spec_id must identify MFOS-SPEC-43 Dafny scope, got {spec_id!r}"))
    if fm.get("implementation_allowed") is not False:
        findings.append(Finding("ERROR", spec, "implementation_allowed must be false"))
    if fm.get("spec_gap_policy") != "implementation_must_not_infer_or_fill_gaps":
        findings.append(Finding("ERROR", spec, "spec_gap_policy must block inferred implementation"))

    for concept, phrases in BOUNDARY_CONCEPTS.items():
        if not _has_any(text, phrases):
            findings.append(Finding("ERROR", spec, f"missing boundary phrase for {concept}"))


def _check_metadata_flags(data: object, path: Path, findings: list[Finding]) -> None:
    if not isinstance(data, dict):
        findings.append(Finding("ERROR", path, ".mfos-dir.yml must be a mapping"))
        return
    if data.get("path") != "formal/executable-semantics/dafny":
        findings.append(Finding("ERROR", path, "path must be formal/executable-semantics/dafny"))

    implementation_allowed = data.get("implementation_allowed")
    if not isinstance(implementation_allowed, dict):
        findings.append(Finding("ERROR", path, "implementation_allowed must be a mapping"))
        return
    for flag in sorted(FORBIDDEN_METADATA_FLAGS):
        if implementation_allowed.get(flag) is True:
            findings.append(Finding("ERROR", path, f"implementation_allowed.{flag} must not be true"))


def _check_scaffold_dir(findings: list[Finding]) -> None:
    if not SCAFFOLD_DIR.exists():
        findings.append(Finding("ERROR", SCAFFOLD_DIR, "Dafny executable-semantics scaffold directory missing"))
        return
    if not README.exists():
        findings.append(Finding("ERROR", README, "README.md missing"))
    if not METADATA.exists():
        findings.append(Finding("ERROR", METADATA, ".mfos-dir.yml missing"))
    else:
        _check_metadata_flags(load_yaml(METADATA), METADATA, findings)

    for path in (README, METADATA):
        if not path.exists():
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            lower = line.lower()
            if any(marker in lower for marker in SAFE_REQUIRED_DAFNY_MARKERS):
                continue
            if any(pattern.search(line) for pattern in REQUIRED_DAFNY_PATTERNS):
                findings.append(Finding("ERROR", path, "scaffold must not require .dafny files", lineno))


def _safe_permission_line(line: str) -> bool:
    lower = line.lower()
    return any(marker in lower for marker in SAFE_PERMISSION_MARKERS)


def _check_phase_1_policy(findings: list[Finding]) -> None:
    for path in PHASE_1_POLICY_FILES:
        if not path.exists():
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if PHASE_1_TRUE_FLAG.search(line):
                findings.append(Finding("ERROR", path, f"Phase 1 policy grants forbidden implementation permission: {line.strip()}", lineno))
                continue
            if _safe_permission_line(line):
                continue
            if any(pattern.search(line) for pattern in PHASE_1_PERMISSION_PATTERNS):
                findings.append(Finding("ERROR", path, f"Phase 1 policy grants forbidden implementation permission: {line.strip()}", lineno))


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    _check_spec_43(findings)
    _check_scaffold_dir(findings)
    _check_phase_1_policy(findings)

    return emit(findings, args.mode, "Dafny semantics scaffold validation OK")


if __name__ == "__main__":
    raise SystemExit(main())
