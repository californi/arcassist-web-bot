# ArcAssist-Web Bot

**Camera-ready replication package for WBOTS 2026**

ArcAssist-Web Bot is an early Web-system prototype for **evidence-grounded architectural decision preparation**. A user states an architectural evolution concern; the implemented Flask/RAG path retrieves PDF/text architecture knowledge, builds a constrained prompt, and asks an external LLM service to draft material for human review.

The artifact accompanies the paper:

> **ArcAssist-Web Bot: A Prototype Instantiation for Evidence-Grounded Architectural Decision Support**  
> Vanusa Rodrigues de Oliveira, Bento Rafael Siqueira, and Samira Santos da Silva  
> Federal University of Lavras (UFLA), Brazil  
> WBOTS 2026 — Workshop on Bots in Software Engineering, São Paulo, Brazil, September 11, 2026.

A demonstration interface used during development is available at:  
<https://arcassist-decision-buddy.lovable.app/>

## Artifact scope

This package reflects the scope claimed in the camera-ready paper. It supports inspection of the **implemented pre-review RAG path**:

1. submit an evolution concern;
2. retrieve architecture evidence from a local corpus;
3. build a constrained prompt;
4. request an LLM-generated draft for review.

The current prototype **does not implement** the planned Validation and QA or Knowledge Management responsibilities. It also does not autonomously accept architectural decisions. The Decision Package and Architect Review gate described in the paper delimit the planned workflow beyond the implemented RAG slice.

## Relationship to the broader ArcAssist product

This public repository is the article-specific WBOTS 2026 research artifact, identified as version `1.0.0-camera-ready` at commit `354d4dc90374f10a77ba899994a2308f3d518fab`. Its scope is the early, limited prototype described above. It is not the full or base ArcAssist product and does not contain that separate product's broader feature set. The full/base software is maintained separately as a distinct intellectual-property asset; this repository does not include or grant rights to that separate software.

Implementation details and model-provider behavior described in this README apply only to this article-specific artifact. They do not describe other ArcAssist versions. This clarification does not grant a license to this repository or determine authorship, ownership, or registration status; see the licensing note below.

## Package contents

- `app.py` — Flask Web application and `/ask` route.
- `templates/` and `static/` — chat interface.
- `rag/vectorstore.py` — PDF/text ingestion, chunking, embeddings, FAISS indexing, and retrieval.
- `rag/llm.py` — constrained prompt construction and external LLM adapter.
- `data/architecture_seed.txt` — sanitized seed knowledge base for smoke testing.
- `documents/README.md` — guidance for adding redistributable architecture documents.
- `replication/scripts/check_artifact.py` — release hygiene check for secrets, local paths, and accidental generated files.
- `replication/scripts/smoke_test_retrieval.py` — retrieval-only smoke test that does not call the external LLM API.
- `replication/sample_queries.md` — example concerns for manual inspection.
- `replication/checklists/camera_ready.md` — camera-ready release checklist.
- `ARTIFACT_INVENTORY.md` — artifact inventory and file hashes.
- `CITATION.cff` — citation metadata for the software artifact.

Derived files `rag/index.faiss` and `rag/docs.npy` are intentionally excluded from the release package. They are rebuilt from the available corpus when needed.

## Requirements

- Python 3.10 or newer is recommended.
- Internet access is required on the first run to obtain the `all-MiniLM-L6-v2` sentence-transformer model unless it is already cached.
- Full LLM-backed interaction requires a Groq-compatible API endpoint and an API key.

Python dependencies are listed in `requirements.txt`.

## Setup

From the package root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

For the full prototype, edit `.env` and set `GROQ_API_KEY`. Optional endpoint/model overrides are documented in `.env.example`.

## Run the prototype

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

A representative concern is:

> A public animal profile should allow a visitor to register initial interest without implementing the full adoption workflow. What architectural alternatives and validation needs should be considered?

Expected behavior: the prototype retrieves relevant chunks from the local architecture corpus, constrains the LLM request to that context, and returns review material that discusses alternatives, trade-offs, assumptions, risks, and validation needs. The generated text is **not** an accepted architectural decision.

## Retrieval-only smoke test

To inspect the implemented retrieval path without sending data to an external LLM service:

```bash
python replication/scripts/smoke_test_retrieval.py
```

The script builds/loads the local FAISS index, runs a representative query, and prints the retrieved chunks. A successful run ends with:

```text
Retrieval smoke test passed.
```

Because the embedding model may need to be downloaded on first use, this test can still require Internet access unless the model is cached locally.

## Release hygiene check

Before publishing or archiving the package:

```bash
python replication/scripts/check_artifact.py
```

The check looks for common secret-like tokens, `.env`, local absolute paths, generated FAISS/NumPy index files, and common OS metadata. It is a lightweight packaging check, not a security audit.

## Corpus and evidence

The release contains a small sanitized seed corpus in `data/architecture_seed.txt`. Redistributable PDF architecture documents can be placed in `documents/`; they are ingested automatically when the index is rebuilt.

The camera-ready paper explicitly notes a current limitation: retrieved chunks do not yet carry stable document/page/section/timestamp/corpus-version identifiers. Therefore, this artifact supports inspection of the connected RAG path and responsibility separation, **not decision-grade provenance or effectiveness claims**.

See `documents/README.md` for the evidence-manifest fields recommended for future corpora.

## External-service and privacy note

When the full prototype is used, the retrieved context and the submitted concern are sent to the configured external LLM endpoint. Do not use private, confidential, personal, or non-redistributable content unless the endpoint and applicable data-handling rules are appropriate for that content.

No API key, `.env` file, private corpus, Git history, or non-redistributable document is included in this package.

## Funding acknowledgment

The authors gratefully acknowledge the financial support provided by the **Fundação de Amparo à Pesquisa do Estado de Minas Gerais (FAPEMIG), Brazil**, through projects **CIN II APQ-06513-25** and **CEX-BIS-00192-25**.

## Citation

Citation metadata for the artifact is provided in `CITATION.cff`. When citing the research contribution, please cite the WBOTS 2026 paper listed at the top of this README. Add the final proceedings DOI to your bibliographic record when it becomes available.

## License and third-party components

No source-code license was present in the reviewed package, so this camera-ready bundle does **not** assign a new license on behalf of the authors. Before long-term public release, the authors may add an explicit license if desired.

Third-party Python packages remain subject to their respective licenses. Any additional documents added to `documents/` should be redistributable under their own terms.
