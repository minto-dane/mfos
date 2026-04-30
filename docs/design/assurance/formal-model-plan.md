# MFOS Formal Model Plan v0.1

Status: Draft assurance plan

Owner area: `docs/design/assurance/formal-model-plan.md`

This plan defines how MFOS formal models are staged, reviewed, checked, and tied to evidence. It expands the `FORMAL-001` through `FORMAL-012` tasks from `docs/design/mfos-design.md` and uses `docs/design/specs/24-formal-methods.md` as the normative model inventory.

MFOS is z/OS-inspired and source-grounded. This plan does not claim compatibility with IBM products, z/Architecture, z/OS APIs, RACF, JES, DFSMS, SMF, JCL, or any other external platform.

## 1. Objectives

The formal model plan exists to:

- Prevent unauthorized success from becoming implementation behavior.
- Make audit obligations explicit and checkable.
- Make stale handle, rollback, freeze, invalid transition, and root mismatch failures visible early.
- Produce reviewable evidence artifacts for the assurance case.
- Keep formal methods staged so the project does not block on whole-system proof.

Formal models are design controls first and proof artifacts second. A model that finds a counterexample is useful if the counterexample leads to a corrected spec, implementation, or SPEC_GAP.

## 2. Ownership Boundaries

Formal models may reference all MFOS design specs, but this plan owns only assurance workflow. It does not edit component specs.

Model work MUST NOT:

- Claim external OS or product compatibility.
- Add implementation semantics not approved by the relevant spec.
- Treat a model assumption as a production guarantee.
- Hide unresolved semantics inside a success transition.
- Replace negative tests with model checking alone.

## 3. Model Roster

| Model ID | Name | Primary risk | Priority | Primary linked specs |
| --- | --- | --- | --- | --- |
| FORMAL-001 | Authorization decision | Unauthorized allow, missing obligations | P0 | 03, 06, 07 |
| FORMAL-002 | Dataset open invariant | Unauthorized handle, stale handle | P0 | 06, 08, 07 |
| FORMAL-003 | Audit append invariant | Audit bypass, hash-chain gaps | P0 | 07, 17 |
| FORMAL-004 | Catalog transaction | Phantom committed entry after crash | P1 | 08, 06, 07 |
| FORMAL-005 | Job lifecycle | Identity spoofing, execution before authorization | P1 | 09, 06, 08, 07 |
| FORMAL-006 | Spool access | Non-owner browse/export/purge | P1 | 09, 06, 07 |
| FORMAL-007 | Operator command | Command execution without authority | P1 | 10, 06, 07 |
| FORMAL-008 | AMF load | Invalid or revoked authorized module load | P0 | 12, 06, 07, 17 |
| FORMAL-009 | Update rollback/freeze | Rollback, freeze, mix-and-match accepted | P0 | 13, 07, 17 |
| FORMAL-010 | PXM lifecycle | Invalid partition transition, HA without Guard | P1 | 16, 07 |
| FORMAL-011 | Device teardown | DMA or interrupt leak after reassignment | P0 | 16, 07 |
| FORMAL-012 | Guard root transition | Root mismatch ignored, root rollback | P0 | 17, 07, 12, 13 |

P0 models gate production claims for their component. P1 models gate Enterprise readiness for their component. Profile-specific claims may require additional evidence beyond this plan.

## 4. Common Deliverables

Every formal model MUST produce:

```text
formal/<model-slug>/README.md
formal/<model-slug>/model.*
formal/<model-slug>/properties.md
formal/<model-slug>/counterexamples/
tests/model-traces/<model-slug>/*.json
docs/design/assurance/evidence/<model-slug>.md
```

Until the repository has a selected model checker, `model.*` is a placeholder pattern, not a specific extension.

Every evidence file MUST include:

- Model ID.
- Linked specs and requirement IDs.
- Source Matrix IDs.
- Tool and version, if any.
- Bounded configuration.
- Properties checked.
- Result summary.
- Counterexamples and disposition.
- Open SPEC_GAPs.
- Trace mapping status.

## 5. Review Gates

### Gate FM-G0: Candidate Accepted

Required:

- Model has purpose, state variables, actions, invariants, liveness, negative properties, evidence artifacts, and SPEC_GAPs.
- No success transition exists for SPEC_GAP or UNSUPPORTED.
- Security-sensitive operations include audit states.

### Gate FM-G1: Bounded Check Clean

Required:

- At least one small bounded configuration is checked.
- All invariants pass for the bounded configuration.
- Negative properties are either checked directly or represented by invariant failure attempts.
- Counterexamples are triaged.

### Gate FM-G2: Spec Trace Ready

Required:

- Each model action maps to a spec operation or an explicit SPEC_GAP.
- Each invariant maps to at least one requirement or stated design invariant.
- Evidence file exists under `docs/design/assurance/evidence/`.

### Gate FM-G3: Implementation Trace Ready

Required:

- Implementation emits trace events or test records for model actions.
- At least one positive trace and one negative trace are checked against the model.
- Trace mismatches are filed as bugs, spec corrections, or model corrections.

## 6. Model Details

### 6.1 FORMAL-001 Authorization Decision

State variables:

- Subjects, objects, operations, contexts, policy version.
- Policy rules and resource profiles.
- Decisions and obligations.
- Audit state by decision.
- Break-glass and dual-control state.
- Final result by request.

Actions:

- Submit authorization request.
- Evaluate policy.
- Attach obligations.
- Approve dual control.
- Enter and expire break-glass.
- Append decision audit.
- Return decision.
- Reject missing policy, stale policy, unsupported operation, and spec gap.

Invariants:

- No allow without exact policy match.
- Deny with audit obligation is not returned before audit append or fail-closed.
- Break-glass requires reason, expiry, subject, and audit.
- Dual control requires two distinct subjects.
- Missing policy cannot allow.

Liveness:

- Every well-formed request eventually reaches a final decision or fail-closed.
- Break-glass eventually expires unless renewed through an audited action.

Negative properties:

- Unauthorized allow never happens.
- Missing policy allow never happens.
- Stale policy allow never happens.
- Break-glass without expiry never happens.
- Unsupported operation success never happens.

Evidence artifacts:

- `formal/authorization/`
- `tests/model-traces/authorization/`
- `docs/design/assurance/evidence/authorization.md`

SPEC_GAPs:

- Final policy language.
- Authentication proof format.
- MFA and dual-control schema.
- Final model-checker runner.

### 6.2 FORMAL-002 Dataset Open

State variables:

- Datasets and catalog entries.
- Catalog generation.
- Subjects and open requests.
- Policy version and security decision.
- Audit state by open.
- Handles, handle state, handle expiry.
- Dataset lock and retention state.

Actions:

- Request open.
- Resolve catalog.
- Authorize open.
- Append open audit.
- Create, use, close, and revoke handle.
- Update policy version.
- Update catalog generation.
- Lock dataset.
- Return catalog not found, policy denied, or audit failure.

Invariants:

- Active handles exist only for committed catalog entries.
- Handles bind subject, operation, policy version, catalog generation, and expiry.
- Denied or unresolved opens never create handles.
- Policy or catalog generation changes can make handles stale.
- Locked datasets cannot produce new handles unless policy permits.

Liveness:

- Every well-formed open reaches active open or a final failure.
- Every active handle eventually closes, revokes, or expires in bounded runs.

Negative properties:

- Unauthorized dataset open never creates handle.
- Catalog not found never creates handle.
- Stale handle use never succeeds.
- Policy mismatch never succeeds.
- Audit failure never creates handle when audit is required.

Evidence artifacts:

- `formal/dataset-open/`
- `tests/model-traces/dataset-open/`
- `docs/design/assurance/evidence/dataset-open.md`

SPEC_GAPs:

- Final DSN grammar.
- Concurrent open compatibility.
- Retention interaction with open handles.
- Record/block access semantics.

### 6.3 FORMAL-003 Audit Append

State variables:

- Audit records and next sequence.
- Previous hash and record hash.
- Append requests.
- Schema validity.
- Durability and remote export state.
- Guard audit root.
- Profile and audit failure policy.

Actions:

- Submit audit record.
- Validate schema.
- Canonicalize record.
- Compute hash.
- Append local record.
- Advance hash chain.
- Export remote record.
- Append Guard root.
- Reject malformed record.
- Detect hash gap and tamper.
- Apply audit failure policy.

Invariants:

- Appended records are strictly monotonic.
- Every appended record links to the prior accepted hash.
- Malformed records never advance the chain.
- Required audit failure cannot be silently downgraded.
- High-Assurance accepted records link to Guard audit root or fail closed.

Liveness:

- Every valid append reaches appended, rejected, or failed-closed.
- Remote export queues drain or enter explicit failure state.

Negative properties:

- Hash-chain gap never undetected.
- Malformed record never appended.
- Deny return before required audit never happens.
- Non-monotonic Guard audit root never accepted.

Evidence artifacts:

- `formal/audit-append/`
- `tests/model-traces/audit-append/`
- `docs/design/assurance/evidence/audit-append.md`

SPEC_GAPs:

- Canonical encoding.
- Hash/signature algorithms.
- Remote export protocol.
- Genesis record format.

### 6.4 FORMAL-004 Catalog Transaction

State variables:

- Catalog entries.
- Journal entries.
- Transaction state.
- Prepared and committed entries.
- Catalog generation.
- Volume extents.
- Authorization decision.
- Audit state by transaction.
- Crash and recovery state.

Actions:

- Begin transaction.
- Validate DSN.
- Authorize update.
- Prepare entry.
- Write journal.
- Commit entry.
- Write commit marker.
- Append audit.
- Crash at modeled points.
- Recover journal.
- Roll back incomplete transactions.
- Verify committed entries.
- Repair orphan extents.

Invariants:

- Resolution returns only committed entries.
- Prepared entries are not visible as committed.
- Generation increases only on commit.
- Immutable/system entries need authority and audit for mutation.
- Crash before commit marker leaves no phantom committed entry.

Liveness:

- Non-crashing transactions commit or roll back.
- Recovery completes with committed entries verified and incomplete work rolled back.

Negative properties:

- Crash before commit never creates committed entry.
- Unauthorized update never commits.
- Immutable update without authority never commits.
- Orphan extent never visible as dataset.
- Malformed DSN never commits.

Evidence artifacts:

- `formal/catalog-transaction/`
- `tests/model-traces/catalog-transaction/`
- `docs/design/assurance/evidence/catalog-transaction.md`

SPEC_GAPs:

- Journal record encoding.
- Extent repair semantics.
- Multi-catalog transactions.
- Concurrent transaction isolation.

### 6.5 FORMAL-005 Job Lifecycle

State variables:

- Jobs and job state.
- Submitter and effective principal.
- JCL parse and conversion state.
- Security decisions.
- Queue and initiators.
- Step state.
- Dataset open state.
- Spool entries.
- Return code.
- Audit state by job.

Actions:

- Submit job.
- Parse JCL-like input.
- Establish effective principal.
- Authorize submit.
- Convert and validate.
- Enqueue, select, and start step.
- Resolve DD.
- Open dataset for step.
- Capture SYSOUT.
- Complete, fail, cancel, hold, or purge job.
- Append job audit.

Invariants:

- Effective principal is established before dataset, program, or spool open.
- Execution requires submit, conversion, validation, and authorization.
- DD resolution cannot bypass catalogd, datasetd, or securityd.
- SYSOUT entries bind job, owner, output class, and security profile.
- Canceled or failed jobs cannot become complete RC=0.

Liveness:

- Valid queued jobs eventually select, hold, cancel, or fail under fair scheduling.
- Executing steps eventually complete, fail, abend, or cancel under bounded execution.

Negative properties:

- Job submit identity spoofing never succeeds.
- Dataset open before effective principal never happens.
- Unauthorized DD resolution never executes.
- Failed step never becomes complete RC=0 without policy.
- Canceled job never executes a new step.

Evidence artifacts:

- `formal/job-lifecycle/`
- `tests/model-traces/job-lifecycle/`
- `docs/design/assurance/evidence/job-lifecycle.md`

SPEC_GAPs:

- Final JCL-like subset.
- ABEND reason taxonomy.
- Initiator fairness.
- Restart and checkpoint semantics.

### 6.6 FORMAL-006 Spool Access

State variables:

- Spool entries and states.
- Owners, job IDs, output class, security profile.
- Retention policy.
- Browse, export, and purge requests.
- Security decision.
- Audit state by spool operation.
- Quota state.

Actions:

- Create spool entry.
- Append SYSOUT.
- Close spool entry.
- Authorize browse/export/purge.
- Browse, export, or purge.
- Apply retention.
- Complete purge.
- Append spool audit.
- Reject quota exceeded.

Invariants:

- Browse, export, and purge require securityd decisions.
- Non-owner access requires explicit policy.
- Retention-protected entries cannot purge early.
- Spool output is not audit evidence.
- Purged entries cannot be browsed or exported.

Liveness:

- Closed spool entries eventually become browseable, held, or purge-pending.
- Purge-pending entries eventually purge when retention permits and no fault remains.

Negative properties:

- Non-owner browse without policy never succeeds.
- Purge under retention never succeeds.
- Purged browse never succeeds.
- Export without audit never succeeds.
- Spool-as-audit never succeeds.

Evidence artifacts:

- `formal/spool-access/`
- `tests/model-traces/spool-access/`
- `docs/design/assurance/evidence/spool-access.md`

SPEC_GAPs:

- Output class policy grammar.
- Quota details.
- Redaction rules.
- Physical spool layout.

### 6.7 FORMAL-007 Operator Command

State variables:

- Commands and parsed command.
- Command ID.
- Operator subject.
- Authority class and target object.
- Confirmation and dual-control state.
- Security decision.
- Execution state.
- Audit state by command.
- Emergency mode and automation hook state.

Actions:

- Enter command.
- Parse and identify command.
- Resolve target.
- Authorize command.
- Request and confirm confirmation.
- Request and approve dual control.
- Execute command.
- Append command audit.
- Display result.
- Enter emergency mode.
- Reject malformed or unauthorized command.

Invariants:

- No command executes without ID, subject, authority class, authorization, and audit obligation.
- Destructive commands requiring confirmation do not execute before confirmation.
- Dual-control commands require two distinct subjects.
- Automation hooks cannot bypass authority or audit.
- Root shell text is not an operator command success path.

Liveness:

- Well-formed commands eventually execute, deny, cancel, return unsupported/spec-gap, or fail closed.
- Pending confirmations expire, confirm, or cancel.

Negative properties:

- Unauthorized command never executes.
- Destructive command without confirmation never executes.
- Same-actor dual control never executes.
- Automation bypass never executes.
- Malformed command never executes.

Evidence artifacts:

- `formal/operator-command/`
- `tests/model-traces/operator-command/`
- `docs/design/assurance/evidence/operator-command.md`

SPEC_GAPs:

- Final operator grammar.
- Destructive command classification.
- Confirmation timeout.
- Automation hook API.

### 6.8 FORMAL-008 AMF Load

State variables:

- AMF modules.
- Artifact source and digest.
- Signer, manifest, signature, and revocation state.
- Catalog immutability.
- Authority class.
- Security decision.
- Guard approval.
- Mapping and registry state.
- Audit state by load.
- Profile.

Actions:

- Request AMF load.
- Resolve artifact.
- Verify signature and manifest.
- Check revocation.
- Check catalog immutability.
- Authorize AMF load.
- Request Guard approval.
- Map RX.
- Register AMF.
- Append audit.
- Reject invalid signature, revocation, mutable source, or Guard denial.

Invariants:

- Registered modules have valid signature, manifest, digest, authority class, source immutability, authorization, and audit.
- Revoked signer, digest, or epoch cannot load.
- Mutable dataset or unapproved source cannot register.
- High-Assurance load requires Guard approval.
- AMF modules cannot gain audit-disable authority.

Liveness:

- Every load request reaches ready or final fail-closed state.
- Revocation updates eventually prevent new revoked-module loads.

Negative properties:

- Invalid signature never loads.
- Revoked signer never loads.
- Mutable dataset AMF load never succeeds.
- Missing authority class never loads.
- High-Assurance Guard-denied AMF never registers.

Evidence artifacts:

- `formal/amf-load/`
- `tests/model-traces/amf-load/`
- `docs/design/assurance/evidence/amf-load.md`

SPEC_GAPs:

- Final AMF manifest schema.
- Signature trust root.
- Revocation freshness.
- ABI safety contract.

### 6.9 FORMAL-009 Update Rollback and Freeze

State variables:

- Root, timestamp, snapshot, and targets metadata versions.
- Timestamp expiry.
- Target artifacts, hashes, and sizes.
- Security epoch.
- Installed and staged generation.
- Metadata set consistency.
- Verification and approval state.
- Guard update root.
- Audit state by update.
- Current time.
- Recovery policy.

Actions:

- Receive metadata.
- Verify root, timestamp, snapshot, targets, and artifacts.
- Check epoch and dependencies.
- Detect rollback.
- Detect freeze.
- Detect mix-and-match.
- Stage, approve, activate, measure, and commit update.
- Perform recovery rollback.
- Append update audit.
- Reject update.

Invariants:

- Committed generation cannot decrease except approved recovery rollback.
- Security epoch cannot decrease except approved recovery rollback.
- Expired timestamp cannot authorize staging or activation.
- Snapshot and targets must form a consistent view.
- Artifact hash/size mismatch cannot stage or activate.
- High-Assurance update root transitions require Guard linkage.

Liveness:

- Every bundle reaches staged, rejected, failed-closed, or needs-approval.
- Approved staged updates commit or roll back under fair activation assumptions.

Negative properties:

- Rollback metadata never accepted.
- Freeze metadata never accepted.
- Mix-and-match metadata never accepted.
- Artifact hash mismatch never stages.
- Unsigned artifact never activates.
- Security epoch downgrade never commits.

Evidence artifacts:

- `formal/update-rollback-freeze/`
- `tests/model-traces/update-rollback-freeze/`
- `docs/design/assurance/evidence/update-rollback-freeze.md`

SPEC_GAPs:

- Final metadata schema.
- Time source and clock-failure model.
- Recovery rollback policy.
- Dependency solver semantics.

### 6.10 FORMAL-010 PXM Lifecycle

State variables:

- Partitions and partition states.
- Activation profile and profile hash.
- Image measurement.
- CPU, memory, device, IOMMU, and interrupt assignments.
- Audit state by PXM operation.
- Backend mode.
- Guard-required and Guard-approval state.

Actions:

- Define, measure, load, activate, start, dispatch, deschedule, quiesce, resume, fault, recover, deactivate, and destroy partition.
- Reject invalid transition.
- Append PXM audit.

Invariants:

- RUNNABLE requires legal define, measure, load, and activate path.
- Illegal transitions never change to success states.
- Implicit backend cannot claim High-Assurance PXM conformance.
- PXM does not interpret MFOS enterprise semantics.
- High-Assurance Guard-required transitions do not succeed without Guard.

Liveness:

- Valid lifecycle commands reach legal next state or fail closed.
- Faulted partitions remain faulted, recover, or destroy through approved actions.

Negative properties:

- Start from defined never succeeds.
- Activate without measure never succeeds.
- Invalid transition never succeeds.
- PXM dataset policy decision never happens.
- High-Assurance without Guard never claims ready.

Evidence artifacts:

- `formal/pxm-lifecycle/`
- `tests/model-traces/pxm-lifecycle/`
- `docs/design/assurance/evidence/pxm-lifecycle.md`

SPEC_GAPs:

- VMX/SVM backend semantics.
- Activation profile schema.
- Partition dispatch fairness.
- Boot audit sink.

### 6.11 FORMAL-011 Device Teardown

State variables:

- Devices and assignment states.
- Owner partition.
- IOMMU mappings.
- Interrupt routes.
- DMA state.
- Command queues.
- Device reset state.
- Memory domains.
- Teardown checklist.
- Audit state by device operation.
- Fault state.

Actions:

- Request assignment.
- Prepare device.
- Create IOMMU domain.
- Create interrupt routes.
- Activate assignment.
- Request release.
- Stop command queues.
- Quiesce access.
- Mask interrupts.
- Stop DMA.
- Revoke IOMMU mappings.
- Flush translations.
- Reset device.
- Revoke interrupt routes.
- Clear ownership.
- Mark released.
- Fault teardown.
- Append audit.

Invariants:

- Exclusive device has at most one active owner.
- Reassignment waits for DMA stop, IOMMU revoke, interrupt revoke, and ownership clear.
- Teardown failure keeps device unavailable.
- Partition memory reuse waits for CPU, IOMMU, interrupt, device ownership, and zeroing requirements.
- IOMMU/interrupt-required assignment cannot become active without them.

Liveness:

- Release reaches released or faulted under fair device response.
- Faulted teardown remains isolated, retries, or moves to recovery workflow.

Negative properties:

- Reassign before teardown never happens.
- Active DMA after release never happens.
- Interrupt route after release never happens.
- IOMMU mapping after release never happens.
- Teardown fault then reassign never succeeds.

Evidence artifacts:

- `formal/device-teardown/`
- `tests/model-traces/device-teardown/`
- `docs/design/assurance/evidence/device-teardown.md`

SPEC_GAPs:

- Device reset semantics.
- PCIe/IOMMU invalidation ordering.
- Interrupt remapping hardware model.
- DMA in-flight completion model.

### 6.12 FORMAL-012 Guard Root Transition

State variables:

- Guard lifecycle state.
- Guard roots, type, version, digest.
- Security epoch and policy version.
- Measurement context.
- Transition requests and approvals.
- Audit root sequence.
- Executable mapping requests.
- AMF registry root.
- SVC table root.
- Emergency state.
- Attestation claims.
- Audit state by Guard operation.

Actions:

- Measure and initialize Guard.
- Seal and verify root.
- Request, approve, deny, and revoke root transition.
- Detect root mismatch.
- Enter lockdown.
- Recovery reseal.
- Authorize executable mapping.
- Authorize AMF load.
- Verify SVC table.
- Append audit root.
- Enter and exit emergency mode.
- Attest.

Invariants:

- Guard scope is limited to approved root types.
- Root transition cannot reduce version or security epoch without approved recovery policy.
- SVC table mismatch cannot be ignored.
- Audit root sequence is monotonic.
- High-Assurance executable mapping requires Guard authorization.
- Guard cannot interpret ordinary business semantics.
- Emergency mode cannot disable audit root append obligations.

Liveness:

- Root transition requests reach approved, denied, revoked, or lockdown.
- Lockdown remains locked down or enters approved recovery workflow.

Negative properties:

- Guard root mismatch ignored never happens.
- Root rollback without recovery never succeeds.
- Non-monotonic audit root never succeeds.
- Executable mapping without Guard never succeeds in High-Assurance.
- Guard dataset policy decision never happens.
- Emergency mode without expiry never succeeds.

Evidence artifacts:

- `formal/guard-root-transition/`
- `tests/model-traces/guard-root-transition/`
- `docs/design/assurance/evidence/guard-root-transition.md`

SPEC_GAPs:

- Guard isolation mechanism.
- Attestation evidence format.
- Root digest canonicalization.
- Emergency recovery policy.
- Executable mapping implementation boundary.

## 7. Initial Work Order

The recommended order is:

1. FORMAL-001 Authorization decision.
2. FORMAL-003 Audit append.
3. FORMAL-002 Dataset open.
4. FORMAL-009 Update rollback and freeze.
5. FORMAL-012 Guard root transition.
6. FORMAL-008 AMF load.
7. FORMAL-011 Device teardown.
8. FORMAL-004 Catalog transaction.
9. FORMAL-005 Job lifecycle.
10. FORMAL-006 Spool access.
11. FORMAL-007 Operator command.
12. FORMAL-010 PXM lifecycle.

Reasoning:

- Authorization, audit, and dataset handles form the first Dafny executable-semantics safety core.
- Update, Guard, AMF, and teardown carry critical high-assurance and supply-chain risk.
- Catalog, job, spool, operator, and PXM lifecycle models then broaden coverage over core workflows.

## 8. Traceability Matrix

| Model ID | Abuse cases covered |
| --- | --- |
| FORMAL-001 | unauthorized allow, missing policy, stale policy, break-glass misuse, unsupported success |
| FORMAL-002 | unauthorized dataset open success, stale handle reuse after policy change |
| FORMAL-003 | audit write failure ignored, deny returned before audit |
| FORMAL-004 | catalog crash leaves phantom committed entry |
| FORMAL-005 | job submit identity spoofing, dataset open before effective principal |
| FORMAL-006 | spool browse by non-owner, purge under retention |
| FORMAL-007 | operator command executed without authority |
| FORMAL-008 | AMF load from mutable dataset, revoked signer accepted |
| FORMAL-009 | revoked update accepted, rollback metadata accepted, freeze accepted, mix-and-match accepted |
| FORMAL-010 | invalid partition transition accepted, PXM interprets MFOS enterprise semantics |
| FORMAL-011 | PXM device reassigned before teardown, DMA/interrupt leak |
| FORMAL-012 | Guard root mismatch ignored, root rollback, executable mapping without Guard |

## 9. Evidence Lifecycle

Evidence states:

```text
PLANNED
MODEL_DRAFTED
BOUNDED_CHECKED
COUNTEREXAMPLE_OPEN
COUNTEREXAMPLE_RESOLVED
SPEC_TRACE_READY
IMPLEMENTATION_TRACE_READY
ACCEPTED
STALE
```

Rules:

- A model with unresolved counterexamples cannot be ACCEPTED.
- A model becomes STALE when linked specs change relevant states, actions, or invariants.
- A production claim cannot rely on STALE evidence.
- SPEC_GAPs must remain visible in the evidence file.

## 10. Counterexample Handling

Each counterexample MUST be classified as:

```text
MODEL_BUG
SPEC_BUG
IMPLEMENTATION_BUG
EXPECTED_UNSUPPORTED
EXPECTED_SPEC_GAP
ASSUMPTION_TOO_WEAK
ASSUMPTION_TOO_STRONG
TOOL_LIMITATION
```

Disposition MUST include:

- Counterexample ID.
- Model ID.
- Property violated.
- Minimal trace.
- Classification.
- Required correction.
- Owner.
- Status.

## 11. Model-to-Test Guidance

For every negative property, create or link a negative test when implementation exists.

Examples:

- `DATAOPEN-NEG-001` maps to an integration test where BOB cannot open ALICE dataset and no handle is created.
- `AUDIT-NEG-004` maps to a test where DENY is not returned before required deny audit is accepted.
- `UPDATE-NEG-001` maps to rollback metadata rejection.
- `DEVTD-NEG-001` maps to device reassignment before teardown rejection.
- `GUARDROOT-NEG-001` maps to Guard root mismatch lockdown.

The formal model does not replace the test. It defines what the test is trying to preserve.

## 12. Tooling Plan

Initial tooling remains a SPEC_GAP. The plan assumes these phases:

```text
TOOL-0:
  Markdown model skeletons and review-only invariants.

TOOL-1:
  TLA+ or equivalent state-machine model runner for P0 models.

TOOL-2:
  Alloy or equivalent relational checker for handles, ownership, and root sets.

TOOL-3:
  Trace checker consuming implementation test traces.

TOOL-4:
  Proof-assistant exploration for the smallest stable core after implementation
  interfaces settle.
```

Tooling selection MUST be documented in an ADR before models are used for production evidence.

## 13. Open SPEC_GAPs

Global formal-methods SPEC_GAPs:

- Final formal language and model runner.
- Repository layout under `formal/`.
- Trace event schema.
- Counterexample file format.
- Evidence signing or immutability mechanism.
- CI gate for model checking.
- Coverage threshold for model-to-test mapping.
- Refinement relation from model actions to Rust/service implementation events.
- Assumption language for hardware, firmware, cryptography, scheduler fairness, and crash timing.
- Criteria for promoting a model from design evidence to production assurance evidence.

These gaps MUST NOT be treated as completed assurance work.

## 14. AI Formal Model Work Prompt

```text
You are an MFOS formal model worker.

Use docs/design/specs/24-formal-methods.md and
docs/design/assurance/formal-model-plan.md.

Work on exactly one model ID at a time.

Hard constraints:
- Do not claim z/OS compatibility.
- Do not turn SPEC_GAP or UNSUPPORTED into success.
- Keep unauthorized success impossible.
- Include audit obligations for security-sensitive actions.
- Preserve the state variables, actions, invariants, liveness, negative
  properties, evidence artifacts, and SPEC_GAPs listed for the model.
- Add counterexamples instead of hiding them.
- Do not broaden PXM or Guard responsibilities.

Required output:
1. Model ID
2. Files changed
3. Requirements and source IDs covered
4. Properties checked
5. Counterexamples found
6. Counterexamples resolved
7. Evidence artifacts updated
8. SPEC_GAPs remaining
9. Negative tests implied
10. Trace mapping status
```
