# TSO/E And ISPF Mapping Notes

## External Anchors

- EXTREF-IBM-ZOS-TSO-E-INTRODUCTION-0001: TSO/E general functions.
- EXTREF-IBM-ZOS-ISPF-INTRODUCTION-0001: ISPF overview.

## Candidate MFOS Concepts

- Interactive user session.
- External command invocation.
- Panel or dialog observation.
- User context and authorization boundary.

## Mapping Guidance

- Keep TSO/E command text opaque unless a targeted adapter owns generation and validation.
- Do not normalize ISPF panel identifiers or service names into MFOS core semantics.
- Record whether an observation came from TSO/E, ISPF, z/OSMF, SDSF, or another surface.

## Remaining Gaps

- Add source cards for TSO/E and ISPF command-entry boundaries without syntax.
- Add source cards for ISPF dialog concepts without panel or service formats.
- Add cross-domain notes for TSO/E access to UNIX System Services.
