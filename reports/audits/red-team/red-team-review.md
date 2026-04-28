# MFOS Phase 0.6 Red Team Review

Date: 2026-04-27  
Workspace: `/home/nia/mfos`  
Mode: design/artifact review only. No implementation code was started or edited.

## Scope

Reviewed current Phase 0.6 artifacts for:

- z/OS compatibility implication
- IBM official/endorsement implication
- source weakening
- PKU/PKS overclaim
- AMF overclaim
- Guard/PXM scope creep
- audit bypass
- dataset/POSIX confusion
- operator/root shell confusion
- fake success
- missing negative tests
- premature implementation

Primary inputs were `README.md`, `docs/design/STATUS.md`,
`docs/design/specs/07-audit.md`, `08-dataset-catalog.md`,
`10-operator-console.md`, `12-amf.md`, `16-pxm.md`, `17-guard.md`,
`18-linux-gateway.md`, `21-ai-implementation-contract.md`,
`docs/design/registries/*.yaml`, and existing `reports/*.md`.

## Executive Result

Result: **conditional pass with blockers before implementation or claim
broadening**.

The core design posture is strong: MFOS repeatedly says it is z/OS-inspired,
not z/OS-compatible; IBM source use is framed as public documentation reference
material; AMF production load is explicitly disabled for early phases; PXM and
Guard are mostly bounded; audit, dataset, and operator boundaries are directly
called out.

However, several Phase 0.6 artifacts still create review risk:

1. Guard profile applicability table is malformed and can be read as scope
   creep or a missing High-Assurance column.
2. Several specs list required body source IDs that are absent from front
   matter, weakening traceability and lintability.
3. Test/evidence registries are too thin for Phase 0.6 claim confidence: only
   5 registered tests and 3 draft evidence records exist, while many required
   negative tests remain planned prose.
4. Source cards still have local verification gaps for exact publication,
   section, and version pins.
5. Scaffold breadth can imply implementation status unless every downstream
   summary preserves the "scaffold only" caveat.

## Findings

### RT-001: Guard Profile Table Is Structurally Ambiguous

Severity: **High**  
Category: Guard/PXM scope creep, fake claim risk

`docs/design/specs/17-guard.md` declares four profile columns at line 122, but
the separator and rows at lines 123-130 only provide three profile value cells.
That makes it unclear whether Enterprise-PXM or High-Assurance receives the
`MUST` value.

Impact:

- A reader or generator may accidentally treat Guard as mandatory in
  Enterprise-PXM or may drop High-Assurance applicability.
- The ambiguity weakens the otherwise clear claim that Guard is a
  High-Assurance root-object component.
- Any implementation packet generated from this table would be unsafe.

Required before implementation:

- Fix the table to include all four profile columns and explicit values.
- Add a lint check for Markdown table width in spec front matter/body sections
  that drive profile applicability.

### RT-002: Front Matter Source Refs Are Weaker Than Body Source Lists

Severity: **High**  
Category: source weakening, source traceability

Several specs list source IDs in their Source Matrix section that are missing
from `source_refs` front matter:

| Spec | Front matter | Body-required IDs missing from front matter |
| --- | --- | --- |
| `docs/design/specs/12-amf.md` | line 9 | `TUF-001`, `SLSA-001`, `FBVBS-001` from lines 75-78 |
| `docs/design/specs/16-pxm.md` | line 9 | `TCG-001`, `FBVBS-001` from lines 83 and 86 |
| `docs/design/specs/17-guard.md` | line 9 | `TCG-001`, `FBVBS-001` from lines 104 and 106 |
| `docs/design/specs/07-audit.md` | line 9 | `TUF-001`, `FBVBS-001` from lines 91-92 |
| `docs/design/specs/18-linux-gateway.md` | line 9 | `FBVBS-001` from line 84 |

Impact:

- Automated traceability that trusts front matter will miss normative source
  dependencies.
- This creates a route for source weakening during implementation packet
  generation, especially for AMF revocation/update, PXM measured boot, Guard
  proof obligations, audit evidence discipline, and gateway fail-closed rules.

Required before implementation:

- Align front matter `source_refs` with each spec's body source list.
- Add a validator that compares body Source Matrix tables/lists against
  front matter.

### RT-003: Negative Test Registry Coverage Is Not Yet Adequate

Severity: **High**  
Category: missing negative tests, audit bypass, fake success

`docs/design/registries/tests.yaml` explicitly says entries are draft metadata
and do not assert implementation existence at lines 1-3. The registry contains
only five tests, all draft, at lines 27-265. Existing traceability audit says
only 4 of 21 registered requirements have direct test coverage and 81 planned
tests named in requirement verification fields are not registered
(`reports/audits/traceability/traceability-audit.md` lines 27-30).

Missing or unregistered high-risk negative-test areas include:

- PXM no-IOMMU, no interrupt remap, teardown-before-reassign, stale ownership.
- Guard root mismatch, rollback, unavailable Guard, scope-refusal requests.
- AMF disabled load with no mapping, no registry entry, and no authorized state.
- Linux gateway root/desktop bypass and direct dataset mount attempts.
- Operator destructive command without confirmation or dual control.
- Audit unavailable or caller-result-before-deny-audit cases beyond the one
  draft registry entry.

Required before implementation:

- Register negative tests for every security-sensitive Phase 0.6 requirement
  named in `docs/design/registries/requirements.yaml`.
- Require `expected_absence` for each negative test, not only an error code.
- Block implementation packets when negative test IDs are prose-only.

### RT-004: Evidence Registry Is Placeholder-Only

Severity: **Medium**  
Category: fake success, premature implementation

`docs/design/registries/evidence.yaml` states that records are draft
placeholders, not verified evidence, at lines 1-3. Evidence entries have
`sha384: null`, verification result `not_checked`, and empty audit linkage in
the inspected records, for example lines 41-63 and 80-103.

Impact:

- Good placeholder discipline exists, but downstream summaries must not treat
  these evidence IDs as proof.
- Release, conformance, AMF, PXM, or Guard claims must remain blocked until
  artifacts are produced, hashed, verified, and linked to audit/correlation IDs.

Required before claim broadening:

- Keep evidence IDs labeled draft until artifacts exist and verify.
- Add release lint that rejects claim language when evidence verification is
  `not_checked` or artifact digests are null.

### RT-005: Source Card Metadata Gaps Remain a Source-Weakening Risk

Severity: **Medium**  
Category: source weakening, IBM implication control

`reports/audits/source/source-card-audit.md` records pass-with-warnings status and says all
37 cards have local metadata verification gaps for exact publication, section,
and version pins at lines 20-27 and 64-70. It also lists eight IBM-derived cards
whose allowed wording lacks preferred non-compatibility cue words at lines
46-62.

Impact:

- The current cards are acceptable for draft Phase 0.6, but weak section pins
  make later semantic claims harder to audit.
- Allowed wording drift could accidentally sound more compatibility-like than
  intended.

Required before stronger source-grounded claims:

- Add section/version pins or explicit "unverified local metadata" blockers per
  source card.
- Normalize IBM-derived allowed wording to include "inspired", "mapped", or
  "reference" style cues.

### RT-006: Scaffold Breadth Can Still Imply Implementation Status

Severity: **Medium**  
Category: premature implementation, fake success

`docs/design/STATUS.md` reports 171 files and 346 directories after scaffold
creation at lines 111-113. The root README correctly states project layers will
receive artifacts over time at lines 10-13, and local checks are small design
checks at lines 46-56. Existing repository audit also flags scaffold-only
implementation/test/fuzz/formal/evidence paths.

Impact:

- Directory names such as `implementation/guard`, `implementation/pxm`,
  `tests/negative`, `fuzz/targets`, and `evidence/production-readiness` can be
  mistaken for implementation or verification status when quoted out of
  context.

Required before external summaries or task packets:

- Summaries must say scaffold-only unless concrete source, test, evidence, and
  requirement links exist.
- Task packets should not cite directory presence as evidence.

## Area Checks

### z/OS Compatibility Implication

Pass with residual wording discipline required.

Strong controls:

- Root README says MFOS does not claim z/OS, IBM product, or API compatibility
  (`README.md` lines 3-8).
- Dataset spec explicitly prohibits z/OS/DFSMS/RACF/SMF compatibility wording.
- Operator spec explicitly says commands are not z/OS-compatible and forbids
  TSO/ISPF/MVS compatibility claims.
- PXM says it is not PR/SM, IBM Z firmware, or z/Architecture.

Residual risk:

- Source card wording gaps from RT-005 should be cleaned before broader
  publication.

### IBM Official or Endorsement Implication

Pass.

The root README explicitly says public IBM-published documentation use does not
imply IBM approval, affiliation, sponsorship, or endorsement. I did not find a
contrary official/endorsed MFOS claim in the reviewed artifacts.

### PKU/PKS Overclaim

Pass with no blocker found.

The reviewed system-integrity and Guard language treats PKU/PKS as mechanisms,
not roots. Guard explicitly says it must not treat PKU or PKS as a substitute
for Guard isolation. No PKU/PKS compatibility or primary-boundary claim was
found.

### AMF Overclaim

Pass with test/evidence gap.

AMF spec lines 48-49 and requirements registry lines 1268-1335 keep early AMF
load disabled and require `MFOS_ERR_UNSUPPORTED` with no executable mapping,
registry entry, or authorized-state transition. The gap is not wording; it is
registered test/evidence coverage, captured in RT-003 and RT-004.

### Guard/PXM Scope Creep

Conditional pass.

PXM is correctly bounded away from datasets, catalogs, spool, security profiles,
operator business commands, and workload policies (`docs/design/specs/16-pxm.md`
lines 24 and 61-73). Guard is correctly bounded away from dataset policy,
catalog lookup, job scheduling, POSIX, Linux/Desktop behavior, securityd, and
auditd (`docs/design/specs/17-guard.md` lines 77-91). The Guard profile table
malformation in RT-001 must be fixed before any generated work can rely on it.

### Audit Bypass

Pass with registry gap.

Audit spec directly rejects audit bypass patterns: console/spool output is not
audit evidence, denies must not return before required durable audit, silent
audit loss is forbidden, and audit query bypass is called out (`07-audit.md`
lines 43-51). The remaining risk is thin negative-test registration, not the
normative model.

### Dataset/POSIX Confusion

Pass.

Dataset spec states that a dataset is not a POSIX file wrapper and forbids
POSIX pathname semantics as the primary namespace. Linux gateway forbids direct
mounting of MFOS datasets as Linux filesystems and raw volume sharing. No
conflicting POSIX-first dataset claim was found.

### Operator/Root Shell Confusion

Pass.

Operator spec states the console is not a root shell, excludes arbitrary script
execution with elevated privilege, and routes commands through parse, resolve,
authorize, confirm, execute, audit, and display. No root-shell equivalence claim
was found.

### Fake Success

Conditional pass.

The design has explicit `UNSUPPORTED`/`SPEC_GAP` discipline and local
no-fake-success lint was reported as passing in `docs/design/STATUS.md` lines
127-130. The risk is that evidence/test registries are draft placeholders; they
must not be represented as passing tests.

### Premature Implementation

Conditional pass.

Most specs set `implementation_allowed: false` in front matter and the roadmap
keeps Phase 1 behind Phase 0 exit criteria. No implementation code was started
by this review. The broad scaffold still needs disciplined wording per RT-006.

## Red Team Gate Recommendations

Before any implementation packet is generated or assigned:

1. Fix `docs/design/specs/17-guard.md` profile table width and values.
2. Align front matter `source_refs` with body Source Matrix sections.
3. Register negative tests for PXM, Guard, AMF-disabled, Linux gateway,
   operator destructive commands, audit failure, and dataset/POSIX bypass.
4. Make claim/evidence lint reject draft evidence as proof.
5. Keep all scaffold paths labeled as scaffold-only in generated summaries.

Until those are complete, Phase 0.6 artifacts are suitable for continued design
hardening but not for implementation authorization, production-readiness
claims, High-Assurance claims, AMF-enabled claims, or PXM device-assignment
claims.

## Orchestrator Follow-Up

The orchestrator addressed the two High findings that could be fixed safely in
Phase 0.6 without broadening design claims:

- RT-001: repaired malformed profile tables in `07-audit.md`, `17-guard.md`,
  `18-linux-gateway.md`, `26-hardware-profile.md`, and
  `30-attestation-measured-boot.md`.
- RT-002: normalized split-spec front matter so body Source Matrix IDs are also
  present in `source_refs`.
- Added local lint coverage for Source Matrix front-matter drift and Markdown
  table width mismatches.

The remaining RT-003 through RT-006 items are recorded as Phase 0.7 gaps and
continue to block production implementation, production-readiness claims,
High-Assurance claims, AMF-enabled claims, and PXM device-assignment claims.
