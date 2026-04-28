# MFOS Source Matrix Lint and Freshness Automation Spec v0.1

Status: design draft

This document specifies source-matrix linting and source freshness automation
for MFOS design work. It is a design spec only. It does not implement code.

MFOS is z/OS-inspired. This spec does not permit z/OS compatibility claims.

## Purpose

Source linting exists to keep MFOS architecture source-grounded, traceable, and
reviewable by independent agents. The linter must catch drift before it becomes
implementation behavior:

- malformed Source Card index or Source Card YAML,
- missing required fields,
- duplicate or malformed source IDs,
- prohibited compatibility wording,
- z/OS-inspired terms without Source Matrix IDs,
- source IDs that do not exist,
- requirements without source linkage,
- tests without requirement linkage,
- evidence without source, requirement, and test linkage,
- stale source reviews,
- fake success around `UNSUPPORTED` and `SPEC_GAP`.

## Scope

The lint design applies to:

- `docs/design/source-matrix/source-matrix.yml`
- `docs/design/source-matrix/cards/*.yml`
- `docs/design/source-matrix/source-card-schema.md`
- `docs/design/source-matrix/source-matrix.md`
- `docs/design/source-matrix/traceability-policy.md`
- `docs/design/source-matrix/traceability-index.md`
- all split specs under `docs/design/specs/`
- future prompt packs, task packs, test registries, evidence registries, and CI
  metadata once those paths exist.

The initial implementation target is documentation linting. Later phases may
extend the same rules to code comments, test metadata, release notes, and
evidence manifests.

## Non-objectives

This spec does not:

- implement a linter,
- define the full source matrix schema beyond lint requirements,
- fetch or archive vendor documentation,
- prove that a vendor source is semantically correct,
- permit compatibility claims with z/OS or IBM subsystems,
- permit source-less z/OS-inspired behavior,
- allow `UNSUPPORTED` or `SPEC_GAP` paths to complete; they must fail closed.

## Lint Severity Model

| Severity | Meaning | CI behavior |
| --- | --- | --- |
| BLOCK | The repository must not merge or produce conformance artifacts. | fail |
| ERROR | The checked document is invalid and must be fixed. | fail |
| WARN | The document is usable but needs review or follow-up. | pass in draft mode, fail in release mode |
| INFO | Informational finding for traceability reports. | pass |

CI mode determines how strict warnings are:

| Mode | Intended use | Behavior |
| --- | --- | --- |
| draft | local design iteration | BLOCK and ERROR fail |
| review | PR or design review | BLOCK and ERROR fail; WARN summarized |
| release | conformance or production claim | BLOCK, ERROR, and WARN fail unless explicitly waived |

## YAML Validation Rules

### Source Card Index Rules

| Rule ID | Severity | Rule |
| --- | --- | --- |
| SRC-LINT-YAML-0001 | ERROR | `source-matrix.yml` must parse as YAML 1.2-compatible data. |
| SRC-LINT-YAML-0002 | ERROR | Root value must be a mapping. |
| SRC-LINT-YAML-0003 | ERROR | Root must contain `schema_version`, `document_id`, `status`, `source_card_schema`, `card_directory`, `compatibility_statement`, `global_rules`, and `cards`. |
| SRC-LINT-YAML-0004 | ERROR | `schema_version` must be an integer. |
| SRC-LINT-YAML-0005 | ERROR | `document_id` must match `MFOS-SOURCE-MATRIX-CARD-INDEX-[0-9]{4}`. |
| SRC-LINT-YAML-0006 | ERROR | `status` must be one of `draft`, `review`, `ready`, `deprecated`, or `superseded`. |
| SRC-LINT-YAML-0007 | ERROR | `compatibility_statement` must state that MFOS does not claim z/OS compatibility. |
| SRC-LINT-YAML-0008 | ERROR | `global_rules.ledger_rules` must be a non-empty list of non-empty strings. |
| SRC-LINT-YAML-0009 | ERROR | `cards` must be a non-empty list of mappings. |

### Source Card Required Fields

Every item in `source-matrix.yml.cards` must contain:

```text
source_id
source_type
vendor
document_title
card_path
status
```

Every `cards/*.yml` Source Card must contain:

```text
source_id
source_kind
source_type
semantic_role
vendor
document_title
document_url
retrieved_at
reference_purpose
review_topics
mfos_mapping
mfos_divergence
prohibited_inference
legal_controls
source_refs
requirement_refs
review_status
```

| Rule ID | Severity | Rule |
| --- | --- | --- |
| SRC-LINT-YAML-0101 | ERROR | Each source card must include all required fields. |
| SRC-LINT-YAML-0102 | ERROR | No source card may include an empty `source_id`, `source_type`, `vendor`, `document_title`, or `review_status`. |
| SRC-LINT-YAML-0103 | ERROR | IBM-derived external source IDs must use `EXTREF-IBM-...-[0-9]{4}`. Legacy `IBM-*` IDs are allowed only in `legacy_source_ids`. |
| SRC-LINT-YAML-0104 | ERROR | Source IDs must be unique. |
| SRC-LINT-YAML-0105 | ERROR | `source_type` must be one of `external_reference` or `internal_transfer`. |
| SRC-LINT-YAML-0106 | ERROR | `review_topics` must be non-empty. |
| SRC-LINT-YAML-0107 | ERROR | `document_url` must be either a non-empty string or a non-empty list of non-empty strings. |
| SRC-LINT-YAML-0108 | WARN | External URLs should use `https://`; internal sources should use `internal:`. |
| SRC-LINT-YAML-0109 | ERROR | `review_topics`, `mfos_divergence`, `prohibited_inference`, and `requirement_refs` must be lists. |
| SRC-LINT-YAML-0110 | ERROR | `review_topics`, `mfos_mapping`, `mfos_divergence`, and `prohibited_inference` must be non-empty. |
| SRC-LINT-YAML-0111 | WARN | `gaps` should be non-empty while an entry is in `draft` or `review` status. |
| SRC-LINT-YAML-0112 | ERROR | `requirement_refs` values must match `^MFOS-REQ-[A-Z0-9]+-(?:[0-9]{4}|\\*)$` or an approved namespace wildcard such as `MFOS-REQ-SI-*`. |
| SRC-LINT-YAML-0113 | ERROR | `verification_refs` values must match `^[a-z0-9]+(?:-[a-z0-9]+)*$`. |
| SRC-LINT-YAML-0114 | ERROR | `legal_controls` must assert public-safe controls and must not claim affiliation, compatibility, or source substitution. |
| SRC-LINT-YAML-0115 | ERROR | `prohibited_inference` must include compatibility-risk wording for IBM-derived external references. |
| SRC-LINT-YAML-0116 | ERROR | External reference cards that use external vendor, product, project, organization, or specification names must set `vendor_mark_used: true` and `legal_controls.trademark_reference_only: true`. |
| SRC-LINT-YAML-0117 | ERROR | Source Cards must not include removed public fields such as `canonical_concepts`, `normative_source`, `detailed_summary`, `source_summary`, copied excerpts, copied tables, record layouts, command syntax, macro signatures, or message tables. |

### Cross-Entry Consistency Rules

| Rule ID | Severity | Rule |
| --- | --- | --- |
| SRC-LINT-YAML-0201 | ERROR | An `external_reference` card must have at least one requirement reference or an explicit gap. |
| SRC-LINT-YAML-0202 | WARN | A design-background source should not be the only source for a conformance requirement. |
| SRC-LINT-YAML-0203 | ERROR | An `internal_transfer` source must not be the only source for external-product semantics. |
| SRC-LINT-YAML-0204 | WARN | All entries with the same `area` should have related requirement namespaces or explain divergence in `gaps`. |
| SRC-LINT-YAML-0205 | ERROR | A source entry must not contradict root `compatibility_statement`. |

## Forbidden Wording Checks

The linter must scan Markdown, YAML string fields, prompt packs, release text,
and future implementation comments for forbidden wording.

### Hard Forbidden Claims

These phrases or equivalent claims are `BLOCK` outside explicitly allowed
negative examples and Source Card `prohibited_inference` fields:

```text
MFOS is z/OS-compatible
z/OS compatible
z/OS-compatible
MFOS implements z/OS
z/Architecture-compatible
JES-compatible
JES2-compatible
RACF-compatible
DFSMS-compatible
SMF-compatible
external-workload-management-compatible
APF-compatible
PR/SM-compatible
DPM-compatible
VBS-compatible
VSM-compatible
VTL-compatible
```

### Semantic Overclaim Checks

These are `ERROR` unless the document is explicitly listing prohibited wording
or documenting divergence:

```text
PKU provides storage-key compatibility
PKS provides storage-key compatibility
PKU protects instruction fetch
CET enforces authorization
dataset is just a POSIX file
operator console is a root shell
AMF is admin privilege
auditd is ordinary logging
Guard protects everything
PXM schedules jobs
PXM decides dataset access
Guard decides dataset policy
signature alone is sufficient update security
measured boot proves runtime integrity
```

### Allowed Contexts for Forbidden Strings

Forbidden strings may appear only in these contexts:

- `prohibited_inference` fields in Source Cards,
- "Prohibited wording" sections in design documents,
- negative-test descriptions that assert the phrase must be rejected,
- this lint spec's forbidden-wording tables,
- generated lint reports that quote the rejected string.

In allowed contexts, the linter must still ensure the surrounding text clearly
labels the phrase as prohibited, rejected, or a negative test.

## Source ID Usage Checks

### Source ID Reference Validation

| Rule ID | Severity | Rule |
| --- | --- | --- |
| SRC-LINT-REF-0001 | ERROR | Every `IBM-*`, `X64-*`, `MS-*`, `TCG-*`, `NIST-*`, `SEL4-*`, `SLSA-*`, `TUF-*`, and `FBVBS-*` token that looks like a Source Matrix ID must exist in `source-matrix.yml`. |
| SRC-LINT-REF-0002 | ERROR | A split spec that uses z/OS-inspired terminology must include a Source Matrix references section or table. |
| SRC-LINT-REF-0003 | ERROR | IBM-derived MFOS terms must link to mapping records with semantic overlap and MFOS divergence. |
| SRC-LINT-REF-0004 | WARN | A source ID referenced by no split spec should be reported as unused. |
| SRC-LINT-REF-0005 | ERROR | A split spec must not cite an informative source as the only basis for a normative requirement unless a waiver is present. |
| SRC-LINT-REF-0006 | ERROR | Internal transfer source `FBVBS-001` must not be used as the only basis for IBM semantic mapping. |

### z/OS-Inspired Term Triggers

The linter should flag these terms when they appear without nearby Source
Matrix IDs or mapping references:

```text
z/OS
MVS
JCL
JES
JES2
RACF
DFSMS
SMF
WLM
APF
PSW
storage key
SVC
PC instruction
cross-memory
LPAR
PR/SM
DPM
z/OS UNIX
SYSIN
SYSOUT
spool
catalog
dataset
operator command
authorized program
authorized module
```

The trigger is not a violation by itself. It becomes a violation when the
document lacks source IDs, mapping records, overlap/divergence text, or allowed
wording.

## Requirement Linkage Checks

| Rule ID | Severity | Rule |
| --- | --- | --- |
| SRC-LINT-REQ-0001 | ERROR | Every `MFOS-REQ-*` token in source-ledger files must match an approved requirement namespace or concrete ID pattern. |
| SRC-LINT-REQ-0002 | ERROR | Every Source Card with `source_type: external_reference` must map to at least one `MFOS-REQ-*` reference or explicitly record a gap. |
| SRC-LINT-REQ-0003 | ERROR | Every requirement in a split spec that uses a source-grounded concept must cite at least one Source Matrix ID. |
| SRC-LINT-REQ-0004 | ERROR | Requirements that mention protected resources must include authorization and audit obligations or explicitly mark a `SPEC_GAP`. |
| SRC-LINT-REQ-0005 | ERROR | Requirements that specify unimplemented behavior must define `UNSUPPORTED` fail-closed behavior. |
| SRC-LINT-REQ-0006 | WARN | Namespace wildcards such as `MFOS-REQ-SI-*` are allowed in index documents but must be resolved to concrete IDs before release mode. |
| SRC-LINT-REQ-0007 | ERROR | A requirement must not use compatibility wording as an obligation. |

## Test Linkage Checks

| Rule ID | Severity | Rule |
| --- | --- | --- |
| SRC-LINT-TEST-0001 | WARN | Every concrete requirement should map to at least one test ID or review ID in draft mode. |
| SRC-LINT-TEST-0002 | ERROR | Every security-sensitive concrete requirement must map to at least one negative test before review mode. |
| SRC-LINT-TEST-0003 | ERROR | Parser requirements must map to fuzz targets or a documented waiver. |
| SRC-LINT-TEST-0004 | ERROR | State-machine requirements must map to legal-transition and illegal-transition tests. |
| SRC-LINT-TEST-0005 | ERROR | Audit requirements must map to ordering tests when denial must be recorded before caller result. |
| SRC-LINT-TEST-0006 | ERROR | Update requirements must map to rollback, freeze, mix-and-match, bad signature, bad hash, bad size, revoked key, and downgrade tests where applicable. |
| SRC-LINT-TEST-0007 | ERROR | PXM device requirements must map to teardown, IOMMU, interrupt remapping, and memory-zeroing tests. |
| SRC-LINT-TEST-0008 | ERROR | Guard requirements must map to root mismatch and fail-secure tests. |

## Evidence Linkage Checks

| Rule ID | Severity | Rule |
| --- | --- | --- |
| SRC-LINT-EVID-0001 | WARN | Every concrete test ID should map to at least one evidence artifact in draft mode. |
| SRC-LINT-EVID-0002 | ERROR | Release mode requires evidence for every requirement included in the claim. |
| SRC-LINT-EVID-0003 | ERROR | Evidence records must include source IDs, requirement IDs, test IDs or review IDs, artifact revision, date, toolchain version when applicable, and result. |
| SRC-LINT-EVID-0004 | ERROR | Evidence for denial must show both denied protected output and required audit evidence. |
| SRC-LINT-EVID-0005 | ERROR | Evidence for `UNSUPPORTED` must show fail-closed behavior. |
| SRC-LINT-EVID-0006 | ERROR | Evidence for `SPEC_GAP` must show the gap is not treated as success. |
| SRC-LINT-EVID-0007 | ERROR | Production claims require provenance, SBOM, source lint report, negative test evidence, and production gate evidence. |
| SRC-LINT-EVID-0008 | ERROR | High-Assurance claims require Guard-root evidence, audit-root evidence, attestation evidence, and explicit assumptions. |

## Freshness Review Workflow

Source freshness automation must track whether the source matrix still reflects
the upstream source and MFOS usage. Freshness review is not a claim that the
source is correct; it is a review that the matrix entry remains current enough
to use.

### Desired Future Metadata

The current Source Card index and cards do not yet include complete freshness metadata. A
future schema revision should add:

```yaml
freshness:
  owner: string
  last_reviewed: YYYY-MM-DD
  review_due: YYYY-MM-DD
  review_interval_days: integer
  pinned_version: string
  pinned_section: string
  retrieval_method: manual | automated | internal
  content_fingerprint: string
  last_result: fresh | stale | unreachable | changed | needs-human-review
```

Until those fields exist, freshness automation should report missing metadata as
`WARN` in draft/review mode and `ERROR` in release mode.

### Review Intervals

| Source class | Default interval | Release-mode requirement |
| --- | --- | --- |
| IBM online docs | 180 days | must be reviewed within interval and version/section pinned |
| Intel/AMD manuals | 180 days | must pin revision or retrieval date |
| Microsoft docs | 180 days | must pin URL and review date |
| TCG/NIST/TUF/SLSA specs | 365 days | must pin version or publication identifier where available |
| seL4 informative material | 365 days | must record assumptions copied into MFOS |
| Internal transfer source | 180 days | must identify internal document revision |

### Freshness States

| State | Meaning | CI behavior |
| --- | --- | --- |
| fresh | Reviewed within interval; no source-breaking change known. | pass |
| stale | Review interval expired. | warn in draft/review; fail in release |
| unreachable | Source could not be accessed by automation. | warn; fail in release unless manual review exists |
| changed | Content fingerprint or title changed. | fail until human review |
| needs-human-review | Automation cannot determine semantic impact. | warn in draft; fail in review/release for affected claims |
| deprecated | Source no longer appropriate for new claims. | fail for new requirements |

### Freshness Review Steps

1. Identify source entries due for review.
2. Retrieve or manually inspect the upstream source.
3. Confirm title, URL, publication number, version, and section anchor.
4. Compare source review notes and bibliographic metadata against Source Card `mfos_mapping` and `mfos_divergence`.
5. Confirm allowed and prohibited wording still matches the source.
6. Confirm requirement references and verification references are still valid.
7. Update freshness metadata and add a review evidence artifact.
8. If a source changed semantically, mark affected requirements as `blocked` or
   `needs-review` until the split spec is reviewed.

## CI Failure Modes

| Failure code | Severity | Meaning |
| --- | --- | --- |
| SRC-CI-YAML-PARSE | ERROR | Source matrix YAML cannot be parsed. |
| SRC-CI-YAML-SCHEMA | ERROR | Required field or type rule failed. |
| SRC-CI-DUPLICATE-ID | ERROR | Duplicate Source Matrix ID. |
| SRC-CI-UNKNOWN-SOURCE-ID | ERROR | A document references a source ID that is not in the ledger. |
| SRC-CI-MISSING-SOURCE-ID | ERROR | A z/OS-inspired term appears without source grounding. |
| SRC-CI-MISSING-DIVERGENCE | ERROR | IBM-derived term lacks MFOS divergence. |
| SRC-CI-FORBIDDEN-WORDING | BLOCK | A prohibited compatibility or overclaim phrase appears outside allowed contexts. |
| SRC-CI-MISSING-REQ-LINK | ERROR | Source-grounded requirement lacks source linkage. |
| SRC-CI-MISSING-NEG-TEST | ERROR | Security-sensitive requirement lacks negative test linkage. |
| SRC-CI-MISSING-EVIDENCE | ERROR | Release claim lacks required evidence. |
| SRC-CI-STALE-SOURCE | WARN/ERROR | Freshness review is overdue. |
| SRC-CI-SOURCE-CHANGED | ERROR | Source content changed and needs human review. |
| SRC-CI-UNSUPPORTED-SUCCESS | BLOCK | Spec, test, or implementation treats `UNSUPPORTED` as success. |
| SRC-CI-SPEC-GAP-SUCCESS | BLOCK | Spec, test, or implementation treats `SPEC_GAP` as success. |
| SRC-CI-PXM-SCOPE-BREACH | BLOCK | PXM interprets MFOS enterprise semantics. |
| SRC-CI-GUARD-SCOPE-BREACH | BLOCK | Guard interprets ordinary business, dataset, job, or spool semantics. |

## Report Format

Lint reports should be machine-readable and human-readable. The machine-readable
shape should be:

```yaml
report_id: SRC-LINT-REPORT-YYYYMMDD-NNNN
mode: draft | review | release
status: pass | fail
summary:
  block: 0
  error: 0
  warn: 0
  info: 0
findings:
  - rule_id: SRC-LINT-YAML-0101
    severity: ERROR
    file: docs/design/source-matrix/source-matrix.yml
    line: 1
    source_id: EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
    requirement_id: MFOS-REQ-SYSINT-0001
    message: string
    remediation: string
evidence_id: EVID-SRC-LINT-YYYYMMDD-NNNN
```

Human-readable reports should group findings by severity, then by file, then by
source ID or requirement ID.

## Waiver Policy

Waivers are intentionally narrow.

- `BLOCK` findings may not be waived for release mode.
- Forbidden compatibility claims may not be waived.
- Missing source IDs for z/OS-inspired concepts may not be waived.
- Missing evidence may be waived only in draft mode.
- A stale source may be waived in review mode only with a human review note and
  due date.
- Waivers must include owner, reason, expiry date, affected files, and evidence
  ID.

Suggested waiver record:

```yaml
waiver_id: SRC-WAIVER-YYYYMMDD-NNNN
rule_id: SRC-LINT-TEST-0001
owner: string
reason: string
expires: YYYY-MM-DD
affected_files:
  - path
evidence_id: EVID-ARCH-REVIEW-YYYYMMDD-NNNN
```

## Rollout Plan

Phase 1:
  Validate YAML shape, required fields, duplicate IDs, and forbidden wording in
  source-matrix documents.

Phase 2:
  Validate source ID references, requirement namespace references, and split
  spec source-reference sections.

Phase 3:
  Validate test and evidence linkage once registries exist.

Phase 4:
  Add freshness metadata and freshness reporting.

Phase 5:
  Enforce release-mode gates for conformance and production claims.

## Spec Gaps

- No linter implementation exists yet.
- Source Cards lack complete freshness metadata fields.
- Requirement IDs are not yet registered in a canonical requirements index.
- Test IDs and evidence IDs do not yet have registry files.
- Split specs do not yet have a uniform machine-readable front matter format.
- The exact list of source-trigger terms needs review after glossary completion.
- External source retrieval and content fingerprinting rules are not defined.
- Waiver storage location and approval workflow are not defined.
- Release-mode CI entry point and artifact retention policy are not defined.
- The linter cannot yet distinguish all allowed explanatory uses of forbidden
  phrases without a context annotation format.
