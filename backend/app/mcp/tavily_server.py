"""Tavily Search MCP server stub.

Exposes educational search interfaces. Real implementation must call an MCP
proxy which enforces educational-only filtering and rate limits.
"""
from typing import List, Dict, Any


class TavilyMCP:
    async def search_concept(self, query: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Return a list of educational resources (stubbed)."""
        return [{"title": "Example Resource", "url": "https://example.edu/resource", "score": 0.9}]

    async def search_academic_resources(self, topic: str, limit: int = 10) -> List[Dict[str, Any]]:
        return [{"title": f"Intro to {topic}", "url": "https://example.edu/tutorial", "score": 0.85}]
