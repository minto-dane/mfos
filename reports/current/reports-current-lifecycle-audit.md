# Reports Current Lifecycle Audit

Status: current.

Scope: every artifact under `reports/current/` was reviewed for lifecycle
placement. `reports/current/` is reserved for cross-phase current status,
readiness, policy, red-team, open-issue, and stable aggregate reports.

## Result

- Phase-specific reports were moved out of `reports/current/`.
- Generated Phase 1.1, Phase 1.2, and Phase 1.3 reports were moved under
  `reports/generated/phase-*`.
- Superseded gap triage, fixed-point readiness, and PR review reports were
  moved under `reports/archive/`.
- Pre-Phase-1 readiness reports were moved under `reports/phases/phase-1/`.
- Stable current packages remain under `reports/current/fixedpoint/` and
  `reports/current/source-grounding/`, with explicit metadata.

## Policy

`reports/current/phase-*`, `reports/current/pre-phase*`, generated report
outputs, and archived/superseded reports are forbidden.

