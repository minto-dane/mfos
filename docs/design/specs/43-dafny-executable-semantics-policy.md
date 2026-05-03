---
spec_id: MFOS-SPEC-43-DAFNY-EXECUTABLE-SEMANTICS-POLICY
title: MFOS Dafny Executable Semantics Policy
canonical_language: en-US
japanese_mirror: missing
status: current
owner: MFOS architecture
last_reviewed: '2026-04-30'
source_refs:
- EXTREF-DAFNY-REFERENCE-0001
- EXTREF-AWS-AUTOMATED-REASONING-0001
- EXTREF-NIST-SECURE-SYSTEMS-ENGINEERING-0001
- EXTREF-NIST-SSDF-0001
- FBVBS-001
requirement_refs:
- MFOS-REQ-DAFNY-*
- MFOS-REQ-SEMSPEC-*
- MFOS-REQ-EXECSPEC-*
- MFOS-REQ-FORMAL-*
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs:
- PACK-34
- PACK-35
- PACK-37
spec_gap_policy: implementation_must_not_infer_or_fill_gaps
---

# MFOS Dafny Executable Semantics Policy

Status: Current Phase 1 policy. This document authorizes non-production Dafny executable-semantics source artifacts and conformance-harness validation. It does not authorize production code, semantic-runner implementation, semantic runner implementation, hosted daemon implementation, Rust semantic-core implementation, a Portable Semantic Core, generated production code, or any production readiness claim.

Phase 1 does not authorize semantic runner implementation.

## 1. Purpose

Define the Phase 1 executable-semantics policy for MFOS. The canonical executable-semantics language for Phase 1 is Dafny. Phase 1 work is limited to non-production Dafny model artifacts, deterministic fixture/oracle/golden loading, structural comparison, verification reporting, and traceability updates.

This policy narrows the meaning of executable semantics. A Dafny artifact may define an MFOS-owned semantic model or proof-oriented contract, but the repository must not infer that a runtime evaluator, product feature, daemon, or production implementation exists.

Dafny source files are allowed only under `formal/executable-semantics/dafny/` and related non-production test/evidence paths. Dafny must consume normalized typed input; it must not parse YAML directly.

## 2. Scope

In scope:

- Dafny as the canonical Phase 1 executable-semantics artifact language.
- Pure executable semantic contracts for authorization, audit, dataset/catalog, job/spool, operator console, and the first vertical slice.
- Deterministic fixture/oracle/golden loading and structural comparison.
- Validation of Dafny artifact metadata, dependency closure, source references, requirement references, and declared proof status.
- Rules for generated code from Dafny.
- Negative authorization boundaries for semantic runners, hosted daemons, Rust semantic-core work, and production claims.

Out of scope:

- Semantic-runner implementation.
- Hosted semantic daemon implementation.
- Rust semantic-core or Portable Semantic Core behavior.
- Production service code.
- Production loader behavior.
- Product conformance claims based on Dafny artifact presence alone.
- PXM, MFVM, Confidential VM, cluster, nucleus, Guard, or service implementation.

## 3. Canonical Artifact Language

Dafny is the canonical executable-semantics language for MFOS Phase 1.

No Phase 1 document, pack, test plan, implementation task, or review note may designate Rust, a hosted semantic prototype, a semantic runner, a daemon, or generated code as the canonical executable-semantics authority.

The canonical artifact is the reviewed Dafny source plus its MFOS metadata. Generated output, tool logs, and translated code are evidence candidates only when explicitly reviewed and linked to a Dafny artifact. They do not replace the Dafny source.

## 4. Phase 1 Non-production Boundary

Phase 1 allows non-production Dafny executable-semantics artifacts and a non-production conformance harness.

Allowed checks and artifacts:

- File discovery under the approved Dafny scaffold.
- Metadata shape validation.
- Requirement ID and source ID presence checks.
- Dependency path and digest declaration checks.
- Declared proof-status checks.
- Detection of missing artifacts, malformed artifacts, unsupported declarations, and SPEC_GAP declarations.
- Pure Dafny functions, predicates, lemmas, and symbolic state-transition contracts.
- Fixture/oracle/golden loading that does not encode MFOS business semantics.
- Structural comparison between model output shapes and golden-vector expectations.
- Emission of validation reports that state verification and comparison status.

Forbidden Phase 1 behavior:

- Executing a semantic model as a product decision engine.
- Treating artifact loading as conformance, production readiness, or runtime correctness.
- Filling unspecified behavior from implementation convenience.
- Converting `UNSUPPORTED` or `SPEC_GAP` into success.
- Implementing future `mfos-semantic-runner` commands.
- Starting a hosted executable-semantics daemon.

The conformance harness is non-production. It may compare deterministic artifacts and record results, but it is not a hosted daemon, service implementation, or product conformance claim.

## 5. Generated Code Policy

Dafny-generated code is test-only in Phase 1.

Dafny-generated code MUST NOT be placed in production paths, linked into production services, packaged as an MFOS runtime component, or used as the implementation of a security decision, audit decision, loader decision, scheduler decision, partition decision, update decision, or operator command decision.

Dafny-generated code MAY be used only inside explicitly non-production validation or test contexts when all of the following are true:

- The generated artifact is traceable to the Dafny source.
- The test context is labeled non-production.
- The generated artifact is excluded from production packages and production readiness evidence.
- The result is reviewed as test evidence, not as product behavior.

## 6. No Semantic Runner

Phase 1 does not authorize the future semantic runner.

The existing semantic-runner contract remains a future contract. A Phase 1 conformance harness may load fixtures, load embedded oracles, normalize deterministic inputs, compare expected output shapes, and record whether Dafny verification was run. It must not implement the named `mfos-semantic-runner` CLI, start a hosted evaluator, or become product behavior.

## 7. No Hosted Daemon

Phase 1 does not authorize a hosted daemon for executable semantics.

No `dafnyd`, hosted semantic service, HTTP service, RPC service, background worker, long-running evaluator, or service adapter may be introduced under this policy. Any request for hosted behavior must stop with `MFOS_ERR_SPEC_GAP` unless a later reviewed specification explicitly authorizes it.

## 8. No Rust Semantic Core

Phase 1 does not authorize a Rust semantic core or Portable Semantic Core.

Rust code must not define MFOS executable semantics, evaluate MFOS semantic behavior, or become a semantic-core substitute for Dafny in Phase 1. Python may be used for non-production validation tools that normalize and compare declared artifact structure without business semantics.

## 9. No Production Claim

This policy authorizes no production implementation.

The following claims are prohibited in Phase 1:

- Production readiness based on Dafny artifact existence.
- Production readiness based on Dafny verification output alone.
- Production use of generated code.
- Production use of a loader validation result.
- Runtime conformance based on loading Dafny artifacts.
- Security, audit, update, partition, job, dataset, catalog, or operator behavior implemented from Dafny-generated code.

Any release, report, or review that cites this policy must state that it is a specification and loader-validation policy only.

## 10. Artifact Location

The Phase 1 Dafny scaffold is:

```text
formal/executable-semantics/dafny/
```

This directory is reserved for Dafny executable-semantics source artifacts, metadata, and documentation. It is not a runtime source tree.

## 11. Toolchain Pin

Phase 1 Dafny verification uses the pinned Dafny release below:

```yaml
dafny_version: 4.11.0
dafny_version_output: 4.11.0+fcb2042d6d043a2634f0854338c08feeaaaf4ae2
z3_version: Z3 version 4.14.1 - 64 bit
install_script: scripts/install-dafny.sh
install_asset: dafny-4.11.0-x64-ubuntu-22.04.zip
install_sha256: a46a9ff7cdd720f7955854c78e95df13f4cfe6b80691b05f8654fe19e8267179
verify_command: scripts/validate-dafny-semantics.sh --require-dafny
module_glob: formal/executable-semantics/dafny/modules/*.dfy
```

CI must install this pinned toolchain before claiming Dafny verification
success. If the toolchain is missing, validation may report artifact status but
must not claim proof success.

## 12. Requirement Rules

| ID | Requirement | Verification |
| --- | --- | --- |
| `MFOS-REQ-DAFNY-0001` | Phase 1 executable-semantics artifacts MUST use Dafny as the canonical artifact language. | spec review |
| `MFOS-REQ-DAFNY-0002` | Phase 1 Dafny work MUST remain non-production conformance semantics and validation. | harness review |
| `MFOS-REQ-DAFNY-0003` | Validation and harness results MUST NOT be represented as production readiness or product correctness. | release review |
| `MFOS-REQ-DAFNY-0004` | Dafny-generated code MUST be test-only and MUST NOT enter production paths or production packages. | package review |
| `MFOS-REQ-DAFNY-0005` | Phase 1 MUST NOT implement or operate a semantic runner. | review |
| `MFOS-REQ-DAFNY-0006` | Phase 1 MUST NOT implement or operate a hosted executable-semantics daemon. | review |
| `MFOS-REQ-DAFNY-0007` | Phase 1 MUST NOT implement a Rust semantic core or Portable Semantic Core. | review |
| `MFOS-REQ-DAFNY-0008` | Missing or unspecified Dafny semantics MUST remain `SPEC_GAP` and MUST NOT be inferred by loader tooling. | negative review |
| `MFOS-REQ-DAFNY-0009` | Unsupported declarations MUST remain `UNSUPPORTED` and MUST NOT be converted into success. | negative review |
| `MFOS-REQ-DAFNY-0010` | No production claim may depend on this policy without a later production readiness gate. | release review |
| `MFOS-REQ-SEMSPEC-0001` | Phase 1 canonical executable semantics MUST be written in Dafny. | spec review |
| `MFOS-REQ-SEMSPEC-0002` | Rust MUST NOT be used as canonical Phase 1 semantic implementation. | negative review |
| `MFOS-REQ-SEMSPEC-0003` | Dafny generated code MUST NOT be linked into production MFOS binaries. | package review |
| `MFOS-REQ-SEMSPEC-0004` | Dafny semantics MUST consume normalized deterministic fixture input. | fixture review |
| `MFOS-REQ-SEMSPEC-0005` | Dafny semantics MUST NOT depend on host OS filesystem, process IDs, wall-clock time, sockets, or random state. | static review |
| `MFOS-REQ-SEMSPEC-0006` | Dafny semantic outputs MUST be comparable to Phase 0.9 golden vectors. | harness review |
| `MFOS-REQ-SEMSPEC-0007` | Semantic model conflicts between Dafny and TLA+/Alloy MUST be recorded as `SEMANTIC_MODEL_CONFLICT`. | model review |
| `MFOS-REQ-SEMSPEC-0008` | Phase 1 Rust semantic-core implementation is forbidden unless explicitly reauthorized by a later phase decision. | negative review |
| `MFOS-REQ-SEMSPEC-0009` | Fixture normalizer MUST NOT implement MFOS business semantics. | code review |
| `MFOS-REQ-SEMSPEC-0010` | Dafny model verification status MUST be recorded as evidence. | evidence review |

## 13. Phase 1.1 Semantic Coverage Closure

Phase 1.1 strengthens the Phase 1 Dafny executable-semantics artifacts without
authorizing production implementation.

Coverage traceability is generated under:

```text
evidence/traceability/generated/phase-1-1/
```

Current coverage judgment:

```yaml
core_domains_coverage_level:
  authorization: C0_NONE
  audit: C0_NONE
  dataset_catalog: C0_NONE
  job_spool: C0_NONE
  operator_console: C0_NONE
first_vertical_slice_coverage_level: C5_CONFORMANCE_LINKED
negative_semantics_complete: false
phase_1_1_semantic_coverage_complete: false
release_ready_model_claimed: false
```

The Phase 1.1 Dafny module set verified with `49 verified, 0 errors`.

## 14. Phase 1.2 Authorization/Audit Deepening

Phase 1.2 deepens the non-production Dafny executable semantics for
Authorization, Audit, and their integration boundary. It does not authorize
production implementation, Rust semantic-core work, hosted daemons, production
semantic runners, or service implementation.

Coverage traceability is generated under:

```text
evidence/traceability/generated/phase-1-2/
```

Current Phase 1.2 judgment:

```yaml
authorization_coverage_level: C4_VERIFIED_PROPERTY
audit_coverage_level: C5_CONFORMANCE_LINKED
auth_audit_integration_coverage_level: C5_CONFORMANCE_LINKED
formal_claim_proof_coverage_complete: false
authorization_audit_exit_blockers_remaining: false
release_ready_model_claimed: false
```

The Phase 1.2 Dafny module set verified with `97 verified, 0 errors`.

## 15. Phase 1.3 Dataset/Catalog Deepening

Phase 1.3 deepens the non-production Dafny executable semantics for
Dataset/Catalog and its Authorization/Audit integration boundary. It does not
authorize production implementation, catalogd, datasetd, storage, Rust
semantic-core work, hosted daemons, production semantic runners, or service
implementation.

Coverage traceability is generated under:

```text
evidence/traceability/generated/phase-1-3/
```

Current Phase 1.3 judgment:

```yaml
dataset_catalog_coverage_level: C5_CONFORMANCE_LINKED
dataset_catalog_requirement_coverage_level: C2_PARTIAL_SEMANTIC
dataset_catalog_auth_audit_integration_coverage_level: C4_VERIFIED_PROPERTY
formal_claim_proof_coverage_complete: false
dataset_catalog_exit_blockers_remaining: false
release_ready_model_claimed: false
```

The Phase 1.3 Dataset/Catalog Dafny closure was verified before Phase 1.4.1.
The current cumulative Phase 1 Dafny module set verifies with
`206 verified, 0 errors`.

Phase 1.3 Dataset/Catalog C5 scenario coverage is limited to the modeled
conformance rows, including fail-closed non-resolution of crash-mid-commit
partial candidates. Full catalog crash recovery selection is not modeled or
claimed in Phase 1.3, so aggregate requirement coverage remains partial.

## 16. Phase 1.4.1 Job Lifecycle / Effective Principal / DD Resolution

Phase 1.4.1 deepens only the non-production Dafny executable semantics for Job
lifecycle, effective principal establishment, and DD resolution. It does not
authorize full spool semantics, operator command semantics, real job execution,
production services, Rust semantic-core work, hosted daemons, production
semantic runners, or service implementation.

Coverage traceability is generated under:

```text
evidence/traceability/generated/phase-1-4-1/
```

Current Phase 1.4.1 judgment:

```yaml
job_lifecycle_coverage_level: C4_VERIFIED_PROPERTY
effective_principal_coverage_level: C4_VERIFIED_PROPERTY
dd_resolution_coverage_level: C4_VERIFIED_PROPERTY
parent_requirement_coverage_level: C2_PARTIAL_SEMANTIC
phase_scoped_requirement_subclaims: C4_VERIFIED_PROPERTY
formal_claim_proof_coverage_complete: false
production_implementation_started: false
release_ready_model_claimed: false
```

## 17. Gaps

| Gap ID | Gap | Impact |
| --- | --- | --- |
| `DAFNY-GAP-0001` | Dafny verification currently covers the Phase 1 module set only. | New modules must be added to the same pinned verification gate before being claimed verified. |
| `DAFNY-GAP-0002` | Dafny artifact metadata schema remains minimal. | Validation uses file/module policy and report evidence until a richer schema exists. |
| `DAFNY-GAP-0003` | No semantic runner is authorized. | Dafny artifacts cannot be exposed through future runner commands or hosted behavior. |
| `DAFNY-GAP-0004` | No generated-code production path is authorized. | Dafny translation targets remain test-only. |
