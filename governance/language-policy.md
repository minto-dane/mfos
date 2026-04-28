# Language Policy

English is canonical for:

- machine-readable keys
- IDs
- enum values
- error codes
- ABI names
- normative requirement text

Japanese documents are explanatory mirrors unless a reviewed bilingual parity
process marks a specific artifact otherwise. If an English canonical artifact
and Japanese commentary conflict, the English canonical artifact wins.

## Japanese Mirror Status

Japanese mirror completeness is tracked by machine-readable registries:

- `docs/design/ja/translation-units.yaml`
- `docs/design/ja/sync-status.yaml`

The repository MUST NOT claim a complete Japanese mirror while
`japanese_mirror_status: incomplete` or `complete_mirror_claimed: false` is
present in `docs/design/ja/sync-status.yaml`.

Japanese prose is explanatory by default. A Japanese artifact can be treated as
synchronized only when the matching translation unit is marked `current` from
the current English source hash and has passed semantic review. Japanese text
MUST NOT add, remove, weaken, or strengthen normative semantics. Any semantic
correction found during Japanese review MUST first be made in the English
canonical artifact.

Machine-readable keys, IDs, enum values, ABI names, state names, error codes,
and registry fields remain English even inside Japanese documents.
