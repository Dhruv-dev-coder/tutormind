from fastapi import APIRouter, Body
from typing import Dict, Any
from app.rag.rag_chain import RAGChain

router = APIRouter()
rag = RAGChain()


@router.post('/query')
async def query_rag(payload: Dict[str, Any] = Body(...)):
    """Query the RAG chain with a question and return grounded context."""
    q = payload.get('query')
    top_k = int(payload.get('top_k', 5))
    result = await rag.answer(q, top_k=top_k)
    return {"status": "ok", "result": result}
