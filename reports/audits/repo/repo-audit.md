# MFOS Phase 0.6 Repository Audit

Audit date: 2026-04-27
Workspace: `/home/nia/mfos`
Git status: unavailable; this workspace is not a Git repository.

## Scope

This audit inspected repository structure and current canonical, bridge,
generated, and implementation-signaling paths. It did not inspect source
history and did not validate implementation behavior. No implementation code was
started.

## Executive Summary

The repository currently declares `docs/design/` as the canonical Phase 0.6
design corpus. Top-level directories such as `specs/`, `requirements/`,
`sources/`, `source-matrix/`, `claims/`, `packs/`, and `tasks/` are mostly
bridge or future-promotion paths. The implementation tree is heavily scaffolded
but contains only README/status material in the inspected paths; production
implementation claims are explicitly disallowed by local documentation.

Primary risk: many empty or named implementation/test/fuzz/formal/CI directories
look like active subsystem status even though the available evidence is
scaffold-only. The repo has useful disclaimers, but auditors and agents should
treat these directories as placeholders until tests, source IDs, requirements,
and evidence records exist.

## Canonical Documentation

Current canonical source-of-truth paths observed:

| Artifact family | Canonical path | Evidence |
| --- | --- | --- |
| Design canon | `docs/design/mfos-design.md` | Root README and ADR-0006 identify it as current design canon/candidate. |
| Design entrypoint | `docs/design/README.md` | Reading order and AI work rules. |
| Status | `docs/design/STATUS.md` | Current work status and known gaps. |
| Split specs | `docs/design/specs/*.md` and `docs/design/specs/INDEX.md` | English canonical split specifications, 00 through 33 plus index. |
| Source Card index | `docs/design/source-matrix/source-matrix.yml` | Declared current Source Card index. |
| Source Cards | `docs/design/source-matrix/cards/*.yml` | 37 Source Cards observed. |
| Requirements registry | `docs/design/registries/requirements.yaml` | Declared current v0.5 priority requirements catalog. |
| Requirements schema note | `docs/design/registries/requirements-schema.md` | Current schema note for the registry. |
| Registry seeds | `docs/design/registries/tests.yaml`, `evidence.yaml`, `tasks.yaml` | Draft seeds downstream of specs. |
| Pack overview | `docs/design/packs/PACKS.md` | Current pack plan. |
| Prompt canon | `docs/design/prompts/ai-prompts.md` | Current canonical prompt content. |
| Assurance docs | `docs/design/assurance/*.md` | Current assurance, evidence, runbook, formal-plan, and release-review docs. |
| Task docs | `docs/design/tasks/*.md` | Current work breakdown, roadmap, test taxonomy, migration, and Japanese sync tasks. |
| Language policy | `docs/design/specs/32-language-localization.md`, `docs/design/ja/SYNC-POLICY.md` | English canonical; Japanese mirror explanatory/incomplete. |

Additional governance/canonical-path documentation:

- `README.md` states the current canonical design corpus lives under `docs/design/`.
- `adr/ADR-0006-canonical-paths-and-implementation-root.md` proposes current Phase 0.6 canonical paths and says top-level bridge paths remain non-canonical until a reviewed migration ADR.

## Bridge Documentation

Observed bridge or future-promotion paths:

| Path | Current role | Canonical target |
| --- | --- | --- |
| `specs/README.md` | Top-level specs bridge; reserved for future promotion. | `docs/design/specs/` |
| `specs/canonical-index.yml` | Machine-readable specs bridge. | `docs/design/specs/INDEX.md`, `docs/design/specs/` |
| `requirements/README.md` | Top-level requirements bridge. | `docs/design/registries/requirements.yaml` |
| `requirements/catalog.yml` | Requirements bridge metadata. | `docs/design/registries/requirements.yaml` |
| `requirements/requirement.schema.yml` | Bridge schema shape. | `docs/design/registries/requirements-schema.md` |
| `requirements/by-domain/README.md` | Reserved future split location. | `docs/design/registries/requirements.yaml` |
| `source-matrix/README.md` | Top-level Source Matrix bridge. | `docs/design/source-matrix/source-matrix.yml` |
| `sources/README.md` | Top-level source-grounding layer; future source/concept card home. | `docs/design/source-matrix/cards/`, `docs/design/source-matrix/source-matrix.yml` |
| `sources/registry.yml` | Source-grounding bridge metadata. | `docs/design/source-matrix/source-matrix.yml` and cards |
| `sources/source-card.schema.yml` | Bridge Source Card shape. | `docs/design/source-matrix/source-card-schema.md` |
| `schemas/README.md` | Future executable schema home. | Current schema notes under `docs/design` plus bridge files |
| `claims/README.md` | Future assurance claim tree home. | `docs/design/specs/19-assurance-case.md` |
| `packs/README.md` | Future AI work packet home. | `docs/design/packs/PACKS.md` |
| `tasks/README.md` | Task and roadmap bridge. | `docs/design/tasks/` |
| `prompts/README.md` | Prompt bridge. | `docs/design/prompts/ai-prompts.md` |

These bridge docs generally state their non-canonical status clearly.

## Generated and Draft Registry Documentation

Observed generated/draft signals:

| Path | Signal | Audit note |
| --- | --- | --- |
| `requirements/generated/README.md` | "Generated matrices belong here. Do not hand-edit generated files." | Directory is scaffold-only. |
| `ai/task-packets/generated/` | Generated task packet path by name. | Empty scaffold; could imply generation exists. |
| `implementation/runtime/generated/` | Generated runtime path by name. | Empty scaffold; could imply generated ABI/types exist. |
| `docs/design/source-matrix/source-matrix.yml` | `generated_from: docs/design/source-matrix/source-matrix.yaml` | Current canonical Source Card index is generated from legacy/intermediate YAML. |
| `docs/design/source-matrix/source-matrix.yaml` | `generated_from: docs/design/source-matrix/source-matrix.md` | Legacy/intermediate conversion artifact remains present. |
| `docs/design/registries/tests.yaml` | Draft registry seed; generated_from spec list; generated_at null. | Metadata, not executed tests. |
| `docs/design/registries/evidence.yaml` | Draft expected evidence records; comments say not verified evidence. | Must not be treated as release evidence. |
| `docs/design/registries/tasks.yaml` | Draft task ownership seed; generator tooling not implemented. | Some task statuses such as `implemented`/`ready` are registry metadata only. |
| `docs/design/ja/translation-units.yaml` | Draft Japanese translation units. | Mirrors mostly missing/partial. |
| `docs/design/ja/sync-status.yaml` | Draft sync status; generator/lint gaps listed. | Does not establish Japanese parity. |

## Implementation Documentation

Implementation-related documentation observed:

| Path | Current evidence | Status implication risk |
| --- | --- | --- |
| `implementation/README.md` | Lists runtime, nucleus, services, PXM, Guard, sidecars, interfaces, tools, prototypes. Explicitly says not to infer production readiness from directory presence. | Low if README is read; medium from directory names alone. |
| `implementation/prototypes/hosted-semantic/README.md` | Declares `production_claim: false`, `hardware_enforcement_claim: false`, `system_integrity_claim: semantic_only`. | Low for prototype claim, but empty child dirs may imply progress. |
| `implementation/services/README.md` | Says early implementation should start under hosted semantic services; production services require requirements/source/tests/audit. | Medium because many service dirs exist with no implementation evidence. |
| `implementation/nucleus/README.md` | Production nucleus work should wait for reviewed specs. | Medium because nucleus substructure is detailed. |
| `implementation/pxm/README.md` | Defines PXM boundary. | Medium because PXM hardware subdirs are detailed. |
| `implementation/guard/README.md` | Defines Guard root-object protection scope. | Medium because Guard root subdirs are detailed. |
| `implementation/runtime/README.md` | Downstream of specs and requirements. | Medium because ABI/generated dirs imply future generated types. |
| `implementation/tools/README.md` | Tools must not bypass `securityd` or `auditd`. | Medium because named tools exist as directories only. |
| `ai/contracts/ai-implementation-contract.md` | Draft implementation contract. | Medium duplicate-risk because canonical counterpart exists under `docs/design/specs/21-ai-implementation-contract.md` and prompts under `docs/design/prompts/ai-prompts.md`. |

No non-README implementation source files were observed under `implementation/`.

## Duplicate Source-of-Truth Risks

| Risk | Paths | Severity | Rationale |
| --- | --- | --- | --- |
| Split specs may be duplicated after promotion starts. | `docs/design/specs/`, `specs/` | Medium | `specs/` is currently a bridge. Any normative spec added there before migration would compete with canonical English specs. |
| Requirement registry may fork. | `docs/design/registries/requirements.yaml`, `requirements/catalog.yml`, `requirements/requirement.schema.yml`, `requirements/by-domain/` | Medium | Top-level requirement files are bridge metadata, but the path names can look canonical. |
| Source Card ledger may fork. | `docs/design/source-matrix/source-matrix.yml`, `source-matrix/`, `sources/registry.yml`, `sources/**/source-cards/` | Medium | Future source-card homes exist while current cards remain canonical under `docs/design`. |
| AI implementation contract may fork. | `docs/design/specs/21-ai-implementation-contract.md`, `docs/design/prompts/ai-prompts.md`, `ai/contracts/ai-implementation-contract.md` | Medium | The top-level AI contract is draft and downstream; it should not override canonical spec/prompt rules. |
| Japanese mirror may be mistaken as canonical. | `docs/design/ja/README.md`, `docs/design/ja/SYNC-POLICY.md`, `docs/design/ja/*.yaml` | Low | Docs state English wins, but mirror status is incomplete and several planned mirror paths are absent. |
| Registry seeds may be mistaken for verified implementation/test/evidence status. | `docs/design/registries/tests.yaml`, `evidence.yaml`, `tasks.yaml` | High | Seed records include task/test/evidence identifiers and statuses, but evidence is draft and generator tooling is not implemented. |
| Generated/intermediate source matrix files may confuse index authority. | `docs/design/source-matrix/source-matrix.md`, `.yaml`, `.yml` | Medium | `source-matrix.yml` is current canonical index; `.yaml` and `.md` remain nearby as source/intermediate/history. |

## Paths That Could Imply Implementation Status Without Evidence

The following directories are scaffolded and could be misread as completed or
in-progress implementation status. Treat them as placeholders unless accompanied
by requirement IDs, source IDs, tests, evidence artifacts, and implementation
files.

Implementation:

- `implementation/services/{securityd,auditd,catalogd,datasetd,jobd,spoold,operatord,workpolicyd,amfd,uvsd,apid,paneld,commandd,common}/`
- `implementation/nucleus/{address-space,arch,boot,memory,scheduler,svc,pcall,ipc,handles,audit-hooks,services,faults,tests}/`
- `implementation/runtime/{abi,common,generated}/`
- `implementation/runtime/abi/{svc,pcall,pxm-call,guard-call}/`
- `implementation/pxm/core/{activation-profile,audit,cpu,devices,interrupts,iommu,lifecycle,memory}/`
- `implementation/guard/{attestation,call-abi,roots,tests}/`
- `implementation/guard/roots/{security-root,audit-root,amf-registry,executable-mapping,page-table-policy,svc-table,update-policy}/`
- `implementation/interfaces/{operator-console,command-processor,panel-ui,management-api,posix-subsystem,linux-gateway}/`
- `implementation/tools/{mfctl,policyc,reqck,sourcecard,tracegen,packgen,claimck,manifestck,catalogck,auditdump,jobsubmit}/`
- `implementation/prototypes/hosted-semantic/{first-vertical-slice,services}/`

Verification, release, and evidence scaffolds:

- `tests/{unit,integration,negative,conformance,crash-recovery,fault-injection,supply-chain}/`
- `fuzz/targets/*/`
- `formal/{tla,alloy,coq,isabelle}/`
- `ci/linters/*/` and `ci/scripts/`
- `build/{profiles,toolchains,images,qemu,hardware-lab,reproducible}/`
- `supply-chain/{sbom,provenance,signing,dependencies,releases}/`
- `evidence/{test-results,reviews,traceability,audits,attestations,coverage,production-readiness}/`
- `claims/{baseline,enterprise-standalone,enterprise-pxm,high-assurance}/`

## Audit Conclusions

- Canonical Phase 0.6 documentation is centralized under `docs/design/`.
- The bridge paths mostly document their bridge status clearly.
- The largest audit concern is status ambiguity from comprehensive empty
  scaffolding, especially implementation, tests, fuzz, CI, formal, evidence, and
  supply-chain directories.
- The second largest concern is duplicate source-of-truth drift if future agents
  write normative content into top-level bridge paths before a migration ADR.
- Draft registries and evidence seeds should remain visibly draft until backed
  by executable validation, real artifacts, and release evidence.
