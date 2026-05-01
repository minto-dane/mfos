# Artifact Hygiene Open Issues

Status: current

No blocking artifact hygiene issues remain.

Nonblocking follow-up:

- Current fixture and golden-vector filenames retain stable scenario sequence
  suffixes such as `0901`. These are treated as deterministic scenario IDs,
  not phase-specific filenames. If the project later wants human-only names,
  perform a separate reference-preserving fixture/golden rename.
