# Dafny Toolchain Report

Status: current
Date: 2026-04-29

## Pin

```yaml
dafny_version: 4.11.0
dafny_version_output: 4.11.0+fcb2042d6d043a2634f0854338c08feeaaaf4ae2
z3_version: Z3 version 4.14.1 - 64 bit
install_script: scripts/install-dafny.sh
install_asset: dafny-4.11.0-x64-ubuntu-22.04.zip
install_sha256: a46a9ff7cdd720f7955854c78e95df13f4cfe6b80691b05f8654fe19e8267179
local_install_path: .tools/dafny/4.11.0/dafny/dafny
ci_install_method: scripts/install-dafny.sh in MFOS Design Validation workflow
ci_runner: ubuntu-22.04
```

The installer uses a pinned GitHub release asset and verifies SHA-256 before
extracting with Python's standard `zipfile` library. The extracted toolchain is
kept under `.tools/`, which is ignored by Git.

## Verification Command

```sh
./scripts/install-dafny.sh
./scripts/validate-dafny-semantics.sh --require-dafny
```

This command verifies all files matched by
`formal/executable-semantics/dafny/modules/*.dfy`.

## Limitations

This report pins and records the Phase 1 verification toolchain. It does not
authorize production implementation, hosted daemons, Rust semantic-core work,
semantic-runner commands, or Dafny-generated production code.
