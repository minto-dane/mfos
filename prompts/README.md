# prompts/

Top-level prompt library bridge. Current canonical prompt content is in
[docs/design/prompts/ai-prompts.md](../docs/design/prompts/ai-prompts.md).

Phase 1 prompt content must preserve the Dafny-first, loader-only boundary:
`formal/executable-semantics/dafny/` scaffold and artifact validation only. It
must not instruct agents to implement a Rust semantic core, semantic runner,
hosted daemon, hosted semantic prototype, production service, PXM/MFVM/CVM
runtime, cluster scheduler, or Dafny-generated production code.
