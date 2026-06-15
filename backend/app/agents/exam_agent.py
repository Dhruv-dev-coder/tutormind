"""Exam Preparation Agent (LangGraph) - skeleton

Generates mock tests, formula sheets and predicts readiness. Uses RAG and
Tavily MCP for resource gathering.
"""
from typing import Dict, Any, List
from app.mcp import get_tavily_mcp


class ExamAgent:
    def __init__(self, tavily_mcp=None):
        self.tavily = tavily_mcp or get_tavily_mcp()

    async def generate_mock_test(self, student_id: str, subject_id: str, mode: str = "30_days") -> Dict[str, Any]:
        return {"mock_test_id": "mt1", "status": "generated"}

    async def generate_formula_sheet(self, subject_id: str) -> Dict[str, Any]:
        return {"subject_id": subject_id, "formulas": []}

    async def predict_readiness(self, student_id: str, exam_id: str) -> Dict[str, Any]:
        return {"readiness_score": 0.0}
