# Copyright Policy

Do not commit external PDFs, HTML mirrors, EPUBs, screenshots, or copied
manuals. Use Source Cards and short paraphrased mappings instead.

Local downloaded references belong only in ignored cache directories such as
`sources/_cache/` or `reference-cache/`.

The repository stores source-grounding metadata, not source material. Public
sources, including IBM documentation, may be consulted during research, but the
committed record must remain limited to:

- bibliographic identity
- public URL
- retrieval date
- version, publication, or section scope
- checksum or cache-manifest metadata for local review copies
- short paraphrased relevance notes
- MFOS overlap, divergence, and prohibited-inference notes
- legal-control flags

The committed record must not include:

- downloaded PDFs or generated text extracted from PDFs
- copied HTML documentation pages
- screenshots of external manuals
- copied tables, diagrams, examples, command syntax, macro signatures, message
  catalogs, record layouts, or API descriptions
- detailed summaries that substitute for the external source
- cache archives or bundled public documentation

`sources/_cache/` is ignored local scratch space. Only its policy files are
committed. A cache manifest may be kept locally while work is in progress, but
the durable committed artifact is the public-safe Source Card, Concept Card, or
retrieval-log entry.

When in doubt, record less source material and more review metadata. A reviewer
must be able to find the public source and understand why MFOS cited it, but
must still need the external source for the original documentation.
