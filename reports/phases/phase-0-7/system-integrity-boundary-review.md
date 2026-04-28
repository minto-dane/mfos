# System Integrity Boundary Review

Date: 2026-04-27

Scope:

- `docs/design/specs/03-system-integrity.md`
- Boundary sections for SVC, PCALL, AMF, securityd, auditd, Dataset/Catalog/Spool, Operator, PXM, and Guard.

Out of scope:

- Production implementation.
- Requirement, test, evidence, source card, claim, or pack registry changes.
- New compatibility claims.

## Review Summary

The reviewed sections already expressed the main system integrity boundaries. This pass tightened fail-closed behavior, operation ordering, audit/security obligations, and component non-responsibilities where ambiguity could let a later implementation infer a permissive fallback.

## Strengthened Rules

### System Interfaces

- Added explicit trusted caller context establishment before caller-supplied identity fields are interpreted.
- Added a general rule that protected-resource operations require a securityd decision before handle creation, state changes, content exposure, or device assignment.
- Added denial-before-return audit obligation for audit-required denies.
- Made `MFOS_ERR_UNSUPPORTED` and `MFOS_ERR_SPEC_GAP` terminal for the requested operation.
- Required fail-closed or recovery-only behavior when securityd or auditd is unavailable.

### SVC

- Added handle lookup requirements for type, generation, subject binding, operation, and expiry.
- Added no-state-mutation-before-validation and no-output-writeback-before-commit rules.
- Explicitly prohibited conversion of denied, unsupported, spec-gap, and audit-unavailable errors into success.

### PCALL

- Required endpoint registry metadata for operations, AuthorityClass, and audit obligations.
- Required copied or sealed buffers instead of raw cross-address-space sharing.
- Prohibited trusted services from becoming shadow policy decision points.

### AMF

- Added an AMF-disabled phase rule:
  - AMF load returns `MFOS_ERR_UNSUPPORTED`.
  - No executable mapping, AMF registry entry, `AUTHORIZED_SERVICE` transition, or AuthorityClass grant is created.
  - Unsupported attempts remain auditable.
- Clarified that production AMF remains blocked until the AMF spec, requirements, tests, evidence, and pack gate are complete.
- Added fail-closed checks for missing manifest, epoch, policy_version, AuthorityClass, audit obligation, or immutable artifact binding.
- Prohibited writable-and-executable mappings and premature executable mapping.

### securityd

- Added required decision metadata: `decision_id`, `decision_time`, `policy_version`, `obligations_hash`, `valid_until`, and `reason_code`.
- Clarified that `DENY`, `UNSUPPORTED`, `SPEC_GAP`, expired decisions, policy mismatch, and missing obligations are non-authorizing.
- Clarified that `REQUIRE_*` decisions are pending states, not execution permission.
- Explicitly prevented callers from treating securityd unavailability as allow-by-default.

### auditd

- Added required audit record fields.
- Required decision_id where a security event is tied to a securityd decision.
- Made required audit write failure block protected operation completion, except explicitly marked recovery-only operations.
- Clarified that auditd does not make final authorization decisions.
- Required redaction not to remove fields needed to prove denial-before-return, policy_version, or binding.

### Dataset, Catalog, and Spool

- Prohibited POSIX file fallback or ordinary file wrapper substitution for dataset access.
- Required no handle creation on uncommitted, rolled-back, recovery-pending, or integrity-failed catalog state.
- Required dataset open allow/deny, stale handle, policy mismatch, and destructive operations to carry audit obligations.
- Added catalog fail-closed rules for ambiguous transaction state, journal mismatch, generation mismatch, and recovery-in-progress.
- Added spool content authorization/redaction ordering and purge authority/retention/audit rules.

### Operator

- Added `AUDIT_INTENT?` and `AUDIT_RESULT` to the command lifecycle.
- Prohibited root-shell bypass of the command registry.
- Required denial audit before display when audit failure policy does not transfer to recovery-only mode.
- Clarified confirmation and dual-control as pending states, not execution authority.
- Required automation hooks to use explicit ProgramIdentity and AuthorityClass.

### PXM

- Reaffirmed PXM cannot inspect or decide enterprise semantics such as dataset names, job classes, spool classes, operator verbs, or security profile contents.
- Added fail-closed PXM_CALL and device assignment/teardown rules.
- Clarified side partition gateway resource exchange remains governed by MFOS gateway policy and securityd; PXM only enforces partition/device isolation.

### Guard

- Reaffirmed Guard root-object-only scope.
- Added explicit prohibited parsers/semantics: JCL, DSN, spool, operator grammar, security profiles, workload policy, POSIX paths, and Linux desktop metadata.
- Required Guard unavailability in Guard-required profiles to block protected operations or enter recovery-only mode.
- Clarified Guard approval is not a replacement for securityd authorization or auditd evidence except when the protected operation is the Guard root transition itself.
- Required root mismatch to produce lockdown, boot denial, or recovery-only behavior.

## Residual Gaps

- Exact binary ABI details remain in the existing SPEC-GAP list.
- The profile-specific audit failure policy still belongs in the audit specification.
- This review did not add registry entries, tests, or evidence records; existing registries remain the machine-readable tracking location for those artifacts.

## Gate

```yaml
production_implementation_allowed: false
hosted_semantic_prototype_allowed: only_for_packs_that_pass_pre_implementation_gate
release_claims_allowed: false
```
