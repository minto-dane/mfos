# Phase 0.7 System Integrity Progress Report

Status: Draft, In Progress  
Date: 2026-04-27  
Scope: System-integrity specification and machine-readable registry expansion only.  
Production implementation: not started.

## Executive Summary

Phase 0.7 is in progress. This pass did not repeat the completed Phase 0.6
scaffold work; it synchronized the current state after registry expansion and
traceability regeneration.

The registry coverage and cross-registry link gaps are currently closed in
draft mode. This is not a Phase 0.7 completion claim: 66 requirements are
reserved as `spec_gap_reserved`, all evidence records are still draft
placeholders, and release-mode evidence checking correctly blocks claim
promotion.

The main correction was to make the system-integrity boundary more explicit: Baseline does not claim protection after nucleus or authorized-service compromise, AMF remains disabled for early implementation, auditd start failure cannot fall through into normal operation, and PXM/Guard remain scoped to their assigned isolation and root-object responsibilities.

## Files Updated

- `docs/design/specs/03-system-integrity.md`
- `docs/design/registries/requirements.yaml`
- `docs/design/registries/tests.yaml`
- `docs/design/registries/evidence.yaml`
- `docs/design/registries/README.md`
- `docs/design/assurance/claim-tree.yml`
- `docs/design/STATUS.md`
- `tasks/phase-0-7-system-integrity-deep-spec.yml`
- `reports/audits/traceability/traceability-audit.md`
- `reports/phases/phase-0-7/phase-0-7-system-integrity-progress.md`

## Critical Corrections Made

- Auditd boot failure language was tightened. Baseline now enters operator recovery mode only, with ordinary jobs, ordinary dataset opens, policy updates, AMF load, update activation, partition device assignment, and destructive operator commands blocked.
- The AMF-disabled path no longer describes a load success. Phase 1 AMF load returns `MFOS_ERR_UNSUPPORTED`, creates no executable mapping, creates no registry entry, and performs no authorized-state transition.
- `CLAIM-GRD-HA-001` now references registered system-integrity requirements and tests instead of unregistered Guard/audit/AMF requirement IDs.
- Draft system-integrity requirements now explicitly cover securityd as final PDP, auditd as evidence service, dataset handle binding, operator command authorization, PXM non-interpretation of enterprise semantics, Guard root-object scope, and hardware-feature non-overclaim.
- Source-card-to-requirement gaps were closed by reserving source-mapped
  requirement IDs as `spec_gap_reserved`; no operational semantics were added
  for those reserved IDs.
- Requirement/test/evidence and claim/test/evidence link warnings were closed
  by registering draft placeholder records for planned IDs. These placeholders
  do not constitute proof or implementation authorization.
- SPEC_GAP/UNSUPPORTED success-path wording warnings were reduced to zero.
- Design validation is wired into CI, while release evidence checking remains
  fail-closed until verified evidence exists.
- `03-system-integrity.md` now covers Purpose, source references, authority
  model, protected resources, system interfaces, prohibited circumventions,
  boundary rules, failure modes, formal invariants, registry-backed tests, and
  spec-gap handling in draft-review form.
- Line-local source-grounding enforcement exists for opt-in specs, and
  `03-system-integrity.md` opts in and passes release-mode source grounding.

## Registry Expansion

```yaml
requirements:
  before_phase_0_7_pass: 21
  after_initial_system_integrity_pass: 40
  after_registry_gap_closure: 106
  added:
    - MFOS-REQ-SI-0002..MFOS-REQ-SI-0020
    - 66 source-mapped spec-gap-reserved requirement IDs
  reservation_status:
    active_or_unset: 40
    spec_gap_reserved: 66
tests:
  before_phase_0_7_pass: 5
  after_initial_system_integrity_pass: 33
  after_reserved_requirement_closure: 99
  after_cross_registry_link_closure: 261
evidence:
  before_phase_0_7_pass: 3
  after_initial_system_integrity_pass: 33
  after_reserved_requirement_closure: 102
  after_cross_registry_link_closure: 170
  status_counts:
    draft: 170
claims:
  total: 5
source_cards:
  total: 37
packs:
  total: 31
```

All new evidence entries are draft placeholders for future artifacts. They are not verified proof and must not be used to broaden production or High-Assurance claims.

## Validation Commands Run

```bash
./scripts/validate-all.sh
python3 -m py_compile scripts/*.py
python3 scripts/check-evidence-status.py --mode release
python3 - <<'PY'
import json, pathlib, yaml
for p in pathlib.Path('.').rglob('*'):
    if any(part in {'.git','__pycache__'} for part in p.parts):
        continue
    if p.suffix in {'.yml','.yaml'}:
        yaml.safe_load(p.read_text(encoding='utf-8'))
    elif p.suffix == '.json':
        json.loads(p.read_text(encoding='utf-8'))
print('YAML_JSON_PARSE_OK')
PY
```

## Validation Results

```yaml
validate_all: passed_in_draft_mode
source_cards: "37 cards validated"
requirements: "106 entries validated"
claims: "5 claims checked, 0 warnings"
spec_front_matter: "35 specs checked, 0 warnings"
packs: "31 packs checked, 0 warnings"
source_grounding: "0 warnings"
audit_obligations: "106 requirements checked, 0 warnings"
spec_gap_unsupported_misuse: "0 warnings"
registry_link_validation: "0 warnings"
evidence_status_draft_mode: "170 entries checked, 0 warnings"
evidence_status_release_mode: "failed closed with 18 errors and 20 warnings"
source_grounding_release_mode: "0 warnings for current opt-in specs"
validate_all_check_mode: passed
python_compile: passed
yaml_json_parse: passed
traceability_matrices: regenerated
traceability_gap_groups: 0
high_traceability_gap_groups: 0
```

## Remaining Gaps

- The traceability gap report currently has zero gap groups, but the registry
  contains 66 `spec_gap_reserved` requirement entries. Those entries are
  reserved for traceability only and must not be used as implementation-ready
  requirements.
- The 170 evidence records are draft records only. Release-mode lint correctly
  rejects claim promotion without real artifacts, digests, verifiers, and
  verification timestamps.
- Source Cards still need tighter section/version pins where local metadata cannot verify them.
- Japanese mirror mechanics remain incomplete and nonblocking while English remains canonical.
- CI design validation is wired, but release-mode evidence archive work remains
  open.
- `docs/design/specs/03-system-integrity.md` is draft-review complete for the
  current Phase 0.7 machine-checkable scaffold, but not implementation-ready.

## Gate Judgment

```yaml
production_implementation_allowed: false
hosted_semantic_prototype_allowed: only_for_packs_that_pass_pre_implementation_gate
release_claims_allowed: false
next_phase: Continue Phase 0.7 System Integrity Deep Spec
```
