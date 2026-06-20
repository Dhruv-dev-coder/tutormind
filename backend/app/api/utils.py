from typing import Any, Dict

from bson import ObjectId
from bson.errors import InvalidId


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

