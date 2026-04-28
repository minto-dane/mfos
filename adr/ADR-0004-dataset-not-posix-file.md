# ADR-0004: Dataset Is Not a POSIX File

MFOS datasets are managed resources with catalog, security, audit, retention,
generation, and integrity bindings. POSIX file behavior may be provided only by
an optional subsystem that cannot bypass MFOS authorization and audit.

