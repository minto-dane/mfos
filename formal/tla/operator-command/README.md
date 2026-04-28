# Operator Command Formal Artifact

Status: Phase 0.8 design model.

This directory freezes the operator command lifecycle as a formal state-machine
artifact. It models the safety properties required by
`docs/design/specs/10-operator-console.md`:

- no command executes without subject, target, authority, authorization, and
  required pre-effect audit;
- destructive commands cannot bypass confirmation or dual control;
- same-actor dual control cannot execute;
- automation cannot bypass the normal lifecycle;
- emergency mode cannot disable authorization or audit;
- root-shell-like input cannot become a successful operator command.

Source refs:

- `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`
- `EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001`
- `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`
- `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001`
- `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`

Files:

- `OperatorCommand.tla` defines the abstract state machine and invariants.
- `OperatorCommand.cfg` lists the invariant names for a future finite TLC
  harness.

This model does not choose concrete implementation data structures, parser
code, service APIs, or storage formats.
