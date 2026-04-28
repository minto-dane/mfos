# MFOS Registry Namespace Audit

Generated: 2026-04-27T22:17:09Z

Scope:

- `docs/design/registries/requirements.yaml`
- `docs/design/registries/tests.yaml`
- `docs/design/registries/evidence.yaml`
- `docs/design/assurance/claim-tree.yml`
- `schemas/*.json`

Constraint: registry files were inspected only. No registry was edited.

## Target Policy

| Namespace | Target style |
| --- | --- |
| Requirements | `MFOS-REQ-<DOMAIN>-NNNN` |
| Tests | `TEST-MFOS-*` or `NEG-MFOS-*` |
| Evidence | `EV-MFOS-*` |
| Claims | `MFOS-CLAIM-*` |
| Source references | `EXTREF-*` |

For tests, this audit interprets `NEG-MFOS-*` as the target namespace for records whose `test_type` is `negative`, and `TEST-MFOS-*` as the target namespace for positive and non-negative test records.

## Executive Findings

1. Requirement IDs are already target-compliant. All 106 requirement definitions match `MFOS-REQ-<DOMAIN>-NNNN`, with no duplicate requirement IDs.
2. Test, evidence, and claim definitions are entirely on legacy namespace families. All 261 test IDs are `MFOS-TEST-*`; all 170 evidence IDs are `MFOS-EVID-*`; all 5 claim IDs are `CLAIM-*`.
3. Source references are entirely pre-target style in the audited registries. The audited files contain 1,433 source-like reference instances across `source_refs[].source_id` and `source_matrix_ids`, covering 37 unique IDs such as `FBVBS-001`, `IBM-SI-001`, and `NIST-218-001`; none use `EXTREF-*`.
4. Cross-registry links are internally consistent under the current names. The parsed requirement, test, evidence, and claim reference fields have zero unresolved references against the current registries.
5. The schemas are not migration-ready. `schemas/requirement.schema.json` actively requires old `MFOS-TEST-*`, `MFOS-EVID-*`, and non-`EXTREF-*` source ID formats, while `schemas/test-case.schema.json`, `schemas/evidence.schema.json`, and `schemas/claim.schema.json` do not enforce the target ID families at all.

## Registry Results

| Area | Definitions | Target-compliant | Non-compliant | Duplicates | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| Requirements | 106 | 106 | 0 | 0 | Domains: AI, AMF, AUD, CAT, DATA, GRD, JOB, NUC, OPER, PROF, PXM, QUAL, SEC, SI, SPL, SRC, UVS, workload policy |
| Tests | 261 | 0 | 261 | 0 | 102 positive, 158 negative, 1 fuzz |
| Evidence | 170 | 0 | 170 | 0 | All definitions use `MFOS-EVID-*` |
| Claims | 5 | 0 | 5 | 0 | All definitions use `CLAIM-*` |

Representative locations:

- Requirement target-compliant example: `docs/design/registries/requirements.yaml:50`
- Legacy source references and test references in requirements: `docs/design/registries/requirements.yaml:58`, `docs/design/registries/requirements.yaml:83`
- Legacy evidence-required IDs in requirements: `docs/design/registries/requirements.yaml:100`
- Legacy test ID definition and source matrix refs: `docs/design/registries/tests.yaml:28`, `docs/design/registries/tests.yaml:37`
- Legacy evidence ID definition and test refs: `docs/design/registries/evidence.yaml:25`, `docs/design/registries/evidence.yaml:32`
- Legacy claim ID and claim-tree refs: `docs/design/assurance/claim-tree.yml:7`, `docs/design/assurance/claim-tree.yml:31`, `docs/design/assurance/claim-tree.yml:35`

## Reference Impact

| File / field family | Instances | Unique IDs | Target-compliant | Unresolved under current IDs |
| --- | ---: | ---: | ---: | ---: |
| `requirements.yaml` requirement definitions | 106 | 106 | 106 | n/a |
| `requirements.yaml` verification test refs | 261 | 248 | 0 | 0 |
| `requirements.yaml` evidence-required refs | 167 | 164 | 0 | 0 |
| `requirements.yaml` `source_refs[].source_id` | 250 | 37 | 0 | n/a |
| `tests.yaml` test definitions | 261 | 261 | 0 | n/a |
| `tests.yaml` requirement refs | 308 | 106 | 308 | 0 |
| `tests.yaml` evidence refs | 101 | 101 | 0 | 0 |
| `tests.yaml` `source_matrix_ids` | 704 | 37 | 0 | n/a |
| `evidence.yaml` evidence definitions | 170 | 170 | 0 | n/a |
| `evidence.yaml` requirement refs | 182 | 106 | 182 | 0 |
| `evidence.yaml` test refs | 341 | 185 | 0 | 0 |
| `evidence.yaml` claim refs | 20 | 5 | 0 | 0 |
| `evidence.yaml` `source_matrix_ids` | 479 | 37 | 0 | n/a |
| `claim-tree.yml` claim definitions | 5 | 5 | 0 | n/a |
| `claim-tree.yml` requirement refs | 19 | 17 | 19 | 0 |
| `claim-tree.yml` test refs | 13 | 13 | 0 | 0 |
| `claim-tree.yml` evidence refs | 18 | 17 | 0 | 0 |

Source-like references use the same 37 unique current IDs in requirements, tests, and evidence: `FBVBS-001`, `IBM-APF-001`, `IBM-DFSMS-001`, `IBM-DFSMS-002`, `IBM-DPM-001`, `IBM-JES-001`, `IBM-JES-002`, `IBM-JES2-001`, `IBM-LPAR-001`, `IBM-RACF-001`, `IBM-RACF-002`, `IBM-SI-001`, `IBM-SMF-001`, `IBM-SMF-002`, `IBM-SMPE-001`, `IBM-STG-001`, `IBM-STG-002`, `IBM-UNIX-001`, `IBM-UNIX-002`, `IBM-WPOL-001`, `IBM-XMEM-001`, `IBM-XMEM-002`, `IBM-ZACS-001`, `IBM-ZARCH-001`, `MS-VBS-001`, `MS-VSM-001`, `NIST-160-001`, `NIST-193-001`, `NIST-218-001`, `SEL4-001`, `SLSA-001`, `TCG-001`, `TUF-001`, `X64-AMD-001`, `X64-INTEL-001`, `X64-LINUX-CET-001`, `X64-LINUX-PKU-001`.

## Schema Findings

| Schema | Finding | Compatibility impact |
| --- | --- | --- |
| `schemas/requirement.schema.json:146` | `source_refs[].source_id` allows current source-card IDs such as `IBM-SI-001`, not target `EXTREF-*`. | Updating requirements to `EXTREF-*` would fail this schema until the pattern is changed. |
| `schemas/requirement.schema.json:166` and `schemas/requirement.schema.json:170` | Requirement verification test refs require `^MFOS-TEST-[A-Z0-9-]+$`. | Target `TEST-MFOS-*` or `NEG-MFOS-*` refs would fail schema validation. |
| `schemas/requirement.schema.json:222` | `evidence_required[].evidence_id` requires `^MFOS-EVID-[A-Z0-9-]+$`. | Target `EV-MFOS-*` refs would fail schema validation. |
| `schemas/requirement.schema.json:241` | `requirement_id` already requires `^MFOS-REQ-[A-Z0-9]+-[0-9]{4}$`. | Requirement namespace is aligned. |
| `schemas/test-case.schema.json:8` | `test_id` is an unconstrained string. | It permits both legacy and target IDs, so it will not enforce migration. |
| `schemas/evidence.schema.json:8` | `evidence_id` is an unconstrained string. | It permits both legacy and target IDs, so it will not enforce migration. |
| `schemas/claim.schema.json:21` | `claim_id` is an unconstrained string; claim refs in `requirements`, `tests`, and `evidence` are also unconstrained strings. | Claim namespace drift can pass schema validation. |
| `schemas/source-card.schema.json:26` and `schemas/source-card.schema.json:43` | `source_id` permits any uppercase hyphenated ID; `source_refs` items are unconstrained objects. | Source-card validation does not require `EXTREF-*`. |
| `schemas/spec-front-matter.schema.json:31` | `source_refs` are unconstrained strings. | Spec front matter can continue using pre-target source refs. |
| `schemas/pack.schema.json:37` | `source_refs` are unconstrained strings. | Work packs can continue using pre-target source refs. |

## Migration Impact

Minimum in-scope rename/update volume:

- Rename 261 test definitions.
- Update 615 test-reference instances: 261 in requirements, 341 in evidence, and 13 in the claim tree.
- Rename 170 evidence definitions.
- Update 286 evidence-reference instances: 167 in requirements, 101 in tests, and 18 in the claim tree.
- Rename 5 claim definitions.
- Update 20 claim-reference instances in evidence.
- Replace or alias 1,433 source-like reference instances if `source_refs` and `source_matrix_ids` both migrate to `EXTREF-*`.
- Update schemas before or atomically with registry migration, especially `schemas/requirement.schema.json`, because it currently rejects target test and evidence references.

The observed current graph has no unresolved links, so the main compatibility risk is not broken existing traceability. The risk is introduced by partial migration: any single registry renamed ahead of its references will break requirements-to-tests, requirements-to-evidence, evidence-to-tests, evidence-to-claims, or claim-tree traceability.

## Compatibility Risks

1. **Schema-first blocker**: If registry IDs migrate before schema patterns do, requirement registry validation will fail for target test refs, evidence refs, and source refs.
2. **Partial rename breakage**: Current cross-registry references resolve cleanly. Renaming only definitions, or only refs, will immediately create unresolved links.
3. **Negative test namespace ambiguity**: Current IDs already include `NEG` inside the body, for example `MFOS-TEST-DATA-NEG-0001`. A naive prefix rewrite to `NEG-MFOS-DATA-NEG-0001` preserves traceability but duplicates the negative marker. A reviewed mapping rule should decide whether the embedded `NEG` remains part of the semantic slug.
4. **Source-card compatibility**: The audited registries reference source matrix/source card IDs such as `IBM-SI-001`; target `EXTREF-*` values require a source-matrix alias map. Migrating only these registries without source-card/source-matrix support will break source resolution.
5. **External prose and generated artifacts**: The registries intentionally preserve legacy IDs and reference IDs already present in prose specs and artifacts. External documents, CI jobs, fixtures, artifact paths, and reports may still depend on current names.
6. **Schema under-enforcement**: Test, evidence, and claim schemas are too permissive to prevent old and new namespaces from mixing after migration.

## Recommended Migration Sequence

1. Define canonical deterministic mapping tables for tests, evidence, claims, and source refs. Keep old IDs as aliases during a transition window.
2. Update schemas to accept the target families and, where needed, explicit legacy alias fields.
3. Migrate definitions and references atomically across requirements, tests, evidence, claim tree, and source matrix/card material.
4. Add CI checks that reject mixed canonical namespaces while allowing declared aliases in `legacy_ids` or equivalent alias fields.
5. Re-run traceability validation and compare unresolved-link counts against the current baseline of zero.
