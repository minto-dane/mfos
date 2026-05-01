# Dafny Authorization/Audit Open Issues

Status: current.

- Formal claim registry remains `proof_claimed: false`; claim-level proof-backed coverage is deferred to a formal-assurance closure task.
- REQUIRE_* authorization scenarios remain below C5 because Phase 1.2 links them only to verified pending-decision Dafny properties; a later conformance execution pass should model evidence-satisfaction transitions before upgrading those entries to C5.
