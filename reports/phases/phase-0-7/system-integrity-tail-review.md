# System Integrity Tail Review

Date: 2026-04-27

Scope:

- `docs/design/specs/03-system-integrity.md`
- Sections 20 through 26:
  - Failure Modes
  - Formal Invariants
  - Positive Tests
  - Negative Tests
  - Spec Gaps

No production implementation was started.

## Changes Made

The system integrity tail sections were tightened without changing registry
contents or implementation files.

Added to Failure Modes:

- explicit `UNSUPPORTED` vs `SPEC_GAP` classification table
- general failure table with required behavior, error/gate, and registry tests
- invalid transition table covering SVC, PCALL, DatasetOpen, CatalogTransaction,
  OperatorCommand, AMFLoad, UpdateActivation, PXM, DeviceAssignment, Guard, and
  hardware-overclaim paths

Strengthened Formal Invariants:

- converted the invariant list into a traceable table
- attached requirement IDs and registered test IDs to each invariant
- clarified that invalid transitions are excluded transitions, not ordinary
  recoverable states

Reworked test sections:

- replaced local-only positive and negative test prose with registry-backed
  tables
- all test IDs referenced in the spec now exist in
  `docs/design/registries/tests.yaml`
- AMF-disabled behavior is mapped to `MFOS_ERR_UNSUPPORTED`, not `SPEC_GAP`

Strengthened Spec Gaps:

- added a gap table with missing artifact, required handling, and registry tests
- explicitly states that spec gaps block implementation of undefined behavior
- explicitly states that defined disabled behavior remains `UNSUPPORTED`
- added closure rule requiring spec, requirements, tests, evidence expectations,
  and pack contract updates before implementation

## Validation

Commands run:

```bash
python3 scripts/checks/check-spec-gap-misuse.py
python3 scripts/validators/validate-spec-front-matter.py
python3 scripts/checks/check-source-grounding.py
python3 - <<'PY'
import re, yaml
from pathlib import Path
spec = Path('docs/design/specs/03-system-integrity.md').read_text()
ids = sorted(set(re.findall(r'MFOS-TEST-[A-Z0-9-]+', spec)))
tests = {e['test_id'] for e in yaml.safe_load(Path('docs/design/registries/tests.yaml').read_text())['entries']}
missing = [i for i in ids if i not in tests]
print(f'test_ids_in_spec={len(ids)}')
print(f'missing={len(missing)}')
for item in missing:
    print(item)
PY
```

Results:

```text
SPEC_GAP/UNSUPPORTED misuse check OK: 0 warnings
Spec front matter validation OK: 35 specs checked: 0 warnings
Source grounding check OK: 0 warnings
test_ids_in_spec=59
missing=0
```

## Remaining Notes

- The linked registry tests and evidence are still draft planning artifacts
  unless separately promoted by evidence status checks.
- This review did not edit registries, claims, packs, source cards, or
  implementation directories.
- Full `validate-all.sh` was intentionally not run from this task because it may
  regenerate traceability/report files outside the owned edit scope.

## Gate

```yaml
production_implementation_allowed: false
hosted_semantic_prototype_allowed: only_for_packs_that_pass_pre_implementation_gate
system_integrity_tail_registry_links: checked
```
