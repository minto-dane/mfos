---
spec_id: MFOS-SPEC-43-DAFNY-EXECUTABLE-SEMANTICS-POLICY
title: MFOS Dafny Executable Semantics Policy
canonical_language: en-US
japanese_mirror: missing
status: draft
owner: MFOS architecture
last_reviewed: '2026-04-28'
source_refs:
- EXTREF-DAFNY-REFERENCE-0001
- EXTREF-AWS-AUTOMATED-REASONING-0001
- EXTREF-NIST-SECURE-SYSTEMS-ENGINEERING-0001
- EXTREF-NIST-SSDF-0001
- FBVBS-001
requirement_refs:
- MFOS-REQ-DAFNY-*
- MFOS-REQ-EXECSPEC-*
- MFOS-REQ-FORMAL-*
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs:
- PACK-34
- PACK-35
spec_gap_policy: implementation_must_not_infer_or_fill_gaps
---

# MFOS Dafny Executable Semantics Policy

Status: Draft Phase 1 policy. This document is specification-only and validation-only. It does not authorize production code, semantic-runner implementation, hosted daemon implementation, Rust semantic-core implementation, a Portable Semantic Core, generated production code, or any production readiness claim.

## 1. Purpose

Define the Phase 1 executable-semantics policy for MFOS. The canonical executable-semantics language for Phase 1 is Dafny. Phase 1 work remains limited to loader-only artifact validation.

This policy narrows the meaning of executable semantics. A Dafny artifact may define an MFOS-owned semantic model or proof-oriented contract, but the repository must not infer that a runtime evaluator, product feature, daemon, or production implementation exists.

No .dafny files are required by this scaffold. Dafny source files remain optional until a later reviewed task creates specific artifacts under this policy.

## 2. Scope

In scope:

- Dafny as the canonical Phase 1 executable-semantics artifact language.
- Loader-only validation of Dafny artifact metadata, dependency closure, source references, requirement references, and declared proof status.
- Rules for generated code from Dafny.
- Negative authorization boundaries for semantic runners, hosted daemons, Rust semantic-core work, and production claims.

Out of scope:

- Semantic-runner implementation.
- Hosted semantic daemon implementation.
- Rust semantic-core or Portable Semantic Core behavior.
- Production service code.
- Production loader behavior.
- Product conformance claims based on Dafny artifact presence alone.

## 3. Canonical Artifact Language

Dafny is the canonical executable-semantics language for MFOS Phase 1.

No Phase 1 document, pack, test plan, implementation task, or review note may designate Rust, a hosted semantic prototype, a semantic runner, a daemon, or generated code as the canonical executable-semantics authority.

The canonical artifact is the reviewed Dafny source plus its MFOS metadata. Generated output, tool logs, and translated code are evidence candidates only when explicitly reviewed and linked to a Dafny artifact. They do not replace the Dafny source.

## 4. Phase 1 Loader-only Boundary

Phase 1 allows loader-only artifact validation for Dafny executable-semantics artifacts. This is validation-only scope.

Allowed loader-only checks:

- File discovery under the approved Dafny scaffold.
- Metadata shape validation.
- Requirement ID and source ID presence checks.
- Dependency path and digest declaration checks.
- Declared proof-status checks.
- Detection of missing artifacts, malformed artifacts, unsupported declarations, and SPEC_GAP declarations.
- Emission of validation reports that say whether the artifact set is loadable.

Forbidden Phase 1 behavior:

- Evaluating MFOS behavior against fixtures or oracles.
- Executing a semantic model as a product decision engine.
- Treating artifact loading as conformance, production readiness, or runtime correctness.
- Filling unspecified behavior from implementation convenience.
- Converting `UNSUPPORTED` or `SPEC_GAP` into success.

Loader-only validation proves artifact shape and declared traceability only. It does not prove semantic correctness.

## 5. Generated Code Policy

Dafny-generated code is test-only in Phase 1.

Dafny-generated code MUST NOT be placed in production paths, linked into production services, packaged as an MFOS runtime component, or used as the implementation of a security decision, audit decision, loader decision, scheduler decision, partition decision, update decision, or operator command decision.

Dafny-generated code MAY be used only inside explicitly non-production validation or test contexts when all of the following are true:

- The generated artifact is traceable to the Dafny source.
- The test context is labeled non-production.
- The generated artifact is excluded from production packages and production readiness evidence.
- The result is reviewed as test evidence, not as product behavior.

## 6. No Semantic Runner

Phase 1 does not authorize a semantic runner.

The existing semantic-runner contract remains a future contract only. A Dafny loader may report whether artifacts are loadable, malformed, missing, unsupported, or blocked by SPEC_GAP. It must not execute test cases, apply fixtures, evaluate oracles, emit PASS or FAIL for MFOS behavior, or act as a conformance runner.

## 7. No Hosted Daemon

Phase 1 does not authorize a hosted daemon for executable semantics.

No `dafnyd`, hosted semantic service, HTTP service, RPC service, background worker, long-running evaluator, or service adapter may be introduced under this policy. Any request for hosted behavior must stop with `MFOS_ERR_SPEC_GAP` unless a later reviewed specification explicitly authorizes it.

## 8. No Rust Semantic Core

Phase 1 does not authorize a Rust semantic core or Portable Semantic Core.

Rust may remain available for ordinary loader tooling only when a later task explicitly authorizes such tooling and keeps it loader-only. Rust code must not define MFOS executable semantics, evaluate MFOS semantic behavior, or become a semantic-core substitute for Dafny in Phase 1.

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

## 11. Requirement Rules

| ID | Requirement | Verification |
| --- | --- | --- |
| `MFOS-REQ-DAFNY-0001` | Phase 1 executable-semantics artifacts MUST use Dafny as the canonical artifact language. | spec review |
| `MFOS-REQ-DAFNY-0002` | Phase 1 Dafny work MUST remain loader-only artifact validation. | loader review |
| `MFOS-REQ-DAFNY-0003` | Loader validation MUST NOT be represented as semantic execution, conformance, production readiness, or product correctness. | release review |
| `MFOS-REQ-DAFNY-0004` | Dafny-generated code MUST be test-only and MUST NOT enter production paths or production packages. | package review |
| `MFOS-REQ-DAFNY-0005` | Phase 1 MUST NOT implement or operate a semantic runner. | review |
| `MFOS-REQ-DAFNY-0006` | Phase 1 MUST NOT implement or operate a hosted executable-semantics daemon. | review |
| `MFOS-REQ-DAFNY-0007` | Phase 1 MUST NOT implement a Rust semantic core or Portable Semantic Core. | review |
| `MFOS-REQ-DAFNY-0008` | Missing or unspecified Dafny semantics MUST remain `SPEC_GAP` and MUST NOT be inferred by loader tooling. | negative review |
| `MFOS-REQ-DAFNY-0009` | Unsupported declarations MUST remain `UNSUPPORTED` and MUST NOT be converted into success. | negative review |
| `MFOS-REQ-DAFNY-0010` | No production claim may depend on this policy without a later production readiness gate. | release review |

## 12. Gaps

| Gap ID | Gap | Impact |
| --- | --- | --- |
| `DAFNY-GAP-0001` | Dafny toolchain source card and version pin are not registered in this policy. | Tool output cannot be accepted as reviewed proof evidence from this document alone. |
| `DAFNY-GAP-0002` | Dafny artifact metadata schema is not defined here. | Loader-only validation remains limited to scaffold and policy review until a schema exists. |
| `DAFNY-GAP-0003` | No semantic runner is authorized. | Dafny artifacts cannot produce PASS/FAIL runtime observations for MFOS behavior. |
| `DAFNY-GAP-0004` | No generated-code production path is authorized. | Dafny translation targets remain test-only. |
