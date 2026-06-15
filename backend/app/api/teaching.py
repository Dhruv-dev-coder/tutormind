from fastapi import APIRouter, Body
from typing import Dict, Any
from app.agents.teaching_agent import TeachingAgent
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

    # Retrieve student's roadmap for context
    students = db['students']
    student = await students.find_one({"firebase_uid": student_id}) if not student_id.startswith('_') else await students.find_one({"_id": student_id})
    roadmap = student.get("roadmap") if student else None

    result = await teaching.teach_concept(student_id, topic, level, roadmap)
    return {"status": "ok", "result": result}
