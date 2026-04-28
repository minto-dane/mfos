# MFOS Split Spec Front Matter Migration Plan v0.1

Status: design draft

This plan describes how to apply
`docs/design/specs/27-spec-front-matter.md` to existing MFOS split specs in a
controlled way.

MFOS is z/OS-inspired. This migration must not introduce z/OS compatibility
claims or compatibility claims with IBM subsystems.

## Purpose

The purpose of this migration is to add common YAML-like front matter and
section-schema alignment to existing split specs without overwriting parallel
work. The migration should improve traceability across source IDs,
requirements, tests, evidence, reviewers, owned files, lint rules, and open
gaps.

This plan does not modify existing specs. It defines the later work order.

## Scope

The migration applies to existing files under:

```text
docs/design/specs/
```

It covers:

- front matter insertion,
- section-schema alignment,
- source ID declaration,
- requirement namespace declaration,
- owned file declaration,
- profile applicability declaration,
- threat model and audit obligation references,
- test, fuzz, and evidence placeholders,
- reviewer routing,
- lint rule declaration,
- gap registration.

## Non-objectives

This plan does not:

- retrofit any existing spec in this task,
- implement lint tooling,
- rewrite source matrix entries,
- finalize requirement, test, fuzz, or evidence registries,
- make production or conformance claims,
- claim z/OS compatibility.

## Migration Principles

1. Preserve existing content.
2. Add front matter before changing body structure.
3. Prefer explicit gaps over invented metadata.
4. Use requirement namespace wildcards in draft where concrete IDs are pending.
5. Do not change another agent's active file without ownership.
6. Keep edits one spec file at a time.
7. Run lint in draft mode before review mode.
8. Do not mark a spec `ready` until source IDs, gaps, reviewers, and lint rules
   are explicit.

## Target Spec Files

The current split spec set is:

```text
docs/design/specs/00-normative-language.md
docs/design/specs/01-glossary.md
docs/design/specs/02-source-matrix.md
docs/design/specs/03-system-integrity.md
docs/design/specs/04-threat-model.md
docs/design/specs/05-object-model.md
docs/design/specs/06-authorization.md
docs/design/specs/07-audit.md
docs/design/specs/08-dataset-catalog.md
docs/design/specs/09-job-spool.md
docs/design/specs/10-operator-console.md
docs/design/specs/11-workload-policy.md
docs/design/specs/12-amf.md
docs/design/specs/13-update.md
docs/design/specs/14-nucleus.md
docs/design/specs/15-svc-pcall.md
docs/design/specs/16-pxm.md
docs/design/specs/17-guard.md
docs/design/specs/18-linux-gateway.md
docs/design/specs/19-assurance-case.md
docs/design/specs/20-conformance.md
docs/design/specs/21-ai-implementation-contract.md
docs/design/specs/22-production-readiness.md
docs/design/specs/23-requirements-catalog.md
docs/design/specs/24-formal-methods.md
docs/design/specs/25-operations-recovery.md
docs/design/specs/26-hardware-profile.md
docs/design/specs/27-spec-front-matter.md
docs/design/specs/INDEX.md
```

`27-spec-front-matter.md` is the schema source and should not be migrated into
itself beyond its existing schema content. `INDEX.md` should be updated only
after individual spec front matter is stable.

## Phases

### Phase 0: Freeze Schema Inputs

Goal:
  Confirm the schema and lint expectations before touching existing specs.

Inputs:

- `docs/design/specs/27-spec-front-matter.md`
- `docs/design/source-matrix/source-matrix.yml`
- `docs/design/source-matrix/source-lint-spec.md`
- `docs/design/source-matrix/traceability-index.md`
- `docs/design/source-matrix/traceability-policy.md`

Tasks:

- Confirm required front matter fields.
- Confirm status values.
- Confirm profile applicability values.
- Confirm minimum lint rules.
- Confirm current Source Matrix IDs.
- Record gaps for missing registries.

Exit criteria:

- No schema changes are pending.
- Migration checklist is agreed.
- Ownership rules are restated for each migration batch.

### Phase 1: Low-Risk Governance Specs

Goal:
  Apply front matter to specs that define process and policy before component
  behavior.

Order:

1. `00-normative-language.md`
2. `01-glossary.md`
3. `02-source-matrix.md`
4. `21-ai-implementation-contract.md`
5. `23-requirements-catalog.md`
6. `20-conformance.md`
7. `22-production-readiness.md`

Rationale:
  These specs establish vocabulary, requirement discipline, AI constraints, and
  release gates. They are lower risk than changing component semantics and will
  provide examples for later batches.

Exit criteria:

- Each file has valid front matter.
- Source IDs and requirement namespaces are explicit.
- Compatibility statement is present.
- Gaps list unresolved registries and lint tooling.

### Phase 2: Core Semantic Specs

Goal:
  Apply front matter to specs that define MFOS enterprise semantics.

Order:

1. `03-system-integrity.md`
2. `05-object-model.md`
3. `06-authorization.md`
4. `07-audit.md`
5. `08-dataset-catalog.md`
6. `09-job-spool.md`
7. `10-operator-console.md`
8. `11-workload-policy.md`

Rationale:
  These specs define the main MFOS object and service model. System integrity,
  authorization, and audit come before dataset/job/operator specs because those
  specs depend on securityd and auditd obligations.

Exit criteria:

- Protected-resource specs list audit obligations.
- Security-sensitive specs list negative tests.
- Parser-bearing specs list fuzz targets or gaps.
- Requirement namespaces are routed through the traceability index.

### Phase 3: Execution, Update, and Platform Specs

Goal:
  Apply front matter to execution and platform-facing specs after the semantic
  core is routed.

Order:

1. `12-amf.md`
2. `13-update.md`
3. `14-nucleus.md`
4. `15-svc-pcall.md`
5. `26-hardware-profile.md`

Rationale:
  AMF, update, nucleus, SVC/PCALL, and hardware profile specs have strong
  safety and source-grounding needs. They should follow semantic-core metadata
  so they can reference established security, audit, and failure-mode fields.

Exit criteria:

- `UNSUPPORTED` and `SPEC_GAP` are distinct.
- AMF and SVC/PCALL list zACS-style negative tests.
- Hardware claims are tied to x64 source IDs and do not overclaim PKU, PKS, or
  CET.
- Update specs list rollback, freeze, mix-and-match, and provenance evidence.

### Phase 4: Partition, Guard, Gateway, Operations, and Assurance

Goal:
  Apply front matter to specs with profile-specific behavior and broad evidence
  needs.

Order:

1. `16-pxm.md`
2. `17-guard.md`
3. `18-linux-gateway.md`
4. `25-operations-recovery.md`
5. `04-threat-model.md`
6. `19-assurance-case.md`
7. `24-formal-methods.md`

Rationale:
  PXM and Guard have strict scope boundaries. Gateway, operations, assurance,
  and formal-method specs depend on earlier requirement routing and evidence
  classes.

Exit criteria:

- PXM front matter states that PXM does not own MFOS enterprise semantics.
- Guard front matter states High-Assurance applicability and root-object scope.
- Gateway front matter lists audit and authorization obligations.
- Assurance and formal-method specs list evidence and proof-boundary gaps.

### Phase 5: Index and Cross-Reference Cleanup

Goal:
  Update indexes and cross-reference tables after all individual specs have
  stable front matter.

Files to update later:

```text
docs/design/specs/INDEX.md
docs/design/source-matrix/traceability-index.md
docs/design/source-matrix/traceability-policy.md
docs/design/source-matrix/source-lint-spec.md
```

Exit criteria:

- `INDEX.md` lists document IDs and statuses.
- Traceability index references front matter document IDs.
- Lint spec reflects any final front matter rule changes.
- No stale namespace routing remains.

## Conflict Avoidance

Before editing any spec in a later migration task:

1. Read the target file.
2. Check whether another agent has recently changed it.
3. Confirm task ownership covers that file.
4. Edit only the assigned file or batch.
5. Add front matter without rewriting body content unless explicitly assigned.
6. If body sections need reordering, record the need in `gaps` instead of
   performing a broad rewrite during front matter insertion.
7. Do not normalize formatting across unrelated sections.
8. Do not remove existing content unless it is duplicated metadata and the task
   explicitly allows cleanup.

If a conflict is found:

- stop editing that file,
- preserve any completed independent files,
- record the conflict in the migration task notes,
- let the next owner decide whether to merge manually.

## Lint Gates

### Draft Gate

Must pass before considering a migrated spec complete for draft use:

- front matter exists,
- required fields are present,
- document ID is unique,
- status is `draft` or `review`,
- source IDs are known or listed as gaps,
- compatibility statement is present,
- owned files include the migrated spec,
- gaps list unresolved metadata.

### Review Gate

Must pass before architecture or security review:

- source IDs exist in `source-matrix.yml`,
- IBM-derived terms have concept mapping sections,
- requirement namespaces are declared,
- protected-resource specs list audit obligations,
- security-sensitive specs list negative tests,
- parser specs list fuzz targets or a gap,
- lint rules list required and release-blocking checks,
- reviewers are assigned by role.

### Release Gate

Must pass before a conformance or production claim:

- namespace wildcards are resolved to concrete requirement IDs,
- test IDs are concrete,
- evidence artifact IDs are concrete,
- release-blocking gaps are closed or have approved waivers,
- forbidden wording scan is clean,
- source freshness status is acceptable,
- no `UNSUPPORTED` or `SPEC_GAP` path is treated as success.

## Review Checklist

For each migrated spec:

- Front matter starts at the top of the file.
- `schema_version` is `1`.
- `document_id` is stable and unique.
- `status` reflects actual maturity.
- `last_updated` is current for the migration patch.
- `owners` and `reviewers` are populated.
- `source_ids` match source-grounded concepts in the spec.
- IBM-derived concepts have allowed and prohibited wording.
- `requirement_namespaces.defines` and `uses` are accurate.
- `owned_files` does not claim unrelated files.
- `profiles` separates Baseline, Enterprise-Standalone, Enterprise-PXM, and High-Assurance.
- `threat_models` links existing sections or records a gap.
- `audit_obligations` are present for protected-resource behavior.
- `tests.negative` exists for security-sensitive behavior.
- `fuzz_targets` exists for parsers or has a gap.
- `evidence_artifacts` uses planned classes or concrete IDs.
- `lint_rules` includes minimum required and release-blocking rules.
- `gaps` are actionable.
- No z/OS compatibility claim appears.

## Rollback Plan

The rollback unit is one spec file.

If a migration patch causes confusion or fails review:

1. Revert only the front matter added to the affected spec.
2. Do not revert unrelated body changes made by other agents.
3. Preserve any migration notes in this task file or a follow-up task.
4. Re-run draft lint for the affected file after rollback.
5. Reattempt migration with a smaller patch that only adds required metadata.

If a batch migration causes repeated conflicts:

- pause the batch,
- split the remaining files into one-file tasks,
- assign explicit ownership per file,
- update this plan with the conflict pattern.

## Files To Update Later

The following files should be updated by later tasks, not by this task:

```text
docs/design/specs/00-normative-language.md
docs/design/specs/01-glossary.md
docs/design/specs/02-source-matrix.md
docs/design/specs/03-system-integrity.md
docs/design/specs/04-threat-model.md
docs/design/specs/05-object-model.md
docs/design/specs/06-authorization.md
docs/design/specs/07-audit.md
docs/design/specs/08-dataset-catalog.md
docs/design/specs/09-job-spool.md
docs/design/specs/10-operator-console.md
docs/design/specs/11-workload-policy.md
docs/design/specs/12-amf.md
docs/design/specs/13-update.md
docs/design/specs/14-nucleus.md
docs/design/specs/15-svc-pcall.md
docs/design/specs/16-pxm.md
docs/design/specs/17-guard.md
docs/design/specs/18-linux-gateway.md
docs/design/specs/19-assurance-case.md
docs/design/specs/20-conformance.md
docs/design/specs/21-ai-implementation-contract.md
docs/design/specs/22-production-readiness.md
docs/design/specs/23-requirements-catalog.md
docs/design/specs/24-formal-methods.md
docs/design/specs/25-operations-recovery.md
docs/design/specs/26-hardware-profile.md
docs/design/specs/INDEX.md
docs/design/source-matrix/traceability-index.md
docs/design/source-matrix/traceability-policy.md
docs/design/source-matrix/source-lint-spec.md
```

## Open Gaps

- No automated front matter linter exists yet.
- Canonical document IDs for existing specs are not assigned.
- Requirement, audit obligation, test, fuzz target, and evidence registries are
  still pending.
- Existing specs may already contain informal metadata that needs manual merge.
- Source freshness metadata is not yet available in `source-matrix.yml`.
- Waiver storage and approval workflow are not defined.
- No release-mode CI entry point exists for front matter validation.
