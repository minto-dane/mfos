# Naming Validator Coverage Report

Date: 2026-04-27

## Scope

This update closes the red-team coverage gaps assigned to the naming validator
worker. It changes validation and documentation only; no production code was
edited.

## Coverage Added

- `scripts/check-mf-owned-names.py` now scans directories as well as text-file
  paths, so empty owned directories can no longer hide external-product tokens.
- `scripts/check-extref-namespace.py` now scans `reports/`. Legacy `IBM-*`
  source IDs remain allowed in Source Cards, the source index
  `legacy_source_ids` context, and `reports/naming-*` migration artifacts only.
- `scripts/check-source-card-public-safe.py` now scans public Source Card
  guidance outside card YAML for stale public-unsafe examples, including
  prohibited removed fields, `source_type: normative`, and guidance that says
  Source Cards store summaries.
- `schemas/source-card.schema.json` no longer validates canonical `IBM-*`
  `source_id` values. IBM-derived canonical source IDs must use the
  `EXTREF-...-[0-9]{4}` form; the legacy three-digit IDs remain valid only in
  `legacy_source_ids`.
- `README.md` now lists `./scripts/validate-naming-safety.sh release` in local
  checks.

## Validation Results

Initial command run:

```bash
./scripts/validate-naming-safety.sh release
```

Result: failed closed at `scripts/check-extref-namespace.py` with 117 errors
and 0 warnings. The failure was expected after adding release-bound report
coverage: non-naming historical reports still contained legacy `IBM-*` IDs
outside the allowed naming migration context.

Error distribution:

| File | Errors |
| --- | ---: |
| `reports/requirement-gap-closure.md` | 56 |
| `reports/source-card-audit.md` | 31 |
| `reports/source-card-pin-audit.md` | 10 |
| `reports/source-card-targeted-review.md` | 9 |
| `reports/mfos-owned-name-audit.md` | 6 |
| `reports/requirement-audit.md` | 3 |
| `reports/mfos-owned-name-audit.yml` | 1 |
| `reports/prohibited-wording-audit.md` | 1 |

Checks run individually after the aggregate script stopped:

| Check | Result |
| --- | --- |
| `python3 scripts/check-source-card-public-safe.py --mode release` | Passed, 0 warnings |
| `python3 scripts/check-requirement-namespace.py --mode release` | Passed, 0 warnings |
| `python3 scripts/check-mf-owned-names.py --mode release` | Passed, 0 warnings |
| `python3 scripts/check-no-compatibility-claims.py --mode release` | Passed, 0 warnings |
| `python3 scripts/check-no-copied-external-docs.py --mode release` | Passed, 0 warnings |
| `python3 -m py_compile scripts/check-mf-owned-names.py scripts/check-extref-namespace.py scripts/check-source-card-public-safe.py` | Passed |

## Follow-Up Remediation

The non-naming report references were migrated to current `EXTREF-*` IDs after
this validator update. A subsequent run of:

```bash
./scripts/validate-naming-safety.sh release
```

passed with 0 warnings.
