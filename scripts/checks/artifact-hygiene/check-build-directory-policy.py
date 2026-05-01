#!/usr/bin/env python3
"""Ensure build/ stays metadata-only and cannot commit generated outputs."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, mode_arg


BUILD_ROOT = ROOT / "build"
BUILD_GITIGNORE = BUILD_ROOT / ".gitignore"
ALLOWED_TRACKED_BUILD_FILES = {
    Path("build/.gitignore"),
    Path("build/.mfos-dir.yml"),
    Path("build/README.md"),
    Path("build/index.yml"),
}
REQUIRED_GITIGNORE_PATTERNS = {
    "*",
    "!/.gitignore",
    "!/.mfos-dir.yml",
    "!/README.md",
    "!/index.yml",
}
DENIED_OUTPUT_PREFIXES = {
    Path("build/cache"),
    Path("build/hardware-lab"),
    Path("build/images"),
    Path("build/out"),
    Path("build/profiles"),
    Path("build/qemu"),
    Path("build/tmp"),
    Path("build/toolchains"),
}


def tracked_build_paths() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--", "build"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise SystemExit(f"git ls-files failed: {result.stderr.strip()}")
    return [Path(line) for line in result.stdout.splitlines() if line.strip()]


def is_under(path: Path, prefix: Path) -> bool:
    return path == prefix or prefix in path.parents


def gitignore_patterns() -> set[str]:
    if not BUILD_GITIGNORE.exists():
        return set()
    return {
        line.strip()
        for line in BUILD_GITIGNORE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    if not BUILD_ROOT.is_dir():
        findings.append(Finding("ERROR", BUILD_ROOT, "build/ metadata root is missing"))
        return emit(findings, args.mode, "Build directory policy check OK")

    patterns = gitignore_patterns()
    if not patterns:
        findings.append(Finding("ERROR", BUILD_GITIGNORE, "build/.gitignore must exist and deny generated outputs by default"))
    else:
        missing = sorted(REQUIRED_GITIGNORE_PATTERNS - patterns)
        if missing:
            findings.append(Finding("ERROR", BUILD_GITIGNORE, f"missing required build/.gitignore patterns: {', '.join(missing)}"))

    for rel in tracked_build_paths():
        if rel in ALLOWED_TRACKED_BUILD_FILES:
            continue
        denied_prefix = next((prefix for prefix in sorted(DENIED_OUTPUT_PREFIXES) if is_under(rel, prefix)), None)
        if denied_prefix is not None:
            findings.append(Finding("ERROR", ROOT / rel, f"tracked build output path is forbidden under {denied_prefix}"))
        else:
            findings.append(Finding("ERROR", ROOT / rel, "tracked build file is outside the metadata-only allowlist"))

    return emit(findings, args.mode, "Build directory policy check OK")


if __name__ == "__main__":
    raise SystemExit(main())
