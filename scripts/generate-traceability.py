#!/usr/bin/env python3
"""Generate MFOS Phase 0.6 traceability matrices."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import yaml

from mfos_lint import EVIDENCE, REQUIREMENTS, ROOT, SOURCE_INDEX, SPECS_DIR, TESTS, load_yaml, parse_front_matter


OUT = ROOT / "evidence/traceability"
REPORT = ROOT / "reports/generated/traceability.md"
CLAIMS = ROOT / "docs/design/assurance/claim-tree.yml"
PACKS = ROOT / "packs/pack-index.yml"


def write_yaml(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def req_matches(pattern: str, rid: str) -> bool:
    if pattern.endswith("*"):
        return rid.startswith(pattern[:-1])
    return pattern == rid


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    source_index = load_yaml(SOURCE_INDEX)
    req_catalog = load_yaml(REQUIREMENTS)
    test_registry = load_yaml(TESTS)
    evidence_registry = load_yaml(EVIDENCE)
    claim_tree = load_yaml(CLAIMS) if CLAIMS.exists() else {"claims": []}
    pack_index = load_yaml(PACKS) if PACKS.exists() else {"entries": []}

    req_entries = [entry for entry in req_catalog.get("entries", []) if isinstance(entry, dict)]
    req_ids = {entry["requirement_id"] for entry in req_entries if isinstance(entry.get("requirement_id"), str)}

    source_to_req: dict[str, set[str]] = defaultdict(set)
    for entry in req_entries:
        rid = entry.get("requirement_id")
        for ref in entry.get("source_refs", []) if isinstance(entry.get("source_refs"), list) else []:
            if isinstance(ref, dict) and ref.get("source_id") and rid:
                source_to_req[str(ref["source_id"])].add(str(rid))

    for card in source_index.get("cards", []) if isinstance(source_index, dict) else []:
        if not isinstance(card, dict):
            continue
        sid = card.get("source_id")
        cpath = card.get("card_path")
        if not sid or not cpath:
            continue
        full = ROOT / str(cpath)
        if not full.exists():
            continue
        cdata = load_yaml(full)
        if isinstance(cdata, dict):
            for rid in cdata.get("requirement_refs", []) if isinstance(cdata.get("requirement_refs"), list) else []:
                source_to_req[str(sid)].add(str(rid))

    specs_by_req: dict[str, set[str]] = defaultdict(set)
    for spec in sorted(SPECS_DIR.glob("*.md")):
        fm, _ = parse_front_matter(spec)
        if not isinstance(fm, dict):
            continue
        for pattern in fm.get("requirement_refs", []) if isinstance(fm.get("requirement_refs"), list) else []:
            for rid in req_ids:
                if req_matches(str(pattern), rid):
                    specs_by_req[rid].add(str(spec.relative_to(ROOT)))

    tests_by_req: dict[str, set[str]] = defaultdict(set)
    for entry in test_registry.get("entries", []) if isinstance(test_registry, dict) else []:
        if not isinstance(entry, dict):
            continue
        tid = entry.get("test_id")
        for rid in entry.get("requirement_ids", []) if isinstance(entry.get("requirement_ids"), list) else []:
            if tid:
                tests_by_req[str(rid)].add(str(tid))

    evidence_by_req: dict[str, set[str]] = defaultdict(set)
    for entry in evidence_registry.get("entries", []) if isinstance(evidence_registry, dict) else []:
        if not isinstance(entry, dict):
            continue
        eid = entry.get("evidence_id")
        for rid in entry.get("requirement_ids", []) if isinstance(entry.get("requirement_ids"), list) else []:
            if eid:
                evidence_by_req[str(rid)].add(str(eid))
    for entry in req_entries:
        rid = entry.get("requirement_id")
        if not rid:
            continue
        for evid in entry.get("evidence_required", []) if isinstance(entry.get("evidence_required"), list) else []:
            if isinstance(evid, dict) and evid.get("evidence_id"):
                evidence_by_req[str(rid)].add(str(evid["evidence_id"]))

    claim_to_req: dict[str, list[str]] = {}
    for claim in claim_tree.get("claims", []) if isinstance(claim_tree, dict) else []:
        if isinstance(claim, dict) and claim.get("claim_id"):
            claim_to_req[str(claim["claim_id"])] = [str(r) for r in claim.get("requirements", []) if isinstance(r, str)]

    pack_to_refs: dict[str, dict[str, list[str]]] = {}
    for pack in pack_index.get("entries", []) if isinstance(pack_index, dict) else []:
        if isinstance(pack, dict) and pack.get("pack_id"):
            pack_to_refs[str(pack["pack_id"])] = {
                "requirements": [str(x) for x in pack.get("requirements", []) if isinstance(x, str)],
                "inputs": [str(x) for x in pack.get("inputs", []) if isinstance(x, str)],
                "outputs": [str(x) for x in pack.get("outputs", []) if isinstance(x, str)],
                "tests": [str(x) for x in (pack.get("positive_tests", []) + pack.get("negative_tests", [])) if isinstance(x, str)],
            }

    gaps: list[dict[str, object]] = []
    unregistered_from_sources = [
        {"source_id": sid, "requirement_id": rid}
        for sid, rids in source_to_req.items()
        for rid in sorted(rids)
        if "*" not in rid and rid not in req_ids
    ]
    if unregistered_from_sources:
        gaps.append({
            "gap_id": "TRACE-SRC-0001",
            "severity": "high",
            "summary": "Source cards or source mappings reference requirements not registered in the priority catalog.",
            "count": len(unregistered_from_sources),
            "items": unregistered_from_sources,
        })

    missing_specs = sorted(rid for rid in req_ids if not specs_by_req.get(rid))
    if missing_specs:
        gaps.append({"gap_id": "TRACE-SPEC-0001", "severity": "medium", "summary": "Priority requirements without spec front matter match.", "count": len(missing_specs), "items": missing_specs})

    missing_tests = sorted(rid for rid in req_ids if not tests_by_req.get(rid))
    if missing_tests:
        gaps.append({"gap_id": "TRACE-TEST-0001", "severity": "high", "summary": "Priority requirements without registered tests.", "count": len(missing_tests), "items": missing_tests})

    missing_evidence = sorted(rid for rid in req_ids if not evidence_by_req.get(rid))
    if missing_evidence:
        gaps.append({"gap_id": "TRACE-EVID-0001", "severity": "high", "summary": "Priority requirements without evidence mapping.", "count": len(missing_evidence), "items": missing_evidence})

    claim_req_missing = [
        {"claim_id": cid, "requirement_id": rid}
        for cid, rids in claim_to_req.items()
        for rid in rids
        if "*" not in rid and rid not in req_ids
    ]
    if claim_req_missing:
        gaps.append({"gap_id": "TRACE-CLAIM-0001", "severity": "medium", "summary": "Claims reference requirements not in priority catalog.", "count": len(claim_req_missing), "items": claim_req_missing})

    envelope = {
        "schema_version": 1,
        "status": "draft",
        "generated_at": "2026-04-27",
        "generated_by": "scripts/generate-traceability.py",
        "non_compatibility_statement": "MFOS is z/OS-inspired and does not claim z/OS compatibility or IBM product compatibility.",
    }

    write_yaml(OUT / "source-to-requirement.yml", envelope | {"entries": [{"source_id": sid, "requirements": sorted(rids)} for sid, rids in sorted(source_to_req.items())]})
    write_yaml(OUT / "requirement-to-spec.yml", envelope | {"entries": [{"requirement_id": rid, "specs": sorted(specs_by_req.get(rid, []))} for rid in sorted(req_ids)]})
    write_yaml(OUT / "requirement-to-test.yml", envelope | {"entries": [{"requirement_id": rid, "tests": sorted(tests_by_req.get(rid, []))} for rid in sorted(req_ids)]})
    write_yaml(OUT / "requirement-to-evidence.yml", envelope | {"entries": [{"requirement_id": rid, "evidence": sorted(evidence_by_req.get(rid, []))} for rid in sorted(req_ids)]})
    write_yaml(OUT / "claim-to-requirement.yml", envelope | {"entries": [{"claim_id": cid, "requirements": rids} for cid, rids in sorted(claim_to_req.items())]})
    write_yaml(OUT / "pack-to-artifacts.yml", envelope | {"entries": [{"pack_id": pid, **refs} for pid, refs in sorted(pack_to_refs.items())]})
    write_yaml(OUT / "gap-report.yml", envelope | {"report_kind": "traceability_gap_report", "summary": {"gap_groups": len(gaps), "high_gap_groups": sum(1 for g in gaps if g.get("severity") == "high")}, "gaps": gaps})

    lines = [
        "# MFOS Draft Traceability Report",
        "",
        "Generated by `scripts/generate-traceability.py`.",
        "",
        f"- Requirements: {len(req_ids)}",
        f"- Sources with requirement links: {len(source_to_req)}",
        f"- Claims: {len(claim_to_req)}",
        f"- Packs: {len(pack_to_refs)}",
        f"- Gap groups: {len(gaps)}",
        "",
        "| Requirement | Specs | Tests | Evidence |",
        "| --- | --- | --- | --- |",
    ]
    for rid in sorted(req_ids):
        lines.append("| " + " | ".join([
            rid,
            ", ".join(sorted(specs_by_req.get(rid, []))) or "MISSING",
            ", ".join(sorted(tests_by_req.get(rid, []))) or "MISSING",
            ", ".join(sorted(evidence_by_req.get(rid, []))) or "MISSING",
        ]) + " |")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote traceability matrices under {OUT.relative_to(ROOT)}")
    print(f"Wrote {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
