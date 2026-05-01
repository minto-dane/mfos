# guard/

Reserved future High-Assurance Guard root-object protection implementation area.
Guard scope must stay small: selected security roots, audit roots, AMF registry
roots, executable mapping policy, SVC table integrity, and related root
transitions only.

No Phase 1 implementation work belongs here. Phase 1 is limited to Dafny
executable-semantics scaffold work and loader-only artifact validation under
`formal/executable-semantics/dafny/`. Guard implementation, PXM integration,
hosted daemon work, semantic runner work, Rust semantic-core work, generated
production code, and production code remain forbidden until a later reviewed
gate explicitly authorizes them.
