# SPEC_GAP/UNSUPPORTED Warning Cleanup

Status: complete
Date: 2026-04-27

## Scope

This cleanup only touched explanatory documentation that produced current
`SPEC_GAP` / `UNSUPPORTED` success-path wording warnings.

Owned paths:

- `docs/design/source-matrix/source-lint-spec.md`
- `docs/design/source-matrix/source-matrix.md`
- `docs/design/source-matrix/traceability-policy.md`
- `docs/design/specs/04-threat-model.md`
- `reports/spec-gap-warning-cleanup.md`

## Changes

- Reworded lint policy text so `UNSUPPORTED` and `SPEC_GAP` paths must fail
  closed instead of completing.
- Reworded source-matrix negative-test wording to require
  `MFOS_ERR_UNSUPPORTED` or `MFOS_ERR_SPEC_GAP` for unsupported or unspecified
  behavior.
- Reworded threat-model abuse and threat rows so unsupported or undefined SVC
  behavior is described as prohibited completion/implementation, not a valid
  result.

## Validation

Command:

```bash
python3 scripts/check-spec-gap-misuse.py
```

Expected result:

```text
SPEC_GAP/UNSUPPORTED misuse check OK: 0 warnings
```

## Policy Impact

No policy was weakened. The updated wording keeps the same rule: unsupported
and unspecified behavior must not produce a usable result and must fail closed.
