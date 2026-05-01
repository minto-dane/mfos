# AI / Pack / Prompt Scaffold Audit

Pack contracts exist in `packs/pack-index.yml` and detailed Phase 0.8 pack files under `docs/design/packs/PACK-05-*` through `PACK-09-*`.

`implementation_allowed` is explicit and does not authorize production implementation.

AI implementation contract exists at `ai/contracts/ai-implementation-contract.md`.

Risk: prompts and task packets are lighter than specs/packs. Before assigning implementation agents, pass only indexed packs and current artifact indexes, not broad empty scaffolds.
