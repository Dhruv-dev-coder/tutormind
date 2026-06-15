"""High-level email service that uses the Email MCP client.

This service centralizes template generation and sends emails via the MCP.
"""
from typing import Dict, Any
from app.mcp import get_email_mcp


class EmailService:
    def __init__(self, email_mcp=None):
        self.email_mcp = email_mcp or get_email_mcp()

    async def send_exam_alert(self, student_id: str, exam_info: Dict[str, Any]):
        subject = f"Upcoming exam: {exam_info.get('subject')}"
        body = f"You have an exam for {exam_info.get('subject')} on {exam_info.get('date')}"
        return await self.email_mcp.send_exam_alert(student_id, {"subject": subject, "body": body, **exam_info})

    async def send_weekly_report(self, student_id: str, report: Dict[str, Any]):
        subject = "Your weekly TutorMind report"
        body = f"Weekly summary: {report.get('summary', '')}"
        return await self.email_mcp.send_weekly_report(student_id, {"subject": subject, "body": body, **report})

    async def send_generic(self, student_id: str, subject: str, body: str, metadata: Dict[str, Any] = None):
        return await self.email_mcp.send_reminder_email(student_id, subject, body, metadata=metadata or {})
