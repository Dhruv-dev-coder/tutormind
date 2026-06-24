"""Embedding service using Google Gemini API."""
from typing import List
import os

from dotenv import load_dotenv

load_dotenv(override=True)

_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            return None
        import google.genai as genai
        _client = genai.Client(api_key=api_key)
    return _client


def embed_texts(texts: List[str]) -> List[List[float]]:
    client = _get_client()
    if not client:
        raise RuntimeError("GOOGLE_API_KEY not configured. Set it in your .env file.")

    embeddings = []
    for text in texts:
        response = client.models.embed_content(
            model="models/embedding-001",
            contents=text,
        )
        embedding = getattr(response, "embedding", None)
        if embedding is None and getattr(response, "embeddings", None):
            embedding = response.embeddings[0].values
        embeddings.append(embedding)
    return embeddings
