# Phase 1.2 Entry Gate

Phase 1.2 may begin as a non-production Dafny Authorization/Audit Deepening task. This is an entry decision only, not permission to merge or exit incomplete Phase 1.2 work.

## Decision

- `phase_1_2_allowed`: `true`
- `authorization_audit_entry_blockers_remaining`: `false`
- `authorization_audit_merge_blockers_remaining`: `true`
- Authorization/Audit C0/C2/C3 gaps are not deferred; they are Phase 1.2 merge-gate work items.

## Allowed Scope

- Dafny authorization semantic deepening
- Dafny audit semantic deepening
- fixture/oracle/golden traceability updates for authorization/audit
- non-production proof/lemma strengthening
- reports and validation updates

## Forbidden Scope

- production implementation
- Rust semantic-core
- hosted daemon
- production-like semantic runner
- securityd/auditd/catalogd/datasetd/jobd/spoold/operatord implementation
- nucleus/PXM/Guard/MFVM/CVM/cluster implementation

## Required Before Phase 1.2 Merge

- Close or explicitly re-scope every Authorization/Audit fix_before_next_merge gap
- Keep formal claims below C4/C5 unless proof artifacts exist
- Run full validation including semantic coverage mapping and formal claim coverage checks

## Merge Blockers

| artifact_kind | artifact_id | domain | coverage_level | classification |
| --- | --- | --- | --- | --- |
| test | TEST-MFOS-AUTH-ALLOW-0901 | authorization | C3_FULL_SEMANTIC | fix_before_next_merge |
| test | TEST-MFOS-AUTH-ALLOW-WITH-AUDIT-0903 | authorization | C3_FULL_SEMANTIC | fix_before_next_merge |
| test | TEST-MFOS-AUTH-REQUIRE-MFA-0904 | authorization | C2_PARTIAL_SEMANTIC | fix_before_next_merge |
| test | TEST-MFOS-AUTH-REQUIRE-DUAL-CONTROL-0905 | authorization | C2_PARTIAL_SEMANTIC | fix_before_next_merge |
| test | TEST-MFOS-AUTH-REQUIRE-BREAK-GLASS-0906 | authorization | C2_PARTIAL_SEMANTIC | fix_before_next_merge |
| test | TEST-MFOS-AUTH-REQUIRE-GUARD-APPROVAL-0907 | authorization | C2_PARTIAL_SEMANTIC | fix_before_next_merge |
| test | TEST-MFOS-AUTH-REQUIRE-OPERATOR-CONFIRMATION-0908 | authorization | C2_PARTIAL_SEMANTIC | fix_before_next_merge |
| test | NEG-MFOS-AUTH-STALE-POLICY-0920 | authorization | C3_FULL_SEMANTIC | fix_before_next_merge |
| test | NEG-MFOS-AUTH-EXPIRED-DELEGATION-0921 | authorization | C0_NONE | fix_before_next_merge |
| test | NEG-MFOS-AUTH-BREAK-GLASS-NO-REASON-0922 | authorization | C2_PARTIAL_SEMANTIC | fix_before_next_merge |
| test | NEG-MFOS-AUTH-BREAK-GLASS-NO-EXPIRY-0923 | authorization | C2_PARTIAL_SEMANTIC | fix_before_next_merge |
| test | NEG-MFOS-AUTH-POLICY-LINT-WILDCARD-0924 | authorization | C0_NONE | fix_before_next_merge |
| test | TEST-MFOS-AUDIT-MINIMUM-FIELDS-0902 | audit | C3_FULL_SEMANTIC | fix_before_next_merge |
| test | NEG-MFOS-AUDIT-MISSING-CORRELATION-0903 | audit | C2_PARTIAL_SEMANTIC | fix_before_next_merge |
| test | TEST-MFOS-AUDIT-HASH-CHAIN-VALID-0904 | audit | C3_FULL_SEMANTIC | fix_before_next_merge |
| test | NEG-MFOS-AUDIT-HASH-CHAIN-TAMPERED-0905 | audit | C2_PARTIAL_SEMANTIC | fix_before_next_merge |
| test | NEG-MFOS-AUDIT-UNAUTHORIZED-QUERY-0907 | audit | C0_NONE | fix_before_next_merge |
| test | NEG-MFOS-AUDIT-REDACTION-FAILURE-0910 | audit | C0_NONE | fix_before_next_merge |
| test | NEG-MFOS-AUDIT-DUPLICATE-RECORD-ID-0911 | audit | C0_NONE | fix_before_next_merge |
| test | NEG-MFOS-AUDIT-NON-MONOTONIC-SEQUENCE-0912 | audit | C2_PARTIAL_SEMANTIC | fix_before_next_merge |
| requirement | MFOS-REQ-AUDIT-0001 | audit | C0_NONE | fix_before_next_merge |
| requirement | MFOS-REQ-AUDIT-0002 | audit | C0_NONE | fix_before_next_merge |
| requirement | MFOS-REQ-AUDIT-0101 | audit | C0_NONE | fix_before_next_merge |
| requirement | MFOS-REQ-AUTH-0001 | authorization | C0_NONE | fix_before_next_merge |
| requirement | MFOS-REQ-AUTH-0003 | authorization | C0_NONE | fix_before_next_merge |
| requirement | MFOS-REQ-AUTH-0101 | authorization | C0_NONE | fix_before_next_merge |
| formal_claim | MFOS-FC-AUTHORIZATION-NO-HANDLE-WITHOUT-ALLOW | authorization | C3_FULL_SEMANTIC | fix_before_next_merge |
| formal_claim | MFOS-FC-AUDIT-DENY-BEFORE-RETURN | audit | C3_FULL_SEMANTIC | fix_before_next_merge |
