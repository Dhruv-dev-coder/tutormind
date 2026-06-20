"""AI Mentor Agent (LangGraph).

Monitors activity, detects burnout/inactivity and triggers motivational
messages and email/notification alerts via MCP.
"""
from datetime import datetime
from typing import Dict, Any
from app.mcp import get_email_mcp, get_notification_mcp, get_analytics_mcp
from app.agents.learning_intelligence import schedule_load_score


class MentorAgent:
    def __init__(self, email_mcp=None, notification_mcp=None, analytics_mcp=None):
        self.email = email_mcp or get_email_mcp()
        self.notification = notification_mcp or get_notification_mcp()
        self.analytics = analytics_mcp or get_analytics_mcp()

    async def monitor_activity(self, student_id: str, activity: Dict[str, Any] = None) -> Dict[str, Any]:
        activity = activity or {}
        analytics = await self.analytics.analyze_performance(student_id, window_days=7)
        missed_goals = int(activity.get("missed_goals", 0) or 0)
        inactive_days = int(activity.get("inactive_days", 0) or 0)
        due_revisions = activity.get("due_revisions", []) or []
        active = inactive_days < 2 and missed_goals < 2
        interventions = self._build_interventions(missed_goals, inactive_days, due_revisions)

        sent = []
        for intervention in interventions:
            if intervention["channel"] == "notification":
                sent.append(await self.notification.send_push_notification(
                    student_id,
                    intervention["title"],
                    intervention["message"],
                    {"type": intervention["type"]},
                ))
            elif intervention["channel"] == "email":
                sent.append(await self.trigger_email_alerts(student_id, intervention["type"], {**activity, **intervention}))

        return {
            "student_id": student_id,
            "active": active,
            "checked_at": datetime.utcnow().isoformat(),
            "analytics": analytics,
            "signals": {
                "missed_goals": missed_goals,
                "inactive_days": inactive_days,
                "due_revision_count": len(due_revisions),
            },
            "interventions": interventions,
            "delivery_results": sent,
        }

    async def detect_burnout(self, student_id: str, workload: Dict[str, Any] = None) -> Dict[str, Any]:
        workload = workload or {}
        score = schedule_load_score(
            float(workload.get("daily_minutes", 0) or 0),
            int(workload.get("weak_topic_count", 0) or 0),
            workload.get("days_until_exam"),
        )
        burnout = score >= 60
        return {
            "student_id": student_id,
            "burnout": burnout,
            "risk_score": score,
            "checked_at": datetime.utcnow().isoformat(),
            "recommendations": self._burnout_recommendations(score),
        }

    async def send_motivation(self, student_id: str, message: str) -> Dict[str, Any]:
        await self.notification.send_push_notification(student_id, "Keep Going", message)
        return {"status": "sent"}

    async def trigger_email_alerts(self, student_id: str, alert_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if alert_type == "exam_alert":
            return await self.email.send_exam_alert(student_id, payload)
        if alert_type == "revision_due":
            return await self.email.send_revision_notification(student_id, payload)
        if alert_type == "achievement":
            return await self.email.send_achievement_email(student_id, payload)
        if alert_type in {"missed_goal", "inactive"}:
            return await self.email.send_reminder_email(
                student_id,
                payload.get("title", "TutorMind Reminder"),
                payload.get("message", "A quick check-in from TutorMind."),
                payload,
            )
        return await self.email.send_weekly_report(student_id, payload)

    def _build_interventions(self, missed_goals: int, inactive_days: int, due_revisions: list) -> list:
        interventions = []
        if inactive_days >= 3:
            interventions.append({
                "type": "inactive",
                "channel": "email",
                "title": "Let's restart with one small session",
                "message": "You have been away for a few days. Start with a 15-minute review to rebuild momentum.",
            })
        elif inactive_days >= 1:
            interventions.append({
                "type": "inactive",
                "channel": "notification",
                "title": "Quick study check-in",
                "message": "A short session today keeps your plan warm.",
            })

        if missed_goals >= 2:
            interventions.append({
                "type": "missed_goal",
                "channel": "email",
                "title": "Adjusting your study target",
                "message": "You missed recent goals, so reduce today's target and finish one high-priority topic.",
            })

        if due_revisions:
            interventions.append({
                "type": "revision_due",
                "channel": "notification",
                "title": "Revision due",
                "message": f"Revise {len(due_revisions)} scheduled topic(s) today.",
                "topics": due_revisions,
            })
        return interventions

    def _burnout_recommendations(self, score: int) -> list:
        if score >= 80:
            return ["Reduce daily load by 30 percent", "Replace one hard session with light revision", "Schedule a mentor check-in"]
        if score >= 60:
            return ["Alternate hard and easy topics", "Add breaks between timed sessions", "Move one non-urgent goal to tomorrow"]
        if score >= 30:
            return ["Keep the plan, but watch missed goals", "Use shorter review blocks for weak topics"]
        return ["Workload looks sustainable"]
