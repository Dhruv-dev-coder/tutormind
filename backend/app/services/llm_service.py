"""Centralized Gemini LLM service for TutorMind agents."""
import asyncio
import json
import logging
import os
import re
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

# Prefer .env over stale shell/system GOOGLE_API_KEY values
load_dotenv(override=True)

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

logger = logging.getLogger(__name__)

_RAW_MODELS: List[str] = [
    os.getenv("GEMINI_MODEL", ""),
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
]
MODEL_FALLBACKS: List[str] = list(dict.fromkeys(m for m in _RAW_MODELS if m))

_client: Optional[Any] = None
_last_error: Optional[str] = None
MAX_RETRIES = 3


def is_configured() -> bool:
    return bool(os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"))


def get_last_error() -> Optional[str]:
    return _last_error


def _get_client():
    global _client
    if _client is None and genai:
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if api_key:
            _client = genai.Client(api_key=api_key)
    return _client


def _extract_json(text: str) -> Dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return json.loads(cleaned)


def _should_try_next_model(error: Exception) -> bool:
    message = str(error).lower()
    return any(
        token in message
        for token in ("429", "quota", "resource_exhausted", "404", "not found", "503", "unavailable")
    )


def _should_retry(error: Exception) -> bool:
    message = str(error).lower()
    return any(token in message for token in ("429", "quota", "503", "unavailable", "resource_exhausted"))


async def generate_text(prompt: str, system_instruction: Optional[str] = None) -> str:
    global _last_error
    client = _get_client()
    if not client:
        raise RuntimeError("GOOGLE_API_KEY is not configured")

    config = None
    if system_instruction and types:
        config = types.GenerateContentConfig(system_instruction=system_instruction)

    errors: List[str] = []
    for model in MODEL_FALLBACKS:
        for attempt in range(MAX_RETRIES):
            try:
                response = await client.aio.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=config,
                )
                text = (response.text or "").strip()
                if not text:
                    raise RuntimeError(f"Empty response from {model}")
                _last_error = None
                logger.info("LLM success via model %s (attempt %d)", model, attempt + 1)
                return text
            except Exception as exc:
                errors.append(f"{model}[{attempt + 1}]: {exc}")
                logger.warning("LLM model %s attempt %d failed: %s", model, attempt + 1, exc)
                if _should_retry(exc) and attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                if not _should_try_next_model(exc):
                    break
                break

    _last_error = "; ".join(errors[-3:])
    raise RuntimeError(_last_error or "All Gemini models failed")


async def generate_json(prompt: str, system_instruction: Optional[str] = None) -> Dict[str, Any]:
    system = system_instruction or (
        "You are TutorMind, an expert AI tutor. Respond with valid JSON only — no markdown fences."
    )
    text = await generate_text(prompt, system)
    try:
        return _extract_json(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise
