# Dafny Authorization/Audit Open Issues

Status: current.

- Formal claim registry remains `proof_claimed: false`; claim-level proof-backed coverage is deferred to a formal-assurance closure task.
- REQUIRE_* conformance fixtures are linked only to pending-decision properties where the Phase 0.9 golden files describe final allow states; a later conformance execution pass should model evidence-satisfaction transitions before upgrading those entries to C5.
