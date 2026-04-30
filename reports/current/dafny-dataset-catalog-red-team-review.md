# Dafny Dataset/Catalog Red-Team Review

Status: current.

Critical/Major checks addressed: handles cannot be created without ALLOW or ALLOW_WITH_AUDIT; uncommitted, rolled-back, partial-journal, and integrity-failed catalog entries cannot resolve; stale policy/catalog/dataset generations are rejected; DENY creates no handle; DENY with audit obligation links to before-return audit or audit-unavailable fail-closed behavior; Dataset is not treated as a POSIX file; coverage C5 rows require Dafny symbols, verification evidence, and fixture/oracle/golden links; formal claims remain below proof-backed levels; Python tooling remains non-semantic; no Rust semantic-core or production implementation was introduced.
