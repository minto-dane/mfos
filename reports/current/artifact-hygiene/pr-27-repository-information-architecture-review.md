# PR 27 Repository Information Architecture Review

Status: current.

## Scope

Reviewed PR #27 (`docs/repository-information-architecture-refactor`) against
`origin/dev` for report-domain sharding, current-report lifecycle boundaries,
index and migration integrity, artifact-hygiene validators, script namespace
ownership, AI-output trust boundaries, build-directory policy, pack bridge
ownership, evidence/test indexes, and Phase 1.4 boundary preservation.

PR #27 is open, non-draft, and GitHub reports clean merge state and passing
remote checks. The remaining merge blockers were remediated by adding
metadata-only build enforcement and reports/current lifecycle metadata
validation.

## Final Judgment

```yaml
pr_27_merge_allowed: true
critical_findings_remaining: false
major_findings_remaining: false
reports_current_domain_sharding_valid: true
migration_map_complete: true
validators_prevent_regression: true
ai_outputs_noncanonical: true
build_directory_policy_safe: true
phase_1_4_planning_only_preserved: true
production_boundary_violated: false
reports_current_lifecycle_metadata_enforced: true
```

## Remediated Findings

1. Build-directory policy is now safe against accidental committed outputs.

   `build/` remains a metadata-only policy root. `build/.gitignore` now ignores
   generated output by default and allows only root metadata files. The new
   `scripts/checks/artifact-hygiene/check-build-directory-policy.py` validator
   checks `git ls-files -- build` and fails tracked files outside the explicit
   metadata allowlist, with direct rejection for likely output paths including
   `build/toolchains/`, `build/profiles/`, `build/qemu/`,
   `build/hardware-lab/`, `build/images/`, `build/cache/`, `build/tmp/`, and
   `build/out/`.

2. Current-report lifecycle metadata is now enforced even when artifacts are
   indexed.

   `reports/current/.mfos-dir.yml` forbids archived or superseded reports
   (`reports/current/.mfos-dir.yml:27`), and each domain index declares
   `archive_reports_allowed: false`. The new
   `scripts/checks/artifact-hygiene/check-reports-current-lifecycle-metadata.py`
   validator rejects current-domain artifact-level `status`, `lifecycle`,
   `lifecycle_status`, `artifact_lifecycle`, `artifact_status`, or
   `phase_status` values that indicate archive, archived, superseded,
   generated, historical, phase-specific, migration-only, or phase-like
   lifecycle state. It also checks Markdown `Status:` lines, domain-index root
   metadata, domain-index policy lifecycle metadata, and per-artifact
   `status`/`lifecycle` entries.

## Minor Findings

1. The migration map has a spurious duplicate destination.

   `reports/current/repository-information-architecture-migration.yml:383`
   correctly maps `reports/current/policy-denial-error-taxonomy.md` to
   `reports/current/dafny/policy-denial-error-taxonomy.md`. A later entry at
   `reports/current/repository-information-architecture-migration.yml:712`
   maps non-base path
   `reports/current/policy/policy-denial-error-taxonomy.md` to the same
   destination. No moved file is missing from the migration map, but the extra
   entry makes the map less precise.

2. `ai/outputs` is clearly untrusted, but the non-canonical marker is inferred.

   `ai/outputs/DO_NOT_TRUST_WITHOUT_REVIEW.md:3` says AI output is untrusted
   until reviewed, traced, and validated, and lines 6-9 block Phase 1.4,
   production, Rust semantic-core, hosted daemon, semantic-runner, and generated
   production-code authorization. The parent `ai/.mfos-dir.yml:6` remains
   canonical for AI workflow artifacts while line 7 states AI outputs are not
   implementation evidence or ownership. This is sufficient for the review
   boolean, but a child `ai/outputs/.mfos-dir.yml` would remove ambiguity.

3. Script flat-directory pressure outside `reports/current` is warning-only in
   normal draft validation.

   `reports/current` flat-root regression is blocked. The separate
   `scripts/checks` and `scripts/validators` direct-file baselines are warnings
   unless run in release mode, so they are useful pressure signals but not hard
   PR gates.

## Passed Checks

- `reports/current` is domain-sharded through stable directories listed in
  `reports/current/index.yml:6`, and the top level contains only navigation
  metadata plus the four repository-information-architecture root artifacts.
- Domain directories have `README.md`, `.mfos-dir.yml`, and `index.yml`
  metadata. The smallest current domains still contain two non-metadata
  artifacts, so no unjustified one-file domain was introduced.
- `reports/index.yml`, `reports/current/index.yml`, and domain indexes had no
  broken required paths in the reviewed tree.
- Existing moved current reports are covered by the migration map; the duplicate
  migration entry above is precision debt, not missing coverage.
- Script namespace ownership is clear. Root `scripts/` entrypoints are indexed
  as canonical entrypoints or thin wrappers, and Python wrapper thinness is
  enforced.
- Build output regression is blocked by `build/.gitignore` and
  `check-build-directory-policy.py`.
- Reports/current archive, superseded, generated, historical, phase-specific,
  and migration-only lifecycle metadata is blocked by
  `check-reports-current-lifecycle-metadata.py` without scanning report prose.
- `packs/` is clearly a bridge: `packs/.mfos-dir.yml:3` marks role `bridge`,
  `packs/.mfos-dir.yml:6` marks it non-canonical, and
  `packs/pack-index.yml:5` declares `docs/design/packs` as canonical source.
- Evidence traceability, fixture, golden, fuzz corpus, and formal TLA indexes
  have valid paths for the reviewed current/generated coverage.
- Phase 1.4 remains planning-only. `docs/design/STATUS.md:88` records planning
  complete with implementation not started, and `docs/design/STATUS.md:195`
  states that no Phase 1.4 semantics, generated Phase 1.4 traceability,
  production code, Rust semantic-core, hosted daemons, semantic-runner commands,
  or `jobd`/`spoold`/`operatord` behavior were introduced.

## Validation

Local validation passed on 2026-05-01:

- `./scripts/validate-all.sh --check`: pass
- `./scripts/validate-naming-safety.sh release`: pass
- `./scripts/validate-artifact-hygiene.sh`: pass
- `./scripts/validate-component-scaffold.sh`: pass
- `./scripts/validate-language-formal-assurance.sh`: pass
- `./scripts/validate-dafny-semantics.sh --require-dafny`: pass,
  `136 verified, 0 errors`
- `python3 -m py_compile $(find scripts tools -name '*.py' -type f | sort)`:
  pass
- `git diff --check`: pass
