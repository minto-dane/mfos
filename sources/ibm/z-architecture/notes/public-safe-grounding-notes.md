# Public-Safe Grounding Notes

## Review Position

The z-architecture artifacts deliberately keep to title, order-number, URL, and
MFOS mapping metadata. The IBM Principles of Operation is identified through an
official IBM listing only; the PDF was not downloaded, stored, mirrored, or
excerpted.

## Requirements Hooks

- `MFOS-REQ-SOURCE-0002` and `MFOS-REQ-SOURCE-0004` need terminology linting and divergence documentation.
- `MFOS-REQ-PARTITION-0001` through `MFOS-REQ-PARTITION-0008` need PXM lifecycle, resource assignment, teardown, and audit coverage.

## Negative Tests

- Reject claims that MFOS implements z/Architecture, PR/SM, LPAR, DPM, HMC, or z/OS compatibility.
- Reject partition transitions that skip explicit state checks.
- Reject storage reuse when teardown did not complete required zeroing or revocation.
- Reject management-plane mutations that produce no audit event.

## Key Gaps

- The LPAR source is an unversioned IBM Support page.
- DPM URL is machine-scope pinned but not pinned to a stable guide order number.
- MFOS still needs the actual PXM object schema and partition state table.
- Architecture glossary needs human review before terms are reused in normative MFOS specs.
