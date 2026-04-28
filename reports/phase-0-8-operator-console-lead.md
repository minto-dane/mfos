# Phase 0.8 Operator Console Lead Report

Date: 2026-04-27

Owner: MFOS Phase 0.8 Operator Console Lead

Status: Semantics frozen for Phase 0.8 design and test planning. No production
code was added.

## Owned Artifacts

| Artifact | Status |
| --- | --- |
| `docs/design/specs/10-operator-console.md` | Rewritten as Phase 0.8 semantics freeze. |
| `schemas/mfos/operator-command.schema.yml` | Added machine-readable design schema. |
| `formal/tla/operator-command/` | Added TLA+ design state-machine artifact and invariant list. |
| `tests/catalog/phase-0-8-operator-console-tests.yml` | Added positive, negative, fault-injection, conformance, and fuzz catalog. |
| `reports/phase-0-8-operator-console-lead.md` | Added this closure report. |

## Source Reference Boundary

Only EXTREF source refs are used:

- `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`
- `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`
- `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`
- `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001`
- `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`
- `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001`
- `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`
- `EXTREF-IBM-ZOS-JES2-LIBRARY-0001`
- `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`
- `EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001`

## Frozen Decisions

- Operator console is the first interactive MFOS UI and is not a root shell.
- Raw command text is hashed and parsed into typed `OperatorCommand` objects;
  raw text is never an execution path.
- The initial command grammar covers display, user definition, dataset
  definition, inline job submit, job cancel, spool browse/purge, workload policy
  activation, emergency enter/exit, confirmation, cancellation, approval, and
  rejection of pending commands.
- Every command has a primary authority class and risk class.
- Target resolution must precede authorization, and stale target generation
  requires re-resolution and reauthorization or fail-closed behavior.
- `securityd` remains the policy decision point; `operatord` is an enforcement
  point and cannot broaden authority.
- Confirmation and dual control are obligations, not authorization decisions.
- Same-actor dual control is always denied.
- Emergency mode requires identity, reason, expiry, authorization, and audit; it
  cannot disable auditd or bypass securityd.
- Automation is caller type plus ingress authority, not elevated privilege.
- Denial audit must precede denial display when an audit obligation is present.
- Display is a typed `ConsoleDisplayFrame`, not shell output.
- Unsupported and spec-gap commands have no target side effects.
- Invalid lifecycle transitions fail closed.

## Evidence Required

- Grammar review record.
- OperatorCommand schema validation report.
- Formal state-machine review or model-checking report.
- Positive test results for boot, parse, schema, display, dataset, submit,
  spool, cancel, purge, dual control, emergency, and automation paths.
- Negative test results for unauthenticated use, unauthorized command, shell
  text, missing confirmation, same-actor approval, stale approval, emergency
  misuse, automation bypass, stale target, audit outage, invalid transition,
  policy-version mismatch, and unredacted display.
- Fuzz corpus manifest for parser, inline submit, target resolution,
  confirmation, dual control, emergency, automation, and display frame targets.
- Audit ordering report showing denial audit before denial display.
- No-root-shell boot report.
- Spec-gap ledger.

## Remaining Spec Gaps

The following remain implementation-blocking for the affected feature:

- Concrete authentication backend and terminal secure-attention model.
- Final policy bundle encoding for command profiles and rate-limit values.
- Full display message catalog and localization rules.
- Guard emergency approval API details for High-Assurance profiles.
- Concrete audit payload schema version for every operator audit event.
- Recovery-mode subset when auditd or securityd is degraded.
- Formal model checking harness values and CI integration.
- Exact production evidence archive paths for Phase 0.8 test outputs.

## No Production Code Statement

This Phase 0.8 pass changed only design, schema, formal, test-catalog, and report
artifacts. It did not add or edit production implementation code.
