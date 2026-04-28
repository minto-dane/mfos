# MFOS Phase 0.6 Lint Audit

Date: 2026-04-27

Scope:

- Local deterministic validators for Source Cards, requirements, claims, pack contracts, split-spec front matter, source grounding, audit obligations, no-fake-success, prohibited wording, and SPEC_GAP/UNSUPPORTED misuse.
- Traceability generation for design registries.
- No production implementation code was started.

## Implemented Scripts

- `scripts/validate-source-cards.py`
- `scripts/validate-requirements.py`
- `scripts/validate-claims.py`
- `scripts/validate-spec-front-matter.py`
- `scripts/validate-packs.py`
- `scripts/check-prohibited-terms.py`
- `scripts/check-no-fake-success.py`
- `scripts/check-source-grounding.py`
- `scripts/check-audit-obligations.py`
- `scripts/check-spec-gap-misuse.py`
- `scripts/generate-traceability.py`
- `scripts/validate-all.sh`

## Phase 0.6 Hardening Added After Red Team Review

- `scripts/mfos_lint.py` now recognizes short Source IDs such as `TUF-001`, `TCG-001`, `SLSA-001`, `SEL4-001`, and `FBVBS-001`.
- `scripts/validate-spec-front-matter.py` now fails when body Source Matrix IDs are missing from front matter `source_refs`.
- `scripts/validate-spec-front-matter.py` now fails on Markdown table width mismatches, while ignoring pipes inside inline code.
- Ambiguous profile tables in audit, Guard, Linux gateway, hardware profile, and attestation specs were repaired.

## Validation Behavior

- Default mode is `draft`.
- Draft mode fails `BLOCK` and `ERROR` findings.
- Release mode also fails `WARN` findings.
- Draft warnings remain allowed because registry coverage is still seed-level and evidence records are not verified artifacts.

## Current Draft Validation Result

`./scripts/validate-all.sh` passes in draft mode.

Remaining warnings are intentional Phase 0.7 work:

- 34 audit-obligation warnings for priority requirements that lack registered test and/or evidence coverage.
- 5 SPEC_GAP/UNSUPPORTED wording warnings in explanatory design text.
- 4 claim warnings for High-Assurance Guard requirements not yet registered in the priority requirement catalog.

## Constraints

`/home/nia/mfos` is not currently a Git repository, so dirty-worktree analysis was limited to direct file inspection.
