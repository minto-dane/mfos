# Test Catalogs

This directory contains current MFOS test catalog artifacts.

Canonical catalogs use stable names such as `authorization.yml` and
`dataset-catalog.yml`. Phase-specific filenames are not allowed in this root.
Historical phase catalogs are retained under `archive/<phase>/`.

Use `index.yml` as the machine-readable inventory.

Do not implement tests from this directory. These files define executable-spec
inputs for later phases.
