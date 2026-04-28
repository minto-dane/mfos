# implementation/

This directory contains implementation work for MFOS.

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
prototypes/   hosted semantic prototype, phase 1
```

Each component may contain its own `src/` directory when code is added:

```text
implementation/services/securityd/src/
implementation/nucleus/src/
implementation/pxm/core/src/
implementation/guard/src/
implementation/tools/mfctl/src/
```

Do not infer production readiness from the presence of a directory. Production
claims require requirements, source IDs, tests, audit obligations, and evidence.
