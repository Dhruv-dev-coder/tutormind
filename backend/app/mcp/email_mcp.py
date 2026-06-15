import os
import smtplib
from typing import Optional, Dict, Any
from email.message import EmailMessage
import requests


class EmailMCP:
    """Production-ready Email MCP supporting SMTP or SendGrid.

    Environment variables:
      - EMAIL_PROVIDER: 'smtp' (default) or 'sendgrid'
      - SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS
      - SENDGRID_API_KEY
      - EMAIL_FROM
    """

    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or os.environ.get("EMAIL_PROVIDER", "smtp")
        if self.provider == "sendgrid":
            self.api_key = os.environ.get("SENDGRID_API_KEY")
        else:
            self.smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
            self.smtp_port = int(os.environ.get("SMTP_PORT", 587))
            self.smtp_user = os.environ.get("SMTP_USER")
            self.smtp_pass = os.environ.get("SMTP_PASS")

    def send_email(self, to: str, subject: str, body: str, html: Optional[str] = None, from_email: Optional[str] = None):
        from_email = from_email or os.environ.get("EMAIL_FROM", "no-reply@tutormind.local")
        if self.provider == "sendgrid":
            return self._send_sendgrid(from_email, to, subject, body, html)
        return self._send_smtp(from_email, to, subject, body, html)

    def _send_smtp(self, from_email: str, to: str, subject: str, body: str, html: Optional[str] = None):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to
        if html:
            msg.set_content(body)
            msg.add_alternative(html, subtype="html")
        else:
            msg.set_content(body)

        with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=30) as server:
            server.starttls()
            if self.smtp_user and self.smtp_pass:
                server.login(self.smtp_user, self.smtp_pass)
            server.send_message(msg)

        return {"ok": True}

    def _send_sendgrid(self, from_email: str, to: str, subject: str, body: str, html: Optional[str] = None):
        if not getattr(self, "api_key", None):
            raise RuntimeError("SENDGRID_API_KEY not configured")
        url = "https://api.sendgrid.com/v3/mail/send"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "personalizations": [{"to": [{"email": to}]}],
            "from": {"email": from_email},
            "subject": subject,
            "content": [{"type": "text/plain", "value": body}],
        }
        if html:
            payload["content"] = [{"type": "text/html", "value": html}]

        r = requests.post(url, json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        return {"ok": True, "status_code": r.status_code}

    # Async interface for agent compatibility
    async def send_reminder_email(self, student_id: str, subject: str, body: str, metadata: Dict[str, Any] = None):
        """Send reminder email to student (async wrapper)."""
        try:
            email = metadata.get("email") if metadata else None
            if not email:
                return {"status": "error", "reason": "email address not provided"}
            self.send_email(to=email, subject=subject, body=body)
            return {"status": "sent", "student_id": student_id, "subject": subject}
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    async def send_exam_alert(self, student_id: str, exam_info: Dict[str, Any]):
        """Send exam alert email (async wrapper)."""
        try:
            email = exam_info.get("email") if exam_info else None
            if not email:
                return {"status": "error", "reason": "email address not provided"}
            subject = f"Exam Alert: {exam_info.get('exam_name', 'Upcoming Exam')}"
            body = f"Exam: {exam_info.get('exam_name')}\nDate: {exam_info.get('date')}\nTime: {exam_info.get('time')}"
            self.send_email(to=email, subject=subject, body=body)
            return {"status": "sent", "student_id": student_id}
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    async def send_weekly_report(self, student_id: str, report: Dict[str, Any]):
        """Send weekly report email (async wrapper)."""
        try:
            email = report.get("email") if report else None
            if not email:
                return {"status": "error", "reason": "email address not provided"}
            subject = "Weekly Learning Report"
            body = f"Report for week: {report.get('week')}\nProgress: {report.get('progress')}"
            self.send_email(to=email, subject=subject, body=body)
            return {"status": "sent", "student_id": student_id}
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    async def send_revision_notification(self, student_id: str, revision_info: Dict[str, Any]):
        """Send revision notification email (async wrapper)."""
        try:
            email = revision_info.get("email") if revision_info else None
            if not email:
                return {"status": "error", "reason": "email address not provided"}
            subject = "Revision Reminder"
            body = f"Topics to revise: {revision_info.get('topics')}"
            self.send_email(to=email, subject=subject, body=body)
            return {"status": "sent", "student_id": student_id}
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    async def send_achievement_email(self, student_id: str, achievement: Dict[str, Any]):
        """Send achievement email (async wrapper)."""
        try:
            email = achievement.get("email") if achievement else None
            if not email:
                return {"status": "error", "reason": "email address not provided"}
            subject = f"Achievement Unlocked: {achievement.get('title')}"
            body = f"Congratulations! You achieved: {achievement.get('title')}\n{achievement.get('description')}"
            self.send_email(to=email, subject=subject, body=body)
            return {"status": "sent", "student_id": student_id}
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    async def health_check(self) -> Dict[str, Any]:
        """Check if email service is healthy."""
        try:
            if self.provider == "sendgrid":
                if not getattr(self, "api_key", None):
                    return {"status": "unhealthy", "reason": "SENDGRID_API_KEY not configured"}
                return {"status": "healthy", "provider": "sendgrid", "configured": True}
            else:
                if not self.smtp_user or not self.smtp_pass:
                    return {"status": "unhealthy", "reason": "SMTP credentials not configured"}
                return {"status": "healthy", "provider": "smtp", "host": self.smtp_host, "port": self.smtp_port}
        except Exception as e:
            return {"status": "unhealthy", "reason": str(e)}
