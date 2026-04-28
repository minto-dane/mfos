# Security Assurance Source Grounding

Status: draft

This directory holds public-safe source grounding for MFOS assurance,
secure-development, update-security, measured-boot, formal-boundary, and
virtualization-assisted isolation concepts.

Primary-source boundary:

- NIST publications are cited by publication page or DOI; PDFs are not stored
  in this repository.
- TUF, SLSA, TCG, seL4, and Microsoft Learn pages are cited as primary source
  locations for their respective projects or vendors.
- These cards do not copy source text, tables, diagrams, code, metadata
  schemas, register tables, or protocol fields as substitute documentation.
- External marks are used only for bibliographic reference and traceability.
- Hardware and virtualization mechanisms are enforcement aids; MFOS policy
  roots remain MFOS requirements, specifications, and assurance evidence.

Current source cards:

- `microsoft/source-cards/MS-VBS-001.yml`
- `microsoft/source-cards/MS-VSM-001.yml`
- `nist/source-cards/NIST-160-001.yml`
- `nist/source-cards/NIST-193-001.yml`
- `nist/source-cards/NIST-218-001.yml`
- `sel4/source-cards/SEL4-001.yml`
- `slsa/source-cards/SLSA-001.yml`
- `tpm-tcg/source-cards/TCG-001.yml`
- `tuf/source-cards/TUF-001.yml`

Open gaps:

- Update-security metadata role mappings need MFOS-owned schema and negative
  tests.
- Supply-chain assurance needs profile-specific SLSA target levels and
  continuous control evidence.
- Measured boot needs a measured-component inventory and event-log evidence
  schema.
- Formal-assurance claims need explicit proof-boundary wording before any
  high-assurance claim is allowed.
