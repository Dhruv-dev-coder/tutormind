"""Revision Agent (LangGraph).

Schedules revisions and implements spaced repetition; generates flashcards.
Uses Calendar and Notification MCPs for scheduling and reminders.
"""
from datetime import datetime
from typing import Dict, Any, List
from app.mcp import get_calendar_mcp, get_notification_mcp
from app.agents.learning_intelligence import next_revision_dates, topic_title


class RevisionAgent:
    def __init__(self, calendar_mcp=None, notification_mcp=None):
        self.calendar = calendar_mcp or get_calendar_mcp()
        self.notification = notification_mcp or get_notification_mcp()

    async def schedule_revision(self, student_id: str, topic: str, when: str) -> Dict[str, Any]:
        scheduled = await self.calendar.schedule_revision(student_id, topic, when)
        notification = await self.notification.schedule_notification(
            student_id,
            when,
            {
                "type": "revision_reminder",
                "title": f"Revise {topic_title(topic)}",
                "message": "Your spaced revision is due today.",
                "topic": topic,
            },
        )
        return {"calendar": scheduled, "notification": notification}

    async def create_spaced_revision_plan(self, student_id: str, topic: str, start_date: str = None) -> Dict[str, Any]:
        base = self._parse_start_date(start_date)
        dates = next_revision_dates(base)
        sessions = []
        for index, date in enumerate(dates):
            result = await self.schedule_revision(student_id, topic, date)
            sessions.append({
                "session": index + 1,
                "date": date,
                "focus": self._session_focus(index),
                "status": result,
            })
        return {
            "student_id": student_id,
            "topic": topic,
            "strategy": "spaced_repetition",
            "created_at": datetime.utcnow().isoformat(),
            "sessions": sessions,
        }

    async def generate_flashcards(self, topic: str, count: int = 10) -> List[Dict[str, Any]]:
        title = topic_title(topic)
        templates = [
            ("Definition", f"What is the core definition of {title}?", f"{title} is the concept, rule, or method used to solve this type of problem."),
            ("Recognition", f"What clue tells you a question is about {title}?", "Look for the keywords, quantities, or relationships that match the core rule."),
            ("Method", f"What is the first step in a {title} problem?", "Write the given information and identify what the question asks for."),
            ("Mistake", f"What common mistake should you avoid in {title}?", "Do not apply a formula or rule before checking whether its assumptions fit."),
            ("Check", f"How do you verify a {title} answer?", "Check units, signs, assumptions, and whether the result answers the exact question."),
        ]
        cards = []
        for i in range(count):
            card_type, question, answer = templates[i % len(templates)]
            cards.append({
                "id": f"fc_{i+1}",
                "type": card_type,
                "q": question,
                "a": answer,
                "difficulty": 1 + (i % 3),
            })
        return cards

    def _parse_start_date(self, start_date: str = None) -> datetime:
        if not start_date:
            return datetime.utcnow()
        try:
            return datetime.fromisoformat(start_date)
        except ValueError:
            return datetime.utcnow()

    def _session_focus(self, index: int) -> str:
        return [
            "Recall definitions and formulas",
            "Solve two guided problems",
            "Attempt mixed practice without notes",
            "Review errors and make flashcards",
            "Complete exam-style timed practice",
        ][min(index, 4)]
