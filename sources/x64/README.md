# x64 Source Grounding

Status: draft

This directory holds public-safe source grounding for the MFOS x64 backend.
The cards here are bibliographic and traceability records only. They do not
copy source text, tables, instruction descriptions, or vendor diagrams.

Primary-source boundary:

- Intel and AMD architecture documents are used for x64 platform capability
  discovery and hardware enforcement mapping.
- Linux kernel documentation is informative only and is used to understand
  observed kernel-facing behavior and limitations.
- Hardware features are enforcement aids. MFOS policy roots remain MFOS
  requirements, specifications, and assurance evidence.
- No card in this tree implies compatibility, certification, endorsement, or
  affiliation with any external vendor, project, or operating system.

Current cards:

- `intel/source-cards/X64-INTEL-001.yml`
- `amd/source-cards/X64-AMD-001.yml`
- `linux-informative/source-cards/X64-LINUX-CET-001.yml`
- `linux-informative/source-cards/X64-LINUX-PKU-001.yml`

Current concept cards:

- `intel/concept-cards/x64-enforcement-aids.yml`
- `amd/concept-cards/amd64-enforcement-aids.yml`

Open gaps:

- Pin exact Intel SDM section anchors for paging, VMX/EPT, CET, PKU, PKS, and
  MSR handling after manual source review.
- Define the MFOS supported CPU feature matrix and fallback behavior per
  profile.
- Keep Linux kernel documentation marked informative; do not promote Linux
  behavior into MFOS policy roots.
