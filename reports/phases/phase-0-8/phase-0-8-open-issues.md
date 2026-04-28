# Phase 0.8 Open Issues

Date: 2026-04-27

Status: Critical, Major, and previously listed Minor red-team findings are
remediated for the Phase 0.8 design-level Core Semantics Freeze. Phase 0.8
remains specification-only and does not authorize Phase 1 implementation,
hosted daemon work, portable semantic core work, or production code.

## Resolved Gate Corrections

| ID | Prior severity | Resolution |
| --- | --- | --- |
| RT-0.8-001 | Critical | Phase 0.8 `010x` tests were materialized as concrete planned semantic tests in domain catalogs and `scripts/check-phase-0-8-traceability.py` now fails unresolved links or generic alias placeholders. |
| RT-0.8-002 | Major | `docs/design/specs/INDEX.md` now describes Phase 0.8 domains as specification-only, not hosted-prototype ready. |
| RT-0.8-003 | Major | Emergency duration is aligned to a 60-minute maximum; longer durations fail closed as `MFOS_ERR_SPEC_GAP`; operator/securityd prose, schema, and formal model use the `MFOS_AUTH_*` enum; audit projection is documented separately; negative tests were added. |
| RT-0.8-004 | Major | `MFOS_RESOURCE_SYSTEM` and `MFOS_RESOURCE_SERVICE` are registered in the authorization spec and SecurityDecision schema; operator target mapping now references those classes. |
| RT-0.8-005 | Major | Operator DSN grammar now delegates to the Phase 0.8 dataset/catalog DSN subset and rejects broader names before authorization; negative test planning was added. |
| RT-0.8-006 | Major | Policy lint now covers broad destructive grants, broad audit query, stale delegation, export controls, and rollback/audit weakening. |
| RT-0.8-007 | Major | PACK-05 through PACK-09 `source_refs` now exactly match owning spec front matter and the new Phase 0.8 traceability check rejects missing or stale extra refs. |
| RT-0.8-008 | Major | First vertical slice conflicts are explicitly classified as implementation-blocking gaps, not design-freeze blockers. |
| RT-0.8-009 | Minor | The authorization TLA model now has initial-state alternatives and reachability predicates for the decision path, policy transaction path, and emergency access path. Policy approval and emergency authorization transitions now set the guard variables needed to make the modeled paths reachable. |
| RT-0.8-010 | Minor | Future implementation prompt sections are retitled as inactive future templates and explicitly state that they do not authorize production, hosted daemon, or portable semantic-core implementation. |
| RT-0.8-011 | Minor | Phase 0.8 job/spool owned identifiers were renamed away from external job-control vocabulary: `JOB_CONTROL_STREAM_ERROR`, `INPUT_STREAM`, `OUTPUT_STREAM`, and `FUZZ-MFOS-JOB-CONTROL-STREAM-0001` now replace the prior terms in schemas, formal artifacts, tests, fuzz plans, and reports. Naming-safety release validation passes. |
| RT-0.8-012 | Minor | `SpoolEntry` schema now carries an explicit evidence-boundary block and clarifies that `audit_correlation_id` is lookup linkage only, not an audit record or evidence substitute. |

## Non-Blocking Issues

No unresolved Phase 0.8 red-team issues remain after the current naming-safety
and model-reachability closure pass.

## Implementation-Blocking First Vertical Slice Issues

These are not Phase 0.8 design-freeze blockers, but they block Phase 0.9
executable-spec or implementation use until resolved or converted to explicit
fail-closed `MFOS_ERR_SPEC_GAP` behavior:

- Dataset staging and dataset content fixture semantics.
- ECHO program identity and program catalog semantics.
- Queue, select, and workload policy executable semantics.
- Failure-summary spool owner, security, and redaction semantics.
- Catalog transaction fixture boundaries.
- Duplicate spec numbering or spec-index ambiguity.

## Gate Policy

No Phase 0.8 artifact is implementation-ready. Traceability evidence must not
count a requirement as covered unless every referenced test ID resolves to an
actual test catalog entry and the corresponding negative path is present.
