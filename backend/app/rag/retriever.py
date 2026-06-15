"""Retriever utilities that use the vector store and embeddings.
"""
from typing import List, Dict, Any
from app.rag.embedding_service import embed_texts
from app.rag.vector_store import MongoVectorStore


class Retriever:
    def __init__(self, store: MongoVectorStore = None):
        self.store = store or MongoVectorStore()

    async def add_document(self, doc_id: str, text: str, metadata: Dict[str, Any] = None):
        chunks = []
        from app.rag.text_chunker import chunk_text
        text_chunks = chunk_text(text)
        texts = [c['text'] for c in text_chunks]
        embeddings = embed_texts(texts)
        for i, c in enumerate(text_chunks):
            chunks.append({
                "chunk_id": f"{doc_id}_{c['chunk_id']}",
                "text": c['text'],
                "embedding": embeddings[i],
                "metadata": metadata or {}
            })
        return await self.store.upsert_chunks(chunks)

    async def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        q_emb = embed_texts([query])[0]
        return await self.store.query_similar(q_emb, top_k=top_k)
