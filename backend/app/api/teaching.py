from fastapi import APIRouter, Body
from typing import Dict, Any
from app.agents.teaching_agent import TeachingAgent

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

    result = await teaching.teach_concept(student_id, topic, level)
    return {"status": "ok", "result": result}
