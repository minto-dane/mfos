# Public-Safe Grounding Notes

## Review Position

The RACF artifacts map public IBM documentation topics to MFOS securityd design
needs. They intentionally omit RACF command syntax, macro signatures, database
fields, messages, record layouts, examples, tables, and administrative
procedures.

## Requirements Hooks

- `MFOS-REQ-AUTH-0001` through `MFOS-REQ-AUTH-0009` need securityd interface, profile, decision, rollback, stale-handle, and obligation tests.
- Audit hooks must connect denied and privileged security decisions to `auditd` without embedding IBM record formats.

## Negative Tests

- Security bypass and unauthorized operator command attempts must fail closed.
- Policy rollback must preserve audit evidence.
- Dataset stale handles must not retain access after policy or object generation changes.
- Public lint must reject claims that securityd is RACF-compatible.

## Key Gaps

- MFOS still needs a native access-authority taxonomy per resource class.
- securityd administrative language is undefined.
- Policy transaction rollback and policy-version binding need executable tests.
- RACF library page is bibliographic; deeper semantic extraction requires human source review without copying protected syntax or layouts.
