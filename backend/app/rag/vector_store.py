"""Vector store backed by MongoDB (basic implementation).

This module stores text chunks with their embeddings into a MongoDB collection
called `vectors`. For production, prefer MongoDB Atlas Vector Search or a
dedicated vector DB; ensure the MCP architecture is used for access control.
"""
from typing import List, Dict, Any
from app.database import db
import asyncio


class MongoVectorStore:
    def __init__(self, collection_name: str = 'vectors'):
        self.collection = db[collection_name]

    async def upsert_chunks(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        # chunks: list of {chunk_id, text, embedding, metadata}
        ops = []
        for c in chunks:
            filter_q = {"chunk_id": c['chunk_id']}
            update = {"$set": {**c}}
            ops.append(asyncio.create_task(self.collection.update_one(filter_q, update, upsert=True)))
        if ops:
            await asyncio.gather(*ops)
        return {"status": "ok", "count": len(chunks)}

    async def query_similar(self, embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        # Naive similarity using dot product on stored vectors — not efficient.
        cursor = self.collection.find({})
        results = []
        async for doc in cursor:
            vec = doc.get('embedding') or []
            score = sum(a * b for a, b in zip(vec, embedding)) if vec else 0
            doc['_score'] = score
            results.append(doc)
        results.sort(key=lambda d: d.get('_score', 0), reverse=True)
        return results[:top_k]
