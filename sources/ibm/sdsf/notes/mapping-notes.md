# SDSF Mapping Notes

## External Anchors

- EXTREF-IBM-ZOS-SDSF-INTRODUCTION-0001: SDSF introduction.
- EXTREF-IBM-ZOS-SDSF-SECURITY-0001: SDSF security boundary.

## Candidate MFOS Concepts

- Operations row observation.
- External action request.
- Job output reference.
- Authorization outcome.

## Mapping Guidance

- Keep SDSF panel names, commands, and action characters out of core MFOS data.
- Store JES job identifiers and SDSF row metadata as external observations with provenance.
- Separate SDSF display authorization from authority to act on the underlying z/OS object.

## Remaining Gaps

- Add source cards for SDSF programming interfaces at a conceptual level.
- Add cross-domain notes for SDSF views over JES and WLM state.
- Add source cards for sysplex operational views without panel details.
