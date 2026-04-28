# Phase 0.8 Red Team Review

Date: 2026-04-27

Scope: Phase 0.8 authorization, audit, dataset catalog, job spool, operator console, cross-domain, first vertical slice, traceability, pack contracts, schemas, test catalogs, and formal model artifacts.

Reviewer role: MFOS Phase 0.8 Red Team Reviewer.

Ownership note: this review is report-only. No production code was changed.

## Gate Verdict

Post-remediation verdict: Phase 0.8 is cleared for design-level Core Semantics
Freeze only. Phase 1 implementation, hosted prototype work, hosted daemon work,
Portable Semantic Core work, and production implementation remain blocked.

Initial review verdict before remediation: Phase 0.8 was not cleared for Phase 1
implementation or hosted prototype work.

The core domain prose contains strong fail-closed intent in several places,
including deny-before-return audit ordering, catalog committed-state boundaries,
dataset-not-POSIX framing, spool-not-audit-evidence framing, typed operator
commands, and no root shell. The initial review found fake-success and
implementation-authorization risks in traceability and pack/index metadata; the
post-review remediation pass closed the Critical/Major items for design-freeze
use. Phase 0.8 outputs still are not implementation-ready.

Specification-only freeze can proceed because the Critical and Major findings
below were corrected in the post-review remediation pass. Minor findings remain
tracked in `reports/phase-0-8-open-issues.md`.

## Findings

### RT-0.8-001 - Critical - Traceability References Non-Existent Tests

Risk areas: fake success, missing negative tests, missing audit obligations, authorization bypass evidence gaps.

Evidence:

- [phase-0-8-requirement-to-test.yml](/home/nia/mfos/evidence/traceability/phase-0-8-requirement-to-test.yml:3) maps Phase 0.8 requirements to `010x`-style test IDs such as `TEST-MFOS-AUTH-SECURITY-DECISION-0101`, `NEG-MFOS-AUTH-BYPASS-0101`, `TEST-MFOS-AUDIT-DENY-BEFORE-RETURN-0102`, and `NEG-MFOS-CATALOG-UNCOMMITTED-0101`.
- [phase-0-8-authorization-tests.yml](/home/nia/mfos/tests/catalog/phase-0-8-authorization-tests.yml:22) and sibling catalogs define `000x`-style test IDs such as `TEST-MFOS-AUTH-POS-0001`.
- A local consistency check found 48 traceability references to test IDs that do not exist in the Phase 0.8 test catalogs.

Impact:

Release evidence can report coverage for negative authorization, audit, catalog, spool, and operator tests that are not actually present. This is a direct fake-success risk and undermines the red-team requirements for authorization bypass, audit bypass, deny-before-return, uncommitted catalog exposure, root shell confusion, stale handle ambiguity, and spool/audit confusion.

Required correction:

Reconcile the Phase 0.8 requirement and test ID namespaces. Add or rename the missing tests, then add a validator that fails when any traceability `tests:` entry does not resolve to a cataloged test ID.

### RT-0.8-002 - Major - Spec Index Implies Hosted Prototype Authorization

Risk areas: Phase 1 implementation authorization, fake success, compatibility implications.

Evidence:

- [INDEX.md](/home/nia/mfos/docs/design/specs/INDEX.md:56) marks `06-authorization` through `10-operator-console` as `Ready for hosted prototype`.
- [PACKS.md](/home/nia/mfos/docs/design/packs/PACKS.md:119) records Phase 0.8 packs as `production: false`, `hosted_daemon: false`, `portable_semantic_core: false`, `executable_spec: false`, and `specification_only: true`.
- [PACKS.md](/home/nia/mfos/docs/design/packs/PACKS.md:129) says no Phase 0.8 pack authorizes Phase 1 implementation.

Impact:

Implementation agents can follow the global spec index and start hosted prototype work despite the pack gate forbidding it. The conflict creates an implementation-authorization bypass at the documentation layer.

Required correction:

Update the global index and readiness wording so Phase 0.8 domains are described as specification-only and frozen for review, not ready for hosted prototype, unless a later explicit gate changes the pack metadata.

### RT-0.8-003 - Major - Emergency Access Duration and Result Names Conflict

Risk areas: broad emergency access, policy lint gaps, invalid transition gaps, audit obligation ambiguity.

Evidence:

- [06-authorization.md](/home/nia/mfos/docs/design/specs/06-authorization.md:571) limits emergency activation lifetime to at most 60 minutes and says longer activation requires `SPEC_GAP`.
- [10-operator-console.md](/home/nia/mfos/docs/design/specs/10-operator-console.md:439) accepts `2H` and `4H` duration tokens.
- [10-operator-console.md](/home/nia/mfos/docs/design/specs/10-operator-console.md:673) says emergency mode has a maximum duration of four hours.
- [06-authorization.md](/home/nia/mfos/docs/design/specs/06-authorization.md:398) uses `MFOS_AUTH_REQUIRE_EMERGENCY_ACCESS`.
- [10-operator-console.md](/home/nia/mfos/docs/design/specs/10-operator-console.md:552) and [audit-record.schema.yml](/home/nia/mfos/schemas/mfos/audit-record.schema.yml:121) use `REQUIRE_BREAK_GLASS`.

Impact:

Emergency authorization may be broader than the authorization model allows. The inconsistent result names also create room for fail-open mapping errors between operatord, securityd, and auditd.

Required correction:

Align operator emergency duration with the authorization limit, or explicitly mark longer durations as `SPEC_GAP` and fail closed. Choose one canonical authorization result enum and document any audit-only reason mapping. Add negative tests for durations over the limit and for unrecognized emergency decision results.

### RT-0.8-004 - Major - Operator SYSTEM and SERVICE Targets Are Not Registered Authorization Resource Classes

Risk areas: authorization bypass, operator/root shell confusion, broad emergency access.

Evidence:

- [10-operator-console.md](/home/nia/mfos/docs/design/specs/10-operator-console.md:472) requires `SYSTEM / ADMINISTER` for emergency commands.
- [10-operator-console.md](/home/nia/mfos/docs/design/specs/10-operator-console.md:486) resolves display targets to `SYSTEM`, `PARTITION`, `SERVICE`, and `OPERATOR_COMMAND`.
- [operator-command.schema.yml](/home/nia/mfos/schemas/mfos/operator-command.schema.yml:79) permits `SERVICE` and `SYSTEM` resource types.
- [security-decision.schema.yml](/home/nia/mfos/schemas/mfos/security-decision.schema.yml:249) does not define `MFOS_RESOURCE_SYSTEM` or `MFOS_RESOURCE_SERVICE`.

Impact:

Operator commands can reference resource classes that the authorization decision schema does not recognize. Implementers may create local allow logic for system and service commands instead of routing through the governed security decision path.

Required correction:

Either register `SYSTEM` and `SERVICE` as authorization resource classes with operation matrices, or remap those operator targets to existing protected classes. Add negative tests proving unregistered resource types are rejected before command execution.

### RT-0.8-005 - Major - Operator DSN Grammar Conflicts With Dataset Catalog Grammar

Risk areas: dataset/POSIX confusion, catalog boundary bypass, compatibility implications.

Evidence:

- [08-dataset-catalog.md](/home/nia/mfos/docs/design/specs/08-dataset-catalog.md:145) freezes dataset names as dot-separated qualifiers where each qualifier starts with an uppercase letter, has length 1 to 8, and contains only uppercase letters, digits, `_`, or `-`.
- [08-dataset-catalog.md](/home/nia/mfos/docs/design/specs/08-dataset-catalog.md:163) says full z/OS catalog naming is not claimed and extensions are `SPEC_GAP`.
- [10-operator-console.md](/home/nia/mfos/docs/design/specs/10-operator-console.md:343) accepts operator `DSN_SEG` values beginning with digits or `$#@` and allows up to 32 characters per segment.

Impact:

Operator commands can parse and authorize dataset names that catalogd must reject. That creates a dataset/catalog confusion path and can produce fake success in operator workflows that never exercise catalog resolution.

Required correction:

Make operator dataset parsing import or delegate to the frozen catalog DSN grammar. Add negative operator tests for digit-leading qualifiers, `$#@` characters, over-8-character qualifiers, and any catalogd-boundary rejection.

### RT-0.8-006 - Major - Policy Lint Requirements Are Incomplete Across Specs

Risk areas: policy lint gaps, broad emergency access, missing negative tests, missing audit obligations.

Evidence:

- [06-authorization.md](/home/nia/mfos/docs/design/specs/06-authorization.md:620) requires linting for broad destructive permissions, authorized module authority, emergency access without expiry, policy update authority, redaction/export policy for spool and audit evidence, and rollback or weakening of audit/security posture.
- [33-policy-lint.md](/home/nia/mfos/docs/design/specs/33-policy-lint.md:143) defines a smaller rule set. For example, the wildcard destructive rule is narrowed to datasets, and the export rule is narrowed to spool or gateway export.
- [auth.yml](/home/nia/mfos/requirements/by-domain/auth.yml:170) also requires lint detection for broad audit-query access and stale delegation.

Impact:

A policy can pass the dedicated policy-lint spec while violating the broader authorization requirements. Missing lint coverage can enable broad emergency access, stale delegation, broad audit query, and weak evidence export policies.

Required correction:

Align `33-policy-lint.md` with `06-authorization.md` and `MFOS-REQ-AUTH-0105`. Add rules and tests for all required protected classes, broad audit-query access, stale delegation, audit/authorization evidence export, and rollback or audit-weakening changes.

### RT-0.8-007 - Major - Pack Source References Are Incomplete or Stale

Risk areas: missing source refs, compatibility implications, IBM-derived owned identifiers.

Evidence:

- [PACK-07-dataset-catalog/pack.yml](/home/nia/mfos/docs/design/packs/PACK-07-dataset-catalog/pack.yml:37) includes a source reference set that differs from [08-dataset-catalog.md](/home/nia/mfos/docs/design/specs/08-dataset-catalog.md:9).
- A local comparison found missing front-matter references in PACK-05 through PACK-09. Examples include RACF/SMF Type 80, JES/JES2, DFSMS catalogs, authorized programs, LPAR/DPM, and workload policy references depending on pack.
- PACK-07 includes `EXTREF-IBM-ZOS-UNIX-INTRODUCTION-0001` while the dataset catalog spec explicitly avoids POSIX semantics.

Impact:

Machine-readable pack contracts do not faithfully carry the source grounding from their owning specs. This weakens review evidence and makes compatibility boundaries harder to enforce.

Required correction:

Align pack `source_refs` with the owning spec front matter, or document a strict subset rule and validate it. Add a pack/source-ref consistency check.

### RT-0.8-008 - Major - First Vertical Slice Conflicts Remain Open While Gap Report Says No Blocking Gaps

Risk areas: fake success, invalid transition gaps, missing audit obligations, job identity confusion.

Evidence:

- [phase-0-8-gap-report.md](/home/nia/mfos/reports/phase-0-8-gap-report.md:6) says no blocking gaps remain for design-level freeze after listed corrections.
- [phase-0-9-readiness.md](/home/nia/mfos/reports/phase-0-9-readiness.md:47) lists first vertical slice conflicts for dataset staging, ECHO program identity, queue/select/workload policy semantics, failure-summary spool ownership, catalog transaction fixtures, and duplicate spec numbering.
- [30-first-vertical-slice-contract.md](/home/nia/mfos/docs/design/specs/30-first-vertical-slice-contract.md:115) requires typed dataset staging and content, while [30-first-vertical-slice-contract.md](/home/nia/mfos/docs/design/specs/30-first-vertical-slice-contract.md:161) says related readiness items remain open.

Impact:

The first vertical slice can be mistaken as implementation-ready even though key identity, catalog, queue, and spool semantics are unresolved.

Required correction:

Classify the listed first-vertical-slice conflicts as implementation-blocking open issues. Do not present the first vertical slice as implementation-ready until the conflicts are closed or converted into explicit fail-closed `SPEC_GAP` behavior.

### RT-0.8-009 - Minor - Formal Authorization Model Has Vacuous Unreachable Paths

Risk areas: invalid transition gaps, broad emergency access, policy update ambiguity.

Evidence:

- [MFOSAuthorization.tla](/home/nia/mfos/formal/tla/authorization/MFOSAuthorization.tla:309) defines emergency lifecycle transitions beginning at `REQUEST_EMERGENCY_ACCESS`.
- [MFOSAuthorization.tla](/home/nia/mfos/formal/tla/authorization/MFOSAuthorization.tla:229) defines policy transaction transitions beginning at `BEGIN_POLICY_TX`.
- The model initialization starts in request-received decision flow, and no reviewed transition reaches those lifecycle entry states from the initial state.

Impact:

Emergency and policy invariants can be satisfied vacuously if their lifecycles are unreachable in the checked model.

Required correction:

Add explicit model modes, initial-state alternatives, or transitions for decision, policy, and emergency workflows. Add reachability checks showing each lifecycle reaches nonterminal and terminal states before using the model as evidence.

Current resolution:

Resolved after review. `formal/tla/authorization/MFOSAuthorization.tla` now has
initial-state alternatives and explicit reachability predicates for the
decision path, policy transaction path, and emergency access path.

### RT-0.8-010 - Minor - AI Implementation Prompt Sections Conflict With Specification-Only Gate

Risk areas: Phase 1 implementation authorization, fake success, ID confusion.

Current resolution:

Resolved after review. Split-spec implementation prompt sections were retitled
as inactive future templates and now explicitly state that they do not
authorize production implementation, hosted daemon implementation, or portable
semantic-core implementation.

Evidence:

- [08-dataset-catalog.md](/home/nia/mfos/docs/design/specs/08-dataset-catalog.md:625) says "You are implementing MFOS catalogd/datasetd behavior."
- [10-operator-console.md](/home/nia/mfos/docs/design/specs/10-operator-console.md:975) says "You are implementing MFOS operatord behavior."
- Both sections use `000x` requirement IDs while other Phase 0.8 traceability artifacts use `010x` IDs.

Impact:

Implementation agents can treat prompt templates as active implementation authorization, and the ID mismatch compounds the traceability problem.

Required correction:

Retitle these as future implementation prompt templates that are inactive in Phase 0.8. Add explicit gate prerequisites and update the requirement IDs after namespace reconciliation.

### RT-0.8-011 - Minor - IBM-Derived Owned Identifiers Still Appear in Phase 0.8 Artifacts

Risk areas: IBM-derived owned identifiers, compatibility implications.

Current resolution:

Resolved after review for the Phase 0.8 owned identifiers listed in this
finding. Job/spool schemas, formal artifacts, test catalogs, fuzz planning, and
reports now use MFOS-native job-control and input/output stream names.
Naming-safety release validation passes.

Evidence:

- `JOB_CONTROL_STREAM_ERROR`, `FUZZ-MFOS-JOB-CONTROL-STREAM-0001`, `INPUT_STREAM`, `OUTPUT_STREAM`, and `WLM` appear in schemas, formal artifacts, tests, fuzz plans, or operator commands.
- [phase-0-8-gap-report.md](/home/nia/mfos/reports/phase-0-8-gap-report.md:17) tracks some IBM-derived naming concerns but does not cover all Phase 0.8 additions.

Impact:

Owned identifiers may imply compatibility or inherit IBM terminology beyond the stated non-compatibility boundary.

Required correction:

Decide whether these terms have explicit non-compatibility waivers. Otherwise rename owned IDs to MFOS-native terms such as batch stream error, input stream, output spool, or workload policy equivalents.

### RT-0.8-012 - Minor - SpoolEntry Schema Can Be Misread as Authorization Evidence

Risk areas: spool/audit confusion, missing audit obligations.

Current resolution:

Resolved after review. `schemas/mfos/spool-entry.schema.yml` now states that a
SpoolEntry is not audit evidence and that `audit_correlation_id` is lookup
linkage only, not an audit record or evidence substitute.

Evidence:

- [09-job-spool.md](/home/nia/mfos/docs/design/specs/09-job-spool.md:390) defines `SpoolEntry` with `audit_correlation_id`.
- [spool-entry.schema.yml](/home/nia/mfos/schemas/mfos/spool-entry.schema.yml:1) requires `audit_correlation_id` but not `security_decision_id`, `policy_version`, or `audit_obligation_id`.
- The prose correctly states that spool content is not audit evidence, but the schema does not make the evidence boundary self-evident.

Impact:

Consumers may incorrectly treat a spool entry plus correlation ID as sufficient authorization or audit proof.

Required correction:

Either add explicit decision, policy, and audit-obligation references to spool metadata, or state in the schema description that these references live only in associated audit records and that spool metadata is not authorization evidence.

## Coverage Notes

The review did not find production Phase 0.8 implementation code beyond placeholder README files under `implementation/`.

The strongest Phase 0.8 security prose is in the audit, authorization, dataset catalog, job spool, and operator console specs. Those specs generally require deny-before-return, protected spool access, committed-only catalog resolution, no POSIX/raw-volume behavior, typed operator command execution, dual-control emergency access, and explicit audit obligations. The blocking issues above are primarily cross-artifact contradictions, stale machine-readable references, and implementation-gate ambiguity.

## Required Gate Corrections

Before Phase 0.8 is used as Phase 1 input:

1. Fix traceability so every referenced test ID exists and every required negative path has catalog coverage.
2. Remove or correct hosted-prototype readiness language for Phase 0.8 packs.
3. Resolve emergency duration and decision-result conflicts across authorization, operator, audit, schemas, tests, and TLA.
4. Register or remap operator `SYSTEM` and `SERVICE` resources in the authorization model.
5. Make operator DSN parsing identical to or delegated to dataset catalog DSN parsing.
6. Complete policy lint requirements and tests.
7. Align pack source references with spec source references.
8. Mark first vertical slice conflicts as implementation blockers until closed.

## Post-Review Remediation

Status after orchestrator correction pass on 2026-04-27:

| Finding | Remediation |
| --- | --- |
| RT-0.8-001 | Added concrete Phase 0.8 `010x` planned semantic test entries to domain catalogs and added `scripts/check-phase-0-8-traceability.py`, including checks that required test IDs are not generic alias placeholders. |
| RT-0.8-002 | Updated the split-spec index so PACK-05 through PACK-09 are specification-only and not hosted-prototype ready. |
| RT-0.8-003 | Aligned emergency duration to 60 minutes, changed the authorization result enum to `MFOS_AUTH_REQUIRE_BREAK_GLASS`, updated operator text and formal operator model to use `MFOS_AUTH_*` securityd result names, documented the audit-record projection boundary, and added over-limit/unknown-result negative test planning. |
| RT-0.8-004 | Registered `MFOS_RESOURCE_SYSTEM` and `MFOS_RESOURCE_SERVICE` in authorization prose and the SecurityDecision schema. |
| RT-0.8-005 | Aligned operator DSN grammar with the dataset/catalog grammar and added catalog-incompatible DSN negative test planning. |
| RT-0.8-006 | Expanded the policy lint spec to cover broad audit query, stale delegation, evidence export, broader destructive wildcards, and rollback/audit weakening. |
| RT-0.8-007 | Aligned PACK-05 through PACK-09 `source_refs` exactly with owning spec front matter and made the new Phase 0.8 traceability check reject both missing and stale/extra refs. |
| RT-0.8-008 | Reclassified first vertical slice conflicts as implementation-blocking gaps in the gap reports. |

Critical and Major findings are closed for the design-level Phase 0.8 freeze.
Minor findings remain in `reports/phase-0-8-open-issues.md`. Implementation is
still blocked.
