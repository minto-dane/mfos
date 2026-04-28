# LPAR DPM Mapping Notes

## External Anchors

- EXTREF-IBM-Z-DPM-OVERVIEW-0001: DPM overview.
- EXTREF-IBM-Z-DPM-PARTITIONS-ADAPTERS-0001: DPM partitions and adapters.

## Candidate MFOS Concepts

- External partition reference.
- Logical resource allocation intent.
- Hardware topology observation.
- Adapter attachment observation.

## Mapping Guidance

- Keep HMC object identifiers opaque.
- Record source system, access path, and observation time for DPM-derived data.
- Avoid representing DPM task availability as a static capability; authorization and system state can change behavior.

## Remaining Gaps

- Add source cards for DPM storage groups and storage configuration.
- Add source cards for DPM monitoring and event concepts.
- Add a cross-domain note for DPM, WLM, and z/OS system topology relationships.
