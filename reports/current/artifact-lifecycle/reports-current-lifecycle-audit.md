# Reports Current Lifecycle Audit

Status: current.

Scope: every artifact under `reports/current/` was reviewed for lifecycle
placement and, after the repository information architecture refactor, grouped
by stable responsibility domain.

## Result

- Phase-specific reports were moved out of `reports/current/`.
- Generated Phase 1.1, Phase 1.2, and Phase 1.3 reports were moved under
  `reports/generated/phase-*`.
- Superseded gap triage, fixed-point readiness, and PR review reports were
  moved under `reports/archive/`.
- Pre-Phase-1 readiness reports were moved under `reports/phases/phase-1/`.
- Stable current packages now live under domain subdirectories listed in
  `reports/current/index.yml`, including `fixedpoint/` and `source-grounding/`.
- Top-level current report bodies are limited to repository information
  architecture outputs.

## Policy

`reports/current/phase-*`, `reports/current/pre-phase*`, generated report
outputs, archived/superseded reports, PR review artifacts, and unsharded
top-level domain reports are forbidden.
