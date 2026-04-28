# Phase 0.8 Job/Spool Lead Report

Status: Draft semantic freeze  
Date: 2026-04-27  
Lead area: job/spool semantics only  
Production implementation: not started and not authorized

## Summary

This pass freezes the Phase 0.8 job/spool design semantics in specification,
schema, formal model, and test-catalog form. No production code was added or
changed.

The freeze defines:

- MFOS job-control stream grammar and parser output obligations.
- Job, JobStep, DDStatement, ProgramIdentity, and SpoolEntry object semantics.
- Job identity and effective principal establishment.
- Program execute authorization before step execution.
- DD resolution through catalogd, datasetd, spoold, securityd, and auditd.
- Job, step, and spool state machines with invalid transitions.
- Return-code aggregation and failure-state behavior.
- INPUT_STREAM as protected spool input and OUTPUT_STREAM as protected spool output.
- Browse, purge, export, retention, stale-reference, and audit ordering rules.
- Positive, negative, fuzz, fault-injection, formal, and evidence test coverage.

## Files Updated

- `docs/design/specs/09-job-spool.md`
- `schemas/mfos/job.schema.yml`
- `schemas/mfos/job-step.schema.yml`
- `schemas/mfos/dd.schema.yml`
- `schemas/mfos/spool-entry.schema.yml`
- `formal/tla/job-lifecycle/README.md`
- `formal/tla/job-lifecycle/JobLifecycle.tla`
- `formal/tla/job-lifecycle/JobLifecycle.cfg`
- `formal/tla/job-lifecycle/state-machine.yml`
- `formal/tla/spool-access/README.md`
- `formal/tla/spool-access/SpoolAccess.tla`
- `formal/tla/spool-access/SpoolAccess.cfg`
- `formal/tla/spool-access/state-machine.yml`
- `tests/catalog/archive/phase-0-8/job-spool-tests.yml`
- `reports/phases/phase-0-8/phase-0-8-job-spool-lead.md`

## Source Grounding

The owned job/spool artifacts use EXTREF Source Matrix IDs only:

- `EXTREF-IBM-ZOS-DFSMS-CATALOGS-0001`
- `EXTREF-IBM-ZOS-JES-INTRODUCTION-0001`
- `EXTREF-IBM-ZOS-JES-JOB-FLOW-0001`
- `EXTREF-IBM-ZOS-JES2-LIBRARY-0001`
- `EXTREF-IBM-ZOS-SECURITY-SERVER-0001`
- `EXTREF-IBM-ZOS-RACF-RESOURCE-AUTHORIZATION-0001`
- `EXTREF-IBM-ZOS-SMF-INTRODUCTION-0001`
- `EXTREF-IBM-ZOS-SMF-RACF-TYPE-80-0001`

No compatibility claim is made for z/OS, JES, JES2, JCL, RACF, DFSMS, or SMF.

## Freeze Decisions

MFOS job-control stream is line-oriented and MFOS-native. The Phase 0.8 subset allows one JOB
card, one or more EXEC cards, dataset DDs, output-stream DDs, inline input-stream DDs, and
comments. Continuations, procedures, symbolic parameters, INCLUDE, conditionals,
concatenation, and nested inline behavior are unsupported.

`job_id` and `spool_id` are server-assigned immutable identifiers. `job_name`
is operator-visible but not a security identity.

`effective_principal` is absent until submit authorization and submit-as
authorization, when applicable, have succeeded. No dataset, program, INPUT_STREAM, or
OUTPUT_STREAM handle can open before `effective_principal` exists.

`PGM=` is a symbolic program identity, not a POSIX path. Program execute
requires a securityd PROGRAM EXECUTE decision before the step can enter
resource-opening or execution states.

Dataset DD resolution is fixed as catalogd canonicalization and lookup,
securityd authorization, required audit completion, datasetd handle issuance,
and DD binding. Deny, stale generation, invalid DSN, missing catalog entry, or
audit failure creates no handle.

Inline INPUT_STREAM is stored as a protected INPUT_STREAM SpoolEntry and closed before step
execution. OUTPUT_STREAM is a protected OUTPUT_STREAM SpoolEntry created before execution,
written during step output capture, and closed before job completion.

Return codes are `0..4095`. Nonzero normal return is a completed step result,
not automatically a failed step in Phase 0.8. If all steps complete, the job
return code is the maximum completed step return code. Failed, abended, or
canceled steps drive the corresponding job terminal state.

Browse, export, and purge all require securityd decisions and required audit
completion. Purge also requires retention eligibility. Purged references are
stale and cannot return content.

## Validation

Commands run:

```bash
python3 - <<'PY'
from pathlib import Path
import yaml
for p in [
Path('schemas/mfos/job.schema.yml'),
Path('schemas/mfos/job-step.schema.yml'),
Path('schemas/mfos/dd.schema.yml'),
Path('schemas/mfos/spool-entry.schema.yml'),
Path('formal/tla/job-lifecycle/state-machine.yml'),
Path('formal/tla/spool-access/state-machine.yml'),
Path('tests/catalog/archive/phase-0-8/job-spool-tests.yml'),
]:
    yaml.safe_load(p.read_text(encoding='utf-8'))
print('PHASE_0_8_YAML_PARSE_OK')
PY

./scripts/validate-all.sh --check
```

Results:

```yaml
phase_0_8_yaml_parse: passed
validate_all_check_mode: passed
source_cards: "37 cards"
requirements: "130 entries"
spec_front_matter: "36 specs checked, 0 warnings"
source_grounding: "0 warnings"
audit_obligations: "130 requirements checked, 0 warnings"
spec_gap_unsupported_misuse: "0 warnings"
registry_links: "0 warnings"
evidence_status_draft_mode: "194 entries checked, 0 warnings"
naming_safety: "0 warnings"
compatibility_claims: "0 warnings"
external_doc_copy_guard: "0 warnings"
```

Additional checks:

```yaml
owned_source_ids_extref_only: passed
git_worktree_status: "not available; /home/nia/mfos is not a Git repository"
tla_model_checker: "not available in workspace; TLA syntax/model checking not run"
```

## Remaining Gaps

- Production implementation remains prohibited.
- TLA models need reviewed model-check output when a TLA checker is available.
- Evidence records are design placeholders; no runtime or release evidence is
  claimed.
- Requirement registry reconciliation remains open: existing `MFOS-REQ-JOB-000x`
  and `MFOS-REQ-SPOOL-000x` references coexist with newer Phase 0.8 `010x`
  draft entries. This pass did not edit the requirement registry because it is
  outside the stated job/spool lead ownership.
- Program loader contract, temporary dataset lifetime, restart metadata,
  conditional execution, procedure libraries, parallel steps, binary spool record
  format, quota hierarchy, external export gateway, and incomplete-output
  completion policy remain explicit spec gaps or unsupported features.

## Gate Judgment

```yaml
semantic_freeze_artifacts_created: true
production_implementation_allowed: false
release_claims_allowed: false
next_required_work:
  - registry reconciliation for job/spool requirement IDs
  - TLA model-check evidence or reviewed traces
  - implementation-planning gate after evidence and registry updates
```
