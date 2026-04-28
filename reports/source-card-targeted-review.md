# Source Card Targeted Review

Date: 2026-04-27

Scope:

- `docs/design/source-matrix/cards/*.yml`
- `reports/source-card-targeted-review.md`

Task boundary:

- Reviewed only the high-priority cards listed after pin normalization.
- Updated only `pin_quality` and `review_notes` in source cards.
- Did not copy long external document text.
- Did not invent publication numbers.
- Did not change `mfos_divergence`, `prohibited_inference`, `source_refs`,
  `requirement_refs`, or requirements.

## Method

Publisher/primary pages were checked where available. If a page exposed only a
floating or unversioned URL, the card remains `needs_review` and the reason is
recorded in `review_notes`.

## Cards With Improved Pin Quality

| source_id | result | verification basis |
|---|---|---|
| `EXTREF-IBM-ZOS-SMPE-SECINT-HOLDDATA-0001` | `official_support_page_verified_event_date_pinned` | IBM support page verified; page states SECINT RECEIVE ORDER enhancement date 2025-10-16. |
| `EXTREF-IBM-ZOS-UNIX-SERVICES-LIBRARY-0001` | `official_library_redirect_verified_release_pinned` | IBM `latest` URL redirects to z/OS 3.2.0 UNIX System Services library page listing publication order numbers and update dates. |
| `X64-INTEL-001` | `official_landing_page_verified_manual_version_pinned` | Intel SDM landing page verified; metadata shows content ID 767375, updated 2026-04-06, SDM downloadable PDFs version 091. |
| `X64-LINUX-PKU-001` | `primary_docs_verified_site_version_pinned` | Linux kernel documentation page verified; site header shows 7.1.0-rc1. |
| `X64-LINUX-CET-001` | `primary_docs_verified_site_version_pinned` | Linux kernel documentation page verified; site header shows 7.1.0-rc1. |
| `SLSA-001` | `latest_redirect_verified_version_pinned` | `spec/latest` redirects to approved SLSA v1.2 page. |
| `TCG-001` | `official_resource_page_verified_spec_version_pinned` | TCG resource page verified; latest listed profile is Version 1.06 Revision 52, 2023-12-04. |
| `MS-VBS-001` | `primary_article_verified_last_updated_pinned` | Microsoft Learn article verified; last updated 2025-11-07. |
| `MS-VSM-001` | `primary_article_verified_last_updated_pinned` | Microsoft Learn article verified; last updated 2025-12-16. |

## Cards Still Requiring Review

These cards remain `needs_review` because the reviewed page was unversioned,
floating, mixed with an unversioned secondary URL, or internal-only.

| source_id | pin_quality | reason |
|---|---|---|
| `FBVBS-001` | `internal_source_unversioned_needs_review` | Internal source identifier only; no independently verifiable URL or versioned local source artifact in this review scope. |
| `EXTREF-IBM-Z-DPM-0001` | `official_topic_verified_machine_scope_needs_review` | IBM Documentation page verified, but no named DPM guide version, document order number, or stable section anchor was visible. |
| `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001` | `official_topic_verified_release_unpinned_needs_review` | IBM Basic Skills page verified, but URL is not release-pinned and no publication/order number was visible. |
| `EXTREF-IBM-ZOS-JES-JOB-FLOW-0001` | `official_topic_verified_release_unpinned_needs_review` | IBM Basic Skills page verified, but URL is not release-pinned; current card URL uses `/de/` path. |
| `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001` | `official_support_page_verified_unversioned_needs_review` | IBM Support page verified, but page is unversioned and no publication/order number was visible. |
| `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001` | `official_topic_verified_release_unpinned_needs_review` | IBM Basic Skills page verified, but URL is not release-pinned and no publication/order number was visible. |
| `EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001` | `official_topic_verified_release_unpinned_needs_review` | IBM Basic Skills page verified, but URL is not release-pinned and no publication/order number was visible. |
| `EXTREF-IBM-ZOS-CROSS-MEMORY-CONTROL-0001` | `official_topic_verified_release_unpinned_needs_review` | IBM Basic Skills page verified, but URL is not release-pinned and no publication/order number was visible. |
| `SEL4-001` | `primary_page_verified_unversioned_needs_review` | seL4 Verification page verified, but page is not versioned; production use should pin a release, proof artifact, or documentation snapshot. |
| `TUF-001` | `versioned_primary_verified_secondary_unversioned_needs_review` | TUF primary spec URL is verified as v1.0.26, but the card also cites an unversioned metadata overview URL. |

## Publisher Pages Checked

- IBM system integrity: <https://www.ibm.com/docs/en/zos-basic-skills?topic=zos-system-integrity>
- IBM JES overview: <https://www.ibm.com/docs/en/zos-basic-skills?topic=jobs-what-is-jes>
- IBM job flow: <https://www.ibm.com/docs/de/zos-basic-skills?topic=jobs-job-flow-through-system>
- IBM storage protection: <https://www.ibm.com/docs/en/zos-basic-skills?topic=storage-what-is-protection>
- IBM logical partitions support page: <https://www.ibm.com/support/pages/introduction-logical-partitions>
- IBM DPM: <https://www.ibm.com/docs/en/systems-hardware/zsystems/2964-N63?topic=cm-dynamic-partition-manager-dpm>
- IBM SECINT HOLDDATA support page: <https://www.ibm.com/support/pages/secint-holddata-now-available-smpe-receive-order>
- IBM z/OS UNIX System Services library: <https://www.ibm.com/docs/en/zos/latest?topic=zos-unix-system-services>
- IBM cross-memory communication: <https://www.ibm.com/docs/en/zos-basic-skills?topic=integrity-controlling-cross-memory-communication>
- Intel SDM landing page: <https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html>
- Linux pkeys documentation: <https://docs.kernel.org/core-api/protection-keys.html>
- Linux x86 CET shadow stack documentation: <https://docs.kernel.org/arch/x86/shstk.html>
- TUF specification v1.0.26: <https://theupdateframework.github.io/specification/v1.0.26/>
- SLSA latest specification redirect: <https://slsa.dev/spec/latest/>
- TCG PC Client Platform Firmware Profile resource: <https://trustedcomputinggroup.org/resource/pc-client-specific-platform-firmware-profile-specification/>
- seL4 Verification page: <https://sel4.org/Verification/>
- Microsoft Learn memory integrity/VBS: <https://learn.microsoft.com/en-us/windows-hardware/drivers/bringup/device-guard-and-credential-guard>
- Microsoft Learn VSM: <https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/tlfs/vsm>

## Validation

Command:

```bash
python3 scripts/validate-source-cards.py
```

Result:

```text
Source Card validation OK: 37 cards
```

Remaining cards whose `pin_quality` contains `needs_review`: 10.
