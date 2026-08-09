# Evidence Documents

This directory is reserved for **redistributable architecture evidence** used by the prototype. At startup, ArcAssist-Web Bot ingests `*.pdf` files from this directory and combines them with the sanitized seed corpus in `data/architecture_seed.txt`.

No private or non-redistributable project documents are included in the camera-ready package.

## Recommended evidence manifest

For future public corpora, register each source in an evidence manifest with at least:

- stable source identifier;
- title;
- origin or URL;
- version and/or access date;
- license;
- redistribution status;
- document type (e.g., ADR, diagram description, backlog item, API contract, deployment constraint, privacy policy, quality scenario);
- whether the source represents implemented facts, planned concepts, or open questions.

The current implementation retrieves text chunks but does **not** yet propagate stable document/page/section/timestamp/corpus-version metadata into the generated answer. This is a limitation described in the accompanying WBOTS 2026 paper.

## Rebuilding the index

The generated files below should not be distributed:

- `rag/index.faiss`
- `rag/docs.npy`

Delete them after changing the corpus; the next startup or smoke test will rebuild the index from the available seed/PDF content.
