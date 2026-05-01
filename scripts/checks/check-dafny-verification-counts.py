#!/usr/bin/env python3
"""Check recorded current Dafny verification counts against verifier output."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, mode_arg


COUNT_RE = re.compile(r"(?P<count>[0-9]+) verified, (?P<errors>[0-9]+) errors")
SUMMARY_RE = re.compile(r"Dafny program verifier finished with (?P<count>[0-9]+) verified, (?P<errors>[0-9]+) errors")

CURRENT_COUNT_PATHS = [
    ROOT / "docs/design/STATUS.md",
    ROOT / "docs/design/specs/43-dafny-executable-semantics-policy.md",
    ROOT / "formal/executable-semantics/dafny/README.md",
    ROOT / "reports/generated/phase-1-3/dafny-dataset-catalog-validation-report.md",
    ROOT / "reports/current/dafny/dafny-semantics-report.md",
    ROOT / "reports/current/dafny/dafny-semantics-validation-report.md",
    ROOT / "reports/current/dafny/dafny-verification-report.md",
    ROOT / "reports/current/readiness/post-merge-integration-sweep-report.md",
    ROOT / "reports/generated/phase-1-1/semantic-coverage-report.md",
    ROOT / "reports/generated/phase-1-1/semantic-coverage.yml",
    ROOT / "scripts/generators/generate-dataset-catalog-coverage.py",
    ROOT / "scripts/generators/generate-semantic-coverage.py",
]

HISTORICAL_ALLOWLIST = [
    (ROOT / "docs/design/specs/43-dafny-executable-semantics-policy.md", 49),
    (ROOT / "docs/design/specs/43-dafny-executable-semantics-policy.md", 97),
    (ROOT / "reports/archive/pr-reviews/pr-19-review-report.md", 97),
    (ROOT / "reports/archive/pr-reviews/pr-19-post-pr21-review-report.md", 97),
    (ROOT / "reports/archive/pr-reviews/pr-19-pr-20-dependency-closure-report.md", 97),
    (ROOT / "reports/generated/phase-1-2/dafny-authorization-audit-validation-report.md", 97),
    (ROOT / "scripts/generators/generate-auth-audit-coverage.py", 97),
]


def parse_summary(path: Path) -> tuple[int, int] | None:
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        match = SUMMARY_RE.search(line)
        if match:
            return int(match.group("count")), int(match.group("errors"))
    return None


def allowed_historical(path: Path, count: int) -> bool:
    return any(path == allowed_path and count == allowed_count for allowed_path, allowed_count in HISTORICAL_ALLOWLIST)


def validate_recorded_counts(actual_count: int, actual_errors: int) -> list[Finding]:
    findings: list[Finding] = []
    if actual_errors != 0:
        findings.append(Finding("ERROR", ROOT, f"Dafny verifier reported nonzero errors: {actual_errors}"))
        return findings

    paths = set(CURRENT_COUNT_PATHS) | {path for path, _ in HISTORICAL_ALLOWLIST}
    for path in sorted(paths):
        if not path.exists():
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for match in COUNT_RE.finditer(line):
                count = int(match.group("count"))
                errors = int(match.group("errors"))
                if errors != 0:
                    findings.append(Finding("ERROR", path, f"line {lineno}: recorded Dafny error count is nonzero"))
                    continue
                if count == actual_count:
                    continue
                if allowed_historical(path, count):
                    continue
                findings.append(
                    Finding(
                        "ERROR",
                        path,
                        f"line {lineno}: recorded Dafny count {count} does not match verifier count {actual_count}",
                    )
                )
    return findings


def main() -> int:
    parser = mode_arg()
    parser.add_argument("--dafny-output", required=True, type=Path)
    args = parser.parse_args()

    summary = parse_summary(args.dafny_output)
    if summary is None:
        return emit([Finding("ERROR", args.dafny_output, "Dafny verification summary line missing")], args.mode, "Dafny verification count check OK")

    findings = validate_recorded_counts(*summary)
    return emit(findings, args.mode, "Dafny verification count check OK")


if __name__ == "__main__":
    raise SystemExit(main())
