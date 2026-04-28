# Phase 0.8 Cross-Domain Lead Report

Status: Draft  
Date: 2026-04-27  
Lead role: MFOS Phase 0.8 Cross-Domain Integration Lead  
Scope: First vertical slice semantic contract only.  
Production implementation: not started and not authorized.

## Summary

Phase 0.8 defines the first vertical slice contract across operator command,
authorization, catalog, dataset, job, spool, and audit domains. The contract
focuses on two paths:

- HELLO success: `ALICE` reads `USER.ALICE.INPUT`, `ECHO` writes OUTPUT_STREAM, the job
  completes `RC=0`, and audit evidence exists.
- BOB denied: `BOB` attempts to read `USER.ALICE.INPUT`, the read is denied,
  no dataset handle exists, denial audit precedes the final result, a protected
  failure summary is captured, and the operator sees `FAILED
  REASON=POLICY_DENIED`.

No production code was added. No hosted prototype behavior is claimed.

## Files Added

| Path | Purpose |
| --- | --- |
| `docs/design/specs/30-first-vertical-slice-contract.md` | Normative semantic obligations and sequence tables for HELLO and BOB paths. |
| `tests/catalog/phase-0-8-first-vertical-slice-tests.yml` | Planned integration, negative, and conformance tests for the contract. |
| `evidence/traceability/phase-0-8-first-vertical-slice.yml` | Draft design-only requirement/test/evidence traceability. |
| `reports/phase-0-9-readiness.md` | Phase 0.9 readiness and conflict list. |
| `reports/phase-0-8-cross-domain-lead.md` | This cross-domain handoff report. |

## Contract Decisions

| Domain | Decision |
| --- | --- |
| Operator | Raw operator text must parse into typed command objects before target resolution, authorization, execution, audit, or display. |
| Authorization | `securityd` remains the final PDP for protected commands, job submit, dataset read, program execute, spool create, and browse/display. |
| Catalog | `catalogd` resolution supplies committed object identity and generation; it does not grant access. |
| Dataset | ALICE allowed read creates a bound handle; BOB denied read creates no active, cached, deferred, placeholder, or reusable handle. |
| Job | Job effective principal is established before dataset, program, or spool open. The BOB path fails at dataset open and must not execute `ECHO` against protected content. |
| Spool | HELLO OUTPUT_STREAM and BOB failure summary are protected spool entries. The BOB summary must not include protected dataset content. |
| Audit | Required audit evidence comes from `auditd`; spool output, console display, and diagnostic logs cannot substitute. |
| Evidence | Phase 0.8 evidence is draft design traceability only, not implementation proof. |

## Sequence Coverage

The contract includes normative sequence tables:

- HELLO success sequence `H01` through `H22`.
- BOB denied sequence `B01` through `B18`.

The planned test catalog maps those sequence IDs to:

- `TEST-MFOS-FVS-HELLO-SUCCESS-0001`
- `NEG-MFOS-FVS-BOB-DENIED-0001`
- `TEST-MFOS-FVS-AUDIT-ORDER-0001`
- `NEG-MFOS-FVS-NO-DATASET-HANDLE-0001`
- `TEST-MFOS-FVS-SPOOL-SUMMARY-0001`
- `NEG-MFOS-FVS-SPOOL-NOT-AUDIT-0001`

## Phase 0.9 Readiness Items

| ID | Required Phase 0.9 action | Status |
| --- | --- | --- |
| `FVS-CONFLICT-001` | Confirm operatord target refs and audit payloads preserve submitter plus requested effective principal. | Aligned by job/spool Phase 0.8; test confirmation needed. |
| `FVS-CONFLICT-002` | Specify dataset staging command or fixture construction rule. | Open. |
| `FVS-CONFLICT-003` | Specify `ECHO` program identity and execute authorization. | Open. |
| `FVS-CONFLICT-004` | Choose materialized queue/select lifecycle or hosted immediate-run equivalent. | Open. |
| `FVS-CONFLICT-005` | Define failure-summary spool owner, security profile, browse/display principal, and redaction. | Open. |
| `FVS-CONFLICT-006` | Confirm vertical-slice tests use `AUDITD_DURABLE_APPEND` before final denial. | Aligned by audit Phase 0.8; test confirmation needed. |
| `FVS-CONFLICT-007` | Define catalog/dataset fixture setup transaction and rollback behavior. | Open. |
| `FVS-CONFLICT-008` | Resolve or explicitly allow the duplicate `30-` spec numbering. | Open. |

## Gate Position

```yaml
phase_0_8_scope_satisfied: true
semantic_contract_only: true
production_code_changed: false
implementation_allowed: false
phase_0_9_ready_for_semantic_review: true
phase_0_9_ready_for_implementation: false
```

The practical next step is Phase 0.9 conflict closure and confirmation of the
domain-spec alignments above. Implementation should stay blocked until fixture
setup, program identity, queue/select behavior, failure-summary spool policy,
and numbering/index decisions are explicit.
