# Contributing

MFOS changes are source-grounded. A change that introduces z/OS-inspired
semantics must cite Source Matrix IDs and update requirements, tests, and audit
obligations where applicable.

Future implementation work must stay under `implementation/` and remains blocked
until a reviewed implementation gate explicitly permits it. The hosted semantic
prototype path `implementation/prototypes/hosted-semantic/` is superseded and
blocked, not implementation-ready.

## Advisory CodeRabbit Review

CodeRabbit is advisory in Phase 1. Its comments and status checks are review
inputs, not required branch-protection gates, and they must not replace the
repository validation suite, human review, source-grounding checks, or phase
boundary review.

Draft PRs are not automatically reviewed by CodeRabbit. Authors may request a
manual CodeRabbit review on a draft PR when early feedback is useful.

Phase 1.4.1 and later Phase 1 PRs should request or record CodeRabbit review,
or explicitly record why it was skipped. A Phase 1 PR must not be blocked solely
because CodeRabbit did not run, failed to run, or produced advisory findings.

Phase 2 is the earliest recommended point to make CodeRabbit hard-required for
implementation-affecting PRs, and only after several successful advisory runs
show stable, low-noise behavior. Repository owners must explicitly update branch
protection before CodeRabbit becomes required.

Phase 3 and later may make CodeRabbit required for all nontrivial PRs if the
advisory period remains stable. CodeRabbit must never become the sole quality
gate.
