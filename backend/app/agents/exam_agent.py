"""Exam Preparation Agent (LangGraph).

Generates mock tests, formula sheets and predicts readiness. Uses RAG and
Tavily MCP for resource gathering.
"""
from datetime import datetime
from typing import Dict, Any, List
from app.mcp import get_tavily_mcp
from app.agents.learning_intelligence import readiness_band, topic_title


class ExamAgent:
    def __init__(self, tavily_mcp=None):
        self.tavily = tavily_mcp or get_tavily_mcp()

    async def generate_mock_test(self, student_id: str, subject_id: str, mode: str = "30_days") -> Dict[str, Any]:
        resources = await self.tavily.search_academic_resources(f"{subject_id} exam practice", limit=5)
        sections = self._mock_sections(subject_id, mode)
        total_marks = sum(section["marks"] for section in sections)
        return {
            "mock_test_id": f"mt_{int(datetime.utcnow().timestamp())}",
            "student_id": student_id,
            "subject_id": subject_id,
            "mode": mode,
            "status": "generated",
            "created_at": datetime.utcnow().isoformat(),
            "duration_minutes": self._duration_for_mode(mode),
            "total_marks": total_marks,
            "sections": sections,
            "resources": resources,
            "instructions": [
                "Attempt under timed conditions",
                "Mark uncertain questions for review",
                "Analyze mistakes before taking another mock",
            ],
        }

    async def generate_formula_sheet(self, subject_id: str) -> Dict[str, Any]:
        title = topic_title(subject_id)
        return {
            "subject_id": subject_id,
            "title": f"{title} Rapid Revision Sheet",
            "formulas": [
                {"name": f"Core rule for {title}", "expression": "Write the required formula from class notes", "use_when": "The problem directly matches the definition"},
                {"name": "Unit or sign check", "expression": "Expected unit/sign from the question", "use_when": "Verifying the final answer"},
                {"name": "Error check", "expression": "Given -> Method -> Result -> Interpretation", "use_when": "Reviewing a solved answer"},
            ],
            "common_mistakes": [
                "Using the right formula with the wrong given value",
                "Skipping assumptions before applying a method",
                "Not checking whether the final answer matches the question",
            ],
        }

    async def predict_readiness(self, student_id: str, exam_id: str) -> Dict[str, Any]:
        resources = await self.tavily.search_concept(f"{exam_id} exam preparation checklist", {"type": "education"})
        score = self._estimate_readiness_score(resources)
        return {
            "student_id": student_id,
            "exam_id": exam_id,
            "readiness_score": score,
            "readiness_band": readiness_band(score),
            "checked_at": datetime.utcnow().isoformat(),
            "signals": {
                "resource_quality": len(resources),
                "practice_consistency": "unknown_until_progress_connected",
            },
            "recommendations": self._readiness_recommendations(score),
        }

    def _mock_sections(self, subject_id: str, mode: str) -> List[Dict[str, Any]]:
        title = topic_title(subject_id)
        if mode == "crash_course":
            return [
                {"name": "High-yield concepts", "question_count": 10, "marks": 20, "focus": title},
                {"name": "Common mistakes", "question_count": 5, "marks": 15, "focus": "error correction"},
                {"name": "Timed mixed practice", "question_count": 5, "marks": 25, "focus": "exam speed"},
            ]
        return [
            {"name": "Concept recall", "question_count": 10, "marks": 20, "focus": title},
            {"name": "Application", "question_count": 8, "marks": 40, "focus": "problem solving"},
            {"name": "Long answer", "question_count": 2, "marks": 40, "focus": "explanation and method"},
        ]

    def _duration_for_mode(self, mode: str) -> int:
        return {"7_days": 45, "crash_course": 60, "30_days": 90}.get(mode, 90)

    def _estimate_readiness_score(self, resources: List[Dict[str, Any]]) -> float:
        if not resources:
            return 35.0
        average_score = sum(float(item.get("score", 0.5)) for item in resources) / len(resources)
        return round(min(95, 45 + average_score * 45), 2)

    def _readiness_recommendations(self, score: float) -> List[str]:
        if score >= 80:
            return ["Take full-length mocks", "Revise only errors and high-yield notes", "Protect sleep before the exam"]
        if score >= 60:
            return ["Finish weak topics first", "Take alternate-day timed tests", "Make a one-page error log"]
        return ["Rebuild core concepts", "Use short daily quizzes", "Schedule mentor check-ins and revision reminders"]
