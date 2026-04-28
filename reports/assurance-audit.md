# MFOS Phase 0.6 Assurance Audit

Date: 2026-04-27

Scope:

- `schemas/claim.schema.json`
- `docs/design/assurance/claim-tree.yml`
- `evidence/traceability/claim-to-requirement.yml`
- `reports/assurance-audit.md`

This audit did not start implementation work and did not modify implementation code.

## Result

Pass after assurance-only updates.

Validation commands:

```text
scripts/validate-claims.py
python3 scripts/validate-claims.py
```

Direct execution of `scripts/validate-claims.py` returned `Permission denied` because the script is not executable in this checkout. Running the same script with `python3` completed successfully:

```text
Claim validation OK: 5 claims checked: 4 warnings
```

Warnings were limited to `CLAIM-GRD-HA-001` requirement IDs not present in the priority catalog:

- `MFOS-REQ-GRD-0001`
- `MFOS-REQ-GRD-0002`
- `MFOS-REQ-AUD-0007`
- `MFOS-REQ-AMF-0006`

## Checks

- Confirmed Baseline claims do not state protection after nucleus compromise.
- Confirmed Baseline claims do not state protection after malicious signed AMF module compromise.
- Added explicit Baseline non-claims for `CLAIM-AUD-BASELINE-001` so both Baseline claims carry the same post-nucleus and post-AMF compromise boundary.
- Confirmed `CLAIM-GRD-HA-001` is the High-Assurance root-object claim and includes Guard evidence refs.
- Confirmed `CLAIM-GRD-HA-001` includes attestation evidence refs.
- Confirmed claim-to-requirement traceability already matches the current claim tree and required no update.

## Schema Work

Updated `schemas/claim.schema.json` to make the policy executable for claim records:

- Baseline claims must list `Protection after nucleus compromise` in `not_claimed`.
- Baseline claims must list `Protection after malicious signed AMF module compromise` in `not_claimed`.
- High-Assurance claims must include at least one `GRD` evidence reference.
- High-Assurance claims must include at least one `ATTESTATION` evidence reference.

## Notes

`/home/nia/mfos` is not a Git worktree, so dirty-worktree conflict detection was limited to direct file inspection.
