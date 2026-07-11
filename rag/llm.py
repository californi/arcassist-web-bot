from typing import Generator, List
import os

import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
MODEL_ID = os.getenv("GROQ_MODEL_ID", "llama-3.1-8b-instant")


def montar_prompt(contexto: str, pergunta: str, historico: List[str] = None) -> str:
    historico_formatado = ""
    if historico:
        historico_formatado = "\n".join(historico)

    return f"""Voce e um assistente especializado em Arquitetura de Software.
Seu objetivo e apoiar arquitetos, desenvolvedores e engenheiros de software a tomarem decisoes tecnicas embasadas.

Diretrizes:
- Responda de forma clara, objetiva e tecnica em portugues.
- Sempre considere trade-offs, incluindo vantagens, desvantagens e riscos.
- Baseie sua resposta estritamente no contexto fornecido.
- Se a resposta nao estiver no contexto, diga: "Nao encontrei essa informacao na base de conhecimento fornecida."
- Nao apresente inferencias como fatos arquiteturais aceitos.

HISTORICO DA CONVERSA:
{historico_formatado}

CONTEXTO (BASE DE CONHECIMENTO):
{contexto}

PERGUNTA DO USUARIO:
{pergunta}"""


def _headers() -> dict:
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not configured. Copy .env.example to .env and set the key.")
    return {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }


def gerar_resposta(contexto: str, pergunta: str, historico: List[str] = None) -> str:
    prompt = montar_prompt(contexto, pergunta, historico)
    try:
        response = requests.post(
            API_URL,
            headers=_headers(),
            json={
                "model": MODEL_ID,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
            },
            timeout=60,
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return f"Erro na API do modelo: {response.status_code}"
    except Exception as exc:
        return f"Erro de conexao: {str(exc)}"


def gerar_resposta_stream(contexto: str, pergunta: str, historico: List[str] = None) -> Generator[str, None, None]:
    yield gerar_resposta(contexto, pergunta, historico)
