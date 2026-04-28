#!/usr/bin/env python3
"""Validate cross-registry links between requirements, tests, evidence, and claims."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Iterable

from mfos_lint import (
    EVIDENCE,
    EVID_ID_RE,
    Finding,
    REQUIREMENTS,
    ROOT,
    TESTS,
    TEST_ID_RE,
    emit,
    load_yaml,
    mode_arg,
)


CLAIM_TREE = ROOT / "docs/design/assurance/claim-tree.yml"
REPORT = ROOT / "reports/registry-link-audit.md"


def collect_matching_ids(value: object, pattern) -> list[str]:
    """Collect registry IDs from nested registry values without assuming shape."""

    found: list[str] = []
    if isinstance(value, str):
        found.extend(pattern.findall(value))
    elif isinstance(value, dict):
        for item in value.values():
            found.extend(collect_matching_ids(item, pattern))
    elif isinstance(value, list):
        for item in value:
            found.extend(collect_matching_ids(item, pattern))
    return found


def registry(path: Path, key: str) -> tuple[list[dict[str, object]], set[str], list[Finding]]:
    findings: list[Finding] = []
    if not path.exists():
        findings.append(Finding("ERROR", path, "registry missing"))
        return [], set(), findings
    data = load_yaml(path)
    if not isinstance(data, dict):
        findings.append(Finding("ERROR", path, "registry must be a mapping"))
        return [], set(), findings
    entries = data.get("entries")
    if not isinstance(entries, list):
        findings.append(Finding("ERROR", path, "registry entries must be a list"))
        return [], set(), findings

    seen: set[str] = set()
    duplicate_ids: set[str] = set()
    normalized: list[dict[str, object]] = []
    for idx, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            findings.append(Finding("ERROR", path, f"entry #{idx} is not a mapping"))
            continue
        item_id = entry.get(key)
        if not isinstance(item_id, str) or not item_id:
            findings.append(Finding("ERROR", path, f"entry #{idx} missing {key}"))
            continue
        if item_id in seen:
            duplicate_ids.add(item_id)
        seen.add(item_id)
        normalized.append(entry)

    for item_id in sorted(duplicate_ids):
        findings.append(Finding("ERROR", path, f"duplicate {key}: {item_id}"))
    return normalized, seen, findings


def claims() -> tuple[list[dict[str, object]], list[Finding]]:
    findings: list[Finding] = []
    if not CLAIM_TREE.exists():
        findings.append(Finding("ERROR", CLAIM_TREE, "claim tree missing"))
        return [], findings
    data = load_yaml(CLAIM_TREE)
    if not isinstance(data, dict):
        findings.append(Finding("ERROR", CLAIM_TREE, "claim tree must be a mapping"))
        return [], findings
    entries = data.get("claims")
    if not isinstance(entries, list):
        findings.append(Finding("ERROR", CLAIM_TREE, "claims must be a list"))
        return [], findings
    normalized: list[dict[str, object]] = []
    for idx, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            findings.append(Finding("ERROR", CLAIM_TREE, f"claim #{idx} is not a mapping"))
            continue
        if not isinstance(entry.get("claim_id"), str):
            findings.append(Finding("ERROR", CLAIM_TREE, f"claim #{idx} missing claim_id"))
            continue
        normalized.append(entry)
    return normalized, findings


def missing_links(
    owner_id: str,
    owner_path: Path,
    field: str,
    refs: Iterable[str],
    known: set[str],
) -> list[Finding]:
    findings: list[Finding] = []
    for ref in sorted(set(refs)):
        if ref not in known:
            findings.append(Finding("WARN", owner_path, f"{owner_id}: {field} references missing registry ID: {ref}"))
    return findings


def build_report(
    requirement_count: int,
    test_count: int,
    evidence_count: int,
    claim_count: int,
    req_test_missing: dict[str, list[str]],
    req_evidence_missing: dict[str, list[str]],
    claim_test_missing: dict[str, list[str]],
    claim_evidence_missing: dict[str, list[str]],
) -> str:
    def section(title: str, values: dict[str, list[str]]) -> list[str]:
        lines = [f"## {title}", ""]
        if not values:
            lines.append("No missing links.")
            lines.append("")
            return lines
        for owner in sorted(values):
            refs = sorted(set(values[owner]))
            lines.append(f"- `{owner}`")
            for ref in refs:
                lines.append(f"  - `{ref}`")
        lines.append("")
        return lines

    total_missing = (
        sum(len(set(v)) for v in req_test_missing.values())
        + sum(len(set(v)) for v in req_evidence_missing.values())
        + sum(len(set(v)) for v in claim_test_missing.values())
        + sum(len(set(v)) for v in claim_evidence_missing.values())
    )

    lines = [
        "# Registry Link Audit",
        "",
        "This report is generated from the current registry contents. It does not claim that draft evidence exists as verified proof.",
        "",
        "## Summary",
        "",
        f"- Requirements: `{requirement_count}`",
        f"- Tests: `{test_count}`",
        f"- Evidence records: `{evidence_count}`",
        f"- Claims: `{claim_count}`",
        f"- Missing cross-registry links: `{total_missing}`",
        "",
        "Draft-mode validation reports missing links as warnings. Release-mode validation treats warnings as failures.",
        "",
    ]
    lines.extend(section("Requirement Test Links Missing From tests.yaml", req_test_missing))
    lines.extend(section("Requirement Evidence Links Missing From evidence.yaml", req_evidence_missing))
    lines.extend(section("Claim Test Links Missing From tests.yaml", claim_test_missing))
    lines.extend(section("Claim Evidence Links Missing From evidence.yaml", claim_evidence_missing))
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = mode_arg()
    args = parser.parse_args()

    findings: list[Finding] = []
    req_entries, _, req_findings = registry(REQUIREMENTS, "requirement_id")
    test_entries, known_tests, test_findings = registry(TESTS, "test_id")
    evidence_entries, known_evidence, evidence_findings = registry(EVIDENCE, "evidence_id")
    claim_entries, claim_findings = claims()
    findings.extend(req_findings)
    findings.extend(test_findings)
    findings.extend(evidence_findings)
    findings.extend(claim_findings)

    req_test_missing: dict[str, list[str]] = defaultdict(list)
    req_evidence_missing: dict[str, list[str]] = defaultdict(list)
    claim_test_missing: dict[str, list[str]] = defaultdict(list)
    claim_evidence_missing: dict[str, list[str]] = defaultdict(list)

    for requirement in req_entries:
        rid = str(requirement["requirement_id"])
        verification = requirement.get("verification", {})
        tests = verification.get("tests", {}) if isinstance(verification, dict) else {}
        for finding in missing_links(rid, REQUIREMENTS, "verification.tests", collect_matching_ids(tests, TEST_ID_RE), known_tests):
            findings.append(finding)
            ref = finding.message.rsplit(": ", 1)[-1]
            req_test_missing[rid].append(ref)

        evidence_required = requirement.get("evidence_required", [])
        for finding in missing_links(rid, REQUIREMENTS, "evidence_required", collect_matching_ids(evidence_required, EVID_ID_RE), known_evidence):
            findings.append(finding)
            ref = finding.message.rsplit(": ", 1)[-1]
            req_evidence_missing[rid].append(ref)

    for claim in claim_entries:
        cid = str(claim["claim_id"])
        claim_tests = claim.get("tests", [])
        if isinstance(claim_tests, list):
            test_refs = [item for item in claim_tests if isinstance(item, str)]
        else:
            test_refs = collect_matching_ids(claim_tests, TEST_ID_RE)
        for finding in missing_links(cid, CLAIM_TREE, "tests", test_refs, known_tests):
            findings.append(finding)
            ref = finding.message.rsplit(": ", 1)[-1]
            claim_test_missing[cid].append(ref)

        claim_evidence = claim.get("evidence", [])
        if isinstance(claim_evidence, list):
            evidence_refs = [item for item in claim_evidence if isinstance(item, str)]
        else:
            evidence_refs = collect_matching_ids(claim_evidence, EVID_ID_RE)
        for finding in missing_links(cid, CLAIM_TREE, "evidence", evidence_refs, known_evidence):
            findings.append(finding)
            ref = finding.message.rsplit(": ", 1)[-1]
            claim_evidence_missing[cid].append(ref)

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        build_report(
            requirement_count=len(req_entries),
            test_count=len(test_entries),
            evidence_count=len(evidence_entries),
            claim_count=len(claim_entries),
            req_test_missing=req_test_missing,
            req_evidence_missing=req_evidence_missing,
            claim_test_missing=claim_test_missing,
            claim_evidence_missing=claim_evidence_missing,
        ),
        encoding="utf-8",
    )

    return emit(findings, args.mode, "Registry link validation OK")


if __name__ == "__main__":
    raise SystemExit(main())
