from fastapi import APIRouter, Body
from typing import Dict, Any
from app.agents.teaching_agent import TeachingAgent
from app.api.utils import student_selector
from app.database import db

router = APIRouter()
teaching = TeachingAgent()


@router.post('/teach')
async def teach(payload: Dict[str, Any] = Body(...)):
    """Teach a concept to a student.

    Expected payload: { student_id, topic, level }
    """
    student_id = payload.get('student_id')
    topic = payload.get('topic')
    level = payload.get('level', 'beginner')

    if not student_id:
        return {"status": "error", "detail": "student_id required"}
    if not topic:
        return {"status": "error", "detail": "topic required"}

    # Retrieve student's roadmap for context
    students = db['students']
    student = await students.find_one(student_selector(student_id))
    roadmap = student.get("roadmap") if student else None

    result = await teaching.teach_concept(student_id, topic, level, roadmap)
    return {"status": "ok", "result": result}
