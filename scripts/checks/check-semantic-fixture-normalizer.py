#!/usr/bin/env python3
"""Check that Phase 1 fixture normalizer tooling stays metadata-only."""

from __future__ import annotations

from pathlib import Path
import re
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, mode_arg


TOOL_ROOTS = [
    ROOT / "tools" / "semantic-fixture-normalizer",
    ROOT / "tools" / "dafny-conformance-harness",
]
BUSINESS_LOGIC = re.compile(
    r"\b(?:authorize|authenticate|decide|evaluate_policy|schedule|dispatch|allocate|mount|open_dataset|execute_job|run_step|purge_spool|browse_spool|create_dataset_handle|create_handle|resolve_catalog|commit_catalog|rollback_catalog|transition_job|job_lifecycle|operator_authorized|operator_authority|execute_command|audit_before_return|audit_obligation)\s*\(",
    re.IGNORECASE,
)
BUSINESS_MARKERS = re.compile(
    r"\b(?:ALLOW|DENY|ALLOW_WITH_AUDIT|REQUIRE_DUAL_CONTROL|REQUIRE_OPERATOR_CONFIRMATION|MFOS_ERR_POLICY_DENIED|MFOS_ERR_SPEC_GAP|MFOS_ERR_UNSUPPORTED|DATASET_READ_NOT_PERMITTED|OPEN_DENY|CATALOG_COMMITTED|CATALOG_ROLLED_BACK|CATALOG_INTEGRITY_FAILED|dataset_handle_created|audit_before_final_result|JOB_STATE_[A-Z0-9_]*|COMMAND_STATE_[A-Z0-9_]*)\b"
)
HOSTED = re.compile(r"\b(?:HTTPServer|socketserver|serve_forever|listen|bind|uvicorn|flask|fastapi)\b")


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []
    for root in TOOL_ROOTS:
        if not root.exists():
            findings.append(Finding("ERROR", root, "required Phase 1 tool directory missing"))
            continue
        for path in sorted(root.rglob("*.py")):
            for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if BUSINESS_LOGIC.search(line):
                    findings.append(Finding("ERROR", path, "normalizer/harness must not encode MFOS business semantics", lineno))
                if BUSINESS_MARKERS.search(line):
                    findings.append(Finding("ERROR", path, "normalizer/harness must not hardcode MFOS business decision markers", lineno))
                if HOSTED.search(line):
                    findings.append(Finding("ERROR", path, "normalizer/harness must not implement hosted daemon behavior", lineno))
    return emit(findings, args.mode, "Semantic fixture normalizer boundary check OK")


if __name__ == "__main__":
    raise SystemExit(main())
