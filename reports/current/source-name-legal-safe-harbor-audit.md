# Source Name Legal Safe-Harbor Audit

Status: current
Date: 2026-04-28
Scope: `sources/`, `docs/design/source-matrix/cards/`, root notices, and public-facing naming policy.

This is an engineering/legal-risk hygiene audit, not legal advice.

## Summary

The current repository passes the MFOS naming-safety and source-card public-safety gates for private technical review:

- IBM and related external names are confined to source-reference, legal, non-compatibility, migration, or historical contexts.
- Canonical IBM-derived source references use `EXTREF-IBM-*`.
- `sources/` is marked as a noncanonical public-safe workbench; `docs/design/source-matrix/` remains canonical.
- Source Cards use metadata and divergence/prohibited-inference controls, not external documentation copies.
- `_cache` downloads were purged from the local working tree; only the committed `README.md` and `DO_NOT_COMMIT.md` guard files remain.

Public release is still not cleared. The project policy still requires IP/trademark attorney review before making the repository public.

## External Trademark Policy Baseline

IBM's current public trademark guidance permits text-only references to product and service names when they are truthful, non-misleading, and clear about the relationship. It also requires attribution, restricts logos, and warns against incorporating IBM product names into another company's product or site names.

MFOS currently aligns with this engineering baseline by using source-reference-only naming, explicit non-affiliation notices, and non-compatibility language. It does not clear legal review by itself.

Reference:

- https://www.ibm.com/legal/copyright-trademark

## Checks Performed

```text
./scripts/validate-naming-safety.sh release
python3 scripts/checks/naming-safety/check-source-card-public-safe.py --mode release
python3 scripts/checks/naming-safety/check-sources-workbench-public-safe.py --mode release
python3 scripts/checks/naming-safety/check-mf-owned-names.py --mode release
python3 scripts/checks/naming-safety/check-no-compatibility-claims.py --mode release
python3 scripts/checks/naming-safety/check-no-copied-external-docs.py --mode release
git ls-files sources/_cache
git ls-files | rg '\\.(pdf|html|htm|tar\\.gz|zip|docx?)$|/downloads/'
```

Observed results:

- Naming-safety release validation passed.
- Source Card public-safety validation passed.
- Sources workbench public-safety validation passed.
- MFOS-owned name validation passed.
- Compatibility-claim validation passed.
- External-doc copy guard passed.
- No external PDF/HTML/archive downloads are tracked under `sources/_cache/downloads/`.
- Local ignored `sources/_cache/downloads/` and `sources/_cache/retrieval-manifest.local.yml` were purged during this review.
- Only `sources/_cache/README.md` and `sources/_cache/DO_NOT_COMMIT.md` are tracked in `_cache`.

## Risk Classification

Critical:

- None detected for private technical review.

Major:

- Public release remains blocked by project policy until IP/trademark counsel reviews notices, disclaimers, source-card policy, public-facing wording, and repository visibility.

Minor:

- `sources/ibm/**` path names intentionally include IBM-related terms as external-reference organization. This is allowed by current MFOS policy but should remain clearly source-reference-only.
- `docs/design/mfos-design.md` still contains explanatory phrases such as `z/OS-inspired` and mapping headings. These are allowed only because they are paired with non-compatibility statements and source IDs.
- `sources/_cache/` is intentionally allowed only for local ignored material. This review purged local cache payloads, and public-release automation should still use `git archive` or tracked-file manifests only.

## Safe-Harbor Conditions Currently Met

- Text references only; no IBM logos or design marks found in tracked files.
- Root README and NOTICE include non-affiliation and non-compatibility statements.
- IBM-related source IDs are external references, not MFOS-owned requirement/spec/test/service identifiers.
- Source Cards include `legal_controls` requiring public-safe metadata and no copied text, tables, diagrams, record layouts, command syntax, macro signatures, or message tables.
- Source Cards and `sources/` workbench entries include divergence and prohibited-inference controls.
- Compatibility claims are blocked by validation.
- Workbench `card_id` values were normalized away from legacy `SRC-CARD-IBM-*`
  forms to `SRC-CARD-EXTREF-*` forms where applicable.
- Dangerous negative examples in `prohibited_inference` and `Avoid saying`
  lists are explicitly labeled `Forbidden claim:` to reduce snippet/context
  detachment risk.
- Local cache-manifest pointers now state `not_committed; see
  sources/_cache/README.md` instead of pointing to an untracked manifest file.

## Conditions Not Yet Met For Public Release

- No attorney review record exists.
- Release evidence is still draft-only.
- Public release gate remains `public_release_allowed: false`.
- `requires_ip_attorney_review_before_public_release: true` remains correct.

## Decision

```yaml
source_name_safe_harbor_private_review_passed: true
source_name_safe_harbor_public_release_passed: false
public_release_allowed: false
requires_ip_attorney_review_before_public_release: true
repository_visibility_change_allowed_now: false
```
