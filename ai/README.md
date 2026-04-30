# ai/

AI contracts, task packets, prompt library mirrors, and reviewed outputs.

Raw AI output must not be trusted as implementation evidence until reviewed and
linked to requirements, source IDs, tests, and audit obligations.

The current Phase 1 AI assignment gate allows non-production Dafny
executable-semantics artifacts and conformance-harness validation under
`formal/executable-semantics/dafny/` and `tools/`. AI prompts must not
authorize Rust semantic-core work, future semantic-runner command
implementation, hosted daemons, hosted semantic prototypes, production
services, PXM/MFVM/CVM implementation, cluster implementation, or
Dafny-generated production code.

Architecture prompts must preserve the x86-64-first but not x86-64-only policy.
x86-64-v4 is optional, SGX is enclave/TEE rather than CVM, and future non-x86
support must not be claimed as implemented without source cards, requirements,
registries, tests, CI, evidence, and reviewed backends.
