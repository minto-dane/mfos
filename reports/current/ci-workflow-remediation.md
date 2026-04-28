# CI and Workflow Remediation

Status: current

`scripts/validate-component-scaffold.sh` is now wired into
`scripts/validate-all.sh`, so GitHub design validation will check scaffold
metadata on pull requests and pushes.

The workflow remains design-validation only. It does not build production code,
run a semantic runner, or execute hosted daemons.
