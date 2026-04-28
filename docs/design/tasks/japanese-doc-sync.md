# Japanese Documentation Synchronization Task Plan

Status: Draft task plan

## 1. Purpose

This task plan defines the work needed to implement complete Japanese auxiliary documentation for MFOS without allowing Japanese text to diverge from English canonical specifications.

## 2. Owned Scope

This plan covers:

- translation unit manifest design
- source hash generation
- Japanese mirror index maintenance
- CI/lint implementation
- translation workflow
- stale-unit reporting
- release documentation gates

This plan does not translate the full documentation set.

## 3. Inputs

- `docs/design/specs/32-language-localization.md`
- `docs/design/ja/README.md`
- `docs/design/ja/SYNC-POLICY.md`
- all English canonical Markdown documents under `docs/design`, excluding the `docs/design/ja` mirror subtree
- machine-readable registries under `docs/design/registries`
- source matrix cards and registries

## 4. Outputs

Planned outputs:

- `docs/design/ja/translation-units.yaml`
- `docs/design/ja/sync-status.yaml`
- `ci/language-lint/`
- stale Japanese unit report
- complete Japanese mirror tree under `docs/design/ja/`

The output paths are planned and not implemented by this task.

## 5. Task Breakdown

| Task ID | Task | Status | Notes |
| --- | --- | --- | --- |
| JA-SYNC-001 | Define language/localization canonical specification. | done | Implemented by `32-language-localization.md`. |
| JA-SYNC-002 | Create initial Japanese documentation entry point. | done | Implemented by `docs/design/ja/README.md`. |
| JA-SYNC-003 | Create Japanese synchronization policy. | done | Implemented by `docs/design/ja/SYNC-POLICY.md`. |
| JA-SYNC-004 | Define translation unit manifest schema. | pending | Should include TU IDs, canonical path, source anchor, source hash, mirror path, mirror anchor, status. |
| JA-SYNC-005 | Implement source hash generator. | pending | Must use normalized UTF-8/LF/trailing-whitespace rules. |
| JA-SYNC-006 | Implement mirror coverage scanner. | pending | Must find in-scope English Markdown files and verify mirror entries. |
| JA-SYNC-007 | Implement ID preservation lint. | pending | Must preserve requirement IDs, source IDs, test IDs, evidence IDs, error codes, state names, enum values. |
| JA-SYNC-008 | Implement normative keyword semantic lint. | pending | Must detect deleted or added `MUST`, `MUST NOT`, `SHOULD`, `MAY`, `UNSUPPORTED`, `SPEC_GAP`, `FAIL-CLOSED`. |
| JA-SYNC-009 | Implement machine-readable key lint. | pending | Must preserve YAML/JSON/TOML keys and schema code blocks. |
| JA-SYNC-010 | Implement high-risk semantic lint. | pending | Must block drift in authorization, audit, dataset handle, update, PXM teardown, AMF, Guard, profile semantics. |
| JA-SYNC-011 | Create stale-unit report. | pending | Must show source hash mismatch and affected mirror path. |
| JA-SYNC-012 | Create Japanese mirror directories. | pending | `ja/specs`, `ja/source-matrix`, `ja/tasks`, `ja/assurance`, `ja/packs`, `ja/prompts`, `ja/registries`. |
| JA-SYNC-013 | Translate core governance docs. | pending | Start with `00`, `01`, `02`, `03`, `21`, `23`, `28`, `32`. |
| JA-SYNC-014 | Translate security-critical specs. | pending | `06`, `07`, `08`, `13`, `16`, `17`. |
| JA-SYNC-015 | Translate remaining specs and indexes. | pending | Complete all in-scope docs. |
| JA-SYNC-016 | Add release gate for complete Japanese documentation claim. | pending | Must block claim while any unit is missing, partial, stale, or blocked. |

## 6. Translation Unit Manifest Draft

Draft schema:

```yaml
schema_version: 1
canonical_language: en
mirror_language: ja
generated_at: "2026-04-27T00:00:00Z"
documents:
  - canonical_path: docs/design/specs/32-language-localization.md
    mirror_path: docs/design/ja/specs/32-language-localization.md
    document_status: missing | partial | current | stale | blocked
    translation_units:
      - tu_id: TU-SPEC-32-0001
        source_anchor: "1. Purpose"
        source_hash_algorithm: sha256
        source_hash: sha256:<hex>
        mirror_anchor: "1. 目的"
        mirror_hash_algorithm: sha256
        mirror_hash: sha256:<hex>
        status: missing | partial | current | stale | blocked
        reviewer: null
```

## 7. CI Gate Draft

`language-lint` MUST fail when:

- a Japanese mirror claims `current` with a stale source hash
- a Japanese unit changes normative strength
- a Japanese unit drops a requirement ID or source ID
- a Japanese unit changes an error code or state name
- a Japanese unit changes machine-readable keys
- a Japanese unit adds an IBM product compatibility claim
- a Japanese unit changes audit obligations
- a Japanese unit changes fail-closed behavior
- a Japanese unit changes profile applicability

`language-lint` MAY warn when:

- a mirror path is planned but missing during early migration
- a translator note lacks a linked TU ID
- heading hierarchy differs in a non-normative section

## 8. Update Workflow

For every English canonical change:

1. Recompute source hashes for changed translation units.
2. Mark matching Japanese units stale.
3. Update stale Japanese units from the current English source.
4. Run `language-lint`.
5. Review high-risk semantic areas manually.
6. Mark translated units current.

For Japanese-only clarity edits:

1. Verify no semantic keywords, IDs, keys, code blocks, state names, or error names changed.
2. Keep source hash fixed.
3. Run `language-lint`.
4. Record as translation-only.

## 9. High-Risk Review Areas

Japanese synchronization MUST receive strict review for:

- catalogd committed-entry behavior
- audit before-return behavior
- securityd central decision behavior
- dataset handle binding
- update rollback/freeze/mix-and-match behavior
- PXM device teardown
- AMF disabled-by-default and production enablement boundaries
- Guard root transitions
- Enterprise profile boundaries
- High-Assurance claims

## 10. Gaps

- Translation unit manifest is not implemented.
- Source hash generator is not implemented.
- CI/language-lint is not implemented.
- Complete Japanese mirror tree is not created.
- No Japanese semantic reviewer roster exists.
- No release gate is wired to translation status yet.
