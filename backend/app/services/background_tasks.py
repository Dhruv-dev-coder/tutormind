"""Background task helpers (examples).

These show how agents might enqueue scheduled tasks (email reminders, weekly
reports). In production, hook these into a task queue or scheduler.
"""
from datetime import datetime
from typing import Dict, Any
from app.services.email_service import EmailService
from app.services.notification_service import NotificationService


email_svc = EmailService()
notif_svc = NotificationService()


async def send_weekly_report_task(student_id: str, report: Dict[str, Any]):
    # example task to send weekly report via email and in-app notification
    await email_svc.send_weekly_report(student_id, report)
    await notif_svc.send_push(student_id, "Weekly Report", report.get('summary', 'Your weekly summary is ready'))


async def send_exam_reminder_task(student_id: str, exam_info: Dict[str, Any]):
    await email_svc.send_exam_alert(student_id, exam_info)
    await notif_svc.send_push(student_id, f"Exam: {exam_info.get('subject')}", f"Exam scheduled for {exam_info.get('date')}")
