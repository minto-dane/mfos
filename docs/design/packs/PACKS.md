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

Hosted semantic prototype work is not allowed in Phase 1. Phase 1 is limited to
Dafny executable-semantics scaffold work and loader-only artifact validation
under `formal/executable-semantics/dafny/`. A later reviewed gate may define a
separate hosted prototype profile, but current pack contracts must keep hosted
prototypes, semantic runners, hosted daemons, Rust semantic-core work, and
production implementation disabled.

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
| PACK-24 | Hardware profile, architecture portability, and attestation | `specs/26-hardware-profile.md`, `specs/30-attestation-measured-boot.md`, `specs/44-architecture-portability-policy.md`, `specs/45-x86-64-target-profiles.md` |
| PACK-25 | Spec and registry schemas | `specs/27-spec-front-matter.md`, `specs/28-machine-readable-registries.md`, `registries/README.md`, `registries/cpu-feature-registry.yml`, `registries/cpu-target-profiles.yml` |
| PACK-26 | Test strategy | `specs/29-test-strategy.md`, `tasks/test-taxonomy.md` |
| PACK-27 | Release workflow | `assurance/release-review-workflow.md`, `specs/31-release-distribution-rollback.md` |
| PACK-28 | Source lint and traceability automation | `source-matrix/source-lint-spec.md`, `source-matrix/traceability-index.md`, `tasks/spec-front-matter-migration.md` |
| PACK-29 | Language and Japanese sync | `specs/32-language-localization.md`, `ja/README.md`, `ja/SYNC-POLICY.md`, `tasks/japanese-doc-sync.md` |
| PACK-30 | Policy lint | `specs/33-policy-lint.md` |
| PACK-31 | MFVM | `specs/42-mfvm.md`, `specs/36-hypervisor-class-virtualization.md` |
| PACK-32 | Confidential VM | `specs/37-confidential-vm.md`, `specs/42-mfvm.md` |
| PACK-33 | Datacenter cluster | `specs/38-datacenter-cluster-operations.md`, `specs/41-performance-and-secure-operations.md` |
| PACK-34 | Language verification | `specs/39-language-and-verification-policy.md`, `specs/43-dafny-executable-semantics-policy.md` |
| PACK-35 | Automated reasoning | `specs/40-automated-reasoning-program.md`, `specs/43-dafny-executable-semantics-policy.md`, `formal/registry.yml` |
| PACK-36 | Performance and secure operations | `specs/41-performance-and-secure-operations.md` |
| PACK-37 | Dafny executable semantics | `specs/43-dafny-executable-semantics-policy.md`, `formal/executable-semantics/dafny/modules/`, `tools/dafny-conformance-harness/` |

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
| PACK-05 | `tests/catalog/authorization.yml`, `tests/fixtures/auth/`, `tests/golden/auth/` |
| PACK-06 | `tests/catalog/audit.yml`, `tests/fixtures/audit/`, `tests/golden/audit/` |
| PACK-07 | `tests/catalog/dataset-catalog.yml`, `tests/fixtures/dataset/`, `tests/golden/dataset/` |
| PACK-08 | `tests/catalog/job-spool.yml`, `tests/fixtures/job/`, `tests/golden/job/` |
| PACK-09 | `tests/catalog/operator-console.yml`, `tests/fixtures/oper/`, `tests/golden/oper/` |
| Cross-domain | `tests/catalog/first-vertical-slice.yml`, `tests/fixtures/first-vertical-slice/`, `tests/golden/first-vertical-slice/` |
| Fuzz planning | `fuzz/targets/fuzz-target-plan.yml`, `fuzz/corpora/*/seed-plan.yml` |

The runner contract is defined in
`docs/design/specs/33-semantic-runner-contract.md`. This contract names future
commands but explicitly prohibits a Phase 0.9 runner implementation.

## PXM / MFVM Deferred Pack Topology

The deferred pack topology records design-only contracts for PXM Core, MFVM,
Confidential VM profiles, datacenter/cluster operations, language verification,
automated reasoning, and performance/secure operations. The current topology
originated in the Phase 0.10 requirements expansion, but the pack contracts are
durable routing artifacts rather than a phase changelog.

The user-facing requested names `PACK-25` through `PACK-29` were not reused
because the repository already assigns those IDs to existing canonical packs;
this topology therefore updates `PACK-14` for PXM and adds `PACK-31` through
`PACK-36` for the new planning domains.

Implementation authorization for `PACK-14` and `PACK-31` through `PACK-36` is:

```yaml
production: false
hosted_daemon: false
semantic_runner: false
portable_semantic_core: false
executable_spec: false
specification_only: true
```

Phase 1 remains limited to loader-only artifact validation for these domains.
No PXM, MFVM, Confidential VM, cluster, semantic evaluator, hosted daemon, or
production implementation is authorized by these design-only pack contracts.

## Architecture Portability And x86-64 Target Profiles

PACK-24 and PACK-25 now route architecture portability and CPU profile policy.
MFOS is x86-64-first for initial implementation planning, not x86-64-only.
Architecture-neutral enterprise semantics must remain separate from
architecture-specific enforcement. x86-64-v4 is an optional performance profile,
not baseline. Intel TDX and AMD SEV-SNP are Confidential VM profile
technologies. Intel SGX is an optional enclave/TEE profile and must not be
modeled as a Confidential VM profile. CPU target profiles must reference
machine-readable CPU Feature Registry IDs before any later architecture-backend
implementation can be assigned.

## Phase 1 Dafny Executable-Semantics Gate

Phase 1 executable semantics are Dafny-first, non-production, and scoped to
reviewed semantic artifacts plus deterministic conformance checks. The
controlling policy is
`docs/design/specs/43-dafny-executable-semantics-policy.md`.

The Phase 1 Dafny verification toolchain is pinned by
`scripts/install-dafny.sh` to Dafny 4.11.0 with bundled Z3 4.14.1. Current
module verification is recorded in `reports/current/dafny-verification-report.md`.

Allowed Phase 1 work:

- Dafny executable-semantics source artifacts under
  `formal/executable-semantics/dafny/modules/`.
- Fixture/oracle/golden loading and deterministic structural comparison.
- Traceability and verification status reporting.
- Non-production conformance harness tooling under `tools/`.

Forbidden Phase 1 work:

- Rust semantic-core or Portable Semantic Core implementation.
- Semantic-runner implementation or semantic-runner commands.
- Hosted semantic prototypes, hosted daemons, service adapters, or production
  services.
- Dafny-generated production code.
- PXM, MFVM, Confidential VM, or cluster implementation.
