# Phase 1.4.1 Open Issues

Status: current.

No Critical or Major merge blockers remain for the Phase 1.4.1 Job lifecycle,
effective principal, and DD resolution scope.

Deferred outside this PR:

- full spool lifecycle and output semantics;
- full operator console semantics;
- first vertical slice completion;
- real job execution and program loading;
- production services or hosted daemons;
- formal proof artifacts for formal claims above C3.

Closed in this review cycle:

- DD authorization decisions are now bound to current Job/DD correlation,
  effective principal subject, object, operation, and policy version.
- Cross-request authorization replay and DENY-with-`MFOS_OK` incoherence are
  verified fail-closed properties.
- PR #29 evidence blockers were remediated: cancelled-job fixture/golden
  evidence now uses one JobState space and modeled `MFOS_ERR_INVALID_STATE`;
  valid-submit evidence now reflects the two atomic Dafny transitions; and
  broad parent requirement rows no longer claim requirement-wide C4.
