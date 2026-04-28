---
spec_id: "MFOS-SPEC-32-LANGUAGE-LOCALIZATION"
title: "MFOS Language and Localization Synchronization v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "NIST-160-001", "NIST-218-001"]
requirement_refs: ["MFOS-REQ-LANG-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Language and Localization Synchronization v0.1

Status: Draft specification

## 1. Purpose

This document defines the MFOS v0.5 language policy and Japanese documentation synchronization mechanism.

MFOS uses English as the canonical specification language. Japanese documentation is required as a complete auxiliary mirror for review and implementation support, but Japanese text must not create, remove, weaken, strengthen, or otherwise change normative semantics.

This document exists to prevent divergence between English canonical specifications, Japanese review material, and machine-readable registries.

## 2. Scope

In scope:

- canonical language rules
- Japanese auxiliary mirror rules
- conflict resolution
- machine-readable key language
- translation unit IDs
- source hash checks
- synchronization status records
- CI and lint rules
- update workflow
- initial Japanese documentation index

Out of scope:

- translating all MFOS documents in this change
- localizing enum names, ABI names, error codes, requirement IDs, source IDs, test IDs, evidence IDs, YAML keys, or file identifiers
- allowing Japanese text to override English canonical semantics
- claiming compatibility with IBM products

## 3. Canonical Language Policy

### 3.1 English canonical

English is the canonical language for MFOS normative specifications.

The following artifacts MUST be authored and reviewed in English as canonical content:

- normative specification text
- requirement IDs and normative requirement text
- Source Matrix IDs and Source Card keys
- object model field names
- enum values
- error codes
- ABI names
- interface IDs
- state names
- test IDs
- evidence IDs
- registry schemas
- CI lint rule IDs
- release claims

### 3.2 Japanese auxiliary mirror

Japanese documents are required as a complete auxiliary mirror for human review, planning, and implementation support.

Japanese mirror documents MUST preserve the canonical English meaning, structure, IDs, examples, and code blocks. Japanese text MAY clarify intent for Japanese readers only when the clarification is marked as explanatory and does not change normative semantics.

Japanese documents MUST NOT introduce new normative behavior. If a Japanese reviewer finds ambiguity or a necessary semantic correction, the English canonical document MUST be patched first.

### 3.3 Conflict rule

If English canonical content and Japanese mirror content conflict, the English canonical content wins.

The conflicting Japanese translation unit MUST be marked stale or blocked until it is corrected from the current English source hash.

### 3.4 Machine-readable keys

Machine-readable keys MUST remain in English ASCII unless an existing external standard requires otherwise.

This rule applies to:

- YAML keys
- JSON keys
- TOML keys
- registry fields
- enum values
- requirement IDs
- source IDs
- test IDs
- evidence IDs
- state names
- error names
- ABI call names
- CLI command identifiers

Japanese translations MAY translate prose descriptions, but MUST preserve all machine-readable keys exactly.

## 4. Japanese Mirror Requirement

Every canonical English Markdown document under `docs/design`, excluding the `docs/design/ja` mirror subtree, MUST have a corresponding Japanese mirror document unless the document is explicitly classified as machine-readable, generated, binary, or non-translatable.

The mirror path MUST be derived by inserting `ja/` after `docs/design/`.

Examples:

| English canonical path | Japanese mirror path |
| --- | --- |
| `docs/design/README.md` | `docs/design/ja/README.md` |
| `docs/design/specs/00-normative-language.md` | `docs/design/ja/specs/00-normative-language.md` |
| `docs/design/source-matrix/source-matrix.md` | `docs/design/ja/source-matrix/source-matrix.md` |
| `docs/design/tasks/implementation-roadmap.md` | `docs/design/ja/tasks/implementation-roadmap.md` |

Machine-readable YAML registries are not translated. Their prose-facing summaries MAY have Japanese mirrors, but their keys and values that are IDs, enums, or schema fields remain English canonical.

MFOS MUST NOT claim a complete Japanese documentation set until every in-scope mirror document exists, has current source hashes, and passes semantic lint.

## 5. Translation Units

Japanese synchronization is managed through translation units.

A translation unit is the smallest stable prose block tracked for synchronization. A translation unit SHOULD normally be one section, subsection, requirement row, table row, or fenced example block.

Translation unit IDs use this format:

```text
TU-<DOC-ID>-<NNNN>
```

Examples:

```text
TU-SPEC-00-0001
TU-SPEC-32-0010
TU-TASK-JA-SYNC-0004
```

Each mirror document MUST contain translation metadata in a front matter block or synchronization manifest. The preferred front matter shape is:

```yaml
---
language: ja
canonical_language: en
canonical_path: docs/design/specs/32-language-localization.md
mirror_path: docs/design/ja/specs/32-language-localization.md
sync_status: current | stale | partial | blocked | missing
translation_scope: complete | partial
source_revision: unknown
source_hash_algorithm: sha256
translation_units:
  - tu_id: TU-SPEC-32-0001
    source_path: docs/design/specs/32-language-localization.md
    source_anchor: "1. Purpose"
    source_hash: sha256:<hex>
    mirror_anchor: "1. 目的"
    mirror_hash: sha256:<hex>
    status: current | stale | blocked
---
```

The source hash MUST be computed from canonical English normalized content. Normalization MUST:

- use UTF-8
- normalize line endings to LF
- trim trailing whitespace
- preserve code blocks exactly
- preserve requirement IDs, source IDs, registry keys, enum values, error codes, and state names exactly

## 6. Semantic Preservation Rules

Japanese translation units MUST preserve these semantic controls exactly:

- normative keywords: `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, `MAY`, `REQUIRED`, `OPTIONAL`, `PROHIBITED`, `UNSUPPORTED`, `SPEC_GAP`, `FAIL-CLOSED`, `FAIL-SECURE`
- requirement IDs
- source IDs
- profile names
- status values
- object names
- state names
- error codes
- API and ABI identifiers
- table row counts for normative tables
- ordered-list item counts for normative procedures
- code blocks and schemas

Japanese prose MAY translate the human-readable explanation of normative keywords, but MUST retain the English keyword next to the Japanese explanation when the keyword is normative.

Example:

```text
MUST（必須）
MUST NOT（禁止）
SHOULD（推奨）
MAY（任意）
```

Japanese translation units MUST NOT:

- weaken `MUST` into `SHOULD` or `MAY`
- strengthen `MAY` into `MUST`
- remove fail-closed behavior
- add success behavior not present in English
- add a new exception to authorization, audit, update, Guard, PXM, AMF, or dataset rules
- change profile applicability
- change error results
- change audit timing
- change source grounding
- add compatibility claims with IBM products

## 7. Synchronization Mechanism

The synchronization mechanism has four records:

1. Canonical document manifest
2. Japanese mirror manifest
3. Translation unit source hashes
4. CI lint result

The canonical manifest records the current English documents and their translation unit hashes.

The Japanese mirror manifest records the Japanese mirror documents and the canonical source hashes used for translation.

When English canonical content changes:

1. The changed translation units receive new source hashes.
2. The corresponding Japanese translation units become stale.
3. CI reports stale Japanese units but does not permit silent drift.
4. A translator or documentation agent updates the Japanese unit from the current English unit.
5. CI verifies preserved IDs, preserved normative keywords, and unchanged machine-readable blocks.
6. The Japanese unit returns to `current`.

Japanese-only edits are allowed only for:

- grammar
- typography
- reader clarity
- translation correction
- explanatory translator notes marked non-normative

Japanese-only edits that change semantics MUST be rejected by CI and converted into an English canonical patch request.

## 8. CI and Lint Rules

### 8.1 Required lint checks

| Rule ID | Severity | Rule |
| --- | --- | --- |
| LANG-LINT-0001 | ERROR | Every in-scope English Markdown file MUST have a Japanese mirror entry in the synchronization manifest. |
| LANG-LINT-0002 | ERROR | Every Japanese mirror MUST name its canonical English path. |
| LANG-LINT-0003 | ERROR | Translation unit IDs MUST be unique within the repository. |
| LANG-LINT-0004 | ERROR | A Japanese translation unit with a mismatched source hash MUST be marked stale or blocked. |
| LANG-LINT-0005 | ERROR | Japanese mirrors MUST preserve requirement IDs, source IDs, test IDs, evidence IDs, and error codes exactly. |
| LANG-LINT-0006 | ERROR | Japanese mirrors MUST preserve fenced code blocks containing schemas, ABI layouts, registry examples, command IDs, or error names exactly unless the block is explicitly marked translatable prose. |
| LANG-LINT-0007 | ERROR | Japanese mirrors MUST NOT introduce normative keywords absent from the matching English translation unit. |
| LANG-LINT-0008 | ERROR | Japanese mirrors MUST NOT remove normative keywords present in the matching English translation unit. |
| LANG-LINT-0009 | ERROR | Japanese mirrors MUST NOT alter profile applicability. |
| LANG-LINT-0010 | ERROR | Japanese mirrors MUST NOT alter audit obligations or fail-closed conditions. |
| LANG-LINT-0011 | ERROR | Japanese mirrors MUST NOT introduce compatibility claims with IBM products. |
| LANG-LINT-0012 | WARN | Japanese mirrors SHOULD preserve heading hierarchy and table row counts. |
| LANG-LINT-0013 | WARN | Translator notes SHOULD be linked to a translation unit ID. |
| LANG-LINT-0014 | ERROR | Machine-readable keys MUST remain English. |
| LANG-LINT-0015 | ERROR | Japanese semantic corrections MUST reference an English canonical patch or ADR. |

### 8.2 Semantic risk checks

The linter MUST treat changes to these areas as security-sensitive:

- catalogd committed-entry rules
- audit before-return rules
- securityd decision rules
- dataset handle binding
- update rollback, freeze, and mix-and-match behavior
- PXM device teardown
- AMF production enablement
- Guard root transitions
- profile boundaries
- fail-closed behavior

Japanese translation drift in these areas MUST block release documentation until corrected.

## 9. Update Workflow

### 9.1 English-first normative change

Normative changes use this workflow:

1. Patch the English canonical document.
2. Update requirement, source, test, and evidence registries if applicable.
3. Regenerate translation unit source hashes.
4. Mark affected Japanese units stale.
5. Translate affected units.
6. Run language lint.
7. Review Japanese output for semantic preservation.
8. Mark units current.

### 9.2 Japanese reviewer finds a semantic issue

If a Japanese reviewer finds a semantic issue:

1. File a canonical English change request.
2. Do not patch Japanese semantics directly.
3. Patch the English canonical document.
4. Apply the normal English-first workflow.

### 9.3 Japanese-only clarity update

Japanese-only clarity updates use this workflow:

1. Edit only Japanese prose.
2. Preserve translation unit IDs and canonical source hashes.
3. Do not modify machine-readable keys or code blocks.
4. Run language lint.
5. Record the update as translation-only.

## 10. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-LANG-0001 | MFOS normative specifications MUST use English as the canonical language. | documentation review / spec lint |
| MFOS-REQ-LANG-0002 | Japanese documents MUST be auxiliary mirrors and MUST NOT override English canonical semantics. | documentation review / language lint |
| MFOS-REQ-LANG-0003 | Machine-readable keys, IDs, enum values, state names, ABI names, and error codes MUST remain English. | automated lint |
| MFOS-REQ-LANG-0004 | Every in-scope English Markdown document under `docs/design` MUST have a Japanese mirror entry. | language lint |
| MFOS-REQ-LANG-0005 | Japanese mirrors MUST use translation unit IDs and source hashes to track synchronization. | language lint |
| MFOS-REQ-LANG-0006 | Japanese mirrors with stale source hashes MUST NOT be presented as current. | CI gate |
| MFOS-REQ-LANG-0007 | Japanese mirrors MUST preserve normative keywords, requirement IDs, source IDs, audit obligations, profile applicability, and failure modes. | semantic lint / review |
| MFOS-REQ-LANG-0008 | Japanese semantic corrections MUST be made by first patching English canonical content. | review checklist |
| MFOS-REQ-LANG-0009 | MFOS MUST NOT claim a complete Japanese documentation set until all in-scope mirrors are current. | release review |
| MFOS-REQ-LANG-0010 | Language lint MUST block Japanese text that changes authorization, audit, dataset handle, update, PXM teardown, AMF, Guard, or profile semantics. | CI gate |

## 11. Positive Tests

PT-LANG-001:

A Japanese mirror with matching translation unit source hashes and preserved requirement IDs passes language lint.

PT-LANG-002:

A Japanese-only typo correction that does not alter IDs, normative keywords, code blocks, or source hashes passes translation-only review.

PT-LANG-003:

A changed English translation unit marks the corresponding Japanese unit stale until retranslated.

PT-LANG-004:

A Japanese mirror preserving English YAML keys while translating descriptions passes machine-readable-key lint.

## 12. Negative Tests

NT-LANG-001:

A Japanese mirror changes `MUST` to a weaker obligation and fails semantic lint.

NT-LANG-002:

A Japanese mirror adds a new exception to an authorization rule and fails semantic lint.

NT-LANG-003:

A Japanese mirror removes a before-return audit obligation and fails semantic lint.

NT-LANG-004:

A Japanese mirror changes an error code from `MFOS_ERR_POLICY_DENIED` to success and fails semantic lint.

NT-LANG-005:

A Japanese mirror introduces an IBM product compatibility claim and fails release lint.

NT-LANG-006:

A Japanese mirror has a mismatched source hash but claims `sync_status: current` and fails CI.

## 13. Spec Gaps

SPEC-GAP-LANG-0001:

The canonical translation unit manifest file path and schema are not yet implemented.

SPEC-GAP-LANG-0002:

The language lint implementation is not yet implemented.

SPEC-GAP-LANG-0003:

The complete Japanese mirror set is not yet translated.

SPEC-GAP-LANG-0004:

The exact normalized hashing algorithm needs a reference implementation.

SPEC-GAP-LANG-0005:

The reviewer assignment model for Japanese semantic review is not yet defined.

## 14. AI Prompt

Use this prompt when asking an AI agent to update MFOS Japanese documentation:

```text
You are updating MFOS Japanese mirror documentation.

Rules:
- English canonical specifications are authoritative.
- Japanese text is auxiliary and must not change semantics.
- Preserve all requirement IDs, source IDs, test IDs, evidence IDs, enum values, state names, error codes, ABI names, and machine-readable keys exactly.
- Preserve normative keywords or show them with Japanese explanation, such as MUST（必須）.
- Do not introduce compatibility claims with IBM products.
- If a semantic correction is needed, stop and produce an English canonical patch request.
- Track translation unit IDs.
- Record source hashes.
- Mark stale units as stale until translated from the current English source.
- Do not translate all docs unless explicitly assigned; update only the requested mirror units.

Output:
1. Canonical files used
2. Japanese files changed
3. Translation unit IDs changed
4. Source hashes updated
5. Semantic changes requested for English canonical specs
6. Lint results
7. Remaining stale units
```
