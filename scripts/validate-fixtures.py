#!/usr/bin/env python3
"""Validate Phase 0.9 conformance fixture YAML artifacts."""

from __future__ import annotations

import sys

from mfos_phase09 import (
    FIXTURE_DIR,
    FIXTURE_RE,
    HOST_SEMANTICS,
    WALL_CLOCK,
    as_list,
    load_yaml,
    rel,
    text_of,
    yaml_files,
)


REQUIRED = {
    "fixture_id",
    "fixture_version",
    "description",
    "target_specs",
    "target_requirements",
    "preconditions",
    "initial_state",
    "inputs",
    "expected_oracle",
    "expected_evidence",
    "not_allowed",
    "status",
}
NOT_ALLOWED = {"production_claim", "external_compatibility_claim", "host_os_semantics_dependency"}


def main() -> int:
    errors: list[str] = []
    files = yaml_files(FIXTURE_DIR)
    if not files:
        errors.append(f"missing fixtures under {rel(FIXTURE_DIR)}")
    for path in files:
        text = text_of(path)
        if HOST_SEMANTICS.search(text):
            errors.append(f"{rel(path)}: fixture contains host OS semantics")
        if WALL_CLOCK.search(text):
            errors.append(f"{rel(path)}: fixture contains wall-clock timestamp")
        data = load_yaml(path)
        if not isinstance(data, dict):
            errors.append(f"{rel(path)}: fixture must be a mapping")
            continue
        fixture_id = str(data.get("fixture_id", "<missing>"))
        missing = sorted(REQUIRED - set(data))
        if missing:
            errors.append(f"{rel(path)}:{fixture_id}: missing fields: {', '.join(missing)}")
        if not FIXTURE_RE.match(fixture_id):
            errors.append(f"{rel(path)}:{fixture_id}: invalid fixture_id namespace")
        not_allowed = set(str(item) for item in as_list(data.get("not_allowed")))
        missing_not_allowed = sorted(NOT_ALLOWED - not_allowed)
        if missing_not_allowed:
            errors.append(f"{rel(path)}:{fixture_id}: not_allowed missing {', '.join(missing_not_allowed)}")
        if not as_list(data.get("target_requirements")):
            errors.append(f"{rel(path)}:{fixture_id}: target_requirements must be non-empty")
        if not data.get("expected_oracle"):
            errors.append(f"{rel(path)}:{fixture_id}: expected_oracle is required")
        if not as_list(data.get("expected_evidence")):
            errors.append(f"{rel(path)}:{fixture_id}: expected_evidence must be non-empty")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Phase 0.9 fixture validation OK: {len(files)} fixtures checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
