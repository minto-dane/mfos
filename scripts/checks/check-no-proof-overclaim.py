#!/usr/bin/env python3
"""Check Phase 0.10 language/formal artifacts for proof overclaims."""

from __future__ import annotations

from pathlib import Path
import re
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg, text_files


FORMAL_REGISTRY = ROOT / "formal/registry.yml"
SCAN_ROOTS = [
    Path("docs/design/specs/39-language-and-verification-policy.md"),
    Path("docs/design/specs/40-automated-reasoning-program.md"),
    Path("docs/design/specs/41-performance-and-secure-operations.md"),
    Path("docs/design/assurance"),
    Path("formal"),
    Path("requirements/by-domain"),
    Path("reports/current"),
    Path("docs/design/packs/PACK-34-language-verification"),
    Path("docs/design/packs/PACK-35-automated-reasoning"),
    Path("docs/design/packs/PACK-36-performance-and-secure-operations"),
]

OVERCLAIM_PATTERNS = [
    re.compile(r"\bproof(?:s)?\s+(?:is|are)\s+(?:complete|accepted|verified)\b", re.IGNORECASE),
    re.compile(r"\b(?:complete|accepted|verified)\s+proof(?:s)?\b", re.IGNORECASE),
    re.compile(r"\bformally\s+verified\s+(?:kernel|hypervisor|implementation|component|authorization|audit|pxm|mfvm|cvm)\b", re.IGNORECASE),
    re.compile(r"\bverified\s+(?:kernel|hypervisor|implementation|authorization|audit-chain|vm isolation|pxm correctness)\b", re.IGNORECASE),
    re.compile(r"\b(?:memory-safe|memory safe)\s+(?:implementation|kernel|hypervisor|component)\b", re.IGNORECASE),
    re.compile(r"\bcomplete\s+(?:memory safety|control-flow integrity|cfi|cet enforcement|proof coverage)\b", re.IGNORECASE),
    re.compile(r"\b(?:absence|free)\s+of\s+(?:undefined behavior|exploitable vulnerabilities)\b", re.IGNORECASE),
    re.compile(r"\bproof_claimed:\s*true\b", re.IGNORECASE),
]

SAFE_MARKERS = (
    "not ",
    "not-",
    "no ",
    "does not",
    "do not",
    "must not",
    "cannot",
    "without",
    "unless",
    "out of scope",
    "out-of-scope",
    "non-objective",
    "non-goal",
    "prohibit",
    "prohibited",
    "forbidden",
    "planned",
    "future",
    "candidate",
    "placeholder",
    "draft",
    "gap",
    "overclaim",
    "ban",
    "bans",
    "not claimed",
    "not_claimed",
    "proof_claimed: false",
)

SAFE_BLOCK_MARKERS = (
    "overclaim ban",
    "overclaim bans",
    "not_claimed:",
    "non-objectives",
    "non-goals",
    "out of scope",
    "out-of-scope",
    "no production",
    "must not claim",
    "not claim",
    "no proof",
    "proof_claimed: false",
    "prohibited",
    "forbidden",
)


def _safe_line(line: str, in_safe_block: bool) -> bool:
    lower = line.lower()
    return in_safe_block or any(marker in lower for marker in SAFE_MARKERS)


def _check_registry(findings: list[Finding]) -> None:
    data = load_yaml(FORMAL_REGISTRY) if FORMAL_REGISTRY.exists() else None
    if not isinstance(data, dict):
        findings.append(Finding("ERROR", FORMAL_REGISTRY, "formal registry must be a mapping"))
        return
    if data.get("proof_claimed") is not False:
        findings.append(Finding("ERROR", FORMAL_REGISTRY, "top-level proof_claimed must remain false"))
    for section in ("proof_obligations",):
        value = data.get(section)
        if not isinstance(value, list):
            findings.append(Finding("ERROR", FORMAL_REGISTRY, f"{section} must be a list"))
            continue
        for item in value:
            if not isinstance(item, dict):
                continue
            oid = str(item.get("obligation_id", "<missing>"))
            if item.get("proof_claimed") is not False:
                findings.append(Finding("ERROR", FORMAL_REGISTRY, f"{oid}: proof_claimed must remain false"))
            if item.get("proof_artifact") not in {None, ""}:
                findings.append(Finding("ERROR", FORMAL_REGISTRY, f"{oid}: proof_artifact must be empty until reviewed proof exists"))


def _scan_text(findings: list[Finding]) -> None:
    for path in text_files(SCAN_ROOTS):
        safe_until = 0
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            lower = line.lower()
            if any(marker in lower for marker in SAFE_BLOCK_MARKERS):
                safe_until = lineno + 35
            if not any(pattern.search(line) for pattern in OVERCLAIM_PATTERNS):
                continue
            if _safe_line(line, lineno <= safe_until):
                continue
            findings.append(Finding("ERROR", path, f"possible proof overclaim: {line.strip()}", lineno))


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    _check_registry(findings)
    _scan_text(findings)

    return emit(findings, args.mode, "No proof overclaim check OK")


if __name__ == "__main__":
    raise SystemExit(main())
