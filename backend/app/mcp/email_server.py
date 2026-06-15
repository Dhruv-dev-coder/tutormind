"""Email MCP server stub.

All external email sending must go through an MCP tool. These stubs provide the
interface the LangGraph agents will call. Implementations should forward calls
to a real MCP server or queue worker that performs the external integration.
"""
from typing import Dict, Any


class EmailMCP:
    """Stub for Email MCP server.

    Methods are async-compatible and return a simple status dict. Replace the
    internals with MCP transport logic (HTTP/gRPC) in production.
    """

    async def send_reminder_email(self, student_id: str, subject: str, body: str, metadata: Dict[str, Any] = None):
        return {"status": "queued", "student_id": student_id, "subject": subject}

    async def send_exam_alert(self, student_id: str, exam_info: Dict[str, Any]):
        return {"status": "queued", "exam_info": exam_info}

    async def send_weekly_report(self, student_id: str, report: Dict[str, Any]):
        return {"status": "queued", "student_id": student_id}

    async def send_revision_notification(self, student_id: str, revision_info: Dict[str, Any]):
        return {"status": "queued", "student_id": student_id}

    async def send_achievement_email(self, student_id: str, achievement: Dict[str, Any]):
        return {"status": "queued", "student_id": student_id}
