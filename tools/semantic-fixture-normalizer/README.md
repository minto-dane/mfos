# Semantic Fixture Normalizer

The normalizer converts Phase 0.9 fixture YAML into a deterministic JSON shape
for Dafny-facing artifact checks.

It does not implement MFOS business semantics, does not evaluate
authorization, does not parse external command syntax, and does not decide
whether a fixture passes.

Example:

```bash
python3 tools/semantic-fixture-normalizer/src/normalize.py tests/fixtures/first-vertical-slice/hello-job.yml
```
