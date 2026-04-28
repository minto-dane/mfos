# Prohibited Wording Lint Audit

Date: 2026-04-27

Scope: `scripts/checks/check-prohibited-terms.py` only, plus this audit report.
No implementation code was changed.

## Coverage Added

The prohibited wording lint now scans these additional roots:

- `reports/`
- `tasks/`
- `evidence/`
- `ai/`
- `governance/`

`governance/` was already covered and remains in scope.

## Prohibited Wording Covered

The lint now detects English and Japanese wording that can imply compatibility,
IBM approval, affiliation, sponsorship, endorsement, or MFOS official status.

New Japanese risk phrases include:

- `IBM公式`
- `公式資料`
- `公式概念`
- `公式の`
- `公式MFOS`
- `IBM による承認`
- `IBM による提携`
- `IBM による後援`
- `IBM による推奨`
- `IBM による公認`

New English risk phrases include:

- `official MFOS`
- `MFOS official`
- `IBM approval`
- `IBM affiliation`
- `IBM sponsorship`
- `IBM endorsement`
- `approved by IBM`
- `endorsed by IBM`
- `sponsored by IBM`

## Allowlisted Contexts

The lint allows clearly explanatory or prohibitive contexts only. Examples:

- `prohibited_inference`, `prohibited_claims`, `prohibited_wording`, and
  `prohibited_terms` fields.
- Negative-test, lint, and non-compatibility sections.
- Lines that explicitly say the project does not imply or must not imply IBM
  approval, affiliation, sponsorship, endorsement, or official status.
- Japanese explanatory lines that explicitly say the project does not claim or
  must not claim approval, affiliation, sponsorship, endorsement, compatibility,
  or official status.
- Red-team scope lists that are clearly describing the category being reviewed.

These contexts are allowlisted only so the project can document forbidden
wording and review it. They do not permit release, marketing, source card, or
spec language that asserts approval, affiliation, sponsorship, endorsement,
compatibility, or official status.

## Validation

Commands run:

```bash
python3 scripts/checks/check-prohibited-terms.py
./scripts/validate-all.sh
```

Results:

```text
Prohibited wording check OK
```

```text
./scripts/validate-all.sh
YAML parse failed: docs/design/source-matrix/cards/EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001.yml
```

The full validation failure is outside this task's owned files. The failure
occurs before the prohibited wording lint step, while parsing a Source Card
that was edited by another worker.
