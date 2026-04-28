---
spec_id: "MFOS-SPEC-27-SPEC-FRONT-MATTER"
title: "MFOS Split Spec Front Matter and Section Schema v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001"]
requirement_refs: []
claim_refs: []
test_refs: ["FUZZ-AREA-PARSER-*", "TEST-AREA-CONF-*", "TEST-AREA-CRASH-*", "TEST-AREA-FAULT-*", "TEST-AREA-NEG-*", "TEST-AREA-PARSER-*", "TEST-AREA-POS-*", "TEST-AREA-STATE-*"]
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Split Spec Front Matter and Section Schema v0.1

Status: design draft

This document defines the common front matter and section schema for all MFOS
split specifications.

MFOS is z/OS-inspired. Split specs must not claim z/OS compatibility or
compatibility with IBM subsystems.

## Purpose

MFOS split specs are intended to be read and updated by humans and AI agents
working in parallel. Common front matter gives every agent the same answer to
these questions:

- what the spec owns,
- which source IDs ground it,
- which requirement namespaces it defines or uses,
- which profiles it affects,
- which threat models, audit obligations, tests, fuzz targets, and evidence
  records apply,
- which gaps remain,
- which lint rules must pass before review or release.

This document defines the required metadata shape and the required section
layout. It does not retrofit existing split specs.

## Scope

This schema applies to future revisions of split specs under:

```text
docs/design/specs/
```

It also applies to newly created split specs, component specs, and source-
grounded design packs that are intended to become normative MFOS design
material.

## Non-objectives

This schema does not:

- implement any lint tooling,
- rewrite existing split spec files,
- replace source matrix entries,
- replace requirement catalogs,
- replace test or evidence registries,
- permit compatibility claims,
- permit source-less z/OS-inspired concepts.

## Front Matter Delimiters

Every split spec should begin with a YAML-like metadata block delimited by
triple dashes:

```yaml
---
schema_version: 1
document_id: MFOS-SPEC-AREA-NNNN
title: "MFOS <Area> Specification"
status: draft
revision: "0.1"
last_updated: YYYY-MM-DD
owners:
  - team-or-agent-id
reviewers:
  required:
    - architecture
    - security
  optional:
    - assurance
source_ids:
  - EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
requirement_namespaces:
  defines:
    - MFOS-REQ-AREA-*
  uses:
    - MFOS-REQ-SOURCE-*
owned_files:
  - docs/design/specs/NN-area.md
related_files:
  - docs/design/source-matrix/source-matrix.yml
profiles:
  baseline: required
  enterprise: required
  high_assurance: conditional
threat_models:
  - docs/design/specs/04-threat-model.md#area
audit_obligations:
  - AUD-AREA-0001
tests:
  positive:
    - TEST-AREA-POS-0001
  negative:
    - TEST-AREA-NEG-0001
  conformance:
    - TEST-AREA-CONF-0001
fuzz_targets:
  - FUZZ-AREA-PARSER-0001
evidence_artifacts:
  - EVID-AREA-CI-YYYYMMDD-NNNN
lint_rules:
  required:
    - SRC-LINT-REF-0001
    - SRC-LINT-REQ-0003
  release_blocking:
    - SRC-CI-FORBIDDEN-WORDING
gaps:
  - GAP-AREA-0001
---
```

The block is YAML-like because early design files may be reviewed manually. A
future lint implementation should parse it as strict YAML.

## Required Front Matter Fields

| Field | Type | Required | Rule |
| --- | --- | --- | --- |
| `schema_version` | integer | yes | Must be `1` for this schema. |
| `document_id` | string | yes | Stable spec ID matching `MFOS-SPEC-[A-Z0-9]+-[0-9]{4}` or approved legacy form. |
| `title` | string | yes | Human-readable title. |
| `status` | enum | yes | One of `draft`, `review`, `ready`, `deprecated`, `superseded`. |
| `revision` | string | yes | Document revision, normally `"0.1"` while draft. |
| `last_updated` | date | yes | ISO date in `YYYY-MM-DD` form. |
| `owners` | list[string] | yes | Responsible maintainers or agents. |
| `reviewers` | mapping | yes | Required and optional review roles. |
| `source_ids` | list[string] | yes | Source Matrix IDs from `source-matrix.yml`. |
| `requirement_namespaces` | mapping | yes | Requirement namespaces defined and used by the spec. |
| `owned_files` | list[string] | yes | Files this spec owns or is allowed to update. |
| `related_files` | list[string] | yes | Non-owned references used by the spec. |
| `profiles` | mapping | yes | Baseline, Enterprise-Standalone, Enterprise-PXM, and High-Assurance applicability. |
| `threat_models` | list[string] | yes | Links to relevant threat model sections or `[]` with a gap. |
| `audit_obligations` | list[string] | yes | Audit obligation IDs or `[]` with a gap if none are specified. |
| `tests` | mapping | yes | Positive, negative, conformance, crash, fault, or other test groups. |
| `fuzz_targets` | list[string] | yes | Fuzz target IDs or `[]` with a gap if not applicable. |
| `evidence_artifacts` | list[string] | yes | Evidence IDs or planned evidence classes. |
| `lint_rules` | mapping | yes | Required and release-blocking lint rules. |
| `gaps` | list[string] | yes | Open gaps that block review, release, or implementation. |

## Field Semantics

### Status

| Status | Meaning |
| --- | --- |
| `draft` | Work in progress. May contain namespace wildcards and planned evidence classes. |
| `review` | Ready for architecture/security review. Source IDs and gaps must be explicit. |
| `ready` | Accepted as a design baseline for scoped implementation. |
| `deprecated` | Kept for history; must not be used for new work. |
| `superseded` | Replaced by another document. The replacement must be linked in `related_files`. |

### Source IDs

`source_ids` must list every Source Matrix ID needed for normative claims in the
spec. A split spec using IBM-derived terms must include IBM source IDs and must
include semantic overlap and MFOS divergence sections in the body.

Rules:

- Unknown source IDs are invalid.
- Informative source IDs may support discussion but must not be the only basis
  for a conformance requirement.
- `FBVBS-001` may transfer assurance discipline but must not be the only basis
  for IBM semantics.
- Split specs must use "inspired", "mapped", or similarly scoped language, not
  compatibility claims.

### Requirement Namespaces

`requirement_namespaces` is split into `defines` and `uses`.

Example:

```yaml
requirement_namespaces:
  defines:
    - MFOS-REQ-AUDIT-*
  uses:
    - MFOS-REQ-SOURCE-*
    - MFOS-REQ-AUTH-*
    - MFOS-REQ-QUALITY-*
```

`defines` means the spec is authoritative for that namespace. `uses` means the
spec depends on requirements owned elsewhere. Namespace wildcards are allowed in
draft and review documents but must resolve to concrete requirement IDs before a
release or production claim.

### Owned Files

`owned_files` exists to prevent accidental cross-agent overwrites. It must list
the files the spec owns or is expected to edit. If a task grants narrower
ownership than the front matter, the task ownership wins.

### Profile Applicability

Allowed values for each profile:

```text
required
recommended
optional
conditional
prohibited
not_applicable
```

Profile fields:

```yaml
profiles:
  baseline: required
  enterprise: required
  high_assurance: conditional
```

If `conditional` is used, the body must define the condition. If a profile is
`prohibited`, the body must explain why.

### Threat Model Links

`threat_models` must point to relevant sections in the threat model spec. If no
threat model exists yet, the field must be an empty list and `gaps` must include
a gap explaining which threat model is missing.

### Audit Obligations

Audit obligation IDs should use this format until a registry exists:

```text
AUD-<AREA>-<NNNN>
```

Every protected-resource operation must have at least one audit obligation or a
declared `SPEC_GAP`. Denial paths must identify whether audit is required before
the caller receives the result.

### Tests

The `tests` mapping should include groups that apply to the spec:

```yaml
tests:
  positive:
    - TEST-AREA-POS-0001
  negative:
    - TEST-AREA-NEG-0001
  parser:
    - TEST-AREA-PARSER-0001
  state_machine:
    - TEST-AREA-STATE-0001
  crash_recovery:
    - TEST-AREA-CRASH-0001
  fault_injection:
    - TEST-AREA-FAULT-0001
  conformance:
    - TEST-AREA-CONF-0001
```

Security-sensitive specs must include negative tests. Parser specs must include
parser or fuzz entries. State-machine specs must include invalid transition
tests.

### Fuzz Targets

Fuzz target IDs should use:

```text
FUZZ-<AREA>-<SUBJECT>-<NNNN>
```

If fuzzing does not apply, the field may be empty only when `gaps` or the body
explains why.

### Evidence Artifacts

Evidence artifact IDs should follow the traceability policy:

```text
EVID-<AREA>-<KIND>-<YYYYMMDD>-<NNNN>
```

Draft specs may use evidence classes such as `EVID-NEG-AUD-*`. Release claims
must use concrete evidence artifact IDs.

### Reviewers

`reviewers.required` must include roles, not only names. At minimum:

- `architecture` for all split specs,
- `security` for specs touching protected resources, identity, authorization,
  audit, AMF, PXM, Guard, update, or nucleus behavior,
- `assurance` for Enterprise-Standalone, Enterprise-PXM, or High-Assurance evidence claims,
- `operations` for operator, recovery, update, and production readiness specs.

### Lint Rules

`lint_rules.required` lists checks that must pass in draft/review mode.
`lint_rules.release_blocking` lists checks that must pass for release or
production claims.

Minimum required rules for all split specs:

```yaml
lint_rules:
  required:
    - SRC-LINT-REF-0001
    - SRC-LINT-REF-0002
    - SRC-LINT-REQ-0003
    - SRC-LINT-REQ-0007
  release_blocking:
    - SRC-CI-FORBIDDEN-WORDING
    - SRC-CI-MISSING-SOURCE-ID
    - SRC-CI-MISSING-REQ-LINK
```

## Required Section Schema

Every split spec should contain these sections in this order unless a waiver is
recorded in `gaps`:

1. Purpose
2. Scope
3. Non-objectives
4. Compatibility Statement
5. Source Matrix References
6. Terminology and Concept Mapping
7. Profile Applicability
8. Requirements
9. Object Model or Data Model
10. State Machines
11. Interfaces and ABIs
12. Authorization Rules
13. Audit Obligations
14. Failure Modes
15. Threat Model Links
16. Tests
17. Fuzz Targets
18. Evidence Artifacts
19. Lint Rules
20. Spec Gaps
21. Review Checklist

Sections that do not apply must say `Not applicable` and explain why. Empty
sections are not allowed.

## Section Requirements

### Purpose

State what design question the spec answers and which MFOS component or concept
it governs.

### Scope

List included objects, services, interfaces, profiles, and lifecycle stages.

### Non-objectives

List explicit exclusions. For IBM-derived specs, this section must state that
compatibility with IBM products or subsystems is not a goal.

### Compatibility Statement

Required text:

```text
MFOS is z/OS-inspired. This specification does not claim z/OS compatibility or
compatibility with IBM subsystems.
```

Specs may add component-specific non-compatibility statements, for example:

```text
securityd is RACF-inspired, not RACF-compatible.
```

### Source Matrix References

Provide a table with:

```text
Source ID | Authority | Concept used | MFOS use | Divergence
```

Every source ID must exist in `source-matrix.yml`.

### Terminology and Concept Mapping

For IBM-derived concepts, include:

- source concept,
- MFOS concept,
- semantic overlap,
- MFOS divergence,
- allowed wording,
- prohibited wording.

### Profile Applicability

Explain Baseline, Enterprise-Standalone, Enterprise-PXM, and High-Assurance behavior separately. Do not mix
High-Assurance Guard obligations into Baseline unless the profile table requires
that behavior.

### Requirements

Requirements must use stable IDs:

```text
MFOS-REQ-<AREA>-<NNNN>
```

Each requirement should include:

```text
ID
Requirement
Source IDs
Profiles
Verification
Audit obligation
Failure mode
Status
Gaps
```

### Object Model or Data Model

Define all structured objects introduced by the spec. Field names should be
stable and machine-readable. If a data model is intentionally deferred, mark it
as `SPEC_GAP`.

### State Machines

State-machine specs must include:

- states,
- legal transitions,
- invalid transitions,
- failure transitions,
- recovery transitions,
- invariants,
- liveness expectations if applicable.

### Interfaces and ABIs

Interface specs must include:

- caller,
- callee,
- request type,
- response type,
- identity source,
- authorization point,
- audit point,
- error model,
- unsupported behavior,
- spec gaps.

### Authorization Rules

Protected-resource specs must state that securityd is the final policy decision
point unless a later approved spec explicitly narrows the path. Local services
may enforce cached decisions but must not invent final authorization policy.

### Audit Obligations

Audit sections must identify:

- operation,
- subject,
- object,
- decision,
- reason code,
- policy version,
- ordering requirement,
- failure policy,
- evidence class.

Denial paths must specify whether audit must complete before the caller receives
the result.

### Failure Modes

Failure modes must distinguish:

- `UNSUPPORTED`: specified but not implemented,
- `SPEC_GAP`: unspecified and must not be implemented as success,
- `POLICY_DENIED`: denied by policy,
- `AUDIT_REQUIRED_BUT_UNAVAILABLE`: audit obligation cannot be met,
- component-specific errors.

### Threat Model Links

Link to relevant threat scenarios or state that the threat model is pending.
Pending threat models must be listed in `gaps`.

### Tests

List positive tests, negative tests, state-machine tests, crash tests,
fault-injection tests, conformance tests, and review-only checks as applicable.

### Fuzz Targets

Required for parsers and structured input boundaries. If fuzzing is deferred,
the spec must list the parser or boundary and the reason for deferral.

### Evidence Artifacts

List planned or concrete evidence artifacts. Draft specs may use evidence
classes. Ready specs should use concrete evidence IDs for reviewed claims.

### Lint Rules

List source, requirement, test, evidence, and wording lint rules required for
the spec. Include release-blocking rules for production or conformance claims.

### Spec Gaps

Gaps must be explicit and actionable. Each gap should include:

```text
Gap ID
Description
Blocks
Owner
Needed decision or artifact
```

## Minimal New Spec Template

```markdown
---
schema_version: 1
document_id: MFOS-SPEC-AREA-0001
title: "MFOS Area Specification"
status: draft
revision: "0.1"
last_updated: YYYY-MM-DD
owners:
  - unassigned
reviewers:
  required:
    - architecture
  optional:
    - security
source_ids:
  - EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
requirement_namespaces:
  defines:
    - MFOS-REQ-AREA-*
  uses:
    - MFOS-REQ-SOURCE-*
owned_files:
  - docs/design/specs/NN-area.md
related_files:
  - docs/design/source-matrix/source-matrix.yml
profiles:
  baseline: required
  enterprise: required
  high_assurance: conditional
threat_models: []
audit_obligations: []
tests:
  positive: []
  negative: []
  conformance: []
fuzz_targets: []
evidence_artifacts: []
lint_rules:
  required:
    - SRC-LINT-REF-0001
    - SRC-LINT-REF-0002
    - SRC-LINT-REQ-0003
    - SRC-LINT-REQ-0007
  release_blocking:
    - SRC-CI-FORBIDDEN-WORDING
    - SRC-CI-MISSING-SOURCE-ID
    - SRC-CI-MISSING-REQ-LINK
gaps:
  - GAP-AREA-0001
---

# MFOS Area Specification v0.1

## Purpose

## Scope

## Non-objectives

## Compatibility Statement

MFOS is z/OS-inspired. This specification does not claim z/OS compatibility or
compatibility with IBM subsystems.

## Source Matrix References

## Terminology and Concept Mapping

## Profile Applicability

## Requirements

## Object Model or Data Model

## State Machines

## Interfaces and ABIs

## Authorization Rules

## Audit Obligations

## Failure Modes

## Threat Model Links

## Tests

## Fuzz Targets

## Evidence Artifacts

## Lint Rules

## Spec Gaps

## Review Checklist
```

## Lint Expectations

Future lint automation should enforce:

| Rule | Severity | Check |
| --- | --- | --- |
| SPEC-FM-0001 | ERROR | Front matter exists and parses as YAML. |
| SPEC-FM-0002 | ERROR | Required fields are present. |
| SPEC-FM-0003 | ERROR | `source_ids` exist in `source-matrix.yml`. |
| SPEC-FM-0004 | ERROR | z/OS-inspired terms have source IDs and concept mapping. |
| SPEC-FM-0005 | BLOCK | Compatibility claims appear outside prohibited-wording or negative-test context. |
| SPEC-FM-0006 | ERROR | Protected-resource specs have audit obligations. |
| SPEC-FM-0007 | ERROR | Security-sensitive specs list negative tests. |
| SPEC-FM-0008 | ERROR | Parser specs list fuzz targets or a gap. |
| SPEC-FM-0009 | WARN | Draft specs use namespace wildcards that must resolve before release. |
| SPEC-FM-0010 | ERROR | Ready or release specs contain unresolved release-blocking gaps. |

## Review Checklist

- Front matter is present.
- Status is accurate.
- Owners and reviewers are assigned.
- Source IDs exist and are appropriate.
- IBM-derived terms have overlap and divergence.
- Requirement namespaces are listed.
- Owned files are explicit.
- Profiles are separated.
- Threat model links exist or gaps are listed.
- Audit obligations are complete for protected-resource operations.
- Negative tests are listed for security-sensitive behavior.
- Fuzz targets are listed for parsers.
- Evidence artifacts or evidence classes are listed.
- Lint rules include required and release-blocking checks.
- `UNSUPPORTED` and `SPEC_GAP` are distinct.
- No compatibility claim appears.

## Spec Gaps

- Existing split specs have not been retrofitted to this schema.
- No parser or CI linter currently enforces this front matter.
- Requirement, audit obligation, test, fuzz target, and evidence registries are
  not yet canonical.
- `document_id` naming for legacy files needs a migration plan.
- The exact waiver format for missing sections is not yet defined.
- Release-mode rules for namespace wildcards need a concrete registry.
