from pathlib import Path

import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


DATA_PATH = Path("data/architecture_seed.txt")
PDF_FOLDER = Path("documents")
INDEX_PATH = Path("rag/index.faiss")
DOCS_PATH = Path("rag/docs.npy")

model = SentenceTransformer("all-MiniLM-L6-v2")


def split_into_chunks(text: str, chunk_size: int = 800, overlap: int = 150) -> list[str]:
    """Split text into overlapping chunks for retrieval."""
    chunks = []
    step = chunk_size - overlap
    for start in range(0, len(text), step):
        chunk = text[start:start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
    return chunks


def extract_pdf_text(path: Path) -> str:
    """Extract text from a PDF file."""
    reader = PdfReader(str(path))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def load_txt_documents() -> list[str]:
    """Load the seed text corpus and split it into chunks."""
    if not DATA_PATH.exists():
        return []
    text = DATA_PATH.read_text(encoding="utf-8")
    return split_into_chunks(text)


def load_pdf_documents() -> list[str]:
    """Load PDF documents from the public artifact folder."""
    if not PDF_FOLDER.exists():
        return []

    documents = []
    for pdf_path in sorted(PDF_FOLDER.glob("*.pdf")):
        print(f"Loading PDF: {pdf_path.name}")
        text = extract_pdf_text(pdf_path)
        documents.extend(split_into_chunks(text))
    return documents


def create_vectorstore():
    """Create or load a FAISS vector index."""
    if INDEX_PATH.exists() and DOCS_PATH.exists():
        print("Loading saved FAISS index...")
        index = faiss.read_index(str(INDEX_PATH))
        documents = np.load(DOCS_PATH, allow_pickle=True).tolist()
        return index, documents

    print("Creating a new vector index...")
    documents = []
    documents.extend(load_txt_documents())
    documents.extend(load_pdf_documents())

    if not documents:
        raise ValueError("No documents found for indexing.")

    print("Loaded chunks:", len(documents))
    embeddings = model.encode(
        documents,
        convert_to_numpy=True,
        show_progress_bar=True,
    )
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))
    np.save(DOCS_PATH, documents)
    print("FAISS index created and saved.")
    return index, documents


def retrieve(query: str, index, documents: list[str], top_k: int = 4) -> list[str]:
    """Return the most relevant chunks for a query."""
    query_embedding = model.encode([query], convert_to_numpy=True)
    _, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(documents):
            results.append(documents[idx])
    return results
