# Catalog Transaction Model

Phase: 0.8 semantic freeze

This directory contains a compact TLA-style state-machine artifact for MFOS
catalog transactions and crash recovery. It is a design model, not production
code.

Source refs:

- `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`
- `EXTREF-IBM-ZOS-DFSMS-LIBRARY-0001`
- `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`

Modeled invariants:

- `MFOS-REQ-CATALOG-0002`: catalog resolve success is possible only for a
  committed, integrity-verified entry.
- Partial, rolled-back, torn, missing, and corrupt states never resolve.
- Protected transaction completion requires audit evidence.
- Recovery either rolls back incomplete state or reaches a verified committed
  state before resolution.

Evidence expectation:

- Model-check output or reviewed transition trace is required before any
  production implementation claims crash-recoverable catalog semantics.
