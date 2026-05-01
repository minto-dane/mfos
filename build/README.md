# build/

Metadata-only build policy scaffold. Generated build profiles, toolchains,
images, reproducibility outputs, caches, temporary files, and lab artifacts are
ignored by default and must not be committed under this directory.

This directory is metadata-only until a later reviewed implementation gate; it
must not contain production build scripts, hosted daemon launchers,
semantic-runner commands, or Phase 1.4 implementation artifacts.
