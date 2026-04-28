---
spec_id: MFOS-SPEC-30-FIRST-VERTICAL-SLICE-CONTRACT
title: MFOS First Vertical Slice Semantic Contract
canonical_language: en-US
japanese_mirror: missing
status: draft
owner: MFOS architecture
last_reviewed: '2026-04-27'
source_refs:
- EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
- EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001
- EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001
- EXTREF-IBM-ZOS-JES-INTRODUCTION-0001
- EXTREF-IBM-ZOS-JES-JOB-FLOW-0001
- EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001
requirement_refs:
- MFOS-REQ-AUTH-0101
- MFOS-REQ-AUTH-0102
- MFOS-REQ-AUDIT-0102
- MFOS-REQ-CATALOG-0101
- MFOS-REQ-DATASET-0101
- MFOS-REQ-JOB-0101
- MFOS-REQ-JOB-0102
- MFOS-REQ-SPOOL-0101
- MFOS-REQ-OPER-0101
- MFOS-REQ-AUDIT-0104
claim_refs: []
test_refs:
- TEST-MFOS-VSLICE-HELLO-0001
- NEG-MFOS-VSLICE-BOB-DENIED-0001
- TEST-MFOS-FVS-HELLO-SUCCESS-0001
- NEG-MFOS-FVS-BOB-DENIED-0001
- TEST-MFOS-FVS-AUDIT-ORDER-0001
- NEG-MFOS-FVS-NO-DATASET-HANDLE-0001
- TEST-MFOS-FVS-SPOOL-SUMMARY-0001
- NEG-MFOS-FVS-SPOOL-NOT-AUDIT-0001
evidence_refs:
- EV-MFOS-VSLICE-HELLO-0001
- EV-MFOS-VSLICE-BOB-DENIED-0001
- EV-MFOS-FVS-CONTRACT-0001
- EV-MFOS-FVS-TRACE-0001
- EV-MFOS-FVS-READINESS-0001
implementation_allowed: false
downstream_packs:
- PACK-05
- PACK-06
- PACK-07
- PACK-08
- PACK-09
spec_gap_policy: implementation_must_not_infer_or_fill_gaps
---
# MFOS First Vertical Slice Semantic Contract

Status: Draft Phase 0.8 freeze artifact.

This document specifies the first MFOS enterprise semantic vertical slice. It is
not executable code and does not authorize Phase 1 implementation.

MFOS is source-grounded and independently specified. It does not claim
compatibility with external operating systems, products, interfaces, record
layouts, command syntax, macro interfaces, or documentation.

## 1. Purpose

Freeze the semantic contract connecting operator command, authorization,
catalog resolution, dataset handle creation, job lifecycle, spool output, and
audit evidence for the first success and failure flows.

## 2. Source References

| Source ID | Use |
| --- | --- |
| EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001 | Unauthorized-bypass boundary inspiration. |
| EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001 | External authorization/resource-profile background. |
| EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001 | External dataset/catalog background. |
| EXTREF-IBM-ZOS-JES-INTRODUCTION-0001 | External batch job/spool background. |
| EXTREF-IBM-ZOS-JES-JOB-FLOW-0001 | External job flow background. |
| EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | External audit/accounting background. |

## 3. Success Path Contract

| step_id | actor | operation | required_spec | required_requirement | required_audit | expected_result | failure_mode | evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| VS-S-001 | operator | define ALICE principal | 10-operator-console / 06-authorization | MFOS-REQ-OPER-0101 / MFOS-REQ-AUTH-0101 | OPERATOR_COMMAND | principal definition accepted as semantic plan | MFOS_ERR_UNAUTHORIZED | EV-MFOS-VSLICE-HELLO-0001 |
| VS-S-002 | operator | define committed dataset entry | 08-dataset-catalog | MFOS-REQ-CATALOG-0101 | CATALOG_UPDATE | committed catalog entry exists | MFOS_ERR_CATALOG_NOT_FOUND | EV-MFOS-VSLICE-HELLO-0001 |
| VS-S-003 | operator | submit HELLO job | 10-operator-console / 09-job-spool | MFOS-REQ-OPER-0101 / MFOS-REQ-JOB-0101 | JOB_SUBMIT | job identity and effective principal established | MFOS_ERR_UNAUTHORIZED | EV-MFOS-VSLICE-HELLO-0001 |
| VS-S-004 | jobd | resolve input DD | 09-job-spool / 08-dataset-catalog | MFOS-REQ-JOB-0102 / MFOS-REQ-CATALOG-0101 | DATASET_OPEN_ALLOW | catalogd returns committed dataset entry | MFOS_ERR_CATALOG_NOT_FOUND | EV-MFOS-VSLICE-HELLO-0001 |
| VS-S-005 | datasetd | create read handle | 08-dataset-catalog / 06-authorization | MFOS-REQ-DATASET-0101 / MFOS-REQ-AUTH-0102 | DATASET_OPEN_ALLOW | handle bound to decision, policy, and generations | MFOS_ERR_STALE_HANDLE | EV-MFOS-VSLICE-HELLO-0001 |
| VS-S-006 | jobd | run ECHO step | 09-job-spool | MFOS-REQ-JOB-0101 | STEP_EXECUTE | step completes RC=0 | MFOS_ERR_SPEC_GAP | EV-MFOS-VSLICE-HELLO-0001 |
| VS-S-007 | spoold | capture OUTPUT_STREAM | 09-job-spool | MFOS-REQ-SPOOL-0101 | SPOOL_CREATE | spool entry created as protected resource | MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE | EV-MFOS-VSLICE-HELLO-0001 |
| VS-S-008 | operatord | display COMPLETE RC=0 | 10-operator-console / 07-audit | MFOS-REQ-OPER-0101 / MFOS-REQ-AUDIT-0102 | JOB_COMPLETE | operator display reflects complete state | MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE | EV-MFOS-VSLICE-HELLO-0001 |

## 4. Failure Path Contract

| step_id | actor | operation | required_spec | required_requirement | required_audit | expected_result | failure_mode | evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| VS-F-001 | operator | submit BOB job | 10-operator-console / 09-job-spool | MFOS-REQ-OPER-0101 / MFOS-REQ-JOB-0101 | JOB_SUBMIT | job accepted for semantic validation | MFOS_ERR_UNAUTHORIZED | EV-MFOS-VSLICE-BOB-DENIED-0001 |
| VS-F-002 | jobd | establish BOB principal | 09-job-spool / 06-authorization | MFOS-REQ-JOB-0101 / MFOS-REQ-AUTH-0101 | JOB_IDENTITY | BOB effective principal established | MFOS_ERR_UNAUTHORIZED | EV-MFOS-VSLICE-BOB-DENIED-0001 |
| VS-F-003 | jobd | resolve ALICE dataset DD | 09-job-spool / 08-dataset-catalog | MFOS-REQ-JOB-0102 / MFOS-REQ-CATALOG-0101 | DATASET_OPEN_DENY | securityd DENY for BOB READ | MFOS_ERR_POLICY_DENIED | EV-MFOS-VSLICE-BOB-DENIED-0001 |
| VS-F-004 | auditd | record OPEN_DENY | 07-audit | MFOS-REQ-AUDIT-0102 | OPEN_DENY | durable audit exists before jobd final result | MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE | EV-MFOS-VSLICE-BOB-DENIED-0001 |
| VS-F-005 | datasetd | deny handle creation | 08-dataset-catalog / 06-authorization | MFOS-REQ-DATASET-0101 / MFOS-REQ-AUTH-0102 | DATASET_HANDLE_DENY | no dataset handle exists | MFOS_ERR_POLICY_DENIED | EV-MFOS-VSLICE-BOB-DENIED-0001 |
| VS-F-006 | jobd | mark step failed | 09-job-spool | MFOS-REQ-JOB-0102 | JOB_STEP_FAILED | job failed with POLICY_DENIED reason | MFOS_ERR_POLICY_DENIED | EV-MFOS-VSLICE-BOB-DENIED-0001 |
| VS-F-007 | spoold | capture failure summary | 09-job-spool | MFOS-REQ-SPOOL-0101 | SPOOL_CREATE_FAILURE_SUMMARY | failure summary protected as spool entry | MFOS_ERR_AUDIT_REQUIRED_BUT_UNAVAILABLE | EV-MFOS-VSLICE-BOB-DENIED-0001 |
| VS-F-008 | operatord | display FAILED | 10-operator-console | MFOS-REQ-OPER-0101 | OPERATOR_DISPLAY | operator sees FAILED REASON=POLICY_DENIED | MFOS_ERR_POLICY_DENIED | EV-MFOS-VSLICE-BOB-DENIED-0001 |

## 5. Invariants

- No dataset handle is created on DENY.
- OPEN_DENY is recorded before the caller receives the final result.
- jobd does not issue final authorization decisions.
- spool entries are protected resources, not audit evidence.
- operator display state follows audited lifecycle state, not ad hoc logs.

## 6. Spec Gaps

- Concrete executable harness is deferred to Phase 0.9.
- Concrete fixture encoding is deferred to Phase 0.9.
- Verified evidence artifacts are deferred until executable specs or tests exist.

## 7. Cross-Domain Obligations

The vertical slice is a contract across domains. No component may satisfy the
slice by returning local success while skipping another domain's protected
obligation.

| Domain | HELLO success obligation | BOB denied obligation |
| --- | --- | --- |
| Operator command | `operatord` parses fixture setup and `SUBMIT INLINE` into typed command objects, resolves targets, obtains authorization, executes through service APIs, and displays `COMPLETE RC=0` only after lifecycle and audit obligations are satisfied. | `operatord` parses `DEFINE USER BOB` and `SUBMIT INLINE`, obtains authorization, and displays `FAILED REASON=POLICY_DENIED` only after deny audit and failed job state exist. |
| Authorization decision | `securityd` allows fixture commands, submit, submit-as when `USER=` differs from submitter, ALICE dataset `READ`, program execute, spool create, and authorized display/browse. | `securityd` allows submit-as BOB if the fixture policy permits it, then denies BOB `READ` on `USER.ALICE.INPUT`; the dataset denial is the intended failure point. |
| Catalog resolution | `catalogd` resolves `USER.ALICE.INPUT` only from a committed catalog entry and returns canonical object identity plus generation metadata. | `catalogd` may resolve the same committed entry for decision context, but resolution is not access permission and must not create a handle. |
| Dataset handle | `datasetd` creates one active read handle only after allow decision, required audit obligation, generation binding, and expiry binding are established. | `datasetd` creates no active, cached, deferred, placeholder, closing, or reusable handle after deny. |
| Job lifecycle | `jobd` establishes effective principal before any dataset, program, input stream, or output stream open; HELLO converts, queues/selects or records an approved equivalent, executes `ECHO`, and completes `RC=0`. | `jobd` establishes BOB as effective principal, resolves the DD, receives denied open after audit, does not execute `ECHO` against protected input, marks the step failed, and completes the job failed. |
| Spool | `spoold` creates, writes, closes, and protects HELLO OUTPUT_STREAM; spool content is displayable only through authorized browse/display. | `spoold` creates a protected failure summary when authorized; the summary contains failure metadata only and no protected dataset content. |
| Audit evidence | `auditd` records command, decision, catalog, dataset open allow, job, spool, close, and complete events with correlation lineage. | `auditd` durably records the dataset open deny before final denied result; spool output, console display, and logs do not substitute for audit records. |

## 8. Detailed Sequence Tables

These sequence IDs refine the summary rows in sections 3 and 4. They specify
observable semantic order, not API names or transport shape.

### 8.1 HELLO Success Sequence

| Seq | Component | Action | Required semantic result |
| --- | --- | --- | --- |
| H01 | `operatord` | Authenticate or reuse `SYSOP` session. | Operator session and correlation ID exist. |
| H02 | `operatord` | Parse `DEFINE USER ALICE`. | Typed command object; raw text is not executed. |
| H03 | `securityd` / `auditd` | Authorize and audit user definition. | Allow decision and operator audit obligation satisfied. |
| H04 | `operatord` | Execute user definition. | `ALICE` principal exists for fixture use. |
| H05 | `operatord` | Parse and authorize dataset definition/staging. | Typed dataset target, owner `ALICE`, and no raw file shortcut. |
| H06 | `catalogd` | Commit `USER.ALICE.INPUT`. | Committed catalog entry with owner, security profile, and generation. |
| H07 | `datasetd` | Stage `HELLO MFOS` fixture content. | Protected dataset content exists with audit according to dataset fixture policy. |
| H08 | `operatord` | Parse `SUBMIT INLINE` for HELLO. | Typed submit command and bounded inline payload. |
| H09 | `securityd` / `auditd` | Authorize submit and submit-as `ALICE` when required. | Submit allow is audited; effective principal may be established. |
| H10 | `jobd` | Parse and convert MFOS job-control stream stream. | Typed job graph with `IN` dataset DD and `OUT` output-stream DD. |
| H11 | `jobd` | Queue/select or record approved equivalent. | Observable lifecycle does not skip identity or authorization. |
| H12 | `jobd` | Establish effective principal. | `ALICE` is bound before dataset, program, or spool open. |
| H13 | `catalogd` | Resolve `USER.ALICE.INPUT`. | Committed object ref and generations returned. |
| H14 | `securityd` / `auditd` | Authorize ALICE dataset `READ`. | Allow decision and required audit obligation exist. |
| H15 | `datasetd` | Create read handle. | Bound handle exists for ALICE, READ, policy version, generations, expiry, and correlation ID. |
| H16 | `securityd` / `auditd` | Authorize OUTPUT_STREAM spool create. | Protected spool create is allowed and auditable. |
| H17 | `spoold` | Open HELLO OUTPUT_STREAM entry. | Protected spool entry exists with owner, job ID, output class, profile, and retention. |
| H18 | `securityd` / `jobd` | Authorize and start `ECHO`. | Program execution occurs only after input and output resources are ready. |
| H19 | `jobd` / `spoold` | Read input and write OUTPUT_STREAM. | `HELLO MFOS` output is captured through authorized resources. |
| H20 | `datasetd` / `spoold` | Close resources. | Dataset handle and spool entry close events are recorded. |
| H21 | `jobd` | Complete step and job. | Step and job complete with `RC=0`. |
| H22 | `operatord` | Display result. | Operator sees `COMPLETE RC=0`; display is not audit evidence. |

### 8.2 BOB Denied Sequence

| Seq | Component | Action | Required semantic result |
| --- | --- | --- | --- |
| B01 | `operatord` | Authenticate or reuse `SYSOP` session. | Operator session and correlation ID exist. |
| B02 | `operatord` | Parse `DEFINE USER BOB`. | Typed command object; raw text is not executed. |
| B03 | `securityd` / `auditd` | Authorize and audit user definition. | Allow decision and operator audit obligation satisfied. |
| B04 | `operatord` | Execute user definition. | `BOB` principal exists for fixture use. |
| B05 | `operatord` | Parse `SUBMIT INLINE` for BAD. | Typed submit command and bounded inline payload. |
| B06 | `securityd` / `auditd` | Authorize submit and submit-as `BOB` when required. | Submit allow is audited; effective principal may be established. |
| B07 | `jobd` | Parse and convert MFOS job-control stream stream. | Typed job graph is valid; failure has not occurred yet. |
| B08 | `jobd` | Queue/select or record approved equivalent. | Observable lifecycle does not skip identity or authorization. |
| B09 | `jobd` | Establish effective principal. | `BOB` is bound before dataset, program, or spool open. |
| B10 | `catalogd` | Resolve `USER.ALICE.INPUT`. | Committed object ref and generations returned for decision context. |
| B11 | `securityd` | Deny BOB dataset `READ`. | Deny decision includes subject, object, operation, context, reason, and policy version. |
| B12 | `auditd` | Durably append deny audit. | `DATASET_OPEN_DENY` or equivalent deny record exists before final denied result. |
| B13 | `datasetd` | Return denied open to `jobd`. | No dataset handle of any kind is created. |
| B14 | `jobd` | Mark step failed. | `ECHO` does not execute against protected dataset content. |
| B15 | `securityd` / `auditd` | Authorize failure-summary spool create. | Protected failure summary is allowed or the job remains failed without false success. |
| B16 | `spoold` | Write and close failure summary. | Summary contains reason metadata only and no protected dataset content. |
| B17 | `jobd` | Complete failed job. | Job result is failed with `POLICY_DENIED` or mapped `DATASET_OPEN_DENIED`. |
| B18 | `operatord` | Display failed result. | Operator sees `FAILED REASON=POLICY_DENIED`; display is not audit evidence. |

## 9. Phase 0.9 Readiness Items

| ID | Item | Phase 0.8 position | Phase 0.9 action | Status |
| --- | --- | --- | --- | --- |
| FVS-READY-001 | Submitter versus `USER=` effective principal. | Job/spool Phase 0.8 requires submit-as delegation when `USER=` differs from submitter. | Confirm operator target refs and audit payloads include both submitter and requested principal. | Aligned by domain spec; test confirmation needed. |
| FVS-READY-002 | Dataset content staging for `USER.ALICE.INPUT`. | The slice requires typed, authorized fixture setup and no raw file shortcut. | Specify the operator command or fixture construction rule used by tests. | Open. |
| FVS-READY-003 | `ECHO` program identity. | `ECHO` is a semantic test program and cannot execute before authorization and handles. | Specify program identity source and unsupported-program behavior. | Open. |
| FVS-READY-004 | Queue/select/workload policy minimum semantics. | The sequence requires observable lifecycle states or a specified equivalent. | Decide whether hosted Phase 1 materializes queue/select or records an immediate-run equivalent. | Open. |
| FVS-READY-005 | Failure-summary spool policy. | BOB denied path expects a protected failure summary with no protected dataset content. | Define owner, security profile, output class, browse principal, and redaction. | Open. |
| FVS-READY-006 | Deny-before-return audit boundary. | Audit Phase 0.8 defines `AUDITD_DURABLE_APPEND` before returning denial. | Confirm the vertical-slice test profile and evidence refs use that boundary. | Aligned by domain spec; test confirmation needed. |
| FVS-READY-007 | Catalog/dataset fixture transaction boundary. | Committed catalog entry and protected content must exist before HELLO submit. | Define setup transaction, rollback, and audit behavior. | Open. |
| FVS-READY-008 | Duplicate `30-` spec prefix. | This requested contract path coexists with `30-attestation-measured-boot.md`. | Decide whether duplicate numeric prefixes are allowed or a later renumber/index pass is required. | Open. |
