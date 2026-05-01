# CI and Workflow Remediation

Status: current

`scripts/validate-component-scaffold.sh` is now wired into
`scripts/validate-all.sh`, so GitHub design validation will check scaffold
metadata on pull requests and pushes.

Phase 0.10 also adds `scripts/validators/validate-formal-registry.py` and
wires it into `scripts/validate-all.sh`. Naming-safety lint now distinguishes
the MFOS-owned term `hypervisor-class` from external product names while
keeping Hyper-V and KVM restricted to external-reference or comparison
contexts.

The workflow remains design-validation only. It does not build production code,
run a semantic runner, or execute hosted daemons.
