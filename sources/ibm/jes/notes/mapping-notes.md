# JES Mapping Notes

## External Anchors

- EXTREF-IBM-ZOS-JES-FUNCTIONS-0001: JES2 functions.
- EXTREF-IBM-ZOS-JES-JOB-CONTROL-0001: JCL and JECL boundary.

## Candidate MFOS Concepts

- Workload request.
- Batch submission envelope.
- External job reference.
- External output artifact reference.

## Mapping Guidance

- Keep JCL and JECL outside the stable MFOS data model unless stored as user-provided opaque text with provenance.
- Record JES type and z/OS level as external adapter context when available.
- Treat submit, hold, release, cancel, purge, and output retrieval as external operations with installation-specific authorization.

## Remaining Gaps

- Add source cards for JES multi-access spool concepts.
- Add source cards for JES2 versus JES3 support distinctions that affect z/OSMF jobs REST behavior.
- Add mapping notes for SDSF and z/OSMF job views over JES-owned state.
