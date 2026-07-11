# ==============================
# IMPORTAÇÕES
# ==============================

# Flask: framework web para criar a aplicação
# render_template: renderiza páginas HTML
# request: captura dados enviados pelo cliente (frontend)
# Response: permite retornar respostas customizadas (como streaming)
from flask import Flask, render_template, request, Response

# Função customizada que cria o vectorstore (RAG)
from rag.vectorstore import create_vectorstore

# requests: usado para fazer chamadas HTTP (para o Ollama)
import requests

# json: manipulação de dados JSON
import json

#CORREÇÃO 2: usa o retrieve do vectorsotre
from rag.vectorstore import retrieve

#CORREÇÃO 3: usar o gera_resposta do llm.py
from rag.llm import gerar_resposta_stream

# ==============================
# INICIALIZAÇÃO DO FLASK
# ==============================

# Cria a aplicação Flask
app = Flask(__name__)


# ==============================
# CARREGAMENTO DO VECTORSTORE (RAG)
# ==============================

# Aqui acontece:
# - Leitura dos documentos (PDFs, textos, etc.)
# - Geração de embeddings
# - Criação de um índice vetorial (ex: FAISS)

# index → estrutura para busca semântica
# docs → lista original dos documentos
index, docs = create_vectorstore()

# Log para confirmar carregamento
print("Vectorstore carregado com", len(docs), "documentos")


# ==============================
# ROTAS DE PÁGINAS (FRONTEND)
# ==============================

# Página inicial
@app.route("/")
def home():
    # Renderiza o arquivo templates/index.html
    return render_template("index.html")


# Página institucional
@app.route("/institucional")
def institucional():
    # Renderiza o arquivo templates/sobre.html
    return render_template("sobre.html")


# ==============================
# ROTA DA IA (RAG + OLLAMA)
# ==============================

# Essa rota recebe perguntas do frontend e retorna respostas da IA
@app.route("/ask", methods=["POST"])
def ask():
    # ==============================
    # RECEBE A PERGUNTA DO USUÁRIO
    # ==============================
    # Captura o JSON enviado pelo frontend
    data = request.get_json()
    # Extrai a pergunta
    question = data["question"]
    # ==============================
    # BUSCA SEMÂNTICA (RAG)
    # ==============================
    try:
        # Busca os 4 documentos mais relevantes no vectorstore
        #CORREÇÃO 1: resultados = index.similarity_search(question, k=4)
        resultados = retrieve(question, index, docs, top_k=4)
        # Junta os conteúdos dos documentos em uma única string
        contexto_relevante = "\n\n---\n\n".join(resultados)
    except Exception as e:
        # Caso o método similarity_search não exista ou falhe
        print("Erro no vectorstore:", e)
        # Fallback: usa os primeiros documentos
        contexto_relevante = "\n".join(docs[:4])
    # ==============================
    # CONSTRUÇÃO DO PROMPT
    # ==============================

    # Aqui você controla o comportamento do modelo (prompt engineering)
    # e injeta o contexto recuperado (RAG)

    # ==============================
    # FUNÇÃO GERADORA (STREAMING)
    # ==============================

    # Essa função envia a resposta aos poucos (token por token)
    #CORREÇÃO 4: agora estou usando o llm.py
    def gerar():
        yield from gerar_resposta_stream(contexto_relevante, question)
    return Response(gerar(), mimetype="text/plain")

# ==============================
# EXECUÇÃO DA APLICAÇÃO
# ==============================

# Só executa se o arquivo for rodado diretamente
if __name__ == "__main__":
    # Inicia o servidor Flask
    # debug=True:
    # - recarrega automaticamente ao salvar
    # - mostra erros detalhados
    app.run(debug=True)