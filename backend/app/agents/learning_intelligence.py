"""Shared deterministic learning intelligence for TutorMind agents.

The helpers in this module keep agent behavior consistent without calling
external services directly. Tool-facing work still belongs in MCP clients.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Iterable, List, Sequence


DIFFICULTY_ORDER = {"beginner": 1, "easy": 1, "medium": 2, "intermediate": 2, "hard": 3, "advanced": 3}


def normalize_level(level: str | None, default: str = "beginner") -> str:
    value = (level or default).strip().lower()
    aliases = {"easy": "beginner", "medium": "intermediate", "hard": "advanced"}
    return aliases.get(value, value if value in {"beginner", "intermediate", "advanced"} else default)


def normalize_difficulty(difficulty: str | None, default: str = "medium") -> str:
    value = (difficulty or default).strip().lower()
    return value if value in {"easy", "medium", "hard"} else default


def split_topic(topic: str | None) -> List[str]:
    raw = (topic or "").replace("_", " ").replace("-", " ").strip()
    return [part for part in raw.split() if part]


def topic_title(topic: str | None) -> str:
    words = split_topic(topic)
    return " ".join(word.capitalize() for word in words) if words else "General Study"


def roadmap_topics(roadmap: Dict[str, Any] | None) -> List[str]:
    if not roadmap:
        return []

    topics: List[str] = []
    for chapter in roadmap.get("chapters", []) or []:
        name = chapter.get("name")
        if name:
            topics.append(str(name))
        for topic in chapter.get("topics", []) or []:
            topics.append(str(topic))

    for daily in roadmap.get("daily_plan", []) or []:
        focus = daily.get("focus")
        if focus:
            topics.append(str(focus))

    return dedupe_keep_order(topics)


def dedupe_keep_order(items: Iterable[str]) -> List[str]:
    seen = set()
    unique = []
    for item in items:
        key = item.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        unique.append(item.strip())
    return unique


def infer_learning_objectives(topic: str, level: str) -> List[str]:
    title = topic_title(topic)
    base = [
        f"Define {title} accurately",
        f"Recognize when {title} applies in a problem",
        f"Solve a guided {title} question",
    ]
    if normalize_level(level) == "intermediate":
        base.extend([f"Compare common methods for {title}", f"Explain mistakes students make in {title}"])
    elif normalize_level(level) == "advanced":
        base.extend([f"Solve multi-step {title} problems", f"Justify solution choices under exam constraints"])
    return base


def build_lesson_path(topic: str, level: str) -> List[Dict[str, Any]]:
    title = topic_title(topic)
    level = normalize_level(level)
    steps = [
        ("Warm up", f"Recall prerequisite ideas connected to {title}.", 5),
        ("Concept", f"Build the core definition and intuition for {title}.", 12),
        ("Worked example", f"Solve one representative {title} problem step by step.", 15),
        ("Practice", f"Attempt focused questions and compare reasoning.", 10),
        ("Reflection", f"Summarize the rule, exception, and next action for {title}.", 3),
    ]
    if level == "advanced":
        steps.insert(3, ("Exam variation", f"Handle a tricky or combined {title} prompt.", 12))
    return [{"stage": name, "activity": activity, "minutes": minutes} for name, activity, minutes in steps]


def mastery_band(score: float) -> str:
    if score >= 85:
        return "mastered"
    if score >= 70:
        return "strong"
    if score >= 50:
        return "developing"
    if score > 0:
        return "weak"
    return "unknown"


def readiness_band(score: float) -> str:
    if score >= 80:
        return "exam-ready"
    if score >= 60:
        return "near-ready"
    if score >= 40:
        return "needs-focused-revision"
    return "at-risk"


def weighted_score(events: Sequence[Dict[str, Any]]) -> float:
    if not events:
        return 0.0
    total_weight = 0.0
    weighted_total = 0.0
    for index, event in enumerate(events):
        percentage = float(event.get("percentage", event.get("score", event.get("accuracy", 0))) or 0)
        recency_weight = 1 + (index / max(len(events), 1))
        effort_weight = 1 + min(float(event.get("time_spent_minutes", 0) or 0) / 120, 1)
        weight = recency_weight * effort_weight
        weighted_total += percentage * weight
        total_weight += weight
    return round(weighted_total / total_weight, 2) if total_weight else 0.0


def next_revision_dates(start: datetime | None = None, intervals: Sequence[int] | None = None) -> List[str]:
    base = start or datetime.utcnow()
    days = intervals or (1, 3, 7, 14, 30)
    return [(base + timedelta(days=day)).strftime("%Y-%m-%d") for day in days]


def schedule_load_score(daily_minutes: float, weak_topic_count: int, days_until_exam: int | None = None) -> int:
    score = 0
    if daily_minutes > 180:
        score += 35
    elif daily_minutes > 120:
        score += 20
    if weak_topic_count >= 5:
        score += 25
    elif weak_topic_count >= 3:
        score += 15
    if days_until_exam is not None and days_until_exam <= 14:
        score += 20
    return min(score, 100)

