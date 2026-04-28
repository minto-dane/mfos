# Naming-Safety Open Issues

Status: draft
Date: 2026-04-27

## Human / Legal Review Required

- Public release is not allowed until an IP/trademark attorney reviews the
  notice, disclaimers, source-card policy, and public-facing wording.
- Legacy `IBM-*` IDs remain as aliases in `legacy_source_ids` and
  `reports/naming-safety/naming-alias-map.yml`. This is intentional for migration
  traceability, but public documentation should prefer the `EXTREF-*`
  canonical IDs.
- `WLM` has been removed from MFOS-owned namespaces and replaced by
  `workload-policy`, `workpolicyd`, and `WPOL` owned IDs. `EXTREF-*` source
  IDs may still contain `WLM` because they identify external references.
- `AMF`, `PXM`, `SVC`, and `PCALL` remain MFOS-owned terms pending a later
  architecture/legal review. They are not treated as public-release clearance.
- Non-naming historical reports have been migrated to current `EXTREF-*`
  source IDs. Older audit conclusions remain audit history, not current
  canonical design.
- Japanese mirror content remains incomplete. English remains canonical until
  translation-unit parity is reviewed.

## Release Gate

Release-mode evidence validation still fails closed because claim-linked
evidence is draft-only. Do not mark evidence verified without actual artifacts,
digests, verifiers, and verification timestamps.
