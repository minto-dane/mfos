# MFOS Design Directory

This directory is the design canon area for MFOS.

MFOS is an x64-native, z/OS-inspired, source-grounded enterprise operating system. It is x86-64-first for initial implementation planning, but it is not x86-64-only. It is not z/OS-compatible and must not be described that way.

Machine-checkable design enforcement around this canon consists of:

```text
- JSON Schemas under ../../schemas/.
- Local validators under ../../scripts/.
- Traceability matrices under ../../evidence/traceability/.
- Report index under ../../reports/index.yml and categorized reports under
  ../../reports/.
- Pack contracts under ../../packs/pack-index.yml.
- Assurance claim tree under assurance/claim-tree.yml.
```

These artifacts are design and validation scaffolding. Their presence does not
mean production implementation, passing tests, verified evidence, AMF enablement,
PXM device-assignment readiness, Guard readiness, or production readiness.

## Reading Order

Start here:

```text
1. mfos-design.md
2. source-matrix/source-matrix.md
3. source-matrix/source-matrix.yml
4. source-matrix/source-card-schema.md
5. source-matrix/cards/EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001.yml
6. source-matrix/traceability-policy.md
7. source-matrix/traceability-index.md
8. registries/requirements.yaml
9. specs/INDEX.md
10. specs/00-normative-language.md
11. specs/01-glossary.md
12. specs/02-source-matrix.md
13. specs/03-system-integrity.md
14. specs/04-threat-model.md
15. specs/05-object-model.md
16. specs/06-authorization.md
17. specs/07-audit.md
18. specs/08-dataset-catalog.md
19. specs/09-job-spool.md
20. specs/10-operator-console.md
21. specs/11-workload-policy.md
22. specs/12-amf.md
23. specs/13-update.md
24. specs/14-nucleus.md
25. specs/15-svc-pcall.md
26. specs/16-pxm.md
27. specs/17-guard.md
28. specs/18-linux-gateway.md
29. specs/19-assurance-case.md
30. specs/20-conformance.md
31. specs/21-ai-implementation-contract.md
32. specs/22-production-readiness.md
33. specs/23-requirements-catalog.md
34. specs/24-formal-methods.md
35. specs/25-operations-recovery.md
36. specs/26-hardware-profile.md
37. specs/27-spec-front-matter.md
38. specs/28-machine-readable-registries.md
39. specs/29-test-strategy.md
40. specs/30-attestation-measured-boot.md
41. specs/30-first-vertical-slice-contract.md
42. specs/31-executable-spec-test-harness.md
43. specs/31-release-distribution-rollback.md
44. specs/32-conformance-fixture-format.md
45. specs/32-language-localization.md
46. specs/33-policy-lint.md
47. specs/33-semantic-runner-contract.md
48. specs/34-oracle-definition-format.md
49. specs/35-fuzz-corpus-plan.md
50. specs/36-hypervisor-class-virtualization.md
51. specs/37-confidential-vm.md
52. specs/38-datacenter-cluster-operations.md
53. specs/39-language-and-verification-policy.md
54. specs/40-automated-reasoning-program.md
55. specs/41-performance-and-secure-operations.md
56. specs/42-mfvm.md
57. specs/43-dafny-executable-semantics-policy.md
58. specs/44-architecture-portability-policy.md
59. specs/45-x86-64-target-profiles.md
```

## Directory Map

```text
docs/design/
  mfos-design.md
    Full architecture canon candidate.

  source-matrix/
    Human source ledger, Source Card index, per-source YAML cards,
    traceability policy, traceability index, source lint specification,
    and freshness workflow.

  specs/
    Split specifications by AI-friendly component/package boundaries.

  prompts/
    Prompt library for concept mapping, implementation, review, testing, and assurance.

  assurance/
    Assurance case template, formal model plan, evidence archive, claim
    registry, release review workflow, and operator runbooks.

  tasks/
    Work breakdown structure, implementation roadmap, test taxonomy, and
    front matter migration plan.

  packs/
    Pack-level index for handing bounded work to AI agents.

  registries/
    Initial machine-readable seeds for requirements, tests, evidence, tasks,
    CPU Feature Registry, and CPU Target Profile Registry.

  ja/
    Japanese mirror entrypoint and synchronization policy. English remains
    canonical.
```

## AI Work Rules

Any AI or human implementer must follow these rules:

```text
- Include requirement IDs in design, code, tests, and evidence.
- Include source matrix IDs for z/OS-inspired concepts.
- Do not claim z/OS compatibility.
- Do not create fake success paths, empty stubs, or silent fallbacks.
- Use UNSUPPORTED when a specified feature is not implemented.
- Use SPEC_GAP when the feature is not specified.
- Route authorization through securityd.
- Route required evidence through auditd.
- Add negative tests for security-sensitive behavior.
- Add fuzz targets for parsers.
- Keep PXM isolated from MFOS enterprise semantics.
- Keep Guard limited to selected root objects.
- Keep architecture-neutral semantics separate from architecture-specific
  enforcement.
- Treat x86-64-v4 as optional performance profile, not baseline.
- Treat Intel SGX as optional enclave/TEE profile, not Confidential VM.
```

## Canonical Output Format for AI Changes

```text
1. Implemented Requirement IDs
2. Source Matrix IDs
3. Assumptions
4. Spec Gaps
5. Unsupported Features
6. Security Invariants
7. Audit Obligations
8. Failure Modes
9. Tests Added
10. Negative Tests Added
11. Fuzz Targets Added
12. Unsafe Code Justification
13. Review Checklist
14. Evidence Artifacts
```
