# MFOS Machine-Readable Registries

Status: Draft seed

This directory contains initial machine-readable registry seeds for MFOS. The schema source is [28-machine-readable-registries.md](../specs/28-machine-readable-registries.md), and the Source Matrix ID ledger is the Source Card index [source-matrix.yml](../source-matrix/source-matrix.yml) plus `../source-matrix/cards/*.yml`.

MFOS is source-grounded and z/OS-inspired. These registries do not claim z/OS compatibility, z/Architecture compatibility, IBM API compatibility, RACF compatibility, JES compatibility, DFSMS compatibility, SMF compatibility, external workload management compatibility, APF compatibility, PR/SM compatibility, Windows VBS compatibility, Linux compatibility, or UNIX compatibility.

## Files

| File | Registry kind | Purpose |
| --- | --- | --- |
| [requirements.yaml](requirements.yaml) | `requirements` | Seed requirement records with Source Matrix IDs, verification methods, test links, evidence links, task links, audit obligations, and gaps. |
| [tests.yaml](tests.yaml) | `tests` | Seed positive, negative, and fuzz test metadata. Negative tests include expected absence of success side effects. |
| [evidence.yaml](evidence.yaml) | `evidence` | Draft expected evidence artifacts for tests and CI. These are placeholders, not verified release evidence. |
| [tasks.yaml](tasks.yaml) | `tasks` | Seed task ownership and expected outputs for registry, Dafny semantic, audit, and CI work. |
| [cpu-feature-registry.yml](cpu-feature-registry.yml) | `cpu_feature_registry` | Design-time CPU feature identity, source grounding, profile affinity, evidence expectation, fallback, and review-state registry. It is not a feature detector. |
| [cpu-target-profiles.yml](cpu-target-profiles.yml) | `cpu_target_profiles` | Design-time x86-64 target profile registry. Profiles reference CPU Feature Registry IDs and do not authorize architecture backend implementation. |

## Current Seed Scope

The v0.5 seed set covers the priority requirements from the current review pass:

- `MFOS-REQ-CATALOG-0002`: `catalogd` resolves only committed catalog entries.
- `MFOS-REQ-AUDIT-0002` / `MFOS-REQ-AUDIT-0005`: deny-audit ordering and audit failure behavior.
- `MFOS-REQ-AUTH-0001` / `0002` / `0004`: central securityd decision discipline.
- `MFOS-REQ-DATASET-0001` / `0002` / `0006`: dataset handle binding and denial behavior.
- `MFOS-REQ-UPDATE-0004` / `0005` / `0006`: rollback, freeze, and mix-and-match defense.
- `MFOS-REQ-PARTITION-0005` / `0006` / `0016` / `0017`: PXM device assignment and teardown.
- `MFOS-REQ-AMF-0021`: AMF disabled mode returns `MFOS_ERR_UNSUPPORTED`.
- `MFOS-REQ-NUCLEUS-0008`: Baseline requires NX-capable platform and W^X policy.
- `MFOS-REQ-PROFILE-0001`: Enterprise profile split.
- `MFOS-REQ-SYSINT-0001` and `MFOS-REQ-AI-0005`: system integrity and no-fake-success baseline.
- `MFOS-REQ-SYSINT-0002` through `MFOS-REQ-SYSINT-0020`: Phase 0.7 system-interface,
  authorized-state, claim-boundary, SVC/PCALL, audit-evidence, dataset-handle,
  job-identity, operator-command, AMF, PXM, Guard, and hardware-mechanism
  integrity requirements.
- `MFOS-REQ-ARCH-*`, `MFOS-REQ-X64-*`, `MFOS-REQ-X64-V4-*`,
  `MFOS-REQ-X64-CVM-*`, `MFOS-REQ-X64-TEE-*`,
  `MFOS-REQ-HARDENING-*`, and `MFOS-REQ-CPUFEAT-*`: architecture
  portability, x86-64 target profiles, optional v4, CVM, SGX/TEE, hardening,
  and CPU feature registry policy.

The linked seed tests cover:

- ALICE authorized dataset read positive path.
- BOB denied access to ALICE dataset with no handle creation.
- deny-audit ordering.
- fake-success scanner fixture.
- DSN parser fuzz target metadata.
- Phase 0.7 system-integrity negative tests covering unregistered interfaces,
  AMF/admin confusion, Baseline overclaim, missing Guard evidence, raw pointers,
  unsupported/SPEC_GAP success, log-as-audit substitution, dataset handle
  binding, missing job principal, operator destructive command, AMF boundary,
  PXM scope, Guard scope, and hardware overclaim.
- Architecture portability and x86-64 target-profile review tests covering
  x86-64-first-but-not-only boundaries, optional v4, TDX/SEV-SNP CVM profiles,
  SGX as TEE rather than CVM, CET/CFI evidence claims, and CPU Feature Registry
  cross-references.

## Validation Intent

Future CI should run these checks:

```text
registry-schema-lint
registry-reference-lint
source-matrix-link-lint
compatibility-wording-lint
requirement-negative-test-lint
audit-obligation-lint
fuzz-target-registry-lint
task-ownership-lint
evidence-manifest-lint
```

Draft-mode CI should parse YAML, validate ID formats, validate `source_refs[].source_id` against `../source-matrix/source-matrix.yml` and `../source-matrix/cards/*.yml`, reject prohibited compatibility claims, and report missing registry relations as warnings.

Release-mode CI must fail on missing evidence, unresolved blocking gaps, unverified evidence, production claims without gates, High-Assurance claims without Guard evidence, and Enterprise-Standalone/Enterprise-PXM/High-Assurance claims without SBOM and signed provenance.

## Explicit Gaps

- `REG-GAP-0001`: Schema files exist under `schemas/` and `schemas/mfos/`,
  but registry-entry-to-schema coverage is still being expanded. Schema
  existence must not be treated as full validation coverage.
- `REG-GAP-0002`: Registry generator tooling is not implemented.
- `REG-GAP-0003`: Legacy test ID migration to canonical `TEST-MFOS-*` IDs is not automated.
- `REG-GAP-0004`: Requirement namespace registry is not fully synchronized with all split specs.
- `REG-GAP-0005`: Evidence storage layout and retention policy are not final.
- `REG-GAP-0006`: Registry signature key hierarchy and signing process are not defined.
- `REG-GAP-0007`: CI waiver schema is not defined.
- `REG-GAP-0008`: Formal model trace schema is not defined.
- `REG-GAP-0009`: Source Matrix freshness and version pinning are not fully automated.
- `REG-GAP-0010`: Machine-readable ownership-scope enforcement is not implemented.

## Editing Rules

- Do not add a source ID here; add it to `docs/design/source-matrix/source-matrix.yml`.
- Do not mark draft evidence as release evidence.
- Do not mark a requirement `released` without verified evidence links.
- Preserve legacy IDs in `legacy_ids` when converting prose test IDs.
- Keep negative tests focused on both denial and absence of success side effects.
- Do not use these registries to broaden conformance or production claims.
