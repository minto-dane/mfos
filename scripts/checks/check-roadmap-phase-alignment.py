#!/usr/bin/env python3
"""Check roadmap and prompt phase alignment for current Phase 1 policy."""

from __future__ import annotations

from pathlib import Path
import re
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, mode_arg, text_files


ROADMAP = ROOT / "docs/design/tasks/implementation-roadmap.md"
SEARCH_ROOTS = [
    Path("docs/design"),
    Path("tasks"),
    Path("packs"),
    Path("prompts"),
    Path("ai"),
    Path("reports/current"),
]
ARCHIVE_PARTS = {"archive", "pre-phase1", "fixedpoint"}
UNSAFE_HOSTED = re.compile(r"\bHosted Semantic Prototype\b|\bhosted semantic prototype\b", re.IGNORECASE)
UNSAFE_RUST = re.compile(r"\bRust semantic-core\b|\bRust semantic core\b|\bportable semantic core implementation\b", re.IGNORECASE)
CURRENT_PHASE1 = re.compile(r"\bPhase 1\b|\bcurrent\b|\ballowed\b|\bauthorize\w*\b|\bimplementation_profile\b", re.IGNORECASE)
SAFE_CONTEXT = re.compile(
    r"\b(?:not|must not|does not|do not|no |forbidden|blocked|superseded|inactive|historical|later reviewed gate|future|prohibit|prohibited|absence|without|proposed|previously|rejected)\b",
    re.IGNORECASE,
)
REQUIRED_ROADMAP_PHRASES = {
    "Phase 1: Verified Executable Semantics + Conformance Harness",
    "Current Phase 1 is Dafny executable semantics",
    "Hosted Semantic Prototype is superseded",
    "Rust semantic-core is not a Phase 1 canonical semantic implementation",
    "MFOS is x86-64-first for initial implementation planning and not x86-64-only",
    "x86-64-v4 is an optional performance profile, not a baseline",
    "Intel SGX is an optional enclave/TEE profile, not a Confidential VM profile",
    "Future AArch64 and RISC-V support is design-allowed but not implemented",
}


def _is_archive(path: Path) -> bool:
    rel_parts = set(path.relative_to(ROOT).parts)
    return bool(rel_parts & ARCHIVE_PARTS)


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    roadmap_text = ROADMAP.read_text(encoding="utf-8") if ROADMAP.exists() else ""
    normalized_roadmap = " ".join(roadmap_text.split())
    if not roadmap_text:
        findings.append(Finding("ERROR", ROADMAP, "implementation roadmap missing"))
    for phrase in sorted(REQUIRED_ROADMAP_PHRASES):
        if phrase not in normalized_roadmap:
            findings.append(Finding("ERROR", ROADMAP, f"missing current phase alignment phrase: {phrase}"))

    for path in text_files(SEARCH_ROOTS):
        if _is_archive(path):
            continue
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for lineno, line in enumerate(lines, 1):
            if not CURRENT_PHASE1.search(line):
                continue
            prev_line = lines[lineno - 2] if lineno > 1 else ""
            next_line = lines[lineno] if lineno < len(lines) else ""
            context = f"{prev_line} {line} {next_line}"
            if UNSAFE_HOSTED.search(line) and not SAFE_CONTEXT.search(context):
                findings.append(Finding("ERROR", path, "Hosted Semantic Prototype appears current rather than superseded/forbidden", lineno))
            if UNSAFE_RUST.search(line) and not SAFE_CONTEXT.search(context):
                findings.append(Finding("ERROR", path, "Rust semantic-core appears current rather than forbidden", lineno))

    return emit(findings, args.mode, "Roadmap phase alignment check OK")


if __name__ == "__main__":
    raise SystemExit(main())
