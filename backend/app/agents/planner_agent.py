"""Planner Agent (LangGraph) - skeleton

Responsible for analyzing syllabus and datesheets and producing study plans.
This is a LangGraph agent skeleton that must call MCP tools for document parsing
and calendar scheduling via the MCP layer.
"""
from typing import Dict, Any, List
from app.mcp import get_document_mcp, get_calendar_mcp


class PlannerAgent:
    def __init__(self, document_mcp=None, calendar_mcp=None):
        self.document_mcp = document_mcp or get_document_mcp()
        self.calendar_mcp = calendar_mcp or get_calendar_mcp()

    async def analyze_syllabus(self, document_bytes: bytes, content_type: str) -> Dict[str, Any]:
        text = await self.document_mcp.extract_text(document_bytes, content_type)
        parsed = await self.document_mcp.parse_syllabus(text)
        return parsed

    async def analyze_datesheet(self, text: str) -> Dict[str, Any]:
        return await self.document_mcp.parse_datesheet(text)

    async def estimate_study_hours(self, chapters: List[Dict[str, Any]]) -> float:
        total = 0.0
        for ch in chapters:
            total += ch.get('estimated_hours', 1)
        return total

    async def generate_roadmap(self, student_id: str, syllabus: Dict[str, Any], datesheet: Dict[str, Any]) -> Dict[str, Any]:
        # Produce semester/monthly/weekly/daily plans (stub)
        roadmap = {"semester": [], "monthly": [], "weekly": [], "daily": []}
        return roadmap
