# Component Scaffold Remediation

Status: current

Added `.mfos-dir.yml` metadata for key canonical, bridge, validation, test,
source, and future implementation scaffold roots. The metadata records role,
maturity, status, canonical authority, allowed contents, forbidden contents,
and implementation permissions.

The new validator rejects Phase 0.x metadata that enables production, hosted
daemon, semantic runner, portable semantic core, or hosted semantic prototype
implementation.
