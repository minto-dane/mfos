# Pre-Phase-1 Deep Directory Audit

Status: current  
Date: 2026-04-28  
Branch: `fix/pre-phase-1-total-readiness-second-pass`

## Scope

The second pass scanned the repository recursively with `find` and
`git ls-files`, then cross-checked the high-risk areas called out in the
Pre-Phase-1 readiness prompt: source matrix, specs, requirements, schemas,
claims, tests, fixtures, golden vectors, fuzz plans, evidence, reports,
scripts, CI, implementation scaffolds, services, nucleus, PXM, Guard,
interfaces, AI prompts, and packs.

Observed local counts at audit time:

- Directories excluding `.git`: 441.
- Files excluding `.git` and Python bytecode caches: 943.
- Git-tracked files: 942.
- Empty directories observed locally: 171. These are untracked planned scaffold
  directories in the working copy, not committed implementation artifacts.

## Critical Fixed

- `deny-before-return` audit golden/catalog artifacts expected `ALLOW` and
  `COMPLETE`; they now expect `DENY`, fail-closed result, and before-return
  audit evidence.
- Current readiness reports overclaimed before the second pass; they are
  superseded by this package and will be updated with the final second-pass
  validation state.
- The canonical prompt library contained an active Rust service implementation
  prompt; it is now an inactive future template and explicitly forbidden for
  Phase 1.

## Major Fixed

- Hosted semantic prototype paths were removed from pack outputs and routing
  tables.
- Source workbench parity now records all 65 canonical Source Matrix cards and
  explicitly marks 28 missing workbench candidates.
- Source guidance that risked treating external documentation as substitute
  documentation was rewritten as public-safe review-topic language.
- Formal model registries no longer point at missing planned directories.
- Formal tool source references are consistent between aggregate and split
  registries.
- Formal claim/proof-obligation schemas now match the split registries, and
  validation checks the registry-entry shape.
- `MFOS-REQ-DAFNY-*` requirements are now in the canonical requirement registry
  with tests and evidence references.
- Fixture/oracle schemas now match the current compact Phase 0.9 artifacts.
- Phase 0.9 generated traceability deduplicates requirement-to-test mappings
  and reports missing fixture evidence as gaps.
- Fuzz seed plans include the minimum category set required by the fuzz corpus
  plan.
- No-implementation validation now scans future implementation scaffold roots.

## Remaining Minor

- Some legacy `schemas/mfos/*.schema.yml` artifacts still emit draft-mode
  schema-shape warnings. They are tracked as nonblocking schema normalization
  work and do not authorize implementation.
- Source grounding remains conditional for semantic evaluator work outside the
  Phase 1 loader-only scope.

## Readiness Decision

Phase 1 may proceed only as Dafny scaffold and loader-only artifact validation.
Rust semantic-core, semantic runner, hosted daemons, hosted semantic
prototypes, production services, and PXM/MFVM/CVM/cluster implementation remain
forbidden.
