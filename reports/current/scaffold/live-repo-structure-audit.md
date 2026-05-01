# Live Repository Structure Audit

Status: current

The live repository is public, defaults to `dev`, and has no open pull requests
at the start of this remediation pass. The working tree was clean before
changes. The canonical design path remains `docs/design/`; top-level
`specs/`, `requirements/`, `source-matrix/`, `packs/`, and `sources/` are
bridge or workbench paths unless explicitly promoted by ADR.

Key structural finding: empty scaffolds are acceptable only when classified.
The remediation adds `.mfos-dir.yml` metadata and validation rather than
placing dummy content in empty implementation or test directories.
