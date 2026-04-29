# Phase 1 Dafny Semantics Open Issues

Status: current  
Date: 2026-04-29

## Open Issues

1. Dafny toolchain is not installed locally.
   - Severity: Minor for artifact creation, blocker for verification-passed
     claim.
   - Required action: install/pin Dafny and record verification evidence.

2. Conformance harness currently performs structural comparison unless Dafny
   model output JSON is supplied.
   - Severity: Minor for current Phase 1 artifact creation.
   - Required action: after Dafny verification is available, add reviewed model
     output generation in non-production evidence paths.

No Critical or Major issues remain.
