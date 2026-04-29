# ci/

CI and local lint gates. The executable validators live under `scripts/`; this
directory records CI-facing policy and future linter scaffolds. Current GitHub
Actions invoke `./scripts/validate-all.sh --check` plus focused gates for
component scaffold and Dafny policy validation.

Required gate families:

- source-card validation
- requirement validation
- no fake success
- prohibited compatibility wording
- audit-obligation coverage
- fuzz-target registration
- Japanese canonical conflict detection
