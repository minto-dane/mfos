# System Integrity Front-Half Review

Date: 2026-04-27

Scope:

- `docs/design/specs/03-system-integrity.md`
- Sections reviewed and strengthened: Purpose, Non-Compatibility Statement, Source Matrix References, Authorized vs Unauthorized, Execution States, Storage Domains, Protected Resources, System Interfaces, Prohibited Circumventions.

Changes made:

- Added explicit Source ID and Requirement ID traceability to the front-half sections.
- Expanded Source Matrix References from a source-only table to a source-to-requirement table.
- Clarified that this specification does not grant production implementation permission.
- Tightened authorization language so AuthorityClass cannot be inferred from `ExecutionState`, UID-like values, root-shell status, or caller-controlled request fields.
- Clarified that authorization decisions are scoped to a specific subject, object, operation, context, and policy version.
- Strengthened ExecutionState language to avoid Baseline overclaim after nucleus or authorized service compromise.
- Clarified StorageDomain as MFOS software classification, not z/Architecture storage-key compatibility.
- Added protected-resource handle binding and audit-before-return requirements.
- Expanded System Interfaces with per-interface Source IDs and Requirement IDs.
- Added `10.1 Prohibited Circumventions` with required fail-closed behavior for forged identity, untrusted pointer use, securityd bypass, audit substitution, stale handles, AMF overclaim, PXM/Guard scope creep, hardware overclaim, and unsupported/spec-gap completed-operation paths.

Validation run:

```text
python3 scripts/validators/validate-spec-front-matter.py
python3 scripts/checks/check-source-grounding.py
python3 scripts/checks/check-prohibited-terms.py
python3 scripts/checks/check-spec-gap-misuse.py
```

Validation results:

```text
Spec front matter validation OK: 35 specs checked: 0 warnings
Source grounding check OK: 0 warnings
Prohibited wording check OK
SPEC_GAP/UNSUPPORTED misuse check OK: 0 warnings
```

Implementation status:

```yaml
production_implementation_started: false
production_implementation_allowed: false
hosted_semantic_prototype_allowed: only_for_packs_that_pass_pre_implementation_gate
```

Remaining notes:

- The front-half specification is stronger and more traceable, but the broader Phase 0.7 status remains incomplete until the full System Integrity deep spec and evidence archive are completed.
- No source cards, requirements, tests, evidence registries, packs, or implementation paths were changed in this review.
