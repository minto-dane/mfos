# Naming-Safety Refactor Report

Status: draft  
Date: 2026-04-27

## 1. Summary

The naming-safety refactor migrated external IBM-derived references into the
`EXTREF-IBM-*` namespace and tightened MFOS-owned identifier checks. The work
did not start production implementation.

Public release remains blocked pending human legal/IP review.

## 2. Old Names Found

- 23 canonical `IBM-*` source IDs in the Source Matrix and source cards.
- Legacy requirement domains such as `MFOS-REQ-SI-*`, `MFOS-REQ-SEC-*`,
  `MFOS-REQ-AUD-*`, `MFOS-REQ-CAT-*`, `MFOS-REQ-DATA-*`, `MFOS-REQ-UVS-*`,
  `MFOS-REQ-PXM-*`, `MFOS-REQ-GRD-*`, `MFOS-REQ-SPL-*`, and
  `MFOS-REQ-SRC-*`.
- Legacy test IDs in `MFOS-TEST-*` form.
- Legacy evidence IDs in `MFOS-EVID-*` form.
- Legacy claim IDs in `CLAIM-*` form.

## 3. New Names Chosen

- IBM-derived external references now use `EXTREF-IBM-*`.
- Requirements use expanded MFOS-owned domains, for example
  `MFOS-REQ-AUTH-*`, `MFOS-REQ-AUDIT-*`, `MFOS-REQ-CATALOG-*`,
  `MFOS-REQ-DATASET-*`, `MFOS-REQ-UPDATE-*`, `MFOS-REQ-PARTITION-*`, and
  `MFOS-REQ-SYSINT-*`.
- Positive tests use `TEST-MFOS-*`.
- Negative tests use `NEG-MFOS-*`.
- Evidence uses `EV-MFOS-*`.
- Claims use `MFOS-CLAIM-*`.

## 4. Files Renamed

The 23 IBM-derived Source Card files under `docs/design/source-matrix/cards/`
were renamed from `IBM-*.yml` to `EXTREF-IBM-*.yml` to match canonical
`source_id` values.

The prohibited implementation scaffold names were also renamed:

- `implementation/interfaces/tso-like/` -> `implementation/interfaces/command-processor/`
- `implementation/interfaces/ispf-like/` -> `implementation/interfaces/panel-ui/`
- `implementation/interfaces/zosmf-like-api/` -> `implementation/interfaces/management-api/`
- `implementation/services/tsoed/` -> `implementation/services/commandd/`
- `implementation/services/ispfd/` -> `implementation/services/paneld/`

## 5. References Updated

- `docs/design/source-matrix/source-matrix.yml`
- `docs/design/source-matrix/source-matrix.yaml`
- `docs/design/source-matrix/cards/*.yml`
- `docs/design/registries/requirements.yaml`
- `docs/design/registries/tests.yaml`
- `docs/design/registries/evidence.yaml`
- `docs/design/assurance/claim-tree.yml`
- `packs/pack-index.yml`
- `docs/design/specs/*.md`
- `evidence/traceability/*.yml`
- non-naming reports under `reports/`
- implementation scaffold references in `scripts/bootstrap-tree.sh`

## 6. Source IDs Migrated

Source ID aliases are recorded in `reports/naming-safety/naming-alias-map.yml`. The map
contains:

- 23 external reference migrations
- 87 requirement ID migrations
- 261 test ID migrations
- 170 evidence ID migrations
- 5 claim ID migrations

## 7. Requirement IDs Checked

`scripts/check-requirement-namespace.py` validates requirement, test, evidence,
claim, and requirement `source_refs` namespaces.

## 8. Remaining External Names And Allowed Contexts

External product names remain allowed in:

- Source Cards and Source Matrix policy
- `NOTICE.md`
- non-compatibility and legal-risk policy
- prohibited-wording examples
- naming migration reports and alias maps
- historical audit reports after migration to current `EXTREF-*` IDs

## 9. Lint Results

```text
./scripts/validate-naming-safety.sh release
EXTREF namespace check OK: 0 warnings
Source Card public-safety check OK: 0 warnings
Requirement namespace check OK: 0 warnings
MFOS-owned name check OK: 0 warnings
Compatibility-claim check OK: 0 warnings
External-doc copy guard OK: 0 warnings
```

`./scripts/validate-all.sh --check` also passes in draft mode.

Red-team remediation status:

- Critical path-name finding remediated for explicitly prohibited implementation
  scaffold terms.
- Source Card guidance stale-shape finding remediated.
- Non-naming report legacy-ID finding remediated.
- Non-IBM external mark-control finding remediated for current Source Cards.
- Validator coverage finding remediated for current local gates.

## 10. Open Issues Requiring Human / Legal Review

See `reports/naming-safety/naming-safety-open-issues.md`.

## Final Judgment

```yaml
naming_safety_refactor_complete: true
public_release_allowed: false
private_internal_use_allowed: true
requires_ip_attorney_review_before_public_release: true
production_implementation_allowed: false
```
