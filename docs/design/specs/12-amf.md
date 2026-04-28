---
spec_id: "MFOS-SPEC-12-AMF"
title: "MFOS AMF Specification v0.1"
canonical_language: "en-US"
japanese_mirror: "missing"
status: "draft"
owner: "MFOS architecture"
last_reviewed: "2026-04-27"
source_refs: ["FBVBS-001", "EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001", "EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001", "EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001", "EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001", "MS-VBS-001", "MS-VSM-001", "NIST-218-001", "SLSA-001", "TUF-001", "X64-AMD-001", "X64-INTEL-001"]
requirement_refs: ["MFOS-REQ-AMF-*"]
claim_refs: []
test_refs: []
evidence_refs: []
implementation_allowed: false
downstream_packs: []
spec_gap_policy: "implementation_must_not_infer_or_fill_gaps"
---
# MFOS AMF Specification v0.1

Status: Draft  
Owner: MFOS architecture  
Profile applicability: Baseline, Enterprise-Standalone, Enterprise-PXM, High-Assurance  
Source basis: user-provided MFOS Source-Grounded High-Assurance Architecture v0.3

## 1. Purpose

This document specifies AMF, the MFOS Authorized Module Facility.

AMF governs loading and use of privileged operating-system extension modules. It exists to make privileged extension loading explicit, measured, signed, revocable, auditable, and profile-bound.

AMF is inspired by enterprise operating-system authorized-program concepts, but MFOS does not claim z/OS compatibility, z/OS API compatibility, APF compatibility, or binary compatibility.

## 2. Scope

AMF covers:

- AMF module identity.
- AMF manifests.
- AMF authority classes.
- AMF load authorization.
- AMF signature, digest, measurement, revocation, and policy checks.
- AMF ABI validation.
- AMF registry maintenance.
- AMF audit obligations.
- Guard approval for High-Assurance profile.
- Failure modes, tests, negative tests, fuzz targets, and open spec gaps.

AMF specification coverage does not imply production AMF load support. Phase 1, Phase 2, and the initial Baseline production path MUST treat AMF load as specified-but-unsupported unless an explicitly non-production AMF test profile is selected.

## 3. Non-Objectives

AMF must not become:

- A general plugin ecosystem.
- An admin privilege bit.
- A substitute for securityd.
- A substitute for PXM Guard.
- A replacement for nucleus memory safety.
- A path for arbitrary kernel pointer access.
- A bypass for auditd.
- A compatibility layer for z/OS APF or authorized assembler services.

## 4. Source Matrix References

Required source IDs for this spec:

- EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001: authorized-program boundary concept.
- EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001: authorized-code scanner style negative testing.
- EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001: system integrity statement.
- EXTREF-IBM-ZOS-STORAGE-PROTECTION-0001: storage-domain inspiration and divergence.
- X64-INTEL-001: x64 protection, page mapping, executable mapping, and privileged execution reality.
- X64-AMD-001: AMD64 privileged execution and memory-management reality.
- MS-VBS-001: executable mapping and code-integrity reference for High-Assurance profile only.
- MS-VSM-001: Guard isolation reference for High-Assurance profile only.
- TUF-001: update metadata and revocation interaction.
- SLSA-001: provenance expectations.
- NIST-218-001: secure development baseline.
- FBVBS-001: requirements, evidence, state-machine, and no-fake-success discipline.

AI implementation rule: code or tests for AMF must cite at least one AMF requirement ID and relevant source matrix IDs in design comments or traceability metadata.

## 5. Terminology

AMF:
  Authorized Module Facility, the MFOS mechanism for approving and loading privileged OS extension modules.

AMF module:
  A signed and measured artifact with an AMF manifest and explicit authority class.

AMF registry:
  Committed registry of authorized module identities, digests, authority classes, policy version bindings, revocation state, and load state.

Authority class:
  A named capability set that constrains what privileged interfaces a module may call.

Authorized state:
  MFOS execution condition that allows an AMF module to invoke selected privileged service endpoints. It is not equivalent to administrator or root access.

AMF load:
  Lifecycle from module load request through artifact resolution, verification, authorization, optional Guard approval, executable mapping, registration, audit, and ready state.

AMF manifest:
  Signed metadata describing the module, authority class, ABI, dependencies, profile applicability, measurements, and revocation references.

Security epoch:
  Monotonic policy and update epoch used to reject stale or downgraded modules.

## 6. AMF Profile Modes

AMF has profile modes separate from the main MFOS conformance profile.

```text
Baseline-AMF-Disabled:
  AMF specification exists.
  AMF manifest parsing may be tested.
  AMF load requests MUST return MFOS_ERR_UNSUPPORTED.
  No production AMF load is allowed.

AMF-Test:
  Signed test-only AMF modules MAY load in a non-production profile.
  Test profile MUST be explicit in the conformance statement.
  Production claims are prohibited.

Enterprise-AMF:
  AMF load is production-eligible only after signed, measured,
  revocable, immutable-source, securityd-authorized, auditd-recorded
  governance is implemented and evidenced.

High-Assurance-AMF:
  Enterprise-AMF requirements apply.
  Guard-approved AMF registry and Guard-approved executable mapping
  are required for any AMF load claim.
```

Initial implementation phases use `Baseline-AMF-Disabled`. AMF support is a specification and governance path before it is a production extension-loading path.

## 7. Roles and Trust Boundaries

### 7.1 Components

- `amfd`: AMF loader and governor.
- `securityd`: final policy decision point for AMF load and privileged AMF operations.
- `auditd`: evidence service for all AMF decisions and state changes.
- `catalogd`: resolves immutable system datasets or approved artifact-store entries.
- `uvsd`: verifies update metadata, artifact freshness, rollback protection, and revocation metadata.
- `nucleus`: maps executable memory, enforces typed handles, performs copy-in/copy-out, and exposes SVC/PCALL boundaries.
- `PXM Guard`: High-Assurance root protection for AMF registry and executable mapping policy.

### 7.2 Trust Boundaries

AMF crosses these boundaries:

- Operator or update workflow to `amfd`.
- `amfd` to `securityd`.
- `amfd` to `auditd`.
- `amfd` to `catalogd`.
- `amfd` to `uvsd`.
- `amfd` to nucleus executable mapping.
- `amfd` to PXM Guard in High-Assurance profile.

No AMF request may trust caller-supplied subject identity, policy version, catalog generation, digest, or authority class without independent verification.

## 8. AMF Object Model and Manifest

### 8.1 AMFModuleIdentity

```yaml
AMFModuleIdentity:
  module_id: string
  component_id: string
  version: semver
  signer_id: string
  digest:
    algorithm: sha384
    value: hex
  manifest_digest:
    algorithm: sha384
    value: hex
  security_epoch: uint64
  source_matrix_refs: [string]
```

### 8.2 AMFManifest

```yaml
AMFManifest:
  manifest_version: 1
  module_id: string
  component_id: string
  component_version: semver
  module_kind: nucleus_extension | trusted_service_extension | driver_adapter | security_hook | audit_hook
  target_arch: x86_64
  target_vendor: intel | amd | any
  profile_applicability:
    - Baseline
    - Enterprise-Standalone
    - Enterprise-PXM
    - High-Assurance
  required_cpu_features:
    - nx
    - smep?
    - smap?
    - cet?
    - pku?
    - pks?
    - iommu?
  authority_class: string
  allowed_entrypoints:
    - name: string
      abi: amf-v1
      endpoint_type: pcall | svc_extension | callback
  denied_entrypoints:
    - string
  required_services:
    - securityd
    - auditd
  dependencies:
    - component_id: string
      min_version: semver
  conflicts:
    - component_id: string
      max_version: semver
  catalog_binding:
    dsn_or_artifact_id: string
    require_immutable: true
    require_system_dataset: bool
  rollback_policy:
    min_generation: uint64
  security_epoch: uint64
  revocation_refs:
    - string
  policy_binding:
    min_policy_version: uint64
    max_policy_version: uint64?
  executable_mapping_policy:
    wx_allowed: false
    rx_after_verify_only: true
    writable_after_rx: false
  guard_required: bool
  audit_class: AMF_SECURITY_CRITICAL
  source_matrix_refs:
    - EXTREF-IBM-ZOS-AUTHORIZED-PROGRAMS-0001
    - EXTREF-IBM-ZOS-AUTHORIZED-CODE-SCANNER-0001
    - EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
  hash:
    algorithm: sha384
    value: hex
  size: uint64
  signing_key_id: string
  signature: string
```

### 8.3 AuthorityClass

```yaml
AuthorityClass:
  authority_class_id: string
  description: string
  allowed_privileged_calls:
    - string
  allowed_object_types:
    - string
  denied_object_types:
    - string
  can_register_svc: bool
  can_register_pcall_endpoint: bool
  can_access_security_root: false
  can_access_audit_root: false
  can_disable_audit: false
  can_modify_policy_without_securityd: false
  requires_dual_control: bool
  requires_guard_approval: bool
```

### 8.4 AMFRegistryEntry

```yaml
AMFRegistryEntry:
  module_id: string
  module_digest: sha384
  manifest_digest: sha384
  signer_id: string
  authority_class: string
  policy_version: uint64
  catalog_entry_generation: uint64
  security_epoch: uint64
  load_state: AMFLoadState
  loaded_at: timestamp?
  loaded_by: SubjectRef?
  measurement_context: sha384
  guard_seal_version: uint64?
  revocation_state: valid | revoked | signer_revoked | epoch_stale | unknown
```

## 9. AMF Load State Machine

```text
REQUEST_LOAD
  -> CHECK_AMF_MODE
  -> RESOLVE_ARTIFACT
  -> VERIFY_MANIFEST_SCHEMA
  -> VERIFY_SIGNATURE
  -> VERIFY_ARTIFACT_HASH_SIZE
  -> VERIFY_SOURCE_REFS
  -> CHECK_PROFILE_APPLICABILITY
  -> CHECK_CPU_FEATURES
  -> CHECK_REVOCATION
  -> CHECK_SECURITY_EPOCH
  -> CHECK_CATALOG_IMMUTABILITY
  -> CHECK_DEPENDENCIES
  -> VALIDATE_ABI
  -> SECURITYD_AUTHORIZE
  -> GUARD_APPROVE?        [High-Assurance or manifest guard_required]
  -> MAP_RX
  -> REGISTER_AMF
  -> AUDIT_READY
  -> READY
```

Failure states:

```text
AMF_UNSUPPORTED
ARTIFACT_NOT_FOUND
MANIFEST_INVALID
SIGNATURE_INVALID
HASH_MISMATCH
SIZE_MISMATCH
SOURCE_REFS_MISSING
PROFILE_NOT_APPLICABLE
CPU_FEATURE_MISSING
REVOKED
SIGNER_REVOKED
SECURITY_EPOCH_STALE
CATALOG_NOT_IMMUTABLE
DEPENDENCY_UNSATISFIED
ABI_INVALID
SECURITY_DENIED
GUARD_REQUIRED
GUARD_DENIED
EXEC_MAPPING_DENIED
AUDIT_REQUIRED_BUT_UNAVAILABLE
LOAD_FAILED_CLOSED
SPEC_GAP
UNSUPPORTED
```

## 10. AMF ABI Rules

AMF module ABI version: `amf-v1`.

Required ABI properties:

- Entry points are named and declared in the manifest.
- Entry points receive typed handles and sealed buffers, not arbitrary user pointers.
- All caller identity comes from nucleus/service context, not module-supplied fields.
- All protected resource access goes through `securityd`.
- All security-sensitive operations return typed MFOS errors.
- All audit obligations are propagated to `auditd`.
- Unsupported operations return `MFOS_ERR_UNSUPPORTED`.
- Undefined operations return `MFOS_ERR_SPEC_GAP`.
- AMF modules cannot create new authority classes at runtime.
- AMF modules cannot disable audit.
- AMF modules cannot write to executable mappings.
- AMF modules cannot map writable executable pages.

### 10.1 AMF Entry Request

```yaml
AMFEntryRequest:
  abi_version: amf-v1
  entrypoint: string
  caller_subject: SubjectRef
  caller_job: JobRef?
  caller_program: ProgramIdentityRef?
  policy_version: uint64
  correlation_id: uuid
  request_buffer: SealedBufferRef
  request_len: uint64
  audit_obligation: AuditObligationRef
```

### 10.2 AMF Entry Response

```yaml
AMFEntryResponse:
  status: MFOS_OK | MFOS_ERR_*
  reason_code: string
  response_buffer: SealedBufferRef?
  audit_record_id: uuid?
  obligations_completed:
    - string
```

## 11. Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| MFOS-REQ-AMF-0001 | AMF module artifacts must be signed before any AMF load can be supported. | signature test |
| MFOS-REQ-AMF-0002 | AMF modules may load only from immutable system datasets or approved artifact-store entries in AMF-Test, Enterprise-AMF, or High-Assurance-AMF modes. | negative test |
| MFOS-REQ-AMF-0003 | AMF modules must declare an explicit authority class. | manifest test |
| MFOS-REQ-AMF-0004 | Supported AMF load and denied AMF load requests must produce an audit record. | audit test |
| MFOS-REQ-AMF-0005 | Revoked signer, revoked digest, or stale security epoch must fail closed. | revocation test |
| MFOS-REQ-AMF-0006 | High-Assurance AMF registry must be Guard-sealed. | Guard test |
| MFOS-REQ-AMF-0007 | AMF modules must not have authority to disable audit. | architecture review |
| MFOS-REQ-AMF-0008 | AMF ABI must not accept arbitrary pointers. | ABI review and fuzz |
| MFOS-REQ-AMF-0009 | AMF manifest must declare source matrix references for authorized-state concepts. | source-matrix lint |
| MFOS-REQ-AMF-0010 | Supported AMF load must call `securityd` before executable mapping. | integration test |
| MFOS-REQ-AMF-0011 | Supported AMF load must call `auditd` before reporting READY. | integration test |
| MFOS-REQ-AMF-0012 | AMF load must call PXM Guard before executable mapping when profile is High-Assurance or manifest requires Guard. | Guard negative test |
| MFOS-REQ-AMF-0013 | AMF module executable mappings must be RX only after signature, digest, manifest, policy, and revocation checks pass. | memory mapping test |
| MFOS-REQ-AMF-0014 | AMF module pages must never be writable and executable at the same time. | W^X test |
| MFOS-REQ-AMF-0015 | AMF registry entries must bind module digest, manifest digest, authority class, policy version, catalog generation, and security epoch. | registry schema test |
| MFOS-REQ-AMF-0016 | AMF registry update must be transactional. | crash test |
| MFOS-REQ-AMF-0017 | AMF load must reject missing or malformed source matrix IDs. | lint negative test |
| MFOS-REQ-AMF-0018 | AMF module cannot register an SVC or PCALL endpoint outside declared authority class. | negative test |
| MFOS-REQ-AMF-0019 | AMF module compromise must not be claimed as contained by Baseline system integrity. | claim review |
| MFOS-REQ-AMF-0020 | AMF failure paths must return typed failure and must not return fake success. | no-fake-success CI |
| MFOS-REQ-AMF-0021 | Baseline-AMF-Disabled MUST return `MFOS_ERR_UNSUPPORTED` for AMF load and MUST NOT create an AMF registry entry or executable mapping. | negative test |
| MFOS-REQ-AMF-0022 | Phase 1 and Phase 2 implementation tasks MUST NOT include production AMF load support. | roadmap review |
| MFOS-REQ-AMF-0023 | AMF-Test MUST be explicitly marked non-production and MUST NOT support production claims. | conformance review |
| MFOS-REQ-AMF-0024 | Enterprise-AMF MUST require signed, measured, revocable, immutable-source, securityd-authorized, auditd-recorded governance before production load is eligible. | evidence review |
| MFOS-REQ-AMF-0025 | High-Assurance-AMF MUST require Guard-approved AMF registry and Guard-approved executable mapping. | Guard evidence review |

## 12. Invariants

```text
INV-AMF-001:
  No AMF module reaches READY unless signature, digest, manifest schema,
  revocation, security epoch, catalog immutability, ABI validation,
  securityd authorization, executable mapping policy, and required audit
  obligations have succeeded.

INV-AMF-002:
  An AMF registry entry is valid only for the exact module digest,
  manifest digest, authority class, policy_version, catalog_generation,
  security_epoch, and profile for which it was approved.

INV-AMF-003:
  AMF modules must not receive arbitrary caller pointers. All caller data
  crosses AMF boundaries through typed handles or sealed bounded buffers.

INV-AMF-004:
  No AMF authority class may include audit disable, policy bypass, direct
  security root mutation, or direct audit root mutation.

INV-AMF-005:
  High-Assurance AMF registry state is not authoritative unless Guard-sealed.

INV-AMF-006:
  A DENY or failure during AMF load must be audited before the caller is told
  that loading failed, unless profile failure policy explicitly enters
  recovery mode because audit is unavailable.
```

## 13. Securityd Obligations

`securityd` must decide:

- Whether the subject may request AMF load.
- Whether the module authority class is allowed.
- Whether the module can bind to the requested service endpoint.
- Whether dual control or operator confirmation is required.
- Whether the request is allowed under the current policy version.
- Whether load is denied because of emergency mode, revocation state, or security epoch.

Decision input:

```yaml
AMFAuthorizationRequest:
  subject: SubjectRef
  operation: AMF_LOAD | AMF_UNLOAD | AMF_REGISTER_ENDPOINT | AMF_REVOKE | AMF_QUERY
  module_id: string
  module_digest: sha384
  manifest_digest: sha384
  signer_id: string
  authority_class: string
  policy_version: uint64
  security_epoch: uint64
  profile: Baseline | Enterprise-Standalone | Enterprise-PXM | High-Assurance
  context:
    correlation_id: uuid
    operator_command_id: string?
    update_transaction_id: string?
```

Decision result:

```yaml
AMFAuthorizationDecision:
  decision: ALLOW | DENY | ALLOW_WITH_AUDIT | REQUIRE_DUAL_CONTROL | REQUIRE_GUARD_APPROVAL | UNSUPPORTED | SPEC_GAP
  reason_code: string
  obligations:
    - audit
    - dual_control
    - operator_confirmation
    - guard_approval
  policy_version: uint64
```

## 14. Audit Obligations

AMF audit records must include:

- `schema_version`.
- `record_id`.
- `timestamp_utc`.
- `component_id = amfd`.
- `correlation_id`.
- `subject`.
- `operation`.
- `module_id`.
- `module_digest`.
- `manifest_digest`.
- `signer_id`.
- `authority_class`.
- `decision`.
- `reason_code`.
- `policy_version`.
- `security_epoch`.
- `catalog_entry_generation`.
- `profile`.
- `guard_seal_version` when applicable.
- `previous_hash`.
- `record_hash`.

Events that must be audited:

- AMF load request.
- Manifest validation failure.
- Signature or digest failure.
- Revocation failure.
- Security epoch failure.
- Securityd allow or deny.
- Guard allow or deny.
- Executable mapping allow or deny.
- AMF registry mutation.
- AMF ready.
- AMF unload.
- AMF runtime endpoint authorization failure.

## 15. Failure Modes

| Failure | Required behavior |
| --- | --- |
| AMF mode disabled | Return `MFOS_ERR_UNSUPPORTED`; do not resolve, map, register, or return success. |
| Missing manifest | Return `MFOS_ERR_INVALID_PARAMETER`; audit failure. |
| Malformed manifest | Return `MFOS_ERR_INVALID_PARAMETER`; audit failure. |
| Missing source refs | Return `MFOS_ERR_SPEC_GAP`; audit failure. |
| Invalid signature | Return `MFOS_ERR_AMF_SIGNATURE_INVALID`; audit failure. |
| Digest mismatch | Return `MFOS_ERR_INTERNAL_CORRUPTION`; audit failure. |
| Revoked signer or digest | Return `MFOS_ERR_AMF_REVOKED`; audit failure. |
| Stale security epoch | Return `MFOS_ERR_ROLLBACK_DETECTED`; audit failure. |
| Non-immutable catalog entry | Return `MFOS_ERR_IMMUTABLE`; audit failure. |
| Securityd unavailable | Fail closed; operator recovery only. |
| Auditd unavailable | Fail according to profile; security-sensitive load fails closed. |
| Guard required but unavailable | Return `MFOS_ERR_GUARD_REQUIRED`; High-Assurance boot/load denied. |
| Guard denies | Return `MFOS_ERR_GUARD_DENIED`; audit alert. |
| W^X mapping cannot be enforced | Return `MFOS_ERR_UNSUPPORTED`; no load. |
| ABI undefined | Return `MFOS_ERR_SPEC_GAP`; no load. |

## 16. Positive Tests

- `amf_disabled_mode_returns_unsupported_without_side_effects`.
- `amf_test_load_valid_signed_module_succeeds`.
- `amf_test_load_from_immutable_system_dataset_succeeds`.
- `amf_manifest_declares_authority_class`.
- `amf_registry_binds_digest_policy_epoch_generation`.
- `amf_ready_emits_audit_record`.
- `amf_enter_endpoint_with_typed_buffer_succeeds`.
- `amf_high_assurance_guard_approved_load_succeeds`.
- `amf_enterprise_revocation_metadata_valid_succeeds`.

## 17. Negative Tests

- `amf_disabled_mode_does_not_map_or_register`.
- `amf_rejects_unsigned_artifact`.
- `amf_rejects_invalid_signature`.
- `amf_rejects_digest_mismatch`.
- `amf_rejects_missing_authority_class`.
- `amf_rejects_unknown_authority_class`.
- `amf_rejects_missing_source_matrix_refs`.
- `amf_rejects_mutable_catalog_entry`.
- `amf_rejects_user_dataset_load`.
- `amf_rejects_revoked_signer`.
- `amf_rejects_revoked_digest`.
- `amf_rejects_stale_security_epoch`.
- `amf_rejects_policy_version_mismatch`.
- `amf_rejects_writable_executable_mapping`.
- `amf_rejects_arbitrary_pointer_abi`.
- `amf_rejects_endpoint_outside_authority_class`.
- `amf_fails_closed_when_securityd_unavailable`.
- `amf_fails_closed_when_audit_required_but_unavailable`.
- `amf_high_assurance_rejects_without_guard_approval`.
- `amf_rejects_fake_success_for_unsupported_load_kind`.

## 18. Fuzz Targets

- `fuzz_amf_manifest_yaml`.
- `fuzz_amf_manifest_json`.
- `fuzz_authority_class_parser`.
- `fuzz_amf_entry_request_decoder`.
- `fuzz_amf_registry_recovery_log`.
- `fuzz_revocation_metadata`.
- `fuzz_amf_error_mapping`.

Fuzz targets must classify malformed input as `MFOS_ERR_INVALID_PARAMETER`, unsupported declared-but-unimplemented features as `MFOS_ERR_UNSUPPORTED`, and undefined behavior as `MFOS_ERR_SPEC_GAP`.

## 19. Conformance Profiles

### Baseline

Baseline uses `Baseline-AMF-Disabled` unless an explicitly non-production AMF test profile is selected.

- AMF specification exists.
- Manifest schema MAY be implemented for validation tests.
- AMF load MUST return `MFOS_ERR_UNSUPPORTED`.
- No AMF registry entry may be committed.
- No AMF executable mapping may be created.
- W^X is still required for the nucleus and for any AMF-Test mapping.
- Guard not required.

### AMF-Test

- Explicitly non-production.
- Signed test-only AMF modules MAY load.
- No production conformance or production readiness claim may depend on AMF-Test.
- securityd authorization, auditd records, W^X, and negative tests are still required.

### Enterprise-Standalone and Enterprise-PXM

Enterprise-Standalone and Enterprise-PXM use AMF disabled by default. A release may separately claim `Enterprise-AMF` only when all of these are implemented and evidenced:

- Signed and measured AMF artifacts.
- Revocation metadata.
- Security epoch.
- Immutable source dataset or approved artifact store.
- securityd authorization.
- auditd records before success or deny returns.
- TUF-like update metadata integration for shipped AMF modules.
- Remote audit export for AMF security events.

Enterprise-PXM MAY use Guard as a measurement helper only, but this does not create a High-Assurance claim.

### High-Assurance

- High-Assurance-AMF includes all Enterprise-AMF requirements.
- Guard approval required for AMF load when AMF is in scope.
- AMF registry Guard seal required.
- Executable mapping policy Guard approval required.
- Remote attestation evidence required for production claim.
- Guard failure policy must be fail-secure.

## 20. Spec Gaps

- AMF authority class taxonomy is not yet complete.
- Concrete signature algorithms and key formats are not yet fixed.
- AMF binary format is not yet specified.
- AMF unload and rollback semantics need a separate state machine.
- AMF runtime revocation behavior for already-loaded modules is not yet finalized.
- AMF interaction with live patching is intentionally unspecified.
- AMF module sandboxing beyond typed ABI and page permissions is not yet specified.
- Guard seal serialization format is not yet specified.
- Dual-control operator workflow is referenced but not fully specified here.

## 21. Inactive Future Implementation Prompt Template

Phase status: inactive future template. This section does not authorize production implementation, hosted daemon implementation, or portable semantic-core implementation.

```text
Future authorized implementation agents would implement MFOS AMF.

Implement only the requirement IDs listed in the task. Do not claim z/OS
compatibility. Treat AMF as MFOS OS-extension authorization, not admin
privilege.

Required output:
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

Rules:
- If the task is Phase 1, Phase 2, or Baseline-AMF-Disabled, AMF load must return MFOS_ERR_UNSUPPORTED and must not map or register a module.
- Only implement production AMF load when the task explicitly names Enterprise-AMF or High-Assurance-AMF requirements.
- Use securityd for final authorization.
- Use auditd for all AMF decisions and state changes.
- Do not return success for missing, unsupported, or undefined behavior.
- Use MFOS_ERR_UNSUPPORTED for specified but unimplemented features.
- Use MFOS_ERR_SPEC_GAP for unspecified behavior.
- Do not accept arbitrary pointers across AMF ABI.
- Enforce W^X and RX-after-verification executable mapping.
- In High-Assurance, require Guard approval before READY.
- Add negative tests with the implementation.
```
