# z/OSMF Mapping Notes

## External Anchors

- EXTREF-IBM-ZOS-MANAGEMENT-FACILITY-TASKS-0001: z/OSMF tasks.
- EXTREF-IBM-ZOS-MANAGEMENT-FACILITY-REST-SERVICES-0001: z/OSMF REST services.

## Candidate MFOS Concepts

- External management endpoint.
- Resource operation request.
- Authenticated operation context.
- External result observation.

## Mapping Guidance

- Keep z/OSMF service availability, SAF profile access, and plugin configuration outside core MFOS assumptions.
- Record target system, z/OSMF level, service area, and observation time where adapters collect facts.
- Avoid storing endpoint paths, header recipes, or JSON payload shapes in source grounding.

## Remaining Gaps

- Add source cards for Workflows and Software Management tasks.
- Add cross-domain notes for z/OSMF jobs REST with JES and z/OSMF data set/file REST with DFSMS and UNIX.
- Add source cards for z/OSMF security configuration at a conceptual level.

