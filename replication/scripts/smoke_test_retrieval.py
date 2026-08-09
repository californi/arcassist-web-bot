"""Retrieval-only smoke test for the ArcAssist-Web Bot artifact.

Run from the repository root:
    python replication/scripts/smoke_test_retrieval.py

The script does not call the external LLM API.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from rag.vectorstore import create_vectorstore, retrieve  # noqa: E402


QUERY = (
    "A public animal profile should allow a visitor to register initial interest. "
    "What architectural concerns and validation needs should be considered?"
)


def main() -> int:
    index, documents = create_vectorstore()
    if not documents:
        raise RuntimeError("The artifact corpus produced no chunks.")

    results = retrieve(QUERY, index, documents, top_k=min(4, len(documents)))
    if not results:
        raise RuntimeError("Retrieval returned no chunks.")

    print(f"Corpus chunks: {len(documents)}")
    print(f"Retrieved chunks: {len(results)}")
    print("\nQuery:\n" + QUERY)

    for position, chunk in enumerate(results, start=1):
        print(f"\n--- Retrieved chunk {position} ---\n{chunk}")

    expected_terms = {"architect", "decision", "validation", "privacy", "web"}
    joined = " ".join(results).lower()
    if not any(term in joined for term in expected_terms):
        raise RuntimeError("Retrieved chunks do not contain expected architecture-related content.")

    print("\nRetrieval smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
