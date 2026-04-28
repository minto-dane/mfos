# MFOS Transfer Map From FBVBS

Grounding source: `https://github.com/minto-dane/fbvbs` at `30e6fb54c76eaec83d03f79e1fd96c030cca504b`

## Required Theme Mapping

| Required theme | FBVBS source card | MFOS transfer |
|---|---|---|
| Assurance discipline | `source-cards/010-assurance-discipline.md` | Adopt validator family taxonomy, design-root traceability, gate levels |
| Partition state-machine discipline | `source-cards/020-partition-state-machine-discipline.md` | Adapt lifecycle contracts to MFOS managed objects |
| Update manifest discipline | `source-cards/030-update-manifest-discipline.md` | Adapt generation, freshness, revocation, dependency, and signature controls; keep source gap visible |
| Proof/evidence structure | `source-cards/040-proof-evidence-structure.md` | Adopt evidence-pack spine and retention revalidation |
| Adopt/adapt/reject transfer rules | `source-cards/050-adopt-adapt-reject-transfer-rules.md` | Adopt as MFOS import rubric |

## MFOS Adoption Matrix

| Pattern | Decision | Reason |
|---|---|---|
| Document authority levels | Adopt | Prevents implementation plans from becoming accidental normative requirements |
| Design-root traceability | Adopt | Gives every validator and derived artifact an accountable source |
| Always-on vs heavy assurance gates | Adopt | Keeps CI practical while preserving deeper release obligations |
| Compatibility windows | Adopt | Missing version windows should be incompatible, not best-effort |
| Reserved-field zero discipline | Adopt | Protects future schema evolution |
| Partition lifecycle transitions | Adapt | Useful shape, but object vocabulary must be MFOS-owned |
| Recovery/destructive artifact preconditions | Adapt | MFOS should define its own approval and confirmation schemas |
| State manifest | Adapt | MFOS needs its own schema, but the window/artifact-state split is useful |
| Evidence pack manifest | Adopt | Canonical digest and retention recheck model transfers cleanly |
| FBVBS service and UI labels | Reject | Source-specific and not MFOS normative |
| Standalone-ready production claim | Reject | Upstream records hard blockers and incomplete closure |

## Suggested MFOS Next Artifacts

1. MFOS design-root catalog.
2. MFOS validator output schema.
3. MFOS lifecycle command-contract schema.
4. MFOS update manifest and freshness policy.
5. MFOS evidence-pack manifest schema.
