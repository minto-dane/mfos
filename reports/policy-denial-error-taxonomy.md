# Policy-Denial Error Taxonomy

Status: closed for PR #5 review.

## Decision

Phase 1 executable-spec artifacts use this minimum error taxonomy:

| Error code | Meaning | Phase 1 use |
| --- | --- | --- |
| `MFOS_ERR_UNAUTHENTICATED` | No valid subject, principal, session, or authenticated identity exists. | Missing job effective principal, missing operator session, or untrusted subject identity. |
| `MFOS_ERR_POLICY_DENIED` | A valid subject exists, but policy denies the requested object, operation, context, and policy version. | Primary policy-denial error for authorization-denied protected-resource operations. |
| `MFOS_ERR_UNAUTHORIZED` | Legacy umbrella wording. | Deprecated alias or cleanup target; not a primary Phase 1 policy-denial result. |

## First Vertical Slice Mapping

BOB is a valid subject in the denied first-vertical-slice path. BOB's attempted
`READ` of `USER.ALICE.INPUT` is therefore a policy denial:

```yaml
subject: BOB
object: USER.ALICE.INPUT
operation: READ
decision: DENY
error_code: MFOS_ERR_POLICY_DENIED
reason_code: DATASET_READ_NOT_PERMITTED
```

Required consequences:

- no dataset handle of any kind is created;
- the deny audit record has `before_return: true`;
- the job failure and operator display remain fail-closed;
- `MFOS_ERR_SPEC_GAP` is no longer used for this path.

## Similar Closure

The Phase 0.9 authorization negative test for protected-resource handle
creation also had a valid subject with a denied protected effect. It now uses:

```yaml
error_code: MFOS_ERR_POLICY_DENIED
reason_code: PROTECTED_RESOURCE_HANDLE_NOT_PERMITTED
```

Pre-Phase 0.9 planning catalogs still contain some `MFOS_ERR_UNAUTHORIZED`
wording. Those entries are not Phase 1 executable-spec inputs and are recorded
as legacy cleanup context rather than Phase 1 blockers.
