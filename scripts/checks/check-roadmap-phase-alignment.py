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
FUTURE_GATE_PATHS = {
    Path("ai/README.md"),
    Path("ai/contracts/ai-implementation-contract.md"),
    Path("docs/design/STATUS.md"),
    Path("docs/design/packs/PACKS.md"),
    Path("docs/design/prompts/ai-prompts.md"),
    Path("docs/design/tasks/implementation-roadmap.md"),
    Path("packs/pack-index.yml"),
    Path("prompts/README.md"),
}
UNSAFE_HOSTED = re.compile(r"\bHosted Semantic Prototype\b|\bhosted semantic prototype\b", re.IGNORECASE)
UNSAFE_RUST = re.compile(r"\bRust semantic-core\b|\bRust semantic core\b|\bportable semantic core implementation\b", re.IGNORECASE)
UNSAFE_PHRASE = re.compile(
    r"\bHosted Semantic Prototype\b|\bhosted semantic prototype\b|"
    r"\bRust semantic-core\b|\bRust semantic core\b|\bportable semantic core implementation\b",
    re.IGNORECASE,
)
FUTURE_GATED_IMPLEMENTATION = re.compile(
    r"\b(?:PXM|MFVM|CVM|TEE|SGX|cluster|architecture backend|hardware path|CPU feature detection)\b"
    r".{0,120}\b(?:implementation|runtime|backend|detector|detection|work|host|run)\b",
    re.IGNORECASE,
)
SAFE_CONTEXT = re.compile(
    r"\b(?:"
    r"must not|does not|do not|not allowed|not authorized|not current|not a Phase 1 canonical|"
    r"forbidden|blocked|superseded|inactive|historical|later reviewed gate|future-gated|later-gated|"
    r"prohibit(?:ed)?|absence|without|proposed|previously|rejected|rejects|non_objectives|"
    r"out of scope|negative .*boundar|intentionally avoids|remain(?:s)? absent|remain(?:s)? false|permissions remain false|not introduced|not added|"
    r"no .*rust semantic|no .*portable semantic|no .*semantic runner.*rust|no phase 1 .* may designate|"
    r"phase [2-9]|future|later|planning|prototype|candidate|must exist before|before assigning|"
    r"allowed:\s*false|:\s*false"
    r")\b",
    re.IGNORECASE,
)
NEGATED_SAFE_TERMS = re.compile(r"\bnot\s+(?:forbidden|blocked|superseded|prohibited|rejected|inactive|historical)\b", re.IGNORECASE)
REQUIRED_ROADMAP_PHRASES = {
    "Phase 1: Verified Executable Semantics + Conformance Harness",
    "Current Phase 1 is Dafny executable semantics",
    "Hosted Semantic Prototype is superseded",
    "Rust semantic-core is not a Phase 1 canonical semantic implementation",
    "MFOS is x86-64-first for initial implementation planning and not x86-64-only",
    "x86-64-v4 is an optional performance profile, not a baseline",
    "Intel SGX is an optional enclave/TEE profile, not a Confidential VM profile",
    "Future AArch64 and RISC-V support is design-allowed but not implemented",
    "PXM/MFVM/CVM/TEE/SGX runtime work, architecture backends, CPU feature detection, and production code",
    "CPU Feature Registry and target profile policy must exist before assigning hardware-facing architecture backend implementation",
}


def _is_archive(path: Path) -> bool:
    rel_parts = set(path.relative_to(ROOT).parts)
    return bool(rel_parts & ARCHIVE_PARTS)


def _check_future_gate_path(path: Path) -> bool:
    return path.relative_to(ROOT) in FUTURE_GATE_PATHS


def _safe_context(context: str) -> bool:
    if NEGATED_SAFE_TERMS.search(context):
        return False
    return bool(SAFE_CONTEXT.search(context))


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
            start = max(0, lineno - 12)
            end = min(len(lines), lineno + 8)
            context = " ".join(lines[start:end])
            if UNSAFE_PHRASE.search(line):
                if UNSAFE_HOSTED.search(line) and not _safe_context(context):
                    findings.append(Finding("ERROR", path, "Hosted Semantic Prototype appears current rather than superseded/forbidden", lineno))
                if UNSAFE_RUST.search(line) and not _safe_context(context):
                    findings.append(Finding("ERROR", path, "Rust semantic-core appears current rather than forbidden", lineno))
            if _check_future_gate_path(path) and FUTURE_GATED_IMPLEMENTATION.search(line) and not _safe_context(context):
                findings.append(Finding("ERROR", path, "future-gated PXM/MFVM/CVM/TEE/SGX/cluster/backend work appears current", lineno))

    return emit(findings, args.mode, "Roadmap phase alignment check OK")


if __name__ == "__main__":
    raise SystemExit(main())
