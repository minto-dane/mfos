# Source Card Audit

Date: 2026-04-27

Scope:

- `docs/design/source-matrix/source-matrix.yml`
- `docs/design/source-matrix/cards/*.yml`
- `schemas/source-card.schema.json`

Constraints honored:

- No implementation code started.
- No source cards were weakened or modified.
- No publication numbers were invented.
- Metadata that cannot be verified from local cards is recorded as a gap.

## Summary

Result: PASS with warnings.

- Source matrix index parsed as YAML.
- Source card files parsed as YAML.
- Index/card coverage matched: 37 index entries and 37 card files.
- Blocking validation errors: 0.
- Warnings: 8.
- Local metadata verification gaps: 37.

## Validation Checks

- `source-matrix.yml` root is a mapping and includes required index fields.
- `schema_version` is `1`.
- `document_id` matches `MFOS-SOURCE-MATRIX-CARD-INDEX-[0-9]{4}`.
- `status` is `draft`.
- `compatibility_statement` states that MFOS does not claim z/OS compatibility.
- `global_rules.ledger_rules` is a non-empty list.
- Every `cards[].card_path` exists.
- Every `cards/*.yml` file has a matching `source_id` filename stem.
- No duplicate index source IDs were found.
- Every card includes required v1 card fields, including `verification_refs`.
- List-shaped fields are lists in the current cards.
- `retrieved_at` is `2026-04-27` in the current cards.
- Normative sources have at least one requirement reference.
- IBM-derived cards include compatibility-risk wording in `prohibited_inference`.

## Warnings

The following IBM-derived cards pass blocking compatibility checks, but their
`mfos_mapping.allowed_wording` does not include the lint spec's preferred
non-compatibility cue words: `inspired`, `mapped`, or `reference`.

- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-JES2-LIBRARY-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-Z-ARCHITECTURE-PRINCIPLES-0001.yml`

These warnings were not auto-fixed because this audit is restricted to schema
and report updates only.

## Local Metadata Gaps

Every current card uses a converted `version_or_scope` statement that says
exact section/version pins remain gaps unless listed. No local archived source
content or locally verifiable publication metadata was found in the audited
card set, so exact publication, section, and version metadata remains
unverified locally for all 37 cards.

Affected cards:

- `docs/design/source-matrix/cards/FBVBS-001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-Z-DPM-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-JES-INTRODUCTION-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-JES-JOB-FLOW-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-JES2-LIBRARY-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-Z-LPAR-INTRODUCTION-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-SECURITY-SERVER-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-STORAGE-PROTECTION-SUMMARY-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-CROSS-MEMORY-SYNCHRONOUS-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001.yml`
- `docs/design/source-matrix/cards/EXTREF-IBM-Z-ARCHITECTURE-PRINCIPLES-0001.yml`
- `docs/design/source-matrix/cards/MS-VBS-001.yml`
- `docs/design/source-matrix/cards/MS-VSM-001.yml`
- `docs/design/source-matrix/cards/NIST-160-001.yml`
- `docs/design/source-matrix/cards/NIST-193-001.yml`
- `docs/design/source-matrix/cards/NIST-218-001.yml`
- `docs/design/source-matrix/cards/SEL4-001.yml`
- `docs/design/source-matrix/cards/SLSA-001.yml`
- `docs/design/source-matrix/cards/TCG-001.yml`
- `docs/design/source-matrix/cards/TUF-001.yml`
- `docs/design/source-matrix/cards/X64-AMD-001.yml`
- `docs/design/source-matrix/cards/X64-INTEL-001.yml`
- `docs/design/source-matrix/cards/X64-LINUX-CET-001.yml`
- `docs/design/source-matrix/cards/X64-LINUX-PKU-001.yml`

## Schema Update

Created `schemas/source-card.schema.json` as an executable JSON Schema for the
current index and source-card shape. The schema preserves the local v1 card
requirements and keeps URL, source reference, requirement reference,
verification reference, negative-test, gap, and compatibility-inference fields
structured.
