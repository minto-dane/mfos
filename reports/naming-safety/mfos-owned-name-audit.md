# MFOS-Owned Name Audit

Date: 2026-04-27

Scope: file paths plus YAML/Markdown identifiers in MFOS-owned contexts. Source
cards, Source Matrix material, NOTICE, non-compatibility/legal/prohibited-wording
material, source policy material, and prior migration/audit reports were treated
as allowed contexts and were not counted as violations.

No source files were edited. This report and the matching YAML report are the
only written artifacts.

## Method

Scans covered path names and identifier-like fields/sections including
`spec_id`, titles, pack titles, requirement/test/evidence/claim IDs, service and
interface directory names, prompt headings/roles, component names, audit event
names, artifact paths, and registry namespaces. Source Matrix IDs such as
`EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001` were allowed only when used as source references.

## Findings

### MFOS-NAME-001 - Critical - IBM interface/product tokens in owned interface and service paths

MFOS-owned implementation paths use exact IBM interface/product tokens:

- `implementation/interfaces/command-processor/`
- `implementation/interfaces/panel-ui/`
- `implementation/interfaces/management-api/`
- `implementation/services/commandd/`
- `implementation/services/paneld/`

Representative identifier references:

- `implementation/interfaces/README.md:3` lists `command processor`, `panel UI`, and `management API`.
- `implementation/README.md:18` lists `command processor` and `panel UI`.

Risk: these are owned interface/service names, not source citations or
non-compatibility examples. They can imply MFOS-owned compatibility surfaces for
IBM TSO, ISPF, or z/OSMF.

Recommended rename/update:

- `command-processor` -> `interactive-session`
- `panel-ui` -> `panel-ui`
- `management-api` -> `management-api`
- `commandd` -> `sessiond`
- `paneld` -> `paneld`
- Update README text, implementation indexes, traceability references, and any
  report-only mentions after the owned paths are renamed.

### MFOS-NAME-002 - Major - workload policy used as an owned MFOS namespace

`WLM` appears as a MFOS-owned spec, pack, service, requirement/test/evidence
namespace, local requirement prefix, audit-event prefix, artifact path, and prompt
target.

Representative locations:

- `docs/design/specs/11-workload-policy.md:2` uses `MFOS-SPEC-11-WORKLOAD-POLICY`.
- `docs/design/specs/11-workload-policy.md:10` uses `MFOS-REQ-WPOL-*`.
- `docs/design/specs/11-workload-policy.md:80` through `89` define `WPOL-R-*`.
- `docs/design/specs/11-workload-policy.md:331` through `339` define `WORKLOAD_POLICY_*` and
  `WLM_*` audit/event identifiers.
- `packs/pack-index.yml:130` through `136` define PACK-10 as Workload Policy
  with `docs/design/specs/11-workload-policy.md`, `workpolicyd`, and `MFOS-REQ-WPOL-*`.
- `requirements/catalog.yml:19` uses planned split domain `wlm`.
- `docs/design/registries/requirements.yaml:5653` and following entries use
  `MFOS-REQ-WPOL-*`.
- `docs/design/registries/tests.yaml:4123` and following entries use
  `MFOS-TEST-WPOL-*`.
- `docs/design/registries/evidence.yaml:3700` and following entries use
  `MFOS-EVID-WPOL-*`.
- `implementation/services/workpolicyd/` and
  `implementation/prototypes/hosted-semantic/services/workpolicyd/` are owned service
  paths.

Risk: workload policy is an IBM z/OS workload management acronym. Source references such as
`EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001` are allowed, but `WLM` as an MFOS-owned namespace creates a
compatibility/name-ownership risk.

Recommended rename/update:

- `docs/design/specs/11-workload-policy.md` -> `docs/design/specs/11-workload-policy.md`
- `MFOS-SPEC-11-WORKLOAD-POLICY` -> `MFOS-SPEC-11-WORKLOAD-POLICY`
- `MFOS-REQ-WPOL-*` -> `MFOS-REQ-WPOL-*`
- `MFOS-TEST-WPOL-*` -> `MFOS-TEST-WPOL-*`
- `MFOS-EVID-WPOL-*` -> `MFOS-EVID-WPOL-*`
- `WPOL-R-*`, `INV-WPOL-*`, and `WORKLOAD_POLICY_*` -> `WPOL-R-*`, `INV-WPOL-*`,
  and `WORK_POLICY_*`
- `workpolicyd` -> `workpolicyd`
- `requirements` planned domain `wlm` -> `workload-policy`
- PACK-10 title `Workload Policy` -> `Workload Policy`
- Keep `EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001` only as a source reference in allowed source-reference
  fields.

### MFOS-NAME-003 - Major - SVC/PCALL used as owned ABI namespaces

The owned ABI and requirement namespace uses IBM-derived system interface terms
`SVC` and `PCALL`.

Representative locations:

- `docs/design/specs/15-svc-pcall.md:2` uses `MFOS-SPEC-15-SVC-PCALL`.
- `docs/design/specs/15-svc-pcall.md:10` uses `MFOS-REQ-PCALL-*` and
  `MFOS-REQ-SVC-*`.
- `docs/design/specs/15-svc-pcall.md:372` through `391` define
  `MFOS-REQ-SVC-*` and `MFOS-REQ-PCALL-*`.
- `packs/pack-index.yml:159` through `165` names PACK-13
  `Nucleus and SVC/PCALL`.
- `evidence/traceability/pack-to-artifacts.yml:138` through `142` references
  `MFOS-REQ-SVC-*`, `MFOS-REQ-PCALL-*`, and `15-svc-pcall.md`.
- Owned paths include `implementation/nucleus/svc/`,
  `implementation/runtime/abi/svc/`, `implementation/guard/roots/svc-table/`,
  `implementation/nucleus/pcall/`, and `implementation/runtime/abi/pcall/`.

Risk: `SVC` is strongly associated with z/OS supervisor-call terminology, and
`PCALL` is used here as the owned name for a source-grounded cross-memory
service-entry concept. These are not just source IDs; they are MFOS-owned ABI
names and path names.

Recommended rename/update:

- `15-svc-pcall.md` -> `15-kcall-service-ipc.md`
- `MFOS-SPEC-15-SVC-PCALL` -> `MFOS-SPEC-15-KCALL-SERVICE-IPC`
- `MFOS-REQ-SVC-*` -> `MFOS-REQ-KCALL-*`
- `MFOS-REQ-PCALL-*` -> `MFOS-REQ-SIPC-*`
- `SVC` path/name family -> `kcall` or `kernel-call`
- `PCALL` path/name family -> `service-ipc` or `endpoint-call`
- `svc-table` -> `kcall-table`
- Update pack title, traceability maps, tests, evidence IDs, artifact paths, and
  prompt snippets consistently.

### MFOS-NAME-004 - Minor - IBM-specific prompt role and prompt field names

The canonical prompt library uses IBM-specific prompt identifiers outside the
Source Matrix directory:

- `docs/design/prompts/ai-prompts.md:54` heading `IBM Concept Mapping Prompt`
- `docs/design/prompts/ai-prompts.md:57` role `MFOS IBM Concept Mapping reviewer`
- `docs/design/prompts/ai-prompts.md:66` and `67` output fields
  `IBM source concept` and `IBM source document title`

Risk: this prompt is source-mapping oriented, but prompts are owned reusable
instructions and were called out as an audit target. If the prompt library is
not formally included in the source-policy allowlist, these names overfit the
workflow to IBM-branded terminology.

Recommended rename/update:

- `IBM Concept Mapping Prompt` -> `External Source Concept Mapping Prompt`
- `MFOS IBM Concept Mapping reviewer` -> `MFOS external source mapping reviewer`
- `IBM source concept` -> `external source concept`
- `IBM source document title` -> `external source document title`
- Keep IBM-specific wording only in source-reference examples or source-card
  workflows.

### MFOS-NAME-005 - Minor - APF-derived AMF namespace needs an explicit allow decision or rename

`AMF` is not an exact IBM product token, but it is an owned MFOS acronym that is
defined as an APF-inspired authorized-module facility. It appears widely as a
spec, pack, service, requirement/test/evidence namespace, artifact path, and
Guard root name.

Representative locations:

- `docs/design/specs/12-amf.md:2` uses `MFOS-SPEC-12-AMF`.
- `docs/design/specs/12-amf.md:10` uses `MFOS-REQ-AMF-*`.
- `docs/design/specs/12-amf.md:399` through `423` define `MFOS-REQ-AMF-*`.
- `docs/design/registries/tests.yaml:1211` and following entries use
  `MFOS-TEST-AMF-*`.
- `docs/design/registries/evidence.yaml:1508` and following entries use
  `MFOS-EVID-AMF-*`.
- Owned paths include `implementation/services/amfd/`,
  `implementation/prototypes/hosted-semantic/services/amfd/`, and
  `implementation/guard/roots/amf-registry/`.

Risk: because AMF intentionally maps APF concepts into MFOS, it may still be
treated as an IBM-related owned identifier under a strict naming policy even
though it is not the literal IBM acronym `APF`.

Recommended rename/update:

- If AMF is allowed, add an explicit naming-policy exception that says `AMF` is a
  coined MFOS term and not an IBM product/interface token.
- If strict prohibition covers IBM-derived analogue names, rename `AMF` to a
  neutral namespace such as `MODAUTH` or `MODULE-AUTH`.
- Suggested concrete names: `12-module-auth.md`, `MFOS-SPEC-12-MODULE-AUTH`,
  `MFOS-REQ-MODAUTH-*`, `moduleauthd`, and `module-auth-registry`.

## Non-Findings

- Source card filenames and Source Matrix source IDs such as `EXTREF-IBM-ZOS-SYSTEM-INTEGRITY-0001`,
  `EXTREF-IBM-ZOS-WLM-SERVICE-CLASSES-0001`, and `EXTREF-IBM-Z-ARCHITECTURE-PRINCIPLES-0001` are allowed in source-card/source-matrix
  contexts.
- `NOTICE.md`, non-compatibility statements, prohibited wording examples, and
  prior audit/migration reports were treated as allowed contexts.
- No prohibited IBM-related token was found in schema file names under
  `schemas/`.
- No claim ID family using prohibited IBM-related tokens was found.

