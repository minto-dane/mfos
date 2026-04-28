#!/usr/bin/env python3
"""Validate the current v0.5 machine-readable requirements catalog."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

import sys
from pathlib import Path

import yaml


SOURCE_INDEX = Path("docs/design/source-matrix/source-matrix.yml")
REQUIREMENTS = Path("docs/design/registries/requirements.yaml")

REQUIRED_ENTRY_FIELDS = {
    "requirement_id",
    "title",
    "normative_text",
    "source_refs",
    "profile_applicability",
    "target_components",
    "verification",
    "audit_obligation",
    "failure_mode",
    "evidence_required",
    "status",
}

PROFILE_KEYS = {
    "baseline",
    "enterprise_standalone",
    "enterprise_pxm",
    "high_assurance",
}

PRIORITY_IDS = {
    "MFOS-REQ-CATALOG-0002",
    "MFOS-REQ-AUDIT-0002",
    "MFOS-REQ-AUDIT-0005",
    "MFOS-REQ-AUTH-0001",
    "MFOS-REQ-AUTH-0002",
    "MFOS-REQ-AUTH-0004",
    "MFOS-REQ-DATASET-0001",
    "MFOS-REQ-DATASET-0002",
    "MFOS-REQ-DATASET-0006",
    "MFOS-REQ-UPDATE-0004",
    "MFOS-REQ-UPDATE-0005",
    "MFOS-REQ-UPDATE-0006",
    "MFOS-REQ-PARTITION-0005",
    "MFOS-REQ-PARTITION-0006",
    "MFOS-REQ-PARTITION-0016",
    "MFOS-REQ-PARTITION-0017",
    "MFOS-REQ-AMF-0021",
    "MFOS-REQ-NUCLEUS-0008",
    "MFOS-REQ-PROFILE-0001",
}


def load_yaml(path: Path) -> object:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - CLI error path
        raise SystemExit(f"YAML parse failed: {path}: {exc}") from exc


def main() -> int:
    source_index = load_yaml(SOURCE_INDEX)
    requirements = load_yaml(REQUIREMENTS)
    errors: list[str] = []

    if not isinstance(source_index, dict):
        print("source index is not a mapping", file=sys.stderr)
        return 1
    source_ids = {
        item.get("source_id")
        for item in source_index.get("cards", [])
        if isinstance(item, dict) and item.get("source_id")
    }

    if not isinstance(requirements, dict):
        print("requirements catalog is not a mapping", file=sys.stderr)
        return 1

    entries = requirements.get("entries")
    if not isinstance(entries, list) or not entries:
        print("requirements catalog has no entries", file=sys.stderr)
        return 1

    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("catalog contains non-mapping requirement entry")
            continue

        requirement_id = entry.get("requirement_id", "<missing-id>")
        if requirement_id in seen:
            errors.append(f"duplicate requirement_id: {requirement_id}")
        seen.add(requirement_id)

        missing = sorted(field for field in REQUIRED_ENTRY_FIELDS if field not in entry)
        if missing:
            errors.append(f"{requirement_id}: missing fields: {', '.join(missing)}")

        profile = entry.get("profile_applicability")
        if not isinstance(profile, dict):
            errors.append(f"{requirement_id}: profile_applicability must be a mapping")
        else:
            keys = set(profile)
            if keys != PROFILE_KEYS:
                errors.append(
                    f"{requirement_id}: profile keys mismatch: missing={sorted(PROFILE_KEYS - keys)} extra={sorted(keys - PROFILE_KEYS)}"
                )

        source_refs = entry.get("source_refs")
        if not isinstance(source_refs, list) or not source_refs:
            errors.append(f"{requirement_id}: source_refs must be a non-empty list")
        else:
            for ref in source_refs:
                if not isinstance(ref, dict):
                    errors.append(f"{requirement_id}: source_refs item is not a mapping")
                    continue
                source_id = ref.get("source_id")
                if source_id not in source_ids:
                    errors.append(f"{requirement_id}: unresolved source_id: {source_id}")
                if not ref.get("source_type"):
                    errors.append(f"{requirement_id}: source_ref lacks source_type")
                if not ref.get("role"):
                    errors.append(f"{requirement_id}: source_ref lacks role")

        audit = entry.get("audit_obligation")
        if not isinstance(audit, dict):
            errors.append(f"{requirement_id}: audit_obligation must be a mapping")
        elif not audit.get("obligation"):
            errors.append(f"{requirement_id}: audit_obligation lacks obligation")

        failure = entry.get("failure_mode")
        if not isinstance(failure, dict):
            errors.append(f"{requirement_id}: failure_mode must be a mapping")
        elif "fail_closed" not in failure:
            errors.append(f"{requirement_id}: failure_mode lacks fail_closed")

    missing_priority = sorted(PRIORITY_IDS - seen)
    if missing_priority:
        errors.append(f"missing v0.5 priority requirements: {', '.join(missing_priority)}")

    if errors:
        print("Requirement validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Requirement validation OK: {len(entries)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
