"""Text chunking utilities.

Simple, synchronous chunker used to split long documents into retrievable
chunks. Replace with a smarter tokenizer-aware chunker when integrating.
"""
from typing import List, Dict


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, str]]:
    chunks = []
    start = 0
    length = len(text)
    idx = 0
    while start < length:
        end = min(start + chunk_size, length)
        chunk_text = text[start:end]
        chunks.append({"chunk_id": f"chunk_{idx}", "text": chunk_text})
        idx += 1
        start = end - overlap if end < length else end
    return chunks
