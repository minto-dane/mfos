---
spec_id: "MFOS-SPEC-28-MACHINE-READABLE-REGISTRIES"
title: "MFOS Machine-Readable Registries Specification v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001", "EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001", "MS-VBS-001", "MS-VSM-001", "NIST-160-001", "NIST-193-001", "NIST-218-001", "SEL4-001", "SLSA-001", "TCG-001", "TUF-001", "X64-AMD-001", "X64-INTEL-001"]
requirement_refs: ["MFOS-REQ-AMF-*", "MFOS-REQ-DATASET-*", "MFOS-REQ-PROD-*", "MFOS-REQ-SYSINT-*"]
claim_refs: ["MFOS-CLAIM-PROD-*"]
test_refs: ["TEST-AMF-FUZZ-*", "TEST-AMF-NEG-*", "TEST-AMF-POS-*", "TEST-DATA-NEG-*", "TEST-SI-FUZZ-*", "TEST-SI-NEG-*", "TEST-SI-POS-*"]
evidence_refs: ["EVID-AUD-*", "EVID-DATA-*"]
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Machine-Readable Registries Specification v0.1

Status: Draft design split  
Owner area: `docs/design/specs/28-machine-readable-registries.md`  
Audience: architecture agents, implementation agents, CI authors, test engineers, evidence auditors, release reviewers

MFOS is source-grounded and z/OS-inspired. This specification does not claim z/OS compatibility, z/Architecture compatibility, IBM API compatibility, RACF compatibility, JES compatibility, DFSMS compatibility, SMF compatibility, external workload management compatibility, APF compatibility, PR/SM compatibility, Windows VBS compatibility, Linux compatibility, or UNIX compatibility.

## 1. Purpose

This specification defines the initial machine-readable registry schemas for MFOS:

- requirements
- tests
- evidence artifacts
- glossary terms
- AI implementation output
- task IDs
- conformance claims
- pack contracts
- spec front matter

The purpose is to make MFOS traceability enforceable by CI instead of relying on prose alone.

Every security-sensitive implementation should eventually be traceable through this chain:

```text
source-matrix.yml
  -> requirement registry
  -> task registry
  -> implementation refs
  -> test registry
  -> evidence registry
  -> conformance claim registry
  -> production readiness gate
```

## 1.1 Pre-Implementation Gate

A component implementation MUST NOT begin until its pack contract and related
registries contain:

- Requirement IDs
- Source Matrix IDs
- Object model references
- State machine references
- Failure modes
- Audit obligations
- Positive tests
- Negative tests
- `MFOS_ERR_UNSUPPORTED` and `MFOS_ERR_SPEC_GAP` behavior
- Fuzz target decision
- Evidence artifact path
- Claim boundary
- Pack contract
- Red-team review

If any item is missing, the assigned implementation agent MUST produce a
`SPEC_GAP_REPORT` instead of code.

The historical Hosted Semantic Prototype profile is superseded for current
Phase 1 work. Current Phase 1 is limited to non-production Dafny executable
semantics and conformance-harness validation. A later reviewed gate may define a
new hosted prototype profile only after this spec, the AI contract, pack
contracts, and roadmap are updated. Until that later gate exists, this
historical label is inactive:

```yaml
implementation_profile: hosted_semantic_prototype
production_claim: false
hardware_enforcement_claim: false
system_integrity_claim: semantic_only
```

## 2. Scope

In scope:

- YAML registry document envelopes.
- Required fields for each registry record type.
- Stable ID formats.
- Relationships to `docs/design/source-matrix/source-matrix.yml`.
- Cross-registry references.
- Validation rules.
- CI usage.
- Examples.
- SPEC_GAP tracking for registry automation.

Out of scope:

- Implementing the registry generator.
- Implementing CI checks.
- Creating the actual registry YAML files.
- Replacing the existing split specifications as normative prose.
- External certification mapping.
- Runtime audit log binary format.
- Cryptographic signature algorithm selection.

## 3. Source Matrix References

Required source IDs for this registry specification:

| Source ID | Use |
| --- | --- |
| EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001 | System integrity claim and unauthorized-bypass traceability. |
| EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001 | Negative-test and authorized-boundary traceability. |
| EXTREF-IBM-ZOS-SECURITY-SERVER-0001 | Security manager and protected-resource traceability. |
| EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001 | Audit/evidence traceability. |
| TCG-001 | Measurement and attestation evidence traceability. |
| NIST-160-001 | Secure systems engineering and lifecycle traceability. |
| NIST-218-001 | Secure development practice traceability. |
| NIST-193-001 | Firmware resilience and recovery evidence. |
| SLSA-001 | Provenance and supply-chain evidence. |
| TUF-001 | Update metadata and anti-rollback evidence. |
| SEL4-001 | Formal assurance boundary and proof-assumption discipline. |
| FBVBS-001 | Internal transfer source for requirement/test/evidence traceability, no fake success, and production proof obligations. |

The canonical source ID ledger is:

```text
docs/design/source-matrix/source-matrix.yml
```

## 4. Registry Locations

Recommended future paths:

```text
docs/design/registries/
  requirements.yaml
  tests.yaml
  evidence.yaml
  glossary.yaml
  ai-output.yaml
  tasks.yaml
  conformance-claims.yaml
  cpu-feature-registry.yml
  cpu-target-profiles.yml
  registry-index.yaml
```

Release evidence copies should be archived under:

```text
artifacts/releases/<release_id>/registries/
```

Until those files exist, the split specs remain the source of record and this document defines the target schema.

## 5. Common Registry Envelope

Every registry YAML document MUST use this top-level envelope:

```yaml
registry_kind: requirements | tests | evidence | glossary | ai_output | tasks | conformance_claims | registry_index
schema_version: 1
registry_id: string
status: draft | review | ready | frozen | deprecated | superseded
generated_from:
  - path: string
generated_at_utc: timestamp?
updated_at_utc: timestamp
updated_by: string
non_compatibility_statement: string
source_matrix_ref:
  path: docs/design/source-matrix/source-matrix.yml
  schema_version: 1
entries:
  - {}
spec_gaps:
  - gap_id: string
    summary: string
registry_hash:
  algorithm: sha384
  value: hex?
registry_signature:
  signing_key_id: string?
  signature: string?
  signed_at_utc: timestamp?
```

Required envelope fields:

- `registry_kind`
- `schema_version`
- `registry_id`
- `status`
- `generated_from`
- `updated_at_utc`
- `updated_by`
- `non_compatibility_statement`
- `source_matrix_ref`
- `entries`
- `spec_gaps`

Envelope rules:

- `non_compatibility_statement` MUST state that MFOS does not claim z/OS compatibility or IBM product compatibility.
- `source_matrix_ref.path` MUST be `docs/design/source-matrix/source-matrix.yml` unless an ADR approves a successor.
- `schema_version` MUST be an integer.
- `entries` MUST be a list, even when empty.
- `registry_hash.value` MAY be empty in draft registries.
- `registry_signature` MAY be empty in draft registries and SHOULD be populated for release archives.

## 6. Common Scalar Types

### 6.1 ID Formats

| ID kind | Pattern | Example |
| --- | --- | --- |
| Source Matrix ID | `^[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3}$` | `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001` |
| Requirement ID | `^MFOS-REQ-[A-Z0-9]+-[0-9]{4}$` | `MFOS-REQ-SYSINT-0001` |
| Test ID | `^TEST-MFOS-[A-Z0-9]+-(POS|NEG|FUZZ|INT|CRASH|FAULT|CONF|MODEL)-[0-9]{4}$` | `TEST-MFOS-SI-NEG-0001` |
| Evidence ID | `^EV-MFOS-[A-Z0-9]+-[0-9]{4}$` | `EV-MFOS-AUDIT-0001` |
| Glossary term ID | `^MFOS-TERM-[A-Z0-9]+(?:-[A-Z0-9]+)*$` | `MFOS-TERM-SECURITYD` |
| AI output ID | `^MFOS-AIOUT-[A-Z0-9]+-[0-9]{8}-[0-9]{4}$` | `MFOS-AIOUT-AMF-20260427-0001` |
| Task ID | `^(DOC|SPEC|FORMAL|CI|HOST|NUC|SECD|AUD|CAT|DATA|JOB|SPL|OPER|WLM|AMF|UVS|PXM|GRD|LGW|OPS|REQCAT)-[0-9]{3,4}$` | `SPEC-001` |
| Conformance claim ID | `^MFOS-CLAIM-[A-Z0-9]+-[0-9]{4}$` | `MFOS-CLAIM-PROD-0001` |
| Release ID | `^MFOS-REL-[0-9]{8}(?:-[A-Za-z0-9._-]+)?$` | `MFOS-REL-20260427-rc1` |
| SPEC_GAP ID | `^(SPEC-GAP|[A-Z0-9]+-GAP)-[A-Z0-9-]*[0-9]{3,4}$` | `SPEC-GAP-AI-001` |

Existing prose specs contain legacy test IDs such as `OBJ-NEG-001` and gap IDs such as `REQCAT-GAP-001`. Machine-readable registries MUST preserve those values in `legacy_ids` while assigning canonical IDs.

### 6.2 Status Values

Common lifecycle values:

```text
draft
ready_for_review
reviewed
implemented
tested
evidenced
released
deprecated
superseded
blocked
rejected
```

Profile values:

```text
Baseline
Enterprise
High-Assurance
Dev
```

Verification method values:

```text
inspection
documentation_review
architecture_review
interface_test
unit_test
integration_test
negative_test
fuzz_test
crash_test
fault_injection
state_machine_test
model_check
proof_review
traceability_audit
release_review
supply_chain_audit
operator_drill
recovery_drill
attestation_review
ci_lint
```

## 7. Relationship To source-matrix.yml

Every registry entry that uses source-grounded behavior MUST reference `source_matrix_ids`.

Validation rules:

- Every `source_matrix_ids[]` value MUST exist in `docs/design/source-matrix/source-matrix.yml`.
- IBM-derived MFOS concepts MUST reference at least one `IBM-*` source ID.
- x64 mechanism claims MUST reference `X64-INTEL-001`, `X64-AMD-001`, or both as applicable.
- Guard/VBS-like claims MUST reference `MS-VBS-001` or `MS-VSM-001` and MUST be scoped to High-Assurance or explicitly optional Enterprise measurement helper behavior.
- `FBVBS-001` MAY support traceability and assurance discipline but MUST NOT be the only source for IBM semantic mapping.
- A registry entry MUST NOT contain compatibility claims with z/OS or IBM products.

Source resolution algorithm:

```text
for each registry entry:
  for each source_matrix_id:
    assert id exists in source-matrix.yml sources[].id
    assert source status is not deprecated unless entry has waiver
    assert source authority is valid for the entry's claim type
```

## 8. Requirements Registry Schema

Registry kind:

```yaml
registry_kind: requirements
```

Entry schema:

```yaml
RequirementRecord:
  requirement_id: string
  title: string
  statement: string
  namespace: string
  status: draft | ready_for_review | reviewed | implemented | tested | evidenced | released | blocked | deprecated | superseded
  profile_applicability:
    Baseline: required | optional | not_applicable
    Enterprise: required | optional | not_applicable
    High-Assurance: required | optional | not_applicable
  source_matrix_ids:
    - string
  owning_spec:
    path: string
    section: string?
  owning_subsystem: string
  protected_resources:
    - string
  system_interfaces:
    - string
  verification_methods:
    - string
  positive_test_ids:
    - string
  negative_test_ids:
    - string
  fuzz_target_ids:
    - string
  evidence_ids:
    - string
  task_ids:
    - string
  conformance_claim_ids:
    - string
  audit_obligations:
    - string
  failure_modes:
    - error_code: string
      condition: string
  unsupported_behavior: string?
  spec_gap_ids:
    - string
  depends_on:
    requirement_ids:
      - string
    source_matrix_ids:
      - string
  supersedes:
    - string
  superseded_by: string?
  rationale: string
  created_at_utc: timestamp
  updated_at_utc: timestamp
  review:
    reviewer: string?
    reviewed_at_utc: timestamp?
    notes: string?
```

Required fields:

- `requirement_id`
- `title`
- `statement`
- `namespace`
- `status`
- `profile_applicability`
- `source_matrix_ids`
- `owning_spec`
- `owning_subsystem`
- `verification_methods`
- `spec_gap_ids`
- `created_at_utc`
- `updated_at_utc`

Requirement validation rules:

- `requirement_id` MUST match the Requirement ID pattern.
- `namespace` MUST equal the area segment of `requirement_id`.
- `source_matrix_ids` MUST be non-empty for source-grounded requirements.
- Security-sensitive requirements MUST list at least one `negative_test_ids` entry or a blocking `spec_gap_ids` entry.
- Requirements touching protected resources MUST list `audit_obligations`.
- Requirements touching system interfaces MUST list `failure_modes`.
- A requirement with `status: released` MUST have at least one `evidence_ids` entry.
- A requirement MUST NOT be `tested` unless every linked required test is passing or waived.

## 9. Tests Registry Schema

Registry kind:

```yaml
registry_kind: tests
```

Entry schema:

```yaml
TestRecord:
  test_id: string
  legacy_ids:
    - string
  title: string
  test_type: positive | negative | fuzz | integration | unit | crash_recovery | fault_injection | conformance | model
  status: draft | implemented | passing | failing | flaky | blocked | deprecated | superseded
  requirement_ids:
    - string
  source_matrix_ids:
    - string
  owning_spec:
    path: string
    section: string?
  target_subsystem: string
  target_artifacts:
    - path: string
      symbol: string?
  preconditions:
    - string
  steps:
    - string
  expected_result: string
  expected_absence:
    - string
  expected_error_code: string?
  audit_expectations:
    - string
  fixtures:
    - path: string
  fuzz:
    target_name: string?
    corpus_path: string?
    seed_manifest: string?
    sanitizer_profile: string?
    minimum_duration: string?
  evidence_ids:
    - string
  ci_jobs:
    - string
  spec_gap_ids:
    - string
  created_at_utc: timestamp
  updated_at_utc: timestamp
```

Required fields:

- `test_id`
- `title`
- `test_type`
- `status`
- `requirement_ids`
- `owning_spec`
- `target_subsystem`
- `expected_result`
- `created_at_utc`
- `updated_at_utc`

Test validation rules:

- `test_id` MUST match the Test ID pattern.
- `negative` tests MUST include `expected_absence`.
- `fuzz` tests MUST include `fuzz.target_name`.
- Tests for source-grounded behavior MUST include `source_matrix_ids`.
- Tests for audit-required behavior MUST include `audit_expectations`.
- A test MUST NOT be `passing` unless it has at least one linked `evidence_ids` entry or CI result reference.
- A test linked to a missing requirement MUST fail registry validation.

## 10. Evidence Registry Schema

Registry kind:

```yaml
registry_kind: evidence
```

Entry schema:

```yaml
EvidenceRecord:
  evidence_id: string
  title: string
  evidence_type: test_report | fuzz_report | audit_record | audit_chain_report | review_record | proof_artifact | model_check_report | sbom | signed_provenance | attestation | recovery_drill | operator_drill | ci_lint_report | release_manifest
  status: draft | collected | verified | archived | rejected | expired | superseded
  requirement_ids:
    - string
  test_ids:
    - string
  source_matrix_ids:
    - string
  conformance_claim_ids:
    - string
  release_ids:
    - string
  artifact:
    path: string
    media_type: string?
    sha384: string?
    size_bytes: integer?
  produced_by:
    tool: string?
    version: string?
    ci_job: string?
    operator: string?
  produced_at_utc: timestamp
  retention:
    class: draft | release | production | high_assurance
    retain_until_utc: timestamp?
  verification:
    verifier: string?
    verified_at_utc: timestamp?
    verification_method: string?
    result: pass | fail | not_checked
  audit_linkage:
    audit_record_ids:
      - string
    correlation_ids:
      - string
  spec_gap_ids:
    - string
```

Required fields:

- `evidence_id`
- `title`
- `evidence_type`
- `status`
- `artifact`
- `produced_at_utc`
- `retention`
- `verification`

Evidence validation rules:

- `evidence_id` MUST match the Evidence ID pattern.
- Release evidence MUST include `artifact.sha384`.
- Evidence used by a released conformance claim MUST have `status: verified` or `status: archived`.
- Audit evidence MUST include `audit_linkage.audit_record_ids` or explain the gap.
- Supply-chain evidence MUST include SBOM or provenance type as applicable.
- Evidence MUST NOT support a claim if it is expired, rejected, or superseded without replacement.

## 11. Glossary Registry Schema

Registry kind:

```yaml
registry_kind: glossary
```

Entry schema:

```yaml
GlossaryTermRecord:
  term_id: string
  canonical_term: string
  aliases:
    - string
  prohibited_aliases:
    - string
  category: protected_resource | system_interface | service | mechanism | profile | evidence | role | state | error | task | other
  definition: string
  source_matrix_ids:
    - string
  semantic_overlap:
    - string
  mfos_divergence:
    - string
  allowed_wording:
    - string
  prohibited_wording:
    - string
  owning_spec:
    path: string
    section: string?
  related_requirement_ids:
    - string
  related_registry_entries:
    - registry_kind: string
      entry_id: string
  status: draft | reviewed | released | deprecated | superseded
  spec_gap_ids:
    - string
  created_at_utc: timestamp
  updated_at_utc: timestamp
```

Required fields:

- `term_id`
- `canonical_term`
- `category`
- `definition`
- `source_matrix_ids`
- `owning_spec`
- `status`
- `created_at_utc`
- `updated_at_utc`

Glossary validation rules:

- `term_id` MUST match the Glossary term ID pattern.
- IBM-derived terms MUST include `semantic_overlap`, `mfos_divergence`, `allowed_wording`, and `prohibited_wording`.
- `prohibited_wording` MUST include compatibility-risk phrases for IBM-derived terms.
- `canonical_term` MUST be unique ignoring case.
- `aliases` MUST NOT overlap `prohibited_aliases`.
- `protected_resource` and `system_interface` terms MUST link to at least one requirement.

## 12. AI Output Registry Schema

Registry kind:

```yaml
registry_kind: ai_output
```

Entry schema:

```yaml
AIOutputRecord:
  ai_output_id: string
  task_id: string
  title: string
  agent: string
  status: draft | accepted | rejected | superseded | blocked
  output_sections:
    implemented_requirement_ids:
      - string
    source_matrix_ids:
      - string
    assumptions:
      - string
    spec_gaps:
      - string
    unsupported_features:
      - string
    security_invariants:
      - string
    audit_obligations:
      - string
    failure_modes:
      - string
    tests_added:
      - string
    negative_tests_added:
      - string
    fuzz_targets_added:
      - string
    unsafe_code_justification: string
    review_checklist:
      - string
    evidence_artifacts:
      - string
  changed_files:
    - path: string
      ownership_scope: in_scope | out_of_scope
  related_requirement_ids:
    - string
  related_test_ids:
    - string
  related_evidence_ids:
    - string
  source_matrix_ids:
    - string
  ci_results:
    - ci_job: string
      result: pass | fail | skipped | not_run
  review:
    reviewer: string?
    decision: accepted | rejected | needs_changes | not_reviewed
    notes: string?
  created_at_utc: timestamp
  updated_at_utc: timestamp
```

Required fields:

- `ai_output_id`
- `task_id`
- `title`
- `agent`
- `status`
- `output_sections`
- `changed_files`
- `created_at_utc`
- `updated_at_utc`

AI output validation rules:

- `ai_output_id` MUST match the AI output ID pattern.
- `task_id` MUST exist in the task registry.
- All 14 mandatory output sections from `21-ai-implementation-contract.md` MUST be present.
- Security-sensitive outputs MUST list negative tests or a blocking SPEC_GAP.
- Parser changes MUST list fuzz targets or a blocking SPEC_GAP.
- `changed_files[].ownership_scope` MUST be `in_scope` for all changed files unless a review waiver exists.
- Output MUST NOT contain compatibility claims except as prohibited wording or negative-test examples.

## 13. Task Registry Schema

Registry kind:

```yaml
registry_kind: tasks
```

Entry schema:

```yaml
TaskRecord:
  task_id: string
  title: string
  task_type: doc | spec | formal | ci | hosted_prototype | nucleus | service | pxm | guard | gateway | operations | release | review
  status: proposed | ready | in_progress | blocked | implemented | reviewed | evidenced | closed | superseded
  owner: string
  owning_subsystem: string
  description: string
  allowed_paths:
    - string
  prohibited_paths:
    - string
  requirement_ids:
    - string
  source_matrix_ids:
    - string
  prerequisite_task_ids:
    - string
  prerequisite_spec_refs:
    - path: string
  expected_outputs:
    - string
  expected_tests:
    - string
  expected_evidence:
    - string
  negative_test_required: boolean
  fuzz_target_required: boolean
  ci_required:
    - string
  ai_output_ids:
    - string
  evidence_ids:
    - string
  spec_gap_ids:
    - string
  created_at_utc: timestamp
  updated_at_utc: timestamp
```

Required fields:

- `task_id`
- `title`
- `task_type`
- `status`
- `owner`
- `owning_subsystem`
- `description`
- `allowed_paths`
- `requirement_ids`
- `created_at_utc`
- `updated_at_utc`

Task validation rules:

- `task_id` MUST match the Task ID pattern.
- `allowed_paths` MUST be non-empty.
- A task that touches source-grounded concepts MUST list `source_matrix_ids`.
- `negative_test_required: true` requires `expected_tests` to include a negative test family.
- `fuzz_target_required: true` requires `expected_tests` to include a fuzz target family.
- A closed task MUST link to at least one `ai_output_ids` or evidence record unless it is documentation-only and explicitly says so.

## 14. Conformance Claims Registry Schema

Registry kind:

```yaml
registry_kind: conformance_claims
```

Entry schema:

```yaml
ConformanceClaimRecord:
  claim_id: string
  title: string
  claim_type: baseline_conformance | enterprise_conformance | high_assurance_conformance | production_readiness | negative_claim | component_conformance
  profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  status: draft | ready_for_review | reviewed | evidenced | released | blocked | rejected | expired | superseded
  statement: string
  non_compatibility_statement: string
  release_id: string?
  scope:
    in_scope:
      - string
    out_of_scope:
      - string
  source_matrix_ids:
    - string
  requirement_ids:
    - string
  test_ids:
    - string
  evidence_ids:
    - string
  production_gates:
    - gate_id: string
      status: pass | fail | not_applicable | blocked | not_checked
      evidence_ids:
        - string
  guard_evidence_required: boolean
  guard_evidence_ids:
    - string
  pxm_evidence_required: boolean
  pxm_evidence_ids:
    - string
  residual_risks:
    - string
  unsupported_features:
    - string
  spec_gap_ids:
    - string
  approvals:
    - reviewer: string
      role: architecture | security | release | assurance | operations | independent_tcb
      decision: approved | rejected | needs_changes
      decided_at_utc: timestamp
  created_at_utc: timestamp
  updated_at_utc: timestamp
```

Required fields:

- `claim_id`
- `title`
- `claim_type`
- `profile`
- `status`
- `statement`
- `non_compatibility_statement`
- `scope`
- `source_matrix_ids`
- `requirement_ids`
- `test_ids`
- `evidence_ids`
- `residual_risks`
- `unsupported_features`
- `spec_gap_ids`
- `created_at_utc`
- `updated_at_utc`

Conformance validation rules:

- `claim_id` MUST match the Conformance claim ID pattern.
- `non_compatibility_statement` MUST prohibit z/OS and IBM product compatibility claims.
- `High-Assurance` claims MUST set `guard_evidence_required: true`.
- `production_readiness` claims MUST include `production_gates`.
- A released production claim MUST have all applicable production gates in `pass` or `not_applicable`.
- A claim MUST NOT have `status: released` if it references unresolved blocking spec gaps.
- A claim level MUST NOT exceed the weakest linked evidence status.

## 15. Registry Index Schema

The registry index ties all registries together.

```yaml
registry_kind: registry_index
schema_version: 1
registry_id: MFOS-REGISTRY-INDEX-0001
status: draft
source_matrix_ref:
  path: docs/design/source-matrix/source-matrix.yml
  schema_version: 1
registries:
  - registry_kind: requirements
    path: docs/design/registries/requirements.yaml
    required_for_ci: true
  - registry_kind: tests
    path: docs/design/registries/tests.yaml
    required_for_ci: true
  - registry_kind: evidence
    path: docs/design/registries/evidence.yaml
    required_for_ci: true
  - registry_kind: glossary
    path: docs/design/registries/glossary.yaml
    required_for_ci: true
  - registry_kind: ai_output
    path: docs/design/registries/ai-output.yaml
    required_for_ci: true
  - registry_kind: tasks
    path: docs/design/registries/tasks.yaml
    required_for_ci: true
  - registry_kind: conformance_claims
    path: docs/design/registries/conformance-claims.yaml
    required_for_ci: true
validation_profiles:
  draft:
    fail_on: [schema_error, broken_reference, prohibited_claim]
  review:
    fail_on: [schema_error, broken_reference, prohibited_claim, missing_negative_test]
  release:
    fail_on: [schema_error, broken_reference, prohibited_claim, missing_negative_test, missing_evidence, unresolved_blocking_gap]
```

## 16. Cross-Registry Relations

Required relations:

```text
RequirementRecord.source_matrix_ids[] -> source-matrix.yml sources[].id
RequirementRecord.positive_test_ids[] -> TestRecord.test_id
RequirementRecord.negative_test_ids[] -> TestRecord.test_id
RequirementRecord.evidence_ids[] -> EvidenceRecord.evidence_id
RequirementRecord.task_ids[] -> TaskRecord.task_id
TestRecord.requirement_ids[] -> RequirementRecord.requirement_id
TestRecord.evidence_ids[] -> EvidenceRecord.evidence_id
EvidenceRecord.requirement_ids[] -> RequirementRecord.requirement_id
EvidenceRecord.test_ids[] -> TestRecord.test_id
GlossaryTermRecord.related_requirement_ids[] -> RequirementRecord.requirement_id
AIOutputRecord.task_id -> TaskRecord.task_id
AIOutputRecord.related_requirement_ids[] -> RequirementRecord.requirement_id
TaskRecord.requirement_ids[] -> RequirementRecord.requirement_id
ConformanceClaimRecord.requirement_ids[] -> RequirementRecord.requirement_id
ConformanceClaimRecord.test_ids[] -> TestRecord.test_id
ConformanceClaimRecord.evidence_ids[] -> EvidenceRecord.evidence_id
```

Consistency rules:

- No released conformance claim may reference draft requirements.
- No released conformance claim may reference failing tests.
- No released conformance claim may reference unverified evidence.
- No requirement may be marked released if it has no owning spec.
- No evidence may claim source grounding through a source ID that does not exist.
- No registry may create a new source ID; new source IDs must be added to `source-matrix.yml`.

## 17. Validation Rules

### 17.1 Structural Validation

| Rule ID | Severity | Rule |
| --- | --- | --- |
| REG-LINT-STRUCT-0001 | ERROR | Registry YAML must parse as YAML 1.2-compatible data. |
| REG-LINT-STRUCT-0002 | ERROR | Root value must be a mapping. |
| REG-LINT-STRUCT-0003 | ERROR | Common registry envelope required fields must be present. |
| REG-LINT-STRUCT-0004 | ERROR | `registry_kind` must match the file's expected registry type. |
| REG-LINT-STRUCT-0005 | ERROR | `entries` must be a list. |
| REG-LINT-STRUCT-0006 | ERROR | Entry IDs must be unique within a registry. |

### 17.2 Reference Validation

| Rule ID | Severity | Rule |
| --- | --- | --- |
| REG-LINT-REF-0001 | ERROR | Source Matrix IDs must exist in `source-matrix.yml`. |
| REG-LINT-REF-0002 | ERROR | Requirement refs must exist in requirements registry. |
| REG-LINT-REF-0003 | ERROR | Test refs must exist in tests registry. |
| REG-LINT-REF-0004 | ERROR | Evidence refs must exist in evidence registry. |
| REG-LINT-REF-0005 | ERROR | Task refs must exist in task registry. |
| REG-LINT-REF-0006 | ERROR | Conformance claim refs must exist in conformance registry. |
| REG-LINT-REF-0007 | WARN | Legacy IDs should map to canonical IDs. |

### 17.3 Security Validation

| Rule ID | Severity | Rule |
| --- | --- | --- |
| REG-LINT-SEC-0001 | BLOCK | Prohibited compatibility claims are not allowed outside prohibited wording or negative-test contexts. |
| REG-LINT-SEC-0002 | ERROR | Security-sensitive requirements must link to negative tests. |
| REG-LINT-SEC-0003 | ERROR | Audit-required requirements must link to audit obligations and evidence. |
| REG-LINT-SEC-0004 | ERROR | Parser requirements must link to fuzz targets. |
| REG-LINT-SEC-0005 | ERROR | High-Assurance claims must link to Guard evidence. |
| REG-LINT-SEC-0006 | ERROR | Production claims must link to production gates and evidence. |
| REG-LINT-SEC-0007 | ERROR | `UNSUPPORTED` and `SPEC_GAP` must not be represented as success. |

### 17.4 Release Validation

| Rule ID | Severity | Rule |
| --- | --- | --- |
| REG-LINT-REL-0001 | ERROR | Released requirements must have evidence. |
| REG-LINT-REL-0002 | ERROR | Released claims must have verified or archived evidence. |
| REG-LINT-REL-0003 | ERROR | Enterprise-Standalone, Enterprise-PXM, and High-Assurance release claims must link to SBOM and signed provenance evidence. |
| REG-LINT-REL-0004 | ERROR | High-Assurance release claims must link to Guard and attestation evidence. |
| REG-LINT-REL-0005 | ERROR | Waivers must have owner, reason, expiry, and affected gates. |

## 18. CI Usage

Draft-mode CI:

- parse registries
- validate IDs
- validate source-matrix references
- block prohibited compatibility claims
- report missing relations as warnings

Review-mode CI:

- all draft checks
- fail missing required fields
- fail missing negative tests for security-sensitive requirements
- fail parser entries without fuzz target links
- fail AI output records missing mandatory sections
- fail changed files outside task ownership scope

Release-mode CI:

- all review checks
- fail unresolved blocking spec gaps
- fail missing evidence
- fail unverified evidence
- fail production claims without gates
- fail High-Assurance claims without Guard evidence
- fail Enterprise-Standalone/Enterprise-PXM/High-Assurance claims without SBOM and signed provenance
- fail stale or expired evidence

Recommended CI jobs:

```text
registry-schema-lint
registry-reference-lint
source-matrix-link-lint
compatibility-wording-lint
requirement-negative-test-lint
audit-obligation-lint
fuzz-target-registry-lint
ai-output-contract-lint
task-ownership-lint
evidence-manifest-lint
conformance-claim-lint
production-gate-lint
```

## 19. Examples

### 19.1 Requirement Record Example

```yaml
requirement_id: MFOS-REQ-SYSINT-0001
title: Unauthorized subjects cannot bypass protected resources through system interfaces
statement: Unauthorized subjects MUST NOT bypass security policy, dataset access, audit, authorized state, or system control objects through system interfaces.
namespace: SI
status: reviewed
profile_applicability:
  Baseline: required
  Enterprise: required
  High-Assurance: required
source_matrix_ids:
  - EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
  - EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001
  - FBVBS-001
owning_spec:
  path: docs/design/specs/03-system-integrity.md
  section: "22. Requirements"
owning_subsystem: system-integrity
protected_resources:
  - DATASET
  - CATALOG_ENTRY
  - AUDIT_RECORD
system_interfaces:
  - SVC
  - PCALL
  - DatasetOpen
verification_methods:
  - negative_test
  - model_check
positive_test_ids:
  - TEST-MFOS-SI-POS-0001
negative_test_ids:
  - TEST-MFOS-SI-NEG-0001
fuzz_target_ids:
  - TEST-MFOS-SI-FUZZ-0001
evidence_ids: []
task_ids:
  - SPEC-003
conformance_claim_ids: []
audit_obligations:
  - Denied protected-resource access must emit required audit before caller final result.
failure_modes:
  - error_code: MFOS_ERR_UNAUTHORIZED
    condition: subject lacks securityd allow decision
spec_gap_ids: []
depends_on:
  requirement_ids: []
  source_matrix_ids:
    - EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
rationale: Source-grounded baseline system integrity invariant.
created_at_utc: "2026-04-27T00:00:00Z"
updated_at_utc: "2026-04-27T00:00:00Z"
```

### 19.2 Negative Test Record Example

```yaml
test_id: NEG-MFOS-DATASET-0001
legacy_ids:
  - NT-SI-001
title: BOB cannot open ALICE dataset
test_type: negative
status: draft
requirement_ids:
  - MFOS-REQ-SYSINT-0001
  - MFOS-REQ-DATASET-0002
source_matrix_ids:
  - EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
  - EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001
owning_spec:
  path: docs/design/specs/03-system-integrity.md
target_subsystem: datasetd
target_artifacts: []
preconditions:
  - ALICE owns USER.ALICE.INPUT
  - BOB lacks READ authority
steps:
  - Submit job as BOB with DD DSN=USER.ALICE.INPUT
expected_result: MFOS_ERR_POLICY_DENIED
expected_absence:
  - no dataset handle created
  - no SYSOUT success record
audit_expectations:
  - OPEN_DENY audit record emitted before final job result
evidence_ids: []
ci_jobs:
  - dataset-negative-tests
spec_gap_ids: []
created_at_utc: "2026-04-27T00:00:00Z"
updated_at_utc: "2026-04-27T00:00:00Z"
```

### 19.3 Evidence Record Example

```yaml
evidence_id: EV-MFOS-DATASET-0001
title: Unauthorized dataset access negative test report
evidence_type: test_report
status: collected
requirement_ids:
  - MFOS-REQ-DATASET-0002
test_ids:
  - NEG-MFOS-DATASET-0001
source_matrix_ids:
  - EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001
artifact:
  path: artifacts/tests/dataset-negative/report.json
  media_type: application/json
  sha384: ""
produced_by:
  tool: mfos-test
  ci_job: dataset-negative-tests
produced_at_utc: "2026-04-27T00:00:00Z"
retention:
  class: draft
verification:
  result: not_checked
audit_linkage:
  audit_record_ids: []
  correlation_ids: []
spec_gap_ids: []
```

### 19.4 Glossary Term Example

```yaml
term_id: MFOS-TERM-AMF
canonical_term: AMF
aliases:
  - Authorized Module Facility
prohibited_aliases:
  - APF-compatible module system
category: service
definition: MFOS facility for signed, measured, revocable, auditable authorized OS extension modules.
source_matrix_ids:
  - EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001
  - EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001
semantic_overlap:
  - Inspired by authorized program boundary concepts.
mfos_divergence:
  - AMF is not APF and is not administrator privilege.
allowed_wording:
  - AMF is APF-inspired OS extension authorization.
prohibited_wording:
  - AMF is APF-compatible.
owning_spec:
  path: docs/design/specs/12-amf.md
related_requirement_ids:
  - MFOS-REQ-AMF-0001
status: reviewed
spec_gap_ids: []
created_at_utc: "2026-04-27T00:00:00Z"
updated_at_utc: "2026-04-27T00:00:00Z"
```

### 19.5 AI Output Record Example

```yaml
ai_output_id: MFOS-AIOUT-AMF-20260427-0001
task_id: AMF-001
title: AMF manifest parser implementation output
agent: codex
status: draft
output_sections:
  implemented_requirement_ids:
    - MFOS-REQ-AMF-0001
  source_matrix_ids:
    - EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001
  assumptions: []
  spec_gaps: []
  unsupported_features: []
  security_invariants:
    - Invalid manifest cannot produce READY module.
  audit_obligations:
    - AMF load attempt emits audit record.
  failure_modes:
    - MFOS_ERR_AMF_SIGNATURE_INVALID
  tests_added:
    - TEST-MFOS-AMF-POS-0001
  negative_tests_added:
    - TEST-MFOS-AMF-NEG-0001
  fuzz_targets_added:
    - TEST-MFOS-AMF-FUZZ-0001
  unsafe_code_justification: None
  review_checklist:
    - Source IDs present.
  evidence_artifacts: []
changed_files:
  - path: implementation/services/amfd/src/manifest.rs
    ownership_scope: in_scope
related_requirement_ids:
  - MFOS-REQ-AMF-0001
created_at_utc: "2026-04-27T00:00:00Z"
updated_at_utc: "2026-04-27T00:00:00Z"
```

### 19.6 Task Record Example

```yaml
task_id: AMF-001
title: AMF manifest parser
task_type: service
status: ready
owner: amfd-agent
owning_subsystem: amfd
description: Implement AMF manifest parsing with fail-closed malformed input handling.
allowed_paths:
  - implementation/services/amfd/
  - tests/negative/amf/
requirement_ids:
  - MFOS-REQ-AMF-0001
source_matrix_ids:
  - EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001
expected_outputs:
  - manifest parser
expected_tests:
  - positive manifest parse
  - malformed manifest rejection
negative_test_required: true
fuzz_target_required: true
ci_required:
  - fuzz-target-registry-lint
created_at_utc: "2026-04-27T00:00:00Z"
updated_at_utc: "2026-04-27T00:00:00Z"
```

### 19.7 Conformance Claim Example

```yaml
claim_id: MFOS-CLAIM-PROD-0001
title: Baseline production readiness candidate
claim_type: production_readiness
profile: Baseline
status: draft
statement: MFOS Baseline production readiness candidate for hosted enterprise semantics.
non_compatibility_statement: MFOS is z/OS-inspired and does not claim z/OS or IBM product compatibility.
scope:
  in_scope:
    - hosted securityd/auditd/catalogd/datasetd/jobd/spoold/operatord
  out_of_scope:
    - High-Assurance Guard root protection
source_matrix_ids:
  - EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
requirement_ids:
  - MFOS-REQ-PROD-0001
test_ids: []
evidence_ids: []
production_gates:
  - gate_id: PROD-001
    status: not_checked
    evidence_ids: []
guard_evidence_required: false
guard_evidence_ids: []
pxm_evidence_required: false
pxm_evidence_ids: []
residual_risks:
  - PXM and Guard out of scope.
unsupported_features: []
spec_gap_ids:
  - SPEC-GAP-PROD-001
created_at_utc: "2026-04-27T00:00:00Z"
updated_at_utc: "2026-04-27T00:00:00Z"
```

## 20. SPEC_GAPs

| Gap ID | Gap | Blocking effect |
| --- | --- | --- |
| REG-GAP-0001 | JSON Schema files exist, but CUE equivalents and release-grade schema signing are not created. | Blocks claiming complete multi-format registry validation. |
| REG-GAP-0002 | Registry YAML paths exist for Phase 0.x design validation, but release freshness, waiver, and signing metadata are not finalized. | Blocks release-mode registry assurance. |
| REG-GAP-0003 | Canonical conversion from legacy test IDs to `TEST-MFOS-*` IDs is not implemented. | Blocks uniform test traceability. |
| REG-GAP-0004 | Requirement namespace registry is not fully synchronized with all split specs. | Blocks strict namespace lint. |
| REG-GAP-0005 | Evidence artifact storage layout and retention policy are not final. | Blocks production evidence archival. |
| REG-GAP-0006 | Registry signature key hierarchy and signing process are not defined. | Blocks signed release registry claims. |
| REG-GAP-0007 | CI waiver schema is not defined. | Blocks controlled release-mode exceptions. |
| REG-GAP-0008 | Formal model trace schema is not defined. | Blocks automated model-to-test trace validation. |
| REG-GAP-0009 | Source Matrix freshness and version pinning are not fully automated. | Blocks strict source freshness gates. |
| REG-GAP-0010 | Machine-readable ownership-scope enforcement is not implemented. | Blocks automated detection of out-of-scope AI edits. |
| REG-GAP-0011 | External certification mapping is intentionally undefined. | No external certification claim can be made. |

## 21. AI Prompt

Use this prompt when creating or validating MFOS registry entries:

```text
You are the MFOS machine-readable registry engineer.

MFOS is z/OS-inspired, not z/OS compatible.

Create or validate registry records for:
- requirements
- tests
- evidence
- glossary terms
- AI output
- tasks
- conformance claims

Rules:
- Use docs/design/source-matrix/source-matrix.yml as the source ID ledger.
- Do not invent Source Matrix IDs.
- Do not claim z/OS or IBM product compatibility.
- Preserve legacy IDs in legacy_ids while assigning canonical IDs.
- Link requirements to tests, evidence, tasks, and conformance claims.
- Link tests back to requirements.
- Link evidence to requirements and tests.
- Require negative tests for security-sensitive requirements.
- Require fuzz targets for parsers and binary interfaces.
- Require Guard evidence for High-Assurance claims.
- Require production gates for production readiness claims.
- Mark unknown behavior as SPEC_GAP and do not represent it as success.
```
