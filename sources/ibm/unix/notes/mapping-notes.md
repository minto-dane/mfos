# z/OS UNIX Mapping Notes

## External Anchors

- EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001: z/OS UNIX introduction.
- EXTREF-IBM-ZOS-UNIX-FILE-SYSTEMS-0001: zFS file systems.

## Candidate MFOS Concepts

- External path reference.
- Mounted file-system observation.
- Process execution request.
- Shell environment metadata.

## Mapping Guidance

- Keep UNIX path, MVS data-set name, and z/OSMF file-service resource identifiers distinct.
- Record encoding, case-sensitivity, and authorization assumptions as adapter context.
- Avoid storing IBM shell command forms or callable-service prototypes.

## Remaining Gaps

- Add source cards for shell customization and RACF OMVS segment behavior.
- Add source cards for fork and spawn concepts without signatures.
- Add cross-domain notes for z/OSMF file REST services and z/OS UNIX files.
