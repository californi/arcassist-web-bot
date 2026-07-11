# ArcAssist-Web Bot

Prototype artifact for the WBOTS 2026 short paper.

The bot is an early Flask-based demonstrator for evidence-grounded architectural
decision support. It receives a software-architecture concern, retrieves context
from a local knowledge base, builds a constrained prompt, and asks an external
LLM service to draft review material.

## What is included

- `app.py`: Flask web application.
- `templates/` and `static/`: chat interface.
- `rag/vectorstore.py`: PDF/text ingestion, chunking, embeddings, FAISS index.
- `rag/llm.py`: sanitized LLM adapter using environment variables.
- `data/architecture_seed.txt`: small seed knowledge base for smoke testing.
- `documentos/README.md`: manifest for architecture PDFs used in the original
  local prototype.

Derived files such as `rag/index.faiss` and `rag/docs.npy` are intentionally
excluded. They are rebuilt automatically when the app starts.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set `GROQ_API_KEY`.

Then run:

```bash
python app.py
```

Open `http://127.0.0.1:5000`.

## Double-blind note

For review, do not publish Git history, credentials, local paths, personal
accounts, or non-anonymized repository links. Replace private corpora with a
public sample corpus or a manifest.

