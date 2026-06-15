"""Calendar MCP server stub.

Schedules revisions, exams and deadlines via MCP. Real implementation should
integrate with calendar providers via the MCP layer.
"""
from typing import Dict, Any


class CalendarMCP:
    async def schedule_revision(self, student_id: str, topic: str, when: str) -> Dict[str, Any]:
        return {"status": "scheduled", "student_id": student_id, "topic": topic, "when": when}

    async def schedule_exam_reminder(self, student_id: str, exam_info: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "scheduled", "exam_info": exam_info}

    async def schedule_goal(self, student_id: str, goal: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "scheduled", "goal": goal}
