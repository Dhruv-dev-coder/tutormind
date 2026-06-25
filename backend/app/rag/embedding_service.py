"""Embedding service using Google Gemini API.

Provides embeddings via Google's Generative AI Embedding API.
Requires GOOGLE_API_KEY environment variable.
"""
from typing import List
import os
import google.genai as genai

# Initialize Gemini API
API_KEY = os.environ.get("GOOGLE_API_KEY")
if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    client = None


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Generate embeddings using Google Gemini Embedding API.
    
    Args:
        texts: List of text strings to embed
        
    Returns:
        List of embedding vectors (each vector is a list of floats)
    """
    if not API_KEY:
        raise RuntimeError("GOOGLE_API_KEY not configured. Set it in your .env file.")
    
    embeddings = []
    for text in texts:
        try:
            # Use Gemini's embedding model via google-genai
            response = client.models.embed_content(
                model="models/embedding-001",
                content=text
            )
            embeddings.append(response.embedding)
        except Exception as e:
            raise RuntimeError(f"Failed to generate embedding: {str(e)}")
    
    return embeddings
