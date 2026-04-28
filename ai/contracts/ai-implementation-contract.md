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

Hosted prototype work is allowed only for packs that pass the
pre-implementation gate and must be labeled:

```yaml
implementation_profile: hosted_semantic_prototype
production_claim: false
hardware_enforcement_claim: false
system_integrity_claim: semantic_only
```

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

