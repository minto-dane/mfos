# Dafny Module Hygiene Report

Status: current  
Date: 2026-04-29

## Result

```yaml
case_duplicate_dafny_modules_remaining: false
camelcase_canonical_module_files_remaining: false
canonical_module_directory: formal/executable-semantics/dafny/modules/
canonical_filename_policy: lower_snake_case.dfy
```

The canonical Phase 1 module set is:

- `audit.dfy`
- `authorization.dfy`
- `common.dfy`
- `dataset_catalog.dfy`
- `errors.dfy`
- `first_vertical_slice.dfy`
- `job_spool.dfy`
- `operator_console.dfy`
- `types.dfy`

No `AuditContracts.dfy`, `AuthorizationContracts.dfy`, `Common.dfy`, or other
case-only duplicate-looking files remain in the canonical Dafny semantics path.

## Verification Impact

The lower-snake-case module set is verified as a group by:

```sh
./scripts/validate-dafny-semantics.sh --require-dafny
```
