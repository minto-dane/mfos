# WLM Mapping Notes

## External Anchors

- EXTREF-IBM-ZOS-WLM-OVERVIEW-0001: MVS workload management.
- EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001: Service classes and reporting.

## Candidate MFOS Concepts

- Workload intent.
- Business importance label.
- Performance observation.
- External service-policy reference.

## Mapping Guidance

- Store WLM service class and report class names as external observations or adapter configuration, not normalized MFOS policy.
- Avoid deriving capacity guarantees from WLM labels.
- When mapping batch work, keep JES scheduling, WLM classification, and MFOS workload request state as separate layers.

## Remaining Gaps

- Add source cards for z/OSMF WLM task administration.
- Add source cards for WLM status observation and policy activation.
- Add cross-domain notes for WLM interactions with UNIX processes and JES batch work.
