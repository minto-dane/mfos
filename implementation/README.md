# implementation/

This directory is the canonical future layout root for MFOS implementation
scaffolds. Its presence does not authorize current implementation work.

It is grouped here so OS body code does not sit at the same top-level as
documentation, requirements, tests, and evidence. MFOS is not a single
application, so the top-level directory is `implementation/` rather than `src/`.

Subdirectories:

```text
runtime/      shared ABI, IDs, errors, handles, serialization, generated types
nucleus/      MFOS nucleus, phase 2+
services/     securityd, auditd, catalogd, datasetd, jobd, spoold, operatord...
pxm/          partition manager, Enterprise-PXM+
guard/        High-Assurance root object protection
sidecars/     Linux desktop, service, recovery, diagnostics partitions
interfaces/   operator console, command-processor, panel-ui, management APIs, gateways
tools/        host and MFOS tools
prototypes/   future non-production prototypes; blocked in Phase 1 unless a later gate explicitly authorizes them
```

Each component may contain its own `src/` directory only after a later approved
implementation gate:

```text
implementation/services/securityd/src/
implementation/nucleus/src/
implementation/pxm/core/src/
implementation/guard/src/
implementation/tools/mfctl/src/
```

Do not infer implementation authority or production readiness from the presence
of a directory. Production claims require requirements, source IDs, tests, audit
obligations, and evidence.

Phase 1 is limited to Dafny executable-semantics scaffold work and loader-only
artifact validation under `formal/executable-semantics/dafny/`. Phase 1 does
not authorize Rust semantic-core work, hosted semantic prototypes, semantic
runner implementation, hosted daemons, service implementation, PXM/MFVM/CVM
implementation, cluster implementation, or production code.
