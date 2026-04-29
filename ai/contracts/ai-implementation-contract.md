# MFOS AI Implementation Contract

Status: Draft  
Canonical language: English

AI agents must treat implementation as downstream of Source Cards,
requirements, specs, tests, evidence, and pack contracts.

## Required Output Sections

Every implementation or review response must include:

1. Implemented Requirement IDs
2. Source Matrix IDs
3. Assumptions
4. Spec Gaps
5. Unsupported Features
6. Security Invariants
7. Audit Obligations
8. Failure Modes
9. Tests Added
10. Negative Tests Added
11. Fuzz Targets Added
12. Unsafe Code Justification
13. Review Checklist
14. Evidence Artifacts

## Pre-Implementation Gate

Before production code is written for a component, the assigned pack must
contain:

- Requirement IDs
- Source Matrix IDs
- Object model
- State machine
- Failure modes
- Audit obligations
- Positive tests
- Negative tests
- `MFOS_ERR_UNSUPPORTED` and `MFOS_ERR_SPEC_GAP` behavior
- Fuzz target decision
- Evidence artifact path
- Claim boundary
- Pack contract
- Red-team review

If any item is missing, the implementation agent must produce a
`SPEC_GAP_REPORT` instead of code.

## Hosted Semantic Prototype Label

Hosted prototype work is not allowed in Phase 1. Phase 1 is limited to
non-production Dafny executable-semantics artifacts and conformance-harness
validation under `formal/executable-semantics/dafny/` and `tools/`.

Hosted prototype work may be considered only after a later reviewed gate for
packs that pass the pre-implementation gate, and it must be labeled:

```yaml
implementation_profile: hosted_semantic_prototype
production_claim: false
hardware_enforcement_claim: false
system_integrity_claim: semantic_only
```

This label does not authorize Rust semantic-core work, semantic-runner commands,
hosted daemons, production services, PXM/MFVM/CVM implementation, cluster
implementation, or Dafny-generated production code.

## Prohibited Patterns

- fake success
- empty stubs
- silent fallback
- treating `SPEC_GAP` as success
- treating `UNSUPPORTED` as success
- bypassing `securityd`
- bypassing `auditd`
- introducing IBM-derived semantics without Source Matrix IDs
- making compatibility claims
