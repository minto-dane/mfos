# MFOS Spec Front Matter Audit

Date: 2026-04-27

Scope: `docs/design/specs/*.md`

## Summary

- Audited 35 Markdown files under `docs/design/specs/`.
- Found 35 files without YAML front matter.
- Added compact YAML front matter to all 35 files.
- Created `schemas/spec-front-matter.schema.json`.
- No spec bodies were rewritten.
- No pack scripts or traceability scripts were touched.

## Canonicalization Policy Used

Required fields were populated as follows:

- `spec_id`: derived from the filename using the `MFOS-SPEC-NN-SLUG` form, with `MFOS-SPEC-INDEX` for `INDEX.md`.
- `title`: copied from the first level-one heading.
- `canonical_language`: set to `en-US`.
- `japanese_mirror`: set to `missing` because no safe mirror path was identified during this pass.
- `status`: normalized to `draft` for all audited files.
- `owner`: copied from an explicit `Owner:` line when present; otherwise set to `MFOS architecture`.
- `last_reviewed`: set to `2026-04-27` for this audit pass.
- `source_refs`: derived from source ID tokens present in the spec body.
- `requirement_refs`: compacted to requirement namespace wildcards when concrete IDs were present.
- `claim_refs`, `test_refs`, and `evidence_refs`: derived from matching ID tokens when present; otherwise set to `[]`.
- `implementation_allowed`: set to `false` because the documents remain draft/index material and this task did not authorize implementation.
- `downstream_packs`: set to `[]` because no safe pack ownership was inferred.
- `spec_gap_policy`: set to `implementation_must_not_infer_or_fill_gaps`.

## File Results

| File | Result |
| --- | --- |
| `00-normative-language.md` | Front matter added |
| `01-glossary.md` | Front matter added |
| `02-source-matrix.md` | Front matter added |
| `03-system-integrity.md` | Front matter added |
| `04-threat-model.md` | Front matter added |
| `05-object-model.md` | Front matter added |
| `06-authorization.md` | Front matter added |
| `07-audit.md` | Front matter added |
| `08-dataset-catalog.md` | Front matter added |
| `09-job-spool.md` | Front matter added |
| `10-operator-console.md` | Front matter added |
| `11-workload-policy.md` | Front matter added |
| `12-amf.md` | Front matter added |
| `13-update.md` | Front matter added |
| `14-nucleus.md` | Front matter added |
| `15-svc-pcall.md` | Front matter added |
| `16-pxm.md` | Front matter added |
| `17-guard.md` | Front matter added |
| `18-linux-gateway.md` | Front matter added |
| `19-assurance-case.md` | Front matter added |
| `20-conformance.md` | Front matter added |
| `21-ai-implementation-contract.md` | Front matter added |
| `22-production-readiness.md` | Front matter added |
| `23-requirements-catalog.md` | Front matter added |
| `24-formal-methods.md` | Front matter added |
| `25-operations-recovery.md` | Front matter added |
| `26-hardware-profile.md` | Front matter added |
| `27-spec-front-matter.md` | Front matter added |
| `28-machine-readable-registries.md` | Front matter added |
| `29-test-strategy.md` | Front matter added |
| `30-attestation-measured-boot.md` | Front matter added |
| `31-release-distribution-rollback.md` | Front matter added |
| `32-language-localization.md` | Front matter added |
| `33-policy-lint.md` | Front matter added |
| `INDEX.md` | Front matter added |

## Open Audit Notes

- The schema captures the Phase 0.6 canonical field set requested for this pass. It intentionally does not implement the broader draft schema described in `27-spec-front-matter.md`.
- `japanese_mirror` remains `missing` across the audited files until mirror paths and synchronization state are explicitly defined.
- Empty reference arrays mean no safe token was found in the local spec body during this pass, not that no future references are required.
- After Red Team review, front matter `source_refs` were normalized so every Source Matrix ID found in a split-spec body is also present in that file's front matter.
- `scripts/validate-spec-front-matter.py` now rejects body/front-matter Source Matrix drift and Markdown table width mismatches.
- `python3 scripts/validate-spec-front-matter.py --mode draft` currently passes with 35 checked specs and 0 warnings.
