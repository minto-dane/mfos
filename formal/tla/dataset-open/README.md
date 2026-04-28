# Dataset Open Model

Phase: 0.8 semantic freeze

This directory contains a compact TLA-style state-machine artifact for MFOS
dataset open semantics. It is a design model, not production code.

Source refs:

- `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`
- `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001`
- `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`
- `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001`

Modeled invariants:

- No active handle without committed catalog resolution.
- No active handle without an ALLOW decision.
- No active handle without required audit being appended.
- No active handle without object generation binding.
- Denied or failed-closed paths create no handle.

Evidence expectation:

- Model-check output or reviewed transition trace is required before any
  production implementation claims these semantics.
