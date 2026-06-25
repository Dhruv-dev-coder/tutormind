"""Tavily Search MCP server.

Exposes educational search interfaces using Tavily API.
"""
from typing import List, Dict, Any
import os
from tavily import TavilyClient


class TavilyMCP:
    def __init__(self):
        self.api_key = os.getenv('TAVILY_API_KEY')
        self.client = TavilyClient(api_key=self.api_key) if self.api_key else None
    
    def is_available(self) -> bool:
        """Check if Tavily API is available."""
        return bool(self.api_key)
    
    async def search_concept(self, query: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Return a list of educational resources."""
        if not self.is_available():
            # Fallback to stub if API not available
            return [
                {
                    "title": f"Understanding {query}",
                    "url": f"https://example.edu/{query.lower().replace(' ', '-')}",
                    "score": 0.9,
                    "snippet": f"Comprehensive guide to {query} concepts and applications."
                }
            ]
        
        try:
            search_result = self.client.search(
                query=f"{query} educational tutorial explanation",
                search_depth="basic",
                max_results=5,
                include_domains=["edu", "khanacademy.org", "coursera.org", "edx.org"]
            )
            
            results = []
            for result in search_result.get('results', []):
                results.append({
                    "title": result.get('title', ''),
                    "url": result.get('url', ''),
                    "score": result.get('score', 0.8),
                    "snippet": result.get('content', '')
                })
            return results
        except Exception as e:
            print(f"Tavily search failed: {e}")
            return []

    async def search_academic_resources(self, topic: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for academic resources on a topic."""
        if not self.is_available():
            # Fallback to stub
            return [
                {
                    "title": f"Academic Paper: {topic}",
                    "url": f"https://scholar.example.edu/{topic.lower().replace(' ', '-')}",
                    "score": 0.9,
                    "snippet": f"Research paper on {topic} concepts and methodologies."
                }
            ]
        
        try:
            search_result = self.client.search(
                query=f"{topic} academic research paper study",
                search_depth="advanced",
                max_results=min(limit, 10),
                include_domains=["scholar.google.com", "arxiv.org", "researchgate.net", "jstor.org"]
            )
            
            results = []
            for result in search_result.get('results', []):
                results.append({
                    "title": result.get('title', ''),
                    "url": result.get('url', ''),
                    "score": result.get('score', 0.8),
                    "snippet": result.get('content', '')
                })
            return results
        except Exception as e:
            print(f"Tavily academic search failed: {e}")
            return []
