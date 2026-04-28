# Linux Informative Boundary

Status: draft

Linux kernel documentation in this tree is informative. It can help identify
kernel-facing behavior, feature exposure, and practical limitations for x86
features such as CET and PKU, but it must not become the MFOS policy source.

MFOS use rules:

- Cite Intel or AMD architecture documents for architectural grounding.
- Cite Linux kernel documentation only for informative behavior context.
- Map CET, PKU, and similar mechanisms as optional enforcement aids.
- Keep authorization, audit, storage-domain, and Guard policy definitions in
  MFOS-owned requirements and specs.
- Add negative tests for claims that a hardware feature alone satisfies a
  higher-level policy or assurance requirement.
