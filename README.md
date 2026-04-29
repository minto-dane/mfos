# MFOS

MFOS is an independent enterprise operating-system design project. It uses
publicly available external documentation as bibliographic reference material
for source discovery, non-compatibility boundaries, and independent design
traceability.

MFOS is not affiliated with, endorsed by, sponsored by, certified by, or
approved by IBM. MFOS does not claim compatibility with IBM products,
interfaces, record layouts, command syntax, macro interfaces, or documentation.

The current canonical design corpus lives under [docs/design](docs/design/).
The top-level directories added here are the project work layers that will
receive implementation, verification, source-grounding, and AI task artifacts
over time. They intentionally do not move or rewrite the existing design docs.

## Canonical Artifacts

- Design canon: [docs/design/mfos-design.md](docs/design/mfos-design.md)
- Source cards: [docs/design/source-matrix/cards](docs/design/source-matrix/cards)
- Source card index: [docs/design/source-matrix/source-matrix.yml](docs/design/source-matrix/source-matrix.yml)
- Requirement registry: [docs/design/registries/requirements.yaml](docs/design/registries/requirements.yaml)
- Split specs: [docs/design/specs](docs/design/specs)
- Status: [docs/design/STATUS.md](docs/design/STATUS.md)

## Project Layers

```text
sources/        source-grounding metadata and future concept cards
specs/          top-level bridge to canonical specifications
requirements/   top-level bridge to machine-readable requirements
schemas/        executable schema home, initially bridged to docs/design
claims/         assurance claim tree home
formal/         formal models and invariants
tests/          positive, negative, crash, conformance, and fault tests
fuzz/           fuzz targets, corpora, dictionaries
evidence/       evidence archive, never a substitute for auditd
ci/             source, requirement, wording, and no-fake-success gates
implementation/ OS body, hosted prototype, runtime, tools, and interfaces
ai/             AI contracts, task packets, reviewed outputs
```

`implementation/` is intentionally not named `src/`. MFOS is not a single
program: nucleus, services, PXM, Guard, hosted prototypes, runtime ABIs, and
tools have different assurance boundaries. Each implementation component may
use its own internal `src/` directory when code is added.

## Local Checks

```bash
./scripts/validate-all.sh --check
python3 scripts/validators/validate-source-cards.py
python3 scripts/validators/validate-requirements.py
./scripts/validate-naming-safety.sh release
./scripts/validate-artifact-hygiene.sh
./scripts/validate-component-scaffold.sh
./scripts/validate-language-formal-assurance.sh
./scripts/validate-dafny-semantics-scaffold.sh
python3 scripts/checks/check-prohibited-terms.py
python3 scripts/checks/check-no-fake-success.py
```

These checks validate the current design artifacts, naming-safety release gate,
artifact hygiene, component scaffold metadata, language/formal assurance, and
Dafny Phase 1 boundary. CI invokes the aggregate gate and focused scaffold
checks.
