# x86-64 Target Profile Report

Status: current
Date: 2026-04-30

## Profiles Defined

- `MFOS-X64-BASELINE`
- `MFOS-X64-SERVER-MODERN`
- `MFOS-X64-V4-PERFORMANCE`
- `MFOS-X64-MAX-FEATURE`
- `MFOS-X64-CVM-INTEL-TDX`
- `MFOS-X64-CVM-AMD-SEV-SNP`
- `MFOS-X64-TEE-INTEL-SGX`
- `MFOS-HARDENING-CET-CFI`

## Key Decisions

- x86-64-v4 is optional performance profile only, not baseline.
- Baseline does not require TDX, SEV-SNP, SGX, or maximum-performance features.
- v4 optimized artifacts must be separate from baseline artifacts and selected
  only after boot-time or runtime capability evidence.
- TDX and SEV-SNP are Confidential VM profiles.
- SGX is optional enclave/TEE profile, not Confidential VM.
- CET/CFI are evidence requirements, not language replacements or proof claims.

## Non-Claims

- No CVM, SGX, TEE, hardening, or v4 runtime implementation is complete.
- No profile implies Hyper-V or KVM compatibility.
- No optional CPU feature is globally assumed.
