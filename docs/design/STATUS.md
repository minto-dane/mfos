# MFOS Design Work Status

Status date: 2026-04-28
Workspace: `/home/nia/mfos`
Git status: working branch `fix/pre-phase-1-total-readiness-second-pass`;
PR #10 (`fix/phase-0.10-pxm-mfvm-expansion`) and PR #11
(`fix/pre-phase-1-total-readiness`) have landed in `dev`, and this branch is
based on the updated `origin/dev`. Repository visibility may be public by owner
instruction, but formal public-release claims remain blocked pending
IP/trademark attorney review.

## Current Phase

Pre-Phase-1 Total Readiness Remediation after Phase 0.10 PXM / MFVM /
Confidential VM / Datacenter / Formal Assurance Requirements Expansion

Final judgment:

```yaml
phase_0_6_status: complete_with_recorded_gaps
phase_0_7_status: in_progress_registry_coverage_closed
phase_0_7_gap_closure_status: complete_for_machine_checkable_scaffold
naming_safety_refactor_status: complete_for_private_internal_review
phase_0_8_status: complete_for_design_level_core_semantics_freeze
phase_0_9_status: complete_for_executable_spec_artifact_freeze
phase_0_9_7_source_grounding_status: semantic_freeze_conditional
structural_freeze_remains_valid: true
semantic_freeze_fully_valid: false
phase_1_loader_allowed: true
phase_1_dafny_skeleton_allowed: true
phase_1_dafny_semantics_allowed: conditional
phase_1_semantic_evaluator_status: conditional_blocked_pending_domain_gates
phase_1_portable_semantic_core_allowed: false
phase_1_rust_semantic_core_allowed: false
phase_1_semantic_evaluator_allowed_domains: []
phase_1_pxm_mfvm_cvm_cluster_semantic_evaluator_allowed: false
production_implementation_allowed: false
hosted_daemon_implementation_allowed: false
portable_semantic_core_implementation_allowed: false
semantic_runner_implementation_allowed: false
hosted_semantic_prototype_allowed: false
public_release_allowed: false
private_internal_use_allowed: true
requires_ip_attorney_review_before_public_release: true
next_phase: Phase 1 Loader-Only Artifact Loading And Traceability Repair
```

No production nucleus, service, PXM, Guard, or other OS-body implementation was
started in Phase 0.6, Phase 0.7, naming-safety refactor, Phase 0.8, or Phase
0.9.

## Completed In Phase 0.10 PXM/MFVM Requirements Expansion

- Added MFVM as an MFOS-based VM management subsystem, not an independent
  hypervisor root, not a nested hypervisor, and not a compatibility layer.
- Reaffirmed that PXM Core is the trusted hardware-facing partition/resource
  authority and that MFVM is less trusted than PXM.
- Reaffirmed that VMs are PXM-managed VM partitions, not nested guests under
  MFVM.
- Expanded `16-pxm.md` with PXM Core authority, PXM Control API, PXM/MFVM
  separation, VM partition primitives, RAM ownership, IOMMU/interrupt
  remapping, device teardown, CVM primitive authority, audit obligations,
  negative tests, and formal proof obligations.
- Expanded specs `36` through `41` and added `42-mfvm.md` as design-only
  requirements skeletons for hypervisor-class virtualization, Confidential VM,
  datacenter/cluster operations, language verification, automated reasoning,
  performance/secure operations, and MFVM.
- Added public-safe EXTREF source cards for Microsoft Hyper-V, Linux KVM,
  Intel TDX/CET, AMD SEV/SEV-ES/SEV-SNP/SEV-TIO, Kani, Verus, AWS automated
  reasoning, GitHub CodeQL, and NIST references.
- Added Phase 0.10 requirement namespaces for `MFOS-REQ-PXM-*`,
  `MFOS-REQ-MFVM-*`, `MFOS-REQ-VIRT-*`, `MFOS-REQ-CVM-*`,
  `MFOS-REQ-CLUSTER-*`, `MFOS-REQ-PERF-*`, `MFOS-REQ-LANG-*`,
  `MFOS-REQ-FORMAL-*`, and `MFOS-REQ-OPS-*`.
- Added object-model schema skeletons, formal registry entries, pack
  contracts, test catalogs, claims, and validation for the Phase 0.10 planning
  domains.
- Added language/formal-assurance policy, red-team, and open-issues reports
  that keep the work limited to policy/spec/registry planning. Phase 1
  loader-only validation remains allowed; semantic evaluator work is
  conditional and remains blocked until domain gates close.
- Updated naming-safety lint so `TDX`, `SEV`, `SEV-SNP`, `CET`, `CFI`, Kani,
  and Verus may be used as technology/profile names while Hyper-V and KVM
  remain restricted to external-reference or comparison contexts.
- Phase gates remain conservative: Phase 1 loader-only validation remains
  allowed; PXM/MFVM/CVM/cluster semantic evaluators, hosted daemons, semantic
  runner, and production implementation remain blocked.

## Completed In Pre-Phase-1 Total Readiness Remediation

- Split Phase 0.10 work into PR #10, merged it into `dev`, and rebased this
  readiness branch on the updated `origin/dev`.
- Added `docs/design/specs/43-dafny-executable-semantics-policy.md`.
- Added the Phase 1 Dafny scaffold at
  `formal/executable-semantics/dafny/`.
- Wired `scripts/validate-dafny-semantics-scaffold.sh` into
  `scripts/validate-all.sh` and GitHub design validation.
- Repaired component scaffold metadata so Phase 1 targets distinguish
  `rust_semantic_core`, `dafny_executable_semantics`, `semantic_runner`,
  `generated_production_code`, and `validation_only`.
- Updated specs 31, 33, 39, 40, PACKS, and AI/prompt guardrails so Phase 1 is
  Dafny-first and loader-only. Rust semantic-core, semantic runner, hosted
  daemon, hosted semantic prototype, service implementation, PXM/MFVM/CVM
  implementation, cluster implementation, and production generated code remain
  forbidden.
- Closed Major red-team wording findings in implementation scaffold README
  files that previously pointed Phase 1 agents at hosted semantic prototypes.

## Completed In Phase 0.10 Total Remediation

- Added component scaffold metadata validation and `.mfos-dir.yml` records for
  canonical, bridge, validation, test, source, and implementation scaffold
  roots.
- Kept empty implementation, test, fuzz, and CI scaffold directories from
  implying implementation readiness.
- Added deferred draft specs `36` through `41` for virtualization planning,
  confidential workload planning, datacenter/cluster operations, language and
  verification policy, automated reasoning, and performance/secure operations.
- Kept those new specs as design scaffolds only; they do not authorize
  hypervisor, confidential workload, cluster scheduler, semantic runner,
  hosted daemon, service, or production implementation.
- Reaffirmed that `docs/design/source-matrix/cards/` is the canonical Source
  Card path and that `sources/` remains a public-safe workbench until an
  ADR-backed migration.
- Reaffirmed that source cards remain draft and semantic freeze remains
  conditional; Phase 1 remains loader-only.
- Updated repository remediation reports and indexes under `reports/current/`.

## Completed In Phase 0.9.9

- Closed artifact-hygiene validator gaps for Phase 1+ filenames, check-mode
  mutation, planned empty parser-target directories, and script/task indexes.
- Moved the Phase 1 pack-readiness recheck out of `reports/current/` and into
  `reports/phases/phase-1/`.
- Synchronized pack failure-mode and fuzz-target IDs with the current Phase 0.9
  fuzz target plan and policy-denial taxonomy.
- Added public-safe workbench cards for the remaining canonical Source Matrix
  IDs that lacked `sources/` candidates.
- Added `sources/source-matrix-parity.yml` and populated retrieval metadata for
  the new workbench source cards.
- Kept `sources/` noncanonical; `docs/design/source-matrix/` remains the
  source authority until an ADR-backed migration.
- Confirmed `./scripts/validate-all.sh --check` does not mutate the generated
  registry-link audit report.

## Completed In Phase 0.6

- Audited current repository structure and canonical-path posture.
- Preserved `docs/design` as the current canonical design area.
- Added ADR proposal for canonical paths and the `implementation/` grouping.
- Added JSON Schemas for Source Cards, requirements, claims, test cases,
  evidence records, pack contracts, and spec front matter.
- Added compact Phase 0.6 YAML front matter to all split specs under
  `docs/design/specs/*.md`.
- Added local validation scripts and `./scripts/validate-all.sh`.
- Added source-grounding, prohibited wording, no-fake-success, audit
  obligation, SPEC_GAP/UNSUPPORTED misuse, pack, claim, and spec-front-matter
  checks.
- Added generated traceability matrices under `evidence/traceability/`.
- Added pack contracts under `packs/pack-index.yml`; every pack keeps
  `implementation_allowed.production: false`.
- Added an assurance claim tree under `docs/design/assurance/claim-tree.yml`.
- Added Japanese mirror tracking seeds under `docs/design/ja/`.
- Added AI pre-implementation gate text to `docs/design/packs/PACKS.md`,
  `docs/design/specs/28-machine-readable-registries.md`, and
  `ai/contracts/ai-implementation-contract.md`.
- Added Phase 0.7 task plan:
  `tasks/archive/phase-0-7/system-integrity-deep-spec.yml`.

## Corrections Preserved

- `MFOS-REQ-CATALOG-0002` remains a `MUST`: catalogd resolves only committed
  catalog entries.
- Baseline requires an NX-capable platform and W^X policy.
- Enterprise remains split into `Enterprise-Standalone` and `Enterprise-PXM`.
- Early AMF implementation remains disabled by default and returns
  `MFOS_ERR_UNSUPPORTED`.
- `SecurityDecision`, `PolicyBinding`, and `ObjectGenerationBinding` remain in
  the design base.
- Policy lint and semantic misuse are first-class design controls.
- Assurance is represented as claim trees with assumptions and non-claims.
- English is canonical; Japanese is explanatory unless explicitly synchronized.

## Red Team Follow-Up Completed

- Fixed malformed profile tables in audit, Guard, Linux gateway, hardware
  profile, and attestation specs.
- Normalized split-spec front matter so body Source Matrix IDs are reflected in
  `source_refs`.
- Hardened local lint to detect Source Matrix front-matter drift and Markdown
  table width mismatches.
- Reworded root project language earlier in the pass to avoid implying IBM
  approval, affiliation, sponsorship, endorsement, or official MFOS status.
- Removed WLM from MFOS-owned namespaces in the current design base:
  workload policy uses `workload-policy`, `workpolicyd`, and `WPOL` owned
  identifiers; `EXTREF-IBM-ZOS-WLM-*` remains external reference ID space only.
- Closed the Phase 0.8 residual minor findings for authorization model
  reachability, inactive future prompt gating, MFOS-native job-control stream
  identifiers, and the SpoolEntry evidence boundary.

## Completed In Current Phase 0.7 Pass

- Tightened `docs/design/specs/03-system-integrity.md` boot failure rules so
  auditd start failure enters operator recovery mode only, with normal job,
  dataset, policy update, AMF, update activation, partition device assignment,
  and destructive operator operations blocked.
- Reworked the AMF-disabled positive path so Phase 1 AMF load returns
  `MFOS_ERR_UNSUPPORTED`, creates no executable mapping, creates no registry
  entry, and performs no authorized-state transition.
- Expanded the priority requirements registry from 21 to 40 entries by adding
  `MFOS-REQ-SYSINT-0002` through `MFOS-REQ-SYSINT-0020`.
- Expanded the test registry from 5 to 33 draft tests, covering system
  interface registration, SVC/PCALL pointer misuse, AMF/admin confusion,
  unsupported/spec-gap success attempts, audit substitution, dataset handle
  binding, operator command confirmation, PXM semantic misuse, Guard scope
  refusal, and hardware overclaim.
- Expanded the evidence registry from 3 to 33 draft evidence records. These
  are traceability placeholders, not verified proof artifacts.
- Updated the High-Assurance Guard claim to use registered system-integrity
  requirements, tests, and evidence placeholders instead of unregistered Guard
  requirement IDs.
- Reserved the source-mapped but not yet deeply specified requirement IDs as
  `spec_gap_reserved` entries. This closed the source-card-to-requirement
  registry coverage gap without adding operational semantics.
- Registered draft test and evidence placeholders for the reserved requirement
  IDs. These records preserve traceability only; they do not authorize
  implementation.
- Registered the remaining planned test and evidence IDs referenced by
  requirements and claims. This closed cross-registry link warnings without
  claiming verified evidence.
- Cleaned the remaining SPEC_GAP/UNSUPPORTED success-path wording warnings.
- Added source-card pin metadata fields and recorded the remaining cards that
  still need human/source review.
- Added Japanese mirror tracking metadata and recorded the mirror as incomplete
  without changing canonical English semantics.
- Added draft evidence status enforcement to local validation and CI workflow
  wiring for design validation.
- Regenerated traceability matrices; `gap-report.yml` now reports zero gap
  groups.
- Strengthened `docs/design/specs/03-system-integrity.md` across Purpose,
  system interface boundary rules, prohibited circumventions, failure modes,
  formal invariants, registry-backed tests, and spec-gap handling.
- Added line-local source-grounding enforcement for opt-in specs and enabled it
  for `03-system-integrity.md`.
- Added a read-only `./scripts/validate-all.sh --check` mode that skips
  traceability regeneration.

## Completed In Naming-Safety Refactor

- Migrated IBM-derived canonical Source IDs from legacy `IBM-*` IDs to
  `EXTREF-IBM-*` IDs.
- Preserved old source IDs only as `legacy_source_ids` aliases and in
  `reports/naming-safety/naming-alias-map.yml`.
- Renamed IBM-derived Source Card filenames to match the new `EXTREF-*`
  canonical IDs.
- Converted Source Cards from concept-summary cards to public-safe
  bibliographic reference cards with `review_topics`, `legal_controls`,
  `mfos_divergence`, and `prohibited_inference`.
- Migrated requirement, test, evidence, and claim IDs to safer MFOS-owned
  namespaces while preserving old IDs in `legacy_*` alias fields.
- Added naming-safety lint scripts:
  `check-mf-owned-names.py`, `check-extref-namespace.py`,
  `check-no-compatibility-claims.py`, `check-source-card-public-safe.py`,
  `check-requirement-namespace.py`, and `check-no-copied-external-docs.py`.
- Added `./scripts/validate-naming-safety.sh` and wired it into
  `./scripts/validate-all.sh`.
- Updated `NOTICE.md`, `README.md`, `docs/design/mfos-design.md`, and
  `docs/design/legal-risk-policy.md` with independent-project,
  non-affiliation, non-endorsement, and non-compatibility language.
- Renamed MFOS-owned implementation scaffold paths from external-interface
  wording to neutral project names:
  `command-processor`, `panel-ui`, `management-api`, `commandd`, and `paneld`.
- Hardened naming-safety validators to scan empty directories, release-bound
  reports, stale Source Card guidance, and canonical IBM-style source IDs.
- Added generic external-name notice language and aligned non-IBM external
  Source Cards to reference-only mark controls.
- Migrated legacy source IDs in non-naming reports to current `EXTREF-*`
  identifiers.

## Completed In Phase 0.8 Core Semantics Freeze

- Froze PACK-05 through PACK-09 at design level only:
  authorization, audit, dataset/catalog, job/spool, and operator console.
- Updated core specs:
  `docs/design/specs/06-authorization.md`,
  `docs/design/specs/07-audit.md`,
  `docs/design/specs/08-dataset-catalog.md`,
  `docs/design/specs/09-job-spool.md`, and
  `docs/design/specs/10-operator-console.md`.
- Added the first vertical slice semantic contract:
  `docs/design/specs/30-first-vertical-slice-contract.md`.
- Added or updated MFOS schemas for `SecurityDecision`, `PolicyBinding`,
  `ObjectGenerationBinding`, `AuditRecord`, dataset/catalog handles, job/spool
  records, and operator commands.
- Added Phase 0.8 design-level state machines and formal artifacts under
  `formal/tla/authorization`, `formal/tla/audit-append`,
  `formal/tla/dataset-open`, `formal/tla/catalog-transaction`,
  `formal/tla/job-lifecycle`, `formal/tla/spool-access`, and
  `formal/tla/operator-command`.
- Added Phase 0.8 planned test catalogs under `tests/catalog/` and a fuzz target
  plan under `fuzz/targets/archive/phase-0-8/fuzz-target-plan.yml`.
- Added Phase 0.8 traceability matrices under `evidence/traceability/`.
- Updated PACK-05 through PACK-09 machine-readable pack contracts with
  `implementation_allowed.production: false`,
  `implementation_allowed.hosted_daemon: false`,
  `implementation_allowed.portable_semantic_core: false`,
  `implementation_allowed.executable_spec: false`, and
  `implementation_allowed.specification_only: true`.
- Added `scripts/phases/phase-0-8/check-traceability.py` and wired it into
  `./scripts/validate-all.sh`.
- Closed red-team Critical/Major issues by materializing `010x` planned semantic tests,
  removing hosted-prototype readiness language, aligning emergency duration and
  break-glass result naming, registering `MFOS_RESOURCE_SYSTEM` and
  `MFOS_RESOURCE_SERVICE`, aligning operator DSN parsing with the dataset/catalog
  grammar, expanding policy lint coverage, aligning pack source refs, and
  classifying first-vertical-slice conflicts as implementation-blocking gaps.
- Confirmed no production implementation, hosted daemon implementation, portable
  semantic core implementation, nucleus, PXM, Guard, or service logic was
  started.

## Completed In Phase 0.9 Executable Specs / Test Harness Freeze

- Added Phase 0.9 executable-spec specs:
  `31-executable-spec-test-harness.md`,
  `32-conformance-fixture-format.md`,
  `33-semantic-runner-contract.md`,
  `34-oracle-definition-format.md`, and
  `35-fuzz-corpus-plan.md`.
- Added Phase 0.9 schemas for test cases, fixtures, oracles, expected audit
  records, expected state transitions, expected failures, and conformance
  suites.
- Added 154 Phase 0.9 test catalog entries across authorization, audit,
  dataset/catalog, job/spool, operator console, first vertical slice, negative
  tests, failure modes, and conformance index catalogs.
- Added 74 deterministic fixtures and 74 golden vectors with embedded oracles.
- Added Phase 0.9 fuzz corpus planning for dataset names, job-control streams,
  operator commands, policy language, audit records, dataset handles, job
  fixtures, spool fixtures, and semantic fixtures.
- Added Phase 0.9 validation scripts and wired
  `./scripts/phases/phase-0-9/validate.sh` into `./scripts/validate-all.sh`.
- Generated Phase 0.9 traceability matrices under `evidence/traceability/`.
- Added Phase 0.9 freeze, validation, gap, red-team, open-issue, and Phase 1
  readiness reports.
- Confirmed no production implementation, hosted daemon implementation,
  Portable Semantic Core implementation, semantic evaluator implementation, or
  semantic runner implementation was started in Phase 0.9.

## Validation Commands

```bash
python3 scripts/validators/validate-source-cards.py
python3 scripts/validators/validate-requirements.py
python3 scripts/validators/validate-claims.py
python3 scripts/validators/validate-spec-front-matter.py
python3 scripts/validators/validate-packs.py
python3 scripts/checks/check-prohibited-terms.py
python3 scripts/checks/check-no-fake-success.py
python3 scripts/checks/check-source-grounding.py
python3 scripts/checks/check-audit-obligations.py
python3 scripts/checks/check-spec-gap-misuse.py
python3 scripts/phases/phase-0-8/check-traceability.py --mode release
./scripts/phases/phase-0-9/validate.sh
python3 scripts/generators/generate-traceability.py
./scripts/validate-all.sh
python3 -m py_compile $(find scripts -name '*.py' -print)
python3 scripts/checks/check-evidence-status.py --mode release
python3 scripts/checks/check-source-grounding.py --mode release
./scripts/validate-naming-safety.sh release
./scripts/validate-artifact-hygiene.sh
```

## Current Validation Results

`./scripts/validate-all.sh --check` passes in draft mode without regenerating
traceability.

Observed draft warnings: none.

`python3 scripts/checks/check-evidence-status.py --mode release` fails closed as
expected with 18 errors and 20 warnings because release claims require
verified or archived evidence with review metadata.

`python3 scripts/checks/check-source-grounding.py --mode release` passes with 0
warnings for current opt-in statement-level grounding.

`python3 scripts/phases/phase-0-8/check-traceability.py --mode release` passes.

`./scripts/phases/phase-0-9/validate.sh` passes and generates Phase 0.9 traceability.

`./scripts/validate-naming-safety.sh release` passes with 0 warnings.

`python3 -m py_compile $(find scripts -name '*.py' -print)` passed. YAML and
JSON parse checks passed.

Current registry counts:

```yaml
requirements: 130
tests: 309
evidence: 194
source_cards: 37
claims: 5
packs: 31
traceability_gap_groups: 0
high_traceability_gap_groups: 0
spec_gap_unsupported_warnings: 0
registry_link_warnings: 0
draft_evidence_warnings: 0
source_grounding_release_warnings: 0
release_evidence_errors: 18
release_evidence_warnings: 20
naming_safety_release_warnings: 0
extref_ibm_source_cards: 23
phase_0_9_test_catalog_entries: 154
phase_0_9_fixtures: 74
phase_0_9_golden_vectors: 74
phase_0_9_fuzz_targets: 9
```

## PR #5 Review Closure

Status: reviewed for merge readiness on 2026-04-28.

- Phase 0.9 artifacts remain executable-spec artifacts only.
- No production implementation, hosted daemon, Portable Semantic Core,
  semantic evaluator, semantic runner, service logic, nucleus, PXM, or Guard
  implementation was added.
- Policy-denial error mapping is resolved for Phase 1 executable-spec inputs:
  no valid subject is `MFOS_ERR_UNAUTHENTICATED`; a valid subject denied by
  policy is `MFOS_ERR_POLICY_DENIED`; `MFOS_ERR_UNAUTHORIZED` is legacy umbrella
  wording and is not a primary Phase 1 policy-denial result.
- The BOB denied first-vertical-slice path now expects
  `MFOS_ERR_POLICY_DENIED` with audit `reason_code:
  DATASET_READ_NOT_PERMITTED`.
- First-vertical-slice fixtures and golden vectors are under the explicit
  `tests/fixtures/first-vertical-slice/` and
  `tests/golden/first-vertical-slice/` paths.
- PR #5 review findings: no Critical or Major findings remain.

## Remaining Gaps

- Evidence registry entries are draft placeholders and must not be treated as
  verified proof.
- Source Cards still need exact publication, section, and version pins where
  local metadata cannot verify them.
- `spec_gap_reserved` requirements close registry coverage, but they are not
  implementation-ready requirements. Deep specs, final tests, evidence, and
  red-team review are still required before any implementation packet can use
  them.
- Source-card pin limits, reserved requirements, draft-only evidence, and
  populated noncanonical `sources/` workbench drift still block production,
  release, Portable Semantic Core behavior, semantic evaluator, and semantic
  runner claims. They do not block Phase 1 loader-only validation of the Phase
  0.9 executable-spec artifact set.
- Release-mode evidence checking intentionally blocks claims until verified
  evidence artifacts, digests, verifiers, and verification timestamps exist.
- CI design validation is wired, but release-mode evidence gates still require
  future verified evidence archive work.
- Japanese mirror mechanics are incomplete; `japanese_mirror_status` remains
  incomplete and nonblocking while English remains canonical.
- Public release remains blocked pending human legal/IP review. Naming-safety
  now includes a `sources/` workbench public-safety check and must continue to
  pass before any public release discussion.
- The first vertical slice now has Phase 0.9 fixtures and golden vectors. The
  user-facing policy-denial error mapping is resolved for Phase 1 as
  `MFOS_ERR_POLICY_DENIED` with audit `reason_code:
  DATASET_READ_NOT_PERMITTED`.
- Phase 0.9 does not provide verified execution evidence; it provides
  executable-spec artifacts that may be loaded and validated, but semantic
  evaluator implementation remains blocked until Phase 0.9.7 source-grounding
  gaps are closed.

## Completed In Phase 0.9.7 Source Grounding Adequacy Audit

- Audited the 37 canonical Source Cards under
  `docs/design/source-matrix/cards/`.
- Confirmed Source Cards are public-safe and do not contain copied external
  documentation fields, record layouts, command syntax, or macro signatures.
- Confirmed no Source Card reaches SG6/SG7 because all remain draft and direct
  card-local spec/test links are missing.
- Rechecked PACK-05 through PACK-09 for loader-only versus semantic evaluator
  readiness.
- Downgraded Phase 1 permission to loader-only artifact validation and
  traceability repair.
- Blocked Portable Semantic Core behavior, semantic evaluator, and semantic
  runner command implementation until source-grounding trace gaps close.
- Recorded conditional refreeze outputs under
  `reports/current/source-grounding/`.

## Completed In Phase 0.9.8 Source Workbench Population

- Populated `sources/` as a public-safe, noncanonical source-grounding
  workbench with IBM, x64, security-assurance, and internal FBVBS source cards,
  concept cards, indexes, and mapping notes.
- Kept `docs/design/source-matrix/source-matrix.yml` and
  `docs/design/source-matrix/cards/` as canonical source authority until an
  ADR-backed migration updates validators, traceability, packs, docs, and
  indexes together.
- Did not commit IBM PDFs, HTML mirrors, screenshots, copied manuals, record
  layouts, command syntax, macro signatures, message catalogs, or external
  source-substitute material.
- Added `sources/` workbench public-safety validation to naming-safety checks.
- Confirmed source population improves review depth but does not upgrade
  semantic freeze from conditional to full.

## Reports

Reports are indexed in `reports/index.yml`. The root `reports/` directory now
contains only index/policy files and categorized report families.

Artifact inventories are maintained in:

- `reports/index.yml`
- `tests/catalog/index.yml`
- `tests/fixtures/index.yml`
- `tests/golden/index.yml`
- `evidence/traceability/index.yml`
- `scripts/index.yml`
- `fuzz/targets/index.yml`
- `tasks/index.yml`
- `docs/design/tasks/index.yml`
- `docs/design/specs/INDEX.md`
- `docs/design/packs/PACKS.md`

Current PR and readiness reports:

- `reports/phases/phase-0-9/pr-5-review-report.md`
- `reports/phases/phase-0-9/pr-5-post-gap-validation.md`
- `reports/current/policy-denial-error-taxonomy.md`
- `reports/phases/phase-1/readiness-report.md`
- `reports/phases/phase-1/open-issues.md`
- `reports/current/source-grounding/conditional-refreeze-plan.md`
- `reports/phases/phase-1/pack-readiness-recheck.md`
- `reports/current/pre-phase1-readiness-audit.md`
- `reports/current/pre-phase1-readiness-red-team-review.md`
- `reports/current/pre-phase1-readiness-final-report.md`
- `reports/phases/phase-1/pre-phase-1-total-readiness.md`

Historical phase reports are under `reports/phases/`. Cross-phase audits are
under `reports/audits/`. Naming-safety reports are under
`reports/naming-safety/`. Deterministic script outputs are under
`reports/generated/`. Superseded reports are retained under
`reports/archive/`.

## Next Recommended Work

After the pre-Phase-1 readiness PR passes required checks and lands in `dev`,
proceed only to Phase 1 Dafny executable-semantics scaffold and loader-only
artifact validation.

Allowed Phase 1 scope:

1. Create reviewed Dafny source artifacts under
   `formal/executable-semantics/dafny/`.
2. Validate Dafny artifact metadata, dependencies, requirement refs, source
   refs, and declared proof status.
3. Repair traceability metadata for executable-spec artifacts.

Forbidden Phase 1 scope remains:

1. Rust semantic-core or Portable Semantic Core implementation.
2. Semantic-runner implementation or semantic-runner commands.
3. Hosted daemon or hosted semantic prototype implementation.
4. Securityd/auditd/catalogd/datasetd/jobd/spoold/operatord implementation.
5. PXM/MFVM/CVM/cluster implementation.
6. Production code or Dafny-generated production code.
