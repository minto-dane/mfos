# MFOS AI Work Packs

This file defines the recommended boundaries for assigning MFOS design and implementation work to AI agents.

Every pack must include:

```text
Purpose
Scope
Non-objectives
Source Matrix IDs
Requirements
Object model
State machine
Failure modes
Audit obligations
Positive tests
Negative tests
Fuzz targets
Spec gaps
Implementation allowed
AI prompt
```

## Pre-Implementation Gate

Before any pack may produce production code, its machine-readable contract must
show:

```text
Requirement IDs
Source Matrix IDs
Object model refs
State machine refs
Failure modes
Audit obligations
Positive tests
Negative tests
UNSUPPORTED and SPEC_GAP behavior
Fuzz target decision
Evidence artifact path
Claim boundary
Pack contract
Red-team review
```

If any item is missing, the assigned agent MUST produce a `SPEC_GAP_REPORT`
instead of code.

Hosted semantic prototype work is allowed only when the pack explicitly sets:

```yaml
implementation_allowed:
  hosted_semantic_prototype: true
  production: false
  hardware_enforcement_claim: false
  system_integrity_claim: semantic_only
```

## Pack Map

| Pack | Scope | Primary files |
| --- | --- | --- |
| PACK-00 | Normative language and profiles | `specs/00-normative-language.md` |
| PACK-01 | Source matrix and external reference mapping | `source-matrix/source-matrix.md`, `specs/02-source-matrix.md` |
| PACK-02 | Glossary | `specs/01-glossary.md` |
| PACK-03 | System integrity | `specs/03-system-integrity.md` |
| PACK-04 | Object model | `specs/05-object-model.md` |
| PACK-05 | Authorization/securityd | `specs/06-authorization.md` |
| PACK-06 | Audit/auditd | `specs/07-audit.md` |
| PACK-07 | Dataset and catalog | `specs/08-dataset-catalog.md` |
| PACK-08 | Job and spool | `specs/09-job-spool.md` |
| PACK-09 | Operator console | `specs/10-operator-console.md` |
| PACK-10 | Workload policy | `specs/11-workload-policy.md` |
| PACK-11 | AMF | `specs/12-amf.md` |
| PACK-12 | Update verification | `specs/13-update.md` |
| PACK-13 | Nucleus and SVC/PCALL | `specs/14-nucleus.md`, `specs/15-svc-pcall.md` |
| PACK-14 | PXM | `specs/16-pxm.md` |
| PACK-15 | PXM Guard | `specs/17-guard.md` |
| PACK-16 | Linux/Desktop gateway | `specs/18-linux-gateway.md` |
| PACK-17 | Assurance and conformance | `specs/19-assurance-case.md`, `specs/20-conformance.md`, `assurance/assurance-case-template.md` |
| PACK-18 | Prompts | `prompts/ai-prompts.md` |
| PACK-19 | Roadmap and task IDs | `tasks/work-breakdown.md` |
| PACK-20 | AI contract and production readiness | `specs/21-ai-implementation-contract.md`, `specs/22-production-readiness.md` |
| PACK-21 | Requirements and roadmap | `specs/23-requirements-catalog.md`, `tasks/implementation-roadmap.md` |
| PACK-22 | Formal methods | `specs/24-formal-methods.md`, `assurance/formal-model-plan.md` |
| PACK-23 | Operations and recovery | `specs/25-operations-recovery.md`, `assurance/operator-runbooks.md`, `assurance/operator-training-drills.md` |
| PACK-24 | Hardware profile and attestation | `specs/26-hardware-profile.md`, `specs/30-attestation-measured-boot.md` |
| PACK-25 | Spec and registry schemas | `specs/27-spec-front-matter.md`, `specs/28-machine-readable-registries.md`, `registries/README.md` |
| PACK-26 | Test strategy | `specs/29-test-strategy.md`, `tasks/test-taxonomy.md` |
| PACK-27 | Release workflow | `assurance/release-review-workflow.md`, `specs/31-release-distribution-rollback.md` |
| PACK-28 | Source lint and traceability automation | `source-matrix/source-lint-spec.md`, `source-matrix/traceability-index.md`, `tasks/spec-front-matter-migration.md` |
| PACK-29 | Language and Japanese sync | `specs/32-language-localization.md`, `ja/README.md`, `ja/SYNC-POLICY.md`, `tasks/japanese-doc-sync.md` |
| PACK-30 | Policy lint | `specs/33-policy-lint.md` |

## Pack Completion Checklist

```text
[ ] All z/OS-derived concepts include Source Matrix IDs.
[ ] All requirements use MFOS-REQ-* IDs.
[ ] All protected operations list audit obligations.
[ ] All fail-closed conditions are explicit.
[ ] All unsupported behavior returns UNSUPPORTED.
[ ] All unspecified behavior returns SPEC_GAP.
[ ] All parser-like inputs list fuzz targets.
[ ] Security-sensitive paths include negative tests.
[ ] implementation_allowed is explicit.
[ ] Pre-implementation gate is satisfied or a SPEC_GAP_REPORT is produced.
[ ] PXM and Guard responsibilities are not mixed with MFOS business semantics.
[ ] No compatibility claim is present.
```

## Phase 0.8 Pack Contract Freeze

PACK-05 through PACK-09 are frozen as specification-only packs for Phase 0.8.
Their machine-readable contracts live under `docs/design/packs/PACK-*/pack.yml`
and are mirrored in `packs/pack-index.yml`.

Implementation authorization for all five packs is:

```yaml
production: false
hosted_daemon: false
portable_semantic_core: false
executable_spec: false
specification_only: true
```

No Phase 0.8 pack authorizes Phase 1 implementation.

## Phase 0.9 Executable-Spec Pack Freeze

Phase 0.9 adds executable-spec artifacts for PACK-05 through PACK-09 without
starting implementation. The Phase 0.9 artifacts are test catalogs, fixtures,
golden vectors, oracle definitions, fuzz corpus plans, runner contracts, and
traceability matrices.

Implementation authorization remains:

```yaml
production: false
hosted_daemon: false
portable_semantic_core: false
semantic_runner: false
specification_only: true
```

Phase 0.9 outputs:

| Pack | Phase 0.9 artifacts |
| --- | --- |
| PACK-05 | `tests/catalog/authorization-tests.yml`, `tests/fixtures/auth/`, `tests/golden/auth/` |
| PACK-06 | `tests/catalog/audit-tests.yml`, `tests/fixtures/audit/`, `tests/golden/audit/` |
| PACK-07 | `tests/catalog/dataset-catalog-tests.yml`, `tests/fixtures/dataset/`, `tests/golden/dataset/` |
| PACK-08 | `tests/catalog/job-spool-tests.yml`, `tests/fixtures/job/`, `tests/golden/job/` |
| PACK-09 | `tests/catalog/operator-console-tests.yml`, `tests/fixtures/oper/`, `tests/golden/oper/` |
| Cross-domain | `tests/catalog/first-vertical-slice-tests.yml`, `tests/fixtures/first-vertical-slice/`, `tests/golden/first-vertical-slice/` |
| Fuzz planning | `fuzz/targets/phase-0-9-fuzz-target-plan.yml`, `fuzz/corpora/*/seed-plan.yml` |

The runner contract is defined in
`docs/design/specs/33-semantic-runner-contract.md`. This contract names future
commands but explicitly prohibits a Phase 0.9 runner implementation.
