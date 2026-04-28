# AI Usage Policy

AI-generated MFOS work must not invent enterprise OS semantics without source
grounding. Before code is written, the AI work packet must identify:

- implemented requirement IDs
- Source Matrix IDs
- assumptions and spec gaps
- security invariants
- audit obligations
- failure modes
- positive and negative tests
- fuzz targets where parsers are involved
- evidence artifacts

Fake success, empty stubs, and silent fallback are prohibited in production
paths.

