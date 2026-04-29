# prompts/

Top-level prompt library bridge. Current canonical prompt content is in
[docs/design/prompts/ai-prompts.md](../docs/design/prompts/ai-prompts.md).

The current Phase 1 prompt gate must preserve the Dafny-first, non-production
boundary: Dafny source artifacts under `formal/executable-semantics/dafny/`
and conformance-support tools under `tools/`. It must not instruct agents to
implement a Rust semantic core, future semantic-runner commands, hosted daemon,
hosted semantic prototype, production service, PXM/MFVM/CVM runtime, cluster
scheduler, or Dafny-generated production code.
