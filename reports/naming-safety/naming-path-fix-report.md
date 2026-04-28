# Naming Path Fix Report

Status: complete  
Date: 2026-04-27

## Scope

Renamed only MFOS-owned implementation path names and direct references to those
paths. No production code was added or changed.

## Path Renames

- `implementation/interfaces/tso-like/` -> `implementation/interfaces/command-processor/`
- `implementation/interfaces/ispf-like/` -> `implementation/interfaces/panel-ui/`
- `implementation/interfaces/zosmf-like-api/` -> `implementation/interfaces/management-api/`
- `implementation/services/tsoed/` -> `implementation/services/commandd/`
- `implementation/services/ispfd/` -> `implementation/services/paneld/`

All renamed directories were empty scaffolds at the time of the move.

## References Updated

- `scripts/bootstrap/bootstrap-tree.sh`
- `reports/naming-safety/naming-safety-red-team-review.md`
- `reports/naming-safety/naming-safety-red-team-review.yml`
- `reports/naming-safety/mfos-owned-name-audit.md`
- `reports/naming-safety/mfos-owned-name-audit.yml`
- `reports/audits/repo/repo-audit.md`
- `reports/audits/repo/repo-audit.yml`

## Workload Policy, SVC, and PCALL Disposition

The later closure pass renamed the owned workload-management paths and
identifiers:

- `docs/design/specs/11-wlm.md` -> `docs/design/specs/11-workload-policy.md`
- `implementation/services/wlmd/` -> `implementation/services/workpolicyd/`
- `implementation/prototypes/hosted-semantic/services/wlmd/` -> `implementation/prototypes/hosted-semantic/services/workpolicyd/`
- `MFOS-REQ-WLM-*` -> `MFOS-REQ-WPOL-*`
- `MFOS-TEST-WLM-*` / `NEG-MFOS-WLM-*` -> `MFOS-TEST-WPOL-*` / `NEG-MFOS-WPOL-*`
- `EV-MFOS-WLM-*` -> `EV-MFOS-WPOL-*`

The owned-name checker now includes `wlm` as a forbidden MFOS-owned token and
release-mode naming validation passes. `EXTREF-IBM-ZOS-WLM-*` remains allowed
only as an external source-reference namespace.

Remaining MFOS-owned paths requiring later ADR/legal decision:

- `implementation/nucleus/svc/`
- `implementation/runtime/abi/svc/`
- `implementation/guard/roots/svc-table/`
- `implementation/nucleus/pcall/`
- `implementation/runtime/abi/pcall/`

## Verification

Commands run:

```sh
rg -n "implementation/interfaces/(tso-like|ispf-like|zosmf-like-api)|implementation/services/(tsoed|ispfd)" . -S -g '!reports/naming-safety/naming-path-fix-report.md'
rg -n "\b(tso-like|ispf-like|zosmf-like-api|tsoed|ispfd)\b" implementation reports scripts/bootstrap/bootstrap-tree.sh -S -g '!reports/naming-safety/naming-path-fix-report.md'
python3 scripts/checks/naming-safety/check-mf-owned-names.py
```

Results:

- No old implementation path references remain outside this report.
- No old path-name tokens remain under `implementation`, `reports`, or
  `scripts/bootstrap/bootstrap-tree.sh`, excluding this report's change log.
- `python3 scripts/checks/naming-safety/check-mf-owned-names.py` reports
  `MFOS-owned name check OK: 0 warnings`.

## Remaining Risks

- Historical report content now points at the renamed paths where direct path
  references were updated; older audit conclusions should still be treated as
  audit history, not canonical current design.
