from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, Body, HTTPException

from app.agents.teaching_agent import TeachingAgent
from app.api.notes import build_structured_notes
from app.api.utils import student_selector, normalize_topic
from app.database import db

router = APIRouter()
teaching = TeachingAgent()


@router.post("/generate")
async def generate_classroom_session(payload: Dict[str, Any] = Body(...)):
    student_id = payload.get("student_id")
    topic = normalize_topic(payload.get("topic") or "")
    level = payload.get("level", "beginner")

    if not student_id:
        raise HTTPException(status_code=400, detail="student_id required")
    if not topic:
        raise HTTPException(status_code=400, detail="topic required")

    student = await db["students"].find_one(student_selector(student_id))
    roadmap = student.get("roadmap") if student else None
    lesson = await teaching.teach_concept(student_id, topic, level, roadmap)

    prompt = f"Teach me {topic} in a structured way based on my learning roadmap and current level."
    session_doc = {
        "student_id": student_id,
        "topic": topic,
        "level": level,
        "prompt": prompt,
        "lesson": lesson,
        "created_at": datetime.utcnow().isoformat(),
    }
    session_result = await db["classroom_sessions"].insert_one(session_doc)

    note_doc = {
        "student_id": student_id,
        "topic": topic,
        "notes": build_structured_notes(topic, lesson),
        "lesson": lesson,
        "source": "ai_classroom",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    note_result = await db["notes"].insert_one(note_doc)

    session_doc["_id"] = str(session_result.inserted_id)
    note_doc["_id"] = str(note_result.inserted_id)

    return {
        "status": "ok",
        "prompt": prompt,
        "session": session_doc,
        "lesson": lesson,
        "notes": note_doc,
    }

