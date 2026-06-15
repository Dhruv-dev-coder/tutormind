"""Analytics service wrapper around Analytics MCP.

Provides concise methods agents and APIs call to generate reports and detect weak topics.
"""
from typing import Dict, Any
from app.mcp import get_analytics_mcp


class AnalyticsService:
    def __init__(self, analytics_mcp=None):
        self.analytics_mcp = analytics_mcp or get_analytics_mcp()

    async def generate_weekly_report(self, student_id: str) -> Dict[str, Any]:
        return await self.analytics_mcp.generate_weekly_report(student_id)

    async def analyze_performance(self, student_id: str, window_days: int = 30) -> Dict[str, Any]:
        return await self.analytics_mcp.analyze_performance(student_id, window_days)

    async def detect_weak_topics(self, student_id: str) -> Dict[str, Any]:
        return await self.analytics_mcp.detect_weak_topics(student_id)
