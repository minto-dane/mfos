---
spec_id: "MFOS-SPEC-35-FUZZ-CORPUS-PLAN"
title: "MFOS Phase 0.9 Fuzz Corpus Plan"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS Phase 0.9 fuzz planning lead"
last_reviewed: "2026-04-27"
source_refs: ["EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001", "EXTREF-IBM-ZOS-JES-INTRODUCTION-0001", "EXTREF-IBM-ZOS-SECURITY-SERVER-0001", "EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001"]
requirement_refs: ["MFOS-REQ-AUTH-*", "MFOS-REQ-AUDIT-*", "MFOS-REQ-CATALOG-*", "MFOS-REQ-DATASET-*", "MFOS-REQ-JOB-*", "MFOS-REQ-SPOOL-*", "MFOS-REQ-OPER-*"]
claim_refs: []
test_refs: ["TEST-MFOS-*-FUZZ-*", "NEG-MFOS-*-FUZZ-*"]
evidence_refs: ["EV-MFOS-PHASE09-FUZZ-*"]
implementation_allowed: false
downstream_packs: ["PACK-05", "PACK-06", "PACK-07", "PACK-08", "PACK-09", "PACK-15"]
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Phase 0.9 Fuzz Corpus Plan

Status: Phase 0.9 executable-spec artifact.

This document freezes fuzz-corpus planning for Phase 1. It does not implement
fuzzers, parser harnesses, semantic evaluators, service daemons, or production
code.

MFOS parser and fixture fuzzing is limited to independently specified MFOS
formats. Source references are used for design background and non-compatibility
boundaries only. Corpus files MUST NOT reproduce external command syntax,
record layouts, macro signatures, message tables, or documentation text.

## 1. Purpose

Phase 0.9 defines seed-corpus requirements for:

- Dataset-name parser inputs.
- MFOS job-control stream parser inputs.
- Operator command parser inputs.
- Policy-language parser inputs.
- Audit-record decoder inputs.
- Dataset-handle decoder inputs.
- Job fixture parser inputs.
- Spool fixture parser inputs.
- Cross-domain semantic fixture parser inputs.

The corpus plan is an executable-spec input. It is not a fuzz campaign, does
not run fuzzers, and does not prove parser safety by itself.

## 2. Corpus Rules

Each corpus target MUST have:

- `target_id` using `FUZZ-MFOS-*`.
- `target_name` using MFOS-owned names.
- `corpus_path`.
- `corpus_categories`.
- deterministic seed categories.
- implementation phase of Phase 1 or later.
- `implementation_allowed: false` in Phase 0.9.

Corpus entries MUST use symbolic timestamps, deterministic identifiers, and
MFOS-defined grammar fragments. Real host paths, process IDs, host users, wall
clock timestamps, and copied external syntax are prohibited.

## 3. Required Targets

The machine-readable plan is:

```text
fuzz/targets/fuzz-target-plan.yml
```

Required target names:

- `dsn-parser`
- `job-control-stream-parser`
- `operator-command-parser`
- `policy-language-parser`
- `audit-record-decoder`
- `dataset-handle-decoder`
- `job-fixture-parser`
- `spool-fixture-parser`
- `semantic-fixture-parser`

## 4. Seed Categories

Seed manifests under `fuzz/corpora/*/seed-plan.yml` define categories, not
runtime corpora. Phase 1 may turn them into concrete seed files after the
runner and parser contracts are approved.

Minimum categories:

- valid minimal input
- boundary length input
- invalid token
- malformed nesting
- unsupported feature
- explicit `SPEC_GAP` trigger
- denied operation fixture
- audit-before-return fixture where relevant

## 5. Exit Gate

Phase 0.9 passes this area only when:

- `scripts/validators/validate-fuzz-corpus-plan.py` passes.
- Naming-safety validation passes.
- No fuzzer implementation exists in Phase 0.9 outputs.
- Traceability maps fuzz targets to requirements.

## 6. Spec Gaps

`GAP-MFOS-PHASE09-FUZZ-0001`: concrete byte-level corpus files are deferred to
Phase 1 because Phase 0.9 freezes categories and contracts only.
