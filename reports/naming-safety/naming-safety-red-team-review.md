# MFOS Naming-Safety Red Team Review

Date: 2026-04-27
Workspace: `/home/nia/mfos`
Mode: read-only design review; no design files were edited. Report artifacts were written under `reports/`.

## Executive Judgment

The naming migration is complete enough for private internal review, but it is not public-release ready.

Current canonical Source Card IDs are no longer `IBM-*`: targeted scans did not find `source_id: IBM-*` in the current source matrix, registries, requirements, packs, claims, or implementation metadata. The active Source Card ledger uses `EXTREF-IBM-*` for IBM-derived external references, with old IDs retained as `legacy_source_ids`.

However, public release remains blocked. The repository says this directly in `docs/design/STATUS.md:20-22` and `docs/design/STATUS.md:228-229`, and the release evidence gate fails with 18 errors and 20 warnings. The naming-safety validator passing is therefore a private-review signal, not a release approval.

## Validation Run

Commands run locally:

| Command | Result |
| --- | --- |
| `./scripts/validate-naming-safety.sh release` | Passed: 0 warnings |
| `./scripts/validate-all.sh --check` | Passed |
| `python3 scripts/checks/check-evidence-status.py --mode release` | Failed closed: 18 errors, 20 warnings |
| `python3 scripts/checks/check-prohibited-terms.py` | Passed |
| `python3 scripts/checks/naming-safety/check-source-card-public-safe.py --mode release` | Passed: 0 warnings |
| `python3 -m py_compile $(find scripts -name '*.py' -print)` | Passed |

Additional targeted scans checked legacy `IBM-*` IDs, prohibited-name paths, Source Card summary/copy-risk fields, NOTICE coverage, and validator coverage.

## Critical Findings

### NSRT-CRIT-001 - Public Release Is Still Blocked

`docs/design/STATUS.md:20-22` marks `public_release_allowed: false` and requires IP attorney review. `docs/design/STATUS.md:177-179` documents the expected release-mode evidence failure, and the local run confirmed `python3 scripts/checks/check-evidence-status.py --mode release` fails with 18 errors and 20 warnings. `docs/design/STATUS.md:211-223` also states evidence entries are draft placeholders and source cards still need publication, section, and version pin work.

Impact: the repository can truthfully say naming-safety lint passes, but it cannot make public release, conformance, production, or verified-evidence claims.

Required action: keep public release blocked until legal/IP review is complete, release-mode evidence passes with verified or archived evidence, and Source Cards move out of draft/public-review gaps.

### NSRT-CRIT-002 - Prohibited IBM-Interface Tokens Remain In MFOS-Owned Paths

MFOS-owned implementation directories still contain exact prohibited or high-risk external interface tokens:

- `implementation/interfaces/command-processor`
- `implementation/interfaces/panel-ui`
- `implementation/interfaces/management-api`
- `implementation/services/commandd`
- `implementation/services/paneld`
- `implementation/services/workpolicyd`
- `implementation/prototypes/hosted-semantic/services/workpolicyd`
- `implementation/nucleus/svc`
- `implementation/runtime/abi/svc`
- `implementation/guard/roots/svc-table`
- `implementation/nucleus/pcall`
- `implementation/runtime/abi/pcall`

`scripts/checks/naming-safety/check-mf-owned-names.py:37-42` explicitly treats `ispf`, `tso`, and `zosmf` as forbidden tokens, but the script walks only text files via `text_files([Path(".")])` at `scripts/checks/naming-safety/check-mf-owned-names.py:112`; empty or placeholder directories are not scanned. The same checker does not include `WLM`, `SVC`, or `PCALL` in its forbidden token list even though they are owned ABI/service namespaces here.

Impact: current validation reports `MFOS-owned name check OK`, while release-visible owned paths can imply TSO, ISPF, z/OSMF, workload policy, SVC, or PCALL compatibility surfaces.

Required action: rename owned path families to neutral MFOS terms, or record an explicit legal/architecture exception before any public artifact includes these paths. Extend the validator to scan directories and strict owned Markdown identifiers, not only YAML/JSON identifiers and text-file paths.

## Major Findings

### NSRT-MAJ-001 - Canonical Source Card Guidance Still Contains Removed Summary-Style Shape

Current Source Card schema text says Source Cards are "not copies, summaries, record-layout databases, command references, macro references, or substitutes for external documentation" at `docs/design/source-matrix/source-card-schema.md:5-7`.

The older canonical design document still instructs that every Source Card include an obsolete shape: `source_type: normative`, `title`, `url`, `canonical_concepts`, and list-style `mfos_mapping` at `docs/design/mfos-design.md:288-303`. `sources/citation-policy.md:3-5` also says Source Cards store "short summaries", which conflicts with the public-safe post-migration framing. `docs/design/source-matrix/source-lint-spec.md:132` says Source Card `source_type` must be `external_reference` or `internal_transfer`, but `docs/design/source-matrix/source-lint-spec.md:276` still refers to Source Cards with `source_type: normative`.

Impact: future contributors can follow stale canonical guidance and reintroduce summary/copy-risk fields that current Source Card validators removed.

Required action: update public guidance and lint specs to the v0.6 public-safe Source Card shape. Add validator coverage for stale Source Card schema examples outside `docs/design/source-matrix/cards/*.yml`.

### NSRT-MAJ-002 - Legacy `IBM-*` IDs Remain In Non-Naming Historical Reports Outside Strict Alias Contexts

`docs/design/legal-risk-policy.md:9-12` says legacy `IBM-*` source IDs are retained only as `legacy_source_ids` aliases and in the naming migration report. In practice, old IDs still appear in non-naming reports as if they were source refs, card names, or review rows:

- `reports/audits/requirements/requirement-gap-closure.md:15-27` lists old IDs such as `IBM-APF-001`, `IBM-ZACS-001`, `IBM-SMF-001`, and `IBM-DFSMS-002`.
- `reports/audits/source/source-card-pin-audit.md:57-65` lists old IBM card IDs for pin review.
- `reports/audits/source/source-card-audit.md:52-97` lists old `docs/design/source-matrix/cards/IBM-*.yml` paths.
- `reports/audits/source/source-card-targeted-review.md:29-53` uses old IBM IDs in review tables.

This issue was closed by scanning `reports/` and allowing legacy aliases only in
source-card alias fields and `reports/naming-safety/` migration artifacts.

Impact: public report bundles would contain obsolete canonical-looking IDs outside the stated alias context, weakening the `EXTREF-IBM-*` migration.

Required action: either migrate historical report references to current `EXTREF-*` IDs, or move/scope historical reports so they are excluded from public release artifacts with an explicit archive disclaimer. Extend namespace lint to scan release-bound reports.

### NSRT-MAJ-003 - Non-IBM External Mark And Affiliation Controls Are Incomplete

`NOTICE.md:5-19` covers IBM names and non-affiliation/non-compatibility with IBM products. It does not provide equivalent generic notice language for Microsoft, Windows, Intel, AMD, Linux, TCG, TUF, SLSA, seL4, or other external names used by Source Cards and specs.

Several non-IBM external Source Cards explicitly name vendors/products but set mark controls false. Examples:

- `docs/design/source-matrix/cards/MS-VBS-001.yml:27-32` names Microsoft and a Microsoft Learn URL, while `MS-VBS-001.yml:28` has `vendor_mark_used: false` and `MS-VBS-001.yml:72` has `trademark_reference_only: false`.
- `docs/design/source-matrix/cards/X64-INTEL-001.yml:29-34` names Intel and the Intel SDM, while `X64-INTEL-001.yml:30` has `vendor_mark_used: false` and `X64-INTEL-001.yml:80` has `trademark_reference_only: false`.

A local card scan found 13 non-IBM external cards with `vendor_mark_used: false` and `legal_controls.trademark_reference_only: false`.

Impact: the IBM disclaimer posture is much stronger than the general external-source posture. Public release could still imply weak affiliation or mark handling for non-IBM references.

Required action: add a generic external-name NOTICE/disclaimer or per-vendor notice policy, and align non-IBM Source Card `vendor_mark_used` / `trademark_reference_only` controls with actual use.

### NSRT-MAJ-004 - Validator Coverage Is Not Release-Grade

The local validators are useful but not sufficient for the naming-safety release surface:

- `check-mf-owned-names.py` originally missed empty owned directories and did
  not cover WLM/SVC/PCALL as strict owned-token risks. WLM is now covered and
  remediated; SVC/PCALL remain later architecture/legal-review items.
- `check-extref-namespace.py` excludes `reports/`, so old `IBM-*` IDs in release-bound reports are invisible.
- `check-source-card-public-safe.py:11-67` checks only Source Card YAML files, not stale public guidance such as `docs/design/mfos-design.md`.
- `schemas/source-card.schema.json:28-34` still accepts any `AAA-BBB-001`-style `source_id`, which would allow a canonical `IBM-*` Source Card through schema validation unless the separate namespace checker also runs.

Impact: a green `./scripts/validate-naming-safety.sh release` can coexist with naming hazards found by basic filesystem and report scans.

Required action: define the release-bound file set, scan directories and reports, align schemas with `EXTREF-IBM-*` policy, and add negative tests that inject old `IBM-*` canonical IDs, prohibited owned directories, stale Source Card examples, and non-IBM mark-control gaps.

## Minor Findings

### NSRT-MIN-001 - Root README Local Checks Omit The New Naming-Safety Gate

`README.md:48-55` lists only four older local checks and does not mention `./scripts/validate-all.sh --check` or `./scripts/validate-naming-safety.sh release`.

Impact: contributors following the root README can miss the naming-safety checks that currently enforce the migration.

Recommended action: update contributor-facing check instructions before public release.

## Non-Findings

- No current canonical `source_id: IBM-*` value was found in the active source matrix/card ledger, registries, requirements, packs, claims, or implementation metadata scanned.
- `python3 scripts/checks/naming-safety/check-source-card-public-safe.py --mode release` passes for the current Source Card YAML files.
- No long Markdown block quotes were found by targeted long-quote scan.
- `NOTICE.md` and `README.md` contain clear IBM non-affiliation and non-compatibility language.

## Public Release Readiness

Public release is not ready. The blockers are release evidence failure, required legal/IP review, draft Source Cards and source-pin gaps, prohibited owned path names, stale Source Card guidance, legacy IDs in report artifacts, incomplete non-IBM external-mark controls, and validator coverage gaps.

## Post-Review Remediation

This review was a point-in-time red-team snapshot. The following remediation was
completed after the review:

- `NSRT-CRIT-002`: remediated for the explicitly prohibited implementation
  scaffold names. `tso-like`, `ispf-like`, `zosmf-like-api`, `tsoed`, and
  `ispfd` were renamed to `command-processor`, `panel-ui`, `management-api`,
  `commandd`, and `paneld`.
- `NSRT-MAJ-001`: remediated. Source Card guidance now uses public-safe
  bibliographic reference cards and removed summary-style fields.
- `NSRT-MAJ-002`: remediated. Non-naming reports now use current `EXTREF-*`
  IDs; old `IBM-*` IDs remain only in naming migration/alias contexts.
- `NSRT-MAJ-003`: remediated for current Source Cards. Non-IBM external cards
  now use reference-only mark controls, and `NOTICE.md` has generic
  external-name notice language.
- `NSRT-MAJ-004`: remediated for current local gates. Validators scan
  directories, release-bound reports, stale public Source Card guidance, and
  reject canonical IBM-style source IDs.
- `NSRT-MIN-001`: remediated. Root README local checks include the
  naming-safety gate.
- `NSRT-OPEN-WLM`: remediated. WLM was removed from MFOS-owned namespaces and
  replaced with `workload-policy`, `workpolicyd`, and `WPOL`; external
  `EXTREF-IBM-ZOS-WLM-*` source-reference IDs remain unchanged.

Still open:

- `NSRT-CRIT-001`: public release remains blocked by legal/IP review and
  release-mode evidence validation. This is intentional fail-closed behavior.
- `AMF`, `PXM`, `SVC`, and `PCALL` remain MFOS-owned terms pending later
  legal/architecture review rather than automatic renaming.
