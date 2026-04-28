# Phase 0.8 Authorization Lead Report

Date: 2026-04-27

Owner: MFOS Phase 0.8 authorization lead

Status: Design freeze artifacts prepared. No production implementation is
authorized by this report.

## Scope Completed

- Updated `docs/design/specs/06-authorization.md` to a Phase 0.8 design freeze.
- Added `schemas/mfos/security-decision.schema.yml`.
- Added `schemas/mfos/policy-binding.schema.yml`.
- Added `formal/tla/authorization/MFOSAuthorization.tla`.
- Added `tests/catalog/phase-0-8-authorization-tests.yml`.

## Semantics Frozen

- Protected resource classes and valid operation families.
- Subject, object, operation, and decision context model.
- `SecurityDecision` result semantics, obligations, handle constraints, cache
  behavior, and evidence hooks.
- `PolicyBinding` effect, selector, obligation, delegation, emergency, and
  dual-control semantics.
- Policy versioning, policy epoch, security epoch, activation, rollback, lint,
  and stale-cache handling.
- Delegation, emergency access, operator confirmation, dual control, Guard
  approval, and audit-before-return or audit-before-effect barriers.
- Failure modes, invalid transitions, invariants, positive tests, negative
  tests, fuzz tests, evidence requirements, and spec gaps.

## Namespace and Source Controls

- Authorization-owned requirement, test, evidence, invariant, gap, schema,
  formal, lint, and state IDs use MFOS-owned namespaces.
- Source references in authorization-owned artifacts use `EXTREF-*` IDs only.
- Source anchors used:
  - `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`
  - `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`
  - `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001`
  - `EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001`
  - `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`
  - `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`
  - `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`
  - `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`
  - `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001`
  - `EXTREF-IBM-Z-LPAR-INTRODUCTION-0001`
  - `EXTREF-IBM-Z-DPM-0001`

## Evidence Required Before Implementation

- `EV-MFOS-AUTH-SPEC-0001`: reviewed authorization design freeze.
- `EV-MFOS-AUTH-SCHEMA-0001`: `SecurityDecision` schema review.
- `EV-MFOS-AUTH-SCHEMA-0002`: `PolicyBinding` schema review.
- `EV-MFOS-AUTH-FORMAL-0001`: state-machine review.
- `EV-MFOS-AUTH-TESTCAT-0001`: phase test catalog review.
- `EV-MFOS-AUTH-LINT-0001`: policy lint gate evidence.
- `EV-MFOS-AUTH-AUDIT-0001`: audit barrier evidence.
- `EV-MFOS-AUTH-GAP-0001`: spec-gap fail-closed review.

## Validation Performed

- `python3 scripts/validate-spec-front-matter.py --mode draft`
- `python3 scripts/check-source-grounding.py --mode draft`
- `python3 scripts/check-extref-namespace.py --mode draft`
- `python3 scripts/check-mf-owned-names.py --mode draft`
- `python3 scripts/check-requirement-namespace.py --mode draft`
- YAML parse check for the two schemas and phase test catalog.
- `./scripts/validate-all.sh --check`

All listed checks completed successfully.

## Open Spec Gaps

The design freeze keeps these gaps explicit and fail-closed:

- Policy expression grammar.
- Bootstrap and recovery query policy.
- External authentication provider integration.
- MFA, dual-control, confirmation, and Guard token wire formats.
- Decision cache protocol and distributed invalidation transport.
- Redaction policy language for authorization evidence export.
- Delegation administration workflow.
- Executable policy lint rule language.
- Profile-specific partition backend authority mapping.
- POSIX subsystem authorization mapping.

## Implementation Boundary

No production code was written. These artifacts support review, schema
alignment, formal-model review, test planning, and evidence planning only.
Future implementation work must first close or explicitly fail-close every
`MFOS-GAP-AUTH-*` item and add reviewed registry/evidence entries for the
requirements it uses.
