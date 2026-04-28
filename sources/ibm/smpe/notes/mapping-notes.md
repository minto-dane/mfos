# SMP/E Mapping Notes

## External Anchors

- EXTREF-IBM-ZOS-SMPE-OVERVIEW-0001: SMP/E overview.
- EXTREF-IBM-ZOS-SMPE-ZONES-0001: SMP/E zones.

## Candidate MFOS Concepts

- Desired software state.
- Installed software observation.
- Maintenance evidence.
- External inventory locator.

## Mapping Guidance

- Keep global, target, and distribution zone identifiers as external metadata.
- Avoid modeling CSI entries unless backed by an adapter that reads supported external outputs and stores only public-safe summaries.
- Separate z/OSMF Software Management inventory from raw SMP/E processing details.

## Remaining Gaps

- Add source cards for SYSMOD concepts without MCS syntax.
- Add source cards for z/OSMF Software Management use of SMP/E-packaged software.
- Add mapping notes for ServerPac and CBPDO installation-package concepts.
