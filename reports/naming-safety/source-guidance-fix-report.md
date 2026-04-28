# Source Guidance Fix Report

Date: 2026-04-27

## Scope

Addressed red-team findings:

- NSRT-MAJ-001: stale Source Card guidance still described old
  `source_type: normative`, `title`, `url`, and `canonical_concepts` shape, and
  treated Source Cards as summaries.
- NSRT-MAJ-003: non-IBM external mark controls were incomplete for external
  vendors, projects, products, and specifications.

No production code was changed.

## Changes

- Updated `NOTICE.md` with generic external-name notice language for Microsoft,
  Windows, Hyper-V, Intel, Intel 64, IA-32, AMD, AMD64, Linux, Trusted Computing
  Group, TCG, TPM, The Update Framework, TUF, SLSA, seL4, NIST, and other
  external names.
- Kept the IBM migration language intact: IBM references remain bibliographic
  only, and MFOS still disclaims compatibility with IBM products, interfaces,
  record layouts, command syntax, macro interfaces, and documentation.
- Updated `sources/citation-policy.md` to state that Source Cards are
  public-safe bibliographic and traceability records, not summaries,
  substitute documentation, copied tables, diagrams, record layouts, command
  syntax, macro signatures, or message tables.
- Updated `docs/design/mfos-design.md` Source Policy and Source Matrix guidance
  to use the current Source Card shape:
  `source_kind`, `source_type: external_reference`, `semantic_role`,
  `document_title`, `document_url`, `review_topics`, `mfos_mapping`,
  `legal_controls`, `source_refs`, and `requirement_refs`.
- Removed stale source-summary prompt wording and stale normative-source table
  wording from the owned Source Card guidance area.
- Updated `docs/design/source-matrix/source-lint-spec.md` so lint policy rejects
  removed public fields and requires external-reference cards using external
  names to set both:
  `vendor_mark_used: true` and
  `legal_controls.trademark_reference_only: true`.
- Corrected the stale lint freshness path from
  `mfos_mapping.semantic_overlap` to current `mfos_mapping` plus
  `mfos_divergence`.
- Updated non-IBM external Source Cards for Microsoft, NIST, seL4, SLSA, TCG,
  TUF, AMD, Intel, and Linux kernel documentation so external mark controls are
  reference-only.

## Validation

Commands run from `/home/nia/mfos`:

```text
rg -n "source_type:\s*normative|source_type: normative|canonical_concepts|short summaries|source summary|SOURCE_SUMMARY|mfos_mapping\.semantic_overlap" NOTICE.md docs/design/mfos-design.md sources/citation-policy.md docs/design/source-matrix/source-lint-spec.md docs/design/source-matrix/cards sources/source-card.schema.yml docs/design/source-matrix/source-card-schema.md -S
```

Result: no stale `source_type: normative`, short-summary guidance,
`SOURCE_SUMMARY`, source-summary wording, or `mfos_mapping.semantic_overlap`
references remain in the owned guidance. Remaining `canonical_concepts` hits are
only in schema/lint removed-field lists.

```text
python3 - <<'PY'
import glob, yaml
for path in sorted(glob.glob('docs/design/source-matrix/cards/*.yml')):
    with open(path, 'r', encoding='utf-8') as f:
        yaml.safe_load(f)
with open('docs/design/source-matrix/source-matrix.yml', 'r', encoding='utf-8') as f:
    yaml.safe_load(f)
print('yaml ok')
PY
```

Result: `yaml ok`.

```text
python3 - <<'PY'
import glob, yaml
bad=[]
for path in sorted(glob.glob('docs/design/source-matrix/cards/*.yml')):
    with open(path, encoding='utf-8') as f:
        d=yaml.safe_load(f)
    if d.get('source_type') == 'external_reference':
        if d.get('vendor_mark_used') is not True or d.get('legal_controls',{}).get('trademark_reference_only') is not True:
            bad.append((path,d.get('source_id'),d.get('vendor_mark_used'),d.get('legal_controls',{}).get('trademark_reference_only')))
print('external mark control gaps:', len(bad))
for item in bad:
    print(item)
PY
```

Result: `external mark control gaps: 0`.

```text
rg -n "vendor_mark_used: false|trademark_reference_only: false" docs/design/source-matrix/cards -S
```

Result: remaining false values are only in
`docs/design/source-matrix/cards/FBVBS-001.yml`, which is
`source_type: internal_transfer` and `vendor: MFOS internal`.

## Residual Notes

- Ruby was not installed, so YAML validation used Python `yaml`.
- This pass did not edit production code or unrelated source-matrix content.
