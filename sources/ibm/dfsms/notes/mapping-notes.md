# DFSMS Mapping Notes

## External Anchors

- EXTREF-IBM-ZOS-DFSMS-OVERVIEW-0001: DFSMS family overview.
- EXTREF-IBM-ZOS-DFSMS-STORAGE-MANAGEMENT-0001: SMS policy model.

## Candidate MFOS Concepts

- Storage policy intent.
- Data lifecycle state.
- Managed versus unmanaged storage boundary.
- External retention and backup authority.

## Mapping Guidance

- Map IBM storage classes, management classes, and data classes only as external labels or adapter inputs.
- Keep ACS selection, DFSMShsm processing, and DFSMS utility execution outside the MFOS core model.
- For migration or restore narratives, describe MFOS state transitions as independent observations unless backed by a live adapter and explicit external evidence.

## Remaining Gaps

- Add source cards for DFSMShsm backup, migration, and recovery concepts.
- Add source cards for DFSMSdss copy, dump, restore, and volume-management concepts.
- Add a cross-domain note for DFSMS interactions with z/OSMF data set and file REST services.
