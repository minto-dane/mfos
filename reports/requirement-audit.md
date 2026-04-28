# MFOS Phase 0.6 Requirement Audit

Date: 2026-04-27

Scope:

- `docs/design/registries/requirements.yaml`
- `docs/design/registries/requirements-schema.md`
- `docs/design/specs/23-requirements-catalog.md`
- `docs/design/source-matrix/source-matrix.yml`
- `schemas/requirement.schema.json`

This audit did not add or change requirement entries.

## Result

Pass with no registry content changes required.

Validation summary:

- Parsed `docs/design/registries/requirements.yaml` successfully.
- Found 21 requirement entries.
- Confirmed requirement IDs are unique.
- Confirmed all entries include required source, profile, audit, failure, evidence, verification, and status fields.
- Confirmed all `source_refs[].source_id` values resolve through `docs/design/source-matrix/source-matrix.yml`.
- Confirmed all entries include the split profile keys: `baseline`, `enterprise_standalone`, `enterprise_pxm`, and `high_assurance`.
- Confirmed `enterprise_standalone` and `enterprise_pxm` are separate profiles in `profile_model`.

## Required Confirmations

`MFOS-REQ-CAT-0002`:

- Present in `docs/design/registries/requirements.yaml`.
- Normative text uses `MUST`.
- Profile applicability is `required` for `baseline`, `enterprise_standalone`, `enterprise_pxm`, and `high_assurance`.
- `audit_obligation` exists with `obligation: required`, `record_type: CATALOG_RESOLVE_DENY`, and `before_return: true`.
- `evidence_required` exists with three evidence descriptors.
- `source_refs` exists with four sourced references: `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`, `EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001`, `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`, and `FBVBS-001`.

Catalog-wide required fields:

- `source_refs` exists on every requirement entry.
- `audit_obligation` exists on every requirement entry.
- `evidence_required` exists on every requirement entry.
- `profile_applicability` contains the split profile keys on every requirement entry.

## Schema Work

Created `schemas/requirement.schema.json` as an executable JSON Schema for the current machine-readable registry shape. The schema requires:

- Source references for every requirement entry.
- Split profile applicability keys.
- Audit obligation fields.
- Evidence requirement fields.
- Failure mode fields.
- A catalog entry for `MFOS-REQ-CAT-0002` whose normative text contains `MUST`.

## Notes

When first checked in this task, `reports/` was absent. It now contains other audit artifacts that were not modified by this requirement audit.

The repository root at `/home/nia/mfos` is not a Git worktree, so dirty-worktree conflict detection was limited to direct file existence and content inspection rather than `git status`.
