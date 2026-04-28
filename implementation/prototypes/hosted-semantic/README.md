# Hosted Semantic Prototype

Phase 1 semantics-only prototype. It may run on a host OS but must be labeled:

```text
implementation_profile: hosted_semantic_prototype
production_claim: false
hardware_enforcement_claim: false
system_integrity_claim: semantic_only
```

AMF production load remains disabled and returns `MFOS_ERR_UNSUPPORTED`.

