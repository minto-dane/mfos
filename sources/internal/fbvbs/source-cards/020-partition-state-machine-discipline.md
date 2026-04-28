---
source_id: INT-FBVBS-PARTITION-STATE-MACHINE-0001
source_kind: repository_reference
source_type: internal_transfer
semantic_role: lifecycle_pattern
vendor: minto-dane
document_title: FBVBS partition state-machine discipline transfer card
document_url:
  - https://github.com/minto-dane/fbvbs
retrieved_at: "2026-04-28"
authority_status: preparatory_until_adr_migration
citation_scope: path_and_commit_only
retrieval_metadata:
  retrieved_at: "2026-04-28"
  retrieved_by: FBVBS Internal Source Grounding Worker
  public_url: https://github.com/minto-dane/fbvbs
  landing_page_url: https://github.com/minto-dane/fbvbs
  source_version: 30e6fb54c76eaec83d03f79e1fd96c030cca504b
  section_scope: partition lifecycle, command contracts, precondition validators
  local_cache_manifest: temporary clone at /tmp/fbvbs-upstream, not committed
cache_disposition: temporary_ignored_cache
reference_purpose:
  - lifecycle concept mapping
  - command safety transfer screening
review_topics:
  - partition state machine
  - mutation preconditions
  - postcondition validation
mfos_mapping:
  mfos_components:
    - lifecycle
    - operator-control
  mfos_specs: []
  mfos_requirements:
    - unassigned-preparatory
mfos_divergence:
  - MFOS object lifecycle names and legal transitions must be independently specified.
prohibited_inference:
  - Do not treat FBVBS partition states as MFOS state names.
  - Do not treat operator UI flows as state-machine authority.
legal_controls:
  public_safe: true
  no_copied_text: true
  no_long_quotes: true
  no_tables_copied: true
  no_diagrams_copied: true
  no_record_layouts_copied: true
  no_command_syntax_copied: true
  no_macro_signatures_copied: true
  no_message_tables_copied: true
  attribution_required: true
  trademark_reference_only: true
  no_affiliation_claim: true
  no_compatibility_claim: true
  no_conformance_claim: true
  no_certification_claim: true
  no_source_substitution: true
  external_affiliation_claimed: false
  compatibility_claimed: false
  substitute_for_source: false
source_refs:
  - source_id: INT-FBVBS-PARTITION-STATE-MACHINE-0001
    source_type: internal_transfer
    source_version: 30e6fb54c76eaec83d03f79e1fd96c030cca504b
    paths:
      - plan/standalone/subsystems/storage-and-state-management.md
      - plan/standalone/operations/operator-control-plane.md
      - hypervisor/tools/partition/standalone_command_contracts.py
      - hypervisor/tools/partition/validate_partition_transition_preconditions.py
requirement_refs:
  - unassigned-preparatory
review_status: draft
---

# Source Card: Partition State-Machine Discipline

Grounding revision: `30e6fb54c76eaec83d03f79e1fd96c030cca504b`

Upstream anchors:

- `plan/standalone/subsystems/storage-and-state-management.md`
- `plan/standalone/operations/operator-control-plane.md`
- `hypervisor/include/fbvbs_abi.h`
- `hypervisor/src/partition.c`
- `hypervisor/tools/partition/standalone_command_contracts.py`
- `hypervisor/tools/partition/validate_partition_transition_preconditions.py`
- `hypervisor/tools/partition/validate_teardown_postconditions.py`

Public-safe MFOS mapping note:

FBVBS encodes lifecycle state as an authoritative runtime contract. Partition states include creation, measurement, loading, runnable/running, quiesced, faulted, and destroyed phases. Management operations are tied to allowed source states and expected repeat behavior. Recovery is guarded by approval artifacts; destructive storage operations require confirmation artifacts.

Transferable mechanism:

1. Give every externally visible mutation a named command contract.
2. Declare allowed source states and predicted status for repeats.
3. Require artifact preconditions for recover, destructive, and break-glass actions.
4. Validate preconditions from diagnostics before issuing commands.
5. Validate postconditions after teardown, detach, revoke, or destroy.

MFOS adoption rule:

- Adopt: source-state allowlists, explicit repeat semantics, and pre/post validators.
- Adapt: FBVBS partition and vdisk names into MFOS object and isolation-domain names.
- Reject: ad hoc transitions introduced only in UI or operator tooling.

MFOS design note:

State-machine discipline should live below presentation layers. Operator surfaces may request actions, but they must not define the legal transition graph.

Known source gap to preserve:

- Upstream marks live migration/checkpoint/replication and cluster control-plane primitives as unimplemented. MFOS should treat migration-state rules as a separate design root, not as already covered by basic partition lifecycle.
