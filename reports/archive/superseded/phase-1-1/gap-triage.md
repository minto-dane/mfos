# Phase 1.1 Gap Triage

Status: superseded by Phase 1.2 Authorization/Audit closure for PR #19.

This triage classifies every remaining C0/C2/C3 Phase 1.1 semantic coverage gap after PR #18 merge. It does not implement Phase 1.2 and does not raise any coverage level.

## Summary

- `phase_1_1_semantic_coverage_complete`: `False`
- `phase_1_2_entry_allowed`: `True`
- `phase_1_2_merge_allowed`: `False`
- `authorization_audit_gap_count`: `28`
- `authorization_audit_deferred_count`: `0`
- `phase_1_2_entry_blocker_count`: `0`
- `phase_1_2_merge_blocker_count`: `28`
- `formal_claims_without_proof_artifacts_treated_as_c4_c5`: `False`

## Classification Counts

```yaml
classification_counts:
  fix_before_next_merge: 28
  accepted_deferred: 41
coverage_level_counts:
  C3_FULL_SEMANTIC: 18
  C2_PARTIAL_SEMANTIC: 14
  C0_NONE: 37
artifact_kind_counts:
  test: 42
  requirement: 16
  formal_claim: 11
```

## Authorization / Audit Gaps

Authorization and Audit gaps are not deferred. They are classified as `fix_before_next_merge`: Phase 1.2 may begin, but a Phase 1.2 PR must close or explicitly re-scope them before merge.

| artifact_kind | artifact_id | domain | coverage_level | classification | phase_1_2_entry_blocker | phase_1_2_merge_blocker |
| --- | --- | --- | --- | --- | --- | --- |
| test | TEST-MFOS-AUTH-ALLOW-0901 | authorization | C3_FULL_SEMANTIC | fix_before_next_merge | false | true |
| test | TEST-MFOS-AUTH-ALLOW-WITH-AUDIT-0903 | authorization | C3_FULL_SEMANTIC | fix_before_next_merge | false | true |
| test | TEST-MFOS-AUTH-REQUIRE-MFA-0904 | authorization | C2_PARTIAL_SEMANTIC | fix_before_next_merge | false | true |
| test | TEST-MFOS-AUTH-REQUIRE-DUAL-CONTROL-0905 | authorization | C2_PARTIAL_SEMANTIC | fix_before_next_merge | false | true |
| test | TEST-MFOS-AUTH-REQUIRE-BREAK-GLASS-0906 | authorization | C2_PARTIAL_SEMANTIC | fix_before_next_merge | false | true |
| test | TEST-MFOS-AUTH-REQUIRE-GUARD-APPROVAL-0907 | authorization | C2_PARTIAL_SEMANTIC | fix_before_next_merge | false | true |
| test | TEST-MFOS-AUTH-REQUIRE-OPERATOR-CONFIRMATION-0908 | authorization | C2_PARTIAL_SEMANTIC | fix_before_next_merge | false | true |
| test | NEG-MFOS-AUTH-STALE-POLICY-0920 | authorization | C3_FULL_SEMANTIC | fix_before_next_merge | false | true |
| test | NEG-MFOS-AUTH-EXPIRED-DELEGATION-0921 | authorization | C0_NONE | fix_before_next_merge | false | true |
| test | NEG-MFOS-AUTH-BREAK-GLASS-NO-REASON-0922 | authorization | C2_PARTIAL_SEMANTIC | fix_before_next_merge | false | true |
| test | NEG-MFOS-AUTH-BREAK-GLASS-NO-EXPIRY-0923 | authorization | C2_PARTIAL_SEMANTIC | fix_before_next_merge | false | true |
| test | NEG-MFOS-AUTH-POLICY-LINT-WILDCARD-0924 | authorization | C0_NONE | fix_before_next_merge | false | true |
| test | TEST-MFOS-AUDIT-MINIMUM-FIELDS-0902 | audit | C3_FULL_SEMANTIC | fix_before_next_merge | false | true |
| test | NEG-MFOS-AUDIT-MISSING-CORRELATION-0903 | audit | C2_PARTIAL_SEMANTIC | fix_before_next_merge | false | true |
| test | TEST-MFOS-AUDIT-HASH-CHAIN-VALID-0904 | audit | C3_FULL_SEMANTIC | fix_before_next_merge | false | true |
| test | NEG-MFOS-AUDIT-HASH-CHAIN-TAMPERED-0905 | audit | C2_PARTIAL_SEMANTIC | fix_before_next_merge | false | true |
| test | NEG-MFOS-AUDIT-UNAUTHORIZED-QUERY-0907 | audit | C0_NONE | fix_before_next_merge | false | true |
| test | NEG-MFOS-AUDIT-REDACTION-FAILURE-0910 | audit | C0_NONE | fix_before_next_merge | false | true |
| test | NEG-MFOS-AUDIT-DUPLICATE-RECORD-ID-0911 | audit | C0_NONE | fix_before_next_merge | false | true |
| test | NEG-MFOS-AUDIT-NON-MONOTONIC-SEQUENCE-0912 | audit | C2_PARTIAL_SEMANTIC | fix_before_next_merge | false | true |
| requirement | MFOS-REQ-AUDIT-0001 | audit | C0_NONE | fix_before_next_merge | false | true |
| requirement | MFOS-REQ-AUDIT-0002 | audit | C0_NONE | fix_before_next_merge | false | true |
| requirement | MFOS-REQ-AUDIT-0101 | audit | C0_NONE | fix_before_next_merge | false | true |
| requirement | MFOS-REQ-AUTH-0001 | authorization | C0_NONE | fix_before_next_merge | false | true |
| requirement | MFOS-REQ-AUTH-0003 | authorization | C0_NONE | fix_before_next_merge | false | true |
| requirement | MFOS-REQ-AUTH-0101 | authorization | C0_NONE | fix_before_next_merge | false | true |
| formal_claim | MFOS-FC-AUTHORIZATION-NO-HANDLE-WITHOUT-ALLOW | authorization | C3_FULL_SEMANTIC | fix_before_next_merge | false | true |
| formal_claim | MFOS-FC-AUDIT-DENY-BEFORE-RETURN | audit | C3_FULL_SEMANTIC | fix_before_next_merge | false | true |

## Deferred Non-Phase-1.2 Gaps

Non-Authorization/Audit gaps are accepted as truthful deferred work for later domain-deepening phases. They remain visible and are not treated as successful coverage.

| artifact_kind | artifact_id | domain | coverage_level | classification | phase_1_2_entry_blocker | phase_1_2_merge_blocker |
| --- | --- | --- | --- | --- | --- | --- |
| test | TEST-MFOS-DATASET-VALID-DSN-0901 | dataset_catalog | C3_FULL_SEMANTIC | accepted_deferred | false | false |
| test | NEG-MFOS-DATASET-MALFORMED-DSN-0902 | dataset_catalog | C2_PARTIAL_SEMANTIC | accepted_deferred | false | false |
| test | TEST-MFOS-DATASET-CATALOG-COMMITTED-0903 | dataset_catalog | C3_FULL_SEMANTIC | accepted_deferred | false | false |
| test | NEG-MFOS-DATASET-RETENTION-DELETE-0911 | dataset_catalog | C3_FULL_SEMANTIC | accepted_deferred | false | false |
| test | NEG-MFOS-DATASET-IMMUTABLE-SYSTEM-0912 | dataset_catalog | C3_FULL_SEMANTIC | accepted_deferred | false | false |
| test | NEG-MFOS-DATASET-NOT-POSIX-FILE-0913 | dataset_catalog | C0_NONE | accepted_deferred | false | false |
| test | TEST-MFOS-DATASET-CRASH-MID-COMMIT-0914 | dataset_catalog | C2_PARTIAL_SEMANTIC | accepted_deferred | false | false |
| test | TEST-MFOS-JOB-HELLO-JOB-0901 | job_spool | C3_FULL_SEMANTIC | accepted_deferred | false | false |
| test | NEG-MFOS-JOB-MALFORMED-CONTROL-0902 | job_spool | C0_NONE | accepted_deferred | false | false |
| test | NEG-MFOS-JOB-SUBMIT-NO-PRINCIPAL-0903 | job_spool | C2_PARTIAL_SEMANTIC | accepted_deferred | false | false |
| test | TEST-MFOS-JOB-STEP-FAILURE-RC-0909 | job_spool | C2_PARTIAL_SEMANTIC | accepted_deferred | false | false |
| test | TEST-MFOS-JOB-SPOOL-CREATE-0911 | job_spool | C3_FULL_SEMANTIC | accepted_deferred | false | false |
| test | TEST-MFOS-JOB-SPOOL-BROWSE-OWNER-0912 | job_spool | C3_FULL_SEMANTIC | accepted_deferred | false | false |
| test | NEG-MFOS-JOB-SPOOL-EXPORT-NO-AUDIT-0915 | job_spool | C0_NONE | accepted_deferred | false | false |
| test | NEG-MFOS-JOB-CANCEL-NO-AUTHORITY-0916 | job_spool | C0_NONE | accepted_deferred | false | false |
| test | NEG-MFOS-JOB-STEP-NO-AUDIT-CORRELATION-0917 | job_spool | C0_NONE | accepted_deferred | false | false |
| test | TEST-MFOS-OPER-DISPLAY-SYSTEM-0901 | operator_console | C3_FULL_SEMANTIC | accepted_deferred | false | false |
| test | TEST-MFOS-OPER-DEFINE-USER-0902 | operator_console | C3_FULL_SEMANTIC | accepted_deferred | false | false |
| test | TEST-MFOS-OPER-DEFINE-DATASET-0903 | operator_console | C3_FULL_SEMANTIC | accepted_deferred | false | false |
| test | TEST-MFOS-OPER-SUBMIT-JOB-0904 | operator_console | C3_FULL_SEMANTIC | accepted_deferred | false | false |
| test | NEG-MFOS-OPER-AUTOMATION-BYPASS-0910 | operator_console | C0_NONE | accepted_deferred | false | false |
| test | NEG-MFOS-OPER-MALFORMED-COMMAND-0911 | operator_console | C0_NONE | accepted_deferred | false | false |
| requirement | MFOS-REQ-CATALOG-0002 | non_phase_1_2_domain | C0_NONE | accepted_deferred | false | false |
| requirement | MFOS-REQ-CATALOG-0101 | non_phase_1_2_domain | C0_NONE | accepted_deferred | false | false |
| requirement | MFOS-REQ-DATASET-0101 | non_phase_1_2_domain | C0_NONE | accepted_deferred | false | false |
| requirement | MFOS-REQ-DATASET-0102 | non_phase_1_2_domain | C0_NONE | accepted_deferred | false | false |
| requirement | MFOS-REQ-JOB-0101 | non_phase_1_2_domain | C0_NONE | accepted_deferred | false | false |
| requirement | MFOS-REQ-JOB-0102 | non_phase_1_2_domain | C0_NONE | accepted_deferred | false | false |
| requirement | MFOS-REQ-OPER-0101 | non_phase_1_2_domain | C0_NONE | accepted_deferred | false | false |
| requirement | MFOS-REQ-OPER-0102 | non_phase_1_2_domain | C0_NONE | accepted_deferred | false | false |
| requirement | MFOS-REQ-OPER-0103 | non_phase_1_2_domain | C0_NONE | accepted_deferred | false | false |
| requirement | MFOS-REQ-SPOOL-0101 | non_phase_1_2_domain | C0_NONE | accepted_deferred | false | false |
| formal_claim | MFOS-FC-UPDATE-NO-ROLLBACK | non_phase_1_2_domain | C0_NONE | accepted_deferred | false | false |
| formal_claim | MFOS-FC-PARTITION-MEMORY-OWNERSHIP | non_phase_1_2_domain | C0_NONE | accepted_deferred | false | false |
| formal_claim | MFOS-FC-PXM-CAPABILITY-REQUIRED-FOR-RESOURCE-OPERATION | non_phase_1_2_domain | C0_NONE | accepted_deferred | false | false |
| formal_claim | MFOS-FC-MFVM-CANNOT-BYPASS-PXM | non_phase_1_2_domain | C0_NONE | accepted_deferred | false | false |
| formal_claim | MFOS-FC-CVM-LAUNCH-REQUIRES-MEASUREMENT | non_phase_1_2_domain | C0_NONE | accepted_deferred | false | false |
| formal_claim | MFOS-FC-CVM-SECRET-RELEASE-REQUIRES-ATTESTATION | non_phase_1_2_domain | C0_NONE | accepted_deferred | false | false |
| formal_claim | MFOS-FC-PRIVATE-SHARED-MEMORY-TRANSITION-VALIDITY | non_phase_1_2_domain | C0_NONE | accepted_deferred | false | false |
| formal_claim | MFOS-FC-CLUSTER-POLICY-DISTRIBUTION-INTEGRITY | non_phase_1_2_domain | C0_NONE | accepted_deferred | false | false |
| formal_claim | MFOS-FC-CLUSTER-ATTESTATION-COLLECTION-INTEGRITY | non_phase_1_2_domain | C0_NONE | accepted_deferred | false | false |

## Validator Decision

No new validator is required in this triage because PR #18 already added `scripts/check-semantic-coverage-mapping.py` and `scripts/check-formal-claim-coverage.py`, and `validate-all.sh` runs both. These gates prevent the reviewed overclaim classes from recurring.

## Stop Rule Result

- No Authorization/Audit gap is classified `accepted_deferred`.
- No Authorization/Audit gap blocks Phase 1.2 entry.
- Authorization/Audit gaps are Phase 1.2 merge/exit blockers until closed or re-scoped in the Phase 1.2 PR.
