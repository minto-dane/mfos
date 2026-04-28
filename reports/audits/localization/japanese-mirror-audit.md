# Japanese Mirror Audit

Status: Draft audit record

Date: 2026-04-27

## Scope

This audit advances Japanese mirror mechanics without translating large
specifications and without changing canonical English semantics.

Owned paths updated:

- `docs/design/ja/translation-units.yaml`
- `docs/design/ja/sync-status.yaml`
- `governance/language-policy.md`
- `reports/audits/localization/japanese-mirror-audit.md`

`docs/design/language-policy.md` does not exist and was not created in this
change.

## Findings

The repository has 60 in-scope canonical English Markdown documents under
`docs/design`, excluding the `docs/design/ja` subtree.

The Japanese mirror tree currently has two Markdown files:

- `docs/design/ja/README.md`
- `docs/design/ja/SYNC-POLICY.md`

Both are treated as partial explanatory artifacts, not complete synchronized
mirrors.

## Changes Made

`docs/design/ja/translation-units.yaml` was expanded from a small seed list to
a document-level translation unit manifest covering all 60 in-scope canonical
English Markdown documents.

Each unit now records:

- `unit_id`
- `canonical_path`
- `canonical_hash`
- `japanese_path`
- `existing_japanese_paths`
- `mirror_role`
- `sync_status`
- `semantic_sync_required`
- `japanese_may_override_canonical`
- `source_hash_status`
- `translation_scope`

`docs/design/ja/sync-status.yaml` was updated to schema version 2 and now
records:

- English canonical authority
- Japanese explanatory role
- incomplete mirror status
- no complete Japanese mirror claim
- Phase 0.7 nonblocking status
- production release documentation blocking status
- unit summary counts
- required next actions

`governance/language-policy.md` now points to the machine-readable Japanese
mirror registries and states that complete Japanese mirror status must not be
claimed while the sync status remains incomplete.

## Machine-Readable Status

```yaml
japanese_mirror_status: incomplete
complete_mirror_claimed: false
canonical_markdown_units: 60
current_units: 0
partial_units: 2
missing_units: 58
stale_units: 0
blocked_units: 0
large_spec_translation_included: false
```

## Remaining Gaps

- Complete Japanese mirror tree is not created.
- Document-level hashes are recorded, but section-level translation unit
  extraction is not implemented.
- Language lint is not wired into CI.
- Japanese mirrors have not been semantically reviewed as complete
  translations.

## Implementation Decision

No production implementation was started.

Japanese mirrors remain explanatory unless a unit is explicitly marked
`current` from the current English source hash and has passed semantic review.
