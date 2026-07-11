from flask import Flask, Response, render_template, request

from rag.llm import generate_response_stream
from rag.vectorstore import create_vectorstore, retrieve


app = Flask(__name__)

# The vector store is loaded once at startup. If no derived index exists, it is
# rebuilt from the documented seed corpus and any PDFs placed in documents/.
index, documents = create_vectorstore()
print("Vector store loaded with", len(documents), "chunks")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/ask", methods=["POST"])
def ask():
    payload = request.get_json()
    question = payload["question"]

    try:
        results = retrieve(question, index, documents, top_k=4)
        relevant_context = "\n\n---\n\n".join(results)
    except Exception as exc:
        print("Vector store error:", exc)
        relevant_context = "\n".join(documents[:4])

    def generate():
        yield from generate_response_stream(relevant_context, question)

    return Response(generate(), mimetype="text/plain")


if __name__ == "__main__":
    app.run(debug=True)
