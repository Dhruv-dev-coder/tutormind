"""Progress Tracking Agent (LangGraph).

Tracks progress, detects weak/strong topics and updates mastery scores.
Should call Analytics MCP for heavy analysis.
"""
from datetime import datetime
from typing import Dict, Any, List
from app.mcp import get_analytics_mcp
from app.agents.learning_intelligence import mastery_band, weighted_score


class ProgressAgent:
    def __init__(self, analytics_mcp=None):
        self.analytics = analytics_mcp or get_analytics_mcp()

    async def update_progress(self, student_id: str, event: Dict[str, Any]) -> Dict[str, Any]:
        """Transform a learning event into mastery deltas.

        Persistence and historical analysis should happen behind Analytics MCP;
        this agent returns the decision payload that callers can store.
        """
        event_type = event.get("type", "learning_event")
        topic_results = self._extract_topic_results(event)
        mastery_updates = []

        for topic, events in topic_results.items():
            score = weighted_score(events)
            mastery_updates.append({
                "topic": topic,
                "score": score,
                "mastery_band": mastery_band(score),
                "recommended_action": self._recommend_action(score),
            })

        return {
            "status": "updated",
            "student_id": student_id,
            "event_type": event_type,
            "updated_at": datetime.utcnow().isoformat(),
            "mastery_updates": mastery_updates,
            "next_focus": [item["topic"] for item in mastery_updates if item["mastery_band"] in {"weak", "developing"}][:3],
        }

    async def detect_weak_topics(self, student_id: str) -> Dict[str, Any]:
        return await self.analytics.detect_weak_topics(student_id)

    async def calculate_mastery(self, student_id: str) -> Dict[str, Any]:
        performance = await self.analytics.analyze_performance(student_id)
        summary = performance.get("summary", {})
        accuracy = float(summary.get("accuracy", 0) or 0)
        return {
            **performance,
            "mastery_band": mastery_band(accuracy),
            "recommended_action": self._recommend_action(accuracy),
        }

    def _extract_topic_results(self, event: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        details = event.get("details") or event.get("answers") or []
        topic_results: Dict[str, List[Dict[str, Any]]] = {}

        if details:
            for item in details:
                topic = item.get("topic") or item.get("subject") or event.get("topic") or "General"
                if "marks_obtained" in item and "total_marks" in item and item.get("total_marks"):
                    percentage = item["marks_obtained"] / item["total_marks"] * 100
                elif "is_correct" in item:
                    percentage = 100 if item["is_correct"] else 0
                else:
                    percentage = item.get("percentage", event.get("percentage", 0))
                topic_results.setdefault(topic, []).append({"percentage": percentage})
            return topic_results

        topic = event.get("topic") or event.get("subject") or "General"
        topic_results[topic] = [{
            "percentage": event.get("percentage", event.get("score", event.get("accuracy", 0))),
            "time_spent_minutes": event.get("time_spent_minutes", 0),
        }]
        return topic_results

    def _recommend_action(self, score: float) -> str:
        if score >= 85:
            return "move_to_advanced_practice"
        if score >= 70:
            return "maintain_with_spaced_revision"
        if score >= 50:
            return "schedule_targeted_practice"
        if score > 0:
            return "reteach_foundations"
        return "collect_more_evidence"
