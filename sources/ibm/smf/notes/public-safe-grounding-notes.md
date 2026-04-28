# Public-Safe Grounding Notes

## Review Position

The SMF artifacts are deliberately metadata-only. They do not store IBM record
layouts, field names, event-code tables, examples, macro signatures, command
syntax, diagrams, or HTML/PDF mirrors. The type 80 page is used only to ground
the existence and review scope of security-event auditing.

## Requirements Hooks

- `MFOS-REQ-AUDIT-0001` through `MFOS-REQ-AUDIT-0005` need schema, tamper, retention, query authorization, failure-policy, and export tests.
- Security decision events need reason-code and policy-version normalization across MFOS services.

## Negative Tests

- Tamper-chain validation must detect modified, reordered, or missing audit records.
- Fail-closed profiles must block protected operations when required audit submission is unavailable.
- DENY-before-return obligations must be enforced for configured security decisions.
- Public lint must reject SMF and RACF type 80 compatibility claims.

## Key Gaps

- MFOS audit record encoding is still undefined.
- Retention and query-authorization policy need a normative spec.
- Reason-code taxonomy is not normalized across securityd, jobd, datasetd, spoold, and operatord.
- Human review must ensure no IBM record-layout fields or event-code tables are imported later.
