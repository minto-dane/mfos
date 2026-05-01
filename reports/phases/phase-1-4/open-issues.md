# Phase 1.4 Open Issues

Status date: 2026-05-01
Status: current planning-only issue ledger.

These issues are known before Phase 1.4 implementation begins. None of them
authorize production code or Phase 1.4 semantic implementation in this PR.

## Implementation-Entry Issues

| ID | Classification | Issue | Required disposition |
| --- | --- | --- | --- |
| `P14-OPEN-001` | deferred_to_phase_1_4_implementation | No Phase 1.4 generated traceability package exists. | Add `evidence/traceability/generated/phase-1-4/` only with real generated rows. |
| `P14-OPEN-002` | deferred_to_phase_1_4_implementation | No Phase 1.4 coverage checker exists. | Add `scripts/check-phase1-4-job-spool-operator-coverage.py` with the real generator and artifacts. |
| `P14-OPEN-003` | deferred_to_phase_1_4_implementation | Current Job/Spool and Operator Dafny surfaces are coarse and do not prove the full required Phase 1.4 row set. | Strengthen or replace with explicit verified properties. |
| `P14-OPEN-004` | deferred_to_phase_1_4_implementation | DD catalog-bypass and authorization-bypass seed fixtures may need split or annotation before C5. | Keep rows distinguishable in generated coverage. |
| `P14-OPEN-005` | deferred_to_phase_1_4_implementation | First vertical slice C5 currently predates Phase 1.4 deepening and must not be upgraded by inference. | Link FVS completion dependencies to generated Phase 1.4 evidence before claiming more. |
| `P14-OPEN-014` | source_grounding_review_needed | MFOS-native job-control grammar and DD-shaped identifiers retain a source-grounding risk. | Refactor or explicitly re-bound the terms before semantic evaluator claims use those shapes. |

## Dependency Issues

| ID | Classification | Issue | Required disposition |
| --- | --- | --- | --- |
| `P14-OPEN-006` | dependency_on_phase_1_2 | Operator, spool, and job-deny paths depend on Authorization/Audit decisions and audit-unavailable fail-closed behavior. | Reuse Phase 1.2 evidence at its actual scoped level. |
| `P14-OPEN-007` | dependency_on_phase_1_3 | DD resolution depends on committed-entry-only catalog resolution and dataset handle binding. | Reuse Phase 1.3 evidence at its actual scoped level. |
| `P14-OPEN-008` | dependency_on_phase_1_3 | Crash-mid-commit recovery selection is not fully modeled. | Do not claim full crash-recovery behavior through Job/Spool DD rows. |

## Deferred Beyond Phase 1.4

| ID | Classification | Issue | Required disposition |
| --- | --- | --- | --- |
| `P14-OPEN-009` | deferred_beyond_phase_1_4 | Full job-control parser, procedures, symbolic parameters, continuation, conditionals, restart, and parallel steps. | Keep as unsupported or spec-gap unless later authorized. |
| `P14-OPEN-010` | deferred_beyond_phase_1_4 | Real spool content browse, purge, export, quotas, record formats, and external gateways. | Keep symbolic and protected-resource-only in Phase 1.4. |
| `P14-OPEN-011` | deferred_beyond_phase_1_4 | Full operator parser, target resolver, display redaction engine, MFA, token binding, rate limiting, replay protection, and degraded recovery. | Keep to verified symbolic properties unless later authorized. |
| `P14-OPEN-012` | not_authorized | Production `jobd`, `spoold`, `operatord`, `securityd`, `auditd`, `catalogd`, `datasetd`, nucleus, PXM, Guard, MFVM, CVM, SGX, and cluster runtime. | Must remain absent. |
| `P14-OPEN-013` | not_authorized | Rust semantic-core, Portable Semantic Core, hosted daemon, hosted semantic prototype, and semantic runner implementation. | Must remain absent. |

## Open-Issue Judgment

```yaml
phase_1_4_open_issues_classified: true
phase_1_4_entry_blockers_for_planning_remaining: false
phase_1_4_implementation_blockers_remaining: true
phase_1_4_implementation_started: false
production_implementation_allowed: false
rust_phase_1_canonical_semantics_allowed: false
hosted_daemon_implementation_allowed: false
recommended_next_action: resolve implementation-entry issues in a later non-production Dafny PR
```
