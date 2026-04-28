#!/usr/bin/env python3
"""Validate Phase 0.9 fuzz corpus planning artifacts."""

from __future__ import annotations

import sys

from mfos_phase09 import FUZZ_PLAN, FUZZ_RE, as_list, load_yaml, rel


REQUIRED_TARGETS = {
    "dsn-parser",
    "job-control-stream-parser",
    "operator-command-parser",
    "policy-language-parser",
    "audit-record-decoder",
    "dataset-handle-decoder",
    "job-fixture-parser",
    "spool-fixture-parser",
    "semantic-fixture-parser",
}


def main() -> int:
    errors: list[str] = []
    if not FUZZ_PLAN.exists():
        errors.append(f"missing fuzz corpus plan: {rel(FUZZ_PLAN)}")
    else:
        data = load_yaml(FUZZ_PLAN)
        if data.get("phase") != "0.9":
            errors.append(f"{rel(FUZZ_PLAN)}: phase must be '0.9'")
        if data.get("implementation_allowed") is not False:
            errors.append(f"{rel(FUZZ_PLAN)}: implementation_allowed must be false")
        targets = as_list(data.get("targets"))
        seen: set[str] = set()
        for target in targets:
            if not isinstance(target, dict):
                errors.append(f"{rel(FUZZ_PLAN)}: target entry must be mapping")
                continue
            target_id = str(target.get("target_id", "<missing>"))
            target_name = str(target.get("target_name", "<missing>"))
            seen.add(target_name)
            if not FUZZ_RE.match(target_id):
                errors.append(f"{rel(FUZZ_PLAN)}:{target_id}: invalid target_id namespace")
            if not as_list(target.get("corpus_categories")):
                errors.append(f"{rel(FUZZ_PLAN)}:{target_id}: corpus_categories must be non-empty")
            if not target.get("corpus_path"):
                errors.append(f"{rel(FUZZ_PLAN)}:{target_id}: corpus_path required")
            if target.get("phase_to_implement") == "Phase 0.9":
                errors.append(f"{rel(FUZZ_PLAN)}:{target_id}: Phase 0.9 must not implement fuzz target")
            if target.get("implementation_allowed") is not False:
                errors.append(f"{rel(FUZZ_PLAN)}:{target_id}: implementation_allowed must be false")
        missing = sorted(REQUIRED_TARGETS - seen)
        if missing:
            errors.append(f"{rel(FUZZ_PLAN)}: missing required targets: {', '.join(missing)}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Phase 0.9 fuzz corpus plan validation OK: {len(load_yaml(FUZZ_PLAN).get('targets', []))} targets checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
