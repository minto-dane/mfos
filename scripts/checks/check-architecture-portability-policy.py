#!/usr/bin/env python3
"""Check MFOS architecture portability and non-x86 overclaim policy."""

from __future__ import annotations

from pathlib import Path
import re
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, mode_arg, text_files


SPEC = ROOT / "docs/design/specs/44-architecture-portability-policy.md"
SEARCH_ROOTS = [
    Path("docs/design"),
    Path("requirements"),
    Path("tasks"),
    Path("packs"),
    Path("prompts"),
    Path("ai"),
    Path("reports/current"),
]
REQUIRED_PHRASES = {
    "MFOS is x86-64-first",
    "it is not x86-64-only",
    "Architecture-neutral semantics include",
    "Authorization.",
    "Audit.",
    "Architecture-specific enforcement includes",
    "Privilege mode transitions.",
    "Platform-specific concerns are separate from CPU architecture concerns",
    "Future AArch64, RISC-V, or other architecture support may be designed",
    "must not be claimed as implemented",
    "No AArch64, RISC-V, or other non-x86 backend is present in the current tree",
    "The CPU Feature Registry is design-time governance",
    "It is not a CPU feature detector",
}
NON_X86_TERM = re.compile(r"\b(?:AArch64|ARM|RISC-V|riscv64|non-x86)\b", re.IGNORECASE)
NON_X86_OVERCLAIM = re.compile(
    r"\b(?:"
    r"(?:AArch64|ARM|RISC-V|riscv64|non-x86)\b.{0,100}\b(?:implemented|supported|available|ready|complete|exists|present|included|includes|enabled)"
    r"|(?:supports|implements|ships|provides|includes|has|contains)\b.{0,100}\b(?:AArch64|ARM|RISC-V|riscv64|non-x86)\b"
    r"|(?:AArch64|ARM|RISC-V|riscv64|non-x86)\b.{0,60}\bbackend\b.{0,40}\b(?:exists|present|available|implemented|ready)"
    r")",
    re.IGNORECASE,
)
SAFE_NON_X86 = re.compile(
    r"\b(?:"
    r"(?:must not|do not) claim|marked implemented without|must not be claimed as implemented|not claimed as implemented|not implemented|not present|"
    r"no .*backend is present|no .* is implemented|no .* exists|claimed as implemented without|support claimed without evidence|"
    r"without source cards|without .*evidence|future .*may be designed|may be designed|design-allowed but not implemented|"
    r"must be supported through explicit architecture/backend boundaries|supported through explicit architecture/backend boundaries|"
    r"planned only|future-gated|source gap|reject(?:ed)?|blocked|forbidden"
    r")\b",
    re.IGNORECASE,
)


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []
    text = SPEC.read_text(encoding="utf-8") if SPEC.exists() else ""
    normalized_text = " ".join(text.split())
    if not text:
        findings.append(Finding("ERROR", SPEC, "architecture portability policy spec missing"))
    for phrase in sorted(REQUIRED_PHRASES):
        if phrase not in normalized_text:
            findings.append(Finding("ERROR", SPEC, f"missing required architecture policy phrase: {phrase}"))

    for path in text_files(SEARCH_ROOTS):
        if "source-matrix/cards" in path.as_posix():
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if NON_X86_TERM.search(line) and NON_X86_OVERCLAIM.search(line) and not SAFE_NON_X86.search(line):
                findings.append(Finding("ERROR", path, "possible non-x86 implementation/support overclaim", lineno))

    return emit(findings, args.mode, "Architecture portability policy check OK")


if __name__ == "__main__":
    raise SystemExit(main())
