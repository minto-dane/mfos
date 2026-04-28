---
spec_id: "MFOS-SPEC-39-LANGUAGE-AND-VERIFICATION-POLICY"
title: "MFOS Language and Verification Policy"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS assurance architecture"
last_reviewed: "2026-04-28"
source_refs: ["X64-INTEL-001", "X64-AMD-001", "X64-LINUX-CET-001", "X64-LINUX-PKU-001", "NIST-160-001", "NIST-218-001", "FBVBS-001"]
requirement_refs: ["MFOS-REQ-LANG-*", "MFOS-REQ-FORMAL-*", "MFOS-REQ-ASSURANCE-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS Language and Verification Policy

Status: Draft scaffold. This document reserves verification policy vocabulary.
It does not authorize production code, unsafe-code decisions, proof claims, or
toolchain enforcement claims.

## 1. Purpose

MFOS needs explicit language and verification policy before implementation work
can be assigned. This spec records the future policy areas and keeps hardware
features and proof tools from being treated as primary policy definitions.

## 2. Source References

- `X64-INTEL-001`
- `X64-AMD-001`
- `X64-LINUX-CET-001`
- `X64-LINUX-PKU-001`
- `NIST-160-001`
- `NIST-218-001`
- `FBVBS-001`

These sources inform hardware-feature constraints, secure engineering, secure
development, and assurance discipline. They do not establish MFOS safety,
control-flow integrity, or proof coverage by themselves.

## 3. Reserved Policy Areas

Future `MFOS-REQ-LANG-*`, `MFOS-REQ-FORMAL-*`, and
`MFOS-REQ-ASSURANCE-*` requirements may cover:

- safe-language default policy
- unsafe boundary review
- assembly boundary contracts
- no-std and freestanding runtime constraints
- control-flow integrity policy
- hardware control-flow aid policy
- memory-protection aid policy
- model-checking harness policy
- proof obligation acceptance criteria
- verified artifact evidence

## 4. Non-Claims

MFOS does not currently claim:

- complete memory safety
- complete control-flow integrity
- verified kernel correctness
- verified authorization correctness
- verified audit-chain correctness
- production proof coverage

## 5. Spec Gaps

`GAP-MFOS-LANG-0001`: final implementation language profile and unsafe-code
policy are not frozen.

`GAP-MFOS-LANG-0002`: proof-tool selection and CI acceptance criteria are not
frozen.
