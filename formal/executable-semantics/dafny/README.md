# Dafny Executable Semantics Scaffold

Status: Phase 1 specification-only scaffold.

This directory is reserved for MFOS Dafny executable-semantics artifacts and related documentation. The canonical Phase 1 executable-semantics artifact language is Dafny.

No .dafny files are required by this scaffold. Dafny source files remain optional until a later reviewed artifact task creates them.

Phase 1 scope is loader-only artifact validation:

- discover Dafny artifacts in this scaffold,
- validate declared metadata shape,
- check source references and requirement references,
- check declared dependencies and proof status,
- report malformed, missing, unsupported, or SPEC_GAP artifacts.

This directory does not authorize:

- semantic-runner implementation,
- hosted daemon implementation,
- Rust semantic-core or Portable Semantic Core implementation,
- production code,
- production use of Dafny-generated code,
- production readiness or conformance claims.

Dafny-generated code, if later produced by an explicitly non-production test task, is test-only and must not be linked into MFOS production services or packages.

Normative policy: `docs/design/specs/43-dafny-executable-semantics-policy.md`.
