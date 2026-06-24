from typing import Any, Dict
import re

from bson import ObjectId
from bson.errors import InvalidId


def normalize_topic(topic: str) -> str:
    """Normalize topic strings for consistent storage and lookup."""
    if not topic:
        return ""
    cleaned = re.sub(r"[\t\n\r]+", " ", str(topic))
    return re.sub(r"\s+", " ", cleaned).strip()


def topic_query(topic: str) -> Dict[str, Any]:
    """Build a MongoDB query for flexible topic matching."""
    normalized = normalize_topic(topic)
    if not normalized:
        return {}
    # Match regardless of tabs vs spaces in stored topics
    parts = [re.escape(part) for part in re.split(r"\s+", normalized) if part]
    if not parts:
        return {}
    pattern = r"\s*".join(parts)
    return {
        "$or": [
            {"topic": normalized},
            {"topic": {"$regex": pattern, "$options": "i"}},
        ]
    }


def student_selector(student_id: str) -> Dict[str, Any]:
    """Build a Mongo selector for backend student ids or Firebase uids."""
    if not student_id:
        return {}
    if student_id.startswith("_"):
        return {"firebase_uid": student_id}
    try:
        return {"_id": ObjectId(student_id)}
    except (InvalidId, TypeError):
        return {"firebase_uid": student_id}

