# Naming Source-ID Audit

Date: 2026-04-27

Scope audited:

- `docs/design/source-matrix/source-matrix.yml`
- `docs/design/source-matrix/cards/*.yml`
- `docs/design/registries/*.yaml`
- `packs/pack-index.yml`
- `docs/design/packs/PACKS.md`
- `scripts/`

Constraints honored:

- No source cards, registries, packs, or scripts were edited.
- Only this report and `reports/naming-source-id-audit.yml` were written.
- This is a proposal only; implementation was not started.

## Summary

The requested scope contains 23 current canonical `IBM-*` source IDs. I propose
renaming those canonical IDs to `EXTREF-IBM-*` while preserving the existing
`IBM-*` values as legacy aliases.

Scope note: "all source IDs" in this report means every current `IBM-*` source
ID in the audited source matrix. Non-IBM IDs such as `X64-*`, `NIST-*`,
`TUF-*`, and `FBVBS-*` were observed but are outside this IBM-focused mapping
proposal.

Recommended canonical shape:

```yaml
source_id: EXTREF-IBM-SI-001
legacy_source_ids:
  - IBM-SI-001
```

This keeps the vendor/source provenance visible without making `IBM-*` the
canonical namespace. During migration, validators should accept both canonical
IDs and `legacy_source_ids`, but generated outputs should normalize to the
`EXTREF-*` canonical ID.

## Mapping Proposal

| old canonical ID | proposed canonical ID | source type | title |
| --- | --- | --- | --- |
| `IBM-APF-001` | `EXTREF-IBM-APF-001` | normative | Authorized programs |
| `IBM-DFSMS-001` | `EXTREF-IBM-DFSMS-001` | normative | DFSMSdfp Catalogs |
| `IBM-DFSMS-002` | `EXTREF-IBM-DFSMS-002` | normative | z/OS DFSMS library |
| `IBM-DPM-001` | `EXTREF-IBM-DPM-001` | normative | Dynamic Partition Manager |
| `IBM-JES-001` | `EXTREF-IBM-JES-001` | normative | What is JES? |
| `IBM-JES-002` | `EXTREF-IBM-JES-002` | normative | Job flow through the system |
| `IBM-JES2-001` | `EXTREF-IBM-JES2-001` | normative | z/OS JES2 library |
| `IBM-LPAR-001` | `EXTREF-IBM-LPAR-001` | normative | Introduction to Logical Partitions |
| `IBM-RACF-001` | `EXTREF-IBM-RACF-001` | normative | z/OS Security Server RACF library |
| `IBM-RACF-002` | `EXTREF-IBM-RACF-002` | normative | Authorizing users to access protected resources |
| `IBM-SI-001` | `EXTREF-IBM-SI-001` | normative | z/OS and system integrity |
| `IBM-SMF-001` | `EXTREF-IBM-SMF-001` | normative | Introduction to SMF |
| `IBM-SMF-002` | `EXTREF-IBM-SMF-002` | normative | Record type 80: RACF processing record |
| `IBM-SMPE-001` | `EXTREF-IBM-SMPE-001` | informative | SECINT HOLDDATA is now available with SMP/E RECEIVE ORDER |
| `IBM-STG-001` | `EXTREF-IBM-STG-001` | normative | What is storage protection? |
| `IBM-STG-002` | `EXTREF-IBM-STG-002` | normative | Storage protection summary |
| `IBM-UNIX-001` | `EXTREF-IBM-UNIX-001` | normative | Introduction to z/OS UNIX |
| `IBM-UNIX-002` | `EXTREF-IBM-UNIX-002` | normative | z/OS UNIX System Services library |
| `IBM-WPOL-001` | `EXTREF-IBM-WPOL-001` | normative | Defining service classes and performance goals |
| `IBM-XMEM-001` | `EXTREF-IBM-XMEM-001` | normative | Synchronous cross memory communication |
| `IBM-XMEM-002` | `EXTREF-IBM-XMEM-002` | normative | Controlling cross-memory communication |
| `IBM-ZACS-001` | `EXTREF-IBM-ZACS-001` | normative | z/OS Authorized Code Scanner introduction and overview |
| `IBM-ZARCH-001` | `EXTREF-IBM-ZARCH-001` | normative | z/Architecture Principles of Operation, SA22-7832-14 |

## Exact Files Needing Updates

Primary ledger files:

- `docs/design/source-matrix/source-matrix.yml`: 46 legacy occurrences across all 23 IBM IDs. Update `cards[].source_id`, `cards[].card_path`, and add legacy alias metadata.
- `docs/design/source-matrix/cards/IBM-APF-001.yml`: 3 occurrences; rename card file to `EXTREF-IBM-APF-001.yml`.
- `docs/design/source-matrix/cards/IBM-DFSMS-001.yml`: 3 occurrences; rename card file to `EXTREF-IBM-DFSMS-001.yml`.
- `docs/design/source-matrix/cards/IBM-DFSMS-002.yml`: 3 occurrences; rename card file to `EXTREF-IBM-DFSMS-002.yml`.
- `docs/design/source-matrix/cards/IBM-DPM-001.yml`: 3 occurrences; rename card file to `EXTREF-IBM-DPM-001.yml`.
- `docs/design/source-matrix/cards/IBM-JES-001.yml`: 3 occurrences; rename card file to `EXTREF-IBM-JES-001.yml`.
- `docs/design/source-matrix/cards/IBM-JES-002.yml`: 3 occurrences; rename card file to `EXTREF-IBM-JES-002.yml`.
- `docs/design/source-matrix/cards/IBM-JES2-001.yml`: 3 occurrences; rename card file to `EXTREF-IBM-JES2-001.yml`.
- `docs/design/source-matrix/cards/IBM-LPAR-001.yml`: 3 occurrences; rename card file to `EXTREF-IBM-LPAR-001.yml`.
- `docs/design/source-matrix/cards/IBM-RACF-001.yml`: 3 occurrences; rename card file to `EXTREF-IBM-RACF-001.yml`.
- `docs/design/source-matrix/cards/IBM-RACF-002.yml`: 3 occurrences; rename card file to `EXTREF-IBM-RACF-002.yml`.
- `docs/design/source-matrix/cards/IBM-SI-001.yml`: 3 occurrences; rename card file to `EXTREF-IBM-SI-001.yml`.
- `docs/design/source-matrix/cards/IBM-SMF-001.yml`: 3 occurrences; rename card file to `EXTREF-IBM-SMF-001.yml`.
- `docs/design/source-matrix/cards/IBM-SMF-002.yml`: 3 occurrences; rename card file to `EXTREF-IBM-SMF-002.yml`.
- `docs/design/source-matrix/cards/IBM-SMPE-001.yml`: 3 occurrences; rename card file to `EXTREF-IBM-SMPE-001.yml`.
- `docs/design/source-matrix/cards/IBM-STG-001.yml`: 3 occurrences; rename card file to `EXTREF-IBM-STG-001.yml`.
- `docs/design/source-matrix/cards/IBM-STG-002.yml`: 3 occurrences; rename card file to `EXTREF-IBM-STG-002.yml`.
- `docs/design/source-matrix/cards/IBM-UNIX-001.yml`: 3 occurrences; rename card file to `EXTREF-IBM-UNIX-001.yml`.
- `docs/design/source-matrix/cards/IBM-UNIX-002.yml`: 3 occurrences; rename card file to `EXTREF-IBM-UNIX-002.yml`.
- `docs/design/source-matrix/cards/IBM-WPOL-001.yml`: 3 occurrences; rename card file to `EXTREF-IBM-WPOL-001.yml`.
- `docs/design/source-matrix/cards/IBM-XMEM-001.yml`: 3 occurrences; rename card file to `EXTREF-IBM-XMEM-001.yml`.
- `docs/design/source-matrix/cards/IBM-XMEM-002.yml`: 3 occurrences; rename card file to `EXTREF-IBM-XMEM-002.yml`.
- `docs/design/source-matrix/cards/IBM-ZACS-001.yml`: 3 occurrences; rename card file to `EXTREF-IBM-ZACS-001.yml`.
- `docs/design/source-matrix/cards/IBM-ZARCH-001.yml`: 3 occurrences; rename card file to `EXTREF-IBM-ZARCH-001.yml`.

Registry and pack files:

- `docs/design/registries/evidence.yaml`: 262 legacy occurrences across all 23 IBM IDs in `source_matrix_ids`.
- `docs/design/registries/requirements.yaml`: 139 legacy occurrences across all 23 IBM IDs in `source_refs[].source_id`.
- `docs/design/registries/tasks.yaml`: 7 legacy occurrences across 5 IBM IDs in `source_matrix_ids`.
- `docs/design/registries/tests.yaml`: 388 legacy occurrences across all 23 IBM IDs in `source_matrix_ids`.
- `packs/pack-index.yml`: 42 legacy occurrences across 17 IBM IDs in string-list `source_refs`.
- `docs/design/packs/PACKS.md`: no literal `IBM-*` source IDs found in the audited file.

Script and schema support:

- `scripts/mfos_lint.py`: update `SOURCE_ID_RE` to recognize `EXTREF-*`; add canonical/alias resolution helpers instead of returning only raw `source_id` values.
- `scripts/validate-source-cards.py`: allow `legacy_source_ids`, validate uniqueness across canonical and legacy IDs, and support renamed card files.
- `scripts/validate-requirements.py`: resolve `source_refs[].source_id` through canonical IDs plus aliases.
- `scripts/validate-spec-front-matter.py`: normalize source IDs before comparing body IDs with front matter IDs.
- `scripts/check-source-grounding.py`: inherits the regex and known-source behavior from `mfos_lint.py`; verify after helper changes.
- `scripts/generate-traceability.py`: normalize aliases to canonical IDs in generated matrices.
- `scripts/validate-packs.py`: currently checks pack shape but not source-ref resolution; add validation or document that pack source refs are checked elsewhere.

Adjacent files outside the requested audit set are likely blockers for a full
migration:

- `docs/design/source-matrix/source-card-schema.md`
- `docs/design/source-matrix/source-lint-spec.md`
- `docs/design/source-matrix/source-matrix.md`
- `docs/design/source-matrix/source-matrix.yaml`
- `docs/design/source-matrix/traceability-index.md`
- `docs/design/source-matrix/traceability-policy.md`
- split specs under `docs/design/specs/`
- generated traceability under `evidence/traceability/`

Repository-wide search found 82 files containing `IBM-*` source-ID-shaped
tokens outside the new reports, so an implementation limited to the audited
machine-readable files would leave old IDs in prose and generated artifacts.

## Top Risks

1. The current source-card model makes `source_id`, `card_id`, filename stem,
   and index `card_path` agree. Changing only one of those will break source
   card validation.
2. There is no alias field today. `legacy_source_ids` must be added to the
   card/index schema before old IDs can be preserved safely.
3. References use multiple shapes: card `source_refs`, requirement
   `source_refs[].source_id`, registry `source_matrix_ids`, and pack string
   `source_refs`. A partial migration will split traceability.
4. `SOURCE_ID_RE` currently enumerates old prefixes, including `IBM`; without
   an `EXTREF` update, grounding/front-matter checks will miss the new
   canonical IDs.
5. Generated or legacy docs can reintroduce old canonical IDs unless the
   generator normalizes aliases and the migration plan covers prose artifacts.
