// MFOS Phase 1 Dafny executable semantics.
// Non-production specification artifact. No host OS, daemon, service, or Rust core.

module Common {
  type MfosId = nat
  type TimestampSymbolic = nat
  type CorrelationId = nat
  type PolicyVersion = nat
  type Generation = nat
  type PartitionId = nat
  type SequenceNumber = nat
  type DeterministicSeed = nat

  datatype Option<T> = None | Some(value: T)
  datatype Result<T> = ResultOk(value: T) | ResultErr(error_code: nat)

  predicate ValidId(id: MfosId) {
    id > 0
  }

  predicate ValidCorrelationId(id: CorrelationId) {
    id > 0
  }

  predicate ValidPolicyVersion(version: PolicyVersion) {
    version > 0
  }

  predicate ValidGeneration(generation: Generation) {
    generation > 0
  }

  predicate Ordered(before: SequenceNumber, after: SequenceNumber) {
    before < after
  }

  function NormalizePair(left: nat, right: nat): (nat, nat) {
    if left <= right then (left, right) else (right, left)
  }
}
