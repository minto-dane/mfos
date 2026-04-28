# Audit Append State Machine

Status: Phase 0.8 design artifact

This directory owns the abstract audit append state machine for `MFOS-SPEC-07-AUDIT`. It models design-level ordering and invalid transitions only. It does not define storage layout, serialization, cryptographic implementation, remote export protocol, or Guard ABI.

Source references are limited to:

- EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001
- EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001
- EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
- EXTREF-IBM-ZOS-SECURITY-SERVER-0001
- EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001

Required invariants:

- Required audit cannot return to caller before durable append.
- High-Assurance audit-root evidence cannot be claimed before Guard sealing.
- Query/export results cannot be returned before `securityd` authorization.
- Committed records are immutable; redaction is a view transform only.
- Logs, console output, spool entries, and spool output are outside the evidence state machine.
