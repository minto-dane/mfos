# Repository Information Architecture Open Issues

Status: current.

- Fixture and golden indexes remain directory-level inventories; per-artifact
  manifests can be added later without changing test semantics.
- Evidence traceability generated/current drift should be addressed by a
  generator `--check` mode in a follow-up.
- Docs/design registry envelope normalization should be handled as a dedicated
  registry governance PR.
- Japanese mirrors remain incomplete and explanatory even though source hashes
  were refreshed.
- Formal/TLA metadata can be deepened in a follow-up boundary metadata pass.
- The repository information architecture migration map contains a duplicate
  destination for `reports/current/dafny/policy-denial-error-taxonomy.md`; one
  entry references a non-base `reports/current/policy/` source.
- `ai/outputs` is explicitly untrusted by README and ignore policy, but a child
  `.mfos-dir.yml` would make the non-canonical boundary machine-readable.
- Script flat-directory pressure outside `reports/current` is currently a
  warning in draft-mode validation; release mode still fails warnings.
