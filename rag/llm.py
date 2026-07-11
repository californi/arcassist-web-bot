from typing import Generator, List, Optional
import os

import requests
from dotenv import load_dotenv


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
MODEL_ID = os.getenv("GROQ_MODEL_ID", "llama-3.1-8b-instant")


def build_prompt(context: str, question: str, history: Optional[List[str]] = None) -> str:
    formatted_history = ""
    if history:
        formatted_history = "\n".join(history)

    return f"""You are an assistant specialized in software architecture.
Your goal is to help architects, developers, and software engineers prepare evidence-grounded technical decisions.

Guidelines:
- Answer clearly, concisely, and technically in English.
- Always consider trade-offs, including benefits, drawbacks, and risks.
- Base the answer strictly on the provided context.
- If the answer is not supported by the context, say: "I did not find this information in the provided knowledge base."
- Do not present inferences as accepted architectural facts.
- Make assumptions and validation needs explicit.

CONVERSATION HISTORY:
{formatted_history}

CONTEXT:
{context}

USER QUESTION:
{question}"""


def _headers() -> dict:
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not configured. Copy .env.example to .env and set the key.")
    return {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }


def generate_response(context: str, question: str, history: Optional[List[str]] = None) -> str:
    prompt = build_prompt(context, question, history)
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
        return f"Model API error: {response.status_code}"
    except Exception as exc:
        return f"Connection error: {str(exc)}"


def generate_response_stream(
    context: str,
    question: str,
    history: Optional[List[str]] = None,
) -> Generator[str, None, None]:
    yield generate_response(context, question, history)
