# ci/

CI and local lint gates. The first checks are implemented as local scripts in
`scripts/` and can later be wired into CI workflows.

Required gate families:

- source-card validation
- requirement validation
- no fake success
- prohibited compatibility wording
- audit-obligation coverage
- fuzz-target registration
- Japanese canonical conflict detection

