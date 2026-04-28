# MFOS Evidence Archive Specification v0.1

Status: Draft

Audience: evidence auditors, release reviewers, CI authors, implementation agents, assurance authors

This document defines the MFOS evidence archive layout and metadata model. MFOS is source-grounded and z/OS-inspired, but this archive must not be used to claim z/OS compatibility, z/Architecture compatibility, IBM API compatibility, RACF compatibility, JES compatibility, DFSMS compatibility, SMP/E compatibility, or IBM product compatibility.

## 1. Purpose

The evidence archive is the durable store for artifacts that support MFOS assurance, conformance, production readiness, and High-Assurance claims.

It exists so claims are not backed by informal notes. Each archived artifact must identify what it proves, which requirements and source IDs it supports, how it was produced, who reviewed it, how it is retained, and whether it is valid for Baseline, Enterprise, or High-Assurance claims.

## 2. Scope

In scope:

- Archive directory layout.
- Evidence artifact classes.
- Artifact IDs and naming rules.
- Artifact metadata schema.
- Hash, signature, and provenance fields.
- Requirement, source, test, and claim relationships.
- Reviewer approval records.
- Release gate evidence mapping.
- Profile claim evidence mapping.
- Retention and immutability policy.
- Unresolved gap tracking.
- AI prompt for evidence archivists.

Out of scope:

- External certification package format.
- Long-term legal records management.
- Replacing auditd runtime audit streams.
- Replacing signed provenance or SBOM formats.
- Replacing the assurance claim registry.

## 3. Archive Root

Recommended repository path:

```text
docs/design/assurance/archive/
```

Recommended generated-release path:

```text
artifacts/assurance/<release_id>/
```

The repository path may hold design-time evidence indexes and small text artifacts. Release-generated evidence should be archived under `artifacts/assurance/<release_id>/` or an equivalent immutable artifact store.

## 4. Directory Layout

```text
artifacts/assurance/<release_id>/
  manifest.yaml
  claims/
    <claim_id>.yaml
  gates/
    PROD-001.yaml
    PROD-002.yaml
    ...
    PROD-015.yaml
  design/
    source-matrix/
    requirements/
    specs/
    threat-models/
    invariants/
  tests/
    unit/
    integration/
    negative/
    fuzz/
    conformance/
    crash-recovery/
    fault-injection/
  reviews/
    architecture/
    security/
    code/
    unsafe/
    tcb/
    release-wording/
    source-grounding/
  runtime/
    audit/
    operator/
    amf/
    update/
    recovery/
  supply-chain/
    sbom/
    provenance/
    dependency-allowlist/
    reproducible-build/
    signatures/
  high-assurance/
    pxm/
    guard/
    attestation/
    formal/
  gaps/
    unresolved-gaps.yaml
  approvals/
    reviewer-approvals.yaml
```

## 5. Artifact Classes

| Class | Prefix | Purpose |
| --- | --- | --- |
| Design evidence | EVD-DES | Source matrix, requirements, specs, state machines, invariants. |
| Test evidence | EVD-TST | Unit, integration, conformance, positive test reports. |
| Negative test evidence | EVD-NEG | Denial, fail-closed, abuse-case, policy rejection reports. |
| Fuzz evidence | EVD-FUZ | Fuzz target registration, corpus summaries, crash reports. |
| Review evidence | EVD-REV | Architecture, security, code, unsafe, TCB, release wording reviews. |
| Runtime evidence | EVD-RUN | auditd records, DENY-before-result proofs, recovery drill records. |
| Supply-chain evidence | EVD-SUP | SBOM, signed provenance, dependency allowlist, build reproducibility. |
| Formal evidence | EVD-FRM | TLA+/Alloy/Coq/Isabelle models and proof or model-check reports. |
| Guard evidence | EVD-GRD | Guard seal, verify, executable mapping, SVC table, AMF registry evidence. |
| PXM evidence | EVD-PXM | Partition lifecycle, IOMMU, interrupt remap, device teardown evidence. |
| Release gate evidence | EVD-GAT | Evidence bundle for PROD gates. |
| Gap evidence | EVD-GAP | Open gaps, waiver records, blocked claims, accepted risks. |

## 6. Artifact Naming

Artifact ID format:

```text
EVD-<CLASS>-<AREA>-<YYYYMMDD>-<NNNN>
```

Examples:

```text
EVD-NEG-DATA-20260427-0001
EVD-FUZ-OPER-20260427-0001
EVD-SUP-RELEASE-20260427-0001
EVD-GRD-AMF-20260427-0001
```

File naming format:

```text
<artifact_id>--<short-name>.<ext>
```

Rules:

- Artifact IDs must be stable after publication.
- Short names must use lowercase ASCII, digits, and hyphen.
- Artifact files must not be overwritten after a release archive is sealed.
- Superseded evidence gets a new artifact ID and references the superseded ID.

## 7. Archive Manifest Schema

```yaml
EvidenceArchiveManifest:
  manifest_version: 1
  archive_id: string
  release_id: string
  created_at_utc: timestamp
  created_by: string
  claimed_profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance | none
  non_compatibility_statement: string
  source_design_refs:
    - path: docs/design/mfos-design.md
    - path: docs/design/specs/19-assurance-case.md
    - path: docs/design/specs/20-conformance.md
  artifact_index:
    - artifact_id: string
      metadata_path: string
      artifact_path: string
  claim_registry_ref: string
  production_gate_index_ref: string
  unresolved_gap_index_ref: string
  archive_hash:
    algorithm: sha384
    value: hex
  archive_signature:
    signing_key_id: string
    signature: string
    signed_at_utc: timestamp
  provenance:
    builder_id: string
    build_invocation_id: string
    source_revision: string?
    toolchain_id: string?
    workflow_ref: string?
```

The `non_compatibility_statement` must state that MFOS does not claim z/OS or IBM product compatibility.

## 8. Evidence Artifact Metadata Schema

```yaml
EvidenceArtifact:
  artifact_id: string
  artifact_class: design | test | negative_test | fuzz | review | runtime | supply_chain | formal | guard | pxm | release_gate | gap
  title: string
  description: string
  release_id: string?
  produced_at_utc: timestamp
  produced_by:
    actor_type: human | ai_agent | ci | tool
    actor_id: string
  profile_applicability:
    - Baseline
    - Enterprise
    - High-Assurance
  claim_ids:
    - string
  requirement_ids:
    - string
  source_matrix_ids:
    - string
  design_refs:
    - path: string
      section: string?
  implementation_refs:
    - path: string
      symbol: string?
  test_refs:
    - test_id: string
      test_kind: positive | negative | fuzz | fault_injection | crash_recovery | conformance
      result: pass | fail | flaky | not_run
  audit_obligations:
    - string
  production_gates:
    - PROD-001
  related_artifacts:
    - relation: supersedes | superseded_by | depends_on | derived_from | contradicts | supports
      artifact_id: string
  artifact_file:
    path: string
    media_type: text/markdown | application/yaml | application/json | text/plain | application/octet-stream | other
    size_bytes: uint64
  hashes:
    - algorithm: sha384
      value: hex
    - algorithm: sha256
      value: hex
  signature:
    required: bool
    signing_key_id: string?
    signature: string?
    signed_at_utc: timestamp?
  provenance:
    provenance_id: string?
    builder_id: string?
    source_revision: string?
    toolchain_id: string?
    command_or_workflow: string?
    environment_digest: sha384?
  retention:
    class: draft | development | release | production | high_assurance | security_incident
    retain_until: date | indefinite
    deletion_allowed: bool
  review:
    required: bool
    approvals:
      - approval_id: string
    status: not_required | pending | approved | rejected | superseded
  unresolved_gaps:
    - gap_id: string
  status: draft | active | rejected | superseded | expired | quarantined
```

## 9. Required Relationships

Every evidence artifact must link to at least one of:

- `claim_ids`.
- `requirement_ids`.
- `production_gates`.
- `unresolved_gaps`.

Security-sensitive evidence must link to:

- requirement IDs.
- source matrix IDs.
- negative tests or a documented reason why the evidence is not test evidence.
- audit obligations when applicable.
- reviewer approvals when used for a claim above CLAIM-L2.

High-Assurance evidence must link to:

- High-Assurance profile applicability.
- Guard or PXM requirement IDs.
- relevant root object or partition boundary.
- formal evidence, attestation evidence, or explicit gap.

## 10. Hash, Signature, and Provenance Rules

Hashing:

- Every artifact must include SHA-384.
- SHA-256 may be included for ecosystem tooling.
- Archive manifests must include an archive-level SHA-384 hash.

Signatures:

- Release, production, supply-chain, Guard, PXM, formal, and High-Assurance artifacts require signatures.
- Draft design evidence may be unsigned but must be marked `status: draft`.
- Signature metadata must include key ID, signature value, and signing time.

Provenance:

- Enterprise-Standalone, Enterprise-PXM, and High-Assurance release evidence must include provenance.
- Provenance must name builder, workflow or command, source revision when available, and toolchain ID when available.
- Generated evidence from AI agents must record the AI agent identity or task identifier in `produced_by`.

## 11. Retention Policy

| Retention class | Minimum retention | Deletion |
| --- | --- | --- |
| draft | Until superseded or claim retired. | Allowed with review note. |
| development | 1 year after supersession. | Allowed after owner approval. |
| release | 7 years after release or product retirement, whichever is later. | Not allowed without release owner approval. |
| production | 10 years after last production claim using it. | Not allowed without security owner approval. |
| high_assurance | Indefinite unless formally retired. | Not allowed by default. |
| security_incident | Indefinite unless legal/security owner approves. | Not allowed by default. |

Artifacts referenced by active production gates or active High-Assurance claims must not be deleted.

## 12. Reviewer Approval Schema

```yaml
ReviewerApproval:
  approval_id: string
  artifact_ids:
    - string
  claim_ids:
    - string
  reviewer:
    reviewer_id: string
    role: architecture | security | code | unsafe | tcb | source_grounding | release | high_assurance | audit | supply_chain
    independence: author | peer | independent | external
  decision: approved | rejected | changes_requested | superseded
  approved_at_utc: timestamp?
  rationale: string
  required_followups:
    - string
  signature:
    signing_key_id: string?
    signature: string?
```

Review requirements:

- CLAIM-L3 and above require at least one reviewer approval.
- TCB changes require independent review before raising claim level.
- High-Assurance claims require high-assurance reviewer approval.
- Release claims require release reviewer approval and release wording review.

## 13. Release Gate Evidence Mapping

Each production gate must have a gate record:

```yaml
ProductionGateEvidence:
  gate_id: PROD-001
  release_id: string
  status: pass | fail | not_applicable | blocked
  profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  required_artifacts:
    - artifact_id: string
  observed_artifacts:
    - artifact_id: string
  blocking_gaps:
    - gap_id: string
  reviewer_approvals:
    - approval_id: string
  decision_rationale: string
```

Gate records must not mark `pass` unless all required evidence artifacts are present, hash-verified, and review requirements are satisfied.

## 14. Profile Claim Evidence

Baseline evidence must cover:

- source matrix lint.
- requirement ID traceability.
- securityd mediation.
- auditd obligations.
- negative tests.
- no-fake-success scan.

Enterprise evidence must also cover:

- Secure Boot and measured boot evidence when claimed.
- TPM evidence when secrets or measurements are bound to TPM.
- TUF-like update evidence.
- SBOM.
- signed provenance.
- remote audit export.
- dependency allowlist.

High-Assurance evidence must also cover:

- PXM partition lifecycle evidence.
- Guard root seal and verify evidence.
- Guard audit root evidence.
- Guard security root evidence.
- Guard AMF registry evidence.
- Guard executable mapping evidence.
- remote attestation.
- formal model or proof evidence for claimed roots.

Optional higher-profile evidence does not upgrade the claimed profile unless the conformance statement and claim registry say so.

## 15. Unresolved Gap Index

```yaml
UnresolvedGap:
  gap_id: string
  title: string
  description: string
  severity: critical | high | medium | low
  status: open | accepted_risk | blocked | resolved | superseded
  opened_at_utc: timestamp
  owner: string
  source_refs:
    - string
  requirement_ids:
    - string
  claim_ids:
    - string
  blocked_profiles:
    - Baseline
    - Enterprise
    - High-Assurance
  blocked_gates:
    - PROD-001
  required_resolution: string
  evidence_needed:
    - string
  accepted_by: string?
  accepted_until: date?
```

Critical or High unresolved gaps block production claims unless explicitly accepted by the required release and security owners. High-Assurance claims must not accept open Guard-root gaps as non-blocking.

## 16. Archive Validation Checklist

- Archive manifest exists.
- Archive manifest has non-compatibility statement.
- All artifact IDs are unique.
- All artifact files exist.
- All artifact hashes verify.
- Required signatures verify.
- Required provenance exists.
- Every production gate has a gate evidence record.
- Every active claim has evidence links.
- Every evidence artifact links to requirements, claims, gates, or gaps.
- Reviewer approvals exist where required.
- Retention class is set.
- Unresolved gaps are indexed.
- Release wording review evidence exists for release archives.

## 17. AI Prompt

```text
You are the MFOS evidence archivist.
Create or review evidence archive metadata for the supplied MFOS artifacts.

Do not claim z/OS compatibility, z/Architecture compatibility, IBM API
compatibility, RACF compatibility, JES compatibility, DFSMS compatibility,
SMP/E compatibility, or IBM product compatibility.

For each artifact, output:
- artifact_id
- artifact_class
- title
- profile_applicability
- claim_ids
- requirement_ids
- source_matrix_ids
- design_refs
- implementation_refs
- test_refs
- audit_obligations
- production_gates
- hashes
- signature requirement
- provenance fields
- retention class and retain_until
- reviewer approvals required
- unresolved gaps
- status

Validation rules:
- Security-sensitive artifacts require requirement IDs, source matrix IDs,
  negative-test linkage, and audit-obligation linkage when applicable.
- Enterprise-Standalone, Enterprise-PXM, and High-Assurance release artifacts require provenance.
- High-Assurance artifacts require Guard/PXM/formal/attestation evidence
  as applicable.
- Missing required evidence must be reported as a gap, not accepted silently.
```

## 18. Spec Gaps

- Exact archive signing key hierarchy is not fixed.
- Machine-readable schema format is YAML in this draft but not yet enforced by CI.
- Artifact store backend is not specified.
- Evidence encryption and access-control model are not specified here.
- Cross-release deduplication rules are not defined.
- Legal hold workflow is not defined.
- External auditor export format is not defined.

