# MFOS Assurance Case Template v0.1

Use this template for every MFOS assurance claim, production readiness gate, High-Assurance root claim, or release claim. Do not use it to claim z/OS compatibility or IBM product compatibility.

## 1. Claim Header

```yaml
claim_id: MFOS-CLAIM-<PROFILE>-<DOMAIN>-<NNNN>
title: <short claim title>
profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
claim_level: CLAIM-L0 | CLAIM-L1 | CLAIM-L2 | CLAIM-L3 | CLAIM-L4 | CLAIM-L5
status: DRAFT | BLOCKED | REVIEWED | EVIDENCED | RETIRED
owner: <name or team>
reviewers:
  - <reviewer>
date_opened: YYYY-MM-DD
date_reviewed: YYYY-MM-DD?
```

## 2. Non-Compatibility Statement

```text
This claim describes MFOS source-grounded, z/OS-inspired semantics only.
It does not claim z/OS compatibility, z/Architecture compatibility,
IBM API compatibility, RACF compatibility, JES compatibility, DFSMS
compatibility, SMP/E compatibility, or IBM product compatibility.
```

## 3. Claim Statement

```text
MFOS claims that <subject> satisfies <property> for <profile/configuration>
under <assumptions>, with <evidence classes>, excluding <non-objectives>.
```

## 4. Source and Requirements

| Type | IDs / Links | Notes |
| --- | --- | --- |
| Source Matrix IDs | `<EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001>`, `<FBVBS-001>` | Include all source grounding. |
| Requirement IDs | `<MFOS-REQ-...>` | Include every applicable requirement. |
| Design specs | `<path#section>` | Link exact spec sections. |
| AI contract IDs | `<AI-MFOS-...>` | Include contract rules checked. |
| Production gates | `<PROD-...>` | Include if production claim. |

## 5. Scope

In scope:

- `<item>`

Out of scope:

- `<item>`

Applicable profiles:

- Baseline: `<yes/no + rationale>`
- Enterprise: `<yes/no + rationale>`
- High-Assurance: `<yes/no + rationale>`

## 6. Assumptions

| ID | Assumption | Impact if false | Evidence or owner |
| --- | --- | --- | --- |
| ASM-001 | `<assumption>` | `<impact>` | `<evidence>` |

## 7. Argument

Use concise, reviewable steps.

```text
ARG-001:
  Because <source/requirement> requires <property>,
  and <design> implements <mechanism>,
  and <tests/evidence> demonstrate <result>,
  the claim is supported for <profile>.
```

## 8. Invariants

```text
INV-<AREA>-001:
  <invariant>
```

## 9. Evidence Artifacts

| Artifact ID | Type | Path / Reference | Required for | Status |
| --- | --- | --- | --- | --- |
| EVD-001 | source matrix lint | `<path>` | CLAIM-L1 | missing |
| EVD-002 | positive test report | `<path>` | CLAIM-L2 | missing |
| EVD-003 | negative test report | `<path>` | CLAIM-L2 | missing |
| EVD-004 | fuzz report | `<path>` | parser/input boundary | missing |
| EVD-005 | code review | `<path>` | CLAIM-L3 | missing |
| EVD-006 | SBOM | `<path>` | Enterprise+ | missing |
| EVD-007 | signed provenance | `<path>` | Enterprise+ | missing |
| EVD-008 | Guard evidence | `<path>` | High-Assurance | missing |

Evidence artifact types:

- design evidence.
- test evidence.
- negative test evidence.
- fuzz evidence.
- review evidence.
- audit evidence.
- supply-chain evidence.
- formal evidence.
- Guard evidence.
- recovery evidence.

## 10. Tests

Positive tests:

- `<test_name>`

Negative tests:

- `<test_name>`

Fuzz targets:

- `<fuzz_target>`

Fault-injection or crash-recovery tests:

- `<test_name>`

Required negative categories checked:

- unauthorized access.
- stale handle.
- policy version mismatch.
- audit write failure.
- malformed input.
- replay attempt.
- downgrade attempt.
- concurrent update.
- crash mid-transaction.
- recovery consistency.
- privilege confusion.
- cross-partition misuse.
- AMF revoked signer.
- Guard root mismatch.
- unsupported command success attempt.

## 11. Audit Obligations

| Operation | Audit record required | Ordering requirement | Evidence |
| --- | --- | --- | --- |
| `<operation>` | yes | DENY before caller result | `<audit evidence>` |

## 12. Review Checklist

Claim review:

- [ ] Claim has profile.
- [ ] Claim has source matrix IDs.
- [ ] Claim has requirement IDs.
- [ ] Claim has non-compatibility statement.
- [ ] Claim separates Baseline, Enterprise-Standalone, Enterprise-PXM, and High-Assurance.
- [ ] Claim lists assumptions.
- [ ] Claim lists non-objectives.
- [ ] Claim lists unsupported features.
- [ ] Claim lists spec gaps.
- [ ] Claim lists residual risks.

Security review:

- [ ] securityd is final PDP where required.
- [ ] auditd obligation is present.
- [ ] DENY-before-result is tested where applicable.
- [ ] no fake success path exists.
- [ ] UNSUPPORTED and SPEC_GAP are separated.
- [ ] stale handles are rejected.
- [ ] policy version mismatch is rejected.
- [ ] malformed input is rejected.
- [ ] revocation or rollback paths fail closed.

Release review:

- [ ] production gates are complete if production is claimed.
- [ ] SBOM exists if Enterprise or higher is claimed.
- [ ] signed provenance exists if Enterprise or higher is claimed.
- [ ] Guard evidence exists if High-Assurance is claimed.
- [ ] compatibility wording review is clean.

## 13. Production Readiness Mapping

| Gate | Applies | Status | Evidence |
| --- | --- | --- | --- |
| PROD-001 | yes/no | PASS/FAIL/N/A | `<evidence>` |
| PROD-002 | yes/no | PASS/FAIL/N/A | `<evidence>` |
| PROD-003 | yes/no | PASS/FAIL/N/A | `<evidence>` |
| PROD-004 | yes/no | PASS/FAIL/N/A | `<evidence>` |
| PROD-005 | yes/no | PASS/FAIL/N/A | `<evidence>` |
| PROD-006 | yes/no | PASS/FAIL/N/A | `<evidence>` |
| PROD-007 | yes/no | PASS/FAIL/N/A | `<evidence>` |
| PROD-008 | yes/no | PASS/FAIL/N/A | `<evidence>` |
| PROD-009 | yes/no | PASS/FAIL/N/A | `<evidence>` |
| PROD-010 | yes/no | PASS/FAIL/N/A | `<evidence>` |
| PROD-011 | yes/no | PASS/FAIL/N/A | `<evidence>` |
| PROD-012 | yes/no | PASS/FAIL/N/A | `<evidence>` |
| PROD-013 | yes/no | PASS/FAIL/N/A | `<evidence>` |
| PROD-014 | yes/no | PASS/FAIL/N/A | `<evidence>` |
| PROD-015 | yes/no | PASS/FAIL/N/A | `<evidence>` |

## 14. Unsupported Features

| Feature | Status | Required failure mode | Tests |
| --- | --- | --- | --- |
| `<feature>` | UNSUPPORTED | fail closed with typed error | `<test>` |

## 15. Spec Gaps

| Gap ID | Description | Blocked claims | Required decision |
| --- | --- | --- | --- |
| GAP-001 | `<gap>` | `<claim IDs>` | `<decision>` |

## 16. Residual Risks

| Risk ID | Risk | Severity | Mitigation | Accepted by |
| --- | --- | --- | --- | --- |
| RISK-001 | `<risk>` | Critical/High/Medium/Low | `<mitigation>` | `<owner>` |

## 17. AI Output Block

When an AI agent implements or reviews work for this claim, it must return:

```text
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
```
