#!/usr/bin/env python3
"""Reject non-current lifecycle metadata inside reports/current packages."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg


CURRENT_ROOT = ROOT / "reports/current"
CURRENT_INDEX = CURRENT_ROOT / "index.yml"
METADATA_FILENAMES = {"README.md", "index.yml", ".mfos-dir.yml"}
LIFECYCLE_KEYS = {
    "artifact_lifecycle",
    "artifact_status",
    "lifecycle",
    "lifecycle_status",
    "phase_status",
    "status",
}
FORBIDDEN_WORD_RE = re.compile(r"\b(?:archive|archived|superseded|generated|historical)\b")
FORBIDDEN_PHRASES = ("phase-specific", "phase specific", "migration-only", "migration only")
PHASE_NAME_RE = re.compile(r"\b(?:pre[-_]?phase[-_]?\d+|phase[-_]\d+(?:[-_.]\d+)*)\b", re.IGNORECASE)
MARKDOWN_STATUS_RE = re.compile(r"^\s*Status:\s*(.+?)\s*$", re.IGNORECASE)


def list_domain_paths(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return []
    items = value.get("domains")
    if not isinstance(items, list):
        return []
    return [
        str(item["path"]).rstrip("/")
        for item in items
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    ]


def forbidden_lifecycle_reason(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    lowered = value.strip().lower().replace("_", "-")
    compact = re.sub(r"\s+", " ", lowered)
    if FORBIDDEN_WORD_RE.search(compact):
        return value
    if any(phrase in compact for phrase in FORBIDDEN_PHRASES):
        return value
    if PHASE_NAME_RE.search(value):
        return value
    return None


def yaml_top(path: Path) -> dict[str, Any]:
    if path.suffix not in {".yml", ".yaml"}:
        return {}
    data = load_yaml(path)
    return data if isinstance(data, dict) else {}


def markdown_status(path: Path) -> str | None:
    if path.suffix != ".md":
        return None
    for line in path.read_text(encoding="utf-8").splitlines()[:20]:
        match = MARKDOWN_STATUS_RE.match(line)
        if match:
            return match.group(1)
    return None


def check_mapping_lifecycle(path: Path, data: dict[str, Any], findings: list[Finding], context: str) -> None:
    for key in sorted(LIFECYCLE_KEYS):
        if key not in data:
            continue
        reason = forbidden_lifecycle_reason(data[key])
        if reason is not None:
            findings.append(Finding("ERROR", path, f"{context} has forbidden current lifecycle metadata {key}: {reason}"))


def check_domain_index(index_path: Path, findings: list[Finding]) -> None:
    data = load_yaml(index_path)
    if not isinstance(data, dict):
        findings.append(Finding("ERROR", index_path, "reports/current domain index must be a mapping"))
        return
    check_mapping_lifecycle(index_path, data, findings, "domain index")
    policy = data.get("policy")
    if isinstance(policy, dict):
        check_mapping_lifecycle(index_path, policy, findings, "domain index policy")
    artifacts = data.get("artifacts")
    if not isinstance(artifacts, list):
        return
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        artifact_path = str(artifact.get("path") or "<unknown>")
        check_mapping_lifecycle(index_path, artifact, findings, f"domain index entry {artifact_path}")


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []
    current_data = load_yaml(CURRENT_INDEX) if CURRENT_INDEX.exists() else {}
    if isinstance(current_data, dict):
        check_mapping_lifecycle(CURRENT_INDEX, current_data, findings, "reports/current index")
        root_artifacts = current_data.get("root_artifacts")
        if isinstance(root_artifacts, list):
            for artifact in root_artifacts:
                if not isinstance(artifact, dict):
                    continue
                artifact_path = str(artifact.get("path") or "<unknown>")
                check_mapping_lifecycle(CURRENT_INDEX, artifact, findings, f"reports/current root artifact entry {artifact_path}")

    for domain in list_domain_paths(current_data):
        index_path = ROOT / domain / "index.yml"
        if index_path.exists():
            check_domain_index(index_path, findings)

    for path in sorted(CURRENT_ROOT.rglob("*") if CURRENT_ROOT.exists() else []):
        if not path.is_file() or path.name in METADATA_FILENAMES:
            continue
        check_mapping_lifecycle(path, yaml_top(path), findings, "reports/current artifact")
        status = markdown_status(path)
        reason = forbidden_lifecycle_reason(status) if status is not None else None
        if reason is not None:
            findings.append(Finding("ERROR", path, f"reports/current Markdown status has forbidden lifecycle metadata: {reason}"))

    return emit(findings, args.mode, "Reports/current lifecycle metadata check OK")


if __name__ == "__main__":
    raise SystemExit(main())
