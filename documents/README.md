# Evidence Documents

Place redistributable architecture documents in this directory when preparing a
public artifact. The prototype will ingest `*.pdf` files from this folder and
combine them with the seed corpus in `data/architecture_seed.txt`.

For a reviewable artifact, each source should be registered in an evidence
manifest with at least:

- source identifier;
- title;
- origin or URL;
- version or access date;
- license;
- redistribution status;
- notes about whether the source represents implemented facts, planned concepts,
  or open questions.

Derived files such as `rag/index.faiss` and `rag/docs.npy` should not be
committed. Delete them before rebuilding the corpus or publishing the package.
