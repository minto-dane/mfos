# MFOS v0.5 Requirements Catalog Schema

This document defines the required shape for
`docs/design/registries/requirements.yaml`. The YAML catalog is the
machine-readable requirement source for v0.5 priority requirements.

## Canonical Language

English is canonical for machine-readable keys, requirement IDs, enum values,
error codes, ABI names, and normative requirement text. Japanese documents may
mirror or explain the catalog, but Japanese commentary must not override this
catalog unless a reviewed bilingual parity process updates both artifacts.

## Registry Fields

Required top-level fields:

- `registry_kind`: must be `requirements`.
- `schema_version`: integer schema version.
- `registry_id`: stable registry identifier.
- `catalog_version`: human version, for example `v0.5`.
- `status`: `draft`, `reviewed`, `approved`, or `superseded`.
- `schema_ref.path`: path to this schema note.
- `source_matrix_ref.path`: path to the source matrix YAML.
- `non_compatibility_statement`: must state that MFOS is z/OS-inspired and does
  not claim z/OS or IBM product compatibility.
- `language_policy`: canonical and conflict-resolution language rules.
- `profile_model`: the four v0.5 profiles and allowed applicability values.
- `source_type_values`: allowed `source_refs[].source_type` values.
- `status_values`: allowed entry statuses.
- `entries`: requirement records.
- `spec_gaps`: known gaps in the registry.

## Requirement Entry Fields

Every entry in `entries` must include these fields:

- `requirement_id`: stable ID, such as `MFOS-REQ-CATALOG-0002`.
- `title`: short English title.
- `normative_text`: normative requirement text using RFC-style uppercase
  `MUST`, `MUST NOT`, `SHOULD`, `MAY`, or explicit fail-closed wording.
- `source_refs`: non-empty list of source references.
- `profile_applicability`: profile applicability for all four v0.5 profiles.
- `target_components`: one or more implementation, CI, docs, or review targets.
- `verification`: primary methods and linked positive/negative tests.
- `audit_obligation`: audit requirement object.
- `failure_mode`: typed fail-closed behavior.
- `evidence_required`: one or more required evidence artifacts.
- `status`: entry lifecycle status.

## Source References

Each `source_refs` item must include:

```yaml
source_id: EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001
source_type: normative
role: system_integrity_semantic_root
```

Allowed `source_type` values:

- `normative`
- `informative`
- `internal_transfer`

`source_id` must resolve through
`docs/design/source-matrix/source-matrix.yml`. Informative sources must not be
used as the sole semantic root for z/OS-inspired MFOS concepts.

## Profile Applicability

Every requirement must include all four v0.5 profile keys:

```yaml
profile_applicability:
  baseline: required
  enterprise_standalone: required
  enterprise_pxm: required
  high_assurance: required
```

Allowed values:

- `required`
- `conditional`
- `optional`
- `not_applicable`
- `prohibited`
- `deferred`

Profile rules:

- `enterprise_standalone` must not claim PXM partition lifecycle,
  side-partition isolation, or passthrough device assignment.
- `enterprise_pxm` is the first Enterprise profile that may claim PXM partition
  lifecycle and device-assignment properties.
- `high_assurance` requires PXM and Guard for selected root-object claims.
- Baseline requires an NX-capable platform and W^X policy.

## Verification Object

`verification` must include:

```yaml
verification:
  primary:
    - negative_test
  tests:
    positive:
      - TEST-MFOS-AREA-POS-0001
    negative:
      - TEST-MFOS-AREA-NEG-0001
```

The `positive` and `negative` lists may be empty only with a written rationale
in a future schema version. For v0.5 priority requirements, both should be
populated.

## Audit Obligation Object

`audit_obligation` must include:

```yaml
audit_obligation:
  obligation: required
  record_type: DATASET_OPEN_DENY
  before_return: true
  redaction_policy: DATASET_NAME_VISIBLE_CONTENT_REDACTED
  notes: "Denied dataset open is audited before final caller result."
```

Allowed `obligation` values:

- `required`
- `conditional`
- `none`

Security-sensitive denials should use `before_return: true`, including
authorization deny, dataset stale handle, operator command deny, AMF load deny
or unsupported load, Guard root mismatch, update rollback, freeze, and
mix-and-match detection.

## Failure Mode Object

`failure_mode` must include:

```yaml
failure_mode:
  error: MFOS_ERR_POLICY_DENIED
  fail_closed: true
  conditions:
    - "securityd denies the operation."
```

Optional field:

- `alternative_errors`: list of `error` and `condition` objects for specific
  typed alternatives.

Runtime security requirements should use `fail_closed: true`.

## Evidence Required

`evidence_required` is a list of evidence descriptors:

```yaml
evidence_required:
  - evidence_type: negative_test_result
    evidence_id: EV-MFOS-DATASET-DENY-0001
```

Expected `evidence_type` values are intentionally open in v0.5. Common values
include `test_result`, `negative_test_result`, `fault_injection_report`,
`audit_record_sample`, `architecture_review_record`, `profile_lint_result`,
`platform_feature_report`, and `conformance_matrix`.

## v0.5 Priority Coverage

The catalog must include machine-readable entries for at least:

- `MFOS-REQ-CATALOG-0002`
- `MFOS-REQ-AUDIT-0002`
- `MFOS-REQ-AUDIT-0005`
- `MFOS-REQ-AUTH-0001`
- `MFOS-REQ-AUTH-0002`
- `MFOS-REQ-AUTH-0004`
- `MFOS-REQ-DATASET-0001`
- `MFOS-REQ-DATASET-0002`
- `MFOS-REQ-DATASET-0006`
- rollback, freeze, and mix-and-match UVS requirements
- `MFOS-REQ-PARTITION-0005`
- `MFOS-REQ-PARTITION-0006`
- `MFOS-REQ-PARTITION-0016`
- `MFOS-REQ-PARTITION-0017`
- an AMF disabled or unsupported-mode requirement
- an NX/W^X Baseline requirement
- an Enterprise profile split requirement

## Validation Checklist

A registry validator should fail when:

- YAML parsing fails.
- An entry lacks any required field.
- `source_refs` is empty.
- A `source_id` does not resolve through the Source Matrix.
- A `profile_applicability` object lacks any of the four v0.5 profile keys.
- A security-sensitive requirement lacks `audit_obligation`.
- A runtime security requirement uses `fail_closed: false`.
- A z/OS-derived term is introduced without a Source Matrix ID.
- `MAY` appears in a security-sensitive requirement without an ADR reference.
- `enterprise_standalone` claims PXM device assignment, side-partition
  isolation, or partition lifecycle properties.
- AMF disabled mode returns success for a load request.
