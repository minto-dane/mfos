# Source Card Pin Audit

Date: 2026-04-27

Scope:

- `docs/design/source-matrix/cards/*.yml`
- `reports/audits/source/source-card-pin-audit.md`

Method:

- Added pin metadata only from existing local card title/URL metadata.
- Did not copy external document body text.
- Did not invent publication numbers.
- Did not weaken `mfos_divergence` or `prohibited_inference`.

## Fields Added

Each Source Card now includes:

- `version_or_release`
- `publication_number`
- `section_scope`
- `pin_quality`
- `review_notes`

`publication_number` is populated only where the identifier was already visible
in the local title or URL:

- `EXTREF-IBM-Z-ARCHITECTURE-PRINCIPLES-0001`: `SA22-7832-14`
- `X64-AMD-001`: `24593`
- `NIST-160-001`: `SP 800-160 Vol. 1 Rev. 1`
- `NIST-193-001`: `SP 800-193`
- `NIST-218-001`: `SP 800-218`

## Pin Quality Summary

| pin_quality | count |
|---|---:|
| `release_and_topic_pinned_from_url` | 12 |
| `release_pinned_from_url` | 1 |
| `publication_identifier_pinned_from_title` | 4 |
| `revision_pinned_from_url` | 1 |
| `versioned_primary_url_mixed_with_unversioned_secondary` | 1 |
| `floating_latest_url_needs_review` | 2 |
| `unversioned_url_needs_review` | 15 |
| `internal_source_unversioned` | 1 |

## Cards Still Needing Human/Source Review

High-priority section/version pin review remains for cards with unversioned,
floating, mixed, or internal-only source pins:

| source_id | pin_quality | current version_or_release |
|---|---|---|
| `FBVBS-001` | `internal_source_unversioned` | internal transfer source; external release not applicable |
| `EXTREF-IBM-Z-DPM-0001` | `unversioned_url_needs_review` | not pinned from local metadata |
| `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001` | `unversioned_url_needs_review` | z/OS Basic Skills documentation path; release not pinned in URL |
| `EXTREF-IBM-ZOS-JES-JOB-FLOW-0001` | `unversioned_url_needs_review` | z/OS Basic Skills documentation path; release not pinned in URL |
| `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001` | `unversioned_url_needs_review` | IBM Support page; release not pinned in URL |
| `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001` | `unversioned_url_needs_review` | z/OS Basic Skills documentation path; release not pinned in URL |
| `EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001` | `unversioned_url_needs_review` | IBM Support page; release not pinned in URL |
| `EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001` | `unversioned_url_needs_review` | z/OS Basic Skills documentation path; release not pinned in URL |
| `EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001` | `floating_latest_url_needs_review` | z/OS latest documentation path; floating release pin |
| `EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001` | `unversioned_url_needs_review` | z/OS Basic Skills documentation path; release not pinned in URL |
| `MS-VBS-001` | `unversioned_url_needs_review` | Microsoft Learn current article; release not pinned in local metadata |
| `MS-VSM-001` | `unversioned_url_needs_review` | Microsoft Learn current article; release not pinned in local metadata |
| `SEL4-001` | `unversioned_url_needs_review` | seL4 verification page; release not pinned in local metadata |
| `SLSA-001` | `floating_latest_url_needs_review` | SLSA latest specification path; floating version pin |
| `TCG-001` | `unversioned_url_needs_review` | TCG resource page; exact profile version not pinned in local metadata |
| `TUF-001` | `versioned_primary_url_mixed_with_unversioned_secondary` | TUF specification v1.0.26 primary URL; metadata overview URL remains unversioned |
| `X64-INTEL-001` | `unversioned_url_needs_review` | Intel SDM landing page; manual revision not pinned in local metadata |
| `X64-LINUX-CET-001` | `unversioned_url_needs_review` | Linux kernel documentation current site; release not pinned in local metadata |
| `X64-LINUX-PKU-001` | `unversioned_url_needs_review` | Linux kernel documentation current site; release not pinned in local metadata |

Publication-number review remains for cards whose local title/URL does not
expose a publication identifier. Those fields are intentionally `null`.

## Validation

Command:

```bash
python3 scripts/validators/validate-source-cards.py
```

Result:

```text
Source Card validation OK: 37 cards
```

