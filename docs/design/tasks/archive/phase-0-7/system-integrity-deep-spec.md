# Phase 0.7 System Integrity Deep Spec

Status: In Progress  
Created: 2026-04-27  
Primary machine-readable plan: `tasks/archive/phase-0-7/system-integrity-deep-spec.yml`

Phase 0.7 deepens `docs/design/specs/03-system-integrity.md` after the Phase
0.6 validation infrastructure pass. It remains a specification phase, not a
production implementation phase.

This Markdown bridge mirrors the machine-readable task status, which is
currently `in_progress`.

## Goals

- Stabilize the complete system integrity specification body.
- Expand system-integrity requirements beyond the v0.5 priority seed.
- Register negative tests for the system interfaces and protected-resource
  boundaries that support the claim.
- Separate planned evidence from verified evidence.
- Tighten Source Card section/version pins without copying external documents.
- Advance Japanese mirror mechanics while keeping English canonical.

## Implementation Gate

Production implementation remains blocked. Hosted semantic prototype work is
allowed only for packs that pass the pre-implementation gate and declare:

```yaml
implementation_profile: hosted_semantic_prototype
production_claim: false
hardware_enforcement_claim: false
system_integrity_claim: semantic_only
```

## Exit Criteria

- `03-system-integrity.md` contains or links every required Phase 0.7 section.
- System-integrity requirements have registered positive and negative tests.
- Audit obligations for system-integrity denies are registered before-return.
- Traceability gap report has no high gaps for system-integrity scope.
- Red Team review has no Critical or High findings for system-integrity scope.

## Current Snapshot

Validation was rerun on 2026-04-27 after the registry expansion.

```yaml
requirements: 106
tests: 261
evidence: 170
source_cards: 37
claims: 5
packs: 31
traceability_gap_groups: 0
high_traceability_gap_groups: 0
registry_link_warnings: 0
draft_evidence_records: 170
release_claims_allowed: false
production_implementation_allowed: false
```

The traceability registry coverage gaps are currently closed, but Phase 0.7 is
not complete. The remaining blockers are specification review, source-card pin
review where local metadata remains weak, and replacement of draft evidence
placeholders with verified evidence before any release claim.
