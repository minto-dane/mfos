# Directory Ownership Audit

Status: current.

This audit classifies duplicate or overlapping repository roots. No production
or Phase 1.4 implementation was introduced.

## Findings

| Path A | Path B | Canonical owner | Noncanonical role | Risk | Action |
| --- | --- | --- | --- | --- | --- |
| `implementation/services/` | `services/` | `implementation/services/` | retired/absent | Low | Keep top-level `services/` absent; future code belongs under `implementation/services/` after a reviewed gate. |
| `implementation/nucleus/` | `nucleus/` | `implementation/nucleus/` | retired/absent | Low | Keep top-level `nucleus/` absent and forbid implementation code before gate approval. |
| `implementation/pxm/` | `pxm/` | `implementation/pxm/` | retired/absent | Low | Keep top-level `pxm/` absent and forbid implementation code before gate approval. |
| `implementation/guard/` | `guard/` | `implementation/guard/` | retired/absent | Low | Keep top-level `guard/` absent and forbid implementation code before gate approval. |
| `tools/` | `implementation/tools/` | `tools/` for current validation tooling | future MFOS product/admin tools | Medium | Clarify README and metadata. |
| `formal/executable-semantics/dafny/` | executable-spec class | Dafny source root | no executable-spec implementation root | Medium | Keep executable-spec as artifact class, not a duplicate root. |
| `docs/design/source-matrix/` | `source-matrix/`, `sources/` | `docs/design/source-matrix/` | bridge/workbench | High | Require ADR and parity before migration. |
| `docs/design/specs/` | `specs/` | `docs/design/specs/` | bridge | Medium | Forbid parallel normative specs. |
| `docs/design/packs/` | `packs/` | `docs/design/packs/` | bridge/review aid | Medium | Metadata clarifies canonical pack contracts. |
| `docs/design/prompts/ai-prompts.md` | `prompts/`, `ai/` | design prompt document | bridge/workflow artifacts | Medium | Metadata clarifies prompt ownership. |
