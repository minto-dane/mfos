# Top-Level Implementation Bridge Retirement Review

Status date: 2026-05-01

Scope: verify retirement of top-level `services/`, `nucleus/`, `pxm/`, and
`guard/` bridges and confirm `implementation/*` is now the only canonical future
implementation location for those components.

## Final Judgment

```yaml
top_level_services_retired: true
top_level_nucleus_retired: true
top_level_pxm_retired: true
top_level_guard_retired: true
implementation_paths_canonical: true
validators_prevent_regression: true
production_boundary_violated: false
pr_26_merge_allowed: true
```

The top-level bridge retirement slice is complete, and the follow-up targeted
lifecycle review now allows PR #26 to be marked ready for review.

## Retirement Checks

The top-level bridge directories are absent from the worktree:

```text
test ! -e services
test ! -e nucleus
test ! -e pxm
test ! -e guard
```

All four commands passed.

`git ls-files services nucleus pxm guard` returned no files, confirming the
retired bridge files are no longer tracked in the index.

The canonical implementation paths each contain the required scaffold files:

```text
implementation/guard/.mfos-dir.yml
implementation/guard/README.md
implementation/guard/index.yml
implementation/nucleus/.mfos-dir.yml
implementation/nucleus/README.md
implementation/nucleus/index.yml
implementation/pxm/.mfos-dir.yml
implementation/pxm/README.md
implementation/pxm/index.yml
implementation/services/.mfos-dir.yml
implementation/services/README.md
implementation/services/index.yml
```

## Validator Checks

`scripts/checks/check-component-scaffold.py` now requires
`implementation/services`, `implementation/nucleus`, `implementation/pxm`, and
`implementation/guard`; it no longer requires top-level `services`, `nucleus`,
`pxm`, or `guard`.

`scripts/checks/artifact-hygiene/check-directory-ownership.py` marks
`services`, `nucleus`, `pxm`, and `guard` as retired top-level implementation
roots and emits an error if any of them reappear. It also expects the
corresponding `implementation/*` locations to be canonical
`implementation_future` directories.

## Documentation Checks

`reports/current/directory-ownership/directory-ownership-audit.md` and
`reports/current/directory-ownership/directory-ownership-audit.yml` record the top-level paths as
`retired/absent` or `retired_absent`, with future code directed to
`implementation/services`, `implementation/nucleus`, `implementation/pxm`, and
`implementation/guard`.

`docs/design/registries/tasks.yaml` keeps old `services/*` entries only under
`retired_top_level_paths`. Live `allowed_paths` point under
`implementation/services/*`.

`docs/design/STATUS.md` does not point to live retired top-level
`services/`, `nucleus/`, `pxm/`, or `guard/` paths.

## Production Boundary

No production implementation, Rust semantic-core, hosted daemon, service
implementation, generated binary, or generated production code was introduced.
The four implementation component directories contain only `.mfos-dir.yml`,
`README.md`, and `index.yml`.

## Validation

```text
./scripts/validate-all.sh --check
PASS

./scripts/validate-artifact-hygiene.sh
PASS

./scripts/validate-component-scaffold.sh
PASS

./scripts/validate-naming-safety.sh release
PASS

./scripts/validate-dafny-semantics.sh --require-dafny
PASS: 136 verified, 0 errors

python3 -m py_compile $(find scripts tools -name '*.py' -type f | sort)
PASS

git diff --check
PASS
```

Note: `py_compile` emits temporary `__pycache__` files. They were removed, and
`./scripts/validate-artifact-hygiene.sh` was rerun successfully afterward.
