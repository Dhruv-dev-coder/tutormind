from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import APIRouter, Body, HTTPException, Query

from app.api.utils import student_selector, normalize_topic, topic_query
from app.database import db

router = APIRouter()


def build_structured_notes(topic: str, lesson: Dict[str, Any] = None, notes: Dict[str, Any] = None) -> Dict[str, Any]:
    """Create a consistent notes payload from classroom output or user content."""
    if notes:
        return notes

    lesson = lesson or {}
    explanation = lesson.get("explanation", {})
    objectives = lesson.get("learning_objectives", [])
    key_points = lesson.get("key_points", [])
    examples = lesson.get("examples", [])

    return {
        "title": f"{topic} Study Notes",
        "headings": [
            {
                "heading": "Overview",
                "points": [explanation.get("overview") or f"Introduction to {topic}"],
            },
            {
                "heading": "Definition",
                "points": [explanation.get("definition") or f"Core definition of {topic}"],
            },
            {
                "heading": "Key Points",
                "points": key_points or objectives,
            },
            {
                "heading": "Examples",
                "points": [example.get("problem", "") for example in examples[:3]],
            },
        ],
        "summary": explanation.get("why_important") or f"Review {topic} with examples and practice questions.",
    }


@router.post("/save")
async def save_notes(payload: Dict[str, Any] = Body(...)):
    student_id = payload.get("student_id")
    topic = normalize_topic(payload.get("topic") or "")

    if not student_id:
        raise HTTPException(status_code=400, detail="student_id required")
    if not topic:
        raise HTTPException(status_code=400, detail="topic required")

    note_doc = {
        "student_id": student_id,
        "topic": topic,
        "notes": build_structured_notes(topic, payload.get("lesson"), payload.get("notes")),
        "lesson": payload.get("lesson"),
        "source": payload.get("source", "ai_classroom"),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }

    result = await db["notes"].insert_one(note_doc)
    note_doc["_id"] = str(result.inserted_id)
    return {"status": "ok", "note": note_doc}


@router.get("")
async def get_notes(
    topic: Optional[str] = Query(default=None),
    student_id: Optional[str] = Query(default=None),
):
    query: Dict[str, Any] = {}
    if topic:
        query.update(topic_query(topic))
    if student_id:
        query["student_id"] = student_id

    notes = []
    cursor = db["notes"].find(query).sort("created_at", -1)
    async for note in cursor:
        note["_id"] = str(note["_id"])
        notes.append(note)

    return {"status": "ok", "notes": notes}

