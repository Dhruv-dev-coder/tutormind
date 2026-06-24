"""Simple RAG chain that retrieves context and synthesizes an answer via Gemini."""
from typing import Dict, Any
from app.rag.retriever import Retriever
from app.services import llm_service


class RAGChain:
    def __init__(self, retriever: Retriever = None):
        self.retriever = retriever or Retriever()

    async def answer(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        docs = await self.retriever.retrieve(query, top_k=top_k)
        context = "\n\n".join([d.get('text', '') for d in docs if d.get('text')])

        answer = None
        if llm_service.is_configured():
            try:
                prompt = f"""Answer the student's question using the study context below.
If context is empty, answer from general knowledge as a tutor.

Context:
{context or "No indexed documents found."}

Question: {query}

Provide a clear, structured answer with key points."""

                answer = await llm_service.generate_text(
                    prompt,
                    system_instruction="You are TutorMind, a helpful AI tutor. Be concise and educational.",
                )
            except Exception:
                answer = None

        return {
            "query": query,
            "answer": answer,
            "context": context,
            "docs": docs,
            "source": "gemini" if answer else "retrieval_only",
        }
