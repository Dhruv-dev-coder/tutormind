"""Document loader utilities for RAG pipeline.

Provide simple helpers to load text from uploaded files. Production should
delegate heavy parsing to the Document MCP server.
"""
from typing import Tuple


def load_text_from_bytes(content_bytes: bytes, content_type: str) -> Tuple[str, dict]:
    """Return extracted text and minimal metadata.

    This is a fallback extractor. Prefer calling the Document MCP for robust
    parsing (OCR, DOCX, structured extraction).
    """
    try:
        text = content_bytes.decode('utf-8')
    except Exception:
        text = ''
    metadata = {"content_type": content_type}
    return text, metadata
