---
concept_id: INT-FBVBS-CONCEPT-STATE-MACHINE-PRECONDITION-0001
source_ids:
  - INT-FBVBS-PARTITION-STATE-MACHINE-0001
source_terms:
  - partition lifecycle
  - command contract
  - transition precondition
summary: Short MFOS-facing abstraction of guarded lifecycle mutation.
mfos_terms:
  - MFOS lifecycle object
  - MFOS command contract
  - MFOS postcondition evidence
mfos_mapping:
  overlap:
    - explicit source-state allowlists
    - artifact preconditions
  divergence:
    - MFOS lifecycle graph and object names are independent
mfos_divergence:
  - MFOS must not reuse FBVBS state names as normative terms without ADR review.
requirements:
  - unassigned-preparatory
negative_tests:
  - mutation with no allowed source-state list
  - recovery without approval artifact
prohibited_inference:
  - Do not infer MFOS state-machine completeness from FBVBS partition examples.
review_status: draft
citation_scope: source-card-id-only
cache_disposition: temporary_ignored_cache
legal_controls:
  public_safe: true
  no_affiliation_claim: true
  no_compatibility_claim: true
  no_conformance_claim: true
  no_certification_claim: true
  no_source_substitution: true
---

# Concept Card: State-Machine Precondition Discipline

Concept:

Mutating commands must be legal only from explicit source states, with explicit artifact preconditions and postcondition evidence.

MFOS pattern:

1. Publish the authoritative lifecycle graph for each managed object.
2. Give every mutation a command contract.
3. Include allowed source states, required artifacts, repeat behavior, and predicted failure reasons.
4. Run a precondition validator before operator tooling issues the command.
5. Run a postcondition validator after teardown, detach, revoke, or destroy.

Derived from:

- `source-cards/020-partition-state-machine-discipline.md`

MFOS implementation sketch:

```json
{
  "operation": "object-recover",
  "allowed_source_states": ["FAULTED"],
  "required_artifacts": ["recovery-approval"],
  "repeat_semantics": "single-transition",
  "postconditions": ["object-runnable", "approval-bound-to-session"]
}
```

Anti-patterns:

- Operator-only transition rules.
- Recovery without approval material.
- Destroy/detach paths without stale-visibility checks.
