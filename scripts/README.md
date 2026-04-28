# scripts/

Local validation and bootstrap scripts.

Current useful checks:

```bash
python3 scripts/validate-source-cards.py
python3 scripts/validate-requirements.py
python3 scripts/validate-claims.py
python3 scripts/validate-spec-front-matter.py
python3 scripts/validate-packs.py
python3 scripts/check-prohibited-terms.py
python3 scripts/check-no-fake-success.py
python3 scripts/check-source-grounding.py
python3 scripts/check-audit-obligations.py
python3 scripts/check-spec-gap-misuse.py
python3 scripts/generate-traceability.py
./scripts/validate-all.sh
```

`./scripts/validate-all.sh` is the Phase 0.6 convenience entrypoint. It runs
the local draft-mode validation suite and regenerates traceability matrices.

Use `--mode release` on validators that support it only after draft warnings
have been resolved. Phase 0.6 remains a design-enforcement phase and does not
authorize production implementation.
