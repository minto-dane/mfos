# Hosted Semantic Prototype

Future hosted semantic prototype scaffold. It is not currently authorized for
Phase 1; Phase 1 remains limited to loader-only artifact validation and
traceability repair until source-grounding and semantic-evaluator gates close.

When a later phase explicitly authorizes a hosted semantic prototype, it must
run on a host OS only with labels equivalent to:

```text
implementation_profile: hosted_semantic_prototype
production_claim: false
hardware_enforcement_claim: false
system_integrity_claim: semantic_only
```

AMF production load remains disabled and returns `MFOS_ERR_UNSUPPORTED`.
