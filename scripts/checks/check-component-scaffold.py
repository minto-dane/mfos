#!/usr/bin/env python3
"""Validate MFOS component scaffold metadata."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPT_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "lib").is_dir()), None)
if _SCRIPT_ROOT is not None and str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from lib.mfos_lint import Finding, ROOT, emit, load_yaml, mode_arg


REQUIRED_METADATA_DIRS = [
    Path("ai"),
    Path("ci"),
    Path("claims"),
    Path("docs/design/source-matrix"),
    Path("docs/design/specs"),
    Path("evidence/traceability"),
    Path("formal"),
    Path("formal/executable-semantics/dafny"),
    Path("formal/models"),
    Path("formal/models/alloy"),
    Path("formal/models/tla"),
    Path("fuzz"),
    Path("guard"),
    Path("implementation"),
    Path("nucleus"),
    Path("packs"),
    Path("pxm"),
    Path("requirements"),
    Path("requirements/by-domain"),
    Path("schemas"),
    Path("schemas/mfos"),
    Path("scripts"),
    Path("reports/current"),
    Path("services"),
    Path("source-matrix"),
    Path("sources"),
    Path("specs"),
    Path("tests/catalog"),
    Path("tests/fixtures"),
    Path("tests/golden"),
]

REQUIRED_FIELDS = {
    "directory_id",
    "path",
    "role",
    "maturity",
    "status",
    "canonical",
    "description",
    "implementation_allowed",
    "phase_allowed_from",
    "depends_on",
    "allowed_contents",
    "forbidden_contents",
    "required_before_agent_assignment",
    "review_status",
}

VALID_ROLES = {
    "ai_work",
    "bridge",
    "canonical_current",
    "canonical_registry",
    "generated",
    "implementation_future",
    "planned",
    "formal_model_scaffold",
    "test_current",
    "validation",
}

VALID_MATURITY = {
    "M1_PLACEHOLDER",
    "M2_CLASSIFIED",
    "M3_CONTRACTED",
    "M4_POPULATED",
    "M5_VALIDATED",
    "M6_FROZEN",
    "M7_ARCHIVED",
}

VALID_STATUS = {
    "current",
    "draft",
    "planned",
    "bridge",
    "generated",
    "historical",
    "conditional",
}

FORBIDDEN_IMPLEMENTATION_FLAGS = {
    "production",
    "hosted_daemon",
    "semantic_runner",
    "portable_semantic_core",
    "hosted_semantic_prototype",
    "rust_semantic_core",
    "generated_production_code",
}

BOOLEAN_IMPLEMENTATION_FLAGS = FORBIDDEN_IMPLEMENTATION_FLAGS | {
    "validation_only",
}

REQUIRED_IMPLEMENTATION_FLAGS = {
    "production",
    "hosted_daemon",
    "rust_semantic_core",
    "dafny_executable_semantics",
    "semantic_runner",
    "generated_production_code",
    "validation_only",
}


def _as_list(value: object) -> list[object]:
    return value if isinstance(value, list) else []


def _validate_metadata(path: Path, expected_dir: Path | None, findings: list[Finding]) -> None:
    data = load_yaml(path)
    if not isinstance(data, dict):
        findings.append(Finding("ERROR", path, "component scaffold metadata must be a mapping"))
        return

    missing = sorted(REQUIRED_FIELDS - set(data))
    if missing:
        findings.append(Finding("ERROR", path, f"missing required fields: {', '.join(missing)}"))

    declared_path = data.get("path")
    if not isinstance(declared_path, str) or not declared_path:
        findings.append(Finding("ERROR", path, "path must be a non-empty string"))
    elif expected_dir is not None and Path(declared_path) != expected_dir:
        findings.append(Finding("ERROR", path, f"path field {declared_path!r} does not match {expected_dir}"))
    elif not (ROOT / declared_path).exists():
        findings.append(Finding("ERROR", path, f"path field points at missing directory: {declared_path}"))

    directory_id = data.get("directory_id")
    if not isinstance(directory_id, str) or not directory_id.startswith("MFOS-DIR-"):
        findings.append(Finding("ERROR", path, "directory_id must start with MFOS-DIR-"))

    role = data.get("role")
    if role not in VALID_ROLES:
        findings.append(Finding("ERROR", path, f"invalid role: {role!r}"))

    maturity = data.get("maturity")
    if maturity not in VALID_MATURITY:
        findings.append(Finding("ERROR", path, f"invalid maturity: {maturity!r}"))

    status = data.get("status")
    if status not in VALID_STATUS:
        findings.append(Finding("ERROR", path, f"invalid status: {status!r}"))

    if not isinstance(data.get("canonical"), bool):
        findings.append(Finding("ERROR", path, "canonical must be a boolean"))

    for field in ("depends_on", "allowed_contents", "forbidden_contents", "required_before_agent_assignment"):
        if not isinstance(data.get(field), list):
            findings.append(Finding("ERROR", path, f"{field} must be a list"))

    implementation_allowed = data.get("implementation_allowed")
    if not isinstance(implementation_allowed, dict):
        findings.append(Finding("ERROR", path, "implementation_allowed must be a mapping"))
        return

    for flag in sorted(REQUIRED_IMPLEMENTATION_FLAGS):
        if flag not in implementation_allowed:
            findings.append(Finding("ERROR", path, f"implementation_allowed.{flag} is required"))
    for flag in FORBIDDEN_IMPLEMENTATION_FLAGS:
        if implementation_allowed.get(flag) is True:
            findings.append(Finding("ERROR", path, f"implementation_allowed.{flag} must not be true in Phase 0.x"))
    if implementation_allowed.get("dafny_executable_semantics") is True and data.get("path") != "formal/executable-semantics/dafny":
        findings.append(
            Finding(
                "ERROR",
                path,
                "implementation_allowed.dafny_executable_semantics may be true only for formal/executable-semantics/dafny",
            )
        )
    for flag in sorted(BOOLEAN_IMPLEMENTATION_FLAGS):
        if flag in implementation_allowed and not isinstance(implementation_allowed.get(flag), bool):
            findings.append(Finding("ERROR", path, f"implementation_allowed.{flag} must be boolean when present"))

    if data.get("role") == "implementation_future" and "implementation code" not in _as_list(data.get("forbidden_contents")):
        findings.append(Finding("WARN", path, "future implementation scaffolds should forbid implementation code explicitly"))


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()
    findings: list[Finding] = []

    for directory in REQUIRED_METADATA_DIRS:
        full = ROOT / directory
        metadata = full / ".mfos-dir.yml"
        if not full.exists():
            findings.append(Finding("ERROR", full, "required scaffold directory missing"))
            continue
        if not metadata.exists():
            findings.append(Finding("ERROR", metadata, "required .mfos-dir.yml missing"))
            continue
        _validate_metadata(metadata, directory, findings)

    for metadata in sorted(ROOT.rglob(".mfos-dir.yml")):
        rel_dir = metadata.parent.relative_to(ROOT)
        if rel_dir not in REQUIRED_METADATA_DIRS:
            _validate_metadata(metadata, None, findings)

    return emit(findings, args.mode, "Component scaffold metadata check OK")


if __name__ == "__main__":
    raise SystemExit(main())
