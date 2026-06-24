"""YouTube Discovery MCP — uses Tavily to find educational videos when no YouTube API key is set."""
import os
from typing import Any, Dict, List

import httpx


class YouTubeMCP:
    def __init__(self):
        self.tavily_key = os.getenv("TAVILY_API_KEY")

    async def _search_youtube(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        if not self.tavily_key:
            return [{
                "title": f"{query} - Lecture",
                "channel": "EduChannel",
                "url": f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}",
                "duration": 600,
            }]

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": self.tavily_key,
                    "query": f"{query} site:youtube.com tutorial",
                    "search_depth": "basic",
                    "max_results": max_results,
                },
            )
            resp.raise_for_status()
            return [
                {
                    "title": item.get("title", ""),
                    "channel": "YouTube",
                    "url": item.get("url", ""),
                    "duration": 0,
                }
                for item in resp.json().get("results", [])
                if "youtube.com" in item.get("url", "")
            ]

    async def find_tutorials(self, topic: str, max_results: int = 5) -> List[Dict[str, Any]]:
        results = await self._search_youtube(f"{topic} tutorial explained", max_results)
        return results or [{
            "title": f"{topic} - Tutorial",
            "channel": "YouTube",
            "url": f"https://www.youtube.com/results?search_query={topic.replace(' ', '+')}+tutorial",
            "duration": 600,
        }]

    async def find_revision_videos(self, topic: str, max_results: int = 5) -> List[Dict[str, Any]]:
        results = await self._search_youtube(f"{topic} revision recap", max_results)
        return results or [{
            "title": f"{topic} - Revision",
            "channel": "YouTube",
            "url": f"https://www.youtube.com/results?search_query={topic.replace(' ', '+')}+revision",
            "duration": 300,
        }]
