"""Simple RAG chain that retrieves context and returns a composed response.

This is a minimal orchestrator: embed query, retrieve top chunks, and return
them as context. Integrate with LangChain/MCP retrieval chains in production.
"""
from typing import Dict, Any, List
from app.rag.retriever import Retriever


class RAGChain:
    def __init__(self, retriever: Retriever = None):
        self.retriever = retriever or Retriever()

    async def answer(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        docs = await self.retriever.retrieve(query, top_k=top_k)
        context = "\n\n".join([d.get('text', '') for d in docs])
        # Placeholder: return retrieved context and the query; actual system
        # must call an LLM chain (via LangChain) with this context.
        return {"query": query, "context": context, "docs": docs}
