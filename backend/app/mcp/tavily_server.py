"""Tavily Search MCP — educational resource discovery."""
import os
from typing import Any, Dict, List

import httpx


class TavilyMCP:
    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")
        self.base_url = "https://api.tavily.com"

    async def _search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        if not self.api_key:
            return [{"title": f"Resource for {query}", "url": "https://example.edu/resource", "score": 0.9}]

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{self.base_url}/search",
                json={
                    "api_key": self.api_key,
                    "query": query,
                    "search_depth": "basic",
                    "max_results": max_results,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            return [
                {
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "score": item.get("score", 0),
                    "content": item.get("content", ""),
                }
                for item in data.get("results", [])
            ]

    async def search_concept(self, query: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        return await self._search(query, max_results=5)

    async def search_academic_resources(self, topic: str, limit: int = 10) -> List[Dict[str, Any]]:
        return await self._search(f"{topic} educational tutorial explained", max_results=limit)
